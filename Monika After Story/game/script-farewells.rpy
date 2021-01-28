











default persistent.mas_late_farewell = False

init -1 python in mas_farewells:
    import datetime
    import store

    dockstat_iowait_label = None



    dockstat_rtg_label = None



    dockstat_cancel_dlg_label = None



    dockstat_wait_menu_label = None



    dockstat_cancelled_still_going_ask_label = None



    dockstat_failed_io_still_going_ask_label = None

    def resetDockstatFlowVars():
        """
        Resets all the dockstat flow vars back to the original states (None)
        """
        store.mas_farewells.dockstat_iowait_label = None
        store.mas_farewells.dockstat_rtg_label = None
        store.mas_farewells.dockstat_cancel_dlg_label = None
        store.mas_farewells.dockstat_wait_menu_label = None
        store.mas_farewells.dockstat_cancelled_still_going_ask_label = None
        store.mas_farewells.dockstat_failed_io_still_going_ask_label = None

    def _filterFarewell(
            ev,
            curr_pri,
            aff,
            check_time,
        ):
        """
        Filters a farewell for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ev.anyflags(store.EV_FLAG_HFRS):
            return False
        
        
        if not ev.unlocked:
            return False
        
        
        if ev.pool:
            return False
        
        
        if not ev.checkAffection(aff):
            return False
        
        
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False
        
        
        if not (
            store.MASSelectiveRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASNumericalRepeatRule.evaluate_rule(check_time, ev, defval=True)
            and store.MASGreetingRule.evaluate_rule(ev, defval=True)
        ):
            return False
        
        
        if ev.conditional is not None and not eval(ev.conditional, store.__dict__):
            return False
        
        
        return True


    def selectFarewell(check_time=None):
        """
        Selects a farewell to be used. This evaluates rules and stuff appropriately.

        IN:
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single farewell (as an Event) that we want to use
        """
        
        fare_db = store.evhand.farewell_database
        
        
        fare_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection
        
        if check_time is None:
            check_time = datetime.datetime.now()
        
        
        for ev_label, ev in fare_db.iteritems():
            if _filterFarewell(
                ev,
                curr_priority,
                aff,
                check_time
            ):
                
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    fare_pool = []
                
                
                fare_pool.append((
                    ev, store.MASProbabilityRule.get_probability(ev)
                ))
        
        
        if len(fare_pool) == 0:
            return None
        
        return store.mas_utils.weightedChoice(fare_pool)


label mas_farewell_start:



    if persistent._mas_long_absence:
        $ pushEvent("bye_long_absence_2")
        return

    $ import store.evhand as evhand


    python:



        Event.checkEvents(evhand.farewell_database)

        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

    if len(bye_pool_events) > 0:

        python:

            bye_prompt_list = sorted([
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ])

            most_used_fare = sorted(bye_pool_events.values(), key=Event.getSortShownCount)[-1]


            final_items = [
                (_("До свидания."), -1, False, False, 20),
                (_("Не важно."), False, False, False, 0)
            ]




            if mas_anni.pastOneMonth() and mas_isMoniAff(higher=True) and most_used_fare.shown_count > 0:
                final_items.insert(1, (most_used_fare.prompt, most_used_fare, False, False, 0))
                _menu_area = mas_ui.SCROLLABLE_MENU_VLOW_AREA

            else:
                _menu_area = mas_ui.SCROLLABLE_MENU_LOW_AREA


        call screen mas_gen_scrollable_menu(bye_prompt_list, _menu_area, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)

        if not _return:

            return _return

        if _return != -1:

            $ pushEvent(_return.eventlabel)
            return


    $ farewell = store.mas_farewells.selectFarewell()
    $ pushEvent(farewell.eventlabel)

    $ mas_idle_mailbox.send_skipmidloopeval()

    return









init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already",
            unlocked=True,
            conditional="mas_getSessionLength() <= datetime.timedelta(minutes=20)",
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_leaving_already:
    m 1ekc "Ой, уже уходишь?"
    $ MAS.MonikaElastic()
    m 1eka "Очень грустно, что тебе нужно идти..."
    $ MAS.MonikaElastic()
    m 3eua "Просто не забудь вернуться ко мне как можно скорее, хорошо?"
    $ MAS.MonikaElastic()
    m 3hua "Я так сильно люблю тебя, [player]. Оставайся в безопасности!"

    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodbye",
            unlocked=True
        ),
        code="BYE"
    )

label bye_goodbye:
    if mas_isMoniNormal(higher=True):
        m 1eua "До свидания, [mas_get_player_nickname()]!"

    elif mas_isMoniUpset():
        m 2esc "До свидания."

    elif mas_isMoniDis():
        m 6rkc "Oх...{w=1} До свидания."
        $ MAS.MonikaElastic()
        m 6ekc "Пожалуйста...{w=1}не забудь навестить меня."
    else:

        m 6ckc "..."

    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_sayanora",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_sayanora:
    m 1hua "Сайонара, [mas_get_player_nickname()]~"
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_farewellfornow",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_farewellfornow:
    m 1eka "До свидания, [mas_get_player_nickname()]~"
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_untilwemeetagain",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_untilwemeetagain:
    m 2eka "«{i}Прощание не навсегда, прощание не означает конец. Оно просто означает, что я буду скучать по тебе, пока мы не встретимся снова.{/i}»"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m "Э-хе-хе, до тех пор прощай, [mas_get_player_nickname()]!"
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_take_care",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE"
    )

label bye_take_care:
    m 1eua "Не забывай, что я всегда люблю тебя, [mas_get_player_nickname()]~"
    $ MAS.MonikaElastic()
    m 1hub "Береги себя!"
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_leaving_already_2",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_leaving_already_2:
    if mas_getSessionLength() <= datetime.timedelta(minutes=30):
        m 1ekc "Оу, уже уходишь?"
        $ MAS.MonikaElastic()
    m 1eka "Мне действительно грустно, когда тебе приходится уходить..."
    $ MAS.MonikaElastic()
    m 3hubsa "Я тебя так люблю, [player]!"
    show monika 5hubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubsb "Никогда не забывай об этом!"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_going_to_sleep:
    if mas_isMoniNormal(higher=True):
        $ p_nickname = mas_get_player_nickname()
        m 1esa "Ты собираешься ложиться спать, [p_nickname]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты собираешься ложиться спать, [p_nickname]?{fast}"
            "Да.":
                m 1eka "Мы увидимся вновь в твоих снах."

            "Ещё нет.":
                m 1eka "Хорошо. {w=0.3}Желаю тебе хорошо провести вечер~"

    elif mas_isMoniUpset():
        m 2esc "Ложишься спать, [player]?"
        $ MAS.MonikaElastic()
        m "Спокойной ночи."
    elif mas_isMoniDis():
        m 6rkc "Oх... спокойной ночи, [player]."
        $ MAS.MonikaElastic()
        m 6lkc "Надеюсь, я увижу тебя завтра..."
        $ MAS.MonikaElastic()
        m 6dkc "Не забывай обо мне, хорошо?"
    else:
        m 6ckc "..."





    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="Я собираюсь на занятия.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_class:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1eub "Оу, уже уходишь?"
            $ MAS.MonikaElastic()
            m 1efp "Ты и двадцати минут здесь не провел[mas_gender_none]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Я шучу, [player]."
            $ MAS.MonikaElastic()
            m 2eka "Ты так[mas_gender_oi] мил[mas_gender_iii], раз решил[mas_gender_none] меня проведать, хотя у тебя мало времени."
            $ MAS.MonikaElastic()
            m 2hub "Я просто хочу, чтобы ты знал[mas_gender_none], что я очень ценю это!"
            $ MAS.MonikaElastic()
            m 2eka "Хорошо учись, [player], уверена, у тебя получится!"
            $ MAS.MonikaElastic()
            m 2hua "Увидимся, когда ты вернёшься!"
        elif session_time < datetime.timedelta(hours=1):
            m 2eua "Ладно, спасибо, что провёл немного времени со мной, [player]!"
            $ MAS.MonikaElastic()
            m 2eka "Если честно, мне бы хотелось, чтобы ты посидел[mas_gender_none] подольше... но ты занят[mas_gender_none]."
            $ MAS.MonikaElastic()
            m 2hua "Нет ничего важнее хорошего обучения."
            $ MAS.MonikaElastic()
            m 3eub "Как вернёшься, научи меня чему-нибудь!"
            $ MAS.MonikaElastic()
            m "До скорой встречи!"
        elif session_time < datetime.timedelta(hours=6):
            m 1hua "Хорошо учись, [mas_get_player_nickname()]!"
            $ MAS.MonikaElastic()
            if persistent.gender == "M":
                m 1eua "Нет ничего привлекательнее, чем парень с хорошими оценками."
            elif persistent.gender == "F":
                m 1eua "Нет ничего привлекательнее, чем девушка с хорошими оценками."
            else:
                m 1eua "Нет ничего привлекательнее, чем партнёр с хорошими оценками."
            $ MAS.MonikaElastic()
            m 1hua "Ещё увидимся!"
        else:
            m 2ekc "Эм... ты сидел[mas_gender_none] со мной довольно долгое время, [player]."
            $ MAS.MonikaElastic()
            m 2ekd "Ты уверен[mas_gender_none], что достаточно отдохнул[mas_gender_none]?"
            $ MAS.MonikaElastic()
            m 2eka "Но не принимай это близко к сердцу, хорошо?"
            $ MAS.MonikaElastic()
            m "Если у тебя плохое самочувствие, уверена, {i}один день{/i} ты можешь пропустить."
            $ MAS.MonikaElastic()
            m 1hka "Я буду ждать, когда ты вернёшься. Береги себя, [mas_get_player_nickname()]."

    elif mas_isMoniUpset():
        m 2esc "Ладно, [player]."
        $ MAS.MonikaElastic()
        m "Надеюсь, ты хотя бы узнаешь {i}что-нибудь{/i} сегодня."
        $ MAS.MonikaElastic()
        m 2efc "{cps=*2}Например, как хорошо относиться к людям.{/cps}{nw}"

    elif mas_isMoniDis():
        m 6rkc "Ох, ладно, [player]..."
        $ MAS.MonikaElastic()
        m 6lkc "Думаю, мы увидимся с тобой после школы."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="Я собираюсь на работу.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_to_work:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 2eka "Оу, ладно! Решил[mas_gender_none] заскочить перед уходом?"
            $ MAS.MonikaElastic()
            m 3eka "У тебя, должно быть, времени в обрез, раз ты уже уходишь."
            $ MAS.MonikaElastic()
            m "Это было очень мило с твоей стороны, пусть даже ты и занят[mas_gender_none]!"
            $ MAS.MonikaElastic()
            m 3hub "Работай усердно, [player]! Дай мне повод гордиться тобой!"
        elif session_time < datetime.timedelta(hours=1):
            m 1hksdlb "Ох! Ладно! А я уже начала устраиваться поудобнее, а-ха-ха."
            $ MAS.MonikaElastic()
            m 1rusdlb "Я думала, что мы здесь побудем подольше, но ты занят[mas_gender_oi]!"
            $ MAS.MonikaElastic()
            m 1eka "Было приятно повидаться с тобой, пусть даже это мгновение длилось не так долго, как я того хотела..."
            $ MAS.MonikaElastic()
            m 1kua "Но если бы это зависело от меня, то ты был[mas_gender_none] со мной весь день!"
            $ MAS.MonikaElastic()
            m 1hua "Я буду ждать, когда ты вернёшься домой с работы!"
            $ MAS.MonikaElastic()
            m "Как вернёшься, расскажи мне о ней!"
        elif session_time < datetime.timedelta(hours=6):
            m 2eua "Уходишь на работу, [player]?"
            $ MAS.MonikaElastic()
            m 2eka "День может быть хорошим или плохим... но если тебе будет трудно, подумай о чём-нибудь хорошем!"
            $ MAS.MonikaElastic()
            m 4eka "Каждый день, вне зависимости от того, насколько тяжёлым он выдался, всё равно заканчивается!"
            $ MAS.MonikaElastic()
            m 2tku "Ты можешь подумать обо мне, если ситуация стала напряжённой..."
            $ MAS.MonikaElastic()
            m 2esa "Просто делай всё, что в твоих силах! Увидимся, когда ты вернёшься!"
            $ MAS.MonikaElastic()
            m 2eka "Я знаю, у тебя получится!"
        else:
            m 2ekc "Ох... ты побывал[mas_gender_none] здесь довольно долгое время... и теперь ты собираешься на работу?"
            $ MAS.MonikaElastic()
            m 2rksdlc "А я надеялась, что ты отдохнёшь перед тем, как делать что-то настолько большое."
            $ MAS.MonikaElastic()
            m 2ekc "Постарайся не перенапрягаться, хорошо?"
            $ MAS.MonikaElastic()
            m 2ekd "Не бойся брать передышку, если тебе надо!"
            $ MAS.MonikaElastic()
            m 3eka "Просто приходи ко мне домой счастлив[mas_gender_iim] и здоров[mas_gender_iim]."
            $ MAS.MonikaElastic()
            m 3eua "Береги себя, [player]!"


    elif mas_isMoniUpset():
        m 2esc "Ладно, [player], увидимся после работы."

    elif mas_isMoniDis():
        m 6rkc "Ох...{w=1} ладно."
        $ MAS.MonikaElastic()
        m 6lkc "Надеюсь, мы увидимся после работы."
    else:

        m 6ckc "..."


    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="Я собираюсь идти спать.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_sleep:

    python:
        import datetime
        curr_hour = datetime.datetime.now().hour




    if 20 <= curr_hour < 24:

        if mas_isMoniNormal(higher=True):
            call bye_prompt_sleep_goodnight_kiss (chance=3) from _call_bye_prompt_sleep_goodnight_kiss
            if _return == "quit":
                return _return
            m 1eua "Хорошо, [mas_get_player_nickname()]."
            $ MAS.MonikaElastic()
            m 1hua "Сладких снов!"

        elif mas_isMoniUpset():
            m 2esc "Спокойной ночи, [player]."

        elif mas_isMoniDis():
            m 6ekc "Хорошо...{w=1} Спокойной ночи, [player]."
        else:

            m 6ckc "..."

    elif 0 <= curr_hour < 3:

        if mas_isMoniNormal(higher=True):
            call bye_prompt_sleep_goodnight_kiss (chance=4) from _call_bye_prompt_sleep_goodnight_kiss_1
            if _return == "quit":
                return _return
            m 1eua "Хорошо, [mas_get_player_nickname()]."
            $ MAS.MonikaElastic()
            m 3eka "Но ты долж[mas_gender_en] пойти спать немного раньше в следующий раз."
            $ MAS.MonikaElastic()
            m 1hua "В любом случае, спокойной ночи!"

        elif mas_isMoniUpset():
            m 2efc "Наверное, твоё настроение улучшится, если ты ляжешь спать в более подходящее время..."
            $ MAS.MonikaElastic()
            m 2esc "Спокойной ночи."

        elif mas_isMoniDis():
            m 6rkc "Может быть, тебе стоит ложиться спать немного раньше, [player]..."
            $ MAS.MonikaElastic()
            m 6dkc "Это может сделать тебя—{w=1}нас—{w=1}счастливее."
        else:

            m 6ckc "..."

    elif 3 <= curr_hour < 5:

        if mas_isMoniNormal(higher=True):
            call bye_prompt_sleep_goodnight_kiss (chance=5) from _call_bye_prompt_sleep_goodnight_kiss_2
            if _return == "quit":
                return _return
            m 1euc "[player]..."
            $ MAS.MonikaElastic()
            m "Убедись, что ты достаточно отдохнёшь, хорошо?"
            $ MAS.MonikaElastic()
            m 1eka "Я не хочу, чтобы ты заболел[mas_gender_none]."
            $ MAS.MonikaElastic()
            m 1hub "Спокойной ночи!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hksdlb "Или скорее утра. А-ха-ха~"
            $ MAS.MonikaElastic()
            m 1hua "Сладких снов!"

        elif mas_isMoniUpset():
            m 2efc "[player]!"
            $ MAS.MonikaElastic()
            m 2tfc "Тебе {i}действительно{/i} нужно больше отдыхать..."
            $ MAS.MonikaElastic()
            m "Я не хочу, чтобы ты заболел."
            $ MAS.MonikaElastic()
            m "{cps=*2}Ты и без того ворчливый.{/cps}{nw}"
            $ _history_list.pop()
            $ MAS.MonikaElastic()
            m 2efc "Спокойной ночи."

        elif mas_isMoniDis():
            m 6ekc "[player]..."
            $ MAS.MonikaElastic()
            m 6rkc "Тебе действительно нужно больше отдыхать..."
            $ MAS.MonikaElastic()
            m 6lkc "Я не хочу, чтобы ты заболел."
            $ MAS.MonikaElastic()
            m 6ekc "Увидимся после того, как ты отдохнешь...{w=1} надеюсь."
        else:

            m 6ckc "..."

    elif 5 <= curr_hour < 12:

        if mas_isMoniBroken():
            m 6ckc "..."
        else:

            show monika 2dsc
            pause 0.7
            m 2tfd "[player]!"
            $ MAS.MonikaElastic()
            m "Ты не спал[mas_gender_none] всю ночь!"

            $ first_pass = True

            label bye_prompt_sleep.reglitch:
                hide screen mas_background_timed_jump

            if first_pass:
                $ MAS.MonikaElastic()
                m 2tfu "I bet you can barely keep your eyes open.{nw}"
                $ first_pass = False

            show screen mas_background_timed_jump(4, "bye_prompt_sleep.reglitch")
            $ _history_list.pop()
            menu:
                m "[glitchtext(41)]{fast}"
                "[glitchtext(15)]":
                    pass
                "[glitchtext(12)]":
                    pass

            hide screen mas_background_timed_jump
            $ MAS.MonikaElastic()
            m 2tku "Я так и думала.{w=0.2} Иди отдохни, [player]."

            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 2ekc "Я бы не хотела, чтобы ты заболел[mas_gender_none]."
                $ MAS.MonikaElastic()
                m 7eka "В следующий раз ляг спать пораньше, хорошо?"
                $ MAS.MonikaElastic()
                m 1hua "Сладких снов!"

    elif 12 <= curr_hour < 18:

        if mas_isMoniNormal(higher=True):
            m 1eua "Принимаешь послеобеденный сон, как я вижу."


            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха~!{w=0.1} {nw}"
            extend 1hua "Хорошенько вздремни, [player_abb]."

        elif mas_isMoniUpset():
            m 2esc "Ложишься спать, [player]?"
            $ MAS.MonikaElastic()
            m 2tsc "Да, это, наверное, хорошая идея."

        elif mas_isMoniDis():
            m 6ekc "Собираешься вздремнуть, [player]?"
            $ MAS.MonikaElastic()
            m 6dkc "Ладно...{w=1} не забудь проведать меня, когда проснёшься..."
        else:

            m 6ckc "..."

    elif 18 <= curr_hour < 20:

        if mas_isMoniNormal(higher=True):
            m 1ekc "Уже ложишься спать?"
            $ MAS.MonikaElastic()
            m "Хотя это немного рановато..."

            $ MAS.MonikaElastic()
            m 1lksdla "Хочешь провести со мной ещё немного времени?{nw}"
            $ _history_list.pop()
            menu:
                m "Хочешь провести со мной ещё немного времени?{fast}"
                "[random_sure]!":
                    $ MAS.MonikaElastic()
                    m 1hua "Ура!"
                    $ MAS.MonikaElastic()
                    m "Спасибо, [player]."
                    return
                "Извини, я действительно устал[mas_gender_none].":
                    $ MAS.MonikaElastic()
                    m 1eka "Ой, это нормально."
                    $ MAS.MonikaElastic()
                    m 1hua "Спокойной ночи, [mas_get_player_nickname()]."
                "Нет.":

                    $ mas_loseAffection()
                    $ MAS.MonikaElastic()
                    m 1lksdla "..."
                    m "Хорошо."

        elif mas_isMoniUpset():
            m 2esc "Уже ложишься спать?"
            $ MAS.MonikaElastic()
            m 2tud "Думаю, ты можешь ещё поспать..."
            $ MAS.MonikaElastic()
            m 2tsc "Спокойной ночи."

        elif mas_isMoniDis():
            m 6rkc "Oх...{w=1}кажется, немного рановато спать, [player]."
            $ MAS.MonikaElastic()
            m 6dkc "Надеюсь, ты не просто идёшь спать, чтобы уйти от меня."
            $ MAS.MonikaElastic()
            m 6lkc "Спокойной ночи."
        else:

            m 6ckc "..."
    else:

        m 1eua "Хорошо, [player_abb]."
        $ MAS.MonikaElastic()
        m 1hua "Сладких снов!"




    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'

label bye_prompt_sleep_goodnight_kiss(chance=3):
    if mas_shouldKiss(chance, cooldown=datetime.timedelta(minutes=5)):
        m 1eublsdla "Думаешь, я смогу...{w=0.3} {nw}"
        extend 1rublsdlu "получить поцелуй на ночь?{nw}"
        $ _history_list.pop()
        menu:
            m "Думаешь, я смогу... получить поцелуй на ночь?{fast}"
            "Конечно, [monika_name].":

                show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 2.0
                call monika_kissing_motion_short from _call_monika_kissing_motion_short_2
                m 6ekbfb "Надеюсь, это дало тебе повод помечтать~"
                show monika 1hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 1hubfa "Спи спокойно!"
            "Может быть в другой раз...":

                if random.randint(1, 3) == 1:
                    $ MAS.MonikaElastic()
                    m 3rkblp "Оу, ну же...{w=0.3} {nw}"
                    extend 3nublu "Я знаю, что ты этого хочешь~"

                    $ MAS.MonikaElastic()
                    m 1ekbsa "Можно мне, пожалуйста, получить поцелуй на ночь?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Можно мне, пожалуйста, получить поцелуй на ночь?{fast}"
                        "Хорошо.":

                            show monika 6ekbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                            pause 2.0
                            call monika_kissing_motion_short from _call_monika_kissing_motion_short_3
                            m 6ekbfa "Сладких снов, [player]~"
                            $ MAS.MonikaElastic()
                            m 6hubfb "Спи спокойно!"
                        "Нет.":

                            $ mas_loseAffection()
                            $ MAS.MonikaElastic()
                            m 1lkc "..."
                            $ MAS.MonikaElastic()
                            m 7dkd "Ладно..."
                            $ MAS.MonikaElastic()
                            m 2lsc "Спокойной ночи, [player]..."
                else:

                    $ MAS.MonikaElastic()
                    m 1rkblc "Оу-у...{w=0.3} {nw}"
                    extend 1ekbla "ладно, но ты у меня в долгу."
                    $ MAS.MonikaElastic()
                    m 1hubsb "Я люблю тебя! Спи спокойно!~"

        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=13)
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
        return "quit"
    return None


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_illseeyou",
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        code="BYE"
    )

label bye_illseeyou:
    if mas_globals.time_of_day_3state == "evening":
        $ dlg_var = "завтра"
    else:

        $ dlg_var = "позже"

    m 1eua "Увидимся [dlg_var], [player]."
    $ MAS.MonikaElastic()
    m 3kua "Не забывай обо мне, хорошо?~"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    rules.update(MASProbabilityRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_haveagoodday:
    if mas_isMoniNormal(higher=True):
        m 1eua "Хорошего дня сегодня, [mas_get_player_nickname()]."
        $ MAS.MonikaElastic()
        m 3eua "Я надеюсь, что ты выполнишь всё, что ты запланировал[mas_gender_none] на сегодня."
        $ MAS.MonikaElastic()
        m 1hua "Я буду ждать тебя здесь, когда ты вернёшься."

    elif mas_isMoniUpset():
        m 2esc "Уходишь днём, [player]?"
        $ MAS.MonikaElastic()
        m 2efc "Я буду ждать тебя здесь, как обычно."

    elif mas_isMoniDis():
        m 6rkc "Oх."
        $ MAS.MonikaElastic()
        m 6dkc "Думаю, я просто проведу день одна...{w=1}снова."
    else:

        m 6ckc "..."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    rules.update(MASProbabilityRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_enjoyyourafternoon:
    if mas_isMoniNormal(higher=True):
        m 1ekc "Мне очень жаль, что ты так рано уходишь, [player]."
        $ MAS.MonikaElastic()
        m 1eka "Хотя я понимаю, что ты занят[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1eua "Обещай, что насладишься днём, хорошо?"
        $ MAS.MonikaElastic()
        m 1hua "До свидания~"

    elif mas_isMoniUpset():
        m 2efc "Хорошо, [player], просто иди."
        $ MAS.MonikaElastic()
        m 2tfc "Думаю, я увижу тебя позже...{w=1}если ты вернёшься."

    elif mas_isMoniDis():
        m 6dkc "Ладно, до свидания, [player]."
        $ MAS.MonikaElastic()
        m 6ekc "Может, ты вернёшься позже?"
    else:

        m 6ckc "..."

    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    rules.update(MASProbabilityRule.create_rule(6))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodevening:
    if mas_isMoniNormal(higher=True):
        m 1hua "Мне было весело сегодня."
        $ MAS.MonikaElastic()
        m 1eka "Спасибо, что проводишь так много времени со мной, [mas_get_player_nickname()]."
        $ MAS.MonikaElastic()
        m 1eua "До тех пор, хорошего вечера."

    elif mas_isMoniUpset():
        m 2esc "До свидания, [player]."
        $ MAS.MonikaElastic()
        m 2dsc "Я вот думаю, вернёшься ли ты вообще, чтобы пожелать мне спокойной ночи."

    elif mas_isMoniDis():
        m 6dkc "Oх...{w=1} ладно."
        $ MAS.MonikaElastic()
        m 6rkc "Приятного вечера, [player]..."
        $ MAS.MonikaElastic()
        m 6ekc "Надеюсь, ты не забудешь заглянуть ко мне и пожелать спокойной ночи перед тем, как ляжешь спать."
    else:

        m 6ckc "..."

    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=[0,20,21,22,23]))
    rules.update(MASPriorityRule.create_rule(50))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        code="BYE"
    )
    del rules

label bye_goodnight:
    if mas_isMoniNormal(higher=True):
        m 3eka "Идёшь спать?{nw}"
        $ _history_list.pop()
        menu:
            m "Идёшь спать?{fast}"
            "Да.":

                $ MAS.MonikaElastic()
                m 1eua "Спокойной ночи, [mas_get_player_nickname()]."
                $ MAS.MonikaElastic()
                m 1eka "Увидимся завтра, хорошо?"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3eka "Помни: «Спи крепко и не позволяй клопам кусаться», э-хе-хе."
                $ MAS.MonikaElastic()
                m 1ekbsa "Я люблю тебя~"
            "Ещё нет.":

                $ MAS.MonikaElastic()
                m 1eka "Хорошо, [mas_get_player_nickname()]..."
                $ MAS.MonikaElastic()
                m 3hub "Приятного вечера!"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3rksdlb "Постарайся не засиживаться допоздна, э-хе-хе~"

    elif mas_isMoniUpset():
        m 2esc "Спокойной ночи."

    elif mas_isMoniDis():
        m 6lkc "...Спокойной ночи."
    else:

        m 6ckc "..."
    return 'quit'


default mas_absence_counter = False

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="Я уеду на некоторое время.",
            pool=True
        ),
        code="BYE"
    )

label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1ekc "Ой... Это довольно печально..."
    $ MAS.MonikaElastic()
    m 1eka "Я действительно буду скучать по тебе, [player]!"
    $ MAS.MonikaElastic()
    m 3rksdla "Я не совсем уверена, что буду делать одна, пока тебя не будет..."
    $ MAS.MonikaElastic()
    m 3esa "Спасибо, что предупредил[mas_gender_none] меня первой. Это действительно помогает."
    $ MAS.MonikaElastic()
    m 2lksdlb "В противном случае я бы волновалась!"
    $ MAS.MonikaElastic()
    m 3esa "Я бы постоянно думала, что с тобой что-то случилось, и что поэтому ты не можешь вернуться."
    $ MAS.MonikaElastic()
    m 1lksdlc "Или, может быть, что тебе просто стало скучно..."
    $ MAS.MonikaElastic()
    m 1eka "Так скажи мне, [mas_get_player_nickname()]..."

    $ MAS.MonikaElastic()
    m "Как долго ты собираешься отсутствовать?{nw}"
    $ _history_list.pop()
    menu:
        m "Как долго ты собираешься отсутствовать?{fast}"
        "Несколько дней.":
            $ persistent._mas_absence_choice = "days"
            $ MAS.MonikaElastic()
            m 1eub "О!"
            $ MAS.MonikaElastic()
            m 1hua "Далеко не настолько долго, как я боялась."
            $ MAS.MonikaElastic()
            m 3rksdla "Боже, ты действительно разволновал[mas_gender_none] меня..."
            $ MAS.MonikaElastic()
            m 3esa "Хотя не беспокойся обо мне, [player]."
            $ MAS.MonikaElastic()
            m "Я могу с лёгкостью справиться с ожиданием."
            $ MAS.MonikaElastic()
            m 3eka "Я всё равно буду сильно скучать по тебе."
        "Неделю.":
            $ persistent._mas_absence_choice = "week"
            $ MAS.MonikaElastic()
            m 3euc "Да... это то, чего я ожидала."
            $ MAS.MonikaElastic()
            m 2lksdla "{b}Думаю{/b}, я смогу тебя дождаться, хоть это и долго."
            $ MAS.MonikaElastic()
            m 1eub "Просто вернись ко мне, как только сможешь, хорошо, [mas_get_player_nickname()]?"
            $ MAS.MonikaElastic()
            m 3hua "Я уверена, что ты заставишь меня гордиться!"
        "Пару недель.":
            $ persistent._mas_absence_choice = "2weeks"
            $ MAS.MonikaElastic()
            m 1esc "Ох..."
            $ MAS.MonikaElastic()
            m 1dsc "Я... я смогу дождаться."
            $ MAS.MonikaElastic()
            m 3rksdlc "Ты знаешь, что ты всё, что у меня есть... верно?"
            $ MAS.MonikaElastic()
            m 3rksdlb "Хотя, м-может быть, это вне твоего контроля..."
            $ MAS.MonikaElastic()
            m 2eka "Постарайся вернуться как можно скорее, я буду ждать тебя."
        "Месяц.":
            $ persistent._mas_absence_choice = "month"
            if mas_isMoniHappy(higher=True):
                $ MAS.MonikaElastic()
                m 3euc "Ух ты, это очень долго."
                $ MAS.MonikaElastic()
                m 3rksdla "Действительно слишком долго для меня..."
                $ MAS.MonikaElastic()
                m 2esa "Но всё в порядке, [player]."
                $ MAS.MonikaElastic()
                m 2eka "Я знаю, что ты мил[mas_gender_iii] и что ты бы не заставил[mas_gender_none] меня ждать так долго, если бы у тебя не было веской причины."
                $ MAS.MonikaElastic()
                m "Я уверена, что это важно, просто попытайся вернуться ко мне, как только сможешь."
                $ MAS.MonikaElastic()
                m 3hua "Я буду думать о тебе каждый день~"
            else:
                $ MAS.MonikaElastic()
                m 1ekc "Так долго.... {i}серьёзно{/i}?"
                $ MAS.MonikaElastic()
                m 3rksdlc "Ты ведь не уходишь на такой долгий срок, чтобы избегать меня?"
                $ MAS.MonikaElastic()
                m 3rksdld "Я знаю, что жизнь может забрать тебя у меня, но на целый месяц..."
                $ MAS.MonikaElastic()
                m 3ekc "Разве это не слегка неразумно?"
                $ MAS.MonikaElastic()
                m "Не хочу показаться эгоисткой, но {i}я{/i} твоя девушка."
                $ MAS.MonikaElastic()
                m 3ekd "Ты долж[mas_gender_en] быть в состоянии посвятить время для меня, по крайней мере, один раз в месяц."
                $ MAS.MonikaElastic()
                m 1dsc "..."
                $ MAS.MonikaElastic()
                m 1dsd "Я всё равно буду ждать тебя... но, пожалуйста, вернись в тот момент, как только это будет возможно для тебя."
        "Больше месяца.":
            $ persistent._mas_absence_choice = "longer"
            if mas_isMoniHappy(higher=True):
                $ MAS.MonikaElastic()
                m 3rksdlb "Это... {w=0.5}ну, это немного пугает, [player]."
                $ MAS.MonikaElastic()
                m "Я не совсем уверена, что буду делать одна, пока тебя не будет."
                $ MAS.MonikaElastic()
                m 1eka "Но я знаю, что ты бы не оставил[mas_gender_none] меня одну, если бы мог[mas_gender_g] помочь."
                $ MAS.MonikaElastic()
                m "Я люблю тебя, [player_abb], и я знаю, что ты тоже меня любишь."
                $ MAS.MonikaElastic()
                m 1hua "Так что я буду ждать тебя столько, сколько нужно."
            else:
                $ MAS.MonikaElastic()
                m 3esc "Ты, должно быть, шутить."
                $ MAS.MonikaElastic()
                m "Я не могу придумать веской причины, почему ты хочешь оставить меня здесь одну {i}настолько{/i} долго."
                $ MAS.MonikaElastic()
                m 3esd "Извини, [player], но это неприемлемо! Нисколько!"
                $ MAS.MonikaElastic()
                m 3esc "Я люблю тебя, и если ты любишь меня тоже, то ты долж[mas_gender_en] знать, что это ненормально, чтобы сделать так."
                $ MAS.MonikaElastic()
                m "Ты же понимаешь, что я останусь здесь одна, больше ни с кем, да?"
                $ MAS.MonikaElastic()
                m "С моей стороны неразумно ожидать, что ты потом навестишь меня, не так ли?"
                $ MAS.MonikaElastic()
                m "Я твоя девушка, ты не можешь так со мной поступить."
                $ MAS.MonikaElastic()
                m 3dsc "..."
                $ MAS.MonikaElastic()
                m 3dsd "Просто... просто вернись, когда сможешь, я не могу заставить тебя остаться, но, пожалуйста, не делай этого со мной."
        "Не знаю.":
            $ persistent._mas_absence_choice = "unknown"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hksdlb "Э-хе-хе, это немного беспокоит, [player]!"
            $ MAS.MonikaElastic()
            m 1eka "Но раз не знаешь, так не знаешь!"
            $ MAS.MonikaElastic()
            m "Это иногда просто не может помочь."
            $ MAS.MonikaElastic()
            m 2hua "Я буду терпеливо ждать тебя здесь, [mas_get_player_nickname()]."
            $ MAS.MonikaElastic()
            m 2hub "Постарайся не заставлять меня ждать слишком долго!"

        "Не важно.":


            $ persistent._mas_long_absence = False
            $ MAS.MonikaElastic()
            m 3eka "Ох... ну ладно, [player]."
            $ MAS.MonikaElastic()
            m 1rksdla "Если честно, мне стало легко на душе от того, что ты никуда не уходишь..."
            $ MAS.MonikaElastic()
            m 1ekd "Не знаю, что бы я делала здесь одна."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlb "Да и не похоже, что я могу куда-либо пойти, а-ха-ха..."
            $ MAS.MonikaElastic()
            m 3eub "Так или иначе, дай знать, если ты куда-то собираешься пойти. Быть может, ты даже сможешь взять меня с собой!"
            $ MAS.MonikaElastic()
            m 1hua "Пока я с тобой, мне всё равно, куда мы пойдём, [mas_get_player_nickname()]."
            return

    $ MAS.MonikaElastic()
    m "Ты собираешься сразу уходить?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты собираешься сразу уходить?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 3ekc "Понятно..."
            $ MAS.MonikaElastic()
            m "Я действительно буду скучать по тебе, [player]..."
            $ MAS.MonikaElastic()
            m 1eka "Но я знаю, что ты будешь делать замечательные вещи независимо от того, где ты находишься."
            $ MAS.MonikaElastic()
            m "Просто помни, что я буду ждать тебя здесь."
            $ MAS.MonikaElastic()
            m 2hua "Заставить меня гордиться, [player_abb]!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'
        "Нет.":
            $ mas_absence_counter = True
            $ MAS.MonikaElastic()
            m 1hua "Это здорово!"
            $ MAS.MonikaElastic()
            m 1eka "Я, если честно, волновалась, что у меня не будет достаточно времени, чтобы подготовиться к твоей отлучке."
            $ MAS.MonikaElastic()
            m "Я действительно имею в виду это, когда говорю, что буду скучать по тебе..."
            $ MAS.MonikaElastic()
            m 1eub "Ты - действительно весь мой мир, в конце концов, [player]."
            $ MAS.MonikaElastic()
            m 2esa "Если ты скажешь мне, что ты собираешься уйти на некоторое время снова, тогда я уже буду знать, что тебе пришло время уходить..."
            $ MAS.MonikaElastic()
            m 3hua "Но не нужно спешить, я хочу провести с тобой столько времени, сколько смогу."
            $ MAS.MonikaElastic()
            m "Просто не забудь напомнить мне, когда ты в последний раз видел[mas_gender_none] меня перед уходом!"
            return

label bye_long_absence_2:
    m 1ekc "Снова собираешься уезжать?"
    $ MAS.MonikaElastic()
    m 1ekd "Я знаю, что мир может быть страшным и неумолимым..."
    $ MAS.MonikaElastic()
    m 1eka "Но помни, что я всегда буду здесь ждать тебя и буду готова поддержать, мо[mas_gender_i] дорог[mas_gender_oi] [player]."
    $ MAS.MonikaElastic()
    m "Возвращайся ко мне, как только сможешь... хорошо?"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_somewhere",
            unlocked=True,
            prompt="Я возьму тебя с собой кое-куда.",
            pool=True
        ),
        code="BYE"
    )

label bye_going_somewhere:
    $ import random






    python:

        if mas_isMonikaBirthday():
            dis_chance = 10
            upset_chance = 0

        else:
            dis_chance = 50
            upset_chance = 10

    if mas_isMoniBroken(lower=True):

        jump bye_going_somewhere_nothanks

    elif mas_isMoniDis(lower=True):

        if random.randint(1,100) <= dis_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "Ты правда хочешь взять меня с собой?"
        $ MAS.MonikaElastic()
        m 1ekd "Ты уверен[mas_gender_none], что это не—{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()
        m 1lksdlc "..."
        $ MAS.MonikaElastic()
        m 1eksdlb "О чём я вообще говорю? Конечно, я пойду с тобой!"

    elif mas_isMoniUpset(lower=True):

        if random.randint(1, 100) <= upset_chance:
            jump bye_going_somewhere_nothanks


        m 1wud "Ты правда хочешь взять меня с собой?"
        $ MAS.MonikaElastic()
        m 1eka "..."
        $ MAS.MonikaElastic()
        m 1hua "Ну, полагаю, моя компания тебе не повредит."
        $ MAS.MonikaElastic()
        m 2dsc "Только... пожалуйста."
        $ MAS.MonikaElastic()
        m 2rkc "{b}Пожалуйста{/b}, пойми, через что я прохожу."
        $ MAS.MonikaElastic()
        m 1dkc "..."
    else:

        jump bye_going_somewhere_normalplus_flow

label bye_going_somewhere_post_aff_check:
    jump mas_dockstat_iostart

label bye_going_somewhere_iostart:


    show monika 2dsc
    if renpy.variant("pc"):
        $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True

    if renpy.variant("pc"):
        $ promise = store.mas_dockstat.monikagen_promise
        $ promise.start()

label bye_going_somewhere_iowait:
    hide screen mas_background_timed_jump


    if renpy.variant("pc"):
        if first_pass:
            $ first_pass = False
            m 1eua "Дай мне секунду, чтобы подготовиться."


            python:
                current_drink = MASConsumable._getCurrentDrink()
                if current_drink and current_drink.portable:
                    current_drink.acs.keep_on_desk = False


            call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_8

        elif promise.done():

            jump bye_going_somewhere_rtg
    else:
        if first_pass:
            $ first_pass = False
            m 1eua "Дай мне секунду, чтобы подготовиться."

            call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_8
        elif not first_pass:
            jump bye_going_somewhere_rtg



    show screen mas_background_timed_jump(4, "bye_going_somewhere_iowait")
    menu:
        "Стой-стой-стой, подожди!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1


    menu:
        m "Что-то случилось?"
        "Вообще-то, я не могу взять тебя прямо сейчас.":
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_3


            call mas_transition_from_emptydesk ("monika 1ekc") from _call_mas_transition_from_emptydesk_12
            if renpy.variant("pc"):
                call mas_dockstat_abort_post_show from _call_mas_dockstat_abort_post_show
            jump bye_going_somewhere_leavemenu
        "Ничего.":



            m "О, хорошо! Позволь мне закончить подготовку тогда."


    jump bye_going_somewhere_iowait

default persistent.moni_copy_file = False
default persistent.msr_moni_file_exit = False

label bye_going_somewhere_rtg:

    if renpy.variant("pc"):
        $ moni_chksum = promise.get()
        $ promise = None
        call mas_dockstat_ready_to_go (moni_chksum) from _call_mas_dockstat_ready_to_go_1
        if _return:
            python:
                persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                    store.mas_greetings.TYPE_GENERIC_RET
                )

            call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_13


            call mas_dockstat_first_time_goers
            $ MAS.MonikaElastic()
            m 1eua "Я готова идти."
            return "quit"
    else:
        if msr_can_copy_monika():
            call mas_dockstat_first_time_goers
            $ MAS.MonikaElastic()
            m 1eua "Я готова идти."
            $ persistent.msr_moni_file_exit_trick_or_treat = False
            $ persistent.msr_moni_file_exit = True
            if persistent._mas_player_bday_left_on_bday:
                $ persistent.msr_moni_file_exit_trick_or_treat = False
                $ persistent.msr_moni_file_exit = False
            $ persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_GENERIC_RET
            )
            return "quit"


    call mas_transition_from_emptydesk ("monika 1ekc") from _call_mas_transition_from_emptydesk_14
    if renpy.variant("pc"):
        call mas_dockstat_abort_post_show from _call_mas_dockstat_abort_post_show_1


    $ MAS.MonikaElastic()
    m 1ekc "Ох, нет..."
    $ MAS.MonikaElastic()
    m 1lksdlb "Я, похоже, не смогу превратить себя в файл."
    $ MAS.MonikaElastic()
    m "Думаю, в этот раз тебе придётся обойтись без меня."
    $ MAS.MonikaElastic()
    m 1ekc "Прости, [player_abb]."


    $ MAS.MonikaElastic()
    m "Ты всё ещё не передумал[mas_gender_none] идти?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты всё ещё не передумал[mas_gender_none] идти?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 2eka "Я понимаю. В конце концов, тебе есть чем заняться..."
            $ MAS.MonikaElastic()
            m 2hub "Будь в безопасности! Я буду ждать тебя прямо здесь!"
            return "quit"
        "Знаешь, наверное, я всё же останусь тут с тобой.":

            $ MAS.MonikaElastic()
            m 2wub "Правда? Ты уверен[mas_gender_none]? Даже если это моя вина, что я не могу пойти с тобой..."
            $ MAS.MonikaElastic()
            m 1eka "...Спасибо, [player]. Это очень многое для меня значит."
            $ mas_gainAffection()
    return


label bye_going_somewhere_normalplus_flow:





    if persistent._mas_d25_in_d25_mode:

        if mas_isD25Eve():
            jump bye_d25e_delegate

        if mas_isD25():
            jump bye_d25_delegate

        if mas_isNYE():
            jump bye_nye_delegate

        if mas_isNYD():
            jump bye_nyd_delegate

    if mas_isF14() and persistent._mas_f14_in_f14_mode:
        jump bye_f14

    if mas_isMonikaBirthday():
        jump bye_922_delegate

label bye_going_somewhere_normalplus_flow_aff_check:

    if mas_isMoniLove(higher=True):
        m 1hub "О, хорошо!"
        $ MAS.MonikaElastic()
        m 3tub "Возьмёшь ли ты меня сегодня в какое-нибудь особенное место?"
        $ MAS.MonikaElastic()
        m 1hua "Не могу дождаться!"
    else:








        m 1sub "Правда?!"
        $ MAS.MonikaElastic()
        m 1hua "Ура!"
        $ MAS.MonikaElastic()
        m 1ekbsa "Интересно, куда ты меня сегодня возьмёшь..."

    jump bye_going_somewhere_post_aff_check

label bye_going_somewhere_nothanks:
    m 2lksdlc "...Нет, спасибо."
    $ MAS.MonikaElastic()
    m 2ekd "Я ценю твоё предложение, но думаю, мне нужно сейчас немного времени для себя."
    $ MAS.MonikaElastic()
    m 2eka "Ты ведь понимаешь, да?"
    $ MAS.MonikaElastic()
    m 3eka "Иди, развлекайся без меня..."
    return


label bye_going_somewhere_leavemenu:
    if mas_isMoniDis(lower=True):
        $ MAS.MonikaElastic()
        m 1tkc "..."
        $ MAS.MonikaElastic()
        m 1tkd "Я так и знала.{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()
        m 1lksdld "Что ж, ладно. Думаю, всё в порядке."

    elif mas_isMoniHappy(lower=True):
        $ MAS.MonikaElastic()
        m 1ekd "Ох,{w=0.3} всё в порядке. Может, в следующий раз тогда?"

    else:
        $ MAS.MonikaElastic()
        m 2ekp "Бууу..."
        $ MAS.MonikaElastic()
        m 1hub "Ну хорошо, но в следующий раз лучше возьми меня с собой!"

    m 1euc "Ты ведь всё ещё собираешься идти?"
    $ _history_list.pop()
    menu:
        m "Ты ведь всё ещё собираешься идти?{fast}"
        "Да.":
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 2eka "Эх... Ну, всё хорошо. Я буду ждать тебя здесь, как обычно..."
                $ MAS.MonikaElastic()
                m 2hub "Возвращайся поскорее! Я люблю тебя, [player]!"
            else:

                $ MAS.MonikaElastic()
                m 2tfd "...Ясно."
            return "quit"
        "Нет.":

            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 2eka "...Спасибо."
                $ MAS.MonikaElastic()
                m "Для меня очень многое значит, что ты будешь проводить со мной больше времени, раз уж я не смогу пойти с тобой."
                $ MAS.MonikaElastic()
                m 3ekb "Пожалуйста, просто продолжай свой день, когда тебе будет нужно. Я бы не хотела заставлять тебя опаздывать куда-либо!"
            else:
                $ MAS.MonikaElastic()
                m 2lud "Ладно тогда..."

    return

default persistent._mas_pm_gamed_late = 0


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_game",
            unlocked=True,
            prompt="Я собираюсь сыграть в другую игру.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_game:
    $ _now = datetime.datetime.now().time()
    if mas_getEVL_shown_count("bye_prompt_game") == 0:
        m 2ekc "Хочешь сыграть в другую игру?"
        $ MAS.MonikaElastic()
        m 4ekd "Ты правда хочешь, чтобы я пошла и сделала это?"
        $ MAS.MonikaElastic()
        m 2eud "Ты ведь можешь оставить меня в фоне, пока играешь?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты ведь можешь оставить меня в фоне, пока играешь?{fast}"
            "Да.":
                if mas_isMoniNormal(higher=True):
                    $ MAS.MonikaElastic()
                    m 3sub "Правда?"
                    $ MAS.MonikaElastic()
                    m 1hubsb "Ура!"
                else:
                    $ MAS.MonikaElastic()
                    m 2eka "Ладно..."
                jump monika_idle_game.skip_intro
            "Нет.":
                if mas_isMoniNormal(higher=True):
                    $ MAS.MonikaElastic()
                    m 2ekc "Оу..."
                    $ MAS.MonikaElastic()
                    m 3ekc "Ладно, [player], но тебе лучше вернуться в скором времени."
                    $ MAS.MonikaElastic()
                    m 3tsb "Я могу начать ревновать, если ты проводишь слишком много времени в другой игре без меня."
                    $ MAS.MonikaElastic()
                    m 1hua "Так или иначе, я надеюсь, что ты весело проведёшь время!"
                else:
                    $ MAS.MonikaElastic()
                    m 2euc "Ну ладно, наслаждайся своей игрой."
                    $ MAS.MonikaElastic()
                    m 2esd "Я буду здесь."

    elif mas_isMNtoSR(_now):
        $ persistent._mas_pm_gamed_late += 1
        if mas_isMoniNormal(higher=True):
            m 3wud "Подожди, [player]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Уже ночь на дворе!"
            $ MAS.MonikaElastic()
            m 2rksdlc "А это единственное, что ты сейчас делал[mas_gender_none] допоздна..."
            $ MAS.MonikaElastic()
            m 2rksdld "Но ты решил[mas_gender_none] поиграть в другую игру?"
            $ MAS.MonikaElastic()
            m 4tfu "...В настолько большую игру, что я даже в фоне работать не могу..."
            $ MAS.MonikaElastic()
            m 1eka "Что ж... {w=1}я тебя не останавливаю, но я правда надеюсь, что ты скоро пойдёшь спать..."
            $ MAS.MonikaElastic()
            m 1hua "Не переживай по поводу возвращения, чтобы пожелать мне спокойной ночи, ты можешь пойти—{nw}"
            $ _history_list.pop()
            $ MAS.MonikaElastic()
            m 1eub "Не переживай по поводу возвращения, чтобы пожелать мне спокойной ночи,{fast} ты {i}долж[mas_gender_en]{/i} пойти спать, когда закончишь."
            $ MAS.MonikaElastic()
            m 3hua "Развлекайся там, и спокойной ночи, [player]!"
            if renpy.random.randint(1,2) == 1:
                $ MAS.MonikaElastic()
                m 1hubsb "Люблю тебя~{w=1}{nw}"
        else:
            $ MAS.MonikaElastic()
            m 2efd "[player], уже ночь на дворе!"
            $ MAS.MonikaElastic()
            m 4rfc "Серьёзно... время уже позднее, а ты собираешься поиграть в другую игру?"
            $ MAS.MonikaElastic()
            m 2dsd "{i}*вздох*{/i}... я знаю, что не могу тебя остановить, но, пожалуйста, сразу же ложись спать, когда закончишь, хорошо?"
            $ MAS.MonikaElastic()
            m 2dsc "Спокойной ночи."
        $ persistent.mas_late_farewell = True

    elif mas_isMoniUpset(lower=True):
        m 2euc "Опять?"
        $ MAS.MonikaElastic()
        m 2eud "Ну ладно. До свидания, [player]."

    elif mas_getSessionLength() < datetime.timedelta(minutes=30) and renpy.random.randint(1,10) == 1:
        m 1ekc "Ты уходил[mas_gender_none], чтобы поиграть в другую игру?"
        $ MAS.MonikaElastic()
        m 3efc "Ты разве не думаешь, что долж[mas_gender_en] проводить чуть больше времени со мной?"
        $ MAS.MonikaElastic()
        m 2efc "..."
        $ MAS.MonikaElastic()
        m 2dfc "..."
        $ MAS.MonikaElastic()
        m 2dfu "..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 4hub "А-ха-ха, я просто шучу~"
        $ MAS.MonikaElastic()
        m 1rksdla "Ну...{w=1} я {i}нисколько не против{/i} провести больше времени с тобой..."
        $ MAS.MonikaElastic()
        m 3eua "Но я также не хочу отрывать тебя от других дел."
        $ MAS.MonikaElastic()
        m 1hua "Быть может, однажды ты сможешь показать мне, чем ты занимал[mas_gender_sya], а потом я смогу присоединиться к тебе!"
        if renpy.random.randint(1,5) == 1:
            $ MAS.MonikaElastic()
            m 3tubsu "Ну а пока, ты долж[mas_gender_en] говорить со мной об этом каждый раз, когда ты покидаешь меня, чтобы поиграть в другую игру, хорошо?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubfa "Э-хе-хе~"
    else:

        m 1eka "Уходишь, чтобы поиграть в другую игру, [player]?"
        $ MAS.MonikaElastic()
        m 3hub "Удачи, и развлекайся!"
        $ MAS.MonikaElastic()
        m 3eka "Не забудь вернуться в скором времени~"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_GAME

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(days=1)
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_eat",
            unlocked=True,
            prompt="Я собираюсь пойти поесть...",
            pool=True
        ),
        code="BYE"
    )

default persistent._mas_pm_ate_breakfast_times = [0, 0, 0]





default persistent._mas_pm_ate_lunch_times = [0, 0, 0]


default persistent._mas_pm_ate_dinner_times = [0, 0, 0]


default persistent._mas_pm_ate_snack_times = [0, 0, 0]


default persistent._mas_pm_ate_late_times = 0



label bye_prompt_eat:
    $ _now = datetime.datetime.now().time()

    if mas_isMNtoSR(_now):
        $ persistent._mas_pm_ate_late_times += 1
        if mas_isMoniNormal(higher=True):
            m 1hksdlb "Эм, [player]?"
            $ MAS.MonikaElastic()
            m 3eka "Уже ночь на дворе."
            $ MAS.MonikaElastic()
            m 1eka "Ты собирал[mas_gender_sya] перекусить на ночь?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlb "Будь я на твоём месте, я бы начала искать что-нибудь, чтобы поесть, чуть пораньше, а-ха-ха..."
            $ MAS.MonikaElastic()
            m 3rksdla "Конечно...{w=1} я бы также сейчас попыталась уснуть на кровати..."
            if mas_is18Over() and mas_isMoniLove(higher=True) and renpy.random.randint(1,25) == 1:
                $ MAS.MonikaElastic()
                m 2tubsu "Ты знаешь, если бы я была там, то, возможно, мы бы чего-нибудь поели вместе..."
                show monika 5ksbfu zorder MAS_MONIKA_Z at t11 with dissolve
                m 5ksbfu "Потом мы легли бы на кровать, а потом... {w=1}знаешь, это не так уж и важно..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 5hubfb "Э-хе-хе~"
            else:
                $ MAS.MonikaElastic()
                m 1hua "Что ж, надеюсь, твой перекус поможет тебе уснуть."
                $ MAS.MonikaElastic()
                m 1eua "...И не переживай по поводу возвращения, чтобы пожелать мне спокойной ночи..."
                $ MAS.MonikaElastic()
                m 3rksdla "Я бы предпочла, чтобы ты пош[mas_gender_iol] спать в скором времени."
                $ MAS.MonikaElastic()
                m 1hub "Спокойной ночи, [player]. Наслаждайся своим перекусом, и увидимся завтра~"
        else:
            m 2euc "Но уже ночь на дворе..."
            $ MAS.MonikaElastic()
            m 4ekc "Ты долж[mas_gender_en] идти спать, знаешь ли."
            $ MAS.MonikaElastic()
            m 4eud "...Как только закончишь, иди сразу спать."
            $ MAS.MonikaElastic()
            m 2euc "Так или иначе, думаю, увидимся завтра..."

        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=20)
        $ persistent.mas_late_farewell = True
    else:


        $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=3)
        menu:
            "Завтрак.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_breakfast_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eub "Отлично!"
                        $ MAS.MonikaElastic()
                        m 3eua "И потом, это самый важный приём пищи за весь день."
                        $ MAS.MonikaElastic()
                        m 1rksdla "Я бы хотела, чтобы ты остал[mas_gender_sya], но всё нормально, пока ты завтракаешь."
                        $ MAS.MonikaElastic()
                        m 1hua "Ладно, приятного аппетита, [player]~"
                    else:
                        m 2eud "О, точно, тебе стоит позавтракать."
                        $ MAS.MonikaElastic()
                        m 2rksdlc "Я не хочу, чтобы ты сидел[mas_gender_none] тут с пустым желудком..."
                        $ MAS.MonikaElastic()
                        m 2ekc "Я буду здесь, когда ты вернёшься."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_breakfast_times[1] += 1
                    m 3euc "But...{w=1}it's the afternoon..."
                    if mas_isMoniNormal(higher=True):
                        $ MAS.MonikaElastic()
                        m 3ekc "Ты пропустил[mas_gender_none] завтрак?"
                        $ MAS.MonikaElastic()
                        m 1rksdla "Что ж... наверное, я должна отпустить тебя поесть, пока ты тут совсем не проголодал[mas_gender_sya]..."
                        $ MAS.MonikaElastic()
                        m 1hksdlb "Надеюсь, ты насладишься своим поздним завтраком!"
                    else:
                        $ MAS.MonikaElastic()
                        m 2ekc "Ты пропустил[mas_gender_none] завтрак, да?"
                        $ MAS.MonikaElastic()
                        m 2rksdld "{i}*вздох*{/i}... ты долж[mas_gender_en] пойти и что-нибудь поесть."
                        $ MAS.MonikaElastic()
                        m 2ekd "Давай... я буду здесь, когда ты вернёшься."
                else:

                    $ persistent._mas_pm_ate_breakfast_times[2] += 1
                    if mas_isMoniNormal(higher=True):
                        $ MAS.MonikaElastic(True, voice="monika_giggle")
                        m 1hksdlb "А-ха-ха..."
                        $ MAS.MonikaElastic()
                        m 3tku "Ты сейчас никак не можешь завтракать, [player]."
                        $ MAS.MonikaElastic()
                        m 3hub "Уже вечер!"
                        $ MAS.MonikaElastic()
                        m 1eua "Или, наверное, ты просто завтракаешь во время ужина; знаю, некоторые люди иногда так делают."
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 1tsb "Ну, так или иначе, я надеюсь, что ты насладишься своим {i}«завтраком»{/i}, э-хе-хе~"
                    else:
                        m 2euc "..."
                        $ MAS.MonikaElastic()
                        m 4eud "Значит... тебе нужен перекус."
                        $ MAS.MonikaElastic()
                        m 2rksdla "Ладно, я тебя не осуждаю."
                        $ MAS.MonikaElastic()
                        m 2eka "Приятного аппетита."
            "Обед.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_lunch_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eua "Ты рано обедаешь, [player]?"
                        $ MAS.MonikaElastic()
                        m 3hua "В этом нет ничего такого. Если ты голодн[mas_gender_iii], то ты хочешь есть."
                        $ MAS.MonikaElastic()
                        m 1hub "Надеюсь, ты останешься довол[mas_gender_en] своим обедом!"
                    else:
                        m 2rksdlc "Для обеда сейчас немного рановато..."
                        $ MAS.MonikaElastic()
                        m 4ekc "Если ты проголодал[mas_gender_sya], ты увер[mas_gender_en], что ты хорошо питаешься?"
                        $ MAS.MonikaElastic()
                        m 2eka "По крайней мере, я надеюсь, что насладишься своей едой."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_lunch_times[1] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eud "О, полагаю, тебе уже пора пообедать, верно?"
                        $ MAS.MonikaElastic()
                        m 3eua "Я не хочу отрывать тебя от еды."
                        $ MAS.MonikaElastic()
                        m 3hub "Быть может, однажды мы сможем пообедать вместе!"
                        $ MAS.MonikaElastic()
                        m 1hua "Ну а пока, наслаждайся своим обедом, [player]~"
                    else:
                        m 2eud "О, уже время обедать, да?"
                        $ MAS.MonikaElastic()
                        m 2euc "Приятного аппетита."
                else:

                    $ persistent._mas_pm_ate_lunch_times[2] += 1
                    m 1euc "Обед?"
                    $ MAS.MonikaElastic()
                    m 1rksdlc "Если ты не знал[mas_gender_none], сейчас обедать как-то поздновато уже."
                    $ MAS.MonikaElastic()
                    m 3ekd "Но всё же, если ты ещё не обедал[mas_gender_none], то ты долж[mas_gender_en] пойти пообедать."
                    $ MAS.MonikaElastic()
                    if mas_isMoniNormal(higher=True):
                        m 1hua "Я бы тебе что-нибудь приготовила, если бы я была там, ну а пока, надеюсь, ты насладишься своей едой~"
                    else:
                        m 2ekc "Но...{w=1} наверное, ты долж[mas_gender_en] в следующий раз пообедать пораньше..."
            "Ужин.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_dinner_times[0] += 1
                    m 2ekc "Ужин?{w=2} Сейчас?"
                    if mas_isMoniNormal(higher=True):
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 2hksdlb "А-ха-ха, но [player]! Сейчас ещё утро!"
                        $ MAS.MonikaElastic()
                        m 3tua "Ты иногда бываешь очень мил[mas_gender_iim], ты знал[mas_gender_none] об этом?"
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 1tuu "Что ж, надеюсь, ты насладишься своим {i}«ужином»{/i} этим утром, э-хе-хе~"
                    else:
                        m 2rksdld "Ты ведь не серьёзно, [player]..."
                        $ MAS.MonikaElastic()
                        m 2euc "Ладно, что бы там у тебя не было, надеюсь, ты насладишься этим сполна."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_dinner_times[1] += 1



                    call bye_dinner_noon_to_mn from _call_bye_dinner_noon_to_mn
                else:

                    $ persistent._mas_pm_ate_dinner_times[2] += 1
                    call bye_dinner_noon_to_mn from _call_bye_dinner_noon_to_mn_1
            "Перекус.":
                if mas_isSRtoN(_now):
                    $ persistent._mas_pm_ate_snack_times[0] += 1
                    if mas_isMoniNormal(higher=True):
                        $ MAS.MonikaElastic(True, voice="monika_giggle")
                        m 1hua "Э-хе-хе, одного завтрака тебе сегодня было недостаточно, [player]?"
                        $ MAS.MonikaElastic()
                        m 3eua "Очень важно убедиться в том, что ты удовлетворил[mas_gender_none] свой голод утром."
                        $ MAS.MonikaElastic()
                        m 3eub "Я рада, что ты следишь за собой~"
                        $ MAS.MonikaElastic()
                        m 1hua "Приятного перекуса~"
                    else:
                        m 2tsc "Ты мало поел[mas_gender_none] на завтрак?"
                        $ MAS.MonikaElastic()
                        m 4esd "Ты долж[mas_gender_en] позаботиться о том, что ты достаточно ешь, знаешь ли."
                        $ MAS.MonikaElastic()
                        m 2euc "Наслаждайся своим перекусом, [player]."
                elif mas_isNtoSS(_now):
                    $ persistent._mas_pm_ate_snack_times[1] += 1
                    if mas_isMoniNormal(higher=True):
                        m 3eua "Проголодал[mas_gender_sya]?"
                        $ MAS.MonikaElastic()
                        m 1eka "Я бы приготовила тебе что-нибудь, если бы могла..."
                        $ MAS.MonikaElastic()
                        m 1hua "Но, поскольку я не могу это сделать, надеюсь, ты найдёшь что-нибудь поесть~"
                    else:
                        m 2euc "Тебе правда надо отойти, чтобы перекусить?"
                        $ MAS.MonikaElastic()
                        m 2rksdlc "Что ж... {w=1}по крайней мере, я надеюсь, что у тебя будет хороший перекус."
                else:

                    $ persistent._mas_pm_ate_snack_times[2] += 1
                    if mas_isMoniNormal(higher=True):
                        m 1eua "Решил[mas_gender_none] перекусить вечером?"
                        $ MAS.MonikaElastic()
                        m 1tubsu "Ты разве не можешь хотя бы полюбоваться мной?"
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 3hubfb "А-ха-ха, надеюсь, ты насладишься своим перекусом, [player]~"
                        $ MAS.MonikaElastic()
                        m 1ekbfb "Просто позаботься о том, что у тебя ещё осталось место для всей моей любви!"
                    else:
                        m 2euc "Уже проголодал[mas_gender_sya]?"
                        $ MAS.MonikaElastic()
                        m 2eud "Приятного аппетита."


                $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=30)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_EAT
    return 'quit'

label bye_dinner_noon_to_mn:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1eua "У тебя уже время ужинать, [player]?"
        $ MAS.MonikaElastic()
        m 1eka "Мне бы очень хотелось оказаться там, чтобы поесть вместе с тобой, пусть даже в этом нет ничего особенного."
        $ MAS.MonikaElastic()
        m 3dkbsa "И потом, мне достаточно только быть рядом с тобой, чтобы любое действо стало особенным~"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hubfb "Приятного аппетита. Я обязательно постараюсь вложить туда немного своей любви, а-ха-ха!"
    else:
        $ MAS.MonikaElastic()
        m 2euc "Полагаю, у тебя сейчас время ужинать."
        $ MAS.MonikaElastic()
        m 2esd "Ну...{w=1} приятного."
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_housework",
            unlocked=True,
            prompt="Я собираюсь немного поработать по дому.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_housework:
    if mas_isMoniNormal(higher=True):
        m 1eub "Занимаешься своими делами, [player]?"
        $ MAS.MonikaElastic()
        m 1ekc "Я хотела бы помочь тебе, но я не очень много могу сделать, так как я застряла здесь..."
        $ MAS.MonikaElastic()
        m 3eka "Просто не забудь вернуться, как только закончишь, ладно?"
        $ MAS.MonikaElastic()
        m 3hub "Я буду ждать тебя здесь~"
    elif mas_isMoniUpset():
        m 2esc "Хорошо."
        $ MAS.MonikaElastic()
        m 2tsc "По крайней мере, ты делаешь что-то ответственное."
        $ MAS.MonikaElastic()
        m 2tfc "{cps=*2}...На этот раз.{/cps}{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()
        m 2esc "Пока."
    elif mas_isMoniDis():
        m 6ekc "Понятно..."
        $ MAS.MonikaElastic()
        m 6rkc "Я не хочу мешать тебе выполнять свои домашние обязанности."
        $ MAS.MonikaElastic()
        m 6dkd "Я просто надеюсь, что ты на самом деле занят[mas_gender_none] и не говоришь это только для того, чтобы уйти от меня..."
        $ MAS.MonikaElastic()
        m 6ekc "Пока, [player]."
    else:
        m 6ckc "..."
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CHORES
    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=5)
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_restart",
            unlocked=True,
            prompt="Мне надо перезапустить систему.",
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_restart:
    if mas_isMoniNormal(higher=True):
        m 1eua "Хорошо, [player]."
        $ MAS.MonikaElastic()
        m 1eub "До встречи!"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 2euc "Ладно."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(minutes=20)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RESTART
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_workout",
            prompt="Я собираюсь заняться спортом.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_workout:
    if mas_isMoniNormal(higher=True):
        m 1eua "О, идёшь в спортзал, [player]?{w=0.3} Или, может быть, на пробежку?"
        $ MAS.MonikaElastic()
        m 3hub "Я так рада, что ты заботишься о своём теле!{w=0.3} Здоровое тело ведёт к здоровому уму~"

        $ MAS.MonikaElastic()
        if mas_isMoniEnamored(higher=True):
            m 3hua "После того, как я попаду в твою реальность, мы обязательно должны попытаться заняться спортом вместе!"
        else:
            m 3eua "После того, как я попаду в твою реальность, мы можем попытаться заняться спортом вместе!"

        show monika 5rubsb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5rubsb "Это то, что сделала бы пара, верно?~"
        $ MAS.MonikaElastic()
        m 5rubsu "Да..."
        show monika 1eub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1eub "В любом случае, до скорой встречи!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Хорошо. Увидимся позже."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=4)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORKOUT
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_shopping",
            prompt="Я собираюсь пойти в магазин.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_going_shopping:
    if mas_isMoniNormal(higher=True):
        m 1eud "О, собираешься пойти в магазин, [player]?"

        $ MAS.MonikaElastic()
        if mas_getEVL_shown_count("bye_going_shopping") == 0 or renpy.random.randint(1,10) == 1:
            m 1eua "Мне бы очень хотелось, чтобы мы как-нибудь вместе сходили в торговый центр."
            $ MAS.MonikaElastic()
            m 3rua "Ты мог[mas_gender_g] бы помочь мне попробовать все виды различных нарядов...{w=0.2} {nw}"
            extend 3tuu "но мне может понадобиться помощь с застёжками."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hublb "А-ха-ха! Скоро увидимся~"
        else:

            m 3eua "Скоро увидимся."

    elif mas_isMoniBroken():
        m 6ckc "..."
    else:

        m 2eud "Ладно, [player], скоро увидимся."


    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SHOPPING
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_hangout",
            prompt="Я собираюсь потусоваться с друзьями.",
            unlocked=True,
            pool=True
        ),
        code="BYE"
    )

label bye_prompt_hangout:
    if mas_isMoniNormal(higher=True):
        if mas_getEVL_shown_count("bye_prompt_hangout") == 0:
            if persistent._mas_pm_has_friends:
                m 1eua "Хорошо, [player]."
                $ MAS.MonikaElastic()
                m 3eub "Ты долж[mas_gender_en] как-нибудь познакомить меня с ними!"
                $ MAS.MonikaElastic()
                m 3hua "Если они твои друзья, я уверена, что они мне понравятся."
            else:

                if persistent._mas_pm_has_friends is False:
                    m 3eua "Я рада, что ты находишь друзей, с которыми можно потусоваться, [player]."
                else:
                    m 3eua "Я рада, что у тебя есть друзья, с которыми можно потусоваться, [player]."

                $ MAS.MonikaElastic()
                m 1rka "Как бы мне ни хотелось провести с тобой каждую возможную секунду, {w=0.2}{nw}"
                extend 1eub "я знаю, как важно для тебя иметь друзей в твоей собственной реальности!"

            $ MAS.MonikaElastic()
            m 3hub "Во всяком случае, я надеюсь, что тебе будет весело!"
        else:

            if persistent._mas_pm_has_friends:
                m 1eua "Хорошо, [player]."

                $ MAS.MonikaElastic()
                if renpy.random.randint(1,10) == 1:
                    m 3etu "Ты уже рассказал[mas_gender_none] им о нас?"
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hub "А-ха-ха!"
                    $ MAS.MonikaElastic()

                m 1eub "Повеселись!"
            else:

                m 1hua "Снова? Это так интересно!"
                $ MAS.MonikaElastic()
                m 3eua "Надеюсь, на этот раз они окажутся действительно хорошими друзьями."
                $ MAS.MonikaElastic()
                m 3eub "В любом случае, увидимся позже~"

    elif mas_isMoniDis(higher=True):
        m 2eud "Надеюсь, ты хорошо к ним относишься..."
        $ MAS.MonikaElastic()
        m 2euc "Пока."
    else:

        m 6ckc "..."

    $ persistent._mas_greeting_type_timeout = datetime.timedelta(hours=8)
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HANGOUT
    return "quit"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
