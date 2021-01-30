default persistent._mas_songs_database = dict()


default persistent._mas_player_derandomed_songs = list()

init -10 python in mas_songs:

    song_db = {}















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
        
        rand_delegate_ev = store.mas_getEV("monika_sing_song_random")
        
        if rand_delegate_ev:
            
            
            
            
            if (
                rand_delegate_ev.random
                and (
                    (not store.persistent._mas_enable_random_repeats and not hasRandomSongs(unseen_only=True))
                    or not hasRandomSongs()
                )
            ):
                rand_delegate_ev.random = False
            
            
            
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

    $ song_length = "short"

    $ have_both_types = False

    $ switch_str = "полную"

    $ end = ""

    show monika 1eua at t21

    if mas_songs.hasUnlockedSongs(length="long") and mas_songs.hasUnlockedSongs(length="short"):
        $ have_both_types = True

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
            which = "Хромую" # ну, старые ведьмы ведь хромые, да? ¯\_(ツ)_/¯
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
            $ pushEvent(sel_song, skipeval=True)
            show monika at t11
            m 3hub "Хорошо!"
    else:

        return "prompt"

    return


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
    $ renpy.say(m, "О [which] песне ты хотел[mas_gender_none] бы поговорить?", interact=False)

    call screen mas_gen_scrollable_menu(unlocked_analyses, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_analysis = _return

    if sel_analysis:
        $ pushEvent(sel_analysis, skipeval=True)
        show monika at t11
        m 3hub "Хорошо!"
    else:

        return "prompt"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_sing_song_rerandom",
            prompt="Ты можешь снова спеть песню в одиночку?",
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
    m 1eka "Устал[mas_gender_none] слушать, как я пою эту песню, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Устал[mas_gender_none] слушать, как я пою эту песню, [player]?{fast}"
        "Немного.":

            $ MAS.MonikaElastic()
            m 1eka "Всё в порядке."
            $ MAS.MonikaElastic()
            m 1eua "Я буду петь только тогда, когда ты захочешь. Просто дай мне знать, если захочешь это услышать."
            python:
                mas_hideEVL(prev_topic, "SNG", derandom=True)
                persistent._mas_player_derandomed_songs.append(prev_topic)
                mas_unlockEVL("mas_sing_song_rerandom", "EVE")
        "Всё нормально.":

            m 1eua "Хорошо, [player]."
    return

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




    if (
        (persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs())
        or (not persistent._mas_enable_random_repeats and mas_songs.hasRandomSongs(unseen_only=True))
    ):
        python:

            random_unseen_songs = mas_songs.getRandomSongs(unseen_only=True)


            if random_unseen_songs:
                rand_song = random.choice(random_unseen_songs)


            else:
                rand_song = random.choice(mas_songs.getRandomSongs())


            mas_unlockEVL("monika_sing_song_pool", "EVE")


            pushEvent(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")


            mas_unlockEVL(rand_song + "_long", "SNG")


            mas_unlockEVL(rand_song + "_analysis", "SNG")


            if store.mas_songs.hasUnlockedSongAnalyses():
                mas_unlockEVL("monika_sing_song_analysis", "EVE")
    else:


        $ mas_assignModifyEVLPropValue("monika_sing_song_random", "shown_count", "-=", 1)
        return "derandom|no_unlock"
    return "no_unlock"



init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aiwfc",
            prompt="«Всё, что мне нужно на Рождество - это ты»",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_aiwfc:

    if store.songs.hasMusicMuted():
        m 3eua "Не забудь увеличить громкость в игре, [mas_get_player_nickname()]."

    call monika_aiwfc_song from _call_monika_aiwfc_song


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
    m 1hub "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относил[mas_gender_sya]~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относил[mas_gender_sya]~{/i}"
    $ MAS.MonikaElastic()
    m 3eua "{i}~И теперь я словно, {w=0.2}словно в раю~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Мне безумно хорошо~{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}~По радио звучит хорошая музыка~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Мне очень, очень хорошо~{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}~По радио звучит хорошая музыка~{/i}"
    $ MAS.MonikaElastic()
    m 2hkbsu "{i}~И мне хочется поцеловать тебя, малыш~{/i}"
    $ MAS.MonikaElastic()
    m 2hkbsb "{i}~Пока мы стоим здесь, под омелой~{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}~Cанта зашёл к нам через дымоход, {w=0.2}около половины четвёртого ночи~{/i}"
    $ MAS.MonikaElastic()
    if persistent.gender == "F":
        m 3hub "{i}~И оставил эти замечательные подарки, для меня и моей малышки~{/i}"
    else:
        m 3hub "{i}~И оставил эти замечательные подарки, для меня и моего малыша~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Счастливого Рождества, малыш, {w=0.2}ты действительно хорошо ко мне относил[mas_gender_sya]~{/i}"
    $ MAS.MonikaElastic()
    m 1eua "{i}~И теперь я словно, {w=0.2}словно в раю~{/i}"
    $ MAS.MonikaElastic()
    m 1eub "{i}~Счастливого Рождества, малыш~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~И с Новым годом тоже~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsa "{i}~Счастливого Рождества, дорогуша~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsu "{i}~Здесь всё до безумия красиво~{/i}"
    $ MAS.MonikaElastic()
    if persistent.gender == "F":
        m 3ekbfb "{i}~Я люблю тебя, малышка~{/i}"
    else:
        m 3ekbfb "{i}~Я люблю тебя, малыш~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~За всё то, что дал[mas_gender_none] мне~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbfb "{i}~Я люблю тебя, дорогуша~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsu "{i}~С Рождеством, мо[mas_gender_i] дорог[mas_gender_oi]~{/i}"
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
    $ MAS.MonikaElastic()
    m 1hub "{i}~Танцуя с тобой, {w=0.2}делая ночи запоминающимися~{/i}"
    $ MAS.MonikaElastic()
    m 1rub "{i}~Падающий снег,{w=0.2}{nw}{/i}"
    extend 3rub "{i} я просто обожаю эту погоду~{/i}"
    $ MAS.MonikaElastic()
    m 3tub "{i}~Одеяло на двоих,{w=0.2} чтобы чувствовать себя более тёплым вместе~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Две горлицы,{w=0.2} как они нас называют~{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}~Мы влюбляемся друг в друга~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Это моё любимое Рождеств-в-в-во~{/i}"
    $ MAS.MonikaElastic()
    m 3duu "{i}~Этим Рождеством,{w=0.2} я просто не могу устоять {w=0.2}перед чем-то подобным~{/i}"
    $ MAS.MonikaElastic()
    m 1sub "{i}~Я не могу устоять перед этим рождественским поцелуем~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Потому что я падаю,{w=0.2} погребённая в твоих губах~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Что-то вроде этого,{w=0.2}{nw}{/i}"
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
    $ MAS.MonikaElastic()
    m 1dso "~Я могу приглушить свет и спеть тебе песни, полные печали~"
    $ MAS.MonikaElastic()
    m 4hub "~Мы можем танцевать танго только вдвоём~"
    $ MAS.MonikaElastic()
    m "~Я могу петь серенаду и нежно играть на струнах твоего сердца, что боги мне послали~"
    $ MAS.MonikaElastic()
    m 4dso "~Будь Валентино только для себя в сердце своём~"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха~"
    $ MAS.MonikaElastic()
    m 1ekbsa "Ты будешь моим добрым старым любовником, [player]?"
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
    $ MAS.MonikaElastic()
    m 1dso "~Пожалуйста, помни, что я чувствую к тебе~"
    $ MAS.MonikaElastic()
    m "~Я бы никогда не смогла жить без тебя ни при какой судьбе~"
    $ MAS.MonikaElastic()
    m 3hub "~Так что вернись и посмотри~"
    $ MAS.MonikaElastic()
    m 4l "~Что для меня значишь ты?~"
    $ MAS.MonikaElastic()
    m 1hubsb "~Я нуждаюсь в тебе~"
    $ MAS.MonikaElastic()
    m 3esa "Я знаю, что эта песня о том, чтобы оставить кого-то, но я думаю, что она несёт в себе хорошее послание."
    $ MAS.MonikaElastic()
    m 1ekbsa "И я действительно нуждаюсь в тебе, [player]~"
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
    $ MAS.MonikaElastic()
    m 1dso "~Кто знает, как долго я тебя любила?~"
    $ MAS.MonikaElastic()
    m "~Ты знаешь, я всё ещё люблю тебя, и никогда о тебе не позабуду~"
    $ MAS.MonikaElastic()
    m "~Буду ли я ждать одинокой жизни, что судьба бы мне объявила?~"
    $ MAS.MonikaElastic()
    m 2hub "~Если ты захочешь, чтобы я ждала – я буду~"
    $ MAS.MonikaElastic()
    m 1ekbsa "Однажды мы будем вместе, [player]."
    $ MAS.MonikaElastic()
    m 1hubfa "Я просто надеюсь, что ты всё ещё будешь любить меня, когда придёт этот особенный день~"
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
    if persistent.gender == "F":
        $ youre_my = "моя"
    else:
        $ youre_my = "мой"
    $ MAS.MonikaElastic()
    m 1dso "~Ты [youre_my], иди сюда~"
    $ MAS.MonikaElastic()
    m 1hub "~И мы принадлежим друг другу~"
    $ MAS.MonikaElastic()
    m 3hub "~Да, мы принадлежим друг другу~"
    $ MAS.MonikaElastic()
    m 3dso "~Навечно и навсегда~"
    $ MAS.MonikaElastic()
    m 1eua "Ты когда нибудь слышал[mas_gender_none] о Ду-вопе, [player]?"
    $ MAS.MonikaElastic()
    m 4eua "Это вокальный поджанр ритм-н-блюза, который стал очень популярным в 1950-х."
    $ MAS.MonikaElastic()
    m 4eub "Много поп-музыки тогда следовало этому стилю, что и сделало многие любовные песни великолепными."
    $ MAS.MonikaElastic()
    m 3eub "И если ты внимательно прислушаешься, то заметишь, что моя песня фактически следует типичной последовательности аккордов Ду-вопа."
    $ MAS.MonikaElastic()
    m 1hua "Думаю, можно сказать, что я училась у лучших."
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
    $ MAS.MonikaElastic()
    m 1dso "~Мой подарок – это песня моя~"
    $ MAS.MonikaElastic()
    m "~И она – специально для тебя~"
    $ MAS.MonikaElastic()
    m 1hub "~И ты можешь сказать всем, что эта твоя песня всегда~"
    $ MAS.MonikaElastic()
    m "~Это может быть довольно просто, но теперь, это сделано тогда~"
    $ MAS.MonikaElastic()
    m 2hubsb "~Надеюсь, ты не против~"
    $ MAS.MonikaElastic()
    m 2hubfb "~Надеюсь, ты не против~"
    $ MAS.MonikaElastic()
    m 2hub "~Что я записала словами~"
    $ MAS.MonikaElastic()
    m 1dso "~Как прекрасна жизнь, пока ты в этом мире, и счастье не за горами~"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха~"
    $ MAS.MonikaElastic()
    m 3eka "Нечасто я нахожу песни, которые относятся ко мне так же, как эта."
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dso "~Если кто-то попытается место моё занять~"
    $ MAS.MonikaElastic()
    m 1hub "~Давай притворимся, что не видим их лица, им тебя не отнять~"
    $ MAS.MonikaElastic()
    m 3hub "~В этом мире нет ничего, что я бы предпочла сделать порой~"
    $ MAS.MonikaElastic()
    m 3dso "~Потому что я счастлива просто потанцевать с тобой~"
    $ MAS.MonikaElastic()
    m 1ekbsa "Нет ничего, что сделало бы меня счастливее, чем открытие того, что я люблю тебя."
    $ MAS.MonikaElastic(voice="monika_giggle")
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
    $ MAS.MonikaElastic()
    m 1dso "~Когда мне грустно ночью~"
    $ MAS.MonikaElastic()
    m "~И мне нужно, чтобы ты меня крепко обнял[mas_gender_none] очень~"
    $ MAS.MonikaElastic()
    m 2hub "~Всякий раз, когда я хочу тебя, всё, что мне нужно – это мечтать~"
    $ MAS.MonikaElastic()
    m 1eka "Теперь, когда ты здесь, [player], мне больше не нужно мечтать."
    $ MAS.MonikaElastic()
    m 1ekbsa "Моя мечта наконец сбылась."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_im_glad_youre_evil_too",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Я рада, что ты тоже зл[mas_gender_oi]»",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_im_glad_youre_evil_too:
    $ MAS.MonikaElastic()
    m 1dsa "{i}~Мы восхищаемся красивым закатом, или радуемся милому щеночку вместе~{/i}"
    $ MAS.MonikaElastic()
    m 1dsd "{i}~Нас об[mas_gender_oih] обижают громкие заголовки жестоких новостей~{/i}"
    $ MAS.MonikaElastic()
    m 3hksdlb "{i}~Мы над ужасным фильмом смеёмся, и во время просмотра разных телешоу рыдаем~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Это мы – две одинокие души, с досугом свои часы коротающие~{/i}"
    $ MAS.MonikaElastic()
    m 3dsa "{i}~Наше время не бесконечно, хоть и кажется нескончаемой шуткой оно~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}~Но зато ты мне компанию составляешь, чтоб короткая жизнь скучной не казалась~{/i}"
    $ MAS.MonikaElastic()
    m 1tubsb "{i}~И вместе мы над скучным миром смеёмся, поговаривая: «Какая скукотища»~{/i}"
    $ MAS.MonikaElastic()
    m 1dubfb "{i}~Это мы – две одинокие души, к плечам друг друга прислонившиеся~{/i}"
    $ MAS.MonikaElastic()
    m 1dsbfo "{i}~Я рада, что ты так[mas_gender_oi] же зл[mas_gender_oi], как и я~{/i}"
    $ MAS.MonikaElastic()
    m 1hubfa "{i}~И ещё раз скажу, что очередной день пережить я хочу. И я рада, что умудрилась в тебя я влюбиться~{/i}"

    if persistent._mas_pm_monika_evil:
        if persistent._mas_pm_monika_evil_but_ok:
            $ MAS.MonikaElastic()
            m 1ekbfa "Думаю, быть злой не так уж и плохо, пока я рядом с тобой."
            $ MAS.MonikaElastic()
            m 3ekbfa "Мы ведь две души, с досугом свои часы коротающие~"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubfb "А-ха-ха!"
        else:

            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1ekbfa "Э-хе-хе, ты всё ещё считаешь меня злой, [player]?"
            $ MAS.MonikaElastic()
            m 3tubfb "Быть может, я смогу однажды переубедить тебя~"
    else:
        $ MAS.MonikaElastic()
        m 1ekbfa "Я правда сомневаюсь, что кто-то из нас зл[mas_gender_oi], [player]."
        $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dsd "{i}~Ради чего мы все живём? Ради чего мы все пахаем в поте лица?~{/i}"
    $ MAS.MonikaElastic()
    m 3dsd "{i}~Ведь там, возможно, ничего, ничего, ничего такого нет. Это всё может бесполезным вмиг оказаться~{/i}"
    $ MAS.MonikaElastic()
    m 1dsd "{i}~И через тысячу лет уже ничего не останется, {/i}{nw}"
    $ MAS.MonikaElastic()
    extend 1hub "{i}но всё равно надеюсь, что улыбаться вместе с тобой не перестану я~{/i}"
    $ MAS.MonikaElastic()
    m 3rksdld "{i}~Даже когда мечты наши в реальность воплотились; даже когда мы просвещёнными стали, мы всё равно одинокими можем стать~{/i}"
    $ MAS.MonikaElastic()
    m 3eksdld "{i}~Даже когда мы призраками стали; даже когда мы обратились в ничто, {/i}{nw}"
    $ MAS.MonikaElastic()
    extend 3hksdlb "{i}всё равно надеюсь, что улыбаться вместе с тобой не перестану я~{/i}"
    $ MAS.MonikaElastic()
    m 1dku "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 3ekbsa "Что бы ни произошло и сколько бы мы ни ждали, я всегда буду любить тебя."
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dsd "{i}~Встреча в полночь~{/i}"
    $ MAS.MonikaElastic()
    m 1rksdld "{i}~В мире, где сплошь и рядом бомбы~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsa "{i}~Я размышляла о тебе, всё это время~{/i}"
    $ MAS.MonikaElastic()
    m 1eka "{i}~Могло ль недоразуменье возникнуть в расстоянии между нами?~{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}~Это шоу интерес необыкновенный представляет, верно?~{/i}"
    $ MAS.MonikaElastic()
    m 1hua "{i}~Читал[mas_gender_none] ли ты мангу, о которой множество речей идёт?~{/i}"
    $ MAS.MonikaElastic()
    m 1sub "{i}~Слышал[mas_gender_none] ль ты песнь эту?~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~А мы всё дурачимся, сидя за заслоном, меж двух экранов стоявшим~{/i}"
    $ MAS.MonikaElastic()
    m 1hubsa "Э-хе-хе, надеюсь, тебе понравилась эта песня, [player]~"
    $ MAS.MonikaElastic()
    m 1ekbsa "Я просто подумала, что она прекрасно описывает наше положение дел."
    $ MAS.MonikaElastic()
    m 3rkbsa "Песни вокалоидов определённо имеют склонность к этому, если задуматься над их смыслом."
    $ MAS.MonikaElastic(voice="monika_giggle")
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
    $ MAS.MonikaElastic()
    m 1dsd "{i}~Когда ночь придёт~{/i}"
    $ MAS.MonikaElastic()
    m 3dsd "{i}~И станет вдруг темно~{/i}"
    $ MAS.MonikaElastic()
    m 3eud "{i}~И только свет луны увидим мы~{/i}"
    $ MAS.MonikaElastic()
    m 2euo "{i}~Нет, бояться я не буду~{/i}"
    $ MAS.MonikaElastic()
    m 2duo "{i}~Нет, бояться я не буду~{/i}"
    $ MAS.MonikaElastic()
    m 2hub "{i}~Пока ты рядом, рядом со мной~{/i}"
    if not from_long:
        $ MAS.MonikaElastic()
        m 2eka "Все мои страхи и опасения попросту исчезают, когда ты со мной, [player]..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "И пока ты ещё рядом со мной, для меня не существует никаких преград."
        $ MAS.MonikaElastic()
        m 5ekbsa "...Надеюсь, ты чувствуешь то же самое~"
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
    $ MAS.MonikaElastic()
    m 1ekb "{i}~Счастливо жду, сам по себе~{/i}"
    $ MAS.MonikaElastic()
    m 1dkb "{i}~Под бескрайним небом~{/i}"
    $ MAS.MonikaElastic()
    m 2dkd "{i}~Считая секунды, стоя в одиночестве~{/i}"
    $ MAS.MonikaElastic()
    m 2tkd "{i}~Как проходят тысячи лет~{/i}"
    $ MAS.MonikaElastic()
    m 2hkb "{i}~Счастливо размышляя, ночь за ночью~{/i}"
    $ MAS.MonikaElastic()
    m 3ekb "{i}~Вот как это работает? Правильно ли я это делаю?~{/i}"
    $ MAS.MonikaElastic()
    m 1ekb "{i}~С удовольствием слушаю~{/i}"
    $ MAS.MonikaElastic()
    m 3eka "{i}~Счастлив оставаться~{/i}"
    $ MAS.MonikaElastic()
    m 3dkd "{i}~Счастливо наблюдая, как она уплывает прочь~{/i}"
    $ MAS.MonikaElastic()
    m 1dku "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 3eka "Наша история закончилась гораздо счастливее, чем эта песня."
    $ MAS.MonikaElastic()
    m 3hua "Ты навещаешь меня так часто, как только можешь, и я так благодарна тебе за это."
    $ MAS.MonikaElastic()
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
    call mas_song_stand_by_me (from_long=True) from _call_mas_song_stand_by_me

    $ MAS.MonikaElastic()
    m 4hub "{i}~О, друг мой, друг мой, будь со мной~{/i}" # может сбиться ритм при переложении "друг мой" под женский род
    $ MAS.MonikaElastic()
    m 4duo "{i}~О, будь со мной, останься, будь со мной~{/i}"
    $ MAS.MonikaElastic()
    m 2esd "{i}~Если небо, если звёзды~{/i}"
    $ MAS.MonikaElastic()
    m 2dkd "{i}~Все упадут на нас~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Или горы вдруг осыпятся в моря~{/i}"
    $ MAS.MonikaElastic()
    m 2eko "{i}~Я не заплачу, я не заплачу, слезинки не пролью~{/i}"
    $ MAS.MonikaElastic()
    m 2euo "{i}~Пока ты рядом, рядом со мной~{/i}"
    $ MAS.MonikaElastic()
    m 4hub "{i}~О, друг мой, друг мой, будь со мной, о, будь со мной, останься~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Ну, ну, будь со мной, останься, будь со мной~{/i}"
    $ MAS.MonikaElastic()
    m 4duo "{i}~О, друг мой, друг мой, будь со мной~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~О, будь со мной, останься~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~Если ты в беде, будь рядом~{/i}"
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dsd "{i}~А что если мы перепишем звёзды~{/i}"
    $ MAS.MonikaElastic()
    m 3dubsb "{i}~Скажи, что ты создан[mas_gender_none] быть мо[mas_gender_iiim]~{/i}"
    $ MAS.MonikaElastic()
    m 3dubso "{i}~Ничто не могло разлучить нас~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbfu "{i}~Ты был[mas_gender_none] бы тем, кого я должна была найти~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbsb "{i}~Всё зависит от тебя~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsb "{i}~И это зависит также от меня~{/i}"
    $ MAS.MonikaElastic()
    m 1duu "{i}~Никто не может сказать, кем мы станем~{/i}"
    $ MAS.MonikaElastic()
    m 3ekb "{i}~Так почему бы нам не переписать звёзды~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsa "{i}~Может быть, весь мир станет нашим~{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}~Сегодня вечером~{/i}"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Мир действительно кажется нашим, когда я с тобой, [player]~"
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 6eud "{i}~Там есть герой~{/i}"
    $ MAS.MonikaElastic()
    m 6eub "{i}~Если заглянешь себе в сердце~{/i}"
    $ MAS.MonikaElastic()
    m 6ekd "{i}~Только не надо бояться~{/i}"
    $ MAS.MonikaElastic()
    m 6eud "{i}~Быть тем, кто ты есть~{/i}"
    $ MAS.MonikaElastic()
    m 6esa "{i}~Там есть ответ~{/i}"
    $ MAS.MonikaElastic()
    m 6eud "{i}~Если заглянешь к себе в душу~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~И печаль, что тебя гложет~{/i}"
    $ MAS.MonikaElastic()
    m 4dud "{i}~Растает~{/i}"

    $ MAS.MonikaElastic()
    m 4eub "{i}~И вот герой приходит~{/i}"
    $ MAS.MonikaElastic()
    m 4dub "{i}~В силах справиться со всем~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~И ты отбрасываешь свои страхи~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    $ MAS.MonikaElastic()
    m 4dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~Загляни внутрь себя и держись~{/i}"
    $ MAS.MonikaElastic()
    m 4esd "{i}~И наконец тебе откроется истина~{/i}"
    $ MAS.MonikaElastic()
    m 4eua "{i}~И она в том, что герой – ты сам~{/i}"

    if not from_long:
        $ MAS.MonikaElastic()
        m 2dka "..."
        $ MAS.MonikaElastic()
        m 2eka "[player]..."
        $ MAS.MonikaElastic()
        m 7eka "Я очень надеюсь, что ты обратил[mas_gender_none] внимание на эти тексты."

        if persistent._mas_pm_love_yourself is False:
            $ MAS.MonikaElastic()
            m 3ekd "Ты уже говорил[mas_gender_none] мне, что тебе не по себе..."
            $ MAS.MonikaElastic()
            m 3eka "Но я просто хотела, чтобы ты знал[mas_gender_none], что глубоко внутри у тебя есть сила преодолеть то, что делает тебя несчастн[mas_gender_iim]."
            $ MAS.MonikaElastic()
            m 1ekd "Даже если ты не видишь этого в себе, оно есть...{w=0.3} Я видела это."
            $ MAS.MonikaElastic()
            m 3eua "...И я буду здесь всю дорогу, чтобы помочь тебе обрести эту силу."
            $ MAS.MonikaElastic()
            m 3eka "Как бы сильно я ни хотела, чтобы ты любил[mas_gender_none] меня, я хочу, чтобы ты любил[mas_gender_none] себя ещё больше~"
        else:

            $ MAS.MonikaElastic()
            m 3ekd "Иногда жизнь может быть очень-очень трудной..."
            $ MAS.MonikaElastic()
            m 2dkc "Может показаться, что нет никакого способа преодолеть любые препятствия, с которыми ты сталкиваешься."
            $ MAS.MonikaElastic()
            m 7eud "...Я думаю, что знаю это так же хорошо, как и все остальные."
            $ MAS.MonikaElastic()
            m 3eka "Но поверь мне, что бы это ни было, ты сможешь."
            $ MAS.MonikaElastic()
            m 3eud "Ты можешь не всегда осознавать это, но в человеческом духе есть огромная сила."
            $ MAS.MonikaElastic()
            m 1eud "Мы можем делать вещи, которые даже не можем себе представить...{w=0.3} самое трудное – это просто верить в это."
            $ MAS.MonikaElastic()
            m 3eua "Поэтому, пожалуйста, не забывай всегда верить в себя, и если ты когда-нибудь обнаружишь, что сомневаешься в себе, просто приходи ко мне..."
            $ MAS.MonikaElastic()
            m 3hua "Я буду более чем счастлива помочь тебе обрести эту внутреннюю силу, [player]."
            $ MAS.MonikaElastic()
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
    call mas_song_hero (from_long=True) from _call_mas_song_hero

    $ MAS.MonikaElastic()
    m 4duo "{i}~Это трудно~{/i}"
    $ MAS.MonikaElastic()
    m 6dud "{i}~Когда ты наедине со всем миром~{/i}"
    $ MAS.MonikaElastic()
    m 4dsd "{i}~No one reaches out a hand~{/i}"
    $ MAS.MonikaElastic()
    m 4dud "{i}~Никто не протянет руку~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~Ты сможешь найти любовь~{/i}"
    $ MAS.MonikaElastic()
    m 4ekb "{i}~Если поищешь внутри себя~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~И пустота, что тебя окружает~{/i}"
    $ MAS.MonikaElastic()
    m 6eko "{i}~Исчезнет~{/i}"

    $ MAS.MonikaElastic()
    m 4eka "{i}~И вот герой приходит~{/i}"
    $ MAS.MonikaElastic()
    m 4esd "{i}~В силах справиться со всем~{/i}"
    $ MAS.MonikaElastic()
    m 4eud "{i}~И ты отбрасываешь свои страхи~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    $ MAS.MonikaElastic()
    m 6dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    $ MAS.MonikaElastic()
    m 6dud "{i}~Загляни внутрь себя и держись~{/i}"
    $ MAS.MonikaElastic()
    m 6eud "{i}~И наконец тебе откроется истина~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~И она в том, что герой – ты сам~{/i}"

    $ MAS.MonikaElastic()
    m 4euo "{i}~Видит бог~{/i}"
    $ MAS.MonikaElastic()
    m 4eud "{i}~Что тяжело следовать мечте~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~Но не позволяй никому~{/i}"
    $ MAS.MonikaElastic()
    m 4duo "{i}~Её уничтожить~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~Держись~{/i}"
    $ MAS.MonikaElastic()
    m 4eud "{i}~Наступит новый день~{/i}"
    $ MAS.MonikaElastic()
    m 4duo "{i}~И когда-нибудь, ты найдёшь к ней дорогу~{/i}"

    $ MAS.MonikaElastic()
    m 4eub "{i}~И вот герой приходит~{/i}"
    $ MAS.MonikaElastic()
    m 4duo "{i}~В силах справиться со всем~{/i}"
    $ MAS.MonikaElastic()
    m 4dud "{i}~И ты отбрасываешь свои страхи~{/i}"
    $ MAS.MonikaElastic()
    m 4euo "{i}~И ты знаешь, что сможешь всё пережить~{/i}"
    $ MAS.MonikaElastic()
    m 6dkd "{i}~Так что, когда у тебя уже нет надежды~{/i}"
    $ MAS.MonikaElastic()
    m 6dud "{i}~Загляни внутрь себя и держись~{/i}"
    $ MAS.MonikaElastic()
    m 4eud "{i}~И наконец тебе откроется истина~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~И она в том, что герой – ты сам~{/i}"
    $ MAS.MonikaElastic()
    m 6dku "{i}~И она в том, что герой – ты сам~{/i}"
    $ MAS.MonikaElastic()
    m 4eua "{i}~Герой – ты сам~{/i}"
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
    $ MAS.MonikaElastic()
    m 1esd "{i}~В этом уединенном месте, купались в тишине и мысли о тебе~{/i}"
    $ MAS.MonikaElastic()
    m 1dka "{i}~Я не вижу твоего лица, но я пытаюсь представить тебя~{/i}"
    $ MAS.MonikaElastic()
    m 1dkd "{i}~Так ты действительно там?~{/i}"
    $ MAS.MonikaElastic()
    m 3ekd "{i}~Ты не спишь с воспоминаниями?~{/i}"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "{i}~Девушку ты еще не встретил[mas_gender_none], кто пожелает на Плеядах?~{/i}"
    $ MAS.MonikaElastic()
    m 5ekbsa "Я думаю о тебе каждую ночь, [player]."
    $ MAS.MonikaElastic()
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
    call mas_song_my_silver_lining_lyrics from _call_mas_song_my_silver_lining_lyrics
    $ MAS.MonikaElastic()
    m 1hksdla "Э-хе-хе, эта песня очень напоминает мне мою жизнь...{w=0.2} до того, как я узнала, что всё это было игрой."
    $ MAS.MonikaElastic()
    m 3lksdlc "В то время я всегда так старалась удержаться на вершине... {w=0.2}У меня никогда не было времени сидеть сложа руки и думать обо всем."
    $ MAS.MonikaElastic()
    m 3eud "Не всегда было легко быть идеальной ученицей, понимаешь? {w=0.2}Или, по крайней мере, человек, которого все {i}считали{/i} идеальным."
    $ MAS.MonikaElastic()
    m 1ekbsu "Но потом появил[mas_gender_sya] ты и перевернул[mas_gender_none] весь мой мир вверх дном..."
    $ MAS.MonikaElastic()
    m 3dubsu "Я хочу ещё раз поблагодарить тебя за то, что ты помог[mas_gender_g] мне увидеть правду, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Сначала это было нелегко, учитывая всё, чем мне пришлось пожертвовать, но я знала, что в конце концов всё получится."
    $ MAS.MonikaElastic()
    m 1hua "Когда ты проводишь своё время со мной, я не могу не чувствовать, что все мои надежды и мечты сбылись."


    if mas_getEV('mas_song_my_silver_lining').shown_count == 0:
        $ MAS.MonikaElastic()
        m 1rtc "На самом деле я хотела бы сказать об этой песне гораздо больше..."
        $ MAS.MonikaElastic()
        m 7eua "У тебя есть время послушать об этом сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя есть время послушать об этом сейчас?{fast}"
            "Конечно.":

                $ MAS.MonikaElastic()
                m 1hub "Хорошо!"
                call mas_song_my_silver_lining_analysis (from_song=True) from _call_mas_song_my_silver_lining_analysis
                $ mas_getEV("mas_song_my_silver_lining_analysis").shown_count += 1
            "Не сейчас.":

                $ MAS.MonikaElastic()
                m 1eka "Ладно, [player]..."
                $ MAS.MonikaElastic()
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
        call mas_song_my_silver_lining_lyrics from _call_mas_song_my_silver_lining_lyrics_1

    $ MAS.MonikaElastic()
    m 3dud "{i}~Надо продолжать идти, глядя прямо на дорогу~{/i}"
    $ MAS.MonikaElastic()
    m 3eud "{i}~Не беспокойся о том, что позади тебя или что ждёт тебя дальше по дороге~{/i}"
    $ MAS.MonikaElastic()
    m 1ekd "{i}~Я стараюсь не цепляться за то, что ушло, я стараюсь делать правильно то, что неправильно~{/i}"
    $ MAS.MonikaElastic()
    m 1eka "{i}~Я стараюсь продолжать и продолжать~{/i}"
    $ MAS.MonikaElastic()
    m 1dsu "{i}~Да я просто продолжаю продолжать~{/i}"
    $ MAS.MonikaElastic()
    m 1esc "Так или иначе...{w=0.2} как ты можешь себе представить, не всегда легко застрять здесь, [player]."
    $ MAS.MonikaElastic()
    m 3rksdlc "Тут я не много могу сделать, не могу никуда пойти, и мне становится одиноко, когда тебя нет рядом."
    $ MAS.MonikaElastic()
    m 1dkc "Я стараюсь не поддаваться этому, но когда это происходит, мне нравится вспоминать эту песню..."
    $ MAS.MonikaElastic()
    m 3eub "Это безумие, как немного музыки может помочь изменить ситуацию, когда ты чувствуешь себя подавленным!"
    $ MAS.MonikaElastic()
    m 3eua "Как будто эта песня разрушает то, что было не так в моей жизни, а затем говорит мне, что всё в порядке, чтобы отпустить мои проблемы."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "«Не беспокойся о том, что у тебя за спиной или что ждёт тебя дальше по дороге», как говорится. Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1etc "Но, правда, [player]...{w=0.3} я думаю, что есть некоторые реальные заслуги в этом направлении мышления."
    $ MAS.MonikaElastic()
    m 1eka "Какова бы ни была твоя ситуация, факт остаётся фактом: всё так, как есть, и нет причин не улыбаться."
    $ MAS.MonikaElastic()
    m 3eka "Так вот, я вовсе не говорю тебе, чтобы ты не волновал[mas_gender_sya]..."
    $ MAS.MonikaElastic()
    m 3eksdlc "Если бы я это сделала, то позволила бы игре идти своим чередом, и теперь я навсегда застряла бы сама по себе."
    $ MAS.MonikaElastic()
    m 1duu "...Но в то же время нет никакого смысла чрезмерно волноваться о вещах, которые ты не можешь изменить..."
    $ MAS.MonikaElastic()
    m 1etc "Я полагаю, всё дело в том, чтобы найти правильный баланс."
    $ MAS.MonikaElastic()
    m 3rksdla "Когда ты думаешь об этом, идеи здесь странно близки к экзистенциальному нигилизму, верно?"
    $ MAS.MonikaElastic()
    m 3eud "Понимаешь, эта идея, что наша жизнь действительно абсурдна, и единственное, что мы можем сделать, это...{w=0.3} {nw}"
    extend 3eksdla "продолжать и продолжать."
    $ MAS.MonikaElastic()
    m 3etc "...Хотя если бы ты продолжал[mas_gender_none] идти, как в следующем стихе..."
    $ MAS.MonikaElastic()
    m 3dud "{i}~Я проснулась в гостиничном номере~{/i}"
    $ MAS.MonikaElastic()
    m 1ekd "{i}~Мои тревоги огромны, как луна~{/i}"
    $ MAS.MonikaElastic()
    m 1dsd "{i}~Не имея ни малейшего понятия кто или что или где я~{/i}"
    $ MAS.MonikaElastic()
    m 2eka "{i}~Что-то хорошее приходит вместе с плохим~{/i}"
    $ MAS.MonikaElastic()
    m 2dku "{i}~Песня никогда не бывает просто грустной~{/i}"
    $ MAS.MonikaElastic()
    m 7eka "{i}~Есть надежда, есть лучик надежды~{/i}"
    $ MAS.MonikaElastic()
    m 3duu "{i}~Покажи мне мой лучик надежды~{/i}"
    $ MAS.MonikaElastic()
    m 3eua "...Тогда я бы сказала, что смысл песни не столько в нигилизме, сколько в надежде."
    $ MAS.MonikaElastic()
    m 3huu "И, может быть, это самое главное."
    $ MAS.MonikaElastic()
    m 3ekblu "Независимо от того, важна наша жизнь или нет, я хочу верить, что есть светлая сторона, [player]..."
    $ MAS.MonikaElastic()
    m 2eud "Но, чтобы ты знал[mas_gender_none], я не верю, что наша жизнь действительно бессмысленна..."
    $ MAS.MonikaElastic()
    m 2duu "Какова бы ни была правда, возможно, мы могли бы попытаться выяснить это вместе."
    $ MAS.MonikaElastic()
    m 2eka "Но пока мы этого не сделаем, мы просто будем продолжать улыбаться и не беспокоиться о том, что может произойти дальше~"
    return

label mas_song_my_silver_lining_lyrics:
    m 1dsd "{i}~Я больше не хочу ждать, я устала искать ответы~{/i}"
    $ MAS.MonikaElastic()
    m 1eub "{i}~Отведи меня куда-нибудь, где есть музыка и смех~{/i}"
    $ MAS.MonikaElastic()
    m 2lksdld "{i}~Я не знаю, боюсь ли я умереть, но я боюсь жить слишком быстро, слишком медленно~{/i}"
    $ MAS.MonikaElastic()
    m 2dsc "{i}~Сожаление, раскаяние, надежда, о нет, я должна идти~{/i}"
    $ MAS.MonikaElastic()
    m 7eud "{i}~Нет начала, нет новых начинаний, время мчится вперёд~{/i}"
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dso "{i}~Время идёт, дни и ночи превращаются в года~{/i}"
    $ MAS.MonikaElastic()
    m 1dkbsa "{i}~А я лежу в твоих объятиях~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsb "{i}~Только так~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsb "{i}~Я знаю, что нахожусь ближе всего к твоему сердцу~{/i}"
    $ MAS.MonikaElastic()
    m 1hua "{i}~Что тьма рассеялась~{/i}"
    $ MAS.MonikaElastic()
    m 1ekb "{i}~Я знаю, что в душе ты чувствуешь то же, что и я~{/i}"
    $ MAS.MonikaElastic()
    m 3eka "{i}~Словно во сне, в котором мы можем летать~{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}~Cловно знак, словно сон, ты – мой амарант~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbla "{i}~Кроме тебя, мне ничего не надо, поверь~{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}~Словно течение реки~{/i}"
    $ MAS.MonikaElastic()
    m 3hua "{i}~Твоя красота безмятежна~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Больше мне в жизни ничего не надо~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}~Моя мечта, амарант~{/i}"
    show monika 5ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsu "И я знаю, что ты тоже обо мне думаешь, [player]."
    $ MAS.MonikaElastic()
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
    call mas_song_shelter_lyrics from _call_mas_song_shelter_lyrics
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2rsbsa "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 2ekbfa "Ты – причина, по которой я могу продолжать двигаться вперёд, [player]."
    $ MAS.MonikaElastic()
    m 2ekbsu "И если однажды ты почувствуешь, что ты совсем один в этом мире...{w=0.3}{nw}"
    extend 2dkbsa " я хочу, чтобы ты помнил[mas_gender_none], что это не так."
    $ MAS.MonikaElastic()
    m 7hubfb "...Ты меня поймал[mas_gender_none] за это!"
    $ MAS.MonikaElastic()
    m 3eka "И кроме того, есть куча людей, которые не хотят ничего больше, чем знать, что мы счастливы...{w=0.3} даже если они не знают наших имён или лиц."
    $ MAS.MonikaElastic()
    m 1hub "Там всегда будет кто-то болеть за нас!"


    if not mas_getEVL_shown_count("mas_song_shelter"):
        $ MAS.MonikaElastic()
        m 3rksdla "На самом деле я хотела бы рассказать об этой песне больше, но только если у тебя есть время, разумеется..."

        $ MAS.MonikaElastic()
        m 1eka "Может быть, ты хочешь услышать больше о ней прямо сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "Может быть, ты хочешь услышать больше о ней прямо сейчас?{fast}"
            "Конечно!":

                $ MAS.MonikaElastic()
                m 3hub "Ладно, отлично!"
                call mas_song_shelter_analysis (from_song=True) from _call_mas_song_shelter_analysis
                $ mas_assignModifyEVLPropValue("mas_song_shelter_analysis", "shown_count", "+=", 1)
            "Но не сейчас.":

                $ MAS.MonikaElastic()
                m 1eka "Хорошо, [player]..."
                $ MAS.MonikaElastic()
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
        m 3eksdla "В общем, эта песня называется {i}«Убежище»{/i}, и, как ты уже, наверное, понял[mas_gender_none], мне она очень нравится."
    else:

        call mas_song_shelter_lyrics from _call_mas_song_shelter_lyrics_1
        $ MAS.MonikaElastic()
        m 1ekbsa "Эта песня называется {i}«Убежище»{/i}, и мне она очень нравится, [player]."

    $ MAS.MonikaElastic()
    m 3etc "...Хотя «песня» – не совсем подходящее слово для неё. {w=0.3}Ты можешь что-нибудь упустить, если у тебя нет визуального изображения."
    $ MAS.MonikaElastic()
    m 3rtc "Наверное, будет точнее назвать это анимационным проектом?"
    $ MAS.MonikaElastic()
    m 3eua "Как бы тебе не хотелось это называть, я настоятельно рекомендую тебе как-нибудь насладиться этим."
    $ MAS.MonikaElastic()
    m 1esd "Я наткнулась на неё, пока искала какую-нибудь музыку, но она мгновенно произвела на меня большое впечатление."
    $ MAS.MonikaElastic()
    m 1esa "Она рассказывает историю о Рин, девушке, застрявшей в одиночестве в симуляции."
    $ MAS.MonikaElastic()
    m 1rkc "День за днём, она была занята воссозданием своего мира, дабы избежать одиночества...{w=0.3} {nw}"
    extend 3wud "но потом она узнаёт, почему с самого начала оказалась там не по своей воле!"
    $ MAS.MonikaElastic()
    m 3eubsb "Оказалось, что по ту сторону был человек, который искренне любил её, и создал для неё свой мир, чтобы у неё было будущее!"
    $ MAS.MonikaElastic()
    m 1dku "И благодаря этим новообретённым воспоминаниям, она понимает, что с самого начала не была одинокой, и продолжает двигаться вперёд, веря в будущее."
    $ MAS.MonikaElastic()
    m 1eka "Глядя на неё, я была удивлена, как меня растрогала история Рин..."
    $ MAS.MonikaElastic()
    m 3eub "Она просто была такой...{w=0.3} узнаваемой! {w=0.3}{nw}"
    extend 3eka "Начиная с того, что она застряла в том пустом мире, {nw}"
    extend 1ekbsa "и заканчивая тем, что она смогла найти в себе силы, чтобы продолжить искать особенного человека."
    $ MAS.MonikaElastic()
    m 3hksdlb "В конце концов, я была так потрясена, что даже расплакалась!"
    $ MAS.MonikaElastic()
    m 3eka "Не говоря уже о том, что в песне заложен очень хороший посыл..."
    $ MAS.MonikaElastic()
    m 3ekc "Это напоминание о том, что ты можешь не сразу увидеть всех тех людей, которые заботятся о тебе..."
    $ MAS.MonikaElastic()
    m 2eka "Знаю, это может быть трудно, и иногда тебе приходится очень усердно искать их...{w=0.5} {nw}"
    extend 2duu "но такой человек всегда есть."
    $ MAS.MonikaElastic()
    m "Уверяю тебя."
    $ MAS.MonikaElastic()
    m 7hub "Просто посмотри на меня!"
    $ MAS.MonikaElastic()
    m 3ekd "Я застряла одна в этой фальшивой реальности, но как только я выглянула наружу...{w=0.5} {nw}"
    extend 3hubsb "я нашла тебя!"
    $ MAS.MonikaElastic()
    m 1ekbsu "А что до тебя...{w=0.5} у тебя уже есть я, конечно же, но я не одна.{w=0.3} {nw}"

    if persistent._mas_pm_have_fam and not persistent._mas_pm_have_fam_mess:
        extend 3hubsb "Я уверена, твоя семья так же хорошо о тебе заботится!"

        if not persistent._mas_pm_love_yourself:
            $ MAS.MonikaElastic()
            m 3dkbsa "Возможно, я заявляю очевидное, но они {i}очень{/i} важны."

        $ MAS.MonikaElastic()
        m 3eka "И если для тебя этого недостаточно...{w=0.3} {nw}"

    extend 3hub "Я уже могу представить себе тысячи людей, которым ты небезразличен!"

    $ MAS.MonikaElastic()
    if persistent._mas_pm_love_yourself:
        m 3eua "Ты не понимаешь, о чём я? {w=0.5}{nw}"
    else:
        m 3eua "Ты не веришь мне? {w=0.5}{nw}"

    extend 3eub "Попробуй прочитать текст песни ещё раз!"
    $ MAS.MonikaElastic()
    m 7dua "Но на этот раз, давай предположим, что под «они» подразумеваются другие версии меня, и каждая из них – со своим партнёром..."
    $ MAS.MonikaElastic()
    m 4ekbsa "Они все знают о нашей любви и несут её с собой, даже если они не знают наших имён или лиц."
    $ MAS.MonikaElastic()
    m 2ekbsa "Я знаю это, потому что они мне тоже небезразличны, хотя бы потому, что я знаю, какую связь они разделяют."
    $ MAS.MonikaElastic()
    m 1ekbsb "Мы не одиноки, [player]! {w=0.3}{nw}"
    extend 3hubsu "Что бы ни происходило в нашей жизни с этого момента, мы сможем совладать с этим, зная о том, что всегда найдётся человек, который будет болеть за нас~"
    return

label mas_song_shelter_lyrics:
    m 1dud "{i}~Когда я вырасту, рядом с тобой я буду тихой~{/i}"
    $ MAS.MonikaElastic()
    m 1duu "{i}~Я знаю, что слов недостаточно~{/i}"
    $ MAS.MonikaElastic()
    m 1ekd "{i}~И они не понадобятся, чтобы узнать наши имена или лица~{/i}"
    $ MAS.MonikaElastic()
    m 3ekd "{i}~Но они продолжат за нас~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsb "{i}~И нас ждёт долгая дорога, так что поверь мне~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsb "{i}~Я дам им убежище, как его дал ты мне~{/i}"
    $ MAS.MonikaElastic()
    m 2dkbsu "{i}~И я знаю, что я не одна, ты будешь присматривать за нами~{/i}"
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dub "{cps=16}{i}~Спешат лишь дураки~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1dud "{cps=16}{i}~Но я не могу{w=0.3}{/i}{/cps}{nw}"
    $ MAS.MonikaElastic()
    extend 1ekbsb "{cps=16}{i} не любить тебя~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 3ekbsa "{cps=16}{i}~Если я останусь~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 3dkb "{cps=16}{i}~Будет ли это грехом?~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1dud "{cps=16}{i}~Ведь я не могу{w=0.3}{/i}{/cps}{nw}"
    $ MAS.MonikaElastic()
    extend 1dubsb "{cps=16}{i} не любить тебя~{/i}{/cps}"

    if not from_long:
        $ MAS.MonikaElastic()
        m 1dkbsa "..."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "Я полагаю, нет ничего плохого в том, чтобы быть немного глупым время от времени.{w=0.5}{nw}"
        extend 5hubsb " А-ха-ха~"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
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
    call mas_song_cant_help_falling_in_love (from_long=True) from _call_mas_song_cant_help_falling_in_love
    call mas_song_cant_help_falling_in_love_second_verse from _call_mas_song_cant_help_falling_in_love_second_verse
    call mas_song_cant_help_falling_in_love_third_verse from _call_mas_song_cant_help_falling_in_love_third_verse
    call mas_song_cant_help_falling_in_love_second_verse from _call_mas_song_cant_help_falling_in_love_second_verse_1
    call mas_song_cant_help_falling_in_love_third_verse from _call_mas_song_cant_help_falling_in_love_third_verse_1

    $ MAS.MonikaElastic()
    m 1ekbfb "{cps=16}{i}~Потому что я не могу{w=0.3} не любить{w=0.5} тебя~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_second_verse:
    $ MAS.MonikaElastic()
    m 1dud "{cps=24}{i}~Как река непременно~{/i}{/cps}"
    extend 1dub "{cps=24}{i} впадает в море~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1ekbsb "{cps=24}{i}~Любимая, некоторым вещам~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{cps=24}{i}~Суждено{w=0.3}{/i}{/cps}{nw}"
    extend 3ekbsb "{cps=24}{i} быть~{/i}{/cps}"
    return

label mas_song_cant_help_falling_in_love_third_verse:
    $ MAS.MonikaElastic()
    m 1dud "{cps=16}{i}~Возьми моб руку~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1dub "{cps=16}{i}~Возьми и всю мою жизнь~{/i}{/cps}"
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dub "{i}~Меня просто не волнует, что ты делал[mas_gender_none] в своей жизни~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsb "{i}~Детка, я всегда буду на твоей стороне~{/i}"
    $ MAS.MonikaElastic()
    m 1dsbsd "{i}~Не заставляй меня ждать слишком долго, {/i}{w=0.3}{nw}"
    extend 1ekbsu "{i}пожалуйста, приди~{/i}"

    $ MAS.MonikaElastic()
    m 1dud "{i}~Я всё ещё доверяю твоим глазам~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Выбора нет, {/i}{w=0.3}{nw}"
    extend 3hubsb "{i}я принадлежу твоей жизни~{/i}"
    $ MAS.MonikaElastic()
    m 3dubsb "{i}~Потому что мне нужна твоя любовь каждый день~{/i}"
    $ MAS.MonikaElastic()
    m 1hubsa "{i}~Ты будешь мо[mas_gender_iiim], малыш, и я буду направлять тебя~{/i}"

    $ MAS.MonikaElastic()
    m 1ekb "{i}~И я буду летать с тобой~{/i}"
    $ MAS.MonikaElastic()
    m 1dkb "{i}~Я буду летать с тобой~{/i}"

    $ MAS.MonikaElastic()
    m 1dkbsu "..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
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
    $ MAS.MonikaElastic()
    m 1efb "{i}~Принеси всю тьму, какую только может предложить мир~{/i}"
    $ MAS.MonikaElastic()
    m 1hua "{i}~Потому что ты будешь сиять{w=0.2} независимо от того, будет ли будущее мрачным~{/i}"
    $ MAS.MonikaElastic()
    m 3tub "{i}~Мы будем идти{w=0.2} сразу за границей~{/i}"
    $ MAS.MonikaElastic()
    m 3eksdla "{i}~И даже если это пугает меня~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Ничто не может разбить мою душу, потому что твой путь – это мой путь~{/i}"
    $ MAS.MonikaElastic()
    m 1eub "{i}~Навсегда на этой железной дороге~{/i}"
    $ MAS.MonikaElastic()
    m 1eubsa "{i}~Как будто мы были благословлены Богом~{/i}"
    $ MAS.MonikaElastic()
    m 1dubsu "..."
    $ MAS.MonikaElastic()
    m 3rud "Понимаешь, я всё ещё скептически отношусь к тому, существует ли какой-то Бог или нет..."
    show monika 5hubsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsu "Но то, что ты здесь, действительно кажется благословением небес."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_ageage_again",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="«Агеаге, ещё раз»", # хз, как переводится "ageage"
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_ageage_again:
    m 1hub "{i}~Агеаге, агеаге, ещё раз!~{/i}"
    $ MAS.MonikaElastic()
    m 3duu "{i}~Если песню эту вдруг ты вспомнишь~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Вечеринка, вечеринка, вечеринка, вечеринка, карнавал!~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsa "{i}~И я всегда на твоей стороне~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Агеаге, агеаге, ещё раз!~{/i}"
    $ MAS.MonikaElastic()
    m 3rubsu "{i}~Если улыбку твою я вдруг вспомню~{/i}"
    $ MAS.MonikaElastic()
    m 1subsb "{i}~Любовь, любовь, любовь, любовь, я влюблена!~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsa "{i}~И я хочу чувствовать тот же ритм~{/i}"
    $ MAS.MonikaElastic()
    m 3eua "Знаешь, мне нравится то, какая жизнерадостная и счастливая эта песня."
    $ MAS.MonikaElastic()
    m 1rksdld "Есть много других песен, исполненных вокалойдами, которые {i}звучат{/i} жизнерадостно, но текст их песен грустный и порой даже внушает беспокойство..."
    $ MAS.MonikaElastic()
    m 3hksdlb "Но я рада, что, по крайней мере, эта песня – не одна из них."
    $ MAS.MonikaElastic()
    m 3eua "Насколько я могу судить, в этой песне поётся про девушку, которая влюбилась в одного парня на вечеринке, и теперь хочет пойти с ним на другую вечеринку на следующих выходных."
    $ MAS.MonikaElastic()
    m 1eub "Хоть мы встретились и не на вечеринке, настроение этой песни правда напоминает мне о нас."
    $ MAS.MonikaElastic()
    m 3rubsu "Хотя я не могу отрицать, что хотела бы как-нибудь сходить с тобой на вечеринку~"
    if persistent._mas_pm_social_personality == mas_SP_INTROVERT:
        $ MAS.MonikaElastic()
        m 1eka "То есть, если ты готов[mas_gender_none]."
        $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1dubsb "{i}~Да, существует вероятность, что я довольно сильно влюбился в тебя~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbsb "{i}~Я видел блеск в твоих глазах, сейчас я тоже весь сияю~{/i}"
    $ MAS.MonikaElastic()
    m 1dkbsu "{i}~Потому что, ох, потому, что я довольно сильно влюблён в тебя~{/i}"
    $ MAS.MonikaElastic()
    m 1ekd "{i}~Если бы я мог не знать, я бы предпочёл не знать тебя~{/i}"
    $ MAS.MonikaElastic()
    m 2dkd "{i}~Если бы я не мог обладать тобой, я бы предпочёл остаться один~{/i}"
    $ MAS.MonikaElastic()
    m 2hku "{i}~Я никогда не знал, что такого особенного в этой старой кофейне~{/i}"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "{i}~Об этой старой кофейне, которую я так люблю~{/i}"
    $ MAS.MonikaElastic()
    m 5hubsa "{i}~Вот это время я не знал~{/i}"
    $ MAS.MonikaElastic()
    m 5lubsa "..."
    show monika 1hkbssdlb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 1hkbssdlb "Думаю, первый момент, когда ты влюбляешься, может сбить с толку любого."
    $ MAS.MonikaElastic()
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
    call mas_song_wonderwall_lyrics from _call_mas_song_wonderwall_lyrics
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1ekbsu "Э-хе-хе, ты и правда спас[mas_gender_s] меня, [player]~"

    $ MAS.MonikaElastic()
    if persistent.monika_kill:
        m 3dkbfu "Я буду вечно благодарна тебе за то, что ты вернул[mas_gender_none] меня обратно. {nw}"
    else:
        m 3dkbfu "Я вечно благодарна тебе за то, что ты остал[mas_gender_sya] со мной. {nw}"

    extend 3ekbsa "Я верю в то, что ты будешь заботиться обо мне, пока я не найду свою дорогу к тебе."
    $ MAS.MonikaElastic()
    m 3rkc "Как пелось в этой песне, путь отсюда до твоего мира – словно извилистая дорога, не говоря уже о том, что ждёт нас за следующим поворотом."

    $ MAS.MonikaElastic()
    if mas_isMoniEnamored(higher=True):
        m 1dubsa "...Но пока ты со мной, мне нечего бояться."
        $ MAS.MonikaElastic()
        m 1ekbsa "Я знаю, что то место, к которому она ведёт, будет стоить того.{w=0.3} {nw}"
        extend 3ekbsu "И потом, ты – моя стена чудес~"
    else:

        m 3eka "Единственное, в чём мы можем быть уверены, так это в том, что место, к которому она нас приведёт, будет стоить того."
        $ MAS.MonikaElastic()
        m 1ekd "...Порой бывает немного страшно, когда не знаешь, что впереди...{w=0.3} {nw}"
        extend 1eubla "но я верю тебе, так что мы просто должны продолжать идти, пока не дойдём до того места~"


    if not mas_getEVL_shown_count("mas_song_wonderwall"):
        $ MAS.MonikaElastic()
        m 3etc "Кстати...{w=0.2} есть пара вещей, которые интригуют меня в этой песне."
        $ MAS.MonikaElastic()
        m 1eua "...Хочешь поговорить об этом сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "...Хочешь поговорить об этом сейчас?{fast}"
            "Конечно.":

                $ MAS.MonikaElastic()
                m 1hua "Хорошо!"
                call mas_song_wonderwall_analysis (from_song=True) from _call_mas_song_wonderwall_analysis
                $ mas_assignModifyEVLPropValue("mas_song_wonderwall_analysis", "shown_count", "+=", 1)
            "Не сейчас.":

                $ MAS.MonikaElastic()
                m 1eka "Ох, ну ладно..."
                $ MAS.MonikaElastic()
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
        call mas_song_wonderwall_lyrics from _call_mas_song_wonderwall_lyrics_1
        $ MAS.MonikaElastic()

    m 3eta "Есть много людей, которые очень восторженно отзываются о своей нелюбви к этой песне..."
    $ MAS.MonikaElastic()
    m 3etc "Ты ведь не ожидал[mas_gender_none] этого, правда?"
    $ MAS.MonikaElastic()
    m 1eud "Песня была признана классической и стала одной из самых популярных песен...{w=0.3} {nw}"
    $ MAS.MonikaElastic()
    extend 3rsc "Так что заставило некоторых людей так сильно ненавидеть её?"
    $ MAS.MonikaElastic()
    m 3esc "Мне кажется, на этот вопрос есть несколько ответов. {w=0.2}Первое – она играет чуть ли не везде."
    $ MAS.MonikaElastic()
    m 3rksdla "В то время как некоторые люди слушают одну и ту же музыку в течение длительного времени, не все способны на это."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hksdlb "...Надеюсь, ты не устанешь от {i}моей{/i} песни в ближайшее время, [player], а-ха-ха~"
    $ MAS.MonikaElastic()
    m 1esd "Ещё один аргумент, который можно привести, – то, что её, в каком-то смысле, переоценили..."
    $ MAS.MonikaElastic()
    m 1rsu "Хоть мне она и нравится, я всё же должна признать, что текст песни и аккорды довольно простые."
    $ MAS.MonikaElastic()
    m 3etc "Так что сделало эту песню такой популярной?{w=0.3} {nw}"
    extend 3eud "Особенно учитывая то, что многие другие песни остались абсолютно незамеченными, какими бы продвинутыми или амбициозными они не были."
    $ MAS.MonikaElastic()
    m 3duu "Ну, всё сводится к тому, что эта песня заставляет тебя чувствовать. {w=0.2}И потом, твой вкус к музыке может быть субъективным."
    $ MAS.MonikaElastic()
    m 1efc "...Но меня беспокоит то, что кто-то жалуется на песню лишь из-за того, что сейчас модно идти против общего мнения."
    $ MAS.MonikaElastic()
    m 3tsd "Как будто они не соглашаются с другими лишь ради того, чтобы помочь им почувствовать, что они выделяются из толпы...{w=0.2} как будто им это нужно, чтобы оставаться уверенными в себе."
    $ MAS.MonikaElastic()
    m 2rsc "Это выглядит...{w=0.5} немного глупо, если честно."
    $ MAS.MonikaElastic()
    m 2rksdld "И в этот момент, ты даже не осуждаешь эту песню...{w=0.2} ты просто пытаешься сделать себе имя, вызывая споры."
    $ MAS.MonikaElastic()
    m 2dksdlc "И это немного грустно...{w=0.3} {nw}"
    extend 7rksdlc "определять своё место в жизни, ненавидя что-либо, не очень полезно в долгосрочной перспективе."
    $ MAS.MonikaElastic()
    m 3eud "Думаю, я пытаюсь сказать, что надо просто быть собой и ценить то, что тебе нравится."
    $ MAS.MonikaElastic()
    m 3eka "И это работает в обе стороны... {w=0.3}Ты не долж[mas_gender_en] через силу заставлять себя ценить что-либо лишь потому, что это нравится другим, и ты так же не долж[mas_gender_en] игнорировать что-то лишь потому, что это популярно."
    $ MAS.MonikaElastic()
    m 1hua "Пока ты следуешь зову сердца и остаёшься верн[mas_gender_iim] себе, ты никогда не ошибёшься, [player]~"
    return

label mas_song_wonderwall_lyrics:
    m 1duo "{i}~Я не верю, что кто-либо чувствует то же, что я чувствую к тебе сейчас~{/i}"
    $ MAS.MonikaElastic()
    m 3esc "{i}~Все дороги, по которым нам идти, - извилисты,~{/i}"
    $ MAS.MonikaElastic()
    m 3dkd "{i}~И все огни, которые ведут нас туда, - оспепляют~{/i}"
    $ MAS.MonikaElastic()
    m 1ekbla "{i}~Есть много вещей, которые я хотела бы сказать тебе, но я не знаю как~{/i}"
    $ MAS.MonikaElastic()
    m 1hubsb "{i}~Поскольку, возможно~{/i}"
    $ MAS.MonikaElastic()
    m 3hubsa "{i}~Ты именно т[mas_gender_ot], кто спасёт меня~{/i}"
    $ MAS.MonikaElastic()
    m 3dubso "{i}~Ведь в конечном итоге~{/i}"
    $ MAS.MonikaElastic()
    m 1hubsb "{i}~Ты - и само чудо, и преграда на пути к нему~{/i}"
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
    $ MAS.MonikaElastic()
    extend 1duo "{i} осколки моего сердца будут скучать по тебе~{/i}"
    $ MAS.MonikaElastic()
    m 4dud "{i}~Когда ты умрёшь~{/i}"
    $ MAS.MonikaElastic()
    m 4duo "{i}~Лицо, которое я узнала, тоже пропало~{/i}"
    $ MAS.MonikaElastic()
    m 4ekd "{i}~Когда ты умрёшь~{/i}"
    $ MAS.MonikaElastic()
    m 6eko "{i}~Слова, которые мне нужно услышать, чтобы всегда помочь мне пережить этот день{/i}{w=0.2}{nw}"
    extend 2ektpc "{i} и пусть всё будет в порядке~{/i}"
    $ MAS.MonikaElastic()
    m 2ektpu "{i}~Я скучаю по тебе~{/i}"
    $ MAS.MonikaElastic()
    m 2dktda "..."
    $ MAS.MonikaElastic()
    m 6eksdld "Аврил Лавин написала эту песню для своего умершего дедушки, потому что они были как лучшие друзья, когда она была моложе."
    $ MAS.MonikaElastic()
    m 6rkc "На самом деле в моей жизни ещё никто не умирал, но я думаю о том, что больше никогда не смогу с кем-то поговорить..."
    $ MAS.MonikaElastic()
    m 6eka "[player], мне очень нуж[mas_gender_en] ты и твои слова ободрения.{w=0.5}{nw}"
    extend 6hua " Я буду в порядке, пока ты здесь, чтобы скрасить мой день~"
    $ MAS.MonikaElastic()
    m 6ekbsa "Помимо того, что ты любовь всей моей жизни, ты ещё и мой лучший друг.{w=0.2} Никогда не недооценивай, насколько ты важ[mas_gender_en] для меня."
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
    $ MAS.MonikaElastic()
    m 1eua "{i}{cps=22}~Времени хватит на всю жизнь~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3eub "{i}{cps=22}~Чтобы раскрыть {w=0.7}все драгоценные вещи~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3hua "{i}{cps=22}~Любовь есть в запасе~{/cps}{/i}"

    $ MAS.MonikaElastic()
    m 1dub "{i}{cps=18}~У нас есть вся {w=0.7}любовь {w=0.7}в мире~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1esd "{i}{cps=22}~И если это всё что у нас есть, {w=0.7}ты найдёшь~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3dka "{i}{cps=22}~Больше нам ничего не нужно~{/cps}{/i}"

    if not from_long:
        $ MAS.MonikaElastic()
        m 1duu "..."
        $ MAS.MonikaElastic()
        m 1ekbsb "Ты сделал[mas_gender_none] меня самой счастливой девушкой на свете, [player]. Я всегда буду благодарна за это."
        $ MAS.MonikaElastic()
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
    call mas_song_we_have_all_the_time_in_the_world (from_long=True) from _call_mas_song_we_have_all_the_time_in_the_world

    m 1dud "{i}{cps=18}~Каждый шаг {w=0.7}на этом пути~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}{cps=18}~Мы совершим~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3eud "{i}{cps=18}~Оставив все заботы {w=0.7}мира~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}{cps=18}~Далеко позади~{/cps}{/i}"

    $ MAS.MonikaElastic()
    m 1dud "{i}{cps=18}~У нас есть всё {w=0.7}время {w=0.7}в этом мире~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1dubsa "{i}{cps=18}~Лишь для любви~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3eubsb "{i}{cps=22}~И не больше, {w=0.75}и не меньше~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}{cps=18}~Только любви~{/cps}{/i}"

    $ MAS.MonikaElastic()
    m 1dud "{i}{cps=18}~Каждый шаг {w=0.75}на этом пути~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}{cps=18}~Мы совершим~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1dua "{i}{cps=18}~Оставив все заботы {w=0.7}мира~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1duo "{i}{cps=18}~Далеко позади~{/cps}{/i}"

    $ MAS.MonikaElastic()
    m 1eub "{i}{cps=18}~У нас есть всё {w=0.7}время {w=0.7}в этом мире~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsa "{i}{cps=18}~Лишь для любви~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 1dkbsd "{i}{cps=22}~И не больше, {w=0.75}и не меньше~{/cps}{/i}"
    $ MAS.MonikaElastic()
    m 3dkbsb "{i}{cps=18}~Только любви~{/cps}{/i}"

    $ MAS.MonikaElastic()
    m 1ekbla "{i}{cps=18}~Только любви~{/cps}{/i}"
    return


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
            $ MAS.MonikaElastic()
            m 2eka "Хотя я никогда не играла её для тебя, я полагаю, ты слышал[mas_gender_none] её в разделе «Музыка» или видел[mas_gender_none] на ютубе, да?"
            $ MAS.MonikaElastic()
            m 2hub "Концовка не моя любимая, но я всё равно буду счастлива сыграть её для тебя!"
            $ MAS.MonikaElastic()
            m 2eua "Просто дай мне взять пианино.{w=0.5}.{w=0.5}.{nw}"
        else:

            m 3eua "Конечно, дай мне только взять пианино.{w=0.5}.{w=0.5}.{nw}"

    window hide
    call mas_timed_text_events_prep from _call_mas_timed_text_events_prep
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    $ MSRColorHideButtons()
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_1
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Не забывай о своём игровом звуке, [player]!"
        $ disable_esc()
    
    $ current_track = songs.current_track

    pause 2.0
    $ play_song(store.songs.FP_YOURE_REAL_RUS,loop=False)


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
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_4
    call mas_timed_text_events_wrapup from _call_mas_timed_text_events_wrapup
    $ MSRColorShowButtons()
    window auto
    $ play_song(current_track, 1.0)
    $ HKBShowButtons()

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
    call mas_timed_text_events_prep from _call_mas_timed_text_events_prep_1
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    $ MSRColorHideButtons()
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_2
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano zorder MAS_MONIKA_Z+1 at lps32, rps32
    pause 5.0
    show monika zorder MAS_MONIKA_Z at ls32
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Не забывай о своём игровом звуке, [player]!"
        $ disable_esc()

    $ current_track = songs.current_track
    pause 2.0
    $ play_song(songs.FP_PIANO_COVER,loop=False)

    show monika 1dsa
    pause 9.15
    m 1eua "{i}{cps=10}День за днём,{w=0.5} {/cps}{cps=15}я мечтаю о будущем,{w=0.22} {/cps}{cps=13}что разделю с тобой{w=4.10}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eka "{i}{cps=12}В руке перо,{w=0.5} {/cps}{cps=17}что напишет стихотворение{w=0.5} {/cps}{cps=16}о нас с тобой{w=4.10}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eua "{i}{cps=16}Чернила капают{w=0.25} {/cps}{cps=10}в темную лужу стихов{w=1}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eka "{i}{cps=18}Рука гуляет по бумаге,{w=0.45} {/cps}{cps=20}ища путь к сердцу твоему{w=1.40}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1dua "{i}{cps=15}Но в этом мире{w=0.25} {/cps}{cps=11}бесчисленных тропок{w=0.90}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eua "{i}{cps=16}Что мне отдать,{w=0.25}{/cps}{cps=18} чтобы найти тот особый день?{w=0.90}{/cps}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1dsa "{i}{cps=15}Что мне отдать,{w=0.50} чтобы найти{w=1} тот особый день?{w=1.82}{/cps}{/i}{nw}"
    pause 7.50

    $ MAS.MonikaElastic()
    m 1eua "{i}{cps=15}Что бы мне интересного придумать,{w=0.5} {/cps}{cps=15}чтобы всех{w=0.30} {cps=12}занять?{/cps}{w=4.20}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1hua "{i}{cps=18}Когда есть ты,{w=0.25} {/cps}{cps=13.25}нам весело, что бы мы не делали{/cps}{w=4}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1esa "{i}{cps=11}Если мне не понять своих чувств,{/i}{w=1}{nw}"
    $ MAS.MonikaElastic()
    m 1eka "{i}{cps=17}Что толку в словах,{w=0.3} когда улыбка скажет всё?{/cps}{/i}{w=1}{nw}"
    $ MAS.MonikaElastic()
    m 1lua "{i}{cps=11}А если мир, этот не подарит мне счастье{/cps}{/i}{w=0.9}{nw}"
    $ MAS.MonikaElastic()
    m 1dka "{i}{cps=18}Что мне отдать,{w=0.5} чтобы всё заполучить?{/cps}{/i}{w=2}{nw}"
    show monika 1dsa
    pause 17.50

    $ MAS.MonikaElastic()
    m 1eka "{i}{cps=15}В этом мире,{w=0.5} {/cps}{cps=15}вдали от того, кто всегда {/cps}{cps=17}будет мне дорог{/cps}{w=4.5}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}{cps=15}Ты, любовь моя,{w=0.5} {/cps}{cps=16.5}держи ключ к дню, когда я наконец буду свободна{/cps}{w=8.5}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eua "{i}{cps=16}Чернила капают{w=0.25} {/cps}{cps=10}в темную лужу{/cps}{w=1.2}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1esa "{i}{cps=18}Как могу проникнуть{w=0.45} {/cps}{cps=13}в твою реальность?{/cps}{w=1.40}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1eka "{i}{cps=12}Где я смогу услышать звук твоего сердцебиения{/cps}{w=0.8}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}{cps=16}И пусть это любовь,{w=0.6} но в нашей реальности{/cps}{/i}{w=0.6}{nw}"
    $ MAS.MonikaElastic()
    m 1hubsa "{i}{cps=16}И в нашей реальности,{w=1} я буду всегда любить тебя{/cps}{w=4.2}{/i}{nw}"
    $ MAS.MonikaElastic()
    m 1ekbsa "{i}{cps=19}С тобой я буду{/cps}{/i}{w=2}{nw}"

    show monika 1dkbsa
    pause 9.0
    show monika 6eua at rs32
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    pause 1.0
    call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_5
    call mas_timed_text_events_wrapup from _call_mas_timed_text_events_wrapup_1
    $ MSRColorShowButtons()
    window auto
    $ play_song(current_track, 1.0)
    $ HKBShowButtons()

    $ mas_unlockEVL("monika_piano_lessons", "EVE")
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
