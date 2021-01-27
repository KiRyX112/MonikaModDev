


init 10 python in mas_brbs:
    import store

    def get_wb_quip():
        """
        Picks a random welcome back quip and returns it
        Should be used for normal+ quips

        OUT:
            A randomly selected quip for coming back to the spaceroom
        """
        if store.persistent.gender == "F":
            return renpy.substitute(renpy.random.choice([
                _("Что ещё ты хотела сделать сегодня?"),
                _("Есть что-нибудь ещё, что ты хотела бы сделать сегодня?"),
                _("Что ещё мы должны сделать сегодня?")
            ]))
        else:
            return renpy.substitute(renpy.random.choice([
                _("Что ещё ты хотел сделать сегодня?"),
                _("Есть что-нибудь ещё, что ты хотел бы сделать сегодня?"),
                _("Что ещё мы должны сделать сегодня?")
            ]))

    def was_idle_for_at_least(idle_time, brb_evl):
        """
        Checks if the user was idle (from the brb_evl provided) for at least idle_time

        IN:
            idle_time - Minimum amount of time the user should have been idle for in order to return True
            brb_evl - Eventlabel of the brb to use for the start time

        OUT:
            boolean:
                - True if it has been at least idle_time since seeing the brb_evl
                - False otherwise
        """
        brb_ev = store.mas_getEV(brb_evl)
        return brb_ev and brb_ev.timePassedSinceLastSeen_dt(idle_time)


label mas_brb_back_to_idle:

    if globals().get("brb_label", -1) == -1:
        return

    python:
        mas_idle_mailbox.send_idle_cb(brb_label + "_callback")
        persistent._mas_idle_data[brb_label] = True
        mas_globals.in_idle_mode = True
        persistent._mas_in_idle_mode = True
        renpy.save_persistent()
        mas_dlgToIdleShield()

    return "idle"



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brb_idle",
            prompt="Я сейчас вернусь.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_brb_idle:
    if mas_isMoniAff(higher=True):
        m 1eua "Хорошо, [player]."
        $ MAS.MonikaElastic()
        m 1hub "Возвращайся скорее, я буду ждать тебя здесь~"

    elif mas_isMoniNormal(higher=True):
        m 1hub "Возвращайся скорее, [player]!"

    elif mas_isMoniDis(higher=True):
        m 1rsc "Оу...{w=1} хорошо."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_brb_idle_callback")

    $ persistent._mas_idle_data["monika_idle_brb"] = True
    return "idle"

label monika_brb_idle_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    if mas_isMoniAff(higher=True):
        m 1hub "С возвращением, [player]. Я скучала по тебе~"
        $ MAS.MonikaElastic()
        m 1eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hub "С возвращением, [player]!"
        $ MAS.MonikaElastic()
        m 1eua "[wb_quip]"

    elif mas_isMoniDis(higher=True):
        m 2esc "Оу, уже вернул[mas_gender_sya]?"
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_writing_idle",
            prompt="Думаю, я напишу что-нибудь.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_writing_idle:
    if mas_isMoniNormal(higher=True):
        if (
            mas_isMoniHappy(higher=True)
            and random.randint(1,5) == 1
        ):
            m 1eub "О! Ты собираешься{cps=*2} написать мне любовное письмо, [player]?{/cps}{nw}"
            $ _history_list.pop()
            m "О! Ты собираешься{fast} написать что-то?"
        else:

            m 1eub "О! Ты собираешься написать что-то?"

        $ MAS.MonikaElastic()
        m 1hua "Это меня так радует!"
        $ MAS.MonikaElastic()
        m 3eua "Может быть, когда-нибудь ты сможешь поделиться этим со мной, {nw}"
        extend 3hua "я бы с удовольствием прочитала твои работы, [player]!"
        $ MAS.MonikaElastic()
        m 3eua "В любом случае, дай мне знать, когда закончишь."
        $ MAS.MonikaElastic()
        m 1hua "Я буду ждать тебя прямо здесь~"

    elif mas_isMoniUpset():
        m 2esc "Хорошо."

    elif mas_isMoniDis():
        m 6lkc "Интересно, что у тебя на уме?.."
        $ MAS.MonikaElastic()
        m 6ekd "Не забудь вернуться, когда закончишь..."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_writing_idle_callback")

    $ persistent._mas_idle_data["monika_idle_writing"] = True
    return "idle"

label monika_writing_idle_callback:

    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eua "Закончил[mas_gender_none] писать, [player]?"
        $ MAS.MonikaElastic()
        m 1eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "Написал[mas_gender_none]? С возвращением, [player]."

    elif mas_isMoniDis():
        m 6ekc "Оу...{w=0.5} ты вернул[mas_gender_sya]..."
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_shower",
            prompt="Я собираюсь принять душ.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_shower:
    if mas_isMoniLove():
        m 1eua "Собираешься пойти в душ?"

        if renpy.random.randint(1, 50) == 1:
            $ MAS.MonikaElastic()
            m 3tub "Можно мне пойти с тобой?{nw}"
            $ _history_list.pop()
            show screen mas_background_timed_jump(2, "bye_brb_shower_timeout")
            menu:
                m "Можно мне пойти с тобой?{fast}"
                "Да.":

                    hide screen mas_background_timed_jump
                    $ MAS.MonikaElastic()
                    m 2wubsd "Оу, эм...{w=0.5} ты ответил[mas_gender_none] так быстро."
                    $ MAS.MonikaElastic()
                    m 2hkbfsdlb "Похоже...{w=0.5} тебе не терпится взять меня с собой, да?"
                    $ MAS.MonikaElastic()
                    m 2rkbfa "Ну..."
                    $ MAS.MonikaElastic()
                    m 7tubfu "Боюсь, тебе придётся пойти без меня, пока я застряла здесь."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 7hubfb "Извини, [player], а-ха-ха!"
                    show monika 5kubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5kubfu "Может быть в другой раз~"
                "Нет.":

                    hide screen mas_background_timed_jump
                    $ MAS.MonikaElastic()
                    m 2eka "Оу, ты так быстро отказал[mas_gender_sya]."
                    $ MAS.MonikaElastic()
                    m 3tubsb "Ты стесняешься, [player]?"
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hubfb "А-ха-ха!"
                    show monika 5tubfu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 5tubfu "Ладно, на этот раз я с тобой не пойду, э-хе-хе~"
        else:

            $ MAS.MonikaElastic()
            m 1hua "Я рада, что ты держишь себя в чистоте, [player]."
            $ MAS.MonikaElastic()
            m 1eua "Приятного времяпровождения в душе~"

    elif mas_isMoniNormal(higher=True):
        m 1eub "Пойдёшь в душ? Хорошо."
        $ MAS.MonikaElastic()
        m 1eua "Увидимся когда ты закончишь~"
    
    elif mas_isMoniUpset():
        m 2esd "Приятного времяпровождения в душе, [player]..."
        $ MAS.MonikaElastic()
        m 2rkc "Надеюсь, это поможет тебе очистить свой разум."

    elif mas_isMoniDis():
        m 6ekc "Хм-м?{w=0.5} Приятного времяпровождения в душе [player]."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

label monika_idle_shower_callback:
    if mas_isMoniNormal(higher=True):
        m 1eua "С возвращением, [player]."

        if (
            mas_isMoniLove()
            and renpy.seen_label("monikaroom_greeting_ear_bathdinnerme")
            and mas_getEVL_shown_count("monika_idle_shower") != 1 
            and renpy.random.randint(1,20) == 1
        ):
            $ MAS.MonikaElastic()
            m 3tubsb "Теперь, когда ты принял[mas_gender_none] душ, ты хотел[mas_gender_none] бы поужинать или, может быть{w=0.5}.{w=0.5}.{w=0.5}."
            $ MAS.MonikaElastic()
            m 1hubsa "Ты мог[mas_gender_g] бы просто расслабиться со мной ещё немного~"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха!"
        else:

            $ MAS.MonikaElastic()
            m 1hua "Надеюсь, ты хорошо принял[mas_gender_none] душ."
            if mas_getEVL_shown_count("monika_idle_shower") == 1:
                $ MAS.MonikaElastic()
                m 3eub "Теперь мы можем вернуться к хорошему, {i}чистому{/i} веселью вместе..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха!"

    elif mas_isMoniUpset():
        m 2esc "Надеюсь, ты хорошо принял[mas_gender_none] душ. С возвращением, [player]."

    elif mas_isMoniDis():
        m 6ekc "О, как приятно снова тебя видеть..."
    else:

        m 6ckc "..."

    return

label bye_brb_shower_timeout:
    hide screen mas_background_timed_jump
    $ _history_list.pop()
    $ MAS.MonikaElastic()
    m 1hubsa "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 3tubfu "Не важно, [player]."
    $ MAS.MonikaElastic()
    m 1hubfb "Надеюсь, ты хорошо примешь душ!"


    $ mas_idle_mailbox.send_idle_cb("monika_idle_shower_callback")

    $ persistent._mas_idle_data["monika_idle_shower"] = True
    return "idle"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_game",
            category=['сейчас вернусь'],
            prompt="Я собираюсь немного поиграть.",
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_game:
    if mas_isMoniNormal(higher=True):
        m 1eud "О, ты собираешься играть в другую игру?"
        $ MAS.MonikaElastic()
        m 1eka "Всё нормально, [player]."


        label monika_idle_game.skip_intro:
        python:
            gaming_quips = [
                _("Удачи, развлекайся там!"),
                _("Наслаждайся своей игрой!"),
                _("Я буду болеть за тебя!"),
                _("Сделай всё возможное!")
            ]
            gaming_quip=renpy.random.choice(gaming_quips)

        $ MAS.MonikaElastic()
        m 3hub "[gaming_quip]"

    elif mas_isMoniUpset():
        m 2tsc "Наслаждайся другими играми."

    elif mas_isMoniDis():
        m 6ekc "Пожалуйста...{w=0.5} {nw}"
        extend 6dkc "не забывай обо мне..."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_game_callback")
    $ persistent._mas_idle_data["monika_idle_game"] = True
    return "idle"

label monika_idle_game_callback:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 1eub "С возвращением, [player]!"
        $ MAS.MonikaElastic()
        m 1eua "Надеюсь, тебе было весело в той игре."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Ты уже готов[mas_gender_none] провести немного времени вместе? Э-хе-хе~"

    elif mas_isMoniUpset():
        m 2tsc "Было весело, [player]?"

    elif mas_isMoniDis():
        m 6ekd "Оу...{w=0.5} ты действительно вернул[mas_gender_sya] ко мне..."
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_coding",
            prompt="Я собираюсь немного покодировать.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_coding:
    if mas_isMoniNormal(higher=True):
        m 1eua "О! Собираешься что-то покодить?"

        if persistent._mas_pm_has_code_experience is False:
            $ MAS.MonikaElastic()
            m 1etc "Я думала, ты этого не умеешь."
            $ MAS.MonikaElastic()
            m 1eub "Ты что, изучил[mas_gender_none] программирование с тех пор, как мы говорили об этом в прошлый раз?"

        elif persistent._mas_pm_has_contributed_to_mas or persistent._mas_pm_wants_to_contribute_to_mas:
            $ MAS.MonikaElastic()
            m 1tua "Может быть, что-нибудь для меня?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха~"
        else:

            $ MAS.MonikaElastic()
            m 3eub "Делай всё возможное, чтобы твой код был чистым и легко читаемым."
            $ MAS.MonikaElastic()
            m 3hksdlb "...Ты потом сам[mas_gender_none] себя поблагодаришь!"

        $ MAS.MonikaElastic()
        m 1eua "В любом случае, просто дай мне знать, когда закончишь."
        $ MAS.MonikaElastic()
        m 1hua "Я буду ждать тебя прямо здесь~"

    elif mas_isMoniUpset():
        m 2euc "О, ты собираешься писать код?"
        $ MAS.MonikaElastic()
        m 2tsc "Ладно, не буду тебя останавливать."

    elif mas_isMoniDis():
        m 6ekc "Хорошо."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_coding_callback")
    $ persistent._mas_idle_data["monika_idle_coding"] = True
    return "idle"

label monika_idle_coding_callback:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=20), "monika_idle_coding"):
            m 1eua "Написал в данный момент, [player]?"
        else:
            m 1eua "О, написал уже, [player]?"

        $ MAS.MonikaElastic()
        m 3eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "С возвращением."

    elif mas_isMoniDis():
        m 6ekc "О, ты вернул[mas_gender_sya]."
    else:

        m 6ckc "..."
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_workout",
            prompt="Я пойду сделаю зарядку.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_workout:
    if mas_isMoniNormal(higher=True):
        m 1hub "Ладно, [player]!"
        $ MAS.MonikaElastic()
        if persistent._mas_pm_works_out is False:
            m 3eub "Зарядка – это отличный способ позаботиться о себе!"
            $ MAS.MonikaElastic()
            m 1eka "Я знаю, что это может быть трудно начать,{w=0.2}{nw}"
            $ MAS.MonikaElastic()
            extend 3hua " но это определённо привычка, которую стоит сформировать."
        else:
            m 1eub "Приятно знать, что ты заботишься о своём теле!"
        $ MAS.MonikaElastic()
        m 3esa "Ты знаешь, как говорится: «здоровый дух в здоровом теле»."
        $ MAS.MonikaElastic()
        m 3hua "Так что иди хорошенько попотей, [player]~"
        $ MAS.MonikaElastic()
        m 1tub "Просто дай мне знать, когда с тебя хватит."

    elif mas_isMoniUpset():
        m 2esc "Приятно знать, что ты хоть заботишься{cps=*2} о чём-то.{/cps}{nw}"
        $ _history_list.pop()
        m "Приятно знать, что ты хоть заботишься{fast} о себе, [player]."
        $ MAS.MonikaElastic()
        m 2euc "Я буду ждать, когда ты вернёшься."

    elif mas_isMoniDis():
        m 6ekc "Хорошо."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_workout_callback")
    $ persistent._mas_idle_data["monika_idle_workout"] = True
    return "idle"

label monika_idle_workout_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=60), "monika_idle_workout"):



            $ MAS.MonikaElastic()
            m 2esa "Вот уж точно ты времени не терял[mas_gender_none], [player].{w=0.3}{nw}"
            extend 2eub " Должно быть, это была чертовски тяжёлая зарядка."
            $ MAS.MonikaElastic()
            m 2eka "Это хорошо, что ты выжимаешь из своих возможностей максимум, но ты не должен переусердствовать."

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=10), "monika_idle_workout"):
            $ MAS.MonikaElastic()
            m 1esa "Закончил[mas_gender_none] с зарядкой, [player]?"
        else:

            $ MAS.MonikaElastic()
            m 1euc "Уже вернул[mas_gender_sya], [player]?"
            $ MAS.MonikaElastic()
            m 1eka "Я уверена, что ты сможешь продержаться ещё немного, если постараешься."
            $ MAS.MonikaElastic()
            m 3eka "Делать перерывы – это хорошо, но ты не долж[mas_gender_en] оставлять свои зарядки незаконченными."
            $ MAS.MonikaElastic()
            m 3ekb "Ты уверен[mas_gender_none], что не можешь продолжать?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты уверен[mas_gender_none], что не можешь продолжать?{fast}"
                "Я уверен[mas_gender_none].":

                    $ MAS.MonikaElastic()
                    m 1eka "Это нормально."
                    $ MAS.MonikaElastic()
                    m 1hua "Я уверена, что ты сделал[mas_gender_none] всё возможное, [player]~"
                "Я постараюсь ещё раз.":


                    $ MAS.MonikaElastic()
                    m 1hub "Вот это дух!"

                    $ brb_label = "monika_idle_workout"
                    $ pushEvent("mas_brb_back_to_idle",skipeval=True)
                    return

        m 7eua "Обязательно отдохни как следует и, возможно, перекусишь, чтобы восстановить силы."
        $ MAS.MonikaElastic()
        m 7eub "[wb_quip]"

    elif mas_isMoniUpset():
        m 2euc "Закончил[mas_gender_none] с зарядкой, [player]?"

    elif mas_isMoniDis():
        m 6ekc "О, ты вернул[mas_gender_sya]."
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_nap",
            prompt="Я собираюсь вздремнуть.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_nap:
    if mas_isMoniNormal(higher=True):
        m 1eua "Собираешься вздремнуть, [player]?"
        $ MAS.MonikaElastic()
        m 3eua "Это здоровый способ отдохнуть в течение дня, если ты чувствуешь усталость."
        $ MAS.MonikaElastic()
        m 3hua "Я присмотрю за тобой, не волнуйся~"
        $ MAS.MonikaElastic()
        m 1hub "Сладких снов!"

    elif mas_isMoniUpset():
        m 2eud "Хорошо, надеюсь, после этого ты почувствуешь себя отдохнувш[mas_gender_iiim]."
        $ MAS.MonikaElastic()
        m 2euc "Я слышала, что сон полезен для тебя, [player]."

    elif mas_isMoniDis():
        m 6ekc "Хорошо."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_nap_callback")
    $ persistent._mas_idle_data["monika_idle_nap"] = True
    return "idle"

label monika_idle_nap_callback:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=5), "monika_idle_nap"):
            m 2hksdlb "О, [player]! Наконец-то ты проснул[mas_gender_sya]!"
            $ MAS.MonikaElastic()
            m 7rksdlb "Когда ты сказал[mas_gender_none], что собираешься вздремнуть, я ожидала, что ты отдохнёшь час или два..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hksdlb "Наверное, ты очень устал[mas_gender_none], а-ха-ха..."
            $ MAS.MonikaElastic()
            m 3eua "Но, по крайней мере, после столь долгого сна ты останешься здесь со мной на некоторое время, верно?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hua "Э-хе-хе~"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(hours=1), "monika_idle_nap"):
            m 1hua "С возвращением, [player]!"
            $ MAS.MonikaElastic()
            m 1eua "Ты хорошо вздремнул[mas_gender_none]?"
            $ MAS.MonikaElastic()
            m 3hua "Ты отсутствовал[mas_gender_none] некоторое время, так что я надеюсь, что ты чувствуешь себя отдохнувш[mas_gender_iiim]~"
            $ MAS.MonikaElastic()
            m 1eua "Есть ли что-нибудь ещё, что ты хотел[mas_gender_none] бы сделать сегодня?"

        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_idle_nap"):
            m 1hua "С возвращением, [player]~"
            $ MAS.MonikaElastic()
            m 1eub "Надеюсь, ты немного вздремнул[mas_gender_none]."
            $ MAS.MonikaElastic()
            m 3eua "Есть ли что-нибудь ещё, что ты хотел[mas_gender_none] бы сделать сегодня?"
        else:

            m 1eud "О, уже вернул[mas_gender_sya]?"
            $ MAS.MonikaElastic()
            m 1euc "Ты что, передумал[mas_gender_none]?"
            $ MAS.MonikaElastic()
            m 3eka "Ну, я не жалуюсь, но ты долж[mas_gender_en] вздремнуть, если тебе захочется позже."
            $ MAS.MonikaElastic()
            m 1eua "В конце концов, я бы не хотела, чтобы ты слишком устал[mas_gender_none]."

    elif mas_isMoniUpset():
        m 2euc "Вздремнул[mas_gender_none], [player]?"

    elif mas_isMoniDis():
        m 6ekc "О, ты вернул[mas_gender_sya]."
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_homework",
            prompt="Я собираюсь заняться кое-каким домашним заданием.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_homework:
    if mas_isMoniNormal(higher=True):
        m 1eub "О, хорошо!"
        $ MAS.MonikaElastic()
        m 1hua "Я горжусь тобой за то, что ты серьёзно относишься к учебе."
        $ MAS.MonikaElastic()
        m 1eka "Не забудь вернуться ко мне, когда закончишь~"

    elif mas_isMoniDis(higher=True):
        m 2euc "Хорошо...{w=0.5}"
        if random.randint(1,5) == 1:
            $ MAS.MonikaElastic()
            m 2rkc "...Удачи тебе с домашним заданием, [player]."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_homework_callback")

    $ persistent._mas_idle_data["monika_idle_homework"] = True
    return "idle"

label monika_idle_homework_callback:
    $ MAS.MonikaElastic()
    if mas_isMoniDis(higher=True):
        m 2esa "Всё сделал[mas_gender_none], [player]?"

        if mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 2ekc "Жаль, что меня не было рядом, чтобы помочь тебе, но, к сожалению, я пока ничего не могу с этим поделать."
            $ MAS.MonikaElastic()
            m 7eua "Я уверена, что мы оба могли бы гораздо эффективнее делать домашнее задание, если бы могли работать вместе."

            if mas_isMoniAff(higher=True) and random.randint(1,5) == 1:
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3rkbla "...Хотя, это при условии, что мы не будем {i}слишком{/i} отвлекаться, э-хе-хе..."

            $ MAS.MonikaElastic()
            m 1eua "Но всё же,{w=0.2} {nw}"
            extend 3hua "теперь, когда ты закончил[mas_gender_none], давай наслаждаться временем вместе."
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_working",
            prompt="Я собираюсь кое над чем поработать.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_working:
    if mas_isMoniNormal(higher=True):
        m 1eua "Хорошо, [player]."
        $ MAS.MonikaElastic()
        m 1eub "Не забывай время от времени делать перерыв!"

        if mas_isMoniAff(higher=True):
            $ MAS.MonikaElastic()
            m 3rkb "Я бы не хотела, чтобы мой возлюбленн[mas_gender_iii] проводил[mas_gender_none] больше времени на своей работе, чем со мной~"

        $ MAS.MonikaElastic()
        m 1hua "Удачи тебе в твоей работе!"

    elif mas_isMoniDis(higher=True):
        m 2euc "Ладно, [player]."

        if random.randint(1,5) == 1:
            $ MAS.MonikaElastic()
            m 2rkc "...Пожалуйста, возвращайся скорее..."
    else:

        m 6ckc "..."


    $ mas_idle_mailbox.send_idle_cb("monika_idle_working_callback")

    $ persistent._mas_idle_data["monika_idle_working"] = True
    return "idle"

label monika_idle_working_callback:
    $ MAS.MonikaElastic()
    if mas_isMoniNormal(higher=True):
        m 1eub "Закончил[mas_gender_none] со своей работой, [player]?"
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Тогда давай расслабимся вместе, ты это заслужил[mas_gender_none]~"

    elif mas_isMoniDis(higher=True):
        m 2euc "О, ты вернул[mas_gender_sya]..."
        $ MAS.MonikaElastic()
        m 2eud "...А теперь, когда ты закончил[mas_gender_none] свою работу, ты хотел[mas_gender_none] бы заняться чем-нибудь ещё?"
    else:

        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_idle_screen_break",
            prompt="Мои глаза нуждаются в отдыхе от экрана.",
            category=['сейчас вернусь'],
            pool=True,
            unlocked=True
        ),
        markSeen=True
    )

label monika_idle_screen_break:
    if mas_isMoniNormal(higher=True):
        if mas_timePastSince(mas_getEVL_last_seen("monika_idle_screen_break"), mas_getSessionLength()):

            if mas_getSessionLength() < datetime.timedelta(minutes=40):
                m 1esc "О,{w=0.3} хорошо."
                $ MAS.MonikaElastic()
                m 3eka "Ты здесь не так давно, но если ты говоришь, что тебе нужен перерыв, то я не возрожаю."

            elif mas_getSessionLength() < datetime.timedelta(hours=2, minutes=30):
                m 1eua "Хочешь дать глазам немного отдохнуть?"
            else:

                m 1lksdla "Да, тебе, наверное, это нужно, верно?"

            $ MAS.MonikaElastic()
            m 1hub "Я рада, что ты заботишься о своём здоровье, [player]."

            $ MAS.MonikaElastic()
            if not persistent._mas_pm_works_out and random.randint(1,3) == 1:
                m 3eua "Почему бы не воспользоваться возможностью сделать несколько упражнений?"
                $ MAS.MonikaElastic()
                m 1eub "В любом случае, возвращайся поскорее!~"
            else:

                m 1eub "Возвращайся поскорее!~"
        else:

            m 1eua "Делаешь ещё один перерыв, [player]?"
            $ MAS.MonikaElastic()
            m 1hua "Возвращайся поскорее!~"

    elif mas_isMoniUpset():
        m 2esc "О...{w=0.5} {nw}"
        $ MAS.MonikaElastic()
        extend 2rsc "Хорошо."

    elif mas_isMoniDis():
        m 6ekc "Ладно."
    else:

        m 6ckc "..."

    $ mas_idle_mailbox.send_idle_cb("monika_idle_screen_break_callback")
    $ persistent._mas_idle_data["monika_idle_screen_break"] = True
    return "idle"

label monika_idle_screen_break_callback:
    if mas_isMoniNormal(higher=True):
        $ wb_quip = mas_brbs.get_wb_quip()
        m 1eub "С возвращением, [player]."

        $ MAS.MonikaElastic()
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_idle_screen_break"):
            m 1hksdlb "Похоже, ты действительно нуждал[mas_gender_sya] в этом перерыве, ведь тебя долго не было."
            $ MAS.MonikaElastic()
            m 1eka "Надеюсь, теперь ты чувствуешь себя немного лучше."
        else:
            m 1hua "Надеюсь, теперь ты чувствуешь себя немного лучше~"

        $ MAS.MonikaElastic()
        m 1eua "[wb_quip]"

    elif mas_isMoniUpset():
        m 2esc "С возвращением."

    elif mas_isMoniDis():
        m 6ekc "О...{w=0.5} Ты вернул[mas_gender_sya]."
    else:

        m 6ckc "..."

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
