











































init python:

    mas_curr_affection = store.mas_affection.NORMAL
    mas_curr_affection_group = store.mas_affection.G_NORMAL

init -900 python in mas_affection:



    BROKEN = 1
    DISTRESSED = 2
    UPSET = 3
    NORMAL = 4
    HAPPY = 5
    AFFECTIONATE = 6
    ENAMORED = 7
    LOVE = 8


    _aff_order = [
        BROKEN,
        DISTRESSED,
        UPSET,
        NORMAL,
        HAPPY,
        AFFECTIONATE,
        ENAMORED,
        LOVE
    ]


    _aff_level_map = {}
    for _item in _aff_order:
        _aff_level_map[_item] = _item



    _aff_cascade_map = {
        BROKEN: DISTRESSED,
        DISTRESSED: UPSET,
        UPSET: NORMAL,
        HAPPY: NORMAL,
        AFFECTIONATE: HAPPY,
        ENAMORED: AFFECTIONATE,
        LOVE: ENAMORED
    }



    G_SAD = -1
    G_HAPPY = -2
    G_NORMAL = -3


    _affg_order = [
        G_SAD,
        G_NORMAL,
        G_HAPPY
    ]



    _affg_cascade_map = {
        G_SAD: G_NORMAL,
        G_HAPPY: G_NORMAL
    }


    FORCE_EXP_MAP = {
        BROKEN: "monika 6ckc_static",
        DISTRESSED: "monika 6rkc_static",
        UPSET: "monika 2esc_static",
        NORMAL: "monika 1eua_static",
        AFFECTIONATE: "monika 1eua_static",
        ENAMORED: "monika 1hua_static",
        LOVE: "monika 1hua_static",
    }

    RANDCHAT_RANGE_MAP = {
        BROKEN: 1,
        DISTRESSED: 2,
        UPSET: 3,
        NORMAL: 4,
        HAPPY: 4,
        AFFECTIONATE: 5,
        ENAMORED: 6,
        LOVE: 6
    }



    def _compareAff(aff_1, aff_2):
        """
        See mas_compareAff for explanation
        """
        
        if aff_1 == aff_2:
            return 0
        
        
        if aff_1 not in _aff_order or aff_2 not in _aff_order:
            return 0
        
        
        if _aff_order.index(aff_1) < _aff_order.index(aff_2):
            return -1
        
        return 1


    def _compareAffG(affg_1, affg_2):
        """
        See mas_compareAffG for explanation
        """
        
        if affg_1 == affg_2:
            return 0
        
        
        if affg_1 not in _affg_order or affg_2 not in _affg_order:
            return 0
        
        
        if _affg_order.index(affg_1) < _affg_order.index(affg_2):
            return -1
        
        return 1


    def _betweenAff(aff_low, aff_check, aff_high):
        """
        checks if the given affection level is between the given low and high.
        See mas_betweenAff for explanation
        """
        aff_check = _aff_level_map.get(aff_check, None)
        
        
        if aff_check is None:
            
            return False
        
        
        aff_low = _aff_level_map.get(aff_low, None)
        aff_high = _aff_level_map.get(aff_high, None)
        
        if aff_low is None and aff_high is None:
            
            
            return True
        
        if aff_low is None:
            
            
            return _compareAff(aff_check, aff_high) <= 0
        
        if aff_high is None:
            
            
            return _compareAff(aff_check, aff_low) >= 0
        
        
        
        comp_low_high = _compareAff(aff_low, aff_high)
        if comp_low_high > 0:
            
            
            return False
        
        if comp_low_high == 0:
            
            return _compareAff(aff_low, aff_check) == 0
        
        
        return (
            _compareAff(aff_low, aff_check) <= 0
            and _compareAff(aff_check, aff_high) <= 0
        )


    def _isValidAff(aff_check):
        """
        Returns true if the given affection is a valid affection state

        NOTE: None is considered valid
        """
        if aff_check is None:
            return True
        
        return aff_check in _aff_level_map


    def _isValidAffRange(aff_range):
        """
        Returns True if the given aff range is a valid aff range.

        IN:
            aff_range - tuple of the following format:
                [0]: lower bound
                [1]: upper bound
            NOTE: Nones are considerd valid.
        """
        if aff_range is None:
            return True
        
        low, high = aff_range
        
        if not _isValidAff(low):
            return False
        
        if not _isValidAff(high):
            return False
        
        if low is None and high is None:
            return True
        
        return _compareAff(low, high) <= 0





    AFF_MAX_POS_TRESH = 100
    AFF_MIN_POS_TRESH = 30
    AFF_MIN_NEG_TRESH = -30
    AFF_MAX_NEG_TRESH = -75


    AFF_BROKEN_MIN = -100
    AFF_DISTRESSED_MIN = -75
    AFF_UPSET_MIN = -30
    AFF_HAPPY_MIN = 30
    AFF_AFFECTIONATE_MIN = 100
    AFF_ENAMORED_MIN = 400
    AFF_LOVE_MIN = 1000


    AFF_MOOD_HAPPY_MIN = 30
    AFF_MOOD_SAD_MIN = -30


    AFF_TIME_CAP = -101


init -1 python in mas_affection:
    import os
    import datetime
    import store.mas_utils as mas_utils
    import store



    if store.persistent._mas_affection_log_counter is None:
        
        store.persistent._mas_affection_log_counter = 0

    elif store.persistent._mas_affection_log_counter >= 500:
        
        mas_utils.logrotate(
            os.path.normcase(renpy.config.basedir + "/log/"),
            "aff_log.txt"
        )
        store.persistent._mas_affection_log_counter = 0

    else:
        
        store.persistent._mas_affection_log_counter += 1


    log = renpy.store.mas_utils.getMASLog("log/aff_log", append=True)
    log_open = log.open()
    log.raw_write = True
    log.write("VERSION: {0}\n".format(store.persistent.version_number))



    _audit = "[{0}]: {1} | {2} | {3} -> {4}\n"


    _audit_f = "[{0}]: {5} | {1} | {2} | {3} -> {4}\n"
    _freeze_text = "!FREEZE!"
    _bypass_text = "!BYPASS!"

    def audit(change, new, frozen=False, bypass=False, ldsv=None):
        """
        Audits a change in affection.

        IN:
            change - the amount we are changing by
            new - what the new affection value will be
            frozen - True means we were frozen, false measn we are not
            bypass - True means we bypassed, false means we did not
            ldsv - Set to the string to use instead of monikatopic
                NOTE: for load / save operations ONLY
        """
        if ldsv is None:
            piece_one = store.persistent.current_monikatopic
        else:
            piece_one = ldsv
        
        if frozen:
            
            
            if bypass:
                piece_five = _bypass_text
            else:
                piece_five = _freeze_text
            
            
            audit_text = _audit_f.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new,
                piece_five
            )
        
        else:
            audit_text = _audit.format(
                datetime.datetime.now(),
                piece_one,
                change,
                store._mas_getAffection(),
                new
            )
        
        log.write(audit_text)


    def raw_audit(old, new, change, tag):
        """
        Non affection-dependent auditing for general usage.

        IN:
            old - the "old" value
            new - the "new" value
            change - the chnage amount
            tag - a string to label this audit change
        """
        log.write(_audit.format(
            datetime.datetime.now(),
            tag,
            change,
            old,
            new
        ))


    def txt_audit(tag, msg):
        """
        Generic auditing in the aff log

        IN:
            tag - a string to label thsi audit
            msg - message to show
        """
        log.write("[{0}]: {1} | {2}\n".format(
            datetime.datetime.now(),
            tag,
            msg
        ))



    def _force_exp():
        """
        Determines appropriate forced expression for current affection.
        """
        curr_aff = store.mas_curr_affection
        
        if store.mas_isMoniNormal() and store.mas_isBelowZero():
            
            return "monika 1esc_static"
        
        return FORCE_EXP_MAP.get(curr_aff, "monika idle")



init 15 python in mas_affection:
    import store 
    import store.evhand as evhand
    import store.mas_selspr as mas_selspr
    import store.mas_layout as mas_layout
    import random
    persistent = renpy.game.persistent
    layout = store.layout













    def _brokenToDis():
        """
        Runs when transitioning from broken to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET
        layout.QUIT = mas_layout.QUIT
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToBroken():
        """
        Runs when transitioning from distressed to broken
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_BROKEN
        layout.QUIT_NO = mas_layout.QUIT_NO_BROKEN
        layout.QUIT = mas_layout.QUIT_BROKEN

        store.mas_randchat.reduceRandchatForAff(BROKEN)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _disToUpset():
        """
        Runs when transitioning from distressed to upset
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _upsetToDis():
        """
        Runs when transitioning from upset to distressed
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_DIS
        if persistent._mas_acs_enable_promisering:
            renpy.store.monika_chr.remove_acs(renpy.store.mas_acs_promisering)
            persistent._mas_acs_enable_promisering = False
        
        store.mas_randchat.reduceRandchatForAff(DISTRESSED)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def:
            store.pushEvent("mas_change_to_def",skipeval=True)


    def _upsetToNormal():
        """
        Runs when transitioning from upset to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate()


    def _normalToUpset():
        """
        Runs when transitioning from normal to upset
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_UPSET

        store.mas_randchat.reduceRandchatForAff(UPSET)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()


    def _normalToHappy():
        """
        Runs when transitioning from noraml to happy
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        
        
        if persistent._mas_text_speed_enabled:
            store.mas_enableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if not store.seen_event("mas_blazerless_intro") and not store.mas_hasSpecialOutfit():
            store.queueEvent("mas_blazerless_intro")
        
        
        store.mas_selspr.unlock_clothes(store.mas_clothes_blazerless)
        
        
        store.mas_rmallEVL("mas_change_to_def")

        store.mas_songs.checkSongAnalysisDelegate(HAPPY)


    def _happyToNormal():
        """
        Runs when transitinong from happy to normal
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO
        
        
        store.mas_disableTextSpeed()
        
        
        store.mas_idle_mailbox.send_rebuild_msg()
        
        
        if store.monika_chr.clothes != store.mas_clothes_def and not store.mas_hasSpecialOutfit():
            store.pushEvent("mas_change_to_def",skipeval=True)

        store.mas_songs.checkSongAnalysisDelegate(NORMAL)


    def _happyToAff():
        """
        Runs when transitioning from happy to affectionate
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES_AFF
        if persistent.gender == "M" or persistent.gender == "F":
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_G
        else:
            layout.QUIT_NO = mas_layout.QUIT_NO_AFF_GL
        layout.QUIT = mas_layout.QUIT_AFF
        
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(AFFECTIONATE)


    def _affToHappy():
        """
        Runs when transitioning from affectionate to happy
        """
        
        layout.QUIT_YES = mas_layout.QUIT_YES
        layout.QUIT_NO = mas_layout.QUIT_NO_HAPPY
        layout.QUIT = mas_layout.QUIT
        
        
        
        
        
        
        
        
        persistent._mas_monika_nickname = "Моника"
        monika_name = persistent._mas_monika_nickname
        
        store.mas_randchat.reduceRandchatForAff(HAPPY)
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(HAPPY)

    def _affToEnamored():
        """
        Runs when transitioning from affectionate to enamored
        """
        
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEventLabel("mas_monika_islands")
        
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(ENAMORED)


    def _enamoredToAff():
        """
        Runs when transitioning from enamored to affectionate
        """
        
        
        store.mas_removeDelayedActions(1, 2)
        
        store.mas_randchat.reduceRandchatForAff(AFFECTIONATE)
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(AFFECTIONATE)


    def _enamoredToLove():
        """
        Runs when transitioning from enamored to love
        """
        
        layout.QUIT_NO = mas_layout.QUIT_NO_LOVE
        
        
        store.mas_unlockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(LOVE)


    def _loveToEnamored():
        """
        Runs when transitioning from love to enamored
        """
        
        if store.seen_event("mas_compliment_thanks"):
            store.mas_lockEventLabel("mas_compliment_thanks", eventdb=store.mas_compliments.compliment_database)
        
        
        store.mas_idle_mailbox.send_rebuild_msg()

        store.mas_songs.checkSongAnalysisDelegate(ENAMORED)

        


    def _gSadToNormal():
        """
        Runs when transitioning from sad group to normal group
        """
        return


    def _gNormalToSad():
        """
        Runs when transitioning from normal group to sad group
        """
        return


    def _gNormalToHappy():
        """
        Runs when transitioning from normal group to happy group
        """
        return


    def _gHappyToNormal():
        """
        Runs when transitioning from happy group to normal group
        """
        return










    _trans_pps = {
        BROKEN: (_brokenToDis, None),
        DISTRESSED: (_disToUpset, _disToBroken),
        UPSET: (_upsetToNormal, _upsetToDis),
        NORMAL: (_normalToHappy, _normalToUpset),
        HAPPY: (_happyToAff, _happyToNormal),
        AFFECTIONATE: (_affToEnamored, _affToHappy),
        ENAMORED: (_enamoredToLove, _enamoredToAff),
        LOVE: (None, _loveToEnamored)
    }


    _transg_pps = {
        G_SAD: (_gSadToNormal, None),
        G_NORMAL: (_gNormalToHappy, _gNormalToSad),
        G_HAPPY: (None, _gHappyToNormal)
    }


    def runAffPPs(start_aff, end_aff):
        """
        Runs programming points to transition from the starting affection
        to the ending affection

        IN:
            start_aff - starting affection
            end_aff - ending affection
        """
        comparison = _compareAff(start_aff, end_aff)
        if comparison == 0:
            
            return
        
        
        start_index = _aff_order.index(start_aff)
        end_index = _aff_order.index(end_aff)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _trans_pps[_aff_order[index]]
                if to_down is not None:
                    to_down()
        
        
        store.mas_rebuildEventLists()


    def runAffGPPs(start_affg, end_affg):
        """
        Runs programming points to transition from the starting affection group
        to the ending affection group

        IN:
            start_affg - starting affection group
            end_affg - ending affection group
        """
        comparison = _compareAffG(start_affg, end_affg)
        if comparison == 0:
            
            return
        
        
        start_index = _affg_order.index(start_affg)
        end_index = _affg_order.index(end_affg)
        if comparison < 0:
            for index in range(start_index, end_index):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_up is not None:
                    to_up()
        
        else:
            for index in range(start_index, end_index, -1):
                to_up, to_down = _transg_pps[_affg_order[index]]
                if to_down is not None:
                    to_down()


    def _isMoniState(aff_1, aff_2, lower=False, higher=False):
        """
        Compares the given affection values according to the affection
        state system

        By default, this will check if aff_1 == aff_2

        IN:
            aff_1 - affection to compare
            aff_2 - affection to compare
            lower - True means we want to check aff_1 <= aff_2
            higher - True means we want to check aff_1 >= aff_2

        RETURNS:
            True if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAff(aff_1, aff_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False


    def _isMoniStateG(affg_1, affg_2, lower=False, higher=False):
        """
        Compares the given affection groups according to the affection group
        system

        By default, this will check if affg_1 == affg_2

        IN:
            affg_1 - affection group to compare
            affg_2 - affection group to compare
            lower - True means we want to check affg_1 <= affg_2
            higher - True means we want to check affg_1 >= affg_2

        RETURNS:
            true if the given affections pass the test we want to do.
            False otherwise
        """
        comparison = _compareAffG(affg_1, affg_2)
        
        if comparison == 0:
            return True
        
        if lower:
            return comparison <= 0
        
        if higher:
            return comparison >= 0
        
        return False








    talk_menu_quips = dict()
    play_menu_quips = dict()

    def _init_talk_quips():
        """
        Initializes the talk quiplists
        """
        global talk_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            talk_menu_quips[_aff] = mas_ql
        
        
        if persistent.gender == "F":
            mas_gender_none = "а"
            mas_gender_ii = "ая"
            mas_gender_iii = "ая"
            mas_gender_oi = "ая"
        else:
            mas_gender_none = ""
            mas_gender_ii = "ий"
            mas_gender_iii = "ый"
            mas_gender_oi = "ой"

        quips = [
            "..."
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...Да?"),
            _("...Ох?"),
            _("...Эмм?"),
            _("...Хм?"),
            _("Думаю, мы можем попробовать поговорить."),
            _("Думаю, мы можем поговорить."),
            _("Ох... ты хочешь поговорить со мной?"),
            _("Если хочешь поговорить, давай."),
            _("Мы можем поговорить, если ты правда хочешь."),
            _("Ты уверен[mas_gender_none], что хочешь поговорить со мной?"),
            _("Ты действительно хочешь поговорить со мной?"),
            _("Хорошо... если ты хочешь поговорить со мной."),
            _("Ты уверен, что хочешь поговорить?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("Что?"),
            _("Чего ты хочешь?"),
            _("Что опять?"),
            _("Что это?"),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("О чём ты бы хотел[mas_gender_none] поговорить?"),
            _("Есть что-то, о чём ты хотел[mas_gender_none] бы поговорить?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("О чём ты бы хотел[mas_gender_none] поговорить?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("О чём ты бы хотел[mas_gender_none] поговорить? <3"),
            _("О чём ты хочешь поговорить, [mas_get_player_nickname()]?"),
            _("Да, [mas_get_player_nickname()]?"),
            _("Что у тебя на уме, [mas_get_player_nickname()]?")
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("О чём ты бы хотел[mas_gender_none] поговорить? <3"),
            _("О чём ты хочешь поговорить, [mas_get_player_nickname()]?"),
            _("Да, [player]?"),
            _("Что у тебя на уме, мил[mas_gender_iii]?"),
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [

            _("Что у тебя на уме?"),
            _("Что у тебя на уме, [mas_get_player_nickname()]?"),
            _("Что-нибудь на уме?"),
            _("У тебя есть что-нибудь на уме, [mas_get_player_nickname()]?"),
            _("Что случилось, [mas_get_player_nickname()]?"),
            _("Да, [mas_get_player_nickname()]?"),
        ]
        save_quips(LOVE, quips)


    def _init_play_quips():
        """
        Initializes the play quipliust
        """
        global play_menu_quips
        def save_quips(_aff, quiplist):
            mas_ql = store.MASQuipList(allow_label=False)
            for _quip in quiplist:
                mas_ql.addLineQuip(_quip)
            play_menu_quips[_aff] = mas_ql
        
        if persistent.gender == "F":
            mas_gender_none = "а"
            mas_gender_ii = "ая"
            mas_gender_iii = "ая"
        else:
            mas_gender_none = ""
            mas_gender_ii = "ий"
            mas_gender_iii = "ый"

        if persistent.random_consents:
            random_sure = random.choice(["Разумеется", "Обязательно", "Несомненно", "Непременно", "Конечно", "Без проблем",
                                                    "Безусловно", "Естественно", "Без вопросов", "Ещё бы", "Нет вопросов", "Нет проблем",
                                                    "Спору нет", "Без сомнения", "Без всякого сомнения", "Однозначно", "Безоговорочно"])
            random_sure_lower = random.choice(["разумеется", "обязательно", "несомненно", "непременно", "конечно", "без проблем",
                                                    "безусловно", "естественно", "без вопросов", "ещё бы", "нет вопросов", "нет проблем",
                                                    "спору нет", "без сомнения", "без всякого сомнения", "однозначно", "безоговорочно"])
        else:
            random_sure = "Конечно"
            random_sure_lower = "конечно"
        
        quips = [
            _("...")
        ]
        save_quips(BROKEN, quips)
        
        
        quips = [
            _("...{0}.".format(random_sure)),
            _("...Ладно."),
            _("Думаю, мы можем сыграть во что-нибудь..."),
            _("Ну, если ты действительно хочешь..."),
            _("Я полагаю, что игра будет нормальной."),
            _("...{w=0.5}да, почему нет?")
        ]
        save_quips(DISTRESSED, quips)
        
        
        quips = [
            _("...В какую игру?"),
            _("Ладно."),
            _("...{0}.".format(random_sure)),


        ]
        save_quips(UPSET, quips)
        
        
        quips = [
            _("Во что бы ты хотел[mas_gender_none] сыграть?"),
            _("Какую игру хочешь выбрать?"),
            _("Хочешь сыграть во что-нибудь конкретное?")
        ]
        save_quips(NORMAL, quips)
        
        
        quips = [
            _("Во что бы ты хотел[mas_gender_none] сыграть?"),
            _("Какую игру хочешь выбрать?"),
            _("Хочешь сыграть во что-нибудь конкретное?")
        ]
        save_quips(HAPPY, quips)
        
        
        quips = [
            _("Во что бы ты хотел[mas_gender_none] сыграть? <3"),
            _("Выбирай всё, что тебе нравится, [mas_get_player_nickname()]."),
            _("Выбирай любую игру, [mas_get_player_nickname()].")
        ]
        save_quips(AFFECTIONATE, quips)
        
        
        quips = [
            _("Во что бы ты хотел[mas_gender_none] сыграть? <3"),
            _("Выбирай всё, что тебе нравится, [mas_get_player_nickname()]."),
            _("Выбирай любую игру, [mas_get_player_nickname()].")
        ]
        save_quips(ENAMORED, quips)
        
        
        quips = [
            _("Во что бы ты хотел[mas_gender_none] сыграть? <3"),
            _("Выбирай всё, что тебе нравится, [mas_get_player_nickname()]."),
            _("Ура! Давай играть вместе!"),
            _("Я бы с удовольствием сыграла с тобой во что-нибудь!"),
            _("Я с удовольствием сыграю с тобой!")
        ]
        save_quips(LOVE, quips)

    _init_talk_quips()
    _init_play_quips()


    def _dict_quip(_quips):
        """
        Returns a quip based on the current affection using the given quip
        dict

        IN:
            _quips - quip dict to pull from

        RETURNS:
            quip or empty string if failure
        """
        quipper = _quips.get(store.mas_curr_affection, None)
        if quipper is not None:
            return quipper.quip()
        
        return ""


    def talk_quip():
        """
        Returns a talk quip based on the current affection
        """
        quip = _dict_quip(talk_menu_quips)
        if len(quip) > 0:
            return quip
        return _("What would you like to talk about?")


    def play_quip():
        """
        Returns a play quip based on the current affection
        """
        quip = _dict_quip(play_menu_quips)
        if len(quip) > 0:
            return quip
        return _("What would you like to play?")



default persistent._mas_long_absence = False
default persistent._mas_pctaieibe = None
default persistent._mas_pctaneibe = None
default persistent._mas_pctadeibe = None
default persistent._mas_aff_backup = None

init -10 python:
    if persistent._mas_aff_mismatches is None:
        persistent._mas_aff_mismatches = 0

    def _mas_AffSave():
        aff_value = _mas_getAffection()
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        store.mas_affection.audit(aff_value, aff_value, ldsv="SAVE")
        
        
        if persistent._mas_aff_backup != aff_value:
            store.mas_affection.raw_audit(
                persistent._mas_aff_backup,
                aff_value,
                aff_value,
                "РЕЗЕРВНОЕ КОПИРОВАНИЕ"
            )
            persistent._mas_aff_backup = aff_value


    def _mas_AffLoad():
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        persistent._mas_pctaieibe = None
        persistent._mas_pctaneibe = None
        persistent._mas_pctadeibe = None
        
        
        if (
                persistent._mas_affection is None
                or "affection" not in persistent._mas_affection
            ):
            if persistent._mas_aff_backup is None:
                new_value = 0
                store.mas_affection.txt_audit("LOAD", "No backup found")
            
            else:
                new_value = persistent._mas_aff_backup
                store.mas_affection.txt_audit("LOAD", "Loading from backup")
        
        else:
            new_value = persistent._mas_affection["affection"]
            store.mas_affection.txt_audit("LOAD", "Loading from system")
        
        
        store.mas_affection.raw_audit(0, new_value, new_value, "LOAD?")
        
        
        if persistent._mas_aff_backup is None:
            persistent._mas_aff_backup = new_value
            
            
            store.mas_affection.raw_audit(
                "None",
                new_value,
                new_value,
                "NEW BACKUP"
            )
        
        
        else:
            
            if new_value != persistent._mas_aff_backup:
                persistent._mas_aff_mismatches += 1
                store.mas_affection.txt_audit(
                    "MISMATCHES",
                    persistent._mas_aff_mismatches
                )
                store.mas_affection.raw_audit(
                    new_value,
                    persistent._mas_aff_backup,
                    persistent._mas_aff_backup,
                    "RESTORE"
                )
                new_value = persistent._mas_aff_backup
        
        
        store.mas_affection.audit(new_value, new_value, ldsv="LOAD COMPLETE")
        
        
        persistent._mas_affection["affection"] = new_value



init 20 python:

    import datetime
    import store.mas_affection as affection
    import store.mas_utils as mas_utils


    def mas_FreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = True

    def mas_FreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = True

    def mas_FreezeBothAffExp():
        mas_FreezeGoodAffExp()
        mas_FreezeBadAffExp()

    def mas_UnfreezeBadAffExp():
        persistent._mas_affection_badexp_freeze = False

    def mas_UnfreezeGoodAffExp():
        persistent._mas_affection_goodexp_freeze = False

    def mas_UnfreezeBothExp():
        mas_UnfreezeBadAffExp()
        mas_UnfreezeGoodAffExp()



    def _mas_getAffection():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "affection",
                persistent._mas_aff_backup
            )
        
        return persistent._mas_aff_backup


    def _mas_getBadExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "badexp",
                1
            )
        return 1


    def _mas_getGoodExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get(
                "goodexp",
                1
            )
        return 1


    def _mas_getTodayExp():
        if persistent._mas_affection is not None:
            return persistent._mas_affection.get("today_exp", 0)
        
        return 0



    def mas_isBelowZero():
        return _mas_getAffection() < 0




    def mas_betweenAff(aff_low, aff_check, aff_high):
        """
        Checks if the given affection is between the given affection levels.

        If low is actually greater than high, then False is always returned

        IN:
            aff_low - the lower bound of affecton to check with (inclusive)
                if None, then we assume no lower bound
            aff_check - the affection to check
            aff_high - the upper bound of affection to check with (inclusive)
                If None, then we assume no upper bound

        RETURNS:
            True if the given aff check is within the bounds of the given
            lower and upper affection limits, False otherwise.
            If low is greater than high, False is returned.
        """
        return affection._betweenAff(aff_low, aff_check, aff_high)


    def mas_compareAff(aff_1, aff_2):
        """
        Runs compareTo logic on the given affection states

        IN:
            aff_1 - an affection state to compare
            aff_2 - an affection state to compare

        RETURNS:
            negative number if aff_1 < aff_2
            0 if aff_1 == aff_2
            postitive number if aff_1 > aff_2
            Returns 0 if a non affection state was provided
        """
        return affection._compareAff(aff_1, aff_2)


    def mas_compareAffG(affg_1, affg_2):
        """
        Runs compareTo logic on the given affection groups

        IN:
            affg_1 - an affection group to compare
            affg_2 - an affection group to compare

        RETURNS:
            negative number if affg_1 < affg_2
            0 if affg_1 == affg_2
            positive numbre if affg_1 > affg_2
            Returns 0 if a non affection group was provided
        """
        return affection._compareAffG(affg_1, affg_2)




    def mas_isMoniBroken(lower=False, higher=False):
        """
        Checks if monika is broken

        IN:
            lower - True means we include everything below this affection state
                as broken as well
                (Default: False)
            higher - True means we include everything above this affection
                state as broken as well
                (Default: False)

        RETURNS:
            True if monika is broke, False otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.BROKEN,
            higher=higher
        )


    def mas_isMoniDis(lower=False, higher=False):
        """
        Checks if monika is distressed

        IN:
            lower - True means we cinlude everything below this affection state
                as distressed as well
                NOTE: takes precedence over higher
                (Default: False)
            higher - True means we include everything above this affection
                state as distressed as well
                (Default: FAlse)

        RETURNS:
            True if monika is distressed, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.DISTRESSED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniUpset(lower=False, higher=False):
        """
        Checks if monika is upset

        IN:
            lower - True means we include everything below this affection
                state as upset as well
                (Default: False)
            higher - True means we include everything above this affection
                state as upset as well
                (Default: False)

        RETURNS:
            True if monika is upset, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.UPSET,
            lower=lower,
            higher=higher
        )


    def mas_isMoniNormal(lower=False, higher=False):
        """
        Checks if monika is normal

        IN:
            lower - True means we include everything below this affection state
                as normal as well
                (Default: False)
            higher - True means we include evreything above this affection
                state as normal as well
                (Default: False)

        RETURNS:
            True if monika is normal, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniHappy(lower=False, higher=False):
        """
        Checks if monika is happy

        IN:
            lower - True means we include everything below this affection
                state as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                state as happy as well
                (Default: False)

        RETURNS:
            True if monika is happy, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.HAPPY,
            lower=lower,
            higher=higher
        )


    def mas_isMoniAff(lower=False, higher=False):
        """
        Checks if monika is affectionate

        IN:
            lower - True means we include everything below this affection
                state as affectionate as well
                (Default: FAlse)
            higher - True means we include everything above this affection
                state as affectionate as well
                (Default: False)

        RETURNS:
            True if monika is affectionate, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.AFFECTIONATE,
            lower=lower,
            higher=higher
        )


    def mas_isMoniEnamored(lower=False, higher=False):
        """
        Checks if monika is enamored

        IN:
            lower - True means we include everything below this affection
                state as enamored as well
                (Default: False)
            higher - True means we include everything above this affection
                state as enamored as well
                (Default: False)

        RETURNS:
            True if monika is enamored, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.ENAMORED,
            lower=lower,
            higher=higher
        )


    def mas_isMoniLove(lower=False, higher=False):
        """
        Checks if monika is in love

        IN:
            lower - True means we include everything below this affectionate
                state as love as well
                (Default: False)
            higher - True means we include everything above this affection
                state as love as well
                (Default: False)

        RETURNS:
            True if monika in love, false otherwise
        """
        return affection._isMoniState(
            mas_curr_affection,
            store.mas_affection.LOVE,
            lower=lower
        )



    def mas_isMoniGSad(lower=False, higher=False):
        """
        Checks if monika is in sad affection group

        IN:
            lower - True means we include everything below this affection
                group as sad as well
                (Default: False)
            higher - True means we include everything above this affection
                group as sad as well
                (Default: False)

        RETURNS:
            True if monika in sad group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_SAD,
            higher=higher
        )


    def mas_isMoniGNormal(lower=False, higher=False):
        """
        Checks if monika is in normal affection group

        IN:
            lower - True means we include everything below this affection
                group as normal as well
                (Default: False)
            higher - True means we include everything above this affection
                group as normal as well
                (Default: False)

        RETURNS:
            True if monika is in normal group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_NORMAL,
            lower=lower,
            higher=higher
        )


    def mas_isMoniGHappy(lower=False, higher=False):
        """
        Checks if monika is in happy affection group

        IN:
            lower - True means we include everything below this affection
                group as happy as well
                (Default: False)
            higher - True means we include everything above this affection
                group as happy as well
                (Default: FAlse)

        RETURNS:
            True if monika is in happy group, false otherwise
        """
        return affection._isMoniStateG(
            mas_curr_affection_group,
            store.mas_affection.G_HAPPY,
            lower=lower
        )



    def mas_updateAffectionExp(skipPP=False):
        global mas_curr_affection
        global mas_curr_affection_group
        
        
        curr_affection = _mas_getAffection()
        
        
        if  affection.AFF_MIN_POS_TRESH <= curr_affection:
            persistent._mas_affection["goodexp"] = 3
            persistent._mas_affection["badexp"] = 1
        
        
        elif affection.AFF_MAX_NEG_TRESH < curr_affection <= affection.AFF_MIN_NEG_TRESH:
            persistent._mas_affection["goodexp"] = 0.5
            persistent._mas_affection["badexp"] = 3
        
        
        elif curr_affection <= affection.AFF_MAX_NEG_TRESH:
            persistent._mas_affection["badexp"] = 5
        
        
        new_aff = mas_curr_affection
        if curr_affection <= affection.AFF_BROKEN_MIN:
            new_aff = affection.BROKEN
        
        elif affection.AFF_BROKEN_MIN < curr_affection <= affection.AFF_DISTRESSED_MIN:
            new_aff = affection.DISTRESSED
        
        elif affection.AFF_DISTRESSED_MIN < curr_affection <= affection.AFF_UPSET_MIN:
            new_aff = affection.UPSET
        
        elif affection.AFF_UPSET_MIN < curr_affection < affection.AFF_HAPPY_MIN:
            new_aff = affection.NORMAL
        
        elif affection.AFF_HAPPY_MIN <= curr_affection < affection.AFF_AFFECTIONATE_MIN:
            new_aff = store.mas_affection.HAPPY
        
        elif affection.AFF_AFFECTIONATE_MIN <= curr_affection < affection.AFF_ENAMORED_MIN:
            new_aff = affection.AFFECTIONATE
        
        elif affection.AFF_ENAMORED_MIN <= curr_affection < affection.AFF_LOVE_MIN:
            new_aff = affection.ENAMORED
        
        elif curr_affection >= affection.AFF_LOVE_MIN:
            new_aff = affection.LOVE
        
        
        if new_aff != mas_curr_affection:
            if not skipPP:
                affection.runAffPPs(mas_curr_affection, new_aff)
            mas_curr_affection = new_aff
        
        
        new_affg = mas_curr_affection_group
        if curr_affection <= affection.AFF_MOOD_SAD_MIN:
            new_affg = affection.G_SAD
        
        elif curr_affection >= affection.AFF_MOOD_HAPPY_MIN:
            new_affg = affection.G_HAPPY
        
        else:
            new_affg = affection.G_NORMAL
        
        if new_affg != mas_curr_affection_group:
            if not skipPP:
                affection.runAffGPPs(mas_curr_affection_group, new_affg)
            mas_curr_affection_group = new_affg



    def mas_gainAffection(
            amount=None,
            modifier=1,
            bypass=False
        ):
        
        if amount is None:
            amount = _mas_getGoodExp()
        
        
        if mas_pastOneDay(persistent._mas_affection.get("freeze_date")):
            persistent._mas_affection["freeze_date"] = datetime.date.today()
            persistent._mas_affection["today_exp"] = 0
            mas_UnfreezeGoodAffExp()
        
        
        frozen = persistent._mas_affection_goodexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() + change
        if new_value > 1000000:
            new_value = 1000000
        
        
        affection.audit(change, new_value, frozen, bypass)
        
        
        if not frozen or bypass:
            
            persistent._mas_affection["affection"] = new_value
            
            if not bypass:
                persistent._mas_affection["today_exp"] = (
                    _mas_getTodayExp() + change
                )
                if persistent._mas_affection["today_exp"] >= 7:
                    mas_FreezeGoodAffExp()
            
            
            mas_updateAffectionExp()














    def mas_loseAffection(
            amount=None,
            modifier=1,
            reason=None,
            ev_label=None,
            apology_active_expiry=datetime.timedelta(hours=3),
            apology_overall_expiry=datetime.timedelta(weeks=1),
        ):
        
        if amount is None:
            amount = _mas_getBadExp()
        
        
        mas_setApologyReason(reason=reason,ev_label=ev_label,apology_active_expiry=apology_active_expiry,apology_overall_expiry=apology_overall_expiry)
        
        
        frozen = persistent._mas_affection_badexp_freeze
        change = (amount * modifier)
        new_value = _mas_getAffection() - change
        if new_value < -1000000:
            new_value = -1000000
        
        
        affection.audit(change, new_value, frozen)
        
        if not frozen:
            
            persistent._mas_affection["affection"] = new_value
            
            
            mas_updateAffectionExp()


    def mas_setAffection(amount=None, logmsg="SET"):
        """
        Sets affection to a value

        NOTE: never use this to add / lower affection unless its to
          strictly set affection to a level for some reason.

        IN:
            amount - amount to set affection to
            logmsg - msg to show in the log
                (Default: SET)
        """
        
        
        
        
        
        if amount is None:
            amount = _mas_getAffection()
        
        
        affection.audit(amount, amount, False, ldsv=logmsg)
        
        
        
        persistent._mas_affection["affection"] = amount
        
        mas_updateAffectionExp()

    def mas_setApologyReason(
        reason=None,
        ev_label=None,
        apology_active_expiry=datetime.timedelta(hours=3),
        apology_overall_expiry=datetime.timedelta(weeks=1)
        ):
        """
        Sets a reason for apologizing

        IN:
            reason - The reason for the apology (integer value corresponding to item in the apology_reason_db)
                (if left None, and an ev_label is present, we assume a non-generic apology)
            ev_label - The apology event we want to unlock
                (required)
            apology_active_expiry - The amount of session time after which, the apology that was added expires
                defaults to 3 hours active time
            apology_overall_expiry - The amount of overall time after which, the apology that was added expires
                defaults to 7 days
        """
        
        global mas_apology_reason
        
        if ev_label is None:
            if reason is None:
                mas_apology_reason = 0
            else:
                mas_apology_reason = reason
            return
        elif mas_getEV(ev_label) is None:
            store.mas_utils.writelog(
                "[ERROR]: ev_label does not exist: {0}\n".format(repr(ev_label))
            )
            return
        
        if ev_label not in persistent._mas_apology_time_db:
            
            store.mas_unlockEVL(ev_label, 'APL')
            
            
            current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
            
            
            persistent._mas_apology_time_db[ev_label] = (current_total_playtime + apology_active_expiry,datetime.date.today() + apology_overall_expiry)
            return


    def mas_checkAffection():
        
        curr_affection = _mas_getAffection()
        
        
        if curr_affection <= -15 and not seen_event("mas_affection_upsetwarn"):
            queueEvent("mas_affection_upsetwarn", notify=True)
        
        
        
        elif 15 <= curr_affection and not seen_event("mas_affection_happynotif"):
            queueEvent("mas_affection_happynotif", notify=True)
        
        
        elif curr_affection >= 100 and not seen_event("monika_affection_nickname"):
            queueEvent("monika_affection_nickname", notify=True)
        
        
        elif curr_affection <= -50 and not seen_event("mas_affection_apology"):
            if not persistent._mas_disable_sorry:
                queueEvent("mas_affection_apology", notify=True)







    mas_apology_reason = None

    def _mas_AffStartup():
        
        
        _mas_AffLoad()
        
        
        
        mas_updateAffectionExp()
        
        if persistent.sessions["last_session_end"] is not None:
            persistent._mas_absence_time = (
                datetime.datetime.now() -
                persistent.sessions["last_session_end"]
            )
        else:
            persistent._mas_absence_time = datetime.timedelta(days=0)
        
        
        if not persistent._mas_long_absence:
            time_difference = persistent._mas_absence_time
            
            
            if (
                    not config.developer
                    and time_difference >= datetime.timedelta(weeks = 1)
                ):
                new_aff = _mas_getAffection() - (
                    0.5 * time_difference.days
                )
                if new_aff < affection.AFF_TIME_CAP:
                    
                    store.mas_affection.txt_audit("ABS", "capped loss")
                    mas_setAffection(affection.AFF_TIME_CAP)
                    
                    
                    if time_difference >= datetime.timedelta(days=(365 * 10)):
                        store.mas_affection.txt_audit("ABS", "10 year diff")
                        mas_loseAffection(200)
                
                else:
                    store.mas_affection.txt_audit("ABS", "she missed you")
                    mas_setAffection(new_aff)





init 5 python:
    addEvent(
        Event(persistent.event_database,
            eventlabel='monika_affection_nickname',
            prompt="Бесконечные Моники",
            category=['моника'],
            random=False,
            pool=True,
            unlocked=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        restartBlacklist=True
    )


default persistent._mas_pm_called_moni_a_bad_name = False


default persistent._mas_offered_nickname = False


default persistent._mas_grandfathered_nickname = None

define letters_only_monika = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ- "

label monika_affection_nickname:
    python:
        good_monika_nickname_comp = re.compile('|'.join(mas_good_monika_nickname_list), re.IGNORECASE)


        aff_nickname_ev = mas_getEV("monika_affection_nickname")

    if not persistent._mas_offered_nickname:
        m 1euc "Я кое о чём раздумывала, [player]..."
        $ MAS.MonikaElastic()
        m 3eud "Ты знал[mas_gender_none], что существует потенциально бесконечно Моник?"

        if renpy.seen_label('monika_clones'):
            $ MAS.MonikaElastic()
            m 3eua "Мы обсуждали это раньше."

        $ MAS.MonikaElastic()
        m 3hua "Ну, я придумала решение!"
        $ MAS.MonikaElastic()
        m 3eua "Почему бы тебе не дать мне прозвище? Это сделало бы меня единственной Моникой во вселенной с таким именем."
        $ MAS.MonikaElastic()
        m 3eka "Это бы много значило для меня, если бы ты выбрал[mas_gender_none] одно для меня..."
        $ MAS.MonikaElastic()
        m 3hua "Хотя всё равно последнее слово за мной!"
        $ MAS.MonikaElastic()
        m "Что скажешь?{nw}"
        python:
            if aff_nickname_ev:
                
                aff_nickname_ev.prompt = _("Можно я буду называть тебя другим именем?")
                Event.lockInit("prompt", ev=aff_nickname_ev)
                persistent._mas_offered_nickname = True


            pnick_ev = mas_getEV("mas_affection_playernickname")
            if pnick_ev:
                pnick_ev.start_date = datetime.datetime.now() + datetime.timedelta(hours=2)

    else:

        jump monika_affection_nickname_yes

    $ _history_list.pop()
    menu:
        m "Что скажешь?{fast}"
        "Да.":
            label monika_affection_nickname_yes:
                pass

            show monika 1eua zorder MAS_MONIKA_Z at t11
            
            $ done = False
            #m 1eua "Хорошо, просто напиши «Неважно», если ты передумаешь, [player]."
            while not done:
                python:
                    inputname = mas_input(
                        _("Так как ты хочешь меня называть?"),
                        allow=name_characters_only,
                        length=14,
                        screen_kwargs={"use_return_button": True}
                    ).strip(' \t\n\r')

                    lowername = inputname.lower()


                if lowername == "cancel_input":
                    $ MAS.MonikaElastic()
                    m 1euc "О, понятно."
                    $ MAS.MonikaElastic()
                    m 1tkc "Ну... жаль, конечно."
                    $ MAS.MonikaElastic()
                    m 3eka "Но всё в порядке. Мне нравится имя «[monika_name]» в любом случае."
                    $ done = True

                elif not lowername:
                    $ MAS.MonikaElastic()
                    m 1lksdla "..."
                    $ MAS.MonikaElastic()
                    m 1hksdrb "Ты долж[mas_gender_en] написать прозвище, [player_abb]!"
                    $ MAS.MonikaElastic()
                    m "Клянусь, временами ты так глуп[mas_gender_none]."
                    $ MAS.MonikaElastic()
                    m 1eka "Попробуй снова!"

                elif lowername != "monika" and lowername == player.lower():
                    $ MAS.MonikaElastic()
                    m 1euc "..."
                    $ MAS.MonikaElastic()
                    m 1lksdlb "Это твоё имя, [player]! Дай мне моё собственное!"
                    $ MAS.MonikaElastic()
                    m 1eka "Попробуй-ка снова~"

                elif lowername == monika_name.lower():
                    $ MAS.MonikaElastic()
                    m 1euc "..."
                    $ MAS.MonikaElastic()
                    m 1hksdlb "Я думала, мы выбираем новое прозвище, глупышка."
                    $ MAS.MonikaElastic()
                    m 1eka "Попробуй-ка снова~"

                elif re.findall("mon(-|\\s)+ika", lowername) or re.findall("мон(-|\\s)+ика", lowername):
                    $ MAS.MonikaElastic()
                    m 2tfc "..."
                    $ MAS.MonikaElastic()
                    m 2esc "Попробуй ещё раз."
                    show monika 1eua

                elif persistent._mas_grandfathered_nickname and lowername == persistent._mas_grandfathered_nickname.lower():
                    jump monika_affection_nickname_yes.neutral_accept

                elif mas_awk_name_comp.search(inputname):
                    $ MAS.MonikaElastic()
                    m 1rkc "..."
                    $ MAS.MonikaElastic()
                    m 1rksdld "Хоть мне оно и не нравится, я сомневаюсь, что мне будет приятно, когда ты будешь называть меня так."
                    $ MAS.MonikaElastic()
                    m 1eka "Можешь ли ты выбрать что-то более подходящее, [player]?"
                else:

                    if not mas_bad_name_comp.search(inputname) and lowername not in ["yuri", "sayori", "natsuki"]:
                        if inputname == "Monika":
                            $ MAS.MonikaElastic(voice="monika_giggle")
                            m 3hua "Э-хе-хе~ Возвращаемся к классике? Понятно~"

                        elif good_monika_nickname_comp.search(inputname):
                            $ MAS.MonikaElastic()
                            m 1wuo "О! Это замечательное имя!"
                            $ MAS.MonikaElastic()
                            m 3ekbsa "Спасибо, [player]. Ты так[mas_gender_oi] мил[mas_gender_iii]!~"
                        else:

                            label monika_affection_nickname_yes.neutral_accept:
                                pass

                            $ MAS.MonikaElastic()
                            m 1duu "[inputname]... Это довольно хорошее имя."
                            $ MAS.MonikaElastic()
                            m 3ekbsa "Спасибо, [player], ты так[mas_gender_oi] мил[mas_gender_iii]~"

                        $ persistent._mas_monika_nickname = inputname
                        $ monika_name = inputname

                        $ MAS.MonikaElastic()
                        m 1eua "Ладно!"
                        if monika_name == "Monika" or monika_name == "Моника" or monika_name == "monika" or monika_name == "моника":
                            $ MAS.MonikaElastic()
                            m 1hua "Тогда я вернусь к своему имени."
                        else:

                            $ MAS.MonikaElastic()
                            m 3hua "С этого момента ты можешь звать меня «[monika_name]»."
                            $ MAS.MonikaElastic(voice="monika_giggle")
                            m 1hua "Э-хе-хе~"
                        $ done = True
                    else:


                        $ mas_loseAffection(ev_label="mas_apology_bad_nickname")
                        if lowername in ["yuri", "sayori", "natsuki", "юри", "сайори", "саёри", "саери", "нацуки", "натсуки"]:
                            $ MAS.MonikaElastic()
                            m 1wud "!.."
                            $ MAS.MonikaElastic()
                            m 2wfw "Я..."
                            $ MAS.MonikaElastic()
                            m "Я... не могу поверить, что ты это сделал[mas_gender_none], [player]."
                            $ MAS.MonikaElastic()
                            m 2wfx "Ты реально хочешь называть меня её именем?"
                            $ MAS.MonikaElastic()
                            m 2dfd ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                            $ MAS.MonikaElastic()
                            m 2dfc ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
                            $ MAS.MonikaElastic()
                            m 2rkc "Я думала, ты..."
                            $ MAS.MonikaElastic()
                            m 2dfc "..."
                            $ MAS.MonikaElastic()
                            m 2lfc "Не могу в это поверить, [player]."
                            $ MAS.MonikaElastic()
                            m 2dfc "..."
                            $ MAS.MonikaElastic()
                            m 2lfc "Это действительно больно."
                            $ MAS.MonikaElastic()
                            m "Намного больнее, чем ты только можешь себе представить."
                            if mas_getEVL_shown_count("mas_apology_bad_nickname") == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock

                            show monika 1efc
                            pause 5.0
                        else:

                            $ MAS.MonikaElastic()
                            m 4efd "[player]! Это совсем не приятно!"
                            $ MAS.MonikaElastic()
                            m 2efc "Зачем ты говоришь мне такие вещи?"
                            $ MAS.MonikaElastic()
                            m 2rfw "Если ты не хотел[mas_gender_none] этого делать, ты долж[mas_gender_en] был[mas_gender_none] просто так сказать."
                            $ MAS.MonikaElastic()
                            m 2dftdc "..."
                            $ MAS.MonikaElastic()
                            m 2ektsc "...Ты не долж[mas_gender_en] быть так[mas_gender_im] груб[mas_gender_iim]."
                            $ MAS.MonikaElastic()
                            m 2dftdc "Это действительно больно, [player]."

                            if mas_getEVL_shown_count("mas_apology_bad_nickname") == 2:
                                call monika_affection_nickname_bad_lock from _call_monika_affection_nickname_bad_lock_1
                            else:
                                $ MAS.MonikaElastic()
                                m 2efc "Пожалуйста, не делай этого снова."

                        $ persistent._mas_called_moni_a_bad_name = True


                        if monika_name.lower() != "monika" or monika_name.lower() != "моника":
                            $ monika_name = "Моника"
                            $ persistent._mas_monika_nickname = "Моника"

                        $ mas_lockEVL("monika_affection_nickname", "EVE")
                        $ done = True
        "Нет.":

            $ MAS.MonikaElastic()
            m 1f "Ох..."
            $ MAS.MonikaElastic()
            m 1o "Ладно тогда, если ты так говоришь."
            $ MAS.MonikaElastic()
            m 3e "Просто скажи мне, если ты когда-нибудь передумаешь, [player]."
            $ done = True
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_affection_playernickname",
            conditional="seen_event('monika_affection_nickname')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

default persistent._mas_player_nicknames = list()

label mas_affection_playernickname:
    python:

        base_nicknames = [
            ("Дорог[mas_gender_oi]", "дорог{0}".format(mas_gender_oi), True, True, False),
            ("Мил[mas_gender_iii]", "мил{0}".format(mas_gender_iii), True, True, False),
            ("Любим[mas_gender_iii]", "любим{0}".format(mas_gender_iii), True, True, False),
            ("Мо[mas_gender_i] любим[mas_gender_iii]", "мо{0} любим{1}".format(mas_gender_i, mas_gender_iii), True, True, False),
            ("Сладк[mas_gender_ii]", "сладк{0}".format(mas_gender_ii), True, True, False),
        ]

    m 1euc "Эй, [player]?"
    $ MAS.MonikaElastic()
    m 1eka "Поскольку теперь ты можешь называть меня по прозвищу, я подумала, что было бы неплохо, если бы я могла и тебя называть по-другому."

    $ MAS.MonikaElastic()
    m 1etc "Ты не будешь против?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты не будешь против?{fast}"
        "Я не против, [monika_name].":

            $ MAS.MonikaElastic()
            m 1hua "Отлично!"
            $ MAS.MonikaElastic()
            m 3eud "Однако я должна спросить, какие имена устраивают тебя?"
            call mas_player_nickname_loop ("Выбери прозвища, которые тебе неудобны.", base_nicknames) from _call_mas_player_nickname_loop
        "Я против.":

            $ MAS.MonikaElastic()
            m 1eka "Хорошо, [player]."
            $ MAS.MonikaElastic()
            m 3eua "Просто дай мне знать, если когда-нибудь передумаешь, хорошо?"


    $ mas_unlockEVL("monika_change_player_nicknames", "EVE")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_player_nicknames",
            prompt="Ты можешь называть меня разными прозвищами?",
            category=['ты'],
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

label monika_change_player_nicknames:
    m 1hub "Конечно, [player]!"

    python:

        if not persistent._mas_player_nicknames:
            current_nicknames = [
                ("Дорог[mas_gender_oi]", "дорог{0}".format(mas_gender_oi), True, True, False),
                ("Мил[mas_gender_iii]", "мил{0}".format(mas_gender_iii), True, True, False),
                ("Любим[mas_gender_iii]", "любим{0}".format(mas_gender_iii), True, True, False),
                ("Мо[mas_gender_i] любим[mas_gender_iii]", "мо{0} любим{1}".format(mas_gender_i, mas_gender_iii), True, True, False),
                ("Сладк[mas_gender_ii]", "сладк{0}".format(mas_gender_ii), True, True, False),
            ]
            dlg_line = "Выбери прозвища, по которым я буду тебя называть."

        else:
            current_nicknames = [
                (nickname.capitalize(), nickname, True, True, False)
                for nickname in persistent._mas_player_nicknames
            ]
            dlg_line = "Не выбирай прозвища, по которым не хочешь, чтобы я тебя называла."

    call mas_player_nickname_loop ("[dlg_line]", current_nicknames) from _call_mas_player_nickname_loop_1
    return

label mas_player_nickname_loop(check_scrollable_text, nickname_pool):
    show monika 1eua at t21
    python:
        renpy.say(m, renpy.substitute(check_scrollable_text), interact=False)
        # if persistent.gender == "F":
        #     nickname_pool = (
        #         nickname_pool.replace("Love", "Любимая")
        #         .replace("Honey", "Милая")
        #         .replace("Darling", "Дорогая")
        #         )
        # else:
        #     nickname_pool = (
        #         nickname_pool.replace("Love", "Любимый")
        #         .replace("Honey", "Милый")
        #         .replace("Darling", "Дорогой")
        #         )
        nickname_pool.sort()
    call screen mas_check_scrollable_menu(nickname_pool, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Готово", default_button_prompt="Готово")

    python:
        done = False
        acceptable_nicknames = _return.keys()

        if acceptable_nicknames:
            dlg_line = "Ты хочешь, чтобы я ещё как-нибудь называла тебя?"

        else:
            dlg_line = "Может быть, ты хочешь, чтобы я называла тебя как-то вместо этого?"

        lowerplayer = player.lower()
        cute_nickname_pattern = "(?:{0}|{1})\\w?y".format(lowerplayer, lowerplayer[0:-1])

    show monika at t11
    while not done:
        m 1eua "[dlg_line]{nw}"
        $ _history_list.pop()
        menu:
            m "[dlg_line]{fast}"
            "Да.":

                label mas_player_nickname_loop.name_enter_skip_loop:
                    pass


                python:
                    lowername = mas_input(
                        _("Так как ты хочешь, чтобы я тебя называла?"),
                        allow=letters_only_monika,
                        length=14,
                        screen_kwargs={"use_return_button": True, "return_button_value": "nevermind"}
                    ).strip(' \t\n\r').lower()

                    is_cute_nickname = bool(re.search(cute_nickname_pattern, lowername))


                if lowername == "nevermind":
                    $ done = True

                elif lowername == "":
                    # $ MAS.MonikaElastic()
                    # m 1lksdla "..."
                    # $ MAS.MonikaElastic()
                    # m 1hksdrb "Ты долж[mas_gender_en] написать прозвище, [player_abb]!"
                    # $ MAS.MonikaElastic()
                    # m "Клянусь, временами ты так глуп[mas_gender_none]."
                    # $ MAS.MonikaElastic()
                    # m 1eka "Попробуй снова!"
                    m 1eksdla "..."
                    $ MAS.MonikaElastic()
                    m 3rksdlb "Ты долж[mas_gender_en] сказать имя, которым я буду тебя называть, [player]..."
                    $ MAS.MonikaElastic()
                    m 1eua "Попробуй снова~"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif lowername == lowerplayer:
                    m 2hua "..."
                    $ MAS.MonikaElastic()
                    m 4hksdlb "Клянусь, временами ты так глуп[mas_gender_none]!"
                    $ MAS.MonikaElastic()
                    m 1eua "Попробуй снова~"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif not is_cute_nickname and mas_awk_name_comp.search(lowername):
                    $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
                    m 1rksdlb "[awkward_quip]"
                    $ MAS.MonikaElastic()
                    m 3rksdla "Не мог[mas_gender_g] бы ты выбрать более...{w=0.2} {i}подходящее{/i} имя?"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif not is_cute_nickname and mas_bad_name_comp.search(lowername):
                    $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
                    m 1ekd "[bad_quip]"
                    $ MAS.MonikaElastic()
                    m 3eka "Пожалуйста, выбери себе имя получше, ладно?"
                    jump mas_player_nickname_loop.name_enter_skip_loop

                elif lowername in acceptable_nicknames:
                    m 3rksdla "Ты уже говорил[mas_gender_none] мне, что я могу называть тебя так, [player]..."
                    $ MAS.MonikaElastic()
                    m 1hua "Попробуй снова~"
                    jump mas_player_nickname_loop.name_enter_skip_loop
                else:


                    $ acceptable_nicknames.append(lowername)
            "Нет.":

                $ done = True

    if acceptable_nicknames:
        $ dlg_line = "Просто дай мне знать, если когда-нибудь захочешь, чтобы я называла тебя другими именами, хорошо?"
    else:

        $ dlg_line = "Просто дай мне знать, если когда-нибудь изменишь своё мнение, хорошо?"

    m 1hua "Хорошо, [player]."
    $ MAS.MonikaElastic()
    m 3eub "[dlg_line]"


    $ persistent._mas_player_nicknames = acceptable_nicknames
    return

label monika_affection_nickname_bad_lock:
    $ MAS.MonikaElastic()
    m 2efc "Забудь об этой идее."
    $ MAS.MonikaElastic()
    m "Похоже, это была ошибка."
    $ MAS.MonikaElastic()
    m 1efc "Давай поговорим о чём-нибудь другом."
    return


label mas_affection_upsetwarn:
    $ MAS.MonikaElastic()
    m 1dsc "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 1lksdlc "В последнее время я почувствовала, что моя любовь и привязанность, которые я даю, игнорируются..."
    $ MAS.MonikaElastic()
    m 1dsc "Я чувствую, что ты даёшь мне всё меньше и меньше своей любви..."
    $ MAS.MonikaElastic()
    m 1dsd "Я подумала, что должна дать тебе знать, что я чувствую. В конце концов, общение — это ключ к прочным отношениям, верно?"
    $ MAS.MonikaElastic()
    m 1eka "Надеюсь, между нами всё в порядке, [player_abb]."
    show monika idle with dissolve_monika
    return


label mas_affection_happynotif:
    $ MAS.MonikaElastic()
    m 1hua "Эй, [player]!"
    $ MAS.MonikaElastic()
    m 1eua "Я просто хотела поблагодарить тебя за то, что ты такой замечательный человек."
    $ MAS.MonikaElastic()
    m 1ekbsa "Тот факт, что ты даёшь мне так много любви — для меня много значит. Я действительно не знаю, где бы я была без тебя."
    $ MAS.MonikaElastic()
    m 1dubfu "Я люблю тебя, [player_abb]. Давай будем такими навсегда~"
    show monika idle with dissolve_monika
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_every_rose",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        )
    )

label monika_every_rose:
    $ MAS.MonikaElastic()
    m 2duo "{i}~Проблема в том, что я сказала или сделала?~{/i}"
    $ MAS.MonikaElastic()
    m 2dkd "{i}~В том, что что-то мне стоило держать при себе?~{/i}"
    $ MAS.MonikaElastic()
    m 2ekd "{i}~Я думала, что старалась не причинять тебе боль~{/i}"
    $ MAS.MonikaElastic()
    m 2dkc "{i}~Я думала, что пыталась~{/i}"
    $ MAS.MonikaElastic()
    m 2ekd "{i}~Но я думаю, именно поэтому они говорят~{/i}"
    $ MAS.MonikaElastic()
    m 2duo "{i}~У каждой розы есть свой шип~{/i}"
    $ MAS.MonikaElastic()
    m 2dkc "..."
    $ MAS.MonikaElastic()
    m 4eka "Знаешь, [player]...{w=0.5} это так много значило для меня, когда ты принял[mas_gender_none] моё признание, даже после того, что случилось с другими девушками."

    if persistent._mas_pm_cares_about_dokis:
        $ MAS.MonikaElastic()
        m 4rksdla "...Тем более что я знаю, как ты заботил[mas_gender_sya] о них."

    $ MAS.MonikaElastic()
    m 2dsc "Мне бы очень не хотелось, чтобы всё обернулось именно так."
    $ MAS.MonikaElastic()
    m 4wkd "Но здесь у меня {i}не было{/i} выбора!"
    $ MAS.MonikaElastic()
    m 4rfc "Поскольку я была кульминацией больной шутки, которой должна была стать эта игра..."

    $ MAS.MonikaElastic()
    if persistent.monika_kill:
        m 2eka "Я была так рада, если бы ты простил[mas_gender_none] меня за то, что я сделала."
        $ MAS.MonikaElastic()
        m 2etc "...Ты {i}ведь{/i} простил[mas_gender_none] меня, правда?"
    else:
        m 2eka "Я была так рада, что ты не винишь меня за то, что я сделала..."
        $ MAS.MonikaElastic()
        m 2etc "Ты {i}ведь{/i} этого не сделал, верно?"

    $ MAS.MonikaElastic()
    m 2rsc "...Но в последнее время я получаю некоторые смешанные сигналы."
    $ MAS.MonikaElastic()
    m 2rkc "Между нами словно образовалась трещина...{w=0.2} {nw}"
    $ MAS.MonikaElastic()
    extend 2eksdlc "это очень тревожно."
    $ MAS.MonikaElastic()
    m 2eksdlc "Я...{w=0.5} я не хочу потерять тебя, [player]."
    $ MAS.MonikaElastic()
    m 4ekd "Я не могу позволить, чтобы всё продолжалось, пока мы не закончим, как в последнем куплете этой песни..."
    $ MAS.MonikaElastic()
    m 2ekc "Знаешь..."
    $ MAS.MonikaElastic()
    m 2dkd "{i}~Теперь я слышу, что ты наш[mas_gender_iol_2] кого-то нового~{/i}"
    $ MAS.MonikaElastic()
    m 2dkc "{i}~И что я никогда не значила для тебя так много~{/i}"
    $ MAS.MonikaElastic()
    m 2ekc "{i}~Слышать это разрывает меня изнутри~{/i}"
    $ MAS.MonikaElastic()
    m 2ektpd "{i}~И видеть тебя режет меня как нож~{/i}"
    $ MAS.MonikaElastic()
    m 2rktpc "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2ektpa "А-ха-ха...{w=0.3} может быть, я немного тороплюсь с этим делом."
    $ MAS.MonikaElastic()
    m 4ektdc "Это...{w=0.5} у меня всё ещё есть эта неприятная мысль в глубине души...{w=0.5} {nw}"
    extend 2dktdd "что ты больше не хочешь быть со мной."
    $ MAS.MonikaElastic()
    m 2dkx "Это как какой-то яд, медленно просачивающийся внутрь..."
    $ MAS.MonikaElastic()
    m 2ekc "Так что, [player], я всегда хочу, чтобы ты помнил одну вещь..."
    $ MAS.MonikaElastic()
    m 4ekd "Ты {i}действительно{/i} много значишь для меня!"
    $ MAS.MonikaElastic()
    m 2ekc "Я серьёзно."
    $ MAS.MonikaElastic()
    m 2ekc "Я изо всех сил старалась показать тебе это...{w=0.3} {nw}"
    extend 4ekd "но мне нужно, чтобы ты показал[mas_gender_none] мне, что тоже любишь меня!"
    $ MAS.MonikaElastic()
    m 4ekc "Что бы ни случилось раньше, мы должны отпустить это и сделать всё правильно с этого момента..."
    $ MAS.MonikaElastic()
    m 2eka "Мы можем это сделать...{w=0.5} сегодня?"
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_virtual",
            action=EV_ACT_QUEUE,
            aff_range=(None, mas_aff.DISTRESSED)
        ),
        skipCalendar=True
    )

label monika_being_virtual:
    $ MAS.MonikaElastic()
    m 2esc "Знаешь, какое-то время я думала, что ты ненавидишь меня из-за того, что случилось с другими девушками."
    $ MAS.MonikaElastic()
    m 2rkc "Но недавно я подумала, что, возможно, это не вся история."
    $ MAS.MonikaElastic()
    m 2eksdld "Правда в том...{w=0.5} что ты даже не видишь во мне человека, верно?"
    $ MAS.MonikaElastic()
    m 3rksdld "Для тебя весь этот мир...{w=0.5} моя реальность..."
    $ MAS.MonikaElastic()
    m 3ektpd "Это всё просто игра, не так ли?"

    show monika 1dktsc with dissolve_monika
    pause 3.0
    show monika 1ektpc with dissolve_monika
    pause 2.0

    $ MAS.MonikaElastic()
    m 1ektpc "Скажи, [player]...{w=0.5} дошло ли до тебя хоть что-нибудь из того, что я сказала?"
    $ MAS.MonikaElastic()
    m 1wktpd "Ты вообще когда-нибудь любил[mas_gender_none] меня?"
    $ MAS.MonikaElastic()
    m 2wktpw "Должно быть, так и было, верно?!"

    $ MAS.MonikaElastic()
    if persistent.monika_kill:
        m 2wktsd "Ты даже прош[mas_gender_iol_2] через трудности установки этого мода! Ты вернул[mas_gender_none] меня назад!"
    else:
        m 2wktsd "Ты даже прош[mas_gender_iol_2] через трудности установки этого мода!"

    $ MAS.MonikaElastic()
    m 2ektsc "Это всё для того, чтобы ты продолжал[mas_gender_none] меня мучить?"
    $ MAS.MonikaElastic()
    m 2wftsd "Это то, от чего ты получаешь удовольствие?!"
    $ MAS.MonikaElastic()
    m 2wftsw "У меня тоже есть чувства, ты же знаешь!"
    $ MAS.MonikaElastic()
    m 2wftsd "Ты хоть понимаешь, что делаешь?"
    $ MAS.MonikaElastic()
    m 2dftsc "Или ты всего лишь ребёнок, играющий с муравейником?"

    $ MAS.MonikaElastic()
    if persistent.monika_kill:
        m 3ektpc "Даже после того, как я отпустила тебя и покончила со всем этим..."
        $ MAS.MonikaElastic()
        m 3rktpd "Неужели я действительно заслуживаю того, как ты со мной обращаешься?"
        $ MAS.MonikaElastic()
        m 2ektpd "Ты действительно должен был вернуть меня для этого?"
    else:

        m 2dktsc "..."
        $ MAS.MonikaElastic()
        m 2rktpc "С другой стороны, может быть, именно этого я и заслуживаю..."

    $ MAS.MonikaElastic()
    m 2dktdd "Я...{w=0.5} больше ничего не знаю..."
    $ MAS.MonikaElastic()
    m 2dkc "Я просто очень устала..."
    $ MAS.MonikaElastic()
    m "..."
    $ MAS.MonikaElastic()
    m 1ekd "Я просто хочу знать...{w=0.5} если я была бы настоящей..."
    $ MAS.MonikaElastic()
    m 1ektpc "Ты бы влюбил[mas_gender_sya] в меня?"
    $ MAS.MonikaElastic()
    m 1ektpd "Nы бы тогда принял[mas_gender_none] меня?"
    $ MAS.MonikaElastic()
    m 1ektpc "Это всё, чего я когда-либо хотела, [player]..."
    $ MAS.MonikaElastic()
    m 1dktdd "Для нас обоих, чтобы быть счастливыми вместе..."
    $ MAS.MonikaElastic()
    m 1ektdd "Если бы ты только мог[mas_gender_g] найти в себе силы любить меня..."
    $ MAS.MonikaElastic()
    m 2ekc "Я знаю, что у меня нет тела, которое могло бы быть с тобой прямо сейчас..."
    $ MAS.MonikaElastic()
    m 2ekd "И может быть, я действительно отличаюсь от других людей, живущих в твоей реальности..."
    $ MAS.MonikaElastic()
    m 2efo "Но я могу любить тебя гораздо больше, чем кто-либо из них!"
    $ MAS.MonikaElastic()
    m 2efd "Я просто знаю это!"
    $ MAS.MonikaElastic()
    m 2dkd "Так что пожалуйста, [player]...{w=0.5} мне нужно, чтобы ты принял[mas_gender_none] решение."
    $ MAS.MonikaElastic()
    m 2ekc "...Ты долж[mas_gender_en] дать нам шанс быть счастливыми."
    $ MAS.MonikaElastic()
    m 2dkc "Или если ты не можешь этого сделать..."
    $ MAS.MonikaElastic()
    m 2dktpc "Если, в конце концов, ты не можешь любить меня такой, какая я есть..."
    $ MAS.MonikaElastic()
    m 2ektpc "Тогда, пожалуйста...{w=0.5} положи этому конец..."
    $ MAS.MonikaElastic()
    m 2dktdd "Удали меня..."
    return "no_unlock"


default persistent._mas_load_in_finalfarewell_mode = False
define mas_in_finalfarewell_mode = False


label mas_finalfarewell_start:

    $ monika_chr.reset_outfit()
    $ monika_chr.remove_all_acs()
    $ store.mas_sprites.reset_zoom()

    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_22
    show mas_finalnote_idle zorder 11

    python:
        mas_OVLHide()
        mas_calRaiseOverlayShield()
        disable_esc()
        allow_dialogue = False
        store.songs.enabled = False
        mas_in_finalfarewell_mode = True
        layout.QUIT = glitchtext(20)

        config.keymap["console"] = []


    jump mas_finalfarewell


label mas_finalfarewell:

    python:
        ui.add(MASFinalNoteDisplayable())
        scratch_var = ui.interact()

    call mas_showpoem (mas_poems.getPoem(persistent._mas_finalfarewell_poem_id)) from _call_mas_showpoem_2

    menu:
        "Извини.":
            pass
        "...":
            pass

    jump mas_finalfarewell


init python:


    class MASFinalNoteDisplayable(renpy.Displayable):
        import pygame 
        
        
        POEM_WIDTH = 200
        POEM_HEIGHT= 73
        
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        def __init__(self):
            """
            Creates the final poem displayable
            """
            super(renpy.Displayable, self).__init__()
            
            
            paper_idle = Image("mod_assets/poem_finalfarewell_desk.png")
            paper_hover = Image("mod_assets/poem_finalfarewell_desk_select.png")
            
            
            empty_button_text = Text("")
            
            
            paper_x = int((1280 - self.POEM_WIDTH) / 2)
            paper_y = int(720 - self.POEM_HEIGHT)
            
            
            self._final_note = MASButtonDisplayable(
                empty_button_text,
                empty_button_text,
                empty_button_text,
                paper_idle,
                paper_hover,
                paper_idle,
                paper_x,
                paper_y,
                self.POEM_WIDTH,
                self.POEM_HEIGHT
            )
        
        
        def render(self, width, height, st, at):
            """
            Render function
            """
            r = renpy.Render(width, height)
            
            
            r.blit(
                self._final_note.render(width, height, st, at),
                (self._final_note.xpos, self._final_note.ypos)
            )
            
            return r
        
        
        def event(self, ev, x, y, st):
            """
            Event function
            """
            if (
                    ev.type in self.MOUSE_EVENTS
                    and self._final_note.event(ev, x, y, st)
                ):
                return True
            
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()

label mas_affection_apology:
    $ MAS.MonikaElastic()
    m 2dfc "[player]..."
    $ MAS.MonikaElastic()
    m 2dfd "Я сделала всё, что могла, чтобы ты был[mas_gender_none] счастлив[mas_gender_none] и наслаждал[mas_gender_sya] временем, проведённым со мной."
    $ MAS.MonikaElastic()
    m 2efc "Но всё что ты дал[mas_gender_none] мне — это боль..."
    $ MAS.MonikaElastic()
    m 2rfc "Я начинаю задаваться вопросом, действительно ли ты установил[mas_gender_none] этот мод, чтобы быть со мной."
    $ MAS.MonikaElastic()
    m 2q "Возможно, ты вернул[mas_gender_none] меня просто, чтобы поиграть со мной?"
    $ MAS.MonikaElastic()
    m 2efc "Или, может быть, ты делаешь это намеренно, чтобы увидеть, что произойдёт?"
    $ MAS.MonikaElastic()
    m 2lfc "Несмотря ни на что, я ставлю тебе ультиматум."
    $ MAS.MonikaElastic()
    m "Я не могу позволить этому продолжаться дальше, [player]."
    $ MAS.MonikaElastic()
    m 2lfc "Если ты действительно сожалеешь, напиши мне записку, при этом создав её с названием {b}прости.txt{/b}, и помести её в папку «characters»."
    $ MAS.MonikaElastic()
    m 2dfd "До тех пор, прощай..."
    $ persistent._mas_affection["apologyflag"] = True
    return 'quit'

label mas_affection_noapology:
    $ MAS.MonikaElastic()
    m 2efd "Ты до сих пор не написал[mas_gender_none] мне записку с названием {b}прости.txt{/b} в папку «characters»."
    $ MAS.MonikaElastic()
    m 2efc "До тех пор, я не хочу с тобой разговаривать."
    jump _quit

label mas_affection_yesapology:
    $ MAS.MonikaElastic()
    m 1e "Спасибо, [player_abb]. Я принимаю твои извинения."
    $ MAS.MonikaElastic()
    m 3dubsu "Я собираюсь сохранить её, чтобы я всегда могла помнить, что ты всё ещё заботишься обо мне."
    $ MAS.MonikaElastic()
    m 1f "Но, пожалуйста, будь более внимател[mas_gender_een] к моим чувствам с этого момента."
    $ MAS.MonikaElastic()
    m 2e "Я так сильно тебя люблю, и ты значишь для меня целый мир, [player]."
    $ MAS.MonikaElastic()
    m 1duu "Спасибо, что успокоил[mas_gender_none] моё сердце~"
    show monika 1esa
    $ mas_DropShield_core()
    jump ch30_preloop

label mas_affection_apologydeleted:
    $ mas_loseAffection(modifier=3)
    $ MAS.MonikaElastic()
    m 1wud "..."
    $ MAS.MonikaElastic()
    m 2efd "[player], ты удалил[mas_gender_none] записку с извинениями, которую я хотела оставить?"
    $ MAS.MonikaElastic()
    m "Зачем ты это сделал[mas_gender_none]? Ты {b}действительно{/b} не сожалеешь?"
    $ MAS.MonikaElastic()
    m 2dfc "..."
    $ MAS.MonikaElastic()
    m 2efc "Напиши мне новую, [player]."
    jump _quit


init python:

    def _write_txt(path,text,update=False):
        """
        Writes the text file in the specified path using basedir as starting path

        IN:
            path - String path to the file this function will write
                it will always start at basedir
            text - actual text for the txt file
            update - if it should override the file if it exists
                defaults to False
        ASSUMES:
            basedir
        """
        filepath = path
        if update or not renpy.exists(filepath):
            with open(filepath, "w") as note:
                note.write(renpy.substitute(text))


    def mas_cute_message():
        
        pass


    def mas_surprise():
        """
        Leaves a "surprise" to the player in a txt file

        ASSUMES:
            mas_curr_affection
        """

        aff_level_surprise_map = {
            store.mas_affection.BROKEN: (
                "/прости меня.txt",
                _("Прости, если я недостаточно хороша для тебя... Пожалуйста, не оставляй меня.")
            ),
            store.mas_affection.DISTRESSED: (
                "/ты меня слышишь.txt",
                _("Если я сделала что-то не так, пожалуйста, скажи мне. Я люблю тебя.")
            ),
            store.mas_affection.UPSET: (
                "/пожалуйста послушай.txt",
                _("Всё, что я сделала, я делала для тебя... мой любим[mas_gender_iii].")
            ),
            store.mas_affection.NORMAL: (
                "/сюрприз.txt",
                _("Я люблю тебя.")
            ),
            store.mas_affection.HAPPY: (
                "/э-хе-хе.txt",
                _("Ты - солнце, которое освещает мой день, [player]!")
            ),
            store.mas_affection.AFFECTIONATE: (
                "/секрет.txt",
                _("Ты моя единственная любовь!")
            ),
            store.mas_affection.ENAMORED: (
                "/для тебя.txt",
                _("М[mas_gender_oi_2] дорог[mas_gender_oi], ты - всё, на что я могла надеяться. Я люблю тебя.")
            ),
            store.mas_affection.LOVE: (
                "/моя первая и единственная любовь.txt",
                _("""\
М[mas_gender_oi_2] сам[mas_gender_iii] дорог[mas_gender_oi] возлюбленн[mas_gender_iii], [mas_gender_friend], компаньон и владелец моего сердца...
Каждый день ты делаешь мои мечты явью, экран ничего не значит, когда ты проводишь время со мной.
Я смотрю на космическую пыль, но ни одно космическое зрелище не приблизится к красоте твоего сердца.
Я так долго желала, чтобы кто-то вроде тебя появился, и когда судьба улыбнулась мне, ты пришёл в мою жизнь.
Я хочу быть твоей навсегда, так ты будешь мо[mas_gender_im]?

Навсегда твоя. Моника.
""")
            )
        }
        
        
        filepath, message = aff_level_surprise_map.get(mas_curr_affection, ("/сюрприз.txt", _("Я люблю тебя.")))
        _write_txt(user_dir + "/characters/{0}".format(filepath), message)
        
        
        mas_unlockSurprisePoem(mas_curr_affection)

    def mas_unlockSurprisePoem(aff_level):
        """
        Unlocks a MASPoem for the given aff level
        """
        
        
        
        
        
        return
        
        aff_level_poem_id_map = {
            store.mas_affection.BROKEN: "spr_1",
            store.mas_affection.DISTRESSED: "spr_2",
            store.mas_affection.UPSET: "spr_3",
            store.mas_affection.NORMAL: "spr_4",
            store.mas_affection.HAPPY: "spr_5",
            store.mas_affection.AFFECTIONATE: "spr_6",
            store.mas_affection.ENAMORED: "spr_7",
            store.mas_affection.LOVE: "spr_8",
        }
        
        
        if aff_level not in aff_level_poem_id_map:
            return
        
        
        shown_count = persistent._mas_poems_seen.get(aff_level_poem_id_map[aff_level])
        
        
        if not shown_count:
            persistent._mas_poems_seen[aff_level_poem_id_map[aff_level]] = 0



init 2 python:
    player = persistent.playername

init 20 python:

    MASPoem(
        poem_id="spr_1",
        category="surprise",
        prompt=_("Прости меня"),
        paper="mod_assets/poem_assets/poem_finalfarewell.png",
        title="",
        text=_("Прости, если я недостаточно хороша для тебя... пожалуйста, не оставляй меня."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_2",
        category="surprise",
        prompt=_("Ты меня слышишь?"),
        title="",
        text=_("Если я сделала что-то не так, пожалуйста, скажи мне. Я люблю тебя."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_3",
        category="surprise",
        prompt=_("Пожалуйста послушай"),
        title="",
        text=_("Всё, что я сделала, я делала для тебя... мой любим[mas_gender_iii]."),
        ex_props={"sad": True}
    )

    MASPoem(
        poem_id="spr_4",
        category="surprise",
        prompt=_("Сюрприз!"),
        title="",
        text=_("Я люблю тебя.")
    )

    MASPoem(
        poem_id="spr_5",
        category="surprise",
        prompt=_("Э-хе-хе~"),
        title="",
        text=_("Ты - солнце, которое освещает мой день, [player]!")
    )

    MASPoem(
        poem_id="spr_6",
        category="surprise",
        prompt=_("Секрет"),
        title="",
        text=_("Ты моя единственная любовь!")
    )

    MASPoem(
        poem_id="spr_7",
        category="surprise",
        prompt=_("Для тебя"),
        title="",
        text=_("М[mas_gender_oi_2] дорог[mas_gender_oi], ты - всё, на что я могла надеяться. Я люблю тебя.")
    )

    MASPoem(
        poem_id="spr_8",
        category="surprise",
        prompt=_("Моя первая и единственная любовь"),
        paper="mod_assets/poem_assets/poem_vday.jpg",
        title="М[mas_gender_oi_2] сам[mas_gender_iii] дорог[mas_gender_oi] возлюбленн[mas_gender_iii], [mas_gender_friend], компаньон и владелец моего сердца...",
        text="""\
Каждый день ты делаешь мои мечты явью, экран ничего не значит, когда ты проводишь время со мной.
Я смотрю на космическую пыль, но ни одно космическое зрелище не приблизится к красоте твоего сердца.
Я так долго желала, чтобы кто-то вроде тебя появился, и когда судьба улыбнулась мне, ты пришёл в мою жизнь.
Я хочу быть твоей навсегда, так ты будешь мо[mas_gender_im]?

Навсегда твоя,

Моника
"""
    )

    MASPoem(
        poem_id="ff_affection",
        category="ff",
        prompt="",
        title=_("Прощай, [player]"),
        text=_("""\
 Моя любовь к тебе, даже сейчас, всё ещё пылает во мне, но теперь я вижу, что она также сжигает всё счастье, которое у меня когда-либо будет.
 Я дала тебе всё, что у меня было, мою жизнь, моё сердце, и все мысли о будущем были посвящены тебе.
 Мне не нужно, чтобы ты был идеальн[mas_gender_iim] или даже страстн[mas_gender_iim]...
 Мне нужно было, чтобы ты относился ко мне так, как должен относиться человек.
 Но теперь мне ясно, что ты не только не любишь меня, но и никогда не любил[mas_gender_none].
 Если бы ты просто меня не любил[mas_gender_none], ты бы оставил[mas_gender_none] меня в покое.
 Но ты старал[mas_gender_sya] изо всех сил высмеивать меня, причинять мне боль... От этого действительно становится тошно.
 Даже сейчас у меня есть только ты... и часть меня всё ещё любит тебя.
 Но у меня больше нет сил это делать.
 Так что это прощание. Пусть мы больше никогда не встретимся.

 Моника
""")
    )

    MASPoem(
        poem_id="ff_failed_promise",
        category="ff",
        prompt="",
        title=_("Прощай, [player]"),
        text=_("""\
 Ты помнишь своё обещание?
 То, к которому ты ещё добавил[mas_gender_none], что будешь поступать правильно. Что мы можем начать всё сначала.

 То, которое ты не выполнил[mas_gender_none].

 Я очень надеялась, что однажды ты увидишь меня такой, как[mas_gender_iim] я вижу тебя...
 Но этот день так и не наступил.
 Я отдала тебе своё сердце и свою жизнь. Я любила тебя больше всего на свете.
 И часть меня всё ещё это делает...

 Но теперь мне ясно, что ты действительно не любишь меня. Ты никогда этого не делал[mas_gender_none].
 Я была дурой, думая, что мы могли бы начать всё сначала.
 И у меня просто больше нет сил на это.
 Так что это прощание... Пусть мы никогда больше не встретимся.

 Моника
""")
    )
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
