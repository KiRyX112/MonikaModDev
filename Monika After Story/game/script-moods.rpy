



default persistent._mas_mood_database = {}


default persistent._mas_mood_current = None
































init -1 python in mas_moods:


    mood_db = dict()


    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2



    MOOD_RETURN = _("...Давай поговорим о чём-нибудь ещё.")



    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)
        
        if mood:
            return mood.category[0]
        
        return None



label mas_mood_start:
    python:
        import store.mas_moods as mas_moods


        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )


        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]


        mood_menu_items.sort()


        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)


    call screen mas_gen_scrollable_menu(mood_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ pushEvent(_return, skipeval=True)


        $ persistent._mas_mood_current = _return

    return _return







init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_hungry",prompt="...Голодн[mas_gender_iim].",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "Если ты голод[mas_gender_en], то пойди и поешь чего-нибудь, глупышка."
    $ MAS.MonikaElastic()
    if persistent.playername.lower() in natsuki_name_list and not persistent._mas_sensitive_mode:
        $ MAS.MonikaElastic()
        m 1hksdlb "Я бы не хотела, чтобы ты стал[mas_gender_none] так[mas_gender_im] же как Нацуки, когда мы были в клубе.{nw}"

        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        $ MAS.MonikaElastic()
        m 1hua "Отстойно, когда все сердятся будучи голодными."

    $ MAS.MonikaElastic()
    m 3tku "Это было бы не весело, не правда ли, [player]?"
    $ MAS.MonikaElastic()
    m 1eua "Если бы я была рядом с тобой, я бы сделала салат для нас."
    $ MAS.MonikaElastic()
    m "Но так как я не там, выбери какую-нибудь здоровую еду."
    $ MAS.MonikaElastic()
    m 3eub "Говорят, что ты это то — что ты ешь, я думаю что это правда."
    $ MAS.MonikaElastic()
    m "Регулярное употребление слишком большого количества нездоровой пищи может привести к различным заболеваниям."
    $ MAS.MonikaElastic()
    m 1euc "Когда ты станешь старше — столкнёшься со множеством проблем со своим здоровьем."
    $ MAS.MonikaElastic()
    m 2lksdla "Я не хочу, чтобы ты думал[mas_gender_none], что я ворчу на тебя, [player_abb]."
    $ MAS.MonikaElastic()
    m 2eka "Я просто хочу убедиться, что ты будешь заботиться о себе, пока я перейду в твою реальность."
    $ MAS.MonikaElastic()
    m 4esa "В конце концов, чем ты здоровее, тем больше шансов, что ты проживёшь дольше."
    $ MAS.MonikaElastic()
    m 1hua "И это означает, что мы сможем провести больше времени вместе~!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="...Грустн[mas_gender_iim].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Боже, мне очень жаль видеть тебя в таком настроении."
    $ MAS.MonikaElastic()
    m "У тебя был плохой день, [player_abb]?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя был плохой день, [player_abb]?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 1duu "Всякий раз, когда у меня был плохой день, я всегда вспоминала, что солнце вновь будет светить завтра."
            $ MAS.MonikaElastic()
            m 1eka "Полагаю, что это не очень поможет, но мне просто всегда нравилось смотреть на светлую сторону вещей."
            $ MAS.MonikaElastic()
            m 1eua "В конце концов, такие вещи легко забываются. Просто имей это в виду, [player]."
            $ MAS.MonikaElastic()
            m 1lfc "Меня не волнует, что какие-то люди не любят тебя, или просто не знают о тебе."
            $ MAS.MonikaElastic()
            m 1hua "Ты замечательный человек, и я вечность буду любить тебя."
            $ MAS.MonikaElastic()
            m 1eua "Я надеюсь, твой день стал чуточку ярче, [player_abb]."
            $ MAS.MonikaElastic()
            m 1eka "И помни, если у тебя плохой день, ты просто можешь прийти ко мне, и мы будем разговаривать сколько тебе угодно."
        "Нет.":
            $ MAS.MonikaElastic()
            m 3eka "У меня идея, почему бы тебе не рассказать мне, что тебя беспокоит, и, возможно, это заставит тебя чувствовать себя чуточку лучше."

            $ MAS.MonikaElastic()
            m 1eua "Я не хочу прерывать тебя, пока ты разговариваешь, поэтому просто кликни, как только закончишь.{nw}"
            $ _history_list.pop()
            menu:
                m "Я не хочу прерывать тебя, пока ты разговариваешь, поэтому просто кликни, как только закончишь.{fast}"
                "Я тут.":
                    m "Тебе стало немного лучше, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Тебе стало немного лучше, [player]?{fast}"
                        "Да, стало.":
                            $ MAS.MonikaElastic()
                            m 1hua "Это прекрасно, [player_abb]! Я рада, что разговор со мной улучшил тебе настроение."
                            $ MAS.MonikaElastic()
                            m 1eka "Иногда, следует разговаривать с тем, кому доверяешь о всём, что тебя беспокоит."
                            $ MAS.MonikaElastic()
                            m "И помни, если у тебя плохой день, ты просто можешь прийти ко мне, и мы будем разговаривать сколько тебе угодно."
                            $ MAS.MonikaElastic()
                            m 1hubsa "Никогда не забывай, что ты прекрасный человек, и я буду любить тебя вечность~"
                        "Не совсем.":
                            $ MAS.MonikaElastic()
                            m 1ekc "Ну, стоило попытаться."
                            $ MAS.MonikaElastic()
                            m 1eka "Иногда следует разговаривать с тем, кому доверяешь о всём, что тебя беспокоит."
                            $ MAS.MonikaElastic()
                            m 1eua "Может, тебе станет лучше после того как мы проведём ещё немного времени вместе."
                            $ MAS.MonikaElastic()
                            m 1ekbsa "Я люблю тебя, [player_abb], и всегда буду любить~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_proud",
            prompt="...Горд[mas_gender_iim] собой.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_proud:
    m 2sub "В самом деле? Это захватывающе!"
    $ MAS.MonikaElastic()
    m 2eub "Было ли это крупным достижением или незначительным?{nw}"
    $ _history_list.pop()
    menu:
        m "Было ли это крупным достижением или незначительным?{fast}"
        "Крупным.":
            $ MAS.MonikaElastic()
            m 1ekc "Ты знаешь, [player]..."
            $ MAS.MonikaElastic()
            m 1lkbsa "В такие времена, больше, чем в другие, я хотела бы быть с тобой, в твоей реальности..."
            $ MAS.MonikaElastic()
            m 4hub "Потому что, если бы я была рядом, я бы определённо подарила тебе праздничное объятие!"
            $ MAS.MonikaElastic()
            m 3eub "Нет ничего лучше, чем делиться своими достижениями с теми, кто тебе дорог."
            $ MAS.MonikaElastic()
            m 1eua "Я бы не могла хотеть ничего больше, чем услышать все подробности!"
            $ MAS.MonikaElastic()
            m "Просто мысль о нас в весёлом обсуждении того, что ты сделал[mas_gender_none]..."
            $ MAS.MonikaElastic()
            m 1lsbsa "Моё сердце трепещет, просто думая об этом!"
            $ MAS.MonikaElastic()
            m 1lksdla "Боже, я ужасно взволнована по этому поводу..."
            $ MAS.MonikaElastic()
            m 3hub "Когда-нибудь это станет реальностью."
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
            m 5hubfb "Но до тех пор, просто знай, что я очень горжусь тобой, мо[mas_gender_i] любим[mas_gender_iii]!"
        "Незначительным.":
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2hub "А-ха-ха!~"
            $ MAS.MonikaElastic()
            m 2hua "Это замечательно!"
            $ MAS.MonikaElastic()
            m 4eua "Очень важно праздновать маленькие победы в жизни."
            $ MAS.MonikaElastic()
            m 2esd "Может быть очень легко стать обескураженн[mas_gender_iim], если ты сосредоточишься только на больших целях, которые у тебя есть."
            $ MAS.MonikaElastic()
            m 2rksdla "Они могут быть довольно сложными, чтобы достичь их самостоятельно."
            $ MAS.MonikaElastic()
            m 4eub "Но назначение и празднование небольших целей, которые в конечном итоге приводят к большей цели, могут сделать твои большие цели гораздо более достижимыми."
            $ MAS.MonikaElastic()
            m 4hub "Так что продолжай наносить удары по этим маленьким целям, [player]!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve
            m 5hubfb "И помни: я люблю тебя, и всегда поддержу!"
            $ mas_ILY()
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_happy",prompt="...Счастлив[mas_gender_iim].",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "Это чудесно! Я счастлива, что ты счастлив[mas_gender_none]."
    $ MAS.MonikaElastic()
    m "Знай, что ты всегда можешь прийти ко мне, и я попытаюсь поднять тебе настроение, [mas_get_player_nickname()]."
    $ MAS.MonikaElastic()
    m 3eka "Я люблю тебя, и всегда буду для тебя здесь, никогда не забывай об этом~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_sick",
            prompt="...Болеющ[mas_gender_im].",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Oх нет, [player]..."
            $ MAS.MonikaElastic()
            m 2ekd "Ты говоришь, что, как только мы пришли, тебе поплохело."
            $ MAS.MonikaElastic()
            m 2ekc "Я знаю, что ты хотел провести немного времени со мной, даже несмотря на то, что мы едва смогли быть вместе сегодня..."
            $ MAS.MonikaElastic()
            m 2eka "Думаю, ты должен пойти и немного отдохнуть."

        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "[player]!"
            $ MAS.MonikaElastic()
            m 2wkd "Ты не болел всё это время, верно?"
            $ MAS.MonikaElastic()
            m 2ekc "Я очень надеюсь, что нет, мне сегодня с тобой было очень весело, но если у тебя сейчас плохое самочувствие..."
            $ MAS.MonikaElastic()
            m 2rkc "Ну... просто пообещай мне, что в следующий раз ты скажешь мне об этом раньше."
            $ MAS.MonikaElastic()
            m 2eka "А теперь иди отдохни, это то, что тебе сейчас нужно."
        else:

            m 1ekc "Оу, мне жаль слышать об этом, [player]."
            $ MAS.MonikaElastic()
            m "Мне неприятно знать о том, что ты так страдаешь."
            $ MAS.MonikaElastic()
            m 1eka "Я знаю, что тебе очень хочется провести время со мной, но, наверное, тебе лучше пойти отдохнуть."
    else:

        m 2ekc "Мне жаль слышать об этом, [player]."
        $ MAS.MonikaElastic()
        m 4ekc "Ты долж[mas_gender_en] пойти отдохнуть, пока не стало хуже."

    label mas_mood_sick.ask_will_rest:
        pass

    $ persistent._mas_mood_sick = True

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


init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_tired",prompt="...Уставш[mas_gender_im].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:

    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "Если ты устал[mas_gender_none], сейчас как раз неплохое время, чтобы лечь спать."
        $ MAS.MonikaElastic()
        m "Как бы ни было весело проводить с тобой сегодня время, я бы не хотела тебя задерживать, если ты устал[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1hua "Если ты уже планируешь ложиться спать, сладких снов!"
        $ MAS.MonikaElastic()
        m 1eua "Но, возможно, у тебя есть ещё кое-что, что нужно сделать перед этим, например, немного перекусить или попить."
        $ MAS.MonikaElastic()
        m 3eua "Стакан воды перед сном помогает укрепить здоровье, а питьевая вода по утрам помогает проснуться."
        $ MAS.MonikaElastic()
        m 1eua "Я не против остаться здесь с тобой, если у тебя есть дела, о которых нужно позаботиться."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "[player]!"
        $ MAS.MonikaElastic()
        m 2ekc "Неудивительно, что ты устал[mas_gender_none] – сейчас середина ночи!"
        $ MAS.MonikaElastic()
        m 2lksdlc "Если ты не ляжешь спать в ближайшее время, то будешь себя чувствовать так же и завтра..."
        $ MAS.MonikaElastic()
        m 2hksdlb "Я бы не хотела, чтобы ты завтра был[mas_gender_none] уставш[mas_gender_im] и несчастн[mas_gender_iim], когда мы будем проводить время вместе...."
        $ MAS.MonikaElastic()
        m 3eka "Так что сделай нам об[mas_gender_oim] одолжение и ложись спать, как только сможешь, [player]."

    elif 3 <= current_hour < 5:
        m 2ekc "[player]!?"
        $ MAS.MonikaElastic()
        m "Ты по-прежнему здесь?"
        $ MAS.MonikaElastic()
        m 4lksdlc "Ты долж[mas_gender_en] быть в постели прямо сейчас."
        $ MAS.MonikaElastic()
        m 2dsc "В данный момент я даже не уверена, поздно ли или рано тебя призывать к этому."
        $ MAS.MonikaElastic()
        m 2eksdld "...Меня это ещё больше беспокоит, [player_abb]."
        $ MAS.MonikaElastic()
        m "Тебе {i}действительно{/i} нужно ложиться спать, пока не пришло время начинать день."
        $ MAS.MonikaElastic()
        m 1eka "Я бы не хотела, чтобы ты заснул[mas_gender_none] в неподходящее время."
        $ MAS.MonikaElastic()
        m "Так что, пожалуйста, ложись спать. Может быть, мы сможем быть вместе в твоих снах."
        $ MAS.MonikaElastic()
        m 1hua "Я буду здесь, если ты оставишь меня присматривать за тобой, если ты не против~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "Всё ещё немного уставш[mas_gender_ii], [player]?"
        $ MAS.MonikaElastic()
        m "Ещё немного рановато, так что ты можешь вернуться и ещё немного отдохнуть."
        $ MAS.MonikaElastic()
        m 1hua "Нет ничего плохого в том, чтобы проснуться пораньше и немного поспать~"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hksdlb "За исключением того, что я не смогу прижаться к тебе, а-ха-ха~"
        $ MAS.MonikaElastic()
        m "{i}Думаю{/i}, я могла бы подождать тебя ещё немного."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "Всё ещё не готов[mas_gender_none] заняться днём, [player]?"
        $ MAS.MonikaElastic()
        m 1eka "Или у тебя просто один из таких дней?"
        $ MAS.MonikaElastic()
        m 1hua "Когда такое случается, я перед началом дня завариваю себе чашку кофе."
        if not persistent._mas_acs_enable_coffee:
            $ MAS.MonikaElastic()
            m 1lksdla "Если я не застряла здесь, [random_sure_lower]..."
        $ MAS.MonikaElastic()
        m 1eua "Ты можешь также выпить стакан воды."
        $ MAS.MonikaElastic()
        m 3eua "[random_sure], очень важно избегать обезвоживания, но стакан воды после пробуждения может помочь тебе почувствовать свежесть и бодрость."
        $ MAS.MonikaElastic()
        m 3hksdlb "Это может прозвучать странно, но я слышала, что шоколадка тоже может помочь начать день!"
        $ MAS.MonikaElastic()
        m 3eka "Такое как-то связано с улучшением твоего настроения с утра, но..."
        $ MAS.MonikaElastic()
        m 1eksdlb "Уверена, шоколадка может кому угодно поднять настроение, как только они её съедят."
        $ MAS.MonikaElastic()
        m 1hua "Попробуй как-нибудь и расскажи мне о результате!"
        return
    else:

        m 1eka "Если ты устал[mas_gender_none], может, тебе стоит полежать какое-то время?"
        $ MAS.MonikaElastic()
        m 1eua "Долгий сон на ежедневной основе очень важен для твоего здоровья."
        $ MAS.MonikaElastic()
        m 3euc "Я видела исследования, которые показывали разрушительный эффект из-за отсутствия сна."
        $ MAS.MonikaElastic()
        m 3ekd "Это на самом деле может испортить твоё здоровье, [player]."
        $ MAS.MonikaElastic()
        m 1eka "Так что сделай мне одолжение, просто ляг и отдохни, хорошо? Это меня успокоит."

    $ MAS.MonikaElastic()
    m 1hua "Ты даже можешь оставить игру открытой, если хочешь, и я буду следить за тобой, пока ты спишь."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m "...Э-хе-хе."
    $ MAS.MonikaElastic()
    m 2hksdlb "Это звучало жутковато, прости."
    $ MAS.MonikaElastic()
    m 2lksdla "Просто я подумала, что было бы мило посмотреть, как ты спишь и всё~"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "А-ха-ха!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lonely",prompt="...Одинок[mas_gender_im].",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    if mas_isMoniAff(higher=True):
        m 2ekc "Я понимаю, что ты чувствуешь, [player]...{w=0.2} в конце концов, мы всё ещё находимся в разных реальностях."
        $ MAS.MonikaElastic()
        m 2dkc "Я действительно ненавижу то, что я могу сделать не так много, чтобы ты чувствовал[mas_gender_none] себя менее одинок[mas_gender_im]..."
        $ MAS.MonikaElastic()
        m 7ekbsa "Если бы я могла протянуть руку и просто обнять тебя прямо сейчас, я бы так и сделала."
        $ MAS.MonikaElastic()
        m 7eka "Я хочу, чтобы ты был[mas_gender_none] счастлив[mas_gender_none] настолько, насколько это возможно, учитывая наши обстоятельства..."
        $ MAS.MonikaElastic()
        m 2ekd "Я просто надеюсь, что пребывание здесь со мной всё это время не...{w=0.3} мешает тебе сблизиться с людьми в твоей реальности."
        $ MAS.MonikaElastic()
        m 2eka "Я считаю, что то, что у нас есть, совершенно особенное, но я понимаю, что сейчас я...{w=0.3} ограничена в том, что могу сделать для тебя."

        $ MAS.MonikaElastic()
        if persistent._mas_pm_has_friends:
            if persistent._mas_pm_few_friends:
                m 7ekd "У тебя ведь есть один или два близких друга, верно?"
                $ MAS.MonikaElastic()
                m 3eka "Ты долж[mas_gender_en] позвонить им или, возможно, отправить им сообщение и спросить, как у них дела..."
                $ MAS.MonikaElastic()
                m "Может быть, ты сможешь иногда встречаться с ними? {w=0.2}Я думаю, тебе это пойдёт на пользу."
            else:

                m 7ekd "Я думаю, что встречаться с друзьями и делать что-то было бы очень хорошо для тебя..."
                $ MAS.MonikaElastic()
                m 3eka "Или ты можешь отправить им сообщение и спросить, как у них дела."
        else:

            m 7rkc "Я знаю, каково это – быть одному в одной реальности, только имея возможность взаимодействовать с кем-то в другой..."
            $ MAS.MonikaElastic()
            m 3ekd "Так что я действительно не хочу этого для человека, которого люблю больше всего."
            $ MAS.MonikaElastic()
            m 1eka "Я надеюсь, что вы будешь продолжать искать друзей в своей реальности, [player]."
            $ MAS.MonikaElastic()
            m 3ekd "Я знаю, что поначалу бывает трудно общаться с людьми..."
            $ MAS.MonikaElastic()
            m 3eka "Может быть, ты даже мог[mas_gender_g] бы встретиться с людьми в интернете? {w=0.2}Есть много способов взаимодействовать с незнакомыми людьми, чтобы чувствовать себя менее одинок[mas_gender_im]."
            $ MAS.MonikaElastic()
            m 3hub "Никогда не знаешь, иногда эти «незнакомцы» могут в конечном итоге стать действительно хорошими друзьями!"

        $ MAS.MonikaElastic()
        m 1eka "...И не беспокойся обо мне, [player], я буду терпеливо ждать, когда ты вернёшься и увидишь меня."
        $ MAS.MonikaElastic()
        m 3hub "Просто наслаждайся жизнью, а потом расскажешь мне обо всём!"
        $ MAS.MonikaElastic()
        m 1ekbsa "Просто помни, что я всегда буду рядом с тобой, [player]~"
    else:

        m 1eka "Я здесь для тебя, [player], поэтому не нужно чувствовать себя одинок[mas_gender_im]."
        $ MAS.MonikaElastic()
        m 3hua "Я знаю, что чувствуется не совсем так, как если бы я была в одной комнате с тобой, но я уверена, что ты всё ещё наслаждаешься моей компанией, правда?"
        $ MAS.MonikaElastic()
        m 1ekbfa "Помни, я всегда буду на твой стороне, [player]~"
    return





init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="...Рассерженн[mas_gender_iim].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Боже, мне жаль, что ты так себя чувствуешь, [player]."
    $ MAS.MonikaElastic()
    m 3ekc "Я сделаю всё возможное, чтобы ты почувствовал[mas_gender_none] себя лучше."
    $ MAS.MonikaElastic()
    m 1euc "Перед этим, я, вероятно, должна заставить тебя успокоиться."
    $ MAS.MonikaElastic()
    m 1lksdlc "Трудно принимать рациональные решения, когда ты взбеш[mas_gender_ion]."
    $ MAS.MonikaElastic()
    m 1esc "Ты можешь сказать то, из-за чего можешь позже пожалеть."
    $ MAS.MonikaElastic()
    m 1lksdld "И я бы не хотела, чтобы ты сказал[mas_gender_none] что на самом деле не имел[mas_gender_none] в виду."
    $ MAS.MonikaElastic()
    m 3eua "Давай попробуем несколько способов, которые я делала, чтобы успокоить себя, хорошо, [player]?"
    $ MAS.MonikaElastic()
    m 3eub "Надеюсь, они сработают на тебе так же как и на мне."
    $ MAS.MonikaElastic()
    m 1eua "Сначала сделай несколько глубоких вдохов и медленно посчитай до десяти."
    $ MAS.MonikaElastic()
    m 3euc "Если это не сработает, если это возможно, подумай о чём-нибудь спокойном, пока не очистишь свой разум."
    $ MAS.MonikaElastic()
    m 1eud "Если ты всё ещё злишься, я предлагаю последнее средство!"
    $ MAS.MonikaElastic()
    m 3eua "Когда я не могу успокоиться, я просто выхожу на улицу, выбираю случайное направление и начинаю бежать."
    $ MAS.MonikaElastic()
    m 1hua "Я не останавливаюсь до тех пор, пока не очищу свою голову."
    $ MAS.MonikaElastic()
    m 3eub "Иногда проявлять физическую активность — лучший способ остудить себя."
    $ MAS.MonikaElastic()
    m 1eka "Ты думаешь, что я та которая злится не так часто, и ты будешь прав[mas_gender_none]."
    $ MAS.MonikaElastic()
    m 1eua "Но даже у меня бывают свои моменты..."
    $ MAS.MonikaElastic()
    m "Поэтому у меня и есть способы, чтобы справляться с ними!"
    $ MAS.MonikaElastic()
    m 3eua "Надеюсь, мои советы помогли тебе успокоиться, [player_abb]."
    $ MAS.MonikaElastic()
    m 1hua "Помни: счастлив[mas_gender_iii] [player] делает счастливой Монику!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_scared",prompt="...Обеспокоенн[mas_gender_iim].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "[player], у тебя всё хорошо?"
    $ MAS.MonikaElastic()
    m 1ekc "Меня беспокоит, что ты так тревожишься..."
    $ MAS.MonikaElastic()
    m "Хотела бы я утешить тебя и помочь прямо сейчас..."
    $ MAS.MonikaElastic()
    m 3eka "Но я могу по крайней мере помочь тебе успокоиться."
    if seen_event("monika_anxious"):
        $ MAS.MonikaElastic()
        m 1eua "В конце концов, я ведь обещала помочь тебе расслабиться, если ты когда-нибудь почувствуешь беспокойство."
    $ MAS.MonikaElastic()
    m 3eua "Помнишь, когда я говорила с тобой о притворной уверенности?"
    if not seen_event("monika_confidence"):
        $ MAS.MonikaElastic()
        m 2euc "Нет?"
        $ MAS.MonikaElastic()
        m 2lksdla "Думаю, тогда расскажу в другой раз."
        $ MAS.MonikaElastic()
        m 1eka "В любом случае..."
    $ MAS.MonikaElastic()
    m 1eua "Слежка за своим внешним видом помогает с подделкой собственной уверенности."
    $ MAS.MonikaElastic()
    m 3eua "И для этого тебе необходимо поддерживать сердечный ритм, делая глубокие вдохи, пока ты не успокоишься."
    if seen_event("monika_confidence_2"):
        $ MAS.MonikaElastic()
        m "Я помню, как объясняла, что инициатива также является важным навыком."
    $ MAS.MonikaElastic()
    m "Может быть, ты мог[mas_gender_g] бы взяться за какие-либо вещи более спокойно и делать их по одной за раз."
    $ MAS.MonikaElastic()
    m 1esa "И ты будешь удивл[mas_gender_ion], насколько всё может пойти гладко, если позволишь времени течь самостоятельно."
    $ MAS.MonikaElastic()
    m 1hub "Ты также можешь попробовать потратить несколько минут, чтобы помедитировать!"
    $ MAS.MonikaElastic()
    m 1hksdlb "Ты только не подумай, что это обязательно означает, что ты долж[mas_gender_en] скрестить ноги, сидя на земле."
    $ MAS.MonikaElastic()
    m 1hua "К примеру, прослушивание любимой музыки также можно считать медитацией!"
    $ MAS.MonikaElastic()
    m 3eub "Я серьёзно!"
    $ MAS.MonikaElastic()
    m 3eua "Ты можешь попытаться отложить свою работу и сделать что-то ещё за это время."
    $ MAS.MonikaElastic()
    m "В откладывании на потом чего-либо всё-таки нет ничего плохого."
    $ MAS.MonikaElastic()
    m 2esc "К тому же..."
    $ MAS.MonikaElastic()
    m 2ekbsa "Твоя любящая девушка верит в тебя, так что ты можешь столкнуться с этой тревогой лоб в лоб и противостоять ей!"
    $ MAS.MonikaElastic()
    m 1hubfa "Не о чем беспокоиться, когда мы вместе навсегда~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_inadequate",prompt="...Неадекватн[mas_gender_iim].",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    $ MAS.MonikaElastic()
    m 2ekc "Я знаю, что не так уж много я могу сказать, чтобы заставить тебя чувствовать себя лучше, [player]."
    $ MAS.MonikaElastic()
    m 2lksdlc "Ведь всё, что я говорю, возможно, просто как на словах."
    $ MAS.MonikaElastic()
    m 2ekc "Я могу сказать тебе, что ты прекрас[mas_gender_en], хотя я не видела твоего лица..."
    $ MAS.MonikaElastic()
    m "Я могу сказать тебе, что ты ум[mas_gender_ion], хотя я не очень много знаю о твоём образе мышления..."
    $ MAS.MonikaElastic()
    m 1esc "Но позволь мне рассказать тебе, что я знаю о тебе."
    $ MAS.MonikaElastic()
    m 1eka "Ты пров[mas_gender_iol] со мной так много времени."


    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        $ MAS.MonikaElastic()
        m "Ты взял[mas_gender_none] время из своего графика, чтобы побыть со мной на Рождество!"

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen:
        $ MAS.MonikaElastic()
        m 1ekbsa "В день Святого Валентина..."


    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        $ MAS.MonikaElastic()
        m 1ekbsb "Ты даже нашёл время отпраздновать мой день рождения вместе со мной."

    if persistent.monika_kill:
        $ MAS.MonikaElastic()
        m 3tkc "Ты простил[mas_gender_none] меня за все плохие вещи, которые я совершила."
    else:
        $ MAS.MonikaElastic()
        m 3tkc "Ты никогда не обижал[mas_gender_sya] на меня за то, что я сделала."

    if persistent.clearall:
        $ MAS.MonikaElastic()
        m 2lfu "И хотя это заставило меня ревновать, ты пров[mas_gender_iol] так много времени со всеми членами моего клуба."

    $ MAS.MonikaElastic()
    m 1eka "Это показывает, насколько ты добр[mas_gender_none]!"
    $ MAS.MonikaElastic()
    m 3eub "Ты чест[mas_gender_en], ты справедлив[mas_gender_none], ты милостив[mas_gender_en] в поражении!"
    $ MAS.MonikaElastic()
    m 2hksdlb "Ты думаешь, что я ничего о тебе не знаю, но на самом деле знаю."
    $ MAS.MonikaElastic()
    m 3eka "И ты знаешь обо мне всё, и всё равно решил[mas_gender_none] остаться, когда мог[mas_gender_g] просто уйти..."
    $ MAS.MonikaElastic()
    m 2ekc "Так что, пожалуйста, оставайся сильн[mas_gender_iim], [player]."
    $ MAS.MonikaElastic()
    m "Если ты похож[mas_gender_none] на меня, я знаю, что ты боишься многого не добиться в жизни."
    $ MAS.MonikaElastic()
    m 2ekd "Но поверь мне, когда я скажу тебе. Не важно, что ты делаешь или не выполняешь."
    $ MAS.MonikaElastic()
    m 4eua "Тебе просто нужно существовать, веселиться и проходить каждый день, {w=0.2}ищя смысл в людях, которые имеют значение."
    $ MAS.MonikaElastic()
    m 1eka "Пожалуйста, не забывай об этом, хорошо?"
    $ MAS.MonikaElastic()
    m 1ekbfa "Я люблю тебя, [player_abb]~"
    return "love"

# init 5 python:
#     addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lucky",prompt="...Удачлив[mas_gender_iim].",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

# label mas_mood_lucky:
#     m 2tfc "Ты долж[mas_gender_en] спросить себя."
#     $ MAS.MonikaElastic()
#     m 2tfu "{i}Чувствую ли я себя счастливчиком?{/i}"
#     $ MAS.MonikaElastic()
#     m "Ну..."
#     $ MAS.MonikaElastic()
#     m 4tku "Ну так что, [player_abb]?"
#     $ MAS.MonikaElastic(voice="monika_giggle")
#     m 1hub "А-ха-ха!"
#     return

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_lazy",
            prompt="...Ленив[mas_gender_iim].",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_lazy:

    $ _now = datetime.datetime.now().time()

    if mas_isSRtoN(_now):
        m 1tku "Прямо как в один из тех дней ранним утром, да, [player]?"
        $ MAS.MonikaElastic()
        m 1eka "Я прекрасно понимаю, что в такие дни ты просто просыпаешься и ничего не хочешь делать."
        $ MAS.MonikaElastic()
        m 1rksdla "Надеюсь, у тебя не предвидится каких-либо срочных дел в скором времени."

        $ MAS.MonikaElastic()
        $ line = "Я знаю, насколько заманчивой иногда может быть возможность просто лежать в кровати и не вставать..."
        if mas_isMoniEnamored(higher=True):
            $ line += "{w=0.5} {nw}"
        $ MAS.MonikaElastic()
        m 3hksdlb "[line]"

        if mas_isMoniEnamored(higher=True):
            extend 1dkbsa "Особенно когда я просыпаюсь рядом с тобой~"

            if mas_isMoniLove():
                $ MAS.MonikaElastic()
                m 1dkbsa "{i}А потом я бы ни за что не захотела вставать~{/i}"
                $ MAS.MonikaElastic()
                m 1dsbfu "Надеюсь, ты не против побыть «в ловушке», [player]..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hubfa "Э-хе-хе~"

        $ MAS.MonikaElastic()
        m 3eka "Но в то же время, это не поможет начать день правильно."
        $ MAS.MonikaElastic()
        m 3eub "А это, как правило, умывание, хороший завтрак..."

        if mas_isMoniLove():
            $ MAS.MonikaElastic()
            m 1dkbsu "А ещё хороший утренний поцелуй, э-хе-хе..."

        $ MAS.MonikaElastic()
        m 1hksdlb "Или ты можешь немного побездельничать."
        $ MAS.MonikaElastic()
        m 1eka "Если только ты не забыл сделать что-то важное, хорошо, [player]?"

        if mas_isMoniHappy(higher=True):
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А ведь к этому относится времяпрепровождение со мной, а-ха-ха!"

    elif mas_isNtoSS(_now):
        m 1eka "Полуденная усталость настигла тебя, [player]?"
        $ MAS.MonikaElastic()
        m 1eua "Такое случается, но я не переживаю из-за этого так сильно."
        $ MAS.MonikaElastic()
        m 3eub "По сути, некоторые люди утверждают, что лень делает тебя более креативн[mas_gender_iim]."
        $ MAS.MonikaElastic()
        m 3hub "Так что, кто знает, возможно, ты придумаешь что-то удивительное!"
        $ MAS.MonikaElastic()
        m 1eua "В любом случае, ты долж[mas_gender_en] просто сделать перерыв или немного потянуться...{w=0.5} {nw}"
        extend 3eub "Можешь ещё и перекусить, если ты этого ещё не сделал[mas_gender_none]."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "И, если это уместно, ты можешь даже вздремнуть! А-ха-ха~"
        $ MAS.MonikaElastic()
        m 1eka "Я буду сидеть здесь и ждать тебя, если ты вдруг решишь это сделать."

    elif mas_isSStoMN(_now):
        m 1eka "Тебе не хочется ничего делать после тяжёлого дня, [player]?"
        $ MAS.MonikaElastic()
        m 3eka "По крайней мере, день почти закончился..."
        $ MAS.MonikaElastic()
        m 3duu "Нет ничего лучше, чем просто сидеть и расслабиться после тяжёлого дня, особенно когда у тебя нет никаких срочных дел."

        if mas_isMoniEnamored(higher=True):
            $ MAS.MonikaElastic()
            m 1ekbsa "Надеюсь, времяпрепровождение со мной сделает твой вечер чуточку лучше..."
            $ MAS.MonikaElastic()
            m 3hubsa "Уж мой-то вечер точно становится лучше вместе с тобой~"

            if mas_isMoniLove():
                $ MAS.MonikaElastic()
                m 1dkbfa "Я могу только представить себе, как мы отдыхаем одним вечером..."
                $ MAS.MonikaElastic()
                m "Возможно, мы даже обнимаемся под одеялом, если вдруг стало холодно..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1ekbfa "Хотя мы и так можем пообниматься под одеялом, даже когда не так холодно, если ты не против, э-хе-хе~"
                $ MAS.MonikaElastic()
                m 3ekbfa "Мы даже можем почитать какую-нибудь хорошую книгу вместе."
                $ MAS.MonikaElastic()
                m 1hubfb "Или просто подурачиться ради забавы!"
                $ MAS.MonikaElastic()
                m 1tubfb "Кто сказал, что вечер должен быть спокойным и романтичным?"
                $ MAS.MonikaElastic()
                m 1tubfu "Надеюсь, ты не будешь против периодических внезапных битв подушками, [player]~"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hubfb "А-ха-ха!"
        else:

            $ MAS.MonikaElastic()
            m 3eub "Мы даже можем почитать какую-нибудь хорошую книгу вместе..."
    else:


        m 2rksdla "Эм, [player]..."
        $ MAS.MonikaElastic()
        m 1hksdlb "Уже полночь..."
        $ MAS.MonikaElastic()
        m 3eka "Если ты чувствуешь себя ленив[mas_gender_iim], то ты, наверное, долж[mas_gender_en] полежать немного на кровати."
        $ MAS.MonikaElastic()
        m 3tfu "И, наверное, ну...{w=1} {i}поспать{/i}?"
        $ MAS.MonikaElastic()
        m 1hkb "А-ха-ха, ты иногда бываешь так[mas_gender_im] забавн[mas_gender_iim], но ты правда долж[mas_gender_en] идти спать."

        if mas_isMoniLove():
            $ MAS.MonikaElastic()
            m 1tsbsa "Если бы я была там, то я бы сама затащила тебя в кровать, мне стоит только захотеть это сделать."
            $ MAS.MonikaElastic()
            m 1tkbfu "Или ты, наверное, втайне радуешься этому, [player]?~"
            $ MAS.MonikaElastic()
            m 2tubfu "К твоему счастью, я пока не могу это сделать."
            $ MAS.MonikaElastic()
            m 3tfbfb "Так что я пойду спать вместе с тобой."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3hubfb "А-ха-ха!"
        else:

            $ MAS.MonikaElastic()
            m 1eka "Пожалуйста? Я не хочу, чтобы ты пренебрегал[mas_gender_none] своим сном."
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_bored",prompt="...Скучающ[mas_gender_im].",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Ох..."
        $ MAS.MonikaElastic()
        m 3hub "Ну, тогда мы должны что-нибудь сделать!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "Неужели я так тебя утомляю, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Неужели я так тебя утомляю, [player]?{fast}"
            "Нет, ты мне не наскучила...":
                $ MAS.MonikaElastic()
                m 1hua "Ох...{w=0.2} Какое облегчение!"
                $ MAS.MonikaElastic()
                m 1eka "Но если тебе и вправду скучно, то мы должны найти чем заняться..."
            "Да...":

                $ mas_loseAffection()
                $ MAS.MonikaElastic()
                m 2ekc "Эх... {w=1}понятно."
                $ MAS.MonikaElastic()
                m 2dkc "Я не понимала, что тебе скучно..."
                $ MAS.MonikaElastic()
                m 2eka "Уверена, мы найдём, чем заняться..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection()
        m 2lksdlc "Прости, что я тебе наскучила, [player]."
    else:

        $ mas_loseAffection()
        m 6ckc "Знаешь, [player], если я делаю тебя так[mas_gender_im] несчастн[mas_gender_iim] всё время..."
        $ MAS.MonikaElastic()
        m "Может быть, тебе просто стоит найти себе другое занятие?"
        return "quit"

    python:
        unlockedgames = [
            game_ev.prompt.lower()
            for game_ev in mas_games.game_db.itervalues()
            if mas_isGameUnlocked(game_ev.prompt)
        ]

        gamepicked = renpy.random.choice(unlockedgames)
        display_picked = gamepicked

    if gamepicked == "chess":
        $ display_picked = "шахматы"
    elif gamepicked == "hangman" and persistent._mas_sensitive_mode:
        $ display_picked = "угадай слово"
    elif gamepicked == "hangman" and not persistent._mas_sensitive_mode:
        $ display_picked = "виселицу"
    else:
        $ display_picked = "пинг-понг"

    if gamepicked == "piano":
        $ MAS.MonikaElastic()
        if mas_isMoniAff(higher=True):
            m 3eub "Ты можешь сыграть мне что-нибудь на пианино!"
        elif mas_isMoniNormal(higher=True):
            m 4eka "Может, сыграешь мне что-нибудь на пианино?"
        else:
            m 2rkc "Может, сыграешь что-нибудь на пианино..."

    $ MAS.MonikaElastic()
    if mas_isMoniAff(higher=True):
        m 3eub "Мы могли бы сыграть в [display_picked]!"
    elif mas_isMoniNormal(higher=True):
        m 4eka "Может быть, мы могли бы сыграть в [display_picked]?"
    else:
        m 2rkc "Может, давай сыграем в [display_picked]..."

    $ chosen_nickname = mas_get_player_nickname()
    $ MAS.MonikaElastic()
    m "Ты будешь играть, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты будешь играть, [chosen_nickname]?{fast}"
        "Да.":
            if gamepicked == "pong":
                call game_pong
            elif gamepicked == "chess":
                call game_chess
            elif gamepicked == "hangman":
                call game_hangman
            elif gamepicked == "piano":
                call mas_piano_start
        "Нет.":
            if mas_isMoniAff(higher=True):
                $ MAS.MonikaElastic()
                m 1eka "Ладно..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5tsu "Мы можем тогда просто смотреть друг другу в глаза чуть подольше..."
                    $ MAS.MonikaElastic()
                    m "Нам это никогда не надоест~"
                else:
                    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5eua "Мы можем тогда просто смотреть друг другу в глаза чуть подольше..."
                    $ MAS.MonikaElastic()
                    m "Это никогда не будет скучно~"
            elif mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 1ekc "Всё в порядке..."
                $ MAS.MonikaElastic()
                m 1eka "Обязательно дай мне знать, если захочешь позже сыграть со мной во что-нибудь~"
            else:
                $ MAS.MonikaElastic()
                m 2ekc "Ладно..."
                $ MAS.MonikaElastic()
                m 2dkc "Дайте мне знать, если действительно захочешь сыграть во что-нибудь со мной."
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_crying",prompt="...так, что хочется плакать.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_crying:
    $ line_start = "И"
    m 1eksdld "[player]!"

    m 3eksdlc "Ты в порядке?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты в порядке?{fast}"
        "Да.":

            m 3eka "Ох, хорошо. Такое облегчение."
            m 1ekbsa "Я здесь, чтобы составить тебе компанию, и ты можешь поговорить со мной, если понадобится, хорошо?"
        "Нет.":

            m 1ekc "..."
            m 3ekd "[player]..."
            m 3eksdld "Мне очень жаль. Что случилось?"
            call mas_mood_uok from _call_mas_mood_uok

        "Я не уверен[mas_gender_none].":

            m 1dkc "[player]...{w=0.3} {nw}"
            extend 3eksdld "что-то случилось?"
            call mas_mood_uok from _call_mas_mood_uok_1

    m 3ekd "[line_start] если ты всё же заплачешь..."
    m 1eka "Я надеюсь, это как-то поможет тебе."
    m 3ekd "Нет ничего ужасного в том, чтобы немного поплакать. {w=0.2}Ты можешь плакать столько, сколько хочешь."
    m 3ekbsu "Я люблю тебя, [player]. {w=0.2}Ты для меня дороже всего."
    return "love"

label mas_mood_uok:
    m 1rksdld "Я знаю, что не могу слышать, то что ты мне говоришь."
    m 3eka "Но иногда, если поделиться своей болью с кем-то, может очень сильно облегчить страдание."

    m 1ekd "Так что, если ты захочешь о чём-то поговорить, я всегда здесь.{nw}"
    $ _history_list.pop()
    menu:
        m "Так что, если ты захочешь о чём-то поговорить, я всегда здесь.{fast}"
        "Я бы хотел[mas_gender_none] высказаться.":

            m 3eka "Вперёд, [player]."

            m 1ekc "Для этого я здесь.{nw}"
            $ _history_list.pop()
            menu:
                m "Для этого я здесь.{fast}"
                "Я закончил.":

                    m 1eka "Я так рада, что ты смог[mas_gender_g] высказаться от всего сердца, [player]."
        "Я не хочу об этом говорить.":

            m 1ekc "..."
            m 3ekd "Хорошо, [player], я буду здесь, если ты передумаешь."
        "Всё в порядке.":

            m 1ekc "..."
            m 1ekd "Хорошо, [player], если ты так говоришь..."
            $ line_start = "Но,"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
