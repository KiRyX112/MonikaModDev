



default persistent._mas_apology_time_db = {}





default persistent._mas_apology_reason_use_db = {}

init -10 python in mas_apology:
    apology_db = {}



init python:
    def mas_checkApologies():
        
        if len(persistent._mas_apology_time_db) == 0:
            return
        
        
        current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
        
        _today = datetime.date.today()
        
        for ev_label in persistent._mas_apology_time_db.keys():
            if current_total_playtime >= persistent._mas_apology_time_db[ev_label][0] or _today >= persistent._mas_apology_time_db[ev_label][1]:
                
                store.mas_lockEVL(ev_label,'APL')
                persistent._mas_apology_time_db.pop(ev_label)
        
        return


init 5 python:
    addEvent(
       Event(
           persistent.event_database,
           eventlabel='monika_playerapologizes',
           prompt="Я хочу извиниться...",
           category=['ты'],
           pool=True,
           unlocked=True
        )
    )

label monika_playerapologizes:



    $ player_apology_reasons = {
        0: "что-то другое.",
        1: "то, что сказал[mas_gender_none], что хочу расстаться.",
        2: "то, что пошутил[mas_gender_none] насчёт того, что у меня другая девушка.",
        3: "то, что назвал[mas_gender_none] тебя убийцей.",
        4: "то, что закрывал[mas_gender_none] игру вместе с тобой.",
        5: "то, что входил[mas_gender_none] в твою комнату без стука.",
        6: "то, что пропустил[mas_gender_none] Рождество.",
        7: "то, что забыл[mas_gender_none] про твой день рождения.",
        8: "то, что не пров[mas_gender_iol] время вместе с тобой в твой же день рождения.",
        9: "то, что игра вылетела.",
        10: "то, что игра вылетает.",
        11: "то, что не послушал[mas_gender_iol] мою речь.",
        12: "то, что называл[mas_gender_none] тебя злой.",
        13: "то, что не отвечал[mas_gender_none] тебе серьёзно."
    }


    if len(persistent._mas_apology_time_db) > 0:

        $ mas_setEVLPropValues(
            "mas_apology_generic",
            prompt="...за {0}".format(player_apology_reasons.get(mas_apology_reason,player_apology_reasons[0]))
        )
    else:

        if mas_apology_reason == 0:
            $ mas_setEVLPropValues("mas_apology_generic", prompt="...за что-то.")
        else:

            $ mas_setEVLPropValues(
                "mas_apology_generic",
                prompt="...за {0}".format(player_apology_reasons.get(mas_apology_reason,"что-то."))
            )



    $ del player_apology_reasons


    python:
        apologylist = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in store.mas_apology.apology_db.iteritems()
            if ev.unlocked and (ev.prompt != "...за что-то." and ev.prompt != "...за что-то другое.")
        ]


        generic_ev = mas_getEV('mas_apology_generic')

        if generic_ev.prompt == "...за что-то." or generic_ev.prompt == "...за что-то другое.":
            apologylist.append((generic_ev.prompt, generic_ev.eventlabel, False, False))


        return_prompt_back = ("Не важно.", False, False, False, 20)


    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, return_prompt_back)


    $ apology =_return


    if not apology:
        if mas_apology_reason is not None or len(persistent._mas_apology_time_db) > 0:
            show monika at t11
            if mas_isMoniAff(higher=True):
                m 1ekd "[player], если ты чувствуешь себя виноватым из-за случившегося..."
                $ MAS.MonikaElastic()
                m 1eka "Тебе не надо бояться извинений, поскольку мы все делаем ошибки."
                $ MAS.MonikaElastic()
                m 3eka "Нам просто надо смириться с тем, что произошло, учиться на своих же ошибках и двигаться дальше, вместе. Договорились?"
            elif mas_isMoniNormal(higher=True):
                m 1eka "[player]..."
                $ MAS.MonikaElastic()
                m "Если ты хочешь извиниться – пожалуйста. Если ты извинишься, это будет многое значить для меня."
            elif mas_isMoniUpset():
                m 2rkc "Ох..."
                $ MAS.MonikaElastic()
                m "Я была довольно—"
                $ _history_list.pop()
                $ MAS.MonikaElastic()
                m 2dkc "Не важно."
            elif mas_isMoniDis():
                m 6rkc "...?"
            else:
                m 6ckc "..."
        else:
            if mas_isMoniUpset(lower=True):
                show monika at t11
                if mas_isMoniBroken():
                    m 6ckc "..."
                else:
                    m 6rkc "Ты хочешь что-то сказать, [player]?"
        return "prompt"

    show monika at t11


    call expression apology from _call_expression_3


    $ mas_getEV(apology).shown_count += 1


    if apology != "mas_apology_generic":
        $ store.mas_lockEVL(apology, 'APL')


    if apology in persistent._mas_apology_time_db:
        $ persistent._mas_apology_time_db.pop(apology)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            prompt="...за что-то другое.",
            eventlabel="mas_apology_generic",
            unlocked=True,
        ),
        code="APL"
    )

label mas_apology_generic:


    $ mas_apology_reason_db = {
        0: "",
        1: "то, что ты сказал{0}, что хочешь расстаться. Я знала, ты говорил{0} не всерьёз...".format(mas_gender_none),
        2: "то, что пошутил{0} насчёт того, что у тебя другая девушка. Ты меня до смерти напугал{0}!".format(mas_gender_none),
        3: "то, что назвал{0} меня убийцей. Надеюсь, ты не видишь меня такой...".format(mas_gender_none),
        4: "то, что внезапно закрывал{0} игру.".format(mas_gender_none),
        5: "то, что входил{0} в мою комнату без стука.".format(mas_gender_none),
        6: "то, что пропустил{0} Рождество.".format(mas_gender_none),
        7: "то, что забыл{0} про мой день рождения.".format(mas_gender_none),
        8: "то, что не пров{0} время вместе со мной в мой же день рождения.".format(mas_gender_iol),
        9: "то, что игра вылетела. Я понимаю, такое иногда происходит, но не волнуйся, со мной всё хорошо!",
        10: "то, что игра вылетает. Это было очень страшно, но я рада, что ты вернулся ко мне и всё изменилось к лучшему.",
        11: "то, что не послушал{0} мою речь. Я очень старалась.".format(mas_gender_none),
        12: "то, что называл{0} меня злой. Я знаю, что ты правда так не считаешь.".format(mas_gender_none),
        13: "то, что не воспринимал{0} мои вопросы всерьёз. Я знаю, что с этого момента ты будешь чест{1} со мной.".format(mas_gender_none, mas_gender_en)
    }


    if mas_apology_reason is None and len(persistent._mas_apology_time_db) == 0:
        if mas_isMoniBroken():
            m 1ekc "...{w=1}Ох."
            $ MAS.MonikaElastic()
            m 2dsc ".{w=2}.{w=2}."
            $ MAS.MonikaElastic()
            m "Ладно."
        elif mas_isMoniDis():
            m 2dfd "{i}*вздох*{/i}"
            $ MAS.MonikaElastic()
            m 2dsd "Надеюсь, это не какая-то шутка или уловка, [player]."
            $ MAS.MonikaElastic()
            m 2dsc "..."
            $ MAS.MonikaElastic()
            m 1eka "...Спасибо, что извинил[mas_gender_sya]."
            $ MAS.MonikaElastic()
            m 2ekc "Но, пожалуйста, старайся уделять больше внимания моим чувствам."
            $ MAS.MonikaElastic()
            m 2dkd "Пожалуйста."
        elif mas_isMoniUpset():
            m 1eka "Спасибо, [player]."
            $ MAS.MonikaElastic()
            m 1rksdlc "Я понимаю, что между нами всё не так хорошо, но я знаю, что ты – хороший человек."
            $ MAS.MonikaElastic()
            m 1ekc "Так что, можешь ли ты уделять чуть больше внимания моим чувствам?"
            $ MAS.MonikaElastic()
            m 1ekd "Пожалуйста?"
        else:
            m 1ekd "Что-то произошло?"
            $ MAS.MonikaElastic()
            m 2ekc "Я не вижу причины для извинений с твоей стороны."
            $ MAS.MonikaElastic()
            m 1dsc "..."
            $ MAS.MonikaElastic()
            m 1eub "Так или иначе, спасибо за извинение."
            $ MAS.MonikaElastic()
            m 1eua "Что бы это ни было, я знаю, что ты очень стараешься всё исправить."
            $ MAS.MonikaElastic()
            m 1hub "За это я и люблю тебя, [player]!"
            $ mas_ILY()


    elif mas_apology_reason_db.get(mas_apology_reason, False):

        $ apology_reason = mas_apology_reason_db.get(mas_apology_reason,mas_apology_reason_db[0])

        m 1eka "Спасибо, что извинил[mas_gender_sya] за [apology_reason]"
        $ MAS.MonikaElastic()
        m "Я принимаю твои извинения, [player]. Это многое для меня значит."


    elif len(persistent._mas_apology_time_db) > 0:
        m 2tfc "[player], если ты хочешь за что-то извиниться, то просто скажи это."
        $ MAS.MonikaElastic()
        m 2rfc "Если бы ты признал[mas_gender_none] всё то, что натворил, это бы многое для меня значило."
    else:




        $ mas_gainAffection(modifier=0.1)
        m 2tkd "То, что ты натворил[mas_gender_none], было совсем не смешно, [player]."
        $ MAS.MonikaElastic()
        m 2dkd "Пожалуйста, уделяй больше внимания моим чувствам в дальнейшем."


    if mas_apology_reason:

        $ persistent._mas_apology_reason_use_db[mas_apology_reason] = persistent._mas_apology_reason_use_db.get(mas_apology_reason,0) + 1

        if persistent._mas_apology_reason_use_db[mas_apology_reason] == 1:

            $ mas_gainAffection(modifier=0.2)
        elif persistent._mas_apology_reason_use_db[mas_apology_reason] == 2:

            $ mas_gainAffection(modifier=0.1)




    $ mas_apology_reason = None
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_bad_nickname",
            prompt="...за то, что обзывал тебя плохими словами.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_bad_nickname:
    $ ev = mas_getEV('mas_apology_bad_nickname')
    if ev.shown_count == 0:
        $ mas_gainAffection(modifier=0.2)
        m 1eka "Спасибо, что извинил[mas_gender_sya] за то имя, которое пытал[mas_gender_sya] дать мне."
        $ MAS.MonikaElastic()
        m 2ekd "Мне было очень больно, [player]..."
        $ MAS.MonikaElastic()
        m 2dsc "Я принимаю твоё извинение, но, пожалуйста, не делай так больше. Ладно?"
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    elif ev.shown_count == 1:
        $ mas_gainAffection(modifier=0.1)
        m 2dsc "Не могу поверить в то, что ты {i}снова{/i} это сделал[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 2dkd "Даже после того, как я дала тебе второй шанс."
        $ MAS.MonikaElastic()
        m 2tkc "Я разочаровалась в тебе, [player]."
        $ MAS.MonikaElastic()
        m 2tfc "Не делай так больше."
        $ mas_unlockEVL("monika_affection_nickname", "EVE")
    else:


        m 2wfc "[player]!"
        $ MAS.MonikaElastic()
        m 2wfd "Как ты мог?"
        $ MAS.MonikaElastic()
        m 2dfc "Я надеялась, что ты дашь мне хорошее прозвище, дабы сделать меня более уникальной, но ты решил отплатить мне чёрной неблагодарностью..."
        $ MAS.MonikaElastic()
        m "Похоже, я не могу доверить тебе такое право."
        $ MAS.MonikaElastic()
        m ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
        $ MAS.MonikaElastic()
        m 2rfc "Я бы приняла твоё извинение, [player], но я сомневаюсь, что ты сказал это на полном серьёзе."

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
