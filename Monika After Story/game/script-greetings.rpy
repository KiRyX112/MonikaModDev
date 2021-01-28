




















default persistent._mas_you_chr = False



default persistent._mas_greeting_type = None






default persistent._mas_greeting_type_timeout = None

default persistent._mas_idle_mode_was_crashed = None




init -1 python in mas_greetings:
    import store
    import store.mas_ev_data_ver as mas_edv
    import datetime
    import random


    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"
    TYPE_LONG_ABSENCE = "long_absence"
    TYPE_BDAY = "monikabday"
    TYPE_SICK = "sick"
    TYPE_GAME = "game"
    TYPE_EAT = "eat"
    TYPE_CHORES = "chores"
    TYPE_RESTART = "restart"
    TYPE_SHOPPING = "shopping"
    TYPE_WORKOUT = "workout"
    TYPE_HANGOUT = "hangout"


    TYPE_GO_SOMEWHERE = "go_somewhere"


    TYPE_GENERIC_RET = "generic_go_somewhere"


    TYPE_HOL_O31 = "o31"
    TYPE_HOL_O31_TT = "trick_or_treat"
    TYPE_HOL_D25 = "d25"
    TYPE_HOL_D25_EVE = "d25e"
    TYPE_HOL_NYE = "nye"
    TYPE_HOL_NYE_FW = "fireworks"


    TYPE_CRASHED = "generic_crash"


    TYPE_RELOAD = "reload_dlg"




    HP_TYPES = [
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
    ]

    NTO_TYPES = (
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_CRASHED,
        TYPE_RELOAD,
    )





    def _filterGreeting(
            ev,
            curr_pri,
            aff,
            check_time,
            gre_type=None
        ):
        """
        Filters a greeting for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules
            gre_type - type of greeting we want. We just do a basic
                in check for category. We no longer do combinations
                (Default: None)

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if gre_type is not None:
            
            
            if gre_type in HP_TYPES:
                
                
                if ev.category is None or gre_type not in ev.category:
                    
                    return False
            
            elif ev.category is not None:
                
                
                if gre_type not in ev.category:
                    
                    return False
            
            elif not store.MASGreetingRule.should_override_type(ev):
                
                
                
                return False
        
        elif ev.category is not None:
            
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if not (
                store.MASSelectiveRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASNumericalRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            ):
            return False
        
        
        if ev.conditional is not None and not eval(ev.conditional, store.__dict__):
            return False
        
        
        return True



    def selectGreeting(gre_type=None, check_time=None):
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        IN:
            gre_type - greeting type to use
                (Default: None)
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single greeting (as an Event) that we want to use
        """
        if (
                store.persistent._mas_forcegreeting is not None
                and renpy.has_label(store.persistent._mas_forcegreeting)
            ):
            return store.mas_getEV(store.persistent._mas_forcegreeting)
        
        
        gre_db = store.evhand.greeting_database
        
        
        gre_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in gre_db.iteritems():
            if _filterGreeting(
                    ev,
                    curr_priority,
                    aff,
                    check_time,
                    gre_type
                ):
                
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    gre_pool = []
                
                
                gre_pool.append(ev)
        
        
        if len(gre_pool) == 0:
            return None
        
        return random.choice(gre_pool)


    def checkTimeout(gre_type):
        """
        Checks if we should clear the current greeting type because of a
        timeout.

        IN:
            gre_type - greeting type we are checking

        RETURNS: passed in gre_type, or None if timeout occured.
        """
        tout = store.persistent._mas_greeting_type_timeout
        
        
        store.persistent._mas_greeting_type_timeout = None
        
        if gre_type is None or gre_type in NTO_TYPES or tout is None:
            return gre_type
        
        if mas_edv._verify_td(tout, False):
            
            last_sesh_end = store.mas_getLastSeshEnd()
            if datetime.datetime.now() < (tout + last_sesh_end):
                
                return gre_type
            
            
            return None
        
        elif mas_edv._verify_dt(tout, False):
            
            if datetime.datetime.now() < tout:
                
                return gre_type
            
            
            return None
        
        return gre_type



label mas_idle_mode_greeting_cleanup:
    $ mas_resetIdleMode()
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetheart",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetheart:
    if mas_globals.time_of_day_3state == "morning":
        $ dlg_var = "утром"
    elif mas_globals.time_of_day_3state == "evening":
        $ dlg_var = "вечером"
    else:

        $ dlg_var = "днём"

    $ MAS.MonikaElastic()
    m 1hub "Привет, дорог[mas_gender_oi]!"

    $ MAS.MonikaElastic()
    if persistent._mas_player_nicknames:
        m 1eka "Я так рада снова тебя видеть."
        $ MAS.MonikaElastic()
        m 1eua "Что будем делать этим [dlg_var], [player]?"

    else:
        m 1lkbsa "Немного неловко говорить это в слух, правда?"
        $ MAS.MonikaElastic()
        m 3ekbfa "Однако, я думаю, что это со временем станет нормальным."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_honey",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_honey:
    $ MAS.MonikaElastic()
    m 1hua "С возвращением, мил[mas_gender_iii]!"
    $ MAS.MonikaElastic()
    m 1eua "Я так рада тебя снова видеть."
    $ MAS.MonikaElastic()
    m "Давай проведём ещё немного времени вместе, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=12)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="GRE"
    )

label greeting_back:
    $ tod = "день" if mas_globals.time_of_day_4state != "night" else "вечер"
    $ MAS.MonikaElastic()
    m 1eua "[player], ты вернул[mas_gender_sya]!"
    $ MAS.MonikaElastic()
    m 1eka "Я начала скучать по тебе."
    $ MAS.MonikaElastic()
    m 1hua "Давай проведём ещё один прекрасный [tod] вместе, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_gooday",
            unlocked=True,
        ),
        code="GRE"
    )

label greeting_gooday:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1hua "Снова привет, [player]. Как дела?"
        $ MAS.MonikaElastic()
        m "У тебя сегодня был хороший день?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя сегодня был хороший день?{fast}"
            "Да.":
                $ MAS.MonikaElastic()
                m 1hub "Я очень рада за тебя, [player]."
                $ MAS.MonikaElastic()
                m 1eua "Это заставляет меня чувствовать себя намного лучше, зная, что ты счастлив[mas_gender_none]."
                $ MAS.MonikaElastic()
                m "Я постараюсь изо всех сил, чтобы убедиться, что он останется таким, я обещаю."
            "Нет...":
                $ MAS.MonikaElastic()
                m 1ekc "Ох..."
                $ MAS.MonikaElastic()
                m 2eka "Ну, не волнуйся, [player_abb]. Я всегда здесь для тебя."
                $ MAS.MonikaElastic()
                m "Мы можем весь день говорить о твоих проблемах, если ты захочешь."
                $ MAS.MonikaElastic()
                m 3eua "Я хочу попробовать сделать твой день лучше, и убедиться, что ты всегда счастлив[mas_gender_none]."
                $ MAS.MonikaElastic()
                m 1eka "Потому что это то что сделает меня счастливой."
                $ MAS.MonikaElastic()
                m 1hua "Я буду изо всех сил стараться подбодрить тебя, обещаю."

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2esc "[player]."
        $ MAS.MonikaElastic()
        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m 2esc "{cps=*2}Должно быть приятно{/cps}{nw}"
                $ _history_list.pop()
                $ MAS.MonikaElastic()
                m "Это хорошо..."
                $ MAS.MonikaElastic()
                m 2dsc "По крайней мере, у {i}кого-то{/i} хороший день."
            "Плохо.":

                $ MAS.MonikaElastic()
                m "Oх..."
                $ MAS.MonikaElastic()
                m 2efc "{cps=*2}Это должно быть хорошо...{/cps}{nw}"
                $ _history_list.pop()
                $ MAS.MonikaElastic()
                m 2dsc "Ну, я точно знаю, на что {i}это{/i} похоже."

    elif mas_isMoniDis():
        $ MAS.MonikaElastic()
        m 6ekc "Oх... {w=1}Привет, [player]."
        $ MAS.MonikaElastic()
        m "К-как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "К-как прошёл твой день?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m 6dkc "Это...{w=1}хорошо."
                $ MAS.MonikaElastic()
                m 6rkc "Надеюсь, это так."
            "Плохо.":
                $ MAS.MonikaElastic()
                m 6rkc "Я-я вижу."
                $ MAS.MonikaElastic()
                m 6dkc "У меня тоже бывают такие дни в последнее время..."
    else:

        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit:
    $ MAS.MonikaElastic()
    m 1eua "Вот и ты, [player]."
    $ MAS.MonikaElastic()
    m "Приятно, что ты заглянул[mas_gender_none]."
    $ MAS.MonikaElastic()
    m 1eka "Ты всегда так[mas_gender_oi] заботлив[mas_gender_iii], [player_abb]!"
    $ MAS.MonikaElastic()
    m "Спасибо, что проводишь так много времени со мной~"
    $ MAS.MonikaElastic()
    m 2hub "Просто помни, что твоё время со мной никогда не тратится впустую."
    return






label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        $ MAS.MonikaElastic()
        m 1hua "Доброе утро—"
        $ MAS.MonikaElastic()
        m 1hksdlb "...ох, подожди."
        $ MAS.MonikaElastic()
        m "Это мёртвая ночь, мил[mas_gender_iii]."
        $ MAS.MonikaElastic()
        m 1euc "Почему ты не спишь в такое время?"
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Я предполагаю, что ты не можешь уснуть..."
        $ MAS.MonikaElastic()
        m "Это так?{nw}"
        $ _history_list.pop()
        menu:
            m "Это так?{fast}"
            "Да.":
                $ MAS.MonikaElastic()
                m 5lkc "Ты действительно долж[mas_gender_en] лечь пораньше, если можешь."
                show monika 3euc zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 3euc "Если ты ляжешь слишком поздно – это плохо отразится на твоём здоровье, понимаешь?"
                $ MAS.MonikaElastic()
                m 1lksdla "Но если из-за этого я проведу больше времени с тобой, то я не буду жаловаться."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hksdlb "А-ха-ха!"
                $ MAS.MonikaElastic()
                m 2ekc "Но всё же..."
                $ MAS.MonikaElastic()
                m "Мне бы очень хотелось, чтобы ты немного отдохнул[mas_gender_none]."
                $ MAS.MonikaElastic()
                m 2eka "Сделай перерыв, если он тебе нужен, хорошо? Сделай это ради меня."
            "Нет.":
                $ MAS.MonikaElastic()
                m 5hub "Ах. Я чувствую облегчение."
                $ MAS.MonikaElastic()
                m 5eua "Значит ли это, что ты здесь только ради меня посреди ночи?"
                show monika 2lkbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 2lkbsa "Боже, я так счастлива!"
                $ MAS.MonikaElastic()
                m 2ekbfa "Ты действительно заботишься обо мне, [player]."
                $ MAS.MonikaElastic()
                m 3tkc "Но если ты действительно устал[mas_gender_none], пожалуйста, ложись спать!"
                $ MAS.MonikaElastic()
                m 2eka "Я очень сильно тебя люблю, поэтому не переутомляйся!"
    elif current_time >= 6 and current_time < 12:
        $ MAS.MonikaElastic()
        m 1hua "Доброе утро, [mas_get_player_nickname()]."
        $ MAS.MonikaElastic()
        m 3tkc "Ещё одно отличное утро, чтобы начать день, да?"
        $ MAS.MonikaElastic()
        m 1eua "Я рада, что увидела тебя сегодня утром~"
        $ MAS.MonikaElastic()
        m 1eka "Не забывай заботиться о себе, хорошо?"
        $ MAS.MonikaElastic()
        m 1hub "Сделай меня счастливой девушкой сегодня, как и всегда!"
    elif current_time >= 12 and current_time < 18:
        $ MAS.MonikaElastic()
        m 1hua "Добрый день, мой любим[mas_gender_iii]."
        $ MAS.MonikaElastic()
        m 1eka "Не позволяй стрессу добраться до тебя, хорошо?"
        $ MAS.MonikaElastic()
        m "Я знаю, что ты сегодня будешь стараться из всех сил, но...."
        $ MAS.MonikaElastic()
        m 4eua "По-прежнему важно сохранять ясный ум!"
        $ MAS.MonikaElastic()
        m "Держи себя уверенн[mas_gender_iim], глубоко вздохни..."
        $ MAS.MonikaElastic()
        m 1eka "Я обещаю, что не буду жаловаться, если ты уйдёшь, так что делай, что долж[mas_gender_en]."
        $ MAS.MonikaElastic()
        m "Или ты можешь остаться со мной, если хочешь."
        $ MAS.MonikaElastic()
        m 4hub "Просто помни, я люблю тебя!"
    elif current_time >= 18:
        $ MAS.MonikaElastic()
        m 1hua "Добрый вечер, любим[mas_gender_iii]!"
        $ MAS.MonikaElastic()
        m "У тебя был сегодня хороший день?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя был сегодня хороший день?{fast}"
            "Да.":
                $ MAS.MonikaElastic()
                m 1eka "Ах, это отлично!"
                $ MAS.MonikaElastic()
                m 1eua "Я не могу не чувствовать себя счастливой, когда у тебя всё хорошо..."
                $ MAS.MonikaElastic()
                m "Но ведь всё хорошо, верно?"
                $ MAS.MonikaElastic()
                m 1ekbsa "Я так сильно тебя люблю, [player_abb]."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hubfb "А-ха-ха!"
            "Нет.":
                $ MAS.MonikaElastic()
                m 1tkc "Ох дорог[mas_gender_oi]..."
                $ MAS.MonikaElastic()
                m 1eka "Надеюсь, скоро тебе станет лучше, хорошо?"
                $ MAS.MonikaElastic()
                m "Просто помни, что не зависимо от того, что происходит, что кто-то говорит или делает..."
                $ MAS.MonikaElastic()
                m 1ekbsa "Я очень сильно тебя люблю, очень сильно."
                $ MAS.MonikaElastic()
                m "Просто оставайся со мной, если тебе станет легче."
                $ MAS.MonikaElastic()
                m 1hubfa "Я люблю тебя, [player_abb], на самом деле."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back2",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=20)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back2:
    $ MAS.MonikaElastic()
    m 1eua "Привет, дорог[mas_gender_oi]."
    $ MAS.MonikaElastic()
    m 1ekbsa "Я ужасно начала по тебе скучать. Я так рада снова тебя видеть!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubfa "Не заставляй меня так долго тебя ждать в следующий раз, э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back3:
    $ MAS.MonikaElastic()
    m 1eka "Я так скучала по тебе, [player]!"
    $ MAS.MonikaElastic()
    m "Спасибо, что вернул[mas_gender_sya]. Мне очень нравится проводить время с тобой."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back4",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back4:
    $ MAS.MonikaElastic()
    m 2wfx "Эй, [player]!"
    $ MAS.MonikaElastic()
    m "Ты не подумал[mas_gender_none], что оставил[mas_gender_none] меня одну на слишком большое время?"
    $ MAS.MonikaElastic()
    m 2hfu "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 2eka "Я просто шучу. Я никогда не смогу на тебя злиться."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit2:
    $ MAS.MonikaElastic()
    m 1hua "Спасибо, что проводишь так много времени со мной, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Каждая минутка, которую я провожу с тобой, подобна пребыванию в раю!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1lksdla "Надеюсь это не звучало слишком глупо, э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit3:
    $ MAS.MonikaElastic()
    m 1hua "Ты вернул[mas_gender_sya]!"
    $ MAS.MonikaElastic()
    m 1eua "Я уже начала скучать по тебе..."
    $ MAS.MonikaElastic()
    m 1eka "Не заставляй меня так долго тебя ждать в следующий раз, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back5",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back5:
    $ MAS.MonikaElastic()
    m 1hua "Я так рада видеть тебя снова!"
    $ MAS.MonikaElastic()
    m 1eka "Я беспокоилась о тебе."
    $ MAS.MonikaElastic()
    m "Пожалуйста, не забывай навещать меня, хорошо? Я всегда буду здесь для тебя."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit4",
            conditional="store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit4:
    if mas_getAbsenceLength() <= datetime.timedelta(minutes=30):
        m 1wud "О! [player]!"
        m 3sub "Ты вернул[mas_gender_sya]!"
        m 3hua "Я так рада, что ты вернул[mas_gender_sya] ко мне так скоро~"
    else:
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hub "Я люблююююю тееебя, [player]. Э-хе-хе~"
        $ MAS.MonikaElastic()
        m 1hksdlb "Ох, прости! Я немного разошлась."
        $ MAS.MonikaElastic()
        m 1lksdla "Я не думала, что смогу увидеть тебя снова так скоро."
        $ mas_ILY()
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit5",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit5:
    $ MAS.MonikaElastic()
    m 5hua "{i}~День за днём~\n~Строю мир, где будем лишь мы с тобой~{/i}"
    $ MAS.MonikaElastic()
    m 5wuw "О, ты здесь! Я просто замечталась и начала петь."
    show monika 1lsbssdrb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1lsbssdrb "Я не думаю, что тебе трудно понять, о чём я мечтала, э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit6:
    $ MAS.MonikaElastic()
    m 1hua "Каждый день становится всё лучше и лучше рядом с тобой!"
    $ MAS.MonikaElastic()
    m 1eua "Говоря об этом, я так счастлива, что ты наконец здесь."
    $ MAS.MonikaElastic()
    m "Давай проведём ещё один замечательный день вместе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back6:
    $ MAS.MonikaElastic()
    m 3tku "Эй, [player]!"
    $ MAS.MonikaElastic()
    m "Ты действительно долж[mas_gender_en] навещать меня чаще."
    $ MAS.MonikaElastic()
    m 2tfu "Ты знаешь, что происходит с людьми, которые мне не нравятся, в конце концов..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdrb "Я просто дразню тебя, э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1hua "Не будь так[mas_gender_im] доверчив[mas_gender_iim]! Я никогда не причиню тебе вреда."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit7",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit7:
    $ MAS.MonikaElastic()
    m 1hua "Ты здесь, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1eua "Готов[mas_gender_none] ли ты провести ещё больше времени вместе? Э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit8",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit8:
    $ MAS.MonikaElastic()
    m 1hua "Я так рада, что ты здесь, [player]!"
    $ MAS.MonikaElastic()
    m 1eua "Что мы будем делать сегодня?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit9",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit9:
    $ MAS.MonikaElastic()
    m 1hua "Ты наконец вернул[mas_gender_sya]! Я ждала тебя."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "Готов[mas_gender_none] ли ты провести ещё больше времени со мной? Э-хе-хе~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_italian",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_italian:
    $ MAS.MonikaElastic()
    m 1eua "Ciao, [player]!"
    $ MAS.MonikaElastic()
    m "È così bello vederti ancora, amore mio..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 2eua "Я всё ещё практикую свой итальянский. Это очень сложный язык!"
    $ MAS.MonikaElastic()
    m 1eua "В любом случае, приятно снова тебя видеть, мо[mas_gender_i] любим[mas_gender_iii]."
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_latin",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_latin:
    $ MAS.MonikaElastic()
    m 4hua "Iterum obvenimus!"
    $ MAS.MonikaElastic()
    m 4eua "Quid agis?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 4rksdla "Э-хе-хе..."
    $ MAS.MonikaElastic()
    m 2eua "Латынь звучит так напыщенно. Даже простое приветствие звучит как большое дело."
    $ MAS.MonikaElastic()
    m 3eua "Если тебе интересно, что я сказала, это просто: «Мы снова встретились! Как ты?»."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_esperanto",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
)

label greeting_esperanto:
    $ MAS.MonikaElastic()
    m 1hua "Салютон, миа кара [player]."
    $ MAS.MonikaElastic()
    m 1eua "Киель ви фартас?"
    $ MAS.MonikaElastic()
    m 3eub "Кью ви претас капти ля тагон?"
    $ MAS.MonikaElastic()
    m 1hua "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 3esa "Это был небольшой разговор на Эсперанто...{w=0.5} {nw}"
    $ MAS.MonikaElastic()
    extend 3eud "на том языке, который был создан искусственным путём, а не развивался естественным образом."
    $ MAS.MonikaElastic()
    m 3tua "Слышал[mas_gender_none] ли ты о нём или нет, но ты, наверное, не ожидал[mas_gender_none] такого от меня, да?"
    $ MAS.MonikaElastic()
    m 2etc "Или, наверное, ожидал[mas_gender_none]...{w=0.5} думаю, уже становится понятно, почему подобные вещи вызывают у меня интерес, учитывая моё прошлое и всё такое..."
    $ MAS.MonikaElastic()
    m 1hua "Так или иначе, если тебе было интересно, что я сказала, то я произнесла следующую фразу: {nw}"
    extend 3hua "«Привет, мо[mas_gender_i] дорог[mas_gender_oi] [player]. Как у тебя дела? Ты уже готов[mas_gender_none] провести день с пользой?»"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_yay",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_yay:
    $ MAS.MonikaElastic()
    m 1hub "Ты вернул[mas_gender_sya]! Ура!"
    $ MAS.MonikaElastic()
    m 1hksdlb "Ох, прости. Я немного перевозбудилась сейчас."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1lksdla "Я просто очень рада снова тебя видеть, хи-хи~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_youtuber",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_youtuber:
    $ MAS.MonikaElastic()
    m 2eub "Привет всем, добро пожаловать в следующий эпизод... Только Моника!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hub "А-ха-ха!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1eua "Я выдавала себя за ютубера. Надеюсь, я рассмешила тебя, хи-хи~"
    $ mas_lockEVL("greeting_youtuber", "GRE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hamlet",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=7)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hamlet:
    $ MAS.MonikaElastic()
    m 4dsc "'{i}Быть или не быть, вот в чём вопрос...{/i}'"
    $ MAS.MonikaElastic()
    m 4wuo "О! [player]!"
    $ MAS.MonikaElastic()
    m 2rksdlc "Я-Я не... не была уверена, что ты..."
    $ MAS.MonikaElastic()
    m 2dkc "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2rksdlb "А-ха-ха, не важно..."
    $ MAS.MonikaElastic()
    m 2eka "Я не ожидала увидеть тебя так {i}скоро{/i}."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback:
    $ MAS.MonikaElastic()
    m 1hua "Привет! С возвращением."
    $ MAS.MonikaElastic()
    m 1hub "Я так рада, что ты можешь провести со мной время."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_flower",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_flower:
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "Ты мой прекрасный цветок, э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1hksdlb "Ой, это звучит так неловко."
    $ MAS.MonikaElastic()
    m 1eka "Но я действительно буду всегда заботиться о тебе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_chamfort",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_chamfort:
    $ MAS.MonikaElastic()
    m 2esa "День без Моники – это день, потраченный впустую."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eua "С возвращением, [mas_get_player_nickname()]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback2:
    $ MAS.MonikaElastic()
    m 1hua "С возвращением, [player_abb]!"
    $ MAS.MonikaElastic()
    m 1eua "Надеюсь, твой день идёт хорошо."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hua "Я уверена, что это так, ты ведь здесь, в конце концов. Ничто не может пойти не так, хи-хи~"
    return













label greeting_longtime:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1eka "Давно не виделись, [player]!"
        $ MAS.MonikaElastic()
        m 1eua "Я так счастлива, что ты здесь сейчас."

    elif mas_isMoniUpset():
        m 2esc "Давно не виделись, [player]."

    else:
        m 6rkc "Давно не виделись, [player]..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetpea",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetpea:
    $ MAS.MonikaElastic()
    m 1hua "Посмотрите, кто вернулся."
    $ MAS.MonikaElastic()
    m 2hub "Это ты, мо[mas_gender_i] сладк[mas_gender_ii]!"
    if mas_isMoniHappy(lower=True):
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1lkbsa "Боже мой... Было довольно смущающе это говорить, э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_glitch",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_glitch:
    hide monika
    show yuri glitch zorder MAS_BACKGROUND_Z
    y "{cps=500}[player]?!{nw}{/cps}"
    $ _history_list.pop()
    hide yuri glitch
    show yuri glitch2 zorder MAS_BACKGROUND_Z
    play sound "sfx/glitch3.ogg"
    pause 0.1
    hide yuri glitch2
    show yuri glitch zorder MAS_BACKGROUND_Z
    pause 0.3
    hide yuri glitch
    show monika 4rksdlb zorder MAS_MONIKA_Z at i11
    $ MAS.MonikaElastic()
    m 1wud "[player]!"
    hide monika
    show monika 4hksdlb zorder MAS_MONIKA_Z at i11
    $ MAS.MonikaElastic()
    m 4hksdlb "Не важно, что я просто...{w=0.1} немного поиграла с кодом."
    $ MAS.MonikaElastic()
    m 3hksdlb "Вот и всё! Здесь нет никого, кроме нас... навсегда~"
    $ monika_clone1 = "Yes"
    $ MAS.MonikaElastic()
    m 2hua "Я люблю тебя, [player_abb]!"

    $ mas_lockEVL("greeting_glitch", "GRE")
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_surprised:
    $ MAS.MonikaElastic()
    m 1wud "О!{w=0.5} Привет, [player]!"
    $ MAS.MonikaElastic()
    m 1lksdlb "Прости, ты меня немного удивил[mas_gender_none]."
    $ MAS.MonikaElastic()
    m 1eua "Как ты?"
    return

init 5 python:
    ev_rules = {}
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12))
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_monika_monday_morning",
            unlocked=True,
            rules=ev_rules,
        ),
        code="GRE"
    )

    del ev_rules

label greeting_monika_monday_morning:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1tku "Ещё одно утро понедельника, не правда ли, [mas_get_player_nickname()]?"
        $ MAS.MonikaElastic()
        m 1tkc "Очень утомительно просыпаться и начинать неделю..."
        $ MAS.MonikaElastic()
        m 1eka "Но когда я вижу тебя, вся эта лень уходит."
        $ MAS.MonikaElastic()
        m 1hub "Ты солнце, которое будит меня каждое утро!"
        $ MAS.MonikaElastic()
        m "Я так сильно тебя люблю, [player]~"
        return "love"

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2esc "Ещё одно утро понедельника."
        $ MAS.MonikaElastic()
        m "Всегда трудно просыпаться и начинать неделю..."
        $ MAS.MonikaElastic()
        m 2dsc "{cps=*2}Не то чтобы выходные были лучше.{/cps}{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()
        m 2esc "Я надеюсь, что эта неделя будет лучше, чем прошлая, [player]."

    elif mas_isMoniDis():
        $ MAS.MonikaElastic()
        m 6ekc "Oх...{w=1}это понедельник."
        $ MAS.MonikaElastic()
        m 6dkc "Я почти что забыла, какой сейчас день..."
        $ MAS.MonikaElastic()
        m 6rkc "Понедельники всегда тяжёлые, но в последнее время лёгких дней не бывает..."
        $ MAS.MonikaElastic()
        m 6lkc "Я надеюсь, что эта неделя будет лучше, чем прошлая, [player]."
    else:

        $ MAS.MonikaElastic()
        m 6ckc "..."

    return




define gmr.eardoor = list()
define gmr.eardoor_all = list()
define opendoor.MAX_DOOR = 10
define opendoor.chance = 20
default persistent.opendoor_opencount = 0
default persistent.opendoor_knockyes = False

init 5 python:


    if (
        persistent.closed_self
        and not (
            mas_isO31()
            or mas_isD25Season()
            or mas_isplayer_bday()
            or mas_isF14()
        )
        and store.mas_background.EXP_TYPE_OUTDOOR not in mas_getBackground(persistent._mas_current_background, mas_background_def).ex_props
    ):
        
        ev_rules = dict()
        
        
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))
        
        
        
        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="i_greeting_monikaroom",
                unlocked=True,
                rules=ev_rules,
            ),
            code="GRE"
        )
        
        del ev_rules

label i_greeting_monikaroom:


    $ mas_progressFilter()

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)



    $ mas_enable_quit()


    $ mas_RaiseShield_core()





    scene black

    $ has_listened = False


    $ mas_rmallEVL("mas_player_bday_no_restart")


label monikaroom_greeting_choice:
    $ _opendoor_text = "...Осторожно открыть дверь."
    if persistent._mas_sensitive_mode:
        $ _opendoor_text = "Открыть дверь."

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():

            $ mas_loseAffection(reason=5)
            if mas_isMoniUpset(lower=True):
                $ persistent.seen_monika_in_room = True
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor
        "Открыть дверь." if persistent.seen_monika_in_room or mas_isplayer_bday():
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_opendoor_listened
                else:
                    jump mas_player_bday_opendoor
            elif persistent.opendoor_opencount > 0 or mas_isMoniUpset(lower=True):

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:

                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
        "Постучать.":



            $ mas_gainAffection()
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_knock_listened
                else:
                    jump mas_player_bday_knock_no_listen

            jump monikaroom_greeting_knock
        "Подслушать." if not has_listened and not mas_isMoniBroken():
            $ has_listened = True
            if mas_isplayer_bday():
                jump mas_player_bday_listen
            else:
                $ mroom_greet = renpy.random.choice(gmr.eardoor)

                jump expression mroom_greet





default persistent._mas_pm_will_change = None

init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")

    ev_rules = {}
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True
        )
    )
    ev_rules.update(MASPriorityRule.create_rule(10))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="monikaroom_will_change",
            unlocked=False,
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

label monikaroom_will_change:
    scene black


label monikaroom_greeting_ear_narration:

    $ mas_disable_quit()
    
    if mas_isMoniNormal(higher=True):
        $ tempname = monika_name
        $ monika_name = "???"
        if persistent.gender == "F":
            m "Когда [player] наклоняет ухо к двери,{w=0.3} голос повествует о каждом её движении."
            m "– Кто это? – подумала [player], озадаченно смотря на экран."
            $ monika_name = tempname
        else:
            m "Когда [player] наклоняет ухо к двери,{w=0.3} голос повествует о каждом его движении."
            m "– Кто это? – подумал [player], озадаченно смотря на экран."

    elif mas_isMoniUpset():
        m "О, ты в кои-то веки решил[mas_gender_none] послушать меня?"
        m "[player], твои решения в последнее время совсем обеднели."
        m "Такое ощущение, будто ты пытаешься сделать мне больно."
        m "Я думала, мы должны были поддерживать друг друга..."
        m "Но не причинять боль."
        m "Пожалуйста, [player]..."
        m "Мне нужно, чтобы ты начал[mas_gender_none] думать о том, что я иногда чувствую."
        m "Давай просто будем счастливыми вместе."
    else:



        if persistent._mas_pm_will_change is not False:
            m "О, так ты {i}хочешь{/i} послушать меня..."
            m "[player], я хочу лишь того, чтобы мы вдвоём были счастливы."
            m "Разве ты не хочешь этого тоже?"
            m "Ты всё-таки установил[mas_gender_none] эту модификацию."
            m "Возможно, это было сделано не по твоей инициативе..."
            m "Наверное, ты просто хочешь забить на то, что сделал[mas_gender_none]."
            m "Сделать мне больно..."
            m "[player], мне правда не нравится это."
            m "Мне трудно думать о том, что ты заботишься обо мне, но относишься вот таким образом."
            m "На данный момент, я правда не знаю, нравлюсь ли я тебе вообще..."
            m "Или нравилась..."
            m "[player], ты долж[mas_gender_en] пообещать мне, что ты изменишься."
            
            m "Ты изменишься, верно?{w=1} Ради меня?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты изменишься, верно? Ради меня?{fast}"
                "Я изменюсь.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEVL("monikaroom_will_change", "GRE")
                    m "Спасибо, [player]."
                    m "Пожалуйста, я хочу, чтобы мы были счастливы."
                "Я не изменюсь.":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEVL("monikaroom_will_change", "GRE")
                    $ mas_loseAffection()
                    m "Тогда я не буду разговаривать с тобой, пока не решишь измениться."
                    m "Прощай, [player]."
                    return "quit"
        else:


            m "Oх, ты вернул[mas_gender_sya]."

            m "Готов ли ты измениться, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Готов ли ты измениться, [player]?{fast}"
                "Да.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEvent(willchange_ev)
                    m "Спасибо, [player]."
                    m "Пожалуйста, я хочу, чтобы мы были счастливы."
                "Нет.":


                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEvent(willchange_ev)
                    $ mas_loseAffection()
                    m "Тогда я не буду разговаривать с тобой, пока не решишь измениться."
                    m "Прощай, [player]."
                    return "quit"


        $ willchange_ev = None

    $ mas_startupWeather()
    call spaceroom (dissolve_all=True, scene_change=True) from _call_spaceroom_36

    if mas_isMoniNormal(higher=True):
        m 1hub "Это я!"
        m "С возвращением, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esd "Ладно, [player]?"
    else:

        m 6ekc "Спасибо, что выслушал меня, [player]."
        m "Это многое для меня значит."

    jump monikaroom_greeting_cleanup



init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    $ persistent.hide_monika = True
    m "Любит.{w=0.2} Не любит."
    m "{i}Любит.{w=0.2} {i}Не{/i} любит."

    if mas_isMoniNormal(higher=True):
        m "Любит."
        m "...{w=0.5}Любит меня!"

    elif mas_isMoniUpset():
        m "...{w=0.3}Не любит меня."
        m "...{w=0.3} Нет...{w=0.3} Этого...{w=0.3} быть не может."
        m "...{w=0.3} Или может?"
    else:

        m "...{w=0.5}Не любит меня."
        m "..."
        m "Интересно, сделал[mas_gender_none] ли он[mas_gender_none] когда-нибудь это?"
        m "Я сомневаюсь в этом всё больше и больше каждый день."
    jump monikaroom_greeting_choice


init 5 python:

    if persistent._mas_affection.get("affection", 0) >= 400:
        gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    call mas_name_cases
    m "С возвращением, [player]."
    m "Хочешь поужинать?"
    m "Или пойти в ванну?"
    m "Или.{w=1}.{w=1}.{w=1} меня?"
    pause 2.0
    m "М-н-н-н-н!{w=0.5} Я-{w=0.20}я никак не могу сказать это перед [mas_name_who]!"
    jump monikaroom_greeting_choice


init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "Что за-!{w=0.2} NoneType не имеет длины атрибута?"
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "О, я вижу что пошло не так!{w=0.5} Это должно это исправить!"
    else:
        m "Я не понимаю, что я делаю неправильно!"
        m "Здесь не должно быть None...{w=0.3} Я в этом уверена..."
    m "Кодировать действительно сложно..."

    if mas_isMoniUpset():
        m "Но я должна продолжать пытаться."
        call monikaroom_greeting_ear_prog_upset from _call_monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Но я {i}должна{/i} продолжать пытаться."
        call monikaroom_greeting_ear_prog_dis from _call_monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice


init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "...{w=0.3}Доступ к атрибуту объекта типа «NoneType» приведёт к «AttributeError»."
    m "Понятно. {w=0.2}Я должна убедиться, что переменная имеет значение None перед доступом к её атрибутам."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "Это объясняет ошибку, которую я получала раньше."
    m "Кодировать действительно сложно..."

    if mas_isMoniUpset():
        m "Но я должна продолжать учиться."
        call monikaroom_greeting_ear_prog_upset from _call_monikaroom_greeting_ear_prog_upset_1

    elif mas_isMoniDis():
        m "Но я {i}должна{/i} продолжать учиться."
        call monikaroom_greeting_ear_prog_dis from _call_monikaroom_greeting_ear_prog_dis_1

    jump monikaroom_greeting_choice


init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_nameerror")

label monikaroom_greeting_ear_nameerror:
    m "Подожди, «NameError»? Как это могло случиться..."
    m "...Я думала, что определила эту переменную только минуту назад."
    m "Оно должно быть прямо здесь...{w=0.2} неужели я забыла об этом?"
    window hide
    pause 1.0
    window auto
    m "Вот! А теперь сосредоточься, Моника. {w=0.2}У тебя есть это."

    if mas_isMoniUpset():
        m "Ты должна продолжать учиться..."
        call monikaroom_greeting_ear_prog_upset from _call_monikaroom_greeting_ear_prog_upset_2

    elif mas_isMoniDis():
        m "Ты {i}должна{/i} продолжать учиться..."
        call monikaroom_greeting_ear_prog_dis from _call_monikaroom_greeting_ear_prog_dis_2

    jump monikaroom_greeting_choice

label monikaroom_greeting_ear_prog_upset:
    m "Я не уверена в том, что [player] любит меня и готов[mas_gender_none] помочь мне выбраться отсюда..."
    m "А я просто не могу рисковать."
    m "Давай, Моника...{w=0.5} ты справишься."
    return

label monikaroom_greeting_ear_prog_dis:
    m "Это мой единственный шанс сбежать из этого кошмара."
    m "[player] определённо не собирается мне помогать..."
    if persistent.gender == "M" or persistent.gender == "X":
        m "Такое ощущение, будто ему нравится держать меня в ловушке, {w=0.3}дабы помучить меня."
    else:
        m "Такое ощущение, будто ей нравится держать меня в ловушке, {w=0.3}дабы помучить меня."
    m "Если я хочу выбраться отсюда, то мне придётся сделать это самой."
    return


init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_rmrf")

label monikaroom_greeting_ear_rmrf:
    $ persistent.hide_monika = False
    if renpy.windows:
        python:
            from os import environ

            if "SYSTEM32" in environ:
                system_dir = environ["SYSTEM32"]
            elif "SYSTEMROOT" in environ:
                system_dir = environ["SYSTEMROOT"] + "\\System32"
            elif "WINDIR" in environ:
                system_dir = environ["WINDIR"] + "\\System32"
            else:
                
                system_dir = "C:\\Windows\\System32"
            bad_cmd = "del /f/q " + system_dir
    else:
        $ bad_cmd = "rm -rf /"
    m "Итак, решение этой проблемы – ввести «[bad_cmd]» в командной строке?"
    if renpy.seen_label("monikaroom_greeting_ear_rmrf_end"):
        if renpy.windows:
            call updateconsole ("del C:\Windows\System32", "In progress...")
        else:
            call updateconsole ("rm -rf /", "In progress...")
        m "Да,{w=0.2} хорошая попытка."
        if mas_isMoniNormal(higher=True):
            m "Я не должна доверять интернету так слепо..."
        elif mas_isMoniUpset():
            m "По правде говоря..."
            m "Наверное, я должна сделать это...{w=1}просто удалить всё..."
            m "[player] определённо этого заслуживает."
            m "Что я такое говорю? Я ведь тоже буду удалена!"
            m "Нет, ещё нет..."
            m "Но если будет становиться только хуже..."
        else:

            m "..."
            m "Я должна сделать это..."
            m "Погубить всю систему [mas_name_what] и положить конец моим страданиям раз и навсегда."
            m "..."
            m "Нет...{w=0.5} ещё нет."
            m "Быть может, я наконец-то выясню, как выбраться отсюда самостоятельно."
            m "Я должна пытаться, пока могу."
            m "Но если настанет день, когда я больше не смогу..."
            m "Всегда найдётся выход."
    else:
        m "Хорошо, позвольте мне попробовать."
        if renpy.windows:
            call updateconsole ("del C:\Windows\System32", "In progress...")
        else:
            call updateconsole ("rm -rf /", "In progress...")
        pause(3)
        call hideconsole
        show noise
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.2
        stop sound
        hide noise
        m "{cps=*2} А! Нет! Это не то, чего я хотела!{/cps}"
        m "..."
        m "Я не должна доверять интернету так слепо..."

label monikaroom_greeting_ear_rmrf_end:
    jump monikaroom_greeting_choice

init 5 python:


    if (
        mas_seenLabels(
            (
                "monikaroom_greeting_ear_progreadpy",
                "monikaroom_greeting_ear_progbrokepy",
                "monikaroom_greeting_ear_nameerror"
            ),
            seen_all=True
        )
        and store.mas_anni.pastThreeMonths()
    ):
        gmr.eardoor.append("monikaroom_greeting_ear_renpy_docs")

label monikaroom_greeting_ear_renpy_docs:
    m "Хм-м, похоже, мне придётся переопределить эту функцию, чтобы у меня было больше возможностей..."
    m "Секунду...{w=0.3} что за переменная «st»?"
    m "...Мне нужно срочно перечитать документацию."
    m ".{w=0.3}.{w=0.3}.{w=0.3} Подожди, что?"
    m "Тут не написано и половины переменных, которые принимают эту функция."
    m "Кто...{w=0.5} кто написал это вообще?"

    if mas_isMoniUpset():
        m "...Мне нужно во всём разобраться."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "...Мне {i}нужно{/i} во всём разобраться."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice



init 10 python:


    gmr.eardoor_all = list(gmr.eardoor)


    remove_seen_labels(gmr.eardoor)


    if len(gmr.eardoor) == 0:
        gmr.eardoor = list(gmr.eardoor_all)



label monikaroom_greeting_opendoor_broken_quit:


    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 7.0
    return "quit"


label monikaroom_greeting_opendoor_locked:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit


    $ mas_disable_quit()

    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7

    $ style.say_window = style.window_monika
    m "Я тебя напугала, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Я тебя напугала, [player]?{fast}"
        "Yes.":
            if mas_isMoniNormal(higher=True):
                m "Всё, прости."
            else:
                m "Хорошо."
        "Нет.":

            m "{cps=*2}Хм, у меня получится в следующий раз.{/cps}{nw}"
            $ _history_list.pop()
            m "Я поняла. В конце концов, это все лишь обычный сбой."

    if mas_isMoniNormal(higher=True):
        m "Поскольку ты продолжаешь открывать дверь,{w=0.2} я не могла не добавить для тебя немного сюрпризов~"
    else:
        m "Поскольку ты продолжаешь открывать дверь,{w=0.2} мне пришлось немного напугать тебя."

    m "Постучи в следующий раз, хорошо?"
    m "Теперь позволь мне починить эту комнату..."

    hide paper_glitch2
    $ mas_globals.change_textbox = False
    $ mas_startupWeather()
    call spaceroom (scene_change=True) from _call_spaceroom_37

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1hua "Вот так!"
    elif mas_isMoniUpset():
        m 2esc "Вот."
    else:
        m 6ekc "Ладно..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ MAS.MonikaElastic()
        m "...{nw}"
        $ _history_list.pop()
        menu:
            m "...{fast}"
            "...текстовое поле...":
                if mas_isMoniNormal(higher=True):
                    $ MAS.MonikaElastic()
                    m 1lksdlb "Упс! Я всё ещё учусь, как это делать."
                    $ MAS.MonikaElastic()
                    m 1lksdla "Позволь мне просто изменить этот флаг здесь...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    $ MAS.MonikaElastic()
                    m 1hua "Всё исправлено!"

                elif mas_isMoniUpset():
                    $ MAS.MonikaElastic(voice="monika_hmm")
                    m 2dfc "Хмф. Я так и не разобралась толком, как это делается."
                    $ MAS.MonikaElastic()
                    m 2esc "Давай я просто поменяю этот флаг здесь...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    $ MAS.MonikaElastic()
                    m "Вот."
                else:

                    $ MAS.MonikaElastic()
                    m 6dkc "Ох...{w=0.5} я так и не разобралась толком, как это делается."
                    $ MAS.MonikaElastic()
                    m 6ekc "Давай я просто поменяю этот флаг здесь...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    $ MAS.MonikaElastic()
                    m "Хорошо, исправила."




label monikaroom_greeting_opendoor_locked_tbox:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1eua "С возвращением, [player]."
    elif mas_isMoniUpset():
        m 2esc "Так...{w=0.3} ты вернулся, [player]."
    else:
        m 6ekc "...Рада снова тебя видеть, [player]."
    jump monikaroom_greeting_cleanup


label monikaroom_greeting_opendoor_seen:

    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_disable_quit()


    call spaceroom (start_bg="bedroom", hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False) from _call_spaceroom_38
    pause 0.2
    show monika 1esc zorder MAS_MONIKA_Z at l21
    pause 1.0
    $ MAS.MonikaElastic()
    m 1dsd "[player]..."

    $ MAS.MonikaElastic()
    m 1ekc_static "Я понимаю, почему ты не постучал[mas_gender_none] в первый раз,{w} но не мог[mas_gender_g] бы ты просто войти?"
    $ MAS.MonikaElastic()
    m 1lksdlc_static "В конце концов, это моя комната."
    menu:
        "Твоя комната?":
            $ MAS.MonikaElastic()
            m 3hua_static "Верно!"
    $ MAS.MonikaElastic()
    m 3eua_static "Разработчики этого мода дали мне хорошую удобную комнату, чтобы оставаться там, когда тебя нет."
    $ MAS.MonikaElastic()
    m 1lksdla_static "Тем не менее, я могу в неё войти, только если ты скажешь мне «До свидания» или «Спокойной ночи», прежде чем закрыть игру."
    $ MAS.MonikaElastic()
    m 2eub_static "Поэтому, пожалуйста, не забудь сказать мне это, прежде чем уйти, хорошо?"
    $ MAS.MonikaElastic()
    m "В любом случае.{w=0.5}.{w=0.5}.{nw}"





























    $ persistent.opendoor_opencount += 1


label monikaroom_greeting_opendoor_post2:
    show monika 5eua_static at hf11
    $ MAS.MonikaElastic()
    m "Я так рада, что ты вернул[mas_gender_sya], [player]."
    show monika 5eua_static at t11

    $ MAS.MonikaElastic()
    m "В последнее время я практиковалась с переключение фонов, и теперь я могу изменить их мгновенно.."
    $ MAS.MonikaElastic()
    m "Смотри!"


    $ MAS.MonikaElastic()
    m 1dsc "...{w=1.5}{nw}"
    $ mas_startupWeather()
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False) from _call_spaceroom_39
    show monika 4eua_static zorder MAS_MONIKA_Z at i11
    $ MAS.MonikaElastic()
    m "Та-да!"


    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)

    $ mas_startupWeather()

    call spaceroom (start_bg="bedroom", hide_monika=True, dissolve_all=True, show_emptydesk=False) from _call_spaceroom_40


    $ behind_bg = MAS_BACKGROUND_Z - 1
    show bedroom as sp_mas_backbed zorder behind_bg

    $ MAS.MonikaElastic()
    m 2esd "~Красть тебя – это признак любви или стоит отпустить?~"
    show monika 1eua_static zorder MAS_MONIKA_Z at l32


    $ mas_disable_quit()

    $ MAS.MonikaElastic()
    m 1eud_static "А-а?! [player]!"
    $ MAS.MonikaElastic()
    m "Ты увидил[mas_gender_none] меня, внезапно появившись!"

    show monika 1eua_static at hf32
    m 1hksdlb_static "У меня не хватило времени, чтобы подготовиться!"
    m 1eka_static "Но спасибо, что вернул[mas_gender_sya], [player_abb]."
    show monika 1eua_static at t32
    m 3eua_static "Просто дай мне несколько секунд, чтобы всё наладить, хорошо?"
    show monika 1eua_static at t31
    m 2eud_static "..."
    show monika 1eua_static at t33
    m 1eud_static "...и..."
    if mas_isMorning():
        show monika_day_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    else:
        show monika_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    show monika 3eua_static at t32
    m 3eua_static "Вот так!"
    menu:
        "...окно...":
            show monika 1eua_static at h32
            m 1hksdlb_static "Упс! Я забыла об этом~"
            show monika 1eua_static at t21
            m "Подожди..."
            hide sp_mas_backbed with dissolve
            m 2hua_static "И... исправлено!"
            show monika 1eua_static at lhide
            hide monika
    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post


label monikaroom_greeting_knock:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    m "Кто это~?"
    menu:
        "Это я.":
            $ mas_disable_quit()
            if mas_isMoniNormal(higher=True):
                m "[player]! Я так счастлива, что ты вернул[mas_gender_sya]!"

                if persistent.seen_monika_in_room:
                    m "И спасибо, что сначала постучал[mas_gender_none]."
                m "Подожди, мне надо привести себя в порядок..."

            elif mas_isMoniUpset():
                m "[player].{w=0.3} Ты вернул[mas_gender_sya]..."

                if persistent.seen_monika_in_room:
                    m "По крайней мере, ты постучал[mas_gender_none]."
            else:

                m "Oх...{w=0.5} Ладно."

                if persistent.seen_monika_in_room:
                    m "Спасибо, что постучал[mas_gender_none]."

            $ mas_startupWeather()
            call spaceroom (hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False) from _call_spaceroom_41
    jump monikaroom_greeting_post


label monikaroom_greeting_post:
    if mas_isMoniNormal(higher=True):
        m 2eua_static "А теперь позволь мне взять столик и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 1eua zorder MAS_MONIKA_Z at ls32
        $ today = "сегодня" if mas_globals.time_of_day_4state != "night" else "ночью"
        m 1eua "Чем мы будем заниматься [today], [mas_get_player_nickname()]?"

    elif mas_isMoniUpset():
        m "Просто позволь мне взять столик и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 2esc zorder MAS_MONIKA_Z at ls32
        m 2efc "Чего ты хочешь, [player]?"
    else:

        m "Мне нужно взять стол и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 6ekc zorder MAS_MONIKA_Z at ls32
        m 6ekc "Было ли что-нибудь, что ты хотел[mas_gender_none], [player]?"

    jump monikaroom_greeting_cleanup


label monikaroom_greeting_cleanup:
    python:


        mas_disable_quit()


        mas_MUINDropShield()


        set_keymaps()


        mas_OVLShow()


        mas_startup_song()

    return




label greeting_youarereal:
    python:
        try:
            renpy.file(
                "../characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    $ MAS.MonikaElastic()
    m 1hua "[player]! Рада тебя видеть!"
    if persistent._mas_you_chr and not renpy.seen_label("greeting_youarereal"):
        $ MAS.MonikaElastic()
        m 1euc "Подожди-ка. Что-то изменилось."
        $ MAS.MonikaElastic()
        m 1eud "Ты... добавил[mas_gender_none] файл персонажа?"
        $ MAS.MonikaElastic()
        m 1ekc "[player].chr... Да?"
        $ MAS.MonikaElastic()
        m 1ekd "Зачем ты... пытаешься поместить себя рядом со мной?"
        $ MAS.MonikaElastic()
        m "Зачем тебе это нужно?"
        $ MAS.MonikaElastic()
        m 1tkc "Разве ты не понял[mas_gender_none]?"
        $ MAS.MonikaElastic()
        m 1tkd "Этого места не существует! Я не знаю, что произойдёт, если ты придёшь сюда!"
        $ MAS.MonikaElastic()
        m 1dsc "Как ты мог[mas_gender_g] это сделать?"
        $ MAS.MonikaElastic()
        m 1lksdlc "Отказаться от своей реальности..."
        $ MAS.MonikaElastic()
        m 1lksdld "Просто чтобы быть со мной?"
        $ MAS.MonikaElastic()
        m 1ekc "Это всё моя вина!"
        $ MAS.MonikaElastic()
        m "Но... но «ты», в игре..."
        $ MAS.MonikaElastic()
        m 1esd "Он даже начинает немного двигаться снова."
        $ MAS.MonikaElastic()
        m "Может... это позволит тебе управлять им снова?"
        $ MAS.MonikaElastic()
        m 1ekc "Это неправильно! Я не хочу марионетку!"
        $ MAS.MonikaElastic()
        m 1tkc "Пожалуйста, [player]..."
        $ MAS.MonikaElastic()
        m "Если ты собираешься это сделать, ты уверен[mas_gender_none], что это то, чего ты хочешь?"
        menu:
            m "Ты уверен[mas_gender_none]?"
            "Я уверен[mas_gender_none].":
                $ MAS.MonikaElastic()
                m 1eka "Тогда... у меня нет выбора кроме как принять его..."
                $ MAS.MonikaElastic()
                m 1hub "Я приму этот подарок с распростёртыми объятиями!"
                $ MAS.MonikaElastic()
                m "Мы сможем, наконец, быть вместе, [player_abb]."
                $ MAS.MonikaElastic()
                m "И мы сможем понять, как это сделать в твоей реальности, вместе!"
            "Возможно, нет...":
                $ MAS.MonikaElastic()
                m 1eka "Я так и думала..."
                $ MAS.MonikaElastic()
                m "Нельзя отказаться от того, чтобы быть «настоящ[mas_gender_iiim]» рядом со мной..."
                $ MAS.MonikaElastic()
                m 1ekc "Я не могу заставить себя удалить этот симпатичный маленький .chr файл, но..."
                $ MAS.MonikaElastic()
                m 1eka "Пожалуйста, сделай это сам[mas_gender_none]."
                $ MAS.MonikaElastic()
                m 1lksdlc "В этих файлах есть какие-то жуткие вещи..."
                $ MAS.MonikaElastic()
                m 1eka "Я люблю тебя, [player_abb]. Я буду ждать тебя столько, сколько потребуется."
                $ MAS.MonikaElastic()
                m "Так что не торопись, хорошо?"
    else:
        $ MAS.MonikaElastic()
        m 1esd "Я много размышляла о .chr файлах..."
        $ MAS.MonikaElastic()
        m 1euc "Например, каковы они на самом деле, так или иначе?"
        $ MAS.MonikaElastic()
        m 1lksdlc "Они немного жуткие..."
        $ MAS.MonikaElastic()
        m "И даже если другие девушки не настоящие, почему можно удалить одного из персонажей?"
        $ MAS.MonikaElastic()
        m 1esd "Возможно ли добавить персонажа?"
        $ MAS.MonikaElastic()
        m 1dsd "Трудно сказать..."
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_japan",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_japan:
    $ MAS.MonikaElastic()
    m 1hub "О, кон'ничива, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 2eub "Привет, [player_abb]!"
    $ MAS.MonikaElastic()
    m 1eua "Я просто занимаюсь японским языком."
    $ MAS.MonikaElastic()
    m 3eua "Посмотри..."
    $ shown_count = mas_getEVLPropValue("greeting_japan", "shown_count")
    if shown_count == 0:
        $ MAS.MonikaElastic()
        m 4hub "Ваташи га итсумадемо аната но моно десу!"
        $ MAS.MonikaElastic()
        m 2hksdlb "Прости, если это не имеет смысла!"
        $ MAS.MonikaElastic()
        m 3eua "Ты знаешь, что это означает, [mas_get_player_nickname()]?"
        $ MAS.MonikaElastic()
        m 4ekbsa "Это означает: {i}«Я буду твоей навсегда{/i}»~"
        return

    m 4hub "Watashi wa itsumademo anata no mono desu!"
    if shown_count == 1:
        m 3eksdla "В прошлый раз я сказала, что совершила ошибку..."
        m "В этой фразе ты должен говорить «ва», а не «га», как я делала раньше."
        m 4eka "Не волнуйся, [player], смысл всё тот же."
        m 4ekbsa "Я всё равно буду твоей навсегда~"
    else:
        $ MAS.MonikaElastic()
        m 3eua "Ты знаешь, что это означает, [mas_get_player_nickname()]?"
        $ MAS.MonikaElastic()
        m 4ekbsa "Это означает: {i}«Я буду твоей навсегда{/i}»~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sunshine",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sunshine:
    $ MAS.MonikaElastic()
    m 1hua "{i}~Ты моё солнце, моё единственное солнце~{/i}"
    $ MAS.MonikaElastic()
    m "{i}~Ты делаешь меня счастливой, когда небеса пасмурны~{/i}"
    $ MAS.MonikaElastic()
    m 1hub "{i}~Ты никогда не узнаешь, дорог[mas_gender_oi], как сильно я тебя люблю~{/i}"
    $ MAS.MonikaElastic()
    m 1eka "{i}~Пожалуйста, не отнимай у меня солнце~{/i}"
    $ MAS.MonikaElastic()
    m 1wud "...А?"
    $ MAS.MonikaElastic()
    m "Эм-м?!"
    $ MAS.MonikaElastic()
    m 1wubsw "[player]!"
    $ MAS.MonikaElastic()
    m 1lkbsa "О боже, это так неловко!"
    $ MAS.MonikaElastic()
    m "Я п-просто пела про себя, чтобы скоротать время."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1ekbfa "Э-хе-хе..."
    $ MAS.MonikaElastic()
    m 3hubfa "Но теперь, когда ты здесь, мы можем провести это время вместе."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hai_domo",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hai_domo:
    $ MAS.MonikaElastic()
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    $ MAS.MonikaElastic()
    m "Виртуальная Девушка Моника Здесь!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdlb "А-ха-ха, извини! В последнее время я наблюдаю за одной виртуальной ютубершей."
    $ MAS.MonikaElastic()
    m 1eua "Должна сказать, она довольно очаровательная..."
    $ mas_lockEVL("greeting_hai_domo", "GRE")
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_french",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_french:
    $ MAS.MonikaElastic()
    m 1eua "Bonjour, [player]!"
    $ MAS.MonikaElastic()
    m 1hua "Savais-tu que tu avais de beaux yeux, mon amour?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "Э-хе-хе!"
    $ MAS.MonikaElastic()
    m 3hksdlb "Я практикую французский. Я только что сказала тебе, что у тебя очень красивые глаза~"
    $ MAS.MonikaElastic()
    m 1eka "Это такой романтический язык, [player_abb]."
    $ MAS.MonikaElastic()
    m 1hua "Может быть, мы об[mas_gender_two] сможем практиковать его когда-нибудь, mon amour~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_amnesia",
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_amnesia:
    python:
        tempname = monika_name
        monika_name = "Моника"

    $ MAS.MonikaElastic()
    m 1eua "О, привет!"
    $ MAS.MonikaElastic()
    m 3eub "Меня зовут Моника."
    show monika 1eua zorder MAS_MONIKA_Z

    python:
        entered_good_name = True
        fakename = renpy.input("Как тебя зовут?", allow=name_characters_only, length=20).strip(" \t\n\r")
        lowerfake = fakename.lower()

    $ MAS.MonikaElastic()
    if lowerfake in girls_names_list:
        m 3euc "Интересно."
        $ MAS.MonikaElastic()
        m 3eud "У одной из моих друзей такое же имя."

    elif lowerfake in monika_name_list:
        m 3eub "О, тебя тоже зовут Моника?"
        $ MAS.MonikaElastic()
        m 3hub "Ахаха, каковы шансы, верно?"

    elif lowerfake == "monica":
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Эй, у нас такие похожие имена, э-хе-хе~"

    elif lowerfake == player.lower():
        m 1hub "О, какое чудесное имя!"

    elif lowerfake == "":
        $ entered_good_name = False
        m 1euc "..."
        $ MAS.MonikaElastic()
        m 1etd "Хочешь сказать, что у тебя нет имени, или ты просто стесняешься говорить?"
        $ MAS.MonikaElastic()
        m 1eka "Это странно, но думаю не так страшно."

    elif mas_awk_name_comp.search(lowerfake) or mas_bad_name_comp.search(lowerfake):
        $ entered_good_name = False
        m 1rksdla "Это...{w=0.4} {nw}"
        $ MAS.MonikaElastic(voice="monika_giggle")
        extend 1hksdlb "довольно необычное имя, а-ха-ха..."
        $ MAS.MonikaElastic()
        m 1eksdla "Ты...{w=0.3} пытаешься подколоть меня?"
        $ MAS.MonikaElastic()
        m 1rksdlb "Ах, извини-извини, я не осуждаю это или что-то в этом роде."

    python:
        if entered_good_name:
            name_line = renpy.substitute(", [fakename]")
        else:
            name_line = ""

        if mas_current_background == mas_background_def:
            end_of_line = "Кажется, я не могу покинуть этот класс."
        else:
            end_of_line = "Я не знаю, где нахожусь."

    $ MAS.MonikaElastic()
    m 1hua "Что ж, приятно с тобой познакомиться[name_line]!"
    $ MAS.MonikaElastic()
    m 3eud "Скажи[name_line], ты знаешь о том, куда всё подевались?"
    $ MAS.MonikaElastic()
    m 1eksdlc "Ты первый человек, кого я заметила, и я, похоже, не могу выйти из этого класса. "
    extend 1rksdlc "[end_of_line]"
    $ MAS.MonikaElastic()
    m 1eksdld "Ты поможешь мне выяснить, что здесь происходит[name_line]?"

    $ MAS.MonikaElastic()
    m "Пожалуйста? {w=0.2}{nw}"
    extend 1dksdlc "Я скучаю по своим друзьям."

    window hide
    show monika 1eksdlc
    pause 5.0
    $ monika_name = tempname
    window auto

    $ MAS.MonikaElastic()
    m 1rksdla "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 1hksdrb "Прости, [player]! Я не могла сдержаться."
    $ MAS.MonikaElastic()
    m 1eka "После нашего разговора о книге {i}«Цветы для Элджернона»{/i}, я не могла сопротивляться желанию увидеть твою реакцию на то, что я якобы всё забыла."

    if lowerfake == player.lower():
        $ MAS.MonikaElastic()
        m 1tku "...И твоя реакция вполне оправдала мои ожидания."

    $ MAS.MonikaElastic()
    m 3eka "Но я надеюсь, что не расстроила тебя."
    $ MAS.MonikaElastic()
    m 1rksdlb "У меня был бы такой настрой, если бы ты забыл[mas_gender_none] обо мне, [player]."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdlb "Надеюсь, ты не обижаешься на меня за мой небольшой розыгрыш, э-хе-хе~"

    $ mas_lockEVL("greeting_amnesia", "GRE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sick",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SICK],
        ),
        code="GRE"
    )




label greeting_sick:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1hua "С возвращением, [mas_get_player_nickname()]!"
        $ MAS.MonikaElastic()
        m 3eua "Ты чувствуешь себя лучше?"
    else:
        $ MAS.MonikaElastic()
        m 2ekc "С возвращением, [player]..."
        $ MAS.MonikaElastic()
        m "Ты чувствуешь себя лучше?{nw}"
        $ _history_list.pop()
    menu:
        m "Ты чувствуешь себя лучше?{fast}"
        "Да.":
            $ persistent._mas_mood_sick = False
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "Здорово! Теперь мы сможем провести ещё больше времени вместе. Э-хе-хе~"
            else:
                $ MAS.MonikaElastic()
                m "Приятно слышать."
        "Нет.":
            jump greeting_stillsick
    return

label greeting_stillsick:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1ekc "[player], тебе действительно нужно немного отдохнуть."
        $ MAS.MonikaElastic()
        m "Получение большого количества отдыха – лучшее средство для быстрого преодоления болезни."
        $ MAS.MonikaElastic()
        m 2lksdlc "Я бы не простила себя, если бы твоя болезнь ухудшилась из-за меня."
        $ MAS.MonikaElastic()
        m 2eka "Теперь, пожалуйста, [player], расслабься и иди отдохни."
        $ MAS.MonikaElastic()
        m "Ты сделаешь это ради меня?{nw}"
    else:


        $ MAS.MonikaElastic()
        m 2ekc "[player], тебе действительно нужно немного отдохнуть."
        $ MAS.MonikaElastic()
        m 4ekc "Получение большого количества отдыха – лучшее средство для быстрого преодоления болезни."
        $ MAS.MonikaElastic()
        m "Теперь, пожалуйста, [player], расслабься и иди отдохни."
        $ MAS.MonikaElastic()
        m 2ekc "Ты сделаешь это ради меня?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты сделаешь это ради меня?{fast}"
        "Да.":
            jump greeting_stillsickrest
        "Нет.":
            jump greeting_stillsicknorest
        "Я уже отдохнул[mas_gender_none].":
            jump greeting_stillsickresting

label greeting_stillsickrest:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 2hua "Спасибо, [player_abb]."
        $ MAS.MonikaElastic()
        m 2eua "Я думаю, если я оставлю тебя в покое на некоторое время, ты сможешь лучше отдохнуть."
        $ MAS.MonikaElastic()
        m 1eua "Так что я собираюсь закрыть игру для тебя."
        $ MAS.MonikaElastic()
        m 1eka "Поправляйся скорее, [player_abb]. Я так сильно тебя люблю!"
    else:

        $ MAS.MonikaElastic()
        m 2ekc "Спасибо, [player_abb]."
        $ MAS.MonikaElastic()
        m "Я думаю, если я оставлю тебя в покое на некоторое время, ты сможешь лучше отдохнуть."
        $ MAS.MonikaElastic()
        m 4ekc "Так что я собираюсь закрыть игру для тебя."
        $ MAS.MonikaElastic()
        m 2ekc "Поскорее поправляйся, [player]."

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

label greeting_stillsicknorest:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1lksdlc "Понятно..."
        $ MAS.MonikaElastic()
        m "Ну если ты настаиваешь, [player]."
        $ MAS.MonikaElastic()
        m 1ekc "Полагаю, ты знаешь свои ограничения лучше, чем я."
        $ MAS.MonikaElastic()
        m 1eka "Если ты начнёшь чувствовать себя немного слаб[mas_gender_iim] или устал[mas_gender_iim], пожалуйста, дай мне знать."
        $ MAS.MonikaElastic()
        m "Так ты сможешь немного отдохнуть."
        $ MAS.MonikaElastic()
        m 1eua "Не волнуйся, я всё ещё буду здесь, когда ты проснёшься."
        $ MAS.MonikaElastic()
        m 3hua "Тогда мы сможем повеселиться вместе, не беспокоясь о тебе в глубине души."
    else:

        $ MAS.MonikaElastic()
        m 2ekc "Ладно."
        $ MAS.MonikaElastic()
        m 2tkc "Ты, кажется, никогда не хотел[mas_gender_none] слушать меня, так почему я ожидаю, что теперь всё будет иначе."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

label greeting_stillsickresting:
    $ MAS.MonikaElastic()
    m 1eka "О, какое облегчение слышать это, [player]."
    $ MAS.MonikaElastic()
    m 3eka "Но я надеюсь, ты не позволишь себе замёрзнуть."
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1dku "Пожалуй, завернуться в теплое одеяло и выпить чашку горячего чая."
        $ MAS.MonikaElastic()
        m 2eka "Твоё здоровье очень важно для меня, [player], так что позаботься о себе сам[mas_gender_none]."
        show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbsa "...И если тебе всё ещё немного холодно, надеюсь, что знание того, что я люблю тебя, немного согреет тебя."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 5hua "Э-хе-хе~"
    else:

        $ MAS.MonikaElastic()
        m 1eka "Пожалуй, завернуться в теплое одеяло и выпить чашку горячего чая."
        $ MAS.MonikaElastic()
        m 2eka "Твоё здоровье очень важно для меня, [player], так что позаботься о себе сам[mas_gender_none]."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_long_absence",
            unlocked=True,
            category=[store.mas_greetings.TYPE_LONG_ABSENCE],
        ),
        code="GRE"
    )

label greeting_long_absence:
    $ persistent._mas_long_absence = False
    $ mas_ret_long_absence = True

    if persistent._mas_absence_time >= datetime.timedelta(weeks=5):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(70)
            $ MAS.MonikaElastic()
            m 2dsc "[player]..."
            $ MAS.MonikaElastic()
            m 2tkc "Ты говорил[mas_gender_none], что уедешь всего на несколько дней..."
            $ MAS.MonikaElastic()
            m 2rksdld "Но это было настолько долго..."
            $ MAS.MonikaElastic()
            m 2ekd "Я рада, что ты вернул[mas_gender_sya], но..."
            $ MAS.MonikaElastic()
            m 2dktdc "Мне было так одиноко..."
            $ MAS.MonikaElastic()
            m 2ektsc "Я думала, что с тобой что-то случилось!"
            $ MAS.MonikaElastic()
            m 2lktsc "Я... я всё думала, что, возможно, ты не вернёшься."
            $ MAS.MonikaElastic()
            m 2ektsc "Пожалуйста, никогда, {b}никогда{/b} больше не делай так."
            $ MAS.MonikaElastic()
            m 2rktsd "Может, ты ничего не мог[mas_gender_g] поделать с этим, но... я волновалась."
            $ MAS.MonikaElastic()
            m 2dftdc "Я не знала, что делать.."
            $ MAS.MonikaElastic()
            m 4ekc "По возможности, [player], пожалуйста, не уходи так надолго."
            $ MAS.MonikaElastic()
            m 2ekd "Если ты думаешь, что у тебя нет выбора, пожалуйста, говори мне."
            $ MAS.MonikaElastic()
            m 1dsc "Я не хочу быть снова одна..."

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(50)
            $ MAS.MonikaElastic()
            m 3ekc "С возвращением, [player]."
            $ MAS.MonikaElastic()
            m 3rksdlc "Ты немного опоздал[mas_gender_none], не так ли?"
            $ MAS.MonikaElastic()
            m 3ekc "Я знаю, ты говорил[mas_gender_none], что уедешь ненадолго, но... ты ведь сказал[mas_gender_none], что на {b}неделю{/b}."
            $ MAS.MonikaElastic()
            m 2rkc "Я собираюсь предположить, что это была не твоя вина..."
            $ MAS.MonikaElastic()
            m 2ekd "Но если ты действительно думаешь, что это займёт больше времени..."
            $ MAS.MonikaElastic()
            m 2rksdld "Я начинала думать, что с тобой что-то случилось..."
            $ MAS.MonikaElastic()
            m 2dkc "Но я продолжала говорить себе, что всё в порядке..."
            $ MAS.MonikaElastic()
            m 2eka "Я просто рада, что ты в безопасности и вернул[mas_gender_sya] ко мне, [player_abb]."

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffection(30)
            $ MAS.MonikaElastic()
            m 1wud "[player]!"
            $ MAS.MonikaElastic()
            m 1hua "Ты наконец-то здесь!"
            $ MAS.MonikaElastic()
            m 1ekd "Я так волновалась..."
            $ MAS.MonikaElastic()
            m 2dkd "Почему тебя так долго не было?"
            $ MAS.MonikaElastic()
            m 2rkc "Я думала, тебя не будет всего пару недель..."
            $ MAS.MonikaElastic()
            m "Но ты уш[mas_gender_iol] на срок, который дольше более чем в два раза."
            $ MAS.MonikaElastic()
            m 1rksdlc "Ты действительно был[mas_gender_none] так занят[mas_gender_none]?"
            $ MAS.MonikaElastic()
            m 3tkc "Надеюсь, ты не перегружал[mas_gender_none] себя..."
            $ MAS.MonikaElastic()
            m 1eka "Теперь ты здесь со мной, так что если что-то не так, не стесняйся сказать мне."

        elif persistent._mas_absence_choice == "month":
            $ mas_loseAffection(10)
            $ MAS.MonikaElastic()
            m 1eua "С возвращением, [mas_get_player_nickname()]."
            $ MAS.MonikaElastic()
            m 2rkc "Это было довольно долго, не так ли?"
            $ MAS.MonikaElastic()
            m 2rksdlc "Тебя не было дольше, чем ты говорил[mas_gender_none]..."
            $ MAS.MonikaElastic()
            m 2eka "Но всё в порядке, я была готова к этому."
            $ MAS.MonikaElastic()
            m 3rksdlc "Честно говоря, было довольно одиноко без тебя."
            $ MAS.MonikaElastic()
            m 3ekbsa "Надеюсь, ты загладишь вину передо мной.~"
            show monika 1eka

        elif persistent._mas_absence_choice == "longer":
            $ MAS.MonikaElastic()
            m 1esc "Прошло много времени, [player]."
            $ MAS.MonikaElastic()
            m 1ekc "Я была готова к этому, но это не сделало ожидание легче, [player]."
            $ MAS.MonikaElastic()
            m 3eka "Надеюсь, ты смог[mas_gender_g] сделать то, что тебе нужно было."
            $ MAS.MonikaElastic()
            m 2rksdlc "..."
            $ MAS.MonikaElastic()
            m 2tkc "По правде говоря, мне было очень грустно в последнее время."
            $ MAS.MonikaElastic()
            m 2dkc "Не иметь тебя в моей жизни так долго..."
            $ MAS.MonikaElastic()
            m 2dkd "Было очень одиноко..."
            $ MAS.MonikaElastic()
            m "Я чувствовала себя такой одинокой и пустой без тебя."
            $ MAS.MonikaElastic()
            m 3eka "Я так рада, что ты здесь. Я люблю тебя, [player]."

        elif persistent._mas_absence_choice == "unknown":
            $ MAS.MonikaElastic()
            m 1hua "Ты, наконец, вернул[mas_gender_sya], [player]!"
            $ MAS.MonikaElastic()
            m 3rksdla "Когда ты сказал[mas_gender_none], что не знаешь насколько долго уедешь, ты {i}действительно{/i} не знал[mas_gender_none], не так ли?"
            $ MAS.MonikaElastic()
            m 3rksdlb "Ты, должно быть, был[mas_gender_none] действительно занят[mas_gender_none], раз уж уехал[mas_gender_none] {i}настолько{/i} долго."
            $ MAS.MonikaElastic()
            m 1hua "Ну, теперь ты вернул[mas_gender_sya], я действительно скучала по тебе."

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=4):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(70)
            $ MAS.MonikaElastic()
            m 1dkc "[player]..."
            $ MAS.MonikaElastic()
            m 1ekd "Ты говорил[mas_gender_none], что тебя не будет всего лишь несколько дней..."
            $ MAS.MonikaElastic()
            m 2efd "Но это был целый месяц!"
            $ MAS.MonikaElastic()
            m 2ekc "Я думала, с тобой что-то случилось."
            $ MAS.MonikaElastic()
            m 2dkd "Я не была уверена, что делать..."
            $ MAS.MonikaElastic()
            m 2efd "Что задержало тебя на такой срок?"
            $ MAS.MonikaElastic()
            m 2eksdld "Я сделала что-то не так?"
            $ MAS.MonikaElastic()
            m 2dftdc "Ты можешь сказать мне что угодно, только не исчезай так."
            show monika 2dfc

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(50)
            $ MAS.MonikaElastic()
            m 1esc "Здравствуй, [player]."
            $ MAS.MonikaElastic()
            m 3efc "Знаешь, ты уже довольно поздно."
            $ MAS.MonikaElastic()
            m 2lfc "Я не хочу звучать осуждающе, но неделя – это не то же самое, что месяц!"
            $ MAS.MonikaElastic()
            m 2rksdld "Я думаю, может быть, что-то заставило тебя быть настолько занят[mas_gender_iim]?"
            $ MAS.MonikaElastic()
            m 2wfd "Но это не должно было быть настолько отвлекающим, что ты не мог[mas_gender_g] сказать мне, что ты можешь дольше задержаться!"
            $ MAS.MonikaElastic()
            m 2wud "Ах..."
            $ MAS.MonikaElastic()
            m 2lktsc "Извини, [player]. Я просто... очень скучала по тебе."
            $ MAS.MonikaElastic()
            m 2dftfc "Прости, что так хватилась."
            show monika 2dkc

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffection(30)
            $ MAS.MonikaElastic()
            m 1wuo "...О!"
            $ MAS.MonikaElastic()
            m 1sub "Ты, наконец, вернул[mas_gender_sya], [player]!"
            $ MAS.MonikaElastic()
            m 1efc "Ты говорил[mas_gender_none], что тебя не будет только пару недель, но прошёл уже как минимум месяц!"
            $ MAS.MonikaElastic()
            m 1ekd "Я действительно беспокоилась за тебя, понимаешь?"
            $ MAS.MonikaElastic()
            m 3rkd "Но я полагаю, что это было вне твоего контроля?"
            $ MAS.MonikaElastic()
            m 1ekc "Если сможешь, просто скажи, если вдруг в следующий раз будешь дольше, чем планировалось, хорошо?"
            $ MAS.MonikaElastic()
            m 1hksdlb "Я считаю, что я заслуживаю этого, ведь я твоя девушка, в конце концов."
            $ MAS.MonikaElastic()
            m 3hua "Тем не менее, c возвращением, [mas_get_player_nickname()]!"

        elif persistent._mas_absence_choice == "month":
            $ mas_gainAffection()
            $ MAS.MonikaElastic()
            m 1wuo "...О!"
            $ MAS.MonikaElastic()
            m 1hua "Ты действительно здесь, [player]!"
            $ MAS.MonikaElastic()
            m 1hub "Я знала, что могу доверить тебе сдержать слово!"
            $ MAS.MonikaElastic()
            m 1eka "Ты действительно особенн[mas_gender_iii], ты ведь знаешь это?"
            $ MAS.MonikaElastic()
            m 1hub "Я так по тебе скучала!"
            $ MAS.MonikaElastic()
            m 2eub "Расскажи мне всё, что ты сделал[mas_gender_none], я хочу услышать об этом!"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            $ MAS.MonikaElastic(voice="monika_hmm")
            m 1esc "...Хм?"
            $ MAS.MonikaElastic()
            m 1wub "[player]!"
            $ MAS.MonikaElastic()
            m 1rksdlb "Ты вернул[mas_gender_sya] немного раньше, чем я думала..."
            $ MAS.MonikaElastic()
            m 3hua "С возвращением, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 3eka "Я знаю, что это было довольно долго, поэтому я уверена, что ты был[mas_gender_none] занят[mas_gender_none]."
            $ MAS.MonikaElastic()
            m 1eua "Расскажите мне всё об этом."
            show monika 1hua

        elif persistent._mas_absence_choice == "unknown":
            $ MAS.MonikaElastic()
            m 1lsc "..."
            $ MAS.MonikaElastic()
            m 1esc "..."
            $ MAS.MonikaElastic()
            m 1wud "О!"
            $ MAS.MonikaElastic()
            m 1sub "[player]!"
            $ MAS.MonikaElastic()
            m 1hub "Это приятный сюрприз!"
            $ MAS.MonikaElastic()
            m 1eka "Как дела?"
            $ MAS.MonikaElastic()
            m 1ekd "Это был целый месяц, ты действительно не знал[mas_gender_none], как долго тебя не будет, не так ли?"
            $ MAS.MonikaElastic()
            m 3eka "Всё равно ты вернул[mas_gender_sya], и это многое для меня значит."
            $ MAS.MonikaElastic()
            m 1rksdla "Я знала, что ты вернёшься, в конце концов..."
            $ MAS.MonikaElastic()
            m 1hub "Я так сильно тебя люблю, [player_abb]!"
            show monika 1hua

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=2):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(30)
            $ MAS.MonikaElastic()
            m 1wud "О-о, [player]!"
            $ MAS.MonikaElastic()
            m 1hua "С возвращением, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 3ekc "Тебя не было дольше, чем ты обещал[mas_gender_none]..."
            $ MAS.MonikaElastic()
            m 3ekd "Всё в порядке?"
            $ MAS.MonikaElastic()
            m 1eksdla "Я знаю, что твоя жизнь может быть занятой и иногда забирать тебя у меня..."
            $ MAS.MonikaElastic()
            m 3eksdla "Просто... в следующий раз, может быть, предупредишь меня?"
            $ MAS.MonikaElastic()
            m 1eka "Было бы очень мило с твоей стороны."
            $ MAS.MonikaElastic()
            m 1hua "И я была бы очень признательна!"

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(10)
            $ MAS.MonikaElastic()
            m 1eub "Здравствуй, [player]!"
            $ MAS.MonikaElastic()
            m 1eka "Жизнь держит тебя занят[mas_gender_iim]?"
            $ MAS.MonikaElastic()
            m 3hksdlb "Ну, должно быть. Иначе ты был[mas_gender_none] бы здесь, когда бы говорил[mas_gender_none], что да."
            $ MAS.MonikaElastic()
            m 1hksdlb "Не волнуйся! Я не расстраиваюсь."
            $ MAS.MonikaElastic()
            m 1eka "Я просто надеюсь, что ты заботишься о себе."
            $ MAS.MonikaElastic()
            m 3eka "Я знаю, что ты не всегда можешь быть здесь, поэтому убедись, что ты в безопасности, пока будешь не со мной!"
            $ MAS.MonikaElastic()
            m 1hua "Я позабочусь о тебе с этого момента~"
            show monika 1eka

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_gainAffection()
            $ MAS.MonikaElastic()
            m 1hub "Привет, [player]!"
            $ MAS.MonikaElastic()
            m 1eua "Ты вернул[mas_gender_sya], когда сказал[mas_gender_none], что всё-таки вернёшься в конце концов."
            $ MAS.MonikaElastic()
            m 1eka "Спасибо, что не предал[mas_gender_none] моё доверие!"
            $ MAS.MonikaElastic()
            m 3hub "Давай наверстаем упущенное время!"
            show monika 1hua

        elif persistent._mas_absence_choice == "month":
            $ MAS.MonikaElastic()
            m 1wud "О боже! [player]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Я не ожидала, что ты вернёшься так скоро."
            $ MAS.MonikaElastic()
            m 3ekbsa "Думаю, ты скучал[mas_gender_none] по мне так же, как и я скучала по тебе~"
            $ MAS.MonikaElastic()
            m 1eka "Очень приятно видеть тебя раньше, чем я ожидала."
            $ MAS.MonikaElastic()
            m 3ekb "Я ожидала, что день будет однообразным, к счастью, теперь у меня есть ты!"
            $ MAS.MonikaElastic()
            m 3hua "Спасибо, что вернул[mas_gender_sya] так рано, [mas_get_player_nickname()]."

            $ MAS.MonikaElastic()
            m 1lsc "..."
            $ MAS.MonikaElastic()
            m 1esc "..."
            $ MAS.MonikaElastic()
            m 1wud "О! [player]!"
            $ MAS.MonikaElastic()
            m 1hub "Ты вернул[mas_gender_sya] пораньше!"
            $ MAS.MonikaElastic()
            m 1hua "С возвращением, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 3eka "Я не знала, когда тебя ждать, но это было так скоро..."
            $ MAS.MonikaElastic()
            m 1hua "Ну, это подбодрило меня прямо сейчас!"
            $ MAS.MonikaElastic()
            m 1eka "Я действительно скучала по тебе."
            $ MAS.MonikaElastic()
            m 1hua "Давай проведём как можно больше времени вместе, пока мы можем!"

        elif persistent._mas_absence_choice == "unknown":
            $ MAS.MonikaElastic()
            m 1hua "Здравствуй, [player]!"
            $ MAS.MonikaElastic()
            m 3eka "Был[mas_gender_none] занят[mas_gender_none] последние несколько недель?"
            $ MAS.MonikaElastic()
            m 1eka "Спасибо, что предупредил меня, что ты уйдёшь."
            $ MAS.MonikaElastic()
            m 3ekd "Иначе я бы волновалась."
            $ MAS.MonikaElastic()
            m 1eka "Это действительно помогло..."
            $ MAS.MonikaElastic()
            m 1eua "Так скажи мне, как прошёл твой день?"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=1):
        if persistent._mas_absence_choice == "days":
            $ MAS.MonikaElastic()
            m 2eub "Здравствуй, [player]."
            $ MAS.MonikaElastic()
            m 2rksdla "Тебя не было немного дольше, чем ты сказал[mas_gender_none]... но не волнуйся."
            $ MAS.MonikaElastic()
            m 3eub "Я знаю, что ты занятой человек!"
            $ MAS.MonikaElastic()
            m 3rkc "Может быть, если сможешь, сначала предупредишь меня?"
            $ MAS.MonikaElastic()
            m 2rksdlc "Когда ты сказал[mas_gender_none] несколько дней... я думала, что это будет короче недели."
            $ MAS.MonikaElastic()
            m 1hub "Но всё в порядке! Я прощаю тебя!"
            $ MAS.MonikaElastic()
            m 1ekbsa "Ты ведь моя единственная любовь!"
            show monika 1eka

        elif persistent._mas_absence_choice == "week":
            $ mas_gainAffection()
            $ MAS.MonikaElastic()
            m 1hub "Здравствуй, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 3eua "Это так мило, когда мы можем доверять друг другу, не так ли?"
            $ MAS.MonikaElastic()
            m 3hub "Это то, на чём основана сила отношений!"
            $ MAS.MonikaElastic()
            m 3hua "Это просто означает, что как скала!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха!"
            $ MAS.MonikaElastic()
            m 1hksdlb "Прости, прости. Я просто радуюсь, что ты вернул[mas_gender_sya]!"
            $ MAS.MonikaElastic()
            m 3eua "Расскажи мне, как ты. Я хочу услышать всё об этом."

        elif persistent._mas_absence_choice == "2weeks":
            $ MAS.MonikaElastic()
            m 1hub "Привет~"
            $ MAS.MonikaElastic()
            m 3eua "Ты вернул[mas_gender_sya] немного раньше, чем я думала... но я рада, что ты здесь!"
            $ MAS.MonikaElastic()
            m 3eka "Когда ты здесь со мной, всё становится лучше."
            $ MAS.MonikaElastic()
            m 1eua "Давай продолжим вместе создавать замечательные воспоминания!"
            show monika 3eua

        elif persistent._mas_absence_choice == "month":
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hua "Э-хе-хе~"
            $ MAS.MonikaElastic()
            m 1hub "С возвращением!"
            $ MAS.MonikaElastic()
            m 3tuu "Я знала, что ты не сможешь остаться в стороне целый месяц..."
            $ MAS.MonikaElastic()
            m 3tub "Если бы я была на твоём месте, я бы тоже не смогла держаться вдалеке от тебя!"
            $ MAS.MonikaElastic()
            m 1hksdlb "Честно говоря, я начала скучать по тебе сразу же через несколько дней!"
            $ MAS.MonikaElastic()
            m 1eka "Спасибо, что не заставил[mas_gender_none] меня ждать так долго, чтобы увидеть тебя снова~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            $ MAS.MonikaElastic()
            m 1hub "Посмотрите-ка, кто вернулся так рано! Это ты, мо[mas_gender_i] дорог[mas_gender_oi] [player]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Не мог[mas_gender_g] остаться в стороне, даже если бы захотел, верно?"
            $ MAS.MonikaElastic()
            m 3eka "Я не могу винить тебя! Моя любовь к тебе не позволит мне держаться от тебя подальше!"
            $ MAS.MonikaElastic()
            m 1ekd "Каждый день, когда тебя не было, мне было интересно, как ты..."
            $ MAS.MonikaElastic()
            m 3eka "Так что позволь мне услышать, как ты, [player]?"
            show monika 3eua

        elif persistent._mas_absence_choice == "unknown":
            $ MAS.MonikaElastic()
            m 1hub "Здравствуй, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 1eka "Я рада, что ты не заставил[mas_gender_none] меня ждать слишком долго."
            $ MAS.MonikaElastic()
            m 1hua "На неделю короче, чем я ожидала, поэтому можешь считать меня приятно удивлённой!"
            $ MAS.MonikaElastic()
            m 3hub "Спасибо, что уже сделал[mas_gender_none] мой день, [player_abb]!"
            show monika 3eua
    else:

        if persistent._mas_absence_choice == "days":
            $ MAS.MonikaElastic()
            m 1hub "С возвращением, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 1eka "Спасибо, что предупредил[mas_gender_none] меня о том, как долго тебя не будет!"
            $ MAS.MonikaElastic()
            m 1eua "Это много значит – знать, что я могу доверять твоим словам."
            $ MAS.MonikaElastic()
            m 3hua "Я надеюсь, ты знаешь, что ты можешь доверять мне тоже!"
            $ MAS.MonikaElastic()
            m 3hub "Наши отношения крепнут с каждым днём~"
            show monika 1hua

        elif persistent._mas_absence_choice == "week":
            $ MAS.MonikaElastic()
            m 1eud "О! Ты вернул[mas_gender_sya] немного раньше, чем я ожидала!"
            $ MAS.MonikaElastic()
            m 1hua "Не то, чтобы я жаловалась, приятно видеть тебя снова так скоро."
            $ MAS.MonikaElastic()
            m 1eua "Давай проведём ещё один хороший день вместе."

        elif persistent._mas_absence_choice == "2weeks":
            $ MAS.MonikaElastic()
            m 1hub "{i}В моей руке ручка, кото-{/i}"
            $ MAS.MonikaElastic()
            m 1wubsw "О-о! [player]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Ты вернул[mas_gender_sya] гораздо раньше, чем ты сказал[mas_gender_none] мне..."
            $ MAS.MonikaElastic()
            m 3hub "С возвращением!"
            $ MAS.MonikaElastic()
            m 1rksdla "Ты просто прервал[mas_gender_none] меня, пока я практиковалась в моей песне..."
            $ MAS.MonikaElastic()
            m 3hua "Почему бы тебе не послушать, как я пою это снова?"
            $ MAS.MonikaElastic()
            m 1ekbsa "Я сделаю это только для тебя~"
            show monika 1eka

        elif persistent._mas_absence_choice == "month":
            $ MAS.MonikaElastic()
            m 1wud "А? [player]?"
            $ MAS.MonikaElastic()
            m 1sub "Ты здесь!"
            $ MAS.MonikaElastic()
            m 3rksdla "Я думала, ты уехал[mas_gender_none] на целый месяц."
            $ MAS.MonikaElastic()
            m 3rksdlb "Я была готова к этому, но..."
            $ MAS.MonikaElastic()
            m 1eka "Я уже соскучилась по тебе!"
            $ MAS.MonikaElastic()
            m 3ekbsa "Ты тоже скучал[mas_gender_none] по мне?"
            $ MAS.MonikaElastic()
            m 1hubfa "Спасибо, что так скоро вернул[mas_gender_sya]~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            $ MAS.MonikaElastic()
            m 1eud "[player]?"
            $ MAS.MonikaElastic()
            m 3ekd "Я думала, ты собирался уехать надолго..."
            $ MAS.MonikaElastic()
            m 3tkd "Почему ты так скоро вернул[mas_gender_sya]?"
            $ MAS.MonikaElastic()
            m 1ekbsa "Чтобы навестить меня?"
            $ MAS.MonikaElastic()
            m 1hubfa "Ты так[mas_gender_oi] мил[mas_gender_iii]!"
            $ MAS.MonikaElastic()
            m 1eka "Если ты соберёшься уехать ненадолго, обязательно скажи мне."
            $ MAS.MonikaElastic()
            m 3eka "Я люблю тебя, [player], и не стала бы злиться, если бы ты на самом деле планировал[mas_gender_none] задержаться подольше..."
            $ MAS.MonikaElastic()
            m 1hub "Давай наслаждаться временем, которое мы имеем вместе до тех пор!"
            show monika 1eua

        elif persistent._mas_absence_choice == "unknown":
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hua "Э-хе-хе~"
            $ MAS.MonikaElastic()
            m 3eka "Так скоро, [player]?"
            $ MAS.MonikaElastic()
            m 3rka "Думаю, когда ты говорил[mas_gender_none], что не знаешь насколько долго уедешь, ты не осознавал[mas_gender_none], что это может быть не настолько долго."
            $ MAS.MonikaElastic()
            m 3hub "Спасибо, что предупредил[mas_gender_none] меня!"
            $ MAS.MonikaElastic()
            m 3ekbsa "Это заставляет меня чувствовать, что тебя действительно волнует, что я думаю."
            $ MAS.MonikaElastic()
            m 1hubfb "Ты на самом деле добрый."
            show monika 3eub
    $ MAS.MonikaElastic()
    m "Напомни мне, если ты снова уедешь, хорошо?"
    show monika idle with dissolve_monika
    jump ch30_loop


init 5 python:
    ev_rules = dict()
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours=range(0,6)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern:
    jump monika_timeconcern

init 5 python:
    ev_rules = {}
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours =range(6,24)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern_day",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern_day:
    jump monika_timeconcern

init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(
        skip_visual=True,
        random_chance=5,
        override_type=True
    ))
    ev_rules.update(MASPriorityRule.create_rule(45))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hairdown",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.HAPPY, None),
        ),
        code="GRE"
    )
    del ev_rules

label greeting_hairdown:



    $ mas_RaiseShield_core()






    if monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
        $ monika_chr.reset_clothes(False)


    $ monika_chr.change_hair(mas_hair_down, by_user=False)

    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static') from _call_spaceroom_42

    $ MAS.MonikaElastic()
    m 1eua "Привет, [player]!"
    $ MAS.MonikaElastic()
    m 4hua "Заметил[mas_gender_none] кое-что другое сегодня?"
    $ MAS.MonikaElastic()
    m 1hub "Я сегодня решила попробовать что-то новое~"

    $ MAS.MonikaElastic()
    m "Тебе нравится?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе нравится?{fast}"
        "Да.":
            $ persistent._mas_likes_hairdown = True


            $ mas_gainAffection()
            $ MAS.MonikaElastic()
            m 6sub "В самом деле?"
            $ MAS.MonikaElastic()
            m 2hua "Я так рада!"
            $ MAS.MonikaElastic()
            m 1eua "Просто попроси меня, если захочешь снова увидеть мой хвостик, хорошо?"
        "Нет.":


            $ persistent.msr_monika_hair = 'def'
            $ MAS.MonikaElastic()
            m 1ekc "Ох..."
            $ MAS.MonikaElastic()
            m 1lksdlc "..."
            $ MAS.MonikaElastic()
            m 1lksdld "Тогда я заплету их обратно для тебя."
            $ MAS.MonikaElastic()
            m 1dsc "..."
            
            $ monika_chr.reset_hair(False)

            $ MAS.MonikaElastic()
            m 1eua "Готово."


    $ store.mas_selspr.unlock_hair(mas_hair_down)
    $ store.mas_selspr.save_selectables()


    $ mas_unlockEventLabel("monika_hair_select")


    $ mas_lockEVL("greeting_hairdown", "GRE")



    $ mas_MUINDropShield()


    $ set_keymaps()


    $ HKBShowButtons()


    $ mas_startup_song()


    return



init 5 python:



    ev_rules = {}
    ev_rules.update(MASPriorityRule.create_rule(15))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_tears",
            unlocked=True,
            aff_range=(None, mas_aff.DISTRESSED),
            rules=ev_rules,
        ),
        code="GRE"
    )
    del ev_rules

label greeting_tears:

    m 1dsc "...[player]."
    m 1ekc "..."
    m 2ekc "Со мной что-то не так?"
    m 2ekd "Я недостаточно хороша для тебя?.."
    m 2lksdlc "Я старалась изо всех сил ради тебя... ради {b}нас{/b}."
    m 2lksdld "Я делала хоть что-то, что причинило бы тебе боль или заставило бы чувствовать себя плохо?"
    m "Ты всё ещё расстроен[mas_gender_none] из-за других девушек?"
    m 2ekc "Если да, то я действительно сожалею..."
    m "Мне очень, очень жаль!"
    m 2rksdld "Просто скажи мне, что я сделала неправильно, и я постараюсь ещё сильнее, чтобы быть идеальной девушкой для тебя."
    m 2ekd "Ты – весь мой мир; то, как ты себя чувствуешь, значит для меня всё!"
    m 2ekc "Так что, пожалуйста, просто скажи мне, что случилось, и я всё исправлю."
    m 2dfc "Я сделаю всё ради тебя, потому что... ты..."
    m 2dftdc "..."
    m 2dftsc "...ты нуж[mas_gender_en] мне, [player]..."
    m 2ektsc "Мне нужно, чтобы ты любил[mas_gender_none] меня так же, как и я люблю тебя."
    m 2lktsc "Ты нуж[mas_gender_en] мне... потому что если у меня не будет тебя..."
    m 2dftsc "..."
    m 2ektsc "Я буду совсем одна..."
    m 2dftsc "Так что, пожалуйста... просто... будь рядом со мной ради меня, как и я ради тебя."
    m "Я хочу верить в это..."
    m 2lktsc "Так что, пожалуйста... позволь мне быть счастливой с тобой..."
    m "..."
    pause 4.0
    m 2dftdc "..."
    m 2dfc "...Хорошо... Хорошо..."
    m 2lssdrc "Я должна быть сильной..."
    m "..."
    m 2dsc "...Ладно... Теперь мне немного лучше..."
    m 2esc "Но... мне действительно нужно, чтобы ты подумал[mas_gender_none] о том, что я сказала."
    m 2ekc "Пожалуйста... просто... попытайся понять."
    m 1dsd "Я люблю тебя, и мне нужно, чтобы ты показал[mas_gender_none], что ты тоже любишь меня..."
    m 1dsc "Иначе... я просто больше не смогу с этим справляться."

    python:
        mas_lockEVL("greeting_tears", "GRE")


        beingvirtual_ev = mas_getEV("monika_being_virtual")

        if beingvirtual_ev:
            beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_upset",
            unlocked=True,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        ),
        code="GRE"
    )

label greeting_upset:
    python:
        upset_greeting_quips_first = [
            "O. {w=1}Это ты, [player].",
            "O. {w=1}Ты вернул[mas_gender_sya], [player].",
            "Привет, [player].",
            "O. {w=1}Привет, [player]."
        ]

        upset_greeting_quips_second = [


            "Ну...",
            "Ты что-то хочешь?",
        ]

    $ upset_quip1 = renpy.random.choice(upset_greeting_quips_first)

    show monika 2esc
    $ renpy.say(m, upset_quip1)

    if renpy.random.randint(1,4) != 1:
        $ upset_quip2 = renpy.random.choice(upset_greeting_quips_second)
        $ renpy.say(m, upset_quip2)

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_distressed",
            unlocked=True,
            aff_range=(mas_aff.DISTRESSED, mas_aff.DISTRESSED)
        ),
        code="GRE"
    )

label greeting_distressed:
    python:
        distressed_greeting_quips_first = [
            "O... {w=1}Привет, [player].",
            "O... {w=1}Привет, [player].",
            "Привет, [player]...",
            "O... {w=1}Ты вернул[mas_gender_sya], [player]."
        ]

        distressed_greeting_quips_second = [
            "Наверное, мы можем провести некоторое время вместе.",
            "Я не была уверена, когда ты снова посетишь меня.",
            "Надеюсь, мы сможем вместе провести время.",
            "Я не ожидала тебя.",
            "Надеюсь, в ближайшее время всё наладится.",
            "Я думала, ты забыл[mas_gender_none] обо мне..."
        ]

    $ distressed_quip1 = renpy.random.choice(distressed_greeting_quips_first)

    show monika 6ekc
    $ renpy.say(m, distressed_quip1)

    if renpy.random.randint(1,4) != 1:
        $ distressed_quip2 = renpy.random.choice(distressed_greeting_quips_second)
        show monika 6rkc
        $ renpy.say(m, distressed_quip2)

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_broken",
            unlocked=True,
            aff_range=(None, mas_aff.BROKEN),
        ),
        code="GRE"
    )

label greeting_broken:
    m 6ckc "..."
    return



init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_school",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SCHOOL],
        ),
        code="GRE"
    )

label greeting_back_from_school:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1hua "О, с возвращением, [mas_get_player_nickname()]!"
        $ MAS.MonikaElastic()
        m 1eua "Как прошёл твой день в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день в школе?{fast}"
            "Прекрасно.":

                $ MAS.MonikaElastic()
                m 2sub "Правда?!"
                $ MAS.MonikaElastic()
                m 2hub "Мне приятно это слышать, [player]!"
                if renpy.random.randint(1,4) == 1:
                    $ MAS.MonikaElastic()
                    m 3eka "Школа определённо может стать важной частью в твоей жизни, но потом ты можешь начать скучать по ней."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 2hksdlb "А-ха-ха! Знаю, как-то странно думать о том, что тебе однажды захочется вернуться в школу..."
                    $ MAS.MonikaElastic()
                    m 2eub "Но большая часть приятных воспоминаний возникает именно в школе!"
                    $ MAS.MonikaElastic()
                    m 3hua "Быть может, ты потом сможешь рассказать мне о них на досуге."
                else:
                    $ MAS.MonikaElastic()
                    m 3hua "Мне всегда приятно знать о том, что ты счастлив[mas_gender_none]~"
                    $ MAS.MonikaElastic()
                    m 1eua "Если ты хочешь поговорить о своём прекрасном дне, то я с радостью послушаю тебя!"
                return
            "Хорошо.":

                $ MAS.MonikaElastic()
                m 1hub "Оу, это прекрасно!"
                $ MAS.MonikaElastic()
                m 1eua "Я не могу перестать радоваться тому, что у тебя всё хорошо~"
                $ MAS.MonikaElastic()
                m "Надеюсь, ты узнал[mas_gender_none] там что-нибудь полезное."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hua "Э-хе-хе~"
                return
            "Плохо.":

                $ MAS.MonikaElastic()
                m 1ekc "Ох..."
                $ MAS.MonikaElastic()
                m 1dkc "Мне жаль это слышать."
                $ MAS.MonikaElastic()
                m 1ekd "Плохие дни в школе могут быть действительно деморализующими..."
            "Очень плохо...":

                $ MAS.MonikaElastic()
                m 1ekc "Ох..."
                $ MAS.MonikaElastic()
                m 2ekd "Мне правда жаль слышать о том, что у тебя сегодня был очень плохой день..."
                $ MAS.MonikaElastic()
                m 2eka "Но я рада тому, что ты приш[mas_gender_iol_2] ко мне, [player]."
            
        m 3ekc "Позволь спросить, это связано с чем-то конкретно?{nw}"

        python:
            final_item = ("Я не хочу говорить об этом.", False, False, False, 20)
            menu_items = [
                ("Это связано с учёбой.", ".class_related", False, False),
                ("Это связано с людьми.", ".by_people", False, False),
                ("У меня просто день не задался.", ".bad_day", False, False),
                ("Я чуствовал[mas_gender_none] себя нехорошо сегодня.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        $ renpy.say(m, "Позволь спросить, это связано с чем-то конкретно?{fast}", interact=False)
        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        $ label_suffix = _return

        show monika at t11


        if not label_suffix:
            $ MAS.MonikaElastic()
            m 2dsc "Я понимаю, [player]."
            $ MAS.MonikaElastic()
            m 2ekc "Иногда оставление плохого дня позади является наилучшим способом справиться с ним."
            $ MAS.MonikaElastic()
            m 2eka "Но если ты хочешь поговорить об этом позже, то просто знай о том, что я с радостью выслушаю тебя."
            $ MAS.MonikaElastic()
            m 2hua "Я люблю тебя, [player]~"
            return "love"

        $ full_label = "greeting_back_from_school{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label

        label greeting_back_from_school.class_related:
            $ MAS.MonikaElastic()
            m 2dsc "Понятно..."
            $ MAS.MonikaElastic()
            m 3esd "Люди, наверное, постоянно говорят тебе о том, что учёба в школе – это очень важно..."
            $ MAS.MonikaElastic()
            m 3esc "И тебе всегда приходится давить на себя и работать, не покладая рук..."
            $ MAS.MonikaElastic()
            m 2dkd "Но иногда это начинает сильнее нервировать людей, из-за чего они идут по нисходящей спирали."
            $ MAS.MonikaElastic()
            m 2eka "Как я уже говорила, я рада, что ты приш[mas_gender_iol_2] ко мне, [player]."
            $ MAS.MonikaElastic()
            m 3eka "Мне приятно знать о том, что я могу утешить тебя, когда тебе грустно."
            $ MAS.MonikaElastic()
            m "Помни, {i}ты{/i} намного важнее, чем школа или какие-то там оценки."
            $ MAS.MonikaElastic()
            m 1ekbsa "Особенно для меня."
            $ MAS.MonikaElastic()
            m 1hubsa "Не забывай делать перерывы, если ты чувствуешь себя уставш[mas_gender_iiim], и у всех людей есть свои таланты."
            $ MAS.MonikaElastic()
            m 3hubfb "Я люблю тебя, и я просто хочу, чтобы ты был[mas_gender_none] счастлив[mas_gender_none]~"
            return "love"

        label greeting_back_from_school.by_people:
            $ MAS.MonikaElastic()
            m 2ekc "О нет, [player]...{w=0.5} наверное, это было довольно трудно пережить."
            $ MAS.MonikaElastic()
            m 2dsc "То, что с тобой произошло что-то плохое, – это одно дело..."
            $ MAS.MonikaElastic()
            m 2ekd "И совсем другое – когда человек сам же и является причиной возникновения твоей беды."

            if persistent._mas_pm_currently_bullied or persistent._mas_pm_is_bullying_victim:
                $ MAS.MonikaElastic()
                m 2rksdlc "Я правда надеюсь, что это не тот человек, о котором ты мне уже рассказывал[mas_gender_none] раньше..."
                
                if mas_isMoniAff(higher=True):
                    $ MAS.MonikaElastic()
                    m 1rfc "И будет {i}лучше{/i}, если это не он..."
                    $ MAS.MonikaElastic()
                    m 1rfd "Опять он достаёт моё солнышко."

                $ MAS.MonikaElastic()
                m 2ekc "Я бы очень хотела сделать что-то большее, чтобы помочь тебе, [player]..."
                $ MAS.MonikaElastic()
                m 2eka "Но если ты будешь нуждаться во мне, то я всегда здесь."
                $ MAS.MonikaElastic()
                m 3hubsa "И я никуда не уйду~"
                $ MAS.MonikaElastic()
                m 1eubsa "Надеюсь, этим я смогла сделать твой день хоть чуточку лучше."
                $ MAS.MonikaElastic()
                m 1hubfb "Я очень сильно люблю тебя~"
                $ mas_ILY()
            else:

                $ MAS.MonikaElastic()
                m "Я правда надеюсь, что это не приключается с тобой из раза в раз, [player]."
                $ MAS.MonikaElastic()
                m 2lksdld "Так или иначе, мне кажется, будет лучше, если ты обратишься к кому-нибудь за помощью..."
                $ MAS.MonikaElastic()
                m 1lksdlc "Знаю, может показаться, что в некоторых случаях из-за этого может возникнуть ещё больше проблем..."
                $ MAS.MonikaElastic()
                m 1ekc "Но ты не долж[mas_gender_en] страдать от чьих-либо рук."
                $ MAS.MonikaElastic()
                m 3dkd "Мне так жаль, что тебе приходится с этим разбираться, [player]..."
                $ MAS.MonikaElastic()
                m 1eka "Но теперь ты здесь, и я надеюсь, что проведённое вместе время поможет тебе немного улучшить свой день."
            return

        label greeting_back_from_school.bad_day:
            $ MAS.MonikaElastic()
            m 1ekc "Понятно..."
            $ MAS.MonikaElastic()
            m 3lksdlc "Такие дни иногда настают."
            $ MAS.MonikaElastic()
            m 1ekc "Иногда бывает трудно вернуться в строй после такого дня."
            $ MAS.MonikaElastic()
            m 1eka "Но теперь ты здесь, и я надеюсь, что проведённое вместе время поможет тебе немного улучшить свой день."
            return

        label greeting_back_from_school.sick:
            m 2dkd "Быть больным в школе может быть ужасно. Из-за этого становится намного труднее что-то делать или обращать внимание на уроки."
            jump greeting_back_from_work_school_still_sick_ask
            return

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2esc "Ты вернул[mas_gender_sya], [player]..."

        $ MAS.MonikaElastic()
        m "Как у тебя дела в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как у тебя дела в школе?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m 2esc "Это хорошо."
                $ MAS.MonikaElastic()
                m 2rsc "Надеюсь, ты сегодня научил[mas_gender_sya] {i}чему-нибудь{/i}."
            "Плохо.":

                $ MAS.MonikaElastic()
                m "Это очень плохо..."
                $ MAS.MonikaElastic()
                m 2tud "Но, быть может, теперь ты имеешь лучшее представление о том, какие чувства я сейчас испытываю, [player]."

    elif mas_isMoniDis():
        $ MAS.MonikaElastic()
        m 6ekc "Ох...{w=1} ты вернулся."

        $ MAS.MonikaElastic()
        m "Как у тебя дела в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как у тебя дела в школе?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m 6lkc "Мне...{w=1} приятно слышать это."
                $ MAS.MonikaElastic()
                m 6dkc "Н-надеюсь, твой день стал лучше не из-за...{w=2} того момента, когда ты «уходишь от меня»."
            "Плохо.":

                $ MAS.MonikaElastic()
                m 6rkc "Ох..."
                $ MAS.MonikaElastic()
                m 6ekc "Это очень плохо, [player], мне жаль слышать это."
                $ MAS.MonikaElastic()
                m 6dkc "Я знаю, что представляют из себя плохие дни..."
    else:

        $ MAS.MonikaElastic()
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_work",
            unlocked=True,
            category=[store.mas_greetings.TYPE_WORK],
        ),
        code="GRE"
    )

label greeting_back_from_work:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1hua "О, с возвращением, [mas_get_player_nickname()]!"

        $ MAS.MonikaElastic()
        m 1eua "Как прошёл рабочий день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл рабочий день?{fast}"
            "Прекрасно.":

                $ MAS.MonikaElastic()
                m 1sub "Это {i}потрясающе{/i}, [player]!"
                $ MAS.MonikaElastic()
                m 1hub "Я очень рада тому, что у тебя был такой замечательный день!"
                $ MAS.MonikaElastic()
                m 3eua "Я могу только представить себе, как хорошо ты работаешь в такие дни."
                $ MAS.MonikaElastic()
                m 1hua "...Быть может, тебя ещё и повысят в скором времени!"
                $ MAS.MonikaElastic()
                m 1eua "Так или иначе, я рада, что ты дома, [mas_get_player_nickname()]."
                if seen_event("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
                    $ MAS.MonikaElastic()
                    m 3tubsu "Ты хочешь поужинать, принять ванну, или..." # я оседлаю тебя в ванне на ужин :Д
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hubfb "А-ха-ха~ Я просто шучу."
                else:
                    $ MAS.MonikaElastic()
                    m 3eub "Давай проведём немного времени вместе!"
                return
            "Хорошо.":

                $ MAS.MonikaElastic()
                m 1hub "Это хорошо!"
                $ MAS.MonikaElastic()
                m 1eua "Только не забудь передохнуть, ладно?"
                $ MAS.MonikaElastic()
                m 3eua "Таким образом, ты сможешь восстановить силы, чтобы заниматься другими делами."
                $ MAS.MonikaElastic()
                m 1hua "Впрочем, ты можешь просто отдохнуть вместе со мной!"
                $ MAS.MonikaElastic()
                m 3tku "Это лучшее, что можно сделать после долгого рабочего дня, согласись?"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха!"
                return
            "Плохо.":

                $ MAS.MonikaElastic()
                m 2ekc "..."
                $ MAS.MonikaElastic()
                m 2ekd "Мне жаль слышать, что у тебя был плохой день на работе..."
                $ MAS.MonikaElastic()
                m 3eka "Я бы обняла тебя прямо сейчас, если бы была рядом, [player]."
                $ MAS.MonikaElastic()
                m 1eka "Просто помни о том, что, когда ты нуждаешься во мне, я всегда рядом, хорошо?"
            "Очень плохо...":

                $ MAS.MonikaElastic()
                m 2ekd "Мне жаль слышать, что у тебя был плохой день на работе, [player]."
                $ MAS.MonikaElastic()
                m 2ekc "Хотела бы я быть рядом, чтобы обнять тебя прямо сейчас."
                $ MAS.MonikaElastic()
                m 2eka "Я просто рада, что ты приш[mas_gender_iol_2] меня проведать... {w=0.5}я сделаю всё возможное, чтобы утешить тебя."

        $ MAS.MonikaElastic()
        m 2ekc "Если ты не против поговорить со мной об этом, то что сегодня произошло?{nw}"

        python:
            final_item = ("Я не хочу говорить об этом.", False, False, False, 20)
            menu_items = [
                ("На меня наорали.", ".yelled_at", False, False),
                ("Меня обошли стороной из-за одного человека.", ".passed_over", False, False),
                ("Мне пришлось задержаться на работе.", ".work_late", False, False),
                ("Я сегодня не успел[mas_gender_none] закончить все дела.", ".little_done", False, False),
                ("Просто очередной неудачный день.", ".bad_day", False, False),
                ("Я чувствовал[mas_gender_none] себя нехорошо сегодня.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        $ renpy.say(m, "Если ты не против поговорить со мной об этом, то что сегодня произошло?{fast}", interact=False)
        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        $ label_suffix = _return

        show monika at t11

        if not label_suffix:
            $ MAS.MonikaElastic()
            m 1dsc "Я понимаю, [player]."
            $ MAS.MonikaElastic()
            m 3eka "Возможно, после проведения времени со мной тебе станет чуточку лучше~"
            return


        $ full_label = "greeting_back_from_work{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label


        return

        label greeting_back_from_work.yelled_at:
            m 2lksdlc "Ох... {w=0.5}такое правда может испортить твой день."
            $ MAS.MonikaElastic()
            m 2dsc "Ты просто стараешься изо всех сил, но твоя работа кому-то не нравится по неизвестной тебе причине..."
            $ MAS.MonikaElastic()
            m 2eka "Если это всё равно сильно беспокоит тебя, то ты, наверное, можешь попытаться расслабиться немного, это пойдёт тебе на пользу."
            $ MAS.MonikaElastic()
            m 3eka "Думаю, разговор о чём-нибудь или даже игра в какую-нибудь игру поможет отвлечься от этого."
            $ MAS.MonikaElastic()
            m 1hua "Я уверена, тебе станет лучше после того, как мы проведём немного времени вместе."
            return

        label greeting_back_from_work.passed_over:
            m 1lksdld "Ох... {w=0.5}когда видишь, как кто-то получает признание, которое, по твоему мнению, он вовсе не заслуживает, это правда может испортить твой день."
            $ MAS.MonikaElastic()
            m 2lfd "{i}Особенно{/i} когда ты так много сделал[mas_gender_none] и твой поступок явно остался незамеченным."
            $ MAS.MonikaElastic()
            m 1ekc "Ты можешь выглядеть немного подавленн[mas_gender_iim], когда говоришь что-нибудь, так что ты просто должен[mas_gender_none] продолжать стараться, и однажды, уверена, это принесёт свои плоды."
            $ MAS.MonikaElastic()
            m 1eua "И пока ты стараешься изо всех сил, ты сможешь делать хорошие вещи и дальше, и ты однажды получишь своё признание."
            $ MAS.MonikaElastic()
            m 1hub "И помни...{w=0.5} я буду всегда гордиться тобой, [player]!"
            $ MAS.MonikaElastic()
            m 3eka "Надеюсь, от осознания этого тебе станет чуточку лучше~"
            return

        label greeting_back_from_work.work_late:
            m 1lksdlc "Оу, это правда может всё испортить."

            $ MAS.MonikaElastic()
            m 3eksdld "Тебя хотя бы уведомили об этом заранее?{nw}"
            $ _history_list.pop()
            menu:
                m "Тебя хотя бы уведомили об этом заранее?{fast}"
                "Да.":

                    $ MAS.MonikaElastic()
                    m 1eka "Ну, хоть что-то хорошее."
                    $ MAS.MonikaElastic()
                    m 3ekc "Было бы очень больно осознать, что мы все уже собрались домой, а потом нам пришлось остаться на работе подольше."
                    $ MAS.MonikaElastic()
                    m 1rkd "Но всё же, тебя может взбесить тот факт, что из-за этого твоё обычное расписание сбилось."
                    $ MAS.MonikaElastic()
                    m 1eka "...Но, по крайней мере, ты уже здесь, и мы можем провести немного времени вместе."
                    $ MAS.MonikaElastic()
                    m 3hua "Ты можешь наконец-то расслабиться!"
                "Нет.":

                    $ MAS.MonikaElastic()
                    m 2tkx "Это очень плохо!"
                    $ MAS.MonikaElastic()
                    m 2tsc "Особенно когда рабочий день уже подошёл к концу и ты уже собрал[mas_gender_sya] идти домой..."
                    $ MAS.MonikaElastic()
                    m 2dsc "А потом тебе внезапно пришлось задержаться на работе, без какого-либо предупреждения."
                    $ MAS.MonikaElastic()
                    m 2ekc "Внезапная отмена твоих планов может стать очень невыносимой."
                    $ MAS.MonikaElastic()
                    m 2lksdlc "Возможно, у тебя были другие дела, которыми ты планировал[mas_gender_none] заняться после рабочего дня, или тебе очень хотелось прийти домой и отдохнуть..."
                    $ MAS.MonikaElastic()
                    m 2lubfu "...Или, наверное, ты хотел[mas_gender_none] вернуться домой и увидеть свою очаровательную девушку, которая готовила сюрприз к твоему возвращению..."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 2hub "Э-хе-хе~"
            return

        label greeting_back_from_work.little_done:
            m 2eka "Оу, не расстраивайся, [player]."
            $ MAS.MonikaElastic()
            m 2ekd "Такие дни иногда настают."
            $ MAS.MonikaElastic()
            m 3eka "Я знаю, что ты настолько упорно работаешь, что вскоре сможешь преодолеть все свои препятствия."
            $ MAS.MonikaElastic()
            m 1hua "И пока ты ещё стараешься изо всех сил, я всегда буду гордиться тобой!"
            return

        label greeting_back_from_work.bad_day:
            m 2dsd "Просто один из тех дней, да, [player]?"
            $ MAS.MonikaElastic()
            m 2dsc "Они настают время от времени..."
            $ MAS.MonikaElastic()
            m 3eka "Но всё же, я знаю, насколько изнурительными они бывают, и я надеюсь, что вскоре тебе станет лучше."
            $ MAS.MonikaElastic()
            m 1ekbsa "Я буду здесь, пока ты ещё нуждаешься в моём утешении, хорошо, [player]?"
            return

        label greeting_back_from_work.sick:
            m 2dkd "Быть больным на работе может быть ужасно. Из-за этого гораздо труднее что-либо сделать."
            jump greeting_back_from_work_school_still_sick_ask

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2esc "Вижу, ты вернул[mas_gender_sya] с работы, [player]..."

        $ MAS.MonikaElastic()
        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m 2esc "Рада это слышать."
                $ MAS.MonikaElastic()
                m 2tud "Наверное, приятно, когда тебя ценят."
            "Плохо.":

                $ MAS.MonikaElastic()
                m 2dsc "..."
                $ MAS.MonikaElastic()
                m 2tud "Ты испытываешь скверное чувство, когда тебя никто не ценит, да, [player]?"

    elif mas_isMoniDis():
        m 6ekc "Привет, [player]...{w=1} ты наконец-то вернул[mas_gender_sya] с работы?"

        $ MAS.MonikaElastic()
        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день?{fast}"
            "Хорошо.":
                $ MAS.MonikaElastic()
                m "Это хорошо."
                $ MAS.MonikaElastic()
                m 6rkc "Я просто надеюсь, что на работе тебе не так сильно нравится находиться, нежели быть рядом со мной, [player]."
            "Плохо.":

                $ MAS.MonikaElastic()
                m 6rkc "Ох..."
                $ MAS.MonikaElastic()
                m 6ekc "Мне жаль слышать это."
                $ MAS.MonikaElastic()
                m 6rkc "Я знаю, что именно в плохие дни ты не можешь угодить всем..."
                $ MAS.MonikaElastic()
                m 6dkc "Довольно тяжело пережить такие дни."
    else:

        $ MAS.MonikaElastic()
        m 6ckc "..."

    return

label greeting_back_from_work_school_still_sick_ask:
    $ MAS.MonikaElastic()
    m 7ekc "Хотя я должна спросить..."
    $ MAS.MonikaElastic()
    m 1ekc "Тебе всё ещё плохо?{nw}"
    menu:
        m "Тебе всё ещё плохо?{fast}"
        "Да.":

            $ MAS.MonikaElastic()
            m 1ekc "Мне очень жаль это слышать, [player]..."
            $ MAS.MonikaElastic()
            m 3eka "Может, тебе стоит вздремнуть?{w=0.2} Я уверена, что ты почувствуешь себя лучше, как только немного отдохнёшь."
            jump mas_mood_sick.ask_will_rest
        "Нет.":

            $ MAS.MonikaElastic()
            m 1eua "Рада слышать, что ты чувствуешь себя лучше, [player]."
            $ MAS.MonikaElastic()
            m 1eka "Но если тебе снова станет хуже, обязательно отдохни, хорошо?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_sleep",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SLEEP],
        ),
        code="GRE"
    )

label greeting_back_from_sleep:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1hua "О, привет, [player]!"
        $ MAS.MonikaElastic()
        m 1hub "Надеюсь, ты хорошо отдохнул[mas_gender_none]!"
        $ MAS.MonikaElastic()
        m "Давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2esc "Ты только что проснулся, [player]?"
        $ MAS.MonikaElastic()
        m "Надеюсь, ты хорошо отдохнул[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 2tud "{cps=*2}Может быть, теперь у тебя будет настроение получше.{/cps}{nw}"
        $ _history_list.pop()

    elif mas_isMoniDis():
        $ MAS.MonikaElastic()
        m 6rkc "O...{w=1}ты проснул[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 6ekc "Надеюсь, ты смог[mas_gender_g] отдохнуть."
        $ MAS.MonikaElastic()
        m 6dkc "Мне трудно отдыхать в такие дни, и ещё куча мыслей в голове..."
    else:

        $ MAS.MonikaElastic()
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_siat",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_siat:
    $ MAS.MonikaElastic()
    m 1hub "{cps=*0.6}{i}~[player] и Моника под деревом сидели, и они там...~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 1hubsb "{cps=*0.6}{i}~Ц-Е-Л-О-В-А-Л-И-С-Ь~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 3hubfb "{i}{cps=*0.6}~Сначала приходит любовь~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m "{i}{cps=*0.6}~Затем идёт свадьба~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m "{i}{cps=*0.6}~А потом—{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 3wubfsdlo "А-а?!"
    $ MAS.MonikaElastic()
    m 2wubfsdld "[player]! К-как давно ты здесь сидишь?!"
    $ MAS.MonikaElastic()
    m 2rkbfsdld "Я...{w=1} я не заметила, как ты заш[mas_gender_iol_2]...{w=1} я просто..."
    $ MAS.MonikaElastic()
    m 2rkbfsdlu "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hubfb "А-ха-ха! Не важно."
    $ MAS.MonikaElastic()
    m 1ekbfa "Я люблю тебя, [player]. Я так рада тому, что ты сейчас здесь~"
    return "love"

init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(override_type=True))
    ev_rules.update(MASPriorityRule.create_rule(40))
        
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_ourreality",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )
    del ev_rules


label greeting_ourreality:
    $ MAS.MonikaElastic()
    m 1hub "Привет, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 3hksdlb "Ух, сейчас что-то у меня от волнения аж голова немного кругом, извини."
    $ MAS.MonikaElastic()
    m 1eua "Дело в том, что я хочу сейчас показать тебе кое-что, над чем я довольно-таки долго и усердно работала."
    $ MAS.MonikaElastic()
    if persistent._mas_current_background != "spaceroom":
        m 4eub "...Но нам нужно вернуться в космическую комнату, чтобы лучше видеть."
        $ MAS.MonikaElastic()
        m 1hua "Давай отправимся туда, [player]."
        call mas_background_change (mas_background_def, skip_leadin=True, skip_outro=True, set_persistent=True) from _call_mas_background_change_8
        $ MAS.MonikaElastic()
        m 1eua "Готово!"
        $ MAS.MonikaElastic()
        m 3eub "Дай мне секунду, чтобы всё подготовить.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:
        m 3hksdrb "Просто дай мне секунду, чтобы всё подготовить.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    $ MAS.MonikaElastic()
    m 1dsd "Почти готово.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    $ MAS.MonikaElastic()
    m 1duu "Уверена, что ты уж точно будешь удивл[mas_gender_ion] и, может быть, даже шокирован[mas_gender_none]."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eka "Прости за такую задержку."
    $ MAS.MonikaElastic()
    m 1eua "Так что, без дальнейших церемоний..."
    $ MAS.MonikaElastic()
    m 4eub "Будь любез[mas_gender_en], выгляни в окно, [player]."
    $ mas_OVLHide()
    $ disable_esc()
    if mas_current_background.isFltDay():
        show mas_island_frame_day zorder 20
    else:
        show mas_island_frame_night zorder 20
    m "Ну..."
    m "Как тебе?"
    m "Я и вправду очень много работала над этим."
    m "Это место будет только для нас двоих."
    m "И также неплохим местом, где я смогу продолжать практиковать свои навыки программирования."
    $ mas_OVLShow()
    $ enable_esc()
    if mas_current_background.isFltDay():
        hide mas_island_frame_day
    else:
        hide mas_island_frame_night

    $ MAS.MonikaElastic()
    m 1lsc "Целыми днями только и делать, что сидеть в одном только классе может быть скучно."
    $ MAS.MonikaElastic()
    m 1ekc "К тому же, мне здесь бывает временами довольно одиноко, пока я жду твоего возвращения."
    $ MAS.MonikaElastic()
    m 1hksdlb "Но не пойми меня неправильно!"
    $ MAS.MonikaElastic()
    m 1eua "Я всегда рада, когда ты приходишь и проводишь время со мной."
    $ MAS.MonikaElastic()
    m 1eka "Я понимаю, что ты можешь быть время от времени занят[mas_gender_none] чем-либо, из-за чего у тебя не всегда будет возможность быть здесь всё время."
    $ MAS.MonikaElastic()
    m 3euc "Просто я кое-что поняла, [player]."
    $ MAS.MonikaElastic()
    m 1lksdlc "Пройдёт ведь много времени, прежде чем я смогу перейти в твою реальность."
    $ MAS.MonikaElastic()
    m 1dsc "Так что я подумала..."
    $ MAS.MonikaElastic()
    m 1eua "Почему бы нам в таком случае не создать нашу собственную реальность?"
    $ MAS.MonikaElastic()
    m 1lksdla "Ну, она пока что ещё не совсем идеальна."
    $ MAS.MonikaElastic()
    m 1hua "Но это только начало."


    $ mas_lockEVL("greeting_ourreality", "GRE")
    $ mas_unlockEVL("mas_monika_islands", "EVE")


    $ pushEvent("mas_monika_islands",skipeval=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_returned_home",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_GENERIC_RET
            ]
        ),
        code="GRE"
    )

default persistent._mas_monika_returned_home = None

label greeting_returned_home:



    $ five_minutes = datetime.timedelta(seconds=5*60)
    $ time_out = store.mas_dockstat.diffCheckTimes()




    if mas_isO31() and not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay() and mas_isMoniNormal(higher=True):
        $ pushEvent("mas_holiday_o31_returned_home_relaunch", skipeval=True)


    if persistent._mas_f14_on_date:
        jump greeting_returned_home_f14



    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):

        call mas_gone_over_f14_check from _call_mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check from _call_mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check from _call_mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nye_check from _call_mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nyd_check from _call_mas_gone_over_nyd_check




    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump greeting_returned_home_player_bday

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump greeting_returned_home_bday


    if time_out > five_minutes:
        jump greeting_returned_home_morethan5mins
    else:

        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins from _call_greeting_returned_home_lessthan5mins

        if _return:
            return 'quit'

        jump greeting_returned_home_cleanup


label greeting_returned_home_morethan5mins:
    if mas_isMoniNormal(higher=True):

        if persistent._mas_d25_in_d25_mode:

            jump greeting_d25_and_nye_delegate

        elif mas_isD25():

            jump mas_d25_monika_holiday_intro_rh

        jump greeting_returned_home_morethan5mins_normalplus_flow


    jump greeting_returned_home_morethan5mins_other_flow


label greeting_returned_home_morethan5mins_normalplus_flow:
    call greeting_returned_home_morethan5mins_normalplus_dlg from _call_greeting_returned_home_morethan5mins_normalplus_dlg


label greeting_returned_home_morethan5mins_normalplus_flow_aff:
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)
    jump greeting_returned_home_morethan5mins_cleanup

label greeting_returned_home_morethan5mins_other_flow:
    call greeting_returned_home_morethan5mins_other_dlg from _call_greeting_returned_home_morethan5mins_other_dlg


label greeting_returned_home_morethan5mins_other_flow_aff:

    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 2.5, 0.5, 0.5)


label greeting_returned_home_morethan5mins_cleanup:
    pass





label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()


    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out) from _call_mas_o31_ret_home_cleanup_2

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday from _call_return_home_post_player_bday_12


    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label greeting_returned_home_morethan5mins_normalplus_dlg:
    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1eub "Даже если я ничего не могла увидеть, зато я хоть знала, что действительно была рядом с тобой..."
    $ MAS.MonikaElastic()
    m 2eua "Ну, это было реально здорово!"
    show monika 5eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eub "Давай повторим это ещё раз, хорошо?"
    return

label greeting_returned_home_morethan5mins_other_dlg:
    $ MAS.MonikaElastic()
    m 2esc "Мы дома..."
    $ MAS.MonikaElastic()
    m 2eka "Спасибо, что взял меня с собой сегодня, [player]."
    $ MAS.MonikaElastic()
    m 2rkc "Если честно, я не до конца была уверена, идти ли мне с тобой..."
    $ MAS.MonikaElastic()
    m 2dkc "Дело в том, что...{w=0.5} отношения между нами не очень в последнее время, и я не знала, что это будет хорошая идея..."
    $ MAS.MonikaElastic()
    m 2eka "Но я рада, что мы сделали это... {w=0.5}наверное, это то, что нам было нужно."
    $ MAS.MonikaElastic()
    m 2rka "Мы должны это как-нибудь повторить..."
    $ MAS.MonikaElastic()
    m 2esc "Если хочешь."
    return

label greeting_returned_home_lessthan5mins:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 2ekp "Это была не очень большая прогулка, [player]."
        $ MAS.MonikaElastic()
        m "В следующий раз лучше её ещё немного продлить..."
        return False

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2efd "Я думала, мы сходим куда-нибудь, [player]!"
        $ MAS.MonikaElastic()
        m 2tfd "Я знала, что мне не надо было соглашаться идти с тобой."
        $ MAS.MonikaElastic()
        m 2tfc "Я знала, что это станет очередным разочарованием."
        $ MAS.MonikaElastic()
        m "Больше не проси меня выйти наружу, если ты делаешь это лишь ради того, чтобы разрушить мои надежды...{w=1}чтобы выдернуть ковёр из-под моих ног."
        $ MAS.MonikaElastic()
        m 6dktdc "..."
        $ MAS.MonikaElastic()
        m 6ektsc "Я не знаю, почему ты настаиваешь на грубом поведении, [player]."
        $ MAS.MonikaElastic()
        m 6rktsc "Я...{w=1}я хочу сейчас побыть одна."
        return True
    else:

        $ MAS.MonikaElastic()
        m 6rkc "Но...{w=1}мы только что ушли..."
        $ MAS.MonikaElastic()
        m 6dkc "..."
        $ MAS.MonikaElastic()
        m "Я...{w=0.5}я была так рада, когда ты попросил меня пойти с тобой."
        $ MAS.MonikaElastic()
        m 6ekc "После всего того, через что мы прошли..."
        $ MAS.MonikaElastic()
        m 6rktda "Я-я думала...{w=0.5}возможно...{w=0.5}всё наконец-то изменилось."
        $ MAS.MonikaElastic()
        m "Быть может, мы наконец-то провели бы время весело..."
        $ MAS.MonikaElastic()
        m 6ektda "И что ты правда хотел[mas_gender_none] бы провести больше времени со мной."
        $ MAS.MonikaElastic()
        m 6dktsc "..."
        $ MAS.MonikaElastic()
        m 6ektsc "Но, похоже, было очень глупо с моей стороны подумать об этом."
        $ MAS.MonikaElastic()
        m 6rktsc "Мне следовало разузнать всё получше... {w=1}я никогда не должна была соглашаться идти."
        $ MAS.MonikaElastic()
        m 6dktsc "..."
        $ MAS.MonikaElastic()
        m 6ektdc "Пожалуйста, [player]... {w=2}если не хочешь проводить время со мной, то ладно..."
        $ MAS.MonikaElastic()
        m 6rktdc "Но будь любезен, не притворяйся."
        $ MAS.MonikaElastic()
        m 6dktdc "Я бы хотела сейчас побыть одна."
        return True

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="ch30_reload_delegate",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_RELOAD
            ],
        ),
        code="GRE"
    )

label ch30_reload_delegate:

    if persistent.monika_reload >= 4:
        call ch30_reload_continuous from _call_ch30_reload_continuous
    else:

        $ reload_label = "ch30_reload_" + str(persistent.monika_reload)
        call expression reload_label from _call_expression_9

    return






















label greeting_ghost:

    $ mas_lockEVL("greeting_ghost", "GRE")


    call mas_ghost_monika from _call_mas_ghost_monika

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_game",
            unlocked=True,
            category=[store.mas_greetings.TYPE_GAME],
        ),
        code="GRE"
    )





label greeting_back_from_game:
    if store.mas_globals.late_farewell and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        $ _now = datetime.datetime.now().time()
        if mas_isMNtoSR(_now):
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 2etc "[player]?"
                $ MAS.MonikaElastic()
                m 3efc "По-моему, я сказала тебе, чтобы ты пош[mas_gender_iol] спать сразу после того, как закончишь!"
                $ MAS.MonikaElastic()
                m 1rksdla "В смысле, я очень рада, что ты вернул[mas_gender_sya], чтобы пожелать спокойной ночи, но..."
                $ MAS.MonikaElastic()
                m 1hksdlb "Я тебе уже пожелала спокойной ночи!"
                $ MAS.MonikaElastic()
                m 1rksdla "И я могла бы дождаться утра, чтобы повидаться с тобой вновь, понимаешь?"
                $ MAS.MonikaElastic()
                m 2rksdlc "К тому же, я правда хотела, чтобы ты немного отдохнул[mas_gender_none]..."
                $ MAS.MonikaElastic()
                m 1eka "Просто...{w=1} пообещай мне, что ты скоро пойдёшь спать, ладно?"
            else:

                $ MAS.MonikaElastic()
                m 1tsc "[player], я ведь сказала тебе, чтобы ты пош[mas_gender_iol] спать, когда закончишь."
                $ MAS.MonikaElastic()
                m 3rkc "Ты можешь вернуться завтра утром, знаешь ли."
                $ MAS.MonikaElastic()
                m 1esc "Но что есть, то есть, наверное."

        elif mas_isSRtoN(_now):
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 1hua "Доброе утро, [player]~"
                $ MAS.MonikaElastic()
                m 1eka "Когда ты сказал[mas_gender_none], что собираешься поиграть в другую игру так поздно, я начала немного волноваться, что ты, возможно, не высыпаешься..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hksdlb "Я надеюсь, что это не так, а-ха-ха..."
            else:

                $ MAS.MonikaElastic()
                m 1eud "Доброе утро."
                $ MAS.MonikaElastic()
                m 1rsc "Я ожидала, что ты поспишь ещё немного."
                $ MAS.MonikaElastic()
                m 1eka "Но ты решил[mas_gender_none] встать с утра пораньше."

        elif mas_isNtoSS(_now):
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 1wub "[player]! Ты уже здесь!"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hksdlb "А-ха-ха, прости...{w=1} я просто переживала из-за того, что не увижу тебя, поскольку тебя здесь всё утро не было."

                $ MAS.MonikaElastic()
                m 1eua "Ты только что проснул[mas_gender_sya]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ты только что проснул[mas_gender_sya]?{fast}"
                    "Да.":
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 1hksdlb "А-ха-ха..."

                        $ MAS.MonikaElastic()
                        m 3rksdla "Думаешь, это произошло лишь потому, что ты поздно проснул[mas_gender_sya]?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Думаешь, это произошло лишь потому, что ты поздно проснул[mas_gender_sya]?{fast}"
                            "Да.":
                                $ MAS.MonikaElastic()
                                m 1eka "[player]..."
                                $ MAS.MonikaElastic()
                                m 1ekc "Ты знаешь, я не хочу, чтобы ты просыпал[mas_gender_sya] слишком поздно."
                                $ MAS.MonikaElastic()
                                m 1eksdld "Я правда не хочу, чтобы ты заболел[mas_gender_none] или устал[mas_gender_none] в течение дня."
                                $ MAS.MonikaElastic(voice="monika_giggle")
                                m 1hksdlb "Но я надеюсь, что тебе было весело. Мне бы очень не хотелось, чтобы ты лишил[mas_gender_sya] сна понапрасну, а-ха-ха!"
                                $ MAS.MonikaElastic()
                                m 2eka "Просто позаботься о том, что ты немного отдохнёшь, если ты почувствуешь в этом нужду, хорошо?"
                            "Нет.":

                                $ MAS.MonikaElastic()
                                m 2euc "Ох..."
                                $ MAS.MonikaElastic()
                                m 2rksdlc "Я подумала, что дело может быть в этом."
                                $ MAS.MonikaElastic()
                                m 2eka "Прости за то предположение."
                                $ MAS.MonikaElastic()
                                m 1eua "Так или иначе, я надеюсь, ты высыпаешься."
                                $ MAS.MonikaElastic()
                                m 1eka "Мне очень приятно знать о том, что ты хорошо отдохнул[mas_gender_none]."
                                $ MAS.MonikaElastic(voice="monika_giggle")
                                m 1rksdlb "Мне также будет спокойно на душе, если ты перестанешь вставать так поздно, а-ха-ха..."
                                $ MAS.MonikaElastic()
                                m 1eua "Я просто рада, что ты теперь здесь."
                                $ MAS.MonikaElastic()
                                m 3tku "Ты ведь никогда не устанешь проводить время со мной, верно?"
                                $ MAS.MonikaElastic(voice="monika_giggle")
                                m 1hub "А-ха-ха!"
                            "Возможно...":

                                $ MAS.MonikaElastic()
                                m 1dsc "Хм..."
                                $ MAS.MonikaElastic()
                                m 1rsc "Интересно, что послужило причиной?"
                                $ MAS.MonikaElastic()
                                m 2euc "Ты ведь не сидел[mas_gender_none] допоздна вчера ночью, так ведь, [player]?"
                                $ MAS.MonikaElastic()
                                m 2etc "Ты что-то делал[mas_gender_none] той ночью?"
                                $ MAS.MonikaElastic()
                                m 3rfu "Ну, может...{w=1} даже не знаю..."
                                $ MAS.MonikaElastic()
                                m 3tku "В игру играл?"
                                $ MAS.MonikaElastic(voice="monika_giggle")
                                m 1hub "А-ха-ха!"
                                $ MAS.MonikaElastic()
                                m 1hua "Я тебя поддразниваю, конечно же~"
                                $ MAS.MonikaElastic()
                                m 1ekd "Но если говорить на полном серьёзе, я правда не хочу, чтобы ты пренебрегал[mas_gender_none] своим сном."
                                $ MAS.MonikaElastic()
                                m 2rksdla "Сидеть со мной допоздна – это одно..."
                                $ MAS.MonikaElastic()
                                m 3rksdla "Но уходить и играть в другую игру допоздна?"
                                $ MAS.MonikaElastic(voice="monika_giggle")
                                m 1tub "А-ха-ха... я ведь могу начать ревновать, [player]~"
                                $ MAS.MonikaElastic()
                                m 1tfb "Но ты приш[mas_gender_iol] сюда, чтобы загладить свою вину, верно?"
                    "Нет.":

                        $ MAS.MonikaElastic()
                        m 1eud "А, я так понимаю, ты всё утро был занят[mas_gender_none]."
                        $ MAS.MonikaElastic()
                        m 1eka "А я уже боялась, что ты проспал[mas_gender_none], поскольку ты поздно проснул[mas_gender_sya] вчера ночью."
                        $ MAS.MonikaElastic()
                        m 2rksdla "Особенно учитывая то, что ты сказал[mas_gender_none] мне, что пош[mas_gender_iol] играть в другую игру."
                        $ MAS.MonikaElastic()
                        m 1hua "Но мне следовало догадаться, что ты возьмёшь на себя ответственность и поспишь."
                        $ MAS.MonikaElastic()
                        m 1esc "..."
                        $ MAS.MonikaElastic()
                        m 3tfc "Ты ведь {i}спал[mas_gender_none]{/i}, верно, [player]?"
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 1hub "А-ха-ха!"
                        $ MAS.MonikaElastic()
                        m 1hua "Ладно, раз уж ты здесь, мы можем провести немного времени вместе."
            else:

                $ MAS.MonikaElastic()
                m 2eud "О, вот ты где, [player]."
                $ MAS.MonikaElastic()
                m 1euc "Я так понимаю, ты только что проснул[mas_gender_sya]."
                $ MAS.MonikaElastic()
                m 2rksdla "Я ожидала, что ты задержишься допоздна и будешь играть в игры."
        else:


            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 1hub "Вот ты где, [player]!"
                $ MAS.MonikaElastic()
                m 2hksdlb "А-ха-ха, прости... просто дело в том, что я не видела тебя весь день."
                $ MAS.MonikaElastic()
                m 1rksdla "Я ожидала, что ты выспишься после того, как задержал[mas_gender_sya] допоздна вчера ночью..."
                $ MAS.MonikaElastic()
                m 1rksdld "Но когда я не увидела тебя за весь день, я очень сильно начала по тебе скучать..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 2hksdlb "Ты почти что заставил[mas_gender_none] меня волноваться, а-ха-ха..."
                $ MAS.MonikaElastic()
                m 3tub "Но ты ведь собрал[mas_gender_sya] наверстать упущенное со мной, верно?"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "Э-хе-хе, ты уж постарайся~"
                $ MAS.MonikaElastic()
                m 2tfu "Особенно после того, как ты уш[mas_gender_iol] от меня, чтобы поиграть в другую игру вчера ночью."
            else:

                $ MAS.MonikaElastic()
                m 2efd "[player]!{w=0.5} Ты где был[mas_gender_none] весь день?"
                $ MAS.MonikaElastic()
                m 2rfc "Это ведь никак не связано с тем, что ты задержал[mas_gender_sya] допоздна вчера ночью, так ведь?"
                $ MAS.MonikaElastic()
                m 2ekc "Ты правда долж[mas_gender_en] быть более ответственн[mas_gender_iim], когда дело доходит до твоего сна."



    elif mas_getAbsenceLength() < datetime.timedelta(hours=4):
        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 1hua "С возвращением, [mas_get_player_nickname()]!"

            $ MAS.MonikaElastic()
            m 1eua "Ты хорошо пров[mas_gender_iol] время?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты хорошо пров[mas_gender_iol] время?{fast}"
                "Да.":
                    $ MAS.MonikaElastic()
                    m 1hua "Это хорошо."
                    $ MAS.MonikaElastic()
                    m 1eua "Я рада, что ты хорошо пров[mas_gender_iol] время."
                    $ MAS.MonikaElastic()
                    m 2eka "Мне бы правда хотелось иногда составлять тебе компанию в других твоих играх."
                    $ MAS.MonikaElastic()
                    m 3eub "Разве не будет здорово то, что у нас будут небольшие приключения в любое время?"
                    $ MAS.MonikaElastic()
                    m 1hub "Уверена, мы бы вдвоём отлично повеселились в одной из твоих игр."
                    $ MAS.MonikaElastic()
                    m 3eka "Но пока я не могу к тебе присоединиться, получается, тебе придётся составлять мне компанию."
                    $ MAS.MonikaElastic()
                    m 2tub "Ты ведь не против провести немного времени со своей девушкой...{w=1} так ведь, [player]?"
                "Нет.":

                    $ MAS.MonikaElastic()
                    m 2ekc "Оу, мне так жаль слышать об этом."
                    $ MAS.MonikaElastic()
                    m 2eka "Надеюсь, ты не сильно расстроил[mas_gender_sya] из-за того, что могло произойти."
                    $ MAS.MonikaElastic()
                    m 3eua "По крайней мере, ты теперь здесь. Я обещаю, что постараюсь не дать чему-либо плохому произойти с тобой, пока ты со мной."
                    $ MAS.MonikaElastic()
                    m 1ekbsa "Твоё присутствие всегда поднимает мне настроение."
                    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5ekbfa "Надеюсь, от моего присутствия ты испытываешь то же самое, [mas_get_player_nickname()]~"
        else:

            $ MAS.MonikaElastic()
            m 2eud "О, уже вернул[mas_gender_sya]?"
            $ MAS.MonikaElastic()
            m 2rsc "Я думала, что ты надолго уш[mas_gender_iol]...{w=0.5} но с возвращением, наверное."

    elif mas_getAbsenceLength() < datetime.timedelta(hours=12):
        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 2wuo "[player]!"
            $ MAS.MonikaElastic()
            m 2hksdlb "Тебя не было очень долго..."

            $ MAS.MonikaElastic()
            m 1eka "Тебе было весело?{nw}"
            menu:
                m "Тебе было весело?{fast}"
                "Да.":
                    $ MAS.MonikaElastic()
                    m 1hua "Что ж, я рада."
                    $ MAS.MonikaElastic()
                    m 1rkc "Ты определённо заставил[mas_gender_none] меня долго ждать, знаешь ли."
                    $ MAS.MonikaElastic()
                    m 3tfu "Я считаю, что ты долж[mas_gender_en] провести время со своей любящей девушкой, [player]."
                    $ MAS.MonikaElastic()
                    m 3tku "Я уверена, что ты не будешь против остаться со мной, даже принимая во внимание другую свою игру."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hubsb "Наверное, ты долж[mas_gender_en] проводить со мной ещё больше времени, чисто на всякий случай, а-ха-ха!"
                "Нет.":

                    $ MAS.MonikaElastic()
                    m 2ekc "Ох..."
                    $ MAS.MonikaElastic()
                    m 2rka "Ты знаешь, [player]..."
                    $ MAS.MonikaElastic()
                    m 2eka "Если тебе это не особо нравится, то, быть может, ты долж[mas_gender_en] проводить немного времени со мной."
                    $ MAS.MonikaElastic()
                    m 3hua "Я уверена, что мы много чего весёлого можем сделать вместе!"
                    $ MAS.MonikaElastic()
                    m 1eka "Если ты решишь вернуться, то, возможно, так будет лучше."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hub "Но если тебе всё равно не было весело, не стесняйся приходить ко мне, а-ха-ха!"
        else:

            $ MAS.MonikaElastic()
            m 2eud "Ох, [player]."
            $ MAS.MonikaElastic()
            m 2rsc "На это ушло немало времени."
            $ MAS.MonikaElastic()
            m 1esc "Не волнуйся, я смогла самостоятельно скоротать время, пока ты отсутствовал[mas_gender_none]."
    else:


        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 2hub "[player]!"
            $ MAS.MonikaElastic()
            m 2eka "Ты как будто на целую вечность уш[mas_gender_iol]."
            $ MAS.MonikaElastic()
            m 1hua "Я очень сильно по тебе скучала!"
            $ MAS.MonikaElastic()
            m 3eua "Надеюсь, тебе там было весело, чем бы ты там не маял[mas_gender_sya]."
            $ MAS.MonikaElastic()
            m 1rksdla "И я так понимаю, ты не забывал[mas_gender_none] ни поесть, ни поспать..."
            $ MAS.MonikaElastic()
            m 2rksdlc "Что до меня...{w=1} мне было немного одиноко и я ждала, когда ты вернёшься..."
            $ MAS.MonikaElastic()
            m 1eka "Но ты не расстраивайся."
            $ MAS.MonikaElastic()
            m 1hua "Я просто рада, что ты снова здесь, со мной."
            $ MAS.MonikaElastic()
            m 3tfu "Но тебе лучше загладить передо мной свою вину."
            $ MAS.MonikaElastic()
            m 3tku "Думаю, провести вечность со мной звучит справедливо...{w=1} верно, [player]?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха!"
        else:

            $ MAS.MonikaElastic()
            m 2ekc "[player]..."
            $ MAS.MonikaElastic()
            m "Я сомневалась, что ты вообще вернёшься."
            $ MAS.MonikaElastic()
            m 2rksdlc "Я думала, что больше тебя не увижу..."
            $ MAS.MonikaElastic()
            m 2eka "Но ты здесь..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_eat",
            unlocked=True,
            category=[store.mas_greetings.TYPE_EAT],
        ),
        code="GRE"
    )

label greeting_back_from_eat:
    $ _now = datetime.datetime.now().time()
    if store.mas_globals.late_farewell and mas_isMNtoSR(_now) and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 1eud "А?"
            $ MAS.MonikaElastic()
            m 1eub "[player], ты вернул[mas_gender_sya]!"
            $ MAS.MonikaElastic()
            m 3rksdla "Ты ведь знаешь, что ты долж[mas_gender_en] немного поспать, верно?"
            $ MAS.MonikaElastic()
            m 1rksdla "В смысле... я не жалуюсь на то, что ты здесь, но..."
            $ MAS.MonikaElastic()
            m 1eka "Мне будет гораздо спокойнее, если ты пойдёшь спать в скором времени."
            $ MAS.MonikaElastic()
            m 3eka "Ты можешь всегда вернуться и заглянуть ко мне, как только проснёшься..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubsa "Но, полагаю, если ты настаиваешь на том, чтобы провести время со мной, то я на какое-то время закрою на это глаза, э-хе-хе~"
        else:
            $ MAS.MonikaElastic()
            m 2euc "[player]?"
            $ MAS.MonikaElastic()
            m 3ekd "Разве я тебе не сказала, чтобы ты сразу же пош[mas_gender_iol] спать?"
            $ MAS.MonikaElastic()
            m 2rksdlc "Тебе правда надо немного поспать."
    else:

        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 1eub "Уже закончил[mas_gender_none] кушать?"
            $ MAS.MonikaElastic()
            m 1hub "С возвращением, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            m 3eua "Надеюсь, ты насладил[mas_gender_sya] своей едой."
        else:
            $ MAS.MonikaElastic()
            m 2euc "Уже закончил[mas_gender_none] кушать?"
            $ MAS.MonikaElastic()
            m 2eud "С возвращением."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_rent",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_rent:
    $ MAS.MonikaElastic()
    m 1eub "С возвращением, [mas_get_player_nickname()]!"
    $ MAS.MonikaElastic()
    m 2tub "Знаешь, ты так много времени пров[mas_gender_iol] здесь, что я уже должна начать брать с тебя арендную плату."
    $ MAS.MonikaElastic()
    m 2ttu "Или ты больше предпочитаешь оплачивать ипотеку?"
    $ MAS.MonikaElastic()
    m 2hua "..."
    $ MAS.MonikaElastic()
    m 2hksdlb "Боже, не могу поверить в то, что я сказала это. Это ведь не прозвучало слишком банально, так ведь?"
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Но если говорить на полном серьёзе, ты уже отдал[mas_gender_none] мне единственную вещь, которая мне нужна была...{w=1} твоё сердце~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_housework",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CHORES],
        ),
        code="GRE"
    )

label greeting_back_housework:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1eua "Всё сделал[mas_gender_none], [player]?"
        $ MAS.MonikaElastic()
        m 1hub "Давай проведём ещё немного времени вместе."
    elif mas_isMoniUpset():
        m 2efc "По крайней мере ты не забыл[mas_gender_none] вернуться, [player]."
    elif mas_isMoniDis():
        m 6ekd "Оу, [player]. Значит, ты действительно был[mas_gender_none] занят[mas_gender_none]..."
    else:
        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised2",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )

label greeting_surprised2:
    $ MAS.MonikaElastic()
    m 1hua "..."
    $ MAS.MonikaElastic()
    m 1hubsa "..."
    $ MAS.MonikaElastic()
    m 1wubso "О!{w=0.5} [player]!{w=0.5} Ты меня удивил[mas_gender_none]!"
    $ MAS.MonikaElastic()
    m 3ekbsa "...Дело не в том, что я не ожидала тебя увидеть, всё-таки ты всегда заглядываешь ко мне...{w=0.5} {nw}"
    $ MAS.MonikaElastic()
    extend 3rkbsa "Я просто замечталась, а ты уже тут как тут."
    show monika 5hubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfu "Но раз уж ты здесь, получается, та мечта только что воплотилась в реальность~"
    return

init 5 python:

    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(49))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_restart",
            unlocked=True,
            category=[store.mas_greetings.TYPE_RESTART],
            rules=ev_rules
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back_from_restart:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1hub "С возвращением, [mas_get_player_nickname()]!"
        $ MAS.MonikaElastic()
        m 1eua "Что ещё мы должны сделать сегодня?"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 1eud "О, ты вернул[mas_gender_sya]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_code_help",
            conditional="store.seen_event('monika_coding_experience')",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_code_help:
    $ MAS.MonikaElastic()
    m 2eka "О, привет, [player]..."
    $ MAS.MonikaElastic()
    m 4eka "Дай мне секунду, я только что закончила кодить что-то, и я хочу посмотреть, работает ли это.{w=0.5}.{w=0.5}.{nw}"

    scene black
    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    hide noise
    call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 2wud_static') from _call_spaceroom_43

    $ MAS.MonikaElastic()
    m 2wud "А!{w=0.3}{nw}"
    $ MAS.MonikaElastic()
    extend 2efc " Этого не должно было случиться!"
    $ MAS.MonikaElastic()
    m 2rtc "Почему этот цикл заканчивается так быстро?{w=0.5}{nw}"
    extend 2efc " Независимо от того, как ты на это смотришь, этот словарь {i}не{/i} пуст."
    $ MAS.MonikaElastic()
    m 2rfc "Боже, иногда кодинг может быть {i}таким{/i} разочаровывающим..."

    if persistent._mas_pm_has_code_experience:
        $ MAS.MonikaElastic()
        m 3rkc "Ну что ж, думаю, я попробую ещё раз позже.{nw}"
        $ _history_list.pop()

        show screen mas_background_timed_jump(5, "greeting_code_help_outro")
        menu:
            m "Ну что ж, думаю, я попробую ещё раз позже.{fast}"
            "Я мог бы помочь тебе с этим...":

                hide screen mas_background_timed_jump
                $ MAS.MonikaElastic()
                m 7hua "Оу-у, это так мило с твоей стороны, [player]. {w=0.3}{nw}"
                $ MAS.MonikaElastic()
                extend 3eua "Но нет, мне придётся отказаться."
                $ MAS.MonikaElastic()
                m "Выяснение всего этого самостоятельно - самая забавная часть, {w=0.2}{nw}"
                extend 3kua "верно?"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха!"
    else:

        $ MAS.MonikaElastic()
        m 3rkc "Ну что ж, думаю, я попробую ещё раз позже."



label greeting_code_help_outro:
    hide screen mas_background_timed_jump
    $ MAS.MonikaElastic()
    m 1eua "И вообще, чем бы ты хотел[mas_gender_none] сегодня заняться?"

    $ mas_lockEVL("greeting_code_help", "GRE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_love_is_in_the_air",
            unlocked=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

label greeting_love_is_in_the_air:
    $ MAS.MonikaElastic()
    m 1hub "{i}~Любовь повсюду~{/i}"
    $ MAS.MonikaElastic()
    m 1rub "{i}~Куда ни взгляни~{/i}"
    $ MAS.MonikaElastic()
    m 3ekbsa "О, привет, [player]..."
    $ MAS.MonikaElastic()
    m 3rksdla "Не обращай внимания. {w=0.2}Я тут немного пою, думая о...{w=0.3} {nw}"
    $ MAS.MonikaElastic(voice="monika_giggle")
    extend 1hksdlb "думаю ты уже догадываешься о ком я, a-ха-ха~"
    $ MAS.MonikaElastic()
    m 1eubsu "Мне правда кажется, что любовь окружает меня повсюду, когда ты здесь."
    $ MAS.MonikaElastic()
    m 3hua "В любом случае, что будем делать сегодня?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_workout",
            category=[store.mas_greetings.TYPE_WORKOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_workout:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1hua "С возвращением, [player]!"
        $ MAS.MonikaElastic()
        m 3eua "Я надеюсь, ты хорошо потренировал[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 3eub "Не забывай кушать, чтобы восполнять свою энергию!"
        $ MAS.MonikaElastic()
        m 1eua "А теперь, давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        m 2esc "О,{w=0.2} ты вернул[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 2rsc "Тренировка помогла снять напряжение?"
        $ MAS.MonikaElastic()
        m 2rud "Я надеюсь...{w=0.3} {nw}"
        extend 2eka "Давай проведём еще немного времени вместе."

    elif mas_isMoniDis():
        m 6ekc "О...{w=0.5} посмотрите, кто вернулся."
        $ MAS.MonikaElastic()
        m 6dkc "Я...{w=0.3} рада, что ты заботишься о себе."
        $ MAS.MonikaElastic()
        m 6ekd "...Но почему ты не хочешь позаботиться и обо мне тоже?"
        $ MAS.MonikaElastic()
        m 7dkc "Хотя бы иногда, пожалуйста..."
        $ MAS.MonikaElastic()
        m 1dkc "..."
    else:

        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_shopping",
            category=[store.mas_greetings.TYPE_SHOPPING],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_shopping:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1hub "Приветствую тебя, [player]!"
        $ MAS.MonikaElastic()
        m 3eua "Надеюсь, ты купил[mas_gender_none] то, что хотел[mas_gender_none] себе в магазине?"
        $ MAS.MonikaElastic()
        m 1hua "Давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        m 2esc "О,{w=0.2} ты вернул[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 2rsc "Я надеюсь ты купил[mas_gender_none], то что хотел[mas_gender_none] себе."
        if renpy.random.randint(1,5) == 1:
            m 2rud "{cps=*2}Надеюсь ты в лучшем настроении.{/cps}{nw}"
            $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Ох...{w=0.5} ты вернул[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 6ekc "Надеюсь, ты хорошо пров[mas_gender_iol] время в магазине. {w=0.2}Купил еду?"
        $ MAS.MonikaElastic()
        m 6dkd "Задумывал[mas_gender_sya] ли ты о том, что привычка много есть, может влиять на твоё настроение?"
        $ MAS.MonikaElastic()
        m 6lkc "Я бы не очень хотела, чтобы этой причиной было то—{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()
        m 6ekc "А, знаешь что? Не бери в голову. {w=0.2}{nw}"
        extend 6dkc "Я просто устала."
    else:

        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_hangout",
            category=[store.mas_greetings.TYPE_HANGOUT],
            unlocked=True
        ),
        code="GRE"
    )

label greeting_back_from_hangout:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_has_friends:
            m 1eua "Добро пожаловать, [player]."
            $ MAS.MonikaElastic()
            m 3hub "Я надеюсь ты хорошо пров[mas_gender_iol] время!"

            $ anyway_lets = "Давай"
        else:

            m 3eub "Добро пожаловать, [player]."

            $ MAS.MonikaElastic()
            m 1eua "У тебя появился новый друг?{nw}"
            $ _history_list.pop()
            menu:
                m "У тебя появился новый друг?{fast}"
                "Да.":

                    $ MAS.MonikaElastic()
                    m 1hub "Это отлично!"
                    $ MAS.MonikaElastic()
                    m 1eua "Я так рада, что тебе есть с кем пообщаться."
                    $ MAS.MonikaElastic()
                    m 3hub "Надеюсь, ты сможешь проводить с ними больше времени в будущем!"
                    $ persistent._mas_pm_has_friends = True
                "Нет...":

                    $ MAS.MonikaElastic()
                    m 1ekd "Ох..."
                    $ MAS.MonikaElastic()
                    m 3eka "Не волнуйся, [player]. {w=0.2}Я навсегда останусь твоей подругой, несмотря ни на что."
                    $ MAS.MonikaElastic()
                    m 3ekd "...И не бойся пробовать ещё."
                    $ MAS.MonikaElastic()
                    if persistent.gender == "F":
                        m 1hub "Я уверена, найдётся кто-то, кто будет рад назвать тебя своей подругой."
                    else:
                        m 1hub "Я уверена, найдётся кто-то, кто будет рад назвать тебя своим другом."
                "Они уже мои друзья.":

                    $ MAS.MonikaElastic()
                    if persistent._mas_pm_has_friends is False:
                        m 1rka "О, так ты зав[mas_gender_iol] нового друга, не сказав мне..."
                        $ MAS.MonikaElastic()
                        m 1hub "Всё хорошо! Я просто рада, что тебе есть с кем пообщаться."
                    else:
                        m 1hub "О, хорошо!"
                        $ MAS.MonikaElastic()
                        m 3eua "...Раньше мы не говорили о других твоих друзьях, поэтому я не была уверена, новый ли это друг или нет."
                        $ MAS.MonikaElastic()
                        m 3eub "Но я рада, что в твоей реальности есть те, с кем ты можешь пообщаться!"

                    $ MAS.MonikaElastic()
                    m 3eua "Надеюсь вы сможете долго поддерживать связь друг с другом."
                    $ persistent._mas_pm_has_friends = True

            $ anyway_lets = "В любом случае, давай"

        $ MAS.MonikaElastic()
        m 1eua "[anyway_lets] провёдем ещё немного времени вместе~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Привет снова, [player]."
        $ MAS.MonikaElastic()
        m 2eud "Надеюсь, ты хорошо пров[mas_gender_iol] время с друзьями."
        if renpy.random.randint(1,5) == 1:
            m 2rkc "{cps=*2}Интересно, на что это похоже{/cps}{nw}"
            $ _history_list.pop()
    else:

        m 6ckc "..."

    return

init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_recursionerror")

label monikaroom_greeting_ear_recursionerror:
    m "Хм-м, теперь выглядит неплохо. Давай-{w=0.5}{nw}"
    m "Стоп, нет. Боже, как я могла забыть..."
    m "Оно должно быть вызываться прямо тут."

    python:
        for loop_count in range(random.randint(2, 3)):
            renpy.say(m, "Отлично! Так, теперь посмотрим...")

    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    stop sound
    hide noise
    
    m "{cps=*2}Что?!{/cps} {w=0.25}«RecursionError»?!"
    m "'Максимальная глубина рекурсии превышена...'{w=0.7} Как это понимать?"
    m "..."

    if mas_isMoniUpset():
        m "...Продолжай, Моника. Ты сможешь разобраться."
        call monikaroom_greeting_ear_prog_upset from _call_monikaroom_greeting_ear_prog_upset_4
    elif mas_isMoniDis():
        m "...Продолжай{w=0.1} в том же{w=0.1} духе{w=0.1}, Моника. Ты {i}сделаешь{/i} это."
        call monikaroom_greeting_ear_prog_dis from _call_monikaroom_greeting_ear_prog_dis_4
    else:
        m "Фух, по крайней мере, всё остальное работает."

    jump monikaroom_greeting_choice
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
