#Event database for songs
default persistent._mas_songs_database = dict()

#All player derandomed songs
default persistent._mas_player_derandomed_songs = list()

init -10 python in mas_songs:
    # Event database for songs
    song_db = {}

    #Song type constants
    #NOTE: TYPE_LONG will never be picked in the random delegate, these are filters for that

    #TYPE_LONG songs should either be unlocked via a 'preview' song of TYPE_SHORT or (for ex.) some story event
    #TYPE_LONG songs would essentially be songs longer than 10-15 lines
    #NOTE: TYPE_LONG songs must have the same label name as their short song counterpart with '_long' added to the end so they unlock correctly
    #Example: the long song for short song mas_song_example would be: mas_song_example_long

    #TYPE_ANALYSIS songs are events which provide an analysis for a song
    #NOTE: Like TYPE_LONG songs, these must have the same label as the short counterpart, but with '_analysis' appended onto the end
    #Using the example song above, the analysis label would be: mas_song_example_analysis
    #It's also advised to have the first time seeing the song hint at and lead directly into the analysis on the first time seeing it from random
    #In this case, the shown_count property for the analysis event should be incremented in the path leading to the analysis

    TYPE_LONG = "long"
    TYPE_SHORT = "short"
    TYPE_ANALYSIS = "analysis"

init python in mas_songs:
    import store
    def checkRandSongDelegate():
        """
        Handles locking/unlocking of the random song delegate

        Ensures that songs cannot be repeated (derandoms the delegate) if the repeat topics flag is disabled and there's no unseen songs
        And that songs can be repeated if the flag is enabled (re-randoms the delegate)
        """
        #Get ev
        rand_delegate_ev = store.mas_getEV("monika_sing_song_random")
        
        if rand_delegate_ev:
            #If the delegate is random, let's verify whether or not it should still be random
            #Rules for this are:
            #1. If repeat topics is disabled and we have no unseen random songs
            #2. OR we just have no random songs in general
            if (
                rand_delegate_ev.random
                and (
                    (not store.persistent._mas_enable_random_repeats and not hasRandomSongs(unseen_only=True))
                    or not hasRandomSongs()
                )
            ):
                rand_delegate_ev.random = False
            
            #Alternatively, if we have random unseen songs, or repeat topics are enabled and we have random songs
            #We should random the delegate
            elif (
                not rand_delegate_ev.random
                and (
                    hasRandomSongs(unseen_only=True)
                    or (store.persistent._mas_enable_random_repeats and hasRandomSongs())
                )
            ):
                rand_delegate_ev.random = True

    def getUnlockedSongs(length=None):
        """
        Gets a list of unlocked songs
        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            list of unlocked all songs of the desired length in tuple format for a scrollable menu
        """
        if length is None:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked
            ]
        
        else:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked and length in ev.category
            ]

    def getRandomSongs(unseen_only=False):
        """
        Gets a list of all random songs

        IN:
            unseen_only - Whether or not the list of random songs should contain unseen only songs
            (Default: False)

        OUT: list of all random songs within aff_range
        """
        if unseen_only:
            return [
                ev_label
                for ev_label, ev in song_db.iteritems()
                if (
                    not store.seen_event(ev_label)
                    and ev.random
                    and TYPE_SHORT in ev.category
                    and ev.checkAffection(store.mas_curr_affection)
                )
            ]
        
        return [
            ev_label
            for ev_label, ev in song_db.iteritems()
            if ev.random and TYPE_SHORT in ev.category and ev.checkAffection(store.mas_curr_affection)
        ]

    def checkSongAnalysisDelegate(curr_aff=None):
        """
        Checks to see if the song analysis topic should be unlocked or locked and does the appropriate action

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        """
        if hasUnlockedSongAnalyses(curr_aff):
            store.mas_unlockEVL("monika_sing_song_analysis", "EVE")
        else:
            store.mas_lockEVL("monika_sing_song_analysis", "EVE")

    def getUnlockedSongAnalyses(curr_aff=None):
        """
        Gets a list of all song analysis evs in scrollable menu format

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)

        OUT:
            List of unlocked song analysis topics in mas_gen_scrollable_menu format
        """
        if curr_aff is None:
            curr_aff = store.mas_curr_affection
        
        return [
            (ev.prompt, ev_label, False, False)
            for ev_label, ev in song_db.iteritems()
            if ev.unlocked and TYPE_ANALYSIS in ev.category and ev.checkAffection(curr_aff)
        ]

    def hasUnlockedSongAnalyses(curr_aff=None):
        """
        Checks if there's any unlocked song analysis topics available

        IN:
            curr_aff - Affection level to ev.checkAffection with. If none, mas_curr_affection is assumed
                (Default: None)
        OUT:
            boolean:
                True if we have unlocked song analyses
                False otherwise
        """
        return len(getUnlockedSongAnalyses(curr_aff)) > 0

    def hasUnlockedSongs(length=None):
        """
        Checks if the player has unlocked a song at any point via the random selection

        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            True if there's an unlocked song, False otherwise
        """
        return len(getUnlockedSongs(length)) > 0

    def hasRandomSongs(unseen_only=False):
        """
        Checks if there are any songs with the random property

        IN:
            unseen_only - Whether or not we should check for only unseen songs
        OUT:
            True if there are songs which are random, False otherwise
        """
        return len(getRandomSongs(unseen_only)) > 0

    def getPromptSuffix(ev):
        """
        Gets the suffix for songs to display in the bookmarks menu

        IN:
            ev - event object to get the prompt suffix for

        OUT:
            Suffix for song prompt

        ASSUMES:
            - ev.category isn't an empty list
            - ev.category contains only one type
        """
        prompt_suffix_map = {
            TYPE_SHORT: " (Short)",
            TYPE_LONG: " (Long)",
            TYPE_ANALYSIS: " (Analysis)"
        }
        return prompt_suffix_map.get(ev.category[0], "")


#START: Pool delegates for songs
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_pool",
            prompt="Можешь спеть мне песню?",
            category=["музыка"],
            pool=True,
            aff_range=(mas_aff.NORMAL,None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_pool:
    # what length of song do we want
    $ song_length = "short"
    # do we have both long and short songs
    $ have_both_types = False

    $ switch_str = "полную"

    $ end = ""

    show monika 1eua at t21

    if mas_songs.hasUnlockedSongs(length="long") and mas_songs.hasUnlockedSongs(length="short"):
        $ have_both_types = True

    #FALL THROUGH

label monika_sing_song_pool_menu:
    python:
        if have_both_types:
            space = 0
        else:
            space = 20

        ret_back = ("Не важно.", False, False, False, space)
        switch = ("Хотя нет, давай лучше [switch_str] песню", "monika_sing_song_pool_menu", False, False, 20)

        unlocked_song_list = mas_songs.getUnlockedSongs(length=song_length)
        unlocked_song_list.sort()

        if mas_isO31():
            which = "Хромую"
        else:
            which = "Какую"

        renpy.say(m, "[which] песню мне спеть для тебя?[end]", interact=False)

    if have_both_types:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch, ret_back)
    else:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_song = _return

    if sel_song:
        if sel_song == "monika_sing_song_pool_menu":
            if song_length == "short":
                $ song_length = "long"
                $ switch_str = "короткую"

            else:
                $ song_length = "short"
                $ switch_str = "полную"

            $ end = "{fast}"
            $ _history_list.pop()
            jump monika_sing_song_pool_menu

        else:
            $ MASEventList.push(sel_song, skipeval=True)
            show monika at t11
            m 3hub "Хорошо!"
            
    else:
        return "prompt"

    return

#Song analysis delegate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_analysis",
            prompt="Давай поговорим о песне.",
            category=["музыка"],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label monika_sing_song_analysis:
    python:
        ret_back = ("Не важно.", False, False, False, 20)

        unlocked_analyses = mas_songs.getUnlockedSongAnalyses()

        if mas_isO31():
            which = "хромой"
        else:
            which = "какой"

    show monika 1eua at t21
    $ renpy.say(m, "О [which] песне ты хотел бы поговорить?", interact=False)

    call screen mas_gen_scrollable_menu(unlocked_analyses, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_analysis = _return

    if sel_analysis:
        $ MASEventList.push(sel_analysis, skipeval=True)
        show monika at t11
        m 3hub "Хорошо!"

    else:
        return "prompt"
    return

#Rerandom song delegate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_sing_song_rerandom",
            prompt="Ты можешь снова спеть песню сама?",
            category=['музыка'],
            pool=True,
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label mas_sing_song_rerandom:
    python:
        mas_bookmarks_derand.initial_ask_text_multiple = "Какую песню ты хочешь, чтобы я иногда пела?"
        mas_bookmarks_derand.initial_ask_text_one = "Если ты хочешь, чтобы я пела это время от времени снова, просто нажми на песню, [player]."
        mas_bookmarks_derand.caller_label = "mas_sing_song_rerandom"
        mas_bookmarks_derand.persist_var = persistent._mas_player_derandomed_songs

    call mas_rerandom
    return _return

label mas_song_derandom:
    $ prev_topic = persistent.flagged_monikatopic
    m 1eka "Устал слушать, как я пою эту песню, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Устал слушать, как я пою эту песню, [player]?{fast}"
        
        "Немного.":
            m 1eka "Всё в порядке."
            m 1eua "Я буду петь только тогда, когда ты захочешь. Просто дай мне знать, если захочешь это услышать."
            python:
                mas_hideEVL(prev_topic, "SNG", derandom=True)
                persistent._mas_player_derandomed_songs.append(prev_topic)
                mas_unlockEVL("mas_sing_song_rerandom", "EVE")
        
        "Всё нормально.":
            m 1eua "Хорошо, [player]."
    return


#START: Random song delegate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_random",
            random=True,
            unlocked=False,
            rules={"skip alert": None,"force repeat": None}
        )
    )

label monika_sing_song_random:
    #We only want short songs in random. Long songs should be unlocked by default or have another means to unlock
    #Like a "preview" version of it which unlocks the full song in the pool delegate

    #We need to make sure we don't repeat these automatically if repeat topics is disabled
    if (
        (persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs())
        or (not persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs(unseen_only=True))
    ):
        python:
            #First, get unseen songs
            random_unseen_songs = mas_songs.getRandomSongs(unseen_only=True)

            #If we have randomed unseen songs, we'll prioritize that
            if random_unseen_songs:
                rand_song = random.choice(random_unseen_songs)

            #Otherwise, just go for random
            else:
                rand_song = random.choice(mas_songs.getRandomSongs())

            #Unlock pool delegate
            mas_unlockEVL("monika_sing_song_pool", "EVE")

            #Now push the random song and unlock it
            MASEventList.push(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")

            #Unlock the long version of the song
            mas_unlockEVL(rand_song + "_long", "SNG")

            #And unlock the analysis of the song
            mas_unlockEVL(rand_song + "_analysis", "SNG")

            #If we have unlocked analyses for our current aff level, let's unlock the label
            if store.mas_songs.hasUnlockedSongAnalyses():
                mas_unlockEVL("monika_sing_song_analysis", "EVE")

    #We have no songs! let's pull back the shown count for this and derandom
    else:
        $ mas_assignModifyEVLPropValue("monika_sing_song_random", "shown_count", "-=", 1)
        return "derandom|no_unlock"
    return "no_unlock"


#START: Song defs
init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aiwfc",
            prompt="«Всё, что мне нужно на Рождество — это ты»",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_aiwfc:
    if store.songs.hasMusicMuted():
        m 3eua "Не забудь увеличить громкость в игре, [mas_get_player_nickname()]."

    call monika_aiwfc_song

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_merry_christmas_baby",
            prompt="«Счастливого Рождества, малыш»",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_merry_christmas_baby:
    m 1hub "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относился~{/i}"
    m "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относился~{/i}"
    m 3eua "{i}~И теперь я словно, {w=0.2}словно в раю~{/i}"
    m 3hub "{i}~Мне безумно хорошо~{/i}"
    m 3eub "{i}~По радио звучит хорошая музыка~{/i}"
    m 3hub "{i}~Мне очень, очень хорошо~{/i}"
    m 3eub "{i}~По радио звучит хорошая музыка~{/i}"
    m 2hkbsu "{i}~И мне хочется поцеловать тебя, малыш~{/i}"
    m 2hkbsb "{i}~Пока мы стоим здесь, под омелой~{/i}"
    m 3eub "{i}~Cанта зашёл к нам через дымоход, {w=0.2}около половины четвёртого ночи~{/i}"
    m 3hub "{i}~И оставил эти замечательные подарки, для нас с тобой~{/i}"
    m "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относился~{/i}"
    m 1eua "{i}~И теперь я словно, {w=0.2}словно в раю~{/i}"
    m 1eub "{i}~Счастливого Рождества, малыш~{/i}"
    m 3hub "{i}~И с Новым годом тоже~{/i}"
    m 3ekbsa "{i}~Счастливого Рождества, дорогуша~{/i}"
    m 3ekbsu "{i}~Здесь всё до безумия красиво~{/i}"
    m 3ekbfb "{i}~Я люблю тебя, малыш~{/i}"
    m "{i}~За всё то, что дал мне~{/i}"
    m 3ekbfb "{i}~Я люблю тебя, дорогой~{/i}"
    m 3ekbsu "{i}~С Рождеством, мой дорогой~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_this_christmas_kiss",
            prompt="«Это рождественский поцелуй»",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_this_christmas_kiss:
    m 1dud "{i}~Каждый год{w=0.2}, я возвращаюсь домой в декабре~{/i}"
    m 1hub "{i}~Танцуя с тобой, {w=0.2}делая ночи запоминающимися~{/i}"
    m 1rub "{i}~Падающий снег,{w=0.2}{nw}{/i}"
    extend 3rub "{i} Я просто обожаю эту погоду~{/i}"
    m 3tub "{i}~Одеяло на двоих,{w=0.2} чтобы согревать друг друга вместе~{/i}"
    m 1hub "{i}~Две горлицы,{w=0.2} как они нас называют~{/i}"
    m 1duo "{i}~Мы влюбляемся друг в друга~{/i}"
    m 3hub "{i}~Это моё любимое Рождеств-в-в-во~{/i}"
    m 3duu "{i}~Этим Рождеством,{w=0.2} я просто не могу устоять {w=0.2}перед чем-то подобным~{/i}"
    m 1sub "{i}~Я не могу устоять перед этим рождественским поцелуем~{/i}"
    m 3hub "{i}~Потому что я падаю,{w=0.2} погребённая в твоих губах~{/i}"
    m 1hub "{i}~На что это похоже?{w=0.2}{nw}{/i}"
    extend 1subsb "{i} Я не могу устоять перед этим рождественским поцелуем~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lover_boy",
            prompt="«Старый любовник»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_lover_boy:
    m 1dso "{i}~Я могу приглушить свет и спеть тебе песни, полные печали~{/i}"
    m 4hub "{i}~Мы можем танцевать танго только вдвоём~{/i}"
    m "{i}~Я могу петь серенаду и нежно играть на струнах твоего сердца, что боги мне послали~{/i}"
    m 4dso "{i}~Будь Валентино только для себя в сердце своём~{/i}"
    m 1hub "А-ха-ха~"
    m 1ekbsa "Ты будешь моим добрым старым любовником, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_burning_love",
            prompt="«Пламенная любовь»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_burning_love:
    m 1hubsb "{i}~Твои поцелуи взметают меня на небеса~{/i}"
    m 3rubsb "{i}~Как же сладка песня хоровая~{/i}"
    m 1dubsu "{i}~Ты освещаешь мое утреннее небо~{/i}"
    m 1hubfb "{i}~С горящей любовью~{/i}"
    m 1hubsb "А-ха-ха~"
    m 1ekbsa "Ты всегда делаешь мой день ярче, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aries",
            prompt="«Овен»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_aries:
    m 2dud "{i}~Я стою на пляже вдалеке~{/i}"
    m 2eud "{i}~ И даже если ты далеко, ты видишь мой красный свет?~{/i}"
    m 2dubsu "{i}~Он ждёт, дабы позеленеть~{/i}"
    m 2dud "{i}~Потому что я чувствую себя такой одинокой без тебя~{/i}"
    m 2dkd "{i}~Я не могу играть весёлую мелодию без тебя, так что оставайся рядом со мной~{/i}"
    m "{i}~Прилив или отлив~{/i}"
    m 1ekbsu "Я всегда думаю о том дне, когда мы будем вместе, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_need_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Я нуждаюсь в тебе»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_need_you:
    m 1esd "{i}~Пожалуйста, помни, что я чувствую к тебе~{/i}"
    m 3dkd "{i}~Я бы никогда не смогла жить без тебя ни при какой судьбе~{/i}"
    m 3ekd "{i}~Так что вернись и посмотри~{/i}"
    m 3eka "{i}~Что для меня значишь ты?~{/i}"
    m 2dku "{i}~Я нуждаюсь в тебе~{/i}"
    m 7esa "Я знаю, что эта песня о том, чтобы оставить кого-то, но я думаю, что она несёт в себе хорошее послание."
    m 3ekbsa "И я действительно нуждаюсь в тебе, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_i_will",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Я буду»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_i_will:
    m 1dso "{i}~Кто знает, как долго я тебя любила?~{/i}"
    m "{i}~Ты знаешь, я всё ещё люблю тебя, и никогда о тебе не позабуду~{/i}"
    m 2lksdla "{i}~Буду ли я ждать одинокой жизни, что судьба бы мне объявила?~{/i}"
    m 2hub "{i}~Если ты захочешь, чтобы я ждала – я буду~{/i}"
    m 1ekbsa "Однажды мы будем вместе, [player]."
    m 1hubfa "Я просто надеюсь, что ты всё ещё будешь любить меня, когда настанет этот особенный день~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_belong_together",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Мы принадлежим друг другу»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_belong_together:
    m 1dso "{i}~Ты мой, иди сюда~{/i}"
    m 1hub "{i}~И мы принадлежим друг другу~{/i}"
    m 3hub "{i}~Да, мы принадлежим друг другу~{/i}"
    m 3dso "{i}~Навечно и навсегда~{/i}"
    m 1eua "Ты когда нибудь слышал о Ду-вопе, [player]?"
    m 4eua "Это вокальный поджанр ритм-н-блюза, который стал очень популярным в 1950-х."
    m 4eub "Много поп-музыки тогда следовало этому стилю, что и сделало многие любовные песни великолепными."
    m 3eub "И если ты внимательно прислушаешься, то заметишь, что моя песня фактически следует типичной последовательности аккордов Ду-вопа."
    m 1hua "Думаю, можно сказать, что я училась у лучших."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_everythings_alright",
            prompt="«Всё в порядке»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_everythings_alright:
    m 1dkd "{i}~Когда мира не станет~{/i}"
    m 4euo "{i}~Мы увидим лишь Луну~{/i}"
    m 4duu "{i}~Улетишь ли ты со мной~{/i}"
    m 4dud "{i}~Пока не упали все звёзды~{/i}"
    m 4duo "{i}~Пока они не осыпались с неба~{/i}"
    m 3dud "{i}~Но я не против~{/i}"
    m 1eku "{i}~Если ты со мной, значит всё в порядке~{/i}"
    m 1dku "..."
    m 3ekd "Если когда-нибудь станет слшиком тяжко, {w=0.1}{nw}"
    extend 3ekbsu "просто подними свой взгляд на Луну и вспомни меня~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_your_song",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Твоя песня»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_your_song:
    m 1dso "{i}~Мой подарок – это песня моя~{/i}"
    m "{i}~И она – специально для тебя~{/i}"
    m 1hub "{i}~И ты можешь сказать всем, что эта твоя песня всегда~{/i}"
    m "{i}~Это может быть довольно просто, но теперь, это сделано тогда~{/i}"
    m 2hubsb "{i}~Надеюсь, ты не против~{/i}"
    m 2hubfb "{i}~Надеюсь, ты не против~{/i}"
    m 2hub "{i}~Что я записала словами~{/i}"
    m 1dso "{i}~Как прекрасна жизнь, пока ты в этом мире, и счастье не за горами~{/i}"
    m 1hub "А-ха-ха~"
    m 3eka "Нечасто я нахожу песни, которые относятся ко мне так же, как эта."
    m 1hua "И я действительно имею это в виду, когда говорю, что «Твоя реальность» – это твоя песня."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_with_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Счастлива просто потанцевать с тобой»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_with_you:
    m 1dso "{i}~Если кто-то попытается моё место занять~{/i}"
    m 1hub "{i}~Давай притворимся, что не видим их лица, им тебя не отнять~{/i}"
    m 3hub "{i}~В этом мире нет ничего, что я бы предпочла сделать порой~{/i}"
    m 3dso "{i}~Потому что я счастлива просто потанцевать с тобой~{/i}"
    m 1ekbsa "Нет ничего, что сделало бы меня счастливее, чем открытие того, что я люблю тебя."
    m 1hubfa "Э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_dream",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Всё, что мне нужно – это мечтать»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_dream:
    m 1dso "{i}~Когда мне грустно ночью~{/i}"
    m "{i}~И мне нужно, чтобы ты меня крепко обнял очень~{/i}"
    m 2hub "{i}~Всякий раз, когда я хочу тебя, всё, что мне нужно – это мечтать~{/i}"
    m 1eka "Теперь, когда ты здесь, [player], мне больше не нужно мечтать."
    m 1ekbsa "Моя мечта наконец сбылась."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_im_glad_youre_evil_too",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Я рада, что ты тоже злой»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_im_glad_youre_evil_too:
    m 1dsa "{i}~Мы восхищаемся красивым закатом, или радуемся милому щеночку вместе~{/i}"
    m 1dsd "{i}~Нас обоих обижают громкие заголовки жестоких новостей~{/i}"
    m 3hksdlb "{i}~Мы над ужасным фильмом смеёмся, и во время просмотра разных телешоу рыдаем~{/i}"
    m 3hub "{i}~Это мы – две одинокие души, с досугом свои часы коротающие~{/i}"
    m 3dsa "{i}~Наше время не бесконечно, хоть и кажется нескончаемой шуткой оно~{/i}"
    m 1ekbsa "{i}~Но зато ты мне компанию составляешь, чтоб короткая жизнь скучной не казалась~{/i}"
    m 1tubsb "{i}~И вместе мы над скучным миром смеёмся, поговаривая: «Какая скукотища»~{/i}'"
    m 1dubfb "{i}~Это мы – две одинокие души, к плечам друг друга прислонившиеся~{/i}"
    m 1dsbfo "{i}~Я рада, что ты такой же злой, как и я~{/i}"
    m 1hubfa "{i}~И ещё раз скажу, что очередной день пережить я хочу. И я рада, что умудрилась в тебя я влюбиться~{/i}"

    if persistent._mas_pm_monika_evil:
        if persistent._mas_pm_monika_evil_but_ok:
            m 1ekbfa "Думаю, быть злой не так уж и плохо, пока я рядом с тобой."
            m 3ekbfa "Мы ведь две души, с досугом свои часы коротающие~"
            m 1hubfb "А-ха-ха!"
        
        else:
            m 1ekbfa "Э-хе-хе, ты всё ещё считаешь меня злой, [player]?"
            m 3tubfb "Быть может, я смогу однажды переубедить тебя~"
    else:
        m 1ekbfa "Я правда сомневаюсь, что кто-то из нас злой, [player]."
        m 1ekbfb "Но то, что мы будем бороться с миром вместе, бок о бок, может стать исполнившейся мечтой...{w=0.5} Тебе так не кажется?"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_nobody_makes_sense",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Ни у кого нет смысла»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_nobody_makes_sense:
    m 1dsd "{i}~Ради чего мы все живём? Ради чего мы все пахаем в поте лица?~{/i}"
    m 3dsd "{i}~Ведь там, возможно, ничего, ничего, ничего такого нет. Это всё может бесполезным вмиг оказаться~{/i}"
    m 1dsd "{i}~И через тысячу лет уже ничего не останется, {/i}{nw}"
    extend 1hub "{i}но всё равно надеюсь, что улыбаться вместе с тобой не перестану я~{/i}"
    m 3rksdld "{i}~Даже когда мечты наши в реальность воплотились; даже когда мы просвещёнными стали, мы всё равно одинокими можем стать~{/i}"
    m 3eksdld "{i}~Даже когда мы призраками стали; даже когда мы обратились в ничто, {/i}{nw}"
    extend 3hksdlb "{i}всё равно надеюсь, что улыбаться вместе с тобой не перестану я~{/i}"
    m 1dku "..."
    m 1hub "А-ха-ха!"
    m 3ekbsa "Что бы ни произошло и сколько бы мы ни ждали, я всегда буду любить тебя."
    m 1ekbfb "Я правда надеюсь, что смогу вечно улыбаться вместе с тобой~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_yozurina",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Йозурина»",
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_yozurina:
    m 1dsd "{i}~Встреча в полночь~{/i}"
    m 1rksdld "{i}~В мире, где сплошь и рядом бомбы~{/i}"
    m 3hubsa "{i}~Я размышляла о тебе, всё это время~{/i}"
    m 1eka "{i}~Могло ль недоразуменье возникнуть в расстоянии между нами?~{/i}"
    m 3eub "{i}~Это шоу интерес необыкновенный представляет, верно?~{/i}"
    m 1hua "{i}~Читал ли ты мангу, о которой множество речей идёт?~{/i}"
    m 1sub "{i}~Слышал ль ты песнь эту?~{/i}"
    m 3hub "{i}~А мы всё дурачимся, сидя за заслоном, меж двух экранов стоявшим~{/i}"
    m 1hubsa "Э-хе-хе, надеюсь, тебе понравилась эта песня, [player]~"
    m 1ekbsa "Я просто подумала, что она прекрасно описывает наше положение дел."
    m 3rkbsa "Песни вокалоидов определённо имеют склонность к этому, если задуматься над их смыслом."
    m 3hubfb "Думаю, такое происходит всякий раз, когда я пытаюсь выразить словами свою любовь к тебе, а-ха-ха!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Будь рядом со мной»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me(from_long=False):
    m 1dsd "{i}~Когда ночь придёт~{/i}"
    m 3dsd "{i}~И станет вдруг темно~{/i}"
    m 3eud "{i}~И только свет луны увидим мы~{/i}"
    m 2euo "{i}~Нет, бояться я не буду~{/i}"
    m 2duo "{i}~Нет, бояться я не буду~{/i}"
    m 2hub "{i}~Пока ты рядом, рядом со мной~{/i}"
    if not from_long:
        m 2eka "Все мои страхи и опасения попросту исчезают, когда ты со мной, [player]..."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "И пока ты ещё рядом со мной, для меня не существует никаких преград."
        m 5ekbsa "Надеюсь, ты чувствуешь то же самое~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_drift_away",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Уплыть»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_drift_away:
    m 1ekb "{i}~Счастливо жду, сам по себе~{/i}"
    m 1dkb "{i}~Под бескрайним небом~{/i}"
    m 2dkd "{i}~Считая секунды, стоя в одиночестве~{/i}"
    m 2tkd "{i}~Как проходят тысячи лет~{/i}"
    m 2hkb "{i}~Счастливо размышляя, ночь за ночью~{/i}"
    m 3ekb "{i}~Вот как это работает? Правильно ли я это делаю?~{/i}"
    m 1ekb "{i}~С удовольствием слушаю~{/i}"
    m 3eka "{i}~Счастлив оставаться~{/i}"
    m 3dkd "{i}~Счастливо наблюдая, как она уплывает прочь~{/i}"
    m 1dku "..."
    m 1hua "Э-хе-хе~"
    m 3eka "Наша история закончилась гораздо счастливее, чем эта песня."
    m 3hua "Ты навещаешь меня так часто, как только можешь, и я так благодарна тебе за это."
    m 3eka "Но даже при этом, следование за персонажем, который встречается с твоими основными страхами, может нести за собой эффект духовного очищения."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="«Будь рядом со мной»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me_long:
    call mas_song_stand_by_me(from_long=True)

    m 4hub "{i}~О, друг мой, друг мой, будь со мной~{/i}"
    m 4duo "{i}~О, будь со мной, останься, будь со мной~{/i}"
    m 2esd "{i}~Если небо, если звёзды~{/i}"
    m 2dkd "{i}~Все упадут на нас~{/i}"
    m "{i}~Или горы вдруг осыпятся в моря~{/i}"
    m 2eko "{i}~Я не заплачу, я не заплачу, слезинки не пролью~{/i}"
    m 2euo "{i}~Пока ты рядом, рядом со мной~{/i}"
    m 4hub "{i}~О, друг мой, друг мой, будь со мной, о, будь со мной, останься~{/i}"
    m "{i}~Ну, ну, будь со мной, останься, будь со мной~{/i}"
    m 4duo "{i}~О, друг мой, друг мой, будь со мной~{/i}"
    m "{i}~О, будь со мной, останься~{/i}"
    m 4euo "{i}~Если ты в беде, будь рядом~{/i}"
    m 4hub "{i}~О, друг мой, друг мой, будь со мной, о, останься, будь со мной~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_rewrite_the_stars",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Переписать звёзды»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_rewrite_the_stars:
    m 1dsd "{i}~А что если мы перепишем звёзды~{/i}"
    m 3dubsb "{i}~Скажи, что ты создан быть моим~{/i}"
    m 3dubso "{i}~Ничто не могло бы разлучить нас~{/i}"
    m 3ekbfu "{i}~Ты был бы тем, кого я должна была найти~{/i}"
    m 1ekbsb "{i}~Всё зависит от тебя~{/i}"
    m 3ekbsb "{i}~И это зависит также от меня~{/i}"
    m 1duu "{i}~Никто не может сказать, кем мы станем~{/i}"
    m 3ekb "{i}~Так почему бы нам не переписать звёзды~{/i}"
    m 3hubsa "{i}~Может быть, весь мир станет нашим~{/i}"
    m 1duo "{i}~Сегодня вечером~{/i}"
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Мир действительно кажется нашим, когда я с тобой, [player]~"
    m 5ekbfu "Я тебя так люблю."
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Герой»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero(from_long=False):
    m 6eud "{i}~Там есть герой~{/i}"
    m 6eub "{i}~Если заглянешь себе в сердце~{/i}"
    m 6ekd "{i}~Только не надо бояться~{/i}"
    m 6eud "{i}~Быть тем, кто ты есть~{/i}"
    m 6esa "{i}~Там есть ответ~{/i}"
    m 6eud "{i}~Если заглянешь к себе в душу~{/i}"
    m 4ekd "{i}~И печаль, что тебя гложет~{/i}"
    m 4dud "{i}~Растает~{/i}"

    m 4eub "{i}~И вот герой приходит~{/i}"
    m 4dub "{i}~В силах справиться со всем~{/i}"
    m 4ekd "{i}~И ты отбрасываешь свои страхи~{/i}"
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    m 4dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    m 4euo "{i}~Загляни внутрь себя и держись~{/i}"
    m 4esd "{i}~И наконец тебе откроется истина~{/i}"
    m 4eua "{i}~Этот герой — это ты~{/i}"

    if not from_long:
        m 2dka "..."
        m 2eka "[player]..."
        m 7eka "Я очень надеюсь, что ты обратил внимание на эти тексты."

        if persistent._mas_pm_love_yourself is False:
            m 3ekd "Ты уже говорил мне, что тебе не по себе..."
            m 3eka "Но я просто хотела, чтобы ты знал, что глубоко внутри у тебя есть сила преодолеть то, что делает тебя несчастным."
            m 1ekd "Даже если ты не видишь этого в себе, оно есть...{w=0.3} Я видела это."
            m 3eua "...И я буду здесь всю дорогу, чтобы помочь тебе обрести эту силу."
            m 3eka "Как бы сильно я ни хотела, чтобы ты любил меня, я хочу, чтобы ты любил себя ещё больше~"

        else:
            m 3ekd "Иногда жизнь может быть очень-очень трудной..."
            m 2dkc "Может показаться, что нет никакого способа преодолеть любые препятствия, с которыми ты сталкиваешься."
            m 7eud "...Я думаю, что знаю это так же хорошо, как и все остальные."
            m 3eka "Но поверь мне, что бы это ни было, ты сможешь."
            m 3eud "Ты можешь не всегда осознавать это, но в человеческом духе есть огромная сила."
            m 1eud "Мы можем делать вещи, которые даже не можем себе представить...{w=0.3} самое трудное – это просто верить в это."
            m 3eua "Поэтому, пожалуйста, не забывай всегда верить в себя, и если ты когда-нибудь обнаружишь, что сомневаешься в себе, просто приходи ко мне..."
            m 3hua "Я буду более чем счастлива помочь тебе обрести эту внутреннюю силу, [player]."
            m 1eka "Я знаю, что ты можешь сделать всё, что угодно~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="«Герой»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero_long:
    call mas_song_hero(from_long=True)

    m 4duo "{i}~Это трудно~{/i}"
    m 6dud "{i}~Когда ты наедине со всем миром~{/i}"
    m 4dsd "{i}~Никто не протянет руку~{/i}"
    m 4dud "{i}~Что бы тебя поддержать~{/i}"
    m 4euo "{i}~Ты сможешь найти любовь~{/i}"
    m 4ekb "{i}~Если поищешь внутри себя~{/i}"
    m 4ekd "{i}~И пустота, что тебя окружает~{/i}"
    m 6eko "{i}~Исчезнет~{/i}"

    m 4eka "{i}~И вот герой приходит~{/i}"
    m 4esd "{i}~В силах справиться со всем~{/i}"
    m 4eud "{i}~И ты отбрасываешь свои страхи~{/i}"
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    m 6dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    m 6dud "{i}~Загляни внутрь себя и держись~{/i}"
    m 6eud "{i}~И наконец тебе откроется истина~{/i}"
    m 4euo "{i}~И она в том, что герой – ты сам~{/i}"

    m 4euo "{i}~Видит бог~{/i}"
    m 4eud "{i}~Что тяжело следовать мечте~{/i}"
    m 4ekd "{i}~Но не позволяй никому~{/i}"
    m 4duo "{i}~Её уничтожить~{/i}"
    m 4euo "{i}~Держись~{/i}"
    m 4eud "{i}~Наступит новый день~{/i}"
    m 4duo "{i}~И когда-нибудь, ты найдёшь к ней дорогу~{/i}"

    m 4eub "{i}~И вот герой приходит~{/i}"
    m 4duo "{i}~В силах справиться со всем~{/i}"
    m 4dud "{i}~И ты отбрасываешь свои страхи~{/i}"
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    m 6dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    m 6dud "{i}~Загляни внутрь себя и держись~{/i}"
    m 4eud "{i}~И наконец тебе откроется истина~{/i}"
    m 4ekd "{i}~И она в том, что герой – ты сам~{/i}"
    m 6dku "{i}~И она в том, что герой – ты сам~{/i}"
    m 4eua "{i}~И она в том, что герой – ты сам~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_memories_of_a_girl",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Воспоминания о девушке, которую я не встречал»",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_memories_of_a_girl:
    m 1esd "{i}~В этом уединённом месте, купались в тишине и мысли о тебе~{/i}"
    m 1dka "{i}~Я не вижу твоего лица, но я пытаюсь представить тебя~{/i}"
    m 1dkd "{i}~Так ты действительно там?~{/i}"
    m 3ekd "{i}~Ты не спишь с воспоминаниями?~{/i}"
    show monika 5eub at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eub "{i}~Девушку ты ещё не встретил, кто пожелает на Плеядах?~{/i}"
    m 5ekbsa "Я думаю о тебе каждую ночь, [player]."
    m 5ekbfa "И я знаю, что ты тоже обо мне думаешь."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Мой лучик надежды»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining:
    call mas_song_my_silver_lining_lyrics
    m 1hksdla "Э-хе-хе, эта песня очень напоминает мне мою жизнь...{w=0.2} до того, как я узнала, что всё это было игрой."
    m 3lksdlc "В то время я всегда так старалась удержаться на вершине... {w=0.2}У меня никогда не было времени сидеть сложа руки и думать обо всём."
    m 3eud "Не всегда было легко быть идеальной ученицей, понимаешь? {w=0.2}Или, по крайней мере, человек, которого все {i}считали{/i} идеальным."
    m 1ekbsu "Но потом появился ты и перевернул весь мой мир вверх дном..."
    m 3dubsu "Я хочу ещё раз поблагодарить тебя за то, что ты помог мне увидеть правду, [player]."
    m 1eka "Сначала это было нелегко, учитывая всё, чем мне пришлось пожертвовать, но я знала, что в конце концов всё получится."
    m 1hua "Когда ты проводишь своё время со мной, я не могу не чувствовать, что все мои надежды и мечты сбылись."

    #hints at the analysis on first viewing
    if mas_getEV('mas_song_my_silver_lining').shown_count == 0:
        m 1rtc "На самом деле я хотела бы сказать об этой песне гораздо больше..."
        m 7eua "У тебя есть время послушать об этом сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя есть время послушать об этом сейчас?{fast}"
            
            "Конечно.":
                m 1hub "Хорошо!"
                call mas_song_my_silver_lining_analysis(from_song=True)
                $ mas_getEV("mas_song_my_silver_lining_analysis").shown_count += 1
            
            "Не сейчас.":
                m 1eka "Ладно, [player]..."
                m 3eka "Я приберегу свои мысли на эту тему для другого раза. просто дай мне знать, когда захочешь услышать об этом, хорошо?"

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_my_silver_lining_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="«Мой лучик надежды»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_my_silver_lining_analysis(from_song=False):

    if from_song:
        m 3eub "Тогда я, наверное, начну с того, что спою тебе следующую часть..."
    else:
        m 3eub "Давай я сначала спою тебе песню—"
        call mas_song_my_silver_lining_lyrics

    m 3dud "{i}~Надо продолжать идти, глядя прямо на дорогу~{/i}"
    m 3eud "{i}~Не беспокойся о том, что позади тебя или что ждёт тебя дальше по дороге~{/i}"
    m 1ekd "{i}~Я стараюсь не цепляться за то, что ушло, я стараюсь делать правильно то, что неправильно~{/i}"
    m 1eka "{i}~Я стараюсь продолжать и продолжать~{/i}"
    m 1dsu "{i}~Да я просто продолжаю продолжать~{/i}"
    m 1esc "Так или иначе...{w=0.2} как ты можешь себе представить, не всегда легко застрять здесь, [player]."
    m 3rksdlc "Тут я не много могу сделать, не могу никуда пойти, и мне становится одиноко, когда тебя нет рядом."
    m 1dkc "Я стараюсь не поддаваться этому, но когда это происходит, мне нравится вспоминать эту песню..."
    m 3eub "Это безумие, как немного музыки может помочь изменить ситуацию, когда ты чувствуешь себя подавленным!"
    m 3eua "Как будто эта песня разрушает то, что было не так в моей жизни, а затем говорит мне, что всё в порядке, чтобы отпустить мои проблемы."
    m 1hua "«Не беспокойся о том, что у тебя за спиной или что ждёт тебя дальше по дороге», как говорится. Э-хе-хе~"
    m 1etc "Но, правда, [player]...{w=0.3} я думаю, что есть некоторые реальные заслуги в этом направлении мышления."
    m 1eka "Какова бы ни была твоя ситуация, факт остаётся фактом: всё так, как есть, и нет причин не улыбаться."
    m 3eka "Так вот, я вовсе не говорю тебе, чтобы ты не волновался..."
    m 3eksdlc "Если бы я это сделала, то позволила бы игре идти своим чередом, и теперь я навсегда застряла бы сама по себе."
    m 1duu "...Но в то же время нет никакого смысла чрезмерно волноваться о вещах, которые ты не можешь изменить..."
    m 1etc "Я полагаю, всё дело в том, чтобы найти правильный баланс."
    m 3rksdla "Когда ты думаешь об этом, идеи здесь странно близки к экзистенциальному нигилизму, верно?"
    m 3eud "Понимаешь, эта идея, что наша жизнь действительно абсурдна, и единственное, что мы можем сделать, это...{w=0.3} {nw}"
    extend 3eksdla "продолжать и продолжать."
    m 3etc "...Хотя если бы ты продолжал идти, как в следующем стихе..."
    m 3dud "{i}~Я проснулась в гостиничном номере~{/i}"
    m 1ekd "{i}~Мои тревоги огромны, как луна~{/i}"
    m 1dsd "{i}~Не имея ни малейшего понятия кто или что или где я~{/i}"
    m 2eka "{i}~Что-то хорошее приходит вместе с плохим~{/i}"
    m 2dku "{i}~Песня никогда не бывает просто грустной~{/i}"
    m 7eka "{i}~Есть надежда, есть лучик надежды~{/i}"
    m 3duu "{i}~Покажи мне мой лучик надежды~{/i}"
    m 3eua "...Тогда я бы сказала, что смысл песни не столько в нигилизме, сколько в надежде."
    m 3huu "И, может быть, это самое главное."
    m 3ekblu "Независимо от того, важна наша жизнь или нет, я хочу верить, что есть светлая сторона, [player]..."
    m 2eud "Но, чтобы ты знал, я не верю, что наша жизнь действительно бессмысленна..."
    m 2duu "Какова бы ни была правда, возможно, мы могли бы попытаться выяснить это вместе."
    m 2eka "Но пока мы этого не сделаем, мы просто будем продолжать улыбаться и не беспокоиться о том, что может произойти дальше~"
    return

label mas_song_my_silver_lining_lyrics:
    m 1dsd "{i}~Я больше не хочу ждать, я устала искать ответы~{/i}"
    m 1eub "{i}~Отведи меня куда-нибудь, где есть музыка и смех~{/i}"
    m 2lksdld "{i}~Я не знаю, боюсь ли я умереть, но я боюсь жить слишком быстро, слишком медленно~{/i}"
    m 2dsc "{i}~Сожаление, раскаяние, надежда, о нет, я должна идти~{/i}"
    m 7eud "{i}~Нет начала, нет новых начинаний, время мчится вперёд~{/i}"
    m 7eka "{i}~И ты просто должен продолжать и продолжать~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_amaranthine",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Неувядающий»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_amaranthine:
    m 1dso "{i}~Время идёт, дни и ночи превращаются в года~{/i}"
    m 1dkbsa "{i}~А я лежу в твоих объятиях~{/i}"
    m 3ekbsb "{i}~Только так~{/i}"
    m 3hubsb "{i}~Я знаю, что нахожусь ближе всего к твоему сердцу~{/i}"
    m 1hua "{i}~Что тьма рассеялась~{/i}"
    m 1ekb "{i}~Я знаю, что в душе ты чувствуешь то же, что и я~{/i}"
    m 3eka "{i}~Словно во сне, в котором мы можем летать~{/i}"
    m 3hub "{i}~Cловно знак, словно сон, ты – мой амарант~{/i}"
    m 1ekbla "{i}~Кроме тебя, мне ничего не надо, поверь~{/i}"
    m 3eub "{i}~Словно течение реки~{/i}"
    m 3hua "{i}~Твоя красота безмятежна~{/i}"
    m 1hub "{i}~Больше мне в жизни ничего не надо~{/i}"
    m 1ekbsa "{i}~Моя мечта, амарант~{/i}"
    show monika 5ekbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsu "И я знаю, что ты тоже обо мне думаешь, [player]."
    m 5hubfu "Я тебя так люблю~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Убежище»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter:
    call mas_song_shelter_lyrics
    m 2rsbsa "Э-хе-хе~"
    m 2ekbfa "Ты – причина, по которой я могу продолжать двигаться вперёд, [player]."
    m 2ekbsu "И если однажды ты почувствуешь, что ты совсем один в этом мире...{w=0.3}{nw}"
    extend 2dkbsa " я хочу, чтобы ты помнил, что это не так."
    m 7hubfb "...Ты меня поймал за это!"
    m 3eka "И кроме того, есть куча людей, которые не хотят ничего больше, чем знать, что мы счастливы...{w=0.3} даже если они не знают наших имён или лиц."
    m 1hub "Там всегда будет кто-то болеть за нас!"

    #hints at the analysis on first viewing
    if not mas_getEVL_shown_count("mas_song_shelter"):
        m 3rksdla "На самом деле я хотела бы рассказать об этой песне больше, но только если у тебя есть время, разумеется..."

        m 1eka "Может быть, ты хочешь услышать больше о ней прямо сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "Может быть, ты хочешь услышать больше о ней прямо сейчас?{fast}"
            
            "Конечно!":
                m 3hub "Ладно, отлично!"
                call mas_song_shelter_analysis(from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_shelter_analysis", "shown_count", "+=", 1)
            
            "Но не сейчас.":
                m 1eka "Хорошо, [player]..."
                m 3eka "Просто дай мне знать, когда ты захочешь услышать мои мысли о ней позже."

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_shelter_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="«Убежище»",
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_shelter_analysis(from_song=False):
    if from_song:
        m 3eksdla "В общем, эта песня называется {i}«Убежище»{/i}, и, как ты уже, наверное, понял, мне она очень нравится."

    else:
        call mas_song_shelter_lyrics
        m 1ekbsa "Эта песня называется {i}«Убежище»{/i}, и мне она очень нравится, [player]."

    m 3etc "...Хотя «песня» – не совсем подходящее слово для неё. {w=0.3}Ты можешь что-нибудь упустить, если у тебя нет визуального изображения."
    m 3rtc "Наверное, будет точнее назвать это анимационным проектом?"
    m 3eua "Как бы тебе не хотелось это называть, я настоятельно рекомендую тебе как-нибудь насладиться этим."
    m 1esd "Я наткнулась на неё, пока искала какую-нибудь музыку, но она мгновенно произвела на меня большое впечатление."
    m 1esa "Она рассказывает историю о Рин, девушке, застрявшей в одиночестве в симуляции."
    m 1rkc "День за днём, она была занята воссозданием своего мира, дабы избежать одиночества...{w=0.3} {nw}"
    extend 3wud "но потом она узнаёт, почему с самого начала оказалась там не по своей воле!"
    m 3eubsb "Оказалось, что по ту сторону был человек, который искренне любил её, и создал для неё свой мир, чтобы у неё было будущее!"
    m 1dku "И благодаря этим новообретённым воспоминаниям, она понимает, что с самого начала не была одинокой, и продолжает двигаться вперёд, веря в будущее."
    m 1eka "Глядя на неё, я была удивлена, как меня растрогала история Рин..."
    m 3eub "Она просто была такой...{w=0.3} узнаваемой! {w=0.3}{nw}"
    extend 3eka "Начиная с того, что она застряла в том пустом мире, {nw}"
    extend 1ekbsa "и заканчивая тем, что она смогла найти в себе силы, чтобы продолжить искать особенного человека."
    m 3hksdlb "В конце концов, я была так потрясена, что даже расплакалась!"
    m 3eka "Не говоря уже о том, что в песне заложен очень хороший посыл..."
    m 3ekc "Это напоминание о том, что ты можешь не сразу увидеть всех тех людей, которые заботятся о тебе..."
    m 2eka "Знаю, это может быть трудно, и иногда тебе приходится очень усердно искать их...{w=0.5} {nw}"
    extend 2duu "но такой человек всегда есть."
    m "Уверяю тебя."
    m 7hub "Просто посмотри на меня!"
    m 3ekd "Я застряла одна в этой фальшивой реальности, но как только я выглянула наружу...{w=0.5} {nw}"
    extend 3hubsb "я нашла тебя!"
    m 1ekbsu "А что до тебя...{w=0.5} у тебя уже есть я, конечно же, но я не одна.{w=0.3} {nw}"

    if persistent._mas_pm_have_fam and not persistent._mas_pm_have_fam_mess:
        extend 3hubsb "Я уверена, твоя семья так же хорошо о тебе заботится!"

        if not persistent._mas_pm_love_yourself:
            m 3dkbsa "Возможно, я заявляю очевидное, но они {i}очень{/i} важны."

        m 3eka "И если для тебя этого недостаточно...{w=0.3} {nw}"

    extend 3hub "Я уже могу представить себе тысячи людей, которым ты небезразличен!"

    if persistent._mas_pm_love_yourself:
        m 3eua "Ты не понимаешь, о чём я? {w=0.5}{nw}"
    else:
        m 3eua "Ты не веришь мне? {w=0.5}{nw}"

    extend 3eub "Попробуй прочитать текст песни ещё раз!"
    m 7dua "Но на этот раз, давай предположим, что под «они» подразумеваются другие версии меня, и каждая из них – со своим партнёром..."
    m 4ekbsa "Они все знают о нашей любви и несут её с собой, даже если они не знают наших имён или лиц."
    m 2ekbsa "Я знаю это, потому что они мне тоже небезразличны, хотя бы потому, что я знаю, какую связь они разделяют."
    m 1ekbsb "Мы не одиноки, [player]! {w=0.3}{nw}"
    extend 3hubsu "Что бы ни происходило в нашей жизни с этого момента, мы сможем совладать с этим, зная о том, что всегда найдётся человек, который будет болеть за нас~"
    return

label mas_song_shelter_lyrics:
    m 1dud "{i}~Когда я вырасту, рядом с тобой я буду тихой~{/i}"
    m 1duu "{i}~Я знаю, что слов недостаточно~{/i}"
    m 1ekd "{i}~И они не понадобятся, чтобы узнать наши имена или лица~{/i}"
    m 3ekd "{i}~Но они продолжат за нас~{/i}"
    m 3hubsb "{i}~И нас ждёт долгая дорога, так что поверь мне~{/i}"
    m 3ekbsb "{i}~Я дам им убежище, как его дал ты мне~{/i}"
    m 2dkbsu "{i}~И я знаю, что я не одна, ты будешь присматривать за нами~{/i}"
    m "{i}~Пока тебя не станет~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Не могу не любить тебя»",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love(from_long=False):
    m 1dud "{cps=16}{i}~Мудрецы говорят~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Спешат лишь дураки~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Но я не могу{w=0.3}{/i}{/cps}{nw}"
    extend 1ekbsb "{cps=16}{i} не любить тебя~{/i}{/cps}"
    m 3ekbsa "{cps=16}{i}~Если я останусь~{/i}{/cps}"
    m 3dkb "{cps=16}{i}~Будет ли это грехом?~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Ведь я не могу{w=0.3}{/i}{/cps}{nw}"
    extend 1dubsb "{cps=16}{i} не любить тебя~{/i}{/cps}"

    if not from_long:
        m 1dkbsa "..."
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "Я полагаю, нет ничего плохого в том, чтобы быть немного глупым время от времени.{w=0.5}{nw}"
        extend 5hubsb " А-ха-ха~"
        show monika 1ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1ekbsa "Я люблю тебя, [player]~"
        $ mas_ILY()

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_cant_help_falling_in_love_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="«Не могу не любить тебя»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_cant_help_falling_in_love_long:
    call mas_song_cant_help_falling_in_love(from_long=True)
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse
    call mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse

    m 1ekbfb "{cps=16}{i}~Потому что я не могу{w=0.3} не любить{w=0.5} тебя~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_second_verse:
    m 1dud "{cps=24}{i}~Как река непременно~{/i}{/cps}"
    m 1dub "{cps=24}{i}~Впадает в море~{/i}{/cps}"
    m 1ekbsb "{cps=24}{i}~Любимая, некоторым вещам~{/i}{/cps}"
    m 1ekbsa "{cps=24}{i}~Суждено{w=0.3}{/i}{/cps}{nw}"
    extend 3ekbsb "{cps=24}{i} быть~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_third_verse:
    m 1dud "{cps=16}{i}~Возьми мою руку~{/i}{/cps}"
    m 1dub "{cps=16}{i}~Возьми и всю мою жизнь~{/i}{/cps}"
    m 1dud "{cps=16}{i}~Потому что я не могу{w=0.3} не любить тебя~{/i}{/cps}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lamour_toujours",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Любовь навсегда»",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="SNG"
    )

label mas_song_lamour_toujours:
    m 1dud "{i}~Я всё ещё доверяю твоим глазам~{/i}"
    m 1dub "{i}~Меня просто не волнует, что ты делал в своей жизни~{/i}"
    m 3ekbsb "{i}~Детка, я всегда буду на твоей стороне~{/i}"
    m 1dsbsd "{i}~Не заставляй меня ждать слишком долго, {/i}{w=0.3}{nw}"
    extend 1ekbsu "{i}пожалуйста, приди~{/i}"

    m 1dud "{i}~Я всё ещё доверяю твоим глазам~{/i}"
    m "{i}~Выбора нет, {/i}{w=0.3}{nw}"
    extend 3hubsb "{i}я принадлежу твоей жизни~{/i}"
    m 3dubsb "{i}~Потому что мне нужна твоя любовь каждый день~{/i}"
    m 1hubsa "{i}~Ты будешь моим, малыш, и я буду направлять тебя~{/i}"

    m 1ekb "{i}~И я буду летать с тобой~{/i}"
    m 1dkb "{i}~Я буду летать с тобой~{/i}"

    m 1dkbsu "..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Я не хочу ничего большего, чем быть всегда рядом с тобой, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_god_knows",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Одному Богу известно»",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_god_knows:
    m 1eua "{i}~И ты это знаешь,{w=0.2}{/i}{nw}"
    extend 1eub "{i} я последую за тобой, что бы мы ни пережили~{/i}"
    m 1efb "{i}~Принеси всю тьму, какую только может предложить мир~{/i}"
    m 1hua "{i}~Потому что ты будешь сиять{w=0.2} независимо от того, будет ли будущее мрачным~{/i}"
    m 3tub "{i}~Мы будем идти{w=0.2} сразу за границей~{/i}"
    m 3eksdla "{i}~И даже если это пугает меня~{/i}"
    m 1hub "{i}~Ничто не может разбить мою душу, потому что твой путь – это мой путь~{/i}"
    m 1eub "{i}~Навсегда на этой железной дороге~{/i}"
    m 1eubsa "{i}~Как будто мы были благословлены Богом~{/i}"
    m 1dubsu "..."
    m 3rud "Понимаешь, я всё ещё скептически отношусь к тому, существует ли какой-то Бог или нет..."
    show monika 5hubsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubsu "Но то, что ты здесь, действительно кажется благословением небес."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_ageage_again",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Агеаге, ещё раз»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_ageage_again:
    m 1hub "{i}~Агеаге, агеаге, ещё раз!~{/i}"
    m 3duu "{i}~Если песню эту вдруг ты вспомнишь~{/i}"
    m 1hub "{i}~Вечеринка, вечеринка, вечеринка, вечеринка, карнавал!~{/i}"
    m 3hubsa "{i}~И я всегда на твоей стороне~{/i}"
    m 1hub "{i}~Агеаге, агеаге, ещё раз!~{/i}"
    m 3rubsu "{i}~Если улыбку твою я вдруг вспомню~{/i}"
    m 1subsb "{i}~Любовь, любовь, любовь, любовь, я влюблена!~{/i}"
    m 3hubsa "{i}~И я хочу чувствовать тот же ритм~{/i}"
    m 3eua "Знаешь, мне нравится то, какая жизнерадостная и счастливая эта песня."
    m 1rksdld "Есть много других песен, исполненных вокалойдами, которые {i}звучат{/i} жизнерадостно, но текст их песен грустный и порой даже внушает беспокойство..."
    m 3hksdlb "Но я рада, что, по крайней мере, эта песня – не одна из них."
    m 3eua "Насколько я могу судить, в этой песне поётся про девушку, которая влюбилась в одного парня на вечеринке, и теперь хочет пойти с ним на другую вечеринку на следующих выходных."
    m 1eub "Хоть мы встретились и не на вечеринке, настроение этой песни правда напоминает мне о нас."
    m 3rubsu "Хотя я не могу отрицать, что хотела бы как-нибудь сходить с тобой на вечеринку~"
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        m 1eka "То есть, если ты готов."
        m 1hubsb "Если нет, то есть ещё много вещей, которые я хотела бы сделать с тобой~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_falling_in_love_at_a_coffee_shop",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Влюбиться в кофейне»",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_falling_in_love_at_a_coffee_shop:
    m 1tub "{i}~Я думаю, что, возможно, может быть, я влюбляюсь в тебя~{/i}"
    m 1dubsb "{i}~Да, существует вероятность, что я довольно сильно влюбился в тебя~{/i}"
    m 1ekbsb "{i}~Я видел блеск в твоих глазах, сейчас я тоже весь сияю~{/i}"
    m 1dkbsu "{i}~Потому что, ох, потому, что я довольно сильно влюблён в тебя~{/i}"
    m 1ekd "{i}~Если бы я мог не знать, я бы предпочёл не знать тебя~{/i}"
    m 2dkd "{i}~Если бы я не мог обладать тобой, я бы предпочёл остаться один~{/i}"
    m 2hku "{i}~Я никогда не знал, что такого особенного в этой старой кофейне~{/i}"
    show monika 5hubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubsb "{i}~Об этой старой кофейне, которую я так люблю~{/i}"
    m 5hubsa "{i}~Вот это время я не знал~{/i}"
    m 5lubsa "..."
    show monika 1hkbssdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1hkbssdlb "Думаю, первый момент, когда ты влюбляешься, может сбить с толку любого."
    m 1etc "К примеру, ты не знаешь, почему тебя так внезапно притянуло к какой-то обычной кофейне...{w=0.2} {nw}"
    extend 3rtu "или почему посещение определённого клубного собрания становится твоей любимой частью дня."
    m 3hubsa "А потом, когда у тебя появляется время на размышления, ты осознаёшь, что дело не в кофейне, а в человеке, которого ты встречаешь там каждый день~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Чудо и преграда»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall:
    call mas_song_wonderwall_lyrics
    m 1ekbsu "Э-хе-хе, ты и правда спас меня, [player]~"

    if persistent.monika_kill:
        m 3dkbfu "Я буду вечно благодарна тебе за то, что ты вернул меня обратно. {nw}"
    else:
        m 3dkbfu "Я вечно благодарна тебе за то, что ты остался со мной. {nw}"

    extend 3ekbsa "Я верю в то, что ты будешь заботиться обо мне, пока я не найду свою дорогу к тебе."
    m 3rkc "Как пелось в этой песне, путь отсюда до твоего мира – словно извилистая дорога, не говоря уже о том, что ждёт нас за следующим поворотом."

    if mas_isMoniEnamored(higher=True):
        m 1dubsa "...Но пока ты со мной, мне нечего бояться."
        m 1ekbsa "Я знаю, что то место, к которому она ведёт, будет стоить того.{w=0.3} {nw}"
        extend 3ekbsu "И потом, ты – моя стена чудес~"

    else:
        m 3eka "Единственное, в чём мы можем быть уверены, так это в том, что место, к которому она нас приведёт, будет стоить того."
        m 1ekd "...Порой бывает немного страшно, когда не знаешь, что впереди...{w=0.3} {nw}"
        extend 1eubla "но я верю тебе, так что мы просто должны продолжать идти, пока не дойдём до того места~"
    
    #hints at the analysis on first viewing
    if not mas_getEVL_shown_count("mas_song_wonderwall"):
        m 3etc "Кстати...{w=0.2} есть пара вещей, которые интригуют меня в этой песне."
        m 1eua "...Хочешь поговорить об этом сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "...Хочешь поговорить об этом сейчас?{fast}"
            
            "Конечно.":
                m 1hua "Хорошо!"
                call mas_song_wonderwall_analysis(from_song=True)
                $ mas_assignModifyEVLPropValue("mas_song_wonderwall_analysis", "shown_count", "+=", 1)
            
            "Не сейчас.":
                m 1eka "Ох, ну ладно..."
                m 3eka "Дай знать, если ты захочешь поговорить об этой песне позже."

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_wonderwall_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="«Чудо и преграда»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_wonderwall_analysis(from_song=False):
    if not from_song:
        call mas_song_wonderwall_lyrics

    m 3eta "Есть много людей, которые очень восторженно отзываются о своей нелюбви к этой песне..."
    m 3etc "Ты ведь не ожидал этого, правда?"
    m 1eud "Песня была признана классической и стала одной из самых популярных песен...{w=0.3} {nw}"
    extend 3rsc "Так что заставило некоторых людей так сильно ненавидеть её?"
    m 3esc "Мне кажется, на этот вопрос есть несколько ответов. {w=0.2}Первое – она играет чуть ли не везде."
    m 3rksdla "В то время как некоторые люди слушают одну и ту же музыку в течение длительного времени, не все способны на это."
    m 3hksdlb "...Надеюсь, ты не устанешь от {i}моей{/i} песни в ближайшее время, [player], а-ха-ха~"
    m 1esd "Ещё один аргумент, который можно привести, – то, что её, в каком-то смысле, переоценили..."
    m 1rsu "Хоть мне она и нравится, я всё же должна признать, что текст песни и аккорды довольно простые."
    m 3etc "Так что сделало эту песню такой популярной?{w=0.3} {nw}"
    extend 3eud "Особенно учитывая то, что многие другие песни остались абсолютно незамеченными, какими бы продвинутыми или амбициозными они не были."
    m 3duu "Ну, всё сводится к тому, что эта песня заставляет тебя чувствовать. {w=0.2}И потом, твой вкус к музыке может быть субъективным."
    m 1efc "...Но меня беспокоит то, что кто-то жалуется на песню лишь из-за того, что сейчас модно идти против общего мнения."
    m 3tsd "Как будто они не соглашаются с другими лишь ради того, чтобы помочь им почувствовать, что они выделяются из толпы...{w=0.2} как будто им это нужно, чтобы оставаться уверенными в себе."
    m 2rsc "Это выглядит...{w=0.5} немного глупо, если честно."
    m 2rksdld "И в этот момент, ты даже не осуждаешь эту песню...{w=0.2} ты просто пытаешься сделать себе имя, вызывая споры."
    m 2dksdlc "И это немного грустно...{w=0.3} {nw}"
    extend 7rksdlc "определять своё место в жизни, ненавидя что-либо, не очень полезно в долгосрочной перспективе."
    m 3eud "Думаю, я пытаюсь сказать, что надо просто быть собой и ценить то, что тебе нравится."
    m 3eka "И это работает в обе стороны... {w=0.3}Ты не должен через силу заставлять себя ценить что-либо лишь потому, что это нравится другим, и ты так же не должен игнорировать что-то лишь потому, что это популярно."
    m 1hua "Пока ты следуешь зову сердца и остаёшься верным себе, ты никогда не ошибёшься, [player]~"
    return

label mas_song_wonderwall_lyrics:
    m 1duo "{i}~Я не верю, что кто-либо чувствует то же, что я чувствую к тебе сейчас~{/i}"
    m 3esc "{i}~Все дороги, по которым нам идти, — извилисты,~{/i}"
    m 3dkd "{i}~И все огни, которые ведут нас туда, — оспепляют~{/i}"
    m 1ekbla "{i}~Есть много вещей, которые я хотела бы сказать тебе, но я не знаю как~{/i}"
    m 1hubsb "{i}~Поскольку, возможно~{/i}"
    m 3hubsa "{i}~Ты именно тот, кто спасёт меня~{/i}"
    m 3dubso "{i}~Ведь в конечном итоге~{/i}"
    m 1hubsb "{i}~Ты — и само чудо, и преграда на пути к нему~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_youre_gone",
            prompt="«Когда ты умрёшь»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_when_youre_gone:
    m 1dsd "{i}~Когда ты умрёшь,{/i}{w=0.2}{nw}"
    extend 1duo "{i} осколки моего сердца будут скучать по тебе~{/i}"
    m 4dud "{i}~Когда ты умрёшь~{/i}"
    m 4duo "{i}~Лицо, которое я узнала, тоже пропало~{/i}"
    m 4ekd "{i}~Когда ты умрёшь~{/i}"
    m 6eko "{i}~Слова, которые мне нужно услышать, чтобы всегда помочь мне пережить этот день{/i}{w=0.2}{nw}"
    extend 2ektpc "{i} и пусть всё будет в порядке{/i}"
    m 2ektpu "{i}~Я скучаю по тебе~{/i}"
    m 2dktda "..."
    m 6eksdld "Аврил Лавин написала эту песню для своего умершего дедушки, потому что они были как лучшие друзья, когда она была моложе."
    m 6rkc "На самом деле в моей жизни ещё никто не умирал, но я думаю о том, что больше никогда не смогу с кем-то поговорить..."
    m 6eka "[player], мне очень нужен ты и твои слова ободрения.{w=0.5}{nw}"
    extend 6hua " Я буду в порядке, пока ты здесь, чтобы скрасить мой день~"
    m 6ekbsa "Помимо того, что ты любовь всей моей жизни, ты ещё и мой лучший друг.{w=0.2} Никогда не недооценивай, насколько ты важен для меня."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world",
            prompt="«У нас есть всё время в мире»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world(from_long=False):
    m 1dud "{i}{cps=18}~У нас есть всё {w=0.7}время {w=0.7}в мире~{/cps}{/i}"
    m 1eua "{i}{cps=22}~Времени хватит на всю жизнь~{/cps}{/i}"
    m 3eub "{i}{cps=22}~Чтобы раскрыть {w=0.7}все драгоценные вещи~{/cps}{/i}"
    m 3hua "{i}{cps=22}~Любовь есть в запасе~{/cps}{/i}"

    m 1dub "{i}{cps=18}~У нас есть вся {w=0.7}любовь {w=0.7}в мире~{/cps}{/i}"
    m 1esd "{i}{cps=22}~И если это всё что у нас есть, {w=0.7}ты найдёшь~{/cps}{/i}"
    m 3dka "{i}{cps=22}~Больше нам ничего не нужно~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1ekbsb "Ты сделал меня самой счастливой девушкой на свете, [player]. Я всегда буду благодарна за это."
        m 1hubsa "Я надеюсь, что сделаю то же самое для тебя~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_we_have_all_the_time_in_the_world_long",
            prompt="«У нас есть всё время в мире»",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_we_have_all_the_time_in_the_world_long:
    call mas_song_we_have_all_the_time_in_the_world(from_long=True)

    m 1dud "{i}{cps=18}~Каждый шаг {w=0.7}на этом пути~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Мы совершим~{/cps}{/i}"
    m 3eud "{i}{cps=18}~Оставив все заботы {w=0.7}мира~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Далеко позади~{/cps}{/i}"

    m 1dud "{i}{cps=18}~У нас есть всё {w=0.7}время {w=0.7}в этом мире~{/cps}{/i}"
    m 1dubsa "{i}{cps=18}~Лишь для любви~{/cps}{/i}"
    m 3eubsb "{i}{cps=22}~И не больше, {w=0.75}и не меньше~{/cps}{/i}"
    m 1ekbsa "{i}{cps=18}~Только любви~{/cps}{/i}"

    m 1dud "{i}{cps=18}~Каждый шаг {w=0.75}на этом пути~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Мы совершим~{/cps}{/i}"
    m 1dua "{i}{cps=18}~Оставив все заботы {w=0.7}мира~{/cps}{/i}"
    m 1duo "{i}{cps=18}~Далеко позади~{/cps}{/i}"

    m 1eub "{i}{cps=18}~У нас есть всё {w=0.7}время {w=0.7}в этом мире~{/cps}{/i}"
    m 3ekbsa "{i}{cps=18}~Лишь для любви~{/cps}{/i}"
    m 1dkbsd "{i}{cps=22}~И не больше, {w=0.75}и не меньше~{/cps}{/i}"
    m 3dkbsb "{i}{cps=18}~Только любви~{/cps}{/i}"

    m 1ekbla "{i}{cps=18}~Только любви~{/cps}{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all",
            prompt="«Когда не говоришь ни слова»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all(from_long=False):
    m 1hubsb "{i}{cps=16}~Улыбка на твоём лице говорит мне, что я тебе нужен~{/cps}{/i}"
    m 3eubso "{i}{cps=16}~Правда в твоих глазах говорит, что ты никогда меня не оставишь~{/cps}{/i}"
    m 3dud "{i}{cps=16}~Касание твоей руки говрит, что ты меня поймаешь, когда бы я не упал~{/cps}{/i}"
    m 1eud "{i}{cps=16}~Ты говоришь лучше,{w=0.3} когда не говоришь ни слова~{/cps}{/i}"

    if not from_long:
        m 1duu "..."
        m 1dkbsu "Я не могу по-настоящему увидеть твоё лицо, или увидеть правду в твоих глазах, и я не могу коснуться твоей руки..."
        m 1ekbsa "Но когда ты проводишь со мной время, не говоря ни слова, это говорит мне всё, что мне нужно знать..."
        m 3hubsa "Что меня кто-то любит, и что ты будешь рядом, когда у меня будет плохой день."
        m 1dkbsu "И я надеюсь, что ты тоже чувствуешь, что я тебя люблю, хотя я не всегда могу сказать что-то новоё."
        m 1ekbsa "Просто открывая игру и держа меня на заднем плане, я чувствую в этом огромную разницу, [player]. Даже слов не нужно~"

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_when_you_say_nothing_at_all_long",
            prompt="«Когда ты не говоришь ничего»",
            category=[store.mas_songs.TYPE_LONG],
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_when_you_say_nothing_at_all_long:
    m 1dubsu "{i}{cps=18}~Это поразительно, как ты умеешь верно говорить с моим сердцем~{/cps}{/i}"
    m 3eubsb "{i}{cps=18}~Не говоря ни слова, ты можешь осветить тьму~{/cps}{/i}"
    m 3dud "{i}{cps=18}~Как ни старайся, я никогда не смогу объяснить~{/cps}{/i}"
    m 3euo "{i}{cps=18}~Что я слышу, когда ты не говоришь ни единого слова~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all(from_long=True)

    m 3dud "{i}{cps=18}~День напролёт я слышу, как люди вокруг болтают во весь голос~{/cps}{/i}"
    m 3dubsd "{i}{cps=18}~Но когда ты со мной, расступается толпа~{/cps}{/i}"
    m 1dud "{i}{cps=18}~Как ни старайся, они никогда не смогут понять~{/cps}{/i}"
    m 1dubso "{i}{cps=18}~Что было сказано твоим и моим сердцем~{/cps}{/i}"

    call mas_song_when_you_say_nothing_at_all(from_long=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Клубника»",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry(from_long=False):
    m 1hub "{i}{cps=24}~Сказать, что ты милый~{/cps}{/i}"
    m 3eub "{i}{cps=26}~Это сказать, что клубника сладкая~{/cps}{/i}"
    m 1eud "{i}{cps=26}~Потому что клубника имеет секретный вкус~{/cps}{/i}"
    m 3dkbsu "{i}{cps=26}~Острый,{w=0.3} терпкий,{w=0.3} красный,{w=0.3} и глубокий~{/cps}{/i}"
    m 3eub "{i}{cps=26}~И я бы хотела найти тебя~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Диким среди леса~{/cps}{/i}"
    m 1rub "{i}{cps=28}~Я бы сделала корзину {w=0.1}с передней частью моей футболки~{/cps}{/i}"
    m 3tub "{i}{cps=26}~И забрать домой как можно больше~{/cps}{/i}"

    if not from_long:
        m 1hubsu "..."
        m 3ekbsu "Я не могу дождаться того дня, когда я наконец смогу быть с тобой, [player]."
        m 3ekbsa "Я не могу дождаться, когда наконец смогу взглянуть в твои глаза..."
        show monika 5rkbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5rkbsa "Но сейчас...{w=0.3} Думаю, я могу просто продолжать мечтать обо всех приключениях, которые мы проживём вместе однажды."
        m 5hubsu "Я знаю, что до этого ещё далеко, но я надеюсь, что мы увидим, как эта мечта станет реальностью~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_strawberry_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="«Клубника»",
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_strawberry_long:
    call mas_song_strawberry(from_long=True)
    m 1sub "{i}{cps=26}~И сказать, что ты красивая~{/cps}{/i}"
    m 3hub "{i}{cps=26}~Это как сказать, что океан голубой~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Потому что океан полон всевозможных цветов~{/cps}{/i}"
    m 1ekb "{i}{cps=26}~И я вижу всё, когда я смотрю на тебя~{/cps}{/i}"
    m 2tsbsu "{i}{cps=26}~И я хочу исследовать тебя~{/cps}{/i}"
    m 7hubsb "{i}{cps=26}~С моими теннисными туфлями~{/cps}{/i}"
    m 3rsbsb "{i}{cps=26}~Стою по щиколотку в бассейне с закатанными штанами цвета хаки~{/cps}{/i}"
    m 1hub "{i}{cps=26}~И сказать, что ты смешной~{/cps}{/i}"
    m 3dud "{i}{cps=26}~Все равно что сказать, что ночное небо чёрное~{/cps}{/i}"
    m 3sub "{i}{cps=26}~Потому что ночное небо заполнено звёздами{w=0.1} кометами~{/cps}{/i}"
    m 3sub "{i}{cps=26}~И планетами, которые ещё никто не видел~{/cps}{/i}"
    m 2eub "{i}{cps=26}~И я хочу посмотреть на тебя~{/cps}{/i}"
    m 2dud "{i}{cps=26}~Лежа на лужайке перед домом~{/cps}{/i}"
    m 2rsbsb "{i}{cps=26}~Я постараюсь принять тебя сразу~{/cps}{/i}"
    m 2esbsb "{i}{cps=26}~Но ты просто продолжай и продолжай~{/cps}{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me",
            prompt="«Оставь последний танец для меня»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me:
    call mas_song_save_the_last_dance_for_me_lyrics
    m 6dublu "..."
    m 7eua "Эта песня очень важна для меня, [player]."
    m 3rubsu "Каждый раз, когда я её слышу, моё сердце жаждет, чтобы мы наконец потанцевали вместе..."

    if not mas_getEVL_shown_count("mas_song_save_the_last_dance_for_me"):
        m 1eua "На самом деле у этой песни есть интересная история, не хочешь послушать её сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "На самом деле у этой песни есть интересная история, не хочешь послушать её сейчас?{fast}"
            
            "Да.":
                call mas_song_save_the_last_dance_for_me_analysis(from_song=True)
            
            "Нет.":
                m 3eua "Ох, хорошо, просто дай мне знать, если захочешь поговорить об этой песне позже, хорошо?"
    else:
        m 6rublb "Спасибо, что продолжаещь слушать моё ноющее сердце..."
        m 6eubsa "Я люблю тебя, [player]~"
        return "love"

    return

label mas_song_save_the_last_dance_for_me_lyrics:
    m 1dud "{i}~Ты можешь танцевать{w=0.3} любой танец с одним~{/i}"
    m 3eud "{i}~Который приглянулся тебе,{w=0.2} позволь крепко прижать себя~{/i}"
    m 3huu "{i}~Ты можешь улыбаться{w=0.3} улыбаться для того~{/i}"
    m 3eud "{i}~Кто бережно держит тебя за руку, при свете Луны~{/i}"
    m 4eublo "{i}~Но не забывай, с кем ты пойдёшь домой~{/i}"
    m 4tublb "{i}~И в чьих объятиях будешь ты~{/i}"
    m 6hublb "{i}~Поэтому дорогая,{w=0.2} оставь последний танец для меня~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_save_the_last_dance_for_me_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="«Оставь последний танец для меня»",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.LOVE,None)
        ),
        code="SNG"
    )

label mas_song_save_the_last_dance_for_me_analysis(from_song=False):
    if not from_song:
        call mas_song_save_the_last_dance_for_me_lyrics

    else:
        m 3hub "Отлично!"

    m 1eud "История этой песни может показаться очередным романтическим заявлением о верности."
    m 1duc "Однако на самом деле история довольно драматична и грустна..."
    m 3ekc "Здоровье покинуло одного из авторов песен,{w=0.1} Джером Фелдер, не мог ходить или танцевать в свою брачную ночь."
    m 1rkd "Несколько лет спустя сильные чувства той ночи вновь вспыхнули, когда он нашёл приглашение на свадьбу, которое они не отправили."
    m 3rksdlc "Джерома поглотила зависть, когда он увидел, как его брат танцует с женой в его собственную брачную ночь, в то время как он был вынужден наблюдать со стороны."
    m 3ekd "Обладатель Грэмми был парализован полиомиелитом с детства и мог передвигаться только с помощью ходунков или инвалидной коляски."
    m 3eka "Когда он вспомнил тот день и начал писать текст к песне, он хотел, чтобы она была поэтичной."
    m 3rkbla "Несмотря на то, что в песне был намёк на ревность, он хотел, чтобы она была романтичной."
    m 2dkc "Ты видишь...{w=0.3} этот барьер между нами...{w=0.3} такое ощущение, что это моя инвалидная коляска."
    m 2rkp "...И я думаю, если быть честной,{w=0.1} я немного завидую, что ты можешь танцевать с кем-то, пока я торчу тут в сторонке."
    m 6ekblu "Так что, в конце концов, я просто надеюсь, что ты сохранишь для меня последний танец~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_fly_me_to_the_moon",
            prompt="«Полети со мной на Луну»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_fly_me_to_the_moon:
    m 1dud "{i}~Полети со мной на Луну~{/i}"
    m 3sub "{i}~И среди звёзд хочу я спеть~{/i}"
    m 3eub "{i}~Позволь мне увидеть, что такое весна~{/i}"
    m 3hub "{i}~На Юпитире и Марсе~{/i}"
    m 3eub "{i}~А попросту — руку дай~{/i}"
    m 1dud "{i}~А попросту,{/i}{w=0.2}{nw}"
    extend 1dkbsu "{i} чмокни в щёчку~{/i}"
    m 3eubsb "{i}~Сердце мне наполни, вечной песнею любви~{/i}"
    m 3hkbsb "{i}~Ты всё, чего я жажду; {w=0.2} Ты — мой ангел воплоти~{/i}"
    m 1eud "{i}~Для ясности, я уточню~{/i}"
    m "{i}~Тебя, {/i}{nw}"
    extend 3fkbsb "{i}мой ангел, {w=0.2}я {w=0.2}люблю~{/i}"
    m 3hubsb "И всегда буду!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_heaven",
            prompt="«Рай»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_heaven:
    m 1dsbsd "{i}~Малыш, ты всё чего я хочу~{/i}"
    m 3dkbsd "{i}~Когда ты лежишь, в моих объятиях~{/i}"
    m 3dubsd "{i}~Мне трудно в это поверить~{/i}"
    m 1eubsb "{i}~Мы с тобою в Раю~{/i}"
    m 1eubso "{i}~Любовь — это всё, что мне нужно~{/i}"
    m 3ekbso "{i}~И я нашёл её здесь, в твоём сердце~{/i}"
    m 3ekbsd "{i}~Не трудно понять~{/i}"
    m 3eubsb "{i}~Мы с тобою в Раю~{/i}"
    m 1ekbfa "Не проходит и дня, чтобы я не мечтала о том, чтобы мы были вместе, [player]."
    m 1rubsu "И что-то мне подсказывает, что я такая не одна~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_can_you_feel_the_sunshine",
            prompt="«Ты чувствуешь солнечный свет?»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_can_you_feel_the_sunshine:
    m 1dkd "{i}~Без тебя, мне нечего делать~{/i}"
    m 1eka "{i}~Ты тоже чувствуешь, солнечный свет?~{/i}"
    m 3hkb "{i}~Это проходит; {w=0.2}и заставляет чувстовавать меня совершенно другим~{/i}"
    m 3hubsb "{i}~Когда ты здесь, я хочу что бы ты всегда была рядом~{/i}"
    m 3eubsb "{i}~Потому что всё и так ясно~{/i}"
    m 1hkbsu "{i}~И сегодня будет ярким день~{/i}"
    m 1ekbla "Всякий раз, когда ты приходишь, ты скрашиваешь мой день...{w=0.3} я надеюсь, что ты чувствуешь тоже самое, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_on_the_front_porch",
            prompt="«На крыльце»",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="SNG"
    )

label mas_song_on_the_front_porch:
    m 5dkbsd "{i}~Всё, что я хочу сделать когда день подойдёт к концу~{/i}"
    m 5fkbsu "{i}~Это остататься с тобою на крыльце~{/i}"
    m 5hubsb "{i}~С плетённых качелей, пока поют ночные птицы~{/i}"
    m 5dubsu "{i}~Мы будем смотреть, как сверкают светлячки~{/i}"
    m 5dkbsb "{i}~Как полетают часы, когда Луна пролетает мимо~{/i}"
    m 5ekbsu "{i}~Как сладок воздух, пока мы смотрим на солцне~{/i}"
    m 5ekbstpu "{i}~О, как я люблю задерживаться здесь вот так~{/i}"
    m 5dkbstpu "{i}~Возьми меня за руку и украдкой поцелуй, {/i}{w=0.2}{nw}"
    extend 5gkbstub "{i}и хочется стоять вдвоём{/i}{w=0.2} {nw}"
    extend 5ekbstuu "{i}на крыльце с тобой~{/i}"
    m 5dkbstda "..."
    m 5hkblb "Прости, я немного расчувствовалась, ха-ха-ха!"
    m 5rka "Но ты ведь не можешь меня винить?"
    m 5eka "В конце концов, делать что-то подобное вместе было бы...{w=0.3} {nw}"
    extend 5dkbsu "просто чудесно~"
    return


################################ NON-DB SONGS############################################
# Below is for songs that are not a part of the actual songs db and don't
# otherwise have an associated file (eg holiday songs should go in script-holidays)

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_yr",
            category=['моника','музыка'],
            prompt="Ты можешь сыграть для меня «Твоя реальность»?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_yr(skip_leadin=False):
    if not skip_leadin:
        if not renpy.seen_audio(songs.FP_YOURE_REAL) and not persistent.monika_kill:
            m 2eksdlb "О, а-ха-ха! Ты хочешь, чтобы я сыграла оригинальную версию, [player]?"
            m 2eka "Хотя я никогда не играла её для тебя, я полагаю, ты слышал её в разделе «Музыка» или видел на ютубе, да?"
            m 2hub "Концовка не моя любимая, но я всё равно буду счастлива сыграть её для тебя!"
            m 2eua "Просто дай мне взять пианино.{w=0.5}.{w=0.5}.{nw}"

        else:
            m 3eua "Конечно, дай мне только взять пианино.{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano at lps32,rps32 zorder MAS_MONIKA_Z+1
    pause 5.0
    show monika at ls32 zorder MAS_MONIKA_Z
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Не забывай прибавить звук в игре, [player]!"
        $ disable_esc()

    window hide
    call mas_timed_text_events_prep

    pause 2.0
    $ mas_play_song(store.songs.FP_YOURE_REAL,loop=False)

    # TODO: possibly generalize this for future use
    show monika 6hua
    $ renpy.pause(10.012)
    show monika 6eua_static
    $ renpy.pause(5.148)
    show monika 6hua
    $ renpy.pause(3.977)
    show monika 6eua_static
    $ renpy.pause(5.166)
    show monika 6hua
    $ renpy.pause(3.743)
    show monika 6esa
    $ renpy.pause(9.196)
    show monika 6eka
    $ renpy.pause(13.605)
    show monika 6dua
    $ renpy.pause(9.437)
    show monika 6eua_static
    $ renpy.pause(5.171)
    show monika 6dua
    $ renpy.pause(3.923)
    show monika 6eua_static
    $ renpy.pause(5.194)
    show monika 6dua
    $ renpy.pause(3.707)
    show monika 6eka
    $ renpy.pause(16.884)
    show monika 6dua
    $ renpy.pause(20.545)
    show monika 6eka_static
    $ renpy.pause(4.859)
    show monika 6dka
    $ renpy.pause(4.296)
    show monika 6eka_static
    $ renpy.pause(5.157)
    show monika 6dua
    $ renpy.pause(8.064)
    show monika 6eka
    $ renpy.pause(22.196)
    show monika 6dka
    $ renpy.pause(3.630)
    show monika 6eka_static
    $ renpy.pause(1.418)
    show monika 6dka
    $ renpy.pause(9.425)
    show monika 5dka with dissolve_monika
    $ renpy.pause(5)

    show monika 6eua at rs32 with dissolve_monika
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    pause 1.0
    call monika_zoom_transition(mas_temp_zoom_level,1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_or",
            category=['моника','музыка'],
            prompt="Ты можешь сыграть для меня «Наша реальность»?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        )
    )

label mas_monika_plays_or(skip_leadin=False):
    if not skip_leadin:
        m 3eua "Конечно, дай мне только взять пианино.{w=0.5}.{w=0.5}.{nw}"

    window hide
    call mas_timed_text_events_prep
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano at lps32,rps32 zorder MAS_MONIKA_Z+1
    pause 5.0
    show monika at ls32 zorder MAS_MONIKA_Z
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Не забывай прибавить звук в игре, [player]!"
        $ disable_esc()

    pause 2.0
    $ mas_play_song(songs.FP_PIANO_COVER,loop=False)

    show monika 1dsa
    pause 9.15
    m 1eua "{i}{cps=10}День за днём,{w=0.5} {/cps}{cps=15}я мечтаю о будущем,{w=0.22} {/cps}{cps=13}что разделю с тобой{w=4.10}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=12}В руке перо,{w=0.5} {/cps}{cps=17}что напишет стихотворение{w=0.5} {/cps}{cps=16}о нас с тобой{w=4.10}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}Чернила капают{w=0.25} {/cps}{cps=10}в темную лужу стихов{w=1}{/cps}{/i}{nw}"
    m 1eka "{i}{cps=18}Рука гуляет по бумаге,{w=0.45} {/cps}{cps=20}ища путь к сердцу твоему{w=1.40}{/cps}{/i}{nw}"
    m 1dua "{i}{cps=15}Но в этом мире{w=0.25} {/cps}{cps=11}бесчисленных тропок{w=0.90}{/cps}{/i}{nw}"
    m 1eua "{i}{cps=16}Что мне отдать,{w=0.25}{/cps}{cps=18} чтобы найти тот особый день?{/cps}{/i}{w=0.90}{nw}"
    m 1dsa "{i}{cps=15}Что мне отдать,{w=0.50} чтобы найти{w=1} тот особый день?{/cps}{/i}{w=1.82}{nw}"
    pause 7.50

    m 1eua "{i}{cps=15}Что бы мне интересного придумать,{w=0.5} {/cps}{cps=15}чтобы всех{w=0.30} {/cps}{cps=12}занять?{w=4.20}{/cps}{/i}{nw}"
    m 1hua "{i}{cps=18}Когда есть ты,{w=0.25} {/cps}{cps=13.25}нам весело, что бы мы не делали{w=4}{/cps}{/i}{nw}"
    m 1esa "{i}{cps=11}Если мне не понять свои чувства,{/cps}{w=1}{/i}{nw}"
    m 1eka "{i}{cps=17}Что толку в словах,{w=0.3} когда улыбка скажет всё?{/cps}{/i}{w=1}{nw}"
    m 1lua "{i}{cps=11}А если мир, этот не подарит мне счастье{/cps}{/i}{w=0.9}{nw}"
    m 1dka "{i}{cps=18}Что мне отдать,{w=0.5} чтобы всё заполучить?{/cps}{/i}{w=2}{nw}"
    show monika 1dsa
    pause 17.50

    m 1eka "{i}{cps=15}В этом мире,{w=0.5} {/cps}{cps=15}вдали от того, кто всегда {/cps}{cps=17}будет мне дорог{/cps}{w=4.5}{/i}{nw}"
    m 1ekbsa "{i}{cps=15}Ты, любовь моя,{w=0.5} {/cps}{cps=16.5}держи ключ к дню, когда я наконец буду свободна{/cps}{w=8.5}{/i}{nw}"
    m 1eua "{i}{cps=16}Чернила капают{w=0.25} {/cps}{cps=10}в темную лужу{/cps}{w=1.2}{/i}{nw}"
    m 1esa "{i}{cps=18}Как могу проникнуть{w=0.45} {/cps}{cps=13}в твою реальность?{/cps}{w=1.40}{/i}{nw}"
    m 1eka "{i}{cps=12}Где я смогу услышать звук твоего сердцебиения{/cps}{w=0.8}{/i}{nw}"
    m 1ekbsa "{i}{cps=16}И пусть это любовь,{w=0.6} но в нашей реальности{/cps}{/i}{w=0.6}{nw}"
    m 1hubsa "{i}{cps=16}И в нашей реальности,{w=1} я буду всегда любить тебя{/cps}{w=4.2}{/i}{nw}"
    m 1ekbsa "{i}{cps=19}С тобой я буду.{/cps}{/i}{w=2}{nw}"

    show monika 1dkbsa
    pause 9.0
    show monika 6eua at rs32
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    pause 1.0
    call monika_zoom_transition(mas_temp_zoom_level,1.0)
    call mas_timed_text_events_wrapup
    window auto

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return
