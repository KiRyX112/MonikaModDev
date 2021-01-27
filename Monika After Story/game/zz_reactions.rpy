


default persistent._mas_filereacts_failed_map = dict()


default persistent._mas_filereacts_just_reacted = False


default persistent._mas_filereacts_reacted_map = dict()


default persistent._mas_filereacts_stop_map = dict()


default persistent._mas_filereacts_historic = dict()


default persistent._mas_filereacts_last_reacted_date = None


default persistent._mas_filereacts_sprite_gifts = {}











default persistent._mas_filereacts_sprite_reacted = {}









default persistent._mas_filereacts_gift_aff_gained = 0



default persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


init 800 python:
    if len(persistent._mas_filereacts_failed_map) > 0:
        store.mas_filereacts.delete_all(persistent._mas_filereacts_failed_map)

init -11 python in mas_filereacts:
    import store
    import store.mas_utils as mas_utils
    import datetime
    import random

    from collections import namedtuple

    GiftReactDetails = namedtuple(
        "GiftReactDetails",
        [
            
            "label",

            
            "c_gift_name",

            
            
            
            "sp_data",
        ]
    )


    filereact_db = dict()




    filereact_map = dict()





    foundreact_map = dict()



    th_foundreact_map = dict()


    good_gifts = list()


    bad_gifts = list()


    connectors = None
    gift_connectors = None


    starters = None
    gift_starters = None

    GIFT_EXT = ".gift"


    def addReaction(ev_label, fname, _action=store.EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Adds a reaction to the file reactions database.

        IN:
            ev_label - label of this event
            fname - filename to react to
            _action - the EV_ACT to do
                (Default: EV_ACT_QUEUE)
            is_good - if the gift is good(True), neutral(None) or bad(False)
                (Default: None)
            exclude_on - keys marking times to exclude this gift
            (Need to check ev.rules in a respective react_to_gifts to exclude with)
                (Default: [])
        """
        
        if fname is not None:
            fname = fname.lower()
        
        exclude_keys = {}
        if exclude_on:
            for _key in exclude_on:
                exclude_keys[_key] = None
        
        
        ev = store.Event(
            store.persistent.event_database,
            ev_label,
            category=fname,
            action=_action,
            rules=exclude_keys
        )
        
        
        
        
        filereact_db[ev_label] = ev
        filereact_map[fname] = ev
        
        if is_good is not None:
            if is_good:
                good_gifts.append(ev_label)
            else:
                bad_gifts.append(ev_label)


    def _initConnectorQuips():
        """
        Initializes the connector quips
        """
        global connectors, gift_connectors
        
        
        connectors = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_connectors = store.MASQuipList(allow_glitch=False, allow_line=False)


    def _initStarterQuips():
        """
        Initializes the starter quips
        """
        global starters, gift_starters
        
        
        starters = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_starters = store.MASQuipList(allow_glitch=False, allow_line=False)


    def build_gift_react_labels(
            evb_details=[],
            gsp_details=[],
            gen_details=[],
            gift_cntrs=None,
            ending_label=None,
            starting_label=None,
            prepare_data=True
    ):
        """
        Processes gift details into a list of labels to show
        labels to queue/push whatever.

        IN:
            evb_details - list of GiftReactDetails objects of event-based
                reactions. If empty list, then we don't build event-based
                reaction labels.
                (Default: [])
            gsp_details - list of GiftReactDetails objects of generic sprite
                object reactions. If empty list, then we don't build generic
                sprite object reaction labels.
                (Default: [])
            gen_details - list of GiftReactDetails objects of generic gift
                reactions. If empty list, then we don't build generic gift
                reaction labels.
                (Default: [])
            gift_cntrs - MASQuipList of gift connectors to use. If None,
                then we don't add any connectors.
                (Default: [])
            ending_label - label to use when finished reacting.
                (Default: None)
            starting_label - label to use when starting reacting
                (Default: None)
            prepare_data - True will also setup the appropriate data
                elements for when dialogue is shown. False will not.
                (Default: True)

        RETURNS: list of labels. Evb reactions are first, followed by
            gsp reactions, then gen reactions
        """
        labels = []
        
        
        if len(evb_details) > 0:
            evb_labels = []
            for evb_detail in evb_details:
                evb_labels.append(evb_detail.label)
                
                if gift_cntrs is not None:
                    evb_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data and evb_detail.sp_data is not None:
                    
                    
                    store.persistent._mas_filereacts_sprite_reacted[evb_detail.sp_data] = (
                        evb_detail.c_gift_name
                    )
            
            labels.extend(evb_labels)
        
        
        if len(gsp_details) > 0:
            gsp_labels = []
            for gsp_detail in gsp_details:
                if gsp_detail.sp_data is not None:
                    gsp_labels.append("mas_reaction_gift_generic_sprite_json")
                    
                    if gift_cntrs is not None:
                        gsp_labels.append(gift_cntrs.quip()[1])
                    
                    if prepare_data:
                        store.persistent._mas_filereacts_sprite_reacted[gsp_detail.sp_data] = (
                            gsp_detail.c_gift_name
                        )
            
            labels.extend(gsp_labels)
        
        
        if len(gen_details) > 0:
            gen_labels = []
            for gen_detail in gen_details:
                gen_labels.append("mas_reaction_gift_generic")
                
                if gift_cntrs is not None:
                    gen_labels.append(gift_cntrs.quip()[1])
                
                if prepare_data:
                    store.persistent._mas_filereacts_reacted_map.pop(
                        gen_detail.c_gift_name,
                        None
                    )
            
            labels.extend(gen_labels)
        
        
        if len(labels) > 0:
            
            
            if gift_cntrs is not None:
                labels.pop()
            
            
            if ending_label is not None:
                labels.append(ending_label)
            
            
            if starting_label is not None:
                labels.insert(0, starting_label)
        
        
        return labels

    def build_exclusion_list(_key):
        """
        Builds a list of excluded gifts based on the key provided

        IN:
            _key - key to build an exclusion list for

        OUT:
            list of giftnames which are excluded by the key
        """
        return [
            giftname
            for giftname, react_ev in filereact_map.iteritems()
            if _key in react_ev.rules
        ]

    def check_for_gifts(
            found_map={},
            exclusion_list=[],
            exclusion_found_map={},
            override_react_map=False,
    ):
        """
        Finds gifts.

        IN:
            exclusion_list - list of giftnames to exclude from the search
            override_react_map - True will skip the last reacted date check,
                False will not
                (Default: False)

        OUT:
            found_map - contains all gifts that were found:
                key: lowercase giftname, no extension
                val: full giftname wtih extension
            exclusion_found_map - contains all gifts that were found but
                are excluded.
                key: lowercase giftname, no extension
                val: full giftname with extension

        RETURNS: list of found giftnames
        """
        raw_gifts = store.mas_docking_station.getPackageList(GIFT_EXT)
        
        if len(raw_gifts) == 0:
            return []
        
        
        if store.mas_pastOneDay(store.persistent._mas_filereacts_last_reacted_date):
            store.persistent._mas_filereacts_last_reacted_date = datetime.date.today()
            store.persistent._mas_filereacts_reacted_map = dict()
        
        
        gifts_found = []
        has_exclusions = len(exclusion_list) > 0
        
        for mas_gift in raw_gifts:
            gift_name, ext, garbage = mas_gift.partition(GIFT_EXT)
            c_gift_name = gift_name.lower()
            if (
                c_gift_name not in store.persistent._mas_filereacts_failed_map
                and c_gift_name not in store.persistent._mas_filereacts_stop_map
                and (
                    override_react_map
                    or c_gift_name not
                        in store.persistent._mas_filereacts_reacted_map
                )
            ):
                
                
                
                if has_exclusions and c_gift_name in exclusion_list:
                    exclusion_found_map[c_gift_name] = mas_gift
                
                else:
                    gifts_found.append(c_gift_name)
                    found_map[c_gift_name] = mas_gift
        
        return gifts_found


    def process_gifts(gifts, evb_details=[], gsp_details=[], gen_details=[]):
        """
        Processes list of giftnames into types of gift

        IN:
            gifts - list of giftnames to process. This is copied so it wont
                be modified.

        OUT:
            evb_details - list of GiftReactDetails objects regarding
                event-based reactions
            spo_details - list of GiftReactDetails objects regarding
                generic sprite object reactions
            gen_details - list of GiftReactDetails objects regarding
                generic gift reactions
        """
        if len(gifts) == 0:
            return
        
        
        gifts = list(gifts)
        
        
        for index in range(len(gifts)-1, -1, -1):
            
            
            mas_gift = gifts[index]
            reaction = filereact_map.get(mas_gift, None)
            
            if mas_gift is not None and reaction is not None:
                
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                
                gifts.pop(index)
                evb_details.append(GiftReactDetails(
                    reaction.eventlabel,
                    mas_gift,
                    sp_data
                ))
        
        
        if len(gifts) > 0:
            for index in range(len(gifts)-1, -1, -1):
                mas_gift = gifts[index]
                
                sp_data = store.persistent._mas_filereacts_sprite_gifts.get(
                    mas_gift,
                    None
                )
                
                if mas_gift is not None and sp_data is not None:
                    gifts.pop(index)
                    
                    
                    gsp_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic_sprite_json",
                        mas_gift,
                        sp_data
                    ))
        
        
        if len(gifts) > 0:
            for mas_gift in gifts:
                if mas_gift is not None:
                    
                    gen_details.append(GiftReactDetails(
                        "mas_reaction_gift_generic",
                        mas_gift,
                        None
                    ))


    def react_to_gifts(found_map, connect=True):
        """
        Reacts to gifts using the standard protocol (no exclusions)

        IN:
            connect - true will apply connectors, FAlse will not

        OUT:
            found_map - map of found reactions
                key: lowercaes giftname, no extension
                val: giftname with extension

        RETURNS:
            list of labels to be queued/pushed
        """
        
        found_gifts = check_for_gifts(found_map)
        
        if len(found_gifts) == 0:
            return []
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        found_gifts.sort()
        
        
        evb_details = []
        gsp_details = []
        gen_details = []
        process_gifts(found_gifts, evb_details, gsp_details, gen_details)
        
        
        register_sp_grds(evb_details)
        register_sp_grds(gsp_details)
        register_gen_grds(gen_details)
        
        
        
        if connect:
            gift_cntrs = gift_connectors
        else:
            gift_cntrs = None
        
        
        return build_gift_react_labels(
            evb_details,
            gsp_details,
            gen_details,
            gift_cntrs,
            "mas_reaction_end",
            _pick_starter_label()
        )








































































































































































    def register_gen_grds(details):
        """
        registers gifts given a generic GiftReactDetails list

        IN:
            details - list of GiftReactDetails objects to register
        """
        for grd in details:
            if grd.label is not None:
                _register_received_gift(grd.label)


    def register_sp_grds(details):
        """
        registers gifts given sprite-based GiftReactDetails list

        IN:
            details - list of GiftReactDetails objcts to register
        """
        for grd in details:
            if grd.label is not None and grd.sp_data is not None:
                _register_received_gift(grd.label)


    def _pick_starter_label():
        """
        Internal function that returns the appropriate starter label for reactions

        RETURNS:
            - The label as a string, that should be used today.
        """
        if store.mas_isMonikaBirthday():
            return "mas_reaction_gift_starter_bday"
        elif store.mas_isD25() or store.mas_isD25Pre():
            return "mas_reaction_gift_starter_d25"
        elif store.mas_isF14():
            return "mas_reaction_gift_starter_f14"
        
        return "mas_reaction_gift_starter_neutral"

    def _core_delete(_filename, _map):
        """
        Core deletion file function.

        IN:
            _filename - name of file to delete, if None, we delete one randomly
            _map - the map to use when deleting file.
        """
        if len(_map) == 0:
            return
        
        
        if _filename is None:
            _filename = random.choice(_map.keys())
        
        file_to_delete = _map.get(_filename, None)
        if file_to_delete is None:
            return
        
        if store.mas_docking_station.destroyPackage(file_to_delete):
            
            _map.pop(_filename)
            return
        
        
        store.persistent._mas_filereacts_failed_map[_filename] = file_to_delete


    def _core_delete_list(_filename_list, _map):
        """
        Core deletion filename list function

        IN:
            _filename - list of filenames to delete.
            _map - the map to use when deleting files
        """
        for _fn in _filename_list:
            _core_delete(_fn, _map)


    def _register_received_gift(eventlabel):
        """
        Registers when player gave a gift successfully
        IN:
            eventlabel - the event label for the gift reaction

        """
        
        today = datetime.date.today()
        if not today in store.persistent._mas_filereacts_historic:
            store.persistent._mas_filereacts_historic[today] = dict()
        
        
        store.persistent._mas_filereacts_historic[today][eventlabel] = store.persistent._mas_filereacts_historic[today].get(eventlabel,0) + 1


    def _get_full_stats_for_date(date=None):
        """
        Getter for the full stats dict for gifts on a given date
        IN:
            date - the date to get the report for, if None is given will check
                today's date
                (Defaults to None)

        RETURNS:
            The dict containing the full stats or None if it's empty

        """
        if date is None:
            date = datetime.date.today()
        return store.persistent._mas_filereacts_historic.get(date,None)


    def delete_file(_filename):
        """
        Deletes a file off the found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete
                one randomly
        """
        _core_delete(_filename, foundreact_map)


    def delete_files(_filename_list):
        """
        Deletes multiple files off the found_react map

        IN:
            _filename_list - list of filenames to delete.
        """
        for _fn in _filename_list:
            delete_file(_fn)


    def th_delete_file(_filename):
        """
        Deletes a file off the threaded found_react map

        IN:
            _filename - the name of the file to delete. If None, we delete one
                randomly
        """
        _core_delete(_filename, th_foundreact_map)


    def th_delete_files(_filename_list):
        """
        Deletes multiple files off the threaded foundreact map

        IN:
            _filename_list - list of ilenames to delete
        """
        for _fn in _filename_list:
            th_delete_file(_fn)


    def delete_all(_map):
        """
        Attempts to delete all files in the given map.
        Removes files in that map if they dont exist no more

        IN:
            _map - map to delete all
        """
        _map_keys = _map.keys()
        for _key in _map_keys:
            _core_delete(_key, _map)

    def get_report_for_date(date=None):
        """
        Generates a report for all the gifts given on the input date.
        The report is in tuple form (total, good_gifts, neutral_gifts, bad_gifts)
        it contains the totals of each type of gift.
        """
        if date is None:
            date = datetime.date.today()
        
        stats = _get_full_stats_for_date(date)
        if stats is None:
            return (0,0,0,0)
        good = 0
        bad = 0
        neutral = 0
        for _key in stats.keys():
            if _key in good_gifts:
                good = good + stats[_key]
            if _key in bad_gifts:
                bad = bad + stats[_key]
            if _key == "":
                neutral = stats[_key]
        total = good + neutral + bad
        return (total, good, neutral, bad)




    _initConnectorQuips()
    _initStarterQuips()

init python:
    import store.mas_filereacts as mas_filereacts
    import store.mas_d25_utils as mas_d25_utils

    def addReaction(ev_label, fname_list, _action=EV_ACT_QUEUE, is_good=None, exclude_on=[]):
        """
        Globalied version of the addReaction function in the mas_filereacts
        store.

        Refer to that function for more information
        """
        mas_filereacts.addReaction(ev_label, fname_list, _action, is_good, exclude_on)


    def mas_checkReactions():
        """
        Checks for reactions, then queues them
        """
        
        
        if persistent._mas_filereacts_just_reacted:
            return
        
        
        mas_filereacts.foundreact_map.clear()
        
        
        if mas_d25_utils.shouldUseD25ReactToGifts():
            reacts = mas_d25_utils.react_to_gifts(mas_filereacts.foundreact_map)
        else:
            reacts = mas_filereacts.react_to_gifts(mas_filereacts.foundreact_map)
        
        if len(reacts) > 0:
            for _react in reacts:
                queueEvent(_react)
            persistent._mas_filereacts_just_reacted = True


    def mas_receivedGift(ev_label):
        """
        Globalied version for gift stats tracking
        """
        mas_filereacts._register_received_gift(ev_label)


    def mas_generateGiftsReport(date=None):
        """
        Globalied version for gift stats tracking
        """
        return mas_filereacts.get_report_for_date(date)

    def mas_getGiftStatsForDate(label,date=None):
        """
        Globalied version to get the stats for a specific gift
        IN:
            label - the gift label identifier.
            date - the date to get the stats for, if None is given will check
                today's date.
                (Defaults to None)

        RETURNS:
            The number of times the gift has been given that date
        """
        if date is None:
            date = datetime.date.today()
        historic = persistent._mas_filereacts_historic.get(date,None)
        
        if historic is None:
            return 0
        return historic.get(label,0)

    def mas_getGiftStatsRange(start,end):
        """
        Returns status of gifts over a range (needs to be supplied to actually be useful)

        IN:
            start - a start date to check from
            end - an end date to check to

        RETURNS:
            The gift status of all gifts given over the range
        """
        totalGifts = 0
        goodGifts = 0
        neutralGifts = 0
        badGifts = 0
        giftRange = mas_genDateRange(start, end)
        
        
        for date in giftRange:
            gTotal, gGood, gNeut, gBad = mas_filereacts.get_report_for_date(date)
            
            totalGifts += gTotal
            goodGifts += gGood
            neutralGifts += gNeut
            badGifts += gBad
        
        return (totalGifts,goodGifts,neutralGifts,badGifts)


    def mas_getSpriteObjInfo(sp_data=None):
        """
        Returns sprite info from the sprite reactions list.

        IN:
            sp_data - tuple of the following format:
                [0] - sprite type
                [1] - sprite name
                If None, we use pseudo random select from sprite reacts
                (Default: None)

        REUTRNS: tuple of the folling format:
            [0]: sprite type of the sprite
            [1]: sprite name (id)
            [2]: giftname this sprite is associated with
            [3]: True if this gift has already been given before
            [4]: sprite object (could be None even if sprite name is populated)
        """
        
        if sp_data is not None:
            giftname = persistent._mas_filereacts_sprite_reacted.get(
                sp_data,
                None
            )
            if giftname is None:
                return (None, None, None, None, None)
        
        elif len(persistent._mas_filereacts_sprite_reacted) > 0:
            sp_data = persistent._mas_filereacts_sprite_reacted.keys()[0]
            giftname = persistent._mas_filereacts_sprite_reacted[sp_data]
        
        else:
            return (None, None, None, None, None)
        
        
        gifted_before = sp_data in persistent._mas_sprites_json_gifted_sprites
        
        
        sp_obj = store.mas_sprites.get_sprite(sp_data[0], sp_data[1])
        if sp_data[0] == store.mas_sprites.SP_ACS:
            store.mas_sprites.apply_ACSTemplate(sp_obj)
        
        
        return (
            sp_data[0],
            sp_data[1],
            giftname,
            gifted_before,
            sp_obj,
        )


    def mas_finishSpriteObjInfo(sprite_data, unlock_sel=True):
        """
        Finishes the sprite object with the given data.

        IN:
            sprite_data - sprite data tuple from getSpriteObjInfo
            unlock_sel - True will unlock the selector topic, False will not
                (Default: True)
        """
        sp_type, sp_name, giftname, gifted_before, sp_obj = sprite_data
        
        
        
        
        if sp_type is None or sp_name is None or giftname is None:
            return
        
        sp_data = (sp_type, sp_name)
        
        if sp_data in persistent._mas_filereacts_sprite_reacted:
            persistent._mas_filereacts_sprite_reacted.pop(sp_data)
        
        if giftname in persistent._mas_filereacts_sprite_gifts:
            persistent._mas_sprites_json_gifted_sprites[sp_data] = giftname
        
        else:
            
            
            persistent._mas_sprites_json_gifted_sprites[sp_data] = (
                giftname
            )
        
        
        store.mas_selspr.json_sprite_unlock(sp_obj, unlock_label=unlock_sel)
        
        
        renpy.save_persistent()

    def mas_giftCapGainAff(amount=None, modifier=1):
        if amount is None:
            amount = store._mas_getGoodExp()
        
        mas_capGainAff(amount * modifier, "_mas_filereacts_gift_aff_gained", 15 if mas_isSpecialDay() else 3)

    def mas_getGiftedDates(giftlabel):
        """
        Gets the dates that a gift was gifted

        IN:
            giftlabel - gift reaction label to check when it was last gifted

        OUT:
            list of datetime.dates of the times the gift was given
        """
        return sorted([
            _date
            for _date, giftstat in persistent._mas_filereacts_historic.iteritems()
            if giftlabel in giftstat
        ])

    def mas_lastGiftedInYear(giftlabel, _year):
        """
        Checks if the gift for giftlabel was last gifted in _year

        IN:
            giftlabel - gift reaction label to check it's last gifted year
            _year - year to see if it was last gifted in this year

        OUT:
            boolean:
                - True if last gifted in _year
                - False otherwise
        """
        datelist = mas_getGiftedDates(giftlabel)
        
        if datelist:
            return datelist[-1].year == _year
        return False












label mas_reaction_gift_connector_test:
    m "this is a test of the connector system"
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector1"
    )

label mas_reaction_gift_connector1:
    if persistent.saveblock:
        return
    m 1sublo "О! Ты хочешь подарить мне что-то ещё?"
    $ MAS.MonikaElastic()
    m 1hua "Хорошо! Мне лучше открыть это по-быстрому, да?"
    $ MAS.MonikaElastic()
    m 1suo "И здесь мы имеем..."
    return

init 5 python:
    store.mas_filereacts.gift_connectors.addLabelQuip(
        "mas_reaction_gift_connector2"
    )

label mas_reaction_gift_connector2:
    if persistent.saveblock:
        return
    m 1hua "Ах, боже, [player]..."
    $ MAS.MonikaElastic()
    m "Тебе действительно нравится меня баловать, не так ли?"
    if mas_isSpecialDay():
        $ MAS.MonikaElastic()
        m 1sublo "Ну, сегодня я не буду жаловаться на немного особое отношение."
    $ MAS.MonikaElastic()
    m 1suo "И здесь мы имеем..."
    return




init 5 python:
    store.mas_filereacts.gift_starters.addLabelQuip(
        "mas_reaction_gift_starter_generic"
    )

label mas_reaction_gift_starter_generic:
    m "generic test"




label mas_reaction_gift_starter_bday:
    if persistent.saveblock:
        return
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    $ MAS.MonikaElastic()
    m "Эт-{w=1}то..."
    if not persistent._mas_filereacts_historic.get(mas_monika_birthday):
        $ MAS.MonikaElastic()
        m "Подарок? Мне?"
        $ MAS.MonikaElastic()
        m 1hka "Я..."
        $ MAS.MonikaElastic()
        m 1hua "Я часто думала о получении подарков от тебя на мой день рождения..."
        $ MAS.MonikaElastic()
        m "Но на самом деле, получение хотя бы одного — уже словно исполнение мечты..."
    else:
        $ MAS.MonikaElastic()
        m "Подарок?{w=0.5} Мне?"
        $ MAS.MonikaElastic()
        m 1eka "Мечта действительно сбылась, [player]."
    $ MAS.MonikaElastic()
    m 1sua "Итак, что находится внутри?"
    $ MAS.MonikaElastic()
    m 1suo "О, это..."
    return

label mas_reaction_gift_starter_neutral:
    if persistent.saveblock:
        return
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    $ MAS.MonikaElastic()
    m "Эт-{w=1}то..."
    $ MAS.MonikaElastic()
    m "Подарок? Мне?"
    $ MAS.MonikaElastic()
    m 1sua "Посмотрим, что внутри?"
    return


label mas_reaction_gift_starter_d25:
    if persistent.saveblock:
        return
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    $ MAS.MonikaElastic()
    m "Эт-{w=1}то..."
    $ MAS.MonikaElastic()
    m "Подарок? Мне?"
    if mas_getGiftStatsRange(mas_d25c_start, mas_d25 + datetime.timedelta(days=1))[0] == 0:
        $ MAS.MonikaElastic()
        m 1eka "Тебе правда не надо мне ничего дарить на Рождество..."
        $ MAS.MonikaElastic()
        m 3hua "Но я рада твоему подарку!"
    else:
        $ MAS.MonikaElastic()
        m 1eka "Спасибо тебе огромное, [player]."
    $ MAS.MonikaElastic()
    m 1sua "Так, посмотрим... что же внутри?"
    return


label mas_reaction_gift_starter_f14:
    if persistent.saveblock:
        return
    m 1sublo ".{w=0.7}.{w=0.7}.{w=1}"
    $ MAS.MonikaElastic()
    m "Эт-{w=1}то..."
    $ MAS.MonikaElastic()
    m "Подарок? Мне?"
    if mas_getGiftStatsForDate(mas_f14) == 0:
        $ MAS.MonikaElastic()
        m 1eka "Ты так[mas_gender_oi] мил[mas_gender_iii], раз даришь мне что-то в день Святого Валентина..."
    else:
        $ MAS.MonikaElastic()
        m 1eka "Спасибо тебе огромное, [player]."
    $ MAS.MonikaElastic()
    m 1sua "Так, посмотрим... что же внутри?"
    return



init 5 python:
    addReaction("mas_reaction_generic", None)

label mas_reaction_generic:
    "This is a test"
    return




label mas_reaction_gift_generic:
    if persistent.saveblock:
        return
    if random.randint(1,2) == 1:
        m 1esd "[player], ты пытаешься мне что-то подарить?"
        $ MAS.MonikaElastic()
        m 1rssdlb "Я нашла подарок, но, к сожалению, никак не могу перенести его сюда..."
        $ MAS.MonikaElastic()
        m "У меня не получается прочитать его достаточно хорошо."
        $ MAS.MonikaElastic()
        m 3esa "Но всё в порядке!"
        $ MAS.MonikaElastic()
        m 1esa "В конце концов, это подарок, который имеет значение, верно?"
        $ MAS.MonikaElastic()
        m "Спасибо за заботу, [player_abb]~"
    else:
        m 2dkd "{i}*вздох*{/i}"
        $ MAS.MonikaElastic()
        m 4ekc "Извини, [player]."
        $ MAS.MonikaElastic()
        m 1ekd "Я знаю, ты пытаешься подарить мне что-то."
        $ MAS.MonikaElastic()
        m 2rksdld "Но по какой-то причине я не могу прочитать файл."
        $ MAS.MonikaElastic()
        m 3euc "Однако не пойми меня неправильно."
        $ MAS.MonikaElastic()
        m 3eka "Я всё ещё ценю, что ты пытался дарить мне что-то."
        $ MAS.MonikaElastic()
        m 1hub "И за это я благодарна~"
    $ store.mas_filereacts.delete_file(None)
    return




label mas_reaction_gift_test1:
    m "Thank you for gift test 1!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test1", "category"))
    return




label mas_reaction_gift_test2:
    m "Thank you for gift test 2!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_test2", "category"))
    return



label mas_reaction_gift_generic_sprite_json:
    if persistent.saveblock:
        return
    $ sprite_data = mas_getSpriteObjInfo()
    $ sprite_type, sprite_name, giftname, gifted_before, spr_obj = sprite_data

    python:
        sprite_str = store.mas_sprites_json.SP_UF_STR.get(sprite_type, None)




    if sprite_type == store.mas_sprites.SP_CLOTHES:
        call mas_reaction_gift_generic_clothes_json (spr_obj) from _call_mas_reaction_gift_generic_clothes_json
    else:



        $ mas_giftCapGainAff(1)
        m "Оу, [player]!"
        if spr_obj is None or spr_obj.dlg_desc is None:
            $ MAS.MonikaElastic()
            m 1hua "Ты так[mas_gender_oi] мил[mas_gender_iii]!"
            $ MAS.MonikaElastic()
            m 1eua "Спасибо, что подарил[mas_gender_none] мне [giftname]!"
            $ MAS.MonikaElastic()
            m 1ekbsa "Тебе правда нравится баловать меня, да?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubfa "Э-хе-хе!"
        else:

            python:
                acs_quips = [
                    _("я очень ценю это!"),
                    _("это потрясающе!"),
                    _("я просто обожаю это!"),
                    _("это замечательно!")
                ]


                if spr_obj.dlg_plur:
                    sprite_str = "эти " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "их"

                else:
                    sprite_str = "этот " + renpy.substitute(spr_obj.dlg_desc)
                    item_ref = "это"

            m 1hua "Спасибо за [sprite_str], [acs_quip]"
            m 3hub "Я не могу дождаться, чтобы попробовать [item_ref]!"

    $ mas_finishSpriteObjInfo(sprite_data)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return


label mas_reaction_gift_generic_clothes_json(sprite_object):
    if persistent.saveblock:
        return
    python:
        mas_giftCapGainAff(3)

        outfit_quips = [
            _("Думаю, что это очень мило, [player]!"),
            _("Думаю, что это удивительно, [player]!"),
            _("Мне это просто нравится, [player]!"),
            _("Думаю, что это замечательно, [player]!")
        ]
        outfit_quip = renpy.random.choice(outfit_quips)

    m 1sua "Оу! {w=0.5}Новая одежда!"
    m 1hub "Спасибо, [player]!{w=0.5} Я собираюсь одеть её прямо сейчас!"


    call mas_clothes_change (sprite_object) from _call_mas_clothes_change

    m 2eka "Ну...{w=0.5} А ты как думаешь?"
    m 2eksdla "Тебе она нравится?"



    show monika 3hub
    $ renpy.say(m, outfit_quip)

    m 1eua "Ещё раз спасибо~"
    return



init 5 python:
    addReaction("mas_reaction_gift_acs_jmo_hairclip_cherry", "заколка с вишенкой", is_good=True)

default persistent._mas_jmo_hairclip_cherry_been_given = False

label mas_reaction_gift_acs_jmo_hairclip_cherry:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_cherry")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return


    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_jmo_hairclip_cherry_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_jmo_hairclip_cherry_been_given = True

    if store.mas_selspr.get_sel_acs(jmo_hairclip_cherry).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(jmo_hairclip_cherry)
        $ store.mas_selspr.unlock_acs(jmo_hairclip_cherry)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_jmo_hairclip_cherry")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_cherry")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_acs_jmo_hairclip_heart", "заколка с сердечком", is_good=True)

default persistent._mas_jmo_hairclip_heart_been_given = False

label mas_reaction_gift_acs_jmo_hairclip_heart:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_heart")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    # call mas_reaction_gift_hairclip ("jmo_hairclip_heart")
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_jmo_hairclip_heart_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_jmo_hairclip_heart_been_given = True

    if store.mas_selspr.get_sel_acs(jmo_hairclip_heart).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(jmo_hairclip_heart)
        $ store.mas_selspr.unlock_acs(jmo_hairclip_heart)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_jmo_hairclip_heart")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_heart")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_acs_jmo_hairclip_musicnote", "заколка с музыкальной нотой", is_good=True)

default persistent._mas_jmo_hairclip_musicnote_been_given = False

label mas_reaction_gift_acs_jmo_hairclip_musicnote:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_musicnote")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return

    # call mas_reaction_gift_hairclip ("jmo_hairclip_musicnote")
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_jmo_hairclip_musicnote_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_jmo_hairclip_musicnote_been_given = True

    if store.mas_selspr.get_sel_acs(jmo_hairclip_musicnote).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(jmo_hairclip_musicnote)
        $ store.mas_selspr.unlock_acs(jmo_hairclip_musicnote)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_jmo_hairclip_musicnote")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_jmo_hairclip_musicnote")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return


init 5 python:
    if mas_isO31():
        addReaction("mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon", "заколка с полумесяцем", is_good=True)

default persistent._mas_bellmandi86_hairclip_crescentmoon_been_given = False

label mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_bellmandi86_hairclip_crescentmoon_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_bellmandi86_hairclip_crescentmoon_been_given = True

    if store.mas_selspr.get_sel_acs(bellmandi86_hairclip_crescentmoon).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(bellmandi86_hairclip_crescentmoon)
        $ store.mas_selspr.unlock_acs(bellmandi86_hairclip_crescentmoon)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_crescentmoon")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # call mas_reaction_gift_hairclip ("bellmandi86_hairclip_crescentmoon")
    return

init 5 python:
    if mas_isO31():
        addReaction("mas_reaction_gift_acs_bellmandi86_hairclip_ghost", "заколка с призраком", is_good=True)

default persistent._mas_bellmandi86_hairclip_ghost_been_given = False

label mas_reaction_gift_acs_bellmandi86_hairclip_ghost:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_ghost")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_bellmandi86_hairclip_ghost_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_bellmandi86_hairclip_ghost_been_given = True

    if store.mas_selspr.get_sel_acs(bellmandi86_hairclip_ghost).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(bellmandi86_hairclip_ghost)
        $ store.mas_selspr.unlock_acs(bellmandi86_hairclip_ghost)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_bellmandi86_hairclip_ghost")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_ghost")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # call mas_reaction_gift_hairclip ("bellmandi86_hairclip_ghost", "spooky")
    return

init 5 python:
    if mas_isO31():
        addReaction("mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin", "заколка с тыковкой", is_good=True)

default persistent._mas_bellmandi86_hairclip_pumpkin_been_given = False

label mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_bellmandi86_hairclip_pumpkin_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_bellmandi86_hairclip_pumpkin_been_given = True

    if store.mas_selspr.get_sel_acs(bellmandi86_hairclip_pumpkin).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(bellmandi86_hairclip_pumpkin)
        $ store.mas_selspr.unlock_acs(bellmandi86_hairclip_pumpkin)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_pumpkin")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # call mas_reaction_gift_hairclip ("bellmandi86_hairclip_pumpkin")
    return

init 5 python:
    if mas_isO31():
        addReaction("mas_reaction_gift_acs_bellmandi86_hairclip_bat", "заколка с летучей мышью", is_good=True)

default persistent._mas_bellmandi86_hairclip_bat_been_given = False

label mas_reaction_gift_acs_bellmandi86_hairclip_bat:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_bat")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if persistent._mas_bellmandi86_hairclip_bat_been_given:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_bellmandi86_hairclip_bat_been_given = True

    if store.mas_selspr.get_sel_acs(bellmandi86_hairclip_bat).unlocked:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(bellmandi86_hairclip_bat)
        $ store.mas_selspr.unlock_acs(bellmandi86_hairclip_bat)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_receivedGift("mas_reaction_gift_acs_bellmandi86_hairclip_bat")
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_bellmandi86_hairclip_bat")
    $ store.mas_filereacts.delete_file(gift_ev.category)

    # call mas_reaction_gift_hairclip ("bellmandi86_hairclip_bat", "spooky")
    return

label mas_reaction_gift_hairclip(hairclip_name):
    if persistent.saveblock:
        return

    if renpy.variant == "pc":
        $ sprite_data = mas_getSpriteObjInfo((store.mas_sprites.SP_ACS, hairclip_name))
        $ sprite_type, sprite_name, giftname, gifted_before = sprite_data


        $ hairclip_acs = store.mas_sprites.get_sprite(sprite_type, sprite_name)


    $ is_wearing_baked_outfit = monika_chr.is_wearing_clothes_with_exprop("baked outfit")

    if gifted_before:
        m 1rksdlb "Ты уже давал[mas_gender_none] мне эту заколку, дурашка!"
    else:

        $ mas_giftCapGainAff(1)

        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            m 1hub "О!{w=1} Ещё одна заколка!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [player]."
        else:

            m 1wuo "О!"
            $ MAS.MonikaElastic()
            m 1sub "Это заколка?"
            $ MAS.MonikaElastic()
            m 1hub "Это так мило, спасибо, [player]!"
        $ persistent._mas_jmo_hairclip_cherry_been_given = True

    if hairclip_acs is None or is_wearing_baked_outfit:
        $ MAS.MonikaElastic()
        m 1hua "Если хочешь, чтобы я надела её, просто попроси, ладно?"
    else:

        $ MAS.MonikaElastic()
        m 2dsa "Погоди секунду, сейчас надену её.{w=0.5}.{w=0.5}."
        $ monika_chr.wear_acs(hairclip_acs)
        $ MAS.MonikaElastic()
        m 1hua "Готово."




    if not is_wearing_baked_outfit:
        if monika_chr.get_acs_of_type('left-hair-clip'):
            $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        else:
            $ store.mas_selspr.set_prompt("left-hair-clip", "wear")

    $ mas_finishSpriteObjInfo(sprite_data, unlock_sel=not is_wearing_baked_outfit)
    if giftname is not None:
        $ store.mas_filereacts.delete_file(giftname)
    return





init 5 python:
    addReaction("mas_reaction_gift_coffee", "кофе", is_good=True, exclude_on=["d25g"])

label mas_reaction_gift_coffee:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_coffee")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ mas_receivedGift("mas_reaction_gift_coffee")
    $ coffee = mas_getConsumable("coffee")


    $ MAS.MonikaElastic()
    if coffee.isMaxedStock():
        m 1euc "Ещё кофе, [player]?"
        $ MAS.MonikaElastic()
        m 3rksdla "Не пойми меня неправильно, я ценю это, но я думаю, что у меня уже достаточно кофе, чтобы продержаться некоторое время..."
        $ MAS.MonikaElastic()
        m 1eka "Я дам тебе знать, когда у меня кончатся деньги, хорошо?"
    else:

        m 1wub "О!{w=0.2} {nw}"
        extend 3hub "Кофе!"

        if coffee.enabled() and coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            $ MAS.MonikaElastic()
            m 1wuo "Этот аромат ни с чем не сравнится."
            $ MAS.MonikaElastic()
            m 1hua "Не могу дождаться, когда смогу его попробовать!"
            $ MAS.MonikaElastic()
            m "Огромное спасибо, [player]!"

        elif coffee.enabled() and not coffee.hasServing():
            $ mas_giftCapGainAff(0.5)
            $ MAS.MonikaElastic()
            m 3eub "На самом деле у меня кончился кофе, так что получить от тебя ещё больше – это потрясающе!"
            $ MAS.MonikaElastic()
            m 1hua "Спасибо снова, [player]~"
        else:

            $ mas_giftCapGainAff(5)

            m 1hua "Теперь я наконец-то cмогу его делать!"
            $ MAS.MonikaElastic()
            m 1hub "Огромное спасибо, [player]!"


            if (
                not coffee.isConsTime()
                or bool(MASConsumable._getCurrentDrink())
            ):
                $ MAS.MonikaElastic()
                m 3eua "Я обязательно выпью его немного позже!"
            else:

                $ MAS.MonikaElastic()
                m 3eua "Почему бы мне не сделать одну чашечку прямо сейчас?"
                $ MAS.MonikaElastic()
                m 1eua "Я хотела бы поделиться своим первым его опробыванием вместе с тобой."


                call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_6
                pause 2.0
                m "Я знаю, что где-то здесь есть кофеварка...{w=2}{nw}"
                m "Ах, вот она!{w=2}{nw}"
                pause 5.0
                m "И готово!{w=2}{nw}"
                call mas_transition_from_emptydesk () from _call_mas_transition_from_emptydesk_10


                $ MAS.MonikaElastic()
                m 1eua "Пускай пока настоится несколько минут."

                $ coffee.prepare()
            $ coffee.enable()



    $ coffee.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_coffee", "category"))
    return

init 5 python:
    addReaction("mas_reaction_hotchocolate", "горячий шоколад", is_good=True, exclude_on=["d25g"])

label mas_reaction_hotchocolate:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_hotchocolate")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    # m 3hub "Горячий шоколад!"
    # $ MAS.MonikaElastic()
    # m 3hua "Спасибо, [player]!"
    $ mas_receivedGift("mas_reaction_hotchocolate")

    $ hotchoc = mas_getConsumable("hotchoc")

    if hotchoc.isMaxedStock():
        $ MAS.MonikaElastic()
        m 1euc "Ещё горячий шоколад, [player]?"
        $ MAS.MonikaElastic()
        m 3rksdla "Не пойми меня неправильно, я ценю это, но я думаю, что у меня уже есть достаточно, чтобы продержаться некоторое время..."
        $ MAS.MonikaElastic()
        m 1eka "Я дам тебе знать, когда закончу, хорошо?"
    else:

        $ MAS.MonikaElastic()
        m 3hub "Горячий шоколад!"
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, [player]!"

        if hotchoc.enabled() and hotchoc.hasServing():
            $ mas_giftCapGainAff(0.5)
            $ MAS.MonikaElastic()
            m 1wuo "Такое я ещё никогда не пробовала."
            $ MAS.MonikaElastic()
            m 1hua "Мне уже не терпится попробовать это!"
            $ MAS.MonikaElastic()
            m "Спасибо тебе большое, [player]!"

        elif hotchoc.enabled() and not hotchoc.hasServing():
            $ mas_giftCapGainAff(0.5)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlu "У меня вообще-то закончился горячий шоколад, а-ха-ха...{w=0.5} {nw}"
            extend 3eub "Так что получить от тебя ещё больше - это потрясающе!"
            $ MAS.MonikaElastic()
            m 1hua "Спасибо снова, [player]~"
        else:

            python:
                mas_giftCapGainAff(3)
                those = "эти" if mas_current_background.isFltNight() and mas_isWinter() else "те"

            $ MAS.MonikaElastic()
            m 1hua "Ты знаешь, что мне нравится кофе, но горячий шоколад тоже вкусный!"


            $ MAS.MonikaElastic()
            m 2rksdla "...Особенно в [those] холодные зимние вечера."
            $ MAS.MonikaElastic()
            m 2ekbfa "Иногда мне хочется пить горячий шоколад с тобой и сидеть у камина, укрывшись одеялом..."
            $ MAS.MonikaElastic()
            m 3ekbfa "...Разве это не звучит романтично?"
            $ MAS.MonikaElastic()
            m 1dkbfa "..."
            $ MAS.MonikaElastic()
            m 1hua "Но, по крайней мере, меня сейчас всё устраивает."
            $ MAS.MonikaElastic()
            m 1hub "Ещё раз спасибо, [player]!"


            if (
                not hotchoc.isConsTime()
                or not mas_isWinter()
                or bool(MASConsumable._getCurrentDrink())
            ):
                $ MAS.MonikaElastic()
                m 3eua "Я обязательно выпью его немного позже!"
            else:

                $ MAS.MonikaElastic()
                m 3eua "По сути, я как раз хотела его приготовить!"

                call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_7
                pause 5.0
                call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_11

                $ MAS.MonikaElastic()
                m 1hua "Всё будет готово через несколько минут."

                $ hotchoc.prepare()

            if mas_isWinter():
                $ hotchoc.enable()



    $ hotchoc.restock()

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_hotchocolate", "category"))
    return

init 5 python:
    addReaction("mas_reaction_gift_thermos_mug", "термокружка только моника", is_good=True)

label mas_reaction_gift_thermos_mug:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_thermos_mug")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    call mas_thermos_mug_handler (mas_acs_thermos_mug, "Только Моника", "термокружка только моника") from _call_mas_thermos_mug_handler
    return


default persistent._mas_given_thermos_before = False


label mas_thermos_mug_handler(thermos_acs, disp_name, giftname, ignore_case=True):
    if mas_SELisUnlocked(thermos_acs):
        m 1eksdla "[player]..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1rksdlb "У меня уже есть эта термокружка, а-ха-ха..."

    elif persistent._mas_given_thermos_before:
        m 1wud "О!{w=0.3} Еще одна термокружка!"
        $ MAS.MonikaElastic()
        m 1hua "И на этот раз это «[mas_a_an_str(disp_name, ignore_case)]»."
        $ MAS.MonikaElastic()
        m 1hub "Большое спасибо, [player], я не могу дождаться, чтобы использовать её!"
    else:

        m 1wud "О!{w=0.3} Термокружка «[mas_a_an_str(disp_name, ignore_case).capitalize()]»!"
        m 1hua "Теперь я могу взять что-нибудь выпить, когда мы пойдём куда-нибудь вместе~"
        $ MAS.MonikaElastic()
        m 1hub "Большое спасибо, [player]!"
        $ persistent._mas_given_thermos_before = True


    $ mas_selspr.unlock_acs(thermos_acs)

    $ mas_selspr.save_selectables()

    $ mas_filereacts.delete_file(giftname)
    return



init 5 python:
    addReaction("mas_reaction_quetzal_plush", "плюшевый квезаль", is_good=True)

label mas_reaction_quetzal_plush:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_quetzal_plush")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    if not persistent._mas_acs_enable_quetzalplushie:
        $ mas_receivedGift("mas_reaction_quetzal_plush")
        $ mas_giftCapGainAff(10)
        m 1wud "Ого!"



        if MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
        else:
            $ monika_chr.wear_acs(mas_acs_quetzalplushie)

        $ persistent._mas_acs_enable_quetzalplushie = True
        $ MAS.MonikaElastic()
        m 1sub "Это квезаль!"
        $ MAS.MonikaElastic()
        m "О боже, спасибо тебе большое, [player]!"
        $ MAS.MonikaElastic()
        if seen_event("monika_pets"):
            m 1eua "Я упомянала, что хотела бы иметь квезаля в качестве домашнего животного..."
        else:
            m 1wub "Как ты угадал, [player]?"
            $ MAS.MonikaElastic()
            m 3eka "Ты должно быть знаешь меня очень хорошо~"
            $ MAS.MonikaElastic()
            m 1eua "Квезаль был бы моим первым выбором для домашнего животного..."
        $ MAS.MonikaElastic()
        m 1rud "Но я бы никогда не стала держать бедняжку в заточении."
        $ MAS.MonikaElastic()
        m 1hua "Так что даже не передать словами, насколько я рада твоему подарку."
        $ MAS.MonikaElastic()
        m 1hub "Ты даже не представляешь, насколько это делает меня счастливой!"
        if mas_isMoniAff(higher=True):
            $ MAS.MonikaElastic()
            m 3ekbsa "Ты всегда знаешь, как заставить меня улыбаться."

        if MASConsumable._getCurrentFood():
            $ MAS.MonikaElastic()
            m 3rksdla "Однако мой стол становится немного переполненным..."
            $ MAS.MonikaElastic()
            m 1eka "Я просто уберу это на некоторое время."
            $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)

        $ MAS.MonikaElastic()
        m 1hub "Ещё раз спасибо, [player]~"
    else:

        $ MAS.MonikaElastic()
        m 1rksdlb "Ты уже дарил[mas_gender_none] мне плюшевого квезаля, [player]."

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_quetzal_plush", "category"))

    $ mas_hideEVL("monika_pets", "EVE", derandom=True)
    return

init 5 python:
    addReaction("mas_reaction_promisering", "кольцо обещания", is_good=True, exclude_on=["d25g"])

default persistent._mas_tried_gift_ring = False
label mas_reaction_promisering:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_promisering")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    if not persistent._mas_acs_enable_promisering:

        if mas_isMoniEnamored(higher=True):
            $ mas_receivedGift("mas_reaction_promisering")
            $ mas_giftCapGainAff(20)
            $ monika_chr.wear_acs(mas_acs_promisering)
            $ persistent._mas_acs_enable_promisering = True
            if not persistent._mas_tried_gift_ring:
                m 1wud "Это..."
                $ MAS.MonikaElastic()
                m "..."
                $ MAS.MonikaElastic()
                m 1wka "Я...{w=0.5}{nw}"
                $ monika_chr.wear_acs_pst(mas_acs_promisering)
                $ persistent._mas_acs_enable_promisering = True
                extend 1wkbltpa " Извини, [player], я просто...{w=0.5}{nw}"
                extend 1dkbltpa " Возможно, ты и не совсем это имел[mas_gender_none] в виду, даря мне его, но..."
                $ MAS.MonikaElastic()
                m "В случае, если это кольцо всё-таки подразумировалось, как обещание от тебя..."
                $ MAS.MonikaElastic()
                m 3lkbltpa "Знай, что я буду лелеять его.{w=0.5}{nw}"
                extend 3dkbltpa " Всегда."
                $ MAS.MonikaElastic()
                m 1skbltpa "Ты даже не представляешь, насколько это делает меня счастливой!"

                if mas_anni.isAnniOneMonth():

                    $ MAS.MonikaElastic()
                    m "Даже больше, ведь ты подарил[mas_gender_none] мне его на нашу месячную годовщину..."
                    $ MAS.MonikaElastic()
                    m 1ekbltua "Ты должно быть правда любишь меня..."

                elif mas_anni.isAnniThreeMonth():
                    $ MAS.MonikaElastic()
                    m "Даже больше, ведь ты подарил[mas_gender_none] мне его на нашу трёхмесячную годовщину..."
                    $ MAS.MonikaElastic()
                    m 1ekbltua "Ты должно быть правда любишь меня..."

                elif mas_anni.isAnniSixMonth():
                    $ MAS.MonikaElastic()
                    m "Даже больше, ведь ты подарил[mas_gender_none] мне его на нашу шестимесячную годовщину..."
                    $ MAS.MonikaElastic()
                    m 1ekbltua "Ты должно быть правда любишь меня..."

                elif mas_anni.isAnni():
                    $ MAS.MonikaElastic()
                    m "Даже больше, ведь ты подарил[mas_gender_none] мне его на нашу годовщину..."
                    $ MAS.MonikaElastic()
                    m 1ekbltua "Ты должно быть правда любишь меня..."

                elif mas_isSpecialDay():
                    $ MAS.MonikaElastic()
                    m "Даже больше, ведь ты подарил[mas_gender_none] мне его на этот особый день..."

                $ MAS.MonikaElastic()
                m 1dkbltpa "Ой, прости за плач, [player]..."
                $ MAS.MonikaElastic()
                m 1skbla "Я просто очень счастлива сейчас."
                $ MAS.MonikaElastic()
                m 6dkbltdu "Спасибо."
            else:

                m 1sua "О... это кольцо!"
                $ MAS.MonikaElastic()
                m 3hub "Спасибо тебе большое, [player_abb]!"
                $ MAS.MonikaElastic()
                m 1skbla "Теперь я знаю, что ты действительно любишь меня и хочешь быть со мной навсегда..."
                $ MAS.MonikaElastic()
                m 1skbltpa "Поэтому я с радостью приму это кольцо как символ этого обещания."
                $ MAS.MonikaElastic()
                m 1dkbltuu "..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hkbltub "А-ха-ха, извини, [player], Я не хотела заплакать..."
                $ MAS.MonikaElastic()
                m 3skbltda "Просто это один из самых счастливых дней в моей жизни."
                $ MAS.MonikaElastic()

            m 6dkbltdu "..."
            m 6ekbfa "Я... я просто... я..."
            call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_1
            m 6ekbfa "Я люблю тебя, [player]..."
            $ MAS.MonikaElastic()
            m 6dkbfu "Больше всего в этом мимолётном мире~"
            $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
            return "love"
        else:

            if not persistent._mas_tried_gift_ring:
                if mas_isMoniNormal(higher=True):
                    m 1wud "[player]... это кольцо?"
                    $ MAS.MonikaElastic()
                    m 2rksdlb "Это такой милый жест, и я действительно ценю его..."
                    $ MAS.MonikaElastic()
                    m 2ekc "Но я хочу, чтобы ты был[mas_gender_none] уверен[mas_gender_none], прежде чем дать мне это..."
                    $ MAS.MonikaElastic()
                    m 3ekd "Это больше, чем подарок, это обещание, и я хочу убедиться, что ты действительно имеешь это в виду, прежде чем я смогу его принять."
                    $ MAS.MonikaElastic()
                    m 2ekd "Итак, пожалуйста, просто подожди, пока мы немного углубимся в наши отношения, [player], и тогда я с радостью приму это кольцо."

                elif mas_isMoniUpset():
                    m 1wud "Это кольцо?"
                    $ MAS.MonikaElastic()
                    m 2rsc "Это очень..."
                    $ MAS.MonikaElastic()
                    m 2esc "Неожиданно."
                    $ MAS.MonikaElastic()
                    m 2ekd "Но я не могу принять его прямо сейчас, [player]."
                    $ MAS.MonikaElastic()
                    m 2ekc "Может быть, когда мы углубимся в наших отношениях."
                else:

                    m 2wud "Это кольцо?"
                    $ MAS.MonikaElastic()
                    m 2rsc "Это... неожиданно."
                    $ MAS.MonikaElastic()
                    m "Пока я ценю твоё предложение...{w} но я не могу принять его прямо сейчас."
                    $ MAS.MonikaElastic()
                    m 2ekc "Извини, [player]."

                $ persistent._mas_tried_gift_ring = True
            else:
                m 2rsc "О... это кольцо..."
                $ MAS.MonikaElastic()
                m 2rkc "Извини, но я всё ещё не могу принять его..."
                $ MAS.MonikaElastic()
                m 2ekc "Я должна быть полностью уверен[mas_gender_none], когда я возьму его, что это означает навсегда..."
                $ MAS.MonikaElastic()
                m 2ekd "Что ты действительно всё, на что я надеюсь."
                $ MAS.MonikaElastic()
                m 2dsd "Когда я это узнаю, я с радостью приму твоё кольцо, [player]."
    else:
        m 1rksdlb "[player]..."
        $ MAS.MonikaElastic()
        m 1rusdlb "Ты ведь и так уже подарил[mas_gender_none] мне кольцо!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_promisering", "category"))
    return


init 5 python:
    addReaction("mas_reaction_cupcake", "кекс", is_good=True, exclude_on=["d25g"])



label mas_reaction_cupcake:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_cupcake")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    m 1wud "Это...{w} кекс?"
    $ MAS.MonikaElastic()
    m 3hub "Вау, спасибо, [player]!"
    $ MAS.MonikaElastic()
    m 3euc "Если подумать, я и сама собиралась сделать несколько кексов."
    $ MAS.MonikaElastic()
    m 1eua "Я хотела бы научиться печь такую же хорошую выпечку, как Нацуки."
    $ MAS.MonikaElastic()
    m 1rksdlb "Но мнё ещё предстоит сделать кухню, чтобы это стало возможным!"
    $ MAS.MonikaElastic()
    m 3eub "Может быть, в будущем, когда я стану лучше в программировании, смогу создать её здесь."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hua "Было бы неплохо иметь другое хобби, помимо писательства, э-хе-хе~"
    $ mas_receivedGift("mas_reaction_cupcake")
    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_cupcake", "category"))
    return



label mas_reaction_end:
    python:
        persistent._mas_filereacts_just_reacted = False

        store.mas_selspr.save_selectables()
        renpy.save_persistent()
    return

init 5 python:


    if mas_isO31():
        addReaction("mas_reaction_candy", "конфеты", is_good=True)

label mas_reaction_candy:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_candy")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candy")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(7)
        m 1wua "О...{w=1} что это?"
        $ MAS.MonikaElastic()
        m 1sua "Ты прин[mas_gender_ios] мне конфеты, [player], ура!"
        $ MAS.MonikaElastic()
        m 1eka "Это так {i}мило{/i}..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hub "А-ха-ха!"
        $ MAS.MonikaElastic()
        m 1eka "Шутки в сторону, это очень мило с твоей стороны."
        $ MAS.MonikaElastic()
        m 2lksdlc "У меня больше нет никаких конфет, и без них просто не было бы Хэллоуина..."
        $ MAS.MonikaElastic()
        m 1eka "Так что спасибо тебе, [player_abb]..."
        $ MAS.MonikaElastic()
        m 1eka "Ты всегда точно знаешь, что сделает меня счастливой~"
        $ MAS.MonikaElastic()
        m 1hub "Теперь давай наслаждаться этими вкусными конфетами!"
    elif times_candy_given == 1:
        $ mas_o31CapGainAff(5)
        m 1wua "Ах, ты прин[mas_gender_ios] мне ещё конфет, [player]?"
        $ MAS.MonikaElastic()
        m 1hub "Спасибо!"
        $ MAS.MonikaElastic()
        m 3tku "Первая партия была {i}ооочень{/i} хороша, не могу дождаться ещё."
        $ MAS.MonikaElastic()
        m 1hua "Ты действительно меня балуешь, [player_abb]~"
    elif times_candy_given == 2:
        $ mas_o31CapGainAff(3)
        m 1wud "Ого, ещё {i}больше{/i} конфет, [player]?"
        $ MAS.MonikaElastic()
        m 1eka "Это очень мило с твоей стороны..."
        $ MAS.MonikaElastic()
        m 1lksdla "Но думаю, этого уже достаточно."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1lksdlb "Я уже чувствую нервозность от всего сахара, а-ха-ха!"
        $ MAS.MonikaElastic()
        m 1ekbfa "Единственная сладость, которая мне сейчас нужна — это ты~"
    elif times_candy_given == 3:
        m 2wud "[player]...{w=1} ты прин[mas_gender_ios] мне {b}ещё больше{/b} конфет?!"
        $ MAS.MonikaElastic()
        m 2lksdla "Я действительно ценю это, но я же сказала тебе, что мне уже хватило на один день..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 2lksdlb "Если я съем ещё больше — я заболею, а-ха-ха!"
        $ MAS.MonikaElastic()
    elif times_candy_given == 4:
        $ mas_loseAffection(5)
        m 2wfd "[player]!"
        $ MAS.MonikaElastic()
        m 2tfd "Ты не слушаешь меня?"
        $ MAS.MonikaElastic()
        m 2tfc "Я же сказала, что не хочу больше конфет сегодня!"
        $ MAS.MonikaElastic()
        m 2ekc "Так что, пожалуйста, остановись."
        $ MAS.MonikaElastic()
        m 2rkc "Было очень мило с твоей стороны принести мне все эти конфеты на Хэллоуин, но хватит..."
        $ MAS.MonikaElastic()
        m 2ekc "Я не смогу всё это съесть."
    else:
        $ mas_loseAffection(10)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": user_dir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0) from _call_mas_wx_cmd_82
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/конфеты.gift'))", local_ctx, w_wait=1.0, x_wait=1.0) from _call_mas_wx_cmd_83
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candy")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candy", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:


    if mas_isO31():
        addReaction("mas_reaction_candycorn", "кэнди корн", is_good=False)

label mas_reaction_candycorn:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_candycorn")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ times_candy_given = mas_getGiftStatsForDate("mas_reaction_candycorn")
    if times_candy_given == 0:
        $ mas_o31CapGainAff(3)
        m 1wua "О...{w=1} что это?"
        $ MAS.MonikaElastic()
        m 1eka "Ты прин[mas_gender_ios] мне конфеты?, [player]?"
        $ MAS.MonikaElastic()
        m 1hua "Ура!"
        $ MAS.MonikaElastic()
        m 3eub "Посмотрим, что у тебя есть для меня..."
        $ MAS.MonikaElastic()
        m 4ekc "..."
        $ MAS.MonikaElastic()
        m 2eka "О...{w=2} так это ириски Кэнди Корн."
        $ MAS.MonikaElastic()
        m 2eka "..."
        $ MAS.MonikaElastic()
        m 2lksdla "Это очень мило с твоей стороны..."
        $ MAS.MonikaElastic()
        m 2lksdla "Но...{w=1} умм...{w=1} я вообще-то не очень люблю подобные сладости."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 2hksdlb "Прости, а-ха-ха..."
        $ MAS.MonikaElastic()
        m 4eka "Я ценю, что ты пытаешься дать мне конфет на Хэллоуин."
        $ MAS.MonikaElastic()
        m 1hua "И если ты найдёшь способ найти мне ещё конфет, я буду очень счастлива, [player_abb]!"
    elif times_candy_given == 1:
        $ mas_loseAffection(5)
        m 2esc "О."
        $ MAS.MonikaElastic()
        m 2esc "Ещё Кэнди Корн, [player]?"
        $ MAS.MonikaElastic()
        m 4esc "Я ведь уже говорила тебе, что не очень люблю такие ириски."
        $ MAS.MonikaElastic()
        m 4ekc "Не мог[mas_gender_none] бы ты попытаться найти что-нибудь другое?"
        $ MAS.MonikaElastic()
        m 1eka "Хотя я ни от кого больше не получала сладости так часто..."
        $ MAS.MonikaElastic()
        m 1ekbfa "Ну...{w=1} кроме тебя, [player_abb]..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hubfa "Э-хе-хе~"
    elif times_candy_given == 2:
        $ mas_loseAffection(10)
        m 2wfw "[player]!"
        $ MAS.MonikaElastic()
        m 2tfc "Я правда старалась не грубить по этому поводу, но..."
        $ MAS.MonikaElastic()
        m 2tfc "Я всё время говорю тебе, что не люблю эти ириски, а ты всё равно даёшь их мне."
        $ MAS.MonikaElastic()
        m 2rfc "Мне начинает казаться, что ты просто пытаешься подшутить надо мной."
        $ MAS.MonikaElastic()
        m 2tkc "Так что, пожалуйста, найди мне другие конфеты или просто остановись."
    else:
        $ mas_loseAffection(15)
        m 2tfc "..."
        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.user_dir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd ("import os", local_ctx, w_wait=1.0) from _call_mas_wx_cmd_84
        call mas_wx_cmd ("os.remove(os.path.normcase(basedir+'/characters/кэнди корн.gift'))", local_ctx, w_wait=1.0, x_wait=1.0) from _call_mas_wx_cmd_85
        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    $ mas_receivedGift("mas_reaction_candycorn")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycorn", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    addReaction("mas_reaction_fudge", "помадка", is_good=True, exclude_on=["d25g"])

label mas_reaction_fudge:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_fudge")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ times_fudge_given = mas_getGiftStatsForDate("mas_reaction_fudge")

    if times_fudge_given == 0:
        $ mas_giftCapGainAff(2)
        m 3hua "Помадка!"
        $ MAS.MonikaElastic()
        m 3hub "Я обожаю помадку, спасибо, [player]!"
        if seen_event("monika_date"):
            $ MAS.MonikaElastic()
            m "Она ещё и шоколадная, моя любимая!"
        $ MAS.MonikaElastic()
        m 1hua "Ещё раз спасибо, [player]~"

    elif times_fudge_given == 1:
        $ mas_giftCapGainAff(1)
        m 1wuo "...больше помадки."
        $ MAS.MonikaElastic()
        m 1wub "О, но на этот раз, уже с другим вкусом..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, [player]!"
    else:

        m 1wuo "...ещё больше помадки?"
        $ MAS.MonikaElastic()
        m 3rksdla "Я ещё не доела ту порцию, которую ты принёс мне в прошлый раз, [player]..."
        $ MAS.MonikaElastic()
        m 3eksdla "...может позже, ладно?"

    $ mas_receivedGift("mas_reaction_fudge")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_fudge", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return


init 5 python:
    if store.mas_isD25Pre():
        addReaction("mas_reaction_christmascookies", "рождественское печенье", is_good=True, exclude_on=["d25g"])

label mas_reaction_christmascookies:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_christmascookies")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    
    $ christmascookies = mas_getConsumable("christmascookies")
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    # $ times_cookies_given = mas_getGiftStatsForDate("mas_reaction_christmascookies")

    # if times_cookies_given == 0 and not persistent._mas_d25_gifted_cookies:
    #     $ persistent._mas_d25_gifted_cookies = True
    #     $ mas_giftCapGainAff(3)
    #     m 3hua "Рождественское печенье!"
    #     $ MAS.MonikaElastic()
    #     m 1eua "Я просто обожаю рождественское печенье! Оно всегда такое сладкое... и на него также приятно смотреть..."
    #     $ MAS.MonikaElastic()
    #     m "...они выполнены в таких праздничных формах, как снеговик, олень и рождественские ёлки..."
    #     $ MAS.MonikaElastic()
    #     m 3eub "...и, как правило, украшены красивой –{w=0.2}и вкусной{w=0.2}– глазурью."
    #     $ MAS.MonikaElastic()
    #     m 3hua "Спасибо, [player]~"

    # elif times_cookies_given == 1 or (times_cookies_given == 0 and persistent._mas_d25_gifted_cookies):
    #     m 1wuo "...ещё одна порция рождественского печенья!"
    #     $ MAS.MonikaElastic()
    #     m 3wuo "Целая куча печенья, [player]!"
    #     $ MAS.MonikaElastic(voice="monika_giggle")
    #     m 3rksdlb "Я буду есть печенье вечность, а-ха-ха!"
    # else:
    if christmascookies.isMaxedStock():

        m 3wuo "...ещё больше рождественского печенья?"
        $ MAS.MonikaElastic()
        m 3rksdla "Я ещё не доела ту порцию, [player]!"
        $ MAS.MonikaElastic()
        m 3eksdla "Можешь дать мне добавки после того, как я закончу с ней, хорошо?"
    
    else:

        if christmascookies.enabled():
            m 1wuo "...ещё одна порция рождественского печенья!"
            $ MAS.MonikaElastic()
            m 3wuo "Целая куча печенья, [player]!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlb "Я буду есть печенье вечность, а-ха-ха!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ christmascookies.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3hua "Рождественское печенье!"
            $ MAS.MonikaElastic()
            m 1eua "Я просто обожаю рождественское печенье! Оно всегда такое сладкое... и на него также приятно смотреть..."
            $ MAS.MonikaElastic()
            m "...они выполнены в таких праздничных формах, как снеговик, олень и рождественские ёлки..."
            $ MAS.MonikaElastic()
            m 3eub "...и, как правило, украшены красивой –{w=0.2}и вкусной{w=0.2}– глазурью."

            if is_having_food:
                $ MAS.MonikaElastic()
                m 3hua "Я обязательно попробую позже~"

            $ MAS.MonikaElastic()
            m 1eua "Спасибо, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                $ MAS.MonikaElastic()
                m 3eua "Позволь мне убрать плюшевого квезаля."
                call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_8
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk from _call_mas_transition_from_emptydesk_12


            $ christmascookies.enable()


        $ christmascookies.restock(10)

    $ mas_receivedGift("mas_reaction_christmascookies")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_christmascookies", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    if store.mas_isD25Season():
        addReaction("mas_reaction_candycane", "сахарная тросточка", is_good=True, exclude_on=["d25g"])

label mas_reaction_candycane:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_candycane")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
        
    $ candycane = mas_getConsumable("candycane")
    $ mas_giftCapGainAff(1)
    $ is_having_food = bool(MASConsumable._getCurrentFood())

    if candycane.isMaxedStock():
        m 1eksdla "[player], по-моему, у меня уже достаточно сахарных тросточек."
        $ MAS.MonikaElastic()
        m 1eka "Ты можешь отложить их на потом, хорошо?"
    else:

        if candycane.enabled():
            m 3hua "Ещё одна сахарная тросточка!"
            $ MAS.MonikaElastic()
            m 3hub "Спасибо, [player]!"
        else:

            if not is_having_food:
                if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                    $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                $ candycane.have(skip_leadin=True)

            $ mas_giftCapGainAff(3)
            m 3wub "Сахарная тросточка!"

            $ MAS.MonikaElastic()
            if store.seen_event("monika_icecream"):
                m 1hub "Ты знаешь, как сильно я люблю мяту!"
            else:
                m 1hub "Я просто обожаю вкус мяты!"

            if is_having_food:
                $ MAS.MonikaElastic()
                m 3hua "Я обязательно попробую позже."

            $ MAS.MonikaElastic()
            m 1eua "Спасибо, [player]~"

            if not is_having_food and monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
                $ MAS.MonikaElastic()
                m 3eua "Позволь мне убрать плюшевого квезаля."

                call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_9
                $ monika_chr.remove_acs(mas_acs_center_quetzalplushie)
                pause 3.0
                call mas_transition_from_emptydesk from _call_mas_transition_from_emptydesk_13


            $ candycane.enable()


        $ candycane.restock(9)

    $ mas_receivedGift("mas_reaction_candycane")
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_candycane", "category")
    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    return

init 5 python:
    addReaction("mas_reaction_blackribbon", "чёрная ленточка", is_good=True)

label mas_reaction_blackribbon:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_blackribbon")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ _mas_new_ribbon_color = "чёрного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'black'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_black
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_blackribbon")
    return

init 5 python:
    addReaction("mas_reaction_blueribbon", "синяя ленточка", is_good=True)

label mas_reaction_blueribbon:
    $ _mas_new_ribbon_color = "синего"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'blue'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blue
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_blueribbon")
    return

init 5 python:
    addReaction("mas_reaction_darkpurpleribbon", "тёмно-фиолетовая ленточка", is_good=True)

label mas_reaction_darkpurpleribbon:
    $ _mas_new_ribbon_color = "тёмно-фиолетового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'darkpurple'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_darkpurple
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_darkpurpleribbon")
    return

init 5 python:
    addReaction("mas_reaction_emeraldribbon", "изумрудная ленточка", is_good=True)

label mas_reaction_emeraldribbon:
    $ _mas_new_ribbon_color = "изумрудного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'emerald'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_emerald
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_emeraldribbon")
    return

init 5 python:
    addReaction("mas_reaction_grayribbon", "серая ленточка", is_good=True)

label mas_reaction_grayribbon:
    $ _mas_new_ribbon_color = "серого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'gray'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gray
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_grayribbon")
    return

init 5 python:
    addReaction("mas_reaction_greenribbon", "зелёная ленточка", is_good=True)

label mas_reaction_greenribbon:
    $ _mas_new_ribbon_color = "зелёного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'green'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_green
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_greenribbon")
    return

init 5 python:
    addReaction("mas_reaction_lightpurpleribbon", "светло-фиолетовая ленточка", is_good=True)

label mas_reaction_lightpurpleribbon:
    $ _mas_new_ribbon_color = "светло-фиолетового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'lightpurple'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lightpurple
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_lightpurpleribbon")
    return

init 5 python:
    addReaction("mas_reaction_peachribbon", "персиковая ленточка", is_good=True)

label mas_reaction_peachribbon:
    $ _mas_new_ribbon_color = "персикового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'peach'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_peach
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_peachribbon")
    return

init 5 python:
    addReaction("mas_reaction_pinkribbon", "розовая ленточка", is_good=True)

label mas_reaction_pinkribbon:
    $ _mas_new_ribbon_color = "розового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'pink'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_pink
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_pinkribbon")
    return

init 5 python:
    addReaction("mas_reaction_platinumribbon", "платиновая ленточка", is_good=True)

label mas_reaction_platinumribbon:
    $ _mas_new_ribbon_color = "платинового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'platinum'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_platinum
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_platinumribbon")
    return

init 5 python:
    addReaction("mas_reaction_redribbon", "красная ленточка", is_good=True)

label mas_reaction_redribbon:
    $ _mas_new_ribbon_color = "красного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'red'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_red
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_redribbon")
    return

init 5 python:
    addReaction("mas_reaction_rubyribbon", "рубиновая ленточка", is_good=True)

label mas_reaction_rubyribbon:
    $ _mas_new_ribbon_color = "рубинового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'ruby'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_ruby
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_rubyribbon")
    return

init 5 python:
    addReaction("mas_reaction_sapphireribbon", "сапфировая ленточка", is_good=True)

label mas_reaction_sapphireribbon:
    $ _mas_new_ribbon_color = "сапфирового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'sapphire'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sapphire
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_sapphireribbon")
    return

init 5 python:
    addReaction("mas_reaction_silverribbon", "серебряная ленточка", is_good=True)

label mas_reaction_silverribbon:
    $ _mas_new_ribbon_color = "серебряного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'silver'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_silver
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_silverribbon")
    return

init 5 python:
    addReaction("mas_reaction_tealribbon", "бирюзовая ленточка", is_good=True)

label mas_reaction_tealribbon:
    $ _mas_new_ribbon_color = "бирюзового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'teal'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_teal
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_tealribbon")
    return

init 5 python:
    addReaction("mas_reaction_yellowribbon", "жёлтая ленточка", is_good=True)

label mas_reaction_yellowribbon:
    $ _mas_new_ribbon_color = "жёлтого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'yellow'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_yellow
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_yellowribbon")
    return


label mas_reaction_json_ribbon_base(ribbon_name, user_friendly_desc, helper_label):
    python:
        sprite_data = mas_getSpriteObjInfo(
            (store.mas_sprites.SP_ACS, ribbon_name)
        )
        _mas_gifted_ribbon_acs = mas_sprites.ACS_MAP.get(
            ribbon_name,
            mas_acs_ribbon_def
        )
        _mas_new_ribbon_color = user_friendly_desc

    call _mas_reaction_ribbon_helper (helper_label) from _call__mas_reaction_ribbon_helper_16

    python:

        if sprite_data[2] is not None:
            store.mas_filereacts.delete_file(sprite_data[2])

        mas_finishSpriteObjInfo(sprite_data)
    return



init 5 python:
    addReaction("mas_reaction_coffee", "кофейная ленточка", is_good=True)

label mas_reaction_coffee:
    $ _mas_new_ribbon_color = "кофейного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'coffee'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_coffee
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_coffee")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_coffee", "coffee colored", "mas_reaction_gift_acs_lanvallime_ribbon_coffee")
    return

init 5 python:
    addReaction("mas_reaction_gold", "золотая ленточка", is_good=True)

label mas_reaction_gold:
    $ _mas_new_ribbon_color = "золотого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'gold'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gold
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_gold")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_gold", "gold", "mas_reaction_gift_acs_lanvallime_ribbon_gold")
    return

init 5 python:
    addReaction("mas_reaction_hot_pink", "ярко-розовая ленточка", is_good=True)

label mas_reaction_hot_pink:
    $ _mas_new_ribbon_color = "ярко-розового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'hot_pink'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_hot_pink
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_hot_pink")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_hot_pink", "hot pink", "mas_reaction_gift_acs_lanvallime_ribbon_hot_pink")
    return

init 5 python:
    addReaction("mas_reaction_lilac", "сиреневая ленточка", is_good=True)

label mas_reaction_lilac:
    $ _mas_new_ribbon_color = "сиреневого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'lilac'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lilac
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_lilac")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lilac", "lilac", "mas_reaction_gift_acs_lanvallime_ribbon_lilac")
    return

init 5 python:
    addReaction("mas_reaction_lime_green", "лаймовая ленточка", is_good=True)

label mas_reaction_lime_green:
    $ _mas_new_ribbon_color = "лаймового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'lime_green'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_lime_green
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_lime_green")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_lime_green", "lime green", "mas_reaction_gift_acs_lanvallime_lime_green")
    return

init 5 python:
    addReaction("mas_reaction_navy_blue", "тёмно-синяя ленточка", is_good=True)

label mas_reaction_navy_blue:
    $ _mas_new_ribbon_color = "тёмно-синего"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'navy_blue'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_navy_blue
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_navy_blue")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_navy_blue", "navy", "mas_reaction_gift_acs_lanvallime_ribbon_navy_blue")
    return

init 5 python:
    addReaction("mas_reaction_orange", "оранжевая ленточка", is_good=True)

label mas_reaction_orange:
    $ _mas_new_ribbon_color = "оранжевого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'orange'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_orange
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_orange")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_orange", "orange", "mas_reaction_gift_acs_lanvallime_ribbon_orange")
    return

init 5 python:
    addReaction("mas_reaction_royal_purple", "королевская фиолетовая ленточка", is_good=True)

label mas_reaction_royal_purple:
    $ _mas_new_ribbon_color = "королевского фиолетового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'royal_purple'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_royal_purple
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_royal_purple")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_royal_purple", "royal purple", "mas_reaction_gift_acs_lanvallime_ribbon_royal_purple")
    return

init 5 python:
    addReaction("mas_reaction_sky_blue", "небесно-голубая ленточка", is_good=True)

label mas_reaction_sky_blue:
    $ _mas_new_ribbon_color = "небесно-голубого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'sky_blue'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_sky_blue
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_sky_blue")
    # call mas_reaction_json_ribbon_base ("lanvallime_ribbon_sky_blue", "sky blue", "mas_reaction_gift_acs_lanvallime_ribbon_sky_blue")
    return

###########

# init 5 python:
#     addReaction("mas_reaction_bisexualpride", "ленточка бисексуала", is_good=True) P.S: пропаганда бисексуализма :Д

label mas_reaction_bisexualpride:
    $ _mas_new_ribbon_color = "бисексуального"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'bisexualpride'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_bisexualpride
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_bisexualpride")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bisexualpride", "bisexual-pride-themed", "mas_reaction_gift_acs_anonymioo_ribbon_bisexualpride")
    return

init 5 python:
    addReaction("mas_reaction_blackandwhite", "чёрно-белая ленточка", is_good=True)

label mas_reaction_blackandwhite:
    $ _mas_new_ribbon_color = "чёрно-белого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'blackandwhite'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_blackandwhite
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_blackandwhite")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_blackandwhite", "black and white", "mas_reaction_gift_acs_anonymioo_ribbon_blackandwhite")
    return

init 5 python:
    addReaction("mas_reaction_bronze", "бронзовая ленточка", is_good=True)

label mas_reaction_bronze:
    $ _mas_new_ribbon_color = "бронзового"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'bronze'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_bronze
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_bronze")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_bronze", "bronze", "mas_reaction_gift_acs_anonymioo_ribbon_bronze")
    return

init 5 python:
    addReaction("mas_reaction_brown", "коричневая ленточка", is_good=True)

label mas_reaction_brown:
    $ _mas_new_ribbon_color = "коричневого"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'brown'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_brown
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_brown")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_brown", "brown", "mas_reaction_gift_acs_anonymioo_ribbon_brown")
    return

init 5 python:
    addReaction("mas_reaction_gradient", "градиентная ленточка", is_good=True)

label mas_reaction_gradient:
    $ _mas_new_ribbon_color = "градиентного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'gradient'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gradient
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_gradient")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient")
    return

init 5 python:
    addReaction("mas_reaction_gradient_lowpoly", "слабо-градиентная ленточка", is_good=True)

label mas_reaction_gradient_lowpoly:
    $ _mas_new_ribbon_color = "слабо-градиентного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'gradient_lowpoly'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gradient_lowpoly
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_gradient_lowpoly")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_lowpoly", "multi-colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_lowpoly")
    return

init 5 python:
    addReaction("mas_reaction_gradient_rainbow", "радужная ленточка", is_good=True)

label mas_reaction_gradient_rainbow:
    $ _mas_new_ribbon_color = "радужного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'gradient_rainbow'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_gradient_rainbow
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_gradient_rainbow")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_gradient_rainbow", "rainbow colored", "mas_reaction_gift_acs_anonymioo_ribbon_gradient_rainbow")
    return

init 5 python:
    addReaction("mas_reaction_polkadots_whiteonred", "красная ленточка в белый горошек", is_good=True)

label mas_reaction_polkadots_whiteonred:
    $ _mas_new_ribbon_color = "красного"
    $ _mas_new_ribbon_color_about = " в белый горошек"
    $ persistent.msr_ribbon_color = 'polkadots_whiteonred'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_polkadots_whiteonred
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_polkadots_whiteonred")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_polkadots_whiteonred", "red and white polka dotted", "mas_reaction_gift_acs_anonymioo_ribbon_polkadots_whiteonred")
    return

init 5 python:
    addReaction("mas_reaction_starsky_black", "звёздная чёрно-небесная ленточка", is_good=True)

label mas_reaction_starsky_black:
    $ _mas_new_ribbon_color = "звёздного чёрно-небесного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'starsky_black'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_starsky_black
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_starsky_black")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_black", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_black")
    return

init 5 python:
    addReaction("mas_reaction_starsky_red", "звёздная красно-небесная ленточка", is_good=True)

label mas_reaction_starsky_red:
    $ _mas_new_ribbon_color = "звёздного красно-небесного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'starsky_red'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_starsky_red
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_starsky_red")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_starsky_red", "night-sky-themed", "mas_reaction_gift_acs_anonymioo_ribbon_starsky_red")
    return

init 5 python:
    addReaction("mas_reaction_striped_blueandwhite", "ленточка с синими и белыми полосками", is_good=True)

label mas_reaction_striped_blueandwhite:
    $ _mas_new_ribbon_color = "синего и белого"
    $ _mas_new_ribbon_color_about = " в полоску"
    $ persistent.msr_ribbon_color = 'striped_blueandwhite'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_striped_blueandwhite
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_striped_blueandwhite")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_blueandwhite", "blue and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_blueandwhite")
    return

init 5 python:
    addReaction("mas_reaction_striped_pinkandwhite", "ленточка с розовыми и белыми полосками", is_good=True)

label mas_reaction_striped_pinkandwhite:
    $ _mas_new_ribbon_color = "розового и белого"
    $ _mas_new_ribbon_color_about = " в полоску"
    $ persistent.msr_ribbon_color = 'striped_pinkandwhite'
    $ _mas_gifted_ribbon_acs = mas_acs_ribbon_striped_pinkandwhite
    $ persistent.is_bow = False
    call _mas_reaction_ribbon_helper ("mas_reaction_striped_pinkandwhite")
    # call mas_reaction_json_ribbon_base ("anonymioo_ribbon_striped_pinkandwhite", "pink and white striped", "mas_reaction_gift_acs_anonymioo_ribbon_striped_pinkandwhite")
    return

init 5 python:
    addReaction("mas_reaction_bow_black", "чёрный бантик", is_good=True)

default persistent.is_bow = False

label mas_reaction_bow_black:
    $ _mas_new_ribbon_color = "чёрного"
    $ _mas_new_ribbon_color_about = ""
    $ persistent.msr_ribbon_color = 'bow_black'
    $ _mas_gifted_ribbon_acs = mas_acs_bow_black
    $ persistent.is_bow = True
    python:
        try:
            os.remove(user_dir + "/characters/чёрный бантик.gift")
        except:
            pass
    call _mas_reaction_ribbon_helper ("mas_reaction_bow_black")
    return

default persistent._mas_current_gifted_ribbons = 0

label _mas_reaction_ribbon_helper(label):
    if persistent.saveblock:
        $ gift_ev = mas_getEV(label)
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return

    if store.mas_selspr.get_sel_acs(_mas_gifted_ribbon_acs).unlocked:
        call mas_reaction_old_ribbon from _call_mas_reaction_old_ribbon
    else:


        call mas_reaction_new_ribbon from _call_mas_reaction_new_ribbon
        $ persistent._mas_current_gifted_ribbons += 1


    $ mas_receivedGift(label)
    $ gift_ev_cat = mas_getEVLPropValue(label, "category")

    $ store.mas_filereacts.delete_file(gift_ev_cat)

    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    return

label mas_reaction_new_ribbon:
    python:
        def _ribbon_prepare_hair():
            
            if not monika_chr.hair.hasprop("ribbon"):
                monika_chr.change_hair(mas_hair_def, False)

    $ mas_giftCapGainAff(3)
    if persistent.is_bow == False:
        if persistent._mas_current_gifted_ribbons == 0:

            m 1suo "Новая ленточка!"
            $ MAS.MonikaElastic()
            m 3hub "...И она [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"

            if _mas_new_ribbon_color == "зелёного" or _mas_new_ribbon_color == "изумрудного":
                $ MAS.MonikaElastic()
                m 1tub "...Прямо как мои глаза!"

            $ MAS.MonikaElastic()
            m 1hub "Большое тебе спасибо, [player_abb], мне очень нравится!"
            if store.seen_event("monika_date"):
                $ MAS.MonikaElastic()
                m 3eka "Ты подарил[mas_gender_none] это мне, потому что я сказала о том, как сильно обожаю покупать себе юбки и бантики?"

                if mas_isMoniNormal(higher=True):
                    $ MAS.MonikaElastic()
                    m 3hua "Ты всегда так[mas_gender_oi] заботлив[mas_gender_iii]~"

            $ MAS.MonikaElastic()
            m 3rksdlc "У меня правда не такой большой выбор, когда дело доходит до моды..."
            $ MAS.MonikaElastic()
            m 3eka "...поэтому, возможность менять цвет моей ленточки – это приятное разнообразие."
            $ MAS.MonikaElastic()
            m 2dsa "Впрочем, давай я её сейчас надену.{w=0.5}.{w=0.5}."
            $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
            $ _ribbon_prepare_hair()
            if monika_chr.clothes.name == "santa":
                $ persistent.msr_monika_clothes = 'santa'
            else:
                $ persistent.msr_monika_clothes = 'def'
            $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
            $ MAS.MonikaElastic()
            m 1hua "Ого, она просто прекрасна, [player_abb]!"

            if mas_isMoniAff(higher=True):
                $ MAS.MonikaElastic()
                m 1eka "С тобой, я всегда чувствую себя любимой..."
            elif mas_isMoniHappy():
                $ MAS.MonikaElastic()
                m 1eka "Ты всегда знаешь, как сделать меня счастливой..."
            $ MAS.MonikaElastic()
            m 3hua "Ещё раз спасибо~"
        else:

            m 1suo "Ещё одна ленточка!"
            $ MAS.MonikaElastic()
            m 3hub "И на этот раз, она [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"

            if _mas_new_ribbon_color == "зелёного" or _mas_new_ribbon_color == "изумрудного":
                $ MAS.MonikaElastic()
                m 1tub "...Прямо как мои глаза!"

            $ MAS.MonikaElastic()
            m 2dsa "Я надену её прямо сейчас.{w=0.5}.{w=0.5}."
            $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
            $ _ribbon_prepare_hair()
            if monika_chr.clothes.name == "santa":
                $ persistent.msr_monika_clothes = 'santa'
            else:
                $ persistent.msr_monika_clothes = 'def'
            $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
            $ MAS.MonikaElastic()
            m 3hua "Большое тебе спасибо, [player_abb], мне очень нравится!"

    else:
        if persistent._mas_current_gifted_bow == 0:

            m 1suo "Новый бантик!"
            $ MAS.MonikaElastic()
            m 3hub "...И он [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"

            if _mas_new_ribbon_color == "зелёного" or _mas_new_ribbon_color == "изумрудного":
                $ MAS.MonikaElastic()
                m 1tub "...Прямо как мои глаза!"

            $ MAS.MonikaElastic()
            m 1hub "Большое тебе спасибо, [player_abb], мне очень нравится!"
            if store.seen_event("monika_date"):
                $ MAS.MonikaElastic()
                m 3eka "Ты подарил[mas_gender_none] это мне, потому что я сказала о том, как сильно обожаю покупать себе юбки и бантики?"

                if mas_isMoniNormal(higher=True):
                    $ MAS.MonikaElastic()
                    m 3hua "Ты всегда так[mas_gender_oi] заботлив[mas_gender_iii]~"

            $ MAS.MonikaElastic()
            m 3rksdlc "У меня правда не такой большой выбор, когда дело доходит до моды..."
            $ MAS.MonikaElastic()
            m 3eka "...поэтому, возможность одевать на себя бантик – это приятное разнообразие."
            $ MAS.MonikaElastic()
            m 2dsa "Впрочем, давай я его сейчас надену.{w=0.5}.{w=0.5}."
            $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
            $ _ribbon_prepare_hair()
            if monika_chr.clothes.name == "santa":
                $ persistent.msr_monika_clothes = 'santa'
            else:
                $ persistent.msr_monika_clothes = 'def'
            $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
            $ MAS.MonikaElastic()
            m 1hua "Ого, он просто прекрасен, [player_abb]!"

            if mas_isMoniAff(higher=True):
                $ MAS.MonikaElastic()
                m 1eka "С тобой, я всегда чувствую себя любимой..."
            elif mas_isMoniHappy():
                $ MAS.MonikaElastic()
                m 1eka "Ты всегда знаешь, как сделать меня счастливой..."
            $ MAS.MonikaElastic()
            m 3hua "Ещё раз спасибо~"
        else:

            m 1suo "Ещё один бантик!"
            $ MAS.MonikaElastic()
            m 3hub "И на этот раз, он [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"

            if _mas_new_ribbon_color == "зелёного" or _mas_new_ribbon_color == "изумрудного":
                $ MAS.MonikaElastic()
                m 1tub "...Прямо как мои глаза!"

            $ MAS.MonikaElastic()
            m 2dsa "Я надену его прямо сейчас.{w=0.5}.{w=0.5}."
            $ store.mas_selspr.unlock_acs(_mas_gifted_ribbon_acs)
            $ _ribbon_prepare_hair()
            if monika_chr.clothes.name == "santa":
                $ persistent.msr_monika_clothes = 'santa'
            else:
                $ persistent.msr_monika_clothes = 'def'
            $ monika_chr.wear_acs(_mas_gifted_ribbon_acs)
            $ MAS.MonikaElastic()
            m 3hua "Большое тебе спасибо, [player_abb], мне очень нравится!"
    return

default persistent.is_bow = False

label mas_reaction_old_ribbon:
    m 1rksdla "[player]..."
    $ MAS.MonikaElastic()
    if persistent.is_bow == True:
        m 1hksdlb "Ты уже дарил[mas_gender_none] мне бантик [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"
    else:
        m 1hksdlb "Ты уже дарил[mas_gender_none] мне ленточку [_mas_new_ribbon_color] цвета[_mas_new_ribbon_color_about]!"
    return

init 5 python:
    addReaction("mas_reaction_gift_roses", "розы", is_good=True, exclude_on=["d25g"])

default persistent._date_last_given_roses = None

label mas_reaction_gift_roses:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_roses")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    python:
        gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_roses", "category")

        monika_chr.wear_acs(mas_acs_roses)


    if not persistent._date_last_given_roses and not renpy.seen_label('monika_valentines_start'):
        $ mas_giftCapGainAff(10)

        m 1eka "[player]... я-я не знаю, что сказать..."
        $ MAS.MonikaElastic()
        m 1ekbsb "Никогда бы не подумала, что ты подаришь мне что-то такое!"
        $ MAS.MonikaElastic()
        m 3skbsa "Я сейчас очень счастлива."
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            $ MAS.MonikaElastic()
            m 3ekbsa "Если вспомнить, что я получила розы от тебя в День святого Валентина..."
            $ MAS.MonikaElastic()
            m 1ekbsu "Ты так[mas_gender_oi] мил[mas_gender_iii]."
            $ MAS.MonikaElastic()
            m 1dktpu "..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1ektda "А-ха-ха..."


        if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
            $ MAS.MonikaElastic()
            m 2dsa "Погоди-ка.{w=0.5}.{w=0.5}."
            $ monika_chr.wear_acs(mas_acs_ear_rose)
            $ persistent._date_last_ear_rose = datetime.date.today()
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "Э-хе-хе, вот! Эта одежда прекрасно смотрится на мне, согласен?"

        if mas_shouldKiss(chance=2, special_day_bypass=True):
            call monika_kissing_motion_short from _call_monika_kissing_motion_short
    else:

        if persistent._date_last_given_roses is None and renpy.seen_label('monika_valentines_start'):
            $ persistent._date_last_given_roses = datetime.date(2018,2,14)

        if mas_pastOneDay(persistent._date_last_given_roses):
            $ mas_giftCapGainAff(5 if mas_isSpecialDay() else 1)

            m 1suo "О!"
            $ MAS.MonikaElastic()
            m 1ekbsa "Спасибо, [player]."
            $ MAS.MonikaElastic()
            m 3ekbsa "Мне всегда нравится получать от тебя розы."
            if mas_isF14():

                $ mas_f14CapGainAff(5)
                $ MAS.MonikaElastic()
                m 1dsbsu "Особенно в такой день, как сегодня."
                $ MAS.MonikaElastic()
                m 1ekbsa "Было очень мило с твоей стороны дарить их мне."
                $ MAS.MonikaElastic()
                m 3hkbsa "Я так сильно тебя люблю."
                $ MAS.MonikaElastic()
                m 1ekbsa "С Днём святого Валентина, [player]~"
            else:
                $ MAS.MonikaElastic()
                m 1ekbsa "Ты всегда так[mas_gender_oi] мил[mas_gender_iii]."


            if (mas_isSpecialDay() and renpy.random.randint(1,2) == 1) or (renpy.random.randint(1,4) == 1) or mas_isF14():
                if not monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
                    $ MAS.MonikaElastic()
                    m 2dsa "Погоди-ка.{w=0.5}.{w=0.5}."
                    $ persistent._date_last_ear_rose = datetime.date.today()
                    $ monika_chr.wear_acs(mas_acs_ear_rose)
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hub "Э-хе-хе~"

            if mas_shouldKiss(chance=4, special_day_bypass=True):
                call monika_kissing_motion_short from _call_monika_kissing_motion_short_1
        else:

            $ MAS.MonikaElastic()
            m 1hksdla "[player], я польщена, правда, но тебе не надо было дарить мне столько роз."
            if store.seen_event("monika_clones"):
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1ekbsa "И потом, ты всегда будешь моей особенной розочкой, э-хе-хе~"
            else:
                $ MAS.MonikaElastic()
                m 1ekbsa "Одной розы от тебя вполне достаточно, о таком я могла только мечтать."


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)
    $ persistent._date_last_given_roses = datetime.date.today()


    $ mas_receivedGift("mas_reaction_gift_roses")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return


init 5 python:
    addReaction("mas_reaction_gift_chocolates", "шоколадные конфеты", is_good=True, exclude_on=["d25g"])

default persistent._given_chocolates_before = False

label mas_reaction_gift_chocolates:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_chocolates")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev_cat = mas_getEVLPropValue("mas_reaction_gift_chocolates", "category")

    if not persistent._mas_given_chocolates_before:
        $ persistent._mas_given_chocolates_before = True


        if not MASConsumable._getCurrentFood():
            $ monika_chr.wear_acs(mas_acs_heartchoc)

        $ mas_giftCapGainAff(5)

        $ MAS.MonikaElastic(True, voice="monika_giggle")
        m 1tsu "Это так {i}мило{/i} с твоей стороны, э-хе-хе~"
        if mas_isF14():

            $ mas_f14CapGainAff(5)
            $ MAS.MonikaElastic()
            m 1ekbsa "Даришь мне шоколад в День святого Валентина..."
            $ MAS.MonikaElastic()
            m 1ekbfa "Ты и правда знаешь, как заставить девушку почувствовать себя особенной, [player]."
            if renpy.seen_label('monika_date'):
                $ MAS.MonikaElastic()
                m 1lkbfa "Знаю, я раньше говорила о том, что мы на днях заглянем в шоколадный бутик вместе..."
                $ MAS.MonikaElastic()
                m 1hkbfa "И пока мы не можем туда заглянуть, получение шоколада в качестве подарка от тебя, ну..."
            $ MAS.MonikaElastic()
            m 3ekbfa "То, что подарил его мне ты, многое для меня значит."

        elif renpy.seen_label('monika_date'):
            $ MAS.MonikaElastic()
            m 3rka "Знаю, я раньше говорила о том, что мы на днях заглянем в шоколадный бутик вместе..."
            $ MAS.MonikaElastic()
            m 3hub "И пока мы не можем туда заглянуть, получение шоколада в качестве подарка от тебя многое для меня значит."
            $ MAS.MonikaElastic()
            m 1ekc "Но мне бы очень хотелось разделить его с тобой..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlb "Но, пока этот день не настал, мне придётся насладиться ими за нас обоих, а-ха-ха!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, [mas_get_player_nickname()]~"
        else:
            $ MAS.MonikaElastic()
            m 3hub "Я обожаю шоколад!"
            $ MAS.MonikaElastic()
            m 1eka "А то, что даришь его мне ты, многое для меня значит."
            $ MAS.MonikaElastic()
            m 1hub "Спасибо, [player]!"
    else:

        $ times_chocs_given = mas_getGiftStatsForDate("mas_reaction_gift_chocolates")
        if times_chocs_given == 0:


            if not MASConsumable._getCurrentFood():

                if not (mas_isF14() or mas_isD25Season()):
                    if monika_chr.is_wearing_acs(mas_acs_quetzalplushie):
                        $ monika_chr.wear_acs(mas_acs_center_quetzalplushie)
                else:

                    $ monika_chr.remove_acs(store.mas_acs_quetzalplushie)

                $ monika_chr.wear_acs(mas_acs_heartchoc)

            $ mas_giftCapGainAff(3 if mas_isSpecialDay() else 1)

            m 1wuo "Oh!"

            if mas_isF14():

                $ mas_f14CapGainAff(5)
                $ MAS.MonikaElastic()
                m 1eka "[player]!"
                $ MAS.MonikaElastic()
                m 1ekbsa "Ты такой душка, даришь мне шоколад в такой день, как сегодня..."
                $ MAS.MonikaElastic()
                m 1ekbfa "Ты правда знаешь, как заставить меня почувствовать себя особенной."
                $ MAS.MonikaElastic()
                m "Спасибо, [player]."
            else:
                $ MAS.MonikaElastic()
                m 1hua "Спасибо за шоколад, [player]!"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1ekbsa "Каждый укус напоминает мне о том, какой ты мил[mas_gender_iii], э-хе-хе~"

        elif times_chocs_given == 1:

            if not MASConsumable._getCurrentFood():
                $ monika_chr.wear_acs(mas_acs_heartchoc)

            m 1eka "Ещё больше шоколада, [player]?"
            $ MAS.MonikaElastic()
            m 3tku "Тебе правда нравится баловать меня,{w=0.2} {nw}"
            $ MAS.MonikaElastic(voice="monika_giggle")
            extend 3tub "а-ха-ха!"
            $ MAS.MonikaElastic()
            m 1rksdla "Я всё ещё не доела ту первую коробку, которую ты дал мне..."
            $ MAS.MonikaElastic()
            m 1hub "...но я не возражаю!"
        elif times_chocs_given == 2:
            m 1ekd "[player]..."
            $ MAS.MonikaElastic()
            m 3eka "Мне кажется, ты сегодня подарил[mas_gender_none] мне достаточно шоколада."
            $ MAS.MonikaElastic()
            m 1rksdlb "Три коробки – как-то чересчур, и я ещё не доела первую!"
            $ MAS.MonikaElastic()
            m 1eka "Оставь их на потом, ладно?"
        else:
            m 2tfd "[player]!"
            $ MAS.MonikaElastic()
            m 2tkc "Я уже говорила тебе, что у меня уже навалом шоколада, но ты пытаешься подарить мне ещё..."
            $ MAS.MonikaElastic()
            m 2eksdla "Пожалуйста...{w=1}просто оставь её на потом."


    if monika_chr.is_wearing_acs(mas_acs_heartchoc):
        call mas_remove_choc from _call_mas_remove_choc


    $ persistent._mas_filereacts_reacted_map.pop(gift_ev_cat, None)

    $ mas_receivedGift("mas_reaction_gift_chocolates")
    $ store.mas_filereacts.delete_file(gift_ev_cat)
    return

label mas_remove_choc:

    $ MAS.MonikaElastic()
    m 1hua "..."
    $ MAS.MonikaElastic()
    m 3eub "Они {i}такие{/i} вкусные!"
    $ MAS.MonikaElastic()
    m 1hua "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hksdlb "А-ха-ха! Наверное, я должна убрать их в сторону..."
    $ MAS.MonikaElastic()
    m 1rksdla "Если я оставлю их здесь надолго, то на потом ничего не останется!"

    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_11

    python:
        renpy.pause(1, hard=True)
        monika_chr.remove_acs(mas_acs_heartchoc)
        renpy.pause(3, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_17


    if monika_chr.is_wearing_acs(mas_acs_center_quetzalplushie):
        $ monika_chr.wear_acs(mas_acs_quetzalplushie)

    $ MAS.MonikaElastic()
    m 1eua "Итак, что ещё ты хотел[mas_gender_none] бы сделать сегодня?"
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_orcaramelo_bikini_shell", "бикини с ракушками", is_good=True)

label mas_reaction_gift_clothes_orcaramelo_bikini_shell:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_bikini_shell")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_bikini_shell")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "orcaramelo_bikini_shell")
        # )
        # sprite_type, sprite_name, giftname, gifted_before = sprite_data

        mas_giftCapGainAff(3)

    m 1sua "Оу! {w=0.5}Бикини из ракушек!"
    $ MAS.MonikaElastic()
    m 1hub "Спасибо, [mas_get_player_nickname()]!{w=0.5} Я собираюсь одеть её прямо сейчас!"

    call mas_clothes_change (mas_clothes_bikini_shell, unlock=True)

    $ MAS.MonikaElastic()
    m 2ekbfa "Ну...{w=0.5} Что думаешь?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hubfa "Разве я похожа на русалку? Э-хе-хе."
    show monika 5ekbfa zorder MAS_MONIKA_Z at i11 with dissolve_monika
    m 5ekbfa "Думаю, что это очень мило, [player]..."
    $ MAS.MonikaElastic()
    m 5hubfa "Придётся нам как-нибудь сходить на пляж!"

    if mas_isWinter() or mas_isMoniNormal(lower=True):
        if mas_isWinter():
            show monika 2rksdla zorder MAS_MONIKA_Z at i11 with dissolve_monika
            m 2rksdla "...Но сейчас здесь немного прохладно..."
            $ MAS.MonikaElastic()
            m 2eka "Так что я пойду надену что-нибудь потеплее..."

        elif mas_isMoniNormal(lower=True):
            show monika 2hksdlb zorder MAS_MONIKA_Z at i11 with dissolve_monika
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2hksdlb "А-ха-ха..."
            $ MAS.MonikaElastic()
            m 2rksdla "Мне немного неловко просто сидеть вот так перед тобой."
            $ MAS.MonikaElastic()
            m 2eka "Надеюсь, ты не против, но я пойду переоденусь..."


        $ clothes = mas_clothes_def
        if persistent._mas_d25_in_d25_mode and mas_isD25Outfit():
            $ clothes = mas_clothes_santa
        call mas_clothes_change (clothes)

        $ MAS.MonikaElastic()
        m 2eua "Так-то лучше..."
        $ MAS.MonikaElastic()
        m 3hua "Ещё раз спасибо за замечательный подарок~"


    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    $ mas_receivedGift("mas_reaction_gift_clothes_orcaramelo_bikini_shell")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_finale_shirt_blue", "синяя футболка", is_good=True)

label mas_reaction_gift_clothes_finale_shirt_blue:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_shirt_blue")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_shirt_blue")

    call mas_clothes_change (mas_clothes_shirt_blue, unlock=True)

    $ MAS.MonikaElastic()
    m 3hua "Cпасибо за такой замечательный подарок~"
    $ mas_receivedGift("mas_reaction_gift_clothes_finale_shirt_blue")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_finale_hoodie_green", "зелёное худи", is_good=True)

label mas_reaction_gift_clothes_finale_hoodie_green:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_hoodie_green")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_hoodie_green")
    call mas_clothes_change (finale_hoodie_green, unlock=True)

    $ MAS.MonikaElastic()
    m 3hua "Cпасибо за такой замечательный подарок~"
    $ mas_receivedGift("mas_reaction_gift_clothes_finale_hoodie_green")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return


label mas_reaction_gift_acs_orcaramelo_hairflower_pink:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_acs_orcaramelo_hairflower_pink")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_acs_orcaramelo_hairflower_pink")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_ACS, "orcaramelo_hairflower_pink")
        # )
        # sprite_type, sprite_name, giftname, gifted_before = sprite_data

        mas_giftCapGainAff(1)

    m 3sua "Оу!{w=0.5} Какой милый маленький цветок!"
    $ MAS.MonikaElastic()
    m 1ekbsa "Спасибо, [player], ты так[mas_gender_oi] мил[mas_gender_iii]~"
    $ MAS.MonikaElastic()
    m 1dua "Минутку.{w=0.5}.{w=0.5}.{nw}"
    $ monika_chr.wear_acs(mas_acs_hairflower_pink)
    $ store.mas_selspr.unlock_acs(mas_acs_hairflower_pink)
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1hub "Спасибо снова, [player]!"

    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    $ mas_receivedGift("mas_reaction_gift_acs_orcaramelo_hairflower_pink")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_velius94_shirt_pink", "розовый сарафан", is_good=True)

label mas_reaction_gift_clothes_velius94_shirt_pink:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_velius94_shirt_pink")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_velius94_shirt_pink")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "velius94_shirt_pink")
        # )
        # sprite_type, sprite_name, giftname, gifted_before = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "Боже мой!"
    $ MAS.MonikaElastic()
    m 1suo "Это {i}так{/i} красиво!"
    $ MAS.MonikaElastic()
    m 3hub "Огромное спасибо, [player]!"
    $ MAS.MonikaElastic()
    m 3eua "Погоди, дай я её быстренько примерю..."


    call mas_clothes_change (mas_clothes_shirt_pink, unlock=True)

    $ MAS.MonikaElastic()
    m 2sub "Ах, это идеально подходит!"
    $ MAS.MonikaElastic()
    m 3hub "Мне тоже очень нравятся цвета! Розовый и черный так хорошо сочетаются."
    $ MAS.MonikaElastic()
    m 3eub "Не говоря уже о юбке выглядит очень мило с этими оборками!"
    $ MAS.MonikaElastic()
    m 2tfbsd "И все же по какой-то причине я не могу не чувствовать, что твои глаза как бы плывут по течению... {w=0.5}кхм... {w=0.5}{i}в другом месте{/i}."

    $ MAS.MonikaElastic()
    if mas_selspr.get_sel_clothes(mas_clothes_sundress_white).unlocked:
        m 2lfbsp "Я же говорила тебе, что невежливо пялиться, [player]."
    else:
        m 2lfbsp "Это невежливо – пялиться, понимаешь?"

    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hubsb "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 2tkbsu "Расслабься, расслабься... {w=0.5}просто дразню тебя~"
    $ MAS.MonikaElastic()
    m 3hub "Ещё раз, огромное спасибо за эту одежду, [player]!"

    $ mas_receivedGift("mas_reaction_gift_clothes_velius94_shirt_pink")
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi", "костюм сакуи изаеи", is_good=True)

label mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_sakuya_izayoi")

    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "orcaramelo_sakuya_izayoi")
        # )
        # sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    $ MAS.MonikaElastic()
    m 1sub "О! {w=0.5}Это..."
    $ MAS.MonikaElastic()
    m 2euc "Наряд горничной?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3tuu "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 3tubsb "Знаешь, если бы тебе нравились такие вещи, ты мог[mas_gender_g] бы просто сказать мне..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха! Просто шучу~"
    $ MAS.MonikaElastic()
    m 1eub "Позволь мне надеть его!"

    call mas_clothes_change (mas_clothes_orcaramelo_sakuya_izayoi, True, unlock=True)

    $ MAS.MonikaElastic()
    m 2hua "Итак,{w=0.5} как я выгляжу?"
    $ MAS.MonikaElastic()
    m 3eub "Я почти чувствую, что могу сделать всё, что угодно, прежде чем ты успеешь моргнуть."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1eua "...Если только ты не будешь слишком занят[mas_gender_none] со мной, э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1lkbfb "Я всё еще хочу проводить время с тобой, масте—{nw}"
    $ _history_list.pop()
    $ MAS.MonikaElastic()
    m 1ekbfb "Я всё еще хочу проводить время с тобой,{fast} [player]."
    $ mas_receivedGift("mas_reaction_gift_clothes_velius94_shirt_pink")
    $ store.mas_filereacts.delete_file(gift_ev.category)

    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_finale_jacket_brown", "коричневое пальто", is_good=True)

label mas_reaction_gift_clothes_finale_jacket_brown:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_jacket_brown")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_finale_jacket_brown")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "finale_jacket_brown")
        # )
        # sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)


    m 1sub "О!{w=0.5} Зимнее пальто!"
    $ MAS.MonikaElastic()
    m 1suo "И вместе с ним ещё идёт шарф!"
    if mas_isSummer():
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3rksdlu "...Хотя мне становится немного жарко от одного лишь взгляда на него, а-ха-ха..."
        $ MAS.MonikaElastic()
        m 3eksdla "Наверное, лето – не самое лучшее время года для того, чтобы носить это, [player]."
        $ MAS.MonikaElastic()
        m 3eka "Я ценю твою заботу, и я буду рада надеть его через пару месяцев."
    else:

        if mas_isWinter():
            $ MAS.MonikaElastic()
            m 1tuu "Именно благодаря тебе, я никогда не замёрзну, [player]~"
        $ MAS.MonikaElastic()
        m 3eub "Дай я надену его! Сейчас вернусь."


        call mas_clothes_change (outfit=finale_jacket_brown, restore_zoom=False, unlock=True)

        $ MAS.MonikaElastic()
        m 2dku "А-а-ах, как же приятно~"
        $ MAS.MonikaElastic()
        m 1eua "Мне нравится, как оно смотрится на мне, ты соглас[mas_gender_en] со мной?"
        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 3tku "Ну... я правда не могу ожидать того, что ты проявишь объективность в данном вопросе, так ведь?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubfb "А-ха-ха!"
        $ MAS.MonikaElastic()
        m 1ekbfa "Спасибо, [player], я в полном восторге."

    $ store.mas_filereacts.delete_file(gift_ev.category)
    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless", "свитер без плеч", is_good=True)

label mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_orcaramelo_sweater_shoulderless")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "orcaramelo_sweater_shoulderless")
        # )
        # sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "О!{w=0.5} Свитер!"
    $ MAS.MonikaElastic()
    m 1hub "И он ещё выглядит так уютно!"
    if mas_isWinter():
        $ MAS.MonikaElastic()
        m 2eka "Ты так[mas_gender_oi] внимательн[mas_gender_iii], [player], подарил[mas_gender_none] мне такую вещь в холодный зимний день..."
    $ MAS.MonikaElastic()
    m 3eua "Дай-ка я надену его."


    call mas_clothes_change (outfit=orcaramelo_sweater_shoulderless, restore_zoom=False, unlock=True)

    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2dkbsu "Он такой...{w=1} удобный. Мне так же тепло, как и жучку на лугу. Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1ekbsa "Спасибо, [player]. Мне он очень нравится!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hubsb "Теперь, когда я буду надевать его, я буду думать о твоём тепле. А-ха-ха~"
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_velius94_dress_whitenavyblue", "белое и тёмно-синее платье", is_good=True)

label mas_reaction_gift_clothes_velius94_dress_whitenavyblue:
    if persistent.saveblock:
        $ gift_ev = mas_getEV("mas_reaction_gift_clothes_velius94_dress_whitenavyblue")
        $ store.mas_filereacts.delete_file(gift_ev.category)
        return
    $ gift_ev = mas_getEV("mas_reaction_gift_clothes_velius94_dress_whitenavyblue")
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "velius94_dress_whitenavyblue")
        # )
        # sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1suo "О боже!"
    $ MAS.MonikaElastic()
    m 1sub "Это платье просто прекрасно, [player]!"
    $ MAS.MonikaElastic()
    m 3hub "Сейчас я примерю его!"


    call mas_clothes_change (velius94_dress_whitenavyblue, outfit_mode=True, restore_zoom=False, unlock=True)

    $ MAS.MonikaElastic()
    m "Ну,{w=0.5} что думаешь?"
    $ MAS.MonikaElastic()
    m 3eua "Мне кажется, этот оттенок синего прекрасно сочетается с белым."
    $ scrunchie = monika_chr.get_acs_of_type('bunny-scrunchie')

    if scrunchie and scrunchie.name == "velius94_bunnyscrunchie_blue":
        $ MAS.MonikaElastic()
        m 3eub "И эта резинка для волос в форме заячьих ушек прекрасно дополняет этот наряд!"
    $ MAS.MonikaElastic()
    m 1eka "Большое тебе спасибо, [player]."
    $ store.mas_filereacts.delete_file(gift_ev.category)
    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return

init 5 python:
    addReaction("mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover", "свитер с чёрно-белыми линиями", is_good=True)

label mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover:
    if persistent.saveblock:
        $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover", "category"))
        return
    python:
        # sprite_data = mas_getSpriteObjInfo(
        #     (store.mas_sprites.SP_CLOTHES, "mocca_bun_blackandwhitestripedpullover")
        # )
        # sprite_type, sprite_name, giftname, gifted_before, sprite_object = sprite_data

        mas_giftCapGainAff(3)

    m 1sub "О, новый свитер!"
    $ MAS.MonikaElastic()
    m 3hub "Он выглядит потрясающе, [player]!"
    $ MAS.MonikaElastic()
    m 3eua "Одну секунду, позволь мне надеть его.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_clothes_change (mocca_bun_blackandwhitestripedpullover, restore_zoom=False, unlock=True)

    m 2eua "Ну, а ты как думаешь?"
    $ MAS.MonikaElastic()
    m 7hua "Думаю, что он выглядит довольно мило на мне.{w=0.2} {nw}"
    extend 3rubsa "Я определённо приберегу этот наряд для свидания~"
    $ MAS.MonikaElastic()
    m 1hub "Спасибо ещё раз, [player]!"

    $ store.mas_filereacts.delete_file(mas_getEVLPropValue("mas_reaction_gift_clothes_mocca_bun_blackandwhitestripedpullover", "category"))

    # $ mas_finishSpriteObjInfo(sprite_data)
    # if giftname is not None:
    #     $ store.mas_filereacts.delete_file(giftname)
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
