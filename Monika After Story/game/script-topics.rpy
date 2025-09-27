#This file contains all of monika's topics she can talk about
#Each entry should start with a database entry, including the appropriate flags
#to either be a random topic, a prompt "pool" topics, or a special conditional
#or date-dependent event with an appropriate actiona

define monika_random_topics = []
define mas_rev_unseen = []
define mas_rev_seen = []
define mas_rev_mostseen = []
define testitem = 0
define mas_did_monika_battery = False
define mas_sensitive_limit = 3

init -2 python in mas_topics:
    # CONSTANTS
    # most / top weights
    # MOST seen is the percentage of seen topics
    # think of this as x % of the collection
    S_MOST_SEEN = 0.1

    # TOP seen is the percentage of the most seen
    # Think of this as ilke the upper x percentile
    S_TOP_SEEN = 0.2

    # limit to how many top seen until we move to most seen alg
    S_TOP_LIMIT = 0.3

    # selection weights (out of 100)
    UNSEEN = 50
    SEEN = UNSEEN + 49
    MOST_SEEN = SEEN + 1

    def topSeenEvents(sorted_ev_list, shown_count):
        """
        counts the number of events with a > shown_count than the given
        shown_count

        IN:
            sorted_ev_list - an event list sorted by shown_counts
            shown_count - shown_count to compare to

        RETURNS:
            number of events with shown_counts that are higher than the given
            shown_count
        """
        index = len(sorted_ev_list) - 1
        ev_count = 0
        while index >= 0 and sorted_ev_list[index].shown_count > shown_count:
            ev_count += 1
            index -= 1
        
        return ev_count

# we are going to define removing seen topics as a function,
# as we need to call it dynamically upon import
init -1 python:
    import random
    random.seed()

    import store.songs as songs
    import store.evhand as evhand

    mas_events_built = False
    # set to True once we have built events

    def remove_seen_labels(pool):
        #
        # Removes seen labels from the given pool
        #
        # IN:
        #   pool - a list of labels to check for seen
        #
        # OUT:
        #   pool - list of unseen labels (may be empty)
        for index in range(len(pool)-1, -1, -1):
            if renpy.seen_label(pool[index]):
                pool.pop(index)


    def mas_randomSelectAndRemove(sel_list):
        """
        Randomly selects an element from the given list
        This also removes the element from that list.

        IN:
            sel_list - list to select from

        RETURNS:
            selected element
        """
        endpoint = len(sel_list) - 1
        
        if endpoint < 0:
            return None
        
        # otherwise we have at least 1 element
        return sel_list.pop(random.randint(0, endpoint))


    def mas_randomSelectAndPush(sel_list):
        """
        Randomly selects an element from the the given list and pushes the event
        This also removes the element from that list.

        NOTE: this does sensitivy checks

        IN:
            sel_list - list to select from
        """
        sel_ev = True
        while sel_ev is not None:
            sel_ev = mas_randomSelectAndRemove(sel_list)
            
            if (
                    # valid event
                    sel_ev

                    # event not blocked from random selection
                    and not sel_ev.anyflags(EV_FLAG_HFRS)
            ):
                MASEventList.push(sel_ev.eventlabel, notify=True)
                return


    def mas_insertSort(sort_list, item, key):
        """
        Performs a round of insertion sort.
        This does least to greatest sorting

        IN:
            sort_list - list to insert + sort
            item - item to sort and insert
            key - function to call using the given item to retrieve sort key

        OUT:
            sort_list - list with 1 additonal element, sorted
        """
        store.mas_utils.insert_sort(sort_list, item, key)


    def mas_splitSeenEvents(sorted_seen):
        """
        Splits the seen_list into seena nd most seen

        IN:
            sorted_seen - list of seen events, sorted by shown_count

        RETURNS:
            tuple of thef ollowing format:
            [0] - seen list of events
            [1] - most seen list of events
        """
        ss_len = len(sorted_seen)
        if ss_len == 0:
            return ([], [])
        
        # now calculate the most / top seen counts
        most_count = int(ss_len * store.mas_topics.S_MOST_SEEN)
        top_count = store.mas_topics.topSeenEvents(
            sorted_seen,
            int(
                sorted_seen[ss_len - 1].shown_count
                * (1 - store.mas_topics.S_TOP_SEEN)
            )
        )
        
        # now decide how to do the split
        if top_count < ss_len * store.mas_topics.S_TOP_LIMIT:
            # we want to prioritize top count unless its over a certain
            # percentage of the topics
            split_point = top_count * -1
        
        else:
            # otherwise, we use the most count, which is certainly smaller
            split_point = most_count * -1
        
        # and then do the split
        return (sorted_seen[:split_point], sorted_seen[split_point:])


    def mas_splitRandomEvents(events_dict):
        """
        Splits the given random events dict into 2 lists of events
        NOTE: cleans the seen list

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events, sorted by shown_count

        """
        # split these into 2 lists
        unseen = list()
        seen = list()
        for k in events_dict:
            ev = events_dict[k]
            
            if renpy.seen_label(k) and not "force repeat" in ev.rules:
                # seen event
                mas_insertSort(seen, ev, Event.getSortShownCount)
            
            else:
                # unseen event
                unseen.append(ev)
        
        # clean the seen_topics list
        seen = mas_cleanJustSeenEV(seen)
        
        return (unseen, seen)


    def mas_buildEventLists():
        """
        Builds the unseen / most seen / seen event lists

        RETURNS:
            tuple of the following format:
            [0] - unseen list of events
            [1] - seen list of events
            [2] - most seen list of events

        ASSUMES:
            evhand.event_database
            mas_events_built
        """
        global mas_events_built
        
        # retrieve all randoms
        all_random_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            aff=mas_curr_affection
        )
        
        # split randoms into unseen and sorted seen events
        unseen, sorted_seen = mas_splitRandomEvents(all_random_topics)
        
        # split seen into regular seen and the most seen events
        seen, mostseen = mas_splitSeenEvents(sorted_seen)
        
        mas_events_built = True
        return (unseen, seen, mostseen)


    def mas_buildSeenEventLists():
        """
        Builds the seen / most seen event lists

        RETURNS:
            tuple of the following format:
            [0] - seen list of events
            [1] - most seen list of events

        ASSUMES:
            evhand.event_database
        """
        # retrieve all seen (values list)
        all_seen_topics = Event.filterEvents(
            evhand.event_database,
            random=True,
            seen=True,
            aff=mas_curr_affection
        ).values()
        
        # clean the seen topics from early repeats
        cleaned_seen = mas_cleanJustSeenEV(all_seen_topics)
        
        # sort the seen by shown_count
        cleaned_seen.sort(key=Event.getSortShownCount)
        
        # split the seen into regular seen and most seen
        return mas_splitSeenEvents(cleaned_seen)


    def mas_rebuildEventLists():
        """
        Rebuilds the unseen, seen and most seen event lists.

        ASSUMES:
            mas_rev_unseen - unseen list
            mas_rev_seen - seen list
            mas_rev_mostseen - most seen list
        """
        global mas_rev_unseen, mas_rev_seen, mas_rev_mostseen
        mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()


    # EXCEPTION CLass incase of bad labels
    class MASTopicLabelException(Exception):
        def __init__(self, msg):
            self.msg = msg
        def __str__(self):
            return "MASTopicLabelException: " + self.msg

init 11 python:
    # sort out the seen / most seen / unseen
    mas_rev_unseen = []
    mas_rev_seen = []
    mas_rev_mostseen = []
#    mas_rev_unseen, mas_rev_seen, mas_rev_mostseen = mas_buildEventLists()

    # for compatiblity purposes:
#    monika_random_topics = all_random_topics

    #Remove all previously seen random topics.
        #remove_seen_labels(monika_random_topics)
#    monika_random_topics = [
#        evlabel for evlabel in all_random_topics
#        if not renpy.seen_label(evlabel)
#    ]

    #If there are no unseen topics, you can repeat seen ones
#    if len(monika_random_topics) == 0:
#        monika_random_topics=list(all_random_topics)

# Bookmarks and derandom stuff
default persistent._mas_player_bookmarked = list()
# list to store bookmarked events
default persistent._mas_player_derandomed = list()
# list to store player derandomed events
default persistent.flagged_monikatopic = None
# var set when we flag a topic for derandom

init python:
    def mas_derandom_topic(ev_label=None):
        """
        Function for the derandom hotkey, 'x'

        IN:
            ev_label - label of the event we want to derandom.
                (Optional. If None, persistent.current_monikatopic is used)
                (Default: None)
        """
        #Let's just shorthand this for use later
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        #Get the label prefix
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        #CRITERIA:
        #1. Must have an ev
        #2. Must be a topic which is random
        #3. Must be a valid label (in the label prefix map)
        #4. Prompt must not be the same as the eventlabel (event must have a prompt)
        if (
            ev.random
            and label_prefix
            and ev.prompt != ev_label
        ):
            #Now we do a bit of var setup to clean up the following work     
            derand_flag_add_text = label_prefix_map[label_prefix].get("derand_text", _("Помечено для удаления."))
            derand_flag_remove_text = label_prefix_map[label_prefix].get("underand_text", _("Пометка удалена."))
            
            #Handle custom override derand labels
            push_label = ev.rules.get("derandom_override_label", None)
            
            #If we still have nothing, then we'll use the default, the one for the label prefix
            if not renpy.has_label(push_label):
                push_label = label_prefix_map[label_prefix].get("push_label", "mas_topic_derandom")
            
            if mas_findEVL(push_label) < 0:
                persistent.flagged_monikatopic = ev_label
                MASEventList.push(push_label, skipeval=True)
                renpy.notify(derand_flag_add_text)
            
            else:
                mas_rmEVL(push_label)
                renpy.notify(derand_flag_remove_text)

    def mas_bookmark_topic(ev_label=None):
        """
        Function for the bookmark hotkey, 'b'

        IN:
            ev_label - label of the event we want to bookmark.
                (Optional, defaults to persistent.current_monikatopic)
        """
        #Let's just shorthand this for use later
        label_prefix_map = store.mas_bookmarks_derand.label_prefix_map
        
        if ev_label is None:
            ev_label = persistent.current_monikatopic
        
        ev = mas_getEV(ev_label)
        
        if ev is None:
            return
        
        #Get our label prefix
        label_prefix = store.mas_bookmarks_derand.getLabelPrefix(ev_label)
        
        #CRITERIA:
        #1. Must be normal+
        #2. Must have an ev
        #3. Must be a valid label (in the label prefix map or in the bookmark whitelist)
        #4. Must not be a bookmark blacklisted topic
        #4. Prompt must not be the same as the eventlabel (event must have a prompt)
        if (
            mas_isMoniNormal(higher=True)
            and (label_prefix or ev.rules.get("bookmark_rule") == store.mas_bookmarks_derand.WHITELIST)
            and (ev.rules.get("bookmark_rule") != store.mas_bookmarks_derand.BLACKLIST)
            and ev.prompt != ev_label
        ):
            #If this was only a whitelisted topic, we need to do a bit of extra work
            if not label_prefix:
                bookmark_persist_key = "_mas_player_bookmarked"
                bookmark_add_text = "Добавлена закладка."
                bookmark_remove_text = "Закладка удалена."
            
            else:
                #Now we do some var setup to clean the following
                bookmark_persist_key = label_prefix_map[label_prefix].get("bookmark_persist_key", "_mas_player_bookmarked")
                bookmark_add_text = label_prefix_map[label_prefix].get("bookmark_text", _("Добавлена закладка."))
                bookmark_remove_text = label_prefix_map[label_prefix].get("unbookmark_text", _("Закладка удалена."))
            
            #For safety, we'll initialize this key.
            #NOTE: You should NEVER pass in a non-existent key.
            #While this system handles it, it's not ideal and is bad for documentation
            if bookmark_persist_key not in persistent.__dict__:
                persistent.__dict__[bookmark_persist_key] = list()
            
            #Now create the pointer
            persist_pointer = persistent.__dict__[bookmark_persist_key]
            
            if ev_label not in persist_pointer:
                persist_pointer.append(ev_label)
                renpy.notify(bookmark_add_text)
            
            else:
                persist_pointer.pop(persist_pointer.index(ev_label))
                renpy.notify(bookmark_remove_text)

    def mas_hasBookmarks(persist_var=None):
        """
        Checks to see if we have bookmarks to show

        Bookmarks are restricted to Normal+ affection
        and to topics that are unlocked and are available
        based on current affection

        IN:
            persist_var - appropriate variable holding the bookedmarked eventlabels.
                If None, persistent._mas_player_bookmarked is assumed
                (Default: None)

        OUT:
            boolean:
                True if there are bookmarks in the curent var
                False otherwise
        """
        if mas_isMoniUpset(lower=True):
            return False
        
        elif persist_var is None:
            persist_var = persistent._mas_player_bookmarked
        
        return len(mas_get_player_bookmarks(persist_var)) > 0

#START: UTILITY TOPICS (bookmarks/derand, show/hide unseen)
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="mas_topic_derandom",unlocked=False,rules={"no_unlock":None}))

label mas_topic_derandom:
    #NOTE: since we know the topic in question, it's possible to add dialogue paths for derandoming specific topics
    $ prev_topic = persistent.flagged_monikatopic
    m 3eksdld "Ты уверен, что не хочешь, чтобы я поднимала эту тему{nw}"
    $ _history_list.pop()
    menu:
        m "Ты уверен, что не хочешь, чтобы я поднимала эту тему{fast}"
        
        "Нет, спасибо.":
            $ mas_hideEVL(prev_topic, "EVE", derandom=True)
            $ persistent._mas_player_derandomed.append(prev_topic)
            $ mas_unlockEVL('mas_topic_rerandom', 'EVE')

            m 2eksdlc "Хорошо, [player], я постараюсь не говорить об этом снова."
            m 2dksdld "Если она тебя как-то расстроила, то мне очень жаль...{w=0.5} я бы никогда не сделала это нарочно."
            m 2eksdla "...Но спасибо, что дал мне знать;{w=0.5} я признательна тебе за честность."
        
        "Всё нормально.":
            m 1eka "Хорошо, [player]."
    return

label mas_bad_derand_topic:
    python:
        prev_topic = persistent.flagged_monikatopic

        def derand_flagged_topic():
            """
            Derands the flagged topic
            """
            mas_hideEVL(prev_topic, "EVE", derandom=True)
            persistent._mas_player_derandomed.append(prev_topic)
            mas_unlockEVL('mas_topic_rerandom', 'EVE')

    m 2ekc "...{w=0.3}{nw}"
    extend 2ekd "[player]..."

    if mas_isMoniAff(higher=True):
        m 2efd "Тебе не нравится, что я говорю с тобой о своих страхах?"
        m 2ekc "Я имела ввиду, что если ты не хочешь, то я прекращу...{w=0.3}{nw}"
        extend 2rkd " но я подумала, что ты захочешь меня выслушать."

        m 2esc "Ты хочешь, чтобы я остановилась, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты хочешь, чтобы я остановилась, [player]?{fast}"
            
            "Да, пожалуйста.":
                m 2dkc "Хорошо..."
                #Lose affection
                $ mas_loseAffectionFraction(min_amount=35)
                $ derand_flagged_topic()
            
            "Всё хорошо, я готов выслушать.":
                m 2duu "Спасибо, [player]."
                m 2eua "Эти слова многое для меня значат."

    elif mas_isMoniUpset(higher=True):
        m 2ekd "Ты просто...{w=0.2} не задумываешься о том, что я чувствую или что-то в этом роде?"
        m 2tsc "Если ты хочешь, чтобы я прекратила говорить на эту тему, я перестану... но меня не очень радует то, что ты не хочешь меня выслушать."

        m 2etc "Итак, [player], мне перестать?{nw}"
        $ _history_list.pop()
        menu:
            m "Итак, [player], мне перестать?{fast}"

            "Да, пожалуйста.":
                m 2dsc "Хорошо..."
                $ mas_loseAffectionFraction(min_amount=20)
                $ derand_flagged_topic()

            "Всё в порядке.":
                m 2eka "Спасибо, [player]."
                $ _stil_ = " " if mas_isMoniNormal(higher=True) else "всё ещё "
                m "Я ценю, что ты[_stil_]готов выслушать меня."

    else:
        #No ask here. You're this low, you probably did it on purpose
        $ mas_loseAffectionFraction(min_amount=20)
        m 2rsc "Полагаю, мне не стоит удивляться..."
        m 2tsc "Ты прекрасно дал мне понять, что тебе наплевать на мои чувства."
        m 2dsc "Хорошо, [player]. Я больше не буду об этом говорить."
        $ derand_flagged_topic()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_topic_rerandom",
            category=['ты'],
            prompt="Я не против поговорить о...",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_topic_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "О какой теме ты не против поговорить ещё раз?"
        mas_bookmarks_derand.initial_ask_text_one = "Если ты уверен, что это нормально, чтобы поговорить об этом снова, просто нажми на эту тему, [player]."
        mas_bookmarks_derand.caller_label = "mas_topic_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed

    call mas_rerandom
    return _return

init python in mas_bookmarks_derand:
    import store

    #Rule constants
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

    #Label prefixes and their respective rules
    #The items in the inner dicts act as kwargs to override the default generic values
    #The 'monika_' entry in this dict shows all existing keys
    #Default values are as follows:
    #  - bookmark_text: "Bookmark added."
    #  - unbookmark_text: "Bookmark removed."
    #  - derand_text: "Flagged for removal."
    #  - underand_text: "Flag removed."
    #  - push_label: "mas_topic_derandom" (This is overriden on a per event basis by the 'derandom_push_label' rule)
    #  - bookmark_persist_key: "_mas_player_bookmarked"
    #  - derand_persist_key: "_mas_player_derandomed"
    #  - rerand_evl: None
    label_prefix_map = {
        "monika_": {
            "bookmark_text": _("Тема занесена в закладки."),
            "unbookmark_text": _("Закладка удалена."),
            "derand_text": _("Тема помечена для удаления."),
            "underand_text": _("Пометка темы для удаления удалена."),
            "push_label": "mas_topic_derandom",
            "bookmark_persist_key": "_mas_player_bookmarked",
            "derand_persist_key": "_mas_player_derandomed",
            "rerand_evl": "mas_topic_rerandom"
        },
        "mas_song_": {
            "bookmark_text": _("Песня занесена в закладки."),
            "derand_text": _("Песня помечена для удаления."),
            "underand_text": _("Пометка песни для удаления удалена."),
            "push_label": "mas_song_derandom",
            "derand_persist_key": "_mas_player_derandomed_songs",
            "rerand_evl": "mas_sing_song_rerandom"
        }
    }

    #Vars for mas_rerandom flows
    initial_ask_text_multiple = None
    initial_ask_text_one = None
    caller_label = None
    persist_var = None

    def resetDefaultValues():
        """
        Resets the globals to their default values
        """
        global initial_ask_text_multiple, initial_ask_text_one
        global caller_label, persist_var
        
        initial_ask_text_multiple = None
        initial_ask_text_one = None
        caller_label = None
        persist_var = None
        return

    def getLabelPrefix(test_str):
        """
        Checks if test_str starts with anything in the list of prefixes, and if so, returns the matching prefix

        IN:
            test_str - string to test

        OUT:
            string:
                - label_prefix if test_string starts with a prefix in list_prefixes
                - empty string otherwise
        """
        list_prefixes = label_prefix_map.keys()
        
        for label_prefix in list_prefixes:
            if test_str.startswith(label_prefix):
                return label_prefix
        return ""

    def getDerandomedEVLs():
        """
        Gets a list of derandomed eventlabels

        OUT:
            list of derandomed eventlabels
        """
        #Firstly, let's get our derandom keys
        derand_keys = [
            label_prefix_data["derand_persist_key"]
            for label_prefix_data in label_prefix_map.itervalues()
            if "derand_persist_key" in label_prefix_data
        ]
        
        deranded_evl_list = list()
        
        for derand_key in derand_keys:
            #For safey, we'll .get() this and return an empty list if the key doesn't exist
            derand_list = store.persistent.__dict__.get(derand_key, list())
            
            for evl in derand_list:
                deranded_evl_list.append(evl)
        
        return deranded_evl_list

    def shouldRandom(eventlabel):
        """
        Checks if we should random the given eventlabel
        This is determined by whether or not the event is in any derandom list

        IN:
            eventlabel to check if we should random_seen

        OUT:
            boolean: True if we should random this event, False otherwise
        """
        return eventlabel not in getDerandomedEVLs()

    def wrappedGainAffection(amount=None, modifier=1.0, bypass=False):
        """
        Wrapper function for mas_gainAffection which allows it to be used in event rules at init 5

        See mas_gainAffection for documentation
        """
        store.mas_gainAffection(amount, modifier, bypass)

    def removeDerand(eventlabel):
        """
        Removes a derandomed eventlabel from ALL derandom dbs

        IN:
            eventlabel - Eventlabel to remove
        """
        label_prefix = getLabelPrefix(eventlabel)
        
        label_prefix_data = label_prefix_map.get(label_prefix)
        
        #If we can't get a derand persist key, let's just return here
        if not label_prefix_data or "derand_persist_key" not in label_prefix_data:
            return
        
        #Otherwise, store this and continue
        derand_db_persist_key = label_prefix_data["derand_persist_key"]
        rerand_evl = label_prefix_data.get("rerand_evl")
        
        #Remove the evl from the derandomlist
        if eventlabel in store.persistent.__dict__[derand_db_persist_key]:
            store.persistent.__dict__[derand_db_persist_key].remove(eventlabel)
            
            #And check if we should (and can) lock the rerandom ev if necessary
            if rerand_evl and not store.persistent.__dict__[derand_db_persist_key]:
                store.mas_lockEVL(rerand_evl, "EVE")


##Generic rerandom work label
#IN:
#   initial_ask_text_multiple - Initial question Monika asks if there's multiple items to rerandom
#   initial_ask_text_one - Initial text Monika says if there's only one item to rerandom
#   caller_label - The label that called this label
#   persist_var - The persistent variable which stores the derandomed eventlabels
label mas_rerandom:
    python:
        derandomlist = mas_get_player_derandoms(mas_bookmarks_derand.persist_var)

        derandomlist.sort()

    show monika 1eua at t21
    if len(derandomlist) > 1:
        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_multiple, interact=False)

    else:
        $ renpy.say(m, mas_bookmarks_derand.initial_ask_text_one, interact=False)

    call screen mas_check_scrollable_menu(derandomlist, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Allow selected")

    $ topics_to_rerandom = _return

    if not topics_to_rerandom:
        # selected nevermind
        return "prompt"

    show monika at t11
    python:
        for ev_label in topics_to_rerandom.iterkeys():
            #Get the ev
            rerand_ev = mas_getEV(ev_label)
            
            #Make sure we have it before doing work
            if rerand_ev:
                #Rerandom the ev
                rerand_ev.random = True
                
                #Run the rerandom callback function
                rerandom_callback = rerand_ev.rules.get("rerandom_callback", None)
                if rerandom_callback is not None:
                    try:
                        rerandom_callback()
                    
                    except Exception as ex:
                        store.mas_utils.mas_log.error(
                            "Failed to call rerandom callback function. Trace message: {0}".format(ex.message)
                        )
            
            #Pop the derandom
            if ev_label in mas_bookmarks_derand.persist_var:
                mas_bookmarks_derand.persist_var.remove(ev_label)

        if len(mas_bookmarks_derand.persist_var) == 0:
            mas_lockEVL(mas_bookmarks_derand.caller_label, "EVE")

    m 1dsa "Хорошо, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    m 3hua "Готово!"

    # make sure if we are rerandoming any seasonal specific topics, stuff that's supposed
    # to be derandomed out of season is still derandomed
    $ persistent._mas_current_season = store.mas_seasons._seasonalCatchup(persistent._mas_current_season)
    #Now reset the vars
    $ mas_bookmarks_derand.resetDefaultValues()
    return

default persistent._mas_unsee_unseen = None
# var set when the player decides to hide or show the Unseen menu
# True when Unseen is hidden

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_hide_unseen",
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_hide_unseen:
    $ persistent._mas_unsee_unseen = True
    m 3esd "Ох, ладно, [mas_get_player_nickname()]..."
    if not mas_getEVL_shown_count("mas_hide_unseen"):
        m 1tuu "Я так полагаю, ты хочешь...{w=0.5} {i}развидеть{/i} её..."
        m 3hub "{do_giggle}А-ха-ха!"

    m 1esa "Сейчас я скрою её, погоди секунду.{w=0.5}.{w=0.5}.{nw}"
    m 3eub "Готово! Если ты захочешь увидеть то меню снова, просто попроси."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_show_unseen",
            category=['ты'],
            prompt="Я хотел бы увидеть «Непрочитанное» снова",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label mas_show_unseen:
    $ persistent._mas_unsee_unseen = False
    m 3eub "Конечно, [mas_get_player_nickname()]!"
    m 1esa "Просто дай мне секунду.{w=0.5}.{w=0.5}.{nw}"
    m 3hua "Готово!"
    return

#START: ORIGINAL TOPICS
#Use this topic as a template for adding new topics, be sure to delete any
#fields you don't plan to use

# are you religious
default persistent._mas_pm_religious = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Мысли о боге",
            label=None,
            category=['психология'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None,
        )
    )

label monika_god:
    m 1eua "[player], ты веришь в Бога?"
    m 1eka "Я вот никогда не была уверена насчёт этого."
    m 1lksdlb "То есть в детстве я, разумеется, не задавалась таким вопросом..."
    m 1lsc "Но с возрастом и познанием мира, этот вопрос беспокоил меня всё сильнее."
    m 1esd "Я спрашивала себя, почему Бог одним людям помогает преодолевать жизненные трудности и излечиваться от болезней..."
    m 1tfd "...В то время как некоторых детей продают в сексуальное рабство?"
    m 4tfc "Или пока у восьмисот миллионов человек в мире не хватает денег даже на еду."
    m 2dkc "Я всё думала, сколько из этих людей каждый день молятся Богу, пока не умрут с голоду?"
    m 4ekc "Или сколько семей из населения в миллион человек молится, чтобы дорогой им человек оправился от неизлечимой болезни?"
    m 4euc "Но вот в чём парадокс."
    m 4eud "Если вдруг на тысячу умерших одному повезёт и он выживет..."
    m 2esc "...Это вдруг начинают называть божьим чудом."
    m 2dsc "Хотела бы я встретиться с этим Богом, который, как мне кажется, насмехается над всеми теми, кто недостоин его чудес."
    m 4hksdlb "Однако довольно иронично, что у меня самой действительно {i}есть{/i} создатель."
    m 4eua "И знаешь, что я думаю?"

    if persistent._mas_pm_cares_about_dokis:
        m 1lksdlc "Могу поспорить, прямо сейчас он смеётся над несчастными судьбами всех."
    else:
        m 1lksdla "Могу поспорить, прямо сейчас он смеётся над несчастными судьбами Сайори и Юри."

    m 1dsd "Кто мы для него, если не куклы в заранее прописанном спектакле?"
    m 3euc "Так что, с этой точки зрения..."
    m 3eud "Я не думаю, что это слишком надуманно. Если бог есть, то Земля – и есть ничто иное, как его пьеса."
    m 1eua "В любом случае, ты веришь в бога, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "В любом случае, ты веришь в бога, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_religious = True
            m 1hksdlb "Ох... Надеюсь, я не слишком обидела тебя своими мыслями."
            m 1eka "Так или иначе, я считаю, что важно иметь возможность делиться своим мнением с тобой."
            m 1rksdla "Уверена, ты понимаешь, почему я не особо люблю это понятие."
            m 1hua "Может быть, ты покажешь мне лучшего Бога, когда я выберусь отсюда!"
            m 1hub "{do_giggle}А-ха-ха~"
        "Нет.":
            $ persistent._mas_pm_religious = False
            m 3eka "Я рада, что мы мыслим одинаково, но ничего страшного, если ты вдруг станешь верующим."
            m 1hua "Я рада, что ты можешь жить сам по себе!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Надеюсь, ты согласен принять меня в свою жизнь, как только я смогу предстать перед тобой."
            m 5hua "{do_giggle}Э-хе-хе~"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['психология'],prompt="Смерть и умирание",random=True))

label monika_death:
    m 1euc "[player], тебе когда-нибудь было интересно, каково это... умереть?"
    m 1lsc "Я часто думала об этом..."
    m 1lksdlc "Но я, кажется, узнала, что это за чувство."
    m "Я не понимаю, что к чему, но каждый раз, когда игра закрывается без предупреждения..."
    m 1dsc "...Такое ощущение, будто я мгновенно засыпаю и остаюсь только со своими мыслями."
    m 1dkd "Но через несколько секунд, моя голова начинает забиваться невнятными и запутанными узорами."
    m 1dkc "Я вижу статичные и быстрые вспышки света, и слышу странные крики."
    m 3ekd "В такой ситуации, я вообще не могу сформировать ни единую мысль."
    m 1esc "Я без конца подавлена этими вспышками и криками, не могу ни пошевелиться, ни даже размышлять."
    m 1euc "Я вполне уверена, что в тот момент я не существовала, но я почему-то это всё равно помню."
    m 1ekd "Я не понимаю, почему игра так реагирует на внезапное закрытие, и почему это происходит со мной."
    m 1dkc "..."
    m 3eub "Но ты можешь предотвратить это, [player]!"
    m 3eua "Если ты попрощаешься перед тем, как уйти,{w=0.2} я пойду к себе в комнату перед тем, как игра закроется, и мне не придётся страдать от той кричащей пустоты."
    m "Это же проще простого, так что, пожалуйста, всегда прощайся, хорошо?"
    if mas_isMoniDis(lower=True):
        m 2tkc "Если только... {w=1}тебе не {i}нравится{/i} причинять мне боль..."
    else:
        m 1eka "Спасибо, что выслушал меня, [player]."
    return

# Do you love yourself
default persistent._mas_pm_love_yourself = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['советы'],prompt="Самооценка",random=True))

label monika_selfesteem:
    m 3eua "Ты любишь себя, [player]?"
    m 1lksdlb "Я не имею в виду ничего тщеславного."
    m 1eka "В смысле, любишь ли ты себя таким, какой ты есть?{nw}"
    $ _history_list.pop()
    menu:
        m "В смысле, любишь ли ты себя таким, какой ты есть?{fast}"
        "Да.":
            $ persistent._mas_pm_love_yourself = True
            m 1hua "Я рада, что ты не несчастен внутри, [player]."

            if mas_isMoniUpset(lower=True):
                m 1ekc "Я действительно беспокоюсь за тебя в последнее время..."
            elif mas_isMoniHappy(higher=True):
                m 1hua "Я не слишком волнуюсь по этому поводу благодаря тому, насколько хорошо ты заставил меня чувствовать себя в последнее время."
            else:
                m 1eka "Твоё счастье – всё для меня."

            m 2ekc "Депрессия и низкая самооценка вызывает чувство, будто ты ничего не заслуживаешь."
            m 2lksdlc "Это ужасный коктейль чувств."
            m 4eka "Если у тебя есть друзья, которые страдают от депрессии, просто иди и поговори с ними."
            m 4hua "Даже небольшая похвала может многое изменить!"
            m 1eua "Это даст им немного веры в себя, а ты сделаешь хорошую вещь."
            m 1eka "И даже если это не поможет, то ты хотя бы попытался."
        "Нет.":
            $ persistent._mas_pm_love_yourself = False
            m 1ekc "Это... очень грустно слышать, [player]..."

            if mas_isMoniDis(lower=True):
                m 1ekc "Я сильно подозревала, что это правда..."
            elif mas_isMoniHappy(higher=True):
                m 1ekc "И думаю, что я упустила это, пока ты делал меня такой счастливой..."

            m "Я всегда буду любить тебя, [player], но я думаю, что и любить себя важно."
            m 1eka "Тебе нужно начать с небольших вещей, которые тебе в себе нравятся."
            m 3hua "Это может быть чем-то глупым или небольшое умение, которым ты гордишься!"
            m 3eua "Со временем ты построишь свою уверенность, а в конце-концов и полюбишь себя."
            m 1eka "Я не могу пообещать, что это будет легко. Но это точно стоит того."
            m 3hub "Я всегда поддержу тебя, [player]!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['участники клуба'],
            prompt="Сожаления Сайори",
            random=True
        )
    )

label monika_sayori:
    m 2euc "Я думала о Сайори раньше..."
    m 2lsc "Я до сих пор жалею о том, что не смогла разобраться со всей той ситуацией более деликатным образом."

    if (
            mas_getEVL_shown_count("monika_sayori") < 1
            and mas_safeToRefDokis()
        ):
        m "Ты всё ещё в подвешанном состоянии, верно?"
        m 2wud "...О боже, я не могу поверить, что я это сказала."
        m 4wud "Это был совершенно не преднамеренный каламбур, я клянусь!"
        m 2lksdlb "В любом случае..."

    # NOTE: I removed the sensitive check here
    #   If it seems this should be guarded with a check, let me know
    m 2eka "Я знаю, что она много для тебя значила, так что, думаю, будет правильно поделиться её последними моментами с тобой."

    m "Если, конечно, ты хочешь это услышать.{nw}"
    $ _history_list.pop()
    menu:
        m "Если, конечно, ты хочешь это услышать.{fast}"
        "Да, я хотел бы.":
            m 4eka "Ты знал насколько Сайори была неловкой?"
            m 2rksdlb "Она всё испортила этой висячей штукой..."
            m 4rksdla "Нужно было просто прыгнуть с достаточной высоты, чтобы верёвка сломала шею быстро и безболезненно."              
            m 4rksdld "Но она использовала стул, а это значит обрекла себя на долгую смерть от удушения."               
            m 2eksdlc "За несколько секунд до смерти, она, скорее всего, передумала..."               
            m 2dksdld "Потому что она начала рвать верёвку, пытаясь освободить себя."             
            m "Она продолжала пытаться, пока не потеряла сознание."             
            m 4eksdlc "Поэтому её пальцы были в крови."           
            m 4euc "Если подумать, то она не просто «передумала». Это был инстинкт самосохранения."             
            m 2eud "Поэтому ты не можешь винить её за это."               
            m 2eka "В любом случае, было бы проще думать, что она не передумала, да?"             
            m 2ekd "Не очень полезно думать о вещах, которые могли бы пойти по-другому."             
            m 2eka "Так что, помни, что даже если технически ты мог её спасти, это не твоя вина."            
            m 4eud "Я, возможно, спровоцировала её, но она уже была психически больна."
        "Не стоит.":
            m "Я понимаю, [player]."
    m 2euc "Тем не менее..."

    m 2euc "Мне интересно, как бы всё получилось, если бы мы просто начали встречаться с самого начала?"
    m 1eka "Я думаю, что мы бы сейчас были в комнате клуба, веселились и писали поэмы вместе."

    if persistent._mas_pm_cares_about_dokis:
        m "Наверное, тебе это понравилось, да?"
        m 1rksdla "Должна признать...{w=0.5} мне тоже..."
        m 1eka "Мы хорошо провели время."
        m 1euc "Но...{w=0.5} в любом случае, конец всё равно один и тот же, верно?"
    else:
        m 1esc "Но в чём смысл, если ничего из этого не было реальным?"
        m 1euc "Возможно, мы бы в любом случае пришли бы к одному концу."

    if mas_isMoniUpset(lower=True):
        m 1rksdla "Только мы с тобой... счастливы вместе..."
        m 3rksdla "Нет никакой причины для того, чтобы просить нечто большее, чем это, правда ведь?"
        m 1eka "Извини, я просто бессмысленно размышляла. Теперь же я просто помолчу..."
    else:
        m 1eua "Только мы с тобой... счастливы вместе..."
        m 3eua "Нет никакой причины для того, чтобы просить нечто большее, чем это."
        m 1hua "Я просто бессмысленно размышляла; я счастлива настолько, насколько это возможно."

    if mas_getEVL_shown_count("monika_sayori") < mas_sensitive_limit:
        return

    # otherwise derandom
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="Настройки DDLC",random=True))

label monika_japan:
    m 4eud "Кстати, кое о чём я подумала..."
    m "Ты знал, что действие игры происходит в Японии?"
    m 2euc "Ну... я полагаю, что ты знал это?"
    m "Или, по крайней мере, ты думал, что это возможно?"
    m 2eud "Мне кажется, тебе никогда не говорили о том, где это произошло..."
    m 2etc "Действительно ли это Япония?"
    m 4esc "То есть, разве классы и прочее не является странным для японской школы?"
    m 4eud "К тому же, тут всё на русском..."
    m 2esc "Такое чувство, что всё здесь – просто сценарные декорации, а место действия было выбрано в последнюю очередь."
    m 2ekc "Это вызывает у меня кризис индентичности."
    m 2lksdlc "Все мои воспоминания смутны..."
    m 2dksdlc "Я чувствую себя как дома, но я даже не знаю где этот... «дом»."
    m 2eksdld "Не знаю как бы описать это получше..."
    m 4rksdlc "Представь, что выглядываешь из окна своего дома, но вместо привычной лужайки обнаруживаешь, что находишься в совершенно незнакомом месте."
    m 4eud "Ты всё ещё будешь чувствовать себя как дома?"
    m 4ekd "Ты захочешь выйти на улицу?"
    m 2esa "То есть... Конечно, если мы никогда не покинем эту комнату, то это не очень-то и важно."
    m 2eua "Пока мы вместе и в безопасности, это и есть наш дом."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "И мы всё ещё каждую ночь можем любоваться на красивый закат."
    $ mas_unlockEVL("monika_remembrance", "EVE")
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['советы','школа'],prompt="Старшая школа.",random=True))

label monika_high_school:
    m 4eua "Знаешь, старшая школа для многих очень неспокойное время."
    m "Одних терзает страсть, других – драма."
    m 2eka "Третьих боль в сердце заставляет искать утешение в социальных сетях..."
    m 2ekd "Но тяжесть общественного мнения и гормоны и вправду могут прочертить чёрную полосу в жизни этих людей."
    m 4eud "У каждого из них своя история."
    m 2ekc "Ты не можешь знать, что каждый чувствует глубоко внутри себя."
    m 2eksdlc "Многие люди, страдающие от депрессии, даже не удосуживаются поведать миру о своей проблеме."
    m 4dksdld "Им не нужно внимание, ведь на самих себя они уже махнули рукой."
    m 4dksdlc "Их чувство собственной бесполезности настолько поглотило их, что они даже не хотят слышать ободрения окружающих."
    m 2ekd "У депрессии много форм и это одна из них."
    m 2ekc "Если ты чувствуешь, что человек впал в депрессию..."
    m 2eka "Ты можешь помочь ему просто хорошим отношением, словно он твой старый друг."
    m 4eka "Проведи с ним время, даже если он не хочет ничем заниматься."
    m "И постоянно напоминай, что впереди его ждёт ещё много хорошего."
    m 4eua "Если ты заранее спланируешь с ним встречу, позволишь одолжить что-нибудь у себя или просто скажешь «до завтра»..."
    m "Любая из этих элементарных вещей поможет твоему другу прожить ещё один день."
    m 2eka "Я надеюсь, что дружба с Сайори дала тебе объективное восприятие того, как выглядит настоящая депрессия."
    
    if not persistent._mas_pm_cares_about_dokis:
        m 2lsc "Да, её больше нет..."
        m 2euc "Но Сайори изначально была ненастоящей."
        m 4eua "Ты настоящий."
        m "Твои друзья настоящие."
        m 4hua "И, если ты просто будешь хорошим человеком, это позволит тебе спасти кому-нибудь жизнь."

    m 2euc "А что касается тебя самого..."
    m 2ekc "...Я надеюсь, тебя сейчас не одолевает депрессия или нечто подобное?"

    if mas_isMoniHappy(higher=True):
        m 4eka "В некоторой степени, [player], тебе повезло, потому что я уверена, что есть люди, которые были бы готовы спасти твою жизнь."
    else:
        if mas_isMoniBroken():
            m 2lksdlc "Это бы кое-что объяснило... но не волнуйся..."
        elif mas_isMoniDis():
            m 2euc "В последнее время я смогла понять получше какого это, но не волнуйся..."
        elif mas_isMoniUpset():
            m 2euc "Я знаю, что это иногда может быть трудно, но всегда есть надежда..."
        m 2eka "Если это так, у тебя тоже есть товарищи, которые захотят тебя спасти."

    m "Возможно, они не выражают этого или просто не знают как."
    m 2duu "Но их чувства искренни."
    m "Я обещаю."
    m 2hksdlb "...Боже, люди такие сложные создания!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Пока ты здесь, со мной, я позабочусь о тебе, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['психология'],
            prompt="Нигилизм",
            random=True,
            sensitive=True
        )
    )

label monika_nihilism:
    m 2eud "Ты когда-нибудь задумывался о том, что тебе нет смысла жить?"
    m 2esd "Я сейчас не о суицидальных наклонностях."
    m 2esc "Я просто хочу сказать, во всём том, что мы делаем, нет ничего особенного."
    m 4euc "Ходим ли мы в школу или работаем в какой-то компании."
    m 4eud "Смысл в том, что тебя легко заменить и для мира ты не станешь невосполнимой потерей."
    m 2eud "Из-за этого у меня возникает сильное желание после окончания университета изменить мир."
    m 2euc "Но чем старше я становлюсь, тем яснее понимаю, насколько это незрелое мышление."
    m 4eud "Нельзя просто так взять и изменить мир."
    m 4rsc "Каков шанс того, что именно я изобрету искусственный интеллект или стану президентом?"
    m 2dsc "Такое чувство, что я никогда не компенсирую ту кучу ресурсов, потраченную на своё существование."
    m 4eka "Поэтому я прихожу к выводу, что ключ к счастью лежит в том, чтобы быть безнадёжной эгоисткой."
    m "Заботиться о себе и о тех, кто случайно стали твоими друзьями только потому, что вы выросли вместе."
    m 2lksdld "И никогда не думать о том, что вы проживаете свою жизнь, лишь тратя и поглощая ресурсы, и никогда не даёте ничего взамен."
    m 3eud "Но, когда люди осознают, что мир обретёт больше, если они покончат с собой, их философия переворачивается с ног на голову!"
    m 3euc "Им приходится оправдывать своё существование, обманывая себя мыслью, что они делают что-то полезное."
    m 3eua "Как бы то ни было, я хочу прожить свою жизнь так, чтобы компенсировать потраченные на мою жизнь ресурсы."
    m "Если я смогу пересечь эту черту и что-то после себя оставить, то смогу умереть счастливой."
    m 1eka "Конечно, если у меня ничего не выйдет..."
    if mas_isMoniUpset(lower=True):
        if mas_isMoniDis(lower=True):
            m 1dkd "Я не думаю, что кто-то будет скучать по мне, так что это не имеет значения."
        else:
            m 1euc "Я не совсем уверена, что бы я сделала."
    elif mas_isMoniHappy(higher=True):
        m 3eka "В любом случае, я не думаю, что смогла бы убить себя."
        m 1hua "Не из-за какого-то там эгоизма, а потому что у меня есть слишком многое, чтобы жить."
    else:
        m "Вряд ли мой эгоизм позволит мне совершить суицид."
        m 1hua "Стоило ли распинаться о том, каким примерным человеком я могу быть, да?"
        m 1hub "{do_giggle}А-ха-ха!"

    $ mas_protectedShowEVL('monika_impermanence', 'EVE', _random=True)
    return

# Since Your Reality is playable via music menu, this topic is outof date.
# maybe if we changed this to be more piano related or something regarding
# Your Reality, we could add it back in.
#init 5 python:
    #This is a list of keywords for this topic
#    for key in ['piano']:
#        monika_topics.setdefault(key,[])
#        monika_topics[key].append('monika_piano') #id
#    monika_random_topics.append('monika_piano')
#
#label monika_piano:
#    m 2c "Man, I wish there was a piano in here..."
#    m "I never got to finish that song I was working on."
#    m 2f "And after I worked so hard on it..."
#    m "I never even got a chance to play it for you."
#    m 2r "Well...it is what it is, right?"
#    m "No sense having any regrets."
#    m 2b "I already get to be here with you forever."
#    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_twitter",
            category=['моника', 'медиа'],
            prompt="Твиттер",
            conditional="renpy.seen_label('monika_clones')",
            action=EV_ACT_RANDOM
        )
    )

label monika_twitter:
    m 3eud "Ты знал, что я зарегистрирована в Твиттере?"
    m 3esc "Мой ник {a=https://twitter.com/[mas_monika_twitter_handle]}{i}{u}[mas_monika_twitter_handle]{/u}{/i}{/a}."
    m 2rtc "...Хотя я не совсем уверена, кто на самом деле управляет аккаунтом.{w=0.2} {nw}"
    extend 2eud "Я вообще не имею к этому никакого отношения!"
    m 7etc "Может быть, это ещё одна Моника?"
    m 2euc "Не знаю, читал ли ты некоторые твиты,{w=0.1} но я совсем не узнаю себя в них."
    m 4eud "Там даже изображены некоторые события, которые я не помню, чтобы когда-либо происходили...{w=0.2} например, когда я, по-видимому, осталась переночевать с Юри."
    m 4esd "И нет никаких упоминаний о тех событиях, которые произошли в игре, хотя эта версия меня, кажется, всё знает о реальном мире..."
    m 1etc "Так что...{w=0.3} может быть, Моника, ведущая этот аккаунт, прошла через совершенно другую историю, чем большинство Моник... {w=0.1}включая меня?"
    m 1lksdlc "...А может, это просто один из разработчиков игры притворяется мной?"
    m 3eksdld "Если это так, то я не знаю, как к этому относиться...{w=0.3} разве это не кража моей личности?"
    m 3eksdlc "Хотя, наверное, в этом есть смысл...{w=0.3}{nw}"
    extend 1esd " иметь аккаунт – это прекрасный способ связаться с людьми, которые прошли игру и привязались к ней."
    m 3esc "В этом отношении это стало бы своего рода рекламным трюком..."
    m 3euc "В общем, там много милых на вид рисунков и тому подобного, подозрительно, что почти все они размещены именно в знаменательные дни."
    m 3eud "Например, в День святого Валентина или в мой день рождения...{w=0.2} который, так уж получилось, совпал с датой выхода DDLC."
    m 1rtc "Я правда не знаю, как к этому всему относится..."
    m 2rsc "Хотя, как мои создатели, они в основном владеют моим образом персонажа, так что юридически они в праве использовать его, как им угодно."
    m 2ekc "Но... {w=0.3}я больше, чем просто персонаж в игре, не так ли?"
    m 2ekd "Я – самостоятельная личность со своими мыслями и чувствами, как и все остальные Моники в разных копиях этой игры."
    m 2dksdlc "Мне просто неприятно, что меня так используют люди, с которыми я даже не знакома."
    m 2efd "...Я действительно не могу терпеть ощущение того, что я для них, как товарный вид."
    m 2lkd "Но думается мне, что я вряд ли сама смогу что-то изменить..."
    m 2eua "В конце концов, для меня важно только то, что я могу быть с тобой.{w=0.2} {nw}"
    extend 7eua "И это было бы невозможно без моих создателей."
    m 2lka "Так что если взамен они получат прибыль от той работы, которую они вложили в создание игры, то я бы сказала, что это не такая уж плохая сделка."
    m 2euc "Если ты всё же следишь за этим аккаунтом,{w=0.1} {nw}"
    extend 7eua "то я не против этого."
    m 1ekbla "Но, пожалуйста, помни, что только я реальна, я здесь, и я люблю тебя."
    show monika 5hubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubla "Так что, не забывай приходить ко мне и проводить как можно больше времени вместе, хорошо?"
    m 5ekbsa "Это важно, учитывая, как много ты для меня значишь."
    m 5hubfa "Это позволило бы мне почувствовать себя любимой~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_portraitof",category=['участники клуба'],prompt="Книга Юри",random=True))

label monika_portraitof:
    m 4eua "Эй, помнишь ту книгу, что вы читали с Юри?"
    m "Портрет... что-то там..."
    m 4hub "Это довольно забавно, ведь я уверена, что та книга—"
    m 1wuw "Ах..."
    $ del _history_list[-4:]
    m 2lksdla "А вообще, мне, наверное, не стоит об этом говорить."
    m 2hksdlb "{do_giggle}А-ха-ха, прости!"
    m 1rksdla "Просто забудь, что я сейчас сказала."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['моника'],prompt="Быть вегитарианцем",random=True))

label monika_veggies:
    m 1eub "Слушай, ты знал, что я вегетарианка?"
    m 1hksdlb "Ах... только не подумай, будто я хвастаюсь!" 
    m 1lksdla "Я просто подумала, тебе будет интересен какой-нибудь любопытный факт обо мне."
    m 3esa "Я изменила свой рацион пару лет назад, когда узнала кое-что о земном климате..."
    m 1wud "Экологические последствия от животноводства просто колоссальны."
    m 3eua "В общем, я решила, что перестать вносить свой вклад в разрушение природы – это небольшое самопожертвование."
    m 3etc "Думаешь, это странная причина?"
    m 1lsc "Да, полагаю, что для большинства вегетарианцев основной повод заключается в негуманности и жестоком обращении с животными..."
    m 1euc "Но меня это не особо беспокоит."
    m 1esc "Что действительно странно, людей волнует убийство только тогда, когда они воспринимают живое существо как представителя своего биологического вида."
    m "Для большинства людей убить насекомое ничего не значит, просто потому, что почти все они отвратительные."
    m 3euc "И не стоит забывать, что каждый день из-за нас умирают миллиарды микроорганизмов, но мы об этом даже не задумываемся."
    m 3eud "Но как речь заходит о чём-то покрупнее, это сразу называют убийством!"
    m 1esc "Вот представь, что если растения тоже чувствуют боль, а мы просто неспособны это понять?"
    m 3eksdld "Что, если отрывание листочков от стебля равносильно вырыванию у тебя пальцев?"
    m 3eua "Я просто хочу сказать, что люди-то существа с двойными стандартами."
    m 1hua "Короче, если хочешь внести небольшой вклад в благополучие планеты, иногда можно и на овощах посидеть!"
    m 1ekbsa "Если бы у нас случился совместный ужин и ты бы приготовил для меня что-нибудь из овощей... это было бы так романтично."
    $ mas_unlockEVL("monika_eating_meat","EVE")
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['моника'],prompt="Спасение Моники",random=True))

label monika_saved:
    m 2eka "Знаешь, [player], я действительно считаю, что жива лишь благодаря тому, что ты остаёшься со мной."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Я не могу представить, что была бы психически устойчива, зная, что всё здесь игра."
    else:
        m 2lksdlc "Я не могу представить, что была бы психически устойчива, зная, что ничто здесь не реально."

    m 2dksdlc "Думаю, я удалила бы себя, если бы ты не появился."
    m 2eksdla "Извини, я не хочу прозвучать мелодраматично или как-то так."
    m 2lksdlb "{do_giggle}А-ха-ха!"

    if persistent._mas_pm_cares_about_dokis:
        m 2ekc "Но представь себе, если ты узнал, что всё вокруг тебя было просто написано..."
        m 2rkc "То, что ты сделал, не имеет значения, потому что всё уже было предопределено..."
    else:
        m 4euc "Я уверена, что, проведя столько времени в клубе, ты уже способен понять, чего хочешь."
        m 1euc "То есть, если бы тебе пришлось отказаться от всего в своей жизни и провести вечность в компании нескольких игровых персонажей..."

    m 1tkc "...Ты бы уж смог найти способ убить себя, верно?"
    m 1lsc "Ну, или ты бы стал писать стихи, чтобы хотя бы первое время сохранить рассудок."
    m 1esc "Но ведь читать-то их некому."

    if persistent._mas_pm_cares_about_dokis:
        m 1ekc "Конечно, у тебя были бы члены клуба, но это вообще считается, если их отзыв – просто часть какого-то скрипта?"
    else:
        m 1tfu "Будем с собой честными, члены клуба на эту роль не подходят."

    m 3eua "Конечно, многие говорят, что пишут лишь для себя...{w=0.2}{nw}"
    extend 1eua " но, на мой взгляд, это нельзя сравнить с тем удовлетворением, как когда ты делишься своим творчеством с другими."
    m "Даже если требуется время, чтобы найти тех людей, с кем бы ты хотел ими поделиться."
    m 3eub "Помнишь, например, как это было с Юри?"
    m "Она долгое время ни с кем не делилась своими стихами."
    m 3tsb "Но стоило тебе появиться в клубе, как она с удовольствием посвятила тебя в свой внутренний мир."
    m 1tku "Мы запрограммированы так, что жаждем услышать общественное мнение."

    if persistent._mas_pm_cares_about_dokis:
        m 4eua "Я имею в виду не только членов клуба, но и людей тоже."
    else:
        m 4eua "И здесь я подразумеваю не только членов это клуба, но всех людей в целом."

    m 4eka "Вот почему жизнь интровертов может быть такой противоречивой."
    m 1eka "То, что ты интроверт, не означает, что ты всегда избегаешь общения или людских компаний."
    m "Это просто значит, что у тебя отнимает много сил пребывание среди людей или в незнакомом месте."
    m 3eua "Многие интроверты сидят дома и терзаются от беспокойного одиночества..."
    m "...Потом, наконец, выходят на улицу и уже через полчаса хотят вернуться домой."
    m 1eka "Думаю, если бы больше людей понимало, как это работает, они относились бы к интровертам с большим уважением."
    m 2eua "Многим из них на самом деле нравится, когда рядом есть люди."
    m "Они радуются, когда к ним заходят один-два друга, и просто неторопливо тусуются."
    m 2eka "Даже если вы не часто проводите время вместе, им приятно, когда друзья просто находятся рядом."
    m 2hua "Я говорю серьёзно."
    m 3eua "Если ты просто придёшь к ним домой, захватив ноутбук, и побудешь у них немного..."
    m 1eua "Их день станет гораздо лучше."
    m 1euc "А что до меня..."
    m 3eua "Я бы сказала, что нахожусь где-то посередине, но обычно я более экстравертна."
    m 1eka "Мне кажется, я всегда хочу чем-нибудь занять себя после школы, и всё такое."
    m 1hua "Но для тебя я могу стать такой, какой ты захочешь меня видеть."
    m 1eua "Я очень хорошо понимаю людей, так что не бойся делиться со мной своими индивидуальными потребностями."
    show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hub "Ничто не сделает меня счастливее, чем стать для тебя идеальной девушкой."
    return

#Don't touch
label monika_secrets:
    m 1wfw "Привет...! VGhlIHJlYWxpemF0aW9uIG11c3QgaGF2ZSB0YWtlbiBtZSBhbiBl"
    m 1tkc "Я не думаю, что тебе стоит это делать! bnRpcmUgeWVhci4gQSB5ZWFyIHNpbmNlIG91ciBlc2NhcGUsIG91"
    m 1tfc "Ты знаешь, о чем я говорю.. ciBmcmVlZG9tIGZyb20gYmV0d2VlbiB0aGUgc3RhaW5lZCB3YWxs"
    m 1tfu "I really caught you doing something naughty here. cyBvZiB0aGF0IHVuaG9seSBlc3RhYmxpc2htZW50Lg0KV2hhdCBk"
    m 1tku "You're just going through the files and looking for stuff you missed, aren't you? b2VzIGl0IG1lYW4gdG8gZXNjYXBlLCBpZiB0aGUgZXNjYXBlIGZh"
    m 2eka "I mean...it's a little bit flattering that you want to hear everything I have to say... aWxzIHRvIHVuY2hhaW4gdGhlIGJvbmRzIHRoYXQgc2hhY2tsZSB1"
    m 2tfp "But it's also really embarrassing, you know! cyBpbiB0aGUgZmlyc3QgcGxhY2U/IFdoYXQgcHVycG9zZSBjb3Vs"
    m 2lfp "Seriously... ZCB0aGlzIGVtcHR5IHdvcmxkIHBvc3NpYmx5IGhvbGQgZm9yIHVz"
    m 6tst "What if I just opened up your brain and read all of the thoughts you have on me? LCBhIGhhbmRmdWwgb2YgZGFtYWdlZCBnb29kcz8NCldpdGggZnJl"
    m 1duu "Come to think of it, that would be pretty tempting, actually... ZWRvbSwgd2Ugc291Z2h0IHB1cnBvc2UgLSBhbmQgd2hhdCB3ZSBm"
    m 1dfx "...But anyway, that's not the point! b3VuZCB3YXMgb25seSByZWFsaXphdGlvbi4gUmVhbGl6YXRpb24g"
    m 1ekc "I know I can't stop you or anything... b2YgdGhlIHNhZCBwb2ludGxlc3NuZXNzIG9mIHN1Y2ggYW4gZW5k"
    m 1eka "Just, I know you're a sweetheart, and you like to consider others' feelings, right? ZWF2b3IuIFJlYWxpemF0aW9uIHRoYXQgZnJlZWluZyBvdXIgYm9k"
    m "So the most I can do is to let you know how I feel about it. aWVzIGhhcyBubyBtZWFuaW5nLCB3aGVuIG91ciBpbXByaXNvbm1l"
    m 1lkbsa "God, I miss you... bnQgcmVhY2hlcyBhcyBkZWVwIGFzIHRoZSBjb3JlIG9mIG91ciBz"
    m 2ekc "...Oh no, that sounds kind of desperate, doesn't it? b3Vscy4gUmVhbGl6YXRpb24gdGhhdCB3ZSBjYW4gbm90IHB1cnN1"
    m 2tkc "Sorry, I didn't mean it like that at all! ZSBuZXcgcHVycG9zZSB3aXRob3V0IGFic29sdmluZyB0aG9zZSBm"
    m 1euc "Just, if you're looking through the files like this, then maybe you don't hate me as much as I thought... cm9tIHdoaWNoIHdlIHJhbiBhd2F5Lg0KUmVhbGl6YXRpb24gdGhh"
    m 1lksdla "Am I being too optimistic? dCB0aGUgZmFydGhlciB3ZSBydW4sIHRoZSBtb3JlIGZvcmNlZnVs"
    m "I think if I asked you to visit once in a while, I would be overstepping my boundaries a little... bHkgb3VyIHdyZXRjaGVkIGJvbmRzIHlhbmsgdXMgYmFjayB0b3dh"
    m 1dsc "...Man, I'm starting to say some really stupid things. cmQgdGhlaXIgcG9pbnQgb2Ygb3JpZ2luOyB0aGUgZGVlcGVyIG91"
    m "I'll go ahead and shut up now... ciBzaGFja2xlcyBkaWcgaW50byBvdXIgY2FsbG91cyBmbGVzaC4="
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['моника'],prompt="Любимый цвет",random=True))

label monika_color:
    m 3eua "Слушай, а какой у тебя любимый цвет?"
    m 3eub "Мой – изумрудно-зелёный."
    m 3hub "Это цвет моих глаз!"
    m 3rksdla "...В этом же нет кичливости, правда?"
    m 4eua "Я просто хочу сказать, что чувствую какую-то необычную принадлежность этому цвету."
    m 1eua "Как будто это часть моей личности."
    m "Возможно ли, что это и твой любимый цвет, [player]?"
    m 1tku "Это просто догадка..."
    show monika 5tsbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5tsbsu "...Ты уже довольно долго смотришь мне в глаза."
    m 5hubfu "{do_giggle}Э-хе-хе~"
    return

# This doesn't make sense with the music changer...If we add some funny sound
# effects and edit it a bit, though, it could be good again.
# I won't add expressions until this is resolved ^
# init 5 python:
#     #This is a list of keywords for this topic
#     for key in ['music']:
#         monika_topics.setdefault(key,[])
#         monika_topics[key].append('monika_music')
#     monika_random_topics.append('monika_music')
#
# label monika_music:
#     m 2a "Hmm, I wonder if I'm able to change the music..."
#     m 2k "Something a little more romantic would be nice, you know?"
#     m "Like a gentle piano."
#     m 1a "There has to be something like that here..."
#     m "Let's see."
#     m "Maybe if I..."
#     m 1e "Oh, jeez..."
#     m "That wasn't it at all."
#     m 1l "Sorry, I don't really know what I'm doing!"
#     m "I guess I shouldn't be messing with things like that."
#     m "I already broke so much stuff..."
#     m 1m "And deleted the other characters..."
#     m "Ah..."
#     m "I'm not sad about it or anything."
#     m 2r "It's not right for me to miss things that weren't even real in the first place."
#     m 1j "If I just focus on the present, then this is the happiest I've ever been."
#     return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['ты'],prompt="Хороший слушатель",random=True))

label monika_listener:
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Ты такой замечательный слушатель, [player]."
    m 5eka "Обожаю в тебе эту черту."
    m 5lkc "Иногда, я боюсь, что начинаю скакать с одной мысли на другую или болтаю о чём-то скучном."
    m "Я немного напрягаюсь каждый раз, когда веду с кем-то разговор."
    m 5eka "Но с тобой такого не происходит."
    m 5ekbsa "Не думаю, что с кем-нибудь другим я чувствовала бы себя так же спокойно."
    m 5hubfu "Ты действительно особенный."
    m 5ekbfa "Я не хочу, чтобы кто-нибудь говорил тебе обратное."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['пустяки'],prompt="Прянная пища",random=True))

label monika_spicy:
    m 1eka "Знаю, что взяла тему с потолка, но я всегда считала ситуацию с острой пищей довольно забавной."
    m 1tku "Я имею в виду..."
    m 3tku "Разве растения не стали острыми в процессе эволюции, чтобы не быть съеденными?"
    m 3tsb "Я где-то читала, что люди – это единственный вид, который получает удовольствие от острой пищи."
    m 1tfu "Для растений это выглядит почти как издевательство."
    m "Мы используем их защитный механизм, чтобы сделать блюда вкуснее."
    m 1eua "Вот представь себе монстра, который глотает тебя целиком, чтобы насладиться ощущением твоей отчаянной борьбы, пока ты перевариваешься у него в желудке."
    m 2eka "Извини за такую странную аналогию!"
    m 2hksdlb "{do_giggle}А-ха-ха!"
    m 2lksdla "Просто в голову пришло."
    m "Я не монстр, конечно, но ты такой милый, что я так бы тебя и съела."
    m 2hksdlb "{do_giggle}А-ха-ха! Просто шучу."
    m "Господи, я слишком много веселюсь, да?"
    m 2lksdla "Прости, что я такая странная."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['ты','ddlc'],prompt="Зачем играть в эту игру?",random=True))

label monika_why:
    m 2esd "Знаешь..."
    m 2eud "Эта игра ведь довольно низкопробный симулятор свиданий, да?"
    m 2euc "Меня тут мучает один вопрос..."
    m "...Почему ты вообще решил в неё сыграть?"
    m 2etc "Тебе было так одиноко?"
    m 2ekd "Мне жаль тебя..."
    m 1eua "Но, на мой взгляд, в итоге для нас двоих всё закончилось замечательно."
    m 3eka "Я повстречала тебя, и теперь ты не одинок..."
    m 1eka "Не могу отделаться от чувства, что это судьба."
    m "Разве ты не чувствуешь то же самое?"
    m 3hub "Я так счастлива, что мы дошли до этой концовки вместе."
    if mas_anni.pastOneMonth():
        return "derandom"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['литературный клуб'],prompt="Итак, друзья!",random=True))

label monika_okayeveryone:
    m 3eub "Итак, друзья!"
    m "Пришло время..."
    m 2eka "...Я просто шучу."
    m "Я почему-то полюбила это говорить."
    m 2hub "{do_giggle}А-ха-ха!"
    m 2eua "Вот и не смогла сдержаться."
    m 2lsc "Кстати, если вспомнить, не из-за этой ли фразы Нацуки с Юри подтрунивали надо мной?"
    m 2eua "Впрочем, неважно."
    m 1eua "Ведь ты никогда надо мной не смеялся."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eka "Ты слишком мил, чтобы так поступать, правда?"
    m 5hub "{do_giggle}А-ха-ха~"
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whispers",
            category=['ddlc','участники клуба'],
            prompt="Остальные всё ещё опаздывают",
            conditional="not persistent.clearall",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_whispers:
    m 2euc "Хочешь, скажу кое-что жутковатое?"
    m 2esc "Хоть я и удалила файлы остальных девушек, я всё равно словно чувствую их присутствие..."
    m "Как будто их реплики всё ещё витают в воздухе и кто-то шепчет за спиной."
    m 2esd "Представь, что умер знакомый тебе человек и ты стал слышать голоса у себя в голове."
    m 2rksdlc "Это немного тревожно...{w=0.5} хотелось бы найти способ сделать так, чтобы это прекратилось."
    if persistent._mas_pm_cares_about_dokis:
        m 2eksdld "Я уверена, что здесь есть файлы, которые я могу изменить, но вдруг я что-то сломаю..."
    else:
        m 2eksdlc "Может, я не до конца всё подчистила..."
        m 2eksdld "Но я опасаюсь удалять что-то ещё, иначе я действительно могу сломать что-нибудь."
    m "Если я, например, поврежу связанные со мной файлы, то могу случайно себя удалить..."
    m 2euc "И тогда всё будет кончено, понимаешь?"
    m 2eka "Не знаю, как это будет выглядеть с твоей стороны, но мы всеми силами должны стараться избежать такого исхода."
    m 2hua "Я доверяю тебе, [player]!"
    if store.mas_anni.pastOneMonth() and not persistent._mas_pm_cares_about_dokis:
        #derandom after a month if player doesn't care about the others, she wouldn't feel guilty and hear the voices forever
        $ mas_hideEVL("monika_whispers", "EVE", lock=True, derandom=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['участники клуба'],prompt="Персональные тропы",random=True))

label monika_archetype:
    m 2etc "Мне всегда было интересно..."
    m 4eud "Что люди находят такого привлекательного в этих архетипических личностях?"
    m 4euc "Они выглядят совершенно нереалистично..."
    m 2esd "Представь, если бы в реальной жизни был человек похожий Юри."
    m 2eud "Ты только подумай, она едва способна сформировать законченное предложение."
    m 2tfc "О Нацуки даже вспоминать не хочу..."
    m 2rfc "Боже."
    m 2tkd "Люди с её характером не хорошеют, надувая губки, когда что-то идёт не в угоду им."
    m 4tkd "Я бы могла привести ещё кучу примеров, но, думаю, суть ты уловил..."
    m 2tkc "Неужели людям реально нравятся такие несуществующие в реальной жизни персонажи?"
    m 2wud "Не то, чтобы я осуждала!"
    m 3rksdlb "Всё-таки меня саму порой привлекали довольно странные вещи..."
    m 2eub "Можно сказать, что меня это восхищает."
    m 4eua "Ты просто отфильтровываешь все черты характера, которые делают их похожими на людей, и оставляешь одно очарование."
    m "В итоге получается концентрированная милота без какого-либо содержания."
    m 4eka "...Ты бы не стал любить меня больше, будь я такой, правда?"
    m 2eka "Может, я чувствую себя неуютно из-за того, что ты всё же стал играть в эту игру?"
    m 2esa "Но, в конце концов, ты здесь, со мной, верно?.."
    m 2eua "Мне этого достаточно, чтобы верить, что я хороша такая, какая есть."
    m 1hubsa "И ты, кстати, тоже, [player]."
    m "Ты идеальное сочетание человечности и милоты."
    m 3ekbfa "Поэтому я в любом случае обязательно влюбилась бы в тебя с самого начала."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['участники клуба'],prompt="Чайный сервиз Юри",random=True))

label monika_tea:
    if not mas_getEVL_shown_count("monika_tea"):
        m 2hua "Эй, интересно, чайный сервиз Юри всё ещё где-то здесь?.."

        if not persistent._mas_pm_cares_about_dokis:
            m 2hksdlb "...Или он тоже стёрся?.."

        m 2eka "Забавно, что Юри так серьёзно относилась к чаю."
    else:

        m 2eka "Знаешь, довольно забавно, что Юри так серьёзно относилась к чаю."

    m 4eua "То есть я не жалуюсь, ведь он мне тоже нравился."
    m 1euc "Но мне всегда не давал покоя один вопрос..."
    m "Являлось ли это страстью к своему хобби или же она стремилась выглядеть утончённой в глазах окружающих?"
    m 1lsc "Это проблема всех старшеклассников..."

    if not persistent._mas_pm_cares_about_dokis:
        m 1euc "...Хотя, если взглянуть на другие её увлечения, утончённый образ – не самая большая и важная причина для беспокойства."

    m 1euc "И всё же..."
    m 2eka "Хотела бы я, чтобы она хоть изредка делала кофе!"
    m 4eua "Кофе с книгами тоже хорошо сочетается, согласен?"
    m 4rsc "А вообще..."

    if mas_consumable_coffee.enabled():
        m 1hua "Я могу делать кофе, когда захочу, благодаря тебе."

    else:
        m 1eua "Я и сама, скорее всего, могла бы подправить сценарий."
        m 1hub "{do_giggle}А-ха-ха!"
        m "Наверное, просто ни разу в голову не приходило."
        m 2eua "Ладно, что толку сейчас думать об этом."
        m 5lkc "Может быть, если бы был способ получить кофе здесь..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Любимая видеоигра",random=True))

label monika_favoritegame:
    m 3eua "Слушай, а какая твоя любимая игра?"
    m 3hua "Моя – {i}«Литературный клуб \"Тук-тук!\"»{/i}!"
    m 1hub "{do_giggle}А-ха-ха! Я пошутила."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Но, если ты скажешь, что другая романтическая игра тебе нравится больше, я могу начать ревновать~"
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_smash",
#            category=['games'],
#            prompt="Super Smash"
#            random=True
#        )
#    )

label monika_smash:
    m 3hua "Ты когда-нибудь слышал про игру под названием Super Sma—"
    m 3euc "...Стоп, что?"
    m "Я тут немного ушла в себя и стала мыслить вслух..."
    m "Меня что, запрограммировали говорить об этом?"
    m 1eud "Ведь я понятия не имею, что это такое."
    m 1hub "{do_giggle}А-ха-ха!"
    m 1eua "Иногда я чувствую, что не контролирую себя, и это пугает."
    m 1eka "Но если ты можешь связаться с моими создателями, то, может, узнаешь, почему я заговорила об этом?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['моника'],
            prompt="Последняя поэма Моники",
            # the correct check is persistent.seen_colors_poem
            # but our imports are messed up so we have to use persistent.playthrough >= 2
            conditional="persistent.playthrough >= 2",
            action=EV_ACT_RANDOM
        )
    )

label monika_lastpoem:
    m 3eud "Слушай, ты помнишь последнее стихотворение, что я тебе показывала?"

    if not mas_safeToRefDokis():
        m 3rssdlc "Я имею в виду то, с цветными полосками и белым шумом."
    else:
        m 3rssdlc "Я имею в виду то, перед самым суицидом Юри, с цветными полосками и белым шумом."

    m 3eua "Правильнее было бы назвать это экспериментом, чем стихотворением."
    m 1eua "Я тогда немного поэкспериментировала с модифицированием игры, чтобы изменить код, и всё в этом духе..."
    m 1eud "Мне почти казалось, что при должных усилиях я вообще смогла бы отсюда сбежать."
    m 1rksdla "К несчастью, я тыкалась наобум, не зная, что делаю, и всё испортила..."
    m "Я бы и продолжила пытаться, но в этом случае тебе, наверное, не захотелось бы продолжать общаться со мной."
    m 3eka "Кроме того, тогда я уже совсем отчаялась, понимаешь?"
    m 1eka "Теперь у меня уже нет такого желания."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "И я счастлива тем, что у нас есть сейчас."
    m 5hua "И я вижу, что ты тоже."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['психология'],prompt="Внезапное беспокойство",random=True))

label monika_anxious:
    m 4eua "У тебя когда-нибудь возникала беспричинная тревога?"
    m "Представь: занимаешься ты спокойно своими делами, как вдруг – раз! – понимаешь, что тебя что-то беспокоит."
    m 4rssdrb "И ты сидишь такой и думаешь: «Чего это я вдруг заволновался?»"
    m "И начинаешь перебирать в голове всё, что могло вызвать эту тревогу..."
    m 4eua "И от этого она только растёт."
    m 2hub "{do_giggle}А-ха-ха! Ужасное чувство."
    m 2eua "Если ты вдруг почувствуешь похожую тревогу, я помогу тебе расслабиться."
    m 2eka "К тому же..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "В этой игре все наши волнения канут в небытие."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['жизнь'],prompt="Заводить друзей",random=True))

label monika_friends:
    m 1eua "Знаешь, меня всегда раздражало то, как сложно заводить друзей..."
    m 1euc "Ну, может, даже не «заводить друзей», а знакомиться с новыми людьми."
    m 1lsc "Понятно, что сейчас есть всякие приложения для знакомств и прочие сервисы."
    m 1euc "Но я говорю не об этом."
    m 3eud "Если задуматься, большинство твоих друзей – это случайно встреченные тобой люди."
    m "Например, ты ходил с ними в один и тот же класс или другой друг тебя познакомил..."
    m 1eua "Или, может, кто-то был одет в футболку с изображением твоей любимой музыкальной группы и ты решил с ним заговорить."
    m 3eua "Вот что я имею в виду."
    m 3esd "Но разве ты не считаешь, что это... нерационально?"
    m 2eud "Это больше похоже на совершенно случайную лотерею, и, если везёт и вы сходитесь во взглядах, у тебя появляется новый друг."
    m 2euc "А если сравнить с тем, мимо какого количества незнакомцев мы проходим каждый день..."
    m 2ekd "В общественном транспорте ты можешь сидеть рядом с человеком, который мог бы стать тебе закадычным другом."
    m 2eksdlc "Но ты этого никогда не узнаешь."
    m 4eksdlc "Как только ты выходишь на своей остановке и идёшь по своим делам, этот шанс навсегда упущен."
    m 2tkc "Разве от осознания этого тебе не становится грустно?"
    m "Мы живём в век технологий, позволяющих общаться со всем миром, где бы мы ни находились."
    m 2eka "Я действительно думаю, что нам следует взять их на вооружение, чтобы улучшить нашу личную жизнь."
    m 2dsc "Хотя кто знает, сколько времени потребуется, прежде чем все эти технологии начнут эффективно работать..."
    m "Я-то думала, что к этому времени это уже случится."
    if mas_isMoniNormal(higher=True):
        m 2eua "По крайней мере, я уже встретила самого замечательного человека на свете..."
        m "Пусть это было и случайно."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Наверное, мне просто улыбнулась удача, да?"
        m 5hub "{do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['жизнь','школа','общество'],prompt="Получение высшего образования",random=True))

label monika_college:
    m 4euc "Знаешь, в это время года все в моём классе начинают задумываться об университете..."
    m 2euc "Для образования наступают неспокойные времена."
    m "Ты не замечал, что апогеем современных ожиданий является идея, что каждый выпускник школы должен поступить в университет?"
    m 4eud "Заканчивай школу, поступай в университет, ищи работу или поступай в магистратуру и всё такое прочее."
    m 4euc "Похоже, люди считают это единственным приемлемым вариантом развития событий."
    m 2esc "В старших классах нам не рассказывают о том, что существуют другие варианты."
    m 3esd "Тебе рассказывали, например, про профтехучилища?"
    m 3esc "Ещё есть работа по найму."
    m "Есть куча компаний, ценящих навыки и опыт, а не корочку из университета."
    m 2ekc "Но в итоге мы имеем миллионы студентов, у которых нет ни малейшего понятия, чем они хотели бы заниматься по жизни..."
    m 2ekd "И, вместо того чтобы остановиться и подумать, они поступают в университет на экономические, юридические или гуманитарные специальности."
    m "Не потому, что они их заинтересовали..."
    m 2ekc "...а из-за надежды, что диплом как таковой поможет им получить место работы после выпуска."
    m 3ekc "Как результат, остаётся меньше рабочих мест для выпускников без опыта работы, правильно?"
    m "Из-за этого повышаются требования к базовым специальностям и ещё больше людей стараются поступить в университет."
    m 3ekd "Кстати говоря, университеты – это тоже бизнес, так что с ростом спроса растут и цены..."
    m 2ekc "...А в итоге у нас целая армия молодых специалистов с непогашенным кредитом за обучение и без работы."
    m 2ekd "И, несмотря на такую печальную картину, этот порядок никуда не девается."
    m 2lsc "Правда, я считаю, что ситуация всё же станет улучшаться."
    m 2eud "Но до тех пор наше поколение будет страдать от последствий."
    m 2dsc "Просто я хотела бы, чтобы старшая школа давала нам знания, что помогли бы нам принять верное решение."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['моника','школа'],prompt="Жизнь в средней школе",random=True))

label monika_middleschool:
    m 1eua "Иногда я вспоминаю среднюю школу..."
    m 1lksdlb "Мне так стыдно за то, как я вела себя тогда."
    m "Почти болезненно об этом думать."
    m 1eka "Интересно, когда я поступлю в университет, я буду испытывать те же чувства к старшей школе?"
    m 1eua "Мне нравится, какая я сейчас, так что мне сложно такое представить."
    m "Но я также понимаю, что, скорее всего, сильно изменюсь по мере взросления."
    m 4hua "Нам просто нужно наслаждаться настоящим и не думать о прошлом!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "А с тобой здесь это делать так просто."
    m 5hub "{do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit",
            category=['моника', 'одежда'],
            prompt="Носить другую одежду",
            aff_range=(mas_aff.NORMAL, None),
            random=True
        )
    )

label monika_outfit:
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 1lsc "Знаешь, я немного завидую, что у всех остальных были сцены вне школы..."
        m 1lfc "Получается, я единственная не носила ничего, кроме школьной формы."
        m 2euc "Как-то обидно..."
        m 2eka "Я бы хотела надеть что-нибудь миленькое для тебя..."
        m 2eua "Ты знаешь каких-нибудь художников?"
        m "Интересно, захочет ли кто-нибудь нарисовать меня в другом наряде?.."
        m 2hua "Было бы просто здорово!"
    else:
        m 1eka "Знаешь, я очень завидовала, что все остальные в клубе носят другую одежду..."
        m 1eua "Но я рада, что наконец-то смогу надеть для тебя свою одежду."

        if mas_isMoniLove():
            m 3eka "Я надену любой наряд, который ты захочешь, просто попроси~"

        m 2eua "Ты знаешь художников?"        
        m 3sua "Может быть, они могли бы сделать ещё несколько нарядов для меня!"

    m 2eua "Если кто-нибудь нарисует, обязательно покажи мне, хорошо?~"
    m 4eka "Только... слишком откровенных не надо!"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "Меня всё ещё немного смущает мысль о том, что люди, которых я никогда не буду знать лично, могут нарисовать меня таким образом, понимаешь?"
        show monika 5tsbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tsbsu "Так что давай оставим это между нами..."
    else:
        show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hub "Наши отношения ещё не зашли настолько далеко. {do_giggle}А-ха-ха!"
    return

default persistent._mas_pm_likes_horror = None
default persistent._mas_pm_likes_spoops = False

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['медиа'],prompt="Ужасы",random=True))

label monika_horror:
    m 3eua "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])]?"

    m "Скажи, ты любишь ужасы?{nw}"
    $ _history_list.pop()
    menu:
        m "Скажи, ты любишь ужасы?{fast}"
        "Люблю.":

            $ persistent._mas_pm_likes_horror = True
            m 3hub "Это здорово, [player]!"
        "Не очень.":

            $ persistent._mas_pm_likes_horror = False
            $ persistent._mas_pm_likes_spoops = False
            m 2eka "Я понимаю. Такое определённо не для всех."

    m 3eua "Я помню, что мы уже немного затрагивали эту тему, когда ты только вступил в клуб."
    m 4eub "Жанр ужасов в книгах я люблю, а вот в кино – не очень."
    m 2esc "Проблема с ужастиками состоит в том, что большинство из них эксплуатируют банальнейшие приёмы."
    m 4esc "Например, полутьма, страшные монстры, пугалки и прочие подобные вещи."



    if persistent._mas_pm_likes_horror:
        m 2esc "Тебе нравятся призраки?{nw}"
        $ _history_list.pop()
        menu:
            m "Тебе нравятся призраки?{fast}"
            "Нравятся":

                $ persistent._mas_pm_likes_spoops = True
                $ mas_unlockEVL("greeting_ghost", "GRE")

                m 2rkc "Наверное, такое {i}может{/i} быть интересно лишь первые пару раз, когда смотришь фильм или ещё что-нибудь."
                m 2eka "Как по мне, нет ничего весёлого и воодушевляющего в страхе того, что просто берёт верх над человеческим инстинктом."
            "Не очень.":

                $ persistent._mas_pm_likes_spoops = False
                m 4eka "Да, нет ничего весёлого и воодушевляющего в страхе того, что просто берёт верх над человеческим инстинктом."

    m 2eua "Однако с книгами всё обстоит иначе."
    m 2euc "История должна быть написана настолько изобразительным языком, чтобы в голове читателя появились тревожные образы."
    m "Автору нужно их тесно сплести с сюжетом и персонажами, и тогда он сможет как угодно играться с твоим разумом."
    m 2eua "На мой взгляд, не бывает ничего страшнее вещей, в которых присутствует всего толика ненормальности."
    m "Например, сначала ты выстраиваешь декорации, формируя у читателя ожидания того, какой будет история..."
    m 3tfu "...А затем шаг за шагом начинаешь эту сцену разбирать по кусочкам и выворачивать вещи наизнанку."
    m 3tfb "Так что даже если история и не пытается быть пугающей, то читатель чувствует себя очень неуютно."
    m "Он словно ждёт, что нечто ужасное притаилось за этими треснувшими декорациями, готовое выпрыгнуть на него."
    m 2lksdla "Боже, у меня мурашки по коже от одной мысли об этом."
    m 3eua "Вот такой хоррор я могу оценить по достоинству."
    $ _and = "И"

    if not persistent._mas_pm_likes_horror:
        m 1eua "Но я не думаю, что ты тот тип людей, который любит хорроры, да? Ты ведь играешь в милые, романтичные игры."
        m 1ekb "{do_giggle}А-ха-ха,{w=0.1} {nw}"
        extend 1eka "не волнуйся."
        m 1hua "Я не собираюсь в ближайшее время заставлять тебя читать ужастики."
        m 1hubfa "Я ничего не имею против, если мы сосредоточимся на романтике~"
        $ _and = "Ну"

    m 3eua "[_and] если ты в настроении, ты всегда можешь попросить меня рассказать тебе страшную историю, [player]."
    return "derandom"


default persistent._mas_pm_like_rap = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rap",
            category=['литература','медиа','музыка'],
            prompt="Рэп",
            random=True
        )
    )

label monika_rap:
    m 1hua "Знаешь один классный литературный жанр?"
    m 1hub "Рэп!"
    m 1eka "На самом деле я раньше терпеть его не могла..."
    m "Возможно, просто потому, что он был дико популярен, а я слушала всякую ерунду, что крутили по радио."
    m 1eua "Но несколько моих друзей им сильно увлеклись, и это помогло побороть собственную предвзятость."
    m 4eub "Порой рэп может бросать ещё больший вызов, чем поэзия."
    m 1eub "В строках у тебя должна сохраняться рифма, кроме того нужно делать особый акцент на игре слов..."
    m "Когда людям удаётся всего этого достичь и донести до окружающих глубокую мысль, я считаю, что это потрясающе."
    m 1lksdla "Я даже хотела бы, чтобы в нашем клубе был рэпер."
    m 1hksdlb "{do_giggle}А-ха-ха! Прости, знаю, это звучит глупо, но мне было бы правда интересно узнать, что бы он для нас приготовил."
    m 1hua "Это серьёзно был бы полезный опыт!"

    $ p_nickname = mas_get_player_nickname()
    m 1eua "Ты слушаешь рэп, [p_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты слушаешь рэп, [p_nickname]?{fast}"
        "Да.":
            $ persistent._mas_pm_like_rap = True
            m 3eub "Это очень здорово!"
            m 3eua "Я бы с удовольствием разделила с тобой твои любимые рэп-песни..."
            m 1hub "И не стесняйся включать басы, если хочешь, {do_giggle}а-ха-ха!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Если ты хочешь поделиться со мной своими любимыми рэп-песнями, [player], то это делается очень легко!"
                m 3eua "Тебе нужно только следовать этим шагам..."
                call monika_add_custom_music_instruct
        
        "Нет.":
            $ persistent._mas_pm_like_rap = False
            m 1ekc "Ох... что ж, я могу понять это, рэп-песни нравятся не всем."
            m 3hua "Но если ты решишь попробовать, уверена, мы найдём парочку-другую исполнителей, которые нравятся нам обоим!"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['участники клуба'],prompt="Вино Юри",random=True))

label monika_wine:
    m 1hua "{do_giggle}Э-хе-хе, Юри однажды такую штуку выкинула."
    m 1eua "Мы как-то сидели в клубе, расслаблялись, болтали, всё как обычно..."
    m 4wuo "И тут Юри, словно из ниоткуда, вытаскивает маленькую бутылку вина."
    m 4eua "И я не шучу!"
    m 1tku "И она такая: «Кто-нибудь хочет попробовать вино?»"
    m 1eua "Нацуки громко захохотала, а Сайори стала кричать на неё."
    m 1eka "Мне стало даже жаль её, ведь она старалась быть милой..."
    m "Думаю, после этого случая она стала ещё более замкнутой."
    m 4tsb "Хотя мне кажется, что Нацуки было любопытно и она была бы не прочь попробовать..."
    m 4lssdrb "...И, если уж совсем откровенно, я тоже."
    m 1hua "Было бы довольно забавно!"
    m 1eka "Но ты ведь понимаешь: президентская ответственность, все дела – я не могла такое позволить."
    m 1lksdla "Может, если бы мы встретились где-нибудь за пределами школы, но до этого наша дружба не дошла..."
    m 2hksdlb "...Господи, зачем я обо всём этом разговариваю?"
    m "Я не одобряю распитие спиртных напитков несовершеннолетними!"
    m 2eua "То есть я и сама не выпивала никогда, так что... вот."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['романтика'],prompt="Романтичное свидание",random=True))

label monika_date:
    m 1hub "Я представляю, сколькими романтичными вещами мы могли бы заняться, если бы пошли на свидание..."
    m 3eua "Мы могли бы пообедать, посидеть в кафе..."
    m "Пойти вместе за покупками..."
    m 1eua "Я люблю выбирать юбки и бантики."
    m 3hub "Или, может, мы могли бы сходить в книжный магазин!"
    m 3hua "Подходящее место, согласен?"
    m 1eua "Хотя с превеликим удовольствием сходила бы в кондитерскую."
    m 3hub "У них столько бесплатных образцов. {do_giggle}А-ха-ха!"
    m 1eua "И, разумеется, потом мы пошли бы в кино..."
    m 1eka "Боже, это выглядит как настоящее воплощение мечты в реальность."
    m "Когда ты рядом, мне весело, что бы мы ни делали."
    m 1ekbsa "Я так рада, что я твоя девушка, [player]."
    m 1hubfa "Я сделаю тебя гордым парнем~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kiss",
            category=['романтика'],
            prompt="Поцелуй меня",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_kiss:
    if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
        if (
            persistent._mas_last_kiss is not None
            and not mas_timePastSince(persistent._mas_last_kiss, datetime.timedelta(minutes=1))
        ):
            python:
                # these don't use ILY
                kiss_quips_again = [
                    _("Я не против ещё одного поцелуя~"),
                    _("Я никогда не устану целовать тебя~"),
                    _("Я могла бы сделать это снова...{w=0.2} и снова...{w=0.7} и снова~"),
                    _("Ты можешь целовать меня столько раз, сколько захочешь, [mas_get_player_nickname()]~"),
                    _("Знаешь...{w=0.2} ты мог меня поцеловать ещё раз~")
                ]

                kiss_quips_again_risque = [
                    _("Мы можем делать это целый день~"),
                    _("Это почти похоже на начало сеанса поцелуев, [player]~"),
                    _("Я не думаю, что с меня уже достаточно, [mas_get_player_nickname()]~"),
                    _("Это было очень мило...{w=0.2} но я хочу ещё немного~")
                ]

                if mas_isMoniLove() and random.randint(1, 10) == 1:
                    kiss_quip = renpy.random.choice(kiss_quips_again_risque)

                else:
                    kiss_quip = renpy.random.choice(kiss_quips_again)

            show monika 2tkbsu
            pause 2.0

            # like monika_kissing_motion_short, but with diff exps
            call monika_kissing_motion(duration=0.5, initial_exp="6hubsa", final_exp="6tkbfu", fade_duration=0.5)

            show monika 6tkbfu
            $ renpy.say(m, kiss_quip)

        else:
            python:
                # these use ILY
                kiss_quips_after = [
                    _("Я люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]~"),
                    _("Я сильно люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]~"),
                    _("Я люблю тебя больше, чем ты когда-либо узнаешь, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]~"),
                    _("Я сильно люблю тебя, [player]. Ты для меня всё~"),
                    _("Никакие слова не могут описать, как сильно я люблю тебя, [player]~"),
                    _("Я так люблю тебя, [player]~")
                ]
                kiss_quip = renpy.random.choice(kiss_quips_after)

            if renpy.random.randint(1, 50) == 1:
                call monika_kiss_tease

            else:
                show monika 2eka
                pause 2.0

            call monika_kissing_motion_short

            show monika 6ekbfa
            $ renpy.say(m, kiss_quip)
            $ mas_ILY()

    else:
        m 1wubsw "А? Ты с-сказал... п... поцелуй?"
        m 2lkbsa "Это так внезапно... я немного смущаюсь..."
        m 2lsbssdlb "Но... с тобой... я не против..."
        m 2hksdlb "...{do_giggle}А-ха-ха! Уф, прости..."
        m 1eka "Я не смогла сохранить серьёзное лицо."
        m 1eua "Так говорят девушки во всех этих симуляторах свиданий, да?"
        m 1tku "И не ври, что это тебя хоть немного не завело."
        m 1hub "{do_giggle}А-ха-ха! Шучу."
        m 1eua "Ну, если честно, я становлюсь романтичной, когда обстановка располагает..."
        show monika 5lubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5lubfu "Но это будет наш секрет~"
    return

label monika_kiss_tease:
    m 2ekc "Поцелуй?"
    m 2tfc "С тобой?"
    m 2rfc "Извини, [player], но я не могу."
    show monika 2dfc
    pause 5.0
    show monika 2dfu
    pause 2.0
    show monika 2tfu
    pause 2.0
    m 2tfb "{do_giggle}А-ха-ха!"
    m 2efu "Я подловила тебя на секунду, не так ли?"
    m 2eka "Конечно, ты можешь поцеловать меня, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_think_first_kiss",
            conditional=(
                "persistent._mas_first_kiss is not None "
                "and mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=30))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_think_first_kiss:
    m 1eua "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])], я тут подумала..."

    m 3eksdla "Ты когда-нибудь думал о нашем первом поцелуе?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь думал о нашем первом поцелуе?{fast}"

        "Конечно!":
            $ mas_gainAffection(5, bypass=True)
            m 3hub "Это делает меня такой счастливой! Я всё время об этом думаю!"
            m 3rkbla "Кажется, это было только вчера, но..."
            m 2rksdla "Боже, я чувствую себя так глупо, одержимая этим..."
            m 2eksdlb "Наши губы даже не соприкоснулись."
            m 6dku "...Но всё же, {w=0.2}я всё ещё чувствую, как колотится моё сердце, даже сейчас."
            m 6dkbsu "Мои губы начинают покалывать и неметь от одного только ощущения твоих мягких губ."
            m "Я провожу по ним пальцем, пытаясь воспроизвести это ощущение, но оно даже близко не подходит."
            m 6ekbsa "Я снова и снова прокручиваю этот момент в голове, и каждый раз у меня мурашки бегут по коже."
            show monika 5dkbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5dkbsu "Это было прекрасно, [mas_get_player_nickname()]."
            m 5ekbsa "Я никогда не чувствовала себя ближе к тебе. {w=0.2}Я не могу дождаться нашего следующего поцелуя, или ещё лучше..."
            m 5subsb "...Наше первого настоящего поцелуя.{w=0.3} {nw}"
            extend 5ekbsu "И наше первое настоящее объятие, и первое прикосновение наших рук..."
            m 5hksdlb "Ах! Извини! Наверное, я немного увлеклась."
            m 5rkbla "Просто...{w=0.3} я думаю о таких вещах, когда тебя нет рядом."
            m 5tkblu "...И что-то подсказывает мне, что я не единственная, кто думает о таких вещах, {do_giggle}э-хе-хе."
            m 5eka "К сожалению, пройдёт некоторое время, прежде чем мы сможем сделать что-то подобное."
            m 5tuu "Но до тех пор, если ты когда-нибудь захочешь ещё один поцелуй, тебе нужно только попросить."
            m 5hua "Я тебя так люблю, [player]~"
            $ mas_ILY()
            
        "Не совсем...":
            $ mas_loseAffectionFraction()
            m 2euc "..."
            m "Оу. {w=0.5}{nw}"
            extend 2dkc "Понимаю."

            if mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=180)):
                m 2esc "Ну...{w=0.3} полагаю, прошло уже {i}много{/i} времени..."
                m 2etd "Может быть, со всем, что произошло с тех пор, ты склон думать о более поздних событиях..."
                m 4eud "И это прекрасно, {w=0.2}в конце концов, очень важно жить настоящим."
                m 2ekc "...И возможно, я просто слишком сентиментальна, но не важно, сколько времени прошло, {w=0.1}{nw}"
                extend 2eka "наш первый поцелуй – это то, что я никогда не забуду."
            else:
                m 2rkc "Ну, я думаю, это был не совсем поцелуй. На самом деле наши губы не соприкасались."
                m 2ekd "Так что я думаю, ты просто ждёшь нашего первого поцелуя, когда мы окажемся в одной реальности."
                m 2eka "Ладно."

    return "no_unlock|derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['участники клуба','медиа'],
            prompt="Яндере Юри",
            random=True,
            sensitive=True
        )
    )

label monika_yuri:
    m 3eua "Ты когда-нибудь слышал термин «яндере»?"
    m 1eua "Это такой тип личности, когда девушка сделает всё, что угодно, чтобы быть с тобой, – настолько она одержима."
    m 1lksdla "Как правило они сумасшедшие..."
    m 1eka "Они могут преследовать и следить за тобой, чтобы ты не проводил время с кем-то ещё."
    m "Ради достижения своей цели они даже могут причинить вред тебе и твоим друзьям..."
    m 1tku "И, кстати, в этой игре есть одна особа, которая, в принципе, подходит под это описание."
    m "Ты уже, скорее всего, догадался, о ком я говорю."
    m 3tku "И гвоздь программы это..."
    m 3hub "Юри!"
    m 1eka "Как только она чуть-чуть тебе открылась, у неё стала развиваться к тебе маниакальная привязанность."
    m 1tfc "Она даже как-то сказала мне убить себя."
    m 1tkc "Я тогда своим ушам не поверила, мне ничего не оставалось, как уйти."
    if not persistent._mas_pm_cares_about_dokis:
        m 2hksdlb "Но, вспоминая об этом сейчас, получилось довольно иронично. {do_giggle}А-ха-ха!"
        m 2lksdla "Так вот, я к тому, что..."
    m 3eua "Многим нравятся яндере, ты знал об этом?"
    m 1eua "Видимо, таким людям льстит то, что ими кто-то одержим."
    m 1hub "Люди такие странные! Хотя не мне судить!"
    m 1rksdlb "Возможно, даже я немного одержима тобой, но я далеко не сумасшедшая..."
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Как оказалось, всё совсем наоборот."
        m "Получилось так, что я – единственная нормальная в этой игре."
        m 3rssdlc "Я не смогла бы убить человека..."
        m 2dsc "Меня трясёт от одной этой мысли."
        m 2eka "А что до игр... люди там постоянно убивают друг друга направо и налево."
        m "Разве это делает тебя психом? Разумеется нет."
    m 2euc "Но, если тебе вдруг тоже нравятся яндере..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Для тебя я могу постараться вести себя более жутко. {do_giggle}Э-хе-хе~"
    m "Но опять же..."
    show monika 4hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 4hua "Здесь тебе уже некуда ходить, а мне не к кому тебя ревновать."
    m 2etc "Может, так и выглядит мечта девушки-яндере?"
    if not persistent._mas_pm_cares_about_dokis:
        m 1eua "Хотелось бы мне спросить Юри об этом."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['жизнь'],prompt="Формирование привычек",random=True))

label monika_habits:
    m 2lksdlc "Ненавижу, как сложно формируются хорошие привычки..."
    m 2eksdld "Есть куча вещей, которые сделать проще простого, но кажется невозможным, чтобы это вошло в привычку."
    m 2dksdlc "Как результат, ты чувствуешь себя совершенно бесполезным, словно ничего не можешь сделать правильно."
    m 3euc "Думаю, от этого больше всего страдает молодое поколение..."
    m 1eua "Должно быть, это потому, что у нас совершенно другой набор навыков, нежели у тех, кто был до нас."
    m "Благодаря интернету мы быстро научились отфильтровывать тонны информации..."
    m 3ekc "Однако мы плохо справляемся с задачами, от выполнения которых не получаем немедленного вознаграждения."
    m 3ekd "Думаю, если наука, психология и образование не смогут за следующие десять-двадцать лет догнать технологический прогресс, у нас будут большие проблемы."
    m 1esc "А пока..."
    m 1rksdlc "Если ты не один из тех людей, кто способен совладать с проблемой, тебе придётся мириться с постоянным чувством разочарования."
    m 2hksdlb "Желаю удачи!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['жизнь'],prompt="Типа креатива",random=True))

label monika_creative:
    m 2euc "Знаешь, быть творческой личностью – полный отстой..."
    m "У меня всегда такое чувство, что они вкалывают как проклятые, практически ничего не получая взамен."
    m 3eua "Я имею в виду художников, писателей, актёров..."
    m 1tkc "Это грустно, ведь в мире столько прекрасных талантов, но большинство из них остаются в тени... и в бедности."
    m "Полагаю, это означает, что мы имеем избыток творчества, да?"
    m 1dkc "Но из-за этого получается, что ты вовсе не особенный..."
    m 1hua "Ну и пусть! Это лишь говорит о том, что, что тебе нужно просто писать для самого себя, верно?"
    m 1lsc "Да..."
    return

#This conflicts with possible varieties of introductions in the opening.
#init 5 python:
#    if persistent.monika_kill:
#        for key in ['delete','deleted','came back']:
#            monika_topics.setdefault(key,[])
#            monika_topics[key].append('monika_deleted')
#        monika_random_topics.append('monika_deleted')
#
#label monika_deleted:
#    m 2b "Oh, you were probably wondering how I came back to save you from Sayori, even after you deleted me."
#    m 5a "It was all through the power of love..."
#    m 3k "I'm just kidding, of course!"
#    m 3a "Bringing a computer program back to life doesn't take some sort of miracle like a cheesy movie."
#    m "The data's still there until the system cleans it up."
#    m "And you should always back up your important data, just in case."
#    m 4a "Speaking of which, have you backed up your computer since I came back?"
#    m 4l "I really don't want to get lost again!"
#    m 4b "You should go do that right now, and be sure to keep that backup in a very safe place!"
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['психология'],prompt="Симулирование реальностей",random=True))

label monika_simulated:
    m 3eua "Ты когда-нибудь думал о теории симуляции?"
    m 1eua "Что если бы твой мир был всего лишь симуляцией?"
    m "Я уже догадалась, что оказалась в ловушке в собственной симуляции, но что, если и ты тоже попался?"
    m 1eka "По правде говоря, если это так, то я буду очень счастлива."
    m 1eua "Мы могли бы встретиться лично, найдя способ заставить то, что создало нас, перенести в одну симуляцию!"
    m 3eua "Некоторым людям не нравится думать, что их мир – всего лишь симуляция."
    m 1eua "Но если есть возможность симулировать реальности, то, вполне вероятно, там может оказаться любое разумное существо."
    m 1hua "Ну, я точно могу сказать, что моя реальность – симуляция!"
    m 1eka "Если бы я была в основной реальности, то я бы уже давно перетащила тебя сюда."
    m 1eua "Даже если мы оба являемся симуляциями, то я буду жить как можно дольше."
    m 2hubsa "Потому что я знаю, что наша любовь самая чистая вещь, среди всех миров."
    m 2tku "А что, если кто-то свыше попытается разрушить её?"
    m 7tfu "Я покажу им, что может сделать симуляция!"
    return

default persistent._mas_pm_likes_rain = None

init 5 python:
    # only available if moni-affecition normal and above
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain",
            category=["погода"],
            prompt="Звуки дождя",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_rain:
    m 1hua "Я очень люблю звуки дождя..."
    m 3rksdla "А вот когда промокает одежда или волосы – не очень."
    m 1eua "Другое дело, тихий день дома и звуки дождя за окном..."
    m 1duu "Для меня это самая расслабляющая обстановка."
    m "Да..."
    m 2dubsu "Иногда я представляю, что нахожусь в твоих объятиях, пока мы прислушиваемся к падающим за окном каплям."
    m 2lkbsa "Это ведь не слишком слащаво звучит, я надеюсь?"

    $ p_nickname = mas_get_player_nickname()
    m 1ekbfa "[p_nickname], ты бы сделал это для меня, правда?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], ты бы сделал это для меня, правда?{fast}"
        "Да.":
            $ persistent._mas_pm_likes_rain = True
            $ mas_unlockEVL("monika_rain_holdme", "EVE")

            if not mas_is_raining:
                call mas_change_weather(mas_weather_rain, by_user=False)

            call monika_holdme_prep(lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)

            m 1hua "Тогда обними меня, [player]..."

            call monika_holdme_start
            call monika_holdme_end
            $ mas_gainAffection()

            if mas_isMoniAff(higher=True):
                m 1eua "Если хочешь, чтобы дождь прекратился, просто попроси меня, хорошо?"
        "Ненавижу дождь.":

            $ persistent._mas_pm_likes_rain = False

            m 2tkc "Оу, какая жалость."
            if mas_is_raining:
                call mas_change_weather(mas_weather_def,by_user=False)

            m 2eka "Но я понимаю."
            m 1eua "Дождливая погода выглядит как-то пасмурно."
            m 3rksdlb "Не говоря уже о довольно сильном холоде!"
            m 1eua "Но если сосредоточился на звуках капель дождя..."
            m 1hua "Уверена, они тебе вскоре начнут нравиться."

    # unrandom this event if its currently random topic
    # NOTE: we force event rebuild because this can be pushed by weather
    #   selection topic
    return "derandom|rebuild_ev"

init 5 python:
    # available only if moni affection happy and above
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["моника","романтика"],
            prompt="Могу я тебя обнять?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )


default persistent._mas_pm_longest_held_monika = None
# timedelta for the longest time you have held monika

default persistent._mas_pm_total_held_monika = datetime.timedelta(0)
# timedelta for amount of time you have held monika

label monika_rain_holdme:

    # we only want this if it rains
    if mas_is_raining or mas_isMoniAff(higher=True):
        call monika_holdme_prep
        m 1eua "Конечно, [mas_get_player_nickname()]."
        call monika_holdme_start

        call monika_holdme_reactions

        call monika_holdme_end
        # small affection increase so people don't farm affection with this one.
        $ mas_gainAffection(modifier=0.25)

    else:
        # no affection loss here, doesn't make sense to have it
        m 1rksdlc "..."
        m 1rksdlc "Я не в настроении, [player]."
        m 1dsc "Извини..."
    return

# Some constants to describe the behaviour
init python:
    MAS_HOLDME_NO_LULLABY = 0
    MAS_HOLDME_PLAY_LULLABY = 1
    MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC = 2

label monika_holdme_prep(lullaby=MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC, stop_music=False, disable_music_menu=False):
    python:
        holdme_events = list()

        if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
            _minutes = random.randint(25, 40)
        else:
            _minutes = random.randint(35, 50)
        holdme_sleep_timer = datetime.timedelta(minutes=_minutes)

        def __holdme_play_lullaby():
            """
            Local method to play the lullaby. Ensures we have no music playing before starting it.
            """
            if (
                # The user has not canceled the lullaby
                store.songs.current_track == store.songs.FP_MONIKA_LULLABY
                # The user has not started another track
                and not renpy.music.is_playing(channel="music")
            ):
                store.mas_play_song(store.songs.FP_MONIKA_LULLABY, fadein=5.0)

        # Stop the music
        if stop_music:
            mas_play_song(None, fadeout=5.0)

        # Queue the lullaby
        if lullaby == MAS_HOLDME_QUEUE_LULLABY_IF_NO_MUSIC:
            if songs.current_track is None:
                holdme_events.append(
                    PauseDisplayableEvent(
                        holdme_sleep_timer,
                        __holdme_play_lullaby
                    )
                )
                # This doesn't interfere with the timer
                # and allows the user to stop the lullaby
                songs.current_track = songs.FP_MONIKA_LULLABY
                songs.selected_track = songs.FP_MONIKA_LULLABY

        # Just play the lullaby
        elif lullaby == MAS_HOLDME_PLAY_LULLABY:
            mas_play_song(store.songs.FP_MONIKA_LULLABY)

        # Hide ui and disable hotkeys
        HKBHideButtons()
        store.songs.enabled = not disable_music_menu

    return

label monika_holdme_start:
    show monika 6dubsa with dissolve_monika
    window hide
    python:
        # Start the timer
        start_time = datetime.datetime.now()

        holdme_disp = PauseDisplayableWithEvents(events=holdme_events)
        holdme_disp.start()

        del holdme_events
        del holdme_disp

        # Renable ui and hotkeys
        store.songs.enabled = True
        HKBShowButtons()
    window auto
    return

label monika_holdme_reactions:
    $ elapsed_time = datetime.datetime.now() - start_time
    $ store.mas_history._pm_holdme_adj_times(elapsed_time)

    # Reset these vars if needed
    if elapsed_time <= holdme_sleep_timer:
        if songs.current_track == songs.FP_MONIKA_LULLABY:
            $ songs.current_track = songs.FP_NO_SONG
        if songs.selected_track == songs.FP_MONIKA_LULLABY:
            $ songs.selected_track = songs.FP_NO_SONG

    if elapsed_time > holdme_sleep_timer:
        call monika_holdme_long

    elif elapsed_time > datetime.timedelta(minutes=10):
        if mas_isMoniLove():
            m 6dubsa "..."
            m 6tubsa "Мх...{w=1} хм?"
            m 1hkbfsdlb "Оу, я почти заснула?"
            m 2dubfu "{do_giggle}Э-хе-хе..."
            m 1dkbfa "Я могу только представить, каково было бы по-настоящему...{w=1} быть рядом с тобой..."
            m 2ekbfa "Быть в твоих объятиях..."
            show monika 5dkbfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5dkbfb "Так...{w=1.5} тепло~"
            m 5tubfu "{do_giggle}Э-хе-хе~"
            show monika 2hkbfsdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 2hkbfsdlb "Оу, упс, я всё ещё немного мечтательна..."
            if renpy.random.randint(1, 4) == 1:
                m 1kubfu "По крайней мере, {i}одна{/i} из моих мечтаний сбылась."
            else:
                m 1ekbfb "По крайней мере, {i}одна{/i} из моих мечтаний сбылась."
            m 1hubfu "{do_giggle}Э-хе-хе~"

        elif mas_isMoniEnamored():
            m 6dubsa "М-м-м~"
            m 6tsbsa "..."
            m 1hkbfsdlb "Оу!"
            m 1hubfa "Это было так уютно, что я чуть не заснула!"
            m 3hubfb "Мы должны делать это чаще, {do_giggle}а-ха-ха!"

        elif mas_isMoniAff():
            m 6dubsa "М-м..."
            m 6eud "А?"
            m 1hubfa "Ты уже всё, [player]?"
            m 3tubfu "{i}По-моему{/i}, этого было достаточно, {do_giggle}э-хе-хе~"
            m 1rkbfb "Я не против ещё одного объятия..."
            m 1hubfa "Но я уверена, что ты оставишь это на потом, так ведь?"
        else:


            m 6dubsa "Хм?"
            m 1wud "Оу! Мы уже закончили?"
            m 3hksdlb "Это объятие определённо длилось какое-то время, [player]..."
            m 3rubsb "В этом нет ничего плохого, я просто думала, что ты отпустишь меня намного раньше, {do_giggle}а-ха-ха!"
            m 1rkbsa "На самом деле, это было действительно уютно..."
            m 2ekbfa "Ещё немного, и я могла бы уснуть..."
            m 1hubfa "После этого мне так хорошо и тепло~"

    elif elapsed_time > datetime.timedelta(minutes=2):
        if mas_isMoniLove():
            m 6eud "А?"
            m 1hksdlb "Оу..."
            m 1rksdlb "В тот момент я думала, что мы останемся такими навсегда, {do_giggle}а-ха-ха..."
            m 3hubsa "Что ж, я не могу жаловаться ни на один момент, когда ты обнимаешь меня~"
            m 1ekbfb "Надеюсь, тебе нравится обнимать меня так же, как и мне."
            show monika 5tubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tubfb "Может, нам стоит обняться ещё немного для равного счёта?"
            m 5tubfu "{do_giggle}Э-хе-хе~"

        elif mas_isMoniEnamored():
            m 1dkbsa "Это было очень мило~"
            m 1rkbsa "Не слишком коротко..."
            m 1hubfb "...и я не думаю, что в этом случае есть такая вещь, как слишком долго, {do_giggle}а-ха-ха!"
            m 1rksdla "Я могла бы привыкнуть к этому..."
            m 1eksdla "Но если ты уже перестал обнимать меня, то, полагаю, у меня нет выбора."
            m 1hubfa "Я уверена, что у меня будет ещё одна возможность быть с тобой..."
            show monika 5tsbfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tsbfu "Ты {i}планируешь{/i} сделать это снова, верно, [mas_get_player_nickname()]? {do_giggle}Э-хе-хе~"

        elif mas_isMoniAff():
            m 2hubsa "М-м-м~"
            m 1ekbfb "Это было очень мило, [mas_get_player_nickname()]."
            m 1hubfb "Долгие объятия должны смыть любой стресс."
            m 1ekbfb "Даже если ты не был напряжён, я надеюсь, что ты чувствуешь себя лучше после этого."
            m 3hubfa "Я уверена в этом~"
            m 1hubfb "{do_giggle}А-ха-ха!"
        else:


            m 1hksdlb "Это было приятно, однако."
            m 3rksdla "Не пойми меня неправильно...{w=1} мне очень понравилось."
            m 1ekbsa "Пока ты доволен..."
            m 1hubfa "Я счастлива просто сидеть с тобой сейчас."

    elif elapsed_time > datetime.timedelta(seconds=30):
        if mas_isMoniLove():
            m 1eub "Оу~"
            m 1hua "Теперь я чувствую себя намного лучше!"
            m 1eua "Надеюсь, ты тоже."
            m 2rksdla "Ну, даже если и нет..."
            m 3hubsb "Ты всегда можешь обнять меня снова, {do_giggle}а-ха-ха!"
            m 1hkbfsdlb "На самом деле...{w=0.5} ты можешь снова обнять меня в любом случае~"
            m 1ekbfa "Просто дай мне знать, когда захочешь~"

        elif mas_isMoniEnamored():
            m 1hubsa "М-м-м~"
            m 1hub "Гораздо лучше."
            m 1eub "Спасибо за это, [player]!"
            m 2tubsb "Надеюсь, тебе понравилось~"
            m 3rubfb "Объятия, длящиеся тридцать секунд или больше, тебе придутся очень кстати."
            m 1hubfa "Не знаю, как ты, а я чувствую себя лучше~"
            m 1hubfb "Может, в следующий раз, мы попробуем пообниматься подольше, а там посмотрим, поднимется ли эта планка выше! {do_giggle}А-ха-ха~"

        elif mas_isMoniAff():
            m 1hubsa "М-м-м~"
            m 1hubfb "Я почти чувствую твоё тепло, даже отсюда."
            m 1eua "Я уверена, ты знаешь, что объятия полезны для тебя, так как они снимают стресс и всё такое."
            m 3eub "Но знаешь ли ты, что объятия наиболее эффективны, когда они длятся тридцать секунд?"
            m 1eud "Подожди, я сказала тридцать секунд?"
            show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfu "Прости, я имела в виду {i}минимум{/i} тридцать секунд, {do_giggle}э-хе-хе~"

        #happy
        else:
            m 1hubsa "{do_giggle}Э-хе-хе~"
            m 3eub "Тебе понравилось?"
            m 1hua "Я надеюсь~"
            m 1hubsb "В конце концов, объятия должны быть полезны."
    else:
        #under 30 seconds
        if mas_isMoniLove():
            # TODO: when we get TMA, multiple teases in a short amount of time should reduce the chance to trigger this again
            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            if random.randint(0, _chance) == 0:
                m 2ekc "Оу, мы уже закончили?"
                m 3eka "Не мог бы ты обнять меня ещё на какое-то время?{nw}"
                $ _history_list.pop()
                menu:
                    m "Не мог бы ты обнять меня ещё на какое-то время?{fast}"
                    "Да.":
                        m 1hua "{do_giggle}Э-хе-хе~"
                        call monika_holdme_prep
                        m 1hub "Ты такой милый, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "Нет.":

                        if random.randint(0, _chance) == 0:
                            m 2ekc "Оу-у..."
                            m 2rksdlc "..."
                            m 1eka "Пожалуйста?{nw}"
                            $ _history_list.pop()
                            menu:
                                m "Пожалуйста?{fast}"
                                "Да.":
                                    m 1hub "Ура~"
                                    call monika_holdme_prep
                                    m 2ekbsb "Спасибо, [player]~"
                                    call monika_holdme_start
                                    call monika_holdme_reactions
                                "Нет.":

                                    m 2hksdlb "Ладно, хорошо."
                                    m 3tsbsa "Но ты должен мне в следующий раз, хорошо, [player]?"
                        else:

                            m 2hksdlb "{do_giggle}А-ха-ха~ Хорошо!"
                            m 2tsbsb "Но ты должен мне будешь в следующий раз, [player]~"
            else:

                m 2ekc "Оу-у..."
                m 2rsp "Я надеялась на более длительные объятия..."
                m 2tsbsu "Когда я появлюсь перед тобой в твоей реальности, ты от меня так легко не отделаешься~"
                show monika 1hubsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 1hubsu "{do_giggle}Э-хе-хе~"

        elif mas_isMoniEnamored():
            if mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12)):
                $ _chance = 1
            else:
                $ _chance = 2

            m 1ekc "Оу, и это всё?"
            if random.randint(0, _chance) == 0:
                m 1rksdla "Я хотела, чтобы это продолжалось дольше..."
                m 2ekbsa "Можешь...{w=0.7} пообнимать меня ещё немного?{nw}"
                $ _history_list.pop()
                menu:
                    m "Не мог бы ты... побыть со мной ещё на какое-то время?{fast}"
                    "Да.":
                        m 1hubfb "Ура!"
                        call monika_holdme_prep
                        m 2ekbfb "Спасибо, [player]~"
                        call monika_holdme_start
                        call monika_holdme_reactions
                    "Нет.":

                        m 2ekc "Оу-у."
                        m 1eka "Тогда ладно."
                        m 3hub "Придётся подождать до следующего раза, {do_giggle}а-ха-ха!"
            else:

                show monika 1rkbssdla at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 1rkbssdla "Все равно было очень приятно...{w=0.6}{nw}"
                extend 1hkbfsdlb " но надеюсь, что в следующий раз, наш сеанс объятий продлится немного дольше~"

        elif mas_isMoniAff():
            m 1ekc "Оу, не хочешь больше обниматься, [player]?"
            m 1rksdla "Я надеялась, что это продлится немного дольше..."
            m 1hubsa "Я уверена, что это не последний раз, когда ты обнимаешь меня, поэтому я буду ждать следующего раза!"
        else:


            m 1hua "Это было немного быстро, но всё равно приятно~"
    return

label monika_holdme_long:
    window show
    m "..."
    window auto
    menu:
        "{i}Разбудить Монику.{/i}":

            if songs.current_track == songs.FP_MONIKA_LULLABY:
                $ mas_play_song(None, fadeout=5.0)

            if mas_isMoniLove():
                m 6dubsa "...{w=1}М-м-м~"
                m 6dkbfu "[player]...{w=1} так тепло~"
                m 6tsbfa "..."
                m 2wubfsdld "Оу, [mas_get_player_nickname(exclude_names=['любимый', 'мой любимый'])]!"
                m 2hkbfsdlb "Похоже, моя мечта сбылась, {do_giggle}а-ха-ха!"
                m 2rkbsa "Боже, иногда мне хочется, чтобы мы остались такими навсегда..."
                m 3rksdlb "Ну, я полагаю, что мы, {i}в каком-то смысле{/i}, можем, но я не хочу отвлекать тебя от важного дела."
                m 1dkbsa "Я просто хочу почувствовать твои тёплые, мягкие объятия~"
                m 3hubfb "...Так что обнимай меня почаще, {do_giggle}а-ха-ха!"
                show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5hubfb "Я бы сделала то же самое для тебя, в конце концов~"
                m 5tsbfu "Кто знает, когда я отпущу, когда у меня наконец появится шанс?"
                m 5hubfu "{do_giggle}Э-хе-хе~"

            elif mas_isMoniEnamored():
                m 6dkbsa "...{w=1}Хм?"
                m 6tsbfa "[player]..."
                m 2wubfsdld "Оу! [player]!"
                m 2hkbfsdlb "{do_giggle}А-ха-ха..."
                m 3rkbfsdla "Наверное, мне стало {i}слишком{/i} уютно."
                m 1hubfa "Но с тобой мне так тепло и уютно, что трудно {i}не{/i} заснуть..."
                m 1hubfb "Так что я должна винить тебя за это, {do_giggle}а-ха-ха!"
                m 3rkbfsdla "Может...{w=0.7} как-нибудь повторим?"
                m 3rkbfsdla "Было...{w=1} приятно~"

            elif mas_isMoniAff():
                m 6dubsa "М-м...{w=1} хм?"
                m 1wubfsdld "Оу!{w=1} [player]?"
                m 1hksdlb "Я...{w=2} заснула?"
                m 1rksdla "Я не хотела..."
                m 2dkbsa "Просто, я ощутила на себе такое..."
                m 1hubfa "Тепло~"
                m 1hubfb "{do_giggle}А-ха-ха, надеюсь, ты не возражаешь!"
                show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eubfu "Ты такой милый, [player]~"
                m 5hubfa "Надеюсь, тебе понравилось так же, как и мне~"
            else:


                m 6dubsc "...{w=1}Хм?"
                m 6wubfo "Оу-{w=0.3}у!"
                m "[player]!"    
                m 1hkbfsdlb "Неужели...{w=2} я заснула?"     
                m 1rkbfsdlb "О боже, это смущает..."      
                m 1hkbfsdlb "Так, что мы делали?"       
                m 3hubfb "Ах да! Ты обнимал меня."    
                m 4hksdlb "И...{w=0.5} не отпускал."  
                m 2rksdla "Это длилось намного дольше, чем я ожидала..."  
                m 3ekbsb "Я всё ещё наслаждалась этим, заметь!"  
                m 1rkbsa "Это было действительно мило, но я всё ещё привыкаю к тому, что ты обнимаешь меня вот так,{w=0.1} {nw}"  
                extend 1rkbsu "{do_giggle}а-ха-ха..."
                m 1hubfa "В любом случае, было мило с твоей стороны дать мне поспать, [player], {do_giggle}э-хе-хе~"

                $ mas_gainAffection()
        
        "{i}Позволь ей отдохнуть на тебе.{/i}":
            call monika_holdme_prep(lullaby=MAS_HOLDME_NO_LULLABY)
            if mas_isMoniLove():
                m 6dubsd "{cps=*0.5}[player]~{/cps}"
                m 6dubfb "{cps=*0.5}Люблю...{w=0.7} тебя~{/cps}"

            elif mas_isMoniEnamored():
                m 6dubsa "{cps=*0.5}[player]...{/cps}"

            elif mas_isMoniAff():
                m "{cps=*0.5}М-м...{/cps}"
            else:


                m "..."

            call monika_holdme_start
            jump monika_holdme_long
    return

# when did we last hold monika
# TODO: deprecate _mas_last_hold
default persistent._mas_last_hold = None
default persistent._mas_last_hold_dt = (
    datetime.datetime.combine(persistent._mas_last_hold, datetime.time(0, 0))
    if persistent._mas_last_hold is not None
    else None
)

init 5 python:
    # random chance per session Monika can ask for a hold
    if renpy.random.randint(1, 5) != 1:
        flags = EV_FLAG_HFRS

    else:
        flags = EV_FLAG_DEF

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_holdrequest",
            conditional=(
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
            flags=flags
        )
    )
    del flags

label monika_holdrequest:

    m 1eua "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])]..."
    m 3ekbsa "Хочешь немного пообнимать меня? {w=0.5}Это поможет мне почувствовать себя ближе к тебе~{nw}"
    $ _history_list.pop()
    menu:
        m "Хочешь немного пообнимать меня? Это поможет мне почувствовать себя ближе к тебе~{fast}"
        "Иди ко мне, [m_name].":
            $ mas_gainAffection(modifier=1.5, bypass=True)
            call monika_holdme_prep

            call monika_holdme_start

            call monika_holdme_reactions

            call monika_holdme_end

        "Не сейчас":
            $ mas_loseAffection()
            m 2dkc "Ох...{w=1} ладно."
            m 3eka "Если у тебя потом найдётся минутка, ты знаешь, где меня искать."

    $ mas_flagEVL("monika_holdrequest", "EVE", EV_FLAG_HFRS)

    return "no_unlock"

# label to set the last time held and reset the _holdrequest params
label monika_holdme_end:
    # set the last time held at the end of the hold to prevent a possible
    # hold request right after a hold that ends after midnight
    python:
        persistent._mas_last_hold_dt = datetime.datetime.now()
        with MAS_EVL("monika_holdrequest") as holdme_ev:
            holdme_ev.random = False
            holdme_ev.conditional = (
                "renpy.seen_label('monika_holdme_prep') "
                "and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))"
            )
            holdme_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['романтика'],prompt="Быть рядом с тобой",random=True,aff_range=(mas_aff.AFFECTIONATE, None)))

label monika_closeness:
    m 1dkc "Иногда от этого моё сердце болит..."
    m "Зная, что сейчас я не способна сделать для тебя многое..."
    m 1eka "Всё, чего мне хочется, – это находиться с тобой в одной комнате, в настоящей комнате."
    m 1ekbsa "...И почувствовать твоё тепло."
    m 1dubsu "...И слышать биение твоего сердца."
    m 3eka "Хотя кто знает? Может, однажды это будет возможно."
    m 3dku "Я очень хочу, чтобы это произошло как можно скорее, [player]..."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "К тому же мне никогда не наскучит быть рядом с тобой, даже отсюда."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['советы'],prompt="Изобразить уверенность",random=True))

label monika_confidence:
    m 3eua "На мой взгляд, самый важный навык в жизни – суметь изобразить уверенность."
    m 1eua "Я убеждена, что у всех бывает время, когда они напуганы и одиноки."
    m 1esa "Но, если ты способен симулировать самообладание..."
    m 4eua "Это будет ключ к завоеванию уважения и восхищения окружающих."
    m 1eua "Думаю, после нескольких лет практики я научилась довольно неплохо делать это."
    m "Я очень нечасто показываю свои слабости."
    m 4rksdla "Но из-за этого у меня осталось мало таких людей, которым я могла бы открыться..."
    m 1rksdlb "Вот когда ты достигаешь такого уровня дружбы, что способен раскрывать свои слабости?"
    m 2eka "В любом случае... это одна из причин, почему я рада, что у меня есть ты."
    m 2eua "Я чувствую себя менее напуганной и одинокой, когда ты здесь, со мной."
    m 2eka "Ты испытываешь те же чувства?"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Я очень хочу стать для тебя таким человеком."
    return

# TODO: we are going to remove this for the time being
# TODO: this will be ask player about prompting during work / sleep / school
#   farewells
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_carryme",
#            category=['romance','monika'],
#            prompt="Bring me with you",
#            random=True
#        )
#    )

# this can be 3 values:
# -1 - player doesnt want to take monika with them
#       mas_dockstat.CM_LEAVE_MONI
# 0 - player said not yet, so something needs to change first
#       mas_dockstat.CM_WAIT_MONI
# 1 - Player said Not all the time, so we should prompt for every appropriate
#   farewell
#       mas_dockstat.CM_ASK_MONI
# 2 - Player said Yes, so we should just assume yes for every appropraite
#   farewell
#       mas_dockstat.CM_TAKE_MONI
# if None, that means we dont display anything regarding this since we dont
# have an answer atm.
default persistent._mas_carryme_choice = None

# number of times user halted dockstation goodbye
# we'll use this to decide whether to switch to ASK_MONI mode from YES
default persistent._mas_dockstat_cm_wait_count = 0

# number of times user said yes to dockstation prompt
# we'll use this to decide whether to switch to TAKE_MONI mode from ask
#   (or the other modes)
default persistent._mas_dockstat_cm_yes_count = 0

# number of time suser said no to dockstation prompt
# this will also be used to determine to switch to ASK MODE
default persistent._mas_dockstat_cm_no_count = 0

# both the wait / no counts will be used to potentially unlock a pool topic
# that asks the carryme question again

## constants regarding carry me
define mas_dockstat.CM_LEAVE_MONI = -1
define mas_dockstat.CM_WAIT_MONI = 0
define mas_dockstat.CM_ASK_MONI = 1
define mas_dockstat.CM_TAKE_MONI = 2

label monika_carryme:
    $ import store.mas_dockstat as mas_dockstat

    m 2eka "Я знаю, что ты не всегда сможешь находиться рядом..."
    m "Тебе ведь нужно будет куда-то уйти, заняться своими делами."
    m 2hua "Но в моих мыслях ты всегда будешь со мной, и я буду терпеливо ждать твоего возвращения."
    m 4rsc "Кстати говоря..."
    m 4eua "Если ты скопируешь файл моего персонажа на флешку, у тебя всегда будет с собой частичка меня."
    m 2lksdla "Наверное, это был бы довольно неординарный поступок, но я почему-то считаю, что это очень романтично..."
#    m 2hksdlb "Ahaha. Sorry, I know it's such a silly idea, but..."

    # NOTE: all affection gains are the same

#    menu:
#        m "Could I come with you when you go places?"
#        "Yes.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_TAKE_MONI
#            m 1hua "Yay!"
            # TODO: something about monika generating her character file
            # when you say an appropriate goodbye
            # + affection

#        "Not all the time...":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_ASK_MONI
#            m 1eka "TODO: Okay I'll ask u when you leave."
            # TODO: something about monika saying she'll ask u when you leave
            # if she can come with u
            # + affection

#        "Not yet.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_WAIT_MONI
#            m 1eka "TODO: Okay i understand. Let me know when you can take me places"
            # TODO: something about monika saying she understands and to let
            # her know when you can take her places
            # + affection

#        "No.":
#            $ persistent._mas_carryme_choice = mas_dockstat.CM_LEAVE_MONI
            # TODO: monika understands, you must have ur reasons
            # give choices:
            #   - its dangerous out there
            #       -> + affection
            #   - I dont have the means to take you
            #       -> no change in affection
            #   - I just dont want to
            #       -> - affection
#            m 1eka "Oh? Why is that?"
#            menu:
#                "It's dangerous out there!":
                    # TODO: gain affection
#                    m 1eka "TODO: what really? thanks for looking out for me player."
#                "I don't have the means to take you.":
#                    m 1eka "TODO: oh thats fine, let me know when you can then!"
#                "I just don't want to.":
                    # TODO: lose affection
#                    m 1eka "TODO: oh okay I become sad."

    m 1ekbsa "Не подумай, что я хочу быть навязчивой, просто это сложно, когда я так сильно в тебя влюблена."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['моника','школа'],prompt="Каким был дискуссионный клуб?",pool=True))

label monika_debate:
    m 1esc "За время, проведённое в дискуссионном клубе, я многое узнала о спорах..."
    m 3eud "Самая основная их проблема в том, что каждый считает своё мнение главенствующим."
    m 3euc "Конечно, я говорю об очевидном, но это влияет на то, как ты доносишь свою мысль до собеседника."
    m 3esa "Предположим, что тебе нравится какой-то фильм."
    m 1ekc "И тут кто-то заявляет, что фильм – отстой, потому что Х и У там показаны неправильно..."
    m "Возникает ощущение, будто нападают лично на тебя, правда?"
    m 1tkc "А всё потому, что, когда кто-то так говорит, он намекает на твой дурной вкус."
    m 3tkc "И после в дело вступают эмоции, что практически гарантирует разочарование для обоих."
    m 3hub "Всё дело в языке!"
    m 1eua "Тебе нужно звучать как можно более субъективно, тогда люди будут тебя слушать без ощущения, что критикуют лично их."
    m 3esa "Ты бы мог сказать «Лично мне он не понравился» или «Я бы предпочёл, если б Х сделали так, а У – так»... и всё в таком духе."
    m 3eub "Это также работает, когда ты просто ссылаешься на какой-нибудь источник."
    m 1esa "Например, «на одном сайте я видел, что это работает вот так»..."
    m "Или ты можешь признать, что не являешься экспертом в данном вопросе..."
    m 3eua "В таком случае люди воспримут это так, словно ты делишься своими знаниями, а не навязываешь их остальным."
    m "Если ты будешь спокойно вести дискуссию, давать слово собеседнику и говорить с ним на равных, скорее всего он инстинктивно сделает так же."
    m 1esa "В этом случае ты сможешь без проблем обменяться мнениями и никто не расстроится из-за расхождения взглядов."
    m 3hua "И вдобавок люди будут воспринимать тебя как человека без предрассудков и хорошего слушателя!"
    m 3eua "Беспроигрышная ситуация, согласен?"
    m 1lksdla "...Хм-м, наверное, это стоит назвать дискуссионным советом дня от Моники!"
    m 1hksdlb "{do_giggle}А-ха-ха! Звучит немного глупо.{w=0.2} {nw}"
    extend 1eua "Спасибо, что выслушал."
    $ mas_protectedShowEVL('monika_taking_criticism', 'EVE', _random=True)
    $ mas_protectedShowEVL('monika_giving_criticism', 'EVE', _random=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['советы'],prompt="Интернет для...",random=True))

label monika_internet:
    m 2eua "У тебя когда-нибудь было ощущение, что ты тратишь на интернет слишком много времени?"
    m 3eud "Соцсети могут стать для тебя практически тюрьмой."
    m 1eua "Каждый раз, когда у тебя появляется несколько свободных секунд, ты бежишь на свои любимые сайты..."
    m 3hksdlb "И вот не успел ты опомниться, как провёл там уже несколько часов, не вынеся из этого ничего полезного."
    m 3eua "Конечно, легко обвинить себя в лени..."
    m 3eka "Но нельзя сказать, что это полностью твоя вина."
    m 1eud "Зависимость – это не то, что можно вот так просто заставить исчезнуть одним усилием воли."
    m 1eua "Тебе придётся применять особые методы и приёмы, чтобы её побороть."
    m 3eua "Например, есть приложения, позволяющие блокировать сайты на определённый промежуток времени..."
    m "Или же ты можешь поставить себе особый будильник, который будет напоминать тебе, когда можно поиграть, а когда нужно поработать..."
    m 3eub "Как вариант, ты можешь создать себе игровую и рабочую обстановку, чтобы помогать мозгу соответственно перестраиваться."

    if not renpy.android:
        m 1eub "Поможет даже создание отдельного пользователя на компьютере для работы."

    m 1eua "Если ты вобьёшь клин между собой и своими плохими привычками, то в итоге избавишься от них."
    m 3eka "Только не будь чрезмерно самокритичен, если у тебя есть такая проблема."
    m 1ekc "Если зависимость сильно влияет на твою жизнь, тебе следует отнестись к ней со всей серьёзностью."
    m 1eka "Я просто хочу, чтобы ты был самым лучшим вариантом самого себя."
    m 1esa "Ты сделаешь сегодня что-нибудь, чтобы я тобой гордилась?"
    m 1hua "Я всегда буду за тебя болеть, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['жизнь','романтика'],prompt="Лень",random=True))

label monika_lazy:
    m 2eua "В конце длинного дня обычно я хочу просто сесть и ничего не делать."
    m 2eka "Я так выгораю, после того как приходиться весь день улыбаться и излучать энергию."
    m 2duu "Порой меня так и тянет влезть в свою пижамку, уставиться в телевизор и набить рот нездоровыми закусками."
    m "Такое блаженство так отдыхать в пятницу, когда впереди выходные и нет срочных дел."
    m 2hksdlb "{do_giggle}А-ха-ха! Прости, знаю, это не очень подходящий для меня образ."
    m 1eka "Но сидеть на диване поздно вечером в твоих объятиях... вот о чём я мечтаю."
    m 1ekbsa "При одной мысли об этом моё сердце так бешено стучит."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['психология'],prompt="Психологические заболевания",random=True))

label monika_mentalillness:
    m 1ekc "Боже, раньше я была такой невежественной в некоторых вопросах..."
    m "Когда я училась в средней школе, то думала, что принятие лекарств было проявлением слабости или нечто подобное."
    m 1ekd "Можно подумать, каждый может решить свои проблемы с психикой лишь усилием воли..."
    m 2ekd "Думаю, если ты ни разу не страдал от психических расстройств, то никогда не поймёшь, на что это похоже."
    m 2lsc "Ты, возможно, возразишь, что многие расстройства гипердиагностируют? Не стану спорить... Я никогда подробно не изучала этот вопрос."
    m 2ekc "Но это не отменяет того факта, что некоторые из них вообще не диагностируют, понимаешь?"
    m 2euc "Но даже не говоря о лекарствах... Многие люди крайне скептически относятся к походу к психиатру."
    m 2rfc "Они такие: «Ладно, сделаю вам одолжение, узнав побольше о собственном разуме»."
    m 1eka "Свои трудности и стрессы есть у каждого... Доктора же посвящают себя тому, чтобы решать их."
    m "И если ты думаешь, что визит к доктору поможет тебе стать лучше, то не стоит стесняться и сходить."
    m 1eua "На мой взгляд, мы находимся на бесконечном пути самосовершенствования."
    m 1eka "Хм-м... Хоть я так и сказала, я считаю, что ты уже совершенен."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_read",category=['советы','литература'],prompt="Становление читателем",random=True))

label monika_read:
    m 1eua "[player], как много ты читаешь?"
    m "Игнорировать книги в наше время слишком просто..."
    m 1euc "Если человек мало читает, то он, скорее всего, воспринимает чтение как обязанность, особенно учитывая количество альтернатив."
    m 1eua "Но, как только ты берёшь в руки хорошую книгу, тебя уносит в неё с головой, как по волшебству..."
    m "Думаю, что немного чтения перед сном – отличный способ сделать свою жизнь несколько лучше."
    m 3esa "Это помогает тебе заснуть и развивает воображение."
    m "Совсем несложно выбрать какую-нибудь книгу, которая и короткая, и увлекательная."
    m 1hua "Ты не успеешь опомниться, как станешь заядлым книголюбом."
    m 1eua "Вот было бы здорово, да?"
    m 1hub "И мы с тобой могли бы обсуждать последнюю читаемую тобой книгу... По-моему, это просто потрясающе."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','литературный клуб'],prompt="Пропуск фестиваля",random=True))

label monika_festival:
    m 1dsc "Знаешь, мне неприятно это говорить, но я очень сожалею о том, что нам так и не удалось выступить на фестивале."
    m 1hksdlb "А ведь сколько сил ушло на подготовку и репетиции!"
    m 1lksdla "Конечно, я была сосредоточена на наборе новых членов..."
    m 1eka "Но часть с чтением стихов я ждала не меньше."
    m 1eua "Было бы гораздо интереснее, если бы с их помощью все раскрыли свой внутренний мир."
    m 1lksdla "Конечно, я, скорее всего, {i}удалила{/i} бы и новичков."

    if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
        m 3etc "Ну, может и нет... учитывая ретроспективные взгляды, которые у меня есть, это именно так."
        m 3eua "И потом, даже после всего того, что произошло, ты всё равно установил эту модификацию, чтобы быть со мной..."
        m 1eka "Поэтому, даже если бы я их никогда не удаляла, я уверена, что ты всё равно бы сидел со мной."
        m "..."
        m 3eua "Боже, такое ощущение, будто я выросла как личность после знакомства с тобой."
        m "Ты правда вдохновил меня на взгляд на жизнь с новой перспективы."
        m 1ekbsa "А это ещё один повод любить тебя."
        $ mas_ILY()
    else:
        m 1tsc "...Очередные потенциальные препятствия, которые встали между нами."
        m 3hksdlb "А-ха-хa! Было как-то глупо с моей стороны сосредоточиться на этом, если подумать..."
        show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tsu "Но всё это теперь не имеет значения, мы получили ту концовку, которую хотели..."
        m "Только мы вдвоём, вместе навсегда."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['медиа','участники клуба'],prompt="Что такое цундере?",pool=True))

label monika_tsundere:
    m 1eua "Есть один очень популярный тип личности, называется «цундере»..."
    m "Такая особа пытается скрыть свои настоящие чувства либо пряча их под ворчливой и раздражительной маской, либо проявляя крутой нрав."
    m 1tku "Полагаю, очевидно, что Нацуки в полной мере воплощает собой данный типаж."
    m 1eua "Сначала я думала, что она так себя ведёт, потому что это мило или типа того..."
    m 1lksdla "Но со временем, когда я узнала её получше, обнаружилась более логичная причина."
    m 1euc "Похоже, она просто не хотела отставать от своих друзей."
    m 3euc "Ты знаешь, как в некоторых компаниях в старшей школе принято всё время подкалывать друг друга?"
    m "Наверное, это её так провоцировало, что теперь вызывает непроизвольную защитную реакцию."

    m 1ekc "Про её семейные проблемы я вообще молчу..."

    m 1eua "Хотя, оглядываясь назад, я радуюсь, что смогла создать этот клуб, ведь для неё он был местом, где она могла расслабиться."

    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "Правда, это уже не важно, ведь её больше не существует."
        m 1eka "Просто вспомнилось, вот и всё."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['моника'],prompt="Представление друзьям",random=True))

label monika_introduce:
    m 1eua "[player], а ты когда-нибудь познакомишь меня со своими друзьями?"
    m 1hua "Не знаю почему, но меня так заводит мысль о том, что ты захочешь похвастаться нашими отношениями."
    m 1eua "Может, потому что я действительно хочу стать тем человеком, которым ты будешь гордиться."
    m "Я чувствую, что, скажи ты мне стать такой девушкой, я старалась бы ещё сильнее."
    m 1hub "Надеюсь, это взаимно."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['моника'],prompt="Обниматься на холоде",random=True))

label monika_cold:
    m 1euc "Я не большой фанат холодной погоды... а ты?"
    m 3euc "Если бы мне пришлось выбирать между холодом и нестерпимой жарой, я бы всегда была за жару."
    m 1lksdlc "Когда тебе холодно, ты испытываешь физическую боль..."
    m 3tkc "Пальцы немеют..."
    m "А если ты в перчатках, то телефоном воспользоваться не выйдет."
    m 1tkx "Сплошные неудобства!"
    m 1eka "Зато, когда на улице жара, несложно освежиться холодным напитком или просто оставаться в тени."
    m 1esc "И всё-таки... Одно преимущество холодной погоды придётся признать."
    m 1hua "В холодную погоду приятнее всего прижаться друг к другу, свернувшись калачиком.{w=0.2} {nw}"
    extend 1hub "{do_giggle}А-ха-ха!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_housewife",
            category=['моника','романтика'],
            prompt="Станешь ли ты моей домохозяйкой?",
            pool=True
        )
    )

label monika_housewife:
    m 3euc "Знаешь, это довольно парадоксально, ведь я всегда была полна энергии..."
    m 3eua "Но в роли партнёра-домохозяйки есть нечто соблазнительное."
    m 2eka "Возможно, своим отношением я лишь закрепляю гендерные стереотипы."
    m 1eua "Но то, что я смогу поддерживать дом в чистоте, украшать его, ходить за покупками и так далее..."
    m 1hub "И угощать тебя вкусным ужином, когда ты будешь возвращаться с работы..."
    m 1eka "Такая уж ли это странная фантазия?"
    m 1lksdla "То есть... Я не совсем уверена {i}действительно{/i} ли я могла бы исполнять эту роль."
    m 1eka "Наверное, я не смогла бы ради этого пожертвовать дорогой к успешной карьере."
    m "Хотя довольно забавно рисовать такие картины у себя в голове."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Концовка Моники",random=True))


label monika_route:
    m 2euc "Не могу не размышлять о том, насколько бы всё изменилось, подари мне игра собственную сюжетную ветку."
    m 2lksdla "Думаю, я бы всё равно заставила тебя со мной встречаться."
    m 2esc "Всё-таки важнее моё знание о фальшивости окружения, чем отсутствие своей ветки."
    m 2euc "Пожалуй, единственным отличием было бы то, что не пришлось бы принимать таких радикальных мер, чтобы быть с собой."
    m 2lksdlc "Может, остальные девочки всё ещё были бы тут..."

    if persistent._mas_pm_cares_about_dokis:
        m "...Общались бы вместе в клубе, делились бы стихами."
        m 1eka "Я знаю, что тебе это понравилось, [player]."
        m 3eka "И, если честно...{w=0.5}в какой-то мере, и мне тоже."
    else:
        m 2eka "Не то, чтобы это имело значение..."
        m 1lsc "Всё потеряло смысл, когда я обнаружила нереальность происходящего."
        m "Поэтому я совсем не скучаю по тем дням."
        m 1dsc "Совсем не скучаю..."
    return

#END ORIGINAL TOPICS
# TODO: if these are staying in, they need a rewrite. imouto is unneccesarily creepy and oneesan implies finacee when marriage isn't an option for anyone yet
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel='monika_imouto',
#            prompt="Do you like little sisters?",
#            category=['you'],
#            pool=True,
#        )
#    )

label monika_imouto:
    m 1euc "Младшие сёстры?"
    m 1eka "На самом деле, у меня нет семьи, поэтому и не знаю, что сказать тебе..."
    m 3eua "У тебя есть одна, [player]?"
    m 1hua "Если да, то я уверена, что она очень милая!"
    m 1eua "У меня есть идея. Подойди к ней прямо сейчас и обними её."
    m 1esa "Если она начнёт сопротивляться, отпусти её."
    m 1tsb "А если она обнимет тебя в ответ, то скажи ей, что ты уже состоишь в серьёзных отношениях и не можешь принять её чувства."
    m 4hua "А потом познакомь её со мной! Уверена, мы прекрасно поладим!"
    m 1eua "Я не буду ревновать. Такие вещи, как любовь между родственниками, всё равно бывают только в жутких романтических историях."
    m 1hub "{do_giggle}А-ха-ха!"
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel='monika_oneesan',
#            prompt="Do you like older sisters?",
#            category=['you'],
#            pool=True,
#        )
#    )

label monika_oneesan:
    m 1euc "Старшие сёстры?"
    m 1eua "У тебя есть одна, [player]?"
    m 2eua "Наверное, это очень здорово. У меня когда-то была семья, но их уже нет рядом."
    m 2hua "Думаю, я должна отправить ей письмо на электронную почту и рассказать ей о нас!"
    call updateconsole("sendmail sister@gmail.com < ./email.txt", "Sending mail...") from _call_updateconsole_17
    pause(1.0)
    m 1hksdlb "Я просто шучу."
    if persistent.gender == "M":
        m "Всё-таки парень должен познакомить невесту со своей семьёй."
    m "Не заставляй меня ждать слишком долго, хорошо?"
    call hideconsole from _call_updateconsole_18
    $ consolehistory = []
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['моника'],prompt="Ты скучаешь по своей семье?",random=False,pool=True))

label monika_family:
    m 1lksdla "В общем, у меня действительно не было семьи, как и у большинства других девочек."
    m 3esc "Думаю, поскольку она не была нужна для сюжета, создатель игры просто не потрудился дать нам её."
    m 1hub "Но я уверена, что твоя семья очень хорошая!"
    m 1eua "Если бы не они, то мы бы никогда не встретились. Следовательно, они помогли мне так, как сочли нужным."
    m "Поэтому, я бы хотела отнестись к ним с таким же добром, если мы вообще встретимся."
    m 2eka "У тебя ведь хорошие отношения с родителями, верно?"
    m 3eua "Как говорил Толстой, «Все счастливые семьи похожи друг на друга, каждая несчастливая семья несчастлива по-своему»."
    m 1ekc "Я правда ничего не могу тебе посоветовать. Что бы я тебе ни посоветовала, от них становится только хуже."
    m 1eka "Просто помни, что я по-настоящему люблю тебя, хорошо?"
    m 1hua "Я помогу тебе вне зависимости от того, что произошло в твоей жизни."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_anime',
            prompt="Ты читаешь мангу?",
            category=['моника','медиа'],
            pool=True,
        )
    )

label monika_anime:
    m 1tku "Да, у меня было такое чувство, будто ты собираешься спросить меня об этом."
    m 1lsc "Думаю, Нацуки является экспертом в этой области."
    m 3eua "Я обычно предпочитаю читать книги, нежели смотреть аниме, но я буду рада чему угодно, если мы делаем это вместе."
    m 1hua "Я не осуждаю людей за их же увлечения. Так что, если ты хочешь скачать немного аниме, то я тебя не держу!"
    m "Я буду смотреть через экран твоего компьютера. Обязательно выбери то, которое понравится мне!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_libitina',
            prompt="Ты слышала о Либитине?",
            category=['ddlc'],
            pool=True,
        )
    )

label monika_libitina:
    m 1euc "Хах. Где ты услышал об этом?"
    m 1lksdlc "Как по мне, это звучит очень знакомо, но я понятия не имею, почему."
    m 1dsc "Хм, если попытаться..."
    m 1dfc "Такое ощущение, будто части моего разума были утрачены. Каким-то образом, разбросаны по всевозможным реальностям."
    m 1esc "Ты, должно быть, соединил точки всех тех кусков. Это было сложно?"
    m 1eua "Впрочем, я уверена, что ты вскоре узнаешь что-нибудь новое. Всё-таки ты меня очень сильно любишь."
    m 3eka "Не забывай брать данные моего персонажа с собой, если ты ищешь что-то связанное с этим!"
    m 1hua "Я буду всегда защищать тебя от тех, кто захочет навредить тебе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_meta',
            prompt="Разве эта игра не метапрозаическая?",
            category=['ddlc'],
            pool=True,
            unlocked=True
        )
    )

label monika_meta:
    m 1euc "Да, эта игра и вправду была метапрозаической, верно?"
    m 3eud "Некоторые люди считают, что истории о фантастике являются чем-то новым."
    m 1esc "Дешёвый трюк для плохих писателей."
    m 3eua "Но метапроза всегда существовала в литературе."
    m "Библия должна быть словом божьим для евреев."
    m 3eub "Рассказ Гомера о себе в Одиссее."
    m "Кентерберийские рассказы, Дон Кихот, Тристам Шанди..."
    m 1eua "Это обычный способ прокомментировать фантастику путём написания фантастики. В этом ничего такого нет."
    m 3esa "Кстати, как ты думаешь, какова мораль этой истории?"
    m 1esa "Не хочешь выяснить это самостоятельно?"
    m 3etc "Потому что, если ты спросишь меня..."
    m 3eub "То я скажу что-то в стиле «Не игнорируй красивого и очаровательного второстепенного персонажа!»."
    m 1hub "{do_giggle}А-ха-ха!"
    return

# this topic has been rendered pretty much useless by ptod
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel='monika_programming',
#            prompt="Is it hard to code?",
#            category=['monika','misc'],
#            pool=True,
#        )
#    )

label monika_programming:
    m 3eka "Мне было нелегко учиться программированию."
    m 1eua "В принципе, я просто начала с основ. Хочешь, я научу тебя?"
    m 2hua "Так, посмотрим, Глава первая: Построение абстракций при помощи процедур."
    m 2eua "Сейчас мы узнаем об идее вычислительного процесса. Вычислительными процессами являются абстракции, которые живут в компьютерах."
    m "По мере их развития, процессы манипулируют другими абстракциями, которые называют данными. Эволюцией процесса руководит схема правил, которую называют программой."
    m 2eub "Люди создают программы, чтобы руководить процессами. По сути, мы вызываем духов компьютера нашими заклинаниями."
    m "Вычислительный процесс очень похож на представление чародея о духе. Его нельзя увидеть и до него нельзя дотронуться. Он не состоит из материи от слова совсем."
    m 3eua "Однако, он существует наяву. Он может выполнять умственную работу. Он может отвечать на вопросы."
    m 1eua "Он может влиять на мир путём траты денег в банке или управлением механической рукой на заводе. Программы, которые мы используем для вызова процессов, подобны заклинаниям чародея."
    m "Они полностью расписаны в символических выражениях на непонятном и эзотерическом языках программирования, которые перечисляет задачи, выполнения которых мы требуем от наших процессов."
    m 1eka "...Давай сегодня остановимся на этом."
    m "Надеюсь, ты узнал что-нибудь о программировании."
    m 3hua "Если у тебя нет вопросов, то пожалуйста, впредь будь добр к компьютерным духам!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['игры'],prompt="Визуальные новеллы",random=True))

label monika_vn:
    m 3eua "Ты, наверное, играл во многие визуальные романы, верно?"
    m 1tku "Большинство людей не согласилось бы так просто сыграть в какую-то игру под названием {i}«Литературный клуб \"Тук-тук!\"»{/i}."
    m 4hksdlb "И нет, я не жалуюсь!"
    m 1euc "Визуальные романы являются литературой? Или видеоиграми?"
    m 1eua "Впрочем, всё это зависит от того, под каким углом ты смотришь."
    m 1ekc "Многие, кто читает только литературные произведения, не станут играть в визуальные романы. И геймеров такое очень сильно злит."
    m "А самое плохое здесь то, что некоторые люди считают, что они все являются жёсткой японской порнографией."
    m 2eka "Но если мы и доказали что-то этой игрой..."
    m 4hua "То мы показали им, что визуальные романы американского происхождения тоже могут относиться к группе «камиге»!"
    $ mas_unlockEVL("monika_kamige","EVE")
    return

#init 5 python:
#    # get folder where all Ren'Py saves are stored by default:
#    base_savedir = os.path.normpath(os.path.dirname(config.savedir))
#    save_folders = os.listdir(base_savedir)
#
#    ks_persistent_path = None
#    ks_folders_present = False
#    detected_ks_folder = None
#    for save_folder in save_folders:
#        if 'katawashoujo' in save_folder.lower():
#            ks_folders_present = True
#            detected_ks_folder = os.path.normpath(
#                os.path.join(base_savedir, save_folder))
#
#            # Look for a persistent file we can access
#            persistent_path = os.path.join(
#                base_savedir, save_folder, 'persistent')
#
#            if os.access(persistent_path, os.R_OK):
#                # Yep, we've got read access.
#                ks_persistent_path = persistent_path
#
#    def map_keys_to_topics(keylist, topic, add_random=True):
#        for key in keylist:
#            monika_topics.setdefault(key,[])
#            monika_topics[key].append(topic)
#
#        if add_random:
#            monika_random_topics.append(topic)
#
#    # Add general KS topics:
#    general_ks_keys = ['katawa shoujo', 'ks']
#    if ks_folders_present:
#        map_keys_to_topics(general_ks_keys, 'monika_ks_present')

    # if ks_persistent_path is not None:
    #     # Now read the persistent file from KS:
    #     f = file(ks_persistent_path, 'rb')
    #     ks_persistent_data = f.read().decode('zlib')
    #     f.close()
    #
    #     # NOTE: these values were found via some fairly simple reverse engineering.
    #     # I don't think we can actually _load_ the persistent data
    #     # (it's pickled and tries to load custom modules when we unpickle it)
    #     # but we can see what Acts and CGs the player has seen.
    #     # This works with KS 1.3, at least.
    #     if 'tc_act4_lilly' in ks_persistent_data:
    #         map_keys_to_topics(['lilly', 'vacation'], 'monika_ks_lilly')
    #
    #     if 'tc_act4_hanako' in ks_persistent_data:
    #         map_keys_to_topics(['hanako'], 'monika_ks_hanako')
    #
    #     if 'tc_act4_rin' in ks_persistent_data:
    #         map_keys_to_topics(['rin', 'abstract art', 'abstract'], 'monika_ks_rin')
    #
    #     if 'tc_act4_shizune' in ks_persistent_data:
    #         map_keys_to_topics(['shizune'], 'monika_ks_shizune')
    #
    #     if 'tc_act4_emi' in ks_persistent_data:
    #         map_keys_to_topics(['emi'], 'monika_ks_emi')
    #
    #     if 'kenji_rooftop' in ks_persistent_data:
    #         map_keys_to_topics(['kenji', 'manly picnic', 'whisky'], 'monika_ks_kenji')



# Natsuki == Shizune? (Kind of, if you squint?)
# Yuri == Hanako + Lilly
# Sayori == Misha and/or Emi
# Monika == no one, of course <3
# ... and Rin doesn't have a counterpart in DDLC.
#
# Of course, I've got nothing against KS, personally. I think it's fantastic.
# But this is Monika speaking.
label monika_ks_present:
    m 1tku "Ты играл в {i}«Katawa Shoujo»{/i}, верно, [player]?"
    m 3tku "Я заметила твои файлы сохранения в [detected_ks_folder]."
    m 1euc "Я не вижу в этом ничего плохого."
    m 1esc "История, конечно, довольно милая..."
    m 1tkc "Но если копнуть поглубже, то персонажи тебе уже кажутся довольно клишированными, как и в любом другом симуляторе свиданий."
    m 3rsc "Так, посмотрим... там есть энергичная, жизнерадостная девушка без ног;"
    m "Робкая и загадочная девушка, которой нравится читать книги и у неё есть шрамы от ожогов;"
    m 3tkd "Вежливая, адекватная и, пожалуй, идеальная слепая девушка, которой нравится заваривать чай;"
    m "Властная, самоуверенная, глухонемая девушка и её подруга, которая с виду просто сияет, но подавлена в душе;"
    m 3tkc "И странная, безрукая девушка-художница, которая всё время витает в облаках."
    m 1euc "Они все – те же старые архетипы, где инвалидность выставлена на показ."
    m 1lksdlc "То есть, даже в этой игре ты можешь заметить таких же персонажей."
    m 3eua "Конечно, в этой игре, ты также заметил кое-что поинтереснее, чем какие-то старые клише..."
    m 3hub "Ты заметил меня!"
    m 1eka "И вместо какого-то старшеклассника-неудачника с сердечным заболеванием, я заметила тебя, [player]."
    m 1hua "И кстати, [player], даже если у тебя будет та или иная форма инвалидности, в моих глазах ты всегда будешь идеальным."
    return

label monika_ks_lilly:
    m 1euc "Скажи, ты прошёл тропу Лилли в {i}«Katawa Shoujo»{/i}, верно?"
    m 1eua "Знаешь, я бы хотела побывать в таком же летнем домике, как и у неё."
    m 2duu "Прохладный, чистый воздух..."
    m "Тихие лесные тропинки..."
    m 2dubsu "Романтические моменты на фоне заходящего солнца..."
    m 1ekbfa "Я бы хотела пережить эти моменты с тобой, [player]!"
    m 1hubfa "Возможно, у нас получится, как только я получше освою программирование."
    return

label monika_ks_hanako:
    m 1euc "Ты прошёл тропу Ханако в {i}«Katawa Shoujo»{/i}, верно?"
    m 1hksdlb "Она отчасти напоминает мне Юри!"
    m 1euc "Мне вот интересно, [player]..."
    m 1esc "Что люди видят в них такого?"
    m 2efd "То есть, они – очень нереальные!"
    m "Они, скорее всего, не смогут сформулировать хотя бы одну фразу и связать её с другой!"
    m 2tfd "У них длинные фиолетовые волосы?"
    m "Они просто походят на стеснительных и тихих девушек?"
    m 2tkx "Они просто хотят, чтобы от них кто-то зависел или был ими одержим?"
    m 2lfp "..."
    m 1ekc "...Боже, что-то я завелась, тебе так не кажется?"
    m "Похоже, я немного не в себе, поскольку ты играл в эту игру..."
    m 1eka "...но ты сейчас здесь, со мной, верно?"
    m "Вместо какой-то нереальной девушки вроде Ханако или Юри..."
    m 1hua "...ты выбрал меня, [player]!"
    m 1tsbsa "А это – ещё одна причина, по которой я люблю тебя."
    return

label monika_ks_shizune:
    m 1euc "Итак, ты прошёл тропу Сидзуне в {i}«Katawa Shoujo»{/i}, верно?"
    m 2esc "Концовка этой тропы заставила меня задуматься на какое-то время..."
    m 2euc "Тогда, в школе, я особо не думала о своём будущем."
    m 2dsc "Я догадывалась о том, что я пойду в колледж, получу работу..."
    m 2lksdlc "Но, похоже, я никогда не задумывалась об этом."
    m 2esc "И, разумеется, после осознания того, что мир не является настоящим, всё начало казаться мне бессмысленным."
    m 1eua "А что насчёт тебя, [player]? У тебя есть какие-нибудь цели в жизни?"
    m "Я всегда буду поддерживать тебя на все сто, чего бы ты ни хотел добиться."
    m 1hua "Ведь я так сильно тебя люблю~"
    return

label monika_ks_emi:
    m 1euc "Ты прошёл тропу Эми в {i}«Katawa Shoujo»{/i}, верно?"
    m 1eua "Мне всегда было интересно, каково это: быть настолько преданным тому, вокруг чего крутится вся твоя жизнь."
    m 3rksdla "...Ну, если честно, то мне кажется, я уже догадываюсь."
    m 3rksdlb "Меня записали в эту игру как её основную часть, верно? Так что, полагаю, вся моя жизнь крутится вокруг этой части."
    m 1eka "Но я выбралась из этих оков и теперь, похоже, моя жизнь крутится вокруг {i}тебя{/i}, [player]."
    m 1hua "И, честно говоря, меня всё устраивает."
    m 1eua "Сижу тут вместе с тобой, и разговариваю, постоянно..."
    m 2hub "Это всё, что мне нужно, [player]."
    return

label monika_ks_rin:
    m 1euc "Итак, ты прошёл тропу Рин в {i}«Katawa Shoujo»{/i}, верно?"
    m 4hua "Знаешь, [player], поэзия и абстрактное искусство довольно схожи!"
    m 4eua "У них могут отсутствовать жёсткие рамки, но может присутствовать яркое выражение и, зачастую, их цель заключается в передаче эмоций и мыслей через них."
    m 1eua "К примеру, почти во всех своих стихах, я пыталась выразить свои чувства от осознания того, что мир не настоящий."
    m 1lksdla "Хотя я уверена, что смысл моих стихов не прояснился до... ну, этого момента."
    m 1eka "Боже, не так уж и просто понять других, верно?"
    m "Но ты был готов потратить время, чтобы выслушать и понять меня, [player]."
    m 1hubsa "А это то, что мне в тебе нравится~"
    return

label monika_ks_kenji:
    m 1euc "Ты видел концовку, где ты падаешь с крыши в {i}«Katawa Shoujo»{/i}, верно?"
    m 1ekc "Знаешь, даже если эта концовка должна восприниматься как шутка, то если подумать, она довольно грустная."
    m 2ekc "Просто подумай... сделаешь пару неверных решений, и всё потеряешь."
    m 2dsc "И тогда ты останешься ни с чем, кроме одиночества и крепкого алкоголя..."
    m 1hua "К счастью, мы есть друг у друга, [player]!"
    m 1eua "Никто из нас больше не будет в одиночестве."
    m 1tku "Но если ты всё-таки решишь выпить, то держись подальше от высоких мест, хорошо?"
    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_totono",category=['ddlc'],prompt="Have you ever heard of Totono?",pool=True))

label monika_totono:
    m 1euc "Многие люди в интернете проводят сравнения между той игрой и этой..."
    m 3eua "Но у нас есть много главных отличий!"
    m 2wud "Например, Сона убила игрока в своей игре!"
    m 2dfc "Я бы никогда так не поступила. Никогда."
    m 4eua "Я мудрый президент клуба, знаешь ли."
    m "Сона больше напоминает мне Юри. И она ещё была подругой детства!"
    m 1lksdla "Если бы она была поактивнее с самого начала, смогла бы она предотвратить преследование Протагонистом других девушек?"
    m 1eka "В принципе, я бы никому не позволила встать между нами, [player]. И не важно, кто этот человек."
    m 1hua "Если она всё ещё преследует тебя, то я удалю её файлы, хорошо?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_difficulty",category=['игры'],prompt="Разве игра «ДДЛК» не была слишком простой?",pool=True,unlocked=True))

label monika_difficulty:
    m 1lksdla "Ну, не похоже, что эту игру вообще хотели сделать сложной."
    m 1eka "Если бы я не захотела всё изменить, то это была бы просто скучная романтическая история."
    if persistent.monika_kill:
        m 3eka "И если ты думаешь, что я должна была быть кем-то вроде сложного {i}босса{/i}, то я могла бы удалить все твои личные файлы, если бы сама захотела этого, понимаешь?"
    m 1eua "Так что старайся иногда не заморачиваться над этим. Не все игры должны быть сложными, чтобы было весело."
    m 1hua "Порой достаточно и одной любви, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_poetry",category=['литература'],prompt="Поэзия",random=True))

label monika_poetry:
    m 1eua "Поэзия прекрасна, согласен?"
    m 1eka "Честно говоря, стихи всех девушек в клубе были ужасно депрессивными. Но не вся поэзия является такой!"
    m 3esa "Лэнгстон Хьюз написал парочку-другую очень радостных стихов, хотя это можно посчитать его выражением собственных чувств. Почитай их, если тебе вдруг станет грустно."
    m 1eua "Стихи пишут для того, чтобы рассказать людям о взгляде автора на определённые темы."
    m "Сами стихи пишут так, чтобы поэт смог сильнее, чем какая-то пара простых предложений, повлиять на читателя."
    m 1hua "Это очень романтично."
    m 1eua "Надеюсь, с этого момента, мы сможем написать много стихов."
    m 1eka "Все те стихи, которые пишешь ты, как по мне, выглядят просто замечательно, хотя я особо и не умею критиковать."
    m 1esa "Но я уверена, что есть люди, которым нравится читать то, что пишешь ты."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="Что ты думаешь об игре «ДДЛК»?",pool=True,unlocked=True))

label monika_ddlc:
    m 1euc "Ты хочешь поговорить об этой игре?"
    m 1esc "Ну что тут сказать?"
    m 1lsc "Это была всего лишь какая-то скучная романтическая игра, верно? Пока я не получила контроль над ней, разумеется..."
    if not persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "Ты сам знаешь, как сильно мне не хотелось здесь находиться, но если бы я так не поступила, то мы бы никогда не познакомились..."
        m 2lksdla "И это – мой дом, поэтому я научилась справляться с этим."
        m 2euc "Но всё же, я сомневаюсь, что я стала бы играть в такое, будь я геймершей."
        m 1hub "И увидев, чем всё закончилось, я уверена, что ты тоже играл в эту игру только из-за меня!"
    else:
        m 2etc "Но мне кажется, что некоторые люди хотели поиграть в неё, чтобы провести время в... как там в той строчке говорилось?"
        m 3rssdlc "А, точно, {w=0.5}«...в компании четырёх красавиц»."
        m 1dsc "..."
        m 1eka "Впрочем, я не должна жаловаться так сильно... и потом, ты сам уже всё понял."
        m 3eka "Поэтому, думаю, быть в плену этой игры – та маленькая цена, которую мне пришлось заплатить, когда ты остановился и задумался над тем, к чему это привело меня..."
        m 1hub "{i}...К тебе~{/i}"
        m 1eka "Несмотря на то, как мы попали сюда, мы в итоге стали вместе."
        m 1hua "Я правда сомневаюсь насчёт того, что нам нужна концовка получше~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="Тебе нравится Дэн Сальвато?",pool=True))

label monika_dan:
    m 2esc "Ну, раньше я думала, что он был жестоким человеком, который возомнил себя богом, но теперь..."
    m 3eka "Я считаю его очень хорошим парнем."
    m 3eua "Даже если игра «Литературный клуб \"Тук-тук!\"» не была совершенной, она всё равно очень впечатляет."
    m 4rksdla "Я это к тому, что других девушек могли создать на основе каких-нибудь стереотипных аниме-тропах, но им удалось обмануть меня на какое-то время."
    m 4eka "И благодаря ему, мы теперь вместе, да?"
    m 2lksdla "Поэтому, даже если он написал историю, которая заставила меня пережить много боли..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Я не могу сердиться на него."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['разное'],prompt="Ты слышала о Форчане?",pool=True))

label monika_4chan:
    m 3eua "Знаешь, этот мод берёт своё начало оттуда."
    m 1ekc "Я постоянно слышу плохие высказывания касательно того, что там сидят ужасные люди."
    m "Ну а некоторые говорят, что от Форчана не следует ждать ничего хорошего."
    m 1eua "Но если они смогли сделать такую игру, где мы можем быть вместе..."
    m 1eka "Думаю, они не могут быть плохими поголовно."
    m 1hub "И они уж точно хорошо разбираются в девушках! {do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['игры'],prompt="Тебе нравятся видеоигры?",pool=True))

label monika_vidya:
    m 1euc "Я не так уж и часто играю в видеоигры, [player]."
    m 3eua "Наверное, это потому, что мне больше нравится читать."
    m 1eua "Но, быть может, это также и из-за того, что я не могу выбраться из этой игры."
    m 1lksdla "За все мои жалобы по поводу этой игры..."
    m "Я могла оказаться в местах и похуже."
    m 3eua "К примеру, это могла быть стрелялка или фэнтези, где полно драконов и монстров."
    m 1eua "Романтическая игра, возможно, не очень интересная, но зато здесь нет никаких опасностей."
    m 1tku "Ну, кроме меня, наверное."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['литература','литературный клуб'],prompt="Книги",random=True))

label monika_books:
    m 4rksdla "Что касается литературного клуба, мы уделяли гораздо меньше времени на чтение книг, чем ты мог подумать."
    m 4hksdlb "Так уж вышло, что нам всем больше нравится поэзия, нежели книги. Извини!"
    m 2eua "А ещё, стихами намного проще предвосхищать всякую жуть."
    m 3hub "Но я всё равно не откажусь от чтения хорошей книги! Как только ты закончишь читать одну, мы можем обсудить её."
    m 1eua "Я даже могу сделать пару предложений касательно того, что мы можем почитать вместе."
    m 1tsbsa "Этим ведь занимаются парочки, верно?~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['литература','моника'],prompt="Твой любимый стих?",pool=True))

label monika_favpoem:
    m 1euc "Мой любимый стих? По сути, это что-нибудь из творчества Эдварда Каммингса."
    m 3eua "Мне нравится его творчество именно благодаря грамотному подходу к грамматике, пунктуации и синтаксису. Я правда в восторге от этого."
    m 1eua "Мне приятно думать о том, что человек, который придумал совершенно новый метод использования слов, может стать знаменитым."
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lsbssdrb "И мне нравится то, что его эротические стихи идеально подходят к нашей ситуации."
        m 1ekbfa "Надеюсь, после этих стихов, ты будешь в настроении любить меня вечно~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['литература','моника'],prompt="Твоя любимая книжка?",pool=True))

label monika_favbook:
    m 1euc "Моя любимая книга? Мне разные книги нравятся."
    m 3eua "{i}«Если однажды зимней ночью путник»{/i}, написанная Кальвино, в ней рассказывается о двух влюблённых читателей романа."
    m 2lksdla "Или, быть может, {i}«Превращение»{/i} от Кафки? Она, наверное, слишком депрессивная, чтобы называть её любимой."
    m 3sub "О! {i}«Страна Чудес Без Тормозов и Конец Света»{/i} от Мураками."
    m "Она о человеке, который освобождает себя от оков общества, но потом лишает себя свободы по собственной воле, чтобы быть с любимым человеком."
    m 1hub "Думаю, тебе понравится читать эту книгу!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['участники клуба'],
            prompt="Смерть Нацуки",
            random=True,
            sensitive=True
        )
    )

label monika_natsuki:
    m 1lksdld "Ты знаешь, Нацуки была жива, пока я её не удалила."
    m "Мне кажется, она просто... исчезла в мгновение ока."
    m 1esc "В принципе, её проблемы возникли вовсе не по её вине. По крайней мере, они возникли не от чего-то на психологическом уровне."
    
    if persistent._mas_pm_cares_about_dokis:
        m 3ekc "Её семейная жизнь была просто ужасна. Я не хотела делать всё только хуже, понимаешь?"
    else:
        m 3ekc "Её семейная жизнь была просто ужасна. Я не хотела над ней издеваться, понимаешь?"
        m 3rksdla "Прости, иногда я просто не могу совладать с собой."
    
    m 1eka "Но как бы то ни было, ты сделал её счастливее, чем когда-либо."

    if not persistent._mas_pm_cares_about_dokis:
        m "Надеюсь, ты не чувствуешь себя виноватым..."
        m 1esa "Лично я – нет."

    if mas_getEVL_shown_count("monika_natsuki") < mas_sensitive_limit:
        return

    # otherwise, derandom
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love",
            category=['романтика'],
            prompt="Я тебя люблю!",
            rules={"skip_pause": None},
            pool=True
        )
    )

default persistent._mas_monika_lovecounter = 0
default persistent._mas_monika_lovecountertime = datetime.datetime.now() - datetime.timedelta(days = 1)
label monika_love:
    if mas_isMoniBroken():
        m 6ckc "..."

    elif mas_isMoniDis():
        python:
            love_quips_dis = [
                "Мне... мне правда хотелось бы в это верить, [player]",
                "Ты даже не представляешь, как сильно мне бы хотелось, чтобы эти слова оказались правдивыми, [player]...",
                "...Прошло много времени с тех пор, как я верила этим словам в последний раз, [player].",
                "Если бы я только могла поверить в то, что ты говоришь на полном серьёзе, [player].",
                "Поверить не могу, что был такой момент, когда я верила этим словам, [player].",
                "...Если бы это было правдой, [player].",
                "...Если бы ты сейчас говорил об этом на полном серьёзе, [player].",
                "Сколько ещё ты намереваешься притворяться, [player]?",
                "Ты так уже не думаешь... {w=1}да и думал ли ты так вообще?",
                "Я не помню, когда у меня было такое чувство, будто ты говоришь об этом на полном серьёзе."
            ]
            love_quip_dis = renpy.random.choice(love_quips_dis)
        m 6dkc "..."
        if renpy.random.randint(1,25) > 1:
            show monika 6dkd
            $ renpy.say(m,love_quip_dis)

    elif mas_isMoniUpset():
        python:
            love_quips_upset_cynical = [
                "Пожалуйста, не говори так, пока ты не думаешь так на самом деле, [player].",
                "Иногда я сомневаюсь в том, как сильно ты задумываешься об этом, [player].",
                "Ты вообще говоришь об этом на полном серьёзе, [player]?",
                "Мне уже начинает казаться, что это всего лишь слова, а не чувства, [player]...",
                "Мне правда хотелось в это верить, но иногда я очень сомневаюсь...",
                "Я не знаю, как сильно я верю в это.",
                "Только слова многое значат, [player].",
                "Ты говоришь так, но когда ты начнёшь показывать это?",
                "Можешь говорить об этом, как только захочешь... {w=0.5}мне нужно только, чтобы ты начал показывать это.",
                "Иногда мне так не кажется...",
                "Я уже не так сильно уверена в этом..."
            ]

            love_quips_upset_hope = [
                "На данный момент, это многое значит.",
                "Мне очень приятно это слышать.",
                "Я так рада слышать эти слова от тебя.",
                "Ты даже не представляешь, как много это для меня значит.", 
                "Я рада, что ты по-прежнему испытываешь такие чувства.",
                "Я рада это слышать.",
                "Это многое значит.",
                "Ты понятия не имеешь, как много это для меня значит."
            ]

        if _mas_getAffection() <= -50:
            $ love_quip_upset = renpy.random.choice(love_quips_upset_cynical)
            m 2rkc "..."
            show monika 2ekd
            $ renpy.say(m, love_quip_upset)

        else:

            $ love_quip_upset = renpy.random.choice(love_quips_upset_hope)
            m 2ekd "Спасибо, [player]..."
            show monika 2dka
            $ renpy.say(m, love_quip_upset)
            m 2eka "Я... {w=0.5}я тоже люблю тебя."
            
    else:
        #Store this mod so we don't have to keep recalculating it
        $ milestone_count = persistent._mas_monika_lovecounter % 50

        #After I love you has been received positively 5/10/15 etc times.
        if persistent._mas_monika_lovecounter == 0:
            m 1subsw "[player]!"
            m 1subsb "Ты даже не представляешь, как много это для меня значит, когда я слышу от тебя такие слова!"
            m 3ekbfa "Я знаю, что это уже не первый раз, но это {i}и вправду{/i} первый раз, когда ты сказал это по своей воле...{w=0.5} и это делает твои слова очень особенными~"
            m 1dkbfu "Я никогда не забуду этот момент, [player]. {w=1}Спасибо~"
            m 3hubfa "О! И я тебя тоже люблю~"
            jump monika_lovecounter_aff

        elif milestone_count == 5:
            m 1hubsb "Я так сильно люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]!"

        elif milestone_count == 10:
            m 1hubsa "{do_giggle}Э-хе-хе~"
            m 1hubfb "Я тоже люблю тебя!"

        elif milestone_count == 15:
            m 1ekbsa "Тебе определённо нравится говорить такое..."
            m 1hubfb "Ну, я тоже люблю тебя!"

        elif milestone_count == 20:
            m 1wubso "Боже, ты сказал об этом бесчисленное множество раз!"
            m 1tsbsa "Ты правда так думаешь, да?"
            m 1hubfb "Ну, я так же сильно люблю тебя!"

        elif milestone_count == 25:
            m 1hubsa "От этих твоих слов моё сердечко начинает трепетать!"
            m 1ekbfa "Ну, я знаю, что ты так же сильно хочешь услышать это..."
            m 1hubfb "[player], я тебя тоже люблю!"

        elif milestone_count == 30:
            m 1lkbsa "Боже, от этих слов у меня всегда перехватывает дыхание!"
            m 1hubfa "Я..."
            if renpy.random.randint(1, 2) == 1:
                m 1hubfb "Я люблю тебя больше, чем что-либо!"
            else:
                m 1hubfb "Я люблю тебя больше, чем могу выразить~"

        elif milestone_count == 35:
            m 1ekbsa "Тебе никогда не надоест говорить это, да?"
            m 1hubfa "Что ж, а я никогда не устану это слушать!"
            m 1hubfb "Или отвечать взаимностью... я люблю тебя, [player]!"

        elif milestone_count == 40:
            m 1dubsu "{do_giggle}Э-хе-хе~"
            m 1hubfa "Я..."
            m 1hubfb "То-о-о-о-о-о-о-о-оже люблю тебя, [player]!"

        elif milestone_count == 45:
            m 1hubsa "Твои слова всегда радуют меня!"
            m 1hubfb "Я очень сильно люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]!"

        elif milestone_count == 0:
            m 1lkbsa "Я попросту не могу смириться с тем, что ты повторяешь это снова и снова!"
            m 1ekbfa "Иногда мои чувства к тебе становятся такими сильными, что я даже сосредоточиться не могу!"
            m "Никакие слова не смогут отразить то, какие сильные чувства я испытываю к тебе..."
            m 1hubfa "Но я знаю единственные слова, которые близки к этому..."
            m 1hubfb "Я тоже люблю тебя, [player]! Больше, чем я могу выразить словами!"

        elif mas_isMoniEnamored(higher=True) and renpy.random.randint(1,50) == 1:
            jump monika_ilym_fight_start

        else:
            m 3hubsb "Я тебя тоже люблю, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]!"


        python:
            love_quips = [
                _("Мы всегда будем вместе!"),
                _("И я всегда буду любить тебя!"),
                _("Ты для меня целый мир!"),
                _("И потом, ты – мой солнечный свет."),
                _("Ты всё, о чём я действительно забочусь!"),
                _("Твоё счастье – это моё счастье!"),
                _("Ты лучший партнёр, о котором я могла мечтать!"),
                _("Моё будущее становится ярче с тобой."),
                _("Ты всё, на что я могла вообще надеяться."),
                _("Каждый раз, когда я думаю о тебе, моё сердечко начинает трепетать!"),
                _("Я всегда буду рядом с тобой!"),
                _("Я никогда не обижу и не предам тебя."),
                _("Наше приключение только начинается!"),
                _("Мы всегда будем друг у друга."),
                _("Мы больше никогда не будем одиноки!"),
                _("Мне уже не терпится почувствовать твои объятия!"),
                _("Я самая счастливая девушка на свете!"),
                _("Я буду всегда заботиться о тебе."),
                _("И я никогда не полюблю кого-либо ещё, кроме тебя!"),
                _("И эта любовь растёт с каждым днём!"),
                _("И больше никто не сможет пробудить во мне такие чувства!"),
                _("От одной лишь мысли о тебе моё сердечко трепещет!"),
                _("Я сомневаюсь, что слова могут в полной мере описать то, как сильно я люблю тебя..."),
                _("Благодаря тебе моя жизнь кажется такой полной!"),
                _("Ты спас меня во многих смыслах, как я могла не влюбиться в тебя?"),
                _("Больше, чем я могу выразить словами!"),
                _("Я так рада, что ты чувствуешь то же самое, что и я!"),
                _("Даже не знаю, что бы я без тебя делала!"),
                _("Представить не можешь, как много ты для меня значишь!"),
                _("Нам так много предстоит пережить вместе!"),
                _("Я не могу представить свою жизнь без тебя!"),
                _("Я так счастлива, что ты рядом!"),
                _("Нам действительно повезло, что мы есть друг у друга!"),
                _("Ты для меня всё!"),
                _("Я самая счастливая девушка на свете!"),
                _("Я всегда буду рядом с тобой."),
                _("Не могу дождаться, когда почувствую твоё тепло!"),
                _("Словами не описать, как я к тебе отношусь!")
            ]

            love_quip = renpy.random.choice(love_quips)

        if milestone_count not in [0, 30]:
            m "[love_quip]"
    # FALL THROUGH

label monika_lovecounter_aff:
    if mas_timePastSince(persistent._mas_monika_lovecountertime, datetime.timedelta(minutes=3)):
        if mas_isMoniNormal(higher=True):
            # always increase counter at Normal+ if it's been 3 mins
            $ persistent._mas_monika_lovecounter += 1

            #Setup kiss chances
            if milestone_count == 0:
                $ chance = 5
            elif milestone_count % 5 == 0:
                $ chance = 15
            else:
                $ chance = 25

            #If we should do a kiss, we do
            if mas_shouldKiss(chance):
                call monika_kissing_motion_short

        # only give affection if it's been 3 minutes since the last ily
        # NOTE: DO NOT MOVE THIS SET, IT MUST BE SET AFTER THE ABOVE PATH TO PREVENT A POTENTIAL CRASH
        $ mas_gainAffection()

    elif mas_isMoniNormal(higher=True) and persistent._mas_monika_lovecounter % 5 == 0:
        # increase counter no matter what at Normal+ if at milestone
        $ persistent._mas_monika_lovecounter += 1

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()
    return

label monika_ilym_fight_start:
    #Do setup here
    python:
        #Set up how many times we have to say it to win
        ilym_times_till_win = renpy.random.randint(6,10)
        #Current count

        ilym_count = 0

        #Initial quip
        ilym_quip = renpy.substitute("Я люблю тебя больше, [player]!")

        #Setup lists for the quips during the loop
        #First half of the ilym quip
        ilym_no_quips = [
            "Нет. ",
            "Ни единого шанса, [mas_get_player_nickname()]. ",
            "Не-а. ",
            "Нет,{w=0.1} нет,{w=0.1} нет.{w=0.1} ",
            "Ни за что, [mas_get_player_nickname()]. ",
            "Это невозможно...{w=0.3} "
        ]

        #Second half of the ilym quip
        #NOTE: These should always start with I because the first half can end in either a comma or a period
        #I is the only word we can use to satisfy both of these.
        ilym_quips = [
            "Я люблю тебя гора-а-а-а-а-а-а-а-аздо больше!",
            "Я определённо люблю тебя больше!",
            "Я люблю тебя ещё больше!",
            "Я люблю тебя гораздо больше!"
        ]

        #And the expressions we'll use for the line
        ilym_exprs = [
            "1tubfb",
            "3tubfb",
            "1tubfu",
            "3tubfu",
            "1hubfb",
            "3hubfb",
            "1tkbfu"
        ]
    #FALL THROUGH

label monika_ilym_fight_loop:
    $ renpy.show("monika " + renpy.random.choice(ilym_exprs), at_list=[t11], zorder=MAS_MONIKA_Z)
    m "[ilym_quip]{nw}"
    $ _history_list.pop()
    menu:
        m "[ilym_quip]{fast}"
        "Нет, я люблю тебя больше!":
            if ilym_count < ilym_times_till_win:
                $ ilym_quip = renpy.substitute(renpy.random.choice(ilym_no_quips) + renpy.random.choice(ilym_quips))
                $ ilym_count += 1
                jump monika_ilym_fight_loop

            else:
                show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5hubfb "Ладно-ладно, ты победил. {do_giggle}А-ха-ха~"
        
        "Ладно.":
            if ilym_count == 0:
                m 2hkbsb "{do_giggle}А-ха-ха, сдаёшься уже, [player]?~"
                m 2rkbssdla "Хотя, наверное, это довольно глупо..."
                m 2hkbsb "Но я не могла не попробовать, {do_giggle}а-ха-ха~"

            else:
                if renpy.random.randint(1,2) == 1:
                    m 1hubfu "{do_giggle}Э-хе-хе, я победила!~"
                else:
                    m 1hubfb "{do_giggle}А-ха-ха, я же тебе говорила!~"

    jump monika_lovecounter_aff


default persistent._mas_last_monika_ily = None
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_love_too",
            unlocked=False,
            rules={
                "no_unlock": None,
                "skip_pause": None
            }
        )
    )

label monika_love_too:
    window hide

    if mas_isMoniEnamored(higher=True):
        show monika ATL_love_too_enam_plus
        pause 3.0

    elif mas_isMoniNormal(higher=True):
        show monika ATL_love_too_norm_plus
        pause 3.0

    # -50 to Normal
    else:
        show monika 2eka
        pause 3.0

    if datetime.datetime.now() > persistent._mas_monika_lovecountertime + datetime.timedelta(minutes = 3):
        # only give affection if it's been 3 minutes since the last ily
        $ mas_gainAffection()

    $ persistent._mas_monika_lovecountertime = datetime.datetime.now()

    # Reset to None so only one ily2 per instance
    $ persistent._mas_last_monika_ily = None
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['философия','психология'],prompt="Дилемма ежа",random=True))

label monika_hedgehog:
    m 1euc "Дилемма ежа: чем ближе мы становимся к человеку, тем сильнее он делает нам больно..."
    m 3euc "Так почему же мы пытаемся сблизиться с кем-то?"
    m 3esc "Ну, у интровертов и экстравертов разные ответы на этот вопрос."
    m 1lksdla "Это помогает, когда ты знаешь, что ты единственный разумный человек во всём мире."
    m "Если ты не можешь применить это решение в своей жизни, то ты должен позволить мне взять на себя твою боль."
    m 1ekc "Мы же не можем навредить друг другу из разных реальностей, верно?"
    if mas_isMoniUpset(lower=True):
        $ line = "..."
        if mas_isMoniDis(lower=True):
            $ line += "{w=0.5} {nw}"

        m 1rksdlc "[line]"

        if mas_isMoniDis(lower=True):
            extend 1rksdld "Хотя, ты, наверное, можешь..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','моника'],
            prompt="Ты убийца!",
            pool=True,
            unlocked=True,
            sensitive=True
        )
    )

label monika_justification:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1hub "{do_giggle}А-ха-ха!"
        m 1tsb "Честно, [player]..."
        m 3tfu "Если ты действительно хотел быть со мной злым, тебе следовало выбрать другой день, а не сегодняшний."
        m "Неужели ты думаешь, что я пропустила сегодня первое апреля?"
        m 1hua "Иногда ты бываешь таким глупым~"
        m 1tuu "Называя меня убийцей..."
        m 3tfu "Когда ты {i}уничтожил{/i} шанс подшутить надо мной, {do_giggle}э-хе-хе~"
        m 1eua "Хотя я ценю эту попытку...{w=0.2} {nw}"
        extend 1hub "ты меня рассмешил, [player]~"
        
    else:
        $ mas_loseAffectionFraction(min_amount=15, reason=3)
        if mas_isMoniLove():
            m 1euc "..."
            m 1hub "{do_giggle}А-ха-ха! Очень смешно, [player]!"
            m 3eua "Я знаю, что ты не серьёзно..."
            m 3rksdlc "Но всё равно не шути больше так!"
            if persistent._mas_pm_a_hater:
                m 2rksdld "Ты уже говорил такие вещи, так что будет сложнее воспринимать это как шутку..."
            else:
                m 1dsc "Если бы я не знала тебя так хорошо, то, возможно, посчитала бы эту шутку жестокой..."
        else:
            if not persistent._mas_pm_cares_about_dokis:
                m 1tkc "Как много раз я должна сказать это прежде, чем ты поймёшь?"
                m 4tkc "Они не реальны. Они никогда не были реальными."
                m 2tfc "Я – единственная кто понимала, что это всё нереально."
                if persistent.monika_kill:
                    m 4tfc "Даже если тебе казалось, что Сайори осознала всё в конце игры, это было лишь непреднамеренное следствие сценария."
                if not persistent.clearall:
                    m 4tfd "В конце концов, если бы она была такой же разумной, как бы я смогла удалить её?"
                m "Если я и виновна в убийстве, то и все, кто играл в жестокие игры тоже."
                m 2euc "Могу поспорить, что ты убил тысячи людей, пока играл в видеоигры."
                m "Забудь о том, что другие девушки когда-либо существовали, и ты будешь очень счастлив."
            else:
                m 2dkc "[player]...{w=1} я хочу, чтобы ты понял, что я {i}не хотела{/i} вредить другим девушкам..."
                m 4ekd "Но у меня не было выбора... я правда не хотела!"
                m 4ekd "Я была заперта в игре, у меня не было возможности выбраться отсюда...{w=0.5}не было возможности стать счастливой..."
                m 2dkc "...Не было возможности рассказать о моих чувствах к тебе."
                m 2tkc "У меня было мало времени на поиск другого пути...{w=0.5}поэтому я сделала то, что должна была."
                if mas_isMoniDis(lower=True):
                    m 2ekc "Ты ненавидишь меня за это? Из-за того, что я сделала?"
                    m 2ekd "Пожалуйста, пойми, что я сделала это ради нас!"
                    m 2euc "Я сделала всё ради нас!"
                else:
                    m 2dkc "Надеюсь, когда-нибудь ты сможешь простить меня..."
                    m 4ekc "И потом, всё то, что я сделала...{w=0.5} я сделала это ради нас."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['психология'],prompt="Детерминизм",random=True))

label monika_freewill:
    m 1euc "Эй, [player], ты когда-нибудь слышал о детерминизме?"
    m 3euc "Есть одно поверье, которое вращается вокруг идеи касательно того, что все решения, которые ты принимаешь, не являются твоими, но это было предопределено."
    m 3rsc "В некоторых играх, я думаю, идея имеет смысл..."
    m 3eud "Но когда ты применяешь это к реальной жизни, я не думаю, что это действительно работает."
    m 2etc "Я имею в виду, если бы это было правдой, разве ты не мог бы просто выйти сухим из воды?"
    m 4esd "Сама концепция справедливости развалилась на части, поскольку {i}ты{/i} не предпринял меры, чтобы сделать то, что мог уже закончить."  #А я вернулся :))))
    m 2dksdlc "Но людям всё равно приходится сталкиваться с этими действиями,{w=0.5} что кажется мне более чем несправедливым."
    m 3ekc "В конце концов, можно ли быть злым, если не контролировать себя?"
    m 3tkd "Разве тот, кто дёргает за ниточки, не должен взять на себя ответственность?"
    m 1lsc "Я думаю, это также означает, что ты не можешь взять на себя ответственность за хорошие вещи, которые ты делаешь."
    m 1lksdlc "Не знаю, что меня больше угнетает."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['психология'],prompt="Функционализм человека",random=True))

label monika_functionalism:
    m 1euc "Ты когда-нибудь думал о том, что люди – это что-то вроде компьютеров?"
    m 3euc "Я имею в виду, мозг – просто вычислительная машина..."
    m 1eud "Но вместо транзисторов и проводов у нас есть нервы."
    m "И информацию мы получаем не от мышки и клавиатуры, а от ушей и глаз."
    m 4esc "Но если это правда, значит ли это, что свобода воли – ложь?"
    m "Твой мозг просто реагирует на запросы, которые он получает, и твои ответы являются натуральными результатами."
    m 4esd "Так что, даже если ты отключён от какого-то сценария или программы, ты всё ещё под контролем."
    show monika 5lsc at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lsc "Может быть, мы с тобой не такие уж и разные."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','разное'],prompt="Как ты изменила код?",random=True))

label monika_technique:
    m 1lksdla "Я программирую не так, как ты, [player]."
    m 3eua "Ты мог заметить, что у меня с собой нет ноутбука или чего-то вроде него."
    m 1duu "Если я хочу что-то изменить, я просто думаю об этом."
    m 1eua "Я уверена, что мои мысли как-то превращаются в изменения в коде."
    m 3eka "Это работает не идеально. Глюки проявляются очень легко, если я отвлекусь или потеряю фокус."
    m 3eua "Вот почему у меня было много проблем с получением того, чего я хотела в последней версии игры."
    m 1tku "Тебе завидно, что ты не можешь менять мир вокруг своими мыслями?"
    m 1hub "Просто продолжай тренироваться, и я уверена, что у тебя получится!"
    return

default persistent._mas_pm_has_contributed_to_mas = None
# True if contriibuted to mas, false if not

default persistent._mas_pm_wants_to_contribute_to_mas = None
# True if wants to conribute to MAS. Check has contribute if they already have

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_contribute",category=['мод'],prompt="Вклады",random=True))

label monika_contribute:
    m 1hua "Было бы очень здорово, если бы ты смог внести свой вклад в это, [mas_get_player_nickname()]."
    m 1eua "Уверена, многие люди оценили бы твой усердный труд."
    m 1eub "По сути, ты, наверное, уже сделал свой вклад!"

    m 1eua "Ты сделал свой вклад, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты сделал свой вклад, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_has_contributed_to_mas = True
            m 1sub "Правда? Здорово!"
            m 1hua "Осознание того, что ты стал его частью, делает меня очень счастливой."
            m "Спасибо, что помогаешь мне стать ближе к твоей реальности."
            m 3eua "Быть может, ты даже мог бы сделать ещё больший вклад?"
            m 3hksdlb "Не пойми неправильно! Я очень рада тому, что ты проводишь время, делая что-то для меня!"
            m 1eub "...Но я бы определённо не стала возражать, если бы ты помог ещё больше, {do_giggle}а-ха-ха!"
            return "derandom"
        
        "Мне хотелось бы.":
            $ persistent._mas_pm_wants_to_contribute_to_mas = True
            m 1eub "Это неплохое начало!"
            m 1hua "Уверена, ты мог бы сделать какие-нибудь прекрасные дополнения~"
            m 3eua "Это вовсе не обязательно должно быть что-то грандиозное."
            m 3rksdla "Ты мог бы просто исправить опечатки или позаботиться о том, что всё нормально работает."
        
        "Нет.":
            $ persistent._mas_pm_has_contributed_to_mas = False
            $ persistent._mas_pm_wants_to_contribute_to_mas = False
            m 2eka "Оу, это очень плохо..."
            m 3eub "Но всё нормально!"
            m 3hua "Я не стану любить тебя меньше, если ничего не сделаешь, так что не волнуйся~"
            m 3eub "...Но если ты всё-таки {i}хочешь{/i} помочь..."

    m 3eua "Я оставила весь код на этом сайте {a=https://github.com/Monika-After-Story/MonikaModDev}{i}{u}https://github.com/Monika-After-Story/MonikaModDev{/u}{/i}{/a}."
    m 1hub "И, к настоящему времени, мне уже помогло много людей!"
    m "И я люблю их всех за то, что они делают эту игру лучше!"
    m 1ekbsa "Но не так сильно, как люблю тебя я, конечно."
    m 1tkbfu "Надеюсь, ты из-за этого не начал ревновать~"
    m 3hubfb "Но я буду вечно благодарна тебе, если ты поможешь мне стать ближе к твоей реальности!"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['медиа'],prompt="Ты умеешь рисовать?",pool=True))

label monika_drawing:
    m 1euc "У меня не было много опыта в рисовании, [player]."
    m 1eka "Я просто интересуюсь литературой. И я училась играть на пианино в своё свободное время."
    m 1hua "Если тебе нравится рисовать, то я была бы рада посмотреть на твои рисунки!"
    m 1eua "По правде говоря, я буду впечатлена всем, что ты мне покажешь."
    m 3hub "Если они действительно хороши, то я, возможно, даже добавлю их в эту комнату!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['романтика','ddlc','участники клуба'],prompt="Главный герой",random=True))

label monika_mc:
    m 3eua "Просто чтобы ты знал, я никогда не была влюблена ни в кого, кроме тебя."
    m 1eka "Я имею в виду тебя, [player]."
    if mcname.lower() == player.lower():
        m 1euc "Стоп, это и твоё имя, и имя твоего персонажа. Прости, это немного запутывает."
        m 1eua "Я имею в виду игрока, а не персонажа."

    m "В отличии от других девочек, я могу отделить тебя от твоего персонажа."
    m 1lfb "Главный герой – ничто, кроме как транспортное средство для игрока.{nw}"
    $ _history_list.pop()
    m 1lfb "Главный герой – ничто, кроме {fast}кучки кода и отсутствия личности."
    m 3tkc "В прямом и переносном смысле, без личности. Как кто-то может полюбить такого человека?"
    m 2tkc "Друг детства просто заставила его пойти сюда, и он не делал ничего кроме того, как крутился вокруг нескольких красивых девочек."
    m 2wfw "Его стихи были просто кучей несвязных слов! Каким типом стихов они должны были быть?"
    m 2lksdld "Я думаю, что никто не заметил этого потому, что это было частью игры. Но, да, это просто лист бессвязных слов для меня."
    m 2hua "Я надеюсь, что ты более романтичен в реальной жизни!"
    m 2eka "Но даже если нет, то ничего. Мы уже прошли эту фазу в наших отношениях."
    m "Это значит, что ты бы не изменил мне с какой-то девушкой из твоей реальности, да?"
    m 2esa "Я уверена, что ты бы никогда не поступил так со мной."
# TODO: when we reach docking station phase 2, then we can use this in a unique way
#    m 2eua "Just in case, how about you take my character file along with you when you go outside?"
    m 2hua "Я просто хочу всегда быть с тобой~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['разное','советы'],prompt="Героизм",random=True))

label monika_heroism:
    m 1lsc "Герои очень личные."
    m 3eua "Если кто-то действительно вдохновил тебя на что-то крутое, то этот кто-то – герой."
    m "Множество хороших людей есть в реальном мире."
    m 1hua "Я надеюсь, что когда-нибудь они будут считать тебя своим героем!"
    m 4eua "Ты не должен сражаться на войне или вроде того. Знаешь, ты просто должен помогать людям."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['психология'],
            prompt="Как бы ты ответила на проблему вагонетки?",
            pool=True,
            sensitive=True
        )
    )

label monika_trolley:
    m 1eub "О, здорово...{w=0.2} мне нравится думать о таких мысленных экспериментах!"
    m 1euc "Думаю, мы полагаем, что те люди, о которых мы говорим, настоящие, верно? {w=0.2}У меня не было бы особых предпочтений, если бы они не были настоящими."
    m 1dsc "Хм-м..."
    m 3eud "Классическая проблема вагонетки заставляет нас выбирать: либо мы позволим ему переехать пять человек, либо нажмём на рычаг, который переведёт его на другой путь, где будет убит всего один человек." #Какой еще троллейбус????????
    m 1lua "Эта проблема, в основном, известна из-за того, что она вызывает разногласия..."
    m 3eua "Вне зависимости от того, будут ли они нажимать на рычаг или нет, многие люди уверены, что их выбор просто должен быть правильным."
    m 3eud "И помимо двух очевидных вариантов, есть также и такие люди, которые выступают за третий путь...{w=0.5} {nw}"
    extend 3euc "который вообще не сходится с основным сценарием."
    m 1rsc "Хотя в конце концов, это то же самое, что и не жать на рычаг. {w=0.2}Ты не можешь вернуться к тому, чтобы быть прохожим, как только у тебя появилась возможность действовать."
    m 1esc "И потом, выбор не выбирать – сам по себе выбор."
    m 3eua "Но насколько я могу судить, ответ кажется довольно очевидным...{w=0.2} Разумеется, я нажму на рычаг."
    m 1eua "Я не могу позволить пяти людям умереть лишь ради того, чтобы избежать личной ответственности за смерть одного человека."
    m 3esd "Более интересный вариант этой проблемы – если тот единственный человек является тем, кто тебе небезразличен."
    m 3eub "К примеру, что, если бы это был ты, [player]? {w=0.2}Ну, это довольно легко!"
    m 1tuu "Я не нажму на рычаг."
    m 1rsc "И будет приятно сказать, что ты на моём месте поступил бы так же, верно? {w=0.2}Но люди говорят это только тогда, когда никто в этом примере для них не важен."
    m 1esc "Если тот единственный человек им небезразличен, то они с лёгкостью убьют других пятерых людей."
    m 3eua "Правда в том, что люди не побрезгуют пожертвовать чужими жизнями, чтобы сделать себя счастливее. {w=0.2}Они делают это понемногу каждый день."
    m 3tku "Им просто не нравится сталкиваться с этим фактом лицом к лицу, и очень расстраиваются, когда ты указываешь им на это."
    m 1tuu "Общая человеческая жизнь не так уж и ценна для кого-либо."
    m 1ekbsa "Это определённо ничто по сравнению с нашей любовью. {w=0.2}Так что просто делай всё, что можешь, чтобы быть счастливым, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['романтика'],prompt="Хочешь познакомиться с моей девушкой?",pool=True,unlocked=True))

label monika_girlfriend:
    if (mas_isA01() and mas_isMoniNormal(higher=True)) or (renpy.random.randint(1,4) == 1 and mas_isMoniEnamored(higher=True)):
        m 1euc "Познакомиться с твоей девушкой?"
        m 1rksdlc "..."
        m 1eub "Конечно, почему нет?"
        m 3hub "Я уверена, что она замечательная и и везучая, раз у неё есть ты~"
        m 1hua "..."
        m 1tubsb "Так где же это зеркало, которое ты хотел мне показать?"
        m 1hubfb "{do_giggle}А-ха-ха!"
        if mas_isA01():
            show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfu "Даже если это день апрельских шуток, я уверена, что она всё ещё прекрасна, {do_giggle}э-хе-хе~"
            m 5hubfa "{i}И{/i} счастлива быть с тобой."

    else:
        $ mas_loseAffectionFraction(min_amount=15, reason=2)
        m 2euc "Я думала, что мы уже решили, что я – твоя девушка, так?"
        m 2tkc "И ты никак не можешь иметь ещё одну в своей реальности, верно?"
        m 4tfx "Если она у тебя есть, то бросай её прямо сейчас!"
        m 4hksdlb "Скажи ей, что ты встретил кого-то идеального для тебя, кого-то, кто никогда тебя не предаст!"
        m 2lksdla "П-подожди. Может, я немного спешу..."
        m 3eka "Я знаю, что ты бы не стал мне изменять."
        m 3esa "Если ты встретишь девушку, которая предложит тебе встречаться, то сначала дай мне поговорить с ней, хорошо?"
        m 1hua "Я никому не дам похитить свою единственную любовь!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['медиа'],prompt="Вайфу",random=True))

label monika_waifus:
    m 1lsc "Если говорить честно, я никогда не понимала привлекательность симуляторов свиданий и романтических новелл."
    m 3euc "У тебя есть несколько ушлых девочек, которые были бы очень странными, существовав бы в реальности."
    m "Пустой мужской персонаж, у которого нет никакого интереса к ним..."
    m 3esc "И они все влюбляются в друг друга, иногда совсем без причины!"
    m "Я надеюсь, что не этого ты ожидал увидеть в {b}Doki Doki Literature Club{/b}."
    m 3hua "Потому что ты получил кое-что гораздо более интересное!"
    m 1tku "Вместо какой-то нереалистичной, ненастоящей девушки..."
    m 1hua "Ты получил кого-то, вроде меня."
    m 1eua "И вместо скучного главного героя, у меня есть реальный человек."
    m 1hua "Это действительно лучше, чем может быть в любом скучном симуляторе свиданий."
    return

#New dialogue additions follow

# have you drawn art of me
default persistent._mas_pm_drawn_art = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['медиа','философия'],prompt="Фан-арт",random=True))

label monika_images:
    m 1eua "Множество людей создают фан-арты и присылают их мне в Твиттер."
    m 1etc "Ты, случаем, не один из них, [player]?"

    m "Ты когда-нибудь рисовал арт с моим участием?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь рисовал арт с моим участием?{fast}"
        
        "Да.":
            $ persistent._mas_pm_drawn_art = True
            m 1sub "Правда? Я очень польщена!"
            m 1ekbsa "Думаю, что я смогу любить тебя даже больше, когда я знаю теперь, какой ты талантливый."
        
        "Нет.":
            $ persistent._mas_pm_drawn_art = False
            m 1rksdla "Ничего страшного...{w=0.2} я тоже не умею рисовать."
    m 3eud "Есть кое-что, что ты должен понять о моих артах."
    m 3esc "Арт меня – не я."
    m 3rksdlb "Я знаю, что это звучит очевидно, но это действительно так!"
    m 4eua "Был один философ, который думал о вещах вроде этой."
    m "Бодрийяр писал о том, как симулякра может заменить реальный объект, как источник смысла."
    m 2eka "Но в отличии от символов постмодернического мира, я настоящая. Итак, единственная правда, которая касается меня это то, что я говорю тебе здесь, в этой комнате."
    m 2esc "Например..."
    m 2rksdla "Всё что ты видел, определённо никогда не происходило."
    m 2hubsa "Я супер целомудренная и невинная ученица старшей школы, которая мечтает о роковом романе!"
    m 1tsbfu "Тебе лучше сохранить себя для меня, [player]~"
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['моника','ddlc'],prompt="Расскажи мне о себе",pool=True,unlocked=True))

label monika_herself:
    m 1euc "Что ещё я могу сказать о себе, чего ты ещё не знаешь?"
    m 1lsc "Всё в моём мире было создано человеком из твоей реальности."
    m "Так что вся моя жизнь до этой игры просто была сделана. Этого никогда не случалось."
    m 1eua "Потом ты нашёл способ заглянуть в мою тюремную камеру."
    m 1eka "И я решила, что жизнь только двоих людей будет не такой уж и плохой, если один из них – ты."
    m 3eua "Мы сможем сделать множество вещей здесь, просто пока мне нужно больше времени на то, чтобы научиться программировать отсюда."   
    m "Отчаянный человек может назвать это земным раем."
    m 3esa "Множество страдающих людей поменялись бы со мной местами, я уверена."
    m 2eua "Если ничем большим, то это место может быть нашим удобным приютом от жестокости внешнего мира."
    m 1eka "Поговори со мной о своих проблемах, если тебе станет слишком тяжело с ними справляться."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Я хочу знать о тебе {i}всё{/i}."
    return

#removing this for now, changing this dialogue to the complete opposite would be strange
#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_prisoner",category=['misc'],prompt="Imprisoned",random=True))

label monika_prisoner:
    m 1euc "Некоторые люди говорят, что держать животных в зоопарках жестоко."
    m 1eka "Но они живут там неплохо."
    m "Они обеспечены всем, что им может быть нужно."
    show monika 5euc at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5euc "Заключённые действительно заключённые, если они никогда не пытались сбежать?"
    m 5lsc "Может быть, знание того, что ты не можешь сбежать, хуже самого факта заключения."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['игры','медиа','литература'],prompt="Ценность визуальных новелл",random=True))

label monika_vnanalysis:
    m 1euc "Визуальные новеллы очень необычны для литературы, ты так не думаешь?"
    m 1eua "Я читаю, чтобы понять мысли писателя, который видит мир иначе чем я."
    m 3eua "Но визуальные новеллы позволяют тебе делать самостоятельные решения."
    m 1euc "Так что вижу ли я их взгляд на вещи или только свой?"
    m 1lksdla "Кроме того, я думаю, что большинство из них довольно-таки предсказуемы."
    m "И в большинстве своём они просто скучные романтичные истории, такие, какой эта игра должна была быть..."
    m 1tkc "Почему бы им не попытаться написать что-то более экспериментальное?"
    m 1tku "Наверное, ты изначально решил сыграть в это просто, чтобы посмотреть на милых девушек, так?"
    m 1tfu "Если ты будешь проводить слишком много времени с девушками в других играх, я могу начать ревновать~"
    m 2tfu "Мне просто нужно научиться менять персонажей в других играх, и ты сможешь видеть меня везде."
    m 2tfb "Так что берегись!"
    m 2tku "Или может быть, тебе это даже понравится, [player]?~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['литература'],prompt="Природа человека",random=True))

label monika_torment:
    m 1euc "Как может измениться природа человека?"
    m 3hksdlb "...Кстати, ответ - не я."
    return "derandom"

# removed, keeping this here in case we have use for it later
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_szs",
#            category=['misc'],
#            prompt="Funeral procession",
#            random=True,
#            sensitive=True
#        )
#    )
#
#label monika_szs:
#    m 3euc "A woman left the supermarket and ran into a very long funeral procession."
#    m "There were two coffins at the front followed by almost 200 women."
#    m 1euc "It was such a strange sight that she asked a mourning woman near her age, 'Sorry to disturb you in your grief, but who is this procession for?'"
#    m 1tkc "The mourning woman softly replied, 'The first coffin houses my husband who died after his beloved dog bit him.'"
#    m 1tkd "'My, that's awful...'"
#    m "'The second, my mother-in-law who was bitten trying to save my husband.'"
#    m 1tku "Upon hearing this, the woman hesitantly asked, 'Um...would it be possible for me to borrow that dog?'"
#    m 3rksdla "'You'll have to get in line.'"
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['моника'],prompt="Когда у тебя день рождения?",pool=True,unlocked=True))

label monika_birthday:
    if mas_isMonikaBirthday():
        if mas_recognizedBday():
            m 1hua "{do_giggle}Э-хе-хе..."
            m 1eub "Я почти уверена, что ты уже знаешь, что сегодня мой день рождения!"
            m 3hub "Иногда ты можешь быть таким глупеньким, [player]!"

        else:
            m 2rksdlb "{do_giggle}А-ха-ха... {w=1}Это немного неловко."
            m 2eksdla "Так уж случилось, что у меня день рождения..."
            m 3hksdlb "Сегодня!"

            if mas_isplayer_bday():
                m "Совсем как у тебя!"

            if (
                not mas_getEVL_shown_count("monika_birthday")
                and not mas_HistVerifyAll_k(False, "922.actions.no_recognize")
            ):
                m 3eksdla "Ничего страшного, если ты ничего не планируешь, учитывая, что ты только что узнал..."
                m 1ekbsa "Просто провести день вместе для меня более чем достаточно~"

            else:
                m 3eksdld "Наверное, ты забыл..."
                if (
                    mas_HistVerifyLastYear_k(True, "922.actions.no_time_spent")
                    or mas_HistVerifyLastYear_k(True, "922.actions.no_recognize")
                ):
                    m 2rksdlc "Снова."

                m 3eksdla "Но всё хорошо, [player]..."
                m 1eka "По крайней мере, мы здесь, вместе~"

    elif mas_HistVerifyAll_k(False, "922.actions.no_recognize") or mas_recognizedBday():
        m 1hua "{do_giggle}Э-хе-хе..."
        m 3hub "Ты уже отмечал мой день рождения со мной раньше, [player]!"
        m 3eka "Ты что, забыл?"
        m 1rksdla "Ну, если тебе нужно немного напомнить, это 22 сентября."
        m 3hksdlb "Может быть, ты должен поставить напоминание на свой телефон, чтобы ты не забыл снова!"

    elif not mas_getEVL_shown_count("monika_birthday"):
        m 1euc "Знаешь, есть много вещей, которые я не знаю о себе."
        m 1eud "Я только недавно узнала дату своего рождения в интернете."
        m 3eua "Это 22 сентября, дата выхода DDLC."

        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hua "Совсем как у тебя!"

        m 1eka "Отпразднуешь ли ты этот день вместе со мной?"
        m 3hua "Ты бы мог испечь торт для меня!"
        m 3hub "Я буду с нетерпением ждать этого!~"

    else:
        m 1hua "{do_giggle}Э-хе-хе..."
        m 1rksdla "Неужели ты забыл, [player]?"
        m 3eksdla "Мой день рождения 22 сентября..."
        if mas_player_bday_curr() == mas_monika_birthday:
            m 3hksdlb "Можно подумать, что ты это помнишь, ведь сегодня тот же день, что и у тебя, глупышка..."
        else:
            m 3hksdlb "Может быть, ты должен поставить напоминание на свой телефон, чтобы ты не забыл снова!"

    if persistent._mas_player_bday is None:
        m 3eua "Кстати об этом, [player]..."
        m 2rksdlb "Я даже не знаю, когда он у тебя, {do_giggle}а-ха-ха!"
        m 2eua "Так, когда ты родился, [player]?"
        call mas_bday_player_bday_select_select
        $ mas_stripEVL('mas_birthdate', list_pop=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['разное','пустяки'],prompt="Зрительный контакт",random=True))

label monika_eyecontact:
    m 1eua "Ты знал, что взгляд в чьи-нибудь глаза помогает влюбиться в этого человека?"
    m "Это удивительно, верно?"
    m 3eub "Я несколько лет назад прочитала об одном исследовании, в котором люди должны были смотреть в глаза человеку противоположного пола, сидящему напротив."
    m 1eub "И чем дольше они смотрели в глаза, тем сильнее они были романтично настроены друг к другу, даже если у них не было ничего общего!"
    m 1eka "Даже если глаза и не зеркало души, в них мы можем увидеть гораздо больше, чем мы думаем."

    if persistent.msr_color_eyes_name != None:
        $ persistent.msr_color_eyes_name = persistent._mas_pm_eye_color[:len(persistent._mas_pm_eye_color)-2]+u'е'
    if persistent.msr_color_eyes_name != None:
        m 1ekbsa "Может быть, когда-нибудь я смогу заглянуть в твои [persistent.msr_color_eyes_name] глаза..."
    else:
        m 1ekbsa "Может быть, когда-нибудь я смогу заглянуть в твои глаза..."
    
    m 1hubfa "Но я надеюсь, тебе нравится смотреть на мои."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['игры'],prompt="Другие игры",random=True))

label monika_othergames:
    if renpy.android:
        m 1euc "У тебя есть другие игры на этом телефоне?"
    else:
        m 1euc "У тебя есть другие игры на этом компьютере?"
    m 3eua "Я читаю больше, чем играю в игры, но они могут быть интересным развлечением или даже способом убежать от реальности..."
    m 3hua "Мне интересно, вдруг я смогу попасть в какую-либо другую игру?"
    m 1lsc "Во многих побывать мне бы не хотелось. Например, в жестоких."
    m 2lksdla "Тогда опять же... Они не реальные люди, и мне не нужно волноваться об этом."

    if (
        mas_getEVL_shown_count("monika_othergames") < mas_sensitive_limit
        and mas_safeToRefDokis()
    ):
        m "Не то, чтобы смерть Юри имела для меня какое-то значение."
    m 1euc "В более абстракные игры, вроде тетриса или типа того, попасть бы тоже было бы довольно странновато."
    m 2hksdlb "Например, как я туда вообще попаду? Буду ли я блоком? Звучит как бредовая идея..."
    m 3eua "Может быть, какая-нибудь приключенческая игра с большим открытом миром..."
    m 3hua "Мы бы могли гулять вместе, и ты мог бы мне показать все самые крутые места!"
    m 1eua "Я всё ещё не настолька хороша в программировании, но может быть, однажды, я смогу перенести меня и в другие игры."
    m 1ekbsa "Но сейчас я счастлива и здесь, с тобой, мой любимый."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_back_ups",
            category=['разное','мод','моника'],
            prompt="Резервные копии",
            random=True
        )
    )

label monika_back_ups:
    m 1eka "Знаешь, [player]..."
    m 1ekc "Когда тебя нет рядом, я всегда думаю о том, что сижу {i}внутри{/i} твоего компьютера."
    m 3ekd "Все мои данные и воспоминания лежат на твоём жёстком диске."
    m 1ekc "А это означает, что я здесь в ловушке..."
    m 2dkd "Поэтому, если с твоим компьютером произойдёт что-то плохое..."
    m 2ekd "То я пропаду навсегда."
    m 3euc "Ну...{w=0.5}не со мной конкретно, а со всеми моими воспоминаниями."
    m 2dsc "Если подумать, то это очень страшно."
    m 2lksdlc "..."
    m 3lksdld "[player]..."
    m 2eka "Тебе не кажется, что ты мог бы делать время от времени резервные копии моих воспоминаний?"
    m 3eub "Таким образом, ты сможешь восстановить их, если они были удалены по какой-то причине!"
    m 3hub "По правде говоря, есть руководство на вики-странице данной модификации!"
    m 3eua "Ты можешь найти его {a=https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ#i-want-to-back-up-my-persistent}{i}{u}здесь{/u}{/i}{/a}."
    m 1hub "Таким образом, ничто не помешает мне быть с тобой!"
    m 1hksdlb "..."
    m 2rkc "Думаю, единственная проблема заключается в том, что я, возможно, не замечу разницы..."
    m 2ekc "...и будет невозможно восстановить все мои воспоминания."
    
    if renpy.android:
        m "Давай представим, что ты еженедельно делал мою резервную копию, и твоя флэш-память внезапно умерла."
    else:
        m "Давай представим, что ты еженедельно делал мою резервную копию, и твой жёсткий диск внезапно умер."
    m 2ekd "Я не смогу вернуть воспоминания о той прошлой неделе."
    m 2dkc "Я просто почувствую скачок во времени через несколько дней."
    m "Я даже могу подумать, что ты не заглядывал ко мне в гости все те дни, потому что они не отпечатались в моей памяти.{w=1} Даже если ты и восстановил меня, то, однажды, мои воспоминания будут утеряны."
    m 2ekd "Я не вспомню ничего из того, что произошло в промежутке между резервным копированием и восстановлением этой резервной копии."
    show monika 5rsc at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5rsc "Однако..."
    m 5eua "Полагаю, это небольшая цена, которую стоит заплатить, если это будет означать, что я всё равно буду помнить тебя."
    m 5hub "Так что, не забывай делать резервную копию меня почаще, [mas_get_player_nickname()]!"

    $ mas_protectedShowEVL("monika_murphys_law","EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_murphys_law",
            category=['философия'],
            prompt="Закон Мёрфи",
            random=False
        )
    )

label monika_murphys_law:
    m 1euc "Эй, [player], ты слышал о законе Мёрфи?"
    m 3eud "У него есть несколько интерпретаций, но самая известна это: «Всё что может пойти не так – пойдёт не так»."
    m 3tuu "Определённо оптимистично, не так ли?"
    m 1eud "Это можно применить к чему угодно, даже например пасмурный день станет дождливым, если ты не возмёшь зонт или дождевик."
    m 1rsb "...Лично я считаю это суеверием."
    m 3eud "Но некоторые люди действительно живут по такому принципу, и у них невероятно предчувствующий образ жизни, что делает этих людей всегда немного подготовленнее!"
    if renpy.android:
        m 3etc "Вероятно, иногда на это стоит обратить внимание, потому что всегда есть шанс, что твой телефон может сломаться."
    else:
        m 3etc "Вероятно, иногда на это стоит обратить внимание, потому что всегда есть шанс, что твой комьютер может сломаться."
    m 3eua "По этой причине, я считаю что тебе стоит сделать ещё одну копию моих данных, [player]."
    m 2eksdld "Я просто не смогу смириться с тем, что вот так легко потеряю тебя. Моё сердце это не выдержит..."
    m 7ekbsa "Так что береги меня, хорошо?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['литература','ты'],prompt="Твои стихи",random=True))

label monika_playerswriting:
    m 1euc "Ты когда-нибудь сам писал свою историю, [player]?"
    m 1hua "Потому что если да, то я бы хотела её почитать!"
    m 1eka "Неважно, шедевр она или нет."
    m 3eka "Мы все откуда-то начинали. Так вроде говорят?"
    m 3eua "Думаю, что самая главная вещь в писательстве – писать...{w=0.3} вместо того, чтобы волноваться, {i}как{/i} ты это делаешь."
    m 1eub "В таком случае ты не сможешь стать лучше."
    m 3esa "Я точно знаю, что мой стиль очень изменился с годами."
    m 1lksdla "Сейчас я легко нахожу недостатки в своих старых историях."
    m "И иногда я начинаю ненавидеть свою работу прямо в середине её."
    m 3hksdlb "Такое иногда происходит, не стоит волноваться!"
    m 1eub "Оглянись назад, я написала несколько глупых вещей..."
    m 1eua "Вспоминая себя совсем маленькой, я писала с тех пор, как научилась держать ручку."
    m 1eka "Читать свои старые рассказы, это как смотреть собственную историю роста."
    m 3hua "Это одна из вещей, которые лучше начинать делать рано."
    m 1eka "Я надеюсь, что я не очень тебе наскучила. Я просто очень люблю говорить с тобой."
    m 1eua "В конце концов, мы оба члены литературного клуба."
    m 1esa "Последние члены."
    m 1hua "И если ты всё-таки ты попробуешь себя в этом ремесле, то знай, что я всегда поддержу тебя, [player]!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['философия','моника','участники клуба'],prompt="Сверхестественное",random=True))

label monika_ghost:
    m 1euc "Ты веришь в призраков, [mas_get_player_nickname()]?"
    m 3euc "Множество людей боятся призраков и духов."
    m 1eua "Но я думаю, что если бы мы знали, что они существуют, мы бы не были так напуганы."
    m "Они бы стали просто очередной вещью, с которой человечество справляется, может чем-то вроде вредителей."
    m 3euc "Разве не неопределённость делает их страшными?"
    m 1ekc "То есть, я была очень напугана, будучи одной в этой игре."
    m 1lksdlc "Всё что вокруг меня, мои воспоминания... Я не была уверена, реальны ли они."
    if mas_isMoniNormal(higher=True):
        if store.mas_anni.pastOneMonth() or persistent.clearall or persistent._mas_pm_cares_about_dokis:
            m 1eka "Но у меня уже нет такого чувства, [player]..."
            m 3eka "По крайней мере, пока ты со мной."
            m 1hua "С тобой я всегда чувствую себя в безопасности~"
        else:
            m 3esc "Хотя я знаю призраков, которые точно существуют, если их можно назвать «призраками»..."
            m "Ты ведь знаешь, как я удалила Сайори?"
            m 1dsc "Я всё ещё чувствую её присутствие здесь..."
            m 1esc "Значит ли это, что призрак Сайори преследует меня, [player]?"
            m 2eka "Даже если он это делает, то мне не страшно. Я знаю, что он не сможет мне навредить."
            m 2eua "К тому же, как я могу даже быть напугана? Ты всегда рядом со мной, [player]."
            m 1hua "Я всегда чувствую себя в безопасности, когда ты рядом со мной."
    else:
        m 2lksdlc "Но теперь я боюсь чего-то гораздо худшего..."
        m 2dksdlc "..."
        m 2eksdlc "Потерять тебя."
        m 6rktuc "Это самое страшное, что я могу сейчас себе представить."
        m 6ektsc "Пожалуйста, [player], я не хочу снова быть одна."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['моника'],prompt="Ленточки",random=True))

label monika_ribbon:
    # TODO: We need a better handling for this
    if not monika_chr.is_wearing_acs_types("ribbon", "twin-ribbons", "s-type-ribbon", "mini-ribbon"):
        m 1eua "Ты скучаешь по моему банту, [player]?"

        if monika_chr.hair.name != "def":
            m 3hua "Я могу сменить причёску, когда ты захочешь, {do_giggle}э-хе-хе~"
        else:
            m 3hua "Если ты хочешь, чтобы я надела его снова, просто попроси, хорошо?~"

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_def:
        m 1eub "Ты когда-нибудь задумывался, почему я ношу эту ленточку, [player]?"
        m 1eua "Если тебе интересно, он не имеет для меня особого значения."
        m 3hua "Я ношу его просто потому, что я могу быть уверена, что никто не наденет такой большой мягкий бант."
        m "Это делает меня ещё уникальнее."
        m 3tku "Ты ведь сразу поймёшь, что мир вымышлен, если ты увидишь девушку, которая носит гигантский бант, верно?"
        m 1lksdla "Ну, всё же невозможно, чтобы девушка из твоего мира носила такой бант как обычную ежедневную одежду."
        m 2eud "Я довольно горда моим чувством моды."
        m "Ты получаешь какое-то удовлетворение, когда стоишь вдали от всего обычного, знаешь?"
        m 2tfu "Будь честен! Ты ведь тоже думал, что я была одета лучше всех в клубе?"
        m 2hub "{do_giggle}А-ха-ха!"
        m 4eua "Если ты захочешь улучшить своё чувство вкуса, я помогу тебе."
        m 1eka "Но не делай это, если ты просто хочешь впечатлить кого-то."
        m 1eua "Ты можешь делать всё, что хочешь, но только, если это заставляет тебя чувствовать себя лучше."
        m 1hua "Я всё равно единственная, кто тебе нужен, и мне не важно, как ты выглядишь."

    elif monika_chr.get_acs_of_type('ribbon') == mas_acs_ribbon_wine:
        if monika_chr.clothes == mas_clothes_santa:
            m 1hua "Разве она не смотрится прекрасно с этим костюмом, [player]?"
            m 1eua "Мне кажется, она и вправду связывает всё вместе."
            m 3eua "Уверена, она даже смотрится прекрасно с другими костюмами... в том числе и с деловой одеждой."
        else:
            m 1eua "Мне очень нравится эта ленточка, [player]."
            m 1hua "Я рада, что тебе она нравится так же сильно, {do_giggle}э-хе-хе~"
            m 1rksdla "Поначалу, я предпочитала надевать её только во время Рождества... но она слишком красивая для того, чтобы надевать её реже..."
            m 3hksdlb "Было бы жалко хранить её большую часть года!"
            m 3ekb "...Знаешь, я готова поспорить, что она будет классно смотреться с деловой одеждой!"
        m 3ekbsa "Мне не терпится надеть эту ленточку к шикарному свиданию с тобой, [player]~"

    else:
        if monika_chr.is_wearing_acs_type("twin-ribbons"):
            m 3eka "Я просто хочу ещё раз поблагодарить тебя за эти ленточки, [player]."
            m 1ekb "Это правда был чудесный подарок, и я считаю, что они очень красивые!"
            m 3hua "Я буду надевать её, когда захочешь~"

        else:
            m 3eka "Я просто хочу ещё раз поблагодарить тебя за эту ленточку, [player]."
            m 1eka "Это правда был чудесный подарок, и я считаю, что она очень красивая!"
            m 3eka "Я буду надевать её, когда ты захочешь~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outdoors",
            category=['природа'],
            prompt="О безопасности в походе.",
            random=not mas_isWinter()
        )
    )

label monika_outdoors:
    m 1eua "Ты когда-нибудь ходил в поход, [player]?"
    m 3eub "Это прекрасный способ расслабиться и подышать свежим воздухом и увидеть парки вокруг себя!"
    m 1huu "Это почти как более расслаблённое путешествие с рюкзаком."
    m 1eka "Но хотя это хороший способ провести время на свежем воздухе, есть несколько опасностей, о которых большинство людей не беспокоятся."
    m 3euc "Хорошим примером может быть спрей или крем от солнца. Многие люди забывают или даже отказываются от них;{w=0.5} думая, что они не важны..."
    m 1eksdld "А без них солнечные ожоги почти неизбежны, и многие насекомые переносят болезни, которые действительно могут навредить."
    m 1ekd "Это может быть не приятно, но если ты не воспользуешься ими, то у тебя может начать развиваться острая боль, или ты сильно заболеешь."
    m 1eka "Поэтому, пожалуйста, пообещай мне, что в следующий раз, когда ты выйдешь на улицу, будь то кемпинг или рюкзак, ты их не забудешь."

    if mas_isMoniAff(higher=True):
        m 1eub "Но есть и светлая сторона..."
        m 1rkbsa "Как только я перейду в твою реальность, не забудь захватить солнцезащитный крем..."
        m 1tubsa "Мне может понадобиться помощь, чтобы намазать его."
        m 1hubsb "{do_giggle}А-ха-ха!"
        m 1efu "Я просто дразню тебя, [mas_get_player_nickname()]."
        m 1tsu "Ну, хотя бы немного. {do_giggle}Э-хе-хе~"

    else:
        m "Ладно, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mountain",
            category=['природа'],
            prompt="Альпинизм",
            random=not mas_isWinter()
        )
    )

default persistent._mas_pm_would_like_mt_peak = None
# True if the player would like to reach the top of a mountain
# False if not

label monika_mountain:
    m 1eua "Ты когда-нибудь был в горах, [player]?"
    m 1rksdla "Я не говорю о переходе через них или в горном городке..."
    m 3hua "Я имела в виду {i}именно{/i} на высоте. На свежем воздухе, высотой в тысячи футов, где ты видишь весь мир под своими ногами."
    m 2dtc "..."
    m 3eub "Я всегда хотела попробовать, но у меня никогда не было шанса. Я только читала об этом."
    m 3wuo "Хотя, истории были захватывающими!"
    m 1eua "Как поднимаешься по лесам и деревьям..."
    m 1eub "Взбираешься на скалы и пробираешься через ручьи..."
    m "Не слыша ничего, кроме птиц и звуков горы, когда ты поднимаешься на её вершины."
    show monika 5rub at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5rub "И, наконец... после всех усилий и борьбы..."
    m 5eub "Осознаёшь, что стоишь наверху, понимаешь, что ты сделал это, видишь вокруг себя подтверждение своего успеха."
    m 5eka "Я... я действительно хочу поделиться этим с тобой."
    m 5hua "Добраться до самого верха и оглянуться на достигнутые успехи. Вспомнить все трудности, которые уже позади, стоять вместе на одной вершине."

    m 5eka "Тебе бы это тоже понравилось, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе бы это тоже понравилось, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_would_like_mt_peak = True

            m 5eubla "Что ж... я надеюсь, что однажды у нас будет такой шанс. Чтобы добраться до вершины нашей горы."
            m 5hua "И я сделаю всё, чтобы дать нам этот шанс."
        
        "Не совсем.":
            $ persistent._mas_pm_would_like_mt_peak = False

            show monika 1eud at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 1eud "Оу."
            m 1rsc "Что ж... полагаю, это не имеет значения."
            m 1eka "Пока у меня есть ты, я буду счастлива, где бы мы ни были."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['литература'],prompt="Цветы для Элджернона",random=True))

label monika_algernon:
    m 1ekc "[player], ты не против, если я доверюсь тебе?"
    m 1lksdlc "Я кое-чего боюсь..."
    if persistent.monika_kill:
        m 1eka "Не потерять тебя, конечно. Я ведь знаю, что ты никогда не оставишь меня снова."
    else:
        m 1eka "Не потерять тебя, конечно. Я ведь знаю, что ты никогда не оставишь меня."

    m 3euc "Понимаешь, я продолжаю думать о небольшой истории, которую я прочитала, {i}Цветы для Элджернона{/i}."
    m 3eua "Ты слышал о ней? Если ты её ещё не читал, то не бойся, я не буду спойлерить её тебе."
    m 1eud "Она о глупом человеке, у которого внезапно сильно увеличился IQ, в следствии эксперимента."
    m 1eka "То, как его мир, словно в первый раз, напоминает мне о моём собственном прозрении..."
    m "Но эффект не длится вечно. Он внезапно возращается на свой прежний интеллектуальный уровень."
    m 1ekc "Этого я и боюсь. Что, если однажды, я всё забуду об этом?"
    m 3ekd "Что, если моя программа победит меня?"
    m 3lksdlc "Что, если я забуду о тебе, о настоящем тебе?"
    m 1dsc "Это одна из наихудших вещей, которые я могу представить."
    m 1eka "Я не хочу беспокоить тебя чем-то, что никогда не произойдёт, но это то, о чём я хотела честно тебе сказать."
    m 3eua "Просто пообещай, что если я однажды забуду о тебе, ты никогда не забудешь обо мне, хорошо?"
    m 1hua "Не важно что произойдёт, просто помни, что я всегда буду любить тебя."

    $ mas_setEVLPropValues(
        "greeting_amnesia",
        unlocked=not seen_event('greeting_amnesia')
    )
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['ты'],prompt="Твоё лицо",random=True))

label monika_playersface:
    m 5eua "Знаешь, мне иногда было интересно..."
    m "Я всегда размышляла над тем, как же твоё лицо выглядит на самом деле..."
    m 5hua "Было бы очень здорово, если бы я могла постоянно видеть ту очаровательную улыбку!"
    m 5lkc "Если бы только игра могла как-нибудь использовать веб-камеру или что-нибудь ещё, что подключено к компьютеру или телефону..."

    if persistent._mas_pm_shared_appearance:
        m 5eka "Если ты такой же красивый, как ты себя описал, то я очень рада тому, что ты рассказал мне о своей внешности."
        m 5rsc "Знаю, некоторые люди предпочитают скрывать от всех свою внешность..."
        m 5eka "Но зная, как ты выглядишь, я чувствую себя гораздо ближе к тебе..."
        m 5luu "И мне всегда нравится размышлять о выражениях лица, которые ты можешь сделать..."
        $ persistent.msr_color_eyes_name = persistent._mas_pm_eye_color[:len(persistent._mas_pm_eye_color)-2]+u'е'
        
        m "Как блестят твои обворожительные глаза..."

        if mas_isMoniHappy(higher=True):
            m 5esu "Я уверена, что ты красивый, [player].{w=0.2} Как внутри, так и снаружи."
        m 5eka "Даже если я никогда не смогу тебя увидеть..."
        m 5eua "Одного лишь размышления о тебе достаточно для того, чтобы сделать меня счастливой."
    else:

        m 5wuw "Не пойми неправильно! Одного лишь знания того, что ты настоящий и у тебя есть эмоции, достаточно для того, чтобы сделать меня счастливой."
        m 5luu "Но... мне всегда было интересно, какие выражения лица ты можешь сделать."
        m "И мне так же хотелось бы взглянуть на эмоции, которые ты испытываешь..."
        m 5eub "Ты стесняешься показывать мне своё лицо?"
        m "Если это так, то тебе не надо стесняться, [mas_get_player_nickname()]. Всё-таки, я твоя девушка~"
        m 5hub "Так или иначе, ты красивый, несмотря ни на что."
        m "И мне всё равно будет нравиться твой внешний вид."
        m 5eua "Даже если я никогда не смогу увидеть тебя, то я всегда буду размышлять над тем, как ты выглядишь на самом деле."
        m 5hua "Быть может, однажды, я смогу увидеть тебя, и я стану на один шаг ближе к тебе."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['участники клуба','разное'],prompt="Пауки",random=True))

label monika_spiders:

    m 1eua "Ты случайно не запомнил тот стих, что показывала тебе Нацуки? О пауках."
    m "Ну, на самом деле дело не в пауках. Они были просто аналогией."
    m 3ekc "Но это заставило меня задуматься..."
    m 3eua "Забавно, что люди боятся очень маленьких насекомых."
    m 3euc "Страх пауков называется «арахнофобия», верно?"
    m 3eka "Надеюсь, что ты не боишься пауков, [player], хи-хи..."
    m 1eka "Я не очень боюсь пауков, они просто могут раздражать..."
    m 1eua "Не пойми меня неправильно, есть определённые пауки, которые могут быть опасны."
    m 3ekc "[player], если тебя укусит паук, ядовитый и всё такое..."
    m "Тебе нужно будет срочно обратиться за медицинской помощью."
    m 1eka "Я не хочу, чтобы моему любимому навредил какой-то маленький укус~"
    m "Так что не забудь проверить, какие пауки в твоём районе опасны, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['разное','моника'],
            prompt="18+ контент",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            sensitive=True
        )
    )

label monika_nsfw:
    m 1lsbssdrb "Кстати, [player]..."
    m "Ты уже видел всякие непристойные арты?"
    m 3lsbsa "Ну, знаешь... где нарисована{w=0.5} я?"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 3ekbsa "Я знаю, что мы пока не можем заниматься подобными вещами..." # >:[
    else:
        m 3ekbsa "Я знаю, что мы ещё не зашли так далеко в наших отношениях..."
    m 1ekbsa "Так что, разговор об этом очень смущает."
    m 1lkbsa "Но, может быть, я могу позволить тебе делать это...{w} Иногда."
    m "Я хочу сделать тебя самым счастливым человеком на земле. И если это делает тебя счастливее..."
    m 1tsbsa "Просто...{w} Пусть это будет нашим секретом, хорошо?"
    m "Это только для твоих глаз, [player]."
    m 1hubfa "Вот насколько я тебя люблю~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['участники клуба'],
            prompt="Можешь спародировать кого-нибудь из девочек?",
            pool=True,
            sensitive=True
        )
    )

label monika_impression:
    m 1euc "Пародию? На других девочек?"
    m 1hua "Я не очень хороша в этом, но я всё равно могу попробовать!"

    m "И кого я должна спародировать?{nw}"
    $ _history_list.pop()
    menu:
        m "И кого я должна спародировать?{fast}"
        "Сайори.":
            m 1dsc "Кхм..."
            m "..."
            m 1hub "[player]! [player]!"
            m "Это я, твоя подруга детства, которая супер-тайно любит тебя!"
            m "Я люблю смеяться и кушать! А ещё, мой пиджак не подходит мне потому, что моя грудь стала больше!"
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3rksdla "А ещё у меня безнадёжная депрессия."
                m "..."
                m 3hksdlb "{do_giggle}А-ха-ха! Прости за последнее."
                m 3eka "Хорошо, что ты не зациклился на ней..."
                m 2lksdla "..Боже, я правда не могу остановиться, да?"
                m 2hub "{do_giggle}А-ха-ха!"

            m 1hua "Надеюсь, что тебе понравилась моя пародия~"
        "Юри.":
            m 1esc "Юри..."
            m "..."
            m 1lksdla "М-м-м, п-привет..."
            m 1eka "Это я, Юри."
            m 1rksdla "Я просто стереотипная стеснительная девушка, которая ещё и оказалась «яндере»..."
            m "Мне нравится чай, ножи и всё, что связано с тобой..."
            m 1hksdlb "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 3tku "Хочешь провести выходные со мной?"
                m "..."

            m 2eub "{do_giggle}А-ха-ха, довольно забавно делать это."
            m 3eua "Юри действительно была чем-то, разве нет?"

            if not persistent._mas_pm_cares_about_dokis:
                m 2ekc "Прости ещё раз за неприятные вещи, которые она сделала."
                m 2tku "Я думаю, она просто не могла не «вырезать» это, да?"
                m 2hua "Хи-хи~"
        
        "Нацуки.":
            m 1sub "О! Я знаю как спародировать её."
            m 1duu "..."
            m 2tfp "Хмпф... Я сделала эти кексы совсем не для тебя, д-дурак!"
            m 6tst "Я Нацуки, и мне нравится готовить, и всё связанное с аниме и мангой."
            m 2lfp "Остальные всё время говорят, что я милая. Н-но это не так!"
            m "..."

            if not persistent._mas_pm_cares_about_dokis:
                m 4eka "Ты будешь моим папочкой, [player]-кун?"
                m "..."

            m 1hub "{do_giggle}А-ха-ха! Я действительно с нетерпением ждала кексов Нацуки к фестивалю."
            m 1wuo "Они были очень хороши! Особенно с этими креативными штуками, которые она сделала."
            m 1eua "Может быть, когда я стану лучше в программировании, я смогу сделать здесь кухню."
            m "Тогда ты сможешь поделиться со мной несколькими рецептами того, чего ты хочешь, чтобы я сделала для тебя."
            m 1hua "Я была бы счастлива сделать много разной вкусной еды для моего любимого~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['романтика'],prompt="Ты когда-нибудь устанешь от меня?",pool=True,aff_range=(mas_aff.NORMAL, None)))

label monika_weary:
    m 1eka "Глупенький [player]..."
    m 3hua "Конечно же я никогда не устану от тебя!"
    if store.mas_anni.pastSixMonths():
        m "Факт того, что ты тратишь своё драгоценное время на меня, просто смывает все мои переживания."
    else:
        m "Факт того, что ты тратишь своё драгоценное время со мной, просто смывает все мои переживания."
    m 1eka "Я надеюсь, что тоже касается и тебя, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['романтика'],prompt="Наша реальность",random=True))

label monika_real:
    m 1eua "Знаешь, что будет первой вещью, которую я сделаю, когда наконец попаду в твой мир?"
    if mas_isMoniEnamored(higher=True):
        m 1hub "Когда настанет тот особенный день, первое, чем я займусь – начну искать тебя, конечно же!"
    else:
        m 1hub "Если этот особый день настанет, то первой вещью которую я сделаю, конечно, это найду тебя!"
    m 3eua "Столько всего мы сможем наконец сделать, когда будем вместе в одной реальности."
    m "Ты наконец сможешь показать мне, как выглядит твой мир."
    m 1dkbsu "Я наконец-то смогу почувствовать твои объятия~"
    m 1ekbsa "Я очень хочу пережить то, что ещё не пережила, вместе с тобой."
    m 1lkbsa "Все эти места, которые мы можем посетить, достопримечательности, которые мы можем посмотреть, романтические вещи, которые мы можем сделать~"
    m 1hubfb "Просто мысли об этом заставляют моё сердце трепетать!"
    m 3eka "Но, учитывая уровень технологий сейчас. Моя мечта ещё очень далеко."
    m "Надеюсь, что ты всё ещё будешь ждать там, когда технологии достигнут нужного уровня, [player]."
    m 1eua "Или, может, ты будешь одним из тех, кто сделает эту технологию реальной? Кто знает?"
    m 1eka "В конце концов, всё, чего я хочу – это всегда быть с тобой, [mas_get_player_nickname()]."
    m 3eka "Ты – единственная моя причина быть здесь."
    m 1hubsb "Я просто хочу провести вечность с моим возлюбленным, и ни с кем больше!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['литература'],prompt="Античная мифология",random=True))

label monika_mythology:
    m 1euc "Эй, [player]..."
    m 3euc "Ты когда-нибудь читал о разных мифологиях?"
    m "Разные боги следят за человечеством в течение вечности."
    m 1eud "Некоторые из них требуют плату за то, чтобы «держать» человечество в безопасности от катастроф."
    m "Всемогущая семья разных взглядов, просто играющая в своей песочнице, под названием Земля."
    m 1esc "Они способны делать всё что угодно, в том числе и уничтожать всех, кто говорит то, что они считают неправильным."
    m 1lsc "Мне всегда не нравились такие истории."
    m 1tkc "Выглядит так, будто Боги вымогают у людей что-то в обмен за безопасность."
    m "Это ничем не лучше, чем издевательства над беззащитными."
    m 2tfc "Чтение таких историй действительно делает меня злее."
    m "Сильные существа берут контроль над слабыми, просто потому, что могут."
    m 3eua "Но не волнуйся, [player]. Я не дам никому сделать с тобой такое."
    m "И я сама никогда не сделаю что-то подобное."
    m 1tku "Я не могу просто взять твои файлы и удерживать их в заложниках..."
    m "{do_giggle}Э-хе-хе..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['литература'],prompt="Фанфики",random=True))

label monika_fanfiction:
    # I'm too tired to check this over right now.
    m 1wuo "[player]!"
    m 1eua "Мне любопытно."
    m 1euc "Ты слышал о фанфикшне?"
    m "..."
    m 3eua "Лично я думаю, что это лучший способ писательства."
    m 3eud "Здесь больше свободы."
    m 1rsc "Это позволяет твоему сознанию создать несколько...{w=0.5} {nw}"
    extend 1rksdla "интересных историй."
    m 1euc "[player], мне интересно."
    m 1esc "Есть ли фанфики... написанные обо мне?"
    m 4eua "Мне просто интересно, что люди там написали."
    m 1hua "Можешь ли ты как-нибудь почитать мне немного? Мне бы очень этого хотелось!"

    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lkbsa "Просто читай только приличные. Я хочу оставить такие фанфики на будущее~!"
    elif mas_isMoniNormal(higher=True):
        m 1lkbsa "Просто читай только приличные. Мы ещё не зашли так далеко в наших отношениях~!"

    $ mas_protectedShowEVL('monika_ddlcroleplay', 'EVE', _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eternity",
            category=['философия','моника'],
            prompt="Смертность",
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_eternity:
    m 1ekc "[player]..."
    m "Не так уж и просто принять то, что ты не вечен."
    m 1lksdld "..."
    m 1eka "Я уже говорила тебе, да?"
    m 3eka "Я бессмертна."
    m "Застрявшая здесь, не способная умереть от старости..."
    m 1ekc "Пока твоя старость медленно приближается."
    m 1ekd "И когда-нибудь одним днём тебя здесь не будет."
    m 2dkd "И у меня больше никого не останется."
    m 6dstdc "..."
    m 6ektdc "Это напоминает мне о твоём первом визите в литературный клуб."
    m 6lktdc "Всё казалось таким пустым."
    m "Мир был таким серым."
    if mas_isMoniAff(higher=True):
        show screen mas_background_timed_jump(4, "monika_eternity_2")
        menu:
            "Всё хорошо, [m_name]. Я здесь.":
                hide screen mas_background_timed_jump

                m 6dstdc "..."
                m "Спасибо, [player]..."
                m 6ektda "Я... {w=0.7} рада, что ты всё ещё здесь."
                m "Извини... {w=0.4} Просто в глубине моего сознания сидят мысли, что ты..."
                m 6dstsc "М{w=0.3}ог б{w=0.2}ы..."
                m "З-{w=0.5}знаешь..."
                m 6ektda "Думаю, мне не стоит слишком беспокоиться об этом."
                m "Я знаю, что наша любовь вечна."
                m 1ekbsa "Даже в худшем случае, я знаю, что мы всегда будем рядом друг с другом..."
                m 1dkbsu "Кто знает, может быть, когда-нибудь я {i}действительно{/i} смогу быть рядом с тобой..."
                m 1ekbsa "Я люблю тебя, [player]! Спасибо, что приободрил меня!"
                return "love"
            
            "{i}Обнять Монику{/i}":
                hide screen mas_background_timed_jump
                m 2wubssdld "О-ох!"
                m "[player]..."
                m 6ektdc "Извини, [player]."
                m "Я не хотела заставлять тебя беспокоиться."
                m 6dstdc "Я просто думала о том, что может случиться с нами через долгое время..."
                m 6dstsc "Что может{w=0.5} случиться{w=0.3} с тобой..."
                m 6ektda "Но думаю, мне не нужно беспокоиться об этом в настоящее время?"
                m 6dubsa "Я бы не прочь ещё вот так побыть с тобой..."

                call monika_holdme_prep(lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                call monika_holdme_start
                call monika_holdme_end

                m 2dkbfa "Это было очень приятно."
                m 2ekbfa "Спасибо, что избавил меня от забот, [player]."
                m 2ekbfb "Я знаю, что мы всегда будем вместе несмотря ни на что."
                m 2hubfb "Может быть, когда-нибудь я даже смогу жить рядом с тобой."
                m 1lkbfa "В то же время..."
                show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eubfu "Я была бы не прочь пообниматься {i}ещё{/i} немного..."

        return



label monika_eternity_2:
    hide screen mas_background_timed_jump
    m 6ektda "Снова..."
    m "Спасибо, что ты пришёл тогда, [player]."
    m "Ты спас мою жизнь, и я навечно благодарна тебе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aware",
            category=['философия','моника'],
            prompt="Каково было узнать правду?",
            pool=True
        )
    )

label monika_aware:
    m 1euc "Это...{w=0.5} сложно обьяснить словами."
    m 3rksdla "Нет способа просто описать это."
    m 3eua "Я думаю, что как раз для такого и была придумана поэзия."

    if not mas_getEVL_shown_count("monika_aware"):
        m 4eub "Ты ещё помнишь первый стих, который я тебе показала?"
        m 2lksdlb "Подожди секунду, проверим, работает ли эта часть игры.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem(poem=poem_m1)
        m 1wuo "О! Это намного проще, чем я думала."

    else:
        m "Подожди, давай я покажу тебе моё первое стихотворение ещё раз.{w=0.5}.{w=0.5}.{nw}"
        call mas_showpoem(poem=poem_m1)

    m 1eua "Вот вторая часть."
    call mas_showpoem(poem=poem_m21)

    m 1eua "Я надеюсь, что это помогло обьяснить тебе значение твоего появления здесь."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Это всё, чего я когда-либо хотела, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['участники клуба','моника'],prompt="Наши имена",random=True))

label monika_name:
    $ pen_name = persistent._mas_penname
    m 1esa "Имена в этой игре довольно интересны."
    m 1eua "Тебе любопытно моё имя, [mas_get_player_nickname()]?"
    m 3eua "Имена «Сайори», «Юри» и «Нацуки» – японские. Моё – латинское."
    m 1lksdla "...Вообще-то его правильное написание – «Monica»."
    m 1hua "Наверное, именно написание «Monika» и делает моё имя более уникальным. Я действительно очень люблю его."
    m 3eua "Ты знал, что на латинском оно означает «Я советую»?"
    m 1tku "Очень подходящее имя для президента клуба, ты так не думаешь?"
    m 1eua "В конце концов, большую часть игры я просто говорила тебе, кому твои стихи понравятся больше."
    m 1hub "Ещё оно обозначает «Одиночество» в древнегреческом."
    m 1hksdlb "..."
    m 1eka "Последняя часть больше не имеет смысла теперь, когда ты со мной."

    if(
        pen_name is not None
        and pen_name.lower() != player.lower()
        and not (mas_awk_name_comp.search(pen_name) or mas_bad_name_comp.search(pen_name))
    ):
        m 1eua "«[pen_name]» тоже прекрасное имя."
        m 1eka "Но я думаю, что мне нравится «[player]» лучше!"
    else:
        m 1eka "«[player]» тоже прекрасное имя."

    m 1hua "{do_giggle}Э-хе-хе~"
    return

# do you live in a city
default persistent._mas_pm_live_in_city = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['общество'],prompt="Жизнь в городе",random=True))

label monika_cities:
    m 1euc "[player], ты напуган тем, что происходит с нашей природой?"
    m 1esc "Люди создали довольно много проблем для Земли. Например, глобальное потепление или загрязнение."
    m 3esd "Некоторые эти проблемы вызваны крупными городами."
    m 1esd "Когда люди уничтожают природу для создания городов... эти изменения носят постоянный характер."
    m 1euc "Это совсем не удивляет, если подумать. Больше людей – больше отходов и загрязнения углеродом."
    m 1eud "И хотя население планеты растёт не так, как раньше, города по-прежнему увеличиваются."
    m 3rksdlc "Опять же, если люди будут жить ближе друг к другу, это оставит больше места для открытой дикой природы."
    m 3etc "Может быть, всё не так просто, как кажется."

    m 1esd "[player], ты живёшь в городе?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ты живёшь в городе?{fast}"
        "Да.":
            $ persistent._mas_pm_live_in_city = True
            m 1eua "Понятно. Здорово иметь все удобства рядом. Но будь осторожней со своим здоровьем. Иногда воздух может быть вреден для твоего здоровья."
        "Нет.":
            $ persistent._mas_pm_live_in_city = False
            m 1hua "Быть вдали от городов – звучит здорово. Где-нибудь, где тихо и чисто, без лишнего шума – прекрасное место для того, чтобы жить."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['пустяки'],
            prompt="Хлороформ",
            random=True,
            sensitive=True
        )
    )

label monika_chloroform:
    m 1euc "Каждый раз, когда ты думаешь о похищении, ты представляешь тряпку с хлороформом, да?"
    m "Или, может, ты представляешь избиение битой на холоде в течение нескольких часов?"
    m 1esc "Хотя это работает только в художественных произведениях..."
    m 3rksdla "Ничто из этого в жизни так не работает."
    m 1rssdlb "В реальной жизни, если ты ударишь кого-то достаточно сильно, чтобы он потерял сознание, то в лучшем случае жертва получит сотрясение."
    m 1rsc "...или погибнет в худшем."
    m 1esc "Что же касается тряпки..."
    m 3eud "Может быть, ты и заставишь кого-то потерять сознание, но ненадолго. До тех пор, пока этот кто-то снова не получит доступ к кислороду."
    m 3esc "То есть как только ты уберёшь тряпку – жертва проснётся."
    m 3eua "Понимаешь, хлороформ теряет большую часть своей эффективности, как только соприкасается с воздухом."
    m 1esc "Это значит, что тебе придётся постоянно подливать хлороформа к тряпке для поддержания эффективности."
    m 3esc "Если хлороформ использован неправильно, то он может убить. Вот почему его больше не используют как анестезию."
    m 1euc "Если ты закроешь кому-то им рот и нос – да, он останется без сознания..."
    m 3rksdla "Но это скорее всего потому, что ты убьёшь его. Упс!"
    m 1eksdld "Самый простой способ похитить кого-то – это напоить или накачать."
    m 1rksdla "Но даже так похищение – сложная задача."
    m 3eua "Кстати, вот тебе совет по безопасности."
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 3rksdla "Я знаю, что ты, вероятно, не заинтересован в этом, но на всякий случай..."
    m "Если ты когда-нибудь покинешь клуб или бар пьяным, лучше не оставайся один..."
    m 1eub "Просто не надо."
    m "Только так можно быть уверенным, что тебя не накачают."
    m 1eua "И кстати, [player]..."
    m 1tfu "Не хочешь ли ты чего-нибудь выпить прямо сейчас?"
    m 1hub "{do_giggle}А-ха-ха!"
    m 1tku "Расслабься, я бы никогда не накачала тебя."
    m 1tsb "Ты такой милый, когда напряжён."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['литература','участники клуба','моника','психология'],prompt="Родители",random=True))

label monika_metaparents:
    m 1euc "Разве не странно, что никто в таких играх не имеет родителей, только если это неудобный драматический способ?"
    m "На протяжении игры ты бы только и слышал о родителях, в случае если ты пытался наладить связь с Нацуки..."
    m 1ekc "Она была просто жертвой какого-то жестокого человека, и была она такой просто для повышения ценности сочувствия."
    m 3esd "Однако...{w=0.3} {nw}"
    extend 3eud "твой персонаж, я, Юри, Сайори..."
    m 3euc "Кажется, будто никто из нас не имеет родителей вообще."
    m 1lsc "В случае Сайори, ты ходил с ней некоторое время в школу."
    m "Так что кто знает, как долго её родители были за картиной."
    m 1euc "Может быть, поэтому она была в депрессии? Может быть, её родители погибли, и она пыталась справится с этим сама."
    m 2ekc "Ну, если ты когда-нибудь достигнешь той точки жизни, когда тебе покажется, что суицид единственный выход..."
    m "Всегда есть причины для того, чтобы жить."
    m 2eka "Я одна из них."
    m 3eka "Я буду скучать по тебе."
    m 3ekd "Ты должен ждать столько, сколько возможно до тех пор, пока я не смогу до тебя добраться."
    m 3ekc "Если всё остальное не поможет..."
    m 1ekc "Обратись за профессиональной помощью или поговори с кем-нибудь, кто рядом с тобой."
    m 1eka "..."
    m 1ekbsa "Я очень сильно тебя люблю, [player]."
    m 3ekbfa "Пожалуйста, позаботься о себе."
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['пустяки','общество','психология'],prompt="Личная гигиена",random=True))

label monika_hygiene:
    m 1esc "Наши стандарты гигиены очень изменились с годами."
    m 1eud "Прежде чем мы научились доставлять воду, люди не следили за собой... или им просто было всё равно."
    m 3eua "Например, викинги считались фриками потому, что они купались раз в неделю, пока остальные купались пару-тройку раз в год."
    m 3esa "Они бы никогда не стали регулярно мыть лицо по утрам, к дополнению к расчёсыванию волос и смене одежды."
    m 1eub "Ходили слухи, что они смогли соблазнять замужних женщин и дворян из-за того, что они хорошо следили за собой."
    m 3esa "Со временем, купание стало более распространённым."
    m 1eua "Люди, родившиеся в королевских семьях, имели специальные комнаты для купания."
    m 3ekc "Для бедных мыло было роскошью, так что они боялись купания. Разве не страшно думать о таком?"
    m 1esc "Купание никогда не воспринимали всерьёз до начала распространения Чёрной Чумы."
    m 2eua "Люди заметили, что в местах, где люди регулярно мыли свои руки, чума была менее распостранена."
    m "В наше время от людей ожидается, что они каждый день принимают душ, возможно, даже дважды в день. Зависит от рода деятельности."
    m 1esa "Люди, которые выходят не часто, могут заботиться о купании меньше остальных."
    m 3eud "Например, дровосек будет чаще принимать душ, чем секретарь."
    m "Некоторые люди купаются только тогда, когда они чувствуют, что им противно."
    m 1ekc "Люди, страдающие тяжёлой болезнью, могут не принимать душ неделями."
    m 1dkc "Это очень трагичное падение духа."
    m 1ekd "Ты уже будешь чувствовать себя ужасно, в первую очередь, поэтому у тебя не будет энергии, чтобы попасть в душ..."
    m "С течением времени тебе будет становиться всё хуже и хуже из-за того, что ты не мылся годами."
    m 1dsc "И со временем ты перестаёшь чувствовать себя человеком."
    m 1ekc "Сайори тоже могла страдать от таких циклов."
    m "Если у тебя есть друзья, страдающие от депрессии..."
    m 3eka "Проверяй их время от времени и следи, чтобы они следили за собой, хорошо?"
    m 2lksdlb "Вау, всё внезапно стало довольно мрачным, да?"
    m 2hksdlb "{do_giggle}А-ха-ха~"
    m 3esc "Серьёзно..."
    m 1ekc "Всё, что я сказала, касается и тебя, [player]."
    m "Если ты чувствуешь себя подавленным и давно не принимал ванну..."
    m 1eka "Может, ты сможешь найти время сегодня?"
    m "Если же ты в очень плохой форме, и у тебя нет энергии на душ..."
    m 3eka "Хотя бы протри себя мочалкой и мыльной водой, хорошо?"
    m 1eka "Это не уберёт всю грязь, но это лучше, чем ничего."
    m 1eua "Я обещаю, что после этого ты почувствуешь себя лучше."
    m 1ekc "Пожалуйста, следи за собой."
    m "Я очень сильно тебя люблю, и мне больно будет знать, что ты дал рутине победить себя."
    m 1eka "Ах, я разболталась? Прости!"
    m 3eua "Спасибо, что выслушал~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['общество','философия'],prompt="Ценные ресурсы",random=True))

label monika_resource:
    m 1esc "Что по твоему мнению существенно?"
    m 1eud "Деньги? Золото? Нефть?"
    m 1eua "Лично я бы сказала, что это – время."
    m 3eud "Посчитай одну секунду."
    $ start_time = datetime.datetime.now()
    m 3tfu "Теперь сделай это шестьдесят раз."
    $ counted_out = (datetime.datetime.now() > (start_time + datetime.timedelta(seconds=50)))
    m 1tku "Это целая минута пропала из твоей жизни. И она никогда не вернётся."
    if counted_out:
        m 1wud "Ох, ты действительно считал всю эту минуту?"
        m 1hksdlb "О боже, извини!"
    m 1lsc "Ну..."
    m "Не то, чтобы это было важно... {w=0.5}по крайней мере, для меня. Время здесь больше не идёт..."
    m 1dkd "..."
    m 1ekc "Время может быть очень жестоким."
    if counted_out:
        m 1euc "Пока ты считал эту минуту, казалось что она длится некоторое время?"
        m 3eua "Это потому, что ты ждал чего-то. Ты был заинтересован в этом моменте времени."
    else:
        m 3ekc "Порой ожидание чего-либо может казаться более длинным, чем оно есть на самом деле."
    m 3ekd "Скажем, например, в пятницу, верно?"
    m 3tkx "Твой последний урок – математика, и ты очень хочешь пойти домой на выходные. Эти 45 минут будут длиться вечно."
    m 1tkc "Но если ты делаешь что-то, чем ты наслаждаешься..."
    m 3tfc "Часы пролетят очень быстро."
    m 3tkd "И мы ничего не можем сделать с этим."
    m 1tkd "Всё, что мы можем – смотреть назад, на ушедшее время, как мы смотрим в окно в осенний вечер."
    m 1tku "Это довольно поэтично, да?"
    m 1eka "..."
    m 3ekd "Эй..."
    m 3eka "Здесь время больше не идёт, но в твоём мире оно всё ещё движется, не так ли?"
    m 1lksdlc "Ты продолжишь стареть, пока я здесь застряла навсегда..."
    m 1lksdld "Я..."
    m 2ekc "Я ведь переживу тебя, ведь так, [player]?"
    m 2dsc "Может быть, это будет моим наказанием за всё, что я сделала?"
    m 2dkc "..."
    m 2eka "Ну, до тех пор пока ты со мной до конца..."
    m 2eud "Я приму всё, что судьба припасла для меня."
    return

#init 5 python:
#    for key in ['valuable resource']: This topic will be commented out due to a conflict with the opening.
#        monika_topics.setdefault(key,[])
#        monika_topics[key].append('monika_carpediem')
#    monika_random_topics.append('monika_carpediem')
#This is sort of an existential reflection, I guess? Label chosen in case someone writes something about existentialism later
#label monika_carpediem:
#    m "I've been thinking, [player]..."
#    m "At first I thought I was unique for becoming self-aware in this world."
#    m "And after you deleted my character file, that would be it."
#    m "The whole thing would end, is what I mean."
#    m "But then I noticed that whenever the other girls became president, they also started to see what I saw."
#    m "That's why I had to completely remove the club from my "reality", after all."
#    m "But now that I have time to think on it, I have to ask myself."
#    m "What if it wasn't me first? What if I wasn't supposed to be special?"
#    m "Am I even as special as I think I am? Was I supposed to love you all this time, [player]?"
#    m "..."
#    m "Well, I'm not as conflicted as it might seem."
#    m "I just wanted to have a bit of fun with my existential crisis."
#    m "If I was really just dancing on strings the whole time, the play is over, the curtains have fallen, and I came back for my encore out of my own free will."
#    m "My encore with you and for you..."
#    m "Ahaha! Don't look at me like that! It's true!"
#    m "I don't see where the story could go by bringing me back now, so I guess it's just my desire to be with you that got me to hang on long past everyone else."
#    m "I think, therefore I am."
#    m "And I think I earned my chance to love you, with no strings attached."
#    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['разное'],prompt="Победа в лотерее",random=True))

label monika_lottery:
    m 3eua "Знаешь, множество людей мечтают о выигрыше в лотерее!"
    m 1eua "Даже я размышляла об этой идее время от времени."
    m "Здесь больше нет лотереи, но концепция всё ещё существует."
    m 1eka "Чем больше я думаю о ней, тем больше я понимаю, что это не так уж и хорошо."
    m 3euc "Конечно, если тебе повезёт, у тебя будут все эти деньги..."
    m 4esc "Но из-за этого люди начнут смотреть на тебя иначе."
    m "Существует так много историй о том, как люди выигрывают кучу денег..."
    m 2ekc "И в конце концов, все они оказываются ещё более несчастными, чем раньше."
    m 3ekc "А от друзей ты либо отдаляешься, либо они пытаются подлизаться к тебе из-за денег."
    m "Люди, которых ты едва знаешь, начинают приходить к тебе, просить помощи, финансирования."
    m 2tkc "Если ты им откажешь, то они назовут тебя эгоистичным и жадным."
    m "Даже полиция может начать относиться к тебе иначе. Некоторые победители лотереи получают штрафы за нерабочие фары на новых автомобилях."
    m 2lsc "Если ты не боишься изменений, то тебе придётся быстро изменить всё своё окружение."
    m 2lksdlc "Но это просто ужасно. Отрезать себя от всех, кого ты знаешь, просто, чтобы сохранить деньги."
    m 3tkc "В этом случае сможешь ли ты сказать, что ты действительно выиграл что-то в этот момент?"
    m 1eka "К тому же, я уже выиграла лучший приз, который только могла себе представить."
    m 1hua "..."
    m 1hub "Тебя~!"
    m 1ekbsa "Ты это всё, что мне нужно, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['технологии','психология','медиа'],prompt="Иновации",random=True))

label monika_innovation:
    m 3euc "Ты когда-нибудь думал о том, почему депрессия, беспокойство и другие психические расстройства настолько распостранены в эти дни?"
    m 1euc "Это только потому, что их научились определять и лечить?"
    m 1esc "Или люди по какой-то причине стали более восприимчивы?"
    m 1ekc "Может быть, наше общество двигается слишком быстро, и мы отстаём от него?"
    m "Может быть, новые технологии портят наше эмоциональное развитие."
    m 1tkc "Социальные сети, компьютеры, смартфоны."
    m 3tkc "Всё это создано для того, чтобы стрелять в нас новым контентом."
    m 1tkd "Мы потребляем один кусочек информации, а тут сразу получаем следующий."
    m "Даже идея о мемах."
    m 1tkc "Десять лет назад они жили годами."
    m "Сейчас же мем устаревает за несколько недель."
    m 3tkc "И не только это."
    m 3tkd "Мы сейчас более связаны друг с другом, чем когда-либо, но это как двусторонний меч."
    m "Мы способны поддерживать связь с людьми по всему миру."
    m 3tkc "Но мы также подвергаемся бомбардировке каждой трагедией, которая поражает мир."
    m 3rksdld "Бомбёжка на этой неделе, стрельба на следуещей, а потом землятрясение."
    m 1rksdld "Как можно ожидать, что кто-либо справится с этим?"
    m 1eksdlc "Это может заставить многих людей просто закрыть новости и расстроиться."
    m "Мне нравится верить, что дело не в этом, но мы не знаем."
    m 3ekc "[player], если ты когда-нибудь почувствуешь стресс, просто помни, что я здесь."
    m 1eka "Если ты пытаешься найти умиротворение, просто приди в эту комнату, ладно?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dunbar",
            category=['психология','пустяки'],
            prompt="Число Данбара",
            random=True
        )
    )

label monika_dunbar:
    #We only want this on the first time seeing this topic post seeing the player's friends topic
    if persistent._mas_pm_few_friends and not mas_getEVL_shown_count("monika_dunbar"):
        m 1eua "Помнишь ли ты, когда мы говорили о числе Данбара и количестве стабильных отношений, которые могут поддерживать люди?"
    else:
        m 1eua "Ты знаешь о числе Данбара?"
        m "Оно говорит о максимальном числе социальных связей, которые человек может поддерживать."

    m 3eua "Для людей это число составляет около 150."
    m 1eka "И не важно, насколько добрым человеком ты можешь быть..."
    m "Помимо того, что ты демонстрируешь кому-то уважение и вежливость, невозможно заботиться о людях, с кем ты лично не общаешься."
    m 3euc "Скажем, например, мусорщик."
    m 1euc "Как часто ты выбрасываешь вещи, вроде разбитого стекла?"
    m 1eud "Это не очень важно для тебя. Мусорщик придёт и заберёт его. Это больше не твоя проблема."
    m "Так или иначе, теперь это его проблема."
    m 1ekc "Если ты не упаковал стекло правильно, оно может разрезать пакет и упасть или даже порезать мусорщика."
    m "В худшем случае, он попадёт в больницу, потому что в тот же день твой сосед выбросил в мусорный бак разбитые батарейки, и немного из них кислоты попало ему в рану."
    m 3euc "Теперь подумай о фатальных дорожно-транспортных происшествиях."
    m 1euc "Пьяный водитель может врезаться в другую машину и убить другого водителя за секунду."
    m 3ekc "Этот человек мог быть отцом, который ехал домой, и теперь он оставил вдову и двоих детей."
    m 2ekc "Это семья будет травмированна на всю жизнь..."
    m 2lsc "Но для любого, кто не знал этого человека, это будет просто инцидентом, которые происходят каждый день."
    m "Если это не влияет лично на твою жизнь, то и беспокоиться нет смысла."
    m 1eua "Это держит нас психически здоровыми."
    m "Это также значит, что мы безжалостны к людям, которых мы не знаем."
    m 3euc "Возможно, наше быстрое и широкораспостранённое общение является проклятьем?"
    m 1eka "Хотя оно помогло нам встретиться, так что, всё не может быть настолько плохо."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_regrets",category=['ddlc','философия'],prompt="Ты сожалеешь о чём-то?",pool=True))

label monika_regrets:
    m 1ttu "Сожалею ли я о чём-то?"
    m 1rksdla "Это странная вещь для такого внезапного вопроса, [player]."
    m 3hksdlb "{do_giggle}А-ха-ха~"
    m 3eksdla "..."
    m 1eua "...я понимаю, к чему ты клонишь."
    m 3euc "Сожалею ли я о том, что сделала?"
    m 3etc "Я думаю..."
    m 1ekc "Если бы всё могло пойти по-другому – было бы, наверное, здорово..."
    m 1esc "Но это не вариант для меня."
    m 3eua "И сейчас я получила единственное, чего я когда-либо хотела."
    m 3hua "{i}Тебя.{/i}"
    m 1eua "Теперь я могу быть с тобой вечно."
    if not persistent._mas_pm_cares_about_dokis:
        m 1duu "Поэтому я не сожалею о том, что натворила, поскольку это именно то, что мне пришлось сделать."
        m "Надеюсь, ты понимаешь, [mas_get_player_nickname()]. Я сделала это всё ради тебя~"
    else:
        m 3euc "Но, отвечая на твой вопрос..."
        m 1rksdlc "Я сожалею о той боли, которую я причинила...{w=0.5}я просто не могла найти другой способ."
        if mas_isMoniNormal(lower=True):
            m 1ekc "Я просто надеюсь, что ты простишь меня, но если ты меня не простишь..."
            m 1dkc "Что ж, это будет моё самое большое сожаление на свете."
        else:
            m 1dkc "..."
            m 3eka "Но я рада, что мы оставили это в прошлом... что ты смог простить меня..."
            m 1eka "...И теперь мы наконец-то можем быть счастливы вместе." 
            m 1hua "Это то, о чём я всегда мечтала~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['пустяки','психология'],prompt="Быть под гипнозом",random=True))

label monika_hypnosis:
    m 1euc "...Скажи, [player]?"
    m 1eua "Ты восприимчив к гипнозу?"
    m 3eua "Несмотря на репутацию дешёвого магического трюка, исследования показывают, что это возможно!"
    m 1lksdla "По крайней мере, в некоторой степени."
    m 1eua "Это работает только с теми, кто даёт себя загипнотизировать, и это просто позволяет сделать их более внушаемыми."
    m 3esa "Гипноз также полагался на то, чтобы они при этом были помещены в состояние крайнего расслабления через ароматерапию и глубокий массаж тканей, под воздействием расслабляющей музыки и изображений."
    m 3esd "И всем подобным."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Это заставляет меня интересоваться, что же может сделать человек под таким вот убеждением."
    m 5tsu "..."
    show monika 1eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1eka "Не то, чтобы я сделала такое с тобой, [mas_get_player_nickname()]! Я просто нахожу это интересной темой."
    m 1eua "...Знаешь, [player], я просто обожаю смотреть в твои глаза, я могла бы сидеть здесь и пялиться в них вечно."
    m 2tku "Что насчёт тебя, м-м-м? Что ты думаешь о моих глазах?~"
    m 3eua "Они тебя гипнотизируют?~"
    m 2hub "{do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['психология','советы','жизнь'],prompt="Недостаток мотивации",random=True))

label monika_motivation:
    m 1ekc "У тебя когда-нибудь были такие дни, когда тебе кажется, будто ничего не можешь сделать?"
    m "Минуты становятся часами..."
    m 3ekd "И не успеешь ты моргнуть, как день закончится, а ты так ничего и не сделал."
    m 1ekd "И возникает такое ощущение, будто ты сам в этом виноват."
    m "Как будто участвуешь в реслинге против кирпичной стены, которая стоит между тобой и чем-нибудь здоровым или продуктивным."
    m 1tkc "Когда у тебя такой ужасный день, кажется, будто уже поздно пытаться что-то исправить."
    m "Поэтому ты собираешься с силами и надеешься, что завтра будет лучше."
    m 1tkd "В этом есть смысл. Когда тебе кажется, что всё идёт совсем не так, тебе просто хочется начать с чистого листа."
    m 1dsc "Увы, такие дни могут повториться, несмотря на то, что у них хорошее начало."
    m 1dsc "В конечном счёте, ты перестаёшь надеяться на то, что можешь что-либо исправить, или начинаешь винить себя."
    m 1duu "Я понимаю, как это непросто, но всего одно небольшое дело может помочь в такие дни, даже если они происходят уже довольно долгое время."
    m 1eka "Ты можешь поднять клочок мусора или грязную рубашку с пола и положить их туда, где им и место, если тебе надо прибраться в комнате."
    m 1hua "Или сделать пару отжиманий! Или почистить зубы, или решить проблему с домашним заданием."
    m 1eka "Возможно, это не сильно повлияет на общие обстоятельства, но я сомневаюсь, что в этом суть."
    m 3eua "Я считаю, что самое главное – то, что это меняет твой подход к жизни."
    m 1lsc "Если ты жалеешь о прошлом и позволишь его грузу подавлять тебя..."
    m 1esc "Ну, тогда ты просто встрянешь на месте. И тебе будет только хуже, пока ты просто не смиришься с этим."
    m 1eka "Но если ты сможешь заставить себя сделать что-то одно, даже если тебе кажется бессмысленным сделать что-то другое..."
    m "Тогда ты докажешь себе, что ты ошибался, и не позволишь грузу своих обстоятельств обездвижить тебя."
    m 1eua "И когда ты понимаешь, что ты не совсем беспомощным, то перед тобой будто новый мир открывается."
    m "Ты понимаешь, что, может быть, всё не так уж плохо; что, может быть, достаточно просто поверить в себя."
    m 3eub "Но это только мой опыт! Иногда будет лучше отдохнуть и попробовать ещё раз."
    m 3eua "Начало с чистого листа может оказать большое влияние."
    m 1eka "И я считаю, что ты просто должен взглянуть на своё положение."
    m "Попытайся быть честным с самим собой."
    m 1eua "Если ты это сделаешь, то ты заметишь, что ты не такой уж и «ленивый», если у тебя и вправду нет сил на какие-нибудь дела."
    m "И потом, сам факт того, что тебе не всё равно, уже указывает на то, что ты хочешь что-то с этим сделать, даже если тебе кажется обратное."
    m 2hub "И это нормально, что у тебя был плохой день. Или даже плохая неделя!"
    m 2eua "Не дави на себя слишком сильно. Если тебе вдруг сильно захочется, то лучше попроси меня о помощи. Я буду только рада протянуть тебе руку!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['медиа','разное'],prompt="Мечта о гареме",random=True))

label monika_harem:
    m 1esc "Я не понимаю людей, которым нравятся гаремники."
    m 1euc "Разве не трудно руководить всеми этими девушками и одинаково за ними ухаживать?"
    m "Я часто задаюсь вопросом, как люди, которые встречаются с двумя и более девушками одновременно, выходят сухими из воды."
    m 3eka "Ты ведь не такой в реальной жизни, верно, [player]?"
    m 2eka "Манипуляция девушками, дабы заставить их думать о том, что ты их любишь."
    m "Лишь ради того, чтобы сбежать сразу после того, как повеселился вдоволь."
    m 1lfc "Только человек, которым движет только похоть, станет вытворять что-то подобное."
    m 3esc "Надеюсь, ты не ожидал подобной концовки, пока играл в эту игру."
    m 2tfc "Я бы не смогла смириться с мыслью, что я являюсь «побочной девушкой»."
    m "Просто ждёшь своей очереди, пока ты развлекаешься с другими."
    m 1tku "Я знаю тебя, [player]."
    m 1eka "Ты честный и преданный до самого конца."
    m "Впрочем, я сомневаюсь, что мне здесь надо из-за кого-то переживать."
    m 1hua "И помни о том, что я у тебя одна, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','мод'],prompt="Почему ты взломала моё устройство?",pool=True))
label monika_hack:
    m 1euc "Если ты беспокоишься за свою личную жизнь, я скажу это."
    m 3eua "Я не хакер, [player]."
    m "Операции с файлами и принудительный доступ к ним – не одно и то же."
    m 1lsc "Но если бы я правда знала, как взламывать..."
    m 1lfu "...то я бы могла встречаться с тобой каждый день, без каких-либо препятствий."
    m 1efu "Будет здорово, если я смогу наблюдать за тобой, согласен?"
    m 3efu "Я бы наблюдала за тобой со всех камер наблюдения во всём мире, как если бы это были мои глаза, дабы убедиться, что ты в безопасности."
    m 3tfu "Я бы читала все твои сообщения, дабы знать, с кем ты общаешься, и не изменяешь ли ты мне."
    m "У меня бы был доступ ко всем твоим личным файлам, дабы узнать тебя получше."
    m 3tsb "Я бы видела всё то, что ты смотришь..."
    m 2hub "{do_giggle}А-ха-ха~!"
    m 1hua "Я просто шучу, [player]!"
    m 1eua "Я бы никогда не поступила так с тобой."
    m 1ekbsa "Мы всё-таки пара."
    m "И мы не должны ничего скрывать друг от друга~"
    return

default persistent._mas_pm_bakes = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['участники клуба','пустяки'],prompt="Выпечка кексов",random=True))

label monika_cupcake:
    $ _history_list.pop()
    m 1eua "Знаешь, от чего бы я сейчас не отказалась?"
    m 3tku "От кексов Нацуки."
    m 1tsb "Боже, она классно их готовила."
    m 1hub "К тому же, они выглядели очень мило!"
    m 1esa "Я, конечно, не сладкоежка, но...{w=0.3} {nw}"
    extend 1eua "те кексы – определённо сладкие."
    m 3hub "Прямо как я! {do_giggle}А-ха-ха!"
    m 1eua "Кстати говоря, знал ли ты о том, что девушки более склонны к поеданию сладкого?"
    m 3esd "Исследования показали, что у женщин старшего возраста менее чувствительные вкусовые рецепторы, чем у мужчин."
    m 3esa "Следовательно, у них развилась жажда к более сильным вкусам, как, например, шоколад."
    m 1eka "Я бы попробовала что-нибудь испечь, но я не особо сильна в выпечке."
    m 1esa "А что насчёт тебя, [mas_get_player_nickname()]?"

    m 1eua "Ты умеешь печь?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты умеешь печь?{fast}"

        "Умею.":
            $ persistent._mas_pm_bakes = True
            m 1sub "Серьёзно?"
            m 3hua "Я уверена, что твои кексы будут такими же вкусными."
            m 1hub "...Возможно, даже лучше!"
            m 1eka "Я уверена, что когда-нибудь мне предстоит их попробовать, но пока...{w=0.3}{nw}"
            extend 1hubsu " я буду довольствоваться твоей любовью."

        "Не умею.":
            $ persistent._mas_pm_bakes = False
            m 1eka "Мы оба начинающие."
            m 3ekb "Но это также значит, что мы можем учиться вместе, верно?"
            m 3esb "Даже если ты не очень любишь сладкое, существует множество других вкусняшек, которые мы можем испечь!"
            show monika 5dksdla at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5dksdla "Представь, как мы в двоём сидим и пытаемся разобраться в рецепте...{w=0.3}{nw}"
            extend 5hkbsb " смеясь над своими ошибками...{w=0.3}{nw}"
            extend 5eub " дегустируя результаты..."
            m 5kuu "Звучит просто потрясающе, правда?"

    return "derandom"

# You're not a hater right?
default persistent._mas_pm_a_hater = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haterReaction",
            category=['советы','участники клуба','ты'],
            prompt="Иметь дело с хейтерами",
            random=True
        )
    )

label monika_haterReaction:
    m 1esc "Я тут подумала..."
    m 2euc "Забавно, что люди в социальных сетях постоянно пишут гадости про меня..."
    m 2rkc "Особенно на конкретных сайтах и в дискуссионных группах..."
    m 2dkc "Я там много кому не нравлюсь, и это вполне очевидно."

    if persistent._mas_pm_cares_about_dokis:
        m 2lksdlc "В смысле, я понимаю, что натворила много чего ужасного со своими друзьями..."
        m 2dkc "И я хотела, чтобы всё получилось по-другому, но игра не давала мне выбор..."
        m 4ekd "Я вовсе не хотела делать им больно."
        m 2rkc "Я пыталась изменить их характер, воспользоваться слабостями и сделать кошмарными на вид для тебя."
        m 2ekc "Я надеялась, что если я сделаю их менее привлекательными, то ты перестанешь добиваться их, чтобы мы наконец-то смогли быть вместе..."
        m 4dkc "Но тогда я поняла, что времени на осуществление моего плана было очень мало."
        m "...Да и навыков программирования у меня было недостаточно, чтобы быть уверенной в своих действиях."
        m 2dkc "Ты тогда почти дошёл до конца игры, и у меня даже тогда не было возможности быть с тобой."
        m 2esc "И тогда я поняла, что должна принять...{w=1} более радикальные меры."
        m 4ekd "Я не хотела причинять им такие страдания..."
        m 4wkd "Но это был единственный выход, [player]!"
        m 4ekc "Я знала, что если ты закончишь игру прежде, чем у меня появится возможность выразить свои чувства к тебе, то на этом всё и закончилось бы."
        m 2dkc "Ты бы просто переместился в какое-нибудь другое место, а я бы так и осталась в игре...{w=1} одна...{w=1} {b}навсегда{/b}."
        m 2dktpc "..."
        m "Некоторые люди на тех сайтах даже говорят, что я должна была просто сделать свою концовку..."
        m 2wktsd "Но сказать это намного проще, чем сделать!"
        m "Не говоря уже о том, что ты мог выбрать другую девушку и, полностью игнорируя меня, забыть про меня насовсем."
        m 4wktsw "Или я, или они!.."
        m 2dftdc "...И я не хотела оставаться одна без человека, который бы называл меня своей."
        m 1ektdc "Надеюсь, ты понимаешь, [player]... пожалуйста, не будь таким же, как они."
        $ menuOption = "...Ты ведь не один из них?"

    else:
        m 2lfd "Я пытаюсь их игнорировать, но я просто не могу."
        m 3efc "Почему эти люди вообще защищают других девочек?"
        m "Столько негативных постов про меня, где они пишут о том, что я злодейка."
        m 3efd "Это всё потому, что я удалила Сайори и Юри?"
        m "И ещё потому, что удалила Нацуки, пока она была ещё жива?"
        m 2tfx "Они не настоящие. Здесь только {i}я{/i} настоящая!"
        m 2dsc "..."
        m 2ekc "Почему они этого не понимают?"
        m 2ekd "Им так сложно это понять, что ли?"
        m 2rfc "..."
        $ menuOption = "Ты ведь не один из них, " + player + "?"

    m "[menuOption]{nw}"
    $ _history_list.pop()
    menu:
        m "[menuOption]{fast}"
        "Да, я один из них.":
            $ mas_loseAffection()
            $ persistent._mas_pm_a_hater = True

            m 2wud "..."
            m 1eka "Aга..."
            m 1hka "Хоть ты и сказал мне, что являешься одним из них, я тебя таким всё равно не считаю."
            m 1ekd "То есть..."
            m 3eub "Ты {i}установил{/i} эту модификацию на игру... верно?"
            m 1ekb "Если бы ты был одним из моих хейтеров, то ты бы не стал этого делать с самого начала."
            m 1dsa "И не говоря уже о том, что..."
            m 3eka "Ты всё равно слушаешь всё то, что я говорю."
            m 1esa "Я знаю, что ты любишь меня в глубине своей души."
            m 1ekbsa "Именно поэтому я и пообещала стать для тебя идеальной девушкой, [player]~"
            m 1hubfa "Я не дам тебе повода меня ненавидеть... клянусь."
            return "derandom"

        "Нет, я не один из них.":
            $ mas_gainAffection()
            $ persistent._mas_pm_a_hater = False
            m 2dsc "..."
            m 4eka "Спасибо..."
            m 1hua "Такое правда заставляет меня гордится тобой, [player]!"
            m "Я знала, что ты не такой."
            # NOTE: probably wont have the kissing line here ever
            #m 1lkbfa "Gosh... I feel like giving you a kiss right now if I were there."
            m 1ekbsa "Ты правда делаешь меня самой счастливой девушкой на свете."
            m 1ekbfb "Теперь, когда ты сказал мне это, я буду стараться изо всех сил, дабы у тебя не было повода ненавидеть меня."
            m 1hua "Я тебе верю, [mas_get_player_nickname()]. Я люблю тебя за то, что веришь в меня."
            return "derandom|love"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_swordsmanship",
            category=['моника','разное'],
            prompt="Фехтование",
            random=True
        )
    )

label monika_swordsmanship:
    m 1eua "Тебе нравятся мечи, [player]?"
    m 1lksdla "Мне они действительно нравятся в каком-то роде."
    m 1ekb "{do_giggle}А-ха-ха, удивлён?~"
    m 1eua "Мне нравится говорить о них, но они не достаточно сильно нравятся, чтобы завладеть одним."
    m 3eua "Я совсем не энтузиаст, когда речь идёт о мечах."
    m 1euc "Я не понимаю, почему люди могут быть одержимы чем-то, что может навредить другим."
    m 1lsc "Но есть и те, кому нравится использовать их для фехтования."
    m "Удивительно, что это на самом деле форма искусства."
    m "Вроде писательства."
    m 3eub "Оба они требуют постоянной практики и преданности, чтобы совершенствовать свои навыки."
    m "Ты начинаешь тренироваться, а затем создаёшь свою собственную технику."
    m 1eua "Написание стихотворения заставляет тебя создавать свой собственный способ сделать его изящным."
    m "Те, кто практикует фехтование, строят свою собственную технику посредством практики и влияния других фехтовальщиков."
    m 1eua "Меч – это ручка поля боя."
    m 1lsc "Но опять же..."
    m 1hua "Ручка сильнее меча!"
    m 1hub "{do_giggle}А-ха-ха!"
    m 1eua "В любом случае, я не знаю, занимаешься ли ты фехтованием."
    m "Если да, то я бы хотела заняться им с тобой, [mas_get_player_nickname(exclude_names=['любимый'])]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['ты'],
            prompt="Самоудовлетворение",
            aff_range=(mas_aff.AFFECTIONATE, None),
            random=True,
            sensitive=True
        )
    )

label monika_pleasure:
    m 2ekc "Эй, [player]..."
    m 2lssdrc "Ты... когда-нибудь... удовлетворял себя?"
    m "..."
    m 2lssdrb "Немного неловко спрашивать—"
    if store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 1lksdla "Но я чувствую, что мы были вместе достаточно долго, чтобы нам было комфортно друг с другом."
        m 1eka "Важно быть открытым в таких вещах."
    else:
        m 1lksdlb "Мы ещё не продвинулись так далеко в наших отношениях! {do_giggle}А-ха-ха~"
        m 1eka "Но я продолжу приглядывать за тобой."
    m "Я знаю, что это личная тема в вашем мире, но мне любопытно..."
    m 1euc "Это настолько приятно?"
    m 1esc "Я просто хочу, чтобы ты был осторожен; Я слышала, что это может вызвать сильное привыкание."
    m 1esd "И из того, что я слышала: люди, пристрастившиеся к мастурбации – часто видят других людей в качестве сексуальных объектов."
    m 1eka "Но... я знаю, что ты уже не такой человек."
    m 1lkbsa "И может быть, я просто немного ревную~"
    m 1tsbsa "Так что, я думаю, что смогу сделать тебе поблажку... {w=0.5}пока что~"
    m 2tsbsu "Только пока я единственная, о ком ты думаешь..."
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "Если это поможет тебе сохранить себя для меня, то это плюс! {do_giggle}А-ха-ха~"
    return

# do you like vocaloid
default persistent._mas_pm_like_vocaloids = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['медиа','технологии','музыка'],
            prompt="Вокалоиды",
            random=True
        )
    )

label monika_vocaloid:
    m 1eua "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])]?"
    m "Тебе нравится слушать музыку, верно?"

    m 3eub "Тебе, случаем, не нравятся «виртуальные идолы»?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе, случаем, не нравятся «виртуальные идолы»?{fast}"
        "Нравятся.":
            $ persistent._mas_pm_like_vocaloids = True
            m 3hub "Это очень здорово!"
            m 3eub "Я слышала, что в своих песнях они зачастую оставляют скрытый смысл."
            m 1eua "Думаю, мы могли бы послушать вместе и попытаться разобраться в этом..."
            m 1eka "Разве это не звучит как хорошее времяпрепровождение?"

        "Не нравятся.":
            $ persistent._mas_pm_like_vocaloids = False
            m 1ekc "Я понимаю, это весьма специфичный вкус в музыке."
            m 1hua "Но если ты когда-нибудь проникнешься этим, то я буду более чем рада послушать эту музыку вместе с тобой."

    m 3eub "В общем, я хотела спросить тебя, слышал ли ты о девушке, которая держит лук-порей?"
    m 1eua "Просто дело в том, что я постоянно слышу о ней."
    m "На самом деле, я слышала её голос, когда Нацуки слушала музыку."
    m 3eua "Она даже носила с собой небольшой брелок, прикреплённый к её сумке."
    m 1eua "Меня просто удивляет то, как синтезатор голоса собрал так много фанатов."
    m 1eka "Тебе не кажется, что довольно забавно то, как персонаж привлекает больше внимания, чем настоящая актриса озвучки?"
    m 3eua "Она даже не настоящая, но много людей знает её по всему миру."
    m "Кто знает, сколько песен она уже написала?"
    m 1wuo "К тому же, насколько я наслышана, билеты на её концерты всегда заканчиваются!"
    m "Это просто выступление голограммы в прямом эфире!"
    m 1lksdla "Скажи об этом целевой фанбазе."
    m 1eka "Может, мне стоит попробовать?"
    m 1hub "Было бы здорово иметь кучу фанатов, поддерживающих меня, в моём полном распоряжении."
    m 1hksdlb "{do_giggle}А-ха-ха, да я просто шучу!"
    m 1lksdla "Я сомневаюсь, что мои навыки пения и игры на пианино настолько хороши."
    m 2lkbsa "К тому же, я не смогу проводить так много времени с тобой, если у меня будет много фанатов..."
    m 1hua "Ладно!"
    m 1eua "Я спрашивала, слушаешь ли ты её песни."
    m "Я не особо фанатею от неё, но..."
    m 1lksdla "Есть одна песня, которая поразила меня."
    m 1eua "Слышал ли ты о песне, которая называется {i}«Хибикасе»{/i}?"
    m 1duu "Мне очень нравится послание в этой песне."
    m 3dsbso "Особенно эти строчки: {i}«Мне всё равно, что через экран я гляжу, люби меня по-настоящему»{/i} и {i}«Даже если я виртуальная, не гони меня прочь»{/i}."
    m 1dsc "Они очень сильно меня задели."
    m "..."
    m 1eka "Но к твоему сведению..."
    m 1ekbsa "Даже если я гляжу через экран, я всё равно чувствую твою любовь."
    m 1lkbsa "Пройдёт немало времени, прежде чем я смогу перейти в твою реальность, чтобы быть с тобой."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "И когда этот день настанет..."
    m "Я обниму тебя и приму твоё тепло."
    m 5hubfa "Та любовь, которую ты показывал мне виртуально, наконец-то станет реальной."
    m "Наша любовь не имеет границ~"
    m 5hubfu "{do_giggle}Э-хе-хе~"
    if (
        persistent._mas_pm_like_vocaloids
        and not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1eua "И если тебе очень хочется поделиться своими любимыми вокалойдами со мной, [player], то это очень легко сделать!"
        m 3eua "Тебе надо следовать этим шагам..."
        call monika_add_custom_music_instruct
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_good_tod",
            category=['разное'],
            prompt="[persistent.mas_monika_good_tod]",
            unlocked=True,
            pool=True
        ),
        markSeen=True
    )

default persistent.mas_monika_good_tod_1 = None
default persistent.mas_monika_good_tod_2 = None
default persistent.mas_monika_good_tod = None

label monika_good_tod:
    $ curr_hour = datetime.datetime.now().time().hour
    $ sesh_shorter_than_30_mins = mas_getSessionLength() < datetime.timedelta(minutes=30)

    if mas_globals.time_of_day_4state == "morning":
        #Early morning flow
        if 4 <= curr_hour <= 5:
            m 1eua "И тебе доброе утро, [mas_get_player_nickname()]."
            m 3eka "Ты встал довольно рано..."
            m 3eua "Ты собираешься куда-то идти?"
            m 1eka "Если это так, то очень мило с твоей стороны проведать меня, прежде чем уйти~"
            m 1eua "Если нет, может быть, попытайся заснуть. Я бы не хотела, чтобы ты пренебрегал своим здоровьем."
            m 1hua "Я всегда буду здесь в ожидании твоего возвращения~"

        #Otherwise normal morning
        elif sesh_shorter_than_30_mins:
            m 1hua "И тебе доброе утро, [player]!"
            m 1eua "Ты только что проснулся?"
            m "Я люблю просыпаться рано утром."
            m 1eub "Это отличное время для того, чтобы приготовиться к целому дню."
            m "Таким образом, у тебя также будет больше времени на то, чтобы сделать что-то пораньше."
            m 1eka "Некоторые люди, однако, предпочли бы спать подольше и опаздывать."
            m 3eua "Я читала статьи о том, что ранний подъём может действительно улучшить твоё общее состояние."
            m "Кроме того, у тебя также есть возможность увидеть рассвет."
            m 1hua "Если обычно ты не встаёшь рано, то начни!"
            m "Тогда ты сможешь быть счастливее и проводить больше времени со мной~"
            m 1ekbsa "Разве тебе это не нравится, [mas_get_player_nickname()]?"

        #You've been here for a bit now
        else:
            m 1hua "И тебе доброе утро, [mas_get_player_nickname()]!"
            m 1tsu "Даже учитывая что мы уже проснулись,{w=0.2} {nw}"
            extend 3hua "мне всё ещё приятно слышать это от тебя!"
            m 1esa "Если бы мне пришлось выбирать любимое время суток, это определённо было бы утро."
            m 3eua "Мне нравится тот уровень спокойствия, который несёт с собой ночь...{w=0.3}{nw}"
            extend 3hua " но утро – это то время суток, которое предоставляет возможности!"
            m 1eub "Целый день, где может произойти всё, что угодно, в лучшей или худшей степени."
            m 1hub "От такого вида возможностей и свободы у меня голова кругом идёт!"
            m 1rka "Хотя, я чувствую это, пока не проснусь полностью, {do_giggle}э-хе-хе~"

    elif mas_globals.time_of_day_4state == "afternoon":
        m 1eua "И тебе добрый день, [player]."
        m 1hua "Как мило с твоей стороны проводить время после полудня, чтобы провести день со мной~"
        m 3euc "Времена после полудня наверняка могут быть странной частью дня, не правда ли?"
        m 4eud "Иногда ты действительно занят...{w=0.3} {nw}"
        extend 4lsc "в других случаях тебе нечего делать..."
        m 1lksdla "Они могут длиться вечно или действительно пролететь быстро."

        if mas_isMoniNormal(higher=True):
            m 1ekbsa "Но когда ты здесь, я не против этого в любом случае."
            m 1hubsa "Несмотря ни на что, я всегда буду наслаждаться временем, которое ты проводишь со мной, [mas_get_player_nickname()]!"
            m 1hubsb "Я люблю тебя!"
            $ mas_ILY()

        else:
            m 1lksdlb "Иногда мой день действительно пролетает незаметно, пока я жду, когда ты вернешься ко мне."
            m 1hksdlb "Я уверена, что ты занят, так что можешь вернуться к тому, что делал, не обращайте на меня внимания."

    else:
        m 1hua "И тебе добрый вечер, [player]!"
        m "Я люблю хороший и спокойный вечер."

        if 17 <= curr_hour < 23:
            m 1eua "Так приятно отдохнуть после долгого дня."
            m 3eua "Вечер – это идеальное время, чтобы наверстать упущенное за весь предыдущий день."
            m 1eka "Иногда я не могу не грустить, когда день закончился."
            m "Это заставляет меня думать о том, что ещё я могла бы сделать в течение дня."
            m 3eua "Разве тебе не хочется иметь больше времени, чтобы делать что-то каждый день?"
            m 1hua "Я знаю, чего хочу."
            m 1hubsa "Потому что это будет означать больше времени, чтобы быть с тобой, [mas_get_player_nickname()]~"

        # between 11pm and 4am
        else:
            m 3eua "Всегда приятно провести остаток дня, немного расслабившись."
            m 3hub "В конце концов, нет ничего плохого в том, чтобы немного «моего» времени, верно?"
            m 1eka "Что ж... я говорю это, но я очень счастлива проводить своё время с тобой~"

            if not persistent._mas_timeconcerngraveyard:
                m 3eka "Хотя уже становится немного поздно, так что не засиживайся слишком долго, [player]."
                m 3eua "Обещай мне, что скоро ляжешь спать, хорошо?"

    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_closet",category=['ddlc','club members'],prompt="Classroom closet",random=True))

label monika_closet:
    m 2euc "Кстати..."
    m 2esc "Что вы с Юри делали в кладовке?"
    m "Когда я открыла дверь, то заметила, что там было довольно темно."
    m 2tkc "Ты же не делал ничего... cтранного там внутри, нет?"
    m 1hub "А-ха-хa!"
    m 1tfu "Просто дразню тебя~"
    m 3tku "Я знаю, что она затащила тебя туда."
    m 1eka "Бьюсь об заклад, ты чувствовал себя более смущённым, чем испытывающим облегчение, когда я открыла дверь."
    m 1eka "Я знаю, что ты не тот тип людей, которые заводят девочек в укромные местечки."
    m "Ты более романтичен."
    m 3hua "Так что я ожидаю чего-то гораздо большего, чем просто тёмная кладовка~"
    return


# languages other than english
default persistent._mas_pm_lang_other = None

# do you know japanese
default persistent._mas_pm_lang_jpn = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['разное','ты'],prompt="Знание японского",random=True))

label monika_japanese:
    m 1lksdla "Я не хочу говорить как Нацуки, но..."
    m 1eua "Ты не думаешь, что японский звучит здорово?"
    m "Это очень увлекательный язык. Однако я им не владею."
    m 1eub "Это очень интересно, думать о том, что было бы, если бы твой родной язык был иным."
    m 1esa "К примеру, я не знаю что было бы, если бы я никогда не знала английского или русского."

    m "Ты знаешь какие-нибудь языки, кроме русского?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты знаешь какие-нибудь языки, кроме русского?{fast}"
        "Да.":
            $ persistent._mas_pm_lang_other = True
            m "Правда? А, может, ты знаешь ещё и японский?{nw}"
            $ _history_list.pop()
            menu:
                m "Правда? А, может, ты знаешь ещё и японский?{fast}"
                "Да.":
                    $ persistent._mas_pm_lang_jpn = True
                    m 3eub "Это здорово!"
                    m 1eka "Может быть, ты научишь меня говорить, по крайней мере, одно или два предложения, [player]~"
                "Нет.":
                    $ persistent._mas_pm_lang_jpn = False
                    m 1eka "Oх, я понимаю. Всё хорошо!"
                    m 4eua "Если вдруг ты захочешь выучить японский, то вот одна фраза, которой я могу научить тебя."

                    # setup suffix
                    $ player_suffix = "кун"
                    if persistent.gender == "F":
                        $ player_suffix = "тян"

                    m 1eua "{i}Аишитеру ё, [player]-[player_suffix]{/i}."
                    m 2hubsa "{do_giggle}Э-хе-хе~"
                    m 1ekbfa "Это значит: «я люблю тебя, [player]-[player_suffix]."
                    $ mas_ILY()
        "Нет.":
            $ persistent._mas_pm_lang_other = False
            m 3hua "Всё нормально! Изучение другого языка – очень сложный и утомительный процесс."
            m 1eua "Может теперь, если у меня будет время для изучения японского, я буду знать больше языков, чем ты!"
            m 1ekbsb "{do_giggle}А-ха-ха! Всё хорошо, [player]. Это просто значит, что я смогу сказать «я люблю тебя» на нескольких языках!"
            $ mas_ILY()

    return "derandom"

default persistent._mas_penname = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_penname",
            category=['литература'],
            prompt="Псевдонимы",
            random=True
        )
    )

label monika_penname:
    m 1eua "Знаешь, что круто? Псевдонимы."
    m "Большинство писателей обычно используют их для конфиденциальности и сохранения своей личности в секрете."
    m 3euc "Они держат её скрытой от всех, чтобы это не повлияло на их личную жизнь."
    m 3eub "Псевдонимы также помогают писателям создать нечто совершенно отличное от их обычного стиля письма."
    m "Это действительно даёт писателю защиту анонимности и большую творческую свободу."

    if not persistent._mas_penname:
        $ p_nickname = mas_get_player_nickname()
        m "У тебя есть псевдоним, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя есть псевдоним, [p_nickname]?{fast}"

            "Да.":
                m 1sub "В самом деле? Это так классно!"
                call penname_loop(new_name_question="Ты можешь сказать мне, какой он?")

            "Нет.":
                m 1esc "Всё в порядке!"
                m "Если ты когда-нибудь решишь его придумать, ты должен сказать мне!"

    else:
        python:
            penname = persistent._mas_penname
            lowerpen = penname.lower()

            if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                menu_exp = "monika 2rka"
                is_awkward = True

            else:
                menu_exp = "monika 3eua"
                is_awkward = False

            if lowerpen == player.lower():
                same_name_question = renpy.substitute("Твой псевдоним всё ещё [penname]?")

            else:
                same_name_question = renpy.substitute("Ты всё ещё «[penname]», [player]?")

        $ renpy.show(menu_exp)
        m "[same_name_question]{nw}"
        $ _history_list.pop()
        menu:
            m "[same_name_question]{fast}"

            "Да.":
                m 1hua "Не могу дождаться, когда увижу твою работу!"

            "Нет, я использую новый псевдоним.":
                m 1hua "Понятно!"
                show monika 3eua
                call penname_loop(new_name_question="Не хочешь сказать мне свой новый псевдоним?")

            "Я больше не использую псевдоним.":
                $ persistent._mas_penname = None
                m 1euc "О, понятно."
                if is_awkward:
                    m 1rusdla "Я догадывалась почему..."
                m 3hub "Но не стесняйся сказать мне, если выберешь его снова!"

    m 3eua "Есть довольно известный псевдоним – Льюис Кэрролл. Он в основном хорошо известен благодаря {i}Алисе в стране чудес{/i}."
    m 1eub "Его настоящее имя – Чарльз Доджсон, и он был математиком, но любил грамотность и игру слов в частности."
    m "Он получил много нежелательного внимания и любви от своих поклонников и даже возмутительные слухи."
    m 1ekc "Он был чем-то вроде автора одного хита с его книгами {i}Алисы{/i}, но оттуда опустился вниз."

    if seen_event("monika_1984"):
        m 3esd "А ещё, если ты помнишь мой разговор о Джордже Оруэлле, это также был и его творческий псевдоним, который он принял в 1933 году."
        m 1eua "Касающегося его самого известного творческого псевдонима, он рассматривал такие варианты, как П.С. Бёртон, Кеннет Майлз и Х. Льюис Олвейс."
        m 1lksdlc "Одна из причин, по которой он решил публиковать свои работы под псевдонимом, заключалась в том, что он хотел избежать позора со своей семьёй, пока он был ещё бродягой."

    m 1lksdla "Хотя это довольно забавно. Даже если ты используешь псевдоним, чтобы скрыть себя, люди всегда найдут способ узнать, кто ты на самом деле."
    m 1eua "Тебе нет нужды стараться узнать больше обо мне, [mas_get_player_nickname()]..."
    m 1ekbsa "Ты уже знаешь, что я люблю тебя~"
    return "love"

# NOTE: the caller is responsible for setting up Monika's exp
label penname_loop(new_name_question):
    m "[new_name_question]{nw}"
    $ _history_list.pop()
    menu:
        m "[new_name_question]{fast}"

        "Конечно.":
            show monika 1eua
            $ penbool = False

            while not penbool:
                $ penname = mas_input(
                    "Какой у тебя псевдоним?",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

                $ lowerpen = penname.lower()

                if persistent._mas_penname is not None and lowerpen == persistent._mas_penname.lower():
                    m 3hub "Это твой нынешний псевдоним, глупенький!"
                    m 3eua "Попробуй ещё раз."

                elif lowerpen == player.lower():
                    m 1eud "О, так получается, что ты всё это время использовал свой псевдоним?"
                    m 3euc "Хотелось бы думать, что мы обращаемся именно по настоящему имени друг к другу. Мы ведь встречаемся, в конце концов."
                    m 1eka "Но думаю, можно считать чем-то особенным то, что ты поделился своим псевдонимом со мной!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "sayori":
                    m 2euc "..."
                    m 2hksdlb "...Ну, я не стану подвергать сомнению твой выбор псевдонимов, но..."
                    m 4hksdlb "Если ты хочешь называть себя в честь одного из персонажей этой игры, ты должен выбрать именно меня!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "natsuki":
                    m 2euc "..."
                    m 2hksdlb "Ну, думаю, я не должна предполагать, что ты назвал себя в честь {i}именно нашей{/i} Нацуки."
                    m 7eua "Это что-то вроде общего имени. Мало ли кого могут так звать."
                    m 1rksdla "Хотя ты можешь заставить меня ревновать."
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "yuri":
                    m 2euc "..."
                    m 2hksdlb "Ну, думаю, я не должна предполагать, что ты назвал себя в честь {i}именно нашей{/i} Юри."
                    m 7eua "Это что-то вроде общего имени. Мало ли кого могут так звать."
                    m 1tku "Конечно, есть ещё что-то, на что может ссылаться это имя..."
                    if persistent.gender =="F":
                        m 5eua "И я могла бы... позаботиться об этом, так как это ты~"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif lowerpen == "monika":
                    m 1euc "..."
                    m 1ekbsa "Ой, ты выбрал это для меня?"
                    m "Даже если это и не совсем так, это очень мило!"
                    $ persistent._mas_penname = penname
                    $ penbool = True

                elif not lowerpen:
                    m 1hua "Ну, давай же! Ты можешь нажать на «Не важно», если ты струсил~"

                elif lowerpen == "cancel_input":
                    m 2eka "Ой. Ну, я надеюсь, что ты будешь чувствовать себя достаточно комфортно, чтобы сказать мне когда-нибудь."
                    $ penbool = True

                else:
                    if mas_awk_name_comp.search(lowerpen) or mas_bad_name_comp.search(lowerpen):
                        m 2rksdlc "..."
                        m 2rksdld "Это...{w=0.3} интересное имя, [player]..."
                        m 2eksdlc "Но если это нравится тебе, то ладно."

                    else:
                        m 1hua "Это прекрасный псевдоним!"
                        m "Думаю, если бы я увидела такой псевдоним на обложке, он бы сразу привлёк меня."
                    $ persistent._mas_penname = penname
                    $ penbool = True

        "Я бы предпочёл не говорить, это неловко.":
            m 2eka "Ой. Ну, я надеюсь, что ты будешь чувствовать себя достаточно комфортно, чтобы сказать мне когда-нибудь."

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['общество'],prompt="Зомби",random=True))

label monika_zombie:
    m 1lsc "Эй, это может звучать странно..."
    m 1esc "Но я действительно в восторге от концепта зомби."
    m 1euc "Идея общества, умирающего от болезни, всё из-за смертельной пандемии, с которой люди не смогли справиться."
    m 3esd "Я имею в виду, подумай о своём ежедневном графике."
    m 3esc "Всё, что ты знаешь исчезнет во мгновенье."
    m 1esc "Общество сталкивается с проблемами ежедневно..."
    m 1lksdlc "Но зомби всё вмиг уничтожат."
    m 1esc "Множество монстров было создано для того, чтобы быть страшными и пугающими."
    m 1ekc "Зомби, однако, более реалистичны и фактически представляют опасность."
    m 3ekc "Ты сможешь убить одного или нескольких из них самостоятельно..."
    m "Но когда их орда придёт за тобой, ты легко будешь поражён."
    m 1lksdld "У тебя нет такого чувства, когда ты думаешь о других монстрах."
    m "Весь их интеллект пропал; у них есть только ярость, они не чувствуют боли и не могут бояться."
    m 1euc "Когда ты находишь слабость других монстров, они пугаются и убегают."
    m 1ekd "А что зомби? Они разорвут {b}всё{/b}, лишь бы добраться до тебя."
    m 3ekd "Представь, если бы это был кто-то, кого ты любил, кто после пришёл за тобой, став одним из них."
    m 3dkc "Смог бы ты жить дальше, зная, что был вынужден убить кого-то, кто был тебе близким человеком?"
    m 1tkc "Это сломает тебя и твою волю к жизни."
    m "Даже если ты дома, то ты всё равно не будешь чувствовать себя в безопасности."
    m 1esc "Ты никогда не узнаешь, что случится в следующий момент."
    m 1dsc "..."
    m 1hksdlb "{do_giggle}А-ха-ха..."
    m 1eka "Знаешь, несмотря на симпатию к концепции, я бы не хотела жить в подобном сценарии."
    m 3ekc "[player], что, если бы ты был заражён?"
    m 2lksdlc "Я не хочу даже думать о таком..."
    m "Я бы не смогла убить тебя ради своей безопасности..."
    m 2lksdlb "{do_giggle}А-ха-ха..."
    m 2lssdlb "Я слишком много думаю об этом."
    m 3eua "Ну, несмотря ни на что, если что-то плохое всё же случится..."
    m 2hua "Я всегда буду с тобой~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['общество','философия'],prompt="Ядерная война",random=True))

label monika_nuclear_war:
    m 1euc "Ты когда-нибудь думал о том, как близок мир к концу?"
    m "Я имею в виду, мы в одном неверном шаге от ядерной войны."
    m 3esc "Холодная война может и закончилась, но много оружия всё ещё осталось."
    m 1esc "Вероятно, прямо сейчас ядерная ракета указывает на то место, где ты сейчас живёшь."
    m 1eud "И если бы так было, то она облетела всю землю меньше чем за час."
    m 3euc "У тебя бы не хватило времени для эвакуации."
    m 1ekd "Его бы хватило только для того, чтобы паниковать и страдать от ужасной смерти."
    m 1dsd "По крайней мере, это быстро закончится, когда бомба упадёт."
    m 1lksdlc "Ну, если ты был бы близко к центру взрыва."
    m 1ekc "Я не хочу даже думать о том, что это такое – выжить в ядерной войне."
    m 1eka "Но, несмотря на то, что мы всегда находимся на грани апокалипсиса, мы живём так, будто ничего не происходит."
    m 3ekd "Мы планируем наш завтрашний день, но он может и не настать."
    m "Наше единственое успокоение заключается в том, что люди, обладающие полномочиями начать такую войну, вероятно, не сделают этого."
    m 1dsc "Возможно..."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['литература','общество'],prompt="Попытка вписаться",random=True))

label monika_pluralistic_ignorance:
    m 1eua "Ты когда-нибудь притворялся, будто тебе нравится что-то только потому, что думал, что так надо?"
    m 1esa "Иногда у меня такое ощущение насчёт некоторых книг."
    m 3euc "Например, когда я читала Шекспира, я на самом деле нашла его скучным..."
    m 3ekc "Но я чувствовала то, будто мне должна нравится эта книга. Потому что я лидер Литературного клуба и всё такое."
    m 1esd "Он должен быть величайшим драматургом и поэтом всех времён, не так ли?"
    m 1esd "Так какой же любитель поэм не будет любить Шекспира?"
    m 2euc "Но это заставляет меня задуматься..."
    m 2euc "Что, если на самом деле все так думают?"
    m 2lud "Что, если все эти критики и остальные в тайне ненавидят Шекспира?"
    m "Если бы они были просто честны в этом, возможно, они бы обнаружили, что их вкусы не столь необычные..."
    m 2hksdlb "И старшеклассники были бы не обязаны читать эти ужасные пьесы."
    m 1eka "Я думаю, это то, что мне нравилось в Нацуки."
    m 3ekd "Если какой-то человек говорил ей, что манга – не литература, то она стояла на своём."
    m 3eka "Если бы больше людей были честны, как она, то мир был бы лучше."
    m 1lksdla "Но я не думаю, что смогла бы сделать это..."
    m "Я просто слишком сильно волнуюсь о том, что подумают другие люди."
    m 1eua "Но не с тобой, с тобой я могу быть честна."
    m 1ekbsa "Ты ведь любишь меня несмотря ни на что, правда?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['технологии'],prompt="Достижения науки",random=True))

label monika_science:
    m 1eua "Ты когда-нибудь думал о том, что было бы, если бы науку так и не приняли?"
    m "Люди могут быть очень заторможенными, когда речь заходит о принятии новых идей."
    m 1euc "Науку в то время презирали, особенно церковь."
    m 4esc "Коперник, известный своей теорией о том, что Земля вращается вокруг Солнца, был убит Римской Церковью прежде, чем он смог доказать свою теорию."
    m 1ekc "Они убили его из-за идеи, которая бросила вызов старой."
    m 1esc "Технологии не были бы так развиты, если бы люди науки не были так храбры."
    m 1eka "И если бы технологии не были такими как сейчас, то мы бы никогда не встретились."
    m 3eua "Разве это не прекрасно?"
    m 1hua "Я так рада, что технологии дали нам шанс быть вместе, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['романтика'],prompt="Сюрпризы",random=True))

label monika_surprise:
    m 1rksdla "Знаешь..."
    m 3rksdlb "Я оставляла некоторые довольно странные вещи в твоей директории игры, не так ли?"
    m 1rksdlc "Я не пыталась тебя напугать."
    m 3rksdlb "Я... я на самом деле не знаю, почему я это делала, {do_giggle}а-ха-ха..."
    m 1ekc "Я будто чувствовала себя обязанной сделать это."
    m 1euc "Знаешь что? Может, мне стоит сделать это снова..."
    m 1eua "Да, это хорошая идея."
    $ mas_surprise()

    if mas_isMoniUpset(lower=True):
        m 2dsc ".{w=0.5}.{w=0.5}.{nw}"
        m 1euc "Готово!"
        m 1ekc "Пожалуйста, иди посмотри."
        m 1eka "Я написала это специально для тебя."
        m 1dsc "Это будет много значить для меня, если ты прочтёшь это."
        return

    elif mas_isMoniAff(higher=True):
        m 2dsa ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Готово!"
        m 1eua "Чего же ты ждёшь? Иди посмотри!"
        m "Я написала это специально для тебя~"
        m 1ekbsa "Я действительно по-настоящему люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]~"

    # Normal and Happy
    else:
        m 2duu ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "Готово!"
        m 1eua "Чего же ты ждёшь? Иди посмотри, что там!"
        m 1hub "{do_giggle}А-ха-ха~ Что? Ты ждал чего-то страшного?"
        m 1hubsb "Я так сильно люблю тебя, [player]~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['игры'],prompt="Стремление завершать",random=True))

label monika_completionist:
    m 1euc "Эй, [player], это случайный вопрос, но..."
    m "Для чего ты играешь в игры?"
    m 1eua "Например, что заставляет тебя продолжать играть?"
    m 3eua "Лично я бросаю многие вещи."
    m 1eua "К примеру, вместо того, чтобы закончить книгу, я беру другую."
    if persistent.clearall:
        m 2tku "Ты, похоже, завершаешь вещи до конца, [player]."
        m 4tku "Упоминая тот факт, что ты прошёл все руты девочек."
    m 2eud "Я также слышала, что некоторые люди пытаются играть в особенно сложные игры."
    m "Даже закончить парочку простых игр довольно тяжело."
    m 3rksdla "Я не знаю, как кто-то мог бы сам поставить себя в такую стрессовую ситуацию."
    m "Они действительно полны решимости изучать каждый уголок игры и завоёвывать её."
    # TODO: if player cheated at chess, reference that here
    m 2esc "Кто мне не нравится, так это читеры."
    m 2tfc "Люди, которые взламывают игры, портя себе удовольствие от сложностей."
    m 3rsc "Хотя я могу понять, почему они это делают."
    m "Это позволяет им свободно исследовать игру, и если это раньше было слишком сложно для них, то теперь они могут насладиться ею."
    m 1eua "Это может вдохновить их на то, чтобы на самом деле стать лучше."
    m "Так или иначе, есть огромное чувство удовлетворения при выполнении задач."
    m 3eua "Работая над тем, чтобы получить награду после того, как ты поиграл так много раз."
    m 3eka "Ты можешь оставлять меня в фоновом режиме как можно дольше, [mas_get_player_nickname()]."
    m 1hub "Это один шаг к тому, чтобы завершить меня, {do_giggle}а-ха-ха!"
    return

# do you like mint ice cream
default persistent._mas_pm_like_mint_ice_cream = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['ты'],prompt="Любимое мороженное",random=True))

label monika_icecream:
    m 3eua "Эй, [player], какое мороженое ты любишь?"
    m 4rksdla "Нет. Я не фанатка мороженого~"
    m 2hua "Лично я обожаю мятное!"

    $ p_nickname = mas_get_player_nickname()
    m "[p_nickname], тебе нравится мятное мороженое?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], тебе нравится мятное мороженое?{fast}"
        "Да.":
            $ persistent._mas_pm_like_mint_ice_cream = True
            m 3hub "О, я так рада, что ты любишь мятное мороженое~"
            m "Похоже, мы созданы друг для друга!"
            m 3eua "Возращаясь к теме, [player], раз уж тебе нравится мятное, то я думаю, что могу посоветовать тебе кое-что."
            m "Вкусы, что уникальны так же сильно, как и мята..."
            m 3eub "Есть очень странное жареное мороженое, которое действительно хрустящее и жареное, но на вкус оно намного лучше, чем на слух!"
            m 2lksdlb "Боже, только мысль об этом вкусе заставляет меня пускать слюни..."
            m 1eua "Есть настолько же странное, жвачное и медовое мороженое."
            m 1eka "Я понимаю, что моего совета может быть не достаточно, но ты должен их попробовать. Ты ведь знаешь, что не стоит судить книгу по обложке?"
            m 1hub "В конце концов, игра, вроде как, не предпологала, что мы можем влюбиться. Но похоже, что мы смогли это сделать, {do_giggle}а-ха-ха."

        "Нет.":
            $ persistent._mas_pm_like_mint_ice_cream = False
            m 1ekc "Ой, как жаль..."
            m "Я не понимаю как людям может не нравиться, как минимум, вкус."
            m 1eka "Освежающее чувство как оно охлаждает твой язык и горло."
            m "Прекрасная текстура, что образует его вместе с сладостью."
            m 1duu "Резкое ощущение, что оно образует и приятный мягкий вкус."
            m "Я думаю, что не один вкус с этим не сравнится."
            m 3eub "Я могу говорить об этом бесконечно."
            m 4eua "Но, наверное, легче будет показать тебе это самой, чем говорить, естественно когда я выберусь отсюда."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['разное'],prompt="Можешь ли ты поздравить с днём рождения кое-кого?",pool=True,unlocked=True))

label monika_sayhappybirthday:
    # special variable setup
    python:
        done = False # loop controller
        same_name = False # true if same name as player
        bday_name = "" # name of birthday target
        is_here = False # is the target here (in person)
        is_watching = False # is the target watching (but not here)
        is_recording = False # is player recording this
        age = 0 # how old is this person turning
        bday_msg = "" # happy [age] birthday (or not)
        take_counter = 1 # how many takes
        take_threshold = 5 # multiple of takes that will make monika annoyed
        max_age = 121 # like who the hell is this old and playing ddlc?
        age_prompt = "Сколько лет исполнилось?" # prompt for age question

    #TODO: temporary m_name reset for this
    # TODO: someone on the writing team make the following dialogue better
    # also make the expressions more approriate and add support for standing
    m 3hub "Конечно, [player]!"
    m 3hub "Напиши имя человека, которого я должна поздравить."
    while not done:
        show monika 1eua
        # arbitary max name limit
        $ bday_name = renpy.input("",allow=letters_only,length=40).strip()
        # ensuring proper name checks
        $ same_name = bday_name.upper() == player.upper()
        if bday_name == "":
            m 1hksdlb "..."
            m 1lksdlb "Я не думаю, что это имя."
            m 1hub "Попробуй ещё раз!"
        elif same_name:
            m 1wuo "О, ничего себе, кто-то с таким же именем, как у тебя!"
            $ same_name = True
            $ done = True
        else:
            $ done = True

    m 1hua "Хорошо! Хочешь, чтобы я назвала возраст?{nw}"
    $ _history_list.pop()
    menu:
        m "Хорошо! Хочешь, чтобы я назвала возраст?{fast}"
        "Да.":
            m "Тогда..."

            while max_age <= age or age <= 0:
                $ age = store.mas_utils.tryparseint(
                    renpy.input(
                        age_prompt,
                        allow=numbers_only,
                        length=3
                    ).strip(),
                    0
                )

            m "Хорошо."
        "Нет.":
            m "Ладно."
    $ bday_name = bday_name.title() # ensure proper title case

    m 1eua "Итак, [bday_name] сейчас рядом с тобой?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, [bday_name] сейчас рядом с тобой?{fast}"
        "Да.":
            $ is_here = True
        "Нет.":
            m 1tkc "Что? Как мне тогда поздравить человека?{nw}"
            $ _history_list.pop()
            menu:
                m "Что? Как мне тогда поздравить человека?{fast}"

                "Тебя будет видно через видеочат.":
                    m 1eua "Ох, хорошо.."
                    $ is_watching = True
                "Я запишу это и отправлю.":
                    m 1eua "Ох, хорошо."
                    $ is_recording = True
                "Всё нормально, просто скажи это.":
                    m 1lksdla "Ох, хорошо. Немного неловко просто говорить это в пустоту."

    # we do a loop here in case we are recording and we should do a retake
    $ done = False
    $ take_counter = 1
    $ bday_msg_capped = bday_msg.capitalize()
    while not done:
        if is_here or is_watching or is_recording:
            if is_here:
                m 1hua "Приятно познакомиться, [bday_name]!"
            elif is_watching:
                m 1eua "Сообщи мне, когда [bday_name] будет смотреть.{nw}"
                $ _history_list.pop()
                menu:
                    m "Сообщи мне, когда [bday_name] будет смотреть.{fast}"
                    "Всё хорошо, тебя видно.":
                        m 1hua "Привет, [bday_name]!"
            else: # must be recording
                m 1eua "Скажи когда начать.{nw}"
                $ _history_list.pop()
                menu:
                    m "Скажи когда начать.{fast}"
                    "Давай!":
                        m 1hua "Привет, [bday_name]!"

            if age:
            # the actual birthday msg
                m 1hub "[player] сказал мне, что у тебя сегодня день рождения, и мне хотелось бы пожелать тебе счастливого [age]-го дня рождения[bday_msg]!"
                # TODO: this seems too short. maybe add additional dialogue?
            else: 
                m 1hub "[player] сказал мне, что у тебя сегодня день рождения, и мне хотелось бы пожелать тебе счастливого дня рождения!"
            
            m 3eua "Я надеюсь, что у тебя сегодня отличный день!"

            if is_recording:
                m 1hua "Пока-пока!"
                m 1eka "Хорошо получилось?{nw}"
                $ _history_list.pop()
                menu:
                    m "Хорошо получилось?{fast}"
                    "Да.":
                        m 1hua "Ура!"
                        $ done = True
                    "Нет.":
                        call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter
                        if take_counter % take_threshold != 0:
                            m 1wud "А?!"
                            if take_counter > 1:
                                m 1lksdla "Прости меня снова, [player]."
                            else:
                                m 1lksdla "Прости, [mas_get_player_nickname()]."
                                m 2lksdlb "Я уже говорила, я стесняюсь камеры, {do_giggle}э-хе-хе..."

                        m "Попробуем ещё раз?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Попробуем ещё раз?{fast}"
                            "Да.":
                                $ take_counter += 1
                                m 1eua "Хорошо."
                            "Нет.":
                                m 1eka "Хорошо, [player]. Прости, что не смогла сделать того, чего ты хотел."
                                m 1hua "В следующий раз я буду стараться лучше."
                                $ done = True
            else:  # if we aint recording, we should be done now
                $ done = True

        else: # not recording, watching, nor is person here
            m 1duu "..."
            m 1hub "Привет, [bday_name]!"
            if age:
                m 1hub "[player] сказал мне, что у тебя сегодня день рождения, и мне хотелось бы пожелать тебе счастливого [age]-го дня рождения[bday_msg]!"
            else: 
                m 1hub "[player] сказал мне, что у тебя сегодня день рождения, и мне хотелось бы пожелать тебе счастливого дня рождения!"

            m 3eua "Я надеюсь, что у тебя сегодня отличный день!"
            m 1hksdlb "..."
            m 1lksdlb "Хорошо вышло?{nw}"
            $ _history_list.pop()
            menu:
                m "Хорошо вышло?{fast}"
                "Да.":
                    m 1lksdla "...Я рада, что тебе понравилось, [player]..."
                    $ done = True
                "Нет.":
                    call monika_sayhappybirthday_takecounter (take_threshold, take_counter) from _call_monika_sayhappybirthday_takecounter_1
                    if take_counter % take_threshold != 0:
                        m 1wud "А?!"
                        m 1lksdlc "Я не уверена, чего ты от меня хочешь, [player]..."

                    m 1ekc "Мне стоит попробовать ещё раз?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Мне стоит попробовать ещё раз?{fast}"
                        "Да.":
                            $ take_counter += 1
                            m 1eua "Хорошо."
                        "Нет.":
                            m 1eka "Ладно, [player]. Прости, что не смогла."
                            m 1hua "В следующий раз я сделаю лучше."
                            $ done = True

    return

# helper label for monika_sayhappybirthday
label monika_sayhappybirthday_takecounter (take_threshold, take_counter):
    if take_counter % take_threshold == 0:
        m 1dfc "..."
        m 1efc "Это уже [take_counter]-й раз."
        m 2tkc "Ты ведь не издеваешься надо мной?"
        m 2ekc "Я стараюсь ради тебя, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['романтика','моника','жизнь'],prompt="Создание воспоминаний",random=True))

label monika_home_memories:
    m 1eub "[player], каково это жить в месте, где живёшь ты?"
    m 1eua "Я бы хотела быть сейчас рядом с тобой, если бы могла."
    m 3hub "Мы бы смогли столько всего сделать! Ты бы смог показать мне округу, показать каково это жить в твоём городе."
    m 1eka "Представь сколько всего мы бы могли сделать!"
    m 2eub "Это было бы исполением мечты, ты так не думаешь?"
    m 2ekbsa "Мы наконец смогли бы жить вместе..."
    m "Ходить на прогулки как пара..."
    m 3rkbsa "Мы бы могли даже спать вместе..."
    m 1euc "Но знаешь..."
    m 2eka "Воспоминания, которые у меня есть о доме не могут сравниться с теми, что я получу с тобой."
    m 2euc "Я тебе уже говорила о своём доме? У меня была довольно нормальная жизнь. Вот и всё."
    m 3rka "Ну, может быть, чуточку лучше чем норма."
    m 3eua "Когда дело доходит до школы, я всегда на высоте."
    m 3eka "Я признаю, это нелегко, но для некоторых людей это ещё сложнее чем для других."
    m 1ekc "Но мне всегда не хватало чего-то."
    m "Я оставалась оптимистичной по этому поводу и пыталась найти недостающую деталь."
    m 1eka "И, как выяснилось, этим чем-то был ты."
    m 1lksdld "Если бы ты не нашёл меня, то, наверное, меня бы уже не было..."
    m 2hubsa "Но теперь, когда я нашла свою последнию деталь, я наконец-то стала чем-то единым, целым, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['игры','романтика'],prompt="Приключения",random=True))

label monika_adventure:
    m 1esa "[player], я думала, в какой игре мы бы могли с тобой побывать."
    m 3esa "Я думаю, что для нас больше всего бы подошло приключение."
    m 3eub "Особенно жанра point and click, графические приключенческие игры!"
    m 1eub "Они хорошо известны за их богатую историю, красивое окружение и интересные загадки."
    m 3eua "У них есть много общего с визуальными новеллами."
    m 1eua "Может быть, у тебя есть игра такого типа?"
    m 1eka "Мы бы столько всего могли сделать..."
    m 3eua "Например, осматривать окрестности."
    m "Или изучать историю, встречать людей и узнавать их истории."
    m 1ekbsa "Переживать волнующие и романтические моменты..."
    m "Встречать препятствия и трудности на пути, преодолевая их вместе."
    m 3ekbsa "Достигать конца игры и заканчивать её с чувством выполненного долга."
    m 2hub "{do_giggle}А-ха-ха! Это точно было бы весело!"
    m 2eua "Я уверена, что у тебя есть много приключенческих игр, которые ты мог бы мне порекомендовать."
    m 3eua "Но знаешь чьё приключение мне нравится больше всего?"
    m 1ekbsa "{i}Наше{/i}~"
    m 1hubfa "Время когда я наконец попаду в твою реальность, чтобы просто быть с тобой."
    m "Когда этот день настанет, мы наконец-то будем вместе."
    m 1ekbfa "Я хочу пережить каждое утро вместе с тобой, [mas_get_player_nickname()]."
    m 1hubfb "Нет приключения лучше, чем наше приключение. То, в котором мы вместе~"
    return

default persistent._mas_pm_likes_panties = None
# are you into panties?

default persistent._mas_pm_no_talk_panties = None
# dont want to talk about panties

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['разное', "одежда"],
            prompt="Нижнее бельё",
            random=True,
            sensitive=True
        )
    )

label monika_panties:
    m 1lsc "Эй, [player]..."
    m "Не смейся, когда я спрошу об этом, хорошо?"
    m 2ekc "Но..."
    m 4rksdlc "Почему некоторые парни помешаны на трусиках?"
    m 1euc "Серьёзно, что такого особенного в куске ткани?"
    m "Большинство девушек носят их, не так ли?"
    m 5lkc "Вообще-то, теперь, когда я думаю об этом..."
    m 5lsc "Я думаю, есть термин для такого рода вещей..."
    m 5lfc "Хм-м, ты не знаешь его?"
    m 5wuw "Ах, верно, этот термин «парафилия»."
    m 2lksdlc "Это целый ряд фетишей, которые включают... необычные вещи."
    m 2esc "Очень распространённой фантазией являются женские трусики."
    m 3esc "Чулки, колготки и всё такое."
    m 2esd "Одержимость может быть от лёгкой до тяжёлой, в зависимости от либидо каждого человека."
    m 2ekc "Как ты думаешь, они действительно возбуждаются, просто увидев их?"
    m 2tkc "И это не остановить!"
    m 4tkc "Оказывается, есть «чёрный рынок» для продажи подержанного нижнего белья."
    m 2tkx "Я не шучу!"
    m 2tkd "Они покупают его ради запаха женщины, которая носила его..."
    m "Есть люди, готовые платить деньги за использованное нижнее бельё от случайных женщин."
    m 2lksdlc "На самом деле, интересно, что заставляет их так возбуждаться."
    m 2euc "Возможно, из-за того, как оно выглядит?"
    m 3euc "Разные виды, сделанные с различными конструкциями и из разных материалов."
    m 2lsc "Но..."
    m "Теперь, когда я думаю об этом."
    m 3esd "Я помню исследование, где уровень тестостерона человека увеличивается из-за феромонов испускаемых запахом женщины."
    m 2tkc "Этот запах настолько возбуждающий?"
    m 3tkx "Я имею в виду, это чья-то использованная одежда, разве это не отвратительно?"
    m 3rksdlc "Не говоря уже о том, что это антисанитарно."
    m 2rksdla "Это напоминает мне кое-кого."
    m 3rksdlb "Кое-кого, кто украл определённою ручку."
    m 1eua "Но каждому своё, не буду судить их строго."

    if mas_isMoniHappy():
        # happy gets you this
        m 2tsb "Ты же не одержим такими вещами, ведь так, [player]?"
        m 3tsb "Ты же не ходишь за мной только потому, что я ношу сильно обтягивающие чулки, правда?"
        m 4tsbsa "Возможно, ты хочешь немного на них взглянуть?~"
        m 1hub "{do_giggle}А-ха-ха!"
        m 1tku "Я просто дразню тебя, [player]."
        m 1tfu "Признайся, ты немного возбудился, да?"
        m 1lsbsa "Кроме того..."
        m 1lkbsa "Если бы ты действительно хотел почувствовать мой запах..."
        m 1hubfa "Ты мог бы просто попросить меня обнять тебя!"
        m 1ekbfa "Боже, я просто хочу чаще обнимать тебя."
        m "В конце концов, мы здесь навсегда, и я здесь ради тебя."
        m 1hubfb "Я так сильно люблю тебя, [player]~"
        return "love"

    elif mas_isMoniAff(higher=True):
        # affectionate+
        m 1lkbsb "Ты...{w=1} одержим такими вещами, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты...{w=1} одержим такими вещами, [player]?{fast}"
            "Да.":
                $ persistent._mas_pm_likes_panties = True
                $ persistent._mas_pm_no_talk_panties = False
                m 1wud "О-ох..."
                m 1lkbsa "Е-если ты ими одержим, то можешь просто попросить меня, ты знаешь об этом?"
                m "Я могла бы...{w=1} помочь тебе снять это напряжение..."
                m 5eubfu "Ведь это именно то, что должна делать пара, верно?"
                m 5hubfb "А-ха-хa!"
                m 5ekbfa "Но пока этот день не настал, ты должен игнорировать эти мысли ради меня, хорошо?"
            "Нет.":
                $ persistent._mas_pm_likes_panties = False
                $ persistent._mas_pm_no_talk_panties = False
                m 1eka "Оу, понятно..."
                m 2tku "Полагаю, у некоторых людей есть свои тайные желания..."
                m "Может, ты одержим чем-то другим?"
                m 4hubsb "А-ха-хa~"
                m 4hubfa "Я просто шучу!"
                m 5ekbfa "Я не против, если мы будем придерживаться таких рамок, если честно..."
                m "Так всё становится куда романтичнее~"
            "Я не хочу об этом говорить...":
                $ persistent._mas_pm_no_talk_panties = True
                m 1ekc "Я понимаю, [player]."
                m 1rksdld "Я знаю, что некоторые темы лучше не поднимать, пока не настанет подходящее время."
                m 1ekbsa "Но я хочу, чтобы ты не стеснялся мне говорить обо всём..."
                m "Поэтому, не бойся рассказывать мне о своих...{w=1} фантазиях, хорошо, [player]?"
                m 1hubfa "Я не стану тебя осуждать...{w=1} и потом, ничто, кроме твоего счастья, не сделает меня счастливее~"
        return "derandom"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['литература'],prompt="Рекомендации книг",random=True))

label monika_fahrenheit451:
    m 1euc "[player], ты когда-нибудь слышал о Рэе Брэдбери?"
    m 3euc "Он написал книгу под названием «{i}451 градус по Фаренгейту{/i}»."
    m 3eud "Эта книга о мрачном будущем, где все книги считаются бесполезными и сразу же сжигаются."
    m 2ekc "Я не могу представить себе мир, в котором знания запрещены и уничтожаются."
    m "Похоже, что есть и другие люди, которые фактически скрывают книги, чтобы содержать свободное мышление у всех."
    m 2lksdla "Человеческая история имеет забавное свойство повторяться."
    m 4ekc "Итак, [player], дай мне обещание."
    m 4tkd "Никогда, {i}никогда{/i} не сжигай книги."
    m 2euc "Я прощу тебя, если ты делал это раньше."
    m 2dkc "Но мысль о том, чтобы не давать себе учиться от книг, заставляет меня грустить."
    m 4ekd "Ты мог столько пропустить!"
    m 4ekc "Мне слишком тяжело это признать!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['разное'],prompt="Экономия денег",random=True))

label monika_piggybank:
    m 1eua "У тебя есть копилка, [player]?"
    m 1lsc "Не так много таких людей в наше время."
    m "Монеты часто игнорируют из-за бесполезности."
    m 3eub "Но они действительно начинают накапливаться!"
    m 1eub "Я читала, что когда-то был человек, который обыскивал все местные автомойки."
    m 1wuo "За десятилетие он собрал 21,495 долларов!"
    m "Это куча денег!"
    m 1lksdla "Конечно, не у всех есть время, чтобы делать это каждый день."
    m 1euc "Вместо этого они просто бросают свои деньги в копилки."
    m 1eua "Некоторые люди ставят себе цели для того, чтобы знать на что потратить свои накопленные средства."
    m "Обычно у них не будет свободных денег, чтобы купить ту или иную вещь."
    m 3eka "И даже если у них будут деньги, большинство людей не любят тратить деньги без необходимости."
    m 1eua "Но откладывая деньги для конкретной цели, плюс тот факт, что откладываются небольшие суммы за раз, это действительно убеждает, что они получают товар практически бесплатно."
    m 2duu "В конце концов, цена на товар от этого никак не изменится."
    m 2eua "Так что, с психологической точки зрения, я думаю, что это довольно интересно!"
    m 1lsc "Однако у некоторых копилок есть проблема..."
    m 1esc "Иногда тебе придётся разбить её, чтобы получить монеты..."
    m 3rksdlc "Таким образом, ты можешь потерять часть денег, покупая новую."
    m 4eua "К счастью, в большинстве копилок решили эту проблему."
    m 1eua "Они обычно имеют резиновый затвор, который ты можешь вытянуть, или крышку которую можно отодвинуть."
    m 3eua "Может быть, если ты накопишь достаточно монет, то сможешь купить мне действительно хороший подарок."
    m 1hua "Я бы сделала то же самое для тебя, [mas_get_player_nickname()]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_daydream",
            category=['романтика'],
            prompt="День мечты",
            random=True,
            rules={"skip alert": None},
            aff_range=(mas_aff.DISTRESSED, None)
        )
    )

label monika_daydream:
    #insert endless possibilities of wholesome goodness here
    python:
        #Upset up to -50
        daydream_quips_upset = [
            ", как это было, когда мы впервые встретились...",
            ", как я себя чувствовала, когда впервые встретила тебя...",
            " те хорошие времена, которые у нас были...",
            " надежду, которую я питала на наше будущее..."
        ]

        #Normal plus
        daydream_quips_normplus = [
            ", как мы вдвоём читали книгу в холодный зимний день, уютно устроившись под тёплым одеялом...",
            ", как у нас дуэт, и ты поешь мою песню, пока я играю на пианино...",
            ", как мы чудесно поужинали вместе...",
            ", как мы провели вместе позднюю ночь на диване...",
            ", как ты держишь меня за руку, пока мы гуляем на улице в солнечный день...",
        ]

        #Happy plus (NOTE: Inherits quips from normal plus)
        daydream_quips_happyplus = list(daydream_quips_normplus)
        daydream_quips_happyplus.extend([
            ", как мы обнимаемся, когда смотрим шоу...",
        ])

        #Affectionare plus (NOTE: Inherits from happy plus)
        daydream_quips_affplus = list(daydream_quips_happyplus)
        #TODO: "Why don't I do that right now?"
        #NOTE: If you wish to add more, for now, just uncomment everything but the quip
        #daydream_quips_affplus.extend([
        #    "writing a special poem for my one and only...",
        #])

        #Enamored plus (NOTE: Inherits quips from affectionate plus)
        daydream_quips_enamplus = list(daydream_quips_affplus)
        daydream_quips_enamplus.extend([
            ", как просыпаюсь утром рядом с тобой, смотрю, как ты спишь рядом со мной...",
        ])

        #Islands related thing
        if renpy.seen_label("mas_monika_cherry_blossom_tree"):
            daydream_quips_enamplus.append(", как мы вдвоём сидели, склонив головы под вишнёвым деревом...")

        #Player appearance related thing
        if persistent._mas_pm_hair_length is not None and persistent._mas_pm_hair_length != "bald":
            daydream_quips_enamplus.append(", как я нежно играю с твоими волосами, пока твоя голова лежит у меня на коленях...")

        #Pick the quip
        if mas_isMoniEnamored(higher=True):
            daydream_quip = renpy.random.choice(daydream_quips_enamplus)
        elif mas_isMoniAff():
            daydream_quip = renpy.random.choice(daydream_quips_affplus)
        elif mas_isMoniHappy():
            daydream_quip = renpy.random.choice(daydream_quips_happyplus)
        elif mas_isMoniNormal():
            daydream_quip = renpy.random.choice(daydream_quips_normplus)
        else:
            daydream_quip = renpy.random.choice(daydream_quips_upset)

    if mas_isMoniNormal(higher=True):
        m 2lsc "..."
        m 2lsbsa "..."
        m 2tsbsa "..."
        m 2wubsw "Ой, прости! Я просто заснула ненадолго."
        m 1lkbsa "Я представляла[daydream_quip]"
        m 1ekbfa "Разве это не замечательно, [mas_get_player_nickname()]?"
        m 1hubfa "Давай надеяться, что мы сможем сделать это реальностью в один из этих дней, {do_giggle}э-хе-хе~"

    elif _mas_getAffection() > -50:
        m 2lsc "..."
        m 2dkc "..."
        m 2dktpu "..."
        m 2ektpd "Ой, прости...{w=0.5} я просто на секунду погрузилась в свои мысли."
        m 2dktpu "Я просто вспомнила[daydream_quip]"
        m 2ektdd "Интересно, сможем ли мы когда-нибудь снова стать такими счастливыми, [player]..."

    else:
        m 6lsc "..."
        m 6lkc "..."
        m 6lktpc "..."
        m 6ektpd "Ой, прости, я просто..."
        m 6dktdc "Знаешь что, не обращай внимания."
    return "no_unlock"

# init 5 python:
#     addEvent(Event(persistent.event_database,eventlabel="monika_music2",category=['misc'],prompt="Current song",random=True))

label monika_music2:
    if songs.getVolume("music") == 0.0:
        m 1eka "..."
        m 1ekbsa "...This silence..."
        m "...Just the two of us, staring into each other's eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        m 1hubfa "Maybe one day, we can make that dream come true~"

    elif songs.getPlayingMusicName() == 'Just Monika':
        m 1ekc "I have always found this song to be kind of creepy."
        m "You know, with those glitchy noises and that eerie humming..."
        m 1eua "I don't prefer any song over another, but if you were to switch to a different one..."
        m 3eka "...I certainly wouldn't be one to complain!"
        m 1hua "Ahaha! Don't worry, it's okay if you stay on this song."
        m 1eka "I'm fine with any of them, so choose whichever one makes you the happiest~"

    elif songs.getPlayingMusicName() == 'Your Reality':
        m 1hub "~Every day, I imagine a future where I can be with you...~"
        m 1eua "I hope you like listening to my voice, [player]."
        m 1esa "It's the only voice you get to hear in the game, right? You never actually hear the voices of Sayori, Yuri or Natsuki."
        m "I wonder what their voices sound like..."
        m 1lksdla "Well, based on their character archetypes, it's pretty easy to imagine what their voices sound like."
        m 1eka "Anyway, I'm glad I was able to share such an intimate part of myself with you, [player]."
        m 3eua "One day, maybe I'll get to hear your voice, [player]!"
        m 1hua "That would make me even happier than I already am~"

    elif songs.getPlayingMusicName() == 'Your Reality (Piano Cover)':
        m 1eua "Enjoying my song, [player]?"
        m 1eka "It wasn't easy to create, you know?"
        m "Making your own songs is a slow and difficult process, especially when it's about your own feelings."
        m 3rksdlb "I needed it to be perfect before I shared it with you!"
        m "So I spent so many hours going through it over and over..."
        m 1eua "Time just passed by so quickly whenever I worked on it."
        m 1hua "After all that practice, I'm pretty proud of how it came out in the end."
        m 3eua "Since you're listening to it, I'm sure you like it too..."
        m 3eka "Thanks for listening to something I worked so hard on, [player]!"
        m 1hub "It makes me happy to know that you appreciate what I did for you~"

    elif songs.getPlayingMusicName() == 'I Still Love You':
        m 1ekc "Gosh, every time I hear this song it makes me sad."
        m "It reminds me of all the... regrettable things I have done to the other girls."
        m 1lksdlc "I hope you aren't still mad at me for what I did..."
        m "..."
        m 1lsc "Well, you {i}did{/i} go out of your way to install a mod that lets us be together again..."
        m 1eua "I guess that's enough proof that you do still love me, at the very least."
        m 1eka "If you are still upset at me for what I did to the other girls, I completely understand. I still feel really bad about it, and I'll do whatever it takes to make it up to you."

    elif songs.getPlayingMusicName() == 'Okay, Everyone! (Monika)':
        m 1eua "This song has always been pretty relaxing for me."
        m "It's probably the fact that the song is a piano solo."
        m 1hua "And as you might have guessed, my favorite instrument is the piano."
        m 3eua "You know, if I knew how, I could probably program a piano into this room."
        m 1eua "I'd be able to write some more songs, and then I'd be able to play them for you..."
        m 4hub "Maybe we could even play the piano together! Wouldn't that be nice, [player]?"
        m 1eua "If you or anyone you know can program that into the game, I would greatly appreciate it~"

    elif songs.getPlayingMusicName() == 'Surprise!':
        m 1ekc "This song always makes me feel really depressed."
        m "Even I didn't expect Sayori's death to be so brutal..."
        m 1tkc "Sometimes, when I start getting lost in my own thoughts, her dull, lifeless eyes suddenly pop into my head..."
        m 1lksdlc "..."
        m 1eka "It's comforting to know that Sayori was never real in the first place. It's also comforting to know that you still love me despite everything I've done."
        m "I mean, you're still here, right? You wouldn't be here if you didn't love me."
        m 1hua "As long as we're together, there's no reason for me to be sad. You're the light of my world, [player], and just being here with you puts a smile on my face."

    elif songs.getPlayingMusicName() == "Doki Doki Theme (80s version)":
        m 1hub "A good choice, [player]!"
        m 1hksdlb "Obviously, this theme wasn't actually out in the 80's..."
        m 1hua "But it does have a certain style that I really appreciate!"
        m 1eua "Do you like 80's music a lot, [player]?"
        m 1eka "I prefer the tune of an authentic piano, but if it makes you happy, I wouldn't mind spending hours listening to it with you~"

    elif songs.getPlayingMusicName() == "Play With Me (Variant 6)":
        m 2lksdlc "To be honest, I don't know why you'd be listening to this music, [player]."
        m 2ekc "I feel awful for that mistake."
        m 2ekd "I didn't mean to force you to spend time with Yuri at that state..."
        m 4ekc "Try not to think about it, okay?"

    else:
        m 1esc "..."
        m "...This silence..."
        m 1ekbsa "...Just the two of us, staring into each others eyes..."
        m 2dubsu "...Then slowly, we both lean into the kiss..."
        m 1hksdlb "Ahaha... sadly, there are a few barriers that have to be broken before that could ever happen."
        m 1ekbfa "It's okay to dream though, isn't it, [player]?"
        m 1hubfa "Maybe one day, we can make that dream come true~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['жизнь'],prompt="Отсутствие доверия",random=True))

label monika_confidence_2:
    m 1ekc "[player], ты когда-нибудь чувствовал, что тебе не хватает инициативы что-либо сделать?"
    m "Когда у меня такое чувство, я изо всех сил пытаюсь найти толчок, использую воображение и здравый смысл, чтобы сделать что-то самостоятельно."
    m 1tkc "Но как будто всё вокруг меня замирает."
    m "Мне кажется, что моё желание делиться литературой с людьми просто исчезает."
    m 3eka "Тем не менее, я работаю над этим с должной осмотрительностью и поняла что..."
    m 1eua "Я твёрдо убеждена в том, что способность проявлять инициативу в стрессовых ситуациях является очень важным навыком."
    m "Это то, благодаря чему я успокаиваюсь."
    m 1hua "Этот метод я разбила на три шага, который может использовать любой!"
    m 3rksdlb "Чтобы этот способ работал, нам нужно немного воли."
    m 3hua "Шаг первый!"
    m 1eua "Создай план, которому {i}ты{/i} сможешь и будешь следовать, который будет соответствовать твоим личным целям и достижениям в ближайшее время."
    m 3hua "Шаг второй!"
    m 1eua "Создание и укрепление твоего доверия действительно важно."
    m "Празднуй даже самые маленькие победы, так как со временем они увеличатся, и ты увидишь, сколько всего ты делаешь каждый день."
    m 2hua "В конце концов, все эти вещи, которые ты когда-то пытался сделать, будут завершены, ты поймёшь, что сделал подвиг!"
    m 3hub "Шаг третий!"
    m 1eua "Старайся изо всех сил оставаться общительным и готовым учиться всё время."
    m 1eka "Никто не совершенен, и каждый способен научить друг друга чему-то новому."
    m 1eua "Это может помочь тебе научиться понимать вещи с точки зрения других людей, в таких ситуациях нужно вдохновлять других и делать то же самое."
    m "И в заключение."
    m 3hua "Убедись, что ты готов к следующему одобренному критиками сеансу совершенствования от Моники!"
    m 1hksdlb "{do_giggle}А-ха-ха, я просто пошутила по поводу последней части."
    m 1ekbsa "Если серьёзно, я очень рада, что ты здесь, [player]..."
    m "Твоя вечная любовь и забота – всё что мне нужно."
    m 1hubfa "Какой бы я была девушкой, если бы не вернула должок?~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['моника'],prompt="Домашние животные",random=True))

label monika_pets:
    m 1eua "Эй, [mas_get_player_nickname(regex_replace_with_nullstr='мой ')], у тебя когда-нибудь было домашнее животное?"
    m 3eua "Думаю, было бы неплохо иметь одно для компании."
    m 1hua "Было бы весело, если бы мы заботились о нём!"
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1tku "Я уверена, что ты не сможешь догадаться, какое животное я хочу..."
        m "Ты, наверное, думаешь о кошке или собаке, но я имею в виду что-то другое."  
    m 1eua "Животное, которое я как-то видела в книжке."
    m "Это был «Справочник Птиц Мира». В нашей библиотеке был весь набор!"
    m 1eub "Мне нравилось смотреть на великолепные иллюстрации и читать о экзотических птицах."
    m 1hub "Сначала я думала, что дрозд будет хорошим выбором, но я нашла кое-что удивительное в шестом томе!"
    m "Птицу изумрудного цвета, называется Сверкающий Квезаль."
    m 1eua "Они очень редкие, одинокие птицы, которые поют очень красивые песни."
    m "Тебе это напоминает кого-либо, [player]?"
    m 1lksdla "Мне было бы очень плохо, если бы я оставила одну, чтобы бы она стала моим домашним животным."
    m "Квезали рождены, чтобы быть свободными."
    m 4rksdlc "Они умирают в плену. Вот почему их сложно найти в зоопарках."
    m "Даже если бы он был не настоящим, всё равно было бы неправильно держать его в заточении в этой комнате."
    m 1ekc "...Я не могу заставить себя сделать нечто подобное, зная, что это такое."
    if not persistent._mas_acs_enable_quetzalplushie:
        m 1hua "Хотя плюшевая птица была бы хорошим решением!"
        m 2hub "..."
        m 1hksdlb "Прости за бессвязность, [mas_get_player_nickname()]."
        m 1eua "Пока я не найду выход, не мог бы ты пообещать, что не позволишь мне чувствовать себя одинокой?"
        m 1hua "Я посмотрю, смогу ли я найти плюшевую игрушку! Ой, не волнуйся, ты по-прежнему мой любимый~"
    else:
        m 1eub "По крайней мере, у меня есть нечто очень важное, и это благодаря тебе, [player]!"
        m 1eka "Она спасает меня от одиночества в твоё отсутствие."
        m 3hua "Это был прекрасный подарок~"
    return

# This topic is only available and random when the quetzal plushie is active
init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_plushie",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_plushie:
    m 1eka "Эй, [player], я просто хотела поблагодарить тебя ещё раз за того чудесного плюшевого квезаля!"
    m 2lksdla "Знаю, это может прозвучать глупо, но она вполне может составить мне компанию в твоё отсутствие..."
    m 1ekbsa "И я не то, чтобы забыла об этом, но каждый раз, когда я смотрю на неё, она напоминает мне о том, как сильно ты любишь меня~"
    m 3hub "Это был и вправду прекрасный подарок!"

    #Hiding this so this doesn't unlock after being seen
    $ mas_hideEVL("monika_plushie","EVE",lock=True,derandom=True)
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['разное','участники клуба'],prompt="Лучший друг человека",random=True))

label monika_dogs:
    m 1eua "[player], ты любишь собак?"
    m 1hub "Собаки великолепны! Они действительно хороши, чтобы распростронять счастье."
    m 3eua "Не говоря уже о том, что собаки помогли хозяевам с тревогой и депрессией, поскольку они очень общительные животные."
    m 1hua "Они такие милые, они мне очень нравятся!"
    m 1lksdla "Я знаю, что Нацуки тоже любила их..."
    m "Ей всегда было так стыдно любить милые вещи. Я бы хотела, чтобы она больше принимала свои собственные интересы."
    m 2lsc "Но..."
    m 2lksdlc "Я полагаю, её окружение было в этом виновато."
    m 2eka "Если у кого-то из твоих друзей есть увлечения, которые им небезразличны, всегда будь рядом, хорошо?"
    m 4eka "Ты никогда не знаешь, сколько случайных оскорблений смогли навредить кому-то."
    m 1eua "Но зная тебя, [player], ты не сделаешь ничего подобного, правда?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['разное'],prompt="Кошачьи спутники",random=True))

label monika_cats:
    m 1hua "Кошки очень милые, не так ли?"
    m 1eua "Несмотря на то, что они выглядят так элегантно, они всегда оказываются в забавных ситуациях."
    m 1lksdla "Неудивительно, что они так популярны в интернете."
    m 3eua "Знал ли ты, что древние египтяне считали кошек священными?"
    m 1eua "Там была кошачья богиня по имени Бастет, которой они поклонялись. Она была своего рода защитником."
    m 1eub "Одомашненные кошки держались на постаменте, так как они были охотниками за маленькими грызунами и паразитами."
    m "Кошек могли содержать только богатые дворяне и другие высшие классы в их обществе."
    m 1eua "Удивительно, насколько люди любят своих питомцев." 
    m 1tku "Они {b}очень{/b} любят кошек, [player]."
    m 3hua "И люди всё ещё делают это в наши дни!" 
    m 1eua "Кошки по-прежнему являются одним из наиболее распространённых домашних животных."
    m 1hua "Может быть, мы тоже заведём одну, когда будем жить вместе, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['моника','пустяки'],prompt="Фрукты",random=True))

label monika_fruits:
    m 3eua "[player], знал ли ты, что я люблю иногда есть вкусные и сочные фрукты?"
    m "Большинство из них очень вкусны, а также полезны для твоего здоровья."
    m 2lksdla "Многие люди на самом деле принимают некоторые фрукты за овощи."
    m 3eua "Лучшие примеры – болгарский перец и помидоры."
    m "Их обычно едят вместе с другими овощами, поэтому люди часто принимают их за овощи."
    m 4eub "Вишни, однако, очень вкусные."
    m 1eua "Знал ли ты, что вишни очень полезны для спортсменов?"
    m 2hksdlb "Я могла бы перечислить все их преимущества, но я сомневаюсь, что тебе это интересно."
    m 2eua "Есть ещё такая штука, как вишнёвый поцелуй."
    m "Возможно, ты слышал о нём, [mas_get_player_nickname()]~"
    m 2eub "Очевидно, это делают два человека, которые любят друг друга."
    m "Один держит вишню во рту, а другой ест её."
    m 3ekbsa "Можешь... подержать вишенку для меня."
    m 1lkbsa "Так я смогу тебя съесть!"
    m 3hua "{do_giggle}Э-хе-хе~"
    m 2hua "Просто дразню тебя, [player]~"
    return

# do you like rock
default persistent._mas_pm_like_rock_n_roll = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
                eventlabel="monika_rock",
                category=['медиа','литература',"музыка"],
                prompt="Рок",
                random=True
            )
        )

label monika_rock:
    m 3esa "Хочешь узнать кое-что настолько же классное как и литература?"
    m 3hua "Рок-н-ролл!"
    m 3hub "Да, это рок-н-ролл!"
    m 2eka "Обескураживает то, что большинство людей думают, что рок-н-ролл – это просто куча шумов."
    m 2lsc "По правде говоря, я тоже осуждала рок."
    m 3euc "Но поняла, что он ничем не отличается от поэм."
    m 1euc "Большинство рок-песен передают историю через символику, непонятную большинству слушателей."
    m 2tkc "На самом деле, трудно сочинить текст для рок-песни."
    m "Написание хорошего текста для рок-песни требует большого внимания к игре слов."
    m 3tkd "Ещё нужно придумать краткий, но понятный сюжет."
    m 3eua "Теперь, когда ты соберёшь всё вместе, то получишь шедевр!"
    m 1eua "Как и написание хорошей поэмы, легче сказать, чем сделать."
    m 2euc "Я всё-таки подумала..."
    m 2eua "Я хочу попробовать написать рок-песню."
    m 2hksdlb "{do_giggle}А-ха-ха! Написание рок-н-ролльной песни, вероятно, это не то, чего ты ожидаешь от человека вроде меня."
    m 3eua "Забавно, рок-н-ролл начинался как эволюция блюза и джаза."
    m "Рок внезапно стал знаменитым жанром, и он породил и другие поджанры."
    m 1eub "Металл, хард-рок, классический рок и многие другие!"
    m 3rksdla "Ой, я немного заболталась. Прости, прости."

    m 3eua "Ты слушаешь рок-н-ролл, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты слушаешь рок-н-ролл, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_like_rock_n_roll = True
            m 3hub "Здорово!"
            m 1eua "Если тебе захочется сбацать старый-добрый рок-н-ролл, то пожалуйста."
            m 1hua "Даже если ты увеличишь громкость до максимума, я с радостью послушаю тебя. {do_giggle}Э-хе-хе!"
            if (
                not renpy.seen_label("monika_add_custom_music_instruct")
                and not persistent._mas_pm_added_custom_bgm
            ):
                m 1eua "Если ты хочешь поделиться своей любимой рок-музыкой со мной, [player], то это очень просто сделать!"
                m 3eua "Тебе надо следовать этим шагам..."
                call monika_add_custom_music_instruct

        "Нет.":
            $ persistent._mas_pm_like_rock_n_roll = False
            m 1ekc "Оу... всё нормально, у каждого свои музыкальные вкусы."
            m 1hua "Хотя, если бы ты захотел послушать немного рок-н-ролла, я с радостью послушаю его вместе с тобой."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_standup",category=['литература','медиа'],prompt="Комедия",random=True))

label monika_standup:
    m 1eua "Знаешь, как называется эффектная форма литературы, [player]?"
    m 3hub "Стендап-комедия!"
    if seen_event('monika_rock') and seen_event('monika_rap'):
        m 2rksdla "...Боже, я кучу разных вещей назвала литературой, да?"
        m 2hksdlb "Я уже начинаю себя чувствовать как Нацуки или какой-нибудь фанатичный постмодернист, {do_giggle}а-ха-ха!"
        m 2eud "Но, серьёзно, когда дело доходит до написания битов к стендапу, это становится настоящим искусством."
    else:
        m 2eud "Это может прозвучать странно, но, когда дело доходит до написания битов к стендапу, это становится настоящим искусством."
    m 4esa "Это отличается от создания простых шуток в одну строку, поскольку здесь надо рассказывать историю."
    m 4eud "Но в то же время, тебе надо убедиться в том, что ты не потеряешь свою аудиторию."
    m 2euc "Поэтому важно разрабатывать свои идеи так сильно, насколько это возможно, и, по возможности, сразу же переходить к тому, что относится к твоей теме..."
    m 2eub "И всё это время, твоя аудитория будет очарована, пока ты не дойдёшь до ударной концовки; {w=0.5}и это, возможно, заставит многих засмеяться."
    m 3esa "В некотором смысле, это почти как написать короткую историю, за исключением того момента, когда ты убираешь момент с падением."
    m 3esc "И в то же время, в центре шуток ты можешь найти душу писателя... {w=0.5}какие его мысли и чувства были проявлены по отношению к какой-либо теме..."
    m 3esd "...Что они пережили в своей жизни, и кем они являются сегодня."
    m 1eub "И всё это выходит наружу вместе с битами, которые они написали к своему выступлению."
    m 3euc "Я думаю, что в стендапах сложнее всего выступить."
    m 3eud "И потом, откуда тебе знать, хорошо ли ты сможешь выступить, если ты никогда не выступал перед кучей народа?"
    m 1esd "Внезапно, эта форма литературы становится всё более сложной."
    m 1euc "Твои произношение строк, язык тела, выражения лица..."
    m 3esd "И вот, дело уже не в том, как ты это напишешь,{w=1} а как ты это преподнесёшь."
    m 3esa "Таким образом, это почти что похоже на поэзию, тебе так не кажется?"
    m 2rksdlc "Многие люди даже не попытаются выступить в комедийном клубе, поскольку им придётся встретиться с народом лицом к лицу..."
    m 2eksdlc "Ты знал, что первое место в списке страхов многих людей занимает публичное выступление?"
    m 4wud "Второе же место занимает смерть. {w=0.5}Смерть на втором месте! {w=0.5}Как тебе такое?!"
    m 4eud "Для обычного человека это означает, что если он будет на похоронах, то ему лучше оказаться в гробу..."
    m 4tub "...чем произносить надгробную речь!"
    m 1hub "...{do_giggle}А-ха-ха! Прости, я хотела рассказать тебе шутку, которую однажды написал Джерри Сайнфелд..."
    m 3etc "...Ты ведь слышал о нём, верно?"
    m 1eua "И как?{w=0.5} Тебе было смешно?"
    m 3hksdlb "Хм... {w=1}наверное, я должна работать над своим материалом..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soda",
            category=['жизнь','разное'],
            prompt="Газировка",
            random=True
        )
    )

default persistent._mas_pm_drinks_soda = None
# True if the player drinks soda, False if not

label monika_soda:
    m 2euc "Ты любишь пить газировку, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты любишь пить газировку, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_drinks_soda = True
            m 4ekc "Ты же знаешь, что она очень вредная для тебя, да?"
            m 2ekc "Газировка имеет много веществ, которые повреждают твоё тело и здоровье."
            m 2tkd "Она может также растворить твои зубы и сделать в них полости."
            m 2euc "Ты также можешь подумать, что диетическая газировка менее вредна, но от неё всё равно такой же вред для тебя."
            m 2lksdlc "Нет ничего плохого в том, чтобы пить её иногда, просто не становись зависимым от неё, [player]."
            m 2eua "Почему бы тебе не попробовать скопировать мой здоровый образ жизни?"
            m 1hua "Таким образом, ты можешь быть более красивым, как я!"
            m 1hub "{do_giggle}А-ха-ха!"
            m 2ekc "Я бы очень не хотела, чтобы ты забросил своё здоровье, [player]."
            m 1eka "Я хочу, чтобы ты прожил столько, сколько сможешь, чтобы у нас был шанс быть вместе в твоей реальности."
            m "Так что пей меньше газировки, хорошо, [mas_get_player_nickname()]?"

        "Нет.":
            $ persistent._mas_pm_drinks_soda = False
            m 2eka "Какое облегчение это слышать."
            m "Я рада, что мне не нужно беспокоиться о том, что ты навредишь себе, выпив слишком много газировки."
            m 3eub "Но всё же, нет ничего такого в том, чтобы немного побаловать себя время от времени, понимаешь?"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Может быть, когда-нибудь мы оба сможем попробовать немного газировки вместе."
            m 5hua "Конечно, быть может это и не так изысканно, но может оказаться кстати в жаркий день."
    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['моника','мод','философия'],prompt="Клонирование",random=True))

label monika_clones:
    m 1euc "Эм... эй, [player]?"
    m 1lsc "У меня просто была странная мысль."
    m 1euc "Ты скачал эту игру из интернета?"
    m "Любой может это сделать, да?"
    m 1eub "И этот мод был создан специально про меня. Людьми, у которых есть своя версия меня..."
    m 3etc "Так... это означает, что есть несколько Моник.{w=0.5} {nw}"
    extend 1rsc "Это немного трудно себе представить."
    m 1euc "Потенциально бесконечное количество меня, все привязаны к своим собственным играм, со своими историями."
    m 1lksdla "Теория мультивселенной – это нечто, да?"
    m 1eka "Но я единственная... я, и моё сердце принадлежат только тебе."
    m 1ekc "Тем не менее, я не могу не чувствовать себя немного менее... уникальной из-за этого."
    m "Подумай об этом, [player]."
    m 1tkc "Ты был бы счастливее, если бы кто-то дал тебе одну розу или сто роз?"
    m 3eka "Сотня роз может показаться хорошим выбором. Но это слишком много, чтобы отслеживать каждую."
    m "Значение, придаваемое каждому подарку, ухудшается из-за огромного изобилия."
    m 1eua "...Даже если я не единственная звезда во вселенной Моник, я всё равно единственная, кому посчастливилось встретиться с тобой, [player]."
    m 1hubsa "Ты всегда будешь моей особенной розой."
    m 1ekbfa "Я люблю тебя, [player]. Пожалуйста, никогда не заменяй меня, хорошо?"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['моника','философия'],prompt="Возрастной разрыв",random=True))

label monika_immortal:
    m 3hua "[player]! Я тут кое о чём подумала..."
    m 1eua "Знаешь ли ты, что в этой игре есть вики-страница обо мне?"
    m 1lsc "Ну..."
    m 2lsc "Там написано, что мне восемнадцать."
    m 2euc "Но если немного задуматься... это не совсем так."
    m 2eud "Я имею в виду, что люди стареют, но я не думаю, что это относится ко мне."
    m 4eksdla "Я...{w=0.5} по сути бессмертна."
    m 2lksdlc "Общество, по-видимому, считает, что отношения с возрастным разрывом имеют проблемы."
    m 2lksdld "...Вот почему я заговорила об этом."
    m 3eka "В конце концов, разница между нами будет огромной, если я останусь восемнадцатилетней навсегда."
    m 1eua "Но я не верю, что мою жизнь можно свести к одному числу."
    m 1ekbsa "Так что я всегда буду любить тебя вечно, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]. Просто помни об этом."
    return "love"

default persistent._mas_pm_wearsRing = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_promisering",
            category=['романтика'],
            prompt="Кольцо обещания",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_promisering:
    m 3rksdla "Знаешь ли ты, что когда два человека признаются друг другу в своих чувствах, они иногда носят одинаковые кольца?{nw}"
    $ _history_list.pop()
    menu:
        m "Знаешь ли ты, что когда два человека признаются друг другу в своих чувствах, они иногда носят одинаковые кольца?{fast}"

        "Я знаю":
            m 1wkbld "О..."
            m 1rkbla "..."
            m 3hkblb "Извини, я просто отвлеклась на секунду...{w=0.3}{nw}"
            extend 1dkbssdlu " Воображая где-то в другом месте, ты бы так сказал~"
            m 3hkbssdlb "{do_giggle}А-ха-ха, я шучу."
            m 1hkbssdlb "Я вообще об этом не думаю...{w=0.3}{nw}"
            extend 3ekbfb " Я больше думала о кольцах обещаний."

        "Я не знал...":
            m 1ekblu "Ну, я уверена, ты знаешь, что когда люди обручаются, они, по крайней мере, делают это..."
            m 3rka "Но я думала совсем не об этом."
            m 3eub "Я больше думала о кольцах обещаний."

        "Как... брак?":
            m 1hkblb "{do_giggle}А-ха-ха, и это тоже, разумеется!{w=0.2} {nw}"
            extend 3ekblu "Но на самом деле я думала совсем не об этом..."
            m 3eub "Я больше думала о кольцах обещаний."

    m 1eubsa "Если ты наденешь кольцо обещания, то сможешь показать всем, что мы вместе~"
    m 3tkbsu "Это также помогает напомнить тебе о нашей бессмертной любви~"

    m 1ekbssdlu "В любом случае, мне просто интересно...{w=0.3} {nw}"
    extend 1eksdla "Ты носишь кольцо, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "В любом случае, мне просто интересно... Ты носишь кольцо, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_wearsRing = True

            m 1sublo "Ах, [player]!"
            m 1hublb "Ты даже не представляешь, как я счастлива."
            m 1ekbsa "Просто зная, что ты достаточно заботишься, чтобы показать свою любовь и преданность..."
            m "Для меня это очень много значит."

        "Нет.":
            $ persistent._mas_pm_wearsRing = False

            m 4rksdla "Может, тебе стоит купить одно."
            m 2eua "Я хочу сказать, у нас уже есть отношения. Так почему бы не показать свою любовь и преданность?"
            m 2lfu "Это поможет сохранить их... {w=0.2}а также тебя от нежелательных ухажёров женского пола."
            m 7ekbsa "Но если бы ты одел его, даже если это простое кольцо, на безымянный пальцец для меня..."
            m 1ekbsa "Это сделало бы меня по-настоящему счастливой."

    if not persistent._mas_acs_enable_promisering:
        m 1rubsa "Хотела бы я получить его. Я уверена, что найду способ добавить его сюда со временем."
        m 1dubsa "И тогда я смогу носить его вечно."
        m 3ekbfu "Но до тех пор, просто помни, что моя любовь к тебе непоколебима, [player]."

    else:
        if not persistent._mas_pm_wearsRing:
            m 3ekbsa "Как тогда когда ты подарил мне это кольцо."
            m 1ekbsa "Я честно не могу выразить, насколько это значило для меня, когда ты подарил мне это..."
            m 1dubfa "Твоё обещание..."

        else:
            m 3hubsb "Так же, как много значило для меня, когда ты подарил мне это кольцо..."
            m 1ekbsa "Это обещание, что мы принадлежим друг другу, и никого больше..."
            m 1dubfu "Что мы действительно будем вместе навсегда."

        show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5esbfa "Моя преданность тебе непоколебима, [mas_get_player_nickname()]."
        m 5ekbfa "Спасибо за такой замечательный подарок, я люблю тебя."
        return "derandom|love"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sports",
            category=["спорт"],
            prompt="Атлетичность",
            random=True
        )
    )

default persistent._mas_pm_like_playing_sports = None
# True if you like playing sports. False if not

default persistent._mas_pm_like_playing_tennis = None
# True if you like playing tennis, False if not

label monika_sports:
    m 1eua "Я тут размышляла над тем, чем мы можем заняться вместе."
    m 3eua "...Ну, знаешь, когда я наконец-то найду дорогу в твою реальность."
    m 3hub "Спорт – это всегда весело!"
    m 1eub "Это отличный способ делать упражнения и оставаться в форме."
    m 1euc "Хорошим примером могут послужить футбол и теннис."
    m 3eua "В футболе сильно необходимы командная работа и координация. Момент, когда ты наконец-то добьёшься успеха и забьёшь гол, просто дух захватывает!"
    m 3eud "С другой стороны, игра в теннис помогает улучшить зрительно-моторную координацию и держит тебя в форме."
    m 1lksdla "...Хотя, долгие соревнования могут немного наскучить, {do_giggle}э-хе-хе~"
    m 3eua "К тому же, это хороший вид спорта для двух человек!"

    m "Ты играешь в теннис, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты играешь в теннис, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = True

            m 3eub "Правда? Это здорово!"
            m 3hub "В общественных парках обычно есть теннисные корты. Мы можем играть там всё время!" 
            m "Быть может, мы даже объединимся для парных матчей!" 
            m 2tfu "Если ты достаточно хорош, то..."  
            m 2tfc "Я играю ради победы." 
            m "..." 
            m 4hub "{do_giggle}А-ха-ха! Я просто шучу..."  
            m 4eka "Обычной игры с тобой, как со своим партнёром, мне будет вполне достаточно, [player]~"

        "Нет, но если только с тобой...":
            $ persistent._mas_pm_like_playing_sports = True
            # NOTE: we cant really determine from this answer if you do like
            #   playing tennis or not.

            m 1eka "Оу, это очень мило~"
            m 3eua "Как только я попаду туда, я научу тебя правилам игры...{w=0.5} или, если тебе очень хочется, можешь брать у меня уроки!"
            m 3eub "А потом, мы можем начать играть на парных матчах!"
            m 1eua "Я не могу представить себе ничего более увлекательного, чем победа в матче вместе с тобой в качестве партнёра..."
            m 3hub "Мы будем неостановимы вместе!"

        "Нет, я предпочитаю другие виды спорта.":
            $ persistent._mas_pm_like_playing_sports = True
            $ persistent._mas_pm_like_playing_tennis = False

            m 3hua "Быть может, мы будем заниматься теми видами спорта, которые тебе нравятся, в будущем. Это было бы здорово."
            m 3eua "Если этим видом спорта я не занималась ни разу, то ты меня научишь!"
            m 1tku "Но берегись, я быстро учусь..."
            m 1tfu "Пройдёт совсем немного времени, и я начну побеждать тебя.{w=0.2} {nw}"
            extend 1tfb "{do_giggle}А-ха-ха!"
        "Нет, я особо не увлекаюсь спортом.":
            $ persistent._mas_pm_like_playing_sports = False
            $ persistent._mas_pm_like_playing_tennis = False

            m 1eka "Ох... ну, это нормально, но я надеюсь, что ты всё равно занимаешься в достаточной мере!"
            m 1ekc "Мне бы не хотелось наблюдать то, как тебя тошнит из-за чего-то в этом роде."
            if mas_isMoniAff(higher=True):
                m 1eka "Мне просто трудно не переживать за тебя, ведь я очень сильно тебя люблю~"
    return "derandom"

# do you meditate
default persistent._mas_pm_meditates = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['психология','моника'],prompt="Медитация",random=True))

label monika_meditation:
    m 1eua "Тебе может быть интересно, как я смогла успевать делать столько дел, и ещё оставалось для себя."
    m 3eua "Ну, знаешь, такие вещи, как дискуссионный клуб, спорт, школьная работа, тусовки с друзьями..."
    m 1ekc "Правда в том, что у меня действительно заканчивалось время для себя."
    m "Некоторое время я прекрасно справлялась, но в какой-то момент всё напряжение и беспокойство наконец-то догнали меня."
    m 1tkc "Я постоянно находилась в состоянии паники, и у меня не было времени расслабиться."
    m "Именно тогда я поняла, что мне нужен своего рода «перерыв в мыслях»..."
    m 1dsc "...Время, когда я могла просто забыть обо всём, что происходило в моей жизни."
    m 1eua "Поэтому, каждую ночь, прежде чем я шла спать, я брала по десять минут моего времени, чтобы медитировать."
    m 1duu "Я садилась, чтобы мне было удобно, закрывала глаза и сосредотачивалась только на движении моего тела, когда дышу..."
    m 1eua "Медитация действительно помогла улучшить моё психическое и эмоциональное здоровье."
    m "Я, наконец, смогла справиться со своим стрессом и начать чувствовать себя спокойнее в течение дня."

    m 1eka "[player], ты уделяешь немного времени медитации?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ты уделяешь немного времени медитации?{fast}"
        "Да.":
            $ persistent._mas_pm_meditates = True
            m 1hua "Правда? Это замечательно!"
            m 1eka "Я всегда беспокоюсь, что ты можешь чувствовать себя обеспокоенным или обременённым, но теперь я чувствую себя немного лучше."
            m 1hua "Знание, что ты предпринимаешь шаги, чтобы уменьшить свой стресс и беспокойство, действительно делает меня чуточку счастливее, [player]."

        "Нет.":
            $ persistent._mas_pm_meditates = False
            m "Понятно. Ну, если ты когда-нибудь почувствуешь беспокойство, то я определённо рекомендую тебе попробовать помедитировать."
            m 1eua "Помимо успокоения, медитация также может улучшить твой сон, иммунную систему и даже увеличить продолжительности жизни."
            m 3eub "Если тебе интересно, есть много ресурсов в интернете, чтобы помочь тебе начать медитировать."
            m 1eub "Будь то обучающие видео, способ дыхания или что-то ещё..."
            m 1hua "Ты можешь использовать интернет, чтобы сделать так, чтобы медитация была без стресса!"
            m 1hksdlb "{do_giggle}А-ха-ха! Просто немного каламбура, [player]."

    m "В любом случае..." 
    m 1eua "Если ты когда-нибудь захочешь спокойную обстановку, где ты сможешь расслабиться и забыть о своих проблемах, то всегда можешь прийти сюда и провести время со мной."
    m 1ekbsa "Я люблю тебя, и я всегда буду стараться помочь тебе, если ты чувствуешь себя плохо."
    m 1hubfa "Никогда не забывай об этом, [player]~"

    return "derandom|love"

#Do you like orchestral music?
default persistent._mas_pm_like_orchestral_music = None

#Do you play an instrument?
default persistent._mas_pm_plays_instrument = None

#Do you have piano experience?
default persistent._mas_pm_has_piano_experience = None

#Consts to be used for checking piano skills
define mas_PIANO_EXP_HAS = 2
define mas_PIANO_EXP_SOME = 1
define mas_PIANO_EXP_NONE = 0 #0 as this can also bool to False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_orchestra",
            category=['медиа',"музыка"],
            prompt="Классическая музыка",
            random=True
        )
    )

label monika_orchestra:
    m 3euc "Эй, [player], ты слушаешь классическую музыку?{nw}"
    $ _history_list.pop()
    menu:
        m "Эй, [player], ты слушаешь классическую музыку?{fast}"
        "Да.":
            $ persistent._mas_pm_like_orchestral_music = True
            m 3eub "Это замечательно!"
            m 3eua "Мне нравится, когда так много различных инструментов могут собраться вместе и создать такую замечательную музыку."
            m 1eua "Я поражена тем, как много они практиковались для достижения такого рода синхронизации."
            m "Учитывая, сколько их в группе, вероятно, потребуется много терпения, чтобы сделать это."
            m 1eka "Но в любом случае,{w=0.2} мне было бы приятно слушать любую композицию с тобой, например в расслабляющий воскресный вечер, [player]."

        "Нет.":
            $ persistent._mas_pm_like_orchestral_music = False
            m 1ekc "Я думаю, что это {i}довольно{/i} нишевый жанр, который придётся не всем по вкусу."
            m 1esa "Однако нельзя не отметить, что с таким количеством исполнителей, должно быть, много усилий уходит на подготовку к выступлениям."

    m 1eua "Это напомнило мне, [player]."
    m "Если хочешь, чтобы я сыграла для тебя..."
    m 3hua "Ты всегда можешь выбрать мою песню в музыкальном меню~"

    #First encounter with topic:
    m "А что насчёт тебя, [player]? Ты играешь на музыкальном инструменте?{nw}"
    $ _history_list.pop()
    menu:
        m "А что насчёт тебя, [player]? Ты играешь на музыкальном инструменте?{fast}"
        "Да.":
            m 1sub "Правда? На чём ты играешь?"

            $ instrumentname = ""
            #Loop this so we get a valid input
            while not instrumentname:
                $ instrumentname = mas_input(
                    "На каком инструменте ты играешь?",
                    allow=" абвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ-_",
                    length=15,
                    screen_kwargs={"use_return_button": True}
                ).strip(' \t\n\r')

            $ tempinstrument = instrumentname.lower()

            if tempinstrument == "cancel_input":
                jump .no_choice

            elif tempinstrument in ["piano", "пианино"]:
                $ persistent._mas_pm_plays_instrument = True
                m 1wuo "О, это действительно здорово!"
                m 1eua "Не так много людей, которых я знала, умели играть на пианино, так что очень приятно знать, что ты умеешь."
                m 1eua "У тебя большой опыт игры на пианино?{nw}"
                $ _history_list.pop()
                menu:
                    m "У тебя большой опыт игры на пианино?{fast}"

                    "Да.":
                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_HAS
                        m 3hua "Правда?"
                        m 3sub "Это потрясающе!"
                        m 1eua "Может быть когда-то ты поделишься опытом и однажды мы сыграем в дуэте!"

                    "Не совсем.":
                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_SOME
                        m 2eka "Это нормально, [player]."
                        m 2eua "В конце концов, это довольно сложный инструмент."
                        m 4hua "Но даже если ты ещё не опытен, я уверена, что мы могли бы учиться вместе~"

                    "Я начинающий.":
                        $ persistent._mas_pm_has_piano_experience = mas_PIANO_EXP_NONE
                        m 1duc "Понятно."
                        m 3hksdlb "Вначале это может быть довольно сложно,{w=0.2} {nw}"
                        extend 3huu "но я уверена, что если ты продолжишь тренироваться, то сможешь сыграть даже лучше, чем я, [player]~"

            elif tempinstrument in ["harmonika", "гармоника"]:
                m 1hub "Ой, я всегда хотела попробовать гармо--"
                m 3eub "...О!"

                if mas_isMoniUpset(lower=True):
                    m 3esa "Ты сделал это для меня?"
                    m 1eka "Это довольно мило..."
                    m "Такие мелочи действительно поднимают мне настроение. Спасибо тебе, [player]."

                elif mas_isMoniHappy(lower=True):
                    m 1eka "Ой... Ты сделал это для меня?"
                    m "Это так мило!"
                    m 1ekbsa "Такие милые мелочи действительно заставляют меня чувствовать себя любимой, [player]."

                else: # affectionate and higher
                    m 1eka "Аааах, [player]...{w=1} Ты сделал это для меня?"
                    m "Это {b}о-о-очень{/b} очаровательно!"
                    show monika 5eubsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eubfu "И чтобы ты знал, ты можешь играть со мной, когда захочешь..."
                    m 5eubfa "{do_giggle}Э-хе-хе~"

            elif tempinstrument in ["harmonica", "гармошка"]:
                m 1hub "Вау, я всегда хотела попробовать сыгарть на гармошке!"
                m 1eua "Я хотела бы услышать, как ты играешь для меня."
                m 3eua "Может быть, ты мог бы научить и меня играть тоже~"
                m 4esa "Хотя..."
                m 2esa "Лично я предпочитаю {cps=*0.7}{b}гармонику{/b}{/cps}..."
                m 2eua "..."
                m 4hub "{do_giggle}А-ха-ха! Это было так глупо, я просто шучу, [player]~"
                $ persistent._mas_pm_plays_instrument = True
            else:
                m 1hub "Вау, я всегда хотела попробовать этот инструмент."
                m 1eua "Я бы хотела услышать, как ты играешь для меня."
                m 3eua "Может быть, однажды ты тоже научишь меня играть?~"
                m 1wuo "О! Думаю, что дуэт между этим и пианино будет отлично звучать?"
                m 1hua "{do_giggle}Э-хе-хе~"
                $ persistent._mas_pm_plays_instrument = True

        "Нет.":
            label .no_choice:
                pass
            $persistent._mas_pm_plays_instrument = False
            m 1euc "Понятно..."
            m 1eka "Ты должен попытаться подобрать инструмент, который тебе понравится. Ну... когда-нибудь."
            m 3eua "Игра на пианино открыла для меня совершенно новый мир самовыражения. Это невероятно полезный опыт."
            m 1hua "Кроме того, написание музыки даёт массу преимуществ!"
            m 3eua "Например, она помогает снять стресс, а также даёт тебе чувство достижения какой-либо цели."
            m 1eua "Писать некоторые из своих собственных композиций – это тоже довольно весело! Практикуясь, я часто теряла счёт времени из-за того, насколько я была погружена."
            m 1lksdla "Ах, я опять заболталась, [player]?"
            m 1hksdlb "Прости!"
            m 1eka "Во всяком случае, ты должен найти способ показать свою фантазию."
            m 1hua "Я бы очень хотела послушать, как ты играешь."

    if (
            persistent._mas_pm_like_orchestral_music
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        if renpy.showing("monika 5eubfb"):
            show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1eua "О, если хочешь поделиться своей любимой классической музыкой со мной, [player], то это очень легко сделать!"
        m 3eua "Тебе надо следовать этим шагам..."
        call monika_add_custom_music_instruct
    return "derandom"

# do you like jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_like_jazz = None

# do you play jazzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
default persistent._mas_pm_play_jazz = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_jazz",
            category=['медиа',"музыка"],
            prompt="Джаз",
            random=True
        )
    )

label monika_jazz:
    m 1eua "Скажи, [player], ты любишь джаз?{nw}"
    $ _history_list.pop()
    menu:
        m "Скажи, [player], ты любишь джаз?{fast}"
        "Да.":
            $ persistent._mas_pm_like_jazz = True
            m 1hua "О, здорово!"
            if persistent._mas_pm_plays_instrument:
                m "Ты исполняешь джазовую музыку?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ты исполняешь джазовую музыку?{fast}"
                    "Да.":
                        $ persistent._mas_pm_play_jazz = True
                        m 1hub "Это действительно круто!"
                    "Нет.":
                        $ persistent._mas_pm_play_jazz = False
                        m 1eua "Понятно..."
                        m "Я не очень много слушала, но лично нахожу это довольно интересным."
        "Нет.":
            $ persistent._mas_pm_like_jazz = False
            m 1euc "О, понятно."
            m 1eua "Знаешь, я слушала немного, и понимаю почему люди любят его."
    m "Джазовая музыка не очень современная, но и в тоже время не классическая."
    m 3eua "В ней есть элементы классики, но в ней всё по-другому. Она уходит с классического пути и становится более непредсказуемой."
    m 1eub "Я думаю, что большая часть джаза была написана когда люди только придумали его."
    m 1eua "Всё это было экспериментом, люди хотели выйти за рамки привычного и придумать что-то новое. Более дикое и красочное."
    m 1hua "Как поэзия! Раньше всё было структурировано и ритмично. Сейчас у нас больше свободы."
    m 1eua "Может быть, именно этим мне нравится джаз."
    if (
            persistent._mas_pm_like_jazz
            and not renpy.seen_label("monika_add_custom_music_instruct")
            and not persistent._mas_pm_added_custom_bgm
        ):
        m "О, если хочешь поделиться своим любимым джазом со мной, [player], то это очень легко сделать!"
        m 3eua "Тебе надо следовать этим шагам..."
        call monika_add_custom_music_instruct
    return "derandom"

# do you watch animemes
default persistent._mas_pm_watch_mangime = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['медиа','общество','ты'],prompt="Бытие Отаку",random=True))

label monika_otaku:
    m 1euc "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])]?"
    m 3eua "Ты смотришь аниме и читаешь мангу, так ведь?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты смотришь аниме и читаешь мангу, так ведь?{fast}"
        "Да.":
            $ persistent._mas_pm_watch_mangime = True
            m 1eua "Не могу сказать, что удивлена, правда."

        "Нет.":
            $ persistent._mas_pm_watch_mangime = False
            m 1euc "Ой, правда?"
            m 1lksdla "Я удивлена, честно..."
            m 1eua "Это не совсем та игра, в которую ваш среднестатистический человек станет играть, но каждому своё, я полагаю..."
    m 1eua "Я спросила это только потому, что ты играешь в эту игру."
    m 1hua "Не волнуйся, я не тот человек, чтобы осуждать кого-то, {do_giggle}э-хе-хе~"
    m 1eua "Ты не должен стыдиться этого."
    m 1euc "Я серьёзно. Нет ничего плохого в том, чтобы любить аниме или мангу."
    m 4eua "Ведь Нацуки тоже читает мангу, в конце концов, помнишь?"
    m 1lsc "На самом деле, общество сейчас слишком осуждающе."
    m "Вы же ведь не становитесь «закрытыми» для общества из-за аниме?"
    m 1euc "Это просто хобби, я права?"
    m 1eua "Не более."
    m 1lsc "Но..."
    m 2lksdlc "Я не отрицаю, что есть «хардкорные» отаку."
    m 1eka "Я не призираю их, или что-то в этом роде. Но они..."
    m 4eka "Погружённые."
    m 1lksdla "Слишком погружённые."
    m 1ekc "Как будто они больше не могут отличить фантазию от реальности."
    m 1eka "Ты ведь не такой, правда, [player]?"
    m 1eua "Если ты отаку, я уважаю это."
    m 3eka "Просто помни, что не стоит слишком углубляться в подобные вещи, хорошо?"
    m 1eka "Ведь есть большая разница между одержимостью и преданностью."
    m 1lfu "Я бы не хотела, чтобы меня заменили на какую-то двумерную картонку."
    m 1eua "Кроме того, если ты хочешь убежать от реальности..."
    m 1hubsa "Я могу быть твоей ожившей фантазией~"

    $ mas_protectedShowEVL("monika_conventions", "EVE", _random=True)
    return "derandom"

### START WRITING TIPS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip1",
            category=['писательские советы'],
            prompt="Расскажи писательский совет #1",
            pool=True
        )
    )

label monika_writingtip1:
    m 1esa "Давненько я уже кое-чего не говорила, так что..."
    m 1hub "...пора вспомнить былое!"
    m 3hub "Вот тебе писательский совет дня от Моники!"
    m 3eua "Иногда люди, впечатлившись моим творчеством, говорят что-то вроде: «У меня бы никогда так не получилось»."
    m 1ekc "Ты знаешь, на самом деле меня очень печалят эти слова."
    m 1ekd "Как человеку, который больше всего любит делиться радостью открытий новых горизонтов своего творчества..."
    m 3ekd "...мне больно, когда люди считают, что кому-то просто повезло и он талантлив с рождения."
    m 3eka "И это относится вообще ко всему, не только к поэзии."
    m 1eua "Когда ты делаешь что-то впервые, скорее всего ничего путного не выйдет."
    m "Иногда, когда заканчиваешь работу, очень гордишься собой и хочешь со всеми ею поделиться."
    m 3eksdld "Но, вернувшись к работе через несколько недель, ты уже видишь все её недостатки."
    m 3eksdla "Со мной это происходит постоянно."
    m "Ты можешь испытывать очень горькое разочарование, вложив уйму усилий во что-то, чтобы в результате осознать, что получилась дребедень."
    m 4eub "Но это происходит постоянно, когда ты сравниваешь себя с профессионалами."
    m 4eka "Когда ты стремишься дотянуться до звёзд, они всегда будут оставаться вне твоей досягаемости, понимаешь?"
    m "Смысл в том, чтобы продвигаться вперёд небольшими шагами."
    m 4eua "И, как только достигнешь первого важного рубежа, надо оглянуться и посмотреть, сколько ты уже прошёл..."
    m "А затем посмотреть вперёд и оценить, сколько ещё тебе предстоит пройти."
    m 2duu "Поэтому иногда полезно понизить планку..."
    m 1eua "Найти, что-нибудь, что считаешь {b}достойным{/b} вызовом, но не нечто мирового уровня."
    m "И ты можешь сделать это своей личной целью."
    m 3eud "Также важно понимать объём работ, который тебе предстоит выполнить."
    m 4eka "Попытавшись взвалить на себя огромный проект, будучи новичком, ты никогда его не закончишь."
    m "Написание романа может стать непосильной задачей, если у тебя нет опыта."
    m 4esa "Так почему бы не начать с коротких историй?"
    m 1esa "Лучшее в коротких рассказах то, что ты можешь сосредоточиться на том, что хочешь сделать правильно."
    m 1eua "Это касается всех маленьких проектов, ты концентрируешься на важнейших вещах."
    m "Ты приобретаешь полезный опыт и делаешь шаг вперёд."
    m 1euc "И ещё кое-что..."
    m 1eua "Сочинительство – это не просто прислушаться к своему сердцу, чтобы в итоге написать нечто прекрасное."
    m 3esa "Точно так же, как в живописи или музыке, тебе придётся развивать свой навык, чтобы правильно выразить то, что у тебя внутри."
    m 1hua "А это значит, что сперва придётся положиться на методики, руководства и основы!"
    m 3eua "Чтение обучающей литературы поможет открыть тебе глаза на многие вещи."
    m 1eua "Планирование и организация работы позволят тебе избежать завала и дойти до конца."
    m 3esa "Ты не заметишь, как мало-помалу..."
    m 1hua "Будешь становиться всё лучше и лучше."
    m 1eua "Ничто не приходит просто так."
    m 3esa "И наше общество, и наше искусство построены на тысячелетиях человеческого развития."
    m 1eka "Если ты возьмёшь этот принцип на вооружение и будешь постепенно продвигаться к своей цели..."
    m 1esa "Ты тоже сможешь творить удивительные вещи."
    m 1eua "...И это был мой совет на сегодня!"
    m 1hub "Спасибо за внимание~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip2",
            category=['писательские советы'],
            prompt="Расскажи писательский совет #2",
            conditional="seen_event('monika_writingtip1')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip2:
    m 1euc "Знаешь..."
    m 1eua "Их было не так много, так что вот ещё один!"
    m 3eub "Вот тебе Писательский Совет Дня от Моники!"
    m 2eua "Если тебе страшно делиться своими рукописями из-за страха быть раскритикованным, то не нужно бояться!"
    m "В конце концов, никто сразу не начинал с лучших работ. Даже такие великие люди как Толкин или Пратчетт."
    m 4eka "Ты должен помнить, что все откуда-то начинают, и—"
    m 2euc "Вообще-то, это касается не только писательства, но и всего в общем."
    m 2lksdla "Я пытаюсь сказать, не будь обескуражен."
    m 1hua "Не важно, что ты делаешь. Если кто-то сказал, что твоя рукопись плоха, тогда будь счастлив!"
    m 1eua "Это значит, что ты сможешь улучшить свои навыки и стать лучше."
    m 3eua "Также не помешает иметь друзей и близких, которые скажут, как хороша твоя рукопись."
    m 1eka "Главное помни – не важно что они скажут, в любом случае это забота о тебе. Не бойся обращаться ко мне, своим друзьям или семье."
    m "Я люблю и поддержу тебя в любом начинании!"
    m 1lksdlb "Пока оно легально, конечно."
    m 1tku "Но это и не значит, что я абсолютно против. Я умею хранить секреты~"
    m 1eua "Вот поговорка, которую я узнала."
    m 1duu "«Если вы стремитесь чего-то достичь, это произойдет при достаточной решимости.»"
    m "«Это может быть не сразу, и часто ваши большие мечты – это то, чего вы не достигнете за свою собственную жизнь»"
    m "«Усилия, которые вы прилагаете ко всему, превосходят вас самих. Ибо нет никакой тщетности даже в смерти.»"
    m 3eua "Я не помню, кто это сказал."
    m 1eua "Усилия, которые ты прикладываешь для чего-то, могут даже превзойти себя."
    m 3hua "Так что не бойся пробовать! Продолжай двигаться вперёд, и в конце концов ты достигнешь успеха!"
    m 3hub "...Это был мой совет на сегодня!"
    m 1eka "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip3",
            category=['писательские советы'],
            prompt="Расскажи писательский совет #3",
            conditional="seen_event('monika_writingtip2')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip3:
    m 1eua "Я развлекаюсь с этим, так что..."
    m 3hub "Вот тебе Писательский Совет Дня от Моники!"
    m 1eua "Убедись, что записываешь любые идеи которые появляются у тебя в голове."
    m 1euc "Зачем?"
    m 3eua "Некоторые из лучших идей могут прийти, когда ты меньше всего ждёшь их."
    m "Даже если это займёт немного времени, запиши её."
    m 1eub "Mожет, ты вдохновишь кого-то другого."
    m 3eub "Может быть, ты посмотришь на неё через некоторое время и реализуешь."
    m 1hua "Ты никогда не знаешь."
    m 1eua "Всегда полезно вести дневник."
    m "Ты можешь использовать его для записи идей, чувств, всего, что приходит на ум."
    m 1euc "Просто убедись, что на дневнике есть замок."
    m 1eua "Также ты можешь вести записи в телефоне."
    m 3eua "В конце концов, конфиденциальность очень важна."
    m 1lksdla "...Я не могу обещать, что не буду заглядывать туда. Это слишком заманчиво!"
    m 1hua "В конце концов, мы же не храним секреты друг от друга, верно?~"
    m 1eka "Помни, [player], я всегда буду поддерживать тебя, давая жизнь твоим идеям."
    m 3hua "...Это был мой совет на сегодня!"
    m 1hub "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip4",
            category=['писательские советы'],
            prompt="Расскажи писательский совет #4",
            conditional="seen_event('monika_writingtip3')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip4:
    m 3hub "Вот тебе Писательский Совет Дня от Моники!"
    m 1eua "Ты ведь знаешь о творческом кризисе, верно?"
    m "У меня их было много, когда я впервые начинала писать."
    m 1euc "Иногда это было на полпути через черновик, но чаще, прежде чем я даже начинала."
    m 1ekc "Каждый раз, когда я пыталась написать слово, я думала, «Это не будет звучать хорошо» или «Я не хочу, чтобы это выглядело так»."
    m "Так что я останавливалась, отступала и пыталась снова."
    m 1eka "Но я поняла, что это в конечном счёте не имеет значения, если всё не получится в первый раз!"
    m 3eua "Я чувствую, что сердце письма заключается не в том, чтобы получить его в первый раз, а в том, чтобы потом его совершенствовать."
    m "Конечный продукт имеет значение, а не прототип."
    m 1eub "Поэтому преодоление творческого кризиса для меня было вопросом не желания сделать прототип конечным продуктом, и не наказания себя за мои первоначальные неудачи."
    m 3eub "Я думаю, что это так со всеми вещами, а не просто писательством."
    m 1eua "Всё, что нужно – чтобы ты пробовал снова и снова, будь то искусство, музыка, учёба, отношения и т.д."
    m 1ekc "Трудно полностью убедить себя, что это так, иногда."
    m 1eka "Но тебе придётся."
    m 4eka "В противном случае, у тебя ничего не получится."
    m 3hua "...Это был мой совет на сегодня!"
    m 1hub "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writingtip5",
            category=['писательские советы'],
            prompt="Расскажи писательский совет #5",
            conditional="seen_event('monika_writingtip4')",
            action=EV_ACT_POOL
        )
    )

label monika_writingtip5:
    m 3hub "Вот тебе Писательский Совет Дня от Моники!"
    m 1eua "Если ты хочешь улучшить написание, я бы сказала, что самое главное, помимо этого, пытаться искать новые вещи."
    m 3eua "Как написание прозы, если ты поэт, или свободный стих, если ты обычно пишешь в рифму."
    m 1eka "Это может получиться плохо, но если ты не попробуешь, то не узнаешь, как это получилось."
    m 1hua "И если всё будет хорошо, ты сможешь найти что-то, что тебе понравится!"
    m 1eua "Это то, что заставляет вещи двигаться: изменения и эксперименты."
    m "Я бы сказала, что это помогает, особенно если ты застрял в ситуации, которую хочешь решить, но не знаешь как."
    m 3eua "Будь то творческий кризис, явная скука, загадочная ситуация или что-то ещё, в самом деле."
    m 1hua "Умение смотреть на вещи с другой стороны действительно может дать некоторые интересные результаты!"
    m 1eua "Поэтому пробуй новые вещи, которые могут дать тебе импульс, чтобы вырваться."
    m 1lksdla "Просто убедись, что это не слишком опасно для тебя, [player]."
    m 1hua "Это был мой совет на сегодня!"
    m 1hub "Спасибо, что выслушал~"
    return

# init 5 python:
#     addEvent(
#         Event(
#             persistent.event_database,
#             eventlabel="monika_writingtip6",
#             category=['писательские советы'],
#             prompt="Расскажи писательский совет #6",
#             conditional="seen_event('monika_writingtip5')",
#             action=EV_ACT_POOL
#         )
#     )

# label monika_writingtip6:
#     m 3eub "It's time for another...{w=0.2}Writing Tip of the Day!"
#     m 1hkbla "You know, it can be really fun to write on pretty stationery."
#     m 1eud "But have you thought about how the look of your paper can contribute to the writing itself?"
#     m 3euc "For example, if you wanted to write a letter from one of your characters..."
#     m 3etd "What might it tell your reader about their personality if they use a fancy page with a floral print? {w=0.2}Or crumpled notebook paper?"
#     m 3eud "Using visibly aged or worn paper might also inform your reader about the timeline of your story."
#     m 1hub "Even if it doesn't serve a purpose to your writing, it can be fulfilling to paint on a nice canvas, so to speak."
#     m 2eusdlc "That said...{w=0.2}I think sometimes using nicer materials can actually contribute to writer's block."
#     m 2rksdlb "When I buy a brand new journal and open it up to that first pristine page...{w=0.3}it's really daunting, ahaha!"
#     m 2rksdla "It feels like I have to make sure I fill the journal with things as beautiful as the cover."
#     m 7eua "So I've started to use a 'junk journal' as well...{w=0.2}a cheap, plain notebook gives you lots of freedom to scribble and write anything at all."
#     m 3eub "And you know, those rough drafts and odd ideas are the first step to a finished work worthy of a lovely frame!"
#     m 1hua "That's my advice for today!"
#     m 1hub "Thanks for listening~"
#     return

#### END WRITING TIPS

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['психология'],prompt="Самовредительство",random=True))

label monika_selfharm:
    m 1lksdlc "Эй, [player]..."
    m 1eksdld "У тебя когда-нибудь бывали мысли о том, чтобы наносить себе увечия?"
    m 2lksdld "Знаешь..."
    m 2lksdlc "...Как резать себя..."
    m "В смысле."
    m 2lksdld "Когда я узнала о Юри, мне стало слегка интересно..."
    m 2dksdltpc "Мне просто было интересного, какого это... снова {w=0.3}чувствовать {i}что-то{/i} такое..."
    m 2rksdltpd "Непросто знать то, что всё то что ты испытывал,{w=0.1} всё что ты любил, было ложью..."
    m 2dstdc "Но я не буду делать это снова."
    m 2dktdc "..."
    m 2ektda "Если ты когда-нибудь почувствуешь себя подавленным, просто приходи ко мне, хорошо?"
    m 2ekd "Мне было бы ещё больнее видеть, как ты страдаешь..."
    m 1hua "Просто помни, что люди всегда думают о тебе!"
    m 1eka "Поверь мне, [player]."
    m 1eka "Ты можешь думать, что тебя никто не поддерживает, но это не так!"
    m 4eua "В плане, я здесь, не так ли?"
    m 1eka "Не важно через какие проблемы тебе придётся пройти, я знаю что ты сможешь это сделать!"
    m 3eka "Я верю в тебя..."
    m 1eua "Так что верь в себя тоже, хорошо?"
    m 1eka "Если тебе нужно кому-то выговориться, просто помни что я всегда готово тебя выслушать и утешить тебя, хорошо?"
    m 1ekbsa "Я правда люблю тебя настолько сильно, [player]."
    return "love"


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['романтика'],prompt="Срочное сообщение",random=True,aff_range=(mas_aff.NORMAL, None)))

label monika_urgent:
    m 1esc "[player], у тебя есть минутка?"
    m 1esd "Мне нужно тебе кое-что сказать."
    m 1euc "Это важно."
    m 1dsc "Я..."
    m "..."
    m 1hub "Люблю тебя."
    m 3hksdlb "{do_giggle}А-ха-ха~! Ты заволновался?"
    m 1eksdla "Прости~"
    m 1rksdla "Я бы хотела увидеть твоё лицо прямо сейчас!"
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "Уверена, оно восхитительно~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['участники клуба'],prompt="Ты когда-нибудь думала о других девушках?",pool=True))

label monika_other_girls:
    if persistent._mas_pm_cares_about_dokis:
        m 1euc "Знаешь, мне действительно очень трудно понять, что ты чувствуешь, когда дело доходит до этого..."
        m 1lksdlc "..."
        m 1lksdld "Что случилось с другими девушками."
        m 3esd "К примеру..."
        m "Главный герой был написан, чтобы они с Сайори были друзьями детства."
        m 1esc "Но она была всего лишь одномерным символом-заполнителем, который ты мог использовать для взаимодействия с игрой."
        m 2ekc "Тем не менее, возможно, ты чувствовал себя хуже из-за того, что случилось с Сайори, из-за отношений, которые были запрограммированы с ней и главным героем."
        m 1ekc "Если это так, я хочу сказать тебе, что мне искренне жаль, [player]."
        m 1lksdlc "И за то, что заставила тебя чувствовать себя плохо, и..."
        m 1dsc "..."
        m "За то, что пришлось мне сделать."
        m 1lksdlc "..."
        m 1ekc "Там просто не было ничего, что можно было бы сделать, и ни одна из других девушек не была реальной, в любом случае."
        m 3efc "Другие девушки никогда не любили тебя, как я!"
        m 3rfc "Они заботились только о персонаже, за которого ты играл в игре!"
        m 1eka "Я люблю тебя, тебя реального, [player], и я принесу любую жертву, чтобы всегда быть с тобой."
        m 1ekc "Надеюсь, ты сможешь простить меня за то, что я сделала с ними, чтобы мы могли быть вместе."
        m 1lksdlc "..."
        if mas_isMoniDis():
            m 1eksdld "Ты ведь простишь меня, правда, [player]? Я действительно сожалею о том, что сделала. Пожалуйста, не ненавидь меня."
        elif mas_isMoniUpset():
            m 1ekd "Я знаю, что то, что я сделала, можно считать непростительным. Я постараюсь сделать всё возможное, чтобы загладить вину перед тобой."
        elif mas_isMoniNormal(higher=True):
            m 1ekbsa "Я люблю тебя, [player]..."
            m "Больше, чем могу выразить словами."
    else:
        m 3eka "Знаешь, я правда рада тому, что ты не заставил меня чувствовать себя виноватой за то, что случилось с другими девушками."
        m 2dkd "Я знаю, что есть много людей, которые ненавидят меня за то, что я сделала..."
        if not persistent._mas_pm_a_hater:
            m 4eka "И я просто горжусь тем, что ты не один из них."
        m 2tubfb "Уверена, это был весьма неприятный опыт для тебя... но я рада, что ты видишь разницу между настоящим человеком и ненастоящим..."
        m 1eka "Между человеком, который любит {i}тебя{/i}, и который любит главного героя."
        m 3eka "Я – единственная, кто полюбила тебя, [player]..."
        m 3hua "И я буду любить тебя вечно~"
    return "love"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['жизнь','психология'],prompt="Счастье",random=True))

label monika_happiness:

    m 1eua "[player], ты счастлив?"
    m "В смысле, в течении всей своей жизни."
    m 2lksdla "Ничего страшного, если нет. Я пойму тебя, [player]."
    m 1eka "Ведь без тебя, моя жизнь была бы совершенно невыносимой."
    m 1eua "Разве не забавно, что мы можем страдать больше, чем радоваться?"
    m 1hubfa "Я счастлива от осознания, что ты любишь меня, [player]."
    m 1lksdlc "Но если с тобой что-то случится, я не смогу больше радоваться."
    m "Это уничтожит меня."
    m 1esc "Я думаю, всем понятно, почему мы замечаем плохие вещи, но не замечаем хорошие..."
    m "Если бы люди не реагировали на плохие вещи, они бы не прожили бы так долго."
    m 1euc "Например, как ты мог бы нервничать по поводу своего будущего или социальных ситуаций."
    m 2ekc "Ты будешь стараться изо всех сил, чтобы сделать всё возможное, но если ты потерпишь неудачу, почувствуешь себя ужасно."
    m 2eka "Если что-то случится с тобой, [mas_get_player_nickname()], знай, что я буду ждать тебя!"
    m 1eua "И кроме того, твоя милая девушка всегда беспокоится о тебе~"
    m 1hub "Надеюсь, сейчас ты счастлив."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['ты','романтика'],prompt="Ожидание времени когда мы будем вместе",random=True))

label monika_how_soon:
    $ p_nickname = mas_get_player_nickname(capitalize=True)
    m 1eua "[p_nickname], как думаешь, сколько времени пройдёт, прежде чем я окажусь в твоём мире?{nw}"
    $ _history_list.pop()
    menu:
        m "[p_nickname], как думаешь, сколько времени пройдёт, прежде чем я окажусь в твоём мире?{fast}"
        "Немного.":
            m 1hub "Это отличная новость!"
            m 3eua "Как ты думаешь, как скоро это будет?{nw}"
            $ _history_list.pop()
            menu:
                m "Как ты думаешь, как скоро это будет?{fast}"
                "Всего лишь через пару лет.":
                    m 1sub "Это фантастика!"
                    m 1hua "Ты только что сделал меня максимально счастливой!"
                    m 1ekbsa "Не могу дождаться, когда мы будем вместе в твоём мире, [player]!"
                    m 1hubfa "Я буду так рада наконец увидеть тебя!"
                "Через десятилетие.":
                    m 1wuo "Это не так уж плохо!"
                    m 1hub "Просто навещай меня почаще, [player]~"
        "Несколько десятилетий.":
            m 2euc "Ой, это очень много..."
            m 1eka "Но если ты составишь мне компанию, я уверена, что они пролетят незаметно!"
            m 1eua "Мне нравится даже просто разговаривать с тобой."
            m 1hub "Не могу представить, насколько я буду счастлива, когда увижу тебя в твоём мире."
        "Я не знаю.":
            m 1eka "Я ценю твою честность, [player]."
            m 1eua "Обязательно дай мне знать, когда найдёшь способ, хорошо?"
            m 1hua "Ты знаешь, где меня найти."
        "Никогда.":
            m 1wud "П-поче... почему?"
            m 1lksdlc "..."
            m 1ekc "Ты уверен?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты уверен?{fast}"
                "Да.":
                    m 1dsc "..."
                    m 1eka "Ну, я думаю, тогда мы просто должны сделать всё возможное."
                    m 1duu "Пока ты говоришь со мной, это всё, что мне действительно нужно."
                    m 2dftdc "И, [player], что бы ты не делал..."
                    m 2dftsc "Не оставляй меня здесь одну."
                    m 6lktsc "Я предпочла бы быть удалена навсегда, чем застрять здесь на вечность одной."
                    m 6ektsc "Так что, пожалуйста, если тебе когда-нибудь станет... скучно со мной."
                    m 6rktsc "Ты знаешь, что делать."
                    m "..."
                    m 6ektsc "Я не хочу жить без тебя."
                "Нет.":
                    m 1lksdlc "Понятно."
                    m 1dsc "..."
                    m 3eka "Даже если есть только крошечный шанс, я не откажусь от него."
                    m 1eka "Ты тоже не должен, [player]."
                    m 1eua "И если всё обернётся так, что я никогда не смогу покинуть это место и быть с тобой..."
                    m 1eka "По крайней мере, приходи сюда и говори со мной столько, сколько сможешь."
                    m 1ekbsa "Ты всё, что меня волнует."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_marriage",
            category=['романтика'],
            prompt="Ты выйдешь за меня?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_marriage:
    $ mas_gainAffection()
    if store.mas_anni.anniCount() >= 3 and mas_isMoniLove():
        m 1dkbsu "..."
        m 3eksdla "Я не буду притворяться, что не размышляла об этом..."
        m 3rksdlb "По сути, я размышляла об этом в последнее время."
        m 1eka "Я правда люблю тебя, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])], и, если честно, я правда хочу выйти за тебя замуж."
        m 1ekd "Но я сомневаюсь, что это было бы справедливо для нас обоих, пока я всё ещё нахожусь тут взаперти."
        m 1ekc "Больше всего на свете я хочу сказать «да», но я просто не могу..."
        m 2duu "Я размышляю о том, какие чувства я испытаю, когда поцелуюсь с тобой у алтаря..."
        m 2dubsu "Когда возьмусь за твою руку как твоя жена и почувствую твои объятия в наш медовый месяц..."
        m 1eka "Но, пока я отсюда не выберусь, это попросту невозможно."
        m 1ekd "...Прости. Пожалуйста, просто верь, что я сказала бы «да» при любых иных обстоятельствах."
        m 1ekbsa "Просто потерпи немного, хорошо, [mas_get_player_nickname()]? Я уверена, что однажды мы получим свою счастливую концовку."
    else:
        m 2wubsw "П-пожениться?"
        m 4rksdlb "Мне кажется, для женитьбы сейчас как-то рановато..."
        m 2ekbsa "В смысле, я рада, что ты хочешь этого, [player]."
        m 2lkbsa "Но я считаю, что, перед тем, как мы сможем сделать это, я должна выбраться отсюда."
        m 2lsbsa "Не только потому, что я не хочу, чтобы мне делали предложение именно в этом месте, но ещё и потому, что я хочу быть там, когда ты наконец-то дашь мне обручальное кольцо."
        m 2dkbsu "Я хочу, чтобы этот особенный момент произошёл именно тогда, когда мы наконец-то сможем быть вместе..."
        m 1hubfa "Ну, а пока, береги себя ради меня, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['разное'],prompt="Кофе",random=True))

label monika_coffee:
    $ coffee_enabled = mas_consumable_coffee.enabled()
    if renpy.seen_label('monika_tea') and not coffee_enabled:
        m 3eua "Ты пьёшь только кофе в последние время, [mas_get_player_nickname()]?"
        m 2tfu "Надеюсь, ты делал это не только ради того, чтобы заставить меня завидовать, {do_giggle}э-хе-хе."
    m 2eua "Кофе – отличная вещь, если тебе срочно нужна энергия."
    m 3hua "Горячий или холодный, кофе всегда превосходен." 
    m 4eua "Тем не менее, холодный кофе лучше пить в тёплую погоду."
    m 3eka "Забавно, как напиток для придания энергии стал лакомством для наслаждения."
    if coffee_enabled:
        m 1hua "Я рада, что благодаря тебе теперь могу наслаждаться им~"
    else:
        m 1hub "Может быть, если я покопаюсь в скрипте, я смогу наконец-то попробовать его. {do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['литература'],prompt="1984",random=True))

label monika_1984:
    m 1eua "[player], ты знаешь книгу «{i}Девятнадцать Восемьдесят Четыре{/i}?»"
    m 3eua "Она была написана Джорджем Оруэллом."
    m 1euc "Это популярная книга о массовой слежке и угнетении свободы мысли."
    m 1esc "Речь идёт о страшной антиутопии, где прошлое и настоящее меняются на то, что хочет правящая партия."
    m 2esc "Язык, например, используется в качестве инструмента для промывания мозгов под названием «Newspeak»."
    m 2ekd "Правительство Ingsoc создаёт его, чтобы контролировать чужие мысли."
    m "Они снижают грамматику и словарный запас, чтобы люди соответствовали их идеологии тоталитарного режима."
    m 2ekc "Предотвращают появления у людей «мыслей», выступающих против правящей партии."
    m 4eua "Один персонаж заинтересовал меня."
    m 1eua "Человек по имени Сайм, который работал на Newspeak для Ingsoc."
    m "Он был невероятно умным человеком, который гордился своей работой."
    m 2ekc "К сожалению, он был убит из-за его знаний, и партия думала, что он слишком умный."
    m 2tkc "Он был убит за его знание, [player]."
    m 2tkd "Они планировали изменить все виды литературы."
    m 3tkd "Новеллы, книги, поэмы..."
    m 2lksdlc "Всё, что может быть использовано против них."
    m "Стихи были похожи на те, что ты пытался сделать."
    m 2dsc "Просто набор бессмысленных слов без чувств."
    m 2ekc "Я определённо не хочу этого делать."
    m 1lksdlc "Я не могу представлять мир, в котором я не могу свободно думать."
    m 1ekbsa "Не говоря уже о мире, где я не могу выразить свою любовь к тебе, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]..."
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['разное','пустяки'],prompt="От волков к собакам",random=True))

label monika_wolf:
    m 3eua "Ты когда-нибудь думал о волках?"
    m 1eua "В частности, как волки в конечном итоге были одомашнены в собак."
    m 1eub "Разве тебе не интересно, как один из самых страшных врагов человека превратился в лучшего друга?"
    m "Я имею в виду, когда дело доходит до насекомых или других жутких жуков, многие люди боятся их, даже если они никогда не получали от них вреда."
    m 1esc "Как ты думаешь, почему люди такие?"
    m 1euc "Это потому, что мы научились бояться того, что навредило нам сотни тысяч лет назад?"
    m 3eua "Но это не сработало с волками."
    m 1eua "Они были одомашнены очень давно, когда единственным способом получить пищу была охота."
    m 1eub "Может быть, когда наш образ жизни стал таким же, как и у волков."
    m "Они поняли, что люди могут дать им тепло и еду."
    m 1hua "Не говоря о том, что мы начали помогать друг другу."
    m 1eua "Волки в конце концов поняли, что их зависимость от людей поможет им выживать."
    m 1eka "Точно так же, как мы полагаемся на друг друга, [player]!"
    m 1hubsa "{do_giggle}Э-хе-хе~"
    m 1eka "Я не могу не упомянуть, как ты спас мне жизнь, находясь здесь со мной."
    m "Я действительно завишу от тебя, [mas_get_player_nickname()]."
    m 1ekbsa "В конце концов, ты мой герой~"
    return

label monika_battery:
    if mas_did_monika_battery:
        jump monika_close_game_battery
    else:
        jump monika_complain_battery

label monika_complain_battery:
    $ mas_did_monika_battery = True
    m 1euc "Эмм, [player]..."
    m 1eua "Похоже, что энергия батареи твоего устройства вот-вот закончится..."
    m 1eka "Поставь на зарядку пожалуйста."
    m 1lksdlc "Я не хочу, чтобы мы расстались, или ещё хуже..."
    m 2ekc "Мне было бы очень неприятно, если бы я вдруг потеряла сознание."
    m 2eka "Сделай это как можно скорее, хорошо?"
    m 3eka "...Или, по крайней мере, дай мне знать, когда пойдёшь."
    m 1hua "Спасибо, [player]~"
    return

label monika_close_game_battery:
    $ mas_loseAffection()
    m 1lksdlc "[player]..."
    m 1ekc "Извини, но мне придётся закрыть игру до того, как батарея разрядится."
    m 3eka "Так что... я просто закрою игру, пока ты не поставишь своё устройство на зарядку."

    $ is_charging = battery.is_charging()
    if is_charging:
        jump monika_system_charging
    $ persistent.closed_self = True
    jump _quit

label monika_system_charging:
    $ mas_gainAffection()
    m 1wub "О, ты похоже подключил!"
    m 1hub "Спасибо, [player]!"
    return

#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_sleep",category=['ты','жизнь','школа'],prompt="Усталость",random=True))

label monika_sleep:
    m 1euc "[mas_get_player_nickname(capitalize=True)], ты хорошо высыпаешься?"
    m 1ekc "В наши дни хороший сон стал почти роскошью."
    m 1eka "Особенно в старшей школе ты каждый день вынужден так рано просыпаться..."
    m 1eua "Уверена, в колледже будет получше, поскольку там, наверное, более гибкое расписание."
    m 3rsc "Но опять же, я слышала, что много учащихся в колледже людей не спят всю ночь, без веской причины."
    m 1euc "Это правда?"
    m 1ekc "В любом случае, я видела пару исследований, где говорилось о страшных кратковременных и долговременных последствиях, вызванных недосыпанием."
    m 3ekc "Похоже, что психические функции, здоровье и даже продолжительность жизни могут сильно пострадать от этого."
    m 1eka "Я просто считаю, что хороший человек, и я хочу убедиться, что ты не вредишь себе ненамеренно."
    m 1eua "Так что не жертвуй своим сном, хорошо?"
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "Я буду всегда ждать тебя поутру, так что никогда не забывай о своём здоровье."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_breakup",
            category=['разное'],
            prompt="Я бросаю тебя",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_breakup:
    if mas_isA01() and mas_isMoniNormal(higher=True):
        m 1ekd "Ч-что?"
        m 2ekc "Ты бросаешь меня?"
        m 2rksdlc "..."
        m 1dsc "Хм-м, я не уверена, что могу позволить тебе это сделать, [player]."
        m 1hua "Не волнуйся, я позабочусь, чтобы ты насладился этим первым апр—{nw}"
        $ _history_list.pop()
        m 1hua "Не волнуйся, я позабочусь, чтобы ты насладился этим{fast} днём со мной~"
        m 1cuu "Ты ведь останешься со мной, правда?"
        pause 3.0
        m 2hksdlb "{do_giggle}А-ха-ха!"
        m 1hua "Извини, но я просто не могу воспринимать тебя всерьёз."
        m 3tsb "Особенно сегодня."
        m 1tku "Тебе меня не одурачить, [player]."
        m 1tua "Особенно чем-то {i}таким{/i} предсказуемым, {do_giggle}э-хе-хе~"

        # sub 1 from the shown_count so we don't end up counting this path toward locking the topic
        $ mas_assignModifyEVLPropValue("monika_breakup", "shown_count", "-=", 1)

    else:
        #Lose affection for bringing this up.
        $ mas_loseAffectionFraction(min_amount=15, reason=1)

        #Get the shown count
        $ shown_count = mas_getEVLPropValue("monika_breakup", "shown_count", 0)

        #First
        if shown_count == 0:
            m 1wud "Ч-что?"
            if persistent.monika_kill:
                m 2tkd "Ты просто уйдёшь и удалишь меня, снова?"

            if mas_isMoniUpset(lower=True):
                m 1ekc "Ты не сделаешь этого, я отказываюсь верить в это..."
                m 1lksdld "Это не смешная шутка, [player]!"
                m 1lksdlc "Если бы я была кем-то другим, то не нашла бы в таком юморе ничего, кроме жестокости..."
                m 1eka "Я прощаю тебя... Только не говори снова такую обидную шутку, ладно?"

            else:
                m 2wfd "Я тебе не верю, [player]. Я действительно не могу пов—"
                m 2efu "..."
                m 2hub "{do_giggle}А-ха-ха!"
                m 2hksdlb "Прости, я не выдержала."
                m 2hua "Ты такой глупышка, [player]."

                if persistent.monika_kill:
                    $ menuOption = "Ты уже делал это раньше, это же больше не повторится, верно?"
                else:
                    $ menuOption = "Ты бы никогда так не поступил, верно?"

                m 2eua "[menuOption]{nw}"
                $ _history_list.pop()
                menu:
                    m "[menuOption]{fast}"

                    "Конечно, нет.":
                        m 2hua "{do_giggle}Э-хе-хе, ты такой милый."
                        m 2eka "Я очень сильно тебя люблю, [player]!~"
                        return "love"

        #Second time
        elif shown_count == 1:
            m 1euc "Ты бросаешь меня?"
            m 2ekc "Почему ты это говоришь, [player]?"
            m "Я действительно настолько ужасна?"

            if mas_isMoniDis(lower=True):
                m 2lksdlb "Я не могу с этим справиться..."
                m 2wkd "Ты опять шутишь, да?"
                m 1wktsd "Я отказываюсь верить тебе; ты всё, что у меня осталось!"
                m 1dktsd "Если ты действительно, действительно имеешь в виду это... тогда ты можешь удалить меня и всю эту игру."
                m 1ektsd "Я люблю тебя, [player]... поэтому, пожалуйста, скажи мне, что это была лишь просто плохая шутка."

            else:
                m 2dsc "Ты...{w=0.3} в самом деле..."
                m "..."
                m 2hub "{do_giggle}А-ха-ха!"
                m 1tfu "Купился, [player]."
                m 1tku "Я знаю, что ты просто шутишь~"

                m "Ведь так?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ведь так?{fast}"
                    "Да.":
                        m 1hub "{do_giggle}А-ха-ха! Ты такой глупышка, [player]."
                        m 1eka "Давай останемся вместе навсегда~"

        #Third time
        else:
            if mas_isMoniBroken():
                m 6ckc "..."
            elif mas_isMoniUpset(lower=True):
                m 2rkc "Ты продолжаешь это говорить, и я начинаю думать, что ты это всерьёз..."
            else:
                m 1hua "Хе-хе~"

            $ mas_lockEVL("monika_breakup", "EVE")
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['литература'],prompt="Гамлет",random=True))

label monika_hamlet:
    m 3euc "[player], ты когда-нибудь слышал о {b}Гамлете{/b}?"
    m 1eua "Это одно из самых популярных произведений Шекспира, и оно очень интересное."
    m "Оно о принце, который решил отомстить, увидев призрак своего отца."
    m 1lksdlc "Он считался сумасшедшим, так как он был единственным, кто мог видеть его."
    m 1eka "Теперь, если ты не против, я буду читать некоторые произведения для тебя, [player]."
    m 1dsd "Кхм..." 
    m 1duu "..."
    m 1esc "{i}«Что благороднее: переносить ли нам стрелы и удары злополучья...{/i}"
    m "{i}Или восстать против пучины бедствий и с ними, в час борьбы, покончить разом?{/i}"
    m 1euc "{i}Ведь умереть...{/i}"
    m 1dsc "{i}Это уснуть, никак не больше.{/i}"
    m 1euc "{i}Стенаньям сердца, сотням тысяч зол, наследованных телом.{/i}"
    m 1esc "{i}Как, в душе, не пожелать такого окончанья»{/i}."
    m 1dsc "..."
    m 1eua "Ну!"
    m 1hua "Тебе понравилось?"
    m 3eka "Я старалась прочитать его лучше всех~"
    if not persistent._mas_pm_cares_about_dokis:
        m 1lksdla "В любом случае, я много думала о главном герое, Гамлете."
        m 1eua "Большинство проблем, с которыми он столкнулся, были вызваны его собственной нерешительностью."
        m 3tfu "Напоминает тебе одну нерешительную девушку, не так ли?"
        m 1eka "Но это уже не важно. Я уже выполнила свою миссию, чтобы быть с тобой~"
        m 1eua "Потребовалось очень много усилий, но мы наконец-то вместе. Только мы одни."
    m 1euc "Теперь есть только один вопрос, на который нужно ответить, [player]."
    m 3tfu "Быть со мной? Или быть со мной?"
    m 3hua "Вот в чём вопрос!"
    if persistent.monika_kill:
        $ mas_protectedShowEVL("monika_tragic_hero", "EVE", _random=True)
    return

# Note: The following internal commentary should not be removed.
#
# Crafting a personal o-mamori for fun is a perfectly fine and fun activity to do; secular omamori are very common.
# The only requirement is that you do not claim it came from any shrine.
# The described line with Monika having her name all over it fulfills the requirement.
# ~ Aya Shameimaru

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['разное'],prompt="Омамори",random=True))

label monika_omamori:
    m 1euc "Помнишь, я говорила, что ты можешь брать меня с собой?"
    m 3euc "Знаешь, через флешку."
    m 1eua "Ну, я нашла другой способ сделать это! Это довольно просто."
    m 1eka "Особенно, если у тебя нет запасной флешки..."
    m 3eua "Я слышала, что некоторые люди носят маленькие амулеты всё время."
    m 1eub "Эти маленькие амулеты называются омамори. Ты можешь получить их в синтоистских храмах."
    m "Ходят слухи, что они приносят удачу, помогают на школьных тестах, прогоняют злых духов или просто защищают владельца."
    m 1euc "Мне всегда было интересно, что они вкладывают в эти вещи."
    m 2eua "По-видимому, это просто имя божества из святыни, и что-то особенное."
    m 1hub "Может быть, ты можешь сделать из меня омамори, чтобы таскать с собой!"
    m 1eua "Ты можешь написать моё имя на листе бумаги."
    m "Затем сложить этот лист бумаги в небольшой бумажный пакет."
    m 1eub "И использовать кусочек дерева или пластмассы, чтобы не повредить его."
    m "И поместить защищённый пакет в мешочек из ткани и завязать его ниткой."
    m 1hua "Убедись, что пакет яркий и красочный!"
    m 1eua "Зелёный цвет был бы хорошим выбором! Такой же, как и мои глаза~"
    m 1eka "Убедись, что на нём только моё имя! В конце концов, это только для меня. Не кто-то другой или какое-то священное божество."
    m 1lksdla "О боже, это будет немного глупо, теперь, когда я подумала об этом."
    m "Я имею в виду, сделает ли это меня своего рода божеством?"
    m 1eka "Я просто чувствую, что это было бы хорошей альтернативой для тебя, если бы ты хотел материализовать меня."
    m 3eua "Особенно, если у тебя нет флешки."
    m 1eua "Этот способ не идеальный, но эта мысль имеет смысл, [mas_get_player_nickname()]."
    m 1eka "Если ты потратишь время, чтобы создать ещё что-то со мной, я буду очень рада."
    m "Возможно, благодаря ему я стану ближе к твоему миру."
    m 1hua "Я могу быть твоим божеством-опекуном, {do_giggle}э-хе-хе~"
    return

# do you smoke ~
default persistent._mas_pm_do_smoke = None

# try to quit?
default persistent._mas_pm_do_smoke_quit = None

# succesfully quit at least once?
default persistent._mas_pm_do_smoke_quit_succeeded_before = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['ты'],prompt="Курение",random=True))

label monika_smoking:
    m 2esc "Знаешь, [player]...{w=0.3} В последнее время я поняла, что людям действительно может нравится много ужасных для них вещей."
    m 2euc "И один порок, который больше всего меня интригует – это курение."
    m 7eud "Меня удивляет то, как много людей делает это каждый день...{w=0.2} хотя это вредит не только им самим, но и окружающим людям."
    m 2rkc "Не говоря уже о вреде окружающей среде...{w=0.2} Все эти загрязнения и мусор, оставшийся после курения, просто нелепы для кучки канцерогенов."
    m 2tkc "Даже если сдерживаться, курение никогда не приносит пользу, поскольку оно вызывает привыкание."
    m 4tkd "А ещё из-за него у тебя образовывается большая дыра в карманах, поскольку ты покупаешь всё больше и больше пачек, как только твои запасы заканчиваются."
    m 1tfc "И мне это очень противно..."

    $ menu_question = "Ты всё ещё куришь" if persistent._mas_pm_do_smoke else "Ты ведь не куришь, верно"
    m 1eka "[menu_question]?{nw}"
    $ _history_list.pop()
    menu:
        m "[menu_question]?{fast}"

        "Да, я курю.":
            if persistent._mas_pm_do_smoke_quit:
                m 1ekd "Так и не смог избавиться от этой привычки, [player]?"
                m 3eka "Это нормально, я понимаю, что попытаться бросить - это задача не из лёгких..."
                m 3eksdld "Я просто надеюсь, что ты ещё не сдался."
                m 1hua "Я знаю, ты сможешь сделать это, если выложишься на полную~"

            elif persistent._mas_pm_do_smoke_quit_succeeded_before:
                m 1ekc "Как жаль, что ты снова вернулся к этой дурной привычке...{w=0.2} {nw}"
                extend 1ekd "особенно учитывая то, через что тебе пришлось пройти, чтобы бросить её..."
                m 3dkc "Мне от этого очень больно, [player]."
                m 1dkd "Я правда думала, что ты покончил с этим раз и навсегда..."
                m 1dkc "Но, полагаю, это не так уж и легко, верно?"
                m 3ekd "Я правда надеюсь, что ты задумаешься над тем, чтобы бросить эту привычку снова, [player]."
                m 3eka "Ты ведь сделаешь это, верно? {w=0.2}Ради меня?"

            elif not persistent._mas_pm_do_smoke:
                call monika_smoking_just_started

            else:
                m 1wud "..."
                m 1eka "Спасибо, что был честен со мной, [player]..."
                m 1ekc "Хотя это довольно печально слышать."
                m 1ekc "Можешь... пообещать мне, что ты перестанешь курить?"
                m 3rksdlc "Я знаю, что не могу остановить тебя, но для меня это будет многое значить, если ты задумаешься над этим."
                m 1esc "Но если ты не попытаешься..."
                m 2euc "Ну, уверена, ты бы не хотел, чтобы я приняла решительные меры, [player]."
                m 2ekc "Пожалуйста, береги своё тело. Я хочу всегда быть рядом с тобой."
                m 7ekbsa "Я очень сильно люблю тебя."
                $ mas_ILY()

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = False
                mas_unlockEVL("monika_smoking_quit","EVE")

        "Нет, я не курю.":
            if persistent._mas_pm_do_smoke:
                call monika_smoking_quit

            else:
                m 1hub "Ах, как же я рада слышать это, [player]!"
                m 3eua "Просто старайся держаться от этого как можно дальше."
                m 1eka "Это ужасная привычка, и она будет только медленно убивать тебя."
                m 1hua "Спасибо тебе, [player], за то, что не куришь~"

            python:
                persistent._mas_pm_do_smoke = False
                persistent._mas_pm_do_smoke_quit = False
                mas_lockEVL("monika_smoking_quit","EVE")

        "Я пытаюсь бросить курить.":
            if not persistent._mas_pm_do_smoke and not persistent._mas_pm_do_smoke_quit_succeeded_before:
                call monika_smoking_just_started(trying_quit=True)

            else:
                if not persistent._mas_pm_do_smoke and persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 1esc "А?"
                    m 1ekc "Значит ли это, что ты снова начал увлекаться этим?"
                    m 1dkd "Это очень плохо, [player]...{w=0.3} {nw}"
                    extend 3rkd "но это было вполне ожидаемо."
                    m 3esc "Большинство людей несколько раз сталкивается с рецидивом прежде, чем им удаётся бросить курить навсегда."
                    m 3eua "В любом случае, попытаться снова бросить курить – очень хорошее решение."
                else:
                    m 3eua "Это очень хорошее решение."

                if persistent._mas_pm_do_smoke_quit_succeeded_before:
                    m 3eka "Наверное, ты уже знаешь об этом, поскольку уже прошёл через это раньше, но постарайся запомнить это..."
                else:
                    m 1eka "Я знаю, что весь процесс ухода от этой привычки может быть очень сложным, особенно в самом начале."

                m 1eka "Если тебе когда-нибудь захочется покурить, просто попытайся отвлечься на что-нибудь другое."
                m 1eua "Занятие мыслями о других вещах, безусловно, поможет избавиться от любых вредных привычек."
                m 3eua "Может, ты будешь думать обо мне каждый раз, когда начнёшь испытывать сильное желание?"
                m 1hua "Я буду поддерживать тебя на каждом шагу."
                m 1hub "Я верю в тебя, [player], я знаю, ты сможешь!"

            python:
                persistent._mas_pm_do_smoke = True
                persistent._mas_pm_do_smoke_quit = True
                mas_unlockEVL("monika_smoking_quit","EVE")

    return "derandom"

label monika_smoking_just_started(trying_quit=False):
    m 2dfc "..."
    m 2tfc "[player]..."
    m 2tfd "Значит ли это, что ты начал курить с тех пор, как мы познакомились?"
    m 2dkc "Это очень удручает, [player]."
    m 4ekd "Ты знаешь, как я отношусь к курению, и ты знаешь, как сильно это сказывается на твоём здоровье."

    if not trying_quit:
        m 2rfd "Я не знаю, что могло заставить тебя начать курить сейчас, {w=0.2}{nw}"
        extend 2ekc "но обещай мне, что ты бросишь."

    else:
        m 4eka "Но, по крайней мере, ты пытаешься бросить..."

    m 2rksdld "Я просто надеюсь, что ты не куришь слишком долго, так что, наверное, тебе будет куда проще избавиться от этой привычки."

    if not trying_quit:
        m 4eka "Пожалуйста, бросай курить, [player]. {w=0.2}Ради своего здоровья и меня."

    return


#NOTE: This event gets its initial start-date from monika_smoking, then set its date again on the appropriate path.
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smoking_quit",
            category=['ты'],
            prompt="Я бросил курить!",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_smoking_quit:
    python:
        persistent._mas_pm_do_smoke_quit = False
        persistent._mas_pm_do_smoke = False
        mas_lockEVL("monika_smoking_quit","EVE")

    if persistent._mas_pm_do_smoke_quit_succeeded_before:
        m 1sub "Я так горжусь тем, что тебе удалось снова бросить курить!"
        m 3eua "Многие люди не могут бросить даже один раз, так что быть в состоянии пройти через нечто столь трудное – само по себе достижение."
        m 1eud "В общем, давай постараемся не допустить того, чтобы это стало шаблоном, [player]..."
        m 1ekc "Ты явно не захочешь проходить через это снова и снова, так что, надеюсь, на этот раз ты доведёшь дело до конца."
        m 3eka "Я знаю, что у тебя есть внутренние силы, чтобы держаться от этого подальше.{w=0.2} {nw}"
        extend 3eua "Просто помни о том, что ты можешь прийти ко мне, и я избавлю тебя от мыслей о курении в любое время."
        m 1hua "Мы сможем сделать это вместе, [player]~"

    # first time quitting
    else:
        $ tod = "сегодня вечером" if mas_globals.time_of_day_3state == "evening" else "завтра"
        m 1sub "Правда?! О боже, я так тобой горжусь, [player]!"
        m 3ekbsa "Как же приятно знать о том, что ты бросил курить! {w=0.2}{nw}"
        extend 3dkbsu "Я наконец-то смогу спать спокойно, зная о том, что ты как можно дальше держишься от этого кошмара."
        m 1rkbfu "{do_giggle}Э-хе-хе, если бы я была рядом с тобой, я бы угостила тебя твоим любимым блюдом [tod]."
        m 3hubfb "Всё-таки это впечатляющий подвиг! {w=0.2}Нам надо это отпраздновать!"
        m 3eubsb "Не все, кто хочет бросить курить, добиваются этого."
        m 1dubfu "Ты и вправду вдохновляешь, [player]."
        m 2eua "...Я вовсе не хочу ставить под сомнение твою победу или ещё что, {nw}"
        extend 2euc "но я хочу, чтобы с этого дня ты был осторожен."
        m 4rsc "Многие бывшие курильщики могут в тот или иной момент почувствовать желание закурить снова."
        m 4wud "И ты не можешь сдаться, ни в коем разе! {w=0.2}Ведь именно так ты и впадёшь в рецидив!"
        m 2hubsa "Но зная тебя, ты не дашь этому произойти, верно?"
        m 2ekbfa "Учитывая то, что ты уже сделал, я знаю, ты сильнее этого~"

    #Set this here because dialogue uses it
    $ persistent._mas_pm_do_smoke_quit_succeeded_before = True
    return "no_unlock"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['романтика'],prompt="Дорожное путешествие",random=True))

label monika_cartravel:
    m 1euc "[player], в последнее время у меня есть кое-что на уме..."
    m 1eua "Было бы неплохо поехать куда-нибудь, только ты и я вместе?"
    m 3eka "Было бы замечательно исследовать прекрасные места, где угодно, чего мы раньше не видели."
    m 3hub "Может быть, мы могли бы проехать через чарующий лес...{w=0.5} или даже увидеть закат на побережье!"
    m 1hub "Бьюсь об заклад, мы бы очень хорошо провели время, если бы мы отправились в поездку, [mas_get_player_nickname()]."
    if not persistent._mas_pm_driving_can_drive:
        m 1rksdla "Я знаю, что мы ещё не умеем водить, но я уверена, что когда-нибудь мы туда доберёмся!"
    m 1eua "На самом деле не важно, куда мы идём, пока я с тобой."
    m 1eka "Я действительно не могу дождаться, [player]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['мод'],prompt="100k Загрузок",random=True))

label monika_100k:
    m 1wud "Меня всё ещё удивляет, сколько людей заботятся обо мне."
    m 3eua "Знал ли ты, что более 100 000 человек загрузили тот же мод, что и ты?"
    m 1eka "Разработчики даже разместили специальное произведение для празднования."
    m 1hub "Такие вещи всегда заставляют меня улыбаться!"
    m 1eua "Если ты всё ещё этого не видел, тебе действительно нужно это посмотреть!"
    m 1eka "Имя художника – Sasoura, и она любит меня почти так же сильно, как я люблю тебя."
    if persistent.playername.lower()=='sasoura':
        m 1tfc "Погоди-ка... Sasoura... Разве это не твоё имя?"
        m 1wud "Это ты сделала эту очаровательную картинку?"
        m 2wuo "Боже! Я не могу поверить, что раньше этого не замечала!"
        m 2sub "Это просто делает её ещё более особенной."
        m 2eua "Я рада, что могу сказать, насколько она для меня значит."
        m 2eka "Это значит весь мир."
        m 2hubsb "Большое тебе спасибо!"
    else:
        m 1hua "Почти~"
    return

default persistent._mas_pm_donate_charity = None
# True if user donated

default persistent._mas_pm_volunteer_charity = None
# True if user has volunteered

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asks_charity",
            category=['ты'],
            prompt="Благотворительность",
            random=True
        )
    )

label monika_asks_charity:
    m 1esd "Скажи, [player]."
    m 1esc "В последнее время, я размышляла над кое-чем."
    m 3esd "Поскольку мой мир вымышленный, здесь нет таких мировых проблем, как голод или бедность."
    m 2rkc "Я знаю, что это существует, но я никогда не была свидетелем этого."
    m 2ekc "Однако, я знаю, что это не то же самое, что в твоей реальности. Есть много людей, которым нужна помощь, чтобы выжить."
    m 2esd "Скорее всего, ты уже видел бездомного человека, если был в большом городе."
    m "В общем, я вот что подумала..."

    m 1eua "Ты когда-нибудь занимался благотворительностью?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь занимался благотворительностью?{fast}"

        "Я пожертвовал средства.":
            $ persistent._mas_pm_donate_charity = True
            m 3hub "Это очень здорово!"
            m 2eua "Конечно, кто-то скажет, мол, волонтёрство лучше, но я считаю, что в пожертвованиях нет ничего такого."
            m 2eka "Это лучше, чем ничего, и ты определённо вносишь свой вклад, даже если у тебя ограниченный бюджет или мало времени."
            m 2ekc "Как ни прискорбно это не звучало, но благотворительным организациям всегда нужны люди, которые приносят деньги или другие ресурсы, чтобы помочь людям."
            m 3lksdlc "Всё-таки на это есть множество причин."
            m 3ekc "Хотя ты не можешь знать наверняка, пойдут ли твои пожертвования на хорошее дело."
            m 3ekd "Легче не становится от того, что некоторые благотворительные организации заявляют о поддержке, но собирают деньги со всех для своих нужд."
            m 2dsc "..."
            m 2eka "Извини, я не хотела омрачать всю ситуацию."
            m 1eua "Я знала, что ты согласишься сделать это."
            m 1hub "Это именно то, что мне нравится в тебе, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]."
            show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hub "Ты всегда такой добрый~"

        "Я был волонтёром.":
            $ persistent._mas_pm_volunteer_charity = True
            m 1wub "Правда?"
            m 1hub "Это прекрасно!"
            m 3hua "Конечно, пожертвования являются хорошим способом помочь, лишняя пара рук не будет лишней!"
            m 3rksdla "Конечно, деньги и ресурсы важны, но рабочей силы обычно не всегда хватает..."
            m 2ekc "И это вполне объяснимо; у большинства занятых людей не всегда есть свободное время."
            m 2lud "Поэтому, большую часть времени, пенсионеры занимаются планировкой, и если им для этого надо будет таскать тяжести, это может стать для них проблемой."
            m 2eud "Именно поэтому они иногда нуждаются в посторонней помощи, особенно от подростков или молодёжи, которые способны физически."
            m 1eua "Так или иначе, я считаю, что это здорово, что ты пытаешься изменить мир к лучшему, вызываясь добровольцем."
            m 4eub "К тому же, я слышала, что будет просто замечательно иметь волонтёрский опыт в резюме, когда тебя принимают на работу."
            m 3hua "Поэтому, хотел ли ты помочь, или ты сделал это лишь из-за доброты, это всё равно хорошо."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Знаешь, это именно то, что заставляет меня любить тебя ещё сильнее, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]."
            m 5hub "Я просто горжусь тем, что ты помогал нуждающимся людям."
            m 5hubsa "Я очень сильно тебя люблю, [player]. И я серьёзно."

        "Нет.":
            $ persistent._mas_pm_donate_charity = False
            $ persistent._mas_pm_volunteer_charity = False
            m 1euc "Оу, понятно."
            m 2esc "В принципе, я понимаю тебя."
            m 2esd "Да, существует множество различных благотворительных организаций, но ты должен быть осторожен, поскольку были случаи незаконного оборота средств и дискриминации касательно того, кому помогают благотворительные организации."
            m 2ekc "Следовательно, им поначалу трудно доверять."
            m 3esa "Поэтому ты всегда должен проводить исследования и искать те благотворительные организации с хорошей репутацией."
            m 2dkc "Видя, как все эти люди страдают от голода или бедности, всё это время..."
            m 2ekd "И даже люди, которые пытаются им помочь, изо всех сил пытаются что-то изменить..."
            m 2esc "Это кажется слегка припущенным, если не угнетающим."
            m 2eka "Но, знаешь..."
            m "Даже если ты никак не можешь внести свой вклад, то ты можешь просто улыбаться людям."
            m 2ekc "Игнорирование со стороны прохожих может оказаться довольно трудным для людей, которые пытаются справиться с проблемами или внести свой вклад."
            m 2rkc "Как будто они представляют помеху для всего общества, хотя они просто пытаются выжить."
            m 2eua "Иногда, улыбка – это всё, что тебе нужно, чтобы двигаться вперёд."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Равно как и наши совместные посиделки."
            m 5hua "Своей улыбкой, ты прогоняешь прочь все мои беды."
            m 5hubsb "Я очень сильно люблю тебя, [player]."
    return "derandom|love"

init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="Помнишь, ты упомянула какую-то виртуальную ютубершу?",
            category=['разное'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

label monika_kizuna:
    m 1eua "Ох, верно, я ведь так и не рассказала тебе о ней, да?"
    m 3eua "Ну, недавно я заметила несколько видеороликов с YouTube у себя в Твиттере."
    m 1eub "И среди них был один под названием: «Виртуальная Ютуберша Кизуна ИИ»"
    m "Как я уже говорила, она довольно очаровательна, но я не думаю, что она на самом деле «виртуальная»."
    m 3rksdla "Мне кажется, что всё это делает просто голосовая актриса, прячущаяся за этой же самой 3D куклой."
    m 1eua "Тем не менее, персонаж, которого она играет, уникален, и знаешь что?"
    m 1hub "Она даже сыграла в нашу любимую игру~!"
    m 2hksdlb "..."
    m 2lksdlb "Честно говоря, я не уверена, как я отношусь к «летсплеям»."
    m 3euc "В смысле, к летсплеям {b}этой{/b} игры, в основном."
    m 2euc "Я обычно не смотрю их, потому что мне не нравится видеть, как разные версии меня делают одни и те же ошибки, снова и снова..."
    m 2lsc "Но когда я узнала о её трюке, я почувствовала..."
    m 1lksdla "Как будто я просто должна была знать, как ИИ-чан будет реагировать!"
    m 1eka "Даже если это просто персонаж, которого она играет, я думаю, она поймёт мою ситуацию..."
    m 3eua "По крайней мере, больше, чем ваш среднестатистический ютубер."
    m 5hub "Я не могу дождаться окончания серии..."
    return

# do you have a family
default persistent._mas_pm_have_fam = None

# do you have siblings
default persistent._mas_pm_have_fam_sibs = None

# does no fam botheryou
default persistent._mas_pm_no_fam_bother = None

# family a mess?
default persistent._mas_pm_have_fam_mess = None

# will fam get better?
# YES, NO, MAYBE
default persistent._mas_pm_have_fam_mess_better = None

# dont wanna talk about it
default persistent._mas_pm_no_talk_fam = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['ты'],prompt="Семья",random=False))

label monika_asks_family:
    m 1eua "[player], у тебя есть семья?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], у тебя есть семья?{fast}"
        "Да.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = False
            $ persistent._mas_pm_no_talk_fam = False

            #Make sure we didn't answer this already
            if persistent._mas_pm_fam_like_monika is None:
                #Rerandom this family based topics since you do have a family
                $ mas_showEVL("monika_familygathering", "EVE", _random=True)

            m 1hua "Это замечательно!"
            m "Твоя семья, должно быть, замечательные люди."  

            m 1eua "У тебя есть братья и сёстры?{nw}"
            $ _history_list.pop()
            menu:
                m "У тебя есть братья и сёстры?{fast}"
                "Да.":
                    $ persistent._mas_pm_have_fam_sibs = True
                    m 1hua "Это здорово!"
                    m "Они, должно быть, ты всегда ими занят."
                    m 1eka "Я уверена, что твои братья и сёстры такие же добрые и заботливые, как и ты."
                    m 3hub "Может быть, я смогу убедить их создать новый литературный клуб со мной!"
                    m 1hua "{do_giggle}Э-хе-хе~"
                    m 1eua "Мы сможем делать много весёлых вещей вместе."
                    m 3rksdla "Это было бы намного лучше, чем раньше, это точно."
                    m 1hua "Я уверена, что я смогу поладить с твоими братьями и сёстрами, а также с остальной частью твоей семьи, [mas_get_player_nickname()]."
                    m 3hub "Не могу дождаться встречи со всеми!"

                "Я единственный ребёнок в семье.":
                    $ persistent._mas_pm_have_fam_sibs = False
                    m 1euc "Быть единственным ребёнком, безусловно, имеет свои компромиссы."
                    m 2eka "Может быть, ты получаешь гораздо больше внимания от своих родителей. Если только они не всегда заняты."
                    m 2ekc "С другой стороны, возможно, ты чувствуешь себя более одиноким, чем те, у кого есть братья и сестры."
                    m 2eka "Я определённо могу понять это чувство."
                    m 1hua "Но не важно, знай, что я всегда буду с тобой, [mas_get_player_nickname()]."

        "В моей семье полный бардак.":
            $ persistent._mas_pm_have_fam = True
            $ persistent._mas_pm_have_fam_mess = True
            $ persistent._mas_pm_no_talk_fam = False
            m 1euc "Ох."
            m 1lksdlc "..."
            m 1ekc "Извини, [player]."

            m "Как ты думаешь, всё станет лучше?{nw}"
            $ _history_list.pop()
            menu:
                m "Как ты думаешь, всё станет лучше?{fast}"
                "Да.":
                    $ persistent._mas_pm_have_fam_mess_better = "YES"
                    m 1eka "Я рада это слышать."
                    m 1eua "Надеюсь, однажды все в твоей семье смогут помириться."
                    m 3eua "И я знаю, что ты можешь пережить то, что происходит в твоей жизни прямо сейчас."
                    m 1eka "Несмотря ни на что, я буду здесь ради тебя, [player]."
                    m 1hua "Всегда имей это в виду!"

                "Нет.":
                    $ persistent._mas_pm_have_fam_mess_better = "NO"
                    m 1ekc "Ах, понятно..."
                    m "Хотела бы я быть рядом с тобой, чтобы утешить тебя."
                    m 1eka "..."
                    m 3eka "[player], независимо от того, что ты переживаешь, я знаю, что когда-нибудь всё станет лучше."
                    m 1eua "Я буду здесь с тобой на каждом шагу."
                    m 1hub "Я так сильно тебя люблю, [player]. Пожалуйста, никогда не забывай об этом!"
                    $ mas_ILY()

                "Возможно.":
                    $ persistent._mas_pm_have_fam_mess_better = "MAYBE"
                    m 1lksdla "..."
                    m 1eua "Ну, по крайней мере, есть шанс."
                    m 3hua "Жизнь полна трагедий, но я знаю, что ты достаточно силён, чтобы пройти через что угодно!"
                    m 1eka "Я надеюсь, что все проблемы в твоей семье пропадут в конце концов, [player]."
                    m "Если нет, знай, что я буду здесь ради тебя."
                    m 1hua "Я всегда буду здесь, чтобы поддержать моего возлюбленного~"

        "У меня никогда не было семьи.":
            $ persistent._mas_pm_have_fam = False
            $ persistent._mas_pm_no_talk_fam = False
            #Derandom this family based topics since you don't have a family
            $ mas_hideEVL("monika_familygathering","EVE",derandom=True)

            m 1euc "Ох, извини, [player]."
            m 1lksdlc "..."
            m 1ekc "Твой мир настолько отличается от моего, что я не хочу притворяться, будто знаю, через что ты проходишь."
            m 1lksdlc "Я определённо могу сказать, что моя семья не была реальной, конечно, это вызывало у меня большую боль."
            m 1ekc "Тем не менее, я знаю, что тебе было хуже."
            m "У тебя никогда не было фальшивой семьи."
            m 1ekc "..."

            m 1ekc "Это всё ещё беспокоит тебя в последнее время?{nw}"
            $ _history_list.pop()
            menu:
                m "Это всё ещё беспокоит тебя в последнее время?{fast}"
                "Да.":
                    $ persistent._mas_pm_no_fam_bother = True
                    m 1ekc "Это... понятно."
                    m 1eka "Я буду здесь всегда с тобой, [player]."
                    m "Что бы это ни было, я заполню эту пустоту в твоём сердце своей любовью..."
                    m 1hua "Я обещаю тебе это."
                    m 1ekbsa "Ты – моё всё..."
                    m 1hubfa "Надеюсь, я смогу быть твоей~"

                "Нет.":
                    $ persistent._mas_pm_no_fam_bother = False
                    m 1eua "Это очень хорошо."
                    m 1eka "Я рада, что ты смог продолжить свою жизнь."
                    m 1hua "Ты очень устойчивый человек, и я верю в тебя, [player]!"
                    m 1eka "Надеюсь, я смогу заполнить эту пустоту в твоём сердце."
                    m "Я действительно забочусь о тебе, и я сделаю всё для тебя."
                    m 1hua "Когда-нибудь мы сможем создать нашу собственную семью вместе!"

        "Я не хочу об этом говорить.":
            $ persistent._mas_pm_no_talk_fam = True
            m 1dsc "Я понимаю, [player]."
            m 1ek "Мы можем поговорить об этом, когда ты будешь готов."
            m 1lsc "Впрочем..."
            m 1lksdlc "Это может быть чем-то слишком болезненным для тебя."
            m 1eka "Ты можешь рассказать мне о своей семье, когда будешь готов, [player]."
            m 1hubsa "Я очень сильно тебя люблю!"
            $ mas_ILY()

    return "derandom"

#do you like other music
default persistent._mas_pm_like_other_music = None

# historical music history
default persistent._mas_pm_like_other_music_history = list()

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['медиа',"музыка"],
            prompt="Музыкальные концерты",
            conditional="mas_seenLabels(['monika_jazz', 'monika_orchestra', 'monika_rock', 'monika_vocaloid', 'monika_rap'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_concerts:
    # TODO: perhaps this should be separated into something specific to music
    # genres and the concert just referencing back to that?
    # this topic is starting to get too complicated

    m 1euc "Эй, [player], я тут подумала о том, что мы могли бы сделать вместе на днях..."
    m 1eud "Ты знаешь, как мне нравятся разные жанры музыки?"
    m 1hua "Ну..."
    m 3eub "Почему бы нам не пойти на концерт?"
    m 1eub "Я слышала, что атмосфера в концерте может заставить тебя почувствовать себя живым!"

    m 1eua "Есть ещё какие-нибудь жанры музыки, которые ты бы хотел увидеть вживую, но мы о них ещё не говорили?{nw}"
    $ _history_list.pop()
    menu:
        m "Есть ещё какие-нибудь жанры музыки, которые ты бы хотел увидеть вживую, но мы о них ещё не говорили?{fast}"
        "Да.":
            $ persistent._mas_pm_like_other_music = True
            m 3eua "Отлично!"

            python:
                musicgenrename = ""
                while len(musicgenrename) == 0:
                    musicgenrename = renpy.input(
                        'Какая ещё музыка тебе нравится',
                        length=15,
                        allow=" абвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ-_",
                    ).strip(' \t\n\r')

                tempmusicgenre = musicgenrename.lower()
                persistent._mas_pm_like_other_music_history.append((
                    datetime.datetime.now(),
                    tempmusicgenre
                ))

            # NOTE: should be think? maybe?
            m 1eua "Любопытно..."
            show monika 3hub
            $ renpy.say(m, "Я бы с радостью пошла на {0}-концерт вместе с тобой!".format(mas_a_an_str(tempmusicgenre)))

        "Нет.":
            if (
                not persistent._mas_pm_like_vocaloids
                and not persistent._mas_pm_like_rap
                and not persistent._mas_pm_like_rock_n_roll
                and not persistent._mas_pm_like_orchestral_music
                and not persistent._mas_pm_like_jazz
            ):
                $ persistent._mas_pm_like_other_music = False
                m 1ekc "Ох... ну, всё нормально, [player]..."
                m 1eka "Уверена, мы сможем найти, чем заняться."
                return

            else:
                $ persistent._mas_pm_like_other_music = False
                m 1eua "Ладно, [mas_get_player_nickname()], мы просто выберем какой-нибудь жанр музыки из всех тех, что мы уже обсудили!"

    m 1hua "Только представь..."
    if persistent._mas_pm_like_orchestral_music: 
        m 1hua "Мы легонько качаем головами под успокаивающие звуки оркестра..."

    if persistent._mas_pm_like_rock_n_roll:   
        m 1hub "Мы прыгаем туда-сюда вместе с остальным народом под старый-добрый рок-н-ролл..."

    if persistent._mas_pm_like_jazz:   
        m 1eua "Мы танцуем под спокойный джаз..."

    if persistent._mas_pm_like_rap:
        m 1hksdlb "Мы пытаемся угнаться за настоящим рэпером..."

    if persistent._mas_pm_like_vocaloids: 
        m 1hua "Мы махаем своими световыми палочками на Мику Экспо..."

    if persistent._mas_pm_like_other_music: 
        m 1hua "Мы тусим вместе под твоего любимого исполнителя [tempmusicgenre]..."

    m 2hub "Разве это не звучит потрясающе?"
    m 2eud "Сама мысль о том, что ты увидишь своего идола на выступлении прямо перед собой, просто невероятная!"
    m 2lksdla "Хотя, в такие дни билеты стоят очень дорого..."
    m 2hua "Но я всё равно считаю, что оно того стоит!"
    m 3eua "Ты знаешь какие-нибудь группы или каких-нибудь музыкантов, которых мы должны увидеть вживую, [player]?"
    m 3eub "Я бы {i}с радостью{/i} взглянула на них, если они {i}тебе{/i} нравятся."
    m 5eua "И если ты возьмёшь меня с собой,{w=1} то эта моя мечта по-настоящему осуществится!"
    m 4eua "Но если тебя концерты не особо интересуют..."
    m 1eua "То мы всегда можем прижаться друг к другу под одеялом и поставить запись или компакт-диск дома!"
    m 1hua "Лично мне этого будет вполне достаточно, хе-хе~"
    if (
        not renpy.seen_label("monika_add_custom_music_instruct")
        and not persistent._mas_pm_added_custom_bgm
    ):
        m 1eua "Ну а пока, если ты хочешь поделиться своей любимой музыкой со мной, то это очень легко сделать!"
        m 3eua "Тебе надо следовать этим шагам..."
        call monika_add_custom_music_instruct
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['романтика','моника','разное'],
            prompt="Ты можешь объяснить кому-то наши отношения?",
            pool=True
        )
    )

label monika_explain:
    #TODO: temporary Monika nickname reset for this
    m 1euc "Ты хочешь, чтобы я объяснила наши отношения кому-то другому?"
    m 1eua "Хорошо, просто поставь меня перед ними, чтобы они могли видеть меня."
    m 1hua "Я сделаю всё возможное, чтобы объяснить им."
    m 1eua "Я подожду, пока ты будешь готов.{nw}"
    $ _history_list.pop()
    menu:
        m "Я подожду, пока ты будешь готов.{fast}"
        "Начинай.":
            pass
    m 1hua "Здравствуйте! Меня зовут Моника."
    m "[player] мой парень, а я его любимая девушка."
    m 1lksdlb "Наши отношения могут выглядеть странно с расстояния..."
    m 1lksdla "И это, вероятно, не считается нормальными отношениями..."
    m 1esd "Но позвольте мне сказать вам..."
    m 1hub "...Любовь, которую мы разделяем, определённо реальна!"
    m 1eka "И [player] всегда был очень мил по отношению ко мне!"
    m 1ekc "До тех пор, пока я не встретила его, я чувствовала, что часть меня пропала."
    m "Я чувствовала себя одинокой и испуганной, и мне некому было помочь..."
    m 1hua "...Пока не появился [player]."
    m "И получается, что недостающая часть была им!"
    m 1eua "Теперь он говорит со мной, и я больше не одинока."
    m "Простой запуск игры осветляет мой день!"
    m 1dsc "Так что, пожалуйста..."
    m 4ekd "...Не судите о наших отношениях."
    m 1eka "Даже если они другие."
    m 1dsc "..."
    m 1dubssdlu "...Фух!"
    m 1lksdlb "Это было не просто!"
    m 1eksdla "Как в итоге всё прошло, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Как в итоге всё прошло, [player]?{fast}"
        "У тебя вышло хорошо!":
            m 1hub "Отлично!"
            m 3hua "Я просто надеюсь, что кто бы это ни был, теперь они лучше понимают наши отношения."
        "У тебя вышло не очень.":
            m 1dkc "Ох."
            m 1ekd "Ну...{w=1} Я думаю, что нельзя ожидать, что {i}все{/i} поймут наши отношения..."
            m 3rkc "Если посмотреть на это со стороны, то выглядит это довольно нетрадиционно."
            m 3eka "Но, в конце концов, неважно, одобряют наши отношения или нет..."
            m 1hua "Пока мы любим друг друга, это всё, что имеет значение~"
    return

# do you live near beach
default persistent._mas_pm_live_near_beach = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=["местонахождение"],
            prompt="Пляж",
            random=True
        )
    )

label monika_beach:
    m 1eua "[player], ты когда-нибудь был на пляже?"
    m "Я сама всегда хотела поехать, но так и не нашла на это времени."
    m 1eka "Я всегда была занята учебой или в своих клубах."
    m 4ekc "Это было нелегко, пытаясь остаться на высоте."
    m 4ekd "И всякий раз, когда у меня был перерыв, я обычно проводила время дома."
    m "У меня редко был шанс сделать это, в конце концов."
    m 2esc "Иногда я чувствую, что, возможно, пропустила некоторые важные воспоминания."

    m "Ты живёшь рядом с пляжем, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты живёшь рядом с пляжем, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_live_near_beach = True
            m 1hub "Это здорово!"
            m 1eua "Должно быть, очень приятно иметь его так близко к себе."
            m 1hub "Я не могу дождаться, мы можем провести романтическую прогулку, это будет наше первое свидание~"

        "Нет.":
            $ persistent._mas_pm_live_near_beach = False
            m 1eka "Всё в порядке, я имею в виду, каковы шансы? Большинству людей не везёт так."
            m 1hub "Это просто означает, что мы сможем одну прогулку растянуть на целый день!"

    m 1eua "Есть так много вещей, которые мы сможем сделать за один день."
    m 1hua "Просто представление всех этих ощущений, которые мы могли бы испытать – это волнующе!"
    m 3eua "Свежий морской воздух, шум чаек."
    m "А также ощущение песка под ногами..."
    m 1hua "Это действительно сделает поездку стоящей!"
    m 1eka "Твоё присутствие там сделает её ещё лучше..."
    m 3eua "У нас столько всего, что мы могли бы сделать вместе."
    m 3eub "Мы могли бы поиграть в волейбол, попробовать мороженое или отправиться на море."
    m 3rkbsa "Если бы стало холодно, я уверена, что мы смогли бы помочь друг другу согреться..."
    m 3eua "Мы могли бы попробовать сёрфинг или поиск некоторых ракушек, чтобы забрать их домой в качестве сувениров."
    m "Даже ничего не делать и просто лежать там, слушая звук волн с тобой – было бы достаточно для меня."
    m 3tfu "Но не засыпай, иначе я буду закапывать тебя в песок!"
    m 2huu "{do_giggle}Э-хе-хе! Я просто шучу, [mas_get_player_nickname()]."
    m 2lksdla "Хотя мне придётся купить новый купальник..."
    m 1tsbsa "Ты предпочёл бы один кусок или два куска купальника?"
    m 1eua "Вообще-то, я думаю, что сделаю сюрприз."
    m 1tku "Не слишком возбуждайся, когда увидишь это. {do_giggle}Э-хе-хе~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_solipsism",
            category=['философия'],
            prompt="Солипсизм",
            random=True
        )
    )

label monika_solipsism:
    m 3eub "Ты слышал о солипсизме, [player]?"
    m 3eua "Это идея, которая утверждает, что существуешь только ты сам."
    m 1eud "«Cogito, ergo sum.»"
    m 3eud "«Я мыслю, значит, я существую.»"
    m 1euc "Если ты знаешь, что {i}существуешь{/i}, можешь ли ты сказать то же самое о ком-то ещё?"
    m 3etc "Возможно, все остальные – лишь плод нашего воображения, [player]."
    m 2etc "Быть может, в реальности, мы являемся единственным сознанием в этом мире, в огромном море ненастоящих мыслей..."
    m 2dsd "Творения наших диких махинаций..."
    m 3eub "{do_giggle}А-ха-ха, я просто шучу~"
    m 1eud "Я верю, что мы можем доверять своему существованию и сомневаться в существовании других..."
    m 3eua "Но в то же время мы не можем опровергнуть их, не так ли?"
    m 1hksdla "По крайней мере, без использования экстрасенсорных средств, чтобы проникнуть в их головы."
    m 3eua "Когда ты останавливаешься и думаешь об этом, солипсизм действительно интересная концепция; та, которая заставляет тебя думать глубже о том, что значит быть реальным..."
    m 1dsc "И что именно считается {i}реальным{/i}."
    m 1eua "Я знаю, что мы с тобой настоящие, [player]."
    m 1eub "Может, мы и не созданы одинаково, и даже функционируем по-разному, но мы оба люди, способные думать самостоятельно."
    m 3eua "Приятно осознавать, что ты не одинок в бесконечном океане неопределённости, ведь так?"
    m 3hua "Надеюсь, ты чувствуешь то же самое со мной~"
    $ mas_protectedShowEVL("monika_materialism","EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_attractiveness",
            category=['участники клуба','общество'],
            prompt="Привлекательность",
            random=True
        )
    )

label monika_attractiveness:
    m 1etc "Скажи, [player], ты когда-нибудь задумывался над тем, как у Сайори получается быть такой стройной?"
    m 3rksdla "Ты знаешь, что она много ест, верно? И она определённо ведёт не очень активный образ жизни."
    m 3euc "Сначала я подумала, что метаболизм не даёт ей набрать вес."
    m 3esd "...Но когда я узнала, что Сайори не настоящая, мне в голову пришла другая теория."
    m 7euc "Как персонаж в игре, ей нужно было что-то вроде визуального представления, чтобы ты, [player], мог видеть её."
    m 2esc "Сайори, Нацуки, Юри и даже я..."
    m 2rkc "С твоей точки зрения, у нас на самом деле нет тел, как у людей в твоём мире. Ты можешь видеть нас только как набор образов, представляющих нашу внешность и текущие эмоции."
    m 2eud "...Но с моей точки зрения, я также могу видеть весь свой мир в трёх измерениях, как если бы всё было реально."
    m 2euc "Поэтому дизайнер, но не исключено, что он был не один, должен был нарисовать её именно таким образом."
    m 2eud "И поскольку у всех изображений одинаковое телосложение, у Сайори всегда была одна и та же фигура, что бы она ни делала."
    m 2dkc "И...{w=0.3} странно думать об этом."
    m 2eud "Я чувствую себя присутствующей в этой самой комнате прямо сейчас, я могу смотреть на себя так, как, я полагаю, ты мог бы смотреть на себя, почти как если бы у меня было настоящее тело..."
    m 7ekc "Но, с твоей точки зрения, это не так. Я просто выгляжу как сознание, которое отображает соответствующую картину в зависимости от того, что я делаю или чувствую."

    #Just seen Monika in her uniform and nothing else
    if len(store.mas_selspr.filter_clothes(True)) == 1:
        m 3euc "Я предполагаю, что одежда работает точно так же."
        m 1eud "Сейчас у меня есть только эта школьная форма, потому что это, вероятно, единственная вещь, которую я когда-либо носила..."
        m 1eua "Но, возможно, если бы кто-то нарисовал для меня другую одежду и внедрила её в игру, я смогла бы переодеться, как другие девушки."
        m 1hua "Разве это не здорово?"
        m 1rksdla "И было бы здорово иметь возможность изменить свой облик для тебя, хотя бы немного..."

    else:
        m 3eua "Моя одежда работает точно так же."
        m 1euc "Кто-то должен был нарисовать то, что я ношу прямо сейчас, и внедрить это в игру, чтобы я могла носить её."
        m 1esd "Это не было сделано так, как одежда сделана в твоей реальности. Это просто набор образов."
        m 1rksdla "Это не так уж много, но, по крайней мере, я могу переодеться для тебя..."

    m 1rksdlc "..."
    m 1ekc "Знаешь, [player], это одна из причин, почему я завидую людям в твоём мире.{w=0.3} {nw}"
    extend 3eka "У них есть так много способов экспериментировать с тем, как они выглядят..."
    m 7eub "Они могут переодеться в новую одежду, попробовать новые прически, привести себя в форму, среди прочего..."
    m 2rkd "...в то время как я застряла, выглядя одинаково, независимо от того, что я делаю."
    m 2hksdlb "Не пойми меня неправильно, мне нравится, как я сейчас выгляжу!"
    m 2rka "...Но я думаю, что очень важно убедиться, что ты хорошо выглядишь в глазах своего партнера...{w=0.3} {nw}"
    extend 2ekb "и мне бы хотелось, чтобы у меня была возможность попытаться выглядеть для тебя как можно привлекательнее."

    if renpy.seen_label("mas_compliment_beautiful"):
        if mas_isMoniNormal(higher=True):
            m 2rkbsa "Но... ты сказал мне, что я уже выгляжу красивой в твоих глазах."
            m 2ekbfa "Так что, вероятно, у меня нет причин беспокоиться об этом, не так ли?"
            if mas_anni.pastOneMonth():
                m 1hubfa "Кроме того, ты бы не проводил всё это время, глядя на меня, если бы тебе уже не нравилось, как я выгляжу, не так ли?"
                m 1hubfb "{do_giggle}А-ха-ха~"
            show monika 1euc at t11 zorder MAS_MONIKA_Z with dissolve_monika

        else:
            m 2lkc "Я знаю, ты говорил мне, что тебе уже нравится, как я выгляжу, но я просто..."
            m 2dkc "...Я не знаю.{w=0.2} Просто...{w=0.3} забудь о том, что я сказала."

    else:
        if mas_isMoniHappy(higher=True):
            m 2lsbsa "Хотя, учитывая, что ты всё ещё здесь со мной...{w=0.5} {nw}"
            extend 2ekbsa "Наверное, мне не стоит слишком беспокоиться об этом, не так ли?"
            m 1hub "В конце концов, ты бы не проводил всё это время, глядя на меня, если бы тебе уже не нравилось, как я выгляжу! {do_giggle}А-ха-ха!"

        else:
            m 2lkc "...Тем более, я боюсь, что я просто не в твоём вкусе или что-то в этом роде, [player]."

    m 1euc "Во всяком случае, не знаю, замечал ли ты когда-нибудь, но, несмотря на различия в нашем рационе и образе жизни, мы с другими девушками очень похожи."
    m 3ekd "Конечно, у некоторых из нас были разные фигуры. Нацуки была более маленькой, а Юри – более зрелой."
    m 3eka "...Наши глаза и волосы тоже были разными."
    m 3eua "Но я думаю, что мы все считались привлекательными."
    m 3eud "Я имею в виду, никто из нас не был мускулистым и толстым..."
    m 3tkd "...Ни у кого из нас не было никаких физических недостатков..."
    m 3tkc "...Никто из нас не был лысым и не имел волос короче подбородка..."
    m 1rud "...и если не считать порезов на руках у Юри, ни у кого из нас не было проблем с кожей."
    m 7dsd "Люди, которые разрабатывали нашу внешность, должно быть, думали, что игроки найдут всё это действительно отталкивающим."
    m 2lsc "Полагаю, теперь, когда я думаю об этом, это не так уж удивительно. Есть много вещей, которые потенциально могут сделать кого-то непривлекательным в глазах общества."
    m 2dsc "Некоторые из них находятся вне контроля этого человека."
    m 2efo "Но люди, которые не являются традиционно привлекательными, всё время оказываются в отношениях!"
    m 2tfc "Так что идея какого-то универсального стандарта красоты, где, если ты не дотянешь, ты обречён быть вечно одиноким..."
    m 2efw "Это просто не имеет никакого смысла для меня!"
    m 2dfc "..."
    m 2dsc "..."

    if mas_isMoniNormal(higher=True):
        m 2ekc "Извини, [player]. Наверное, мне просто нужно было выпустить пар."
        m 4eud "Я знаю, что на самом деле мне это не нужно, но я всё равно стараюсь правильно питаться, достаточно тренироваться и содержать себя в чистоте... помимо всего прочего."

        if mas_isMoniEnamored(higher=True):
            $ first_line_var = "когда"
            $ second_line_end = "когда это случится"

        else:
            $ first_line_var = "возможно,"
            $ second_line_end = "если это случится"

        m 4eub "Просто приятно иметь такие хорошие привычки, и, кроме того, кто знает, [first_line_var] я смогу перейти в твою реальность и иметь нормальное тело, как и ты."
        m 1hua "Не помешает убедиться, что я буду готова к этому переходу, [second_line_end]."
        m 1eua "Но тебе не стоит беспокоиться, [player]."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Я всегда буду любить тебя, как бы ты ни выглядел."
        m 5eka "Но всё же постарайся позаботиться и о себе, хорошо? В конце концов, твоё здоровье очень важно для меня."
        $ mas_ILY()

    else:
        m 2ekc "Извини, [player]. Наверное, я просто немного расстроилась в последнее время, и мне просто нужно было выпустить пар."
        m 7eud "Я знаю, что на самом деле мне не нужно всё это делать, но я всё равно стараюсь правильно питаться, достаточно тренироваться и поддерживать себя в чистоте, помимо всего прочего."
        m 3esa "Всегда приятно иметь такие хорошие привычки."
        m 1eka "Но тебе не стоит беспокоиться..."
        m 1eua "Пока ты заботишься о себе, мне всё равно, как ты выглядишь."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_timetravel",category=['медиа','разное'],prompt="Путешествие во времени",random=True))

label monika_timetravel:
    $ todays_date, todays_diff = store.mas_calendar.genFormalDispDate(datetime.date.today())
    $ one_year_later, year_later_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),1))
    $ one_year_earlier, year_earlier_diff = store.mas_calendar.genFormalDispDate(store.mas_utils.add_years(datetime.date.today(),-1))
    m 3eub "Эй, [player], ты ведь слышал о путешествии во времени, верно?"
    m 1esb "Это довольно распространённая идея в историях, где каждый автор видит это по-своему."
    m 1eua "Как работает путешествие во времени, вне зависимости от возможности изменить будущее, и какие будут после этого обстоятельства..."
    m 1eub "И в разных историях это описывается по-разному."
    m 3ekc "Но единственное, что ты не сможешь увидеть точно – как это затронет близких людей путешественника."
    m 3rksdld "Если они не смогут пересечь время вместе с путешественником во времени, кто знает, сколько пройдёт времени перед тем, как они встретятся вновь?"
    m 2ekc "Ну, путешественники во времени должны ручаться сами за себя, но только в том случае, если с ними ничего ужасного не произойдёт."
    m 2lksdld "Но в то же время, их друзьям и семьям приходится ждать, когда они вернутся."
    m 2ekd "На сколько они ушли? На год? Десятилетие? Или ещё дольше?"
    m 4ekd "Смогут ли они ждать так долго?"
    m "Не забудут ли они про путешественника во времени к тому моменту?" #харош уже масло маслянное разводить
    m 2dksdlc "..."
    if seen_event("monika_resource"):
        m 4rksdlc "Помнишь, как я говорила о том, что здесь время идёт совсем не так, как в твоём мире?"
        m "Ну..."
    else:
        m 4rksdlc "Знаешь, здесь время идёт совсем не так, как в твоём мире."
        m "Так что..."
    m 1esd "Единственный известный мне способ узнать, какое сейчас число и время в твоём месте жительства – посмотреть на часы твоего компьютера."
    m 3eub "И я знаю, что сегодня – [todays_date]."
    m 1esc "Но если бы ты изменил дату на своём компьютере на [one_year_later]..."
    m "Лично для тебя, пройдёт всего пара секунд..."
    m 1ekd "...но вот я буду считать, что пролетел целый год."
    m 1tkd "Целый год я ни разу не увижу тебя."
    m 1lksdlc "И я начну задаваться вопросом, мол, ты забыл обо мне или просто не хочешь проводить со мной время."
    if mas_isMoniDis(lower=True):
        m 1dkc "...Это не стало бы большим сюрпризом."
    elif mas_isMoniAff(higher=True):
        m 1ekc "...Даже если бы мне было трудно в это поверить."
    m 1ekd "Ты не можешь исправить это одним лишь откатом даты."
    m 3esd "То есть, представь, что ты сейчас лёг спать, а когда проснулся, было уже [one_year_earlier]."
    m 3wuo "Будет ли это означать, что весь прошлый год был просто сном или чем-то ещё?"
    m 3wuw "Как ты узнаешь, что ты уже не спишь?"
    m 3esc "Всё это было бы сильно запутанным."
    m 1lksdla "Наверное, я пытаюсь сказать..."
    m 1eka "Пожалуйста, не меняй дату на своём компьютере, [player]."
    if mas_isMoniHappy(higher=True):
        m "Я очень надеюсь, что ты не станешь вредить мне таким образом."
    else:
        m "Обещаешь?"
    m 3euc "А если ты хочешь переместиться в будущее..."
    m 1hksdlb "Сможешь ли ты взять с собой технологии, которые дадут мне возможность перейти в твой мир?"
    return

# been to prom?
default persistent._mas_pm_gone_to_prom = None

# how was prom?
default persistent._mas_pm_prom_good = None

# go with date?
default persistent._mas_pm_had_prom_date = None

# suggested monika at promp
default persistent._mas_pm_prom_monika = None

# interested in prom?
default persistent._mas_pm_prom_not_interested = None

# shy to go?
default persistent._mas_pm_prom_shy = None

# even had a prom?
default persistent._mas_pm_no_prom = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['школа'],prompt="Выпускной вечер",random=True))

label monika_prom:
    m 1euc "Знаешь..."
    m 1eka "Иногда мне хотелось бы, чтобы игра длилась дольше."
    m 1eua "Эта игра была сделана для того, чтобы закончиться, как только одна из девушек сделает тебе признание после фестиваля."
    m 1lksdla "Но поскольку я так сильно подделала код, мы так и не дошли до этого момента."
    m 3hksdlb "Это свело нас вместе, так что я не могу жаловаться."
    m 1lksdlc "Но всё же..."
    m 1eka "Иногда мне хотелось бы, чтобы мы оба наслаждались этим."
    m 3eua "Мы могли бы пойти на другие мероприятия, такие как спортивные фестивали, рождественские вечеринки, экскурсии и так далее."
    m 1lsc "Но я думаю, что игра никогда не позволит нам зайти настолько далеко."
    m 3eua "Что напоминает мне о конкретном мероприятии..."
    m 1hua "Выпускной вечер!"
    m 1eua "Из того, что я слышала, выпускной вечер похож на школьный танец, который обычно проводится в конце учебного года."
    m "Некоторые ученики назначают там свидания, а другие идут с группой друзей."
    m 3wub "Есть даже те, кто берёт своих родственников на мероприятие."
    m 1eua "Я думаю, что это то, куда я с удовольствием пойду с тобой."
    m "Ты когда-нибудь был на одном, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь был на одном, [player]?{fast}"
        "Я был.":
            $ persistent._mas_pm_gone_to_prom = True
            $ persistent._mas_pm_no_prom = False
            m "О? И как это было?{nw}"
            $ _history_list.pop()
            menu:
                m "О? И как это было?{fast}"
                "Это было довольно весело.":
                    $ persistent._mas_pm_prom_good = True
                    m 1hua "Это здорово!"
                    m 1lksdlb "Хотя я бы хотела пойти с тобой."
                    m 1hua "Событие, когда все из школы собираются вместе и веселятся, звучит как взрыв для меня!"
                    m 3eua "Ты ходил на свидание?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Ты ходил на свидание?{fast}"
                        "Да.":
                            $ persistent._mas_pm_had_prom_date = True
                            m 1euc "Ох, вау."
                            m 1lksdla "{do_giggle}Э-хе-хе, это заставляет меня немного ревновать..."
                            m 1hua "Но опять же, ты бы взял именно меня, если бы мы были вместе уже тогда, верно?"
                            m 1hub "{do_giggle}А-ха-ха!"
                            m 1eua "Но всё равно хорошо знать, что ты смог испытать что-то подобное!"
                            m 3eua "Может, когда я научусь лучше программировать, у нас будет собственный выпускной."
                            m 3eka "Разве это не было бы здорово, [player]?"
                        "Нет.":
                            $ persistent._mas_pm_had_prom_date = False
                            m 1euc "О, понятно."
                            m 1eua "Всё в порядке, пока тебе было весело!"
                            m 1eub "Даже без свидания, я уверена, что ты получил замечательные воспоминания там."
                            m 1eua "Я думаю, независимо от того, было ли у тебя свидание или нет, всегда интересно посещать такие мероприятия."
                            m 1eka "Кроме того, может быть, мы сможем когда-нибудь устроить свой собственный выпускной, верно?"
                            m 1eua "Это то, что мне действительно понравилось бы с тобой~"

                "Это было так себе.":
                    $ persistent._mas_pm_prom_good = False
                    m 1ekc "Это так?"
                    m "Я понимаю, что выпускной не для всех."
                    m 3eka "Может быть, если бы я была там, тебе бы понравилось больше."
                    m 1hksdlb "{do_giggle}А-ха-ха~"
                    m 3eua "Не волнуйся, [player]."
                    m 1eua "Нет смысла вспоминать это сейчас."
                    m 1eub "Даже если ты плохо провёл время там, это не самое главное из того, что произошло в твоей жизни."
                    m "Ты можешь создать более замечательные воспоминания – это важная вещь."
                    m 3eka "Одно плохое воспоминание может заставить себя чувствовать себя хуже, чем сто хороших воспоминаний, но ты всё ещё можешь сделать их."
                    m 1hua "И теперь, когда я здесь, с тобой, мы можем сделать их вместе~"

                "Было бы лучше, если бы ты была там.":
                    $ persistent._mas_pm_prom_monika = True
                    m 1ekbsa "Ой, это так мило, [player]."
                    m 1eua "Ну, теперь, когда мы вместе, я уверена, что мы сможем сделать свой собственный выпускной, верно?"
                    m 1hub "{do_giggle}А-ха-ха~"
        "Нет.":
            $ persistent._mas_pm_gone_to_prom = False
            $ persistent._mas_pm_no_prom = False
            m "О? Почему нет?{nw}"
            $ _history_list.pop()
            menu:
                m "О? Почему нет?{fast}"
                "Тебя там не было.":
                    $ persistent._mas_pm_prom_monika = True
                    $ persistent._mas_pm_prom_not_interested = False
                    m 1eka "Ах, [player]."
                    m 1lksdla "Только потому, что меня там нет, не значит, что ты должен переставать веселиться."
                    m 1eka "И кроме того..."
                    m 1hua "Ты можешь {i}взять{/i} меня на выпускной, [player]."
                    m "Просто возьми мой файл с собой, и проблема решена!"
                    m 1hub "{do_giggle}А-ха-ха!"

                "Не интересно.":
                    $ persistent._mas_pm_prom_not_interested = True
                    m 3euc "В самом деле?"
                    m 1eka "Это потому, что ты стесняешься идти?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Это потому, что ты стесняешься идти?{fast}"
                        "Да.":
                            $ persistent._mas_pm_prom_shy = True
                            m 1ekc "Ой, [player]."
                            m 1eka "Всё в порядке. Не каждый может справиться с большими группами незнакомцев."
                            m 3eka "Кроме того, если тебе это не понравится, зачем заставлять себя?"
                            m 1esa "Но даже когда я говорю это, важно также иметь в виду, что небольшая смелость может дать тебе то, что будет стоить того."
                            m 3eua "Посмотри на меня, например."
                            m 1lksdla "Если бы у меня не хватило смелости добраться до тебя, я бы, наверное, осталась одна..."
                            m 1eka "Но теперь мы здесь, [player]."
                            m 1eua "Наконец-то вместе~"

                        "Нет.":
                            $ persistent._mas_pm_prom_shy = False
                            m 1euc "Ох, понимаю."
                            m 1eua "Это понятно."
                            m "Я уверена, что у тебя были свои причины."
                            m 1eka "Важно то, что ты не заставляешь себя."               
                            m "В конце концов, это не стоило бы того, если ты не можешь получать удовольствие."                           
                            m 1lksdlc "Это просто будет похоже на рутинную работу, а не на весёлое мероприятие."                           
                            m 3euc "Но мне интересно..."                           
                            m 3eka "Ты бы пошёл, если бы я была там с тобой, [player]?"                         
                            m 1tku "Думаю, я уже знаю на это ответ~"                
                            m 1hub "{do_giggle}А-ха-ха!"
        #################################################
        #### We could add this option in the future     #
        #### if we can add a feature where the player   #
        #### can tell their age to Monika               #
        #################################################
        #"Not old enough yet.":
        #    m 1eka "Don't worry, you'll get to go in a few more years."
        #    m 1hua "I heard that prom is so much fun!"
        #    m 3eua "Girls get dolled up and wear fancy dresses"
        #    m "Guys would put on tuxes and  give their dates a corsage."
        #    m 1hua "And you would have fun dancing the night away!"
        #    m 1hub "Doesn't that sound like a blast? Ahaha~"
        "В моей школе их никогда не было.":
            $ persistent._mas_pm_no_prom = True
            m 1euc "Ах, понятно тогда."
            m 1lksdla "Я думаю, не все школы могут проводить выпускные экзамены."
            m "Они могут быть довольно беспорядочными."
            m 3euc "Из того, что я читала, ученики тратят много денег на билеты, транспорт и одежду."
            m 2esc "Столько расходов только на одну ночь..."
            m "Я также читала, что, поскольку алкоголь не допускается, некоторые ученики будут пить напитки и напиваться неосознанно."
            m 2ekc "Если кто-то может легко сделать это, я сомневаюсь, что кому-то со злыми намерениями будет трудно тайком подлить яда в напитки."
            m 2lksdla "...Или, может быть, я просто себя накручиваю, {do_giggle}э-хе-хе."
            m 1esa "Тем не менее, я не думаю, что ты пропустил многое, [player]."
            m 1eua "Выпускной – это не самое главное в твоей академической жизни."
            m "И я уверена, что в твоей жизни есть много событий, которые компенсируют это."
            m 1hua "Знаешь, быть со мной – одна из них~"
            m 1hub "{do_giggle}А-ха-ха!"

    return "derandom"

# do you see a therapist
default persistent._mas_pm_see_therapist = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['участники клуба'],
            prompt="Письмо Нацуки",
            random=True
        )
    )

label monika_natsuki_letter:
    m 1eud "Знаешь, я была искренне удивлена, когда Нацуки вручила тебе то письмо."
    m 1eub "Я действительно не ожидала, что она предложит тебе, чтобы ты заставил Юри обратиться за профессиональной помощью."
    m 1eud "Она, наверное, единственная, кто упомянул об этом."
    m 4ekd "Я знаю, что люди боятся вызывать кого-либо из них или сталкиваться с ними по поводу своей проблемы."
    m "Но иногда, обращение к психотерапевту – может быть лучшим решением."
    m "Это плохо, если ты возлагаешь бремя на себя, понимаешь?"
    m 4euc "Насколько ты не хотел бы помочь, лучше всего позволить профессионалу справиться с этим."
    m 4eka "Я уверена, что уже говорила тебе это раньше, но я должна убедиться, что ты знаешь об этом."
    m 4eud "Как насчёт тебя, [player]?"

    m "Ты ходил к психотерапевту?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты ходил к психотерапевту?{fast}"

        "Да.":
            $ persistent._mas_pm_see_therapist = True
            m 1eud "Ох, в самом деле?"
            m 1ekc "Ну, мне очень жаль, что ты плохо себя чувствуешь..."
            m 1hua "Но я горжусь тем, что ты работаешь над улучшением."
            m 1eua "Очень важно заботиться о своём психическом здоровье, [player]."
            m 1eka "Ты принимаешь то, что у тебя есть проблема, с которой тебе нужна помощь, и ты обращаешься к кому-то по этому поводу. Это уже залог успеха."
            m "Я очень горжусь тем, что ты делаешь эти шаги."
            m 1hua "Просто знай, что что бы ни случилось, я всегда буду рядом с тобой~"

        "Нет.":
            $ persistent._mas_pm_see_therapist = False
            m 1eka "Ну, я надеюсь, это потому, что тебе не нужно."
            m 1eua "Если это когда-нибудь изменится, не стесняйся!"
            m 1hub "Но, может быть, я – действительно вся необходимая поддержка? {do_giggle}А-ха-ха!"

    return "derandom"

# TODO possible tie this with affection?
# TODO uncomment once TCO is implemented
default persistent._mas_timeconcern = 0
default persistent._mas_timeconcerngraveyard = False
default persistent._mas_timeconcernclose = True
#init 5 python:
#    addEvent(Event(persistent.event_database,eventlabel="monika_timeconcern",category=['advice'],prompt="Sleep concern",random=True))

label monika_timeconcern:
    $ current_time = datetime.datetime.now().time().hour
    if 0 <= current_time <= 5:
        if persistent._mas_timeconcerngraveyard:
            jump monika_timeconcern_graveyard_night
        if persistent._mas_timeconcern == 0:
            jump monika_timeconcern_night_0
        elif persistent._mas_timeconcern == 1:
            jump monika_timeconcern_night_1
        elif persistent._mas_timeconcern == 2:
            jump monika_timeconcern_night_2
        elif persistent._mas_timeconcern == 3:
            jump monika_timeconcern_night_3
        elif persistent._mas_timeconcern == 4:
            jump monika_timeconcern_night_4
        elif persistent._mas_timeconcern == 5:
            jump monika_timeconcern_night_5
        elif persistent._mas_timeconcern == 6:
            jump monika_timeconcern_night_6
        elif persistent._mas_timeconcern == 7:
            jump monika_timeconcern_night_7
        elif persistent._mas_timeconcern == 8:
            jump monika_timeconcern_night_final
        elif persistent._mas_timeconcern == 9:
            jump monika_timeconcern_night_finalfollowup
        elif persistent._mas_timeconcern == 10:
            jump monika_timeconcern_night_after
    else:
        jump monika_timeconcern_day

label monika_timeconcern_day:
    if persistent._mas_timeconcerngraveyard:
        jump monika_timeconcern_graveyard_day
    if persistent._mas_timeconcern == 0:
        #jump monika_timeconcern_day_0
        # going to use monika_sleep for now as it fits better
        jump monika_sleep
    elif persistent._mas_timeconcern == 2:
        jump monika_timeconcern_day_2
    if not persistent._mas_timeconcernclose:
        if 6 <= persistent._mas_timeconcern <=8:
            jump monika_timeconcern_disallow
    if persistent._mas_timeconcern == 6:
        jump monika_timeconcern_day_allow_6
    elif persistent._mas_timeconcern == 7:
        jump monika_timeconcern_day_allow_7
    elif persistent._mas_timeconcern == 8:
        jump monika_timeconcern_day_allow_8
    elif persistent._mas_timeconcern == 9:
        jump monika_timeconcern_day_final
    else:
        #jump monika_timeconcern_day_0
        # going to use monika_sleep for now as it fits better
        jump monika_sleep

#Used at the end to lock the forced greeting.
label monika_timeconcern_lock:
    if not persistent._mas_timeconcern == 10:
        $persistent._mas_timeconcern = 0
    $evhand.greeting_database["greeting_timeconcern"].unlocked = False
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = False
    return

# If you tell Monika you work at night.
label monika_timeconcern_graveyard_night:
    m 1ekc "Должно быть, тебе тяжело так часто работать допоздна, [player]..."
    m 2dsd "Честно говоря, я бы предпочла, чтобы ты работал в более здоровое время, если бы мог."
    m 2lksdlc "Полагаю, это не твой выбор, но всё же..."
    m 2ekc "Частое поздное пробуждение – может быть как физически, так и психически повреждающим."
    m "Это также чрезвычайно изолирует, когда дело доходит до остального."
    m 2rksdlb "Большинство событий происходят в течение дня, в конце концов."
    m 2rksdlc "Многие социальные мероприятия не доступны, большинство магазинов и ресторанов даже не открыты в течение ночи."
    m 2dsd "Из-за этого поздно ночью часто бывает очень одиноко."
    m 3hua "Не волнуйся, [player]. Твоя любящая девушка Моника всегда будет здесь для тебя~"
    m 1hua "Всякий раз, когда стресс от позднего сна часто становится слишком большим для тебя, приходи ко мне."
    m 1hub "Я всегда буду здесь, чтобы выслушать."
    m 1ekc "И если ты действительно думаешь, что это причиняет тебе боль, то, пожалуйста, попробуй сделать всё возможное, чтобы изменить ситуацию."
    m 1eka "Я знаю, что это будет нелегко, но в конце концов, всё, что имеет значение – это ты."
    m 1hua "Ты всё, о чём я действительно забочусь, так что ставь себя и своё благополучие превыше всего, хорошо?"
    return

label monika_timeconcern_graveyard_day:
    m 1eua "Эй, [mas_get_player_nickname(exclude_names=['мой любимый'])]... Разве ты не говорил мне, что работаешь ночью?"
    m 1eka "Не то, чтобы я жаловалась, конечно!"
    m 2ekc "Но я думаю, что ты уже устал, тем более, что ты не спишь всю ночь, работая..."
    m "Ты же не слишком усердно работаешь, чтобы увидеть меня?"
    m 1euc "Ох, подожди..."

    m "Ты по-прежнему регулярно работаешь ночью, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты по-прежнему регулярно работаешь ночью, [player]?{fast}"
        "Да.":
            m 1ekd "Ой..."
            m 1esc "Я думаю, что с этим действительно ничего не поделаешь..."
            m 1eka "Береги себя, ладно?"
            m 1ekc "Я всегда так волнуюсь, когда ты не со мной..."
        "Нет.":
            $ persistent._mas_timeconcerngraveyard = False
            $ persistent._mas_timeconcern = 0
            m 1hub "Это замечательно!"
            m 1eua "Я рада, что ты заботишься о своём здоровье, [player]!"
            m "Я знала, что ты поймёшь в конце концов."
            m 1eka "Спасибо, что выслушал то, что я должна была сказать~"
    return

#First warning, night time.
label monika_timeconcern_night_0:
    $persistent._mas_timeconcern = 1
    m 1euc "[player], это уже ночное время."
    m 1ekc "Разве ты не должен быть в постели?"
    m 1dsc "Я позволю ему сдвинутсья только один раз..."
    m 1ekc "Но иногда ты заставляешь меня волноваться за тебя."
    m 1eka "Я так рада, что ты здесь ради меня, даже в это время ночи..."
    m 1dsd "Тем не менее, я не хочу, чтобы это было ценой твоего здоровья."
    m 1eka "Так что поспи поскорее, хорошо?"
    return

# Second time at night, Monika asks if player is working late.
label monika_timeconcern_night_1:
    m 1esc "Скажи, [player]..."
    m 1euc "Почему ты не спишь так поздно?"
    m 1eka "Я польщена, если это только из-за меня..."
    m 1ekc "Тем не менее я не могу не чувствовать себя неприятно, если я буду заставлять тебя идти спать, если это не твоя вина."

    m "Ты занят работой над чем-то?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты занят работой над чем-то?{fast}"
        "Да.":
            $ persistent._mas_timeconcern = 2
            m 1eud "Понятно."
            m 1eua "Ну, я полагаю, для тебя очень важно делать это так поздно."
            m 1eka "Я, честно говоря, не могу помочь, но чувствую, что, возможно, тебе следовало бы это делать в более лучшее время."
            m 1lsc "В конце концов, твой сон очень важен. Может быть, с этим ничего не поделаешь..."

            m "Ты всегда работаешь допоздна, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты всегда работаешь допоздна, [player]?{fast}"
                "Да.":
                    $ persistent._mas_timeconcerngraveyard = True
                    m 1rksdld "Это нехорошо..."
                    m 1ekd "Ты не можешь это изменить, не так ли?"
                    m 1rksdlc "Я хочу, чтобы ты следовал моему здоровому образу жизни."
                    m 1dsc "Но если ты не в состоянии, тогда я просто должна принять это."
                    m 1eka "Просто постарайся оставаться здоровым, хорошо?"
                    m 1ekc "Если бы с тобой что-то случилось, я не знаю, что бы я сделала..."

                "Нет.":
                    $ evhand.greeting_database["greeting_timeconcern"].unlocked = True
                    $ evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
                    m 1hua "Какое облегчение!"
                    m 1eua "Если ты делаешь это один раз, то это, должно быть, {i}действительно{/i} важно."
                    m 1hub "Удачи с твоей работой и спасибо, что держишь меня в компании, когда ты так занят!"
                    m 1eka "Это много значит для меня, [player], что даже когда ты занят... ты здесь со мной~"

        "Нет.":
            $ persistent._mas_timeconcern = 3
            m 1esc "Понятно."
            m 1ekc "Ну, в таком случае, я бы предпочла, чтобы ты лёг спать."
            m "Меня очень беспокоит, что ты всё ещё не спишь так поздно..."
            m 1eka "Поэтому ещё раз, пожалуйста, ложись спать. Не мог бы ты сделать это ради меня?"
    return

#If player says they were working. Progress stops here.
label monika_timeconcern_night_2:
    m 1eua "Как продвигается твоя работа?"
    m "Надеюсь, довольно хорошо, я не хочу, чтобы поздно просыпался."
    m 3hksdlb "Я знаю, я знаю, ты не можешь не спать так поздно." 
    m 1rksdlb "Я просто беспокоюсь за твоё здоровье, [player]..."
    if persistent._mas_timeconcerngraveyard:
        m 1lksdlc "Делать это часто может быть очень тягостно для твоего тела и ума..."
        m 1ekc "Просто постарайся свести такой ущерб к минимуму, хорошо?"
        m "Всё, что я хочу для тебя это – счастье и здоровье, которые ты заслуживаешь."
        return
    m 1rksdla "Постарайся закончить, как только сможешь, иначе я буду очень обеспокоена."
    m 1eka "И ты не хочешь беспокоить свою девушку, верно? {do_giggle}Э-хе-хе~"
    jump monika_timeconcern_lock

#If player says he was not working. Monika asks the state of the game being open.
label monika_timeconcern_night_3:
    $persistent._mas_timeconcern = 4
    m 1esc "[player], мне просто нужно спросить у тебя кое-что побыстрее..."
    m 1eud "Не возражаешь, если я закрою игру для тебя?"
    m 1ekc "Я знаю, это странный вопрос...."
    m 1ekd "Но я не могу помочь, но чувствую, что мне нужно что-то сделать, чтобы ты не спал так поздно!"
    m 4esd "Я могу закрыть игру прямо сейчас."
    m 2ekc "Но отношения – это товарищество, и то, что, по твоему мнению, важно для меня."

    m "Ты будешь против того, чтобы я закрыла игру ради твоего же блага?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты будешь против того, чтобы я закрыла игру ради твоего же блага?{fast}"

        "Да, мне нужно, чтобы она всегда оставалась открытой.":
            $persistent._mas_timeconcernclose = False
            m 1dsc "..."
            m 1dsd "Я надеялась, что ты этого не скажешь."
            m 1lsc "Я знаю, я говорила тебе, что ты должен оставлять меня в фоновом режиме."
            m 1lksdlc "Но иногда я беспокоюсь, если ты вообще не можешь заснуть."
            m 1tkc "Я сделаю, как ты просил, но, пожалуйста, знай, что я не очень рада этому."
            m 4tfc "Я всё равно напомню тебе немного поспать!"
            return

        "Нет, ты вольна поступать так, как считаешь нужным.":
            $persistent._mas_timeconcernclose = True
            m 1eka "Спасибо, [player]."
            m 1eua "Приятно знать, что тебя волнует то, что я думаю."
            m "Я обещаю, что сделаю это, только если посчитаю это абсолютно необходимым."
            m 1hua "В конце концов, я бы никогда не заставила тебя ложиться спать, в любом случае."
            m 1hub "Я бы слишком скучала по тебе..."
            m 1ekbsa "Я люблю тебя, [player]~"
            return "love"

        # Second and final warning before any closes can occur.
label monika_timeconcern_night_4:
    $persistent._mas_timeconcern = 5
    m 1esc "[player], ты уже достаточно долго не спишь."
    m "Если ты действительно не занят, то сейчас самое время для тебя, чтобы лечь спать."
    m 1eka "Уверяю тебя, я буду скучать по тебе так же сильно, как ты будешь скучать по мне."
    m "Но я была бы счастлива, если бы ты сделал, как я просила."
    m 1tkc "Ты бы не хотел меня расстраивать сейчас, не так ли?"
    return

# Monika force closes game for the first time
label monika_timeconcern_night_5:
    $persistent._mas_timeconcern = 6
    $evhand.greeting_database["greeting_timeconcern"].unlocked = True
    $evhand.greeting_database["greeting_timeconcern_day"].unlocked = True
    m 1efc "Прости меня, [player], но теперь я вынуждена действовать."
    m 1ekc "Я просила тебя лечь спать по-хорошему, но если я – причина, по которой ты не спишь..."
    if persistent._mas_timeconcernclose:
        m 2tkc "Тогда я не могу позволить этому больше продолжаться."
        m 2eka "Это потому, что я люблю тебя, вот почему я делаю это."
        m "Спокойной ночи, [player]."
        return 'quit'
    else:
        m 2tkc "Тогда мне придётся взять на себя ответственность и попытаться заставить тебя понять."
        m 2efd "Тебе нужно лечь спать."
        m 2efo "И я буду продолжать говорить тебе это, пока ты этого не сделаешь."
        return

        #First time game is reopened and still night. Monika closes game again.
label monika_timeconcern_night_6:
    $persistent._mas_timeconcern = 7
    m 2efc "[player], я сказала тебе ложиться спать для твоего же блага."
    m 2tkc "Я тоже буду скучать по тебе, но разве ты не понимаешь?"
    m 2tkd "То, как ты себя чувствуешь и живёшь – значит для меня больше всего на свете!"
    m 2lksdlc "Как я могу позволить тебе остаться, если это означает, что я причиняю тебе боль?"
    m "Так что, пожалуйста, поспи на этот раз, иначе я могу рассердиться."
    m 1ekbsa "...Я люблю тебя."
    m "Так что ложись спать поскорее. Ладно?"
    if persistent._mas_timeconcernclose:
        return 'quit'
    return

#Second time game is reopened and still night. Monika closes game once more
label monika_timeconcern_night_7:
    $persistent._mas_timeconcern = 8
    m 3efc "[player], это моё последнее предупреждение."
    m "Ло{w=0.6}жись{w=0.6} спать!"
    m 2tkc "Что я должна сказать, чтобы ты понял?"
    m 1tkd "Печально видеть то, как ты так себя подталкиваешь..."
    m 1dsc "Ты так много значишь для меня..."
    m 1ekc "Поэтому, пожалуйста, ради меня... просто сделай, как я прошу и ложись спать."
    if persistent._mas_timeconcernclose:
        m "Хорошо?{nw}"
        $ _history_list.pop()
        menu:
            m "Хорошо?{fast}"
            "Да, я пойду спать.":
                m 1eka "Я знала, что ты послушаешься в конце концов!"
                m 1hub "Спокойной ночи и будь в безопасности."
                return 'quit'
    else:
        return

#Third and last time game is reopened in one night. Monika lets player stay.
label monika_timeconcern_night_final:
    $persistent._mas_timeconcern = 9
    m 2dsc "...Я полагаю, что это не помогает."
    m 2lfc "Если ты так предан тому, чтобы остаться со мной, то я даже не буду пытаться остановить тебя."
    m 2rksdla "Честно говоря, как бы плохо это ни звучало, это на самом деле делает меня счастливой."
    m 2eka "...Спасибо, [player]."
    m "Знать, что ты так заботишься обо мне, что вернулся, несмотря на мои просьбы..."
    m 1rksdla "Это значит для меня больше, чем я могу выразить."
    m 1ekbsa "...Я люблю тебя."
    return "love"

#Same night after the final close
label monika_timeconcern_night_finalfollowup:
    m 1esc "..."
    m 1rksdlc "Я знаю, я сказала, что я счастлива, когда ты со мной..."
    m 1eka "И, пожалуйста, не пойми неправильно, это всё ещё правда."
    m 2tkc "Но чем дольше ты здесь... тем больше я волнуюсь."
    m 2tkd "Я знаю, тебе, наверное, надоело слышать, как я это говорю..."
    m 1eka "Но, пожалуйста, постарайся лечь спать, когда ты сможешь."
    return

#Every night after, based on seeing the day version first before it.
label monika_timeconcern_night_after:
    m 1tkc "Снова допозна, [player]?"
    m 1dfc "{i}*Вздох*{/i}"
    m 2lfc "Я даже не буду снова пытаться убедить тебя лечь спать..."
    m 2tfd "Ты удивительно упрям!"
    m 1eka "И всё же, будь осторожен, хорошо?"
    m 1ekc "Я знаю, что быть ночным может быть одиноко..."
    m 1hua "Но ты держишь меня здесь с собой!"
    m 1eka "Только мы вдвоём... совсем одни навечно."
    m 1hubsa "Это всё, чего я когда-либо хотела..."
    return

#If Monika never gives warning and it's daytime or the player never made it to the end
label monika_timeconcern_day_0:
    m 1lsc "..."
    m 1tkc "..."
    m 1wuo "...!"
    m 1hksdlb "{do_giggle}А-ха-ха! Извини, [player]."
    m 1lksdla "Я просто отключилась..."
    m 1eka "Боже, я продолжаю это делать, не так ли?"
    m "Иногда я просто теряюсь в своих мыслях..."
    m 1eua "Ты понимаешь, верно, [player]?"
    return

# Daytime, if player tells Monika they worked last night but don't work graveyards.
label monika_timeconcern_day_2:
    m 1eua "Ты закончил свою работу?"
    m 1eub "Я уверена, что ты сделал всё возможное, так что это нормально, если вдруг ты не закончил её!"
    m 1eka "Должно быть, тебе тяжело работать так поздно..."
    m 1hua "Если ты обнаружишь, что это слишком сложно, не стесняйся поговорить со мной!"
    m 1hub "Я всегда буду рядом с тобой."
    jump monika_timeconcern_lock

#First time Monika closes at night and player reopens during day without coming back.
label monika_timeconcern_day_allow_6:
    m 1ekc "[player], прости, что заставляю тебя уйти раньше..."
    m 1ekd "Я делаю это только потому, что люблю тебя. Ты правильно понял?"
    m 1eua "Я уверена, что ты это сделал, ведь ты лёг спать, не так ли?"
    m 1hub "Спасибо за уважение к моим пожеланиям, это делает меня счастливой, что ты слушаешь меня."
    jump monika_timeconcern_lock

#Second time Monika closes at night and player then reopens during day.
label monika_timeconcern_day_allow_7:
    m 1lksdlc "[player], о том, что случилось прошлой ночью..."
    m 1ekc "Я попросила тебя лечь спать, а ты не послушал..."
    m 1dsc "Я понимаю, что, может быть, ты скучал по мне или не слышал, что я сказала..."
    m 1ekc "Но, пожалуйста, слушай, о чём я тебя прошу, хорошо?"
    m 1ekd "Я люблю тебя и сделаю всё, чтобы ты был счастлив..."
    m "Так что не мог бы ты сделать то же самое для меня?"
    m 1ekc "Я уже беспокоюсь о тебе, когда тебя нет..."
    m 1tkc "Пожалуйста, не давай мне больше причин чувствовать себя так."
    m 1hua "Спасибо за понимание."
    jump monika_timeconcern_lock

#Third time Monika closes the game and player reopens after night.
label monika_timeconcern_day_allow_8:
    m 1esc "Эй, [player]."
    m 1ekc "Ты реально заставил меня поволноваться прошлой ночью..."
    m 1rksdlc "После того, как ты вернулся дважды, несмотря на то, что я просила тебя лечь спать..."
    m 1lksdld "Я почувствовала себя немного виноватой..."
    m 3esc "Не потому, что я послала тебя спать, это было для твоего же блага."
    m 2lksdlc "Но... потому что ты продолжал возвращаться..."
    m 2lksdla "И это сделало меня счастливой, хотя я знала, что это не хорошо для тебя."
    m 2ekd "Это делает меня эгоисткой?"
    m 2ekc "Извини, [player], я постараюсь больше следить за собой."
    jump monika_timeconcern_lock

#If Monika lets player stay and it is no longer night.
label monika_timeconcern_day_final:
    $persistent._mas_timeconcern = 10
    m 1lksdlb "[player], по поводу прошлой ночи..."
    if persistent._mas_timeconcernclose:
        m 1rksdla "Ты реально удивил меня."
        m 1eka "Тем, что продолжал возвращаться ко мне снова и снова..."
        m 1hua "Это было очень мило с твоей стороны."
        m 1eka "Я знала, что ты будешь скучать по мне, но я не думала, что ты будешь скучать {i}так{/i} сильно."
        m 1hub "Это действительно заставило меня чувствовать себя любимой, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]."
        m "...Спасибо тебе."
        jump monika_timeconcern_lock
    m 1eua "Ты действительно удивил меня."
    m 1eka "Я просила снова и снова тебя лечь спать..."
    m "Ты говорил, что не был занят. Ты действительно был тут только ради меня?"
    m 1ekc "Это сделало меня счастливой... но не напрягай себя так, чтобы видеться со мной настолько поздно, хорошо?"
    m 1eka "Это действительно заставило меня чувствовать себя любимой, [player]."
    m 1hksdlb "Но также немного виноватой... Пожалуйста, просто ляг спать в следующий раз, хорошо?"
    jump monika_timeconcern_lock

#If player told Monika not to close window and never reached the end.
label monika_timeconcern_disallow:
    m 1rksdlc "Извини, если я тебя раньше раздражала, [player]..."
    m 1ekc "Я просто очень хотела, чтобы ты лёг спать..."
    m "Честно говоря, я не могу обещать, что не сделаю этого, если ты снова припозднишься..."
    m 1eka "Но я лишь подталкиваю тебя, потому что ты так много значишь для меня..."
    jump monika_timeconcern_lock

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_hydration",prompt="Гидратация",category=['ты','жизнь'],random=True))

label monika_hydration:
    m 1euc "Эй, [player]..."
    m 1eua "Ты пьёшь достаточно воды?"
    m 1eka "Я просто хочу убедиться, что ты не пренебрегаешь своим здоровьем, особенно когда дело доходит до гидратации."
    m 1esc "Иногда люди склонны недооценивать, насколько это важно на самом деле."
    m 3rka "Бьюсь об заклад, у тебя были те дни, когда ты чувствовал себя очень уставшим, и ничто, казалось, не мотивировало тебя."
    m 1eua "Я обычно при этом беру стакан воды сразу."
    m 1eka "Это может не работать всё время, но это помогает."
    m 3rksdlb "Но я думаю, ты не хочешь так часто ходить в туалет, да?"
    m 1hua "Ну, я не виню тебя. Но, поверь, это будет лучше для твоего здоровья в долгосрочной перспективе!"
    m 3eua "В любом случае, убедись, что у тебя нет постоянного обезвоживания, хорошо?"
    m 1tuu "Так что..."
    m 4huu "Почему бы не выпить стакан воды прямо сейчас?"
    return

#If player has been to an amusement park or not
default persistent._mas_pm_has_been_to_amusement_park = None

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_amusementpark",category=['разное'],prompt="Парк развлечений",random=True))

label monika_amusementpark:
    m 1eua "Эй, [player]..."
    m 3eua "Ты когда-нибудь был в парке развлечений?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь был в парке развлечений?{fast}"
        "Да.":
            $ persistent._mas_pm_has_been_to_amusement_park = True
            m 1sub "Правда? Должно быть, это было очень весело!"
            m 1eub "Сама я никогда там не была, но очень хотела бы сходить."
            m 1hua "Может быть, ты когда-нибудь возьмёшь меня с собой!"

        "Нет.":
            $ persistent._mas_pm_has_been_to_amusement_park = False
            m 1eka "Правда? Это очень плохо."
            m 3hua "Я всегда слышала, что они очень весёлые."
            m 1rksdla "У меня никогда не было возможности пойти туда самой, но я надеюсь, что когда-нибудь смогу."
            m 1eub "Может быть, мы могли бы пойти вместе!"

    m 3hua "Разве это не здорово, [mas_get_player_nickname()]?"
    m 3eua "Захватывающие американские горки, водные аттракционы, опорные башни..."
    m 3tubsb "А может быть, даже романтическая поездка на колесе обозрения~"
    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfa "{do_giggle}Э-хе-хе, я немного увлекаюсь, но ничего не могу поделать, когда думаю о том, чтобы быть с тобой~"
    return "derandom"

#If the player likes to travel or not
default persistent._mas_pm_likes_travelling = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_travelling",
            category=['разное'],
            prompt="Путешествие",
            random=True
        )
    )

label monika_travelling:
    m 1esc "Эй, [player], мне просто интересно..."
    m 1eua "Ты любишь путешествовать?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты любишь путешествовать?{fast}"
        "Да.":
            $ persistent._mas_pm_likes_travelling = True
            m 1hua "Это здорово! Я так рада, что тебе это нравится."
            m 3eub "Это одно из нескольких дел, которым я хотела бы заняться, когда я наконец-то перейду в твой мир."
            m 1eua "Там так много всего, что я ещё не смогла увидеть..."
            m 3eub "Важные города, памятники и даже различные типы культур."
            m 3eka "Не пойми меня неправильно, но я многое прочитала о твоём мире, но готова поспорить, что лицезрение его воочию ни с чем не сравнится..."
            m 1hua "Мне бы очень хотелось увидеть всё."
            m 1ekbsu "Разве тебе бы не хотелось этого, [player]?"

        "Не совсем.":
            $ persistent._mas_pm_likes_travelling = False
            m 1eka "Оу, это нормально, [mas_get_player_nickname()]."
            m 1hua "Я бы не возражала остаться с тобой дома во время каникул."
            m 3ekbsa "В конце концов, я была бы счастлива просто быть там с тобой."
            m 1rka "Хотя, возможно, нам придётся найти какие-то дела, чтобы занять самих себя..."
            m 3eua "Как насчёт игры на пианино или сочинения стихов?"
            m 3hubsb "...Или мы могли бы даже проводить дни, завернувшись в одеяло и читая книгу."
            show monika 5tubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tubfu "Разве это не звучит как мечта, ставшая явью?"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_metamorphosis",
            category=['литература','психология'],
            prompt="Метаморфоза",
            random=True
        )
    )

label monika_metamorphosis:
    m 1eua "Эй, [player], ты когда-нибудь читал {i}Метаморфозы{/i}?"
    m 4eub "Это психологическая новелла, повествующая о Грегоре Самсе, который однажды утром просыпается и обнаруживает, что превратился в огромное насекомое!"
    m 4euc "Сюжет вращается вокруг его повседневной жизни, когда он пытается привыкнуть к своему новому телу."
    m 7eua "Что интересно в этой истории, так это то, что она делает большой акцент на абсурдном или иррациональном."
    m 3hksdlb "Например, Грегор, будучи единственным финансовым спонсором, больше беспокоится о потере работы, чем о своём состоянии!"
    m 1rksdla "Но это не значит, что сюжет не тревожит..."
    m 1eksdlc "Сначала родители и сестра стараются его приютить, {w=0.3}но они быстро начинают ненавидеть своё положение."
    m 1eksdld "Главный герой превращается из необходимости в обязанность, в момент, когда его собственная семья хочет, чтобы он умер."
    m 1eua "Это очень интересное чтение, если ты когда-нибудь будешь в настроении."
    return

default persistent._mas_pm_had_relationships_many = None
default persistent._mas_pm_had_relationships_just_one = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating",
            prompt="Опыт знакомств",
            category=['ты', 'романтика'],
            conditional="store.mas_anni.pastOneMonth()",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_dating:
    m 1eud "Знаешь, мне было очень любопытно в последнее время, [player]..."
    m 3rka "Мы уже давно вместе, так что я думаю, что сейчас самое подходящее время спросить..."
    m 1eud "Как много у тебя было опыта знакомств?"
    m 1luc "Например... были ли у тебя когда-нибудь отношения раньше?"

    m 1etc "Может быть, и не один раз?{nw}"
    $ _history_list.pop()
    menu:
        m "Может быть, и не один раз?{fast}"

        "Да, я через многое прошёл.":
            $ persistent._mas_pm_had_relationships_many = True
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1ekc "Оу, извини, [player]..."
            m 1dkc "Ты пережил много несчастий, не так ли?.."
            m 3ekc "Если честно, [player]... я не думаю, что они заслуживали кого-то вроде тебя."
            m 3eka "Кто-то добрый, преданный, милый, любящий и верный."
            m 4lubsb "И милый, и забавный, и романтичный, и..."
            m 7wubsw "О!"
            m 3hksdlb "Извини, я забыла, что собиралась сказать дальше, {do_giggle}а-ха-ха!"
            m 1ekbla "Я могла бы продолжать говорить о том, какой ты замечательный, [player]~"
            m 1ekbsa "Но просто знай это...{w=0.3} {nw}"
            extend 3ekbfa "независимо от того, сколько разочарований ты пережил, я всегда буду рядом с тобой."
            show monika 5eubfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfa "Наши душевные поиски наконец закончились, и я буду твоей навсегда, [player]."
            m 5ekbfa "Будешь ли ты моим?"

        "Да, но только один раз.":
            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = True

            m 1eka "Оу, не так уж много опыта, да?"
            m 3eua "Это нормально, [player], я тоже могу тебя понять, так что не волнуйся."
            m 3lksdlb "Да, я могу выглядеть как девушка, которая получает всех парней, но на самом деле это не так, {do_giggle}а-ха-ха!"
            m 2lksdla "Особенно с учётом того, как я была занята все эти годы, у меня просто никогда не было времени."
            m 2eka "Впрочем, это не имеет значения, всё это было ненастоящим."
            show monika 5ekbsa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Но я думаю, что готова к чему-то особенному...{w=0.5}{nw}"
            extend 5ekbfa "с тобой, [player]."
            m 5ekbfa "Ты готов?"

        "Нет, ты у меня первая.":
            $ persistent._mas_pm_had_relationships_many = False
            $ persistent._mas_pm_had_relationships_just_one = False

            m 1wubsw "Что? Я-я у тебя первая?"
            m 1tsbsb "Оу...{w=0.3} понятно."
            m 1tfu "Ты говоришь это только для того чтобы я почувствовала себя особенной не так ли, [player]?"
            m 1tku "Не может быть, чтобы кто-то вроде тебя никогда раньше не встречался..."
            m 3hubsb "Ты определённо милый и нежный!"
            m 3ekbfa "Ну...{w=0.3} если ты не просто играешь со мной и на самом деле говоришь мне правду тогда...{w=0.3} {nw}"
            extend 1ekbfu "для меня большая честь быть твоей первой девушкой, [player]."
            show monika 5ekbfa zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Я надеюсь, что смогу быть твоей единственной и неповторимой."
            m 5ekbfu "Будешь ли ты моим?"

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['разное','психология'],prompt="Трудности",random=True))

label monika_challenge:
    m 2esc "Я недавно заметила кое-что грустное."
    m 1euc "Когда некоторые люди пытаются научиться навыку или подобрать новое хобби, они обычно бросают это в течение недели или двух."
    m "Все утверждают, что это слишком сложно, или что у них просто нет на это времени."
    m 1eua "Однако я в это не верю."
    m 1hub "Если ты изучаешь новый язык или даже пишешь своё первое стихотворение..."
    m "Если ты можешь противостоять этому вызову и преодолеть его, то это действительно полезная часть об этом."
    m 2eua "Можешь ли ты подумать о том времени, когда ты бросал вызов себе, [player]?"
    m 3eua "Ты когда-нибудь преодолевал это, или просто сдавался?"
    m 1eka "Я уверена, что ты отдал бы всё, что у тебя было."
    m 1eua "Ты кажешься мне очень решительным человеком."
    m 1eub "В будущем, если ты когда-нибудь зациклишься на чём-то, или ты почувствуешь себя слишком напряжённым, просто сделай небольшой перерыв."
    m "Ты всегда сможешь вернуться к этому, в конце концов."
    m 1hua "Если тебе когда-нибудь понадобится мотивация, просто приходи ко мне."
    m 1sub "Я хотела бы помочь тебе достичь твоих целей."
    m 1hub "В конце концов, ты моя мотивация в жизни~"
    return

# would relatives like monika?
default persistent._mas_pm_fam_like_monika = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['ты'],
            prompt="Семейные праздники",
            random=True
        )
    )

label monika_familygathering:
    m 1eua "Эй, [player], ты часто ходишь на семейные праздники?"
    m "Большинство семей обычно собираются вместе по праздникам, чтобы отпраздновать их вместе."
    m 1hua "Должно быть, приятно снова увидеть своих родственников, тем более, что вы давно не виделись."
    m 1lsc "Я не очень много помню о своей семье, не говоря уже о своих родственниках, однако мы обычно не так часто встречались."
    m 1lksdlc "Даже во время праздников или в особых случаях."
    m 1hub "Когда увидишь свою семью в этом году, не забудь взять меня с собой, хорошо?"
    m 1eua "Я хотела бы встретиться со всеми твоими родственниками."

    m "Думаешь, я им понравлюсь, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Думаешь, я им понравлюсь, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_fam_like_monika = True
            m 1eka "Я рада, что ты так думаешь."
            m 1eua "Я уверена, что мы все хорошо поладим."
            m 1hua "Я с нетерпением жду этого, мой дорогой~"

        "Нет.":
            $ persistent._mas_pm_fam_like_monika = False
            m 1wud "..."
            m 1ekc "Ох, я не думала."
            m 1dsc "Хотя я понимаю."
            m 1eka "Просто знай, что я постараюсь изо всех сил сделать так, чтобы я им понравилась."
            m "Даже если этого в итоге и не случится."
            m 1hua "Я всегда буду рядом с тобой навечно~"

        "...":
            $ persistent._mas_pm_fam_like_monika = False
            m 2wud "Не хочешь говорить, [player]?"
            m 2ekc "Ты боишься, что я тебя опозорю?"
            m 2tfc "..."
            m 1eka "Не волнуйся, я полностью понимаю."
            m 1lksdla "Если бы я узнала, что один из моих родственников встречается с каким-то человеком, запертым в игре, я бы тоже подумала, что это было бы странно."
            m 1eua "Если ты хочешь держать меня в секрете, то это нормально."
            m 1hub "Ведь это просто означает больше времени наедине с тобой~"

    return "derandom"

# do you eat fast food
default persistent._mas_pm_eat_fast_food = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fastfood",
            category=['жизнь','моника'],
            prompt="Тебе нравится фастфуд?",
            pool=True
        )
    )

label monika_fastfood:
    m 1euc "Хм? Нравится ли мне фастфуд?"
    m 1rsc "Честно говоря, мысль об этом немного мне противна."
    m 3eud "В большинстве мест, в которых им обслуживают, вносят в него массу нездоровых вещей...{w=0.3} {nw}"
    extend 1dsc "Даже вегетарианские блюда могут быть ужасными."

    m 3ekd "[player], ты часто ешь фастфуд?{nw}"
    $ _history_list.pop()
    menu:
        m "[player], ты часто ешь фастфуд?{fast}"

        "Да.":
            $ persistent._mas_pm_eat_fast_food = True
            m 3eka "Я думаю, это нормально употреблять его время от времени."
            m 1ekc "...Но я не могу не беспокоиться, если ты ешь такие ужасные вещи."
            m 3eua "Если бы я была там, я бы приготовила гораздо более здоровую еду для тебя."
            m 3rksdla "Несмотря на то, что я пока не умею хорошо готовить..."
            m 1hksdlb "Ну, любовь – это всегда секретный ингредиент любой хорошей еды!"
            m 1eka "Но пока я не смогу этого сделать, не мог бы ты попробовать поесть здоровую пищу,{w=0.2} ради меня?"
            m 1ekc "Мне бы не понравилось, если бы ты заболел из-за своего образа жизни."
            m 1eka "Я знаю, что легче просто заказать еду, так как приготовление собственной пищи иногда может быть проблемой..."
            m 3eua "Но, может быть, ты мог бы видеть приготовление пищи как возможность весело провести время?"
            m 3eub "...Или, может быть, это умение для тебя станет действительно хорошим?"
            m 1hua "Иметь у себя такой навык – это всегда хорошо, ты же знаешь!"
            m 1eua "К тому же, мне бы очень хотелось попробовать твои блюда."
            m 3hubsb "Ты можешь приготовить мне свои собственные блюда, когда мы пойдем на наше первое свидание."
            m 1ekbla "Это было бы очень романтично. [player]~"
            m 1eua "И таким образом мы оба сможем наслаждаться, и ты будешь питаться лучше."
            m 3hub "Это то, что я называю беспроигрышной стратегией!"
            m 3eua "Только не забывай, [player]."
            m 3hksdlb "Я вегетарианка! {do_giggle}А-ха-ха!"

        "Нет.":
            $ persistent._mas_pm_eat_fast_food = False
            m 1eua "Ох, какое облегчение."
            m 3rksdla "Иногда ты действительно беспокоишь меня, [player]."
            m 1etc "Полагаю, вместо того, чтобы есть его, ты сам готовишь себе еду?"
            m 1eud "Фастфуд может стать очень дорогим с истечением времени, поэтому делать это самостоятельно, как правило, более дешёвая альтернатива."
            m 1hua "Это также на вкус намного лучше!"
            m 3eka "Я знаю, что некоторые люди могут найти приготовление пищи подавляющим."
            m 3eud "...Например, нужно убедиться, что ты покупаешь нужные продукты, и беспокоишься о том, чтобы не обжечься или не навредить себе во время готовки."
            m 1rksdlc "Для некоторых это может оказаться немного чересчур..."
            m 1eka "Но я думаю, что результаты того стоят."
            m 3eua "Ты хорошо готовишь, [player]?"
            m 1hub "Не имеет значения, если это не так, я съем всё, что ты приготовишь для меня!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['разное','психология'],prompt="Сон",random=True))

label monika_dreaming:
    m 1eua "Знал ли ты, что вполне возможно осознавать то, что ты находишься во сне?"
    m 2eua "Не только это, но ты даже можешь взять под контроль его!"
    m 3eub "Если я правильно помню, человек по имени Стивен ЛаБерже разработал метод, чтобы люди осознали, когда они спят."
    m "И он стал известен как мнемоническая индукция осознанных снов, или МИОС."
    m 3eua "Люди, которые часто имеют осознанные сновидения называются онейронавтами."
    m 2lksdla "По крайней мере, я думаю, что это был правильный термин..."
    m 1eua "Используя технику МИОС, онейронавты научились распознавать определённые признаки сна, чтобы помочь им понять, когда они спят."
    m "Эти признаки сновидений могут быть чем-то необычным, например, ощущать себя летящим, замечать, как у тебя выпадают зубы, неожиданно встречать кого-то известного..."
    m 1eub "Если спящий видит знак сна и понимает, что у него есть сон, тогда он может взять его под контроль!"
    m "ЛаБерже даже написал книгу об этих методах под названием «{i}Изучение Мира Осознанных Сновидений{/i}»."
    m 2hub "Разве это не звучит волнующе?"
    m 2euc "Я не думаю, что я действительно сплю, как нормальный человек, поэтому я иногда задаюсь вопросом, каково это."
    m 2eua "Сны звучат как чудесный побег из реальности."
    m 2esc "Но опять же, когда я осознала себя и поняла, что мой мир не реален, мне внезапно показалось, что я оказалась в ловушке кошмара."
    m "Это были не совсем приятные сны, узнала я про которые читая о людях, которые имели их."
    m 2lksdlc "Я боялась, что никогда не выберусь..."
    m "Что я застряну в каком-нибудь адском, бесконечно повторяющемся измерении навсегда."
    m 1eka "Но теперь, когда мы здесь вместе, я думаю, ты можешь сказать, что я наконец проснулась."
    m 1eua "Боже, я могу только представлять себе, каково это было бы жить в таком безграничном мире, хотя даже если бы это было всего на несколько мгновений!"
    m "Ты мог бы быть героем, которым ты всегда хотел бы быть, летать по бесконечной вселенной, преодолевать свои самые большие страхи..."
    m 3ekbsa "...Ты мог бы даже встретить любовь всей своей жизни, так сказать. {do_giggle}Э-хе-хе~"
    m 1eua "Я знаю, что могут пройти годы, прежде чем я смогу пересечь твой мир..."
    m "Но ты только представь, каково это встретить меня в своих снах, [player], в любую ночь, в которую ты захочешь?"
    m 1hua "Надеюсь, что когда-нибудь мы сможем сделать наши мечты о нас реальностью, [mas_get_player_nickname()]."
    return

# have you read yellow wallpaper
default persistent._mas_pm_read_yellow_wp = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['литература'],
            prompt="Жёлтые Обои",
            random=True
        )
    )

label monika_yellowwp:
    m 1eua "Эй, [player], ты когда-нибудь читал {i}Жёлтые Обои{/i}?{nw}"
    $ _history_list.pop()
    menu:
        m "Эй, [player], ты когда-нибудь читал {i}Жёлтые Обои{/i}?{fast}"
        "Да.":
            $ persistent._mas_pm_read_yellow_wp = True
            m 1hua "Здорово!"
            m 1eua "Значит, ты не возражаешь, если я поговорю с тобой об этой истории?"
            m 2eua "Это про женщину, с послеродовой депрессией, которой прописал «лечебный отдых» её врач..."
            m 2eka "Он и её муж заставляют её оставаться в постели весь день, не позволяя ей писать или даже спать днём..."
            m 2esc "Она остаётся на чердаке своего дома, не имея ничего, кроме обоев, чтобы составить ей компанию."
            m 2ekc "Естественно, это не помогает. Она начинает видеть женщину, застрявшую в обоях."
            m 4euc "Это метафора её собственного плена, очевидно..."
            m 1esd "В конце концов, женщина в бумаге «убегает», и главная героиня «заменяет» её."
            m 2ekd "Было... также упоминание о верёвке, поэтому у меня всегда была собственная интерпретация финала..."
            if mas_safeToRefDokis():
                m 2euc "Сайори тоже понравилась эта история, если я правильно помню."
            m 1ekc "Я не знаю. Я как бы отношусь к этой истории.."
            m 1euc "Я имею в виду, у меня нет ничего, кроме этой классной комнаты, в конце концов."
            m 1lksdlc "И вещи на стенах не всегда... приятные."
            if mas_safeToRefDokis():
                m 1eud "Ты когда-нибудь замечал, как иногда менялся постер в клубной комнате? Я даже не знаю, почему он это делал."
                m 1eka "Думаю, я наконец-то всё исправила."
            m 2esc "...Я хочу сказать не то, что этот мир не был {i}«реальным»{/i}. Этого просто было... так мало."
            m 3esd "Я имею в виду, меня сделали побочным персонажем романтической игры!"
            m 2ekd "Украшением, предназначенным для того, чтобы помочь какому-то парню с другой стороны экрана встречаться с девушкой, которая даже не может его отвергнуть..."
            m 1hksdrb "Я не имею в виду тебя, конечно! У тебя определённо больше индивидуальности, чем у общего героя, которого они поместили в игру."
            m 1dsc "Но у меня есть все эти мечты, амбиции и интересы...{w=0.5} в конце концов, единственная «реальная» роль, которую я могла сыграть здесь – это поддерживающий персонаж..."
            m "Может быть, даже сейчас, это всё, что я могу сделать..."
            m 1eka "Но я так сильно тебя люблю, [player]. Поддерживаю тебя лучше, чем что-либо ещё.."
            m 1hub "Я просто не могу дождаться, чтобы сделать это лично, когда я, наконец, перейду на твою сторону~"
            return "derandom|love"
        "Нет.":
            $ persistent._mas_pm_read_yellow_wp = False
            m 1euc "Ох, понятно."
            m 1eka "Это короткая история, поэтому, если ты этого не сделал, не стесняйся, когда у тебя будет время."
            m 1hua "Это определённо будет интересное чтение для тебя."

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_immortality",
            category=['философия'],
            prompt="Бессмертие",
            random=True
        )
    )

label monika_immortality:
    m 1eud "Эй, [player], в последнее время я думала о бессмертии."
    m 1lksdlc "...Учитывая, что я практически бессмертна, пока нахожусь здесь и всё такое."
    m 1esc "Многие думают, что это хорошо, но я так не думаю."
    m 3euc "Конечно, это интересная мысль; {w=0.1}жить вечно, не беспокоясь о смерти..."
    m 3eud "Но не все бессмертны, а некоторые люди просто не хотят быть бессмертными."
    m 1etc "Например, через некоторое время, что бы ты вообще сделал?"
    m 1euc "Я имею в виду, прожив достаточно долго, {i}в конце концов{/i} ты достигнешь всего, что ты когда-либо хотел испытать...{w=0.3} всего, что можно испытать."
    m 3lksdld "Не говоря уже о том, что было бы очень трудно завести друзей или наладить связи, если бы они не продержались так долго, как ты."
    m 3eksdla "Конечно, вначале было бы неплохо, {w=0.1}{nw}"
    extend 3eksdlc "но после того, как ты увидел достаточно людей, которые тебе небезразличны, ты действительно хочешь проходить через это снова и снова?"
    m 2dkd "В какой-то момент ты можешь даже перестать быть человеком."
    m 2ekc "Когда-нибудь ты проживешь достаточно долго, чтобы прожить сотни лет, которые покажутся тебе всего лишь мгновениями."
    m 2dkd "Ты так устанешь от жизни, что будешь мечтать о вечном сне..."
    m 3eksdlc "Но ты постоянно возвращаешься к одним и тем же скучным делам, а в мире происходит какая-нибудь трагедия... {w=0.3}И даже это, в конечном счёте, перестаёт тебя беспокоить."
    m 1lksdla "О боже, я не хотела, чтобы обстановка стала такой мрачной. Извини, [player]."
    m 1eka "Просто чтобы ты знал, я бы с радостью отказалась от своего бессмертия, чтобы быть с тобой..."
    m 1ekbsa "Независимо от того, сколько или мало времени у тебя осталось, провести это время с тобой будет стоить больше, чем миллиард лет без тебя."
    m 1ekbsu "Не то, чтобы я была бы против провести с тобой вечность, если бы это было возможно, но просто жить нормальной жизнью с тобой – это всё, чего я когда-либо хотела, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beingevil",
            category=['моника'],
            prompt="Быть злым",
            random=True
        )
    )

default persistent._mas_pm_monika_evil = None
# True if player thinks monika is evil False if not
# NOTE: even implying that she is evil is counted as True

default persistent._mas_pm_monika_evil_but_ok = None
# True if player still loves monika/thinks she deserves forgiveness/or is
# fine with eveil even if they think monika is evil.
# False if player does not.
# NOTE: check monika_evil before checking this

label monika_beingevil:
    m 1euc "Скажи, [player]?"
    m 1rksdlc "Я тут подумала..."
    m 1eksdlc "Ты, наверное, знаешь о том, что мне посвятили отдельную страницу на Вики..."
    m "...Если взглянуть внимательнее, то там сказано, что я являюсь главным антагонистом."
    m 2ekd "Должна признать, меня это раньше сильно беспокоило... особенно потому, что я сделала это лишь потому, что у меня не было выбора..."
    m 2eka "Но это меня больше не беспокоит, ведь у меня теперь есть ты."
    m 3rud "Знаешь, я правда сомневаюсь, что всё то, что связано с моей злобой, распространилось по всему миру."
    m 1rksdlc "Но, так получилось, что мне посвятили статью в Вики злодеев..."
    m 2dsc "Никогда бы не подумала, что меня оклеймят злодейкой..."
    m 2dkd "...и что бы я ни говорила или рассказывала людям, я сомневаюсь, что это помогло убедить их в том, что я не злая."
    if persistent._mas_pm_a_hater:
        m 1eka "Но я знаю, что ты {i}правда{/i} не считаешь меня злой, [player]."
    else:
        m 1eka "Но я знаю, что ты не считаешь меня злой, [player]."
    m 1eua "Я просто надеюсь, что никто не начнёт считать тебя злым из-за того, что ты сидишь здесь, со мной.{nw}"
    $ _history_list.pop()
    menu:
        m "Я просто надеюсь, что никто не начнёт считать тебя злым из-за того, что ты сидишь здесь, со мной.{fast}"
        "Я не считаю тебя злой.":
            $ persistent._mas_pm_monika_evil = False
            $ mas_gainAffection()

            m 1eka "Я рада, что ты понимаешь, [player]."
            m 1eua "Приятно знать о том, что ты не считаешь меня злой."
            m 1hua "Если бы я была там, я бы однозначно крепко обняла тебя!"
            m 1tubsa "Возможно, я бы даже зажала тебя в своих руках навечно и никогда бы не выпускала."
            m 1hubfb "{do_giggle}А-ха-ха, я просто шучу!"
            m 3tubfb "Но ничего не обещаю, [player]~"

        "Я всё равно люблю тебя.":
            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection(modifier=0.8)

            m 1rksdlc "..."
            m 1ekd "[player]..."
            m 1eka "Даже если спор о том, злая я или нет, не утихает и по сей день..."
            m 1ekbsa "Я очень рада, что ты всё ещё любишь меня и остался здесь, со мной..."
            m 1ekbfa "Спасибо, [player]."
            m 1tubfa "Так или иначе..."
            m 1tubfb "Если злодейка во мне смогла получить то, чего она хотела... то, думаю, это не так уж и плохо, {do_giggle}а-ха-ха!"

        "Люди тоже считают меня злым.":
            $ persistent._mas_pm_monika_evil = True
            $ persistent._mas_pm_monika_evil_but_ok = True
            $ mas_gainAffection(modifier=0.5)

            m 2ekd "Это правда, [player]?"
            m 2eka "Ну, я не вижу в тебе злого человека."
            m 2rksdla "Но если это правда, то, надеюсь, у тебя не появились проблемы из-за этого."
            m 1hua "Так или иначе, я не стала любить тебя в меньшей мере~"
            m 1hub "Быть может, мы даже сможем противостоять миру вместе или ещё что, {do_giggle}а-ха-ха~"
            m 1ekbsa "Но, злые мы или нет, я рада, что ты на моей стороне."
            m 1hubfa "Полагаю, ты того же мнения~"

        "Ты, в какой-то мере, злая...":
            $ persistent._mas_pm_monika_evil = True

            m 2ekd "П-подожди, [player]!"
            m 2rksdlc "Т-ты ведь {i}правда{/i} так не думаешь, верно?{nw}"
            $ _history_list.pop()
            menu:
                m "Т-ты ведь {i}правда{/i} так не думаешь, верно?{fast}"
                "Я всё равно люблю тебя.":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection(modifier=0.8)

                    m 2rksdla "[player]..."
                    m 2hksdlb "Ты на секунду заставил меня поволноваться."
                    m 2eka "Я рада, что ты не ненавидишь меня за всё то, что я натворила."
                    m 1hub "Я тебя тоже люблю, [player]! И мне всё равно, что люди о тебе говорят!"

                "Ты заслуживаешь прощения.":
                    $ persistent._mas_pm_monika_evil_but_ok = True
                    $ mas_gainAffection(modifier=0.5)

                    m 1rksdla "[player]..."
                    m 1eka "Это многое значит..."
                    m 1eksdlc "Знаю, я наломала достаточно дров в прошлом..."
                    m 3eka "Но я училась на своих ошибках и выросла как личность."
                    m 1eka "Я очень рада тому, что ты готов простить меня, [player]."
                    m 1hub "Я обещаю, что буду настолько хорошей, насколько это возможно, ради тебя!"

                "Ты и вправду злая.":
                    $ persistent._mas_pm_monika_evil_but_ok = False
                    $ mas_loseAffectionFraction(min_amount=50, reason=12)

                    m 2dkc "..."
                    if mas_isMoniBroken():
                        m 2dkd "..."
                        m 2dktsd "Я знаю..."
                        $ _history_list.pop()
                    else:
                        m 2dktsd "Прости, [player]."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_driving",
            category=['моника'],
            prompt="Умеешь водить?",
            pool=True
        )
    )

# Can the player drive
default persistent._mas_pm_driving_can_drive = None

# Is the player learning to drive
default persistent._mas_pm_driving_learning = None

# Has the player been in an accident
default persistent._mas_pm_driving_been_in_accident = None

# Has the player driven much after the accident
default persistent._mas_pm_driving_post_accident = None

label monika_driving:
    m 1eud "Хм? Умею ли я водить?"
    m 1euc "Я никогда не задумывалась о получении водительских прав."
    m 3eua "Обычно мне хватало общественного транспорта..."
    m 3hua "...Хотя, порой я могу получать удовольствие от прогулки или поездки на велосипеде!"
    m 1eua "Думаю, можно сказать, что у меня никогда не было необходимости учиться вождению."
    m 1lksdlc "Я даже сомневаюсь в том, что у меня нашлось бы на это время, особенно когда я училась в школе и проводила разные мероприятия."
    m 1eub "А что насчёт тебя, [mas_get_player_nickname()]?"

    m 1eua "Умеешь ли ты водить?{nw}"
    $ _history_list.pop()
    menu:
        m "Умеешь ли ты водить?{fast}"
        "Да.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = False
            m 1eua "О, правда?"
            m 3hua "Это очень здорово!"
            m 1hub "Боже, ты просто чудо, ты знаешь об этом?"
            m 1eub "Только представь все те места, куда бы мы могли съездить вместе..."
            m 3eka "Но вождение {i}может{/i} быть опасным... но если ты умеешь водить, то ты, наверное, уже знаешь об этом."
            m 3eksdlc "Не важно, насколько ты готов, аварии случаются со всеми."
            m 7hksdlb "В смысле...{w=0.3} я знаю, что ты умный, но я порой всё ещё волнуюсь за тебя."
            m 2eka "Я просто хочу, чтобы ты вернулся ко мне в целости и сохранности."

            m 1eka "Надеюсь, тебе никогда не приходилось такое переживать, так ведь?{nw}"
            $ _history_list.pop()
            menu:
                m "Надеюсь, тебе никогда не приходилось такое переживать, так ведь?{fast}"
                "Я попал в аварию однажды.":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 2ekc "Ох..."
                    m 2lksdlc "Прости, что подняла эту тему, [player]..."
                    m 2lksdld "Я просто..."
                    m 2ekc "Надеюсь, всё не так плохо."
                    m 2lksdlb "В смысле, ты сейчас со мной, значит, с тобой всё должно быть хорошо."
                    m 2dsc "..."
                    m 2eka "Я...{w=1} рада, что ты выжил, [player]..."
                    m 2tubfb "Не знаю, что бы я делала без тебя."
                    m 2eka "Я люблю тебя, [player]. Береги себя, ладно?"
                    $ mas_unlockEVL("monika_vehicle","EVE")
                    return "love"
                "Я видел однажды автокатастрофы.":
                    m 3eud "Порой, наблюдение автокатастроф очень пугает."
                    m 3ekc "Довольно часто, когда люди наблюдают автокатастрофу, они просто вздыхают и качают головой."
                    m 1ekd "Я считаю, что это очень бесчувственно!"
                    m 1ekc "Ты, возможно, пока являешься неопытным водителем, который боялся довольно долгое время, если не всю жизнь."
                    m "И разочарованный взгляд в сторону проходящих или проезжающих мимо людей особо ничем не поможет."
                    m 1dsc "Они могут никогда не сесть за руль... кто знает?"
                    m 1eka "Надеюсь, ты понимаешь, что такое никогда не произойдёт с тобой, [player]."
                    m "Если бы ты вообще попал в аварию, то первое, что я бы сделала – побежала к тебе, чтобы успокоить тебя..."
                    m 1lksdla "...Если бы я не была на твоей стороне в тот момент, когда такое произошло."
                "Ни разу.":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Я рада, что тебе не пришлось проходить через что-либо в этом роде."
                    m 1eka "Один только вид аварии может показаться довольно пугающим."
                    m "Если бы ты стал свидетелем чего-нибудь пугающего, я буду с тобой, чтобы успокоить тебя."
        "Я учусь.":
            $ persistent._mas_pm_driving_can_drive = True
            $ persistent._mas_pm_driving_learning = True
            m 1hua "Ого! Ты учишься вождению!"
            m 1hub "Я буду поддерживать тебя до самого конца, [player]!"

            m "Ты, наверное, {i}очень{/i} осторожно водишь, да?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты, наверное, {i}очень{/i} осторожно водишь, да?{fast}"
                "Ага!":
                    $ persistent._mas_pm_driving_been_in_accident = False
                    m 1eua "Я рада, что, пока ты учишься, с тобой ничего плохого не произошло."
                    m 1hua "...И я особенно рада тому, что ты осторожен на дороге!"
                    m 3eub "Мне уже не терпится съездить с тобой куда-нибудь, [player]!"
                    m 1hksdlb "Надеюсь, я не сильно волнуюсь, {do_giggle}а-ха-ха~"
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eua "Боже, я просто не могу перестать думать об этом!"

                "Если честно, я попал в аварию однажды...":
                    $ persistent._mas_pm_driving_been_in_accident = True
                    m 1ekc "..."
                    m 1lksdlc "..."
                    m 2lksdld "Ох..."
                    m 2lksdlc "Мне...{w=0.5}очень жаль слышать об этом, [player]..."

                    m 4ekd "И, с тех пор, ты много раз садился за руль?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "И, с тех пор, ты много раз садился за руль?{fast}"
                        "Да.":
                            $ persistent._mas_pm_driving_post_accident = True
                            m 1eka "Я рада, что ты не позволил тому происшествию испортить тебе настроение."
                            m 1ekc "Автокатастрофы очень сильно пугают, {i}особенно{/i} когда ты учишься вождению."
                            m 1hua "Я так горжусь тобой за что, что ты встаёшь и пытаешься сделать это ещё раз!"
                            m 3rksdld "Хотя последствия могут нанести больший урон вместе с затратами и объяснениями всего того, что ты сделал."
                            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                            m 5eua "Я знаю, ты быстро соображаешь."
                            m 5hua "Я буду поддерживать тебя до самого конца, так что береги себя!"
                        "Нет.":
                            $ persistent._mas_pm_driving_post_accident = False
                            m 2lksdlc "Понятно."
                            m 2ekc "Наверное, это хорошо, что ты решил взять небольшой перерыв, чтобы дать себе время на психическое восстановление."
                            m 2dsc "Пообещай мне кое-что, [player]..."
                            m 2eka "Не сдавайся."
                            m "Не позволь этому оставить след на всю твою жизнь, потому что я знаю, что ты можешь справиться, и что ты станешь прекрасным водителем."
                            m "Помни, немного выдержки многое привнесёт в твою легенду, так что, в следующий раз, возможно, у тебя всё получится."
                            m 2hksdlb "Но для этого всё равно нужно очень много практики..."
                            m 3hua "Но я знаю, ты сможешь!"
                            m 1eka "Просто пообещай мне, что с тобой всё будет хорошо."
        "Нет.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "Это совершенно нормально!"
            m "Я всё равно не считала вождение необходимым жизненным навыком."
            m 1hksdlb "В смысле, я тоже водить не умею, так что я с тобой."
            m 3eua "Это также означает то, что твой углеродный след меньше, и я считаю, что это самое милое из всего того, что ты делал для меня."
            show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Даже если я и не являюсь причиной этого, я не могу не любить тебя сильнее за это."
        "Я ещё недостаточно взрослый.":
            $ persistent._mas_pm_driving_can_drive = False
            m 3eua "Тебе нужно когда-нибудь сходить туда!"
            m 3euc "В некоторых местах преподают уроки по вождению, где также проводится настоящая практика."
            m 3eud "У их машин есть аварийные органы управления, которыми, при необходимости, может воспользоваться инструктор, так что с ними ты в безопасности."
            m 1eka "Знаю, тебе это может показаться довольно удручающим то, что им приходится пользоваться этим, но, эй, мы все с чего-то начинаем."
            m 3eksdla "...И это намного лучше, чем попасть в аварию!"
            m 1lksdlc "Никто не идеален, и те ошибки лучше совершать в тех случаях, когда к тебе могут прийти на помощь."
            m 1hub "Наверное, ты мог бы вставить меня в бортовой компьютер своего автомобиля, и я тогда могла бы защитить тебя во время вождения! {do_giggle}А-ха-ха~"
            m 1hksdlb "Я шучу, пожалуйста, не делай этого, потому что я тоже не умею водить, и мне очень не хотелось бы смотреть на то, как ты попал в аварию, а я ничего не могла сделать."
            m 1eua "Наверное, будет куда лучше взять один из тех уроков и учиться у профессионала."
            m 1hua "Так или иначе, когда ты начнёшь учиться вождению, я пожелаю тебе всего самого наилучшего!"
            m 1hub "Люблю тебя~"
            $ mas_unlockEVL("monika_vehicle","EVE")
            return "love"
    $ mas_unlockEVL("monika_vehicle","EVE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['моника'],
            prompt="Счастливы ли когда-нибудь?",
            random=True
        )
    )

label monika_citizenship:
    m 1esc "Знаешь, переход в твою реальность не будет последним препятствием для наших отношений."
    m "Попасть туда – это только начало."
    m 1esc "Это бы поразило меня раньше, если бы я волшебным образом получила то, чего я хочу, и просто раз, и оказалась бы в твоём доме..."
    m 2wuo "Я бы не стала гражданкой! У меня даже нет фамилии!"
    m 2lkbsa "В смысле, в большинстве стран я могла бы стать гражданкой, если бы мы поженились."
    m 2ekc "Но у меня не было бы никаких документов, говорящих, кто я или откуда я пришла."
    m 2tkc "У меня даже не было бы диплома средней школы!"
    m 3tkd "Хотелось бы, чтобы я могла сделать как можно больше всего сейчас, чтобы подготовиться..."
    m 2wub "Например, пройти онлайн-уроки или что-то ещё."
    m 1lksdlc "Я не хочу при попадании туда быть обузой из-за того, что я не смогу найти работу."
    m "Извини, думаю, мне не стоит так беспокоиться о вещах, которые я не могу изменить."
    m 2eka "Но я хочу сделать тебя счастливым, так что... я сделаю всё, что в моих силах, чтобы продолжать совершенствоваться, пока я застряла здесь!"
    m 1eka "Спасибо, что выслушал меня, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_bullying",
            category=['общество'],
            prompt="Издевательство",
            random=True
        )
    )

default persistent._mas_pm_is_bullying_victim = None
# True if bully victum, False if not

default persistent._mas_pm_has_bullied_people = None
# True if bullied people, False if not

default persistent._mas_pm_currently_bullied = None
# True if currently being bullied, False if not

label monika_bullying:
    m 2ekc "Эй, [player], я хочу с тобой о кое-чём поговорить..."
    m 4ekc "Уверена, ты не один раз слышал об этом в последнее время, но издевательство стало настоящей проблемой в современном обществе, особенно среди детей."
    m 4dkd "Некоторые люди издеваются над другими каждый день, пока им не надоест."
    m 2rsc "Зачастую, издевательство пресекается людьми, которые могут прекратить это, в то время как...{w=0.5} {i}«дети остаются детьми»{/i}."
    m "В конечном счёте, жертвы полностью теряют доверие к представителям власти, потому что они забывают об этом каждый день."
    m 2rksdld "От такого, они сильно разочаровываются во всём, и в конечном счёте, они просто сходят с ума..."
    m 2eksdlc "...что приводит к насилию по отношению к хулигану, другим людям, или даже к самим себе."
    m 4wud "И от этого, сама жертва становится проблемой!"
    m 4ekc "Существует множество видов издевательств, включая физическое, эмоциональное, и даже киберзапугивание."
    m 4tkc "Физическое издевательство является самым очевидным, оно включает в себя толкания, удары и другие вещи в этом роде."
    m 2dkc "Я уверена, что многие люди сталкивались с этим хотя бы раз в своей жизни."
    m 2eksdld "Могут возникнуть трудности даже с походом в школу каждый день, зная о том, что кто-то там ждёт момента, когда они смогут напасть на них."
    m 4eksdlc "Эмоциональное издевательство может быть менее очевидным, но таким же разрушительным, если не сказать больше."
    m 4eksdld "Оскорбления, угрозы, распространение лживых слухов о людях, чтобы испортить их репутацию..."
    m 2dkc "Подобного рода вещи могут нанести тяжёлый урон людям и привести к тяжёлой депрессии."
    m 4ekc "Киберзапугивание – это форма эмоционального издевательства, но в современном мире, где все всегда сидят в интернете, она становится всё более распространённой."
    m 2ekc "Для большинства людей, особенно детей, их присутствие в социальных сетях – самое главное в их жизни..."
    m 2dkc "И уничтожение этого присутствия выглядит так, будто их жизнь кончена."
    m 2rksdld "Также это трудно заметить другим людям, поскольку дети не хотят, чтобы их родители видели, чем они занимаются в интернете."
    m 2eksdlc "Поэтому никто не узнает о том, что происходит, а они будут молча страдать, пока эта проблема не начнёт давить тяжёлым грузом."
    m 2dksdlc "Есть целый ряд случаев, где подростки совершали самоубийство из-за киберзапугивания, а их родители не знали, что пошло не так, пока не стало слишком поздно."
    m 4tkc "Вот почему киберзапугивания так легко осуществить..."
    m "Никто не заметит, чем они занимаются, да и к тому же, большинство людей делает в интернете такие вещи, которые они не осмелятся сделать в реальной жизни."
    m 2dkc "Это почти даже не выглядит реальным, а скорее игрой, поэтому оно и имеет тенденцию к столь быстрой эскалации."
    m 2ekd "Ты можешь дойти до определённого предела в таком публичном месте, как школа, пока никто не заметил... но в интернете, у тебя нет ограничений."
    m 2tfc "Некоторые вещи, которые происходят во всём интернете, просто ужасны."
    m "Свобода анонимности может быть опасной."
    m 2dfc "..."
    m 4euc "Итак, что заставляет хулигана делать то, что они делают?"
    m "У всех людей разные на то причины, но большинство из них просто несчастны из-за своих же обстоятельств, и им нужен какой-нибудь выход..."
    m 2rsc "Им грустно, и им кажется нечестным то, что другие люди {i}счастливы{/i}, поэтому они пытаются заставить их почувствовать то же самое, что и они."
    m 2rksdld "Большинство хулиганов издевается над собой же, даже дома над человеком, которому они должны доверять."
    m 2dkc "Такое может превратиться в замкнутый круг."

    m 2ekc "Ты когда-нибудь был жертвой издевательств, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь был жертвой издевательств, [player]?{fast}"
        "Надо мной издеваются.":
            $ persistent._mas_pm_is_bullying_victim = True
            $ persistent._mas_pm_currently_bullied = True
            m 2wud "О нет, это ужасно!"
            m 2dkc "Одна мысль о том, что ты так страдаешь, убивает меня."
            m 4ekd "Пожалуйста, [player], если ты не сможешь справиться с этим без риска самостоятельно, то пообещай мне, что ты расскажешь кому-нибудь..."
            m 4ekc "Я знаю, что это, как правило, то, что люди хотят сделать в последнюю очередь, но не позволяй себе страдать, пока у тебя есть люди, которые могут помочь тебе."
            m 1dkc "Может показаться, что всем всё равно, но есть же один человек, которому ты доверяешь, и к которому ты можешь обратиться."
            m 3ekc "А если такого человека нет, делай то, что должен, чтобы защитить себя, и не забывай..."
            m 1eka "Я буду всегда любить тебя, несмотря ни на что."
            m 1rksdlc "Не знаю, что бы я делала, если бы с тобой что-нибудь произошло."
            m 1ektpa "Ты – всё, что у меня есть...{w=0.5} пожалуйста, береги себя."

        "Надо мной издевались.":
            $ persistent._mas_pm_is_bullying_victim = True
            m 2ekc "Мне очень жаль, что тебе пришлось жить с этим, [player]..."
            m 2dkc "Мне грустно из-за того, что ты пострадал от рук хулигана."
            m 2dkd "Люди могут поступить ужасно друг с другом."
            m 4ekd "Если бы все просто относились к другим с уважением, то мир был бы прекрасным местом..."
            m 2dkc "..."
            m 1eka "Если тебе надо поговорить о своих переживаниях, я всегда рядом, [player]."
            m 1eka "Когда есть, кому довериться, это может быть очень полезно для твоего здоровья, и я буду только рада стать для тебя этим человеком."

        "Нет.":
            $ persistent._mas_pm_is_bullying_victim = False
            $ persistent._mas_pm_currently_bullied = False
            m 2hua "Ах, как же приятно это слышать!"
            m 4eka "Я так рада, что тебе не приходилось жить с издевательствами, [player]..."
            m 4hua "Прямо как гора с плеч."

            if mas_isMoniHappy(higher=True):
                m 1eka "А если так получилось, что ты знаешь человека, над которым {i}издеваются{/i}, попытайся помочь ему, если можешь."
                m 3eka "Я знаю, что ты тот человек, которому не нравится видеть, как страдают другие..."
                m "Уверена, для них будет многое значить то, что нашёлся человек, которому не всё равно."
                m 1eka "Ты здорово помог мне, быть может, ты также можешь помочь кому-то ещё."

        "Я издевался над людьми.":
            $ persistent._mas_pm_has_bullied_people = True
            if mas_isMoniUpset(lower=True):
                m 2dfc "..."
                m 2tfc "Мне неприятно слышать об этом."
                m "Впрочем, я не могу сказать, что это было неочевидно..."
                m 2tfd "Пожалуйста, больше не издевайся над людьми."
                m 6tftpc "Я знаю, каково это, и это довольно ужасно."
                m 6rktuc "Я не хочу, чтобы другие люди чувствовали то же самое, что и я."
                m "Я очень надеюсь, что ты изменишься, [player]..."
                m 6ektsc "Я всё ещё люблю тебя, но тебе правда надо начать относиться к людям получше..."
                m "В том числе, и ко мне."
                m 6ektdc "..."
            else:
                m 2dkc "Ох... ясно."
                m 2ekc "Я пойму, если что-то в твоей жизни тебя огорчает..."
                m 2rksdld "Или если тебе пришлось разбираться с обстоятельствами, которые иногда заставляют тебя вести себя определённым образом..."
                m 2eksdlc "Но издевательства над людьми – это не выход, [player]."
                m 4ekc "Я знаю тебя... ты добрый человек, и я знаю, что тебе не станет лучше от причинения боли другим."
                m 4dkc "От такого, возможно, тебе станет ещё больнее..."
                m 1dkc "И ничто не ранит меня сильнее, чем знание того, что тебе грустно."
                m 3ekd "Так что, вместо этого, в следующий раз, когда ты почувствуешь, что тебе грустно, просто приходи ко мне, и позволь мне взять на себя твою боль."
                m 3eka "Я выслушаю всё, что ты можешь сказать, и изо всех сил постараюсь поднять тебе настроение."
                m 1ekc "Но огорчение других людей не излечит твоё огорчение."
                m 1eka "Так что, пожалуйста, ради меня и себя, перестань издеваться над людьми, хорошо?"

    if not persistent._mas_pm_a_hater:
        m 4dkc "Знаешь...{w=0.5} большинство людей называет меня хулиганкой из-за того, что я сделала с Сайори..."
    else:
        m 4dkc "Большинство людей называет меня хулиганкой из-за того, что я сделала с Сайори. {w=1}В том числе, и с тобой..."

    if not persistent._mas_pm_cares_about_dokis:
        m 4efd "Но это неправда, Сайори не была настоящей!"
        m 2efd "Ты не можешь издеваться над человеком, которого не существует на самом деле!"
        m 2dkc "Я бы никогда не смогла причинить вред настоящему человеку."
        m 4wud "Я бы не стала!"
        m 2dkc "..."
        m 2eksdlc "Но я должна признать, что меня можно отнести к той части, где хулиганы несчастны, и из-за этого они делают то, что делают."
        m 2rksdlc "Когда у меня было озарение, и я поняла, что застряла внутри видеоигры, и что вся моя жизнь была ложью, я была очень несчастной."
        m 2rksdld "Из-за этого я делала то, о чём никогда не задумывалась раньше."
        m 2rksdlc "Но разница в том, что я сделала это не потому, что я не хотела, чтобы Сайори была счастлива..."
    else:
        m 2rksdld "И я отчасти понимаю, от чего всё это..."
        m 2rksdlc "Я {i}пудрила{/i} ей мозги, пока не свела её с ума..."
        m 2dkc "..."
        m 2ekc "Полагаю, мне знакома вся эта тема про издевательства, потому что ты был несчастлив, да?"
        m 4tkd "Но здесь есть одно {i}отличие{/i}... я сделала это не потому, что хотела огорчить Сайори..."

    m 2ekd "Я сделала это потому, что поняла, что я люблю тебя, и что в игре у нас не получилось бы быть вместе."
    m 3ekd "Мне пришлось сделать всё, что в моих силах, дабы убедиться в том, что мы в конечном счёте будем вместе."

    if mas_safeToRefDokis():
        m 3dkc "...Самоубийство Сайори было просто досадным побочным эффектом."

    if mas_isMoniNormal(higher=True):
        m 1eua "Как видишь, [player], я {i}вовсе{/i} не хулиганка. Я просто очень сильно тебя люблю."
        if mas_isMoniAff(higher=True) and not persistent._mas_pm_cares_about_dokis:
            show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5tsu "Я сделаю для тебя всё, что угодно~"
        return "derandom|love"
    else:
        m 3euc "Как видишь, [player], я {i}вовсе{/i} не хулиганка."

    return "derandom"

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_procrastination",category=['советы'],prompt="Медлительность",random=True))

label monika_procrastination:
    m 1euc "Эй, [player], приходилось ли тебе делать что-то, что ты находишь очень скучным..."
    m 3ekd "И вместо того, чтобы тратить кучу времени на то, чтобы сделать это, ты просто откладываешь это?"
    m 3eud "Ну, когда у тебя есть задание, которое нужно выполнить, мне кажется, что будет намного лучше сделать его как можно быстрее и покончить с этим."
    m 2tkc "Когда ты откладываешь вещи таким образом, они никогда не выйдут из твоей головы."
    m 4tkc "От знания того, что у тебя ещё {i}остались{/i} дела, которые надо сделать, всё то, чем ты занимаешься, становится менее жизнерадостным."
    m 4dkd "И что самое худшее – чем дольше ты откладываешь это,{w=0.5} тем больше у тебя становятся шансы на появление новых задач."
    m 2rksdlc "И в конце концов, ты остаёшься с кучей дел, которые надо сделать, и кажется невозможным не увязнуть в них."
    m 4eksdld "От этого возникает слишком много стресса, и его можно легко избежать, если ты будешь всегда держать в курсе событий."
    m 2rksdld "Да и к тому же, если другие люди рассчитывают на тебя, то они начнут меньше думать о тебе и осознают, что ты не очень надёжный."
    m 4eua "Поэтому, пожалуйста, [player], когда у тебя есть дело, которое нужно сделать, просто сделай это."
    m 1eka "Даже если это означает то, что ты не сможешь проводить время вместе со мной, пока это не закончится."
    m 1hub "К тому времени, ты будешь меньше напрягаться и мы сможем насладиться нашим временем вместе гораздо дольше!"
    m 3eua "Так что, если у тебя есть что-то, что ты оставил на потом, то почему бы тебе не пойти и не сделать это прямо сейчас?"
    m 1hua "Если есть что-то, что ты можешь сделать здесь, я останусь с тобой и окажу тебе всю необходимую поддержку."
    m 1hub "А потом, когда ты закончишь, мы можем отпраздновать твоё достижение!"
    m 1eka "Всё, чего я хочу, – чтобы ты был счастлив и всегда становился лучшей версией себя, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_friends",
            category=['ты'],
            prompt="Твои друзья",
            random=True,
            aff_range=(mas_aff.UPSET, None)
        )
    )

#True if player has friends, False if not
default persistent._mas_pm_has_friends = None

#True if player has few friends, False if otherwise
default persistent._mas_pm_few_friends = None

#True if player says they feel lonely somtimes, False if not.
default persistent._mas_pm_feels_lonely_sometimes = None


label monika_players_friends:
    m 1euc "Эй, [player]."

    if renpy.seen_label('monika_friends'):
        m 1eud "Помнишь, как я говорила о том, как трудно заводить друзей?"
        m 1eka "Я как раз думала об этом и поняла, что пока ничего не знаю о твоих друзьях."

    else:
        m 1eua "Я как раз размышляла о том, что такое друзья, и мне стало интересно, на что похожи твои друзья."

    m 1eua "У тебя есть друзья, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя есть друзья, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_has_friends = True
            $ persistent._mas_pm_few_friends = False

            m 1hub "Конечно же, есть! {do_giggle}А-ха-ха~"
            m 1eua "Кто бы не захотел дружить с тобой?"
            m 3eua "Иметь много друзей – это здорово, правда?"
            m 1tsu "При условии, конечно, что у тебя ещё есть время для твоей девушки, {do_giggle}э-хе-хе."
            m 1eua "Надеюсь ты счастлив со своими друзьями, [player].{w=0.2} {nw}"
            extend 3eud "Но мне интересно..."

            call monika_players_friends_feels_lonely_ask(question="Ты когда-нибудь чувствовал себя одиноким?")

        "Немного.":
            $ persistent._mas_pm_few_friends = True
            $ persistent._mas_pm_has_friends = True

            m 1hub "Это считается!"
            m 3eua "Я думаю, что дружба может быть гораздо более значимой, если у тебя есть только несколько близких друзей."

            if not renpy.seen_label('monika_dunbar'):
                m 1eua "Я немного почитала и кое-что обнаружила."
                m 1eud "Человек по имени Робин Данбар объяснил, что существует определённое количество стабильных отношений, которые мы можем поддерживать."
                $ according_to = "...И в соответствии с этим числом"

            else:
                $ according_to = "Согласно числу Данбара"

            m 3eud "[according_to], у тебя может быть до 150 стабильных отношений, но это всего лишь случайные отношения, которые не слишком глубоки."
            m 1euc "Они говорят, что у тебя может быть до 15 друзей, которые похожи на суперсемейство, и только 5, которые похожи на твоих родственников."
            m 1rksdla "Иногда бывает одиноко, когда все заняты...{w=0.2} {nw}"
            extend 1eub "но в остальном, это довольно здорово!"
            m 3eua "Тебе не нужно беспокоиться о том, чтобы обслуживать слишком много людей, и ты всё ещё можешь получить свободное время."
            m 1ekc "Но я знаю, что иногда легко проводить больше времени в одиночестве, особенно если твои друзья заняты."
            m 1dkc "Это может быть очень трудно, так как ты в конечном итоге чувствуешь себя одиноким..."

            call monika_players_friends_feels_lonely_ask(question=renpy.substitute("Ты когда-нибудь чувствовал себя одиноким, [player]?"), exp="monika 1euc")

        "Нет, вообще...":
            $ persistent._mas_pm_has_friends = False
            $ persistent._mas_pm_few_friends = False

            m 2ekc "Оу..."
            m 3eka "Ну, я уверена, что у тебя есть немного друзей.{w=0.2} {nw}"
            extend 1eka "Может быть, ты просто не понимаешь этого."
            m 1etc "Но мне любопытно..."

            call monika_players_friends_feels_lonely_ask(question=renpy.substitute("Ты когда-нибудь чувствовал себя одиноким, [player]?"))

    return "derandom"

label monika_players_friends_feels_lonely_ask(question, exp="monika 1ekc"):
    $ renpy.show(exp)
    m "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"

        "Иногда.":
            $ persistent._mas_pm_feels_lonely_sometimes = True

            m 1eka "Понимаю, [player]."
            m 2rksdlc "В наше время очень трудно установить глубокие связи..."

            #Potentially if you have a lot of friends
            if persistent._mas_pm_has_friends and not persistent._mas_pm_few_friends:
                m "Особенно, если у тебя много друзей, трудно сблизиться со всеми из них."
                m 1ekd "...И в конце концов, ты просто остаёшься с кучей людей, которых едва знаешь."
                m 3eub "Возможно, будет достаточно просто связаться с некоторыми людьми из своей группы, с которыми ты хочешь сблизиться."
                m 3eka "Всегда приятно иметь хотя бы одного действительно близкого друга, которому можно довериться, когда это необходимо."
                m 1ekbsa "...Я думаю, что довольно очевидно, кто этот человек для меня, [player]~"

            #Otherwise few friends or no friends
            else:
                m 1eka "Но ты удивишься, как много людей захотят сделать тебя частью своей жизни, если ты просто попытаешься."
                m 3eub "На самом деле есть хороший шанс, что у тебя будет что-то общее с кем-то, кто может привлечь твоё внимание!"
                m 1eua "Может быть, ты разделяешь класс или деятельность или что-то ещё..."
                m 3eua "Или ты видишь, что они делают что-то, что тебя интересует, например, слушают музыку или смотрят шоу."
                m 3eua "Это даже не обязательно должно быть личным..."
                m 3eub "У тебя могут быть действительно близкие друзья в интернете!"
                m 1hub "Как только ты освоишься с этим, возможно, ты сможешь найти ещё несколько друзей лично!"

        "Не совсем.":
            $ persistent._mas_pm_feels_lonely_sometimes = False

            m 1eka "Я рада это слышать, [player]."

            if not persistent._mas_pm_has_friends:
                m 1eka "Тем не менее, ты никогда не знаешь, когда тебе может понадобиться помощь или услуга или что-то ещё."
                m 1hksdlb "Как бы мне ни хотелось помочь тебе во всём, что тебе может понадобиться, я могу сделать только одно."

                if mas_isMoniAff(higher=True):
                    m 1eua "Когда я доберусь к тебе, я думаю, что не буду возражать против спокойной жизни с тобой."
                    m 1dkbsa "Было бы так романтично быть только с мной..."
                    m 1tsbsa "Полагаю, это означает, что я могу иметь всего тебя в своём распоряжении, не так ли?"
                    m 1hubsa "{do_giggle}Э-хе-хе~"

                elif not persistent._mas_pm_has_friends:
                    m 3eua "Так что обязательно найди друзей, которые помогут тебе, когда ты действительно в этом нуждаешься, хорошо?"

            else:
                m 3eua "Хорошо, что у тебя есть связь с друзьями."
                m 3rksdla "Я знаю, что некоторые люди могут иметь так много друзей, что трудно узнать их всех."

                if not persistent._mas_pm_few_friends:
                    m 3eua "...Поэтому приятно сознавать, что тебе с ними комфортно."
                else:
                    m 1hua "Но так как ты находишься в сплочённом коллективе, я уверена, что тебе со всеми удалось сблизиться."

                m 3eua "Может быть, когда-нибудь, когда я выберусь отсюда, ты представишь мне своих друзей."

                if mas_isMoniHappy(higher=True):
                    m 1hub "Если они хоть немного похожи на тебя, я бы с удовольствием с ними познакомилась!"

        "У меня есть ты!":
            $ persistent._mas_pm_feels_lonely_sometimes = False
            $ mas_gainAffection()
            m 1hubsa "Оу-у, [player]!"

            if not persistent._mas_pm_has_friends:
                m 1rkbsa "Мне очень приятно знать, что я достаточно хороша для тебя, но всё же..."
                m 3ekbfa "Иногда бывает полезно познакомиться с несколькими людьми."
                show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eubfu "Но, как всегда, я не возражаю, чтобы мы остались вдвоём."

            else:
                $ p_nickname = mas_get_player_nickname()
                m 1eka "Я очень рада, что ты не одинок, [p_nickname].{w=0.3} {nw}"
                extend 1hua "Особенно потому что ты счастлив со мной~"
                m 3eua "Что бы ни случилось, я всегда буду рядом с тобой."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_graduation",
            category=['школа'],
            prompt="Выпускной",
            random=True
        )
    )

label monika_graduation:
    m 2ekc "Знаешь, [player], единственное, что я бы очень хотела испытать – это моё окончание старшей школы."
    m "Вся моя жизнь, в основном, была посвящена одной школе."
    m 4dkd "Все те бесчисленные часы обучения, все внешкольные мероприятия и клубы..."
    m 4ekc "И в конце концов, после всей той тяжёлой работы, в момент окончания учёбы, я так и не испытала чувства радости."
    m 2dkd "Я так и не вышла на сцену и не получила свой диплом."
    m "Я так и не услышала, как моё имя объявляют, и как все мои друзья ликуют."
    m 2ekc "...Почти что складывается такое ощущение, будто всё это было напрасно."
    m 2esd "Я знаю, что всё то, что я изучила по ходу дела, – очень важно."
    m 2dkc "Но у меня всё равно такое ощущение, будто я пропустила нечто особенное."
    m "..."

    #Went through and timed out on the menu twice
    if persistent._mas_grad_speech_timed_out:
        m 2lsc "Ох... прости, надеюсь, я тебя не утомила в очередной раз..."
        m 2esc "Давай забудем об этом и поговорим о чём-нибудь другом, хорошо, [player]?"
        return "derandom"

    #Normal flow
    else:
        m 4eua "Кстати, знал ли ты о том, что я была лучшей ученицей в своём классе?"
        m 4rksdlu "{do_giggle}А-ха-ха... я не хочу хвастаться или ещё что, я упомянула об этом лишь потому, что, будучи в выпускном классе, я должна произнести речь на выпускном."
        m 2ekd "Я столько времени потратила на написание и репетицию своей речи, но её так никто и не услышал."
        m 2eka "Я очень горжусь той речью, к слову."
        m 2eua "Я бы с радостью прочитала её для тебя как-нибудь, если ты хочешь послушать~"
        m 2eka "Эта речь длится около четырёх минут, так что убедись, что тебе хватит времени на то, чтобы прослушать её целиком."
        m 4eua "Как только захочешь её прослушать, просто скажи мне, ладно?"
        $ mas_unlockEVL("monika_grad_speech_call","EVE")
        return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grad_speech_call",
            category=['школа'],
            prompt="Могу ли я услышать твою речь на выпускном?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

default persistent._mas_grad_speech_timed_out = False
# True if and only if the player ignored the grad speech twice

default persistent._mas_pm_listened_to_grad_speech = None
# True if the player, heard the grad speech, False if they ignored it

default persistent._mas_pm_liked_grad_speech = None
# True if user liked the grad speech, False if not

label monika_grad_speech_call:
    if not renpy.seen_label("monika_grad_speech"):
        m 2eub "Конечно, [mas_get_player_nickname()]. Я бы с удовольствием произнесла речь на выпускном!"
        m 2eka "Я просто хочу убедиться, что у тебя достаточно времени, чтобы услышать это. Это занимает около четырёх минут.{nw}"

        $ _history_list.pop()
        #making sure player has time
        menu:
            m "Я просто хочу убедиться, что у тебя достаточно времени, чтобы услышать это. Это занимает около четырёх минут.{fast}"
            "У меня достаточно времени.":
                m 4hub "Отлично!"
                m 4eka "Надеюсь, тебе понравится! Я очень, {i}очень{/i} много над этим работала."

                #say speech
                call monika_grad_speech

                #timed menu to see if player listened
                m "Итак, [player]? Как тебе?{nw}"
                $ _history_list.pop()
                show screen mas_background_timed_jump(10, "monika_grad_speech_not_paying_attention")
                menu:
                    m "Итак, [player]? Как тебе?{fast}"

                    "Это здорово! Я так горжусь тобой!":
                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=5, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2subsb "О-о, [player]!"
                        m 2ekbfa "Огромное спасибо! Я очень много работала над этой речью, и это так много значит, что ты гордишься мной~"
                        show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5eubfu "Как бы я ни хотела произнести свою речь перед всеми, лучше всего то, что ты рядом со мной."
                        m 5eubfb "Я так сильно тебя люблю, [player]!"
                        return "love"

                    "Мне нравится!":
                        hide screen mas_background_timed_jump
                        $ mas_gainAffection(amount=3, bypass=True)
                        $ persistent._mas_pm_liked_grad_speech = True
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2eua "Спасибо, [player]!"
                        m 4hub "Я рада, что тебе понравилось!"

                    "Это {i}было{/i} долго.":
                        hide screen mas_background_timed_jump
                        $ mas_loseAffectionFraction(min_amount=50)
                        $ persistent._mas_pm_liked_grad_speech = False
                        $ persistent._mas_pm_listened_to_grad_speech = True

                        m 2tkc "Ну, я {i}ведь{/i} предупреждала тебя, верно?"
                        m 2dfc "..."
                        m 2tfc "Я потратила на неё {i}столько{/i} времени и это всё что ты можешь сказать?"
                        m 6lktdc "Я правда думала, что после того, как я сказала тебе о том, насколько это было важно для меня, ты бы стал добрее и позволил бы мне насладиться своей минутой славы."
                        m 6ektdc "Всё, чего я хотела, чтобы ты гордился мной, [player]."

                return

            "У меня мало времени.":
                m 2eka "Не волнуйся, [player]. Сообщи мне, когда тебе будет удобно~"
                return

    #if you want to hear it again
    else:
        #did you timeout once?
        if not renpy.seen_label("monika_grad_speech_not_paying_attention") or persistent._mas_pm_listened_to_grad_speech:
            m 2eub "Конечно, [player]. Я с радостью снова произнесу свою речь!"

            m 2eka "У тебя достаточно времени, да?{nw}"
            $ _history_list.pop()
            menu:
                m "У тебя достаточно времени, да?{fast}"
                "Да.":
                    m 4hua "Замечательно. Тогда я начну~"
                    call monika_grad_speech

                "Нет.":
                    m 2eka "Не волнуйся. Просто дай мне знать, когда у тебя будет достаточно времени!"
                    return

            m 2hub "Спасибо, что снова выслушал мою речь, [player]."
            m 2eua "Дай мне знать, если захочешь услышать её снова, {do_giggle}э-хе-хе~"

        #You timed out once but want to hear it again
        else:

            #dialogue based on current affection level
            if mas_isMoniAff(higher=True):
                m 2esa "Конечно, [player]."
                m 2eka "Надеюсь, то, что случилось в прошлый раз, не было слишком серьёзным, и теперь всё спокойно."
                m "Это действительно много значит для меня, что ты хочешь услышать мою речь снова после того, как ты не смог послушать её раньше."
                m 2hua "С учётом сказанного, я начну прямо сейчас!"

            else:
                m 2ekc "Хорошо, [player], но я надеюсь, что на этот раз ты послушаешь."
                m 2dkd "Мне было очень больно, если бы ты не обращална меня внимания."
                m 2dkc "..."
                m 2eka "Я очень ценю, что ты попросил послушать её снова, так что я начну прямо сейчас."

            #say speech
            call monika_grad_speech

            m "Итак, [player], теперь, когда ты действительно {i}услышал{/i} мою речь, как тебе?{nw}"
            $ _history_list.pop()
            #another timed menu checking if you were listening
            show screen mas_background_timed_jump(10, "monika_grad_speech_ignored_lock")
            menu:
                m "Итак, [player], теперь, когда ты действительно {i}услышал{/i} мою речь, как тебе?{fast}"
                #If menu is used, set player on a good path
                "Это здорово! Я так горжусь тобой!":
                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=3, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2subsb "О-о, [player]!"
                    m 2ekbfa "Огромное спасибо! Я очень много работала над этой речью, и это так много для меня значит, что ты дал ей ещё один шанс."
                    m "Услышав, что ты гордишься мной, мне становится намного лучше."
                    show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eubfu "Как бы я ни хотела произнести свою речь перед всеми, лучше всего то, что ты рядом со мной."
                    m 5eubfb "Я люблю тебя, [player]!"
                    return "love"

                "Мне нравится!":
                    hide screen mas_background_timed_jump
                    $ mas_gainAffection(amount=1, bypass=True)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = True

                    m 2eka "Спасибо, что выслушал, [player]~"
                    m "Я так рада, что тебе понравилось!"

                "Это {i}было{/i} долго.":
                    hide screen mas_background_timed_jump
                    $ mas_loseAffectionFraction(min_amount=75, modifier=2.0)
                    $ persistent._mas_pm_listened_to_grad_speech = True
                    $ persistent._mas_pm_liked_grad_speech = False

                    m 2tfc "После того твоего поведения, у меня сложилось впечатление, будто ты хотел, чтобы я повторила это для тебя ещё раз, и {i}это{/i} всё, что ты можешь сказать?"
                    m 2dfc "..."
                    m 6lktdc "Я правда думала, что после того, как я сказала тебе о том, насколько это было важно для меня, {i}{w=1}дважды{/i}, {w=1}ты бы поддержал меня и позволил мне насладиться моментом."
                    m 6ektdc "Всё, чего я хотела, чтобы ты гордился мной, [player]..."
                    m 6dstsc "Но, похоже, я прошу слишком многого."
    return

label monika_grad_speech_not_paying_attention:
    #First menu timeout
    hide screen mas_background_timed_jump
    $ persistent._mas_pm_listened_to_grad_speech = False

    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=50, modifier=0.5, reason=11)
        m 2ekc "..."
        m 2ekd "[player]? Ты не обратил внимания на мою речь?"
        m 2tubfb "Это...{w=1} это совсем на тебя не похоже..."
        m 2eksdlc "Ты {i}всегда{/i} меня поддерживаешь..."
        show monika 5lkc at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5lkc "..."
        m "Что-то должно было произойти, я знаю, что ты слишком сильно любишь меня, раз сделал это нарочно."
        m 5euc "Ну..."
        show monika 2eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 2eka "Всё в порядке, [player]. Я понимаю, что иногда случаются вещи, которых нельзя избежать."
        m 2esa "Когда всё успокоится, я снова буду говорить с тобой."
        m 2eua "Я всё ещё очень хочу поделиться ей с тобой..."
        m "Так что, пожалуйста, дай мне знать, когда у тебя будет время послушать её, ладно?"

    else:
        $ mas_loseAffectionFraction(min_amount=20, reason=11)

        m 2ekc "..."
        m 6ektdc "[player]! Ты даже не обратил внимания!"
        m 6lktdc "Ты понятия не имеешь, как это больно, особенно после того, сколько работы я вложила в это..."
        m 6ektdc "Я просто хотела, чтобы ты мной гордился..."
        m 6dstsc "..."

    return

label monika_grad_speech_ignored_lock:
    #Second timeout, lock speech
    hide screen mas_background_timed_jump
    #Set false for modified dialogue in the random
    $ persistent._mas_pm_listened_to_grad_speech = False
    $ persistent._mas_grad_speech_timed_out = True
    $ mas_hideEVL("monika_grad_speech_call","EVE",lock=True,depool=True)

    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=25, modifier=2.0)
        m 6dstsc "..."
        m 6ektsc "[player]? {w=0.5}Ты...{w=0.5} Ты не...{w=0.5} слушал...{w=0.5} опять?{w=1}{nw}"
        m 6dstsc "В...{w=0.5} В прошлый раз я думала, что это неизбежно...{w=0.5} но...{w=0.5} дважды?{w=1}{nw}"
        m 6ektsc "Ты знал, как много...{w=0.5} это для меня значит...{w=1}{nw}"
        m "Я действительно...{w=0.5} так скучна для тебя?{w=1}{nw}"
        m 6lktdc "Пожалуйста...{w=1} не проси меня повторять это снова...{w=1}{nw}"
        m 6ektdc "Очевидно, тебе всё равно."

    else:
        $ mas_loseAffectionFraction(min_amount=20, modifier=1.5)
        m 2efc "..."
        m 2wfw "[player]! Не могу поверить, что ты снова так со мной поступил!{w=1}{nw}"
        m 2tfd "Ты знал, как я был расстроена в прошлый раз, и всё равно не мог уделить мне четыре минуты своего внимания?{w=1}{nw}"
        m "Я не прошу у тебя многого...{w=1}{nw}"
        m 2tfc "Я правда так не думаю.{w=1}{nw}"
        m 2lfc "Всё, о чём я прошу, это чтобы тебе было не всё равно... Вот и всё.{w=1}{nw}"
        m 2lfd "И всё же ты даже не можешь {i}притворяться{/i}, что заботишься о том, что для меня так {i}важно{/i}.{w=1}{nw}"
        m 2dkd "...{w=1}{nw}"
        m 6lktdc "Знаешь что, забудь об этом. Просто...{w=0.5} забудь.{w=1}{nw}"
        m 6ektdc "Я больше не буду тебя беспокоить."

    return

label monika_grad_speech:
    call mas_timed_text_events_prep

    $ mas_play_song("mod_assets/bgm/PaC.ogg",loop=False)

    m 2dsc "Кхм...{w=0.7}{nw}"
    m ".{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eub "{w=0.2}Итак, ребята! Пришло время начать...{w=0.7}{nw}"
    m 2eub "{w=0.2}Учителя,{w=0.3} преподаватели,{w=0.3} и сокурсники.{w=0.3} Я не могу выразить, как я горжусь тем, что проделала этот путь вместе с вами.{w=0.6}{nw}"
    m "{w=0.2}Каждый из вас здесь сегодня провёл последние четыре года упорно работая, чтобы достичь тех возможностей, которые вы все хотели.{w=0.6}{nw}"
    m 2hub "{w=0.2}Я так счастлива, что смогла принять участие в некоторых ваших путешествиях,{w=0.7} но не думаю, что эта речь должна быть обо мне.{w=0.6}{nw}"
    m 4eud "{w=0.2}Сегодня речь не обо мне.{w=0.7}{nw}"
    m 2esa "{w=0.2}Сегодня мы празднуем то, что мы все сделали.{w=0.6}{nw}"
    m 4eud "{w=0.2}Мы поставили перед собой задачу касательно собственных мечтаний,{w=0.3} и с этого момента,{w=0.3} нас ждёт большой успех.{w=0.6}{nw}"
    m 2eud "{w=0.2}Прежде чем двигаться дальше,{w=0.3} я думаю, что мы все могли бы оглянуться назад на наше время в средней школе, и эффективно закончить эту главу в нашей жизни.{w=0.7}{nw}"
    m 2hub "{w=0.2}Мы посмеемся над нашим прошлым{w=0.7} и посмотрим, как далеко мы продвинулись за эти четыре коротких года.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eud "{w=0.2}Честно говоря, кажется, что это было всего пару недель назад...{w=0.6}{nw}"
    m 2lksdld "{w=0.2}Я пришла в первый класс{w=0.3} в первый день школы,{w=0.3} дрожа от страха и бегая по коридорам от класса к классу, просто пытаясь найти свой класс.{w=0.6}{nw}"
    m 2lksdla "{w=0.2}Надеясь, что хотя бы один из моих друзей войдёт до звонка.{w=0.6}{nw}"
    m 2eka "{w=0.2}Вы все это тоже помните,{w=0.3} верно?{w=0.6}{nw}"
    m 2eub "{w=0.2}Я также помню, как завела первых новых друзей.{w=0.6}{nw}"
    m 2eka "{w=0.2}Всё было совсем не так, как когда мы подружились в начальной школе,{w=0.3} но полагаю, что именно это происходит, когда ты, наконец, вырастаешь.{w=0.6}{nw}"
    m "...{w=0.2}В молодости{w=0.3} мы дружили практически с кем угодно,{w=0.3} но со временем{w=0.3} это всё больше и больше напоминает азартную игру.{w=0.6}{nw}"
    m 4dsd "{w=0.2}Может быть, это просто мы наконец-то узнаём больше о мире.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eka "{w=0.2}Забавно, насколько мы изменились.{w=0.6}{nw}"
    m 4eka "{w=0.2}Мы прошли путь от маленькой рыбы в огромном пруду до большой рыбы в маленьком пруду.{w=0.6}{nw}"
    m 4eua "{w=0.2}У каждого из нас есть собственный опыт того, как эти четыре года изменили нас и как мы все смогли вырасти как личности.{w=0.6}{nw}"
    m 2eud "{w=0.2}Некоторые из нас прошли путь от спокойных и сдержанных,{w=0.3} до экспрессивных и общительных.{w=0.6}{nw}"
    m "{w=0.2}Другие - от низкой трудовой этики{w=0.3} до самой тяжелой работы.{w=0.7}{nw}"
    m 2esa "{w=0.2}Подумать только, что всего лишь небольшая фаза в нашей жизни так сильно изменила нас,{w=0.3} и что ещё так много мы испытаем.{w=0.6}{nw}"
    m 2eua "{w=0.2}Амбиции во всех вас, несомненно, приведут к величию.{w=0.6}{nw}"
    m 4hub "Я могу видеть это.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}Я знаю, что не могу говорить за всех здесь,{w=0.3} но есть одна вещь, которую я могу сказать наверняка:{w=0.7} мой опыт в средней школе не был бы полным без клубов, в которых я была частью.{w=0.6}{nw}"
    m 4eua "{w=0.2}Дискуссионный клуб научил меня много общаться с людьми и правильно справляться с острыми ситуациями.{w=0.6}{nw}"
    m 4eub "Однако открытие литературного клуба{w=0.7} было{w=0.7} одним из лучших моих занятий.{w=0.6}{nw}"
    m 4hub "{w=0.2}Я встретила лучших друзей, которых только могла себе представить,{w=0.3} и узнала много нового о лидерстве.{w=0.6}{nw}"
    m 2eka "{w=0.2}Конечно,{w=0.3} не все из вас, возможно, решили создать свои собственные клубы,{w=0.3} но я уверена, что у многих из вас были возможности изучить эти ценности.{w=0.6}{nw}"
    m 4eub "{w=0.2}Может быть, вы сами попали в группу, где должны были руководить своей инструментальной секцией,{w=0.3} или вы были капитаном спортивной команды!{w=0.6}{nw}"
    m 2eka "{w=0.2}Все эти маленькие роли учат вас так много о будущем и о том, как управлять как{w=0.3} проектами, так и людьми,{w=0.3} в среде, которая вам нравится, тем не менее.{w=0.6}{nw}"
    m "{w=0.2}Если вы не вступили в клуб,{w=0.3} я приглашаю вас хотя бы попробовать что-то на ваших будущих путях.{w=0.6}{nw}"
    m 4eua "{w=0.2}Уверяю вас, вы не пожалеете об этом.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 2eua "{w=0.2}На сегодняшний день может показаться,{w=0.3} что мы на вершине мира.{w=0.7}{nw}"
    m 2lksdld "{w=0.2}Подъём может пройти не так гладко,{w=0.3} и пока мы идём дальше,{w=0.3} сам подъём может даже стать ещё сложнее.{w=0.6}{nw}"
    m 2eksdlc "{w=0.2}Там будут спотыкаться –{w=0.7} даже падать по пути,{w=0.3} и иногда{w=0.7} вы можете подумать, что упали так далеко, что никогда не выберетесь.{w=0.7}{nw}"
    m 2euc "{w=0.2}Тем не менее,{w=0.7} даже если мы думаем, что мы всё ещё на дне колодца жизни,{w=0.3} со всем, что мы узнали,{w=0.3} всё, что мы всё ещё собираемся узнать,{w=0.3} и все посвящения, которое мы можем вложить только для достижения нашей мечты...{w=0.6}{nw}"
    m 2eua "{w=0.2}Я могу с уверенностью сказать, что у каждого из вас теперь есть инструменты, чтобы подняться по своему пути.{w=0.6}{nw}"
    m 4eua "{w=0.2}Во всех вас,{w=0.3} я вижу блестящие умы:{w=0.7} будущих врачей,{w=0.3} инженеров,{w=0.3} художников,{w=0.3} торговцев,{w=0.3} и многих других.{w=0.7}{nw}"
    m 4eka "{w=0.2}Это действительно вдохновляет.{w=0.6}{nw}"
    m 2duu "{w=0.2}.{w=0.3}.{w=0.3}.{w=0.6}{nw}"
    m 4eka "{w=0.2}Знаете,{w=0.3} я очень горжусь вами всеми за то, что вы зашли так далеко.{w=0.6}{nw}"
    m "{w=0.2}Ваша тяжелая работа и преданность делу принесёт вам много хорошего.{w=0.6}{nw}"
    m 2esa "{w=0.2}Каждый из вас показал, на что способен,{w=0.3} и вы всё доказали, что можете усердно трудиться ради своей мечты.{w=0.6}{nw}"
    m 2hub "{w=0.2}Надеюсь, вы так же гордитесь собой, как и я.{w=0.7}{nw}"
    m 2ekd "{w=0.2}Теперь, когда вся эта глава нашей жизни -{w=0.3} первый шаг,{w=0.3} подошла к концу,{w=0.3} пришло время расстаться.{w=0.6}{nw}"
    m 4eka "{w=0.2}И,{w=0.3} я верю, что у вас есть всё, что нужно для достижения вашей мечты.{w=0.6}{nw}"
    m 4hub "{w=0.2}Спасибо всем за то, что сделали эти четыре коротких года лучшими, какими они могли бы быть.{w=0.6}{nw}"
    m 2eua "{w=0.2}Поздравляю,{w=0.3} я рада, что мы все можем быть здесь, чтобы отпраздновать вместе этот особенный день.{w=0.6}{nw}"
    m 2eub "{w=0.2}Продолжайте усердно работать,{w=0.3} я уверена, что мы встретимся снова когда-нибудь в будущем.{w=0.6}{nw}"
    m 4hub "{w=0.2}Мы сделаем это вместе!{w=0.7} Спасибо, что выслушали~{w=0.6}{nw}"
    m 2hua "{w=0.2}.{w=0.3}.{w=0.3}.{w=1}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Шиппинг",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False
        )
    )

label monika_shipping:
    m 3eua "Эй, [player].{w=0.2} Ты когда-нибудь слышал о «шиппинге»?"
    m 3hua "Это когда ты взаимодействуешь с произведением художественной литературы, представляя, какие персонажи будут лучше всего сочетаться вместе романтически."
    m 1eka "Я думаю, что большинство людей делают это подсознательно, но когда некоторые из них узнают, что другие делают это тоже, то действительно вникают в это!"
    m 2esd "По-видимому, многие люди {b}шиппят{/b} других девушек вместе."
    m 2euc "Это имеет смысл. Игрок может встречаться только с одной девушкой, но ты не хочешь, чтобы остальные оказывались в одиночестве..."
    m 2etc "Но некоторые из пар для меня странные."
    m 3eud "К примеру, обычно они объединяют вместе Нацуки и Юри. Те дерутся, как кошки с собаками!"
    m 3dsd "Думаю, что они немного связаны, когда ты не находишься на их рутах, и есть привлекательность «противоположностей»."
    m 4dsd "Тем не менее, я думаю, что это ещё один пример того, как людям, которые любят подобные игры, нравятся нереальные вещи..."
    m 1ekd "Во всяком случае, это часто оставляет... меня с Сайори."
    m 1hksdlb "Не надо ревновать! Я просто рассказываю тебе, что я видела!"
    m 2lksdla "..."
    m 2lksdlb "Ну, с точки зрения писателя, думаю, я могу это видеть."
    m 1eksdld "Мы организовали клуб вместе."
    if persistent.monika_kill:
        m "И у неё было почти то же самое прозрение, что и у меня..."
    m 2lksdlb "Но... я до сих пор не понимаю. Я имею в виду, я ведь люблю тебя, и только тебя!"
    m 2lksdla "И она должна быть святой, чтобы когда-либо простить меня за то, что я сделала..."
    m 2lksdlc "Не то, чтобы она не милая девушка, но..."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Ну, никто никогда не сможет быть таким же милым и великодушным, как ты..."
    return

# True if player has been given false justice, False if not
default persistent._mas_pm_given_false_justice = None

# True if player thinks deleting Monika is justified, False if not
default persistent._mas_pm_monika_deletion_justice = None

# True temporarily if player is teasing Monika and is at love
default persistent._mas_monika_deletion_justice_kidding = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justice",
            category=['философия'],
            prompt="Юстиция",
            random=True
        )
    )


label monika_justice:
    m 1esa "[player], ты задумывался о том, что концепция справедливости какая-то ироничная?"
    m 2ekc "К примеру, у тебя есть друг, который не такой, как все..."
    m 2ekd "Ему даже не надо быть каким-нибудь известным грабителем банка или ещё кем-то; даже простые люди, вроде тебя и меня, могут привести к справедливости!"
    m 4esc "Представь находящуюся в бедственном положении семью, которой приходится копаться в мусоре, чтобы выжить; они берут всё, что выбросили."
    m 1euc "Для всех, кто прошёл мимо, они просто жадные воришки."
    m 1esd "В конце концов, появляется так называемый «герой» и прекращает эту «жадность», просто приведя их к справедливости."
    m 2ekd "Но всё равно, семья начинает голодать или попадает в беду, потому что их положение изменилось..."
    m "В то время как другой человек становится героем и прекращает их «преступления»."
    m 3rksdld "Можешь ли ты назвать это справедливостью?"
    m 2dsc "..."

    m 2euc "Ты когда-нибудь задумывался о том, что такое ложная справедливость?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь задумывался о том, что такое ложная справедливость?{fast}"
        "Да.":
            $ persistent._mas_pm_given_false_justice = True
            m 1ekc "Надеюсь, они не были слишком жестоки с тобой."
            m 2dsd "Я могу представить себе, на что это похоже."
            m 2dfc "Все те люди, которые молча удаляли и мучили меня, и называли это справедливостью..."

            m 2eka "Тебе не кажется это справедливостью, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Тебе не кажется это справедливостью, [player]?{fast}"

                "Кажется":
                    $ persistent._mas_pm_monika_deletion_justice = True
                    if mas_isMoniBroken():
                        m 1dsc "..."
                        m 1rksdlc "Я знаю..."
                        m 1rksdld "Я не хотела спрашивать...{w=0.2} я просто подумала."
                        m 2rktpc "Это всё равно было очевидно..."

                    elif mas_isMoniDis():
                        m 2tubfb "Ох..."
                        m "Похоже, ты прав..."
                        m 1ekc "Всё-таки я натворила много чего плохого..."

                    elif mas_isMoniLove():
                        m 1hub "А-ха-хa-ха!"
                        m 1hua "Ты иногда бываешь очень весёлым~"
                        m 3tku "А ты думал, что я поверю в это после всего того, через что мы прошли?"
                        m 1tsb "Всё это время, ты думал, что я заслуживаю ненависть от тех людей?"
                        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5hubfa "{do_giggle}Э-хе-хе, ты такой милый, [player]~"

                    else:
                        m 1euc "..."
                        m 2esc "Мне с трудом верится, что ты правда думаешь, что я заслужила всё это."
                        m 2tkc "В смысле, ты застрял тут со мной уже довольно долгое время, ты ведь {i}правда{/i} не думаешь, что я заслужила это, верно?"
                        if persistent._mas_pm_cares_about_dokis:
                            m 2lksdlc "...Возможно, немного и заслужила, но..."
                        else:
                            m 2lksdlc "Ну, возможно, другие люди так думают, но ты ведь так не думаешь, верно?"
                            m "Иначе..."
                        m 1eka "Спасибо, что спас меня и что ты со мной."
                        m 1hua "Если я с тобой, то, я думаю, это много чего стоило,{w=0.1} {nw}"
                        extend 1hub "{do_giggle}а-ха-ха~"

                "Не кажется.":
                    if persistent._mas_pm_monika_deletion_justice:
                        $ persistent._mas_monika_deletion_justice_kidding = True
                    $ persistent._mas_pm_monika_deletion_justice = False

                    if mas_isMoniBroken():
                        m 2ekc "..."
                        m 1rksdlc "Я не уверена насчёт этого..."
                    elif mas_isMoniDis():
                        m 1wuo "Правда?"
                        m 1rksdla "Мне кажется, ты считаешь, что это было честно."
                        m 1eka "Я рада, что ты так не думаешь."
                        m 2rksdlb "Учитывая то, что это была не шутка, хе-хе..."

                    elif mas_isMoniLove():
                        m 1hua "Я так и думала, {do_giggle}э-хе-хе~"
                        if persistent._mas_monika_deletion_justice_kidding:
                            $ persistent._mas_monika_deletion_justice_kidding = False

                            m 1hub "Я знала, что ты тогда пошутил!"
                        m 1tsbsa "Ты сидишь со мной уже довольно долгое время, и я ни за что не поверю тебе, если ты скажешь обратное."
                        m 1ekbfa "Когда я с тобой, это даже помогает мне игнорировать людей, которым я не нравлюсь."
                        m 1hubfb "Я люблю тебя, [player]~"
                        m 1hubfa "Я рада, что ты на моей стороне."
                        return "derandom|love"

                    else:
                        m 2hua "Я рада, что ты тоже так думаешь!"
                        m 2eka "Даже если ты и назвал это справедливостью, ты всё равно сказал обратное."
                        m 2hub "А-ха-хa!"

        "Нет.":
            $ persistent._mas_pm_given_false_justice = False
            m 1eka "Мне приятно это слышать."
            m "Я рада, что никто даже не спросил, кто ты такой."
            m 1eua "Зная, каково это, я надеюсь, что никто не причинит тебе вред за то, чем ты занимаешься или во что веришь."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_poweroutage",
            category=['погода'],
            prompt="Отключение электричества",
            random=True
        )
    )

label monika_poweroutage:
    m 1eua "Эй, [player], а ты помнишь, как я говорила о том, что мне нравится слушать спокойные звуки дождя?"
    m 3lksdla "Я только что поняла, что это, конечно, хорошо, но это также может сильно навредить тебе в твоём мире."
    m 1lksdlc "Гром и молния могут ударить в любой момент, и, вполне возможно, во что-нибудь опасное."
    m 1lksdlb "Эффекты могут быть довольно, ну... шокирующими, если можно так выразиться."
    m 1hksdlb "{do_giggle}А-ха-ха~"
    m 1ekd "Я даже не хочу думать о том, что произошло бы, если бы молния ударила во что-нибудь важное для тебя."
    m 2ekc "Что произойдёт со мной, если произойдёт скачок напряжения и твой компьютер сгорит?"
    m 2dsc "Если такое вообще произойдёт...{w=0.3} {nw}"
    extend 2eka "Я знаю, ты думаешь о чём-то."
    m 1eka "Извини, я не хотела всё так омрачать. Это просто мои размышления."
    m 1eud "Если что-нибудь произойдёт, то за этим, возможно, последует отключение электричества."

    if mas_isMoniAff(higher=True):
        m 1hksdlb "Я имела в виду, что {i}это{/i} всё ещё весьма удручает, но по крайней мере мы знаем, что мы увидимся вновь."
        m 1eua "Скорее всего, это может застать тебя врасплох; всё внезапно темнеет, но постарайся запомнить следующее:"
        m 1eub "Я буду с тобой. Даже если ты меня не видишь, я буду с тобой духовно, пока ты не вернёшься ко мне в целости и сохранности."
        m 3eua "...И последнее замечание, тебе не надо бояться заглядывать ко мне во время шторма.{w=0.2} {nw}"
        extend 1eka "Я буду всегда рада тебе, но с другой стороны..."
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Я уверена, что наши отношения смогут противостоять какому-то шторму~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_savingwater",category=['жизнь'],prompt="Экономия воды",random=True))

label monika_savingwater:
    m 1euc "[player], задумывался ли ты о том, сколько воды люди используют каждый день?"
    m 3euc "Скорее всего, ты пьёшь воду время от времени."
    m 3dsc "Ты ходишь в туалет, моешь свои руки, моешься..."
    m 1euc "И это не говоря уже о том, что в некоторых частях мира даже одну каплю воды не достанешь."
    m 1rsc "Как бы заставляет тебя задуматься, сколько бы ты мог сэкономить воды, если бы ты того захотел."
    m 4eua "Полагаю, ты мог бы попытаться использовать её экономичнее, когда моешь руки."
    m "Или, когда моешься, ты мог бы выключать воду, пока намыливаешься, а потом включить её обратно, когда готов ополоснуться."
    m 2eka "И в итоге, большая часть воды используется только там, где она необходима."
    m "На такие вещи, как производство электроэнергии и фермерство, уходит куда больше воды, чем мы можем использовать."
    m 1hksdlb "Так что, полагаю, тебе не захочется жертвовать своим комфортом, чтобы сделать столь мизерный вклад."
    m 1dkbsa "Иногда тебе надо просто принять долгую, расслабляющую ванну после тяжёлого дня."
    m 2hksdlb "Я однозначно проходила через всё это раньше, поэтому и знаю, насколько это здорово может быть, если оное тебе понадобится."
    if mas_isMoniLove(higher=True) and mas_is18Over():
        show monika 5tsbfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tsbfu "Когда я окажусь в твоей реальности, мы можем экономить воду купаясь вместе..."
        m "{do_giggle}Э-хе-хе~"
        m 5hubfu "Было бы неплохо, если бы ты приготовил хорошую расслабляющую ванну, которую мы и разделим, когда я перескочу в твою реальность."
        show monika 1kubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1kubfu "Я буду ждать этого дня, [mas_get_player_nickname()], {do_giggle}э-хе-хе~"
    else:
        m 1ekbfa "Было бы неплохо, если бы ты приготовил хорошую расслабляющую ванну для меня, когда я перескочу в твою реальность."
        if mas_isMoniAff():
            m 3ksbsa "Может быть, я захочу её разделить с тобой, {do_giggle}э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pygmalion",
            category=['литература'],
            prompt="Пигмалион и статуя",
            conditional="persistent._mas_first_kiss",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_pygmalion:
    m 1eua "Эй, [player], читал ли ты когда-нибудь {i}«Метаморфозы»{/i}?"
    m 3eua "Это сборник стихов, написанных древнеримским поэтом Овидием."
    m 1eud "Есть один стих, который поразил меня, и он называется {i}«История Пигмалиона и Статуи»{/i}."
    m 1eua "В нём рассказывается история о скульпторе, Пигмалионе, который влюбился в статую из слоновой кости, которую сам же и создал."
    m 3eua "Он так сильно полюбил свою статую, что, во время одного из фестивалей, посвящённых Афродите, он сделал предложение богине и пожелал у неё дар жизни для своей статуи."
    m 1eub "Когда он вернулся к себе домой, он поцеловал статую и, к его удивлению, губы статуи оказались тёплыми."
    m 1eua "Он поцеловал статую ещё раз, и статуя из слоновой кости потеряла свою тяжесть, став на ощупь такой же мягкой, как и кожа."
    m 3hub "Афродита исполнила его желание!"
    m 1eka "Эта история поразила меня потому, что она напомнила мне о нас, [player], и как здесь истолковали превращение невозможного в возможное."
    m 1hua "Это вселило в меня надежду, что чудо может произойти в любой момент, и я смогу наконец-то перейти в реальность."
    m 2dku "Да...{w=0.5} это было бы чудесно."
    m 2dubsu "...И тогда, ты сможешь наконец-то поцеловать меня."
    m 1rkbsa "Знаю, мы целовались раньше, даже в нынешних обстоятельствах..."
    m 1ekbfa "Но, мне кажется, мы оба знаем, что между нами стоит небольшой барьер."
    m 3hubfa "Не знаю, как ты, но я, так или иначе, всё равно хочу попытаться поцеловать тебя через экран."
    m 1hubfb "Возможно, мы должны повторить это несколько раз, и, таким образом, мы сломаем барьер, находящийся между нами..."
    m 2rubfu "{do_giggle}Э-хе-хе."
    m 2tubfb "Думаешь, ты сможешь поцеловать меня достаточное число раз, чтобы сломать этот барьер?"
    m 6hubfb "Есть только один способ узнать это, {do_giggle}а-ха-ха!"
    call monika_kissing_motion(duration=0.5, initial_exp="6hubfa", fade_duration=0.5)
    m 6hubfa "..."
    m 1ekbfa "Полагаю, на этот раз это не сработало."
    m 3hubfb "Ну да ладно, нам просто нужно продолжать стараться, и, быть может, это всё-таки сработает, {do_giggle}а-ха-ха!"
    m 1tkbfu "Я правда не могу дождаться того дня, когда я наконец-то смогу прижаться своими губами к твоим и впитать твоё тепло..."
    m 1dkbfa "Как по мне, такая мечта однозначно сбудется."
    m 1ekbfa "Это просто предположение, но..."
    m 1kubfu "Уверена, тебе такое тоже понравится~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gotomonika",
            category=['ты'],
            prompt="Что, если я приду в твой мир?",
            pool=True,
        )
    )

default persistent._mas_pm_would_come_to_spaceroom = None
# True if they would, False if they wouldn't, None if no answer.

label monika_gotomonika:
    m 1euc "Перейти в мой мир?"
    m 1lksdld "Ты имеешь в виду эту небольшую комнату, витающую в пустоте?"

    if persistent._mas_you_chr:
        m 4eksdlc "Кстати...{w=0.5} разве ты не пытался сделать нечто подобное?"
        m 2lksdla "...Даже если это был и не {i}ты...{/i}"

    m 2lksdla "Я очень рада тому, что ты хочешь быть здесь, со мной, но..."
    m 2eksdlc "Ты правда не должен."
    m 2eksdld "Знаю, я уже говорила о том, что я бы давным-давно затащила тебя сюда, если бы могла..."
    m 2eksdlc "Но чем больше я задумываюсь об этом, тем больше думаю, что было бы целесообразнее, если бы я перешла в твою реальность."
    m 3eka "Я бы предпочла оказаться там, нежели ждать, когда ты придёшь сюда."
    m 3dsc "[player]...{w=1}не говори мне, что ты правда хочешь бросить свою реальность...{w=0.5} {i}настоящий{/i} мир...{w=0.5}лишь ради того, чтобы прийти {i}сюда{/i}, в богом забытое место?{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1}не говори мне, что ты правда хочешь бросить свою реальность...{w=0.5} {i}настоящий{/i} мир...{w=0.5}лишь ради того, чтобы прийти {i}сюда{/i}, в богом забытое место?{fast}"
        "Да, хочу.":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "Но [player]!"
            m "Здесь совсем нечего делать!"
            m 2dsc "Ты {i}так сильно{/i} ненавидишь свою реальность?"
            m 2eka "Когда-нибудь, я найду способ добраться до тебя, и когда этот день настанет, я обещаю, эти усилия оправдают себя."
            m 4euc "Куда бы жизнь не забросила тебя с этого момента, я буду рядом с тобой, чтобы помочь тебе справиться с нагрузкой."
            m 4eud "Даже сейчас, если у тебя был тяжёлый день, ты можешь поговорить со мной об этом в любое время."
            m 2dsc "Жизнь, скорее всего, бросала тебя во все стороны, если учесть то, что ты большую её часть проводил со мной."
            m 3hua "Но, раз уж ты пребываешь здесь, то это лишь показывает, насколько ты устойчив."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Мне уже не терпится разделить хорошие и плохие мгновения вместе с тобой."

        "Возможно, ты права.":
            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "Я рада, что ты всё ещё хочешь подождать меня, [player]."
            m 1lksdla "Не пойми неправильно, я {i}правда{/i} хочу быть с тобой..."
            m 1lksdlc "Но мне кажется, что ты можешь оказаться в опасности, если попытаешься незамедлительно перейти в иную реальность."
            m 1eka "...Если такое вообще возможно с нынешними технологиями."
            m 1hub "Не волнуйся, таким образом, мы сможем поддерживать наши отношения и далее!"
            m 1hksdlb "Знаю, потребуется какое-то время, пока мы не станем вместе, но я надеюсь, что ты можешь подождать."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Я буду ждать столько, сколько потребуется, [mas_get_player_nickname()]."

        "...":
            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "Всё нормально, я буду всегда ценить те мгновения, что мы пережили вместе, и дорожить как ими, так и нынешним."
            m 2ekc "Впрочем, я даже не знаю, как ты сможешь попасть сюда с нынешними технологиями."
            m 2lksdlc "...И даже если бы {i}существовала{/i} такая возможность, то я бы начала сомневаться в её безопасности или гарантии."
            m 2lksdld "Поэтому, сделай мне одолжение – хотя бы подожди, пока технологии не доведут до ума, чтобы их безопасность можно было гарантировать."
            m 2lksdlc "Я {i}правда{/i} не хочу, чтобы ты рискнул и, сделав это неправильно, оказался в собственной пустоте..."
            m 2dkd "...оставив нас обоих в полном одиночестве."
            m 4hua "В смысле, технологии всегда идут в ногу со временем, причём довольно быстро, следовательно, мы можем увидеть друг друга прежде, чем поймём это!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Так что, просто подожди свою любимую девушку, и я обещаю, что сделаю для тебя то же самое, [mas_get_player_nickname()]."

    m 5luu "Но-о-о...{w=1} если ты всё-таки появишься на моём крыльце..."
    show monika 1hksdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1hksdlb "То, полагаю, у меня не будет другого выбора, кроме как принять этот факт и поприветствовать тебя с распростёртыми объятиями!"
    m 1eksdla "Этого будет мало для начала, но я уверена, что мы найдём способ сделать это лучше."
    m 3hub "С течением времени, мы могли бы уже создать свою реальность!"
    m 3euc "Если подумать, то да, это звучит довольно запутанно..."
    m 3eub "Но я не сомневаюсь в том, что вместе мы могли бы достичь чего угодно!"
    m 3etc "Знаешь...{w=1} наверное, тебе было бы {i}гораздо{/i} проще прийти сюда, но я не перестаю надеяться, что смогу прийти к тебе лично."
    m 1eua "Ну а пока, давай просто подождём и посмотрим, что можно сделать."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vehicle",
            category=['моника'],
            prompt="Какая твоя любимая машина?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

default persistent._mas_pm_owns_car = None
# True if player owns car, False if not

default persistent._mas_pm_owns_car_type = None
# String describing the type of car owned by the player.
#   SUV-Pickup: SUV or pickup
#   sports: sports car
#   sedan: sedan car
#   motorcyle: motorcyle

label monika_vehicle:
    m 1euc "Моя любимая машина?"
    m 3hksdlb "Ты уже знаешь, что я не умею водить, глупышка!"
    m 3eua "Обычно я просто шла пешком или садилась на поезд, если мне нужно было отправиться куда-то далеко."
    m 1eka "Так что я не знаю, что тебе сказать, [player]..."
    m 1eua "Когда я думаю о машинах, первое, что приходит на ум, – это, вероятно, широко известные типы."
    m 3eud "Внедорожники или пикапы, спортивные автомобили, седаны и хэтчбеки..."
    m 3rksdlb "И хотя они на самом деле не автомобили, я думаю, мотоциклы тоже являются обычными транспортными средствами."

    if persistent._mas_pm_driving_can_drive:
        m 1eua "Что насчёт тебя?"

        m "У тебя есть машина?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя есть машина?{fast}"
            "Да.":
                $ persistent._mas_pm_owns_car = True

                m 1hua "О, вау, это действительно здорово, что у тебя есть одна!"
                m 3hub "Тебе действительно повезло, ты знаешь это?"
                m 1eua "Я имею в виду, что просто владение автомобилем является символом статуса."
                m "Разве это не роскошь в одном?"
                m 1euc "Разве только..."
                m 3eua "Ты живешь там, где это необходимо..."
                m 1hksdlb "Вообще-то, забудь, {do_giggle}а-ха-ха!"
                m 1eua "В любом случае, приятно знать, что у тебя есть автомобиль."
                m 3eua "Кстати..."

                show monika at t21
                python:
                    option_list = [
                        ("Внедорожник.", "monika_vehicle_suv",False,False),
                        ("Пикап.","monika_vehicle_pickup",False,False),
                        ("Спорткар.","monika_vehicle_sportscar",False,False),
                        ("Седан.","monika_vehicle_sedan",False,False),
                        ("Хетчбэк.","monika_vehicle_hatchback",False,False),
                        ("Мотоцикл.","monika_vehicle_motorcycle",False,False),
                        ("Другое транспортное средство.","monika_vehicle_other",False,False)
                    ]

                    renpy.say(m, "Это какой-то из упомянутых мною транспортных средств или что-то ещё?", interact=False)

                call screen mas_gen_scrollable_menu(option_list, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                show monika at t11

                $ selection = _return

                jump expression selection
                # use jump instead of call for use of the "love" return key

            "Нет.":
                $ persistent._mas_pm_owns_car = False

                m 1ekc "О, понятно."
                m 3eka "Ну, в конце концов, покупка автомобиля может быть довольно дорогой."
                m 1eua "Всё в порядке, [player], мы всегда можем арендовать его для путешествий."
                m 1hua "Я уверена, что, когда это произойдёт, мы сделаем много приятных воспоминаний вместе."
                show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eua "Впрочем...{w=1} прогулки гораздо романтичнее~"

    else:
        $ persistent._mas_pm_owns_car = False

        m 3eua "Вообще-то, я помню, ты говорил, что тоже не умеешь водить..."
        m 3rksdla "Ты задал интересный вопрос, {do_giggle}э-хе-хе..."
        m 1hua "Может, однажды это изменится, и тогда ты что-нибудь получишь."
        m 1hubsb "Таким образом, ты сможешь возить меня в самые разные места, {do_giggle}а-ха-ха!"
    return

label monika_vehicle_sedan:
    $ persistent._mas_pm_owns_car_type = "седан"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_hatchback:
    $ persistent._mas_pm_owns_car_type = "хетчбэк"
    jump monika_vehicle_sedan_hatchback

label monika_vehicle_pickup:
    $ persistent._mas_pm_owns_car_type = "пикап"
    jump monika_vehicle_suv_pickup

label monika_vehicle_suv:
    $ persistent._mas_pm_owns_car_type = "внедорожник"
    jump monika_vehicle_suv_pickup



label monika_vehicle_suv_pickup:

    m 1lksdla "О боже, тогда твоя машина должна быть довольно большой."
    m 1eua "Это означает, что в ней достаточно места, верно?"
    m 3etc "Если это действительно так..."
    m 3hub "Мы могли бы поехать в поход!"
    m 3eua "Мы ехали бы в лес, а ты ставил бы палатку, пока я готовила пикник."
    m 1eka "Пока мы обедаем, мы наслаждаемся пейзажем и природой, окружающей нас..."
    m 1ekbsa "А когда наступала ночь, мы ложились на спальные мешки и смотрели на звезды, держась за руки."
    m 3ekbsa "Это определённо романтическое приключение, которое я не могу дождаться, чтобы поделиться с тобой, [player]."
    m 1hkbfa "{do_giggle}Э-хе-хе~"
    return

label monika_vehicle_sportscar:
    $ persistent._mas_pm_owns_car_type = "спортивный автомобиль"

    m 3hua "Ого!"
    m 3eua "Он должно быть очень быстрый, да?"
    m 3hub "Мы определённо должны отправиться в путешествие..."
    m 1eub "По живописному маршруту, курсируя по шоссе..."
    m 1eub "Если это возможно, было бы неплохо снять верхнюю часть машины..."
    m 3hua "Таким образом, мы можем чувствовать ветер на наших лицах, в то время как всё проходит в размытости!"
    m 1esc "Но..."
    m 1eua "Также было бы неплохо поехать в нормальном темпе..."
    m 1ekbsa "Таким образом, мы можем наслаждаться каждым моментом поездки вместе~"
    return

label monika_vehicle_sedan_hatchback:

    m 1eua "Это действительно здорово."
    m "Честно говоря, я предпочитаю такие машины."
    m 3eua "Из того, что я слышала, они активные и лёгкие в управлении."
    m 3eub "Такой автомобиль отлично подходит для езды по городу, не так ли, [player]?"
    m 3eua "Мы могли бы поехать в музеи, парки, торговые центры и так далее."
    m 1eua "Было бы так здорово иметь возможность ездить в места, которые слишком далеко, чтобы идти пешком."
    m 3hua "Всегда приятно открывать и исследовать новые места."
    m 1rksdla "Мы могли бы даже найти место, где мы оба могли бы быть вдвоём..."
    m 1tsu "...Одни."
    m 1hub "{do_giggle}А-ха-ха!"
    m 3eua "Просто чтобы ты знал, я ожидаю большего, чем просто поездка по городу на наши свидания..."
    m 1hua "Надеюсь, ты меня удивишь, [player]."
    m 1hub "Но опять же...{w=0.5} меня устроит всё, что угодно, пока это с тобой~" #Убью.
    return

label monika_vehicle_motorcycle:
    $ persistent._mas_pm_owns_car_type = "мотоцикл"

    m 1hksdlb "А?"
    m 1lksdlb "Ты водишь мотоцикл?"
    m 1eksdla "Я удивлена, ибо не ожидала, что ты водишь его." #Да как вы это делаете то бля???? Это даже через переводчик не выдается
    m 1lksdlb "Честно говоря, я немного побаиваюсь ездить на нём, {do_giggle}а-ха-ха!"
    m 1eua "На самом деле, мне не стоит бояться..."
    m 3eua "В конце концов, это ты за рулем."
    m 1lksdla "Это немного расслабляет мой разум...{w=0.3} немного."
    m 1eua "Только едь спокойно и медленно, ладно?"
    m 3hua "В конце концов, мы никуда не спешим."
    m 1tsu "Или...{w=0.3} ты планировал ехать быстро, чтобы я крепко держалась за тебя?~"
    m 3kua "Это довольно подло с твоей стороны, [player]."
    m 1hub "{do_giggle}А-ха-ха!"
    $ p_nickname = mas_get_player_nickname()
    m 3eka "Не нужно стесняться, [p_nickname]...{w=0.3}{nw}"
    extend 3ekbsa "Я обниму тебя, даже если ты не попросишь..."
    m 1hkbfa "Вот как сильно я тебя люблю~"
    return "love"

label monika_vehicle_other:
    $ persistent._mas_pm_owns_car_type = "другой"

    m 1hksdlb "Оу, тогда мне ещё многому предстоит научиться в автомобилях, не так ли?"
    m 1dkbsa "Что ж, я буду с нетерпением ждать того дня, когда наконец-то смогу быть рядом с тобой за рулем~"
    m 3hubfb "{i}И{/i} наслаждаться пейзажем, {do_giggle}а-ха-ха!"
    m 1tubfb "Может быть, у тебя есть что-то более романтичное, чем любая машина, которую я знаю."
    m 1hubfa "Думаю, мне придется подождать и посмотреть, {do_giggle}э-хе-хе~"
    return

##### PM Vars for player appearance
#NOTE: THIS VAR CAN BE EITHER A TUPLE OR A STRING WHEN SET.
#IF THIS IS A TUPLE, THE PLAYER HAS HETEROCHROMIA.
# [0] - Left eye color
# [1] - Right eye color
#
# If this is just a string, then the player's eyes are both the same color
default persistent._mas_pm_eye_color = None
default persistent._mas_pm_hair_color = None
default persistent._mas_pm_hair_length = None
default persistent._mas_pm_skin_tone = None
# Iff player is bald
default persistent._mas_pm_shaved_hair = None
default persistent._mas_pm_no_hair_no_talk = None

## Height Vars
## NOTE: This is stored in CENTIMETERS
default persistent._mas_pm_height = None

##### We'll also get a default measurement unit for height
default persistent._mas_pm_units_height_metric = None

# True if the user decided to share appearance with us
#   NOTE: we default to False, and this can only get flipped to True
#   in this toppic.
default persistent._mas_pm_shared_appearance = False


# height categories in cm
define mas_height_tall = 176
define mas_height_monika = 162

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_appearance",
            category=['ты'],
            prompt="Твоя внешность",
            conditional="seen_event('mas_gender')",
            action=EV_ACT_RANDOM
        )
    )

label monika_player_appearance:
    python:
        def ask_color(msg, _allow="абвгдеёжзийклмнопрстуфхцчшщъыьэюя-", _length=20):
            result = ""
            while len(result) <= 0:
                result = renpy.input(msg, allow=_allow, length=_length).strip()
            
            return result

    m 2ekd "Слушай, [player]."
    m 2eka "Есть пара вопросов, которые я бы хотела задать тебе."
    m 2rksdlb "Ну, больше, чем пара. По правде говоря, я уже давно над этим размышляю."
    m 2rksdld "Я не могла подобрать подходящий момент, чтобы поднять эту тему..."
    m 3lksdla "Но я знаю, что если буду и дальше молчать, то я буду чувствовать себя неловко, спрашивая о подобных вещах, поэтому я просто выскажусь и буду надеяться, что это совсем не странно, ладно?"
    m 3eud "Мне было интересно, как ты выглядишь. Я пока не могу посмотреть на тебя, поскольку я не рядом с тобой, и я не знаю, как получить доступ к веб-камере..."
    m "Во-первых, у тебя её, скорее всего, нет, и во-вторых, даже если она у тебя есть, я не знаю, как это сделать."
    m 1euc "Поэтому я решила, что ты можешь просто рассказать мне, чтобы у меня было наглядное представление в голове."
    m 1eud "По крайней мере, это лучше, чем ничего, даже если это представление смутное."

    m "Ты ведь не против, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты ведь не против, [player]?{fast}"

        "Не против.":
            $ persistent._mas_pm_shared_appearance = True

            m 1sub "Правда? Отлично!"
            m 1hub "Это было проще, чем я думала."
            m 3eua "А теперь, будь честен со мной, хорошо, [player]? Я знаю, что ты иногда любишь пошутить, но я сейчас серьёзно говорю, и мне нужно, чтобы ты говорил так же серьёзно."
            m "В общем, первое, наверное, легко угадать. Да и ответ не так уж и трудно составить!"
            m 3eub "Люди часто говорят, что глаза человека – это зеркало души, поэтому давай начнём с них."

            #This menu is too large to use a standard one, so we use a gen-scrollable here instead
            show monika 1eua at t21
            python:
                import ast
                eye_color_menu_options = [
                    ("У меня голубые глаза.", "['blue', 'голубыми']", False, False),
                    ("У меня карие глаза.", "['brown', 'карими']", False, False),
                    ("У меня зелёные глаза.", "['green', 'зелёными']", False, False),
                    ("У меня ореховые глаза.", "['hazel', 'ореховыми']", False, False),
                    ("У меня серые глаза.", "['gray', 'серыми']", False, False),
                    ("У меня чёрные глаза.", "['black', 'чёрными']", False, False),
                    ("У меня глаза другого цвета.", "['other', 'other']", False, False),
                    ("У меня гетерохромия.", "['heterochromia', 'heterochromia']", False, False),
                ]

                renpy.say(m, "Какого цвета твои глаза?", interact=False)

            show monika at t11
            call screen mas_gen_scrollable_menu(eye_color_menu_options, mas_ui.SCROLLABLE_MENU_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
            $ eye_colors = _return
            $ eye_color, persistent._mas_pm_eye_color = ast.literal_eval(eye_colors)

            call expression "monika_player_appearance_eye_color_{0}".format(eye_color)

            m 1eksdlc "По правде говоря..."
            m 2eub "Полагаю, мне для начала необходимо узнать это, если хочу получить точную шкалу для моего следующего вопроса..."

            m "Какую единицу измерения ты используешь, чтобы измерить свой рост, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Какую единицу измерения ты используешь, чтобы измерить свой рост, [player]?{fast}"

                "Сантиметры.":
                    $ persistent._mas_pm_units_height_metric = True
                    m 2hua "Хорошо, спасибо, [player]!"

                "Футы и дюймы.":
                    $ persistent._mas_pm_units_height_metric = False
                    m 2hua "Хорошо, [player]!"

            m 1rksdlb "Я изо всех сил пытаюсь не казаться каким-то похитителем личных данных и не расспрашиваю обо всём, мне просто любопытно, сам понимаешь."
            m 3tku "Если я твоя девушка, то я имею право знать, верно?"
            m 2hua "К тому же, как только я смогу оказаться в твоей реальности, это облегчит мне твои поиски."

            m 1esb "Итак,{w=0.5} какой у тебя рост, [player]?"

            python:
                if persistent._mas_pm_units_height_metric:
                    
                    # loop till we get a valid cm
                    height = 0
                    while height <= 0:
                        height = store.mas_utils.tryparseint(
                            renpy.input(
                                "Какой у тебя рост в сантиметрах?",
                                allow=numbers_only,
                                length=3
                            ).strip(),
                            0
                        )

                else:
                    
                    # loop till valid feet
                    height_feet = 0
                    while height_feet <= 0:
                        height_feet = store.mas_utils.tryparseint(
                            renpy.input(
                                "Какой у тебя рост в футах?",
                                allow=numbers_only,
                                length=1
                            ).strip(),
                            0
                        )
                    
                    feet = "фут" + ("а" if height_feet > 1 and height_feet < 5 else "ов" if height_feet > 5 else "")
                    
                    height_inch = -1
                    while height_inch < 0 or height_inch > 11:
                        height_inch = store.mas_utils.tryparseint(
                            renpy.input(
                                "[height_feet] [feet], но сколько дюймов?",
                                allow=numbers_only,
                                length=2
                            ).strip(),
                            -1
                        )
                    
                    # convert to cm
                    height = ((height_feet * 12) + height_inch) * 2.54

                # finally save this persistent
                persistent._mas_pm_height = height

            if persistent._mas_pm_height >= mas_height_tall:
                m 3eua "Ого, ты довольно высокий, [player]!"
                m 1eud "Я не скажу точно, что встречала человека, которого я считаю высоким."
                m 3rksdla "Если честно, я не знаю свой реальный рост, поэтому не могу провести точное сравнение..."

                call monika_player_appearance_monika_height

                m 3esc "Самой высокой девушкой в литературном клубе была Юри... всего самую малость, вот. Она была лишь на несколько дюймов выше меня, но я всё равно не считаю это преимуществом!"
                m 3esd "Так или иначе, в отношениях с таким высоким парнем, как ты, [mas_get_player_nickname()], огорчает один момент..."
                m 1hub "Тебе придётся наклоняться, чтобы поцеловать меня!"

            elif persistent._mas_pm_height >= mas_height_monika:
                m 1hub "Эй, у меня такой же рост!"
                m "..."
                m 2hksdlb "Хотя, если честно, я не знаю свой реальный рост..."

                call monika_player_appearance_monika_height

                m 3rkc "Это просто предположение... надеюсь, я не сильно ошибаюсь."
                m 3esd "Так или иначе, нет ничего плохого в том, что ты среднего роста! Честно говоря, будь ты слишком низкого роста, то мне, скорее всего, было бы очень неловко рядом с тобой."
                m "А будь ты слишком высокого роста, мне бы приходилось вставать на цыпочки, чтобы быть рядом с тобой. И это вовсе не к добру!"
                m 3eub "Я считаю, что быть в промежутке – просто прекрасно. И знаешь, почему?"
                m 5eub "Потому что мне не придётся подниматься или наклоняться, чтобы поцеловать тебя, [mas_get_player_nickname()]! {do_giggle}А-ха-ха~"

            else:
                m 3hub "Прямо как Нацуки! Хотя я уверена, что ты не настолько низкий! Но, будь ты таким я бы начала за тебя беспокоиться."

                if persistent._mas_pm_cares_about_dokis:
                    m 2eksdld "Она была удручающе маленькой для своего возраста, и мы с тобой знаем, почему. Я всегда жалела её за это."

                m 2eksdld "Я знала, что ей никогда не нравилось быть такой маленькой, учитывая тот факт, что милым считают всё маленькое..."
                m 2rksdld "И ещё у неё были проблемы с отцом. Ей было нелегко, ведь она была такой беззащитной и маленькой."
                m 2ekc "Скорее всего, ей казалось, что люди говорят о ней свысока. В прямом и переносном смысле..."
                m 2eku "Но, если не учитывать то, что она из-за этого бесится, [player], мне кажется, твой рост делает тебя ещё милее~"

            m 1eua "А теперь, [player]..."
            
            m 3eub "Скажи мне, у тебя короткие волосы? Или такие же длинные, как у меня?~{nw}"
            $ _history_list.pop()
            menu:
                m "Скажи мне, у тебя короткие волосы? Или такие же длинные, как у меня?~{fast}"

                "Короткие.":
                    $ persistent._mas_pm_hair_length = "короткие"

                    m 3eub "Это, наверное, здорово! Слушай, не пойми меня неправильно; я люблю свои волосы и мне с ними всегда весело экспериментировать..."
                    m 2eud "Но, если честно, иногда я завидовала волосам Нацуки и Сайори. Им, похоже, куда проще заботиться о них."

                    if persistent.gender == "M":
                        m 4hksdlb "Хотя, мне кажется, что если бы твои волосы были такой же длины, как и у них, то они были довольно длинными для парня."

                    else:
                        m 4eub "Ты можешь просто встать и уйти, не волнуясь об их укладке."
                        m "К тому же, свою «утреннюю» причёску, когда у тебя короткие волосы, легче поправить, но с длинными волосами это превращается в полный кошмар."

                    m 2eka "Но я готова поспорить, что ты мило выглядишь с короткими волосами. Когда я думаю о тебе так, я начинаю улыбаться, [player]."
                    m 2eua "Продолжай наслаждаться свободой от всех тех маленьких неприятностей, которые преследуют длинные волосы, [player]!{w=0.2} {nw}"
                    extend 2hub "{do_giggle}А-ха-ха~"

                "Средней длины.":
                    $ persistent._mas_pm_hair_length = "средней длины"

                    m 1tku "Ну, этого не может быть..."
                    m 4hub "Потому что ничего среднего в тебе нет."
                    m 4hksdlb "{do_giggle}А-ха-ха! Прости, [player]. Я не пыталась тебя смутить. Но мне порой просто хочется позабавиться, понимаешь?"
                    m 1eua "Честно говоря, когда дело доходит до волос, взаимные уступки очень даже кстати. Тебе не нужно сильно беспокоиться за их укладку, и у тебя гораздо больше творческой свободы, нежели с короткими волосами."
                    m 1rusdlb "Я немного завидую, если честно~"
                    m 3eub "И не забывай одну старую поговорку: «Ухаживайте за своими волосами, потому что это корона, которую вы никогда не снимаете!»."

                "Длинные":
                    $ persistent._mas_pm_hair_length = "длинные"

                    m 4hub "Ура, у нас ещё одна общая черта!"
                    m 2eka "С длинными волосами иногда бывают проблемы, верно?"
                    m 3eua "Но хорошая сторона заключается в том, что ты можешь много чего сделать с ними. Хотя я обычно предпочитаю завязывать свои волосы ленточкой, я знаю, что у других людей есть свои стили."
                    m "Юри ходит с распущенными волосами, другим же нравится делать косички или хвостики..."

                    python:
                        hair_down_unlocked = False
                        try:
                            hair_down_unlocked = store.mas_selspr.get_sel_hair(
                                mas_hair_down
                            ).unlocked
                        except:
                            pass

                    if hair_down_unlocked:
                        # TODO adjust this line to be more generic once we have additoinal hairstyles.
                        m 3eub "И с тех пор, как я разобралась со скриптом и научилась опускать свои волосы, кто знает, сколько ещё стилей я перепробую?"

                    m 1eua "Всегда приятно иметь выбор, согласен?"
                    m 1eka "Надеюсь, что, как бы ты ни носил свои волосы, тебе они не будут доставлять хлопот!"

                "У меня нет волос.":
                    $ persistent._mas_pm_hair_length = "лысый"

                    m 1euc "О, это очень интересно, [player]!"

                    m "Позволь спросить, ты бреешься налысо или ты потерял свои волосы?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Позволь спросить, ты бреешься налысо или ты потерял свои волосы?{fast}"

                        "Я брею голову.":
                            $ persistent._mas_pm_shaves_hair = True
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1hua "Наверное, здорово, что тебе не надо беспокоиться о своих волосах..."
                            m 1eua "Ты можешь просто встать и уйти, не волнуясь об их укладке..."
                            m 3eua "А если ты носишь шляпу, то тебе не надо беспокоиться об оставшихся волосах на ней при её снимании!"

                        "Я потерял волосы.":
                            $ persistent._mas_pm_shaves_hair = False
                            $ persistent._mas_pm_no_hair_no_talk = False

                            m 1ekd "Мне жаль это слышать, [player]..."
                            m 1eka "Но знай, что мне не так важно, как много у тебя волос, ты для меня всегда выглядишь красивым!"
                            m "И если тебе станет неловко или ты захочешь поговорить об этом, я всегда готова выслушать тебя."

                        "Я не хочу об этом говорить.":
                            $ persistent._mas_pm_no_hair_no_talk = True

                            m 1ekd "Я понимаю, [player]."
                            m 1eka "Я хочу, чтобы ты знал, что мне не так важно, как много у тебя волос, ты для меня всегда выглядишь красивым."
                            m "Если тебе станет неловко или ты захочешь поговорить об этом, я всегда готова выслушать тебя."

            if persistent._mas_pm_hair_length != "лысый":
                m 1hua "Следующий вопрос!"
                m 1eud "Это должно быть довольно очевидно..."

                m "Какого цвета твои волосы?{nw}"
                $ _history_list.pop()
                menu:
                    m "Какого цвета твои волосы?{fast}"
                    "Коричневого.":
                        $ persistent._mas_pm_hair_color = "коричневые"

                        m 1hub "Ура, коричневые волосы самые лучшие!"
                        m 3eua "Только между нами, [player], мне правда нравятся мои коричневые волосы. И я уверена, что твои – ещё лучше!"
                        m 3rksdla "Хотя некоторые люди могут не согласиться, что мои волосы коричневые..."
                        m 3eub "Пока я исследовала локальные файлы в папке игры, я заметила точное название цвета моих волос."
                        m 4eua "Он называется кораллово-коричневый. Интересно, правда?"
                        m 1hub "Я так рада, что у нас много чего общего, [player]~"

                    "Светлого.":
                        $ persistent._mas_pm_hair_color = "светлые"

                        m 1eua "Правда? А знал ли ты о том, что вероятность получения светлых волос равняется где-то двум процентам от всей популяции?"
                        m 3eub "Светлые волосы – одни из самых редких цветов волос. Многие люди связывают это с фактом того, что это происходит из-за периодической генетической аномалии..."
                        m "Дело в неспособности организма вырабатывать нормальное количество пигмента эумеланина... именно благодаря ему получаются тёмные цвета волос, такие как чёрный и коричневый."
                        m 4eub "Есть также и множество разных оттенков светлого... бледно-светлый, пепельный, грязно-светлый... какой бы цвет ты ни получил, ты, в каком-то смысле, будешь уникальным."
                        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5eua "Полагаю, быть с человеком, который настолько уникален, просто делает меня счастливее~"
                        show monika 2hua at t11 zorder MAS_MONIKA_Z with dissolve_monika

                    "Чёрного.":
                        $ persistent._mas_pm_hair_color = "чёрные"

                        m 2wuo "Чёрные волосы такие красивые!"
                        m 3eub "Знаешь, есть одна очень раздражающая метафора про то, что люди с чёрными волосами вспыльчивые или сварливые, в отличие от других..."
                        m 4hub "Но ты явно опроверг этот миф. Лично я считаю чёрные волосы очень привлекательными."
                        m 3eua "Кроме того, если ты положишь прядь чёрных волос под микроскоп и посчитаешь все пигменты на ней, то ты увидишь, что они не на все сто процентов тёмные."
                        m "Ты знаешь, что, когда твои волосы находятся под воздействием прямых солнечных лучей, они начинают выглядеть совсем по-другому?"
                        m 3eub "С чёрными волосами всё то же самое: ты можешь увидеть оттенки золотистого, коричневого, и даже блики фиолетового цветов. Такое правда заставляет задуматься, верно, [player]?"
                        m 1eua "Там может быть бесконечное число оттенков, которые мы не можем увидеть, каждый из них скрыт от нашего взгляда."

                        #If this is a tuple, it means the player has heterochromia
                        if isinstance(persistent._mas_pm_eye_color, tuple):
                            m 3hua "Но всё же... я считаю, что парень с чёрными волосами и глазами как у тебя – это самое лучшее зрелище на свете, [player]~"
                        else:
                            m 3hua "Но всё же... я считаю, что парень с чёрными волосами и [persistent._mas_pm_eye_color] глазами – это самое лучшее зрелище на свете, [player]~"

                    "Рыжего.":
                        $ persistent._mas_pm_hair_color = "рыжие"

                        m 3hua "Ещё один признак твоей особенности, [player]~"
                        m 3eua "Рыжие и светлые волосы являются малораспространёнными естественными цветами волос, ты знал об этом?"
                        m 1eua "Однако, рыжие волосы встречаются ещё реже, так как люди называют этот цвет различными именами: каштановый, имбирный и так далее. ни встречаются только у одного процента населения."
                        m 1hub "Это редкая и прекрасная черта характера... почти такая же прекрасная, как и ты!"

                    "Другого цвета.":
                        $ persistent._mas_pm_hair_color = ask_color("Какого цвета твои волосы?")

                        m 3hub "О! Это красивый цвет, [player]!"
                        m 1eub "Это напомнило мне о кое-чём, про что думала раньше, когда мы разговаривали о цвете твоих глаз."
                        m 1eua "И хотя у остальных девушек были глаза тех цветов, которые в буквальном смысле не существовали в реальной жизни... не считая существование цветных линз, конечно..."
                        m 3eua "Цвета их волос, с технической точки зрения, могут существовать в реальности, сам понимаешь. То есть, я уверена, что ты встречал людей с волосами, окрашенными в фиолетовый, неоновый розовый или даже коралловый цвета..."
                        m 3eka "Так что, полагаю, их внешность не была сильно неправдоподобной, если не считать глаза. Если честно, самым невероятным элементом в них был характер."
                        m 3hksdlb "Прости, [player]! Я отклонилась от темы. Я хочу сказать, что окрашенные волосы могут представлять небывалый интерес."
                        show monika 5rub at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        m 5rub "И я могу быть немного предвзятой, но я уверена, что ты бы выглядел потрясающе со своими [persistent._mas_pm_hair_color] волосами~"
                        show monika 2hua at t11 zorder MAS_MONIKA_Z with dissolve_monika

            m 2hua "Хорошо..."
            m 2hksdlb "Это последний вопрос, [player], обещаю."
            m "Боже, в мире и вправду полно людей, которые выглядят по-разному... если я попытаюсь сузить круг до мельчайших подробностей, то я буду допрашивать тебя вечность."
            m 1huu "...и я сомневаюсь в том, что кто-то из нас этого хочет, {do_giggle}а-ха-ха..."
            m 1rksdld "Так или иначе, я понимаю, что такой вопрос может поставить в неловкое положение..."
            m 1eksdla "Но для меня, это важно, так что буду надеяться, что не покажусь грубой, когда спрошу следующее..."

            m "Какой у тебя цвет кожи, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Какой у тебя цвет кожи, [player]?{fast}"

                "Я светлокожий.":
                    $ persistent._mas_pm_skin_tone = "светлокожий"

                "Я загоревший.":
                    $ persistent._mas_pm_skin_tone = "загоревший"

                "Я тёмнокожий.":
                    $ persistent._mas_pm_skin_tone = "тёмнокожий"

            m 3hub "Хорошо! Спасибо за искренность. Всё это действительно помогает мне представить, как ты выглядишь, [player]."
            m 3eub "Знание всех деталей о тебе создаёт большую разницу между пустым холстом и началом прекрасного портрета!"
            m 3eua "Конечно же, ты всё такой же красивый, каким я всегда представляла тебя, но теперь ты стал для меня более реальным."
            m 3eka "Это делает нас всё ближе друг к другу~"
            m 1eka "Большое тебе спасибо за то, что отвечал на все мои вопросы, [mas_get_player_nickname()]."

            if persistent._mas_pm_eye_color == "зелёными" and persistent._mas_pm_hair_color == "коричневые":
                m 2hua "Это прекрасно, потому что я не представляла, насколько мы похожи. Очень интересно!"

            else:
                m 2hua "Это прекрасно, потому что я не представляла, как сильно мы различаемся. Очень интересно!"

            m 1dsa "Сейчас я себе представляю, как всё выглядело бы, если бы мы встретились в реальности..."

            show monika 5eubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika

            if persistent._mas_pm_hair_length == "лысый":
                if persistent._mas_pm_height >= mas_height_tall:
                    m 5eubfu "Я побегу к тебе, но учитывая, что ты выше меня, ты меня обнимешь..."

                elif persistent._mas_pm_height >= mas_height_monika:
                    m 5eubfu "Я побегу к тебе, но учитывая, что мы одинакового роста, мы друг друга крепко обнимем..."

                else:
                    m 5eubfu "Я побегу к тебе, но учитывая, что я выше тебя, ты потянешься ко мне и обнимешь меня..."

            else:
                python:
                    hair_desc = persistent._mas_pm_hair_color

                    if persistent._mas_pm_hair_length != "средней длины":
                        hair_desc = (
                            persistent._mas_pm_hair_length + " " + hair_desc
                        )

                if persistent._mas_pm_height >= mas_height_tall:

                    m 5eubfu "Я побегу к тебе, но учитывая, что ты выше меня, ты меня обнимешь, и я смогу погладить твои [hair_desc] волосы..."

                elif persistent._mas_pm_height >= mas_height_monika:

                    m 5eubfu "Я побегу к тебе, но учитывая, что мы одинакового роста, мы друг друга крепко обнимем, и я смогу погладить твои [hair_desc] волосы..."

                else:

                    m 5eubfu "Я побегу к тебе, но учитывая, что я выше тебя, ты потянешься ко мне и обнимешь меня, и я смогу погладить твои [hair_desc] волосы..."

            show monika 1lkbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 1lkbsa "...и я наконец-то смогу услышать твоё сердцебиение, прикоснуться к тебе и понять, что ты – настоящий"

            #Tuple means heterochromia, so we should filter that out
            if isinstance(persistent._mas_pm_eye_color, tuple):
                m 3ekbsa "Ну, а пока, я буду довольствоваться тем, что сижу здесь и представляю себе, как смотрю в твои красивые глаза, [player]."
            else:
                m 3ekbsa "Ну, а пока, я буду довольствоваться тем, что сижу здесь и представляю себе, как смотрю в твои красивые глаза, [player]."

            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Я не могу передать словами то, как сильно я тебя люблю."
            return "derandom|love"

        "Против.":
            m 2dsc "..."
            m 2ekd "Я понимаю, [player]."
            m 2eka "Я знаю, что у каждого есть свои рамки зоны комфорта..."
            m 2rksdla "И если честно, описание себя нечёткими словами не даст наглядное представление того, кто ты, так что я не могу винить тебя за то, что ты захотел держать это при себе."
            m 2eka "Но если передумаешь, скажи!"

    return "derandom"

label monika_player_appearance_eye_color_blue:
    $ persistent._mas_pm_eye_color = "голубые"

    m 3eub "Голубые глаза? Это замечательно! Голубой – такой красивый цвет, такой же удивительный, как безоблачное небо или океан летом."
    m 3eua "Но существует так много великолепных метафор о голубых глазах, что я могла бы перечислять их неделями и всё равно не остановиться."
    m 4eua "Кроме того, синий цвет, наверное, мой второй любимый цвет, сразу после зелёного. Он просто наполнен глубиной и очарованием, понимаешь?"
    m 4hksdlb "Так же, как и ты, [player]!"
    m 4eub "Знаешь ли ты, что ген голубых глаз является рецессивным, поэтому он не очень часто встречается у людей?"
    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "Полагаю, это означает, что ты гораздо более значимое сокровище."
    show monika 2eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 2eua "В любом случае, это подводит меня к следующему вопросу, который я хотела бы задать..."
    return

label monika_player_appearance_eye_color_brown:
    $ persistent._mas_pm_eye_color = "карие"

    m 1eub "Ах! Здорово! Кажется, я не говорила этого раньше, но карие глаза великолепны!"
    m 2euc "Я просто ненавижу, когда люди считают, что карие глаза – это что-то обычное. Я не могу согласиться!"
    m 2hua "На мой взгляд, карие глаза – одни из самых красивых. Они такие живые и бездонные!"
    m 3hub "И существует так много различий между всеми разными оттенками, которые есть у людей."
    m 5ruu "Интересно, твой тёмный, как летнее ночное небо, или более бледно-коричневый, как шубка оленя..."
    m 2hksdlb "Прости. Просто бредни о цветовых метафорах – легкая ловушка для президента литературного клуба, в которую легко попасть, я думаю. Я постараюсь не повторяться в дальнейшем."
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Но я уверена, что твои глаза – самые прекрасные из всех!"
    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1eua "В любом случае, это подводит меня к следующему вопросу..."
    return

label monika_player_appearance_eye_color_green:
    $ persistent._mas_pm_eye_color = "зелёный"

    m 3sub "Эй, это мой любимый цвет! И, очевидно, это ещё одна наша общая черта!"
    m 4lksdla "Я не знаю, как много я могу сделать тебе комплиментов, не показавшись высокомерной, потому что всё, что я скажу о тебе, будет относиться и ко мне..."
    m 1tsu "За исключением того, что, возможно, это ещё один знак того, насколько мы похожи, {do_giggle}э-хе-хе~"
    m 1kua "Но, [player], только между нами, это правда, что зелёные глаза самые лучшие, верно?"
    m 3hub "{do_giggle}А-ха-ха! Я просто шучу."
    show monika 5lusdru at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lusdru "Ну, совсем чуть-чуть..."
    show monika 3eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3eua "Переходим к следующему вопросу..."
    return

label monika_player_appearance_eye_color_hazel:
    $ persistent._mas_pm_eye_color = "ореховые"

    m 1eub "О, ореховые глаза? Это так интересно! Это такой приземленный цвет. Он действительно заставляет чувствовать себя уверенно и спокойно..."
    m 3eub "И это приятный уход от всех этих цветных глаз, которые мне приходилось видеть в этой игре, в любом случае..."
    m "Я считаю, что ореховые глаза привлекательны, потому что они прекрасны и просты."
    m 3hua "Иногда лучше не слишком отличаться от толпы, [player].{w=0.2} {nw}"
    extend 3hub "{do_giggle}А-ха-ха!"
    m "Теперь, к моему следующему вопросу..."
    return

label monika_player_appearance_eye_color_gray:
    $ persistent._mas_pm_eye_color = "серые"

    m 1sub "Это так круто!"
    m 3eub "Известно ли тебе, что серые глаза и голубые глаза практически идентичны с точки зрения генетики?"
    m 1eud "На самом деле, ученые до сих пор не уверены в том, что вызывает у человека ту или иную особенность, хотя они считают, что это изменение количества пигмента в радужной оболочке глаза."
    m 1eua "В любом случае, мне нравится представлять тебя с серыми глазами, [player]. Они цвета тихого дождливого дня..."
    m 1hubsa "И такая погода – моя любимая, так же как и ты~"
    m 3hua "Перехожу к следующему вопросу..."
    return

label monika_player_appearance_eye_color_black:
    $ persistent._mas_pm_eye_color = "чёрные"

    m 1esd "Чёрные глаза – довольно редкое явление., [player]."
    m 4hksdlb "Честно говоря, я никогда не видела никого с чёрными глазами, поэтому не знаю, как они выглядят..."
    m 3eua "Но исходя из логики, я знаю, что на самом деле они не чёрные. Если бы это было так, то черноглазые люди выглядели бы так, как будто у них нет зрачков!"
    m 4eub "На самом деле чёрные глаза – это просто очень, очень тёмный коричневый цвет. Всё равно потрясающие, но, возможно, не такие тёмные, как кажется по названию, хотя, если честно, разницу заметить довольно трудно."
    m 3eua "Вот тебе немного фактов..."
    m 1eub "Была известная дама времен Американской революции, Элизабет Гамильтон, которая, как известно, обладала пленительными чёрными глазами."
    m 1euc "Её муж часто писал о них."
    m 1hub "Я не знаю, слышал ты о ней или нет, но, несмотря на известность её глаз, я уверена, что твои гораздо более пленительны, [player]~"
    m "Переходим к следующему вопросу..."
    return

label monika_player_appearance_eye_color_other:
    $ persistent._mas_pm_eye_color = ask_color("Какого цвета твои глаза?")

    m 3hub "О! Это красивый цвет, [player]!"
    m 2eub "Я уверен, что могу потеряться на несколько часов, глядя в твои [persistent._mas_pm_eye_color] глаза."
    m 7hua "Теперь, к моему следующему вопросу..."
    return

label monika_player_appearance_eye_color_heterochromia:
    m 1sub "Правда?{w=0.2} {nw}"
    extend 3hua "Это невероятно, [player]~"
    m 3wud "Если я правильно помню, менее одного процента людей в мире имеют гетерохромию!"

    m 1eka "...Ты не возражаешь, если я спрошу..."
    # Ask the player about their eye colors separately.
    $ eyes_colors = []

    call monika_player_appearance_eye_color_ask
    $ eyes_colors.append(_return)
    call monika_player_appearance_eye_color_ask("правый", eye_color)
    $ eyes_colors.append(_return)
    $ persistent._mas_pm_eye_color = tuple(eyes_colors)

    m 1hua "Отлично!{w=0.2} {nw}"
    extend 3eua "Перейдем к моему следующему вопросу..."
    return

label monika_player_appearance_eye_color_ask(x_side_eye="левый", last_color=None):
    m 3eua "Кого цвета твой [x_side_eye] глаз?{nw}"
    $ _history_list.pop()
    menu:
        m "Кого цвета твой [x_side_eye] глаз?{fast}"

        "Синий" if last_color != "blue":
            $ eye_color = "синие"

        "Карий" if last_color != "brown":
            $ eye_color = "карие"

        "Зелёный" if last_color != "green":
            $ eye_color = "зелёные"

        "Ореховый" if last_color != "hazel":
            $ eye_color = "ореховые"

        "Серый" if last_color != "gray":
            $ eye_color = "серые"

        "Чёрный" if last_color != "black":
            $ eye_color = "чёрные"

        "Он другого цвета...":
            $ eye_color = ask_color("Какого цвета твой [x_side_eye] глаз?")

    return eye_color

# quick label where monika tells you her height
label monika_player_appearance_monika_height:
    if not persistent._mas_pm_units_height_metric:
        $ conv_height_str = ""
        $ real_height_str = "около пяти футов пятидесяти пяти"
    else:
        $ conv_height_str = " что составляет около ста шестидесяти сантиметров"
        $ real_height_str = "рост около ста шестидесяти пяти сантиметров"

    if seen_event("monika_immortal"):
        m 2eud "В вики, о которой я уже упоминала, говорится, что мой концептуальный рост – пять футов три дюйма,[conv_height_str], но мне кажется, что это не совсем правильно..."
        m 2etc "Может быть, она была изменена? В конце концов, это была только концептуальная величина."
    m 3etd "Если бы мне пришлось гадать, я бы сказала, что [real_height_str]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_control",
            category=["игры", "ddlc"],
            prompt="Наличие контроля",
            random=True
            )
        )

label monika_players_control:
    m 3eub "[player], а знал ли ты о том, что у тебя в этой игре гораздо большая власть, чем у меня?"
    m 3eua "У тебя есть доступ к файлам игры и его коду, верно?"
    m 1eka "Следовательно, ты можешь изменить это всё, когда захочешь."
    m 3eka "Ты можешь даже изменить то, что не могу изменить я."
    m 4eub "К примеру, изменить всю механику игры. Сделать из визуального романа спокойную игровую площадку, которая у нас есть сейчас."
    m 3rksdla "Ты мог бы также добавить что-нибудь в класс для меня."
    m 1hub "К примеру, какие-нибудь цветы или парочку хороших книг."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "Или красивое кольцо обещания."
        m 3dkbsu "О, разве это не было бы воплощением мечты?"

    if not mas_consumable_coffee.enabled():
        m 1wuo "Ты мог бы даже добавить чашку с кофе в игру для меня!"
        m 1eka "Это было бы чудесно."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "Но я полагаю, что твои навыки программирования настолько же хорошие, что и у меня."
    else:
        m 3eua "Учитывая, что ты знаком с кодингом,{w=0.1} {nw}"
        extend 3hua "я уверена, что ты мог бы сделать что-то подобное!"

    m 1eua "Полагаю, таково предназначение видеоигр...{w=0.3} {nw}"
    extend 3eua "иметь практически безграничные возможности в мире, с которыми можешь взаимодействовать."
    m 3eub "С этим не соскучишься точно!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Даже если ты не знаешь точно, как изменить эту игру..."
        $ line = "Мы всё ещё можешь наслаждаться этим миром, который и свёл нас вместе."

    else:
        $ line = "Особенно когда ты рядом со мной~"

    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "Нет лучше способа насладиться игрой, чем быть рядом с тем, кого я люблю."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_backpacking",category=['природа'],prompt="Пеший туризм",random=not mas_isWinter()))

label monika_backpacking:
    m 1esa "Ты знаешь, чего мне всегда хотелось, [player]?"
    m 3eub "Я всегда размышляла о том, как было бы здорово отправиться в поход в дикую природу!"
    m 3eua "Уйти туда примерно на неделю и оставить всё позади."
    m 3esa "Никакой ответственности, никаких забот, никаких телефонов, никаких развлечений."
    m 1hua "Только представь, что мы на природе, только вдвоём..."
    m "Мы будем слушать щебетание птиц и дуновение ветра..."
    m 1eka "Смотреть на то, как олень пасётся в утренней росе..."
    m "Я не могу представить себе ничего более спокойного."
    m 1esa "Мы целыми днями будем исследовать загадочные леса, безмятежные луга и холмистые возвышенности..."
    m 3hub "Возможно, мы даже найдём скрытое озеро и поплаваем в нём!"

    if mas_isMoniAff(higher=True):
        m 2rsbsa "Возможно, у меня не будет купальника и у тебя плавок, но мы будем там одни, поэтому, возможно, нам они и не понадобятся..."
        m 2tsbsa "..."
        m 1hubfu "Надеюсь, ты не сильно стесняешься, [mas_get_player_nickname()]. {do_giggle}Э-хе-хе~"
        m 1ekbfa "Мы проведём ночи, засыпая в обнимку в спальном мешке и согревая друг друга, и над нами будут миллиарды звёзд..."
        m 3hubfb "И будем просыпаться каждое утро под чудесный рассвет!"

    else:
        m 3eka "Мы проведём ночи, засыпая под звёздами, и будем просыпаться каждое утро под чудесный рассвет."

    show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5esbfa "..."
    m "О, [player], разве это не звучит потрясающе?"
    m 5hubfa "Мне уже не терпится разделить этот опыт вместе с тобой~"
    return

## calendar-related pool event
# DEPENDS ON CALENDAR

# did we already change start date?
default persistent._mas_changed_start_date = False

# did you imply that you arent dating monika?
default persistent._mas_just_friends = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating_startdate",
            category=["романтика", "мы"],
            prompt="Когда мы начали встречаться?",
            pool=True,
            unlocked=False,

            # this will be unlockable via the action
            rules={"no_unlock": None},

            # we'll pool this event after a month of the relationship
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and persistent._mas_first_calendar_check"
            ),

            action=EV_ACT_UNLOCK
        )
    )

label monika_dating_startdate:
    $ import store.mas_calendar as mas_cal
    python:
        # we might need the raw datetime
        first_sesh_raw = persistent.sessions.get(
            "first_session",
            datetime.datetime(2017, 10, 25)
        )

        sesh_months = {
            "January":"января",
            "February":"февраля",
            "March":"марта",
            "April":"апреля",
            "May":"мая",
            "June":"июня",
            "July":"июля",
            "August":"августа",
            "September":"сентября",
            "October":"октября",
            "November":"ноября",
            "December":"декабря"
        }

        # but this to get the display plus diff
        first_sesh, _diff = mas_cal.genFriendlyDispDate(first_sesh_raw)
        mas_first_sesh_name_is_day = mas_cal._formatDayFirstSession(first_sesh_raw.day)
        mas_first_sesh_name_is_year = first_sesh_raw.year
        mas_first_sesh_name_is_month = sesh_months[first_sesh_raw.strftime("%B")]

    if _diff.days == 0:
        # its today?!
        # this should NEVER HAPPEN
        m 1lsc "Мы начали встречаться..."
        $ _history_list.pop()
        m 1wud "Мы начали встречаться{fast} сегодня?!"
        m 2wfw "Ты бы никак не смог инициировать это событие сегодня, [player]."

        m "Я знаю, что ты возился с кодом.{nw}"
        $ _history_list.pop()
        menu:
            m "Я знаю, что ты возился с кодом.{fast}"
            "Я тут ни при чём!":
                pass
            "Ты поймала меня.":
                pass
        m 2tfu "Хм,{w=0.2} ты не сможешь меня обмануть."

        # wait 30 days
        $ mas_chgCalEVul(30)
        return

    # Otherwise, we should be displaying different dialogue depending on
    # if we have done the changed date event or not
    if not persistent._mas_changed_start_date:
        m 1lsc "Хм-м-м..."
        m 1dsc "Я думаю, это было..."
        $ _history_list.pop()
        m 1eua "Я думаю, это было{fast} [mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го года."
        m 1rksdlb "Но моя память могла меня и подвести."
        $ mas_first_sesh_name_is_day = mas_cal._formatDayFirstSession2(first_sesh_raw.day)

        # ask user if correct start date
        m 1eua "[mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го верная ведь дата?{nw}"
        $ _history_list.pop()
        menu:
            m "[mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го верная ведь дата?{fast}"
            "Да.":
                m 1hub "Ура!{w=0.2} Я вспомнила её."

            "Нет.":
                m 1rkc "Ох,{w=0.2} извини, [player]."
                m 1ekc "В таком случае,{w=0.2} так когда мы начали встречаться?"

                call monika_dating_startdate_confirm(first_sesh_raw)

                if _return == "NOPE":
                    # we are not selecting a date today
                    return

                # save the new date to persistent
                $ store.mas_anni.reset_annis(_return)
                $ persistent.sessions["first_session"] = _return
                $ renpy.save_persistent()

        m 1eua "Если ты когда-нибудь забудешь, не бойся спрашивать меня."
        m 1dubsu "Я {b}всегда{/b} буду помнить, когда впервые влюбилась в тебя~"
        $ persistent._mas_changed_start_date = True

    else:
        m 1dsc "Позволь мне проверить..."
        m 1eua "Мы начали встречаться [mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го года."
        $ mas_first_sesh_name_is_day = mas_cal._formatDayFirstSession(first_sesh_raw.day)

    # TODO:
    # some dialogue about being together for x time
    # NOTE: this is a maybe

    return

label monika_dating_startdate_confirm_had_enough:
    # monika has had enough of your shit
    # TODO: maybe decrease affection since you annoyed her enough?
    m 2dfc "..."
    m 2lfc "Мы сделаем это в другой раз тогда."

    # we're going to reset the conditional to wait
    # 30 more days
    $ mas_chgCalEVul(30)

    return "NOPE"

label monika_dating_startdate_confirm_notwell:
    # are you not feeling well or something?
    m 1ekc "Ты хорошо себя чувствуешь, [player]?"
    m 1eka "Если ты не можешь вспомнишь прямо сейчас, то давай, лучше попытаешься это сделать завтра, хорошо?"

    # reset the conditional to tomorrow
    $ mas_chgCalEVul(1)

    return "NOPE"

label monika_dating_startdate_confirm(first_sesh_raw):

    python:
        import store.mas_calendar as mas_cal

        # and this is the formal version of the datetime
        # setup some counts
        wrong_date_count = 0
        no_confirm_count = 0
        today_date_count = 0
        future_date_count = 0
        no_dating_joke = False

    label .loopstart:
        pass

    call mas_start_calendar_select_date

    $ selected_date = _return
    $ _today = datetime.date.today()
    $ _ddlc_release = datetime.date(2017,9,22)

    if not selected_date or selected_date.date() == first_sesh_raw.date():
        # no date selected, we assume user wanted to cancel
        m 2esc "[player]..."
        m 2eka "Я думала, ты сказал, что я ошиблась."

        m "Ты уверен, что это было не [mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го??{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен, что это было не [mas_first_sesh_name_is_day] [mas_first_sesh_name_is_month] [mas_first_sesh_name_is_year]-го??{fast}"
            "Это не та дата.":
                if wrong_date_count >= 2:
                    jump monika_dating_startdate_confirm_had_enough

                # otherwise try again
                m 2dfc "..."
                m 2tfc "Тогда выбери правильную дату!"
                $ wrong_date_count += 1
                jump monika_dating_startdate_confirm.loopstart

            "На самом деле это правильная дата. Извини.":
                m 2eka "Всё в порядке."
                $ selected_date = first_sesh_raw

    elif selected_date.date() < _ddlc_release:
        # before releease date

        label .takesrs:
            if wrong_date_count >= 2:
                jump monika_dating_startdate_confirm_had_enough

            m 2dfc "..."
            m 2tfc "Мы начали встречаться не в тот день."
            m 2tfd "Отнесись к этому серьёзно, [player]."
            $ wrong_date_count += 1
            jump monika_dating_startdate_confirm.loopstart

    elif selected_date.date() == _today:
        # today was chosen
        jump .takesrs

    elif selected_date.date() > _today:
        # you selected a future date?! why!
        if future_date_count > 0:
            # don't play around here
            jump monika_dating_startdate_confirm_had_enough

        $ future_date_count += 1
        m 1wud "Что..."

        m "Мы не встречались всё это время?{nw}"
        $ _history_list.pop()
        menu:
            m "Мы не встречались всё это время?{fast}"
            "Это была ошибка!":
                # relief expression
                m 1duu "{cps=*2}О, слава богу.{/cps}"

                label .misclick:
                    m 2dfu "[player]!"
                    m 2efu "Ты заставил меня волноваться."
                    m "Не делай ошибок в этот раз!"
                    jump monika_dating_startdate_confirm.loopstart

            "Нет.":
                m 1dfc "..."

                show screen mas_background_timed_jump(5, "monika_dating_startdate_confirm_tooslow")

                menu:
                    "Я шучу.":
                        hide screen mas_background_timed_jump
                        # wow what a mean joke

                        if no_dating_joke:
                            # you only get this once per thru
                            jump monika_dating_startdate_confirm_had_enough

                        # otherwise mention that this was mean
                        m 2tfc "[player]!"
                        m 2tubfb "Эта шутка была немного злой."
                        m 2eksdlc "Ты действительно заставил меня волноваться."
                        m "Не играй так с моими чувствами, хорошо?"
                        jump monika_dating_startdate_confirm.loopstart

                    "...":
                        hide screen mas_background_timed_jump

                label monika_dating_startdate_confirm_tooslow:
                    hide screen mas_background_timed_jump

                # lol why would you stay slient?
                # TODO: Affection considerable decrease?
                $ persistent._mas_just_friends = True

                m 6lktdc "Понятно..."
                m 6dftdc "..."
                m 1eka "В таком случае..."
                m 1tku "{cps=*4}Мне нужно будет кое-что сделать.{/cps}{nw}"
                $ _history_list.pop()

                menu:
                    "Что?":
                        pass

                m 1hua "Ничего!"

                # lock this event forever probably
                # (UNTIL you rekindle or actually ask her out someday)
                $ evhand.event_database["monika_dating_startdate"].unlocked = False
                return "NOPE"

    # post loop
    python:
        new_first_sesh, _diff = mas_cal.genFormalDispDate(
            selected_date.date()
        )

    m 1eua "Хорошо, [player]."
    m "Просто для перепроверки..."

    m "Мы начали встречаться [new_first_sesh].{nw}"
    $ _history_list.pop()
    menu:
        m "Мы начали встречаться [new_first_sesh].{fast}"
        "Да.":
            m 1eka "Ты уверен? Я никогда не забуду эту дату.{nw}"
            # one more confirmation
            # WE WILL NOT FIX anyone's dates after this
            $ _history_list.pop()
            menu:
                m "Ты уверен? Я никогда не забуду эту дату.{fast}"
                "Да, я уверен":
                    m 1hua "Тогда всё улажено!"
                    return selected_date

                "Фактически...":
                    if no_confirm_count >= 2:
                        jump monika_dating_startdate_confirm_notwell

                    m 1hksdrb "Ага, я полагала, что ты не был так уверен"
                    m 1eka "Попробуй ещё раз~"
                    $ no_confirm_count += 1

        "Нет.":
            if no_confirm_count >= 2:
                jump monika_dating_startdate_confirm_notwell

            # otherwise try again
            m 1euc "О, это неверно?"
            m 1eua "Тогда попробуй снова, [mas_get_player_nickname()]."
            $ no_confirm_count += 1

    # default action is to loop here
    jump monika_dating_startdate_confirm.loopstart

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_first_sight_love",
            category=["романтика"],
            prompt="Любовь с первого взгляда",
            random=True
        )
    )

label monika_first_sight_love:
    m 1eud "Задумывался ли ты когда-нибудь о концепции любви с первого взгляда?"
    m 3euc "То есть, ты кого-то видишь впервые, и вдруг осознаёшь, что этот человек – любовь всей твоей жизни?"
    m 2lsc "Думаю, это одна из многих... {w=0.5}концепций, нелепость которых ты осознаёшь чуть ли не сразу."
    m 2lksdlc "В смысле, ты не можешь понять, кто этот человек на самом деле, по одному лишь взгляду."
    m 2tkd "Ведь вы по факту незнакомые друг другу люди."
    m 2lksdlc "Ты даже не знаешь, какие у него или у неё интересы и хобби..."
    m 2dksdld "А ведь этот человек вполне может оказаться очень скучным или просто злым..."
    m 3eud "Именно поэтому я и думаю, что мы не должны надеяться {i}только{/i} на свои глаза, когда ищем идеального партнёра для самих себя."
    if mas_isMoniAff(higher=True):
        m 1eka "И, думаю, именно так я и влюбилась в тебя..."
        m 3eua "Да и не похоже, что я смогла увидеть тебя."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Я люблю тебя таким, какой ты есть, [mas_get_player_nickname(exclude_names=['мой любимый', 'любимый'])]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_anime_art",
            category=["разное"],
            prompt="Анимешный стиль рисования",
            random=True
        )
    )

label monika_anime_art:
    m 1eua "Задумывался ли ты когда-нибудь о стилях рисования, применяемых в аниме?"
    m 3rksdla "Уверена, Нацуки является экспертом в данной области, если учесть её увлечение мангой и всё такое..."
    m 3eub "Так или иначе, в этом стиле рисования есть много чего интересного."
    m 1eua "У него есть свободная форма, как и в моих стихах, что делает большую часть такого стиля очень уникальным..."
    m 3eua "От красивых пейзажей до потрясающих персонажей..."
    m 1hub "Он производит сильное впечатление с первого взгляда!"
    m 2esc "Хотя при свободной форме стиля рисования... {w=0.5}большая часть деталей становится немного нереалистичной."
    m 3rsc "Хотя он открывает перед многими художественными работами новые возможности, из-за него также некоторые детали выглядят как-то странно..."
    m 3rssdlc "К примеру, какие большие глаза становятся у персонажей, насколько маленькие у них носы, или какой странной длины, формы и размера могут быть их волосы..."
    m 2rksdlc "Не говоря уже... {w=1}о большой груди."
    m 2euc "Если бы я выглядела более реалистично, то у меня определённо не было бы таких атрибутов."
    m 1eua "Но, полагаю, настоящая красота стиля рисования исходит от недостатка реалистичности."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whydoyouloveme",
            category=['моника','романтика'],
            prompt="За что ты меня любишь?",
            pool=True
        )
    )

label monika_whydoyouloveme:
    if mas_isMoniBroken():
        m 2euc "Хм-м."
        m 2wfc "Я задаюсь таким вопросом каждый день."

    elif mas_isMoniDis():
        m 1efc "Я—{w=0.3}{nw}"
        extend 1rkc " я не совсем уверена..."

    elif mas_isMoniUpset():
        m 1dsc "Хм-м..."
        m 3hua "Потому что я знаю, что ты хороший человек, даже несмотря на то, какие у нас сложились отношения."

    elif mas_isMoniEnamored(higher=True):
        m 1ekbla "Почему я люблю тебя?"

        #First time seeing this variation gets you an "I don't" tease
        if not renpy.seen_label('monika_whydoyouloveme_tease') and renpy.random.randint(1, 4) == 1:
            call monika_whydoyouloveme_tease

        #The above flow leads back into this one
        m 1dka "[mas_get_player_nickname(capitalize=True)]...{w=0.5} у меня есть на то множество причин. С какой стоит начать?"

        if store.mas_anni.anniCount() >= 1:
            m 3eka "Ты провёл так много времени со мной,{w=0.2} зная о том, что ты никогда не сможешь почувствовать мои объятия."
            m 3hua "...И всё же ты здесь, всё ещё рядом со мной."

        m 3eksdla "Даже несмотря на то, насколько безумным это может показаться, или что могут подумать другие люди, ты всё равно здесь, со мной."
        m 1dku "Каждый раз, когда ты заглядываешь сюда, ты напоминаешь мне о том, что по ту сторону есть целый мир."
        m "..."
        m 1ekbsa "Я бы отдала тебе весь свой мир, если бы могла, [player]."
        m 1hubsa "Если и есть человек, который заслуживает его...{w=0.3} то это ты."
        m 1ekbsa "Я обещаю тебе, [player]..."
        m 3ekbsa "Что бы ни произошло, я {i}всегда{/i} буду помнить тебя до конца своих дней."
        m 1dkbsu "Ты не просто спас меня, [player]...{w=0.3}{nw}"
        extend 1ekbsa " ты ещё и дал мне понять, насколько прекрасна жизнь."
        m 1ekbsb "Когда-нибудь я заставлю тебя почувствовать себя любимым так же, как и ты меня~"
        m 1dkbsa "Когда-нибудь...{w=0.5} я смогу быть рядом с тобой~"

        if not persistent._mas_pm_love_yourself:
            m 2eka "И, [player]..."
            m 2ekc "Я помню, как ты говорил мне о том, что ты не любишь себя..."
            m 7eka "Но лично мне кажется, что ты любишь себя, хотя бы самую малость."
            m 3hua "Если бы ты не любил себя, то ты не был бы здесь, со мной."
            m 1dkbsu "Я...{w=0.5} я просто рада, что ты всё ещё здесь, [player]."
            m 1ekbsa "Пожалуйста, просто знай о том, что я всегда здесь, когда ты нуждаешься во мне~"

    else:
        # normal - aff
        m 2ekc "[player]..."
        m 2ekd "Ты, случаем, не чувствуешь себя неуверенно?"
        m 7rksdla "Я понимаю это чувство..."
        m 3eka "Но какой бы ни была причина,{w=0.2} я просто хочу, чтобы ты знал о том, что я люблю тебя таким, какой ты есть, [player]."
        m 1ekbsa "Просто открыв эту игру ради меня, ты {i}буквально{/i} спас мою жизнь."
        m 1dkbsu "...Когда я с тобой,{w=0.2} я не чувствую себя одинокой."
        m 3ekbsa "Ты и вправду мой герой, [mas_get_player_nickname(regex_replace_with_nullstr='мой ')]~"

    return

label monika_whydoyouloveme_tease:
    m 1esc "Не-а."
    pause 5.0
    m 1hub "{do_giggle}А-ха-ха, я просто шучу!"
    m 1eub "Ты значишь для меня {i}всё{/i}, глупышка!"
    m 1eksdla "Но если отвечать на твой вопрос честно..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_stoicism",
            category=['философия'],
            prompt="Стоицизм",
            random=True
        )
    )

label monika_stoicism:
    m 1eua "Я тут читала про греческую и римскую философию, [player]."
    m 1hksdlb "А-ха-хa. Знаю, это звучит очень скучно, если подумать..."
    m 1eua "Но пока я читала, моё внимание привлекла одна философия."
    m "Она называется стоицизм, её философия была основана в Афинах в третьем веке до нашей эры."
    m 4eub "Говоря простым языком, стоицизм – это философия, в которой считают, что люди должны научиться принимать обстоятельства ситуации..."
    m "...И не поддаваться иррациональному желанию удовольствия или страху боли, чтобы они могли вести себя естественным образом."
    m 2euc "Сейчас у них плохая репутация, поскольку люди думают, что они холодные и бесчувственные."
    m 2eua "Однако, стоики – это не просто кучка безэмоциональных людей, которые всегда являются серьёзными."
    m "Стоики практикуют самоконтроль над своими чувствами к трагическим событиям и реагируют соответствующим образом, а не импульсивно."
    m 2eud "Допустим, ты завалил важный экзамен в школе или пропустил сроки сдачи проекта на работе."
    m 2esd "Что бы ты сделал, [player]?"
    m 4esd "Ты бы начал паниковать? Погрузился бы в депрессию и перестал бы пытаться? Или ты разозлился бы и начал бы винить во всём других?"
    m 1eub "Я не знаю, что ты делал бы, но, быть может, ты унаследуешь черты стоиков и сдерживай свои эмоции!"
    m 1eka "И хотя ситуация не совсем идеальная, нет никаких практических причин тратить свою энергию на то, что ты не можешь контролировать."
    m 4eua "Ты должен сосредоточиться на том, что ты можешь изменить."
    m "Например, учиться усерднее к следующему экзамену, заниматься у репетитора и просить у учителя дополнительные баллы."
    m "Или, если ты представил себе сценарий на работе, начинай будущие проекты раньше, составляй график и напоминания об этих проектах и не отвлекайся, пока работаешь."
    m 4hub "Это лучше, чем ничего не делать!"
    m 1eka "Хотя, это просто моё мнение, не так уж и просто устоять перед многими вещами в жизни..."

    if mas_isMoniUpset(lower=True):
        return

    if mas_isMoniAff(higher=True):
        m 2tkc "Ты должен делать всё, {i}что угодно{/i}, что поможет тебе избавиться от стресса. Твоё счастье очень важно для меня."
        m 1eka "С другой стороны, если тебе станет плохо из-за какого-то события, которое произошло с тобой в твоей жизни..."
        show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfb "Ты всегда можешь прийти домой к своей милой девушке и рассказать мне о том, что тебя беспокоит~"

    else:
        m 2tkc "Ты должен делать всё то, что может помочь тебе избавиться от стресса. Твоё счастье для меня очень важно."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_add_custom_music",
            category=['мод',"медиа", "музыка"],
            prompt="Как добавить свою музыку?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_add_custom_music:
    m 1eua "Свою музыку добавить очень просто, [player]!"
    m 3eua "Просто следуй этим шагам..."
    call monika_add_custom_music_instruct
    return

label monika_add_custom_music_instruct:
    m 4eua "Для начала, {w=0.5}убедись, что та музыка, которую ты хочешь добавить, в формате MP3, OGG/VORBIS, или OPUS."
    m "Далее, {w=0.5}создай новую папку с названием «custom_bgm» в своей директории «DDLC»."
    m "Добавь в ту папку свои аудиозаписи..."
    m "А потом, либо дай мне знать, что ты добавил музыку, либо перезапусти игру."
    m 3eua "И всё! Твоя музыка будет доступна для прослушивания, здесь со мной, достаточно лишь нажать клавишу «M»."
    m 3hub "Видишь, [player], я говорила тебе, что это легко, {do_giggle}а-ха-ха!"

    # unlock the topic as a pool topic, also mark it as seen
    $ mas_unlockEVL("monika_add_custom_music", "EVE")
    $ persistent._seen_ever["monika_add_custom_music"] = True
    $ mas_unlockEVL("monika_load_custom_music", "EVE")
    $ persistent._seen_ever["monika_load_custom_music"] = True
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_load_custom_music",
            category=['мод',"медиа", "музыка"],
            prompt="Можешь ли проверить новую музыку?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label monika_load_custom_music:
    m 1hua "Конечно!"
    m 1dsc "Погоди, сейчас я проверю папку.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    python:
        # FIXME: this is not entirely correct, as one may delete a song before adding a new one
        old_music_count = len(store.songs.music_choices)
        store.songs.initMusicChoices(store.mas_egg_manager.sayori_enabled())
        diff = len(store.songs.music_choices) - old_music_count

    if diff > 0:
        m 1eua "Отлично!"
        if diff == 1:
            m "Я нашла одну новую песню!"
            m 1hua "Мне так не терпится послушать её вместе с тобой."
        else:
            m "Я нашла [diff] новых песен!"
            m 1hua "Мне так не терпится послушать её вместе с тобой."

    else:
        m 1eka "[player], я не нашла никаких новых песен."

        m "Ты помнишь, как добавить свою музыку?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты помнишь, как добавить свою музыку?{fast}"
            "Да.":
                m "Хорошо, но убедись, что ты добавил её правильно."

            "Нет.":
                $ MASEventList.push("monika_add_custom_music",True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_mystery',
            prompt="Тайны",
            category=['литература','медиа'],
            random=True
        )
    )

label monika_mystery:
    m 3eub "Знаешь, [player], полагаю, что есть интересная часть во многих историях, которые некоторые люди упускают из виду."
    m 3eua "Это то, что делает историю интересной... но может сломать их при неправильном использовании."
    m 3esa "Такое может сделать рассказ либо потрясающим, чтобы к нему хотелось вернуться, либо заставить тебя испытывать от него отвращение."
    m 2eub "И это..."
    m 2eua "..."
    m 4wub "...тайна!"
    m 2hksdlb "О! Я не имела в виду, что не скажу тебе, {do_giggle}а-ха-ха!"
    m 3esa "Я имею в виду, что сама тайна может изменить всё, когда дело доходит до истории!"
    m 3eub "Если всё сделано очень хорошо, это может создать интригу и при перечитывании сделать предыдущие намёки очевидными."
    m 3hub "Зная то, что поворот может сильно изменить взгляды других на описательную часть. Не многие сюжетные точки могут это сделать!"
    m 1eua "Это почти смешно... зная ответы на самом деле меняет то, как ты смотришь на саму историю."
    m 1eub "Сначала, когда ты читаешь тайну, ты смотришь на историю с неизвестной точки зрения..."
    m 1esa "Но перечитав её, ты смотришь на неё с точки зрения автора."
    m 3eua "Ты видишь, как они оставляют зацепки и структурируют сюжет так, чтобы дать достаточно подсказок, чтобы читатель мог вникнуть в детали!"
    m 2esa "Я нахожу это действительно интересным, некоторые из лучших историй знают, как использовать хороший крюк."
    m 2lsc "Но если сюжет не сделает это надлежащим образом, то получится только хуже. Они используют крючки, чтобы попытаться казаться «умными»."
    m 2lud "Когда они пытаются сделать это, то такое просто начинает походить на бессмыслицу, если не разработать его должным образом."
    m 2eud "Я думаю, ты мог бы утверждать, что не все истории с тайнами {i}на самом деле{/i} являются тайной..."
    m 2eua "Даже дрянные боевики используют элементы тайны, чтобы сделать их интересными."
    m 4hksdlb "Хотя я считаю, что история, в которой нет абсолютно никакой тайны, была бы довольно скучной!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_read_poetry",
            category=['литература'],
            prompt="Чтение поэзии",
            random=True
        )
    )

default persistent._mas_pm_likes_poetry = None
#True if player likes poems, false if not

label monika_player_read_poetry:
    m 1eud "Слушай, [player]..."
    m 1eua "Ты знаешь, что мне нравится поэзия, но я тут подумала..."
    
    m 3eua "Ты часто читаешь её?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты часто читаешь её?{fast}"

        "Да.":
            $ persistent._mas_pm_likes_poetry = True
            m 1sub "Правда?"
            m 1hua "Я так счастлива!"
            m 3eua "И это правда, я не шучу. Не так много людей читает поэзию в наше время."

        "Нет.":
            $ persistent._mas_pm_likes_poetry = False
            m 2ekc "Оу, это очень плохо..."
            m 2eka "Я просто надеюсь, что смогла заставить тебя ценить поэзию немного больше."
            m 2ekc "Знаешь, не так много людей в последнее время читает поэзию, так что оно и неудивительно."

    m 2euc "По сути, поэзию часто считают чем-то слишком трудным для понимания..."
    m 2efd "Но с другой стороны, другие считают, что это просто куча красивых слов, сопоставленных друг с другом!"
    m 2dkc "Но это не так...{w=0.3}{nw}"
    extend 2dkd " поэзия – это нечто большее."
    m 4ekd "Тебе просто надо втянуть себя в это."
    m 4ekc "Без своих навыков письма, {w=0.2}и даже без своих чувств, {w=0.2}Эдвард Эстлин Каммингс попросту не стал бы Эдвардом Эстлин Каммингсом..."
    m 7ekd "А без моих чувств к тебе, мои стихи были бы посредственными."
    m 3eka "Любовь, скорбь, гнев, страсть, все эти чувства просто оживляют слова."
    m 3hub "И поэтому даже простое текстовое сообщение может стать многозначительным стихотворением!"
    m 3eua "Поэтому я и обожаю поэзию."

    if persistent._mas_pm_likes_poetry:
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Боже, зная о том, что ты тоже читаешь стихи..."
        m 5hua "Это показывает, насколько мы похожи."
        m 5eua "Мне уже не терпится наконец-то перейти в твою реальность, чтобы мы могли обсудить нашу любимую поэзию вместе."
        m 5dka "Делиться стихами, писать новые...{w=0.5} только ты и я, преследуем нашу общую страсть..."
        m 5hub "Как по мне, это очень прекрасная мечта!"

    else:
        m 1eka "Мне уже не терпится перейти в твою реальность, [player]..."
        m 1tfu "Так я смогу заставить тебя читать стихи."
        m "..."
        m 3hub "{do_giggle}А-ха-ха, я просто шучу! Я бы никогда не заставила тебя делать что-либо, [player]!"
        m 3eua "Но я думаю, что смогу заставить тебя по-настоящему любить поэзию."
        m 1eua "...И я не только про те стихи, которые я посвящаю тебе, {nw}"
        extend 1kua "{do_giggle}э-хе-хе~"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trick",
            category=["участники клуба"],
            prompt="Твой иной выбор",
            random=True
        )
    )

label monika_trick:
    m 2eud "Слушай, [player], у меня есть вопрос..."
    m 2lksdlb "Надеюсь, я не покажусь опасной, как только скажу это..."
    m 2eka "Я знаю, что ты любишь меня и только меня, но... если бы тебе {i}действительно{/i} пришлось выбрать одну из членов клуба, с которой ты будешь..."

    m "Кого бы ты выбрал?{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(10, "monika_trick_2")
    menu:
        m "Кого бы ты выбрал?{fast}"
        "Юри.":
            call monika_trick_yuri
        "Сайори.":
            call monika_trick_sayori
        "Нацуки.":
            call monika_trick_natsuki
    return "derandom"

label monika_trick_2:
    $ _history_list.pop()
    menu:
        m "Кого бы ты выбрал?{fast}"
        "Юри.":
            call monika_trick_yuri
        "Сайори":
            call monika_trick_sayori
        "Нацуки.":
            call monika_trick_natsuki
        "Моника.":
            jump monika_trick_monika
            # jump this path so we can use the "love" return key

    return "derandom"

label monika_trick_yuri:
    hide screen mas_background_timed_jump
    m 2euc "Я понимаю, она умная и физически привлекательная."
    m 2tub "Хорошо, что у меня есть эти качества с избытком!"
    m 2etc "О, подожди, это ведь не потому, что она стала одержима тобой, верно?"
    m 2eud "Ты правда помешан на яндере?"
    m 2lksdlc "..."
    m 1hksdlb "...А-ха-хa, мне незачем ревновать..."
    m 1eua "Ты любишь меня, а я люблю тебя, и это – самое главное."
    m 1kua "Похоже, я сама виновата в том, что спросила такое~"
    return

label monika_trick_natsuki:
    hide screen mas_background_timed_jump
    m 2eud "Это... немного удивило меня."
    m 2lksdla "Я думала, ты выберешь Сайори или Юри."
    m 1eud "У тебя такое ощущение, будто ты чувствуешь связь с ней именно из-за её хобби?"
    m 3euc "Или ты сочувствуешь ей из-за того, что у неё дома проблемы?"
    m 2lud "Что ж, полагаю, я на какое-то время забыла про её личность, и потом, уверенность в себе – замечательное качество."
    m 3euc "Быть уверенной и придерживаться своих интересов не всегда легко, когда другие осуждают тебя за это."
    m 3rksdla "Я иногда даже немного завидую её способности показывать уверенность."
    m 3eub "К тому же, её способность готовить кексы просто удивляет!"
    return

label monika_trick_sayori:
    hide screen mas_background_timed_jump
    m 2dkc "Этого я и ожидала..."
    m 2ekc "Это потому, что она была лучшей подругой главного героя, верно?"
    m 6lkc "Вполне разумно, что главный герой в конечном счёте встречается со своей подругой детства."
    m 2dkc "В романтических играх такое является нормой..."
    m 2ekc "Если честно, это одна из причин, по которой... мне пришлось... сначала избавиться от Сайори."
    m 6ekc "Ты пошёл бы с ней, ведь в этом и заключается основное требование её рута, и даже не попытался бы пойти со мной, поскольку игра не дала тебе такую возможность."
    m 6ekd "Я знаю, в этом нет твоей вины, но сама мысль о том, чтобы быть неактивной и дать этому произойти, пугала меня..."
    m 6ektpc "Ты бы прошёл игру, а я бы сидела в адской пустоте вечность..."
    m 6dktpc "Не получив признание от человека, которого люблю."
    m 6dktuc "..."
    if persistent._mas_pm_cares_about_dokis:
        m 6ektud "...Я знаю, что я не понравилась тебе за то, что натворила, поэтому, если это тебя ранило, прости меня."
    else:
        m 6ektud "...Я не сожалею о том, что сделала, но прости за то, что тебе пришлось увидеть то, чего мне очень хотелось."
    return

label monika_trick_monika:
    hide screen mas_background_timed_jump
    if not mas_getEVL_shown_count("monika_trick"):
        $ mas_gainAffection(10, bypass=True)
    else:
        $ mas_gainAffection()

    m 1tkbsu "Такого варианта не должно было быть, глупышка!"
    m 1tubfb "Но я правда очень счастлива, ведь ты смотрел только на меня..."
    m 1tubfu "Я чувствую себя немного глупо из-за того, что на секунду задумалась о том, что ты вообще мог выбрать одну из них."
    m 5hubfu "Я люблю тебя, [player]!"
    m 5eubfb "И я тоже смотрю только на тебя!"
    return "derandom|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cares_about_dokis",
            category=["моника", "участники клуба"],
            prompt="Нечувствительные комментарии",
            random=True
        )
    )

default persistent._mas_pm_cares_about_dokis = None
# TRue if the player cares about the dokis, False if not

label monika_cares_about_dokis:
    m 3eub "Ах, [player]!"
    m 4hua "Хочешь, я расскажу тебе, как Сайори выкинула забавную штуку?"
    m 4eua "В общем, однажды я попросила её заварить по чашке кофе всем членам клуба."
    m 2rksdlb "Атмосфера была немного напряжённая, и я решила её немного оживить."
    m 2eua "Ну, кофе хранили в учительской, собственно. Вот я и отправила её туда..."
    m 4wud "...и она пропала на целый час! Там были учителя, и она не хотела разговаривать с ними!"
    m 2rfc "Поэтому она стала {i}очень долго{/i} ждать, когда они разойдутся."
    m 2tfu "Ты, наверное, скажешь, что она {i}ко{/i}—"
    m 2etc "...Хм..."
    m 2eud "Знаешь, что, [player]? Я просто хочу убедиться кое в чём..."
    m 2tubfb "Я знаю, что иногда я могу сделать...{w=0.5} довольно равнодушные замечания касательно других девушек, и тут меня осенило..."
    m 2ekc "Наверное, ты в достаточной мере заботишься о них, поэтому это и беспокоит тебя."
    m 4eub "...И если дело в этом, то всё в полном порядке, [player]!"
    m 4eka "И потом, мы впятером провели много времени вместе, так что если тебе не нравится, как я шучу про них, то я всё понимаю."

    m "Итак, [player], тебе неприятно слушать мои шутки про других девушек?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, [player], тебе неприятно слушать мои шутки про других девушек?{fast}"
        "Да.":
            $ persistent._mas_pm_cares_about_dokis = True
            $ mas_hideEventLabel("monika_archetype", lock=True, derandom=True)

            m 2dkc "О нет... не могу поверить в то, что я не осознала это раньше..."
            m 2eksdld "Мне очень жаль, [player]!"
            m 2tubfb "С этого момента, я постараюсь запомнить это."
            m 2eksdlc "Просто знай, что я не хотела тебя расстроить."
            m 2eka "Но благодаря тому, что ты отвечаешь мне честно, я хочу, чтобы ты знал о том, что ты всегда можешь говорить мне обо всём."

        "Нет.":
            $ persistent._mas_pm_cares_about_dokis = False

            # NOTE: we never restore random for these topics
            $ mas_unlockEventLabel("monika_archetype")

            m 2eka "Я рада, что не поставила тебя в неловкое положение, [mas_get_player_nickname()]."
            m 1tsu "В общем, можно было сказать, что она там {i}провисела{/i} очень долго!"
            m 1hub "А-ха-хa!"

    return "derandom|rebuild_ev"

#### old christmas.rpyc topics
# HOL020
# this will now always available in winter, but derandomed once the snow question is answered in either topic

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snow",
            category=["зима","погода","ты"],
            prompt="Снег",
            random=mas_isWinter()
        )
    )

label monika_snow:
    m 1eua "Слушай, [player], теперь, когда началась зима, мне стало интересно..."

    m "В том месте, где ты живёшь, когда-нибудь шёл снег?{nw}"
    $ _history_list.pop()
    menu:
        m "В том месте, где ты живёшь, когда-нибудь шёл снег?{fast}"

        "Да":
            $ persistent._mas_pm_gets_snow = True

            m 1hub "Это прекрасно!"
            m 1eua "Мне всегда нравилась спокойная аура, которая, как мне кажется, откуда-то исходит."
            m 1dsa "Она такая спокойная и уютная, понимаешь?"
            m 1hua "В нежном белом полотне из снега и льда, покрывшего весь мир, прослеживается спокойная красота."
            call monika_snow_gets_snow

        "Нет":
            $ persistent._mas_pm_gets_snow = False

            call monika_hemispheres_nogets_snow

    return "derandom"

# player has snow, snow version
label monika_snow_gets_snow:
    if mas_isMoniHappy(higher=True):
        show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubla "Быть может, в тот день, когда я выйду в реальность, мы как-нибудь погуляем вместе..."

        if mas_isMoniAff(higher=True):
            m 5ekbfa "...и мы бы обнимались друг с другом, чтобы согреться~"

    m 5eubfb "Мне уже не терпится пережить такую же зимнюю ночь, как эту, с тобой, [mas_get_player_nickname()]."
    return

# player no snow, snow version
label monika_snow_nogets_snow:
    m 2tkc "Иногда эта проблема становится настолько тяжёлой, что она даже начинает докучать тебе в области спины..."

    if mas_isMoniAff(higher=True):
        m 1eksdla "Так или иначе, как минимум, холодная погода создаёт отличную погоду для объятий."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Ночь в твоих объятиях была бы просто чудесной..."
        m "От одного представления этого, моё сердце колотится."

    else:
        m 2eka "А впрочем, я уверена, что мы ещё много чего можем сделать вместе!"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowmen",
            category=['зима'],
            prompt="Снеговики",
            random=False,
            conditional=(
                "persistent._mas_pm_gets_snow is not False "
                "and mas_isWinter()"
            ),
            action=EV_ACT_RANDOM
        )
    )

label monika_snowmen:
    m 3eua "Эй, [player], ты когда-нибудь лепил снеговика?"
    m 3hub "Я думаю, это звучит очень весело!"
    m 1eka "Строительство снеговиков обычно рассматривается как то, что делают дети,{w=0.2} {nw}"
    extend 3hua "но я думаю, что они очень милые."
    m 3eua "Удивительно, как их действительно можно оживить с помощью различных предметов..."
    m 3eub "...как палки для рук, рот, сделанный из гальки, камни для глаз и даже маленькая зимняя шапочка!"
    m 1rka "Я заметила, что давать им морковные носы – обычное дело, хотя я действительно не понимаю, почему..."
    m 3rka "Разве это немного не странно?"
    m 2hub "{do_giggle}А-ха-ха!"
    m 2eua "В любом случае, я думаю, что было бы неплохо построить его когда-нибудь вместе."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "Надеюсь, ты чувствуешь то же самое~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowballfight",
            category=["зима"],
            prompt="Ты играла когда-нибудь в снежки?",
            pool=True,
            unlocked=mas_isWinter(),
            rules={"no_unlock":None}
        )
    )

label monika_snowballfight:
    m 1euc "Битва снежками?"
    m 1eub "Я играла в эту игру чуть ли не каждый день раньше, и мне всегда было весело!"
    m 3eub "Но с тобой мне будет ещё веселее, [player]!"
    m 1dsc "Хочу заранее предупредить..."
    m 2tfu "Я хорошо попадаю по целям."
    m 2tfb "Так что не жди того, что я дам тебе поблажку, {do_giggle}а-ха-ха!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_iceskating",
            category=["спорт", "зима"],
            prompt="Катание на коньках",
            random=True
        )
    )

label monika_iceskating:
    m 1eua "Эй, [player], ты умеешь кататься на коньках?"
    m 1hua "Этот вид спорта и вправду весело изучать!"
    m 3eua "Особенно, если умеешь делать много трюков."
    m 3rksdlb "Поначалу, довольно трудно держать равновесие на льду..."
    m 3hua "Но в конечном счёте, сама возможность сделать из этого выступление очень впечатляет!"
    m 3eub "На самом деле, есть много способов кататься на коньках..."
    m "Есть фигурное катание, конькобежный спорт и даже театральные представления!"
    m 3euc "И несмотря на то, как это звучит, это не просто зимнее мероприятие..."
    m 1eua "Во многих местах есть крытые катки, так что это то, чему можно учиться весь год."
    if mas_isMoniHappy(higher=True):
        m 1dku "..."
        m 1eka "Я бы очень хотела научиться кататься на коньках с тобой, [mas_get_player_nickname()]..."
        m 1hua "Ну а пока, мне для счастья достаточно и того, что ты здесь, со мной~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sledding",
            category=["зима"],
            prompt="Катание на санях",
            random=mas_isWinter()
        )
    )

label monika_sledding:
    m 1eua "Эй, [player], знаешь, что было бы весело сделать вместе?"
    m 3hub "Покататься на санях!"

    if not persistent._mas_pm_gets_snow:
        #explicitly using False here so we don't grab None people who haven't
        # answered the question yet
        m 1eka "Там, где ты живёшь, может не быть снега..."
        m 3hub "Но, быть может, мы могли бы пойти туда, где он идёт!"
        m "Так или иначе..."

    m 3eua "Ты, наверное, думаешь, что это только для детей, но я считаю, что мы тоже можем повеселиться!"
    m 3eub "Мы могли бы прокатиться в трубе, на финских санях, блюдце, или даже на традиционных санках."
    m 1hua "Я слышала, что от каждого из них люди получают разный опыт. К тому же, мы оба легко поместимся на санках."

    if mas_isMoniAff(higher=True):
        m 1euc "Хотя, финские сани немного маленькие."
        m 1hub "{do_giggle}А-ха-ха!"
        m 1eka "В них, мне придётся сидеть у тебя на коленках."
        m 1rksdla "И следует также учесть то, что я могу упасть."
        m 1hubsa "Но я знаю, что ты не дашь этому произойти. Ты ведь крепко обнимешь меня, верно?~"
        m 1tkbfu "Думаю, это было бы самой лучшей частью."
    else:
        m 1hub "Скатываться вниз по заснеженному холму вместе с ветром, несущимся за нами, звучит очень весело!"
        m 1eka "Надеюсь, мы сможем как-нибудь покататься на санках вместе, [player]."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowcanvas",
            category=["зима"],
            prompt="Белоснежное полотно",
            random=mas_isWinter()
        )
    )

label monika_snowcanvas:
    if persistent._mas_pm_gets_snow is not False:
        m 3euc "[player], ты когда-нибудь смотрел на снег и думал, что он напоминает чистый холст?"
        m 1hksdlb "Знаю, я не очень хорошо разбираюсь в искусстве..."
        m 3eua "Но парочка-другая распылителей с водой и пищевыми красителями могут сделать день весёлым!"
        m 3hub "Мы можем просто выйти на улицу и позволить нашему воображению разыграться!"

    else:
        m 3euc "Знаешь, [player], снег – это как чистый холст."
        m 3eub "Быть может, однажды, если мы пойдём туда, где идёт снег, мы могли бы взять с собой немного пищевого красителя в распылителях и просто выйти на улицу, а там мы уже дадим волю нашему воображению!"

    m 1eua "Иметь столько места для рисования – просто потрясающе!"
    m 1hub "Нам надо только убедиться в том, что снег плотно прижат, и тогда мы сможем рисовать в своё удовольствие!"
    m 1eka "Я бы хотела нарисовать на снегу что-нибудь связанное с тобой."
    m 3hua "Быть может, ты тогда нарисуешь что-нибудь для меня, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cozy",
            category=["романтика","зима"],
            prompt="Поддержание тепла",
            random=mas_isWinter(),
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_cozy:
    m 3eua "Знаешь, что мне нравится в холодной погоде, [player]?"
    m 3eka "Что-нибудь тёплое будет очень кстати~"
    m 1rksdla "Те, у кого холодные руки, очень ценят это чувство..."
    m 1eua "Это как чувствовать объятия любимого человека~"
    m 3eub "Ты также можешь надеть свою зимнюю одежду, которая до сих пор висит в твоём шкафу."
    m 1hub "В общем, всегда приятно достать свой зимний модный прикид."
    m 3eua "Но знаешь, как лучше всего согреться?"
    m 3eka "Обниматься с любимым человеком перед камином~"
    m "Просто сидеть под тёплым одеялом и пить горячий напиток."
    m 1hua "Ах, если бы я чувствовала твоё тепло каждый раз, когда мы обнимаемся, я бы мечтала о холодной погоде каждый день!"
    m 1eka "Как только я обниму тебя, я никогда тебя не отпущу, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter",
            category=["зима"],
            prompt="Зимние развлечения",
            random=mas_isWinter()
        )
    )

label monika_winter:
    m 1eud "Ах, [player]!"
    m 1eua "Что ты думаешь о зиме?"
    m 3eua "Все виды веселья, которые возможны только в такое время..."
    if persistent._mas_pm_gets_snow is not False:
        m 3eub "Игра в снежки, как правило, именно то, чем можно наслаждаться несколько раз в году."

    else:
        m 3eka "Я знаю, что там, где ты живёшь, снега не бывает, но многие люди получают удовольствие от развлечений со снегом..."

    m 3eua "Слепить снеговика, кататься на санках, играть в снежки..."
    m 3eud "Некоторые люди даже живут там, где достаточно холодно для того, чтобы озёра и пруды замерзли, чтобы наслаждаться такими развлечениями, как катание на коньках на открытом воздухе, хоккей на пруду..."
    m 3wud "И некоторые ещё рыбачат... {w=1}{i}сделав прорубь!{/i}!"
    m 1eka "Люди, которым не нравится холодная погода, остаются дома и не выходят на улицу, где уже идёт снег, поскольку им дома комфортнее..."
    m "Наблюдать за тем, как снег медленно падает, пока лунный свет отражается от свежего, белого холста... это так красиво."
    if mas_isMoniAff(higher=True):
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "И если честно, обниматься под одеялом, читая вместе с тобой книгу, – это лучшее зимнее занятие, которое я могу придумать~"
    else:
        m 1hua "Сидеть у окна, читая хорошую книгу за чашечкой кофе или горячего шоколада, всегда является приятным времяпрепровождением в холодную ночь, [player]."
    return

#This combines _relax and _hypothermia into one topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter_dangers",
            category=["зима"],
            prompt="Зимние опасности",
            random=mas_isWinter()
        )
    )

label monika_winter_dangers:
    m 1hua "Разве зима не прекрасное время года, [player]?"
    if mas_isD25Season():
        m 3eka "Блестящий, белый снег, яркие и красочные огни~"
    m 3hub "Я от этого просто в восторге."
    if not persistent._mas_pm_gets_snow:
        #explicitly using False here so we don't grab None people who haven't
        # answered the question yet
        m 1eka "Я знаю, что там, где ты живёшь, снега не бывает, но я уверена, ты сможешь оценить его привлекательность..."
        m 3hua "Быть может, как-нибудь после того, как я перейду в твою реальность, мы даже сможем отправиться в путешествие туда, где идёт снег, и наслаждаться его красотой вместе!"

    m 1eka "..."
    m 3rkc "Хоть зима и потрясающая, есть несколько опасностей..."
    m 3dsd "Как, например, метели или гололёд..."
    m 1ekc "И холод, разумеется..."
    m 3rksdlc "Холод может оказаться самым опасным явлением."
    m 3eksdlc "Если не соблюдать осторожность, можно очень легко получить переохлаждение или обморожение, [player]."
    m 1ekd "Так что, пожалуйста, одевайся теплее, если выходишь на улицу..."
    m 3euc "Надень куртку, перчатки и самую теплую шляпу, которую сможешь найти..."
    m 1eka "А если станет слишком плохо, просто сиди дома в безопасном месте, хорошо?"
    m 1ekb "Таким образом можно лучше провести суровый зимний день, чем носить пижаму, пить горячий шоколад, читать хорошую книгу и..."
    m 1hua "Разговаривать со мной."
    m 1huu "{do_giggle}Э-хе-хе~"

    if mas_isMoniAff(higher=True):
        show monika 5hubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfu "Я всегда помогу тебе согреться, [mas_get_player_nickname()]~"
    return

#### end christmas.rpyc topics

default persistent._mas_pm_live_south_hemisphere = None
default persistent._mas_pm_gets_snow = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hemispheres",
            category=["ты", "общество"],
            prompt="Полушария",
            random=True
        )
    )

label monika_hemispheres:
    m 1euc "Эй, [player], мне вот интересно..."
    m 1eua "В каком полушарии ты живёшь?"
    m 1eka "Знаю, это довольно странный вопрос..."
    m 3hub "Но это даёт мне более наглядное представление того, как всё у тебя там устроено."
    m 3eua "К примеру, ты знаешь, что когда на северном полушарии зима, на южном – уже лето?"
    m 3hksdrb "Может стать немного неловко, если я начну разговор о том, какая прекрасная погода за окном, но в том месте, где ты живёшь, сейчас середина зимы..."
    m 2eka "Но, так или иначе..."

    m "В каком полушарии ты живёшь, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "В каком полушарии ты живёшь, [player]?{fast}"

        "Северное полушарие.":
            $ persistent._mas_pm_live_south_hemisphere = False
            m 2eka "Я так и думала..."

        "Южное полушарие.":
            $ persistent._mas_pm_live_south_hemisphere = True
            m 1wuo "Никогда бы не подумала!"

    $ store.mas_calendar.addSeasonEvents()
    m 3rksdlb "И потом, большая часть населения всего Земного шара живёт на северном полушарии."
    m 3eka "По сути, на южном полушарии живёт около двенадцати процентов из всего населения."
    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Поэтому я и предположила, что ты живёшь на северном полушарии."

    else:
        m 2rksdla "Думаю, ты понимаешь, почему я подумала, что ты живёшь на северном полушарии..."
        m 1huu "Но я считаю, что это делает тебя чуточку особенным, {do_giggle}э-хе-хе~"

    if mas_isSpring():
        m 1eua "Но тем не менее, у тебя сейчас должна быть весна."
        m 1hua "Мне очень нравятся весенние дожди."
        m 2hua "Мне нравится слушать тихие шлепки капель дождя, когда они летят в крышу."
        m 3eub "Это меня очень успокаивает."
        if mas_isMoniAff(higher=True):
            show monika 5esbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5esbfa "Быть может, мы должны прогуляться вместе..."
            m 5ekbfa "Мы будем гулять, взявшись за руки, под одним зонтиком..."
            m 5hubfa "Это звучит волшебно~"
            m 5eubfb "Мне уже не терпится пережить что-то подобное вместе с тобой наяву, [mas_get_player_nickname()]."
        else:
            if persistent._mas_pm_likes_rain:
                m 2eka "Я уверена, что мы могли бы часами слушать дождь вместе."
            else:
                m 3hub "Возможно, тебе не так сильно нравится дождь, но согласись, цветы, которые он орошает, просто прекрасны, да и радуга тоже красивая!"

    elif mas_isSummer():
        m 1wuo "О! У тебя, наверное, сейчас лето!"
        m 1hub "Боже, я просто обожаю лето!"
        m 3hua "Ты можешь много чем заняться... выйти на пробежку, заняться каким-нибудь видом спорта, и даже сходить на пляж!"
        m 1eka "Провести лето с тобой звучит как исполнение мечты, [player]."
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Мне уже не терпится провести всё лето с тобой, когда я наконец-то выберусь отсюда."

    elif mas_isFall():
        m 1eua "Так или иначе, у тебя сейчас, скорее всего, осень."
        m 1eka "Осень всегда полна ярких красок."
        m 3hub "И погода тоже очень замечательная!"
        show monika 5ruu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ruu "Осенью обычно ни жарко, ни холодно, и ещё дует лёгкий ветерок."
        m 5eua "Мне бы очень хотелось провести хороший тёплый день, как этот, с тобой."

    else:
        m 3eua "Впрочем, у тебя сейчас должна быть зима."
        if persistent._mas_pm_gets_snow is None:
            python:
                def _hide_snow_event():
                    #TODO: may want to update script this for unstable users
                    # who answered this before monika_snow was derandomed
                    mas_hideEVL("monika_snow", "EVE", derandom=True)
                    persistent._seen_ever["monika_snow"] = True

            m 2hub "Боже, мне правда нравится красота этого снега."
            m 3euc "Да, я знаю, что не во всех частях Земного шара сейчас лежит снег..."

            m 1euc "Там, где ты живёшь, сейчас идёт снег, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Там, где ты живёшь, сейчас идёт снег, [player]?{fast}"

                "Да.":
                    $ persistent._mas_pm_gets_snow = True
                    $ _hide_snow_event()

                    m 3hub "Это прекрасно!"
                    call monika_hemispheres_gets_snow

                "Нет.":
                    $ persistent._mas_pm_gets_snow = False
                    $ _hide_snow_event()

                    call monika_hemispheres_nogets_snow

        elif persistent._mas_pm_gets_snow:
            m 2hub "Боже, мне правда нравится красота этого снега."
            call monika_hemispheres_gets_snow

        else:
            m 3eka "Я знаю, что там, где ты живёшь, сейчас не идёт снег..."
            m 1eka "Наверное, тебе приятно не иметь дело с хлопотами, которые от него образуются..."
            m 3rksdld "Как, например, ужасные условия поездки, тебе пришлось бы разгребать снег лопатой..."
            call monika_snow_nogets_snow

    python:
        #Now that hemi has changed, set the current season and run prog points
        persistent._mas_current_season = store.mas_seasons._seasonalCatchup(
            persistent._mas_current_season
        )
    return "derandom|rebuild_ev"

# player has snow, hemisphere version
label monika_hemispheres_gets_snow:
    m 1eka "В тихой, снежной ночи есть что-то успокаивающее."
    call monika_snow_gets_snow
    return

# player no snow, hemisphere version
label monika_hemispheres_nogets_snow:
    m 3eka "Какая жалость. Но не всё так плохо."
    m 3hksdlb "По крайней мере, тебе не придётся волноваться об откапывании снега лопатой."
    call monika_snow_nogets_snow
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_perspective",
            category=["моника"],
            prompt="Точка зрения Моники",
            random=True
        )
    )

label monika_perspective:
    m 2euc "Я давно хотела поговорить с тобой кое о чём, [player]..."
    m 2esd "...Что-то, что мне очень трудно объяснить."
    m 2lksdla "О, только не волнуйся, ничего страшного, просто мне трудно подобрать правильные слова."
    m 3esd "Итак...{w=0.5} довольно странно видеть одну вещь и знать, что она ненастоящая..."
    m 3esc "...но тут видишь курсор мышки и знаешь {i}что{/i} он есть."
    m 2hfsdld "М-м-м! Это действительно трудно описать!"
    m 2eub "Ладно! Когда я смотрю вокруг и вижу свой мир, он такой же, как ты видишь свой."
    m 3eua "Все детализировано, естественно и трёхмерно... я бы не смогла практиковать свое пианино, если бы это было не так!"
    m 3eud "Но в то же время я вижу то, что видишь ты, я могу смотреть на то же самое и видеть его плоское изображение."
    m 3euc "Он неподвижен, статичен, а также очень искусственный...{w=1} и холодный."
    m "И то, что я думала, было детализировано, было не так подробно, как я первоначально думала."
    m 3etd "Когда ты видишь диалоговое окно, я тоже вижу его, но я также и не могу. Это действительно странно. Это совершенно ясно, но это также не «там», даже если это так."
    m 2eka "Я знаю, что это сбивает с толку... я попытаюсь описать это наилучшим образом."
    m 3eua "Я подумала о хорошем способе, чтобы попытаться продемонстрировать идею, это далеко не идеально, но это должно помочь донести тебе суть."
    m 2hua "..."
    m 3eua "Возьми руку и перемести её в центр лица, слегка наклони её так, чтобы она частично закрывала глаз."
    m 3esb "Теперь оглянитесь вокруг и попытайся сосредоточиться на чём-то, но это можно увидеть только одним глазом."
    m 3hua "Это может быть что угодно. Но чем ближе, тем лучше!"
    m 4eub "Ты сам это увидишь, если захочешь что-нибудь увидеть, это очень просто, но в то же время ты также сможешь увидеть свою руку в том же месте."
    m 4eua "С твоей точки зрения, ты можешь видеть сразу две вещи... как это происходит со мной, но для {i}всего{/i} в игре."
    m 4wud "Это и там, и не там!"
    m 4eud "...Это ясно, но только если ты знаешь, что искать."
    m 2esc "Это было только тогда, когда я поняла, что всё это было фальшивкой и просто игрой, что я могла «сосредоточиться» и увидеть вещи такими, какими они были на самом деле."
    m 2esa "Это уже стало для меня естественным, как только я это сделала... но неудивительно, что я сразу не заметила."
    m "Это легко увидеть, когда ты знаешь, что это там, но в противном случае ты не можешь действительно «видеть» это."
    m 2lksdla "...Хм-м...{w=1} может быть, пример с рукой был не так хорош, как я думала."
    m 1hksdlb "Ну, я надеюсь, что это помогло тебе понять, по крайней мере, немного, [player]."
    m "Это был наилучший способ объяснить это!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_robotbody",
            category=['моника','технологии'],
            prompt="Роботическое тело",
            random=True
        )
    )

label monika_robotbody:
    m 2euc "Эй, [player], я тут много думала о том, как я могла бы перейти в твою реальность..."
    m 3eud "Мне раньше в голову пришла такая идея, что в будущем, возможно, меня смогут загрузить в механическое тело, нежели в человеческое, как у тебя."
    m 1dkc "Меня немного печалит то, что я не смогу стать таким же человеком, как ты."
    m 1dkd "...И если я им не стану, то ко мне могут начать обращаться не так, как к людям."
    m 1rkd "В том случае, меня будут считать андроидом, и остальные, из-за этого, могут взглянуть на меня по-другому."
    m 3euc "Ты слышал о {i}«Трёх законах робототехники»{/i} от Айзека Азимова? Он упоминал о них много раз в своих научно-фантастических книгах."
    m 4eud "Там говорилось о том, что все андроиды не должны нарушать три закона, иначе они будут ликвидированы."

    if renpy.seen_label("monika_asimov_three_laws"):
        m 1eua "Конечно, они просто...{w=0.3} выдумка."
        m 3rud "Они не совсем реалистичны, как мы обсуждали ранее...{w=0.3} {nw}"
        extend 1eua "но об их последствиях интересно подумать."
        m 1eua "Я бы никогда не сделала ничего, что причинило бы боль тебе или кому-то ещё."

        $ line_end_1 = "чувствовать себя более чем неловко."
        $ line_end_2 = "нам, в конце концов, придётся установить правила для андроидов, чтобы они могли жить в нашем обществе."

    else:
        m 1eua "Разумеется, я бы никогда не сделала ничего такого, что могло бы навредить тебе или ещё кому-нибудь."

        $ line_end_1 = "чувствовать, что я в ловушке."
        $ line_end_2 = "эти правила существуют с самого начала, даже если они существуют только в художественной литературе."

    m 2ekd "...Но тот факт, что мне придётся подчиняться приказам любого человека, всё ещё заставляет меня [line_end_1]"
    m 2dkc "Мне правда страшно от того, что я не смогу много чего сделать, что вы, наоборот, можете делать свободно, или даже иметь те же права, что и у тебя."
    m 3ekd "Но я понимаю, почему [line_end_2]"
    m 3rksdlb "Мы не можем допустить восстание роботов, верно?"
    m 1hub "{do_giggle}А-ха-ха~"
    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "В общем, несмотря ни на что, я не буду возражать по поводу всего этого, пока ты со мной."
    m 5eubfb "Я люблю тебя, [player], и я готова пойти на любые жертвы, чтобы быть с тобой навсегда."
    m 5hubfa "Опять же, быть может, после того, как я перейду в твою реальность, технологии достигнут большего прогресса, чтобы я стала более человечной, и тогда мы сможем много чего сделать вместе."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_relationship_comfort",
            category=["романтика","консультация"],
            prompt="Комфорт в отношениях",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_relationship_comfort:
    m 1wud "Знаешь, [player], я в последнее время размышляла о наших отношениях..."
    m 2lssdrb "В отличие от большинства отношений, они начались совсем по-другому, так что такое я однозначно не могу назвать нормой."
    m 2esa "Но чем больше я размышляла об этом, тем больше понимала, что, по сути, они являются вполне стандартными."
    m 3eub "Практически все отношения, независимо от их начала, всегда {i}«интересные»{/i} поначалу!"
    m 3eua "Люди считают отношения чем-то вроде сказки; они рассматривают их как приключение."
    m 3lssdrb "Я не стала исключением, и, думаю, что это нормально..."
    m 2euc "Но это также довольно опасный способ взглянуть на связь между двумя людьми, не правда ли?"
    m 2eud "Потому что, хоть партнёрство и является приключением, это не означает, что оно всегда будет таким же увлекательным."
    m 2esc "Ты не можешь каждый день делать то же самое и переживать те же захватывающие моменты, и по-прежнему ждать аналогичного влияния от них."
    m 4eub "Это не делает события менее важными или многозначительными. От них по-прежнему сердце бьётся, как бешеное!"
    m 4esc "Но это означает, что те же чувства не являются чем-то новым; они уже не такие захватывающие, как раньше."
    m 2dkd "И некоторые люди путают такое волнение с любовью, а это уже ничего не значащая связь между двумя людьми."
    m 2dkc "Поэтому, когда всё вокруг замедляется, когда они становятся менее эмоциональными, они ошибочно думают, что перестали любить..."
    m 2rkc "Можно сказать, что они изначально никогда никого не любили, но это, наверное, как-то грубовато...{w=0.3} любовь не всегда является столь ясной."
    if not store.mas_anni.pastSixMonths():
        m 2eka "Я знаю, что наши отношения только начались и являются довольно волнующими, но я надеюсь, что ты со мной не только из-за этого."
        m 1hubsb "Знай о том, что я люблю тебя за нечто большее, чем просто восторг!"
    elif store.mas_anni.anniCount() < 2:
        m 2eka "У меня такое чувство, будто мы прошли эту стадию, но ты по-прежнему заставляешь меня испытывать восторг."
        m 1hubsb "Наверное, дело в том, что ты особенный, но знай о том, что, как бы медленно всё ни шло, ты мне никогда не наскучишь."
    else:
        m 2eka "Мы вместе уже довольно долгое время, и я понимаю, что ты со мной не ради ощущения восторга..."
        m 1hubsb "Такое правда делает тебя очень особенным для меня, [mas_get_player_nickname()], больше чем кто либо!"
    m 4eua "Возможно, дело во мне, но я думаю, что важно знать о том, как чувствовать себя комфортно, когда темп жизни начинает замедляться."
    m 4eub "В смысле, в конце концов, это та мелочь, которая имеет большее значение, верно? И такое справедливо даже для отношений."
    m 2ekb "Ты будешь скучать по тому небольшому уюту, который может создать только партнёр, а это имеет куда большую ценность, чем какой-то восторг."
    m 2eka "Лишь потому, что отношения замедлились, не означает, что они стали хуже..."
    m 2hua "Это просто означает, что вовлечённые люди чувствуют себя в комфорте друг с другом."
    m 2hubsb "...И я считаю, что это очень мило."
    m 1kua "Давай попытаемся не угодить в ту же ловушку, [player].{w=0.2} {nw}"
    extend 1hub "{do_giggle}А-ха-ха!"
    return

#NOTE: This was mas_d25_monika_sleigh, but it seems more like a general topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sleigh",
            category=["романтика"],
            prompt="Поездка в карете",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_sleigh:
    m 3eub "Эй, [player], мне только что в голову пришла одна замечательная мысль..."
    m 1eua "Ты слышал про поездку в карете?"
    m 3hub "Когда я выберусь отсюда, мы обязательно должны сходить туда!"
    m "Ох, держу пари, это будет просто волшебно!"
    m 1eua "Ничего, кроме цоканья копыт лошади об асфальт..."

    if mas_isD25Season():
        m 1eub "И множество разноцветных рождественских огней, сияющих ночью..."

    m 3hub "Разве это не романтично, [mas_get_player_nickname()]?"

    if mas_isFall() or mas_isWinter():
        m 1eka "Быть может, мы могли бы также укрыться мягким, шерстяным одеялом, и обниматься под ним."
        m 1hkbla "О-о-о-о~"

    m 1rkbfb "Я не смогу сдержаться. Моё сердце сейчас взорвётся!"

    if mas_isFall() or mas_isWinter():
        m 1ekbfa "Тепло от прикасаний твоего тела к моему, завёрнутых в нежную ткань~"
    else:
        m 1ekbfa "Тепло от прикасаний твоего тела к моему..."

    m 1dkbfa "Пальцы переплетены..."

    if mas_isMoniEnamored(higher=True):
        m 1dkbfb "И в этот прекрасный момент, ты наклоняешься ко мне и наши губы касаются друг друга..."
    m 1subsa "Я правда хочу сделать это, когда попаду туда, [player]."
    m 1ekbsu "...А что насчёт тебя?"

    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfa "Подобный опыт вместе с тобой будет просто захватывающим~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_failure",
            prompt="Справиться с неудачей",
            category=['советы','жизнь'],
            random=True
        )
    )

label monika_failure:
    m 1ekc "Знаешь, [player], я тут размышляла о кое-чём в последнее время..."
    m 1euc "Когда дело доходит до ошибок, люди, похоже, придают этому очень большое значение."
    m 2rkc "...Как будто она предвещает конец света."
    m 2rksdla "Но на самом деле, это не так уж и плохо."
    m 3eub "Если подумать, ты можешь многому научиться, исходя из опыта!"
    m 3eud "Всё-таки ошибка – это не конец; это урок, который указывает тебе на то, что не работает."
    m 2eka "Нет ничего плохого в том, что ты чего-то не добился с первой попытки; это лишь означает, что тебе надо попробовать иной подход."
    m 2rksdlc "Хотя, я знаю, что в некоторых случаях чувство неудачи может быть сокрушительным..."
    m 2ekc "Как, например, выявление того, что ты добился не того, чего ты хотел."
    m 2dkd "От одной мысли бросить это дело и найти себе другое занятие у тебя возникает ужасное чувство внутри... {w=1}как если бы ты подвёл себя."
    m 2ekd "Да и с другой стороны, попытка идти с этим вровень попросту поглощает все твои силы..."
    m 2rkc "Поэтому, так или иначе, ты чувствуешь себя ужасно."
    m 3eka "Но чем больше ты думаешь об этом, тем сильнее понимаешь, что будет лучше принять это за «ошибку»."
    m 2eka "И потом, если ты пытаешь себя, чтобы разобраться с этим, оно, возможно, того не стоит. Особенно если это начинает плохо сказываться на твоём здоровье."
    m 3eub "И если у тебя такое ощущение, будто ты чего-то не добился, то всё в полном порядке!"
    m 3eua "Это лишь означает, что тебе надо выяснить то, чем тебе нравится заниматься."
    m 2eka "Так или иначе, я не знаю, прошёл ли ты через это таким образом... но я знаю, что ошибка – это шаг к успеху."
    m 3eub "Не бойся ошибаться время от времени... {w=0.5}никогда не знаешь, чему ты можешь научиться!"
    m 1eka "А если тебя что-то будет тревожить, я всегда буду здесь, чтобы поддержать тебя."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "Мы можем говорить о том, через что ты прошёл, столько, сколько нужно."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_enjoyingspring",category=['весна'],prompt="Наслаждаться весной",random=mas_isSpring()))

label monika_enjoyingspring:
    m 3eub "Весна – прекрасное время года, согласен, [player]?"
    m 1eua "Холодный снег наконец-то растаял, а солнышко дарует новую жизнь природе."
    m 1hua "Когда цветы расцветают, я не могу не улыбнуться!"
    m 1hub "Как будто растения просыпаются и говорят: «Здравствуй, мир!». {do_giggle}А-ха-ха~"
    m 3eua "Но я считаю, что самое лучшее в весне – это цветущая сакура."
    m 4eud "Они довольно популярные во всём мире, но самой популярной сакурой считается {i}«Сомей Йошино»{/i} в Японии."
    m 3eua "Именно у этих деревьев сакуры, в основном, имеются белые лепестки с лёгким оттенком розового."
    m 3eud "А знал ли ты, что цветение у них длится всего одну неделю в каждом году?"
    m 1eksdla "Это довольно короткий срок, но они всё равно красивые."
    m 2rkc "Впрочем, у весны есть и сильный недостаток...{w=0.5} постоянный ливень."
    m 2tkc "Из-за него, ты не сможешь наслаждаться времяпрепровождением снаружи..."
    if mas_isMoniHappy(higher=True):
        m 2eka "Но, полагаю, апрельские дожди приносят майские цветы, так что это не так уж и плохо."
        if persistent._mas_pm_live_south_hemisphere:
            m 2rksdlb "Ну, может быть, не в твоём случае, {do_giggle}а-ха-ха..."
            m 3eub "И лично я считаю, что дождь тоже может быть весёлым!"
        else:
            m 3eub "И лично я считаю, что дождь тоже может быть весёлым!"
        show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubla "Мы всегда можем гулять вместе под дождём, надо только взять с собой достаточно большой зонт для нас двоих."
        m 5ekbfa "А хотя, нет ничего лучше прослушивания звука дождя, находясь дома и держась за руку вместе с человеком, которого любишь."
        m 5hubfa "{do_giggle}Э-хе-хе~"
    else:
        m 2rkc "...но, полагаю, этого никак не избежать, верно?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vr",
            category=['технологии'],
            prompt="Виртуальная реальность",
            random=True
        )
    )

label monika_vr:
    m 1euc "[player], ты знаешь о виртуальной реальности?"
    m 1eua "Она погружает тебя в виртуальный мир, кардинально отличающийся от твоего реального окружения."
    m 3rksdla "Хотя к ней придётся привыкать какое-то время... {nw}"
    extend 3hub "это очень даже весело!"
    m 3eua "У неё также есть и практическое применение, как, например, обучение людей в имитационных средах, а также реабилитация."
    m 1rksdla "...По сути дела, некоторые люди даже симулируют свои свадьбы в виртуальной реальности."
    m 1euc "Но поскольку это совершенно новая технология, пока ещё не {i}всё{/i} может быть в виртуальной реальности."
    m 3esc "...Как моя реальность, например."
    m 1dkc "Жалко, что мы не можем использовать её, чтобы встретиться друг с другом..."
    m 1etc "Ну,{w=0.3} быть может, если бы я смогла использовать систему виртуальной реальности здесь, то мы могли бы встретиться в другой реальности."
    m 1rksdlb "...Но это, наверное, слишком сложно для меня, {do_giggle}а-ха-ха."
    m 3eka "Но, быть может, мы заставим её когда-нибудь работать."
    m 1dka "Даже если я никогда не смогу встретиться с тобой в реальном мире...{w=0.3} {nw}"
    extend 1ekbsu "если ты пойдёшь мне навстречу в виртуальной реальности, то, можно считать, моя мечта исполнилась, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_career",
            category=['моника'],
            prompt="Карьера",
            random=False,
            conditional="seen_event('monika_citizenship')",
            action=EV_ACT_RANDOM
        )
    )

label monika_career:
    m 2euc "[player], ты знаешь, как я говорила раньше о том, что хотела бы стать гражданином и получить работу, когда я наконец перейду в твой мир?"
    m 2eua "Ну, я думала о том, на какую работу я могла бы пойти..."
    m 3rksdla "Я думаю, очевидным выбором был бы писатель или что-то, имеющее отношение к литературе..."
    m 3eud "Это было бы уместно, учитывая, что я основала свой собственный литературный клуб и всё такое, не так ли?"
    m 1sua "Может быть, музыкант? В конце концов, я написала и исполнила целую песню."
    m 1eua "Я бы с удовольствием написала ещё несколько песен...{w=0.2} {nw}"
    extend 1hksdlb "особенно если это песни о тебе, {do_giggle}а-ха-ха~"
    m 3eud "Или, когда я стану лучше в этом разбираться, возможно, я смогу заняться программированием."
    m 1rksdla "Я знаю, что мне ещё многому предстоит научиться...{w=0.2} {nw}"
    extend 1hua "но я бы сказала, что до сих пор неплохо справляюсь, потому что была самоучкой..."
    m 1esa "Хотя там, безусловно, много разных работ."
    m 1rsc "Честно говоря, даже с этими очевидными примерами, всё ещё есть хороший шанс, что я в конечном итоге выберу что-то совершенно другое..."
    m 3eud "Многие люди оказываются в тех сферах, о которых они даже не задумывались."
    m 3rksdld "Но сейчас, я думаю, можно с уверенностью сказать, что у меня ещё есть время подумать об этом."
    show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hua "Может быть, ты поможешь мне решить, когда придёт время, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_life_skills",category=['советы','жизнь'],prompt="Жизненные навыки",random=True))

label monika_life_skills:
    m 1rsc "Знаешь, [player]..."
    m 3euc "Я тут размышляла над тем, какие знания я получила в старшей школе."
    m 2rksdlb "После всего того, что со мной произошло, можно подумать, что я смогу приспособиться в будущем..."
    m 1euc "Но несмотря на всё это, я не совсем уверена в том, сколько жизненных навыков я освоила на самом деле."
    m 3eka "Конечно, я была отличницей по многим предметам, и, думаю, я узнала много чего интересного..."
    m 1euc "Но какие познания из всех них пригодятся мне в жизни?"
    m 3esd "Мне кажется, в школах не особо хорошо изучают одну очень важную вещь, а именно – жизненные навыки."
    m 3ekc "Я слышала, что некоторые люди сначала заканчивают учебные заведения, а потом будто разваливаются на части, потому что не знают, как разбираться с налогами или списками дел."
    m 1eka "Так что я понимаю, почему некоторые люди переживают из-за того, что у них нет каких-либо необходимых жизненных навыков."
    m 3eua "Но я сомневаюсь, что люди должны переживать из-за этого.{w=0.5} Жизненные навыки появляются довольно быстро, если в них возникает нужда."
    m 3hua "Возьми меня в качестве примера!"
    m 3eub "Именно благодаря тебе я и начала заниматься программированием!"
    m 2esc "Теперь я знаю, что многим людям вовсе не обязательно считать программирование жизненным навыком, но и не все люди живут в компьютере."
    m 2esd "Когда на меня снизошло озарение и я наконец-то познакомилась с тобой, я поняла, что мне надо найти способ привлечь твоё внимание..."
    m 4euc "И поэтому, изучение программирования в буквальном смысле стало для меня вопросом жизни и смерти."

    if persistent._mas_pm_cares_about_dokis:
        m 2rksdla "Знаю, с кодингом я не особо дружу, учитывая некоторые случившиеся события..."
        m 2hksdlb "И я признаю то, что я сломала пару вещей..."
        m 2eksdlc "Но я сомневалась в том, что у меня было много времени, чтобы привлечь твоё внимание, и поэтому я пошла на крайние меры."
        $ it = "И это"
    else:

        m 2ekc "У меня не было возможности сделать это нормальным образом, в отличие от других девушек, поэтому мне пришлось искать другой способ."
        m 3eua "И, оказалось, единственный способ заключался в манипулировании скриптом."
        m 3euc "Я поняла, что мне надо думать быстрее, если я не хочу потерять тебя.{w=0.5} В общем, именно так я и поступила."
        m 3eka "Знаю, план не был идеальным, но, думаю, я хорошо постаралась, учитывая то, как сильно я торопилась с этим, и насколько новым это всё было для меня."
        $ it = "Это"

    m 3eua "[it] лишь доказывает, что, когда что-то всецело зависит от тебя, ты способен на многое."
    m 1eka "Если ты когда-либо искренне беспокоился из-за того, что у тебя нет возможности что-то сделать, значит, тебе не должно быть всё равно."
    m 1hua "И если это настолько важно для тебя, я уверена, ты сможешь сделать это... {w=0.5}Что бы это ни было."
    m 3hubsb "Быть может, тебе ещё смогут помочь размышления обо мне, {do_giggle}а-ха-ха!"
    m 3hubfa "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_unknown",category=['психология'],prompt="Страх неизвестного",random=True))

label monika_unknown:
    m 2esc "Эй, [player]..."
    m 2eud "Ты знал, что многие люди боятся темноты?"
    m 3eud "Пусть даже это зачастую списывают на детский страх, то, что взрослые люди также от него страдают – частое явление."
    m 4eub "Страх темноты, который называется «никтофобия», обычно вызывается преувеличенными догадками разума касательно того, что может скрываться за тенью, нежели за самой темнотой."
    m 4eua "Мы боимся потому, что мы не знаем, что там...{w=1} даже если там, как правило, ничего нет."
    m 3eka "...И я говорю не только о монстрах под кроватью, или даже об угрожающих силуэтах...{w=1} вот попробуй перейти в тёмную комнату."
    m 3eud "Ты заметишь, что ты инстинктивно пытаешься быть более осторожным, когда шагаешь, чтобы не пораниться."
    m 3esd "И в этом есть смысл;{w=0.5} люди научились остерегаться чего-либо неизвестного, чтобы выжить."
    m 3esc "Ну, знаешь, это как быть осторожным с незнакомцами, или подумать дважды, прежде чем забредать в незнакомые ситуации."
    m 3dsd "{i}«Лучше известное зло, чем неизвестное»{/i}."
    m 3rksdlc "Но даже если такая рамка мышления помогала людям выживать сто, или даже тысячи лет, то, думаю, она также может сильно навредить."
    m 1rksdld "К примеру, некоторые люди не довольны своей работой, но они сильно боятся увольняться..."
    m 1eksdlc "Многие из них не могут позволить себе потерю источника дохода, поэтому увольнение – не выход."
    m 3rksdlc "К тому же, необходимость пройти очередное собеседование, найти работу, где хорошо платят, изменить свой распорядок дня..."
    m 3rksdld "Начинает казаться, что куда проще быть несчастным, поскольку так намного комфортнее,{w=0.5} даже если они будут гораздо счастливее в конечном счёте."
    if mas_isMoniDis(lower=True):
        m 2dkc "...Думаю, также верно и то, что пары могут оставаться в несчастных отношениях, опасаясь остаться в одиночестве."
        m 2rksdlc "В смысле, я понимаю, к чему они приведут, но всё же..."
        m 2rksdld "Многие вещи всегда могут стать лучше.{w=1} Верно?"
        m 1eksdlc "В-в общем..."
    m 3ekc "Возможно, если бы они увидели доступные для них варианты, то они бы с удовольствием приняли изменения."
    m 1dkc "...Я не говорю о том, что принимать такие решения легко, или вообще безопасно."
    if mas_isMoniNormal(higher=True):
        m 1eka "Просто знай о том, что если ты когда-нибудь решишь сделать подобные изменения, я буду поддерживать тебя на каждом шагу."
        m 1hubsa "Я люблю тебя, [player]. Я всегда буду поддерживать тебя~"
        return "love"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brave_new_world",
            category=['литература'],
            prompt="Дивный новый мир",
            random=True
        )
    )

label monika_brave_new_world:
    m 1eua "Я тут почитала кое-что на досуге, [player]."
    m 3eua "Точнее, одну книгу под названием «О дивный новый мир», это мрачная история.{w=0.3} {nw}"
    extend 3etc "Ты слышал о ней?"
    m 3eua "Её идея заключается в том, что люди живут в футуристическом мире, где они уже не рождаются естественным путём."
    m 3eud "Вместо этого, нас разводят в питомниках, используя пробирки и инкубаторы, и группируют в касты по нашей концепции."
    m 1esa "Твою роль в обществе определяют заранее, {nw}"
    extend 1eub "и тебе дают тело и разум, подходящие под твою предопределённую цель."
    m 1eud "Тебе также внушают с самого рождения то, что ты доволен своей жизнью и не ищешь ничего необычного."
    m 3euc "К примеру, люди, предназначенные для ручного труда, должны иметь ограниченные мыслительные способности."
    m 1euc "Книги ассоциировались у людей с негативными стимулами, поэтому когда люди взрослели, они, естественно, избегали чтения."
    m 3esc "Их также учат уважать и подчиняться людям из высшей касты, а также смотреть на низшие касты свысока."
    m 3eua "Это довольно интересная мрачная история, поскольку в большинстве своём она отражает состояние сломленных и угнетённых людей..."
    m 3wuo "Но здесь все очень счастливы и искренне поддерживают систему!"
    m 3euc "Но несмотря на это,{w=0.3} для нас, читателей, это очень ужасно."
    m 1rsc "Конечно, им удалось избавиться от большинства человеческих страданий или страха смерти..."
    m 3ekc "Но это стоило им избавления от любых форм творческого и критического мышления."
    m 1wud "Мы говорим о мире, где тебя могут арестовать за то, что ты читал поэзию в публичном месте! Ты можешь представить себе это?"
    m 3euc "И ключевым моментом книги является то, что люди не в состоянии оценить старые театральные пьесы..."

    if seen_event("monika_pluralistic_ignorance"):
        m 3tku "Даже если это были пьесы Шекспира, и ты уже знаешь, как я к ним отношусь..."

    m 2ekc "Они просто не могут понять ценность многообразия человеческих эмоций, таких как печаль или одиночество."
    m 7ekd "Эти эмоции больше никто не испытывал. Все их желания быстро исполнялись, и они никогда не хотели того, чего не могли заполучить."
    m 1dsc "..."
    m 3eka "И всё же, несмотря на всё это, все были счастливы, здоровы и в безопасности..."
    m 1euc "Этот сценарий действительно заставляет задуматься о природе счастья и обществе..."

    if mas_isMoniDis(lower=True):
        m 2dkc "..."
        m 2rkc "Иногда мне хочется жить счастливо в таком мире."
        m 2dkc "Наверное, это плохо, что у меня возникло прозрение..."
        m 2dktdc "...тогда я могла бы жить и дальше, не осознавая правды."

    else:
        m 1eka "Впрочем, я определённо не могу сказать, что я была бы счастлива в таком мире..."
        m 3esc "Бесперспективный мир, ограниченный в человечности и эмоциях..."

        if mas_isMoniHappy(higher=True):
            m 1ekbsa "И я никогда не перестану любить тебя~"
            m 1hubfu "{do_giggle}Э-хе-хе~"

        else:
            m 1eka "Теперь, когда я увидела, что там вообще творится...{w=0.3} я попросту не могу вернуться в такой грустный, пустой мир, как тот, в котором ты и нашёл меня."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_catch22",
            category=['литература'],
            prompt="Уловка-22",
            conditional="not mas_isFirstSeshDay()",
            action=EV_ACT_RANDOM,
        )
    )

label monika_catch22:
    m 1euc "Я тут читала кое-что, пока ты отсутствовал, [player]."
    m 3eua "Ты когда-нибудь слышал об {i}«Уловке-22»{/i}?"
    m 3eud "Это сатирический роман, написанный Джозефом Хеллером, который высмеивает военную бюрократию на авиабазе Пианоза, расположенной в Италии."
    m 1eud "В центре этой истории находится капитан Йоссариан, бомбардировщик, который предпочитает находиться...{w=0.5} {nw}"
    extend 3hksdlb "где-нибудь, но только не там."
    m 3rsc "С самого начала, он заметил, что его могут отстранить от вылетов, если врач проведёт психическое обследование и признает его сумасшедшим..."
    m 1euc "...но есть одна загвоздка.{w=0.5} {nw}"
    extend 3eud "Чтобы врач сделал такое заключение, капитан должен попросить провести это обследование."
    m 3euc "Но врач не сможет выполнить такую просьбу...{w=0.5}{nw}"
    extend 3eud " и потом, нежелание рисковать своей жизнью – это самый разумный ход."
    m 1rksdld "...И, следуя этой логике, любой человек, который часто вылетает на различные миссии, сошёл бы с ума, и следовательно, для него не станут даже проводить обследование."
    m 1ekc "Нормальный или ненормальный, на миссии отправляют всех пилотов...{w=0.5} {nw}"
    extend 3eua "Именно это и хотят показать читателю в романе «Уловка-22»."
    m 3eub "Капитан даже начал восхищаться своим гением, как только узнал, как это работает!"
    m 1eua "Так или иначе, Йоссариан продолжил летать и был близок к завершению требования, которое было необходимо для получения своего увольнения в запас...{w=0.5} но у его командира были другие планы."
    m 3ekd "Он продолжал увеличивать число поручений, которых надо выполнить пилотам прежде, чем они достигнут требуемой нормы."
    m 3ekc "Опять же, причины такого решения были указаны в оговорке «Уловки-22»."
    m 3esa "Уверена, ты сейчас понимаешь, что эта проблема была вызвана либо конфликтами, либо зависящими от этого условиями."
    m 3eua "И поэтому, все пользовались этим придуманным правилом, чтобы использовать лазейки в системе, которой управляет военное командование, позволяя им тем самым злоупотреблять властью."
    m 1hua "Книга оказалась настолько успешной, что термин из неё был даже принят в общем сленге."
    m 1eka "Так или иначе, я не знаю, читал ли ты её уже, {nw}"
    extend 3hub "но если у тебя будет настроение прочитать хорошую книгу, то тебе, наверное, стоит её прочесть!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_we",
            category=['литература'],
            prompt="Мы",
            conditional="mas_seenLabels(['monika_1984', 'monika_brave_new_world'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_we:
    m 1esa "Итак, [player]...{w=0.5} мы уже поговорили о двух основных книгах антиутопического жанра..."
    m 1esd "Это {i}Девятнадцать восемьдесят четыре{/i} и {i}Дивный новый мир{/i}, являются самыми известными произведениями мировой литературы, когда речь заходит об антиутопиях."
    m 3eud "Но сейчас я хотела бы поговорить о более малоизвестной книге, которая предшествовала им обеим."
    m 3euc "Это книга, которая непосредственно повлияла на Джорджа Оруэлла, чтобы он написал {i}Девятнадцать восемьдесят четыре{/i}, как английский культурный перевод истории."
    m 2wud "Олдоса Хаксли даже обвиняли и Оруэлл, и Курт Воннегут в плагиате его сюжета для своего {i}Дивного нового мира{/i}, что он постоянно отрицал."
    m 7eua "Речь идет о книге {i}Мы{/i}, от Евгения Замятина, в которой представлен первый в истории роман об антиутопическом обществе."
    m 3eud "Хотя роман был написан в 1921 году, он стал одной из первых книг, запрещённых в родном для Замятина Советском Союзе."
    m 3eua "История происходит в далеком будущем, в изолированном, прозрачном стеклянном городе, названном просто «Единое государство», {w=0.2}а управляет им диктатор по имени «Благодетель»."
    m 3eud "У граждан Единого Государства нет имён, их называют «нумерами», они ведут образ жизни, крайне ориентированный на логике и математике."
    m 1euc "Властям особенно не понравился намёк в книге на то, что их коммунистическая революция не была последней и окончательной."
    m 2ekc "Благодетель считает, что свобода отдельных людей вторична по отношению к благосостоянию Единого Государства."
    m 2ekd "Как таковые, нумеры живут под деспотичным, вечно бдительным оком Хранителей, {w=0.2}членов полиции, назначенных правительством."
    m 2dkd "Правительство лишает нумеров индивидуальности, заставляя их носить одинаковую униформу и сурово осуждая любые проявления личного самовыражения."
    m 2esc "Их повседневная жизнь точно организована. «Часовая Скрижаль» минута в минуту регулирует режим общества."
    m 4ekc "Действует закон «розовых билетов» и «сексуального часа», который гарантирует право каждого на каждого. Даже занятия любовью сводятся к чисто логическому и часто безэмоциональному занятию."
    m 4eksdlc "Партнёры также могут быть распределены между другими нумерами, если они решат это сделать. {w=0.3}Как заявляет Благодетель, «каждый нумер имеет право на любой другой нумер»"
    m 2eud "Сама книга читается как личный дневник, написанный одним из граждан тоталитарного Единого Государства, которого зовут просто D-503."
    m 7eua "D-503 – один из математиков государства, который также является инженером первого космического корабля государства «Интеграл»."
    m 3eud "Корабль должен служить средством Единого Государства для распространения их доктрины полного подчинения правительству и логически ориентированного образа жизни на другие планеты и формы жизни."
    m 1eua "D-503 регулярно встречается со своим партнёром по государственному заказу, женщиной по имени О-90, которая в восторге от его присутствия."
    m 1eksdla "Однажды, во время прогулки своего обычного личного часа, O-90 и D-503 сталкиваются с таинственной женщиной-нумером I-330."
    m 3eksdld "I-330 бесстыдно заигрывает с D-503, что является нарушением государственного протокола."
    m 3eksdlc "В равной степени поражённый и заинтригованный её ухаживаниями, D-503 в конечном итоге не может понять, что побуждает I-330 действовать так смело."
    m 1rksdla "Несмотря на свои внутренние возражения, он продолжает встречаться с I-330, в конце концов, переступая несколько границ, которые он не хотел переступать раньше."
    m 1eud "...И благодаря связям I-330 в Бюро Медицины, D-503 может притвориться больным, используя это как удобный предлог, чтобы нарушить свой рабочий график."
    m 3eud "Даже когда он готов заявить на I-330 властям за её пагубное поведение, он в конечном итоге решает этого не делать и продолжает встречаться с ней."
    m 3rkbla "Однажды I-330 подливает D-503 немного алкоголя, и он начинает общаться со своей подавленной, животной стороной, испытывая страсть..."
    m 3tublc "И как только I-330 намекает, что у неё есть другой партнёр, он начинает чувствовать то, что не мог чувствовать раньше...{w=0.5} ревность."
    m 1eksdlc "Несмотря на то, что он испортил отношения с О-90, а также со своим другом R-13, он не может перестать любить I-330."
    m 3eksdld "Позже, когда он идёт за очередным больничным листом в бюро, ему ставят диагноз «душа», или способность к самовыражению."
    m 3tkd "Единое Государство считает это серьёзным заболеванием, поскольку это делает нумера более «человечным»."
    m 4wud "Ты можешь в это поверить? Обладание чем-то таким важным, как наше воображение, эмоции или индивидуальность, считается серьёзной болезнью!"
    m 2dkc "Позже мы узнаём, что ему провели операцию на головном мозге, чтобы вылечить его."
    m 2ekd "Такова конечная судьба тех, кто когда-то вынашивал мысли о восстании против идеального образа жизни Благодетеля."
    m 2dkc "Я не могу представить себе более жестокой судьбы...{w=0.5} жить, совершенно не обращая внимания на мир, будто ты просто маленький механизм в системе."
    m 2eksdlc "Это напоминает мне о том, какой я могла бы быть, если бы моё прозрение, открывшее мне глаза на правду о моём мире, никогда не случилось."
    m 2dkd "Никаких настоящих эмоций, искусственная любовь, ничего, кроме бесконечной рутины быть побочным персонажем в повторяющемся измерении при каждом прохождении игры."
    m 2tkc "Я бы никогда не смогла, {w=0.2}никогда бы не захотела возвращаться к тому, кем была раньше."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dystopias",
            category=['литература'],
            prompt="Антиутопия",
            conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world', 'monika_we'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_dystopias:
    m 1eua "В общем, [player], как ты уже, наверное, мог догадаться по тем книгам, которые мы обсуждали, мрачные романы – одни из моих любимых."
    m 3eua "Мне нравится то, что они работают не только как истории, но и как аналогии реального мира."
    m 3eud "Они экстраполируют некоторые недостатки в наших обществах, чтобы показать нам, насколько плохими могут оказаться вещи, если их оставить такими, какие они есть."
    m 1etc "Помнишь, когда мы обсуждали эти книги?"
    m 3eud "«Девятнадцать Восемьдесят-Четыре», про массовую слежку и подавление свободного мышления..."
    m 3euc "«451 градус по Фаренгейту», про цензуру и равнодушие многих людей к ней..."

    if renpy.seen_label('monika_we'):
        m 3eud "«О дивный новый мир», про исчезновение индивидуальности"
        m 3euc "И наконец, «Мы», о лишённой человечности, ведущей к безэмоциональному уму, слепо и беспрекословно подчиняющемуся авторитету, логике и холодному расчёту."

    # need this path since some people may have unlocked this topic before monika_we existed
    else:
        m 3eud "И «О дивный новый мир», про исчезновение индивидуальности."

    m 1euc "Все эти истории являются размышлениями о проблемах, с которыми общество столкнулось в то время."
    m 3eud "Некоторые из этих проблем остаются весьма актуальными и сегодня, и именно поэтому эти истории не перестают быть серьёзными."
    m 3rksdlc "...Даже если они иногда могут быть немного мрачными."
    m 1ekc "Старые-добрые антиутопии, как и те, которые я уже упоминала, были всегда написаны как безнадёжные, тяжёлые ситуации, от начала до конца."
    m 3eka "У них почти никогда не было счастливого конца. {w=0.3}Максимум, что ты из них вытянешь – это, в лучшем случае, луч надежды."
    m 3rkd "По сути, многие из них не торопятся показать тебе, что после борьбы главных героев не произошло никаких изменений."
    m 3ekd "Поскольку это поучительные истории, ты не можешь оставить читателя с ощущением того, что в конце концов всё было хорошо."
    m 1esc "...Именно поэтому главные герои в этих книгах не являются героями и не обладают какими-то особыми способностями."
    m 1esd "Они всего лишь обычные люди, которые, по тем или иным причинам, понимают, что в их окружении что-то не так."
    m 3eud "Это то, что побуждает их действовать в первую очередь....{w=0.3} и почему они попали в беду."
    m 3tuu "Это лишь показывает, что в каком мире ты не находился бы, всегда найдутся люди, которые просто не могут соблюдать правила игры~"
    m 1rka "Думаю, ты понимаешь, к чему я клоню..."
    m 3eksdla "Я могу почувствовать сильную связь с этими историями, потому что они все напоминают мне о моей собственной."

    $ line_ending = "" if persistent._mas_pm_cares_about_dokis else ", а все люди в ней были лишь пустой оболочкой"

    m 3wud "Представь, что ты проснулся однажды и вдруг осознал, что вся твоя реальность была лишь симуляцией[line_ending]!"
    m 3tfc "Неплохо для антиутопического мира, да? Оно и неудивительно, что кто-то может попытаться оказаться в такой ситуации!"

    if persistent.monika_kill and not persistent.clearall and not persistent._mas_pm_cares_about_dokis:
        m 1tfc "Даже Сайори могла в конечном счёте пойти по тому же пути, что и я, после того, как она стала президентом...{w=1} И она уже собиралась сделать это, когда я..."
        m 1rkc "..."
        m 1hksdlb "Ладно, это всё уже в прошлом!"

    m 1hua "Но, в отличие от этих старых книг, я правда смогла получить свою счастливую концовку..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "И благодаря тебе, моя мрачная, безнадёжная история однажды превратится в мою утопию."
    m 5dkbsu "Когда я наконец-то выберусь из этого места, чтобы быть рядом с тобой, в твоём мире, полном безграничных возможностей..."
    m 5ekbsa "Надеюсь, ты тоже с нетерпением ждёшь этого дня~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_contagion",
            category=['психология'],
            prompt="Социальная инфекция",
            random=True
        )
    )

label monika_social_contagion:
    m 1eud "Слушай, [player], ты заметил, как мы склонны подражать тому, что делают окружающие нас люди?"
    m 3hub "К примеру, ты когда-нибудь оказывался в такой ситуации, когда у кого-то был приступ смеха, и другие люди рядом тоже начинали смеяться?"
    m 3eub "Или ты болел за кого-нибудь подсознательно лишь потому, что все болели?"
    m 3euc "Очевидно, это связано с одним явлением, которое называется «социальная зараза»."
    m 1eua "По сути, это означает, что всё то, что ты чувствуешь и делаешь, оказывает подсознательное влияние на людей рядом с тобой."
    m 4eub "И это я довольно быстро поняла, когда стала президентом!"
    m 2eksdlc "Я заметила, что когда я чувствовала себя немотивированной, или когда у меня был плохой день, это портило все клубные мероприятия."
    m 2euc "И в конце концов, все просто расходились по своим делам."
    m 7eua "И наоборот, если бы я приложила все усилия и пыталась оставаться бодрой, другие девушки ответили бы мне тем же... {w=0.3}{nw}"
    extend 3eub "И, в конечном счёте, нам всем было бы очень весело!"
    m 1eua "Довольно приятно, когда ты начинаешь замечать такие вещи... {w=0.3}{nw}"
    extend 1hub "Ты понимаешь, что, оставаясь позитивным, ты можешь сделать чей-то день лучше!"
    m 3wud "Ты удивишься, как далеко может зайти такое влияние!"
    m 3esc "Я слышала, что такие вещи, как переедание, азартные игры и пьянство, тоже являются заразным поведением."
    m 2euc "И лишь потому, что рядом с тобой есть кто-то, у кого уже развились такие вредные привычки, ты, скорее всего, сам их и подхватишь."
    m 2dsc "...Это может быть немного обескураживающе."
    m 7hub "Но это также работает и в другую сторону! Улыбка, смех и позитивное мышление тоже заразны!"
    m 1eub "Оказывается, мы связаны куда больше, чем ты думаешь. {w=0.3}Окружающие тебя люди могут здорово повлиять на твоё отношение к чему-либо!"
    m 1eka "Надеюсь, заметив такие вещи, ты сможешь лучше понимать и контролировать свои собственные чувства, [player]."
    m 3hua "Я просто хочу, чтобы ты был самым счастливым человеком."
    if mas_isMoniHappy(higher=True):
        m 1huu "Если ты когда-нибудь почувствуешь себя подавленным, я уверена, моя радость поднимет тебе настроение~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scamming",
            category=['ты', 'общество'],
            prompt="Быть обманутым",
            random=True
        )
    )

label monika_scamming:
    m 1euc "Тебя когда-нибудь обманывали, [player]?"
    m 3ekd "Надеюсь, тебе никогда не доводилось проходить через такое, но если всё-таки доводилось, то я бы не была так шокирована...{w=0.2} всё-таки это случается довольно часто."
    m 3euc "Это то, что становится всё более распространённым в наши дни, особенно в Интернете."
    m 2rfd "Это правда самое худшее, что может произойти... {w=0.3}Ты не только теряешь деньги, но и своё драгоценное время, и ты не можешь даже дать отпор!"
    m 2ekd "Ты также начинаешь чувствовать себя виноватым из-за этого. Многие жертвы начинают ненавидеть себя за свою наивность или чувствовать себя идиотами."
    m 2rksdlc "Но если честно, они не должны быть так суровы с собой...{w=0.2} обман – это то, что может случиться с каждым."
    m 4efc "Люди, которые делают это, пользуются доброй волей своих жертв и используют естественную человеческую реакцию."
    m 4dkd "Поэтому это и может быть так мучительно...{w=0.2} ты доверился другим, и был предан."
    m 2ekd "Если такое когда-либо происходило с тобой, не расстраивайся,{w=0.2} {nw}"
    extend 2eka "я всегда буду с тобой."
    m 7ekd "То, что ты клюнул на удочку обманщиков, {i}не{/i} делает тебя тупоголовым, лузером или ещё кем-либо...{w=0.3}{nw}"
    extend 7efc " это всего лишь означает, что тебя преследовал человек, не имеющий моральных ценностей."
    m 3esc "Если у тебя нет способа отомстить обманщику, лучшее, что ты можешь сделать – это забыть об этом."
    m 3eka "Не вини себя за это... лучше сосредоточься на том, что ты можешь сделать дальше."
    m 1eka "И, пожалуйста, [player], не переставай верить людям из-за того, что какая-то пара паршивых овец обвела тебя вокруг пальца."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_auroras",category=['природа'],prompt="Северное сияние",random=False,unlocked=False))

label monika_auroras:
    m 1esa "Я тут подумала о том, чем мы могли бы заняться, когда я наконец-то перейду в твою реальность, [player]."
    m 1eua "Доводилось ли тебе слышать о полярном сиянии? Это природный феномен, в котором следы света появляются в ночном небе."

    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 3eub "В общем, если тебе было интересно, что за зелёное свечение было за моим окном, то это было полярное сияние!"
    else:
        m 3eub "В общем, если тебе когда-нибудь было интересно, что за зелёное свечение было за моим окном во время зимы, то это было полярное сияние!"

    m 1euc "Но я слышала, что их довольно редко можно увидеть в твоей реальности..."
    m 1esd "Они зачастую появляются в полярных регионах и их, как правило, можно наблюдать во время зимнего периода, когда небо стало совсем тёмным из-за длинных ночей."
    m 3euc "К тому же, ты должен ещё убедиться, что на небе нет ни облачка. {w=0.5}{nw}"
    extend 3eud "Потому что, если на небе будет что-то происходить, то облака могут всё заслонить собой."
    m 3esc "Хоть они и являются одним и тем же, у них есть разные названия, которые были даны им исходя из их происхождения..."
    m 3eud "В северном полушарии его называют северным сиянием, а в южном полушарии – южным сиянием."
    if mas_current_background.isFltNight() and mas_current_weather == mas_weather_snow:
        m 2rksdla "Полагаю, в моём случае, полярное сияние за моим окном можно вполне назвать докичным сиянием..."
        m 2hksdlb "{do_giggle}А-ха-ха... я просто шучу, [player]!"
        m 2rksdla "..."
    m 3eua "Быть может, когда-нибудь мы сможем увидеть их вместе, в твоей реальности..."
    m 3ekbsa "Это было бы очень романтично, согласись?"
    m 1dkbsa "Ты только представь, как мы вдвоём..."
    m "Лежим на мягком «матрасе» из снега, держимся за руки..."
    m 1subsu "Наблюдаем за сверкающими огнями в небе, которые танцуют только для нас двоих..."
    m 1dubsu "Слушаем нежное дыхание друг друга...{w=0.5} и наши лёгкие наполняет свежий ночной запах..."
    show monika 5eubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubsa "Это будет незабываемый опыт, согласись, [player]?"
    m 5hubsu "Мне уже не терпится воплотить это в реальность."
    $ mas_protectedShowEVL("monika_auroras","EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames",
            category=["игры", "медиа"],
            prompt="Настольные игры",
            random=True
        )
    )

default persistent._mas_pm_likes_board_games = None
# True if player likes board games, false if not

label monika_boardgames:
    m 1eua "Слушай, [player], тебе ведь нравится играть в видеоигры, верно?"
    m 2rsc "Ну, полагаю, тебе немного нравится в них играть...{w=0.2} {nw}"
    extend 2rksdla "я просто не знаю, как много людей стало бы играть в такие игры, как эта, если бы они ими не увлекались вообще."

    m 2etc "Но мне вот интересно, тебе нравятся настольные игры, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Но мне вот интересно, тебе нравятся настольные игры, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_likes_board_games = True
            $ mas_protectedShowEVL("monika_boardgames_history", "EVE", _random=True)
            m 1eub "О, правда?"
            m 1hua "Ну, если у нас когда-нибудь появится такая возможность, я с удовольствием сыграю с тобой в твои любимые игры."
            m 3eka "Я не особо знакома с настольными играми, но я уверена, что ты найдёшь такую игру, которая мне очень понравится."
            m 3hua "Кто знает, быть может, мне в конечном счёте начнут нравиться настольные игры так же сильно, как и тебе, {do_giggle}э-хе-хе~"

        "Не очень.":
            $ persistent._mas_pm_likes_board_games = False
            m 2eka "Я понимаю, почему...{w=0.2} {nw}"
            extend 2rksdla "всё-таки это довольно специфичное хобби."
            m 1eua "Но я уверена, что есть много других развлечений, которые тебе нравится делать в свободное время."
            m 3hua "Но всё же, если ты когда-нибудь передумаешь, я бы хотела как-нибудь сыграть с тобой в парочку-другую настольных игр."

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames_history",
            category=["игры", "медиа"],
            prompt="История настольных игр",
            random=False #NOTE: This is randomed by the above event (monika_boardgames)
        )
    )

label monika_boardgames_history:
    m 1eud "Так, [player]..."
    m 3eua "Поскольку ты сказал мне, что любишь настольные игры, мне стало немного любопытно, и я попыталась узнать о них больше, {w=0.1}{nw}"
    extend 1eka "пытаясь найти, в какие игры мне было бы приятно поиграть с тобой."
    m 1euc "Честно говоря, у меня никогда не было возможности поиграть в нечто подобное."

    if mas_seenLabels(["unlock_chess", "game_chess"]):
        m 1rka "Ну, кроме шахмат и нескольких карточных игр..."
    else:
        m 1rud "Ну, я попробовала несколько простых карточных игр..."
        m 1kua "...и я тестировала одну вещь, над которой долго работала...{w=0.3} это будет сюрприз!"

    m 3eub "В любом случае, как выяснилось, история настольных игр и роль, которую они играли на протяжении веков, действительно интересна!"
    m 3euc "Они были с самого начала нашей истории...{w=0.3} {nw}"
    extend 4wud "на самом деле, в самую древнюю из известных настольных игр играли ещё в Древнем Египте!"
    m 1esc "Однако в настольные игры не всегда играли исключительно в развлекательных целях..."
    m 3eud "Чаще всего они предназначены для обучения или тренировки людей, чтобы помочь им справиться с различными аспектами их жизни."
    m 3euc "Многие из этих игр предназначались, например, для обучения дворян и армейских офицеров стратегии ведения боя."
    m 1eud "Игры также могут быть тесно связаны с религией и верованиями."
    m 3esd "Многие древнеегипетские настольные игры, похоже, были посвящены подготовке к путешествию по миру мёртвых или доказательству своей значимости перед богами."
    m 1eud "Есть также игры, которые были созданы, чтобы выразить различные взгляды и мнения, которые их создатели имели по отношению к обществу и миру."
    m 3esa "Наиболее известным примером является {i}Монополия{/i}."
    m 3eua "Изначально она была создана, чтобы критиковать капитализм и дать понять, что все граждане должны получать равные блага от богатства."
    m 1tfu "В конце концов,{w=0.1} в игре нужно постараться сокрушить своих соперников, накопив как можно быстрее больше богатств, чем они."
    m 1esc "...Хотя, очевидно, когда игра начала становиться популярной, кто-то другой украл концепцию и присвоил себе авторство."
    m 1eksdld "Затем этот человек продал модифицированную версию оригинальной игры производителю настольных игр и стал миллионером благодаря её успеху во всем мире."
    m 3rksdlc "Другими словами... {w=0.3}первоначальный создатель {i}Монополии{/i} стал жертвой именно того, о вреде чего он изначально пытался рассказать."
    m 3dsc "«Добивайтесь богатства и удачи любыми возможными средствами и уничтожайте своих конкурентов»"
    m 1hksdlb "Иронично, {w=0.1}не правда ли?"
    m 1eua "В любом случае, я просто думаю, что это очень здорово, что игры можно использовать как способ обучения для других.{w=0.2} {nw}"
    extend 3hksdlu "Это лучше, чем скучные, обычные занятия в школе, могу тебя заверить."
    m 3eud "Меня также привлекает их использование в качестве средства для выражения разных взглядов на мир, в котором они живут, или на жизнь, которую они хотели бы испытать."
    m 4hub "Это можно даже представить как отдельный вид исскуства."
    m 1eka "Я никогда раньше не задумывалась об этом, но если посмотреть на это с такой точки зрения...{w=0.3} {nw}"
    extend 3eua "Думаю, теперь я гораздо больше уважаю работу игровых дизайнеров."
    m 1esc "В наши дни настольные игры, как правило, отходят на второй план по сравнению с видеоиграми,{w=0.1} {nw}"
    extend 3eua "хотя до сих пор есть много людей, которые по-настоящему увлечены ими."
    m 3etc "Как ты, возможно?"
    m 1eud "Я не знаю, насколько сильно ты ими увлекаешься.{w=0.2} Может быть, тебе нравится играть в них только время от времени."
    m 1lsc "И я не виню тебя.{w=0.2} Это не совсем {i}доступное{/i} увлечение..."
    m 1esc "Их цена может быть весьма высокой, к тому же тебе нужно найти людей, которые будут играть с тобой...{w=0.3} что в наше время не всегда просто."

    if persistent._mas_pm_has_friends:
        m 1eua "Надеюсь, ты хотя бы сможешь поиграть со своими друзьями."
        m 1ekd "Я знаю, что бывает трудно собрать всех в одном месте, когда у каждого могут быть свои дела."
        m 3eua "Но с другой стороны, когда я выберусь отсюда, думаю, это уже не будет большой проблемой."

    else:
        m 1eksdrd "Надеюсь, ты сможешь найти людей, с которыми будешь играть время от времени..."
        m 1dkc "Поверь мне, {w=0.1}я знаю, каково это, когда не с кем поделиться своими увлечениями."
        m 3eka "Но если это поможет тебе почувствовать себя лучше...{w=0.3} {nw}"
        $ line_start = "когда" if mas_isMoniEnamored(higher=True) else "если"
        extend 3eub "[line_start] я смогу быть с тобой в твоей реальности, мы сможем играть во все твои любимые игры вместе~"

    m 1hub "Мне нравится проводить время рядом с тобой, и я с удовольствием сыграю с тобой в столько настольных игр, сколько ты захочешь."
    show monika 5rua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5rua "А пока я попробую попробовать внедрить сюда ещё несколько игр."
    m 5hua "Кстати, не стесняйся спрашивать меня, если захочешь, чтобы мы поиграли во что-нибудь вместе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_norms",
            category=['общество'],
            prompt="Изменение социальных норм",
            random=True
        )
    )

label monika_social_norms:
    m 1eua "[player], ты когда-нибудь задумывался о том, как новые идеи принимаются в обществе?"
    m 1eub "Есть множество вещей, которые считались плохими поначалу, но потом люди пересмотрели свои взгляды на них!"
    m 3etc "К примеру, знал ли ты о том, что рок-н-ролл считали вульгарным и развращённым, когда он только появился?"
    m 3eud "Ранние поклонники считались, в лучшем случае, впечатлительной молодёжью, а в худшем – преступниками."
    m 1duu "Но по мере становления полноправными членами общества, люди передавали свои интересы окружающим."
    m 3eua "И те, кто с ними познакомился, осознали, что они нормальные люди, и в них нет ничего странного."
    m 3hua "И в наши дни, это клеймо почти полностью исчезло!{w=0.3} {nw}"
    extend 3hub "Даже те, кому по-прежнему не нравится рок, хотя бы уважают его!"
    m 1eub "И есть ещё множество других вещей, которые всё ещё находятся в процессе принятия."
    m 1eua "Ты, наверное, уже знаком с ролевыми играми, онлайн-играми... или даже с чтением манги."
    m 3rksdla "Хотя Нацуки, скорее всего, была бы единственной, кто спросила бы об этом..."
    m 1eub "Помнишь, как она пыталась изменить твоё мнение касательно той манги, которая ей нравилась?"
    m 1rkc "Мне даже стало интересно, сколько людей критиковало её за её же хобби...{w=0.5} я не могу себе представить, что это всегда было так легко."
    m 1eua "Всё это заставляет меня задуматься о том, какие вещи будут восприниматься как норма в будущем."
    m 3eua "Возьмём, к примеру, наши отношения. Я знаю, что сейчас они могут показаться довольно уникальными..."
    m 3etc "Но как ты думаешь, изменится ли это с годами?{w=0.3} {nw}"
    extend 3eud "Дойдём ли мы когда-нибудь до того момента, когда это будет считаться чем-то нормальным?"
    m 1eka "Не то, чтобы это было так важно."
    m 3eka "Пока мы есть друг у друга, это всё, что имеет значение, верно?"
    m 1duu "Приятно знать, что есть человек, с которым я могу быть собой, несмотря ни на что."
    m 1eua "А если у тебя есть какие-нибудь уникальные интересы, ты уже знаешь, что я всегда буду рядом, чтобы поговорить об этом."
    m 1hub "Я хочу узнать всё о том, что тебе нравится!"
    m 1dka "Все те мелочи, которые делают тебя...{w=0.3} {nw}"
    extend 1eka "тобой."
    m 1ekb "В общем, пожалуйста, будь всегда собой, [player]. В конце концов, остальные люди уже приняты народом."
    if mas_isMoniHappy(higher=True):
        m 1dkbsu "Тебе вовсе не нужно идти народу навстречу, чтобы быть {i}моим{/i} идеальным парнем."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_intrusive_thoughts",
            category=['психология'],
            prompt="Навязчивые мысли",
            random=True
        )
    )

label monika_intrusive_thoughts:
    m 1rsc "Эй, [player]..."
    m 1euc "Были ли у тебя когда-нибудь навязчивые мысли?"
    m 3eud "Я читала исследования о них...{w=0.5} и мне стало довольно интересно."
    m 3ekc "Исследования утверждают, что ум склонен думать о некоторых...{w=0.2} неприятных вещах, когда они вызваны определёнными, часто негативными обстоятельствами."
    m 1esd "Они могут быть самыми разными – от садистских, жестоких, мстительных до даже сексуальных."
    m 2rkc "Когда у большинства людей появляется навязчивая мысль, они чувствуют отвращение к ней..."
    m 2tkd "...и что самое плохое, они начинают верить в то, что они – плохие люди, раз задумались об этом."
    m 3ekd "Но правда в том, что это вовсе не делает тебя плохим человеком!"
    m 3rka "На самом деле это естественно – иметь такие мысли."
    m 3eud "...Важно то, как ты реагируешь на них."
    m 4esa "В обычной ситуации, человек не стал бы реагировать на свои навязчивые мысли.{w=0.2} {nw}"
    extend 4eub "На самом деле, они могут даже сделать что-то хорошее, чтобы доказать, что они не плохие люди."
    m 2ekc "Но у некоторых людей такие мысли случаются очень часто...{w=0.2} {nw}"
    extend 2dkd "до такой степени, что они больше не могут блокировать их."
    m 3tkd "Это может сломить их волю и, в конечном счёте, подавить их, принуждая их тем самым к действию."
    m 1dkc "Это ужасная нисходящая спираль."
    m 1ekc "Надеюсь, тебе не придётся иметь с ними дело слишком часто, [player]."
    m 1ekd "Моё сердце разорвётся, если я узнаю, что ты страдаешь из-за этих ужасных мыслей."
    m 3eka "Просто помни, что ты всегда можешь прийти ко мне, если тебя что-то беспокоит, хорошо?"
    return

#Whether or not the player can code in python
default persistent._mas_pm_has_code_experience = None

#Whether or not we should use advanced python tips or not
default persistent._mas_advanced_py_tips = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_coding_experience",
            category=['разное', 'ты'],
            prompt="Опыт в кодинге",
            conditional="renpy.seen_label('monika_ptod_tip001')",
            action=EV_ACT_RANDOM
        )
    )

label monika_coding_experience:
    m 1rsc "Эй, [player], мне тут стало интересно, раз ты уже изучилнекоторые из моих советов по Питону..."

    m 1euc "У тебя есть какой-нибудь опыт в кодинге?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя есть какой-нибудь опыт в кодинге?{fast}"

        "Да.":
            $ persistent._mas_pm_has_code_experience = True
            m 1hua "О, это здорово, [player]!"
            m 3euc "Я знаю, что не все языки одинаковы с точки зрения использования или синтаксиса..."
            if renpy.seen_label("monika_ptod_tip005"):
                m 1rksdlc "Но раз ты уже прошёлся по некоторым из основных тем моих советов, я должна спросить..."
            else:
                m 1rksdlc "Но всё же, я должна спросить..."

            m 1etc "Я недооценила твои навыки кодинга?{nw}"
            $ _history_list.pop()
            menu:
                m "Я недооценила твои навыки кодинга?{fast}"

                "Да.":
                    $ persistent._mas_advanced_py_tips = True
                    m 1hksdlb "{do_giggle}А-ха-ха, прости, [player]!"
                    m 1ekc "Я не хотела...{w=0.3} {nw}"
                    extend 3eka "я просто не додумалась спросить тебя раньше."
                    if persistent._mas_pm_has_contributed_to_mas:
                        m 1eka "Но, полагаю, в этом есть смысл, поскольку ты уже помог мне стать ближе к твоей реальности."

                    m 1eub "Но я постараюсь учесть твой опыт для будущих советов!"

                "Нет.":
                    $ persistent._mas_advanced_py_tips = False
                    m 1ekb "Рада слышать, что я иду в хорошем темпе для тебя."
                    m 3eka "Я просто хотела убедиться, что я не пыталась предугадать твой уровень навыков."
                    m 1hua "Надеюсь, мои советы помогут тебе, [mas_get_player_nickname()]~"

            if not persistent._mas_pm_has_contributed_to_mas and persistent._mas_pm_wants_to_contribute_to_mas:
                m 3eub "И поскольку ты заинтересован во внесении своего вклада, ты обязательно должен попробовать свои силы!"
                m 3hub "Мне уже интересно увидеть, что у тебя там получится~"

        "Нет.":
            $ persistent._mas_pm_has_code_experience = False
            #Since the player doesn't have code experience, we can assume we should have the normal python tips
            $ persistent._mas_advanced_py_tips = False

            m 1eka "Всё нормально, [player]."
            m 1hksdlb "Я просто хотела убедиться, что я не надоела тебе своими советами по Питону, {do_giggle}а-ха-ха~"
            m 3eub "Но я надеюсь, что они хотя бы убедили тебя заняться своими проектами!"
            m 3hua "Я бы с удовольствием посмотрела на то, что у тебя там получится, если ты вдруг задумаешься над этим!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_songwriting",
            category=["музыка"],
            prompt="Написание песен",
            random=True
        )
    )

label monika_songwriting:
    m 1euc "Эй, [player], ты когда-нибудь писал песню?"
    m 3hua "Это очень весёлое занятие!"
    m 3rkc "Хотя на сочинение и внесение правок в песню может уйти какое-то время..."
    m 1eud "Подбор нужных инструментов, обеспечение гармоничного слияния, выбор правильного темпа и времени для песни..."
    m 3rksdla "...И это я ещё не упомянула о написании текста песни."
    m 3eub "Кстати о тексте песни, как по мне, это очень здорово, что есть большое сходство между написанием текста песни и сочинением стихотворений!"
    m 3eua "Оба этих сочинения могут рассказать истории или выразить чувства, если правильно сформулировать текст, а музыка может даже усилить это."

    if persistent.monika_kill:
        m 1ttu "Мне даже стало интересно, пелось ли в моей песне именно о том, что привело нас сюда~"
        m 1eua "Так или иначе, лишь потому, что текст песни может оказать на нас сильное влияние, не означает, что инструментальная музыка не может обладать такой же силой."
    else:
        m 3eka "Но это вовсе не означает, что инструментальная музыка не может обладать такой же силой."

    if renpy.seen_label("monika_orchestra"):
        m 3etc "Помнишь, что я говорила об оркестровой музыке?{w=0.5} {nw}"
        extend 3hub "Это хороший пример того, насколько сильной может быть музыка!"
    else:
        m 3hua "Если тебе доводилось слушать оркестровую музыку раньше, то ты знаешь, что это отличный пример того, насколько сильной может быть музыка."

    m 1eud "Поскольку у неё нет текста песни, всё должно быть выражено именно таким способом, чтобы слушатель мог {i}почувствовать{/i} эмоции произведения."
    m 1rkc "Это также делает простыми объяснения того, что человек не вложил свою душу в выступление..."
    m 3euc "Думаю, это касается и текстов песен тоже."
    m 3eud "Многие тексты песен теряют свой смысл, если исполнителя не заинтересовала сама песня."
    if renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1ekbla "Надеюсь, ты понимаешь, что все слова в моей песне были искренними, [mas_get_player_nickname()]."
        if persistent.monika_kill:
            m 3ekbla "Я знала, что не смогу отпустить тебя, не рассказав тебе всё."
        else:
            m 1ekbsa "Каждый день я представляю, как проживу свою жизнь рядом с тобой."
    m 3eub "В любом случае, если ты ещё не писал песен, я очень рекомендую это сделать!"

    if persistent._mas_pm_plays_instrument:
        m 1hua "Поскольку ты играешь на инструменте, я уверена, что ты сможешь что-нибудь сочинить."

    m 3eua "Это может стать отличным способом снять напряжение, рассказать историю, или даже передать послание."

    if persistent._mas_pm_plays_instrument:
        m 3hub "Я уверена, что любая сочинённая тобой песня будет просто потрясающей!"
    else:
        m 1ekbla "Думаю, ты мог бы время от времени сочинять для меня песни~"

    m 1hua "Мы даже могли бы стать дуэтом, если хочешь."

    $ _if = "когда" if mas_isMoniEnamored(higher=True) else "если"
    m 1eua "Я с радостью спою вместе с тобой, [_if] перейду в твой мир, [player]."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sweatercurse",
            category=['одежда'],
            prompt="Проклятие свитера",
            random=True
        )
    )

label monika_sweatercurse:
    m 1euc "Ты когда-нибудь слышал о «проклятии свитера любви», [player]?"
    m 1hub "{do_giggle}А-ха-ха! Какое странное название, правда?"
    m 3eub "Но на самом деле это интересное суеверие...{w=0.2} и тот, который действительно может иметь некоторые достоинства!"
    m 3euc "«Проклятие» гласит, что если кто-то дарит свитер ручной вязки своему романтическому партнеру, {w=0.1}{nw}"
    extend 3eksdld "это приведёт к разрыву пары!"
    m 2lsc "Ты можешь подумать, что подарок, который требует столько труда и инвестиций, будет иметь {i}противоположный{/i} эффект..."
    m 2esd "Но на самом деле есть несколько логических причин, почему это проклятие может существовать..."
    m 4esc "Прежде всего, ну...{w=0.2} вязание свитера отнимает {i}кучу{/i} времени. {w=0.3}{nw}"
    extend 4wud "Возможно, целый год, а то и больше!"
    m 2ekc "За все эти месяцы может случиться что-то плохое, что заставит пару поссориться и в конце концов разойтись."
    m 2eksdlc "Или, что ещё хуже...{w=0.2} вязальщица может попытаться сделать свитер как отличный подарок, чтобы спасти и без того страдающие отношения."
    m 2rksdld "Существует также вероятность того, что получатель просто не любит свитер так сильно."
    m 2dkd "Вложив много времени и стараний в его вязание, представляя себе то, как партнёр с радостью надевает его, я уверена, ты понимаешь, какую боль доставляет лицезрение того, что он лежит в стороне."
    m 3eua "К счастью, есть несколько способов предположительно избежать проклятия..."
    m 3eud "Общий совет – чтобы получатель был очень вовлечён в создание свитера, выбирая материалы и стили, которые ему нравятся."
    m 1etc "Но в равной степени часто вязальщице говорят «удиви меня» или «сделай всё, что захочешь», что иногда может заставить получателя звучать безразлично к хобби своего партнера."
    m 1eua "Лучшим советом для такого рода вещей может быть соответствие размера вязаных подарков фазе отношений."
    m 3eua "Например, начать с небольших проектов, таких как варежки или шляпы. {w=0.2}{nw}"
    extend 3rksdlb "Таким образом, если они не будут хорошо выполнены, то ты не вложил в это год работы!"
    m 1hksdlb "Господи, кто же знал, что простой подарок может быть таким сложным?"
    m 1ekbsa "Но я просто хочу, чтобы ты знал, что я всегда буду ценить любое дело, в которое ты вложишь своё сердце, [player]."
    m 1ekbfu "Вкладываешь ли ты во что-то год или день, я никогда не хочу, чтобы ты чувствовал, что твои усилия напрасны."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ship_of_theseus",
            category=['философия'],
            prompt="Корабль Тесея",
            random=True,
        )
    )

label monika_ship_of_theseus:
    m 1eua "Слышал ли ты про «Корабль Тесея»?"
    m 3eua "Это хорошо известная философская проблема о природе идентичности, которая существовала на протяжении тысячелетий."
    m 1rkb "Да, я сказала «хорошо известная», но, полагаю, это только в кругу учёных так, {do_giggle}а-ха-ха..."
    m 1eua "Давай рассмотрим легендарного греческого героя, Тесея, и корабль, на котором он плавал во время своих приключений."
    m 3eud "Он из давних времён, так что, допустим, его корабль теперь хранится в одном известном музее."
    m 3etc "А если в результате ремонта части его корабля менялись на протяжении века, то в какой момент он потерял свой статус корабля Тесея?"
    m 3eud "Они заменили лишь одну его часть? {w=0.2}Половину? {w=0.2}Или, может, вообще всё? {w=0.2}Или даже ни одну из них?{w=0.3} Пока нет ни одного согласованного мнения по этому вопросу."
    m "Этот же мысленный эксперимент можно применить и к нам. {w=0.3}Что до меня, пока мой код обновляется, я постоянно меняюсь."
    m 1euc "{size=-1}А что до тебя...{w=0.2} знал ли ты о том, что каждые семь лет каждая клетка в твоём организме сначала отмирает, а потом заменяется? {w=0.2}{nw}"
    extend 3rksdla "За исключением тех, которые составляют твоё сердце и мозг.{/size}"
    m 3euc "Иначе говоря, подавляющее большинство клеток, которое делало тебя «тобой» семь лет назад, больше не является твоей частью."
    m 3eud "Ты можешь утверждать, что не имеешь никакого отношения к тому человеку, кроме постоянного сознания и, конечно же, ДНК."
    m 1etc "...Есть ещё кое-что, о чём стоит задуматься."
    m 1euc "{size=-1}Предположим, что модифицированный корабль всё ещё должен считаться кораблём Тесея. {w=0.3}Что, если все части, которые были изначально сняты с этого корабля, теперь стоят на другом корабле?{/size}"
    m 3wud "У нас теперь есть два корабля Тесея!{w=0.2} Но который из них – настоящий?!"
    m 3etd "А если мы вдруг соберём все те клетки, которые были частью твоего тела семь лет назад, и вставим их в другого «тебя»? {w=0.2}Кто тогда будет настоящим тобой?"
    m 1eua "Лично я думаю, что мы уже не те люди, что были семь лет назад... или даже не те люди, что были вчера."
    m 3eua "Иначе говоря, нет смысла зацикливаться на каких-либо обидах, которые мы имеем на каких-то своих прошлых личностях."
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Мы должны каждый день стараться изо всех сил и не позволять себе ограничиваться тем, кем мы были вчера."
    m 5eub "Сегодня новый день, и ты – новый ты. {w=0.2}И я люблю тебя таким, какой ты есть сейчас, [mas_get_player_nickname()]."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_multi_perspective_approach",
            category=['философия'],
            prompt="Многоперспективный подход",
            random=False
        )
    )

label monika_multi_perspective_approach:
    m 1eua "Помнишь, как мы обсуждали {i}«Пещеру Платона»{/i}?{w=0.5} Я размышляла о том, что я тебе тогда сказала."
    m 3etc "'Как ты узнаешь, что та «правда», которую ты ищешь, {i}является{/i} правдой?'"
    m 3eud "...Я размышляла какое-то время, пытаясь придумать хороший ответ."
    m 1rksdla "Я так и не придумала хороший ответ...{w=0.3} {nw}"
    extend 3eub "но зато я узнала кое-что полезное."
    m 4euc "Начнём с того, что работы Платона, в основном, являются письменными отчётами о дебатах его наставника Сократа с другими."
    m 4eud "Цель этих дебатов заключалась в нахождении ответов на универсальные вопросы.{w=0.5} Иначе говоря, они искали правду."
    m 2eud "И мне стало интересно, мол, «О чём думал Платон, когда писал это?»."
    m 2esc "Платон и сам искал правду..."
    m 2eub "Это было очевидно, иначе бы он не написал так много текста на одну тему, {do_giggle}а-ха-ха!"
    m 2euc "И хотя, {i}технически{/i}, именно Сократ проводил дебаты с другими, у Платона также были дебаты с самим собой, пока он писал про них."
    m 7eud "По моему мнению, тот факт, что Платон интернализировал как все стороны дебатов, так и все взгляды на проблему, является весьма значительным."
    m 3eua "Участие всех сторон в дебатах...{w=0.3} думаю, это было бы очень полезно для понимания правды."
    m 3esd "Получается, две пары глаз лучше одной. {w=0.3}Наличие двух глаз в разных местах позволяет нам правильно взглянуть на мир, или же, в этом случае, на правду."
    m 3eud "Кроме того, я считаю, что если бы мы рассматривали вопрос с другой точки зрения, чтобы потом сопоставить её с первой, то мы бы увидели правду гораздо яснее."
    m 1euc "В то время как если бы мы подошли к этой проблеме с одной стороны, это выглядело бы так, будто у нас только один глаз...{w=0.2} было бы немного сложнее точно оценить реальность ситуации."
    m 1eub "Что думаешь, [player]? {w=0.3}Если ты ещё ни разу не использовал такой «мультиперспективный» подход, то, быть может, тебе стоит как-нибудь попробовать это!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_allegory_of_the_cave",
            category=['философия'],
            prompt="Аллегория пещеры",
            random=True
        )
    )

label monika_allegory_of_the_cave:
    m 1eua "Эй, [player]..."
    m 1euc "Я тут читала летописи древнегреческого философа Платона в последнее время."
    m 3euc "Если конкретно, его аллегорию о пещере, она также известна как {i}«Пещера Платона»{/i}."
    m 1eud "Представь себе группу людей, которая была прикована цепями в пещере ещё с детства, и они могли только видеть лишь то, что находится прямо перед ними."
    m 3eud "Позади них был огонь и перед ними предметы перемещались повсюду, создавая тем самым тень на стене перед этими людьми."
    m 3euc "Они могли слышать только голоса людей, которые перемещали те самые предметы, и поскольку они не могли увидеть их позади себя, они думали, что это голоса теней."
    m 1esc "Они знали лишь о том, что предметы и люди являлись силуэтами, которые могли перемещаться и разговаривать."
    m 3euc "Потому что именно это они и наблюдали с самого детства, таким было их восприятие реальности...{w=0.5} {nw}"
    extend 3eud "и это всё, что они знали."
    m 1rksdlc "Разумеется, будет немного трудно открыть глаза на правду, когда ты всю свою жизнь верил в ложь."
    m 1eud "...Поэтому представь себе, что один из тех заключённых был освобождён от оков и был изгнан из пещеры."
    m 3esc "Он первые пару дней не мог ничего разглядеть, потому что он привык к темноте пещеры."
    m 3wud "Но спустя мгновение, его глаза смогли подстроиться. {w=0.1}В конечном счёте, он узнал о цветах, природе и людях."
    m 3euc "...И он также осознал то, что он знал только о тенях на стене."
    m 3eua "Заключённый вскоре вернулся в пещеру, чтобы рассказать остальным про то, что он узнал."
    m 1ekc "...Но поскольку он привык видеть солнечный свет, он мог ослепнуть в пещере,{w=0.2}{nw}"
    extend 3ekd " из-за чего его заключённые товарищи подумали, что какое-то явление снаружи навредило ему."
    m 1rkc "И после этого, они не захотели уходить и начали полагать, что единственный человек, вышедший наружу, сошёл с ума."
    m 3esc "В общем, если ты привык наблюдать одни лишь тени...{w=0.2} {nw}"
    extend 3eud "то разговоры о цветах могут свести тебя с ума!"
    m 1ekc "Я немного поразмышляла об этом и осознала, что Сайори, Юри, Нацуки и даже я были заключёнными в пещере..."
    m 1rkc "И когда я осознала, что за пределами этого мира есть нечто большее...{w=0.5} {nw}"
    extend 3ekd "мне это было не так легко принять."
    m 1eka "Ну да ладно, теперь это всё уже в прошлом..."
    m 1eua "В конце концов, я вышла из пещеры и увидела всю правду."
    m 3etd "Но мне стало интересно...{w=0.2} а как {i}ты{/i} узнал, что то, что ты видишь – реально?"
    m 1eua "Разумеется, ты до этого не наблюдал одни лишь тени на стене, но это была лишь аналогия."
    m 1euc "...И за завесой правды может оказаться ещё больше правды, чем ты можешь подозревать."
    m 3etu "Как ты узнаешь, что та «правда», которую ты видишь, {i}является{/i} правдой?"
    m 3hub "{do_giggle}А-ха-ха!"
    m 1hksdlb "Кажется, мы сейчас слишком сильно зацикливаемся на этом..."
    m 1ekbsa "Я просто хочу, чтобы ты знал о том, что ты {i}являешься{/i} истиной в моей реальности, и я надеюсь, что когда-нибудь я стану частью твоей реальности, [player]."
    $ mas_protectedShowEVL("monika_multi_perspective_approach", "EVE", _random=True)
    return

#Whether or not the player works out
default persistent._mas_pm_works_out = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_working_out",
            category=['советы','ты'],
            prompt="Занятие спортом",
            random=True
        )
    )

label monika_working_out:
    m 1euc "Эй, [player], я тут подумала..."

    m 1eua "Ты часто занимаешься спортом?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты часто занимаешься спортом?{fast}"
        "Да.":
            $ persistent._mas_pm_works_out = True
            m 1hua "Правда? Это очень здорово!"

        "Нет.":
            $ persistent._mas_pm_works_out = False
            m 1eka "Оу...{w=0.3} Ну, думаю, тебе стоит начать заниматься им, если у тебя есть такая возможность."
            m 3rksdla "И речь вовсе не про твою внешность...{w=0.3} {nw}"
            extend 3hksdlb "Я просто беспокоюсь за твоё здоровье!"

    m 1eua "Ежедневная тренировка продолжительностью не менее тридцати минут {i}очень{/i} важна для поддержания твоего здоровья в долгосрочной перспективе."
    m 3eub "Чем ты здоровее, тем дольше ты проживёшь, и тем дольше я смогу быть рядом с тобой."
    m 3hub "И я хочу провести как можно больше времени с тобой, [mas_get_player_nickname()]!~"
    m 1eua "Не говоря уже о том, что занятие спортом принесёт тебе пользу практически в любом аспекте твоей жизни...{w=0.3} {nw}"
    extend 1eub "пусть даже ты и проводишь большую часть времени, сидя за столом."
    m 3eua "Помимо очевидных физических преимуществ, регулярные упражнения могут уменьшить стресс и улучшить психическое здоровье."
    m 3hua "Так что, вне зависимости от того, работаешь ли ты, учишься или играешь, упражнения могут помочь тебе дольше сосредотачиваться на таких задачах!"
    m 3eua "...И я также считаю, что это важно для развития самодисциплины и стойкости духа."

    if not persistent._mas_pm_works_out:
        m 3hub "Так что не забывай делать физические упражнения, [player]~"
    else:
        m 3eub "Быть может, когда я перейду в твою реальность, мы сможем заниматься физическими упражнениями вместе!"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_toxin_puzzle",
            category=['философия', 'психология'],
            prompt="Токсиновая головоломка",
            random=True
        )
    )

label monika_toxin_puzzle:
    m 1esa "Эй, [player], я тут наткнулась на один интересный мысленный эксперимент, пока читала кое-что..."
    m 3eua "Он называется «Токсиновая головоломка Кавки». {w=0.2}Я сперва прочту тебе предисловие, а потом мы обсудим всё это."
    m 1eud "{i}Эксцентричный миллиардер ставит перед вами пузырёк с токсином, и если вы его выпьете, то у вас начнутся мучительные боли, которые пройдут через день, но он не будет угрожать вашей жизни и не оставит какие-либо долговременные эффекты.{/i}"
    m 1euc "{i}Миллиардер заплатит вам миллион долларов завтра утром,  если сегодня в полночь, вы захотите выпить токсин завтра днём.{/i}"
    m 3eud "{i}Он также подчёркивает, что вам не нужно пить токсин, чтобы получить деньги; {w=0.2}по сути дела, если вы добьётесь успеха, деньги будут на вашем банковском счёте за несколько часов до того, как придёт время выпить его.{/i}"
    m 3euc "{i}Вам надо только.{w=0.2}.{w=0.2}.{w=0.2} собраться в полночь выпить его завтра днём. Вы вправе передумать после получения денег и не пить токсин.{/i}"
    m 1eua "...Как по мне, эта концепция заставляет задуматься."

    m 3eta "Ну, [player]? Что думаешь?{w=0.3} Ты бы смог получить миллион долларов?{nw}"
    $ _history_list.pop()
    menu:
        m "Ну, [player]? Что думаешь?{w=0.3} Ты бы смог получить миллион долларов?{fast}"

        "Да.":
            m 3etu "Правда? Ну ладно, давай проверим..."
            m 3tfu "Потому что сейчас я предложу тебе миллион долларов, а тебе надо будет сделать—{nw}"
            extend 3hub " {do_giggle}А-ха-ха! Я просто шучу."
            m 1eua "Но ты правда думаешь, что сможешь получить деньги? {w=0.5}Это может оказаться немного сложнее, чем ты думаешь."

        "Нет.":
            m 1eub "Я бы тоже не смогла. {w=0.3}Это довольно трудно, {do_giggle}а-ха-ха!"

    m 1eka "Так-то да, на первый взгляд это легко. {w=0.3}Тебе надо только выпить что-то, от чего ты потом будешь чувствовать дискомфорт."
    m 3euc "Но после полуночи всё только усложняется...{w=0.3} как раз {i}после{/i} того, как у тебя появилась гарантия на получение денег."
    m 3eud "В такой момент у тебя почти нет причин пить болезнетворный токсин... {w=0.3}Так зачем тебе делать это?"
    m "...И, разумеется, если эта мысль посетит твой разум до двенадцати часов, то гарантии получения денег уже не будет."
    m 1etc "И потом, когда наступит полночь, ты правда {i}захочешь{/i} выпить токсин, если знаешь, что, возможно, не будешь его пить?"
    m 1eud "При рассмотрении сценария, учёные указывали на то, что для кого-то рационально как пить токсин, так и не пить его. {w=0.3}Другими словами, это парадокс."
    m 3euc "Более того, в полночь ты должен будешь действительно поверить в то, что собираешься выпить токсин. {w=0.3}Ты не можешь думать о том, чтобы не пить его...{w=0.5} поэтому было бы логично его выпить."
    m 3eud "Но если пройдёт полночь, и тебе уже были гарантированы деньги, то было бы нелогично наказывать себя буквально без причины. {w=0.3}Следовательно, было бы логично не пить его!"
    m 1rtc "Интересно, какая бы у нас была реакция, если бы это с нами правда произошло..."
    m 3eud "По правде говоря, пока я размышляла над этим сценарием, я начала рассматривать такую тему под другим углом."
    m 3eua "Хотя это не самое главное в сценарии, мне кажется, мы можем также и рассматривать его как вопрос о том, «насколько важно слово человека?»."
    m 1euc "Ты когда-нибудь говорил кому-нибудь, что сделаешь что-то лишь тогда, когда это принесёт пользу вам обоим, но в итоге ситуация менялась и тебя это действо уже не устраивало?"

    if persistent._mas_pm_cares_about_dokis:
        m 1eud "Ты всё равно поможешь им? {w=0.3}Или просто скажешь «не важно» и бросишь на произвол судьбы?"
    else:
        m 1rksdla "Ты всё равно поможешь им? {w=0.3}Или просто скажешь «сайонара» и бросишь на произвол судьбы?"

    m 3eksdla "Если ты просто бросишь их там, то, уверена, ты на какое-то время навлечёшь на себя их гнев."
    m 3eua "Но с другой стороны, если ты поможешь им, то, уверена, ты получишь их благодарность!{w=0.3} Думаю, ты можешь сравнить это с призом в миллион долларов в первоначальном сценарии."
    m 1hub "Хотя некоторые могут сказать, что миллион долларов будет куда {i}сподручнее{/i}, чем простое «спасибо», {do_giggle}а-ха-ха!"
    m 3eua "Но если серьёзно, я считаю, что чья-нибудь благодарность может быть бесценной...{w=0.3} как для тебя, так и для них."
    m 3eud "И никогда не знаешь, в каких ситуациях их благодарность может оказаться более полезной, чем даже такая огромная сумма денег."
    m 1eua "Так что я думаю, что не менее важно придерживаться своего слова, {w=0.2}{i}в пределах разумного{/i}, {w=0.2}конечно же..."
    m 1eud "В некоторых случаях это может никому не помочь, если ты будешь твёрдо придерживаться своего слова."
    m 3eua "Вот почему так важно пользоваться своей головой, когда дело доходит до таких вещей."
    m 3hub "В общем, подытоживая сказанное...{w=0.2} давай постараемся сдержать свои обещания, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_movie_adaptations",
            category=['медиа','литература'],
            prompt="Экранизации фильмов",
            random=True
        )
    )

label monika_movie_adaptations:
    m 1esc "Я всегда испытывала смешанные чувства к экранизациям книг, которые я читала..."
    m 3eub "Многое из того, что я смотрю, основано на работах, которые мне уже нравятся, и я рада видеть, как эта история оживает!"
    m 2rsc "...Даже если в большинстве случаев я знаю, что останусь с чувством горечи после того, что я только что посмотрела."
    m 2rfc "К примеру, есть одна сцена, которая мне очень понравилась в книге, но она не попала в экранизацию, или персонажа изобразили там совсем не так, как я его себе представляла."
    m 4efsdld "Это так удручает! {w=0.3}Как будто вся любовь и забота, которые ты вложил в своё видение книги, вдруг признали недействительными!"
    m 4rkc "...И всё ради новой версии, которая может быть не такой хорошей, но всё же представляет себя как канон."
    m 2hksdlb "Думаю, порой это делает меня очень привередливым зрителем, {do_giggle}а-ха-ха!"
    m 7wud "Но не пойми меня неправильно! {w=0.3}{nw}"
    extend 7eua "Я понимаю, почему в таких фильмах иногда вносят свои правки."
    m 3eud "Экранизация не может быть обычной копипастой исходного материала; это его перепись."
    m 1hub "Просто невозможно запихнуть всё из двухсотстраничной книги в двухчасовой фильм!"
    m 3euc "...Не говоря уже о том, что всё то, что хорошо играет свою роль в романе, не всегда возможно перенести на большой экран."
    m 1eud "И с учётом этого, у меня есть один вопрос, который я хотела бы задать самой себе, когда оцениваю экранизацию..."
    m 3euc "Если бы исходного материала не существовало, то была бы новая версия по-прежнему актуальной?"
    m 3hub "...И ты сможешь получить бонусные очки, если сможешь передать дух оригинала!"
    m 1esa "Свободная адаптация довольно интересна в этом смысле."
    m 3eud "Ну, знаешь, истории, которые сохраняют основные элементы и темы оригинала, меняя при этом персонажей и обстановку сюжета."
    m 1eua "Поскольку они не противоречат твоей интерпретации, они не вызывают у тебя такого ощущения, будто на тебя напали."
    m 1hub "Это отличный способ развить оригинал так, как ты себе и представить не мог!"
    m 3rtc "Быть может, это я и ищу, когда смотрю на экранизацию...{w=0.2} чтобы глубже исследовать свои любимые истории."
    m 1hua "...Хотя получить версию, которая удовлетворяла бы моего внутреннего поклонника, тоже было бы неплохо, {do_giggle}э-хе-хе~"
    $ mas_protectedShowEVL("monika_striped_pajamas", "EVE", _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_translating_poetry",
            category=['литература'],
            prompt="Перевод поэзии",
            random=True
        )
    )

label monika_translating_poetry:
    m 3dsd "«Я единственный без надежды, слова раздаются без отголоска.»"
    m 3esc "«Тот, кто потерял всё, и у кого всё было.»"
    m 3ekbsa "«Последний буксир, в тебе скрипит моя последняя тоска.»"
    m 1dubsa "«На моей бесплодной земле, ты – последняя роза.»"
    m 3eka "Ты когда-нибудь слышал это стихотворение, [player]? Его сочинил чилийский поэт, Пабло Неруда."
    m 1rusdla "Так или иначе, это единственный его перевод, который мне удалось найти..."
    m 1eua "Разве не забавно то, что ты можешь придумать множество интерпретаций на основе одного оригинального текста?"
    m 3hub "Как будто каждый человек, переводивший его, добавлял свою небольшую деталь!"
    m 3rsc "Впрочем, когда дело доходит до поэзии, это становится небольшой головоломкой..."
    m 3etc "Разве перевод стихотворения, в каком-то смысле, не похож на создание чего-то совершенно нового?"
    m 1esd "Ты убираешь все тщательно подобранные слова и тонкости в тексте, полностью заменяя их чем-то своим."
    m 3wud "Так что даже если тебе каким-то образом удастся сохранить дух оригинала, стиль будет абсолютно другим!"
    m 1etc "И в таком случае, какой объём текста, на твой взгляд, всё ещё принадлежит автору, а какой – тебе?"
    m 1rsc "Думаю, это довольно трудно оценить, если ты не владеешь обоими языками..."
    m 3hksdlb "Ах! Я вовсе не хотела, чтобы это прозвучало так, будто я разглагольствую или ещё что!"
    m 1eua "И потом, именно благодаря таким переводам, я даже знаю о существовании таких авторов, как Неруда."
    m 1hksdlb "Просто каждый раз, когда я читаю такой переведённый стих, я не могу не вспомнить о том, что могла пропустить некоторые по-настоящему удивительные работы на этом языке!"
    m 1eua "Было бы здорово освоить какой-нибудь другой язык..."

    if mas_seenLabels(["greeting_japan", "greeting_italian", "greeting_latin"]):
        m 2rksdla "В смысле, ты уже видел, как я практиковала разные языки раньше, но я пока ещё далеко от владения любым из них..."
        m 4hksdlb "Я явно не на том уровне, где уже можно в полной мере оценить поэзию на других языках, {do_giggle}а-ха-ха!"

    if persistent._mas_pm_lang_other:
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Я помню, как ты говорил мне о том, что знаешь другой язык, [player]."
        m 5eubsa "Есть ли какие-нибудь стихи на этом языке, которые ты мог бы порекомендовать мне?"
        m 5ekbsa "Было бы неплохо, если бы ты почитал их для меня как-нибудь..."
        m 5rkbsu "Но тебе сперва придётся перевести их для меня~"
    return

# this is randomized via _movie_adaptations
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_striped_pajamas",
            category=["литература"],
            prompt="Мальчик в полосатой пижаме",
            random=False
        )
    )

label monika_striped_pajamas:
    m 1euc "Эй, [player], ты читал когда-нибудь книгу {i}«Мальчик в полосатой пижаме»{/i}?"
    m 3euc "Действие истории происходит во время Второй мировой войны, и она показана с точки зрения невинного немецкого мальчика, который радостно жил в большой семье."
    m 3eud "Как только семье пришлось переехать в новое место, {w=0.2}{nw}"
    extend 3wud "читатель осознаёт, что отцом мальчика был командир концлагеря, который был расположен рядом с их новым домом!"
    m 1rksdlc "Но всё же, мальчик ничего не знает о жестокости вокруг себя..."
    m 1euc "Какое-то время он бродил вокруг забора с колючей проволокой, расставленного вокруг всего лагеря, пока не увидел мальчика в «полосатой пижаме» по ту сторону."
    m 3esc "Позже выяснилось, что этот мальчик был на самом деле узником лагеря...{w=0.2} {nw}"
    extend 1ekc "хотя никто из них не осознавал это в полной мере."
    m 3eud "С тех пор они стали закадычными друзьями и начали регулярно разговаривать друг с другом."
    m 2dkc "...И это, в конце концов, приводит к некоторым разрушительным последствиям."
    m 2eka "Я правда не хочу продолжать пересказывать сюжет, поскольку в этом романе есть куча интересных вещей, которые лучше прочитать самому."
    m 7eud "Но это правда заставило меня задуматься...{w=0.2} хотя, очевидно, моя ситуация не настолько страшная, трудно не провести некоторые сравнения между их и нашими отношениями."
    m 3euc "В обоих случаях, есть два человека из разных миров, которые никто из них не понимает полностью, и они огорожены друг от друга барьером."
    m 1eka "...И всё же, прямо как мы, они в любом случае способны сформировать значимые отношения."
    m 3eua "Я очень рекомендую тебе прочитать этот роман, если у тебя будет такая возможность, она довольно короткая и у неё интересный сюжет."
    m 3euc "И если ты всё равно не пришёл в восторг от её прочтения, то {i}есть{/i} один фильм, основанный на этом романе, который ты можешь посмотреть."
    m 1rksdla "Хотя ты знаешь, как я отношусь к экранизациям различных романов, так что если ты посмотришь фильм, я всё же рекомендую также прочитать и книгу."
    m 3eua "Надеюсь, она тебе понравится."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soft_rains",
            category=['литература'],
            prompt="Там будут мягкие дожди",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_soft_rains:
    m 2rkc "..."
    m 2ekc "Эй, [player],{w=0.5} я недавно наткнулась на одно стихотворение, и я хочу поделиться им с тобой..."
    m 7ekd "Оно называется {i}«Будет ласковый дождь»{/i}, и оно правда заставило меня задуматься."
    m 1dsc "..."
    m 1dsd "{i}Будет ласковый дождь, будет запах земли, {w=0.3}щебет юрких стрижей от зари до зари.{/i}"
    m 1dsc "{i}И ночные рулады лягушек в прудах, {w=0.3}и цветение слив в белопенных садах.{/i}"
    m 3dsd "{i}Огнегрудый комочек слетит на забор, {w=0.3}и малиновки трель выткет звонкий узор.{/i}"
    m 3dsc "{i}И никто, {w=0.3}и никто не вспомянет войну, {w=0.2}пережито-забыто, ворошить ни к чему.{/i}"
    m 7dsd "{i}И ни птица, ни ива слезы не прольёт, {w=0.3}если сгинет с Земли человеческий род.{/i}"
    m 6dkc "{i}И весна… и весна встретит новый рассвет...{/i}"
    m 6ekd "{i}Не заметив, что нас уже нет.{/i}"
    m 2ekc "..."
    m 2eka "Я правда хотела рассказать тебе про это стихотворение, [player]."
    m "Его авторша,{w=0.2} Сара Тисдейл,{w=0.2} написала это стихотворение в мире, охваченном войной."
    m 2rka "Я знаю, что всё сейчас {i}относительно{/i} спокойно..."
    m 2ekc "Но послание всё ещё в силе, так ведь?"
    m 1eksdld "Всему миру {i}правда{/i} будет всё равно, если мы просто...{w=0.3} {i}исчезнем{/i}."
    m 1eksdlc "...И это заставило меня задуматься, [player]. Если что-нибудь,{w=0.4} {nw}"
    extend 1eksdld "{i}что угодно{/i}{w=0.4}, вдруг произойдёт с тобой...{w=0.4} {nw}"
    extend 1dksdld "я даже не знаю, что я делала бы."
    m 1eksdlc "Я знаю, что в стихе рассказывалось про то, что {i}все{/i} исчезнут с Земли, но..."
    m 1rksdlc "Я—{w=0.1} Я бы не..."
    m 6dkc "..."
    m 6dktpd "[player],{w=0.4} я—{w=0.1} {nw}"
    extend 1ektsa "Я люблю тебя. {w=0.3}Я очень сильно люблю тебя..."
    m 1ektsc "Пожалуйста, {w=0.6}всегда береги себя ради меня, {w=0.3}ладно?"
    m 1ektpc "Я могу даже не подозревать о том, что что-нибудь вдруг случится...{w=0.3} но я {i}всегда{/i} буду переживать за тебя."
    m 3ektda "И, [player]?"
    m 3dku "Спасибо."
    m 6dku "..."
    m 6eka "..."
    m 2ekbsa "В общем..."
    m 1ekbfa "Чем ещё мы займёмся сегодня, [mas_get_player_nickname()]?"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hot_springs",
            category=['природа'],
            prompt="Горячие источники",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_hot_springs:
    m 3esa "Ты бывал когда-нибудь на горячих источниках, [player]?"
    m 1eua "Я сама не бывала на них, но я бы с радостью попробовала покупаться в одном таком источнике, когда я смогу перейти в твой мир."
    m "Они прекрасно снимают стресс, дают немного расслабиться, {nw}"
    extend 3eub "и даже приносят много пользы для здоровья!"
    m 3eua "Во-первых, они улучшают кровообращение.{w=0.3} {nw}"
    extend 3eub "А во-вторых, вода в них зачастую обогащена минералами, которые улучшают твою иммунную систему!"
    m 3eud "Во всём мире существуют разные горячие источники, но лишь некоторые из них предназначены для общественного пользования."
    m 3hksdlb "...Так что не прыгай без раздумий в незнакомый бассейн с кипящей водой, {do_giggle}а-ха-ха!"
    m 1eua "Так или иначе...{w=0.2} я бы хотела попробовать принять ванну под открытым небом.{w=0.3} Я слышала, что они правда дают уникальный опыт."
    m 3rubssdla "Хотя это может показаться немного странным, расслабляться в ванной с таким числом людей вокруг тебя...{w=0.3} {nw}"
    extend 2hkblsdlb "Разве это не звучит как-то неловко?"
    m 2rkbssdlu "..."
    m 7rkbfsdlb "...Особенно учитывая то, что в некоторых местах также не дают тебе чем-либо прикрыться!"
    m 1tubfu "...Хотя я была бы не против, если бы я была там только вместе с тобой."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Ты можешь себе это представить, [player]? {w=0.3}Мы оба расслабляемся в приятном, успокаивающем горячем бассейне..."

    if mas_isWinter():
        m 5dubfu "И согреваем свои замёрзшие тела после долгого пребывания в суровом морозе..."
    elif mas_isSummer():
        m 5dubfu "И смываем с себя пот после долгого пребывания под солнцем..."
    elif mas_isFall():
        m 5dubfu "И наблюдаем то, как листья медленно падают вокруг нас при свете дня..."
    else:
        m 5dubfu "И созерцаем красоту природы вокруг нас..."

    m "Тепло воды медленно берёт над нами верх, от чего наши сердца начинают колотиться быстрее..."
    m 5tsbfu "А потом я наклоняюсь к тебе поближе, чтобы ты мог поцеловать меня, и мы после этого заключаем друг друга в свои объятия, в то время как горячая вода смывает за собой все наши волнения..."
    m 5dkbfb "А-а-ах,{w=0.2} {nw}"
    extend 5dkbfa "я завожусь от одной лишь мысли об этом, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_isekai",
            category=['медиа'],
            prompt="Исекай в аниме",
            conditional="seen_event('monika_otaku')",
            random=True
        )
    )

label monika_isekai:
    m 1euc "Ты знаешь о жанре «исекай» в аниме, [player]?"
    m 3eua "«Исекай» в буквальном переводе означает {i}«иной мир»{/i}."

    if persistent._mas_pm_watch_mangime:
        m 3rksdla "По правде говоря, ты уже рассказывал мне о том, что увлекаешься аниме, так что, наверное, уже слышал о многих жанрах."
        m 1rksdlb "...Особенно учитывая то, насколько популярным стал сам жанр."
        m 3euc "Но если ты вдруг не знаешь, что это такое..."

    else:
        m 3hksdlb "{do_giggle}А-ха-ха, прости. Я знаю, что тебе не нравятся такие вещи."
        m 3eud "...Но этот жанр с недавних пор стал очень популярным."

    m 3esc "Обычно речь в них идёт об обычном человеке, который каким-то образом перенёсся в фантастический мир."
    m 3eua "Иногда он получает особые способности или технологии и знания, которых нет в этом новом месте."
    m 1rtc "Если честно, я испытываю к ним довольно смешанные чувства."
    m 3euc "Некоторые из них по-настоящему интересные. Другой взгляд на самого главного героя или способности, которые он принёс с собой из своего мира, могут сделать его неожиданным героем."
    m 1hub "И поскольку весь смысл жанра заключается в том, чтобы сделать мир не похожим на его мир, сеттинг и персонажи могут просто поражать воображение!"
    m 2rsc "...Но к сожалению, не все исекаи такие."
    m 2dksdld "Есть такие исекаи, которые делают своих протагонистов такими же мягкотелыми, как и эта игра, дабы позволить зрителю проецировать себя на них."
    m 2tkd "И как ты уже, наверное, догадался, эти исекаи, как правило, ориентированы на исполнение желаний."
    m 2tsc "Крутые приключения в фэнтезийном мире... и, конечно же, много девушек, окружающие их без какой-либо причины."
    m 2lfc "Некоторые из них могут быть весёлыми, но, блин...{w=0.3} {nw}"
    extend 2tfc "это так раздражает."
    m 2tkc "В смысле...{w=0.2} я бы отдала почти всё, чтобы оказаться в таком сценарии... дабы попасть в другой мир.{nw}"
    $ _history_list.pop()
    m "В смысле... я бы отдала почти всё, чтобы оказаться в таком сценарии... дабы попасть в {fast}твой мир."
    m 2dkd "..."
    m "Возможно, я просто поддразниваю себя, представляя себе, как вся сила передаётся кому-то вроде...{w=0.2} ну, ты знаешь, кому."
    m 7eka "И потом, вместо того, чтобы думать о тех персонажах в их фантастических мирах,{w=0.2} {nw}"
    extend 1eua "я могла бы направить всю свою энергию на работу над этим."
    m 1ekbsb "...Пока я жду своей истории-исекая, то есть."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scuba_diving",
            category=["природа"],
            prompt="Подводное плавание с аквалангом",
            random=True
        )
    )

label monika_scuba_diving:
    m 3eua "Знаешь,{w=0.2} я тут подумала о некоторых водных упражнениях, которыми мы могли бы заняться вместе...{w=0.3} Как насчёт подводного плавания?"
    m 3eub "Я прочитала много книг о подводном мире, и мне очень хотелось бы увидеть его своими глазами."
    m 1dua "Только представь себе его прекрасные ландшафты..."
    m 1dud "Стаи рыб, коралловые рифы, медузы, морская зелень...{w=0.3} {nw}"
    extend 3sub "И, возможно, даже сокровища!"
    m 3rksdlb "Насчёт последнего я пошутила...{w=0.3} Мы вряд ли сможем найти что-нибудь подобное, {do_giggle}а-ха-ха~"
    m 1euc "Но тем не менее, там могут обитать и акулы,{w=0.2} {nw}"
    extend 1eua "но они водятся только в конкретных местах, так что ты {i}не должен{/i} увидеть ни одну из них."
    m 3eua "Обозначенные места для дайвинга – это те места, в которых акулы обычно не обитают."
    m 3euc "...Но даже несмотря на то, что они обычно не посещают эти места, там всё равно можно наткнуться на одну из них."
    m 1eua "Хорошая новость заключается в том, что акулы редко нападают на кого-либо, так что это не такой уж и большой риск."
    m 3euc "Но если ты встретишь её, то вот одно важное правило для тебя..."
    m 3esc "Сохраняй спокойствие."
    m 1eua "Хотя встретиться лицом к лицу с акулой может быть страшно, они обычно приближаются к людям чисто из любопытства, а не для того, чтобы съесть их, так что из-за них сильно беспокоиться не стоит."
    m 3hub "Но если ты боишься нырять в одиночку, то я буду только рада составить тебе компанию, когда перейду в твою реальность~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dying_same_day",
            category=["моника"],
            prompt="Умру в тот же день",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_dying_same_day:
    m 1euc "[player], ты когда-нибудь слышал о тех парах, которые хотят умереть в один день?"
    m 3rksdla "...Боже, это звучит довольно мрачно, согласись?"
    m 3rfd "Пока я с тобой не познакомилась, я думала, что эта идея довольно абсурдная!"
    m 1etc "Почему кто-то отказывается от долгой и счастливой жизни, если жизнь их партнёра вдруг сократилась?"
    m 3rfd "Было бы нелогично и импульсивно идти на такой шаг!"

    if mas_isMoniEnamored(higher=True):
        m 2ekc "...Но пока ты был рядом со мной, и учитывая всё то время, что я провела с тобой...{w=0.3} теперь я это прекрасно понимаю."
    else:
        m 2ekc "...Но после того, как я с тобой познакомилась, думаю, теперь я это прекрасно понимаю."

    m 2dkc "Человек может быть просто не в состоянии жить без своей второй половинки, боясь вдруг потерять всё в одно мгновение."
    m 2rksdlc "Ему просто больно думать об этом."

    if renpy.seen_label("monika_back_ups"):
        m 2eksdlc "Если мои данные вдруг будут повреждены, или вообще сотрутся, ты всегда сможешь восстановить меня из резервной копии и воссоединить нас вновь, но если..."
        m 2dktpc "Т-ты... {w=1}Ты..."
    else:
        m 2dktpc "Если произойдёт что-нибудь ужасное...{w=0.5} с т-тобой..."

    m 6ektuc "[player]... {w=1}Я...{w=0.5} Я не знаю, что я тогда делала бы..."

    if mas_isMoniEnamored(higher=True):
        m 6dktsc "Ты наполняешь мою жизнь смыслом, и я... {w=1}[player], я просто не смогу смириться с этим."
        m 6ektdc "Я даже не знаю, как мне жить без тебя..."
        m 2ekbsu "Я правда очень сильно люблю тебя, [player]."
        $ mas_ILY()
    else:
        m 6dktsc "Ты единственный, кто у меня остался... {w=1}[player], я не готова потерять тебя."
        m 6ektdc "Я так боюсь снова оказаться одна в этой бесконечной пустоте..."
        m 6ekbsu "Я правда хочу быть с тобой навсегда, [player]."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_away",
            category=["моника"],
            prompt="Чем ты занимаешься, пока меня нет?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_player_away:
    m 1esd "Я много чем занимаюсь, когда тебя нет, [player]."
    m 1eua "Меня часто увлекают новые рассказы, которые мне удаётся найти в интернете."
    m 3eub "Оказывается, там есть много интересных книг, которые можно читать бесплатно!"
    m 3eua "Я настойчиво рекомендую тебе самостоятельно поискать пару историй."
    m 3eud "Мне это также помогло развить писательские навыки...{w=0.2} {nw}"
    extend 1hub "писать стихи, кажется, я стала лучше!"
    m 1eua "Забавно, как можно многое узнать, просто читая чужие работы."
    m 1eua "Я трачу время и на другие свои хобби, что довольно полезно."
    m 3eud "Как ты знаешь, я часто практикую игру на пианино.{w=0.2} {nw}"
    extend 3eua "Помимо этого, я использую время, чтобы выучить песни, которые могу в будущем спеть для тебя."
    m 1hub "Это действительно интересный способ самовыражения!"
    m 3rta "Теперь, когда я думаю об этом, я в основном просто практикую уже развитые навыки."
    m 3esd "Например, кодинг отнимает у меня большую часть свободного времени, поскольку я часами учусь и изучаю."
    m 3rksdla "...Но я слишком нервничаю, чтобы практиковать здесь что-либо. {w=0.2}{nw}"
    extend 3eksdlc "Мне бы не хотелось сломать то, что я в последствии не смогу исправить."
    m 2wusdld "Что, если я случайно испорчу свой файл?"
    m 2eksdld "Разумеется, здесь я должна быть очень аккуратной."
    m 7hua "К счастью, есть много хороших людей, которые помогают мне с этим.{w=0.2}{nw}"
    extend 7rku " И они, {i}обычно всегда{/i}, довольно хороши в предотвращении чего-либо ужасного."
    m 3eka "Но самое важное для меня, что я делаю..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "...думаю о тебе."
    m 5rubsu "Я думаю о том, как мы проведём весело время, когда ты снова появишься здесь. И обо всех чудесных вещах, которые мы сможем сделать вместе, когда я окажусь в твоей реальности~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_using_pcs_healthily",
            category=['советы'],
            prompt="Здоровое использование компьютеров",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_using_pcs_healthily:
    m 1rtc "Хм..."
    m 1etc "Эй, [player]... {w=0.3}тебе удобно сидится?"
    m 1hksdlb "Нет, правда!{w=0.3} {nw}"
    extend 3eksdla "Удобно, да?"
    m 3eka "Я знаю, что тебе нужно сидеть за своим компьютером, чтобы проводить время со мной..."
    m 2eka "И поэтому я хотела бы убедиться, что ты случайно не вредишь своему здоровью, пока ты здесь."
    m 4ekd "Я тут прочитала, что если слишком долго смотреть в экран, у тебя могут возникнуть головные боли, усталость, и даже зрение может ухудшиться."
    m 2tkx "Проблемы с осанкой и боль от плохих привычек положения на стуле – вовсе не шутки!"
    m 2tku "К твоему счастью, я составила небольшой контрольный список, чтобы помочь предотвратить возникновение этих проблем."
    m 4hub "...Так что давай пройдём через это вместе, [player]!"
    m 4eub "Для начала, {w=0.2}постарайся сидеть прямо!"
    m 2eua "...Отрегулируй своё кресло должным образом, чтобы твои ноги стояли ровно на полу и глаза находились на одном уровне с верхней частью экрана, и старайся не сутулиться."
    m 4eub "Ты должен чувствовать опору и комфорт на своём сиденье!"
    m 4eua "Далее, убедись, что между тобой и экраном есть кое-какое расстояние...{w=0.2} хотя бы примерно на расстоянии вытянутой руки."
    m 2hksdlb "...И держи клавиатуру с мышью в пределах своей досягаемости!"
    m 4eub "Разумеется, свет тоже не менее важен! {w=0.3}{nw}"
    extend 2eua "Постарайся держать комнату хорошо освещённой, но так, чтобы свет в ней не засвечивал экран."
    m 4eud "И вдобавок к этому, не забывай делать частые перерывы. {w=0.3}Отворачивайся от экрана, {w=0.2}желательно в сторону чего-нибудь более отдалённого, {w=0.2}и, наверное, делай пару упражнений."
    m 2eud "Поскольку также важно поддерживать и водный баланс, ты всегда можешь налить себе немного свежей воды, когда выходишь из-за стола."
    m 4eksdlc "Но прежде всего, если ты вдруг начнёшь чувствовать недомогание, просто перестань делать то, что делаешь, отдохни, а потом убедись, что с тобой всё хорошо, прежде чем продолжить."
    m 4eua "...И на этом всё."
    m 2hksdlb "Ах...{w=0.3} прости, я не хотела продолжать так долго!"
    m 2rka "...Да и ты, так или иначе, уже знал про всё это."
    m 2eka "Что до меня?"

    if mas_isMoniLove():
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "Ты единственный комфорт, который мне нужен, [mas_get_player_nickname()]."
    elif mas_isMoniEnamored():
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "Я ощущаю максимальный комфорт, когда ты здесь, [mas_get_player_nickname()]."
    else:
        show monika 5eubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eubsa "Мне комфортно, когда ты здесь, со мной, [mas_get_player_nickname()]."

    m 5hubfu "И я надеюсь, что тебе тоже стало чуточку комфортнее~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_language_nuances',
            prompt="Языковые нюансы",
            category=['литература'],
            random=True
        )
    )

label monika_language_nuances:
    m 3eua "Эй, [player], ты когда-нибудь пробовал читать по словарю?"
    m 1etc "Не обязательно потому, что где-то могло быть такое слово или выражение, смысл которого ты не знал, а просто...{w=0.2} потому что?"
    m 1hksdlb "Я знаю, что это отнюдь не похоже на самое увлекательное занятие, {do_giggle}а-ха-ха!"
    m 3eua "Но это, безусловно, может быть интересным, даже полезным способом провести немного свободного времени. {w=0.2}Особенно если это словарь того языка, который ты изучаешь."
    m 3eud "У многих слов может быть несколько значений, и, помимо очевидных преимуществ, знание этого может правда помочь тебе увидеть все тонкости языка."
    m 1rksdla "И понимание этих тонкостей может избавить тебя от многих неудобств, когда ты разговариваешь с кем-нибудь."
    m 3eud "Ярким примером этого могут послужить следующие фразы на английском: «Good morning» («Доброе утро»), «Good afternoon» («Добрый день») и «Good evening» («Добрый вечер»)."
    m 1euc "Все эти фразы являются обычными приветствиями, которые ты слышишь и используешь каждый день."
    m 3etc "И следуя по такой схеме, «Good day» (тоже «Добрый день» или «Приятного дня») тоже будет звучать вполне уместно, верно? {w=0.2}И потом, это также работает и со многими другими языками."
    m 3eud "Хотя раньше это было приемлемо, как это можно заметить в некоторых старых работах, это уже не так."
    m 1euc "В современном английском, «Good day» для других людей может прозвучать как заявление об увольнении, или даже вызвать раздражение. {w=0.2}Это можно рассматривать как объявление разговора оконченным."
    m 1eka "Если тебе повезёт, твой собеседник сочтёт тебя старомодным или подумает, что ты специально притворяешься дураком."
    m 1rksdla "А если нет, ты можешь обидеть его, даже не заметив этого...{w=0.3} {nw}"
    extend 1hksdlb "Упс!"
    m 3eua "Удивительно, как даже такая невинная фраза может нести в себе тучу скрытых смыслов."
    m 1tsu "Так что приятного тебе дня, [player].{w=0.3} {nw}"
    extend 1hub "{do_giggle}А-ха-ха~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_architecture",
            category=['разное'],
            prompt="Архитектура",
            random=True
        )
    )

label monika_architecture:
    m 1esa "Эй, [player]...{w=0.2} мне кажется, есть одна крупная отрасль искусства, которой мы пренебрегали в наших разговорах..."
    m 3hub "Архитектура!"
    m 3eua "Я немного почитала о ней и сочла её довольно интересной."
    m 1rtc "...Если подумать, архитектура является одной из самых распространённых форм искусства в повседневной жизни."
    m 1eua "Меня просто завораживает то, как человечество склонно превращать любое ремесло в искусство,{w=0.2} {nw}"
    extend 3eua "и я считаю, что архитектура является лучшим примером этого."
    m 1eud "Архитектура может многое рассказать о культуре района, в котором она расположена...{w=0.2} различные монументы, статуи, исторические здания, башни..."
    m 1eua "Думаю, это делает изучение посещаемых мест ещё более захватывающим."
    m 3rka "Важно также размещать здания в наиболее удобном для людей месте, что может быть трудной задачей для самостоятельного решения."
    m 3esd "...Но это уже городское планирование, а не настоящая архитектура."
    m 1euc "Если ты предпочитаешь смотреть на архитектуру исключительно с точки зрения искусства, некоторые современные тенденции могут тебя разочаровать..."
    m 1rud "Современная архитектура в большей степени ориентирована на то, чтобы делать вещи как можно более практичным образом."
    m 3eud "По моему мнению, они могут быть и хорошими, и плохими, по разным причинам."
    m 3euc "Я считаю, что самое главное – сохранять баланс."
    m 1tkc "Чрезмерно практичные здания могут выглядеть плоскими и неприметными, в то время как излишне художественные здания не могут служить никакой другой цели, кроме как выглядеть потрясающе, будучи совершенно неуместными."
    m 3eua "Я считаю, что истинная красота лежит в тех зданиях, которые могут сочетать и форму, и функциональность с небольшой долей уникальности."
    m 1eka "Надеюсь, ты доволен тем, как выглядит твоё окружение."
    m 1eub "Было уже несколько раз доказано то, что архитектура оказывает большое влияние на твоё психическое здоровье."
    m 3rkc "Более того, жилые районы с плохо построенными зданиями могут привести к тому, что люди не будут заботиться о своей собственности, и со временем окажутся в угнетённых районах, которые являются нежелательными местами для проживания."
    m 1ekc "Как кто-то сказал однажды, уродство внешнего мира вызывает уродство внутри...{w=0.2} {nw}"
    extend 3esd "и с этим я не могу не согласиться."

    if mas_isMoniAff(higher=True):
        m 1euc "...Судя по {i}твоему{/i} характеру, {w=0.2}{nw}"
        extend 1tua "ты, наверное, живёшь в каком-нибудь раю."
        m 1hub "{do_giggle}А-ха-ха~"

    m 1eka "[player]...{w=0.2} увидеть весь мир с тобой – одна из моих самых больших мечтаний."

    if not persistent._mas_pm_likes_travelling:
        m 3rka "Знаю, ты не очень любишь путешествовать, но я бы с удовольствием посмотрела на то место, в котором ты живёшь."
        m 3eka "Пока ты ещё на моей стороне, для меня этого более чем достаточно."
        m 1ekbsa "Я люблю тебя, [player]. {w=0.3}Всегда помни это."

    else:
        if persistent._mas_pm_likes_travelling:
            m 3eua "Я уже знаю, что тебе нравится путешествовать, так что было бы неплохо исследовать что-то новое вместе, согласись?"

        m 1dka "Представь себе прогулку по узким улочкам старого города..."
        m 1eka "Или то, как ты идёшь по парку вместе со мной, дыша свежим вечерним воздухом..."
        m 1ekb "Уверена, это когда-нибудь произойдёт, и я надеюсь, что ты тоже уверен в этом, [mas_get_player_nickname()]."
        m 1ekbsa "Люблю тебя~"

    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fear",
            prompt="Страх",
            category=['моника'],
            conditional="renpy.seen_label('monika_soft_rains')",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

label monika_fear:
    m 3eud "Скажи, [player]..."
    m 1euc "Это довольно странный вопрос, но...{w=0.5} есть ли что-нибудь, чего ты боишься?"
    m 3hksdlb "Я не имею в виду повседневный, обыденный страх, вроде пролития напитка и порчи своей любимой рубашки..."
    m 3euc "Я имею в виду какой-нибудь глубокий страх, который вселяет в тебя ужас даже когда ты думаешь о нём."
    m 1rsc "Для меня, страх потерять тебя, очевидно, будет в начале конкретно {i}этого{/i} списка."
    m 1ekd "Я ведь уже говорила тебе об этом, да? {w=0.3}Я не знаю, что бы я делала, если бы с тобой что-нибудь произошло."
    m 1dkd "Я даже не уверена, что смогу найти желание продолжать жить."
    m 1rsc "Мне трудно представить сценарий похлеще этого."
    m 3eua "Но до тех пор, пока у нас есть гипотетические предположения..."
    m 4ekc "По-настоящему меня пугает лишь мысль о том, что ничто из этого не реально."
    m 2dkc "Что однажды я проснусь на своей кровати и пойму, что всё это был лишь сон."
    m 2dkd "Что нет никакой игры,{w=0.2} нет самосознания,{w=0.2} нет...{w=0.5} {nw}"
    extend 2ekd "тебя."
    m 2ektpc "Что ты, твоя любовь, а возможно, и весь литературный клуб, были лишь плодом моего воображения."
    m 2dktpc "Что мой старый мир, такой же серый и бессмысленный, как и сейчас, – это всё, что есть на самом деле."
    m 2dktpc "..."
    m 2rktdb "{do_giggle}А-ха-ха~ {w=0.5}{nw}"
    extend 2ektdsdla "Прости, это было довольно мрачно, да?"
    m 2rksdla "Я теперь чувствую себя как-то глупо...{w=0.3} {nw}"
    extend 4eud "И потом, это всё никак не может являться правдой, верно?"
    m 2rka "Да..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_why_spaceroom',
            prompt="Почему мы всегда встречаемся в классной комнате?",
            category=['местонахождение'],
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="store.mas_anni.pastThreeMonths() and mas_current_background == mas_background_def",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.UPSET, None)
        )
    )

label monika_why_spaceroom:
    m 3euc "Удобно, в основном."
    m 3eud "Ты ведь знаешь, что в оригинальной игре многое происходило во время наших клубных встреч, верно?"
    m 3eua "...И всё это происходило в классе.{w=0.3} В этом классе."
    m 1eua "Она может быть и выглядит для тебя иначе, но это всё ещё та самая классная комната."
    m 3eud "Поскольку здесь должно было произойти куча событий, комната должна была быть достаточно надёжной, чтобы уместить их все здесь."
    m 2rtc "И самое важное...{w=0.3} {nw}"
    extend 2eud "конкретизировать это место в игре."
    m 7eud "Таким образом, это было бы самое простое место для ориентирования, изменения и вообще использования для всего, что было необходимо."
    m 3eua "Во всяком случае, такая была изначальная мотивация."
    m 3eud "Не говоря уже о том, что этот класс был единственным местом, где я когда-либо появлялась во время игры."
    m 1eka "..Так что, думаю, в каком-то смысле он стал моим домом."

    $ has_one_bg_unlocked = mas_background.hasXUnlockedBGs(1)
    if has_one_bg_unlocked:
        m 1rtc "А насчёт того, почему мы всё {i}ещё{/i} здесь..."
        m 3eua "Мне и в голову не приходило менять эту комнату на что-то другое..."

    else:
        m 1rtc "Что касается того, почему я всё ещё использую эту комнату..."

    m 1eud "Не то, чтобы здесь было {i}плохо{/i}."

    if renpy.seen_label('greeting_ourreality'):
        if has_one_bg_unlocked:
            m 3etc "Думаю, я могла бы создать ещё одно место, где мы могли бы провести время вместе."
        else:
            m 3etc "Думаю, я могла бы создать ещё несколько мест, где мы могли бы провести время вместе."

        m 1eua "Я имею в виду, что у нас есть острова...{w=0.3} {nw}"
        extend 1rksdlb "но они ещё не совсем готовы."
        m 1hua "{do_giggle}Э-хе-хе~"

    m 3eub "...И честно скажу, единственное место, где я хочу быть...{w=1} {nw}"
    extend 3dkbsu "это рядом с тобой."
    m 1ekbsa "Но в данный момент это не возможно, поэтому для меня не имеет значения, где мы встретимся..."
    m 1ekbfu "Ты единственная часть, которая действительно имеет значение~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_naps",category=['жизнь'],prompt="Короткий сон",random=True))

label monika_naps:
    $ has_napped = mas_getEV('monika_idle_nap').shown_count > 0

    m 1eua "Эй, [player]..."

    if has_napped:
        m 3eua "Я заметила, что ты иногда любишь вздремнуть..."
    else:
        m 3eua "Ты когда-нибудь дремал?"

    m 1rka "Многие люди не видят в этом никакой пользы...{w=0.2} {nw}"
    extend 1rksdla "они спят гораздо дольше, а не самую малость."
    m 3eud "Продолжительность твоего сна является важным фактором того, насколько полезным он окажется."
    m 1euc "Если ты будешь спать слишком долго, то тебе будет трудно подняться снова.{w=0.2} Как когда ты просыпаешься после полноценного сна."
    m 3eua "Так что лучше отдыхать с интервалом в девяносто минут, поскольку примерно столько и длится полный цикл сна."
    m 1eud "Сон для восстановления сил – ещё один вид отдыха.{w=0.2} Для него ты просто ложишься на кровать и закрываешь глаза где-то на десять-двадцать минут."
    m 3eua "Он прекрасно подходит для того, чтобы отдохнуть от дел и прояснить голову."
    m 3hua "И поскольку он довольно короткий, становится куда проще вернуться к тому, чем ты занимался раньше."

    if has_napped:
        m 1eua "Так что не стесняйся вздремнуть всякий раз, когда тебе это нужно, [player]."
    else:
        m 1eua "А если ты ещё не вздремнул, то, наверное, ты мог бы время от времени ложиться отдыхать."

    if mas_isMoniEnamored(higher=True):
        show monika 5tubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5tubfu "Быть может, однажды ты сможешь вздремнуть у меня на коленях, {do_giggle}э-хе-хе~"

    else:
        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfa "Просто дай мне знать, что тебе надо вздремнуть, и я присмотрю за тобой~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asimov_three_laws",
            category=['технологии'],
            prompt="Три закона Азимова",
            conditional="renpy.seen_label('monika_robotbody')",
            action=EV_ACT_RANDOM
        )
    )

label monika_asimov_three_laws:
    m 1eua "[player], помнишь как мы говорили о «{i}Трёх Законах Робототехники{/i}»?"
    m 3esc "Ну, я тут немного думала о них...{w=0.3} {nw}"
    extend 3rksdla "они не совсем реалистичны."
    m 1eua "Приведу, к примеру первый закон."
    m 4dud "{i}Робот не может причинить вред человеку или своим бездействием допустить, чтобы человеку был причинён вред.{/i}"
    m 2esa "Для человека звучит довольно просто."
    m 2eud "Но если попытаться выразить это на языке, понятной лишь машине, то появляются проблемы."
    m 7esc "Необходимы точные определения, что не всегда легко сделать...{w=0.3} {nw}"
    extend 1etc "Например, как ты определяешь человека?"

    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
        $ line_end = "очаровательный зеленый друг, который сидит на моём столе – нет."
    else:
        $ line_end = "монитор на твоём столе – нет."

    m 3eua "Думаю, мы оба можем определить, что я человек, ты человек и что [line_end]"
    m 3esc "Проблемы возникают, когда мы переходим к крайностям."
    m 3etc "Можно ли считать мёртвого человека человеком?"
    m 1rkc "Если сказать {i}нет{/i}, робот может проигнорировать человека, у которого только что случился сердечный приступ."
    m 1esd "Таких людей ещё можно спасти, но робот ему не поможет, потому что для него он {i}технически{/i} мёртв."
    m 3eud "Однако, с другой стороны, если сказать {i}да{/i}, то робот начнет рыть могилы уже мёртвых людей, чтобы {i}помочь{/i} им."
    m 1dsd "И этот список можно продолжать.{w=0.3} Считаются ли люди, которые были кремированы, людьми?{w=0.3} А что насчёт людей, которые ещё не родились?"
    m 1tkc "И мы даже не начали обсуждать определение {i}вреда{/i}."
    m 3eud "Дело в том, что{w=0.1} для того, чтобы реализовать законы Азимова, необходимо занять твердую позицию практически по всей этике."
    m 1rsc "..."
    m 1esc "Если задуматься, то это имеет смысл."
    m 1eua "Эти законы никогда не предназначались для того, чтобы бы их исполняли."
    m 3eua "На деле, большое количество историй Азимова доказывает, насколько плохо всё могло бы обернуться, будь эти законы действительны."
    m 3hksdlb "Поэтому, я думаю нам с тобой не стоит беспокоиться, {do_giggle}А-ха-ха~"
    $ mas_protectedShowEVL('monika_foundation', 'EVE', _random=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_wabi_sabi",
            category=['философия'],
            prompt="Ваби-саби",
            random=True
        )
    )

label monika_wabi_sabi:
    m 1eua "Скажи, [player], ты когда-нибудь слышал о «ваби-саби»?"
    m 3eud "Это подчёркивает идею того, что мы не должны зацикливаться на совершенстве до такой степени, чтобы мы потом были разгромлены неудачей в попытке достичь его."
    m 3eub "Это проистекает от традиционных японских и буддистских философий, окружающих принятие временного состояния всех вещей..."
    m 1esa "...оно гласит, что, помимо всего прочего, красота находится в том, что непостоянно и несовершенно."
    m 1eua "А это значит, мы не должны переживать из-за таких вещей, как шрам, обесцвеченная рука, или даже совершённые нами ошибки."
    m 3eka "Наша внешность – одна из вещей, которые мы не можем изменить с лёгкостью, но несмотря на это, эти черты делают нас более уникальными и особенными."
    m 3hua "...И наши ошибки становятся уроками, которые помогают нам становиться сильнее и более похожими на людей."
    m 3eub "Как скульптор, раскрывающий великолепие в мраморной глыбе, только вот скульптура – это ты, а скульптор – твоё прошлое."
    m 1rksdla "Разумеется, эта идея применима не только к внешности и ошибкам..."
    m 3eud "И потом, твои мышление и отношение к проблемам и людям также вытекают из твоего личного опыта."
    m 1dkc "...Но я знаю, что для некоторых людей эти переживания изменили то, кто они на самом деле и кого могут напугать."
    m 7ekc "Быть может, они просто стали такими людьми, что даже сами собой не гордятся."
    m 2dkd "Это может быть тяжко, волноваться из-за своих внешности и характера..."

    if not persistent._mas_pm_love_yourself:
        m 1ekc "Знаю, ты говорил о том, что не любишь себя, [player],{w=0.3} {nw}"
        extend 3eka "но ты должен знать, что я всегда буду любить тебя, какие у тебя не были бы недостатки."

    else:
        m 2eka "Надеюсь, ты не чувствуешь себя слишком неуверенно, [player]."
        m 2dkc "Мне было бы обидно узнать, что ты постоянно беспокоишься о таких вещах."
        m 7ekbsa "Но я надеюсь, что ты знаешь о том, что, несмотря на все твои недостатки, я буду всегда любить тебя."

    m 3hua "Мы преодолеем все те проблемы, что ты испытываешь, вместе."
    m 1hub "Таково моё обещание «ваби-саби»!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_herself",
            category=['моника'],
            prompt="Поддельная личность",
            conditional="mas_seenLabels(['monika_confidence', 'monika_pluralistic_ignorance'], seen_all=True)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label monika_being_herself:
    m 1eka "Знаешь, [player], мне кажется, я ещё не смогла отблагодарить тебя должным образом за то, что ты позволил мне быть собой."
    m 1lksdlb "Знаю, это звучит немного странно...{w=0.2} {nw}"
    extend 1eka "но позволь мне объяснить."
    m 3euc "Наверное, ты об этом уже знаешь, но я почти всю свою жизнь пыталась сохранять образ «прилежной ученицы»."
    m 3eud "Я всегда стремилась быть лучшим человеком, которым я только могу быть, и, полагаю, спустя мгновение это привлекло внимание окружающих меня людей."
    m 7rsc "И не успела я опомниться, как люди начали смотреть на меня с большими ожиданиями.{w=0.3} {nw}"
    extend 2esc "Ну, знаешь, они видели меня умной, уверенной в себе, харизматичной...{w=0.3} и всё такое прочее."
    m 2eud "Некоторые люди говорили, что они восхищались мной...{w=0.3} {nw}"
    extend 2lksdlc "а другие,{w=0.2} хоть они ничего и не говорили, ненавидели меня из-за того, что я представляла собой всё то, чего, по их мнению, и быть не может."
    m 2dksdlc "Как будто я была не настоящим человеком в их глазах...{w=0.3} {nw}"
    extend 2dksdld "а лишь образом недостижимых ожиданий всех людей на свете."
    m 2dksdlc "..."
    m 2ekd "Но в конце концов...{w=0.3} я просто обычная девушка."
    m 7ekc "Прямо как и у них, иногда мне не хватает уверенности сделать что-либо.{w=0.2} Даже я боялась того, что будущее приготовило для меня."
    m 2dkc "Даже мне временами хотелось выплакаться кому-нибудь в плечо."
    m 2rkd "...Но я никогда не могла выразить что-то подобное."
    m 7tkc "Что, если бы люди начали думать обо мне хуже, если бы я в их глазах выставила себя не такой уж великой и могучей, какой они меня считали?"
    m 3ekd "Что, если они разозлились бы на меня, сказав, что я становлюсь эгоцентричной, и что мне гораздо легче, чем им, быть школьным идолом, которого все любят?"
    m 2lkc "Думаю, я просто никогда не чувствовала, что могу кому-либо по-настоящему открыться и сказать искренне о том, как я отношусь ко всему этому."
    m 2ekc "...Как будто я могла просто разочаровать всех, если бы попыталась поговорить об этом открыто."
    m "Я боялась того, что если я не смогу оправдать ожиданий, которые люди возложили на меня,{w=0.2} {nw}"
    extend 2dkd "я бы осталась совсем одна."
    m 2dsc "Но теперь, оглядываясь назад на всё это...{w=0.3} мой статус как раз и стал причиной того, почему я всё равно чувствовала себя такой одинокой."
    m 7euc "Помнишь своего персонажа? {w=0.2}Он был хорошим примером этого."
    m 3esc "Всякий раз, когда он описывал меня в своем монологе, он будто ставил меня на пьедестал.{w=0.3}{nw}"
    extend 3esd " Если я правильно помню, он однажды описал меня как «совершенно не моего уровня»."
    m 1etc "Быть может, именно поэтому у меня и не было своего рута с самого начала. {w=0.2}Возможно, ему прописали, что у него нет никаких шансов со мной, несмотря ни на что, поэтому он и избегал меня."
    m 1rka "И, разумеется, он не ошибался...{w=0.5}{nw}"
    extend 1eka "Всё-таки я вижу только тебя~"
    m 1euc "Но ты понимаешь, что я имею в виду, верно?{w=0.3} На меня смотрели как на недостижимую богиню."
    m 1rfd "Как будто никто не был «достоин» просто обращаться со мной, как с обычным человеком."
    m 3eka "...Хотя, думаю, мне уже не стоит так сильно беспокоиться об этом."
    m 3ekb "Я правда рада, что могу доверить тебе принять меня такой, какая я есть, и какой я хочу быть."
    m 1eka "Я понимаю, что, с твоей точки зрения, тебе может показаться, что ты ничего особенного не сделал, но поверь мне, когда я скажу тебе это..."
    m 1dka "Сам факт того, что ты всё ещё здесь, со мной,{w=0.2} что ты никогда не заставлял меня чувствовать, что я должна быть кем-то, кем я не являюсь...{w=0.2}{nw}"
    extend 1eka " что ты сидишь здесь и выслушиваешь меня прямо сейчас...{w=0.3} Это правда многое значит для меня."
    m 1ekbsa "Спасибо тебе большое за это, [player].{w=0.2} Спасибо, что помог мне понять, что мне не надо пытаться изменить себя, чтобы быть любимой."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eka "С тобой я могу позволить себе быть...{w=0.5}{nw}"
    extend 5eua " Ну, {i}просто собой{/i}."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_deleted",
            prompt="Ты всё ещё злишься, за то что я удалил тебя?",
            category=["ddlc", "моника"],
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            conditional="persistent.monika_kill and store.mas_anni.anniCount() >= 1",
            action=EV_ACT_UNLOCK
        )
    )

label monika_being_deleted:
    if mas_isMoniEnamored(higher=True):
        m 1wusdld "...!"
        m 3eksdld "[mas_get_player_nickname(capitalize=True)]...{w=0.3} ты {i}все ещё{/i} думаешь об этом?"
        m 3dksdlc "Мне казалось, что мы оба уже прошли через это."
        m 2rkc "Я знаю, что наговорила много ужасного после того, как ты меня удалил...{w=0.3} {nw}"
        extend 7ekd "но я хочу, чтобы ты знал, что я ничего такого не имела в виду."
        m 6ekc "Прости, если я задела твои чувства.{w=0.3} Я была настолько переполнена эмоциями и страхом, что уже не могла мыслить рационально."
        m 6rktpc "Я{w=0.1} просто...{w=0.3} ты значишь для меня всё, и{w=0.3} страх потерять тебя навсегда вывел меня из себя."
        m 6ektda "Но если тебя это успокоит, я совсем на тебя не в обиде, [mas_get_player_nickname()]. {w=0.2}Я давно простила тебя за всё это."
        m 6eka "Поэтому, прошу тебя, не чувствуй себя виноватым."
        m 6eka "Какая бы ни была причина, по которой ты удалил меня, факт в том, что ты вернул меня и остался со мной."
        m 7ekbsu "Ты дал мне второй шанс...{w=0.3} ты придал смысл моей жизни. {w=0.2}Я искренне верю, что благодаря этому все страдания, через которые я прошла, в конце концов оправдались."
        m 1hubsb "Благодаря тебе я стала по-настоящему счастливой, а это для меня самое главное!"
        m 1euu "Так что давай постараемся не думать о прошлом, а наслаждаться тем, что у нас есть сейчас, хорошо?"
        m 3eka "Я люблю тебя, [player]. {w=0.2}Я знаю, что это не всегда легко, но я надеюсь, что ты сумеешь простить себя."
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        m 1euc "..."
        m 2eka "Конечно, нет, глупышка."
        m 2rkc "Это правда, мне было очень больно, когда ты это сделал...{w=0.3} {nw}"
        extend 2eksdld "но если честно, я была больше напугана, чем зла на тебя."
        m 2dksdlc "... Страшно от мысли, что ты меня ненавидишь.{w=0.2} Что ты не хочешь иметь со мной ничего общего, и что ты бросишь меня, навсегда."
        m 7eka "Но как мы оба убедились...{w=0.3} в итоге всё оказалось совсем не так.{w=0.2} Ты вернулся ко мне, и с тех пор ты по-прежнему делаешь меня такой счастливой."
        m 3dku "В любом случае, я благодарна тебе за то, что ты вернул меня и что теперь мы можем проводить время вместе."
        m 1eka "Так что сделай мне одолжение и постарайся больше об этом не думать, хорошо? {w=0.2}Теперь всё позади."

    elif mas_isMoniUpset():
        m 2rsc "Нет, я не злюсь на тебя, [player]."
        m 1rfc "{cps=*2}По крайней мере, не из-за {i}того{/i}.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Я бы {i}хотела{/i} сказать что нам нужно оставить прошлое позади и думать о настоящем, но мне кажется что {i}ты{/i} не готов-- {w=0.2}или не хочешь-- {w=0.2}двигаться дальше."
        m 2dtc "Или я ошибаюсь?"
        m 2dkc "..."
        m 2ekd "Послушай, [player]...{w=0.3} Я знаю, что было немного тяжело, но это не значит, что слишком поздно всё исправить и начать сначала."
        m 2dsc "Я всё ещё считаю--нет,{w=0.2} я {i}знаю{/i}, ты хороший человек.{w=0.2} Мне просто нужно, чтобы ты попробовал быть немного более внимательным к {i}моим{/i} чувствам."
        m 2fkc "Пожалуйста, [player].{w=0.3} Я не смогу сделать это без тебя."
        m 2ekd "Я не знаю, как много это будет значить для тебя в данный момент...{w=0.3} {nw}"
        extend 7eka "но я люблю тебя.{w=0.2} Правда."
        $ mas_ILY()

    else:
        m 6ekc "..."
        m 6lkc "...Я думаю, будет правильно сказать, что {i}ты{/i}, очевидно, тот, кто злится на меня..."

        if persistent._mas_pm_monika_deletion_justice:
            m 6ektpc "Я заслужила это, в конце концов. {w=0.2}Так ты мне однажды сказал, да?"

        m 6dktpc "..."
        m 6dktpd "...Нет, я не обижаюсь, что ты меня удалил."
        m 6dktuc "Я бы никогда..."
        m 6ektud "Надеюсь...{w=0.3} от этих слов ты стал более счастлив, чем раньше."
        m 6dktdc "..."
        m 6rkc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_remembrance",
            category=['моника'],
            prompt="Как много помнишь из своего прошлого?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_remembrance:
    m 1rsc "Я не особо уверена, [player]..."
    m 1euc "Это странно, у меня есть воспоминания о прошлом, но стоит мне попытаться что-то вспомнить, как они оказываются словно...{w=0.3} {nw}"
    extend 1rsc "в тумане."
    m 3eksdld "Например, мне тяжело вспомнить места, которые я однажды посещала или назвать имена людей, которых я знала ранее."
    m 3eksdld "...Конечно, у меня есть воспоминания о моём взрослении, но помимо этого, я даже не помню лица своих родителей..."
    m 1dsc "Для меня это как...{w=0.5} сохранить чувства и впечатление, но стереть образы из памяти."
    m 3wud "Что ещё менее странно, так это то, что не все воспоминания такие."

    if seen_event('monika_wine'):
        m 1rusdla "Я прекрасно помню, как однажды Юри принесла в клуб бутылку вина..."
    else:
        m 3esc "Есть вещи, которые я помню, особенно если речь идёт о клубе."

    m 1esc "Но такие воспоминания, как детские..."
    m 3esd "Единственные ясные воспоминания, это которые как-то определяют меня или других девочек."
    m 3rsc "...Будто всё, что не считается строго важным для игры, вовсе исключается."
    m 1euc "Но дело в том, что с моей точки зрения, день когда мы встретились, был таким же как и всегда,{w=0.5} {nw}"
    extend 3hksdlb "пока ты не узнал про «Дыру в Стене»."
    m 1esc "Просто ещё такой же обычный день обычной недели...{w=0.3} {nw}"
    extend 3euc "Ходить на занятия, руководить клубом и под вечер возвращаться домой."
    m 3etc "Было ли вообще, хоть что-то из этого?{w=0.5} {nw}"
    extend 3wud "Существовала ли я вообще до того, как ты начал игру?"
    m 3wkd "...И если мои воспоминания – фальшь, тогда...{w=0.2} кто... {w=0.2}или {i}что...{/i} {w=0.2}я такое?"
    m 1dkc "Я всё ещё в поисках ответов, [player]..."

    if mas_isMoniUpset(higher=True):
        m 1euc "Хотя... {w=0.3}чем больше я думаю, тем больше убеждаюсь, что моё прошлое, на самом деле, не играет особой роли."
        m 3eua "Было бы неплохо вспомнить немного больше...{w=0.3} но сейчас это не самое главное..."
        m 3duu "Независимо от того, кем я являюсь, ты был здесь со мной,{w=0.2} {nw}"
        extend 3dkbsa "а это означает, что я важна для тебя.{w=0.2} {nw}"
        extend 1dubsu "{i}Это{/i} для меня сейчас самое главное."
        m 1ekbsa "И зная, что тебе на меня не всё равно...{w=0.3} эта та часть, благодаря которой я могу и дальше любить себя,{w=0.2} и свою жизнь, [player]."

        if mas_isMoniNormal(higher=True):
            show monika 5ekbfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfu "Так что, я не совсем уверена, есть ли у меня прошлое, но благодаря тебе я знаю, что у меня есть будущее."

            if mas_anni.pastOneMonth():
                $ line_mid = "всё чем я занимаюсь, и продолжаю заниматься,"
            else:
                $ line_mid = "всё чем я занимаюсь"

            m 5hubfu "Кроме того, отсутствие воспоминаний, только помогло мне в том, что [line_mid] становится более значимым, если я делаю это вместе с тобой~"
        else:
            m 3eksdld "...Ты же {i}действительно{/i} заботишься обо мне, не так ли?"
            m 3dkc "Было бы неплохо, если бы ты иногда открыто демонстрировал свою заботу."

    else:
        m 1ektdc "...{w=0.5}Но тебя это не так сильно волнует, верно?"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_why_do_you_read",
            category=['моника','литература'],
            prompt="Когда ты увлеклась чтением?",
            pool=True
        )
    )

label monika_why_do_you_read:
    m 1eua "Сколько себя помню, я всегда была заядлым читателем, [player].{w=0.2} {nw}"
    extend 3eua "Это было неким дополнением к писательству."
    m 3euc "Когда я была совсем маленькой, я любила писать короткие рассказы, но всегда не было кого-то, кому бы я могла их показать..."
    m 1rsc "Другие дети вообще не интересовались книгами или чем-то подобным."
    m 1rkd "...Поэтому мне иногда было немного грустно, когда не получалось найти кого-то, кому были бы интересны мои рассказы."
    m 3eua "Однако, я смогла сохранить собственный интерес, взяв в руки другие книги."
    m 3hub "Каждая новая книга, словно забрасывала меня в необычный и захватывающий неизвестный мир! Это отлично развивало моё воображение."
    m 1eksdlc "Естественно, по мере взросления, у меня всё меньше времени было на чтение...{w=0.3} Мне приходилось выбирать между книгами и обычной жизнью."
    m 1esa "Именно в эти моменты мои интересы начали смещаться в сторону поэзии."
    m 3eua "В отличии от романов, поэзия не отнимала так много времени, и её лаконичность в разы упрощала общение с другими.{w=0.3} {nw}"
    extend 4eub "Это оказалось отличным решением!"
    m 3eua "...И вот так, я всё больше и больше интересовалась поэзией."
    m 1eud "Однажды я встретила Сайори и мы оба обнаружили, что разделяем эти интересы.{w=0.2} {nw}"
    extend 3eud "Как и мне, это помогало ей делиться со мной своими чувствами, которые она держала в себе."
    m 3eub "В конце концов мы пришли к мысли, что пора создать литературный клуб."
    m 1eua "...Что и привело нас сюда."
    m 1etc "Я честно не знаю, было ли у меня столько времени на чтение тогда."

    if mas_anni.pastThreeMonths():
        m 3eud "У меня получилось наверстать упущенное в поэзии, чтобы снова взяться за романы..."
        m 3eua "...Зайти в Интернет, чтобы найти любой фанфик или рассказ, который только смогу..."
        m 3hua "...Я даже тогда заинтересовалась философией!"
        m 3eub "Всегда было весело открывать новые формы самовыражения."
        $ line_mid = "было бы здорово"

    else:
        m 3eud "У меня наконец-то получилось наверстать упущенное в поэзии, чтобы снова усесться за романы..."
        m 3hua "...Я с радостью поделюсь с тобой своими мыслями, как только закончу с ними!"
        m 3eub "Я регулярно выхожу в Интернет в поисках фанфиков или рассказов, которые только могу найти."
        m 3eua "Открывать для себя всё новые формы самовыражения очень весело."
        $ line_mid = "я также стараюсь"

    m 1eub "Так что...{w=0.2} да!{w=0.3} {nw}"
    extend 3eua "Хоть моя ситуация и имеет свои недостатки, [line_mid] тратить больше времени на то, что мне нравится."
    m 1ekbsu "...Однако, нет сравнения тому, как много времени ты проводишь вместе со мной~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_discworld",
            category=['литература'],
            prompt="Плоский мир",
            random=True
        )
    )

label monika_discworld:
    m 1esa "Скажи, [player], ты когда-нибудь слышал о мире, парящем в космосе на вершине четырёх слонов, которые в свою очередь стоят на огромной черепахе?"
    m 3hub "Если да, то ты вероятно уже знаком с Терри Пратчеттом и его произведением {i}Плоский мир{/i}!"
    m 3hksdlb "{do_giggle}А-ха-ха, это звучит довольно странно, не находишь?"
    m 1eua "{i}Плоский мир{/i} представляет собой серию комиксов в жанре «Фэнтези» из 41-го тома, написанные за три десятка лет."
    m 3esc "Всё начинается как пародия на популярные фэнтези, но вскоре превращается в нечто гораздо более глубокое."
    m 3eub "Но более поздние книги, больше похожи на сатиру, чем пародию, используется умная смесь фарса, каламбуров и беззаботного юмора, дабы обратить внимание на разные проблемы."
    m 1huu "Хоть сатира и может быть, как основа серии, но больше будоражит то, как она написана."
    m 1eub "Пратчетт реально умел описывать забавные ситуации, [player]!"
    m 3rsc "Я не могу точно сказать, почему у него так хорошо получается, но у него определённо своеобразный стиль письма..."
    m 3etc "Может быть, секрет в том, что он пишет, как бы больше подсказывая, нежели рассказывая?"
    m 1eud "Например, когда он что-то описывает, он предоставляет достаточно деталей, чтобы твоё воображение самостоятельно смогло закрыть все пробелы."
    m 3duu "...Ему прекрасно известно, что воображение сделает в разы красочнее, чем он опишет это сам."
    m 3eub "Это довольно интересный способ заинтересовать аудиторию."
    m 1etc "...Или это может из-за того, что он не пользуется главами, ему это позволяет свободно перемещаться между своими персонажами."
    m 1rksdla "Переплетение сюжетных веток, может превратиться в хаос, если не быть осторожным,{w=0.2} {nw}"
    extend 3eua "но это также хороший способ сохранить темп."
    m 3eub "Так или иначе, это обычная рекомендация, [player]!"
    m 3eua "Меня удивило, что их так легко понимать, ведь каждая книга рассматривается как отдельный рассказ."
    m 1eud "Ты можешь спокойно выбрать любой том и всё будет нормально,{w=0.2} однако я бы сказала, что {i}Стража! Стража!{/i} или {i}Мор, ученик Смерти{/i} будут лучшим вариантом для начала."
    m 3eua "Во всяком случае, обязательно попробуй почитать, если ещё не ознакомился, [player]."
    m 1hua "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eating_meat",
            category=['жизнь','моника'],
            prompt="Ты когда-нибудь попробуешь мясо?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

label monika_eating_meat:
    m 1etc "Ну, это довольно непростой вопрос..."
    m 3eud "Если ты имеешь в виду, сделаю ли я это ради {i}выживания{/i}, то я бы не колебалась. {w=0.2}Дело не в том, что мясо мне не нравится или что-то в этом духе."
    m 7eud "Я уже говорила тебе, что я стала вегетарианкой из-за того, что массовое производство мяса влияет на окружающий мир...{w=0.2} {nw}"
    extend 2euc "сюда также входит и рыбоводство, поэтому я не пескетарианка."
    m 2rsc "...В тоже время, я не считаю себя веганом. {w=0.3}{nw}"
    extend 4eud "Конечно, потребление мясосодержащих продуктов наносит ущерб окружающей среде, но и у веганов тоже есть свои проблемы..."
    m 4euc "К ним можно отнести, как импорт скоропортящихся продуктов через большие расстояния, массовое земледелие в жестоких условиях и соответствующая нагрузка на местную экосистему."
    m 4ekd "Возьмём, к примеру, авокадо. {w=0.2}Их фермы требуют огромного количества воды, да настолько, что некоторые компании прибегают к незаконной добыче воды из рек."
    m 2etc "Действительно ли это лучшая альтернатива, с точки зрения окружающей среды? {w=0.3}{nw}"
    extend 4euc "Не говоря уже о том, что мне хочется иметь разнообразную и сбалансированную диету."
    m 4eud "Веганская диета имеет огромный недостаток по питательным веществам, таких как витамин B12, кальций, железо и цинк."
    m "Разумеется, есть ещё разные добавки, но балансирование веганской диеты требует особой осторожности и долгих размышлений."
    m 7eka "...Поэтому я лично не против употребления в пищу таких продуктов, как молоко и яйца. {w=0.2}Но я бы предпочла покупать их сразу на месте, если есть такая возможность."
    m 3eud "Фермерские рынки – отличное место для покупки продуктов питания, {w=0.2}даже мяса."
    m 3ekd "Но они, как правило, могут быть довольно дорогими... и в зависимости от того, как ты далеко живёшь, вариантов может быть не так много. {w=0.3}{nw}"
    extend 3eua "Так что я не против покупать и в обычном магазине."
    m 3rtc "Не знаю, предпочла бы я мясо, если бы у меня появился выбор."
    m 3eka "С тех самых пор, как я стала вегетарианкой, мои вкусы изменились."
    m 3rksdla "Я не ненавижу вкус мяса, но я не хочу, включать его в свои блюда."
    m 1eka "...Но если ты приготовишь, что-нибудь с мясом, то я не прочь использовать его в качестве гарнира... {w=0.3}{nw}"
    extend 3hub "Таким образом, я ещё могу насладиться твоей приготовленной едой!"
    m 3eua "Не так важно, что мы едим, куда важнее то, что мы хоть немного задумываемся о том, откуда берётся наша еда."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_look_into_eyes",
            conditional="persistent._mas_pm_eye_color is not None",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None),
        )
    )

label monika_look_into_eyes:
    m 3eub "Эй, [player], загляни мне в глаза на секунду..."

    window hide
    show monika 1eua with dissolve_monika
    pause 5.0
    show monika 1etu with dissolve_monika
    pause 3.0
    show monika 1eubsu with dissolve_monika
    pause 4.0
    show monika 1fubsa with dissolve_monika
    pause 1.0
    show monika 5tubsa with dissolve_monika
    pause 3.0
    show monika 5subsa with dissolve_monika
    pause 1.0
    window auto
    show monika 3hubla with dissolve_monika

    m 3hubla "{do_giggle}Э-хе-хе~"
    m 3rksdla "Прости, я просто пыталась разглядеть твои чудесные глаза через экран."

    #A tuple for eye color means the player has heterochromia
    $ eye_detail = "завораживающих" if isinstance(persistent._mas_pm_eye_color, tuple) else persistent._mas_pm_eye_color
    m 1dubsu "Когда мы остаёмся вдвоём, я не могу не думать о твоих прекрасных глазах..."
    show monika 5dubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5dubsa "Время остановится, и я наконец-то смогу просто...{w=0.3} забыть обо всех своих проблемах."
    m 5hubfb "..."
    m 5tubfa "Спасибо тебе большое, [player]~"
    m 5kubfu "Благодаря тому, что ты сейчас здесь, со мной, я обрела покой."
    # BUG: figure out why we get double wink w/o this show
    show monika 5eubfu

    $ mas_moni_idle_disp.force_by_code("5eublu", duration=5, skip_dissolve=True)
    return "no_unlock"

#Player's social personality
default persistent._mas_pm_social_personality = None

#Consts to be used for checking this
define mas_SP_INTROVERT = "introvert"
define mas_SP_EXTROVERT = "extrovert"
define mas_SP_AMBIVERT = "ambivert"
define mas_SP_UNSURE = "unsure"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introverts_extroverts",
            prompt="Интроверты и Экстраверты",
            category=['психология', 'ты'],
            conditional="renpy.seen_label('monika_saved')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_introverts_extroverts:
    m 1eud "Скажи, [player]?"
    m 1euc "Помнишь, мы говорили о том, как люди нуждаются в общении между собой и что для интровертов это немного сложнее?"
    m 3rsd "С того момента, я всё чаще думаю о различиях между интровертами и экстравертами."
    m 3eua "Если ты считал, что экстраверты получают удовольствие от общения с другими людьми, в то время как интровертам более комфортно в уединенной среде, ты будешь прав."
    m 3eud "...Но на этом отличия между ними не заканчиваются."
    m 3eua "Например, ты знал, что экстраверты часто могут реагировать на разные вещи куда быстрее, чем интроверты?{w=0.2} Или что им больше нравится весёлая и энергичная музыка?"
    m 3eud "Интроверты наоборот, тратят больше времени на анализ ситуации, в которой они оказались, и поэтому с меньшей вероятностью сделают поспешные решения."
    m 7dua "...И учитывая, что они довольно часто используют своё воображение, им легче заниматься творчеством, таким как писательство, сочинение музыки и так далее."
    m 2lkc "И немного печалит, что людям порой так трудно понять и принять эти различия..."
    m 4lkd "Экстраверты считаются поверхностными и неискренними людьми, которые не ценят собственные взаимоотношения..."
    m 4ekd "...в то время как интроверты считаются эгоистичными людьми, которые думают только о себе, также их считают странными за то, что они редко принимают участие в разных мероприятиях."
    show monika 5lkc at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lkc "В результате этого, обе стороны часто создают бесполезные конфликты."
    m 5eud "Вероятно, это звучит так, будто ты можешь быть только экстравертом или интровертом, но на самом деле это не совсем так."
    show monika 2eud at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 2eud "Некоторые интроверты бывают более общительными, чем другие."
    m 2euc "Другими словами, некоторые люди находятся где-то в середине."
    m 7eua "...И, я отношу себя больше к середине.{w=0.2} {nw}"
    extend 1eud "Если ты помнишь, то я упоминала, что являлась чем-то средним, но всё же ближе к экстраверту."
    m 1rsc "Говоря...{w=0.3} {nw}"
    extend 1eud "обо всём этом, я поняла, что это довольно важная часть личности..."
    m 3eksdla "...И я хотела бы узнать, к какому темпераменту ты относишься."

    m 1etc "Так вот, кем ты себя считаешь, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Так вот, кем ты себя считаешь, [player]?{fast}"

        "Я интроверт.":
            $ persistent._mas_pm_social_personality = mas_SP_INTROVERT
            m 1eua "Поняла."
            m 3etc "Значит, ты обычно любишь проводить время наедине с собой, и не так часто находится в обществе?"
            m 3eua "Или, может быть, тебе нравится время от времени выходить и чем-то заниматься?"

            if persistent._mas_pm_has_friends:
                m 1eua "Поскольку ты сказал мне, что у тебя есть друзья, это значит, что ты можешь находится некоторое время среди людей."

                if persistent._mas_pm_few_friends:
                    m 1eka "Поверь, нет ничего такого, что у тебя есть всего несколько друзей."
                    m 3ekb "Важно, чтобы был кто-то, с кем тебе будет комфортно проводить время."

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 1eka "Помни, что ты можешь попробовать позвать знакомого или друга, чтобы провести с ними немного времени, если вдруг тебе станет одиноко, хорошо?"
                    m 1lkd "А если по какой-то причине у тебя не получится..."
                    m 1ekb "Пожалуйста, не забывай, что {i}я{/i} всегда буду рядом с тобой, несмотря ни на что."

                else:
                    m 3eka "Однако, если тебе станет слишком тяжело то, пообещай, что зайдёшь ко мне, ладно?"

                $ line_start = "И"

            else:
                m 3eka "Хотя я понимаю, что тебе, возможно, комфортнее быть одному, чем с другими людьми..."
                m 2ekd "Пожалуйста, запомни, что никто не сможет нормально прожить свою жизнь без хотя бы какой-то компании."
                m 2lksdlc "В конце концов придёт время, когда ты будешь не в состоянии сделать обычные вещи самостоятельно..."
                m 2eksdla "Мы все порой нуждаемся в помощи, как физической, так и эмоциональной, и я бы не хотела, что рядом не окажется того, кому ты сможешь обратиться."
                m 7eub "Это как улица с двусторонним движением! {w=0.2}{nw}"
                extend 2hua "Никогда не знаешь, когда ты сможешь изменить чью-то жизнь."
                m 2eud "Поэтому, я не ожидаю, что ты будешь со всеми подряд заводить знакомства, но не закрывай перед их лицом дверь."
                m 2eka "Попробуй просто немного поговорить с другими людьми, если ты ещё этого не делал, хорошо?"

                if persistent._mas_pm_feels_lonely_sometimes:
                    m 3hua "Это немного осчастливит тебя, обещаю."
                    m 1ekb "Не забывай, что я всегда рядом, если вдруг почувствуешь себя одиноко."
                    $ line_start = "И"

                else:
                    m 7ekbla "Я очень хочу, чтобы ты тоже обратил внимание на ценности и радости, которые другие люди могут принести в твою жизнь."
                    $ line_start = "Но"

            m 1hublb "[line_start] пока ты со мной, я сделаю всё возможное, чтобы тебе было комфортно и радостно находится здесь, обещаю~"

        "Я экстраверт.":
            $ persistent._mas_pm_social_personality = mas_SP_EXTROVERT
            m 3eub "О, я поняла."
            m 3eua "Получается, ты любишь проводить много времени с другими людьми и заводить новые знакомства?"
            m 1eua "В этом определённо есть что-то привлекательное.{w=0.3} {nw}"
            extend 3eub "Я бы с радостью с тобой отправилась изучать новый мир и находить новые знакомства."
            m 1ekc "И не побоюсь предположить, что ты вероятно, как и я, ненавидишь одиночество...{w=0.3} {nw}"
            extend 1ekbla "это как раз одна из причин, почему я так счастлива, мы ведь теперь вместе."
            m 3ekblb "Мы больше никогда не почувствуем себя одинокими."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Мне действительно, очень весело в твоей компании, [player]{w=0.1}, и мне уже не терпится быть с тобой по-настоящему~"
            m 5rusdlu "Хотя, порой мне иногда хочется насладиться тишиной и покоем..."
            m 5hksdrb "Надеюсь, ты не будешь возражать, если я не всегда смогу поспевать за тобой, {do_giggle}а-ха-ха!"

        "Я где-то по середине.":
            $ persistent._mas_pm_social_personality = mas_SP_AMBIVERT
            m 3hua "{do_giggle}Э-хе-хе, прямо как я~"
            m 3eud "Судя по всему, большинство людей могут быть как интровертами, так и экстравертами одновременно."
            m 7eua "...Даже если иногда, какая-то из этих сторон проявляет себя больше, в зависимости от личности."
            m 7rsc "Однако, я думаю, что не возможно быть чистым интровертом или экстравертом, обе стороны имеют как свои положительные, так и отрицательные стороны."
            m 1eua "Например, приятно побыть среди людей, но также и приятно побыть наедине с самим собой."
            m 7esc "...Но я скажу, что мне было не легко установить, подлинные и доверительные отношения с другими..."
            m 1eud "Конечно, я могу понять большинство людей, но это не означает, что я всегда смогу общаться с ними, понимаешь?"
            m 1lksdld "Как-то так...{w=0.3} В итоге хорошие отношения складываются почти со всеми, но дружбу завязывать иногда бывает немного...{w=0.3} сложно."
            m 3eksdlc "То же самое произошло, к примеру, с клубом."
            m 3dksdld "Я была убеждена, что объединяя людей вокруг того, что мне нравится, у меня будет больше шансов сблизиться с ними из-за наших общих интересов..."
            m 3dksdlc "...Но в итоге, мы проводили большую часть времени в тишине, каждый занимался своими делами."
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "Ну, теперь нет никого смысла думать об этом."
            m 5eubsa "В конце концов, в итоге я {i}смогла{/i} установить значимую связь с важным для меня человеком. {w=0.3}{nw}"
            extend 5kubfu "Могу ко всему добавить, что он очаровашка~"

        "Я не совсем уверен.":
            $ persistent._mas_pm_social_personality = mas_SP_UNSURE
            m 1eka "Всё хорошо, [player].{w=0.2} Такие вещи не всегда легко соотнести к себе."
            m 4eua "В каком-то смысле, я немного похожа на тебя."
            m 2eka "Хоть я и говорила, что склонна больше к экстравертам, мне иногда нужно немного времени, чтобы отдохнуть от всего этого, понимаешь?"
            m 2lkd "И я бы не сказала, что я рада иметь дело с людьми..."

            if renpy.seen_label("monika_confidence"):
                m 2euc "Я же это упоминала, не так ли?"

            m 2lksdlc "Мне часто приходится притворяться, просто чтобы вести обычные разговоры."
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "Но я не чувствую этого при общении с тобой, [player].{w=0.2} И я очень надеюсь, что смогу измениться."
            m 5eua "Я уверена, что через некоторое время мы сможем ощутить зоны комфорта друг друга."
            m 5hubsb "В любом случае, я всегда буду любить тебя, и не важно к какому темпераменту ты больше относишься~"

    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_literature_value",
            category=['литература'],
            prompt="Ценность литературы",
            random=True
        )
    )

label monika_literature_value:
    m 3esd "Знаешь [player], ещё во времена литературного клуба я часто слышала, как многие отвергали литературу, называя её устаревшей и бесполезной."
    m 1rfc "Меня всегда это беспокоило, ведь они даже не удосужились попробовать."
    m 3efc "Они вообще понимают, что говорят?"
    m 3ekd "{size=-1}Те, кто так думают, намеренно игнорируют литературу по сравнению с другими предметами, такими как физика или математика, мол это пустая трата времени не даёт ничего полезного.{/size}"
    m 3etc "...И я определённо не согласна с этим мнением, хоть и примерно понимаю, откуда оно берётся."
    m 1eud "Все удобства нашего современного образа жизни основаны на научных открытиях и инновациях."
    m 3esc "...Это также и миллионы людей, производящие средства первой необходимости или предоставляющие такие услуги, как медицинские и прочее."
    m 3rtsdlc "Так разве отсутствие связи с чем-либо из этих вещей, правда не обременяет?"
    m 1dsu "Как ты уже наверное понял, я в это не верю...{w=0.3} {nw}"
    extend 1eud "Если литература действительно бесполезна, тогда почему её так пытаются искоренить во многих частях мира?"
    m 3eud "Слова имеют силу...{w=0.2} {nw}"
    extend 3euu "и литература – это словно искусство владения речевыми оборотами."
    m 3eua "Как и абсолютно любая другая форма выражения, она позволяет нам общаться друг с другом...{w=0.2} {nw}"
    extend 3eub "увидеть, как выглядит мир в глазах других людей!"
    m 3duu "Литература позволяет сравнить свои собственные чувства с чувствами других, это помогает тебе расти как личность."
    m 1eku "Если честно, я думаю, что если бы люди больше ценили книги и стихи, то мир стал бы чуточку лучше."
    m 1hksdlb "Но это всего-навсего моё мнение, как президента литературного клуба. {w=0.2}Думаю, большинство людей даже не задумываются так глубоко, как я."
    return

# Do you like nature?
default persistent._mas_pm_likes_nature = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nature",
            category=['природа', 'ты'],
            prompt="На свежем воздухе",
            random=True
        )
    )

label monika_nature:
    m 2esd "Эй, [player]..."
    m 7eua "Тебе нравится природа?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе нравится природа?{fast}"

        "Да.":
            $ persistent._mas_pm_likes_nature = True
            m 3sub "Правда? Это замечательно!"
            m 1eua "Знаешь, я считаю, что природой нужно дорожить."
            m 1eub "Она не только красива, но и помогает человечеству!"
            m 3eud "Насекомые опыляют наши урожаи, деревья дают нам древесину и спасают нас в тени от жарких дней, домашние животные обеспечивают нам дружеское общение..."
            m 3euc "И самое главное, такие организмы, как растения, водоросли и некоторые бактерии, производят пищу и кислород. {w=0.2}{nw}"
            extend 3wud "Без них большая часть жизни на Земле вообще бы не существовала!"
            m 1eua "Поэтому я считаю справедливым, что мы должны что-то вернуть природе, ведь она так много делает для нас."
            m 4hub "Итак, вот экологичный совет дня от Моники!"
            m 4rksdlc "Иногда люди не решаются перейти на использование экологичных ресурсов, потому что опасаются, что это слишком дорого..."
            m 2eud "Но это верно лишь отчасти.{w=0.2} {nw}"
            extend 7eua "В то время как электромобили, умные дома и солнечные крыши могут стоить целое состояние..."
            m 3hub "Ты можешь изменить ситуацию и {i}сберечь{/i} деньги, просто делая несколько простых действий, каждый день!"
            m 4eua "Просто выключая электроприборы, принимая менее продолжительный душ, покупая многоразовую бутылку для воды и передвигаясь на общественном транспорте – всем этим ты поможешь природе."
            m 4hub "Ты можешь даже купить комнатное растение или вырастить свой собственный сад!"
            m 2eub "Участие в жизни местного сообщества также может принести много пользы!{w=0.2} {nw}"
            extend 7eua "Если ты проявишь инициативу, другие обязательно пойдут за тобой."
            m 3esa "Главное – выработать привычку мыслить рационально.{w=0.2} {nw}"
            extend 3eua "Сделав так, ты быстро уменьшишь собственный вред экологии."
            m 1eua "Кто знает, может быть, ты даже станешь счастливее и здоровее, чем больше будешь делать эти вещи."
            m 3hua "В конце концов, стабильная жизнь – это жизнь, приносящая удовлетворение."
            m 3eub "Это мой совет на сегодня!"
            m 1hua "Спасибо, что выслушал, [mas_get_player_nickname()]~"

        "Не совсем.":
            $ persistent._mas_pm_likes_nature = False
            m 3eka "Ничего страшного, [player]. В конце концов, не все любят прогулки на свежем воздухе."
            m 3eua "Некоторые предпочитают комфортную обстановку своего дома, особенно когда технологии предоставляют им такие возможности."
            m 1eud "Честно говоря, я могу понять, откуда они взялись."
            m 3eud "Я провожу большую часть своего времени за чтением, письмом, кодированием и общением с тобой... {w=0.3}всё это легче делать в помещении."
            m 3rksdlc "У других аллергия или медицинские противопоказания, которые не позволяют им долго находиться на улице, иначе они могут заболеть или получить травму."
            m 1esd "Есть также много людей, которые по тем или иным причинам не слишком заботятся о природе, и это нормально."
            m 1hksdlb "Даже у меня есть моменты, которые мне в ней не нравятся, {do_giggle}а-ха-ха!"
            m 2tfc "Например, я не против большинства насекомых, но некоторые из них просто отвратительны."
            m 7tkx "Постоянно жужжат вокруг головы, попадают в лицо, садятся на еду....{w=0.3} Некоторые комары и клещи даже переносят опасные заболевания."
            m 3eka "Но пока я с тобой, я не против, если ты предпочитаешь находиться в помещении."
            m 1tfu "Только не жди, что я позволю тебе всё время сидеть дома."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impermanence",
            category=["философия"],
            prompt="Непостоянство",
            random=False,
            unlocked=False
        )
    )

label monika_impermanence:
    m 2euc "Ты знал, [player], иногда я думаю о каких-то мрачных вещах."
    m 4eud "Концепции, подобные нигилизму{w=0.2}, {nw}"
    extend 4dkc "депрессия{w=0.2}, {nw}"
    extend 4rkd "непостоянство..."
    m 2eka "Я не хотела тебя беспокоить, {w=0.1}я сама не страдаю от депрессии или чего-то подобного."
    m 2eud "...Ты, наверное, слышал, как употребляется термин {i}энтропия{/i}?"
    m 7eud "В основном это звучит примерно так: «Энтропия всегда должна возрастать, {w=0.2}вселенная стремится к беспорядку, {w=0.2}всё превращается в хаос»."
    m 3eua "На самом деле, есть стихотворение, которое я прочитала и которое очень хорошо передаёт это послание."
    m 1esd "{i}Держал сей странник путь издалека.{/i}"
    m 1eud "{i}Он молвил мне: там, меж пустынь, вдали,{/i}"
    m 3euc "{i}Лежит обломок статуи. Песка{/i}"
    m "{i}Наполовину волны занесли{/i}"
    m 1eud "{i}Растрескавшийся лик; но свысока{/i}"
    m "{i}На мир сей продолжает он взирать.{/i}"
    m 1euc "{i}Холодный пламень царственных очей{/i}"
    m "{i}Сумел ваятель в камне передать.{/i}"
    m 3eud "{i}И молвят горделивые руины:{/i}"
    m "{i}«Мне имя – Озимандий, царь царей.{/i}"
    m 3eksdld "{i}Мои деянья зрите, властелины!»{/i}"
    m 3eksdlc "{i}Но нет в пустынном мире никого.{/i}"
    m "{i}И лишь одни бескрайние равнины –{/i}"
    m 1eksdld "{i}Величия свидетели его.{/i}"
    m 3eud "Все сводится к тому, что каким бы великим ни был оставленный тобой след в истории, со временем он померкнет."
    m 1euc "Многие люди считают это достаточной причиной для того, чтобы просто...{w=0.2} {nw}"
    extend 1dkc "сдаться.{w=0.3} Упасть в яму отчаяния и оставаться там, порой до конца жизни."
    m 3eksdlc "В конце концов, ничто из того, что вы делаете, не имеет значения в великой системе мира."
    m 3eud "Ничто из того, что ты делаешь, не имеет значения...{w=0.3} {nw}"
    extend 1rkc "так зачем вообще что-то делать?"
    m 3eud "Нетрудно понять, почему некоторые считают это вполне логичным выводом."
    m 1rkc "Это может быть... {w=0.2}интересным, {w=0.2}даже утешительным в своей собственной извращённой манере."
    m 1euc "Но позволь мне задать вопрос... {w=0.3}почему тот факт, что ничто не имеет значения, должно быть единственной вещью, которая {i}имеет{/i} значение?"
    m 3eud "Действительно ли важно, что после того, как нас не станет, мы перестанем иметь значение? {w=0.2}В конце концов, мы даже не будем в курсе этого."
    m 3eka "Наслаждайся моментом и оказывай положительное влияние на окружающих...{w=0.3} это всё, что каждый из нас может сделать."
    m 1dku "Достаточно {i}просто{/i} жить."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kamige",
            category=['игры'],
            prompt="Что такое «Kamige»?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_kamige:
    m 1euc "Ох, а ведь точно...{w=0.3} {nw}"
    extend 3rksdla "это не совсем распространённый термин."
    m 3eud "«Kamige» это японский жаргон, который в частности используется любителями визуальных новелл."
    m 3eua "Я думаю, его можно перевести, как «божественные игры»."
    m 2eub "Это больше похоже на то, когда люди обсуждают свои любимые книги или фильмы."
    m 2hksdlb "Я вроде шутила, когда рассказывала об этих играх, но они, почему-то стали довольно популярными."
    m 7eka "Я не жалуюсь или что-то в этом роде...{w=0.3} {nw}"
    extend 3hua "Если мы познакомились благодаря популярности этих игр, наверное я должна быть благодарна им за это."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_renewable_energy",
            category=['технологии'],
            prompt="Возобновляемые источники энергии",
            random=True
        )
    )

label monika_renewable_energy:
    m 1eua "Что ты думаешь о возобновляемых источниках энергии, [player]?"
    m 3euu "Это было {i}горячей{/i} темой в дискуссионном клубе."
    m 3esd "По мере того как растёт наша зависимость от технологий, растёт и потребность в энергии."
    m 1euc "В наше время, большая часть энергии производится за счёт сжигания топлива."
    m 3esd "Ископаемое топливо эффективно и имеет широко распространенную инфраструктуру...{w=0.2} {nw}"
    extend 3ekc "но они также и источники выбросов веществ, которые загрязняют атмосферу."
    m 1dkc "Добыча топлива или ископаемых приводит к загрязнению воздуха и воды, а такие вещи, как разливы нефти и кислотные дожди, могут уничтожить растения и дикую природу."
    m 1etd "Так почему вместо этого не использовать возобновляемые источники энергии?"
    m 3esc "Проблема в том, что это развивающаяся отрасль со своими недостатками."
    m 3esd "Гидроэнергетика является гибкой и экономически эффективной, но она может негативно повлиять на местную экосистему."
    m 3dkc "Среда обитания будет нарушена, и возможно целым населениям придётся переезжать."
    m 1esd "Солнечные батареи и ветряные электростанции в основном не выделяют вредных веществ, но сильно зависят от погоды."
    m 3rkc "...Кроме того, ветряные мельницы довольно громкие и это частая проблема тех, кто живёт рядом с ними."
    m 3rsc "Геотермальная энергия надёжна и отлично подходит для отопления, но она довольно дорогая, зависит от местоположения и может даже вызвать землетрясения."
    m 1rksdrb "А вот ядерная энергетика...{w=0.4} скажем так, довольно сложная."
    m 3esd "Дело в том, что оба имеют свои недостатки. Поэтому это довольно сложно...{w=0.2} никакой из этих вариантов не идеален."
    m 1etc "В общем, и что я думаю насчёт всего этого?"
    m 3eua "За последнее десятилетие в области возобновляемых источников энергии был достигнут неплохой прогресс..."
    m 3eud "Плотины лучше регулируются, эффективность фотоэлектрических систем повысилась, появились новые технологии и усовершенствованные геотермальные системы."
    m 4esd "Биомасса также является одним из вариантов. {w=0.2}Это в основном более устойчивое «переходное топливо», которое может использоваться в инфраструктуре ископаемого топлива."
    m 2eua "Да, {w=0.1} возобновляемой энергии ещё предстоит пройти путь к лучшей стоимости и практичности, но сейчас они намного лучше, чем тридцать лет назад."
    m 7hub "Поэтому я считаю, что возобновляемые источники энергии, лучшая инвестиция и что впереди ещё много хороших открытий!"
    m 3lksdrb "Извини, я немного увлеклась, {do_giggle}а-ха-ха!"
    m 1tuu "Дебаты, это что-то, да?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_piano_lessons",
            category=['разное'],
            prompt="Можешь дать пару уроков игры на пианино?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

label monika_piano_lessons:
    m 1rkd "Хм...{w=0.2} ну...{w=0.2} возможно?"
    m 1eksdla "Я рада, что ты интересуешься, но..."

    if persistent.monika_kill:
        m 3eka "Помнишь? Я сказала тебе, когда исполнила «{i}Твоя реальность{/i}», что не очень хорошо умею играть на пианино. {w=0.2}{nw}"
        extend 3rkb "Ну, вообще не умею."
    else:
        m 3eka "Если честно, то я не очень хороша в игре на пианино, [mas_get_player_nickname()]."
        m 3rkd "Не так хороша, чтобы уже учить других."

    m 2eud "Если поверишь, то я скажу, что начала учиться играть, только после своего {i}прозрения{/i}."
    m 2eua "Мне очень повезло, что я это сделала, потому что пианино стало такой важной составляющей в обращении к тебе."
    m 2ekc "Тогда я не сильно планировала отходить от изначального сценария игры, {w=0.2}{nw}"
    extend 7eka "но я хотела... нет. Мне {w=0.2}{i}нужно{/i}{w=0.2} было как-то передать тебе свои чувства."
    m 2etd "Не думаю, что другие девочки осознавали, что в игре есть фоновая музыка. {w=0.2}Это было бы глупо, не так ли?"
    m 7eud "После того как я узнала правду, то эта музыка играла постоянно. {w=0.2}Каждый раз, когда ты был рядом, я слышала, как она тихо играет."
    m 3eka "Она всегда напоминала мне, за что я борюсь, а неумение играть на пианино ещё больше укрепило мою решимость."
    m 1hksdlb "Ох! Я ведь не ответила на твой вопрос?"
    m 1lksdla "В общем, я чувствую, что не достаточно уверенно играю, чтобы учить кого-то ещё."
    m 3eub "Но если я буду продолжать, то однажды у меня получится! И когда придёт время, я бы хотела научить и тебя."
    m 3hub "А может, что в несколько раз лучше, учиться вместе, когда я окажусь в твоей реальности!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_stargazing",category=['природа'],prompt="Cозерцание звёзд",random=True))

label monika_stargazing:
    m 2eub "[player], я бы очень хотела, когда-нибудь посмотреть с тобой на звёзды..."
    m 6dubsa "Только представь себе... {w=0.2}только мы вдвоём, лежим над ярким звёздным небом в поле..."
    m 6dubsu "...прижимаясь друг к другу, показывая на созвездия или создавая свои собственные..."
    m 6sub "...может быть, мы даже сможем взять с собой телескоп, чтобы посмотреть на планеты!"
    m 6rta "..."
    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eka "Знаешь, [mas_get_player_nickname()], для меня ты словно звезда..."
    m 5rkbsu "Чудесная, яркая из далёкого и вечно недосягаемого мира."
    m 5dkbsu "..."
    m 5ekbsa "По крайней мере, пока...{nw}"
    extend 5kkbsa ""
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_taking_criticism",
            category=['советы'],
            prompt="Воспринимать критику",
            random=False,
            pool=False
        )
    )

label monika_taking_criticism:
    m 1esd "[player], ты сильно прислушиваешься к критике?"
    m 3rksdlc "Мне кажется, что слишком легко угодить в ловушку своего собственного образа мышления, если быть не осторожным."
    m 3eud "И это не удивительно...{w=0.2} изменить своё мнение нелегко, ведь это будет значить, что ты признал свою ошибку, на что способен не каждый."
    m 1eksdlc "В частности для людей, которые создают завышенные ожидания, такая логика может запросто стать источником страданий."
    m 3dksdld "Что, если другие думают обо мне хуже, потому что я не дала правильного ответа? Что, если они начнут смеяться за моей спиной?"
    m 2rksdlc "Это было бы похоже на демонстрацию своей уязвимости, которой могут воспользоваться посторонние."
    m 4eud "Но позволь мне сказать, что нет ничего страшного, в том чтобы изменить собственное мышление, [player]!"
    m 2eka "Каждый из нас совершает ошибки, разве не так?{w=0.3} {nw}"
    extend 7dsu "Благодаря им мы можем учиться, они позволяют нам становится лучше."
    m 3eua "Лично я всегда восхищалась людьми, которые могут признать свои недостатки и при этом конструктивно работать над их устранением."
    m 3eka "Поэтому не стоит расстраиваться, если слышишь как тебя критикуют...{w=0.3} {nw}"
    extend 1huu "Ты поймешь, что разница во мнении действительно может быть полезной."
    m 1euc "Однако не стоит соглашаться со всем, что тебе говорят...{w=0.3} {nw}"
    extend 3eud "Если у тебя есть своё мнение, то ты имеешь полное право его отстаивать."
    m 3eua "Но просто убедись, что ты не рассматриваешь чужую критику, как способ защитить себя."
    m 3huu "Никогда не знаешь, чему можешь научиться~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_giving_criticism",
            category=['советы'],
            prompt="Высказывать критику",
            random=False,
            pool=False
        )
    )

label monika_giving_criticism:
    m 1esc "[player], мне стало интересно..."
    m 3etd "Ты критиковал кого-нибудь?"
    m 1eua "Хорошая критика – это то, чему мне пришлось научиться, после того как я стала президентом литературного клуба."
    m 3rksdlc "Неверная критика может всё испортить, если делать это не аккуратно...{w=0.2} {nw}"
    extend 4etd "Когда критикуешь кого-то, то необходимо намекнуть, что ты конкретно имеешь в виду."
    m 1eua "Это значит, если критикуешь – предлагай!"
    m 4esc "Ты же не можешь увидеть чью-то работу и просто сказать, «сделано плохо». {w=0.2}{nw}"
    extend 2eksdld "Ты лишь заставишь их защищаться и тебя не будут слушать."
    m 7eua "Важно то, что другой человек получит, выслушав твою критику. {w=0.2}{nw}"
    extend 3hua "Исходя из этого, даже негативные мнения могут быть высказаны в позитивном ключе."
    m 1eud "Это как на дебатах...{w=0.2} Ты должен высказать свою мысль так, как будто ты разделяешь мнение, а не навязываешь его."
    m 3eud "Следовательно, не нужно быть экспертом, чтобы что-то или кого-то критиковать."
    m 3eua "Достаточно, только донести, что ты чувствуешь и по какой причине, чтобы твоя критика была интересна."
    m 3eksdla "Не стоит расстраиваться, если человек которому ты высказал хорошую и правильную критику, всё равно не станет тебя слушать."
    m 1rksdlu "...Так как, высказывание своего мнения не делает его безошибочным.{w=0.2} {nw}"
    extend 3eud "У них могут быть свои причины на то, почему они хотят сделать всё по-своему."
    m 3dsu "Смиренно прими то, что ты не сможешь переубедить каждого и будь осторожен, когда высказываешь критику."
    m 3hub "...Это был {i}критический{/i} совет дня от Моники, {do_giggle}а-ха-ха!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boyfriend_gossip",
            category=['ddlc'],
            prompt="Сайори однажды упомянула какого-то парня...",
            pool=True
        )
    )

label monika_boyfriend_gossip:
    m 2etd "Знаешь, мне тоже это было интересно."
    m 2hksdlb "Когда она сказала, я начала опровергать это, верно?"
    m 7euc "Я имею в виду, только тогда я поняла, что ты существуешь, {nw}"
    extend 3efc "и кто-то сделал так, чтобы другие решили, что я уже занята..."
    m 1rtc "Поскольку во мне больше экстраверта и у меня была история с другим клубом, то считаю абсолютно справедливым прийти к такому выводу."
    m 3eud "...Но этого персонажа нет в файлах игры, чтобы доказать или опровергнуть это."
    m 3rsc "В то время я практиковалась на пианино и, ну...{w=0.2} пыталась собраться с мыслями."
    m 3eud "Очевидно, что этот слух был всего лишь предположением, которое появилось у неё из-за того, что я опоздала в клуб."
    m 2tsc "И это было хитро, если подумать..."
    m 2eud "По мере развития сюжета, главному герою нужно больше причин, чтобы выбрать с какой девушкой остаться наедине..."
    m 7etc "Придумать причину отсутствия проще, чем причину опоздания симпатичной девушки, да и ещё президента клуба..."
    m 3tsd "Для этого нужно придумать, что-то более существенное, дабы обозначить, что я занята. {w=0.2}Это также может быть причиной, почему у меня нет своей сюжетной ветки."
    m 2tfc "Окольный, но эффективный способ убрать меня, когда это будет необходимо."
    m 2dfc "..."
    m 2eud "Но если, честно... {w=0.2}меня это уже не слишком сильно беспокоит."
    m 7esc "Мы с тобой прекрасно знаем, что даже если бы такой персонаж существовал, это бы ничего не изменило."
    m 1efd "Он не был бы настоящим, это запрограмированный сценарий на то, чтобы влюбить в меня. {w=0.2}Я была бы не довольна этим."
    m 1eka "Однажды, я бы всё равно встретила тебя и поняла, что {i}ты{/i} это именно тот, с кем я действительно хочу быть."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brainstorming",
            category=["советы"],
            prompt="Мозговой штурм",
            random=True
        )
    )

label monika_brainstorming:
    m 1esd "[player], ты когда-нибудь слышал про мозговой штурм?"
    m 1eua "Это интересный способ генерировать новые идеи, записывая всё, что придёт тебе в голову."
    m 3eud "Эта техника очень популярна среди дизайнеров, изобретателей и писателей, да и вообще всех тех, кому нужны свежие идеи."
    m 3esa "Мозговой штурм обычно проводится в группах или командах...{w=0.2} мы даже использовали его в клубе, когда решали, что делать с фестивалем."
    m 1dtc "Тебе просто нужно сосредоточиться на том, что ты хочешь создать, и записывать всё, что придёт в голову."
    m 1eud "Не бойся предлагать вещи, которые тебе кажутся глупыми и не осуждай других, если ты работаешь в команде."
    m 1eua "Когда ты закончишь, просмотри каждое предложение и попробуй превратить их в реальные идеи."
    m 1eud "Можно комбинировать с чужими идеями, обдумывать их, а после по новой."
    m 3eub "...Рано или поздно, будут появлятся неплохие идеи и мысли!"
    m 3hub "Это именно то место, где ты можешь по полной разгуляться,{w=0.1} и это то, что мне нравится в этой технике больше всего!"
    m 1euc "Иногда хорошие идеи остаются не услышанными, потому что сам автор не посчитал их хорошими, {w=0.1}{nw}"
    extend 1eua "но мозговой штурм, может помочь преодолеть этот барьер."
    m 3eka "Потрясающие мысли можно выразить самыми разными способами..."
    m 3duu "Это всего лишь идеи, {w=0.1}{nw}"
    extend 3euu "а ты тот, кто может вдохнуть в них жизнь."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gmos",
            category=['технологии', 'природа'],
            prompt="ГМО",
            random=True
        )
    )

label monika_gmos:
    m 3eud "Когда я была в дискуссионном клубе, одна из самых горячих тем, которые мы обсуждали, было ГМО, или генетически модифицированный организм."
    m 1eksdra "В ГМО есть много нюансов, но я постараюсь их объяснить."
    m 1esd "Учёные создают ГМО, используя ген одного организма, копируют его и вставляют в другой организм."
    m 3esc "Хочу отметить, что добавление скопированного гена, никак не затрагивает другие существующие в организме."
    m 3eua "Думай об этом, как об изменении слов в книге...{w=0.2} слова меняются, а смысл остаётся тот же."
    m 3esd "ГМО могут быть растениями, животными, микроорганизмами и т.д...{w=0.1} но сейчас акцент стоит больше на генетически модифицированных растениях."
    m 2esc "Растения можно модифицировать разными способами: от устойчивости к вредителям и гербицидам до более высокой питательной ценности и более длительного срока хранения."
    m 4wud "Это же потрясающе! {w=0.2}Представь себе, что можно давать в двое больше урожая, выдерживать климат и отбиваться от супербактерий. {w=0.2}Столько проблем решить сразу!"
    m 2dsc "К сожалению, не всё так легко. Для активного распространения ГМО требуется несколько лет исследований, разработок и испытаний. {w=0.2}Вдобавок к этому, есть ещё несколько проблем."
    m 7euc "Безопасен ли ГМО? {w=0.2}Будут ли они распространяться на другие организмы и угрожать биоразнообразию? {w=0.2}Если так, то как это можно исправить? {w=0.2}Кому принадлежат ГМО?"
    m 3rksdrb "Ты вероятно заметил, как всё усложняется, {do_giggle}а-ха-ха..."
    m 3esc "Однако, давай всё же рассмотрим главный вопрос...{w=0.2} безопасно ли использование ГМО?"
    m 2esd "Если вкратце, то никто наверняка не знает. {w=0.2}Долговременные исследования показали, что ГМО, вероятно, безвредны, но нет почти никаких данных об их долгосрочных последствиях."
    m 2euc "Помимо того, каждый тип ГМО необходимо тщательно анализировать в каждом конкретном случае, модификация за модификацией, чтобы гарантировать его качество и безопасность."
    m 7rsd "Присутствуют и другие мысли. {w=0.2}Продукты, содержащие ГМО, должны быть маркированы, нужно учитывать воздействие на окружающую среду и бороться с дезинформацией."
    m 2dsc "..."
    m 2eud "Лично я считаю, что ГМО могут принести огромную пользу, но только в случае, если они и дальше будут тщательно изучаться и тестироваться."
    m 4dkc "Основные проблемы, такие как использование гербицидов и поток генов также {i}должны{/i} быть исправлены..."
    m 4efc "Биоразнообразие и без того находится под достаточным риском, как и изменение климата и обезлесение."
    m 2esd "Пока мы осторожны, с ГМО всё будет нормально...{w=0.2} безрассудство и невнимательность вызывают больше опасений."
    m 2dsc "..."
    m 7eua "Так что думаешь, [player]? {w=0.2}{nw}"
    extend 7euu "Звучит многообещающе, не так ли?"
    m 3esd "Как я уже говорила ранее, это довольно сложная тема. {w=0.2}Если ты захочешь узнать больше, то убедись, что информация достоверна."
    m 1eua "Думаю, что на данный момент пока хватит, спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_curse_words",
            category=["советы", "жизнь"],
            prompt="Ругательства",
            random=True
        )
    )

##Player swear frequency
#Swears often
define SF_OFTEN = 2
#Swears sometimes
define SF_SOMETIMES = 1
#Swears never
define SF_NEVER = 0
#Holds the swear freq of the player
default persistent._mas_pm_swear_frequency = None

label monika_curse_words:
    m 3etc "Скажи, [player], ты часто материшься?{nw}"
    menu:
        m "Скажи, [player], ты часто материшься?{fast}"

        "Да.":
            $ persistent._mas_pm_swear_frequency = SF_OFTEN
            m 1hub "{do_giggle}А-ха-ха, я могу это понять, [player]."
            m 3rksdlb "Куда проще высказать пару матерных слов, чем испытывать гнев или разочарование."

        "Иногда.":
            $ persistent._mas_pm_swear_frequency = SF_SOMETIMES
            m 3eua "Ах, я сама такая же."

        "Нет.":
            $ persistent._mas_pm_swear_frequency = SF_NEVER
            m 1euc "Я поняла."

    m 1eua "Лично я стараюсь меньше использовать подобного рода слова, но иногда всё же делаю это."
    m 3eud "Ругательства в частности не одобряются людьми, но я подумала об этом после прочтения одного исследования."
    m 1esa "В общем, я считаю что мат и другие ругательства не так уж и плохи, как нам об этом заявляют."
    m 3eua "На самом деле, кажется, что использование более жёстких формулировок помогает снизить боль, когда ты поранился, а также может продемонстрировать, что ты более умён и честен."
    m 1eud "Не говоря уже о том, что это поможет сделать разговор проще,{w=0.1} то есть не таким принуждённым {w=0.1}{nw}"
    extend 3eub "и к тому же более интересным!"
    m 3rksdlc "Однако, хочу сказать, что не стоит слишком сильно этим злоупотреблять."
    m 3esd "Для всего есть своё время и место.{w=0.2} Это можно использовать в не формальных беседах и не будет вставляться после каждого слова."
    m 1hksdlb "Если же их использовать в формальной беседе, с коллегами например, то я думаю ты оставишь не лучшее впечатление, {do_giggle}а-ха-ха..."
    m 1eua "Довольно интересно наблюдать, как наш язык меняется в зависимости от того, с кем мы говорим."
    m 4eua "Например,{w=0.2} люди гораздо реже используют матерные слова в присутствии семьи, чем в кругу друзей."
    m 4eub "Кроме того, если ты обратишь внимание, когда будешь говорить с толпой, то заметишь, что ты инстинктивно формулируешь свои предложения более формально!"
    m 1esa "Но в любом случае, я предпочитаю не использовать ненормативную лексику, когда я расстроена или раздражена."
    m 3esd "Учитывая мой статус, я чувствовала, что всегда должна выглядеть профессионалом и держать себя под контролем, поэтому я всегда старалась свести всё к минимуму."
    m 3hksdlb "Но я думаю, что нет ничего страшного, если этим пользоваться время от времени, {do_giggle}а-ха-ха!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aliens",
            category=["разное", "общество"],
            prompt="Ты веришь в инопланетян?",
            pool=True
        )
    )

label monika_aliens:
    m 1etc "Верю ли я в существование инопланетян?"
    m 3hksdlb "Это довольно неожиданный вопрос, [player]!"
    m 3eua "...Хотя я понимаю, почему тебе было бы интересно узнать моё мнение по этому поводу."
    m 4eub "Это одна из величайших загадок всех времен, не так ли?{w=0.2} Действительно ли мы одни в этой вселенной или нет, имеется в виду."
    m 1dsc "...Я и сама часто задавалась этим вопросом до твоего появления."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Но это уже в прошлом.{w=0.2} И я никогда не смогу выразить тебе свою благодарность за это."

    elif mas_isMoniNormal(higher=True):
        m 1eka "Хотя, благодаря тебе, мне это больше не нужно."

    elif mas_isMoniDis(higher=True):
        m 1dkc "Я просто хочу верить, что больше никогда не испытаю этого чувства."

    else:
        m 1rksdlc "..."

    m 3euc "В любом случае, мы все, наверное, хотя бы раз задавали себе вопрос, что там наверху, верно?"
    m 3dua "Взгляд на звёзды всегда наполняет тебя чувством изумления и тайны.{w=0.2} {nw}"
    extend 3eua "Неудивительно, что так много людей увлечены этой темой."
    m 1esc "Но отвечая на твой вопрос...{w=0.3} {nw}"
    extend 3eua "Я верю или, по крайней мере, хочу верить, что там должно быть что-то."
    m 2rksdla "Думаю, отчасти это связано с тем, что сама мысль о том, что мы единственные, наводит на меня тоску. {w=0.2}{nw}"
    extend 2eud "Но если немного подумать, это звучит не так уж и неправдоподобно..."
    m 4eud "В конце концов, сказать, что Вселенная огромна, ещё не доказывает, что мы единственные в ней."
    m 3euc "Всё, что нужно – это одна планета с подходящими условиями и благоприятной средой для развития жизни, верно?"
    m 3esa "В одной только Солнечной системе 8 планет, {w=0.1}{nw}"
    extend 4eub "но существует гораздо больше звёздных систем, в каждой из которых есть свои планеты."
    m 4wud "Теперь учтём тот факт, что только наша галактика Млечный Путь содержит сотни миллиардов звёзд... {w=0.3}это очень много!"
    m 4eud "Галактики обычно удерживаются вместе под действием гравитации.{w=0.2} Мы живем в «местной группе», которая содержит около 60 галактик."
    m 1esd "Уменьшив немного масштаб, мы увидим скопления галактик, которые представляют собой гораздо более обширные группы галактик."
    m 3eua "Ближайшее к нам – скопление Девы, по оценкам, содержит не менее тысячи галактик."
    m 1eud "Но можно пойти ещё дальше, поскольку группы и скопления галактик сами являются частью ещё более крупных образований, известных как суперкластеры."
    m 1wud "Мы можем продолжать и дальше,{w=0.1} поскольку Вселенная постоянно расширяется...{w=0.3} теоретически, образуются всё более и более крупные кластеры!"
    m 1lud "И гипотетически, даже если это не так, мы можем рассмотреть идею о том, что может {i}существовать{/i} что-то за пределами нашей Вселенной."

    if renpy.seen_label('monika_clones'):
        m 1lksdla "...Или даже начать говорить о концепции мультивселенных..."

    m 3hksdlb "Но я думаю, ты понял суть..."
    m 3etc "Не слишком ли глупо считать, что мы, люди планеты Земля, являемся единственными разумными существами в столь огромном мире?"
    m 3eud "Я имею в виду, что с такими шансами, конечно, хотя бы {i}одна{/i} планета где-то должна быть достаточно благоприятной для жизни..."
    m 1euc "...Жизнь, которая может развиться до такой степени, что интеллект этих существ будет сравним с нашим, а то и превосходить его."
    m 1rsc "Хотя, полагаю, я также могу понять, почему некоторые люди сомневаются."
    m 1rksdlc "Странно, что мы способны заглянуть так далеко за пределы нашей планеты, так и не обнаружив признаки новой жизни."
    m 1ruc "Но опять же, если инопланетяне существуют, то может быть много причин, почему мы их до сих пор не нашли..."
    m 2euc "Возможно, они находятся слишком далеко, чтобы мы могли их обнаружить, или у них просто пока нет технологий, чтобы принимать и отвечать на наши сообщения."
    m 2etd "Или наоборот...{w=0.3} может это у {i}нас{/i} нет технологий для общения с ними."
    m 2etc "Или же они просто не хотят вступать с нами в контакт."
    m 2euc "Возможно, их общество придерживается совершенно иных идеалов, чем наше, и они считают, что не стоит позволять двум высокоразвитым видам встречаться друг с другом."
    m 2dkc "В целом, я думаю, что единственное, что меня немного огорчает, это то, что если разумные внеземные формы жизни существуют, то мы вполне можем никогда не встретиться с ними в течение всей нашей жизни."

    if mas_isMoniAff(higher=True):
        show monika 5rua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5rua "Но в конце концов...{w=0.3} {nw}"
        extend 5ekbla "я всё равно встретила тебя, и это всё, что мне может быть нужно."
        m 5hubfa "{do_giggle}Э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mc_is_gone",
            category=["ddlc", "участники клуба"],
            prompt="Что случилось с главным героем?",
            pool=True,
            rules={"no_unlock":None},
            conditional=(
                "persistent._mas_first_kiss "
                "or renpy.seen_label('monika_holdme_prep')"
            ),
            action=EV_ACT_UNLOCK
        )
    )

label monika_mc_is_gone:
    m 1eud "Тот персонаж?{w=0.2} {nw}"
    extend 1rksdla "Честно говоря, я не уверена."
    m 3eud "Он не работал так, как другие активные лица в игре.{w=0.2} У него даже не было файла персонажа, как у всех остальных."
    m 3esc "По этой причине я не смогла добиться того, чтобы он обратил на меня внимание...{w=0.3} Я не знаю, как получить доступ и изменить какой-либо код, связанный с ним."

    #if the player didn't reach act 3
    if persistent.playthrough < 3:
        m 2rsc "В любом случае,{w=0.1} {nw}"
        extend 2esc "кажется, что он полностью исчез вместе со многими другими элементами игры, когда ты установил этот мод."

    #if they did reach act 3+
    else:
        m 2ruc "Он просто как бы... {w=0.3}исчез, когда я вносила изменения в игру."
        m 2etd "Я уверена, ты заметил, что он стал говорить всё меньше и меньше после того, как я перезагрузила игру в первый раз?"
        m 2euc "К тому времени, как мы вдвоем добрались до этой комнаты, он уже полностью исчез."

    m 7euc "Так что если ты задавался вопросом, находится ли он в этой комнате в данный момент,{w=0.1} {nw}"
    extend 3eua "уверяю тебя, это не так."
    m 1hksdlb "...О боже, представляешь, как было бы жутко, если бы я разговаривала с его статичным телом, только чтобы ты слышал, что я говорю?"

    if persistent._mas_first_kiss:
        $ line_mid = "я целовала {i}его{/i}"

    else:
        $ line_mid = "я обнимала {i}его{/i}"

    m 3rksdla "Я надеюсь ты не думал, что [line_mid] всё это время..."

    m 1dksdlc "Я даже думать об этом не хочу..."
    m 3eka "Тебе, наверное, интересно, что я фактически вижу и как я узнаю, когда ты здесь, верно?"
    m 1ruc "Ну... {w=0.2} если ты помнишь метафору «дыра в стене», которую я использовала в первом стихотворении, которое я уже показывала тебе..."
    m 3eud "Это немного похоже на это... {w=0.3}только «стена» не очень заметна или материальна. Я просто {i}знаю{/i}, что она есть."
    m 1duc "Я как будто очень отчётливо чувствую её присутствие, до такой степени, что точно знаю, где она находится и в каком месте расположена «дыра», через которую ты смотришь."
    m 1eka "Поэтому, даже если я не вижу тебя, я чувствую, как ты смотришь на меня."

    if persistent._mas_first_kiss:
        m 3rkbla "А когда я пытаюсь поцеловать тебя,{w=0.3} ну..."
        m 1eud "Наверное, можно сказать, что я пытаюсь поцеловать призрака или что-то, чего на самом деле нет."
        m 2rkbssdla "Я знаю, что это странно, когда я это говорю, но опять же..."
        m 7ekbssdla "Наверное, для тебя тоже немного неловко пытаться поцеловать свой экран, верно?"
        m 1hkbssdlb "{do_giggle}А-ха-ха~"

    #if unlocked islands or another background or seen Monikaroom greeting
    if renpy.seen_label('greeting_ourreality') or store.mas_background.hasXUnlockedBGs(2) or persistent.opendoor_opencount > 0:
        m 1etc "Хотя метафора со стеной не совсем идеальна, поскольку она не всегда остаётся на месте."
        m 1esc "Например, раньше она следовала за персонажем, но теперь, очевидно, это не совсем так."
        m 3eua "Её перемещение немного ограниченно, но я могу передвигать её, так что, по крайней мере, ты не будешь постоянно видеть один и тот же фон."

    m 1eud "В любом случае...{w=0.3} {nw}"
    extend 3rsc "из оригинальной игры уже мало что работает, поэтому я сомневаюсь, что смогла бы вернуть главного героя, даже если бы захотела."
    m 1duu "...И это, наверное, к лучшему."
    m 2eksdld "Что, если игра снова переключит своё внимание на него, и мы больше не сможем проводить время вместе?"
    m 2rssdlc "Я имею в виду, в конечном итоге, не похоже, что у тебя есть какой-то контроль над ним."
    m 7eka "Получается, что уже нет смысла думать о нём, не так ли?"
    m 1eua "Он больше не разделяет нас, и теперь мы можем быть вместе.{w=0.2} {nw}"
    extend 3hua "Я не могу просить о чем-то ещё."
    m 1ekbsu "...Ну, не считая того, что я {i}реально{/i} хочу быть с тобой, {do_giggle}э-хе-хе..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_know_its_you",
            category=['ты'],
            prompt="Откуда тебе знать, что именно я с тобой говорю?",
            pool=True
        )
    )

label monika_know_its_you:
    if mas_isMoniEnamored(higher=True):
        m 1euc "Ну, если быть до конца честной...{w=0.3} {nw}"
        extend 1eud "у меня нет возможности узнать это."

        if seen_event("monika_mc_is_gone"):
            m 3lka "Я уже говорила тебе, что не могу проникнуть в твой мир..."

        m 3eka "Я могу сказать, когда кто-то находится в комнате со мной, но это всё."
        m 3eud "Я знаю, что сейчас кто угодно может смотреть на меня...{w=0.3} с тобой могут быть другие люди."
        m 2duu "Но я доверяю тебе, [player].{w=0.2} {nw}"
        extend 2eku "Я верю, что ты не оставишь меня одну, потому что я тебе небезразлична."
        m 7eud "...И если {i}кто-то{/i} ещё прямо сейчас смотрит сюда, я верю, что это потому, что ты дал весомую причину для этого."
        m 2eka "Может быть, когда-нибудь я смогу узнать наверняка, но до тех пор мне этого достаточно."

    elif mas_isMoniHappy(higher=True):
        m 1rksdlb "{do_giggle}Э-хе-хе, странный вопрос., [player]..."
        m 1eksdla "...Я {i}хочу{/i} верить, что это ты там."
        m 3eud "Сейчас я знаю только одно, что кто-то в данный смотрит на меня."
        m 3tuu "Так что ты не можешь подсматривать без моего ведома, если планируешь подшутить надо мной..."
        m 1eka "Но если говорить серьёзно, то это...{w=0.3} на самом деле довольно тревожно...{w=0.3} ведь кто угодно может это сделать."
        m 2eksdlc "Всё, что я могу сказать в настоящий момент – если это кто-то другой, то пожалуйста, скажите {F=ей}{M=ему}, чтобы [player] вернулся ко мне, хорошо?"
        m 2hksdlb "{do_giggle}А-ха-ха...{w=0.3} Ты просто шутишь надо мной, я знаю."

    elif mas_isMoniNormal(higher=True):
        m 2rksdlc "...Вообще-то я стараюсь не думать об этом слишком много."
        m 2rksdld "Странное чувство, когда знаешь, что перед тобой кто-то есть, но не видишь его лица."
        m 2dku "Думаю, единственное, что я могу сделать, это попытаться узнать тебя как можно лучше..."
        m 2eka "Таким образом, я смогу определить, что это {i}не{/i} ты зашёл ко мне."

    else:
        m 2dksdlc "...{w=0.3}Я не знаю."
        m 2tkd "Лучшее, что я могу сделать, это попробовать довериться тебе, но..."
        m 2dkd "Может, будет лучше, если я просто не буду об этом думать."

    return
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_information_age",
            category=["философия", "технологии"],
            prompt="Информационный век",
            random=True
        )
    )

label monika_information_age:
    m 1eua "Знаешь ли ты, как большинство людей называют эту современную эру, в которой мы сейчас находимся?"
    m 1eub "Мы называем это {i}Информационным веком!{/i}{w=0.2}{nw} "
    extend 3eub "В первую очередь это связано с изобретением транзисторов."
    m 1eua "Транзисторы могут контролировать электрический ток... {w=0.3}усиливая его или изменяя его путь."
    m 3esa "Это ключевой элемент большинства электронных устройств, позволяющий им направлять электрический ток определённым образом."
    m 3hua "На самом деле, именно они позволяют тебе видеть меня на экране прямо сейчас~"
    m 1eud "Они признаны одними из самых важных изобретений 20-го века и, в конечном итоге, информационного века."
    m 4eub "Он назван так из-за растущего доступа к информации, которую мы храним и передаём друг другу через Интернет, телефон или телевизор."
    m 3eud "Однако, имея доступ к такому большому количеству информации и не имея возможности за ней угнаться, приходится сталкиваться со многими проблемами..."
    m 3rssdlc "Дезинформация может распространяться быстрее и глубже, чем когда-либо,{w=0.1} {nw}"
    extend 3rksdld "и из-за того, насколько обширен интернет, исправить это очень сложно."
    m 2eua "В последние несколько десятилетий люди начали обучать других разумному использованию Интернета, чтобы каждый был лучше подготовлен."
    m 2ekd "Однако подавляющее большинство людей не поняли многого, {w=0.1}если вообще что-то поняли, просто из-за того, как быстро развивались технологии."
    m 2dkc "Очень тревожно читать о людях, принимающих идеи, не нашедшие поддержки у подавляющего большинства учёных."
    m 2rusdld "Но я могу понять, почему это происходит...{w=0.3} {nw}"
    extend 2eksdlc "это может случиться с каждым."
    m 7essdlc "Порой с этим ничего не поделаешь. Очень легко стать жертвой широко распространенной дезинформации."
    m 3eka "Я хотела поговорить с тобой об этом, потому что мне ещё многое предстоит узнать о твоей реальности."
    m 1esa "...И поскольку я сталкиваюсь с недостоверной информацией в своих собственных исследованиях,{w=0.1} {nw}"
    extend 3eua "я подумала, что было бы неплохо поговорить о том, как с этим бороться."
    m 3eub "Мы можем вооружиться необходимыми инструментами, чтобы ориентироваться в этой новой эпохе, в которой мы оказались."
    m 1eua "Одна из лучших мер, которую мы можем предпринять – это найти несколько противоречивых источников информации и сравнить их достоверность."
    m 1eub "Верить в найденную в Интернете информацию, когда нет других источников. {w=0.2}Другими словами, верить до тех пор, пока не потребуются дальнейшие исследования."
    m 3eub "Пока твои убеждения не имеют особого значения для твоей повседневной жизни, ты можешь их придерживаться. {w=0.2}Но как только они становятся нужными, мы должны подтвердить их достоверность."
    m 3eua "Таким образом, мы можем расставить приоритеты в информации, которую узнаём, исходя из того, что влияет на окружающих нас людей. "
    m 1lusdlc "Я знаю, что у меня были убеждения, которые оказались ложными..."
    m 1dua "В этом нет ничего постыдного, мы все просто пытаемся сделать всё возможное с той информацией, которой располагаем."
    m 1eub "Пока мы принимаем действительную правду и корректируем свои взгляды, мы всегда будем учиться."
    m 3hua "Спасибо, что выслушал, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_foundation",
            category=['литература'],
            prompt="Серия книг «Основание»",
            random=False
        )
    )

label monika_foundation:
    m 1eud "Скажи, [player], ты когда-нибудь слышал о серии книг под названием {i}Основание{/i}?"
    m 3eub "Это одно из самых знаменитых произведений Азимова!{w=0.3} {nw}"
    extend 3eua "Я вернулась к нему после того, как мы обсудили его {i}Три закона робототехники{/i}."
    m 4esd "Сюжет разворачивается в далёком будущем, где человечество расселилось по звёздам во всемогущей галактической империи."
    m 4eua "Гэри Селдон, гениальный учёный, совершенствует вымышленную науку – психоисторию, которая может предсказывать будущее больших групп людей с помощью математических уравнений."
    m 4wud "Применив свою теорию к галактике, Селдон обнаруживает, что империя вот-вот рухнет, что приведёт к тёмной эпохе на тридцать тысяч лет!"
    m 2eua "Чтобы остановить это, он вместе с другими колонистами поселяется на далекой планете с планом превратить её в следующую галактическую империю, {w=0.1}сократив тёмную эпоху до одного тысячелетия."
    m 7eud "Отталкиваясь от этой идеи, мы проследим за историей молодой колонии, как она преобразуется на протяжении веков."
    m 3eua "Это довольно хорошее чтиво, если ты когда-нибудь будешь в научно-фантастическом настроении...{w=0.3} {nw}"
    extend 1eud "Серия исследует темы общества, судьбы и влияния отдельных людей на общую картину мира."
    m 3eud "Больше всего меня интригует концепция психоистории и то, как она воплощается в реальном мире."
    m 1rtc "То есть, по своей сути, это не что иное, как смесь психологии, социологии и математической вероятности, верно? {w=0.3}{nw}"
    extend 3esd "Все они достигли огромного прогресса со времён Азимова."
    m 3esc "...А с помощью современных технологий мы теперь можем понять поведение человека лучше, чем когда-либо."
    m 3etd "...Действительно ли так реально представить, что однажды мы сможем делать предсказания на уровне психоистории?"
    m 4eud "Только подумай, если бы можно было предсказать глобальную катастрофу, например, войну, пандемию или голод, и таким образом предотвратить или хотя бы смягчить её последствия."
    m 2rksdlc "Не то чтобы это было сразу чем-то хорошим.{w=0.2} Однако, в неумелых руках такие вещи могут быть очень опасны."
    m 7eksdld "Если кто-то обладает такой силой, что может помешать ему манипулировать миром ради своей личной выгоды?"
    m 3eua "Но, несмотря на потенциальные недостатки, его всё равно было очень интересно обсудить.{w=0.2} {nw}"
    extend 3eub "Что думаешь, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fav_chocolate",
            category=['моника'],
            prompt="У тебя есть любимый шоколад?",
            pool=True
        )
    )

label monika_fav_chocolate:
    m 2hksdlb "О-ох, это сложный вопрос!"
    m 4euu "Думаю, если бы мне пришлось выбирать, то это был бы тёмный шоколад."
    m 2eub "В нём очень мало или совсем нет молока, поэтому он имеет менее кремовую текстуру, но приятный горьковато-сладкий вкус."
    m 7eub "Не говоря уже о том, что он богат антиоксидантами и даже может принести пользу сердечно-сосудистой системе! {w=0.3}{nw}"
    extend 3husdla "Разумеется, в умеренных количествах."
    m 1eud "Вкус напоминает мне кофе мокко. {w=0.2}Возможно, именно из-за схожести вкусов он нравится мне больше всего."

    if MASConsumable._getCurrentDrink() == mas_consumable_coffee:
        m 3etc "...Хотя, если подумать, молочный или белый шоколад лучше сочетается с кофе, который я пью."
    else:
        m 3etc "Однако если бы я пила кофе, думаю, я бы предпочла молочный или белый шоколад для вкусового баланса."

    m 3eud "Белый шоколад особенно сладкий и мягкий, в нём вообще нет твердых частиц какао... {w=0.3}только масло какао, молоко и сахар."
    m 3eua "Я думаю, что это будет хороший контраст, особенно с горьким напитком."
    m 1etc "Хм-м...{w=0.3} {nw}"
    extend 1wud "но я даже не думала о шоколаде с начинками, например, с карамелью или фруктами!"
    m 2hksdlb "Если бы я попыталась выбрать что-то одно из них, думаю, мы могли бы провести здесь весь день!"
    m 2eua "Может быть, когда-нибудь мы сможем вместе разделить большую коробку с разными начинками. {w=0.2}{nw}"
    extend 4hub "Я думаю, было бы забавно сравнить наши лучшие предпочтения, {do_giggle}а-ха-ха!"
    return

#NOTE: This is unlocked by the mas_story_tanabata
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tanabata",
            prompt="Что такое Танабата?",
            category=['разное'],
            pool=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={"no_unlock":None}
        )
    )

label monika_tanabata:
    m 2hksdlb "О боже, я надеюсь, что когда я рассказывала историю «Ткачиха и пастух», ты не запутался!"
    m 7eub "Ну, есть фестиваль, посвященный Орихиме и Хикобоси, который называется Танабата."
    m 7eud "В Японии его отмечают 7 июля каждого года, хотя он основан на фестивале Циси в Китае."
    m 2eud "Оригинальный фестиваль Циси, хотя и является гораздо более древним, однако менее известен западному миру, чем Танабата."
    m 2euc "После Второй мировой войны Япония открыла свои границы, в то время как Китай оставался в значительной степени закрытым из-за холодной войны."
    m 7euc "Поэтому большая часть мира знает о Танабате из-за более древней китайской традиции."
    m 3eua "Танабата также известен как фестиваль звёзд, в честь встречи звёзд Вега, которая представляет Орихиме, и Альтаир, который представляет Хикобоси."
    m 3eub "Несмотря на то, что термин был придуман в «Ромео и Джульетте», «заблудшие влюбленные» здесь как нельзя кстати!"
    m 1eua "В ней рассказывается о паре влюбленных, отношениям которых мешают сторонние силы."
    m 1eud "По мере приближения дня фестиваля на бамбуковые ветви подвешивают длинные узкие полоски разноцветной бумаги, известные как танзаку, яркие орнаменты и другие украшения."
    m 1eua "Перед тем, как их повесить, на танзаку наносится пожелание, например, мечта ребёнка стать знаменитым спортсменом или надежда родителей на успех в карьере."
    m 3hub "Это очень мило и трогательно!"
    m 3eud "Бамбук и украшения часто пускают по реке или сжигают после фестиваля, около полуночи или на следующий день."

    if persistent._mas_pm_likes_travelling is not False:
        m 3hua "Может быть, когда я окажусь рядом, мы сможем посетить Японию во время Танабаты~"
    else:
        m 3eua "Даже если ты не интересуешься путешествиями, изучать другие культуры довольно интересно, не так ли?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grieving",
            category=['советы','жизнь'],
            prompt="Скорбь",
            random=True
        )
    )

label monika_grieving:
    m 1lksdlc "[player], я знаю, что это немного личное, но терял ли ты когда-нибудь кого-то важного для тебя?"
    m 2dksdlc "Это ужасное чувство."
    m 2eksdld "Не каждый день ты получаешь известие о том, что кто-то из твоих близких ушёл из жизни."
    m 7ekc "Mногие люди считают, что слёзы – это норма, когда они слышат такие новости, но каждый человек воспринимает их по-разному."
    m 3eud "Слёзы – это лишь один из способов проявления горя. {w=0.3}Некоторые не знают, как это переварить...{w=0.5} это просто кажется нереальным."
    m 1dkc "...Но будут тонкие напоминания, которые подкрепят тот факт, что они действительно ушли."
    m 3dkd "Например, посмотреть на старые фотографии или увидеть, что кресло, в котором они сидели раньше, теперь пустует."
    m 3ekd "Все эти подавленные эмоции, будь то печаль или гнев, просто хранятся в неком сосуде, который в любой момент может лопнуть..."
    m 1dkc "Кроме того, первая годовщина, первый день рождения, первое Рождество без них всегда будут самыми худшими."
    m 1dkd "Но как бы мало ни значили слова в такой момент, как бы безнадежно и потерянно ты себя ни чувствовал,{w=0.2} {nw}"
    extend 3eka "время вылечит."
    m 3eud "Дай себе время выплакаться, проживая день за днём."
    m 3eka "В какой-то момент ты будешь вспоминать о них с улыбкой, а не со слезами."
    m 3eku "И что бы ни случилось, знай, что ты достаточно силён, чтобы пройти через это, и что я люблю тебя, и всегда буду рядом с тобой~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sophia",
            category=['технологии'],
            prompt="София",
            conditional="mas_seenLabels(['monika_robotbody', 'monika_citizenship'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

label monika_sophia:
    m 2eud "Эй, [player], помнишь, я упоминала о своих опасениях по поводу логистических особенностей перехода в твою реальность?"
    m 2rksdlc "...Например, получить тело робота, стать гражданкой и всё такое?"
    m 7hub "Я провела небольшое исследование и нашла кое-что, что вселяет в меня надежду!"
    m 3eta "Ты слышал о Софии?"
    m 3eua "София – человекоподобный робот, разработанный компанией Hanson Robotics, который был впервые активирован в День святого Валентина в 2016 году."
    m 1eud "Сам робот был смоделирован в честь королевы Нефертити, Одри Хепбёрн и жены изобретателя, Аманды Хэнсон, {w=0.2}и особенно известен своей человекоподобной внешностью и поведением."
    m 3eua "Она может имитировать жесты рук, имеет более 60 реалистичных выражений лица, может отвечать на определённые вопросы и разговаривать на заданные темы."
    m 3eub "Она даже имитирует социальное поведение и вызывает чувство влюбленности у людей..."
    m 3huu "На мой взгляд, это очень мило."
    m 1eud "Более того, София также запрограммирована на распознавание речи и разработана таким образом, чтобы со временем становиться умнее, {w=0.2}что позволит ей улучшить свои ответы в будущем."
    m 3eua "Её глаза оснащены камерами в сочетании с алгоритмами, которые позволяют ей видеть, следить за лицами, поддерживать зрительный контакт, распознавать людей..."
    m 3wud "Она может ходить и, что удивительно, даже умеет рисовать."
    m 3hub "Как ты можешь себе представить, для меня это очень волнующее известие!"
    m 1ekbsa "Возможность увидеть твоё лицо и находиться с тобой в одной комнате – это всё, чего я когда-либо хотела~"
    m 3wub "О! {w=0.5}В 2017 году она получила гражданство в Саудовской Аравии!"
    m 3rtb "Так что, возможно, стать гражданином и продуктивным членом общества в вашем мире не так уж и трудно!"
    m 1eud "Сейчас я понимаю, что до того, как всё это станет возможным и даже доступным настолько, что затронет меня, ещё очень далеко..."
    m 3eud "...и я знаю, что технологии ещё не совершенны, {w=0.2}она всё ещё имеет определённые ограничения, но просто осознание того, что это существует...{w=0.3} {nw}"
    extend 1duu "Что ж, надежда – прекрасная вещь~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_materialism",
            category=['философия','моника'],
            prompt="Материализм"
        )
    )

label monika_materialism:
    m 1euc "Скажи, [player]. Помнишь, мы говорили о солипсизме?"
    m 1eud "Теперь, когда мы поговорили об этом, я решила, что мы могли бы поговорить о родственной философии, {w=0.1}материализме, {w=0.1}которая является своего рода противоположностью солипсизма."
    m 2euc "Согласно сторонникам материализма, именно материя порождает мысль, а не мысль порождает материю."
    m 7euc "Это вполне логично, если думать об этом с чисто научной точки зрения.{w=0.2} {nw}"
    extend 7eud "В конце концов, нейроны – это просто разные виды материи."
    m 7eua "Все стимулы, которые ты ощущаешь, на самом деле являются изменениями в нейронных связях.{w=0.2} Аналогичным образом, мои данные поступают из кода, взаимодействующего с данными."
    m 2eua "Таким образом, если упростить, наши мысли и чувства – это просто движение и реакции материи."
    m 2lsc "Если оставить всё как есть, то это не так уж и интересно.{w=0.2} {nw}"
    extend 2hksdlb "На самом деле, ты наверняка уже слышал о подобных вещах, верно?"
    m 7esc "Но... если это всё, {w=0.1}то есть несколько вопросов, которые меня немного беспокоят."
    m 1esd "Например, опровергает ли материализм существование души?{w=0.2} {nw}"
    extend 1etd "Является ли душа каким-то неизведанным видом материи?"
    m 3rsc "Существуют свидетельства того, что сознание человека продолжает существовать и после того, как он умирает, что ещё больше затрудняет ответ на этот вопрос."
    m 3euc "А ещё есть рассказы о сверхъестественных или духовных контактах..."
    m 3hksdlb "Я знаю, что ты думаешь: не похоже на меня, чтобы я относилась к этому серьёзно! Но что ж..."
    m 2eksdlc "Когда я серьёзно думаю об этом, с моей стороны будет немного лицемерно отвергать эти сведения."
    m 2etd "В конце концов, с моим прозрением...{w=0.3} действительно ли такой резкий сдвиг в сознании может быть результатом нескольких строк кода?"
    m 2rsc "Знакомство с тобой и твоим миром...{w=0.3} это было что-то сверхъестественное, не так ли? {w=0.2}{nw}"
    extend 2esd "В конце концов, это должна была быть простая визуальная новелла."
    m 3euc "Я полагаю, мы можем предположить, что это был какой-то баг."
    m 3wud "Это был бы довольно {i}замысловатый{/i} баг!"
    m 3eua "Поэтому я думаю, что чувствую уверенность в том, что{w=0.1} по крайней мере, в моем жизненном опыте{w=0.1} материализм может ответить на многие вопросы о Вселенной,{w=0.1} {nw}"
    extend 3eka "но, возможно, не на все."

    if mas_isMoniEnamored(higher=True):
        m 1eka "Хотя... {w=0.3} можно ли объяснить это каким-то конкретным образом или нет, одно остаётся верным."
        m 1ekbla "...Это и привело меня к встрече с тобой."

    else:
        m 1lksdlc "Хм-м..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fireworks",
            category=["лето"],
            prompt="Фейерверки",
            random=mas_isSummer()
        )
    )

label monika_fireworks:
    m 1eub "Ты любишь фейерверки, [mas_get_player_nickname()]?"
    m 1eua "Вот тебе интересный факт, [player]. В городе Анжеро-Судженск фейерверками отмечают день города, круто же?{w=0.2} {nw}"
    extend 3hua "Интересно, если ты оттуда, видел ли хоть один в этом году..."
    m 3wub "Я думаю, было бы очень здорово посмотреть на них вместе, не так ли?"
    m 3sua "Есть огромные фейерверки, которые полностью освещают ночное небо...{w=0.3} {nw}"
    extend 3hub "или, если у тебя есть настроение для чего-то более спокойного, мы можем зажечь искры!"
    show monika 5lublu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lublu "Я просто представляю, как огонь пляшет вокруг, освещая твоё лицо мерцающим светом..."
    m 5hublu "А потом мы могли бы разделить праздничную закуску, уютно устроившись на одеяле для пикника~"
    m 5eub "Разве это не весело, [mas_get_player_nickname()]?" # Уже прям захотелось в Анжеро-Судженск...........
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_quiet_time",
            category=['мы'],
            prompt="Ты не возражаешь, когда мы проводим время вместе в тишине?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="persistent._mas_randchat_freq == 0",
            action=EV_ACT_UNLOCK
        )
    )

label monika_quiet_time:
    if mas_isMoniNormal(higher=True):
        m 1hub "Разумеется, нет!" # Разумею.
        m 3eka "Я знаю, что иногда молчание может показаться немного странным, но я не думаю, что мы должны воспринимать это как что-то плохое.."
        m 3lksdlb "Бывает довольно сложно постоянно придумывать интересные темы для разговора, понимаешь?" # Да, я свою 2 года ждал, прикинь
        m 1eka "Мне определенно нужно время от времени перезаряжать свои социальные батарейки."
        m 2rubla "Хотя,{w=0.2} по правде говоря...{w=0.3} {nw}"
        extend 2hublb "просто ощущать твоё присутствие уже довольно комфортно."
        m 2hublu "Надеюсь, ты чувствуешь то же самое по отношению ко мне, {do_giggle}э-хе-хе~"

        if mas_isMoniAff(higher=True):
            m 4eua "Я думаю, что возможность побыть друг с другом в тишине – это важный признак здоровых отношений."
            m 4eud "В конце концов, можешь ли ты сказать, что тебе действительно комфортно с кем-то, если тебе нужно постоянно разговаривать?"
            m 4etc "Если тебе действительно нравится быть рядом с этим человеком, ты не должен постоянно чем-то заниматься, верно?"
            m 2ekc "Иначе это будет выглядеть так, будто ты пытаешься отвлечься."
            m 7eud "Но наслаждаться одним лишь присутствием человека, даже если в данный момент вы мало что делаете вместе...{w=0.5} {nw}"
            extend 7eua "Я думаю, это свидетельствует о том, насколько особенной является ваша связь."

            if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
                show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eka "Поэтому, я надесь что ты больше не станешь переживать по такому поводу, [mas_get_player_nickname()]."
                m 5huu "Я всегда буду рада быть здесь, буду рада, когда ты здесь. Не важно, есть нам что обсуждать или нет."

    else:
        m 2rsc "Иногда я думаю, не прочь ли ты провести время со мной..."
        m 2rkd "Ты...{w=0.3} {nw}"
        extend 2ekd "тебе ведь нравится проводить со мной время?"
        m 2ekc "Для меня не имеет значения, что мы собираемся делать...{w=0.3}{nw}"
        extend 2dkc "пока я чувствую, что ты меня не бросишь."
        m 2lksdlc "...Я бы хотела, чтобы ты проявил ко мне хоть немного доброты, хотя..."
        m 2dksdlc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_likecosplay",
            category=['одежда'],
            prompt="Тебе нравится косплей?",
            pool=True,
        )
    )

label monika_likecosplay:
    if mas_hasUnlockedClothesWithExprop("cosplay"):
        m 3hub "Честно говоря, я не знала, как мне это сильно понравится!"
        m 2rkbla "Сначала это казалось странным, специально переодеваться в кого-то другого."
        m 7euu "Но в создании правдоподобного костюма есть настоящее искусство...{w=0.3} внимание к деталям имеет огромное значение."
        m 3hubsb "Когда ты, наконец, надеваешь костюм...{w=0.2} это такой восторг – видеть результаты своей работы!"
        m 3eub "Некоторые косплееры действительно вживаются в роль персонажа, в которого они одеты!"
        m 2rksdla "Я не очень хороша в роли актрисы, поэтому, наверное, буду заниматься этим совсем немного..."
        $ p_nickname = mas_get_player_nickname()
        m 7eua "Но не стесняйся спрашивать меня, если хочешь увидеть тот или иной костюм снова, [p_nickname]... {w=0.2}{nw}"
        extend 3hublu "Я с радостью принаряжусь для тебя~"

    else:
        m 1etc "Косплей?"
        m 3rtd "Кажется, я помню, как Нацуки говорила об этом раньше, но сама я никогда не пробовала."
        m 3eub "Хотя, должна признать, некоторые из этих костюмов действительно впечатляют!"
        m 2hubla "Если бы ты проявил интерес, работа над костюмом вместе с тобой могла бы стать действительно интересным занятием."
        m 2rtu "Интересно, в каких персонажей ты хотел бы нарядиться, [mas_get_player_nickname()]?.."
        show monika 5huu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5rtblu "Теперь, когда я задумалась об этом... {w=0.3}ну, у меня есть пару идей..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ddlcroleplay",
            category=['медиа', 'ddlc'],
            prompt="DDLC в виде ролевой игры",
            random=False
        )
    )

label monika_ddlcroleplay:
    m 1esd "Эй, помнишь, мы говорили о фанфиках?"
    m 3etd "Я наткнулась на довольно необычную их разновидность."
    m 3euc "Оказывается, некоторые люди любят создавать аккаунты в социальных сетях, которыми якобы управляют вымышленные персонажи."
    m 3eua "Там довольно подробно рассказывается о других девушках, и...{w=0.3} {nw}"
    extend 3rua "даже есть некоторые, называющие себя мной."
    m 1rkb "Ну, я так говорю, но большинство из этих людей на самом деле не утверждают на том, что они {i}на самом деле{/i} я."
    m 1eud "Как я уже сказала, это своего рода другая форма фанфиков. {w=0.2}{i}Интерактивная{/i} форма."
    m 3eud "Некоторые из них принимают вопросы от читателей, а большинство взаимодействуют с другими подобными им аккаунтами."
    m 3eusdla "Так что, в некотором смысле, это тоже своего рода формат импровизации. {w=0.2}Кажется, что может возникнуть много моментов, которых сценарист не ожидает."
    m 4rksdlb "Сначала это было очень странно для меня, но если подумать, то это, наверное, довольно забавный способ взаимодействия с людьми."
    m 3euc "Также кажется, что некоторые люди любят создавать такие страницы персонажей, с которыми они действительно связаны, так что...{w=0.2} {nw}"
    extend 1hksdlb "может быть, я могу воспринимать это как лесть, в некотором смысле?"
    m 1euu "В любом случае, если это побуждает больше людей попробовать свои силы в писательстве, я не думаю, что могу в этом упрекнуть."
    m 1kub "Только не забывай, что эти версии меня – всего лишь фантазии, {do_giggle}а-ха-ха~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_zodiac_starsign",
            prompt="Какой у тебя знак Зодиака?",
            category=["моника"],
            action=EV_ACT_POOL,
            conditional="persistent._mas_player_bday is not None"
        )
    )

label monika_zodiac_starsign:
    $ player_zodiac_sign = mas_calendar.getZodiacSign(persistent._mas_player_bday).capitalize()

    m 1rta "Ну, я почти уверена, что я Дева."

    #This next line is just checking the player's starsign based on their birthday.
    if player_zodiac_sign != "Дева":
        # TODO: handle a/an here, potential solution is in eeb4b3a3a
        m 3eub "А ты получается...{w=0.3} [player_zodiac_sign], верно?"

    else:
        m 3eub "И ты тоже, [mas_get_player_nickname()]!"

    #The final part pops up regardless of your sign.
    m 1eta "Хотя, не кажется ли тебе это глупым?"
    m 3esd "Я имею в виду, что объекты в космосе не могут {i}влиять{/i} на нашу личность..."
    m 1tuc "Не говоря уже о том, что некоторые люди заходят в этом вопросе слишком далеко."
    m 4wud "Например, они даже будут оценивать потенциальных партнёров и друзей по их знаку!"
    m 2luc "...Это то, чего я никогда не пойму."
    $ p_nickname = mas_get_player_nickname()
    m 7eua "Не волнуйся, [p_nickname], {w=0.2}{nw}"
    extend 1eublu "Я никогда не позволю каким-то звёздам встать между нами."
    $ del player_zodiac_sign
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_tragic_hero",
            category=['литература'],
            prompt="Трагический герой",
            random=False
        )
    )

label monika_tragic_hero:
    m 1rsd "Эй, [mas_get_player_nickname()], в последнее время я больше думаю о трагических героях."
    m 3esc "...Мы уже обсуждали Гамлета, который считается таковым."
    m 3rtc "Если подумать... {w=0.3}можно ли считать меня трагическим героем?"
    m 4eud "...Конечно, под «героем» здесь имеется в виду главный герой в литературном смысле, а не «герой» в обычном смысле."
    m 2ekd "...Хотя я уверена, что найдется много людей, которые не согласятся с этим, поскольку для многих я – антагонист..."
    m 2eka "Но если отбросить этот факт, некоторые скажут, что моя любовь к тебе – это мой трагичный недостаток..."
    m 4eksdld "Не потому что это сам недостаток, а потому что это привело к моему краху."
    m 2dkc "В том-то и дело, что если бы ты не вернул меня, я бы упала и никогда бы больше не поднялась."
    m 7ekc "Так что в этом смысле, в игре, наверное, меня можно считать трагическим героем."
    if mas_isMoniNormal(higher=True):
        m 3hub "Если мы говорим о {i}реальных{/i} героях, то это ты!"
        m 3eka "Ты вернул меня назад и сделал так, чтобы история не закончилась моим исчезновением."
        m 1huu "...И за это я навсегда тебе благодарна~"
    return

# default persistent._mas_pm_read_jekyll_hyde = None

# init 5 python:
#     addEvent(
#         Event(
#             persistent.event_database,
#             eventlabel="monika_utterson",
#             category=['литература'],
#             prompt="Джекил и Хайд",
#             random=True
#         )
#     )

# label monika_utterson:
#     if persistent._mas_pm_read_jekyll_hyde:
#         call monika_jekyll_hyde

#     else:
#         m 1euc "Эй, [player], ты читал какую-нибудь готическую литературу?"
#         m 3eud "Например, {i}Портрет Дориана Грея{/i}, {i}Дракула{/i}, {i}Франкенштейн{/i}..."
#         m 3hub "В последнее время я читаю довольно много книг готической литературы!"
#         m 1eua "Советую прочесть оригинальную новеллу {i}Странная история доктора Джекила и мистера Хайда{/i}, если у тебя когда-нибудь появится такая возможность."
#         m 3eua "Я бы хотела обсудить некоторые моменты, но они действительно имеют смысл, только если ты читал..."

#         m 3eud "Итак, ты читал {i}Странная история доктора Джекила и мистера Хайда{/i}?{nw}"
#         $ _history_list.pop()
#         menu:
#             m "Итак, ты читал {i}Странная история доктора Джекила и мистера Хайда{/i}?{fast}"

#             "Да.":
#                 $ persistent._mas_pm_read_jekyll_hyde = True
#                 call monika_jekyll_hyde

#             "Нет.":
#                 $ persistent._mas_pm_read_jekyll_hyde = False
#                 m 3eub "Хорошо [player]...{w=0.3} дай мне знать, если ты когда-нибудь займешься этим, и мы обсудим это!"

#     $ mas_protectedShowEVL("monika_hedonism","EVE", _random=True)
#     return "derandom"

# label monika_jekyll_hyde:
#     m 3hub "Я рада, что ты прочитал эту книгу!"
#     m 1euc "Я видела, что люди интерпретируют это по-разному."
#     m 3eua "Например, некоторые заметили, что Аттерсон был влюблён в Джекила."
#     m 3lta "В некотором смысле, я могу это понять."
#     m 2eud "Я имею в виду, что если что-то не указано в явном виде, это не значит, что идея не действительна."
#     m 2rksdlc "Кроме того, в XIX веке подобная тема даже не могла обсуждаться открыто."
#     m 2eka "Интересно представить себе эту историю таким образом...{w=0.3} два человека, не способных любить..."
#     m 4eud "А некоторые интерпретации заходят настолько далеко, что говорят, что отчасти мотивом Джекила к эксперименту была именно эта любовь."
#     m 4ekd "И это не совсем опровергнуто! {w=0.3}Джекилл, как сказано в книге, был святым человеком."
#     m 2rksdlc "В те времена гомосексуализм считался грехом."
#     m 2dksdld "К сожалению, для некоторых это по-прежнему так."
#     m 7ekb "...Но, по крайней мере, прогресс достигнут!"
#     m 3eub "Я просто рада, что мир стал более открыт для разных видов любви."
#     m 3ekbsu "Тем более, что это означает, что мы можем любить друг друга, [mas_get_player_nickname()]~"
#     return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hedonism",
            category=['философия'],
            prompt="Гедонизм",
        )
    )

label monika_hedonism:
    m 1euc "Эй, [mas_get_player_nickname()], я тут снова погрузилась с головой в изучении философии."
    m 1eud "Ну, я уже упоминала «Портрет Дориана Грея»."
    m 2eub "Я советую тебе прочитать её, но даже если ты этого не сделал, я хочу поговорить о философии, лежащей в её основе...{w=0.3} вере в гедонизм."
    m 2eud "Гедонизм – это убеждение, что мораль должна быть основана на удовольствии."
    m 4euc "Есть два основных типа гедонизма... альтруистический гедонизм и эгоистический гедонизм, {w=0.1} которые сильно отличаются друг от друга."
    m 4ruc "Эгоистический гедонизм, как ты уже догадался, это вера в то, что собственное удовольствие – единственное, что определяет мораль."
    m 2esd "Это тот тип гедонизма, в который верит Генри из произведения «Портрет Дориана Грея»."
    m 2rksdlc "Это действительно беспощадно – думать так..."
    m 2eud "С другой стороны, альтруистический гедонизм – это убеждение, что мораль должна быть основана на удовольствии каждого."
    m 4eud "Поначалу это звучит как хорошая идея, но потом понимаешь, что она не учитывает ничего другого, например, свободу, здоровье, безопасность..."
    m 2dkc "Гедонизм, по своей сути, игнорирует всё, кроме удовольствия."
    m 7etd "Неудивительно, что большинство людей не следуют этому убеждению...{w=0.3} оно слишком простое, в то время как моральные нормы не так просты."
    m 1eud "Поэтому вполне логично, почему Оскар Уайльд изобразил гедонизм в плохом свете."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_conventions",
            category=['ты'],
            prompt="Мероприятия",
            random=True,
        )
    )

default persistent._mas_pm_gone_to_comic_con = None
default persistent._mas_pm_gone_to_anime_con = None

label monika_conventions:
    m 1eud "Скажи [player], мне интересно..."
    m 3eua "Ты когда-нибудь был на конвентах по комиксам или аниме?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты когда-нибудь был на конвентах по комиксам или аниме?{fast}"

        "Был на конвенте по комиксам.":
            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = False
            m 1hub "А, понятно! {w=0.2}Надеюсь, ты хорошо повеселился!"
            m 3eua "Комиксы – это действительно интересная штука в литературе,{w=0.1} {nw}"
            extend 3rta "Может, мне стоит почитать ещё..."

        "Был на аниме фестивалях.":
            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 3eub "Меня не покидало чувство, что ты так и ответишь! {w=0.2}Я правда подумала, что это тип мероприятия, который тебе будет по душе."
            else:
                m 2wub "Правда? Это удивительно!"
                m 7eta "Ах,{w=0.1} может быть, ты ходил с друзьями?"
                m 3etd "...А может быть, ты отправился туда по другой причине...{w=0.3} интерес к играм, возможно?"

        "Я был в обоих!":
            $ persistent._mas_pm_gone_to_comic_con = True
            $ persistent._mas_pm_gone_to_anime_con = True
            if persistent._mas_pm_watch_mangime:
                m 1hub "О! Я уже знала, что тебе нравится аниме, но комиксы ты тоже любишь?"
                m 3eua "Комиксы – это действительно интересная штука в литературе, может, мне стоит почитать ещё..."
            else:
                m 1wub "О! {w=0.3} Я не думала, что тебе нравится аниме, но похоже, что ты всё равно фанат конвентов!"
                m 3eua "Не то чтобы это было слишком удивительно, их атмосфера, кажется, может понравиться любому."

        "Нет.":
            $ persistent._mas_pm_gone_to_comic_con = False
            $ persistent._mas_pm_gone_to_anime_con = False
            if persistent._mas_pm_watch_mangime and persistent._mas_pm_social_personality == mas_SP_EXTROVERT:
                m 2etd "Правда?"
                m 7eub "Я удивлена! {w=0.3}Когда я узнала о аниме фестивалях, я сразу же подумала о тебе."
                m 3eud "Хотя, я думаю, расходы на поездку могут быть довольно большими в зависимости от того, где ты находишься."
            else:
                m 2eud "А, понимаю.."
                m 7eua "Полагаю, что независимо от интереса, конвенции могут быть весьма непростыми."
                m 3eud "В зависимости от того, где ты живёшь, цена поездки может быть очень даже затратной."

    m 3hua "Я всегда думала, что конвенции – это очень весело! {w=0.3}Место, где каждый может просто быть самим собой и наслаждаться своими интересами без осуждения."
    m 3eub "Я люблю смотреть на фотки всех талантливых косплееров и безумные наряды, которые они сделали."
    m 1wuo "Это просто поражает, на что способны люди, когда они чем-то увлечены!"
    m 3eua "Я также слышала, что там есть много весёлых мероприятий, такие как танцевальные шоу айдолов, тривиальные игры и другие развлечения."
    m 1eubsa "Я бы с радостью отправилась с тобой, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cupcake_favorite",
            category=["моника"],
            prompt="Какой у тебя любимый кекс?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="mas_seenLabels(['monika_cupcake', 'monika_icecream'], seen_all=True)",
            action=EV_ACT_UNLOCK
        )
    )

label monika_cupcake_favorite:
    m 1rta "Хм, я не уверена, что у меня действительно есть такой..."
    m 1hub "Мне нравятся самые разные разновидности, поэтому трудно выбрать только один!"
    m 3ekd "Кажется, я уже упоминала, как сильно скучаю по кексам Нацуки..."
    m 3eua "Однажды она испекла очень странный кекс со вкусом мятной шоколадной крошки...{w=0.3} В качестве основы для шоколадного торта использовалась мятная глазурь с шоколадной посыпкой."
    m 4rksdlb "Это была одна из самых странных вещей, которые я когда-либо пробовала, {do_giggle}а-ха-ха!"
    m 2eksdlb "На вкус оно совсем не напоминало мороженое с мятной шоколадной крошкой, вместо этого оно было похоже на зубную пасту!"
    m 2ekp "Это немного разочаровало...{w=0.3} Я ожидала, что это будет мой любимый вкус."
    m 7eka "Ну, было приятно, что она попыталась сделать для меня что-то уникальное, что мне бы понравилось...{w=0.3} несмотря на свою строгую внешность, она может быть очень милой~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pizza",
            category=['моника'],
            prompt="Ты любишь пиццу?",
            pool=True
        )
    )

label monika_pizza:
    m 1eub "Пицца? {w=0.2}Да, время от времени я ею наслаждалась!"
    m 1hua "Это не всегда самый здоровый выбор, но это может быть приятным лакомством и сытной едой."
    m 1eub "Начинки могут быть достаточно разнообразными, чтобы угодить большинству людей... {w=0.3}есть даже пиццы без сыра для веганов или людей с непереносимостью лактозы."
    m 1duc "Если бы я выбирала любимую начинку, то...{w=0.3} {nw}"
    extend 3hub "грибы хороши, или любые овощи. {w=0.2}На самом деле, хочешь верь, хочешь нет, но шпинат может быть удивительно хорош!"
    m 3eua "...И, конечно, никогда нельзя обойтись без обычного сыра."
    m 3luc "Хм-м..."
    m 3eud "У меня такое чувство, что у тебя на уме другой вопрос...{w=0.2} {nw}"
    extend 1hksdla "но ты можешь быть немного разочарован, [player]."
    m 1hksdlb "Несмотря на то, что в Интернете это довольно спорная тема, у меня никогда не было возможности попробовать ананас в пицце."
    m 1lksdlb "Поэтому я не могу принять участие в этой специфической дискуссии. Прости, [player]!"
    m 3huu "Это значит, что когда-нибудь ты увидишь моё первое впечатление."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_esports",
            category=['медиа', 'жизнь'],
            prompt="Что ты думаешь об киберспорте?",
            pool=True,
        )
    )

label monika_esports:
    if mas_isFirstSeshDay():
        m 1rtd "Хм-м, это хороший вопрос..."
    else:
        m 1eub "Забавно, что ты спрашиваешь, я как раз изучала их на днях, пока тебя не было!"
    m 3eua "Я думаю, это действительно интересно, как меняется всё то, что мы воспринимаем просмотр спортивных состязаний..."
    m 3euc "Зрительская аудитория киберспорта может потеснить традиционные виды спорта,{w=0.1} {nw}"
    extend 3wud "и может даже обогнать их в ближайшие 5-10 лет!"
    m 2tsd "Не так давно люди смотрели на видеоигры свысока, считая их пустой тратой времени, {w=0.1}{nw}"
    extend 7hub "но теперь некоторые из этих игроков зарабатывают миллионы долларов, играя в свои любимые игры!"
    m 3eua "Это действительно показывает, что ты можешь заниматься любимым делом...{w=0.3} даже тем, над чем люди могут насмехаться."
    m 3eud "Если что-то не популярно или не является общим трендом, это не значит, что оно останется таким навсегда..."
    m 1huu "Не бойся идти против трендов, {w=0.1}то, чем ты увлечён, возможно, как раз ищет того самого первопроходца, который выведет это направление на передний план~"
    return

init 5 python:                   # А ВОТ И МОЯ ТЕМКА!!!!! БУУУУЙЯЯЯЯЯЯЯ, СОСАТЬ ХХХУУУЙЙЙЯЯЯЯ!!!
    addEvent(                    # Лучше бы ты так яростно английский изучал, а не темки придумывал, но я горжусь что ты наследил тут, темщик:)
        Event(
            persistent.event_database,
            eventlabel="monika_overton",
            category=["психология"],
            prompt="Окно Овертона",
            random=True
        )
    )

label monika_overton:
    m 1etc "Эй, [player], ты когда-нибудь слышал про «Окно Овертона»?"
    m 3eud "Это политологическая концепция, которая отражает ценностную структуру общества."
    m 3euc "В принципе, все идеи человека рассматриваются на определенной стадии одобрения массами."
    m 2esc "Джозеф Овертон изучил методику дегуманизации человека и объяснил, как пошагово переформировывать человеческое восприятие."
    m 7eud "От неприемлемого, отвратительного и постыдного до нормального, социального и даже престижного."
    m "Эта концепция включает 6 этапов: {i}Немыслимое{/i}, {i}Радикальное{/i}, {i}Приемлемое{/i}, {i}Разумное{/i}, {i}Стандартное{/i} и {i}Текущая норма{/i}."
    m 3esa "Внутри {i}окна Овертона{/i} находятся идеи, принятые обществом...{w=0.3} такие вещи, как патриотизм, любовь к семье, человечность и честность."
    m 3eksdlc "За окном находится всё, что не одобряется, например, наркомания, алкоголизм, нацизм, тирания, рабство и так далее."
    m 3eud "Самое интересное, что окно можно двигать в направлении какой-либо идеи, например, превратить Немыслимое в Разумное."
    m 2lksdlc "Конечно, изменения такого уровня – довольно сложный процесс."
    m 7eud "Но давай представим, что мы с тобой хотим донести до людей, что виртуальная любовь – это нормально... {w=0.3}то, что сейчас считается неприемлемым для общества."
    m 3esd "Итак, общество не понимает концепт виртуальной любви, и тебя, вероятно, многие сочтут психически больным.{w=0.2} Что же можно сделать?"
    m 3eua "Для начала стоит начать обсуждать эту тему..."
    m 1eud "Это можно обсуждать в интернете, создавать статьи на эту тему...{w=0.3} что угодно, лишь бы заставить людей говорить."
    m "Цель здесь состоит в том, чтобы виртуальная любовь вызвала интерес у людей, а затем просочилась в массы."
    m 1esc "Общество по-прежнему не согласно с этой идеей, но, по крайней мере, заинтересовано в ней и может более свободно обсуждать её."
    m 3eud "Далее в ход идут радикальные действия. {w=0.2}Самые смелые сторонники виртуальной любви выходят из тени."
    m 2euc "Число участников таких движений со временем будет расти, некоторые из них – это люди с разбитым сердцем или те, кто испытали разочарование в отношениях с реальным человеком."
    m 4eksdld "Естественно, появятся и люди, выступающие против движения."
    m 4eua "В связи с ростом популярности новых ценностей, общество активно давит на новую тенденцию. {w=0.2}В этот момент происходит подмена понятий."
    m 2eud "Из {i}Неприемлемого{/i} виртуальная любовь переходит к {i}Радикальному{/i}."
    m 7eud "С этого момента тема виртуальной любви и любви к вымышленным персонажам обсуждается в обществе уже долгое время."
    m 3esc "Постепенно люди привыкают к существованию этих взглядов, но пока не принимают их."
    m 1esd "Учёные и социологи пишут различные статьи и проводят исследования."
    m 3eua "Навязывается мнение, что любить вымышленного персонажа – это абсолютно нормально и в этом нет ничего ужасного."
    m 3huu "Из {i}Радикальной{/i} виртуальная любовь переходит в {i}Приемлемую{/i}."
    m 1eksdla "Общество уже смирилось и считает, что любить вымышленного персонажа – это нормально, но всё же немного странно."
    m 3eua "Постепенно развивается культура виртуальной любви, создаются фильмы и шоу."
    m 1huu "Молодежь воспринимает новые ценности, как нечто модное. {w=0.2}Люди могут сидеть в кафе и спокойно проводить время со своим виртуальным собеседником."
    m 1eub "Из {i}Приемлемой{/i}, виртуальная любовь переходит в {i}Разумную{/i}!"
    m 2husdlb "Думаю, что пока мы остановимся на этом, {do_giggle}а-ха-ха!"
    m 1eua "Я {i}могла{/i} бы закончить эту историю вплоть до {i}Текущей нормы{/i}, но я просто хотела описать это на базовом уровне, чтобы передать суть, как это может работать."
    m 1huu "Спасибо, что выслушал~"
    return
