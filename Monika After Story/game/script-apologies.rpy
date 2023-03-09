#Create an apology db for storing our times
#Stores the event label as a key, its corresponding data is a tuple where:
#   [0] -> timedelta defined by: current total playtime + apology_active_expiry time
#   [1] -> datetime.date defined by the date the apology was added + apology_overall_expiry time
default persistent._mas_apology_time_db = {}

#Create a generic apology db. We'll want to know how many times the player has apologized for mas_apology_reason
#Allows us the ability to apply diminishing returns on affection for repeated use of the same apology
#This db here simply stores the integer corresponding to apology reason as a key,
#corresponding int value is the amt of times it was used
default persistent._mas_apology_reason_use_db = {}

init -10 python in mas_apology:
    apology_db = {}
    # Event database for apologies


init python:
    def mas_checkApologies():
        #Let's not do extra work
        if len(persistent._mas_apology_time_db) == 0:
            return
        
        #Calculate the current total playtime to compare...
        current_total_playtime = persistent.sessions['total_playtime'] + mas_getSessionLength()
        
        _today = datetime.date.today()
        #Iter thru the stuffs in the apology time tb
        for ev_label in persistent._mas_apology_time_db.keys():
            if current_total_playtime >= persistent._mas_apology_time_db[ev_label][0] or _today >= persistent._mas_apology_time_db[ev_label][1]:
                #Pop the ev_label from the time db and lock the event label. You just lost your chance
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

    #Firstly, let's check if there's an apology reason for the prompt
    #NOTE: When adding more apology reasons, add a reason the player would say sorry for here (corresponding to the same #as the apology reason)
    $ player_apology_reasons = {
        0: "из-за кое-чего.", 
        1: "то, что сказал, что хочу расстаться.",
        2: "то, что пошутил насчёт того, что у меня другая девушка.",
        3: "то, что назвал тебя убийцей.",
        4: "то, что закрывал игру вместе с тобой.",
        5: "то, что входил в твою комнату без стука.",
        6: "то, что пропустил Рождество.",
        7: "то, что забыл про твой день рождения.",
        8: "то, что не провёл время вместе с тобой в твой же день рождения.",
        9: "то, что игра вылетела.",
        10: "то, что игра вылетает.",
        11: "то, что не послушал мою речь.",
        12: "то, что называл тебя злой.",
        13: "то, что не отвечал тебе серьёзно."
    }

    #Set the prompt for this...
    if len(persistent._mas_apology_time_db) > 0:
        #If there's a non-generic apology reason pending we use "for something else."
        $ mas_setEVLPropValues(
            "mas_apology_generic",
            prompt="...за {0}".format(player_apology_reasons.get(mas_apology_reason,player_apology_reasons[0]))
        )
    else:
        #Otherwise, we use "for something." if reason isn't 0
        if mas_apology_reason == 0:
            $ mas_setEVLPropValues("mas_apology_generic", prompt="......за что-то.")
        else:
            #We set this to an apology reason if it's valid
            $ mas_setEVLPropValues(
                "mas_apology_generic",
                prompt="...за {0}".format(player_apology_reasons.get(mas_apology_reason,"что-то."))
            )

    #Then we delete this since we're not going to need it again until we come back here, where it's created again.
    #No need to store excess memory
    $ del player_apology_reasons

    #Now we run through our apology db and find what's unlocked
    python:
        apologylist = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in store.mas_apology.apology_db.iteritems()
            if ev.unlocked and (ev.prompt != "за..." and ev.prompt != "из-за кое-чего другого...")
        ]

        #Now we add the generic if there's no prompt attached
        generic_ev = mas_getEV('mas_apology_generic')

        if generic_ev.prompt == "за..." or generic_ev.prompt == "из-за кое-чего другого...":
            apologylist.append((generic_ev.prompt, generic_ev.eventlabel, False, False))

        #The back button
        return_prompt_back = ("Забудь.", False, False, False, 20)

    #Display our scrollable
    show monika at t21
    call screen mas_gen_scrollable_menu(apologylist, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, return_prompt_back)

    #Make sure we don't lose this value
    $ apology =_return

    #Handle backing out
    if not apology:
        if mas_apology_reason is not None or len(persistent._mas_apology_time_db) > 0:
            show monika at t11
            if mas_isMoniAff(higher=True):
                m 1ekd "[player], если ты чувствуешь себя виноватым..."
                m 1eka "Тебе не нужно бояться извиняться, в конце концов, мы все совершаем ошибки."
                m 3eka "Мы просто должны принять то, что произошло, учиться на своих ошибках и двигаться дальше вместе. Ладно?"
            elif mas_isMoniNormal(higher=True):
                m 1eka "[player]..."
                m "Если ты хочешь извиниться, давай. Для меня это много значило бы, если бы ты это сделал."
            elif mas_isMoniUpset():
                m 2rkc "Ох..."
                m "Я..."
                $ _history_list.pop()
                m 2dkc "Забудь."
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
                    m 6rkc "Тебе есть что сказать, [player]?"
        return "prompt"

    show monika at t11
    #Call our apology label
    #NOTE: mas_setApologyReason() ensures that this label exists
    call expression apology

    #Increment the shown count
    $ mas_getEV(apology).shown_count += 1

    #Lock the apology label if it's not the generic
    if apology != "mas_apology_generic":
        $ store.mas_lockEVL(apology, 'APL')

    #Pop that apology from the time db
    if apology in persistent._mas_apology_time_db: #sanity check
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
    #dict of all generic apologies
    #Note, if a custom apology is needed, add it here and reference the apology reason by the integer associated.
    $ mas_apology_reason_db = {
        0: "",
        1: "то, что ты сказал, что хочешь расстаться. Я знала, ты говорил не всерьёз...",
        2: "то, что пошутил насчёт того, что у тебя другая девушка. Ты меня до смерти напугал!",
        3: "то, что назвал меня убийцей. Надеюсь, ты не видишь меня такой...",
        4: "то, что внезапно закрывал игру.",
        5: "то, что входил в мою комнату без стука.",
        6: "то, что пропустил Рождество.",
        7: "то, что забыл про мой день рождения.",
        8: "то, что не провёл время вместе со мной в мой же день рождения.",
        9: "то, что игра вылетела. Я понимаю, такое иногда происходит, но не волнуйся, со мной всё хорошо!",
        10: "то, что игра вылетает. Это было очень страшно, но я рада, что ты вернулся ко мне и всё изменилось к лучшему.",
        11: "то, что не послушал мою речь. Я очень старалась.",
        12: "то, что называл меня злой. Я знаю, что ты правда так не считаешь.",
        13: "то, что не воспринимал мои вопросы всерьёз. Я знаю, что с этого момента ты будешь честен со мной."
    }

    #If there's no reason to apologize
    if mas_apology_reason is None and len(persistent._mas_apology_time_db) == 0:
        if mas_isMoniBroken():
            m 1ekc "...{w=1}Оу."
            m 2dsc ".{w=2}.{w=2}."
            m "Ладно."
        elif mas_isMoniDis():
            m 2dfd "{i}*вздох*{/i}"
            m 2dsd "Я надеюсь, что это не какая-то шутка или трюк, [player]."
            m 2dsc "..."
            m 1eka "Спасибо за извинения."
            m 2ekc "Но, пожалуйста, постарайся быть более внимательным к моим чувствам."
            m 2dkd "Прошу."
        elif mas_isMoniUpset():
            m 1eka "Спасибо, [player]."
            m 1rksdlc "Я знаю, что между нами не всё хорошо, но я знаю, что ты всё ещё хороший человек."
            m 1ekc "Так не мог бы ты быть немного внимательнее к моим чувствам?"
            m 1ekd "Пожалуйста?"
        else:
            m 1ekd "Что-то случилось?"
            m 2ekc "Не вижу повода для извинений."
            m 1dsc "..."
            m 1eub "Как бы то ни было, спасибо за извинения."
            m 1eua "Что бы это ни было, я знаю, что ты делаешь всё возможное, чтобы всё исправить."
            m 1hub "За это я и люблю тебя, [player]!"
            $ mas_ILY()

    #She knows what you are apologizing for
    elif mas_apology_reason_db.get(mas_apology_reason, False):
        #Set apology_reason
        $ apology_reason = mas_apology_reason_db.get(mas_apology_reason,mas_apology_reason_db[0])

        m 1eka "Спасибо, что извинился за [apology_reason]"
        m "Извинения приняты, [player]. Это многое для меня значит."

    #She knows that you've got something else to apologize for, and wants you to own up
    elif len(persistent._mas_apology_time_db) > 0:
        m 2tfc "[player], если тебе есть за что извиняться — пожалуйста, говори."
        m 2rfc "Для меня это значило бы гораздо больше, если бы ты просто признался в том, что сделал."

    #She knows there's a reason for your apology but won't comment on it
    else:
        #Since this 'reason' technically varies, we don't really have a choice as we therefore can't add 0 to the db
        #So recover a tiny bit of affection
        $ mas_gainAffection(modifier=0.1)
        m 2tkd "Это не смешно, [player]."
        m 2dkd "Пожалуйста, будь более внимателен к моим чувствам в будущем."

    #We only want this for actual apology reasons. Not the 0 case or the None case.
    if mas_apology_reason:
        #Update the apology_reason count db (if not none)
        $ persistent._mas_apology_reason_use_db[mas_apology_reason] = persistent._mas_apology_reason_use_db.get(mas_apology_reason,0) + 1

        if persistent._mas_apology_reason_use_db[mas_apology_reason] == 1:
            #Restore a little bit of affection
            $ mas_gainAffection(modifier=0.2)
        elif persistent._mas_apology_reason_use_db[mas_apology_reason] == 2:
            #Restore a little less affection
            $ mas_gainAffection(modifier=0.1)

        #Otherwise we recover no affection.

    #Reset the apology reason
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
        m 1eka "Спасибо за то, что извинился за то прозвище."
        m 2ekd "Это очень больно, [player]..."
        m 2dsc "Извинения приняты. Но, пожалуйста, не делай так больше. Ладно?"
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    elif ev.shown_count == 1:
        $ mas_gainAffection(modifier=0.1)
        m 2dsc "Не могу поверить, что ты сделал это {i}снова{/i}."
        m 2dkd "Даже после того, как я дала тебе второй шанс."
        m 2tkc "Я разочарована, [player]."
        m 2tfc "Даже не думай сделать это снова."
        $ mas_unlockEVL("monika_affection_nickname", "EVE")

    else:
        #No recovery here. You asked for it.
        m 2wfc "[player]!"
        m 2wfd "Не могу поверить..."
        m 2dfc "Я надеялась, что ты дашь мне хорошее прозвище... Оно сделало бы меня более уникальной, но ты просто швырнул его мне в лицо..."
        m "Зря я доверилась тебе."
        m ".{w=0.5}.{w=0.5}.{nw}"
        m 2rfc "Извинения приняты, [player], но я не думаю, что они искренни."

    return
