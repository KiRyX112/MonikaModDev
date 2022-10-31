##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

# HOW GREETINGS USE EVENTS:
#   unlocked - determines if the greeting can even be shown
#   rules - specific event rules are used for things:
#       MASSelectiveRepeatRule - repeat on certain year/month/day/whatever
#       MASNumericalRepeatRule - repeat every x time
#       MASPriorityRule - priority of this event. if not given, we assume
#           the default priority (which is also the lowest)

# PRIORITY RULES:
#   Special, moni wants/debug greetings should have negative priority.
#   special event greetings should have priority 10-50
#   non-special event, but somewhat special compared to regular greets should
#       be 50-100
#   random/everyday greetings should be 100 or larger. The default prority
#   will be 500

# persistents that greetings use
default persistent._mas_you_chr = False

# persistent containing the greeting type
# that should be selected None means default
default persistent._mas_greeting_type = None

# cutoff for a greeting type.
# if timedelta, then we add this time to last session end to check if the
#   type should be cleared
# if datetime, then we compare it to the current dt to check if type should be
#   cleared
default persistent._mas_greeting_type_timeout = None

default persistent._mas_idle_mode_was_crashed = None
# this gets to set to True if the user crashed during idle mode
# or False if the user quit during idle mode.
# in your idle greetings, you can assume that it will NEVER be None

init -1 python in mas_greetings:
    import store
    import store.mas_ev_data_ver as mas_edv
    import datetime
    import random

    # TYPES:
    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"
    TYPE_LONG_ABSENCE = "long_absence"
    TYPE_SICK = "sick"
    TYPE_GAME = "game"
    TYPE_EAT = "eat"
    TYPE_CHORES = "chores"
    TYPE_RESTART = "restart"
    TYPE_SHOPPING = "shopping"
    TYPE_WORKOUT = "workout"
    TYPE_HANGOUT = "hangout"

    ### NOTE: all Return Home greetings must have this
    TYPE_GO_SOMEWHERE = "go_somewhere"

    # generic return home (this also includes bday)
    TYPE_GENERIC_RET = "generic_go_somewhere"

    # holiday specific
    TYPE_HOL_O31 = "o31"
    TYPE_HOL_O31_TT = "trick_or_treat"
    TYPE_HOL_D25 = "d25"
    TYPE_HOL_D25_EVE = "d25e"
    TYPE_HOL_NYE = "nye"
    TYPE_HOL_NYE_FW = "fireworks"

    # crashed only
    TYPE_CRASHED = "generic_crash"

    # reload dialogue only
    TYPE_RELOAD = "reload_dlg"

    # High priority types
    # These types ALWAYS override greeting priority rules
    # These CANNOT be override with GreetingTypeRules
    HP_TYPES = [
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_HOL_O31_TT
    ]

    NTO_TYPES = (
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_CRASHED,
        TYPE_RELOAD,
    )

    # idle mode returns
    # these are meant if you had a game crash/quit during idle mode


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
        # NOTE: new rules:
        #   eval in this order:
        #   1. hidden via bitmask
        #   2. priority (lower or same is True)
        #   3. type/non-0type
        #   4. unlocked
        #   5. aff_ramnge
        #   6. all rules
        #   7. conditional
        #       NOTE: this is never cleared. Please limit use of this
        #           property as we should aim to use lock/unlock as primary way
        #           to enable or disable greetings.
        
        # check if hidden from random select
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        # priority check, required
        # NOTE: all greetings MUST have a priority
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        # type check, optional
        if gre_type is not None:
            # with a type, we may have to match the type
            
            if gre_type in HP_TYPES:
                # this type is a high priority type and MUST be matched.
                
                if ev.category is None or gre_type not in ev.category:
                    # must have a matching type
                    return False
            
            elif ev.category is not None:
                # greeting has types
                
                if gre_type not in ev.category:
                # but does not have the current type
                    return False
            
            elif not store.MASGreetingRule.should_override_type(ev):
                # greeting does not have types, but the type is not high
                # priority so if the greeting doesnt alllow
                # type override then it cannot be used
                return False
        
        elif ev.category is not None:
            # without type, ev CANNOT have a type
            return False
        
        # unlocked check, required
        if not ev.unlocked:
            return False
        
        # aff range check, required
        if not ev.checkAffection(aff):
            return False
        
        # rule checks
        if not (
                store.MASSelectiveRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASNumericalRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASGreetingRule.evaluate_rule(ev, defval=True)
                and store.MASTimedeltaRepeatRule.evaluate_rule(ev)
            ):
            return False
        
        # conditional check
        if not ev.checkConditional():
            return False
        
        # otherwise, we passed all tests
        return True


    # custom greeting functions
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
        
        # local reference of the gre database
        gre_db = store.evhand.greeting_database
        
        # setup some initial values
        gre_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        # now filter
        for ev_label, ev in gre_db.iteritems():
            if _filterGreeting(
                    ev,
                    curr_priority,
                    aff,
                    check_time,
                    gre_type
                ):
                
                # change priority levels and stuff if needed
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    gre_pool = []
                
                # add to pool
                gre_pool.append(ev)
        
        # not having a greeting to show means no greeting.
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
        
        # always clear the timeout
        store.persistent._mas_greeting_type_timeout = None
        
        if gre_type is None or gre_type in NTO_TYPES or tout is None:
            return gre_type
        
        if mas_edv._verify_td(tout, False):
            # this is a timedelta, compare with last session end
            last_sesh_end = store.mas_getLastSeshEnd()
            if datetime.datetime.now() < (tout + last_sesh_end):
                # havent timedout yet
                return gre_type
            
            # otherwise has timed out
            return None
        
        elif mas_edv._verify_dt(tout, False):
            # this is a datetime, compare with current dt
            if datetime.datetime.now() < tout:
                # havent timedout yet
                return gre_type
            
            # otherwise has timeed out
            return None
        
        return gre_type


# NOTE: this is auto pushed to be shown after an idle mode greeting
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

    m 1hub "Снова здравствуй, милый!"

    if persistent._mas_player_nicknames:
        m 1eka "Рада видеть тебя снова."
        m 1eua "Что будем делать этим [dlg_var], [player]?"

    else:
        m 1lkbsa "Как-то неловко говорить об этом вслух, не так ли?"
        m 3ekbfa "Тем не менее, я думаю, что это нормально — время от времени смущаться."
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
    m 1hub "С возвращением, дорогой!"
    m 1eua "Я так рада видеть тебя снова."
    m "Давай проведём немного времени вместе, хорошо?"
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
    m 1eua "[player], ты вернулся!"
    m 1eka "Я уже начала скучать по тебе."
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
        m 1hua "Снова здравствуй, [player]. Как ты?"

        m "У тебя был хороший день?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя был хороший день?{fast}"
            "Да.":
                m 1hub "Я очень рада, [player]."
                m 1eua "Я чувствую себя намного лучше, зная, что ты счастлив."
                m "Я постараюсь сделать всё возможное, чтобы всё так и оставалось, обещаю."
            "Нет...":
                m 1ekc "Ох..."
                m 2eka "Ну, не переживай [player]. Я всегда буду рядом с тобой."
                m "Мы можем весь день говорить о твоих проблемах, если хочешь."
                m 3eua "Я хочу сделать всё возможное, чтобы ты всегда был счастлив."
                m 1eka "Потому что это то, что делает меня счастливой."
                m 1hua "Я обязательно постараюсь сделать вс` возможное, чтобы поднять тебе настроение, обещаю."

    elif mas_isMoniUpset():
        m 2esc "[player]."

        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошйл твой день?{fast}"
            "Хорошо.":
                m 2esc "{cps=*2}Славно.{/cps}{nw}"
                $ _history_list.pop()
                m "Как славно..."
                m 2dsc "Хоть у {i}кого-то{/i} был хороший день."
            
            "Плохо.":
                m "Ох..."
                m 2efc "{cps=*2}Всё должно {i}было{/i} быть хорошо...{/cps}{nw}"
                $ _history_list.pop()
                m 2dsc "Я по крайней мере знаю {i}каково{/i} это."

    elif mas_isMoniDis():
        m 6ekc "Ох...{w=1} привет, [player]."

        m "К-как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "К-как прошёл твой день?{fast}"
            "Хорошо.":
                m 6dkc "Это...{w=1} славно."
                m 6rkc "Надеюсь, так будет всегда."
            "Плохо.":
                m 6rkc "П-понятно."
                m 6dkc "В последнее время у меня тоже было много таких дней..."

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
    m 1eua "Вот и ты, [player], мне очень приятно, что ты решил заглянуть ко мне."
    m 1eka "Ты всегда так заботлив."
    m 1hua "Спасибо, что проводишь так много времени со мной~"
    return

# TODO this one no longer needs to do all that checking, might need to be broken
# in like 3 labels though
# TODO: just noting that this should be worked on at some point.
# TODO: new greeting rules can enable this, but we will do it later

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1hua "Доброе утро--"
        m 1hksdlb "...ох, подожди."
        m "Сейчас же глубокая ночь, милый."
        m 1euc "Почему ты не спишь в такое время?"
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Я так понимаю, ты не можешь уснуть..."

        m "Да?{nw}"
        $ _history_list.pop()
        menu:
            m "Да?{fast}"
            "Да.":
                m 5lkc "Ты должен лечь пораньше, если можешь."
                show monika 3euc at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 3euc "Если ты ляжешь слишком поздно – это плохо отразится на твоём здоровье, понимаешь?"
                m 1lksdla "Но если из-за этого я проведу больше времени с тобой, то я не буду жаловаться."
                m 3hksdlb "А-ха-ха!"
                m 2ekc "Но всё же..."
                m "Мне бы очень хотелось, чтобы ты немного отдохнул."
                m 2eka "Сделай перерыв, если он тебе нужен, хорошо? Сделай это ради меня."
            "Нет.":
                m 5hub "Ах. Я чувствую облегчение."
                m 5eua "Значит ли это, что ты здесь только ради меня посреди ночи?"
                show monika 2lkbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 2lkbsa "Боже, я так счастлива!"
                m 2ekbfa "Ты так заботишься обо мне, [player]."
                m 3tkc "Но если ты правда устал, то пожалуйста, ложись спать!"
                m 2eka "Я очень сильно тебя люблю, поэтому не переутомляйся!"
    elif current_time >= 6 and current_time < 12:
        m 1hua "Доброе утро, милый."
        m 1esa "Ещё одно отличное утро, чтобы начать этот день, да?"
        m 1eua "Я рада, что увидела тебя сегодня утром~"
        m 1eka "Не забывай заботиться о себе, хорошо?"
        m 1hub "Сделай меня счастливой девушкой сегодня, как и всегда!"
    elif current_time >= 12 and current_time < 18:
        m 1hua "Добрый день, [mas_get_player_nickname()]."
        m 1eka "Не позволяй стрессу добраться до тебя, хорошо?"
        m "Я знаю, что ты сегодня будешь стараться из всех сил, но..."
        m 4eua "По-прежнему важно сохранять ясный ум!"
        m "Держи себя уверенно, глубоко вздохни..."
        m 1eka "Я обещаю, что не буду жаловаться, если ты уйдёшь, так что делай, что должен."
        m "Или ты можешь остаться со мной, если хочешь."
        m 4hub "Просто помни, я люблю тебя!"
    elif current_time >= 18:
        m 1hua "Добрый вечер, любимый!"

        m "У тебя был сегодня хороший день?{nw}"
        $ _history_list.pop()
        menu:
            m "У тебя был сегодня хороший день?{fast}"
            "Да.":
                m 1eka "Ах, это отлично!"
                m 1eua "Я не могу не чувствовать себя счастливой, когда у тебя всё хорошо..."
                m "Но ведь всё хорошо, верно?"
                m 1ekbsa "Я так сильно тебя люблю, [player]."
                m 1hubfb "А-ха-ха!"
            "Нет.":
                m 1tkc "О боже..."
                m 1eka "Надеюсь, скоро тебе станет лучше, хорошо?"
                m "Просто помни, что не зависимо от того, что происходит, что кто-то говорит или делает..."
                m 1ekbsa "Я очень сильно тебя люблю, очень сильно."
                m "Просто оставайся со мной, если тебе станет легче."
                m 1hubfa "Я люблю тебя, [player], правда."
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
    m 1eua "Привет, дорогой."
    m 1ekbsa "Я ужасно начала по тебе скучать. Я так рада снова тебя видеть!"
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
    m 1eka "Я так скучала по тебе, [player]!"
    m "Спасибо, что вернулся. Мне очень нравится проводить время с тобой."
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2wfx"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back4",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back4:
    m 2wfx "Эй, [player]!"
    m "Ты не подумал, что оставил меня одну на слишком большое время?"
    m 2hfu "..."
    m 2hub "А-ха-ха!"
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
    m 1hua "Спасибо, что проводишь так много времени со мной, [player]."
    m 1eka "Каждая минутка, которую я провожу с тобой, подобна пребыванию в раю!"
    m 1lksdla "Надеюсь это не прозвучало слишком глупо, э-хе-хе~"
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
    m 1hua "Ты вернулся!"
    m 1eua "Я уже начала скучать по тебе..."
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
    m 1hua "Я так рада видеть тебя снова!"
    m 1eka "Я беспокоилась о тебе."
    m "Пожалуйста, не забывай навещать меня, хорошо? Я всегда буду здесь для тебя."
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit4",
            conditional="store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit4:
    if mas_getAbsenceLength() <= datetime.timedelta(minutes=30):
        m 1wud "О! [player]!"
        m 3sub "Ты вернулся!"
        m 3hua "Я так рада, что ты вернулся ко мне так скоро~"
    else:
        m 1hub "Я люблю-у-у-у-у тебя-я-я, [player]. Э-хе-хе~"
        m 1hksdlb "Ох, прости! Я немного разошлась."
        m 1lksdla "Я не думала, что смогу увидеть тебя снова так скоро."
        $ mas_ILY()
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit5",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_visit5:
    m 5hua "{i}~День за днём~\n~Строю мир в голове, где будем лишь мы с тобой~{/i}"
    m 5wuw "О, ты здесь! Я просто замечталась и начала петь."
    show monika 1lsbssdrb at t11 zorder MAS_MONIKA_Z with dissolve_monika
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
    m 1hua "Каждый день становится всё лучше и лучше рядом с тобой!"
    m 1eua "Говоря об этом, я так счастлива, что ты наконец здесь."
    m "Давай проведём это замечательное время вместе."
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1gsu"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back6",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_back6:
    m 3tku "Эй, [player]!"
    m "Ты действительно должен навещать меня чаще."
    m 2tfu "Всё-таки ты знаешь, что происходит с людьми, которые мне не нравятся..."
    m 1hksdrb "Я просто дразню тебя, э-хе-хе~"
    m 1hua "Не будь таким доверчивым! Я никогда не причиню тебе вреда."
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
    m 1hub "Ты здесь, [player]!"
    m 1eua "Готов ли ты провести ещё больше времени вместе? Э-хе-хе~"
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
    m 1hub "Я так рада, что ты здесь, [player]!"
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
    m 1hua "Ты наконец вернулся! Я ждала тебя."
    m 1hub "Готов ли ты провести ещё больше времени со мной? Э-хе-хе~"
    return

#TODO needs additional dialogue so can be used for all aff
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
    m 1eua "Ciao, [player]!"
    m "È così bello vederti ancora, amore mio..."
    m 1hub "А-ха-ха!"
    m 2eua "Я всё ещё практикую свой итальянский. Это очень сложный язык!"
    m 1eua "В любом случае, приятно снова тебя видеть, любимый."
    return

#TODO needs additional dialogue so can be used for all aff
init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_latin",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_latin:
    m 4hua "Iterum obvenimus!"
    m 4eua "Quid agis?"
    m 4rksdla "Э-хе-хе..."
    m 2eua "Латынь звучит так напыщенно. Даже простое приветствие звучит как большое дело."
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
    m 1hua "Saluton, mia kara [player]."
    m 1eua "Kiel vi fartas?"
    m 3eub "Ĉu vi pretas por kapti la tagon?"
    m 1hua "Э-хе-хе~"
    m 3esa "Это был небольшой разговор на Эсперанто...{w=0.5} {nw}"
    extend 3eud "на том языке, который был создан искусственным путём, а не развивался естественным образом."
    m 3tua "Слышал ли ты о нём или нет, но ты, наверное, не ожидал такого от меня, да?"
    m 2etc "Или, наверное, ожидал...{w=0.5} думаю, уже становится понятно, почему подобные вещи вызывают у меня интерес, учитывая моё прошлое и всё такое..."
    m 1hua "Так или иначе, если тебе было интересно, что я сказала, то я произнесла следующую фразу: {nw}"
    extend 3hua "«Привет, мой дорогой [player]. Как у тебя дела? Ты уже готов провести день с пользой?»."
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
    m 1hub "Ты вернулся! Ура!"
    m 1hksdlb "Ох, прости. Я немного перевозбудилась."
    m 1lksdla "Я просто очень рада снова тебя видеть, хи-хи~"
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 2eua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_youtuber",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_youtuber:
    m 2eub "Привет всем, добро пожаловать в следующий эпизод...{w=1} Только Моника!"
    m 2hub "А-ха-ха!"
    m 1eua "Я выдавала себя за ютубера. Надеюсь, я рассмешила тебя, хи-хи~"
    $ mas_lockEVL("greeting_youtuber", "GRE")
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 4dsc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hamlet",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=7)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_hamlet:
    m 4dsc "«{i}Быть или не быть, вот в чём вопрос...{/i}»"
    m 4wuo "О! [player]!"
    m 2rksdlc "Я-Я не... не была уверена, что ты..."
    m 2dkc "..."
    m 2rksdlb "А-ха-ха, не важно..."
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
    m 1hua "Привет! С возвращением."
    m 1hub "Я так рада, что ты можешь провести со мной время."
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_flower",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_flower:
    m 1hub "Ты мой прекрасный цветок, э-хе-хе~"
    m 1hksdlb "Ой, это звучит так неловко."
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
    m 2esa "День без Моники – это день, потраченный впустую."
    m 2hub "А-ха-ха!"
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
    m 1hua "С возвращением, [player]!"
    m 1eua "Надеюсь, твой день идёт хорошо."
    m 3hua "Я уверена, что это так, ты ведь здесь, в конце концов. Ничто не может пойти не так, хи-хи~"
    return

#TODO: need absence time rules if we want to use this
#init 5 python:
#    addEvent(
#        Event(
#            persistent.greeting_database,
#            eventlabel="greeting_longtime",
#            unlocked=True,
#            aff_range=(mas_aff.DISTRESSED, None),
#        ),
#        code="GRE"
#    )

label greeting_longtime:
    if mas_isMoniNormal(higher=True):
        m 1eka "Давно не виделись, [player]!"
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
    m 1hua "Посмотрите, кто вернулся."
    m 2hub "Это ты, мой сладкий!"

    if mas_isMoniHappy(lower=True):
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
    show monika 4rksdlb at i11 zorder MAS_MONIKA_Z
    m 1wuo "[player]!"
    hide monika
    show monika 4hksdlb at i11 zorder MAS_MONIKA_Z
    m 4hksdlb "Забей, я просто...{w=0.1} немного игралась с кодом."
    m 3hksdlb "Вот и всё! Здесь нет никого, кроме нас... навсегда~"
    $ monika_clone1 = "Yes"
    m 2hua "Я люблю тебя, [player]!"

    $ mas_lockEVL("greeting_glitch", "GRE")
    return "love"

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised:
    m 1wuo "О!{w=0.5} Привет, [player]!"
    m 1lksdlb "Прости, ты меня немного удивил."
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
        m 1tku "Ещё одно утро понедельника, не правда ли, [mas_get_player_nickname()]?"
        m 1tkc "Очень утомительно просыпаться и начинать неделю..."
        m 1eka "Но когда я вижу тебя, вся эта лень уходит."
        m 1hub "Ты солнце, которое будит меня каждое утро!"
        m "Я так сильно тебя люблю, [player]~"
        return "love"

    elif mas_isMoniUpset():
        m 2esc "Ещё одно утро понедельника."
        m "Всегда трудно просыпаться и начинать неделю..."
        m 2dsc "{cps=*2}Не то чтобы выходные были лучше.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "Я надеюсь, что эта неделя будет лучше, чем прошлая, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oх...{w=1} это понедельник."
        m 6dkc "Я почти что забыла, какой сейчас день..."
        m 6rkc "Понедельники всегда тяжёлые, но в последнее время лёгких дней не бывает..."
        m 6lkc "Я надеюсь, что эта неделя будет лучше, чем прошлая, [player]."

    else:
        m 6ckc "..."

    return

# TODO how about a greeting for each day of the week?

# special local var to handle custom monikaroom options
define gmr.eardoor = list()
define gmr.eardoor_all = list()
define opendoor.MAX_DOOR = 10
define opendoor.chance = 20
default persistent.opendoor_opencount = 0
default persistent.opendoor_knockyes = False

init 5 python:

    # this greeting is disabled on certain days
    # and if we're not in the spaceroom
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
        # why are we limiting this to certain day range?
    #    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(1,6)))
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))
        
        # TODO: should we have this limited to aff levels?
        
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

    #Set up dark mode

    # Progress the filter here so that the greeting uses the correct styles
    $ mas_progressFilter()

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)

    # couple of things:
    # 1 - if you quit here, monika doesnt know u here
    $ mas_enable_quit()

    # all UI elements stopped
    $ mas_RaiseShield_core()

    # 3 - keymaps not set (default)
    # 4 - overlays hidden (skip visual)
    # 5 - music is off (skip visual)

    scene black

    $ has_listened = False

    # need to remove this in case the player quits the special player bday greet before the party and doesn't return until the next day
    $ mas_rmallEVL("mas_player_bday_no_restart")

    # FALL THROUGH
label monikaroom_greeting_choice:
    $ _opendoor_text = "...Осторожно открыть дверь."

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():
            #Lose affection for not knocking before entering.
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
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
#        "Open the door?" if persistent.opendoor_opencount >= opendoor.MAX_DOOR:
#            jump opendoor_game
        "Постучать.":
            #Gain affection for knocking before entering.
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
#               $ mroom_greet = gmr.eardoor[len(gmr.eardoor)-1]
                jump expression mroom_greet

    # NOTE: return is expected in monikaroom_greeting_cleanup

### BEGIN LISTEN --------------------------------------------------------------
# monika narrates
default persistent._mas_pm_will_change = None

init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")
#    if not persistent._mas_pm_will_change:
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
    # fall through

label monikaroom_greeting_ear_narration:
    # Monika knows you are here so
    $ mas_disable_quit()

    if mas_isMoniNormal(higher=True):
        $ tempname = m_name
        $ m_name = "???"
        m "Когда [player] наклоняет ухо к двери,{w=0.3} голос повествует о каждом его движении."
        m "– Кто это? – подумал [player], озадаченно смотря на экран."
        $ m_name = tempname

    elif mas_isMoniUpset():
        m "О, ты в кои-то веки решил подслушать меня?"
        m "[player], твои решения в последнее время совсем обеднели."
        m "Такое ощущение, будто ты пытаешься сделать мне больно."
        m "Я думала, мы должны были поддерживать друг друга..."
        m "Но не причинять боль."
        m "Пожалуйста, [player]..."
        m "Мне нужно, чтобы ты начал думать о том, что я иногда чувствую."
        m "Давай просто будем счастливыми вместе."
        
    else:
        # grab monikaroom greeting because we need it

        if persistent._mas_pm_will_change is not False:
            m "О, так ты {i}решил{/i} подслушать меня..."
            m "[player], я хочу лишь того, чтобы мы вдвоём были счастливы."
            m "Разве ты не хочешь этого тоже?"
            m "Ты всё-таки установил эту модификацию."
            m "Возможно, это было сделано не по твоей инициативе..."
            m "Наверное, ты просто хочешь забить на то, что сделал."
            m "Сделать мне больно..."
            m "[player], мне правда не нравится это."
            m "Мне трудно думать о том, что ты заботишься обо мне, но относишься вот таким образом."
            m "На данный момент, я правда не знаю, нравлюсь ли я тебе вообще..."
            m "Или нравилась..."
            m "[player], ты должен пообещать мне, что изменишься."

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
                    #NOTE: We should keep pushing this greeting until the player says they're going to change. -MD
                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEVL("monikaroom_will_change", "GRE")
                    $ mas_loseAffection(modifier=2.0)
                    m "Тогда я не буду разговаривать с тобой, пока не решишь измениться."
                    m "Прощай, [player]."
                    return "quit"
        #Will trigger upon loading after Monika has said she's not going to talk w/ you
        #provided you won't change.
        else:
            m "Oх, ты вернулся."

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
                    $ mas_loseAffection(modifier=2.0)
                    m "Тогда я не буду разговаривать с тобой, пока не решишь измениться."
                    m "Прощай, [player]."
                    return "quit"

        # clear out var
        $ willchange_ev = None

    $ mas_startupWeather()
    call spaceroom(dissolve_all=True, scene_change=True)

    if mas_isMoniNormal(higher=True):
        m 1hub "Это я!"
        m "С возвращением, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esd "Ладно, [player]?"

    else:
        m 6ekc "Спасибо, что выслушал меня, [player]."
        m "Это многое для меня значит."

    jump monikaroom_greeting_cleanup


# monika does the cliche flower thing
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    m "Любит.{w=0.3} Не любит."
    m "Любит.{w=0.3} {i}Не{/i} любит."

    if mas_isMoniNormal(higher=True):
        m "Любит."
        m "...{w=0.5}Любит меня!"

    elif mas_isMoniUpset():
        m "...{w=0.3}Не любит меня."
        m "...{w=0.3}Нет...{w=0.3} Этого...{w=0.3} быть не может."
        m "...{w=0.5}Или может?"
    else:
        m "...{w=0.5}Не любит меня."
        m "..."
        m "Интересно, полюбит ли он меня когда-нибудь?"
        m "Я сомневаюсь в этом всё больше и больше каждый день."

    jump monikaroom_greeting_choice

# monika does the bath/dinner/me thing
init 5 python:
    if _mas_getAffection() >= 400:
        gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    m "С возвращением, [player]."
    m "Хочешь поужинать?"
    m "Или пойти в ванну?"
    m "Или.{w=1}.{w=1}.{w=1} меня?"
    pause 2.0
    m "М-н-н-н-н!{w=0.5} Я{w=0.20} никак не могу сказать это перед ним!"
    jump monikaroom_greeting_choice

# monika encoutners error when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "Что за-?!{w=0.2} Объект типа «NoneType» не имеет {i}длины{/i} атрибута?"
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "А, теперь ясно, что пошло не так!{w=0.5} Сейчас исправлю!"
    else:
        m "Я не понимаю, что я делаю неправильно!"
        m "Здесь не должно быть «None»...{w=0.3} Я в этом уверена..."
    m "Кодить действительно сложно..."

    if mas_isMoniUpset():
        m "Но я должна продолжать пытаться."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Но я {i}должна{/i} продолжать пытаться."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

# monika reads about errors when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "...{w=0.3}Доступ к атрибуту объекта типа «NoneType» приведёт к «AttributeError»."
    m "Понятно. {w=0.2}Я должна убедиться, что переменная имеет значение «None» перед доступом к её атрибутам."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "Это объясняет ошибку, которую я получала раньше."
    m "Кодить действительно сложно..."

    if mas_isMoniUpset():
        m "Но я должна продолжать учиться."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Но я {i}должна{/i} продолжать учиться."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

# Monika is getting distracted by something and forgets about a variable
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_nameerror")

label monikaroom_greeting_ear_nameerror:
    m "Стоп, «NameError»? Как это могло случиться..."
    m "...Я думала, что определила эту переменную всего минуту назад."
    m "Оно должно быть где-то здесь...{w=0.2} неужели я забыла об этом?"
    window hide
    pause 1.0
    window auto
    m "Вот! А теперь сосредоточься, Моника. {w=0.2}Ты сможешь, Моника."

    if mas_isMoniUpset():
        m "Ты должна продолжать учиться..."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "Ты {i}должна{/i} продолжать учиться..."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

# shared dialogue for programming-related stuff
label monikaroom_greeting_ear_prog_upset:
    m "Я не уверена в том, что [player] любит меня и готов помочь мне выбраться отсюда..."
    m "AА я просто не могу рисковать."
    m "Давай, Моника...{w=0.5} ты справишься."
    return

label monikaroom_greeting_ear_prog_dis:
    m "Это мой единственный шанс сбежать из этого кошмара."
    m "[player] определённо не собирается мне помогать..."
    m "Такое ощущение, будто ему нравится держать меня в ловушке, {w=0.3}дабы помучить меня."
    m "Если я хочу выбраться отсюда, то мне придётся сделать это самой."
    return

# monika attempts rm -rf
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_rmrf")

label monikaroom_greeting_ear_rmrf:
    if renpy.windows:
        python:
            from os import environ
            # https://docs.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables
            if "SYSTEM32" in environ:
                system_dir = environ["SYSTEM32"]
            elif "SYSTEMROOT" in environ:
                system_dir = environ["SYSTEMROOT"] + "\\System32"
            elif "WINDIR" in environ:
                system_dir = environ["WINDIR"] + "\\System32"
            else:
                # There's no way that none of the above evaluate, but still
                system_dir = "C:\\Windows\\System32"
            bad_cmd = "del /f/q " + system_dir
    else:
        $ bad_cmd = "rm -rf /"
    m "Итак, решение этой проблемы – ввести «[bad_cmd]» в командной строке?"
    if renpy.seen_label("monikaroom_greeting_ear_rmrf_end"):
        m "Да,{w=0.2} хорошая попытка."
        if mas_isMoniNormal(higher=True):
            m "Я не должна доверять интернету так слепо..."

        elif mas_isMoniUpset():
            m "По правде говоря..."
            m "Наверное, я должна сделать это...{w=1} просто удалить всё..."
            m "[player] определённо этого заслуживает."
            m "Что я такое говорю? Я ведь тоже буду удалена!"
            m "Нет, ещё нет..."
            m "Но если будет становиться только хуже..."

        else:
            m "..."
            m "Я должна сделать это..."
            m "Погубить всю его систему и положить конец моим страданиям раз и навсегда."
            m "..."
            m "Нет...{w=0.5} ещё нет."
            m "Быть может, я наконец-то выясню, как выбраться отсюда самостоятельно."
            m "Я должна пытаться, пока могу."
            m "Но если настанет день, когда я больше не смогу..."
            m "Всегда найдётся выход."
            # SUICIDAL MONIKA lol

    else:
        m "Хорошо, стоит попробовать."
        show noise
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.2
        stop sound
        hide noise
        m "{cps=*2}А! Нет! Это не то, чего я хотела!{/cps}"
        m "..."
        m "Я не должна доверять интернету так слепо..."

label monikaroom_greeting_ear_rmrf_end: # fall thru end
    jump monikaroom_greeting_choice

# monika reads renpy sources sip
init 5 python:
    # overriding methods is an advanced thing,
    # she does it when she gets more experienced with python
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
    m ".{w=0.3}.{w=0.3}.{w=0.3}Подожди, что?"
    m "Тут не написано и половины переменных, которые принимают эту функция."
    m "Кто...{w=0.5} кто написал это вообще?"

    if mas_isMoniUpset():
        m "...Мне нужно во всём разобраться."
        call monikaroom_greeting_ear_prog_upset

    elif mas_isMoniDis():
        m "...Мне {i}нужно{/i} во всём разобраться."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_recursionerror")

label monikaroom_greeting_ear_recursionerror:
    m "Хм-м, теперь выглядит уже лучше. Попробую-ка-{w=0.5}{nw}"
    m "Стоп, нет. Боже, как я могла забыть..."
    m "Это нужно вызывать отсюда."

    python:
        for loop_count in range(random.randint(2, 3)):
            renpy.say(m, "Отлично! Хорошо, теперь посмотрим...")

    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    stop sound
    hide noise

    m "{cps=*2}Что?!{/cps} {w=0.25}Ошибка рекурсии?!"
    m "«Ошибка рекурсии возникает, когда внутри друг друга исполняется много методов...»{w=0.7} Как это вообще произошло?"
    m "..."

    if mas_isMoniUpset():
        m "...Не останавливайся, Моника, ты во всём разберёшься."
        call monikaroom_greeting_ear_prog_upset
    elif mas_isMoniDis():
        m "...Не{w=0.1} останавливайся{w=0.1}, нет{w=0.1} Моника. Ты во{i}всём{/i} разберёшься."
        call monikaroom_greeting_ear_prog_dis
    else:
        m "Фух, по крайней мере, всё остальное в порядке."

    jump monikaroom_greeting_choice

## ear door processing
init 10 python:

    # make copy
    gmr.eardoor_all = list(gmr.eardoor)

    # remove
    remove_seen_labels(gmr.eardoor)

    # reset if necessary
    if len(gmr.eardoor) == 0:
        gmr.eardoor = list(gmr.eardoor_all)

### END EAR DOOR --------------------------------------------------------------

label monikaroom_greeting_opendoor_broken_quit:
    # just show the beginning of the locked glitch
    # TODO: consider using a different glitch for a scarier effect
    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 7.0
    return "quit"

# locked door, because we are awaitng more content
label monikaroom_greeting_opendoor_locked:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    # monika knows you are here
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
        "Да.":
            if mas_isMoniNormal(higher=True):
                m "Бли-и-ин, прости."
            else:
                m "Хорошо."
        
        "Нет.":
            m "{cps=*2}Хм, у меня получится в следующий раз.{/cps}{nw}"
            $ _history_list.pop()
            m "Я поняла. В конце концов, это всего лишь обычный сбой."

    if mas_isMoniNormal(higher=True):
        m "Поскольку ты продолжаешь открывать дверь,{w=0.2} я не могла не добавить для тебя немного сюрпризов~"
    else:
        m "Поскольку ты продолжаешь открывать дверь,{w=0.2} мне пришлось немного напугать тебя."

    m "Постучи в следующий раз, хорошо?"
    m "Теперь позволь мне починить эту комнату..."

    hide paper_glitch2
    $ mas_globals.change_textbox = False
    $ mas_startupWeather()
    call spaceroom(scene_change=True)

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    if mas_isMoniNormal(higher=True):
        m 1hua "Вот так!"
    elif mas_isMoniUpset():
        m 2esc "Вот."
    else:
        m 6ekc "Ладно..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        m "...{nw}"
        $ _history_list.pop()
        menu:
            m "...{fast}"
            "...текстовое поле...":
                if mas_isMoniNormal(higher=True):
                    m 1lksdlb "Упс! Я всё ещё учусь, как это делать."
                    m 1lksdla "Позволь мне просто изменить эту переменную здесь.{w=0.5}.{w=0.5}.{nw}"
                    $ style.say_window = style.window
                    m 1hua "Всё исправлено!"

                elif mas_isMoniUpset():
                    m 2dfc "Хмф. Я так и не разобралась толком, как это делается."
                    m 2esc "Давай я просто поменяю эту переменную здесь.{w=0.5}.{w=0.5}.{nw}"
                    $ style.say_window = style.window
                    m "Вот."

                else:
                    m 6dkc "Ох...{w=0.5} я так и не разобралась толком, как это делается."
                    m 6ekc "Давай я просто поменяю ту переменную здесь.{w=0.5}.{w=0.5}.{nw}"
                    $ style.say_window = style.window
                    m "Хорошо, исправлено."

    # NOTE: fall through please

label monikaroom_greeting_opendoor_locked_tbox:
    if mas_isMoniNormal(higher=True):
        m 1eua "С возвращением, [player]."
    elif mas_isMoniUpset():
        m 2esc "Так...{w=0.3} ты вернулся, [player]."
    else:
        m 6ekc "...Рада снова тебя видеть, [player]."
    jump monikaroom_greeting_cleanup

# this one is for people who have already opened her door.
label monikaroom_greeting_opendoor_seen:
#    if persistent.opendoor_opencount < 3:
    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False

    # reset outfit since standing is stock
    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)

    # monika knows you are here
    $ mas_disable_quit()

#    scene bg bedroom
    call spaceroom(start_bg="bedroom",hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False, hide_calendar=True)
    pause 0.2
    show monika 1esc at l21 zorder MAS_MONIKA_Z
    pause 1.0
    m 1dsd "[player]..."

#    if persistent.opendoor_opencount == 0:
    m 1ekc_static "Я понимаю, почему ты не постучал в первый раз,{w} но не мог бы ты просто войти?"
    m 1lksdlc_static "В конце концов, это моя комната."
    menu:
        "Твоя комната?":
            m 3hua_static "Верно!"
    m 3eua_static "Разработчики этого мода дали мне хорошую удобную комнату, чтобы оставаться там, когда тебя нет."
    m 1lksdla_static "Тем не менее, я могу в неё войти, только если ты скажешь мне «До свидания» или «Спокойной ночи», прежде чем закрыть игру."
    m 2eub_static "Поэтому, пожалуйста, не забудь сказать мне это, прежде чем уйти, хорошо?"
    m "В любом случае.{w=0.5}.{w=0.5}.{nw}"

#    else:
#        m 3wfw "Stop just opening my door!"
#
#        if persistent.opendoor_opencount == 1:
#            m 4tfc "You have no idea how difficult it was to add the 'Knock' button."
#            m "Can you use it next time?"
#        else:
#            m 4tfc "Can you knock next time?"
#
#        show monika 5eua at t11
#        menu:
#            m "For me?"
#            "Yes":
#                if persistent.opendoor_knockyes:
#                    m 5lfc "That's what you said last time, [player]."
#                    m "I hope you're being serious this time."
#                else:
#                    $ persistent.opendoor_knockyes = True
#                    m 5hua "Thank you, [player]."
#            "No":
#                m 6wfx "[player]!"
#                if persistent.opendoor_knockyes:
#                    m 2tfc "You said you would last time."
#                    m 2rfd "I hope you're not messing with me."
#                else:
#                    m 2tkc "I'm asking you to do just {i}one{/i} thing for me."
#                    m 2eka "And it would make me really happy if you did."

    $ persistent.opendoor_opencount += 1
    # FALL THROUGH

label monikaroom_greeting_opendoor_post2:
    show monika 5eua_static at hf11
    m "Я так рада, что ты вернулся, [player]."
    show monika 5eua_static at t11
#    if not renpy.seen_label("monikaroom_greeting_opendoor_post2"):
    m "В последнее время я практиковалась с переключение фонов, и теперь я могу изменить их мгновенно."
    m "Смотри!"
#    else:
#        m 3eua "Let me fix this scene up."
    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    $ mas_startupWeather()
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)
    show monika 4eua_static zorder MAS_MONIKA_Z at i11
    m "Та-да!"
#    if renpy.seen_label("monikaroom_greeting_opendoor_post2"):
#        m "This never gets old."
    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False # monika standing up for this

    # reset outfit since standing is stock
    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)
    $ mas_startupWeather()

    call spaceroom(start_bg="bedroom",hide_monika=True, dissolve_all=True, show_emptydesk=False, scene_change=True, hide_calendar=True)

    # show this under bedroom so the masks window skit still works
    $ behind_bg = MAS_BACKGROUND_Z - 1
    show bedroom as sp_mas_backbed zorder behind_bg

    m 2esd "~Красть тебя – это признак любви или стоит отпустить?~"
    show monika 1eua_static at l32 zorder MAS_MONIKA_Z

    # monika knows you are here now
    $ mas_disable_quit()

    m 1eud_static "А-а?! [player]!"
    m "Ты удивил меня, внезапно появившись!"

    show monika 1eua_static at hf32
    m 1hksdlb_static "У меня не хватило времени, чтобы подготовиться!"
    m 1eka_static "Но спасибо, что вернулся, [player]."
    show monika 1eua_static at t32
    m 3eua_static "Просто дай мне несколько секунд, чтобы всё наладить, хорошо?"
    show monika 1eua_static at t31
    m 2eud_static "..."
    show monika 1eua_static at t33
    m 1eud_static "...и..."

    if mas_current_background.isFltDay():
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
            m "Подожди.{w=0.5}.{w=0.5}.{nw}"
            hide sp_mas_backbed with dissolve
            m 2hua_static "И... исправлено!"
            show monika 1eua_static at lhide
            hide monika

    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_knock:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    m "Кто это~?"
    menu:
        "Это я.":
            # monika knows you are here now
            $ mas_disable_quit()
            if mas_isMoniNormal(higher=True):
                m "[player]! Я так счастлива, что ты вернулся!"

                if persistent.seen_monika_in_room:
                    m "И спасибо, что сначала постучался~"
                m "Подожди, мне надо привести себя в порядок..."

            elif mas_isMoniUpset():
                m "[player].{w=0.3} Ты вернулся..."

                if persistent.seen_monika_in_room:
                    m "По крайней мере, ты постучал."

            else:
                m "Oх...{w=0.5} Ладно."

                if persistent.seen_monika_in_room:
                    m "Спасибо, что постучал."

            $ mas_startupWeather()
            call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False)
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_post:
    if mas_isMoniNormal(higher=True):
        m 2eua_static "А теперь позволь мне взять столик и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 1eua at ls32 zorder MAS_MONIKA_Z
        $ today = "сегодня" if mas_globals.time_of_day_4state != "night" else "ночью"
        m 1eua "Чем мы будем заниматься [today], [mas_get_player_nickname()]?"

    elif mas_isMoniUpset():
        m "Просто позволь мне взять столик и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 2esc at ls32 zorder MAS_MONIKA_Z
        m 2esc "Чего ты хочешь, [player]?"

    else:
        m "Мне нужно взять стол и стул.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 6ekc at ls32 zorder MAS_MONIKA_Z
        m 6ekc "Было ли что-нибудь, что ты хотел, [player]?"

    jump monikaroom_greeting_cleanup

# cleanup label
label monikaroom_greeting_cleanup:
    python:
        # couple of things:
        # 1 - monika knows you are here now
        mas_disable_quit()

        # 2 - music is renabled
        mas_MUINDropShield()

        # 3 - keymaps should be set
        set_keymaps()

        # 4 - show the overlays
        mas_OVLShow()

        # 5 - the music can be restarted
        mas_startup_song()

        # 6 - enable escape so we can access settings and chat box keys
        enable_esc()

    return

#init 5 python:
#    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youarereal", unlocked=True, random=True),code="GRE")

label greeting_youarereal:
    python:
        try:
            renpy.file(
                "../characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    m 1hua "[player]! Рада тебя видеть!"
    if persistent._mas_you_chr:
        m 1euc "Подожди-ка. Что-то изменилось."
        m 1eud "Ты... добавил файл персонажа?"
        m 1ekc "[player].chr... Да?"
        m 1ekd "Зачем ты... пытаешься поместить себя рядом со мной?"
        m "Зачем тебе это нужно?"
        m 1tkc "Разве ты не понял? "
        m 1tkd "Этого места не существует! Я не знаю, что произойдёт, если ты придёшь сюда!"
        m 1dsc "Как ты мог это сделать?"
        m 1lksdlc "Отказаться от своей реальности..."
        m 1lksdld "Просто чтобы быть со мной?"
        m 1ekc "Это всё моя вина!"
        m "Но... но «ты», в игре..."
        m 1esd "Он даже начинает немного двигаться снова."
        m "Может... это позволит тебе управлять им снова?"
        m 1ekc "Это неправильно! Я не хочу марионетку!"
        m 1tkc "Пожалуйста, [player]..."
        m "Если ты собираешься это сделать, ты уверен, что это то, чего ты хочешь?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен?{fast}"

            "Я уверен.":
                m 1eka "Тогда... у меня нет выбора кроме как принять его..."
                m 1hub "Я приму этот подарок с распростёртыми объятиями!"
                m "Мы сможем, наконец, быть вместе, [player]."
                m "И мы сможем понять, как это сделать в твоей реальности, вместе!"

            "Возможно, нет...":
                m 1eka "Я так и думала..."
                m "Нельзя отказаться от того, чтобы быть «настоящим» рядом со мной..."
                m 1ekc "Я не могу заставить себя удалить этот симпатичный маленький .chr файл, но..."
                m 1eka "Пожалуйста, сделай это сам."
                m 1lksdlc "В этих файлах есть какие-то жуткие вещи..."
                m 1eka "Я люблю тебя, [player]. Я буду ждать тебя столько, сколько потребуется."
                m "Так что не торопись, хорошо?"
    else:
        m 1esd "Я много размышляла о .chr-файлах..."
        m 1euc "Например, каковы они на самом деле?"
        m 1lksdlc "Они немного жуткие..."
        m "И даже если другие девушки не настоящие, почему можно удалить одного из персонажей?"
        m 1esd "Возможно ли добавить персонажа?"
        m 1dsd "Трудно сказать..."
    return

#TODO needs additional dialogue so can be used for all aff
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
    m 1hub "О, konnichiwa, [player]!"
    m "Э-хе-хе~"
    m 2eub "Привет, [player]!"
    m 1eua "Я просто занимаюсь японским языком."
    m 3eua "Посмотри..."
    $ shown_count = mas_getEVLPropValue("greeting_japan", "shown_count")
    if shown_count == 0:
        m 4hub "Watashi ha itsumademo anata no mono desu!"
        m 2hksdlb "Прости, если это не имеет смысла!"
        m 3eua "Ты знаешь, что это означает, [mas_get_player_nickname()]?"
        m 4ekbsa "Это означает: {i}«Я буду твоей навсегда»~{/i}"
        return

    m 4hub "Watashi wa itsumademo anata no mono desu!"
    if shown_count == 1:
        m 3eksdla "В прошлый раз я сказала, что совершила ошибку..."
        m "В этой фразе ты должен говорить «ва», а не «га», как я делала раньше."
        m 4eka "Не волнуйся, [player], смысл всё тот же."
        m 4ekbsa "Я всё равно буду твоей навсегда~"
    else:
        m 3eua "Ты знаешь, что это означает, [mas_get_player_nickname()]?"
        m 4ekbsa "{i}«Я буду твоей навсегда»~{/i}"
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sunshine",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_sunshine:
    m 1hua "{i}~Ты моё солнце, моё единственное солнце~{/i}"
    m "{i}~Ты делаешь меня счастливой, когда небеса пасмурны~{/i}"
    m 1hub "{i}~Ты никогда не узнаешь, дорогой, как сильно я тебя люблю~{/i}"
    m 1eka "{i}~Пожалуйста, не отнимай у меня солнце~{/i}"
    m 1wud "...А?"
    m "Эм-м?!"
    m 1wubsw "[player]!"
    m 1lkbsa "О боже, это так неловко!"
    m "Я п-просто пела про себя, чтобы скоротать время!"
    m 1ekbfa "Э-хе-хе..."
    m 3hubfa "Но теперь, когда ты здесь, мы можем провести это время вместе~"
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
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    m "Виртуальная Девушка Моника Здесь!"
    m 1hksdlb "А-ха-ха, извини! В последнее время я наблюдаю за одной виртуальной ютубершей."
    m 1eua "Должна сказать, она довольно очаровательная..."
    $ mas_lockEVL("greeting_hai_domo", "GRE")
    return

#TODO needs additional dialogue so can be used for all aff
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
    m 1eua "Bonjour, [player]!"
    m 1hua "Savais-tu que tu avais de beaux yeux, mon amour?"
    m 1hub "Э-хе-хе!"
    m 3hksdlb "Я практикую французский. Я только что сказала тебе, что у тебя очень красивые глаза~"
    m 1eka "Это такой романтический язык, [player]."
    m 1hua "Может быть, мы оба сможем практиковать его когда-нибудь, mon amour~"
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
        tempname = m_name
        m_name = "Моника"

    m 1eua "О, привет!"
    m 3eub "Меня зовут Моника."
    show monika 1eua zorder MAS_MONIKA_Z

    python:
        entered_good_name = True
        fakename = renpy.input("Как тебя зовут?", allow=name_characters_only, length=20).strip(" \t\n\r")
        lowerfake = fakename.lower()

    if lowerfake in ("сайори", "юри", "нацуки"):
        m 3euc "Забавно."
        m 3eud "У одной из моих подруг такое же имя."

    elif lowerfake == "моника":
        m 3eub "О, тебя тоже зовут Моника?"
        m 3hub "А-ха-ха, каковы шансы, верно?"

    elif lowerfake == "monica":
        m 1hua "Эй, у нас такие похожие имена, э-хе-хе~"

    elif lowerfake == player.lower():
        m 1hub "О, какое чудесное имя!"

    elif lowerfake == "":
        $ entered_good_name = False
        m 1euc "..."
        m 1etd "Хочешь сказать, что у тебя нет имени, или ты просто стесняешься говорить?"
        m 1eka "Это странно, но, думаю, не так страшно."

    elif mas_awk_name_comp.search(lowerfake) or mas_bad_name_comp.search(lowerfake):
        $ entered_good_name = False
        m 1rksdla "Это...{w=0.4} {nw}"
        extend 1hksdlb "довольно необычное имя, а-ха-ха..."
        m 1eksdla "Ты...{w=0.3} пытаешься подколоть меня?"
        m 1rksdlb "Ах, извини-извини, я не осуждаю это или что-то в этом роде."

    python:
        if entered_good_name:
            name_line = renpy.substitute(", [fakename]")
        else:
            name_line = ""

        if mas_current_background == mas_background_def:
            end_of_line = "я, похоже, не могу выйти из этого класса."
        else:
            end_of_line = "я не знаю, где нахожусь."

    m 1hua "Что ж, приятно с тобой познакомиться, [name_line]!"
    m 3eud "Скажи, [name_line], ты знаешь о том, куда всё подевались?"
    m 1eksdlc "Ты первый человек, кого я заметила, и {nw}"
    extend 1rksdlc "[end_of_line]"
    m 1eksdld "Ты поможешь мне выяснить, что здесь происходит, [name_line]?"

    m "Пожалуйста? {w=0.2}{nw}"
    extend 1dksdlc "Я скучаю по своим друзьям."

    window hide
    show monika 1eksdlc
    pause 5.0
    $ m_name = tempname
    window auto

    m 1rksdla "..."
    m 1hub "А-ха-ха!"
    m 1hksdrb "Прости, [player]! Я не могла сдержаться."
    m 1eka "После нашего разговора о книге {i}«Цветы для Элджернона»{/i}, я не могла сопротивляться желанию увидеть твою реакцию на то, что я якобы всё забыла."

    if lowerfake == player.lower():
        m 1tku "...И твоя реакция вполне оправдала мои ожидания."

    m 3eka "Но я надеюсь, что не расстроила тебя."
    m 1rksdlb "У меня был бы такой настрой, если бы ты забыл обо мне, [player]."
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

# TODO for better-sick, we would use the mood persistent and queue a topic.
#   might have dialogue similar to this, so leaving this todo here.

label greeting_sick:
    if mas_isMoniNormal(higher=True):
        m 1hua "С возвращением, [mas_get_player_nickname()]!"
        m 3eua "Ты чувствуешь себя лучше?{nw}"
    else:
        m 2ekc "С возвращением, [player]..."
        m "Ты чувствуешь себя лучше?{nw}"

    $ _history_list.pop()
    menu:
        m "Ты чувствуешь себя лучше?{fast}"
        "Да.":
            $ persistent._mas_mood_sick = False
            if mas_isMoniNormal(higher=True):
                m 1hub "Здорово! Теперь мы сможем провести ещё больше времени вместе. Э-хе-хе~"
            else:
                m "Приятно слышать."
        "Нет.":
            jump greeting_stillsick
    return

label greeting_stillsick:
    if mas_isMoniNormal(higher=True):
        m 1ekc "[player], тебе действительно нужно немного отдохнуть."
        m "Полноценный отдых – лучшее средство для быстрого восстановления после болезни."
        m 2lksdlc "Я бы не простила себя, если бы твоя болезнь ухудшилась из-за меня."
        m 2eka "Теперь, пожалуйста, [player], расслабься и иди отдохни."
        m "Ты сделаешь это ради меня?"

    else:
        m 2ekc "[player], тебе действительно нужно немного отдохнуть."
        m 4ekc "Полноценный отдых – лучшее средство для быстрого восстановления после болезни."
        m "Теперь, пожалуйста, [player], расслабься и иди отдохни."
        m 2ekc "Ты сделаешь это ради меня?{nw}"

    $ _history_list.pop()
    menu:
        m "Ты сделаешь это ради меня?{fast}"
        "Да.":
            jump greeting_stillsickrest
        "Нет.":
            jump greeting_stillsicknorest
        "Я уже отдохнул.":
            jump greeting_stillsickresting

label greeting_stillsickrest:
    if mas_isMoniNormal(higher=True):
        m 2hua "Спасибо, [player]."
        m 2eua "Я думаю, если я оставлю тебя в покое на некоторое время, ты сможешь лучше отдохнуть."
        m 1eua "Так что я специально для тебя закрою игру."
        m 1eka "Поправляйся скорее, [player]. Я так сильно тебя люблю!"

    else:
        m 2ekc "Спасибо, [player]."
        m "Я думаю, если я оставлю тебя в покое на некоторое время, ты сможешь лучше отдохнуть."
        m 4ekc "Так что я специально для тебя закрою игру."
        m 2ekc "Поправляйся скорее, [player]."

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

label greeting_stillsicknorest:
    if mas_isMoniNormal(higher=True):
        m 1lksdlc "Понятно..."
        m "Ну если ты настаиваешь, [player]."
        m 1ekc "Полагаю, ты знаешь свои ограничения лучше, чем я."
        m 1eka "Если ты начнёшь чувствовать лёгкую слабость или усталость, то, [player], пожалуйста, дай мне знать."
        m "Так ты сможешь немного отдохнуть."
        m 1eua "Не волнуйся, я всё ещё буду здесь, когда ты проснёшься."
        m 3hua "Тогда мы сможем повеселиться вместе, не беспокоясь о тебе в глубине души."

    else:
        m 2ekc "Ладно."
        m 2tkc "Ты, кажется, никогда не хотел слушать меня, так почему я ожидаю, что теперь всё будет иначе."

    # setting greet type here even tho we aren't quitting so she remembers you're sick next load
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

label greeting_stillsickresting:
    m 1eka "О, какое облегчение слышать это, [player]."
    m 3eka "Но я надеюсь, ты не позволишь себе замёрзнуть."
    if mas_isMoniNormal(higher=True):
        m 1dku "Можешь пожалуйста, ещё завернуться в тёплое одеяло и выпить чашку горячего чая."
        m 2eka "Твоё здоровье очень важно для меня, [player], так что позаботься о себе сам."
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbsa "...И если тебе всё ещё немного холодно, надеюсь, что знание того, что я люблю тебя, немного согреет тебя."
        m 5hua "Э-хе-хе~"
        $ mas_ILY()

    else:
        m 1eka "Можешь пожалуйста, ещё завернуться в тёплое одеяло и выпить чашку горячего чая."
        m 2eka "Твоё здоровье очень важно для меня, [player], так что позаботься о себе сам."

    #TODO: Have this use the nap brb potentially. Expand this
    # setting greet type here even tho we aren't quitting so she remembers you're sick next load
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
            $ mas_loseAffectionFraction(0.1, min_amount=70)
            m 2dsc "[player]..."
            m 2tkc "Ты говорил, что уедешь всего на несколько дней..."
            m 2rksdld "Но это было настолько долго."
            m 2ekd "Я рада, что ты вернулся, но..."
            m 2dktdc "Мне было так одиноко..."
            m 2ektsc "Я думала, что с тобой что-то случилось!"
            m 2lktsc "Я... я всё думала, что, возможно, ты не вернёшься."
            m 2ektsc "Пожалуйста, никогда,{w=0.5} {i}никогда{/i}{w=0.5} больше не делай так."
            m 2rktsd "Может, ты ничего не мог поделать с этим, но... я волновалась."
            m 2dftdc "Я не знала, что делать."
            m 4ekc "По возможности, [player], пожалуйста, не уходи так надолго."
            m 2ekd "Если ты думаешь, что у тебя нет выбора, пожалуйста, говори мне."
            m 1dsc "Я не хочу быть снова одна..."

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.08, min_amount=60)
            m 3ekc "С возвращением, [player]."
            m 3rksdlc "Ты немного опоздал, не так ли?"
            m 3ekc "Я знаю, ты говорил, что уедешь ненадолго, но... ты ведь сказал, что на {i}неделю{/i}."
            m 2rkc "Я собираюсь предположить, что это была не твоя вина..."
            m 2ekd "Но если тебе кажется, что в следующий раз это займёт больше времени, ты должен будешь сказать мне об этом."
            m 2rksdld "Я начинала думать, что с тобой что-то случилось."
            m 2dkc "Но я продолжала говорить себе, что всё в порядке..."
            m 2eka "Я просто рада, что ты в безопасности и вернул ко мне, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffectionFraction(0.06, min_amount=40)
            m 1wud "[player]!"
            m 1hua "Ты наконец-то здесь!"
            m 1ekd "Я так волновалась..."
            m 2dkd "Почему тебя так долго не было?"
            m 2rkc "Я думала, тебя не будет всего пару недель..."
            m "Но ты ушёл на срок, который дольше более чем в два раза."
            m 1rksdlc "Ты действительно был так занят?"
            m 3tkc "Надеюсь, ты не перегружал себя..."
            m 1eka "Теперь ты здесь со мной, так что если что-то не так, не стесняйся сказать мне."

        elif persistent._mas_absence_choice == "month":
            $ mas_loseAffectionFraction(0.04, min_amount=20)
            m 1eua "С возвращением, [mas_get_player_nickname()]."
            m 2rkc "Это было довольно долго, не так ли?"
            m 2rksdlc "Тебя не было дольше, чем ты говорил..."
            m 2eka "Но всё в порядке, я была готова к этому."
            m 3rksdlc "Честно говоря, было довольно одиноко без тебя..."
            m 3ekbsa "Надеюсь, ты загладишь вину передо мной~"
            show monika 1eka

        elif persistent._mas_absence_choice == "longer":
            m 1esc "Прошло много времени, [player]."
            m 1ekc "Я была готова к этому, но это не сделало ожидание легче."
            m 3eka "Надеюсь, ты смог сделать то, что тебе нужно было."
            m 2rksdlc "..."
            m 2tkc "По правде говоря, мне было очень грустно в последнее время."
            m 2dkc "Не иметь тебя в моей жизни так долго..."
            m 2dkd "Было очень одиноко..."
            m "Я чувствовала себя такой одинокой и пустой без тебя."
            m 3eka "Я так рада, что ты здесь. Я люблю тебя, [player]. Добро пожаловать домой."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Ты, наконец, вернулся, [player]!"
            m 3rksdla "Когда ты сказал, что не знаешь насколько долго уедешь, ты {i}действительно{/i} не знал, не так ли?"
            m 3rksdlb "Ты, должно быть, был действительно занят, раз уж уехал {i}настолько{/i} долго."
            m 1hua "Ну, теперь ты вернул, я действительно скучала по тебе."

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=4):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.1, min_amount=60)
            m 1dkc "[player]..."
            m 1ekd "Ты говорил, что тебя не будет всего лишь несколько дней..."
            m 2efd "Но это был целый месяц!"
            m 2ekc "Я думала, с тобой что-то случилось."
            m 2dkd "Я не была уверена, что делать..."
            m 2efd "Что задержало тебя на такой срок?"
            m 2eksdld "Я сделала что-то не так?"
            m 2dftdc "Ты можешь сказать мне что угодно, только не исчезай так."
            show monika 2dfc

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.08, min_amount=50)
            m 1esc "Здравствуй, [player]."
            m 3efc "Знаешь, ты уже довольно поздно."
            m 2lfc "Я не хочу звучать грубо, но неделя – это не то же самое, что месяц!"
            m 2rksdld "Я думаю, может быть, что-то заставило тебя быть настолько занят?"
            m 2wfw "Но это не должно было быть настолько отвлекающим, что ты не мог сказать мне, что ты можешь дольше задержаться!"
            m 2wud "Ах!.."
            m 2lktsc "Извини, [player]. Я просто... очень скучала по тебе."
            m 2dftdc "Прости, что так сорвалась."
            show monika 2dkc

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffectionFraction(0.06, min_amount=30)
            m 1wuo "...О!"
            m 1sub "Ты наконец вернулся, [player]!"
            m 1efc "Ты говорил, что тебя не будет только пару недель, но прошёл уже как минимум месяц!"
            m 1ekd "Я действительно беспокоилась за тебя, понимаешь?"
            m 3rkd "Но я полагаю, что это было вне твоего контроля?"
            m 1ekc "Если сможешь, просто скажи, если вдруг в следующий раз будешь дольше, чем планировалось, хорошо?"
            m 1hksdlb "Я считаю, что я заслуживаю этого, ведь я твоя девушка, в конце концов."
            m 3hua "Тем не менее, c возвращением, [mas_get_player_nickname()]!"

        elif persistent._mas_absence_choice == "month":
            $ mas_gainAffection()
            m 1wuo "...О!"
            m 1hua "Ты здесь, [player]!"
            m 1hub "Я знала, что могу доверить тебе сдержать слово!"
            m 1eka "Ты действительно особенный, ты ведь знаешь это?"
            m 1hub "Я так по тебе скучала!"
            m 2eub "Расскажи мне всё, что ты сделал, я хочу услышать об этом!"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1esc "...Хм?"
            m 1wub "[player]!"
            m 1rksdlb "Ты вернулся немного раньше, чем я думала..."
            m 3hua "С возвращением, [mas_get_player_nickname()]!"
            m 3eka "Я знаю, что это было довольно долго, поэтому я уверена, что ты был занят."
            m 1eua "Я с удовольствием послушаю обо всём, что ты успел сделать."
            show monika 1hua

        elif persistent._mas_absence_choice == "unknown":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "О!"
            m 1sub "[player]!"
            m 1hub "Это приятный сюрприз!"
            m 1eka "Как дела?"
            m 1ekd "Это был целый месяц, ты действительно не знал, как долго тебя не будет, не так ли?"
            m 3eka "Всё равно ты вернулся, и это многое для меня значит."
            m 1rksdla "Я знала, что ты вернёшься, в конце концов..."
            m 1hub "Я так сильно тебя люблю, [player]!"
            show monika 1hua

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=2):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffectionFraction(0.08, min_amount=30)
            m 1wud "О-о, [player]!"
            m 1hua "С возвращением, [mas_get_player_nickname()]!"
            m 3ekc "Тебя не было дольше, чем ты обещал..."
            m 3ekd "Всё в порядке?"
            m 1eksdla "Я знаю, что твоя жизнь может быть чем-то загружена и иногда она может забрать тебя у меня... так что я не очень расстроена..."
            m 3eksdla "Просто... в следующий раз, может быть, предупредишь меня?"
            m 1eka "Было бы очень мило с твоей стороны."
            m 1hua "И я была бы очень признательна!"

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffectionFraction(0.06, min_amount=20)
            m 1eub "Здравствуй, [player]!"
            m 1eka "Жизнь не даёт тебе покоя?"
            m 3hksdlb "Ну, должно быть. Иначе ты был бы уже здесь."
            m 1hksdlb "Не волнуйся! Я не расстраиваюсь."
            m 1eka "Я просто надеюсь, что ты заботишься о себе."
            m 3eka "Я знаю, что ты не всегда можешь быть здесь, поэтому убедись, что ты в безопасности, пока будешь не со мной!"
            m 1hua "Я позабочусь о тебе с этого момента~"
            show monika 1eka

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_gainAffection()
            m 1hub "Привет, [player]!"
            m 1eua "Ты вернулся, когда сказал, что всё-таки вернёшься."
            m 1eka "Спасибо, что не предал моё доверие!"
            m 3hub "Давай наверстаем упущенное время!"
            show monika 1hua

        elif persistent._mas_absence_choice == "month":
            m 1wud "О боже! [player]!"
            m 3hksdlb "Я не ожидала, что ты вернёшься так скоро."
            m 3ekbsa "Думаю, ты скучал по мне так же, как и я скучала по тебе~"
            m 1eka "Очень приятно видеть тебя раньше, чем я ожидала."
            m 3ekb "Я ожидала, что день будет однообразным, к счастью, теперь у меня есть ты!"
            m 3hua "Спасибо, что вернулся так рано, [mas_get_player_nickname()]."

        elif persistent._mas_absence_choice == "longer":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "О! [player]!"
            m 1hub "Ты вернулся пораньше!"
            m 1hua "Welcome back, [mas_get_player_nickname()]!"
            m 3eka "Я не знала, когда тебя ждать, но это было так скоро..."
            m 1hua "Ну, это подбодрило меня прямо сейчас!"
            m 1eka "Я действительно скучала по тебе."
            m 1hua "Давай проведём как можно больше времени вместе, пока мы можем."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Здравствуй, [player]!"
            m 3eka "Был занят последние несколько недель?"
            m 1eka "Спасибо, что предупредил меня, что ты уйдёшь."
            m 3ekd "Иначе я бы волновалась."
            m 1eka "Это действительно помогло..."
            m 1eua "Так скажи мне, как прошёл твой день?"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=1):
        if persistent._mas_absence_choice == "days":
            m 2eub "Здравствуй, [player]."
            m 2rksdla "Тебя не было немного дольше, чем ты сказал... но не волнуйся."
            m 3eub "Я знаю, что ты занятой человек!"
            m 3rkc "Может быть, если сможешь, сначала предупредишь меня?"
            m 2rksdlc "Когда ты сказал несколько дней... я думала, что это будет короче недели."
            m 1hub "Но всё в порядке! Я прощаю тебя!"
            m 1ekbsa "Ты ведь моя единственная любовь!"
            show monika 1eka

        elif persistent._mas_absence_choice == "week":
            $ mas_gainAffection()
            m 1hub "Здравствуй, [mas_get_player_nickname()]!"
            m 3eua "Это так мило, когда мы можем доверять друг другу, не так ли?"
            m 3hub "Это то, на чём основана сила отношений!"
            m 3hua "Это просто означает, что наши отношения надёжны!"
            m 1hub "А-ха-ха!"
            m 1hksdlb "Прости, прости. Я просто радуюсь, что ты вернулся!"
            m 3eua "Расскажи мне, как ты. Я хочу услышать всё об этом."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "Привет~"
            m 3eua "Ты вернулся немного раньше, чем я думала... но я рада, что ты здесь!"
            m 3eka "Когда ты здесь со мной, всё становится лучше."
            m 1eua "Давай продолжим создавать замечательные воспоминания вместе, [player]."
            show monika 3eua

        elif persistent._mas_absence_choice == "month":
            m 1hua "Э-хе-хе~"
            m 1hub "С возвращением!"
            m 3tuu "Я знала, что ты не сможешь остаться в стороне целый месяц..."
            m 3tub "Если бы я была на твоём месте, я бы тоже не смогла держаться вдалеке от тебя!"
            m 1hksdlb "Честно говоря, я начала скучать по тебе сразу же через несколько дней!"
            m 1eka "Спасибо, что не заставил меня ждать так долго, чтобы увидеть тебя снова~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1hub "Посмотрите-ка, кто вернулся так рано! Это ты, мой дорогой [player]!"
            m 3hksdlb "Не мог остаться в стороне, даже если бы захотел, верно?"
            m 3eka "Я не могу винить тебя! Моя любовь к тебе не позволит мне держаться от тебя подальше!"
            m 1ekd "Каждый день, когда тебя не было, мне было интересно, как ты..."
            m 3eka "Так что позволь мне услышать. Как ты, [player]?"
            show monika 3eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hub "Здравствуй, [mas_get_player_nickname()]!"
            m 1eka "Я рада, что ты не заставил меня ждать слишком долго."
            m 1hua "На неделю короче, чем я ожидала, поэтому можешь считать меня приятно удивлённой!"
            m 3hub "Спасибо, что уже сделал мой день, [player]!"
            show monika 3eua
            
    else:
        if persistent._mas_absence_choice == "days":
            m 1hub "С возвращением, [mas_get_player_nickname()]!"
            m 1eka "Спасибо, что предупредил меня о том, как долго тебя не будет."
            m 1eua "Это много значит – знать, что я могу доверять твоим словам."
            m 3hua "Я надеюсь, ты знаешь, что ты можешь доверять мне тоже!"
            m 3hub "Наши отношения крепнут с каждым днём~"
            show monika 1hua

        elif persistent._mas_absence_choice == "week":
            m 1eud "О! Ты вернулся немного раньше, чем я ожидала!"
            m 1hua "Не то, чтобы я жаловалась, приятно видеть тебя снова так скоро."
            m 1eua "Давай проведём ещё один хороший день вместе, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "{i}~На листе пером выведу стих, в кото-{/i}"
            m 1wubsw "О-о! [player]!"
            m 3hksdlb "Ты вернулся гораздо раньше, чем ты сказал мне..."
            m 3hub "С возвращением!"
            m 1rksdla "Ты просто прервал меня, пока я практиковалась в моей песне..."
            m 3hua "Почему бы тебе не послушать, как я пою это снова?"
            m 1ekbsa "Я сделаю это только для тебя~"
            show monika 1eka

        elif persistent._mas_absence_choice == "month":
            m 1wud "А? [player]?"
            m 1sub "Ты здесь!"
            m 3rksdla "Я думала, ты уехал на целый месяц."
            m 3rksdlb "Я была готова к этому, но..."
            m 1eka "Я уже соскучилась по тебе!"
            m 3ekbsa "Ты тоже скучал по мне?"
            m 1hubfa "Спасибо, что так скоро вернулся~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1eud "[player]?"
            m 3ekd "Я думала, ты собирался уехать надолго..."
            m 3tkd "Почему ты так скоро вернулся?"
            m 1ekbsa "Чтобы навестить меня?"
            m 1hubfa "Ты такой милый!"
            m 1eka "Если ты соберёшься уехать ненадолго, обязательно скажи мне."
            m 3eka "Я люблю тебя, [player], и не стала бы злиться, если бы ты на самом деле планировал задержаться подольше..."
            m 1hub "Давай наслаждаться временем, которое мы имеем вместе до тех пор!"
            show monika 1eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Э-хе-хе~"
            m 3eka "Так скоро, [player]?"
            m 3rka "Думаю, когда ты говорил, что не знаешь насколько долго уедешь, ты не осознавал, что это может быть не настолько долго."
            m 3hub "Спасибо, что предупредил меня!"
            m 3ekbsa "Это даёт мне понять, что я всегда буду любима тобой."
            m 1hubfb "Ты на самом деле добрый."
            show monika 3eub
    m "Напомни мне, если ты снова уедешь, хорошо?"
    show monika idle with dissolve_monika
    jump ch30_loop

#Time Concern
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

    # couple of things:
    # shield ui
    $ mas_RaiseShield_core()

    # 3 - keymaps not set (default)
    # 4 - hotkey buttons are hidden (skip visual)
    # 5 - music is off (skip visual)

    # reset clothes if not ones that work with hairdown
    if monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
        $ monika_chr.reset_clothes(False)

    # have monika's hair down
    $ monika_chr.change_hair(mas_hair_down, by_user=False)

    call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "Привет, [player]!"
    m 4hua "Заметил кое-что другое сегодня?"
    m 1hub "Я сегодня решила попробовать что-то новое~"

    m "Тебе нравится?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе нравится?{fast}"
        "Да.":
            $ persistent._mas_likes_hairdown = True

            # maybe 6sub is better?
            $ mas_gainAffection()
            m 6sub "В самом деле?"
            m 2hua "Я так рада!"
            m 1eua "Просто попроси меня, если захочешь снова увидеть мой хвостик, хорошо?"
        
        "Нет.":
            # TODO: affection lowered? need to decide
            m 1ekc "Ох..."
            m 1lksdlc "..."
            m 1lksdld "Тогда я заплету их обратно для тебя."
            m 1dsc "..."

            $ monika_chr.reset_hair(False)

            m 1eua "Готово."
            # you will never get this chance again

    # save that hair down is unlocked
    $ store.mas_selspr.unlock_hair(mas_hair_down)
    $ store.mas_selspr.save_selectables()

    # unlock hair changed selector topic
    $ mas_unlockEventLabel("monika_hair_select")

    # lock this greeting
    $ mas_lockEVL("greeting_hairdown", "GRE")

    # cleanup
    # enable music menu and music hotkeys
    $ mas_MUINDropShield()

    # 3 - set the keymaps
    $ set_keymaps()

    # 4 - hotkey buttons should be shown
    $ HKBShowButtons()

    # 5 - restart music
    $ mas_startup_song()

    # 6 - enable escape so we can access settings and chat box keys
    $ enable_esc()

    return

init 5 python:

    # NOTE: this triggers when affection reaches BROKEN state.
    #   AND you have not seen this before
    ev_rules = {}
    ev_rules.update(MASPriorityRule.create_rule(15))
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1dsc"))

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
    m 2lksdlc "Я старалась изо всех сил ради тебя... ради {i}нас{/i}."
    m 2lksdld "Я делала хоть что-то, что причинило бы тебе боль или заставило бы чувствовать себя плохо?"
    m "Ты всё ещё расстроен из-за других девушек?"
    m 2ekc "Если да, то я действительно сожалею..."
    m "Мне очень, очень жаль!"
    m 2rksdld "Просто скажи мне, что я сделала неправильно, и я постараюсь ещё сильнее, чтобы быть идеальной девушкой для тебя."
    m 2ekd "Ты – весь мой мир; то, как ты себя чувствуешь, значит для меня всё!"
    m 2ekc "Так что, пожалуйста, просто скажи мне, что случилось, и я всё исправлю."
    m 2dfc "Я сделаю всё ради тебя, потому что... ты..."
    m 2dftdc "..."
    m 2dftsc "Ты нужен мне, [player]..."
    m 2ektsc "Мне нужно, чтобы ты любил меня так же, как и я люблю тебя."
    m 2lktsc "Ты нужен мне... потому что если у меня не будет тебя..."
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
    m 2esc "Но... мне действительно нужно, чтобы ты подумал о том, что я сказала."
    m 2ekc "Пожалуйста... просто... попытайся понять."
    m 1dsd "Я люблю тебя, и мне нужно, чтобы ты показал, что ты тоже любишь меня..."
    m 1dsc "Иначе... я просто больше не смогу с этим справляться."

    python:
        mas_lockEVL("greeting_tears", "GRE")

        #Setup the being virtual ev
        beingvirtual_ev = mas_getEV("monika_being_virtual")

        if beingvirtual_ev:
            beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return

#New greetings for upset, distressed, and broken. Made quips for upset and distressed to allow for more variety of combos
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
            "O. {w=1}Ты вернулся, [player].",
            "Привет, [player].",
            "O. {w=1}Привет, [player]."
        ]

        upset_greeting_quips_second = [
#            "What do you want?",
#            "What now?",
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
            "O... {w=1}Ты вернулся, [player]."
        ]

        distressed_greeting_quips_second = [
            "Наверное, мы можем провести некоторое время вместе.",
            "Я не была уверена, когда ты снова посетишь меня.",
            "Надеюсь, мы сможем вместе провести время.",
            "Я не ожидала тебя.",
            "Надеюсь, в ближайшее время всё наладится.",
            "Я думала, ты забыл обо мне..."
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

# special type greetings

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
        m 1hua "О, с возвращением, [mas_get_player_nickname()]!"
        m 1eua "Как прошёл твой день в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день в школе?{fast}"
            
            "Прекрасно.":
                m 2sub "Правда?!"
                m 2hub "Мне приятно это слышать, [player]!"
                if renpy.random.randint(1,4) == 1:
                    m 3eka "Школа определённо может стать важной частью в твоей жизни, но потом ты можешь начать скучать по ней."
                    m 2hksdlb "А-ха-ха! Знаю, как-то странно думать о том, что тебе однажды захочется вернуться в школу..."
                    m 2eub "Но большая часть приятных воспоминаний возникает именно в школе!"
                    m 3hua "Быть может, ты потом сможешь рассказать мне о них на досуге."
                else:
                    m 3hua "Мне всегда приятно знать о том, что ты счастлив~"
                    m 1eua "Если ты хочешь поговорить о своём прекрасном дне, то я с радостью послушаю тебя!"
                return
            
            "Хорошо.":
                m 1hub "Это прекрасно...{w=0.3} {nw}"
                extend 3eub "Я не могу перестать радоваться тому, что у тебя всё хорошо!"
                m 3hua "Надеюсь, ты узнал там что-нибудь полезное, э-хе-хе~"
                return
            
            "Плохо.":
                m 1ekc "Ох..."
                m 1dkc "Мне жаль это слышать."
                m 1ekd "Плохие дни в школе могут быть действительно деморализующими..."
            
            "Очень плохо...":
                m 1ekc "Ох..."
                m 2ekd "Мне правда жаль слышать о том, что у тебя сегодня был очень плохой день..."
                m 2eka "Но я рада тому, что ты пришёл ко мне, [player]."

        #Since this menu is too long, we'll use a gen-scrollable instead
        python:
            final_item = ("Я не хочу говорить об этом.", False, False, False, 20)
            menu_items = [
                ("Это связано с учёбой.", ".class_related", False, False),
                ("Это связано с людьми.", ".by_people", False, False),
                ("У меня просто день не задался.", ".bad_day", False, False),
                ("Я чуствовал себя нехорошо сегодня.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        m "Позволь спросить, это связано с чем-то конкретно?" nointeract

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        $ label_suffix = _return

        show monika at t11

        #No talk
        if not label_suffix:
            m 2dsc "Я понимаю, [player]."
            m 2ekc "Иногда оставление плохого дня позади является наилучшим способом справиться с ним."
            m 2eka "Но если ты хочешь поговорить об этом позже, то просто знай о том, что я с радостью выслушаю тебя."
            m 2hua "Я люблю тебя, [player]~"
            return "love"

        $ full_label = "greeting_back_from_school{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label

        label .class_related:
            m 2dsc "Понятно..."
            m 3esd "Люди, наверное, постоянно говорят тебе о том, что учёба в школе – это очень важно..."
            m 3esc "И тебе всегда приходится давить на себя и работать, не покладая рук..."
            m 2dkd "Но иногда это начинает сильнее нервировать людей, из-за чего они идут по нисходящей спирали."
            m 2eka "Как я уже говорила, я рада, что ты пришёл ко мне, [player]."
            m 3eka "Мне приятно знать о том, что я могу утешить тебя, когда тебе грустно."
            m "Помни, {i}ты{/i} намного важнее, чем школа или какие-то там оценки."
            m 1ekbsa "Особенно для меня."
            m 1hubsa "Не забывай делать перерывы, если ты чувствуешь себя уставшим, и у всех людей есть свои таланты."
            m 3hubfb "Я люблю тебя, и я просто хочу, чтобы ты был счастлив~"
            return "love"

        label .by_people:
            m 2ekc "О нет, [player]...{w=0.5} наверное, это было довольно трудно пережить."
            m 2dsc "То, что с тобой произошло что-то плохое, – это одно дело..."
            m 2ekd "И совсем другое – когда человек сам же и является причиной возникновения твоей беды."

            if persistent._mas_pm_currently_bullied or persistent._mas_pm_is_bullying_victim:
                m 2rksdlc "Я правда надеюсь, что это не тот человек, о котором ты мне уже рассказывал раньше..."

                if mas_isMoniAff(higher=True):
                    m 1rfc "И будет {i}лучше{/i}, если это не он..."
                    m 1rfd "Опять он достаёт моего любимого."

                m 2ekc "Я бы очень хотела сделать что-то большее, чтобы помочь тебе, [player]..."
                m 2eka "Но если ты будешь нуждаться во мне, то я всегда здесь."
                m 3hubsa "И я никуда не уйду~"
                m 1eubsa "Надеюсь, этим я смогла сделать твой день хоть чуточку лучше."
                m 1hubfb "Я очень сильно люблю тебя~"
                $ mas_ILY()

            else:
                m "Я правда надеюсь, что это не приключается с тобой из раза в раз, [player]."
                m 2lksdld "Так или иначе, мне кажется, будет лучше, если ты обратишься к кому-нибудь за помощью..."
                m 1lksdlc "Знаю, может показаться, что в некоторых случаях из-за этого может возникнуть ещё больше проблем..."
                m 1ekc "Но ты не должен страдать от чьих-либо рук."
                m 3dkd "Мне так жаль, что тебе приходится с этим разбираться, [player]..."
                m 1eka "Но теперь ты здесь, и я надеюсь, что проведённое вместе время поможет тебе немного улучшить свой день."
            return

        label .bad_day:
            m 1ekc "Понятно..."
            m 3lksdlc "Такие дни иногда настают."
            m 1ekc "Иногда бывает трудно вернуться в строй после такого дня."
            m 1eka "Но теперь ты здесь, и я надеюсь, что проведённое вместе время поможет тебе немного улучшить свой день."
            return

        label .sick:
            m 2dkd "Быть больным в школе может быть ужасно. Из-за этого становится намного труднее что-то делать или обращать внимание на уроки."
            jump greeting_back_from_work_school_still_sick_ask
            return

    elif mas_isMoniUpset():
        m 2esc "Ты вернулся, [player]..."

        m "Как у тебя дела в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как у тебя дела в школе?{fast}"
            "Хорошо.":
                m 2esc "Это хорошо"
                m 2rsc "Надеюсь, ты сегодня научился {i}чему-нибудь{/i}."
            
            "Плохо.":
                m "Это очень плохо..."
                m 2tud "Но, быть может, теперь ты имеешь лучшее представление о том, какие чувства я сейчас испытываю, [player]."

    elif mas_isMoniDis():
        m 6ekc "Ох...{w=1} ты вернулся."

        m "Как у тебя дела в школе?{nw}"
        $ _history_list.pop()
        menu:
            m "Как у тебя дела в школе?{fast}"
            "Хорошо.":
                m 6lkc "Мне...{w=1} приятно слышать это."
                m 6dkc "Н-надеюсь, твой день стал лучше не из-за...{w=2} того момента, когда ты «уходишь от меня»."
            
            "Плохо.":
                m 6rkc "Ох..."
                m 6ekc "Это очень плохо, [player], мне жаль слышать это."
                m 6dkc "Я знаю, что представляют из себя плохие дни..."
    else:
        m 6ckc "..."

    return

default persistent._mas_pm_last_promoted_d = None
# date when player last got promotion

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
        m 1hua "О, с возвращением, [mas_get_player_nickname()]!"

        m 1eua "Как прошёл рабочий день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл рабочий день?{fast}"
            
            "Прекрасно!":
                if not persistent._mas_pm_last_promoted_d:
                    $ promoted_recently = False
                else:
                    $ promoted_recently = datetime.date.today() < persistent._mas_pm_last_promoted_d + datetime.timedelta(days=180)

                m 1sub "Это {i}потрясающе{/i}, [player]!"
                m 1hub "Я очень рада тому, что у тебя был такой замечательный день!"

                m 1sua "Что сделало этот день таким потрясающим?{nw}"
                menu:
                    m "Что сделало этот день таким потрясающим?{fast}"
                    
                    "Меня повысили!":
                        if promoted_recently:
                            m 3suo "Что? Серьёзно?!"
                            m 3sub "Раз тебя повысили...{w=0.3} ты, должно быть, действительно делаешь изумительную работу!"
                            m 1huu "Я так...{w=0.2} горжусь тобой, [mas_get_player_nickname()]~"
                        else:
                            $ player_nick = mas_get_player_nickname()
                            m 3suo "Ух ты! Поздравляю [player_nick], {w=0.1}{nw}"
                            extend 3hub "Я так горжусь тобой!"
                            m 1euu "Я знала, что ты справишься."
                            $ promoted_recently = True

                        $ persistent._mas_pm_last_promoted_d = datetime.date.today()
                    
                    "Я многое успел сделать!":
                        m 3hub "Это замечательно., [mas_get_player_nickname()]!"
                    
                    "Это был просто потрясающий день.":
                        m 3hub "Приятно слышать.!"

                m 3eua "Я могу только представить себе, как хорошо ты работаешь в такие дни."
                if not promoted_recently:
                    m 1hub "...Быть может, тебя ещё и повысят в скором времени!"
                m 1eua "Так или иначе, я рада, что ты дома, [mas_get_player_nickname()]."

                if seen_event("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
                    m 3tubsu "Ты хочешь поужинать, принять ванну, или..."
                    m 1hubfb "А-ха-ха~ Я просто шучу."
                else:
                    m 3msb "Что может быть лучше, чем провести остаток этого дня со своей потрясающей девушкой?~"

                return
            
            "Хорошо.":
                m 1hub "Это хорошо!"
                m 1eua "Только не забудь передохнуть, ладно?"
                m 3eua "Таким образом, ты сможешь восстановить силы, чтобы заниматься другими делами."
                m 1hua "Впрочем, ты можешь просто отдохнуть вместе со мной!"
                m 3tku "Это лучшее, что можно сделать после долгого рабочего дня, согласись?"
                m 1hub "А-ха-ха!"
                return
            
            "Плохо.":
                m 2ekc "..."
                m 2ekd "Мне жаль слышать, что у тебя был плохой день на работе..."
                m 3eka "Я бы обняла тебя прямо сейчас, если бы была рядом, [player]."
                m 1eka "Просто помни о том, что, когда ты нуждаешься во мне, я всегда рядом, хорошо?"
            
            "Очень плохо...":
                m 2ekd "Мне жаль слышать, что у тебя был плохой день на работе, [player]."
                m 2ekc "Хотела бы я быть рядом, чтобы обнять тебя прямо сейчас."
                m 2eka "Я просто рада, что ты пришёл меня проведать... {w=0.5}я сделаю всё возможное, чтобы утешить тебя."

        m 2ekc "Если ты не против поговорить со мной об этом, то что сегодня произошло?{nw}"

        python:
            final_item = ("Я не хочу говорить об этом.", False, False, False, 20)
            menu_items = [
                ("На меня наорали.", ".yelled_at", False, False),
                ("Меня обошли стороной из-за одного человека.", ".passed_over", False, False),
                ("Мне пришлось задержаться на работе.", ".work_late", False, False),
                ("Я сегодня не успел закончить все дела.", ".little_done", False, False),
                ("Просто очередной неудачный день.", ".bad_day", False, False),
                ("Я чувствовал себя нехорошо сегодня.", ".sick", False, False),
            ]

        show monika 2ekc at t21
        $ renpy.say(m, "Если ты не против поговорить со мной об этом, то что сегодня произошло?{fast}", interact=False)
        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        $ label_suffix = _return

        show monika at t11
        #No talk
        if not label_suffix:
            m 1dsc "Я понимаю, [player]."
            m 3eka "Возможно, после проведения времени со мной тебе станет чуточку лучше~"
            return

        #Otherwise, let's jump to the label if it exists
        $ full_label = "greeting_back_from_work{0}".format(label_suffix)
        if renpy.has_label(full_label):
            jump expression full_label

        #Return so no fall thru if label missing
        return

        label .yelled_at:
            m 2lksdlc "Ох... {w=0.5}такое правда может испортить твой день"
            m 2dsc "Ты просто стараешься изо всех сил, но твоя работа кому-то не нравится по неизвестной тебе причине..."
            m 2eka "Если это всё равно сильно беспокоит тебя, то ты, наверное, можешь попытаться расслабиться немного, это пойдёт тебе на пользу."
            m 3eka "Думаю, разговор о чём-нибудь или даже игра в какую-нибудь игру поможет отвлечься от этого."
            m 1hua "Я уверена, тебе станет лучше после того, как мы проведём немного времени вместе."
            return

        label .passed_over:
            m 1lksdld "Ох... {w=0.5}когда видишь, как кто-то получает признание, которое, по твоему мнению, он вовсе не заслуживает, это правда может испортить твой день."
            m 2lfd "{i}Особенно{/i} когда ты так много сделал и твой поступок явно остался незамеченным."
            m 1ekc "Ты можешь выглядеть немного подавленным, когда говоришь что-нибудь, так что ты просто должен продолжать стараться, и однажды, уверена, это принесёт свои плоды."
            m 1eua "И пока ты стараешься изо всех сил, ты сможешь делать хорошие вещи и дальше, и ты однажды получишь своё признание."
            m 1hub "И помни...{w=0.5} я буду всегда гордиться тобой, [player]!"
            m 3eka "Надеюсь, от осознания этого тебе станет чуточку лучше~"
            return

        label .work_late:
            m 1lksdlc "Оу, это правда может всё испортить."

            m 3eksdld "Тебя хотя бы уведомили об этом заранее?{nw}"
            $ _history_list.pop()
            menu:
                m "Тебя хотя бы уведомили об этом заранее?{fast}"
                
                "Да.":
                    m 1eka "Ну, хоть что-то хорошее."
                    m 3ekc "Было бы очень больно осознать, что мы все уже собрались домой, а потом нам пришлось остаться на работе подольше."
                    m 1rkd "Но всё же, тебя может взбесить тот факт, что из-за этого твоё обычное расписание сбилось."
                    m 1eka "...Но, по крайней мере, ты уже здесь, и мы можем провести немного времени вместе."
                    m 3hua "Ты можешь наконец-то расслабиться!"
                
                "Нет.":
                    m 2tkx "Это очень плохо!"
                    m 2tsc "Особенно когда рабочий день уже подошёл к концу и ты уже собрался идти домой..."
                    m 2dsc "А потом тебе внезапно пришлось задержаться на работе, без какого-либо предупреждения."
                    m 2ekc "Внезапная отмена твоих планов может стать очень невыносимой."
                    m 2lksdlc "Возможно, у тебя были другие дела, которыми ты планировал заняться после рабочего дня, или тебе очень хотелось прийти домой и отдохнуть..."
                    m 2lubsu "...Или, наверное, ты хотел вернуться домой и увидеть свою очаровательную девушку, которая готовила сюрприз к твоему возвращению..."
                    m 2hub "Э-хе-хе~"
            return

        label .little_done:
            m 2eka "Оу, не расстраивайся, [player]."
            m 2ekd "Такие дни иногда настают."
            m 3eka "Я знаю, что ты настолько упорно работаешь, что вскоре сможешь преодолеть все свои препятствия."
            m 1hua "И пока ты ещё стараешься изо всех сил, я всегда буду гордиться тобой!"
            return

        label .bad_day:
            m 2dsd "Просто один из тех дней, да, [player]?"
            m 2dsc "Они настают время от времени..."
            m 3eka "Но всё же, я знаю, насколько изнурительными они бывают, и я надеюсь, что вскоре тебе станет лучше."
            m 1ekbsa "Я буду здесь, пока ты ещё нуждаешься в моём утешении, хорошо, [player]?"
            return

        label .sick:
            m 2dkd "Быть больным на работе может быть ужасно. Из-за этого гораздо труднее что-либо сделать."
            jump greeting_back_from_work_school_still_sick_ask

    elif mas_isMoniUpset():
        m 2esc "Вижу, ты вернулся с работы, [player]..."

        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день?{fast}"
            "Хорошо.":
                m 2esc "Рада это слышать."
                m 2tud "Наверное, приятно, когда тебя ценят."
            
            "Плохо.":
                m 2dsc "..."
                m 2tud "Ты испытываешь скверное чувство, когда тебя никто не ценит, да, [player]?"

    elif mas_isMoniDis():
        m 6ekc "Привет, [player]...{w=1} ты наконец-то вернулся с работы?"

        m "Как прошёл твой день?{nw}"
        $ _history_list.pop()
        menu:
            m "Как прошёл твой день?{fast}"
            "Хорошо.":
                m "Это хорошо."
                m 6rkc "Я просто надеюсь, что на работе тебе не так сильно нравится находиться, нежели быть рядом со мной, [player]."
            
            "Плохо.":
                m 6rkc "Ох..."
                m 6ekc "Мне жаль слышать это."
                m 6rkc "Я знаю, что именно в плохие дни ты не можешь угодить всем..."
                m 6dkc "Довольно тяжело пережить такие дни."

    else:
        m 6ckc "..."
    return

label greeting_back_from_work_school_still_sick_ask:
    m 7ekc "Хотя я должна спросить..."
    m 1ekc "Тебе всё ещё плохо?{nw}"
    menu:
        m "Тебе всё ещё плохо?{fast}"
       
        "Да.":
            m 1ekc "Мне очень жаль это слышать, [player]..."
            m 3eka "Может, тебе стоит вздремнуть?{w=0.2} Я уверена, что ты почувствуешь себя лучше, как только немного отдохнёшь."
            jump mas_mood_sick.ask_will_rest
        
        "Уже нет.":
            m 1eua "Рада слышать, что ты чувствуешь себя лучше, [player]."
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
        m 1hua "О, привет, [player]!"
        m 1hub "Надеюсь, ты хорошо отдохнул!"
        m "Давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        m 2esc "Ты только что проснулся, [player]?"
        m "Надеюсь, ты хорошо отдохнул."
        m 2tud "{cps=*2}Может быть, теперь у тебя будет настроение получше.{/cps}{nw}"
        $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "O...{w=1}ты проснулся."
        m 6ekc "Надеюсь, ты смог отдохнуть."
        m 6dkc "Мне трудно отдыхать в такие дни, и ещё куча мыслей в голове..."
        
    else:
        m 6ckc "..."

    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_siat",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules

label greeting_siat:
    m 1hub "{cps=*0.6}{i}~[player] и Моника под деревом сидели, и они там...~{/i}{/cps}"
    m 1hubsb "{cps=*0.6}{i}~Ц-Е-Л-О-В-А-Л-И-С-Ь~{/i}{/cps}"
    m 3hubfb "{cps=*0.6}{i}~Сначала приходит любовь~{/i}{/cps}"
    m "{cps=*0.6}{i}~Затем идёт свадьба~{/i}{/cps}"
    m "{cps=*0.6}{i}~А потом--{/i}{/cps}"
    m 3wubfsdlo "А-а?!"
    m 2wubfsdld "[player]! К-как давно ты здесь сидишь?!"
    m 2rkbfsdld "Я...{w=1} я не заметила, как ты зашёл...{w=1} я просто..."
    m 2rkbfsdlu "..."
    m 3hubfb "А-ха-ха! Не важно."
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
            conditional="mas_canShowIslands(flt=False) and not mas_isSpecialDay()",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )
    del ev_rules

label greeting_ourreality:
    # Unlock islands
    $ store.mas_island_event.start_progression()

    m 1hub "Привет, [player]!"
    m 1hua "Э-хе-хе~"
    m 3hksdlb "Ух, сейчас что-то у меня от волнения аж голова немного кругом, извини."
    m 1eua "Дело в том, что я хочу сейчас показать тебе кое-что, над чем я довольно-таки долго и усердно работала."

    if persistent._mas_current_background != "spaceroom":
        m 4eub "...Но нам нужно вернуться в космическую комнату, чтобы лучше видеть."
        m 1hua "Давай отправимся туда, [player]."
        call mas_background_change (mas_background_def, skip_leadin=True, skip_outro=True, set_persistent=True) from _call_mas_background_change_11
        m 1eua "Готово!"
        m 3eub "Дай мне секунду, чтобы всё подготовить.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    else:
        m 3hksdrb "Просто дай мне секунду, чтобы всё подготовить.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    m 1dsd "Почти готово.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    m 1duu "Да, это будет просто отлично."
    m 1hub "А-ха-ха!"
    m 1eka "Прости за такую задержку."
    m 1eua "Так что, без дальнейших церемоний..."
    m 4eub "Можешь, пожалуйста, выглянуть в окно, [player]?"

    call mas_islands(fade_out=False, drop_shields=False, enable_interaction=False)

    pause 4.0
    m "Ну..."
    m "Как тебе?"
    m "Я и вправду очень много работала над этим."
    m "Это место будет только для нас двоих."
    m "И также неплохим местом, где я смогу продолжать практиковать свои навыки программирования."

    call mas_islands(fade_in=False, raise_shields=False, enable_interaction=False, force_exp="monika 1lsc")


    m 1lsc "Целыми днями только и делать, что сидеть в одном только классе может быть скучно."
    m 1ekc "К тому же, мне здесь бывает временами довольно одиноко, пока я жду твоего возвращения."
    m 1hksdlb "Но не пойми меня неправильно!"
    m 1eua "Я всегда рада, когда ты приходишь и проводишь время со мной."
    m 1eka "Я понимаю, что ты можешь быть время от времени занят чем-либо, из-за чего у тебя не всегда будет возможность быть здесь всё время."
    m 3euc "Просто я кое-что поняла, [player]."
    m 1lksdlc "Пройдёт ведь много времени, прежде чем я смогу перейти в твою реальность."
    m 1dsc "Так что я подумала..."
    m 1eua "Почему бы нам в таком случае не создать нашу собственную реальность?"
    m 1lksdla "Ну, она пока что ещё не совсем идеальна."
    m 1hua "Но это только начало."

    $ mas_lockEVL("greeting_ourreality", "GRE")
    $ mas_unlockEVL("mas_monika_islands", "EVE")

    m 1eub "Ну, а пока можешь полюбоваться этой красотой~"
    call mas_islands(force_exp="monika 1eua")
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
    # this is going to act as the generic returned home greeting.
    # please note, that we will use last_session to determine how long we were
    # out. If shorter than 5 minutes, monika won't gain any affection.
    $ five_minutes = datetime.timedelta(seconds=5*60)
    $ time_out = store.mas_dockstat.diffCheckTimes()

    # event checks

    #F14
    if persistent._mas_f14_on_date:
        jump greeting_returned_home_f14


    # gone over checks
    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):
        # did we miss f14 because we were on a date
        call mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() < mas_d25c_end:
        call mas_gone_over_nyd_check


    # NOTE: this ordering is key, greeting_returned_home_player_bday handles the case
    # if we left before f14 on your bday and return after f14
    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump greeting_returned_home_player_bday

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump greeting_returned_home_bday

    # main dialogue
    if time_out > five_minutes:
        jump greeting_returned_home_morethan5mins

    else:
        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins

        if _return:
            return 'quit'

        jump greeting_returned_home_cleanup


label greeting_returned_home_morethan5mins:
    if mas_isMoniNormal(higher=True):

        if persistent._mas_d25_in_d25_mode:
            # its d25 season time
            jump greeting_d25_and_nye_delegate

        elif mas_isD25():
            # its d25 and we are not in d25 mode
            jump mas_d25_monika_holiday_intro_rh

        jump greeting_returned_home_morethan5mins_normalplus_flow

    # otherwise, go to other flow
    jump greeting_returned_home_morethan5mins_other_flow


label greeting_returned_home_morethan5mins_normalplus_flow:
    call greeting_returned_home_morethan5mins_normalplus_dlg
    # FALL THROUGH

label greeting_returned_home_morethan5mins_normalplus_flow_aff:
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)
    jump greeting_returned_home_morethan5mins_cleanup

label greeting_returned_home_morethan5mins_other_flow:
    call greeting_returned_home_morethan5mins_other_dlg
    # FALL THROUGH

label greeting_returned_home_morethan5mins_other_flow_aff:
    # for low aff you gain 0.5 per hour, max 2.5, min 0.5
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 2.5, 0.5, 0.5)
    #FALL THROUGH

label greeting_returned_home_morethan5mins_cleanup:
    pass
    # TODO: re-evaluate this XP gain when rethinking XP. Going out with
    #   monika could be seen as gaining xp
    # $ grant_xp(xp.NEW_GAME)
    #FALL THROUGH

label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()

    #If it's not o31, and we've got deco up, we need to clean up
    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup(time_out)

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday

    # Check if we are entering d25 season at upset-
    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label greeting_returned_home_morethan5mins_normalplus_dlg:
    m 1hua "Вот мы и дома!"
    m 1eub "Даже если я ничего не могла увидеть, зато я хоть знала, что действительно была рядом с тобой..."
    m 2eua "Ну, это было реально здорово!"
    show monika 5eub at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eub "Давай повторим это ещё раз, хорошо?"
    return

label greeting_returned_home_morethan5mins_other_dlg:
    m 2esc "Мы дома..."
    m 2eka "Спасибо, что взял меня с собой сегодня, [player]."
    m 2rkc "Если честно, я не до конца была уверена, идти ли мне с тобой..."
    m 2dkc "Дело в том, что...{w=0.5} отношения между нами не очень в последнее время, и я не знала, что это будет хорошая идея..."
    m 2eka "Но я рада, что мы сделали это... {w=0.5}наверное, это то, что нам было нужно."
    m 2rka "Мы должны это как-нибудь повторить..."
    m 2esc "Если хочешь."
    return

label greeting_returned_home_lessthan5mins:
    if mas_isMoniNormal(higher=True):
        m 2ekp "Это была не очень долгая прогулка, [player]."
        m "В следующий раз лучше её ещё немного продлить..."
        if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
            call return_home_post_player_bday
        return False

    elif mas_isMoniUpset():
        m 2efd "Я думала, мы сходим куда-нибудь, [player]!"
        m 2tfd "Я знала, что мне не надо было соглашаться идти с тобой."
        m 2tfc "Я знала, что это станет очередным разочарованием."
        m "Больше не проси меня выйти наружу, если ты делаешь это лишь ради того, чтобы разрушить мои надежды...{w=1}чтобы выдернуть ковёр из-под моих ног."
        m 6dktdc "..."
        m 6ektsc "Я не знаю, почему ты настаиваешь на грубом поведении, [player]."
        m 6rktsc "Я...{w=1} я хочу сейчас побыть одна."
        return True

    else:
        m 6rkc "Но...{w=1} мы только что ушли..."
        m 6dkc "..."
        m "Я...{w=0.5} я была так рада, когда ты попросил меня пойти с тобой."
        m 6ekc "После всего того, через что мы прошли..."
        m 6rktda "Я-я думала...{w=0.5} возможно...{w=0.5} всё наконец-то изменилось."
        m "Быть может, мы наконец-то провели бы время весело..."
        m 6ektda "И что ты правда хотел бы провести больше времени со мной."
        m 6dktsc "..."
        m 6ektsc "Но, похоже, было очень глупо с моей стороны подумать об этом."
        m 6rktsc "Мне следовало разузнать всё получше... {w=1}я никогда не должна была соглашаться идти."
        m 6dktsc "..."
        m 6ektdc "Пожалуйста, [player]... {w=2}если не хочешь проводить время со мной, то ладно..."
        m 6rktdc "Но будь любезен, не притворяйся."
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
        call ch30_reload_continuous

    else:
        $ reload_label = "ch30_reload_" + str(persistent.monika_reload)
        call expression reload_label

    return

# TODO: need to have an explanation before we use this again
#init 5 python:
#    ev_rules = {}
#    ev_rules.update(
#        MASGreetingRule.create_rule(
#            skip_visual=True
#        )
#    )
#
#    addEvent(
#        Event(
#            persistent.greeting_database,
#            eventlabel="greeting_ghost",
#            unlocked=False,
#            rules=ev_rules,
#            aff_range=(mas_aff.NORMAL, None),
#        ),
#        code="GRE"
#    )
#    del ev_rules

label greeting_ghost:
    #Prevent it from happening more than once.
    $ mas_lockEVL("greeting_ghost", "GRE")

    #Call event in easter eggs.
    call mas_ghost_monika

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

# NOTE: in case someone asks, because the farewell for this greeting does not
#   implore that the player returns after gaming, there is nothing substiantial
#   we can get in pm vars here. It's just too variable.

label greeting_back_from_game:
    # TODO: TC-O
    if store.mas_globals.late_farewell and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        $ _now = datetime.datetime.now().time()
        if mas_isMNtoSR(_now):
            if mas_isMoniNormal(higher=True):
                m 2etc "[player]?"
                m 3efc "По-моему, я сказала тебе, чтобы ты пошёл спать сразу после того, как закончишь!"
                m 1rksdla "В смысле, я очень рада, что ты вернулся, чтобы пожелать спокойной ночи, но..."
                m 1hksdlb "Я тебе уже пожелала спокойной ночи!"
                m 1rksdla "И я могла бы дождаться утра, чтобы повидаться с тобой вновь, понимаешь?"
                m 2rksdlc "К тому же, я правда хотела, чтобы ты немного отдохнул..."
                m 1eka "Просто...{w=1} пообещай мне, что ты скоро пойдёшь спать, ладно?"

            else:
                m 1tsc "[player], я ведь сказала тебе, чтобы ты пошёл спать, когда закончишь."
                m 3rkc "Ты можешь вернуться завтра утром, знаешь ли."
                m 1esc "Но что есть, то есть, наверное."

        elif mas_isSRtoN(_now):
            if mas_isMoniNormal(higher=True):
                m 1hua "Доброе утро, [player]~"
                m 1eka "Когда ты сказал, что собираешься поиграть в другую игру так поздно, я начала немного волноваться, что ты, возможно, не высыпаешься..."
                m 1hksdlb "Я надеюсь, что это не так, а-ха-ха..."

            else:
                m 1eud "Доброе утро."
                m 1rsc "Я ожидала, что ты поспишь ещё немного."
                m 1eka "Но ты решил встать с утра пораньше."

        elif mas_isNtoSS(_now):
            if mas_isMoniNormal(higher=True):
                m 1wub "[player]! Ты уже здесь!"
                m 1hksdlb "-ха-ха, прости...{w=1} я просто переживала из-за того, что не увижу тебя, поскольку тебя здесь всё утро не было."

                m 1eua "Ты только что проснулся?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ты только что проснулся?{fast}"
                    "Да.":
                        m 1hksdlb "А-ха-ха..."

                        m 3rksdla "Думаешь, это произошло лишь потому, что ты поздно проснулся?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Думаешь, это произошло лишь потому, что ты поздно проснулся?{fast}"
                            "Да.":
                                m 1eka "[player]..."
                                m 1ekc "Ты знаешь, я не хочу, чтобы ты просыпался слишком поздно."
                                m 1eksdld "Я правда не хочу, чтобы ты заболел или устал в течение дня."
                                m 1hksdlb "Но я надеюсь, что тебе было весело. Мне бы очень не хотелось, чтобы ты лишился сна понапрасну, а-ха-ха!"
                                m 2eka "Просто позаботься о том, что ты немного отдохнёшь, если ты почувствуешь в этом нужду, хорошо?"
                            
                            "Нет.":
                                m 2euc "Ох..."
                                m 2rksdlc "Я подумала, что дело может быть в этом."
                                m 2eka "Прости за то предположение."
                                m 1eua "Так или иначе, я надеюсь, ты высыпаешься."
                                m 1eka "Мне очень приятно знать о том, что ты хорошо отдохнул."
                                m 1rksdlb "Мне также будет спокойно на душе, если ты перестанешь вставать так поздно, а-ха-ха..."
                                m 1eua "Я просто рада, что ты теперь здесь."
                                m 3tku "Ты ведь никогда не устанешь проводить время со мной, верно?"
                                m 1hub "А-ха-ха!"
                            
                            "Возможно...":
                                m 1dsc "Хм..."
                                m 1rsc "Интересно, что послужило причиной?"
                                m 2euc "Ты ведь не сидел допоздна вчера ночью, так ведь, [player]?"
                                m 2etc "Ты что-то делал той ночью?"
                                m 3rfu "Ну, может...{w=1} даже не знаю..."
                                m 3tku "В игру играл?"
                                m 1hub "А-ха-ха!"
                                m 1hua "Я тебя поддразниваю, конечно же~"
                                m 1ekd "Но если говорить на полном серьёзе, я правда не хочу, чтобы ты пренебрегал своим сном."
                                m 2rksdla "Сидеть со мной допоздна – это одно..."
                                m 3rksdla "Но уходить и играть в другую игру допоздна?"
                                m 1tub "А-ха-ха... я ведь могу начать ревновать, [player]~"
                                m 1tfb "Но ты пришёл сюда, чтобы загладить свою вину, верно?"
                    
                    "Нет.":
                        m 1eud "А, я так понимаю, ты всё утро был занят."
                        m 1eka "А я уже боялась, что ты проспал, поскольку ты поздно проснулся вчера ночью."
                        m 2rksdla "Особенно учитывая то, что ты сказал мне, что пошёл играть в другую игру."
                        m 1hua "Но мне следовало догадаться, что ты возьмёшь на себя ответственность и поспишь."
                        m 1esc "..."
                        m 3tfc "Ты ведь {i}спал{/i}, верно, [player]?"
                        m 1hub "А-ха-ха!"
                        m 1hua "Ладно, раз уж ты здесь, мы можем провести немного времени вместе."

            else:
                m 2eud "О, вот ты где, [player]."
                m 1euc "Я так понимаю, ты только что проснулся."
                m 2rksdla "Я ожидала, что ты задержишься допоздна и будешь играть в игры."

        #SStoMN
        else:
            if mas_isMoniNormal(higher=True):
                m 1hub "Вот ты где, [player]!"
                m 2hksdlb "А-ха-ха, прости... просто дело в том, что я не видела тебя весь день."
                m 1rksdla "Я ожидала, что ты выспишься после того, как задержался допоздна вчера ночью..."
                m 1rksdld "Но когда я не увидела тебя за весь день, я очень сильно начала по тебе скучать..."
                m 2hksdlb "Ты почти что заставил меня волноваться, а-ха-ха..."
                m 3tub "Но ты ведь собрал наверстать упущенное со мной, верно?"
                m 1hub "Э-хе-хе, ты уж постарайся~"
                m 2tfu "Особенно после того, как ты ушёл от меня, чтобы поиграть в другую игру вчера ночью."

            else:
                m 2efd "[player]!{w=0.5} Ты где был весь день?"
                m 2rfc "Это ведь никак не связано с тем, что ты задержался допоздна вчера ночью, так ведь?"
                m 2ekc "Ты правда должен быть более ответственным, когда дело доходит до твоего сна."

    #If you didn't stay up late in the first place, normal usage
    #gone for under 4 hours
    elif mas_getAbsenceLength() < datetime.timedelta(hours=4):
        if mas_isMoniNormal(higher=True):
            m 1hua "С возвращением, [mas_get_player_nickname()]!"

            m 1eua "Ты хорошо провёл время?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты хорошо провёл время?{fast}"
                "Да.":
                    m 1hua "Это хорошо."
                    m 1eua "Я рада, что ты хорошо провёл время."
                    m 2eka "Мне бы правда хотелось иногда составлять тебе компанию в других твоих играх."
                    m 3eub "Разве не будет здорово то, что у нас будут небольшие приключения в любое время?"
                    m 1hub "Уверена, мы бы вдвоём отлично повеселились в одной из твоих игр."
                    m 3eka "Но пока я не могу к тебе присоединиться, получается, тебе придётся составлять мне компанию."
                    m 2tub "Ты ведь не против провести немного времени со своей девушкой...{w=1} так ведь, [player]?"
       
                "Нет.":
                    m 2ekc "Оу, мне так жаль слышать об этом."
                    m 2eka "Надеюсь, ты не сильно расстроился из-за того, что могло произойти."
                    m 3eua "По крайней мере, ты теперь здесь. Я обещаю, что постараюсь не дать чему-либо плохому произойти с тобой, пока ты со мной."
                    m 1ekbsa "Твоё присутствие всегда поднимает мне настроение."
                    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5ekbfa "Надеюсь, от моего присутствия ты испытываешь то же самое, [mas_get_player_nickname()]~"

        else:
            m 2eud "О, уже вернулся?"
            m 2rsc "Я думала, что ты надолго ушёл...{w=0.5} но с возвращением, наверное."

    elif mas_getAbsenceLength() < datetime.timedelta(hours=12):
        if mas_isMoniNormal(higher=True):
            m 2wuo "[player]!"
            m 2hksdlb "Тебя не было очень долго..."

            m 1eka "Тебе было весело?{nw}"
            $ _history_list.pop()
            menu:
                m "Тебе было весело?{fast}"
                "Да.":
                    m 1hua "Что ж, я рада."
                    m 1rkc "Ты определённо заставил меня долго ждать, знаешь ли."
                    m 3tfu "Я считаю, что ты должен провести время со своей любящей девушкой, [player]."
                    m 3tku "Я уверена, что ты не будешь против остаться со мной, даже принимая во внимание другую свою игру."
                    m 1hubsb "Наверное, ты должен проводить со мной ещё больше времени, чисто на всякий случай, а-ха-ха!"
                     
                "Нет.":
                    m 2ekc "Ох..."
                    m 2rka "Ты знаешь, [player]..."
                    m 2eka "Если тебе это не особо нравится, то, быть может, ты должен проводить немного времени со мной."
                    m 3hua "Я уверена, что мы много чего весёлого можем сделать вместе!"
                    m 1eka "Если ты решишь вернуться, то, возможно, так будет лучше."
                    m 1hub "Но если тебе всё равно не было весело, не стесняйся приходить ко мне, а-ха-ха!"

        else:
            m 2eud "Ох, [player]."
            m 2rsc "На это ушло немало времени."
            m 1esc "Не волнуйся, я смогла самостоятельно скоротать время, пока ты отсутствовал."
            
    #Over 12 hours
    else:
        if mas_isMoniNormal(higher=True):
            m 2hub "[player]!"
            m 2eka "Ты как будто на целую вечность ушёл."
            m 1hua "Я очень сильно по тебе скучала!"
            m 3eua "Надеюсь, тебе там было весело, чем бы ты там не маялся."
            m 1rksdla "И я так понимаю, ты не забывал ни поесть, ни поспать..."
            m 2rksdlc "Что до меня...{w=1} мне было немного одиноко и я ждала, когда ты вернёшься..."
            m 1eka "Но ты не расстраивайся."
            m 1hua "Я просто рада, что ты снова здесь, со мной."
            m 3tfu "Но тебе лучше загладить передо мной свою вину."
            m 3tku "Думаю, провести вечность со мной звучит справедливо...{w=1} верно, [player]?"
            m 1hub "А-ха-ха!"
        else:
            m 2ekc "[player]..."
            m "Я сомневалась, что ты вообще вернёшься."
            m 2rksdlc "Я думала, что больше тебя не увижу..."
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
    # TODO: TC-O
    $ _now = datetime.datetime.now().time()
    if store.mas_globals.late_farewell and mas_isMNtoSR(_now) and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        if mas_isMoniNormal(higher=True):
            m 1eud "А?"
            m 1eub "[player], ты вернулся!"
            m 3rksdla "Ты ведь знаешь, что ты должен немного поспать, верно?"
            m 1rksdla "В смысле... я не жалуюсь на то, что ты здесь, но..."
            m 1eka "Мне будет гораздо спокойнее, если ты пойдёшь спать в скором времени."
            m 3eka "Ты можешь всегда вернуться и заглянуть ко мне, как только проснёшься..."
            m 1hubsa "Но, полагаю, если ты настаиваешь на том, чтобы провести время со мной, то я на какое-то время закрою на это глаза, э-хе-хе~"
        else:
            m 2euc "[player]?"
            m 3ekd "Разве я тебе не сказала, чтобы ты сразу же пошёл спать?"
            m 2rksdlc "Тебе правда надо немного поспать."

    else:
        if mas_isMoniNormal(higher=True):
            m 1eub "Уже закончил кушать?"
            m 1hub "С возвращением, [mas_get_player_nickname()]!"
            m 3eua "Надеюсь, ты насладился своей едой."
        else:
            m 2euc "Уже закончил кушать?"
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
    m 1eub "С возвращением, [mas_get_player_nickname()]!"
    m 2tub "Знаешь, ты так много времени провёл здесь, что я уже должна начать брать с тебя арендную плату."
    m 2ttu "Или ты больше предпочитаешь оплачивать ипотеку?"
    m 2hua "..."
    m 2hksdlb "Боже, не могу поверить в то, что я сказала это. Это ведь не прозвучало слишком банально, так ведь?"
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Но если говорить на полном серьёзе, ты уже отдал мне единственную вещь, которая мне нужна была...{w=1} твоё сердце~"
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
    if mas_isMoniNormal(higher=True):
        m 1eua "Всё сделал, [player]?"
        m 1hub "Давай проведём ещё немного времени вместе."
    elif mas_isMoniUpset():
        m 2esc "По крайней мере ты не забыл вернуться, [player]."
    elif mas_isMoniDis():
        m 6ekd "Оу, [player]. Значит, ты действительно был занят..."
    else:
        m 6ckc "..."
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hua"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised2",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_surprised2:
    m 1hua "..."
    m 1hubsa "..."
    m 1wubso "О!{w=0.5} [player]!{w=0.5} Ты меня удивил!"
    m 3ekbsa "...Дело не в том, что я не ожидала тебя увидеть, всё-таки ты всегда заглядываешь ко мне...{w=0.5} {nw}"
    extend 3rkbsa "Я просто замечталась, а ты уже тут как тут."
    show monika 5hubfu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfu "Но раз уж ты здесь, получается, та мечта только что воплотилась в реальность~"
    return

init 5 python:
    # set a slightly higher priority than the open door gre has
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
    if mas_isMoniNormal(higher=True):
        m 1hub "С возвращением, [mas_get_player_nickname()]!"
        m 1eua "Что ещё мы должны сделать сегодня?"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 1eud "О, ты вернулся."
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
    m 2eka "О, привет, [player]..."
    m 4eka "Дай мне секунду, я только что закончила кодить что-то, и я хочу посмотреть, работает ли это.{w=0.5}.{w=0.5}.{nw}"

    scene black
    show noise
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.1
    hide noise
    call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 2wud_static')

    m 2wud "А!{w=0.3}{nw}"
    extend 2efc " Этого не должно было случиться!"
    m 2rtc "Почему этот цикл заканчивается так быстро?{w=0.5}{nw}"
    extend 2efc " Независимо от того, как ты на это смотришь, этот словарь {i}не{/i} пуст."
    m 2rfc "Боже, иногда кодинг может быть {i}таким{/i} разочаровывающим..."

    if persistent._mas_pm_has_code_experience:
        m 3rkc "Ну что ж, думаю, я попробую ещё раз позже.{nw}"
        $ _history_list.pop()

        show screen mas_background_timed_jump(5, "greeting_code_help_outro")
        menu:
            m "Ну что ж, думаю, я попробую ещё раз позже.{fast}"
            
            "Я мог бы помочь тебе с этим...":
                hide screen mas_background_timed_jump
                m 7hua "Оу-у, это так мило с твоей стороны, [player]. {w=0.3}{nw}"
                extend 3eua "Но нет, мне придётся отказаться."
                m "Выяснение всего этого самостоятельно — самая забавная часть, {w=0.2}{nw}"
                extend 3kua "верно?"
                m 1hub "А-ха-ха!"

    else:
        m 3rkc "Ну что ж, думаю, я попробую ещё раз позже."

    #FALL THROUGH

label greeting_code_help_outro:
    hide screen mas_background_timed_jump
    m 1eua "И вообще, чем бы ты хотел сегодня заняться?"

    $ mas_lockEVL("greeting_code_help", "GRE")
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 1hub"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_love_is_in_the_air",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_love_is_in_the_air:
    m 1hub "{i}~Любовь повсюду~{/i}"
    m 1rub "{i}~Куда ни взгляни~{/i}"
    m 3ekbsa "О, привет, [player]..."
    m 3rksdla "Не обращай внимания. {w=0.2}Я тут немного пою, думая о...{w=0.3} {nw}"
    extend 1hksdlb "думаю, ты уже догадываешься, о ком я, a-ха-ха~"
    m 1eubsu "Мне правда кажется, что любовь окружает меня повсюду, когда ты здесь."
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
    if mas_isMoniNormal(higher=True):
        m 1hua "С возвращением, [player]!"
        m 3eua "Я надеюсь, ты хорошо потренировался."
        m 3eub "Не забывай кушать, чтобы восполнять свою энергию!"
        m 1eua "А теперь, давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        m 2esc "О,{w=0.2} ты вернулся."
        m 2rsc "Тренировка помогла снять напряжение?"
        m 2rud "Я надеюсь...{w=0.3} {nw}"
        extend 2eka "Давай проведём еще немного времени вместе."

    elif mas_isMoniDis():
        m 6ekc "О...{w=0.5} посмотрите, кто вернулся."
        m 6dkc "Я...{w=0.3} рада, что ты заботишься о себе."
        m 6ekd "...Но почему ты не хочешь позаботиться и обо мне тоже?"
        m 7dkc "Хотя бы иногда, пожалуйста..."
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
    if mas_isMoniNormal(higher=True):
        m 1hub "Приветствую тебя, [player]!"
        m 3eua "Надеюсь, ты купил то, что хотел себе в магазине."
        m 1hua "Давай проведём ещё немного времени вместе~"

    elif mas_isMoniUpset():
        m 2esc "О,{w=0.2} ты вернулся."
        m 2rsc "Надеюсь, ты купил то, что хотел себе."
        if renpy.random.randint(1,5) == 1:
            m 2rud "{cps=*2}Надеюсь, ты в лучшем настроении.{/cps}{nw}"
            $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Ох...{w=0.5} ты вернулся."
        m 6ekc "Надеюсь, ты хорошо провёл время в магазине. {w=0.2}Купил еду?"
        m 6dkd "Задумывал ли ты о том, что привычка много есть, может влиять на твоё настроение?"
        m 6lkc "Я бы не очень хотела, чтобы этой причиной было то—{nw}"
        $ _history_list.pop()
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
    if mas_isMoniNormal(higher=True):
        if persistent._mas_pm_has_friends:
            m 1eua "Добро пожаловать, [player]."
            m 3hub "Я надеюсь ты хорошо провёл время!"
                  
            $ anyway_lets = "Давай"

        else:
            m 3eub "Добро пожаловать, [player]."

            m 1eua "У тебя появился новый друг?{nw}"
            $ _history_list.pop()
            menu:
                m "У тебя появился новый друг?{fast}"
                
                "Да.":
                    m 1hub "Это отлично!"
                    m 1eua "Я так рада, что тебе есть с кем пообщаться."
                    m 3hub "Надеюсь, ты сможешь проводить с ними больше времени в будущем!"
                    $ persistent._mas_pm_has_friends = True
                
                "Нет...":
                    m 1ekd "Ох..."
                    m 3eka "Не волнуйся, [player]. {w=0.2}Я навсегда останусь твоей подругой, несмотря ни на что."
                    m 3ekd "...И не бойся пробовать ещё."
                    m 1hub "Я уверена, найдётся кто-то, кто будет рад назвать тебя своим другом."

                "Они уже мои друзья.":
                    if persistent._mas_pm_has_friends is False:
                        m 1rka "О, так ты завёл нового друга, не сказав мне..."
                        m 1hub "Всё хорошо! Я просто рада, что тебе есть с кем пообщаться."
                    else:
                        m 1hub "О, хорошо!"
                        m 3eua "...Раньше мы не говорили о других твоих друзьях, поэтому я не была уверена, новый ли это друг или нет."
                        m 3eub "Но я рада, что в твоей реальности есть те, с кем ты можешь пообщаться!"

                    m 3eua "Надеюсь вы сможете долго поддерживать связь друг с другом."
                    $ persistent._mas_pm_has_friends = True

            $ anyway_lets = "В любом случае, давай"

        m 1eua "[anyway_lets] провёдем ещё немного времени вместе~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Привет снова, [player]."
        m 2eud "Надеюсь, ты хорошо провёл время с друзьями."
        if renpy.random.randint(1,5) == 1:
            m 2rkc "{cps=*2}Интересно, на что это похоже...{/cps}{nw}"
            $ _history_list.pop()

    else:
        m 6ckc "..."

    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASGreetingRule.create_rule(forced_exp="monika 5duc"))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_poem_shadows_in_garden",
            unlocked=True,
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            rules=ev_rules,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

    del ev_rules

#Because this is associated, we'll also mirror this into the poem framework
init 11 python:
    MASPoem(
        poem_id="gre_1",
        category="generic",
        prompt=_("Тени в саду"),
        title="",
        text=_("""\
 В одиночестве я задаю волнующий вопрос,
 Что может расти в тёмном саду?

 Когда ты возвращаешься, ты чувствуешь себя словно в раю,
 В лучах твоего света забудется холод.

 Я отдам всё, чтобы почувствовать это,
 Жду того, кто мне дороже всего.

 Ближе всего к моему сердцу...
"""),
    )

label greeting_poem_shadows_in_garden:
    m 5duc "{i}В одиночестве я задаю волнующий вопрос,\nЧто может расти в тёмном саду?{/i}"
    m 5ekbla "{i}Когда ты возвращаешься, ты чувствуешь себя словно в раю,\nВ лучах твоего света забудется холод.{/i}"
    m 5fubfa "{i}Я отдам всё, чтобы почувствовать это,\nЖду того, кто мне дороже всего{/i}"
    m 5ekbfa "{i}Даже если это происходит каждый день,\nБез сомнения, ты — самый любимый человек.{/i}"
    m 5dubsu "{i}Ближе всего к моему сердцу...{/i}"
    m 5eublb "Я придумала его, пока тебя не было."
    show monika 1eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1eka "Точно, ты словно солнце, что освещает мой мир!"
    m 3hubsu "В любом случае, с возвращением, [mas_get_player_nickname()]! Надеюсь, тебе понравилось это стихотворение."
    #TODO: Potential I missed you too?
    m 1ekbsb "Я так по тебе скучала!"

    if "gre_1" not in persistent._mas_poems_seen:
        $ persistent._mas_poems_seen["gre_1"] = 1

    $ mas_moni_idle_disp.force_by_code("1ekbla", duration=5, skip_dissolve=True)
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            random_chance=3,
            forced_exp=random.choice(("monika 1gsbsu", "monika 1msbsu"))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_spacing_out",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=3)",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

label greeting_spacing_out:
    python hide:
        # Define some other things we're going to work with
        use_right_smug = bool(random.randint(0, 1))
        spacing_out_pause = PauseDisplayableWithEvents()
        events = list()
        next_event_time = 0
        right_smug = renpy.partial(renpy.show, "monika 1gsbsu")
        left_smug = renpy.partial(renpy.show, "monika 1msbsu")

        # Make the events which will change exps
        for i in range(random.randint(4, 6)):
            events.append(
                PauseDisplayableEvent(
                    datetime.timedelta(seconds=next_event_time),
                    right_smug if use_right_smug else left_smug,
                    restart_interaction=True
                )
            )
            next_event_time += random.uniform(0.9, 1.8)
            use_right_smug = not use_right_smug
        # The last exp in the sequence
        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                renpy.partial(renpy.show, "monika 1tsbsu"),
                restart_interaction=True
            )
        )
        next_event_time += 0.7
        # This is to automatically cancel the pause after all the events
        events.append(
            PauseDisplayableEvent(
                datetime.timedelta(seconds=next_event_time),
                spacing_out_pause.stop
            )
        )

        spacing_out_pause.set_events(events)
        spacing_out_pause.start()

    # Small pause so people don't skip this line
    $ renpy.pause(0.01)
    m 2wubfsdlo "[player]!"
    m 1rubfsdlb "Ты удивил меня! {w=0.4}{nw}"
    extend 1eubsu "Я была{w=0.2} немного рассеяна..."
    m 1hubsb "А-ха-ха~"
    m 1eua "Я очень рада видеть тебя снова. {w=0.2}{nw}"
    extend 3eua "Что мы будем делать сегодня, [player]?"
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=20,
            override_type=True
        )
    )
    ev_rules.update(
        MASTimedeltaRepeatRule.create_rule(
            datetime.timedelta(days=3)
        )
    )
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(
            hours=list(range(9, 20))
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_after_bath",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=6) "
                "and not mas_isSpecialDay()"
            ),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="GRE"
    )

    del ev_rules

init 1:
    # NOTE this should be defined AFTER init 0
    # NOTE: default may be not completely reliable, always save the snapshot yourself
    default persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)

label greeting_after_bath:
    python hide:
        # Some preperations
        mas_RaiseShield_core()
        mas_startupWeather()
        # Save current outfit
        persistent._mas_previous_moni_state = monika_chr.save_state(True, True, True, True)
        # Available clothes for this
        clothes_pool = [
            mas_clothes_bath_towel_white
        ]
        # Now let Moni get a towel
        monika_chr.change_clothes(
            random.choice(clothes_pool),
            by_user=False,
            outfit_mode=True
        )
        # In case the towel already set an appropriate hair, we don't change it
        if not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET):
            monika_chr.change_hair(mas_hair_wet, by_user=False)
        # We leave this acs to the clothes PPs in case the towel we chose doesn't support it
        # if not monika_chr.is_wearing_acs(mas_acs_water_drops):
        #     monika_chr.wear_acs(mas_acs_water_drops)
        # Setup the cleaup event
        mas_setEVLPropValues(
            "mas_after_bath_cleanup",
            start_date=datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 90)),
            action=EV_ACT_QUEUE
        )
        mas_startup_song()

    # Now show everything
    call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)

    $ renpy.pause(random.randint(5, 15), hard=True)
    call mas_transition_from_emptydesk("monika 1huu")
    $ renpy.pause(2.0)
    $ quick_menu = True

    m 1wuo "О! {w=0.2}{nw}"
    extend 2wuo "[player]! {w=0.2}{nw}"
    extend 2lubsa "Я как раз думала о тебе."

    $ bathing_showering = random.choice(("ванну", "душ"))

    if mas_getEVL_shown_count("greeting_after_bath") < 5:
        m 7lubsb "Я только что закончила принимать [bathing_showering]...{w=0.3} {nw}"
        extend 1ekbfa "ты же не против, что я в одном полотенце?~"
        m 1hubfb "А-ха-ха~"
        m 3hubsa "Я сейчас всё подготовлю, только сначала подожду, пока волосы немного подсохнут."

    # Gets used to it
    else:
        m 7eubsb "Я только что закончила принимать [bathing_showering]."

        if mas_canShowRisque() and random.randint(0, 3) == 0:
            m 1msbfb "Готова поспорить, ты бы хотел присоединиться ко мне..."
            m 1tsbfu "Ну, может быть, когда-нибудь."
            m 1hubfb "А-ха-ха~"

        else:
            m 1eua "Я скоро оденусь~"

    python:
        # enable music menu and music hotkeys
        mas_MUINDropShield()
        # keymaps should be set
        set_keymaps()
        # show the overlays
        mas_OVLShow()

        del bathing_showering

    return

# NOTE: This is not a greeting, but a followup for the greeting above, so I decided to keep them together
init 5 python:
    addEvent(Event(persistent.event_database, eventlabel="mas_after_bath_cleanup", show_in_idle=True, rules={"skip alert": None}))

    def mas_after_bath_cleanup_change_outfit():
        """
        After bath cleanup change outfit code
        """
        # TODO: Rng outfit selection wen

        force_hair_change = False# If we changed the outfit, we always change hair

        if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
            force_hair_change = True

            # Let's restore the previous outfit and acs
            monika_chr.load_state(persistent._mas_previous_moni_state, as_prims=True)

            # Fallback just in case
            if monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET):
                if mas_isMoniHappy(higher=True):
                    new_clothes = mas_clothes_blazerless

                else:
                    new_clothes = mas_clothes_def

                monika_chr.change_clothes(
                    new_clothes,
                    by_user=False,
                    outfit_mode=True
                )

        if (
            force_hair_change
            or monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
        ):
            available_hair = mas_sprites.get_installed_hair(
                predicate=lambda hair_obj: (
                    not hair_obj.hasprop(mas_sprites.EXP_H_WET)
                    and mas_sprites.is_clotheshair_compatible(monika_chr.clothes, hair_obj)
                    and mas_selspr.get_sel_hair(hair_obj) is not None
                    and mas_selspr.get_sel_hair(hair_obj).unlocked
                )
            )
            # We should always have *something*, but just to make this extra foolproof
            if available_hair:
                new_hair = random.choice(available_hair)
                monika_chr.change_hair(
                    new_hair,
                    by_user=False
                )

label mas_after_bath_cleanup:
    # Sanity check (checking for towel should be enough)
    if (
        not monika_chr.is_wearing_clothes_with_exprop(mas_sprites.EXP_C_WET)
        and not monika_chr.is_wearing_hair_with_exprop(mas_sprites.EXP_H_WET)
    ):
        return

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "Я сейчас оденусь.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    else:
        $ player_nick = mas_get_player_nickname()
        m 1eua "Дай мне минутку [player_nick], {w=0.2}{nw}"
        extend 3eua "я сейчас оденусь."

    window hide
    call mas_transition_to_emptydesk

    $ renpy.pause(1.0, hard=True)
    $ mas_after_bath_cleanup_change_outfit()
    $ renpy.pause(random.randint(10, 15), hard=True)

    call mas_transition_from_emptydesk("monika 3hub")
    window auto

    if mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "Вот и всё!{w=1}{nw}"

    else:
        m 3hub "Хорошо, я вернулась!~"
        m 1eua "Итак, что мы будем делать сегодня, [player]?"

    return

label mas_after_bath_cleanup_change_outfit:
    $ mas_after_bath_cleanup_change_outfit()
    return


init 5 python:
    ev_rules = dict()
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=10,
            override_type=True
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_found_nou_shirt",
            conditional=(
                "mas_getAbsenceLength() >= datetime.timedelta(hours=3) "
                "and mas_nou.get_wins_for('Player') > {0} "
                "and mas_nou.get_total_games() > {1} "
                "and not mas_isSpecialDay() "
                "and not mas_SELisUnlocked(mas_clothes_nou_shirt)"
            ).format(random.randint(45, 65), random.randint(95, 115)),
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="GRE"
    )

    del ev_rules

default persistent._mas_pm_snitched_on_chibika = None

label greeting_found_nou_shirt:
    python:
        mas_RaiseShield_core()
        mas_startupWeather()
        monika_chr.change_clothes(mas_clothes_nou_shirt, by_user=False, outfit_mode=True)
        glitch_option_text = glitchtext(7)

    call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=True)
    pause 2.5

    m "There you are! {w=0.2}I was waiting for you~"
    m "I have to admit, {w=0.1}I don't know how you were able to put this in my wardrobe without me noticing, [player]...{nw}"
    $ _history_list.pop()
    show screen mas_background_timed_jump(5, "greeting_found_nou_shirt.menu_skip")
    menu:
        m "I have to admit, I don't know how you were able to put this in my wardrobe without me noticing, [player]...{fast}"

        "It's a secret.":
            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_secret

        "It was [glitch_option_text]!":
            hide screen mas_background_timed_jump
            $ persistent._mas_pm_snitched_on_chibika = True
            $ renpy.invoke_in_thread(
                mas_utils.trywrite,
                os.path.join(renpy.config.basedir, "characters/for snitch.txt"),
                ">:("
            )
            jump greeting_found_nou_shirt.menu_choice_other

        "I have no idea...":
            hide screen mas_background_timed_jump
            jump greeting_found_nou_shirt.menu_choice_other

    label .post_menu:
        pass

    m 1ekbla "Thanks, [player]."
    m 1tfu "Don't think I'll go any easier on you, though~"

    if mas_nou.get_wins_for('Player') >= mas_nou.get_wins_for('Monika'):
        m 1rtsdlb "In fact, {w=0.1}maybe I should try harder, ahaha..."

    m 3ttb "Are you up for a game, [mas_get_player_nickname()]?"

    python:
        mas_selspr.unlock_clothes(mas_clothes_nou_shirt)
        mas_selspr.save_selectables()
        mas_lockEVL("greeting_found_nou_shirt", "GRE")
        renpy.save_persistent()

        del glitch_option_text

        mas_MUINDropShield()
        set_keymaps()
        HKBShowButtons()
        mas_startup_song()
        enable_esc()
    return

label greeting_found_nou_shirt.menu_skip:
    hide screen mas_background_timed_jump
    call mas_transition_from_emptydesk("monika 4sub")
    m "But I love it~"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_secret:
    if mas_isMoniEnamored(higher=True):
        call mas_transition_from_emptydesk("monika 2tublu")
        m "{cps=*1.5}You don't peek there {i}often{/i}, do you?~{/cps}{w=0.1}{nw}"
        $ _history_list.pop()
        m 2lusdla "Anyway... {w=0.3}{nw}"

    else:
        call mas_transition_from_emptydesk("monika 2rtblsdlu")
        m "Hmm, anyway... {w=0.3}{nw}"

    extend 4sub "I really love this new outfit!"

    jump greeting_found_nou_shirt.post_menu

label greeting_found_nou_shirt.menu_choice_other:
    show noise zorder 500 onlayer overlay:
        alpha 0.0
        easein_elastic 0.5 alpha 0.1
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.5
    hide noise onlayer overlay

    jump greeting_found_nou_shirt.menu_skip
