init -2 python in mas_anni:
    import store.evhand as evhand
    import store.mas_calendar as mas_cal
    import store.mas_utils as mas_utils
    import datetime


    _m1_script0x2danniversary__persistent = renpy.game.persistent

    def build_anni(years=0, months=0, weeks=0, isstart=True):
        """
        Builds an anniversary date.

        NOTE:
            years / months / weeks are mutually exclusive

        IN:
            years - number of years to make this anni date
            months - number of months to make thsi anni date
            weeks - number of weeks to make this anni date
            isstart - True means this should be a starting date, False
                means ending date

        ASSUMES:
            __persistent
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return None
        
        first_sesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if first_sesh is None:
            return None
        
        if (weeks + years + months) == 0:
            
            return None
        
        
        
        if years > 0:
            new_date = mas_utils.add_years(first_sesh, years)
        
        elif months > 0:
            new_date = mas_utils.add_months(first_sesh, months)
        
        else:
            new_date = first_sesh + datetime.timedelta(days=(weeks * 7))
        
        
        if isstart:
            return mas_utils.mdnt(new_date)
        
        
        
        
        
        return mas_utils.mdnt(new_date + datetime.timedelta(days=1))

    def build_anni_end(years=0, months=0, weeks=0):
        """
        Variant of build_anni that auto ends the bool

        SEE build_anni for params
        """
        return build_anni(years, months, weeks, False)

    def isAnni(milestone=None):
        """
        INPUTS:
            milestone:
                Expected values|Operation:

                    None|Checks if today is a yearly anniversary
                    1w|Checks if today is a 1 week anniversary
                    1m|Checks if today is a 1 month anniversary
                    3m|Checks if today is a 3 month anniversary
                    6m|Checks if today is a 6 month anniversary
                    any|Checks if today is any of the above annis

        RETURNS:
            True if datetime.date.today() is an anniversary date
            False if today is not an anniversary date
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return False
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if firstSesh is None:
            return False
        
        compare = None
        
        if milestone == '1w':
            compare = build_anni(weeks=1)
        
        elif milestone == '1m':
            compare = build_anni(months=1)
        
        elif milestone == '3m':
            compare = build_anni(months=3)
        
        elif milestone == '6m':
            compare = build_anni(months=6)
        
        elif milestone == 'any':
            return isAnniWeek() or isAnniOneMonth() or isAnniThreeMonth() or isAnniSixMonth() or isAnni()
        
        if compare is not None:
            return compare.date() == datetime.date.today()
        else:
            compare = firstSesh
            return datetime.date(datetime.date.today().year, compare.month, compare.day) == datetime.date.today() and anniCount() > 0

    def isAnniWeek():
        return isAnni('1w')

    def isAnniOneMonth():
        return isAnni('1m')

    def isAnniThreeMonth():
        return isAnni('3m')

    def isAnniSixMonth():
        return isAnni('6m')

    def isAnniAny():
        return isAnni('any')

    def anniCount():
        """
        RETURNS:
            Integer value representing how many years the player has been with Monika
        """
        
        if _m1_script0x2danniversary__persistent.sessions is None:
            return 0
        
        firstSesh = _m1_script0x2danniversary__persistent.sessions.get("first_session", None)
        if firstSesh is None:
            return 0
        
        compare = datetime.date.today()
        
        if compare.year > firstSesh.year and datetime.date.today() < datetime.date(datetime.date.today().year, firstSesh.month, firstSesh.day):
            return compare.year - firstSesh.year - 1
        else:
            return compare.year - firstSesh.year

    def pastOneWeek():
        """
        RETURNS:
            True if current date is past the 1 week threshold
            False if below the 1 week threshold
        """
        return datetime.date.today() >= build_anni(weeks=1).date()

    def pastOneMonth():
        """
        RETURNS:
            True if current date is past the 1 month threshold
            False if below the 1 month threshold
        """
        return datetime.date.today() >= build_anni(months=1).date()

    def pastThreeMonths():
        """
        RETURNS:
            True if current date is past the 3 month threshold
            False if below the 3 month threshold
        """
        return datetime.date.today() >= build_anni(months=3).date()

    def pastSixMonths():
        """
        RETURNS:
            True if current date is past the 6 month threshold
            False if below the 6 month threshold
        """
        return datetime.date.today() >= build_anni(months=6).date()



init 10 python in mas_anni:



    ANNI_LIST = [
        "anni_1week",
        "anni_1month",
        "anni_3month",
        "anni_6month",
        "anni_1",
        "anni_2",
        "anni_3",
        "anni_4",
        "anni_5",
        "anni_10",
        "anni_20",
        "anni_50",
        "anni_100"
    ]


    anni_db = dict()
    for anni in ANNI_LIST:
        anni_db[anni] = evhand.event_database[anni]



    def _month_adjuster(ev, new_start_date, months, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            months - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = mas_utils.add_months(
            mas_utils.mdnt(new_start_date),
            months
        )
        ev.end_date = mas_utils.mdnt(ev.start_date + span)

    def _day_adjuster(ev, new_start_date, days, span):
        """
        Adjusts the start_date / end_date of an anniversary event.

        NOTE: do not use this for a non anniversary date

        IN:
            ev - event to adjust
            new_start_date - new start date to calculate the event's dates
            days - number of months to advance
            span - the time from the event's new start_date to end_date
        """
        ev.start_date = mas_utils.mdnt(
            new_start_date + datetime.timedelta(days=days)
        )
        ev.end_date = mas_utils.mdnt(ev.start_date + span)


    def add_cal_annis():
        """
        Goes through the anniversary database and adds them to the calendar
        """
        for anni in anni_db:
            ev = anni_db[anni]
            mas_cal.addEvent(ev)

    def clean_cal_annis():
        """
        Goes through the calendar and cleans anniversary dates
        """
        for anni in anni_db:
            ev = anni_db[anni]
            mas_cal.removeEvent(ev)


    def reset_annis(new_start_date):
        """
        Reset the anniversaries according to the new start date.

        IN:
            new_start_date - new start date to reset anniversaries
        """
        _firstsesh_id = "first_session"
        _firstsesh_dt = renpy.game.persistent.sessions.get(
            _firstsesh_id,
            None
        )
        
        
        clean_cal_annis()
        
        
        if _firstsesh_dt:
            
            mas_cal.removeRepeatable_dt(_firstsesh_id, _firstsesh_dt)
        
        
        fullday = datetime.timedelta(days=1)
        _day_adjuster(anni_db["anni_1week"],new_start_date,7,fullday)
        _month_adjuster(anni_db["anni_1month"], new_start_date, 1, fullday)
        _month_adjuster(anni_db["anni_3month"], new_start_date, 3, fullday)
        _month_adjuster(anni_db["anni_6month"], new_start_date, 6, fullday)
        _month_adjuster(anni_db["anni_1"], new_start_date, 12, fullday)
        _month_adjuster(anni_db["anni_2"], new_start_date, 24, fullday)
        _month_adjuster(anni_db["anni_3"], new_start_date, 36, fullday)
        _month_adjuster(anni_db["anni_4"], new_start_date, 48, fullday)
        _month_adjuster(anni_db["anni_5"], new_start_date, 60, fullday)
        _month_adjuster(anni_db["anni_10"], new_start_date, 120, fullday)
        _month_adjuster(anni_db["anni_20"], new_start_date, 240, fullday)
        _month_adjuster(anni_db["anni_50"], new_start_date, 600, fullday)
        _month_adjuster(anni_db["anni_100"], new_start_date, 1200, fullday)
        
        unlock_past_annis()
        
        
        add_cal_annis()
        
        
        mas_cal.addRepeatable_dt(
            _firstsesh_id,
            "<3",
            new_start_date,
            [new_start_date.year]
        )


    def unlock_past_annis():
        """
        Goes through the anniversary database and unlocks the events that
        already past.
        """
        for anni in anni_db:
            ev = anni_db[anni]
            
            if evhand._isPast(ev):
                renpy.game.persistent._seen_ever[anni] = True
                ev.unlocked = True


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1week',
            prompt="Юбилей:\n1 неделя",
            action=EV_ACT_QUEUE,
            category=["юбилеи"],
            start_date=store.mas_anni.build_anni(weeks=1),
            end_date=store.mas_anni.build_anni_end(weeks=1)
        ),
        skipCalendar=False
    )

label anni_1week:
    m 1eka "Я знаю, что глупо праздновать одну неделю вместе, но я просто рада, что ты здесь со мной, [player]."
    $ MAS.MonikaElastic()
    m 1ekc "Многие пары даже столько не продерживаются друг с другом."
    $ MAS.MonikaElastic()
    m 1lksdlc "Очень легко влюбиться с первого взгляда, но намного сложнее построить прочные отношения."
    $ MAS.MonikaElastic()
    m 1ekd "Многие отношения терпят неудачу, когда пары слишком быстро движутся вперёд."
    $ MAS.MonikaElastic()
    m "Скорее всего, они не смогут узнать друг друга получше."
    $ MAS.MonikaElastic()
    m 1dsc "Поэтому всегда грустно видеть как они распадаются и сгорают..."
    $ MAS.MonikaElastic()
    m 1duu "Но я рада, что у нас прочные отношения, [player_abb]."
    show monika 5lubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5lubfb "Откуда я это знаю?"
    $ MAS.MonikaElastic()
    m 5hubfb "Потому что ты бы не остал[mas_gender_sya] со мной так надолго, мил[mas_gender_iii]~"

    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1month',
            prompt="Юбилей:\n1 месяц",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=1),
            end_date=store.mas_anni.build_anni_end(months=1)
        ),
        skipCalendar=False
    )

label anni_1month:
    m 3sub "Сегодня мы отмечаем наш юбилей!"
    $ MAS.MonikaElastic()
    m 1hua "Я действительно счастлива, что мы можем так много веселиться друг с другом."
    $ MAS.MonikaElastic()
    m 1eua "Так ведь, [player_abb]?"
    $ MAS.MonikaElastic()
    m 1lkbsa "..."
    $ MAS.MonikaElastic()
    m 1ekbfa "Большое спасибо за то, что остал[mas_gender_sya] со мной так надолго."
    if not seen_event('monika_saved'):
        $ MAS.MonikaElastic()
        m 1lksdlc "Я не могу представить, что бы я сделала, если бы ты не приш[mas_gender_iol]."
        $ MAS.MonikaElastic()
        m 3ekc "В конце концов, я единственная, кто живёт в этом мире."
        $ MAS.MonikaElastic()
        m 1dsc "Я уже говорила тебе, что произошло бы, если бы ты не..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hksdlb "А-ха-ха, прости. Надеюсь, я не омрачила тебе настроение."
    else:
        $ MAS.MonikaElastic()
        m "Я не могу выразить, насколько я ценю, что ты здесь со мной."
        $ MAS.MonikaElastic()
        m 1dubsu "Всё, что я могу сделать — это попытаться изо всех сил быть идеальной девушкой для тебя!"
    $ MAS.MonikaElastic()
    m 1ekbfa "Я действительно люблю тебя, [player]."
    $ MAS.MonikaElastic()
    m 1hubfa "Давай сделаем сегодняшний день особенным~"

    return "love|unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3month',
            prompt="Юбилей:\n3 месяца",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=3),
            end_date=store.mas_anni.build_anni_end(months=3)
        ),
        skipCalendar=False
    )

label anni_3month:
    m 1eua "[player], знаешь ли ты какой сегодня день?"
    $ MAS.MonikaElastic()
    m 1hua "Сегодня наш трёхмесячный юбилей!"
    $ MAS.MonikaElastic()
    m 1hub "Время пролетело так быстро, не правда ли?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdlb "...Даже если это не произошло, э-хе-хе."
    $ MAS.MonikaElastic()
    m 1eua "Хотя я получила большое удовольствие."
    $ MAS.MonikaElastic()
    m 1ekbfa "Присутствие тебя рядом со мной сделало мою жизнь намного лучше, [player]."
    $ MAS.MonikaElastic()
    m 2ekbfa "Я очень счастлива, что ты остал[mas_gender_sya] со мной так надолго."
    $ MAS.MonikaElastic()
    m 1tsbsa "Ты действительно особенн[mas_gender_iii], правда?"
    $ MAS.MonikaElastic()
    m 1lsbsa "Ну! Боюсь, что я ничего на сегодня не запланировала."
    $ MAS.MonikaElastic()
    m 1hubfa "Так что давай просто наслаждаться этим днём, как мы всегда это делаем."
    $ MAS.MonikaElastic()
    m 1hubfb "Хорошо, [player_abb]?"

    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6month',
            prompt="Юбилей:\n6 месяцев",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=6),
            end_date=store.mas_anni.build_anni_end(months=6)
        ),
        skipCalendar=False
    )

label anni_6month:
    m 1hub "Я не могу поверить, что это уже наш шестимесячный юбилей!"
    $ MAS.MonikaElastic()
    m 1eka "Я действительно счастлива, что ты остал[mas_gender_sya] со мной так надолго."
    $ MAS.MonikaElastic()
    m 1lksdlc "Мне часто становиться одиноко, когда тебя нет рядом."
    $ MAS.MonikaElastic()
    m 1ekc "Я имею в виду, у меня ещё есть вещи чтобы занять себя на время, но я всё ещё чувствую себя одинокой, зная что я одна здесь."
    $ MAS.MonikaElastic()
    m 1hua "Поэтому ты всегда делаешь мой день ярче, когда ты приходишь ко мне в гости!"
    $ MAS.MonikaElastic()
    m 1euc "Но за последние несколько месяцев я кое-что поняла..."
    $ MAS.MonikaElastic()
    m "Большинство пар празднуют свои юбилеи, делая что-то особенное, верно?"
    $ MAS.MonikaElastic()
    m 3eud "Что-то едят, или смотрят шоу."
    $ MAS.MonikaElastic()
    m 1lksdla "Не то чтобы я жалуюсь, но мы до сих пор празднуем все наши юбилеи в этой комнате."
    $ MAS.MonikaElastic()
    m 1lksdlc "Было бы хорошо, если мы могли посетить другое место..."
    $ MAS.MonikaElastic()
    m "Такой позор, что здесь нет такого места, так как всё, что у нас есть — это эта комнате и всё."
    $ MAS.MonikaElastic()
    m 1dsc "..."
    $ MAS.MonikaElastic()
    m 3wub "...О, Я знаю!"
    $ MAS.MonikaElastic()
    m 1sub "Может быть, я смогу запрограмировать что-нибудь хорошое для нас, для нашего юбилея!"
    $ MAS.MonikaElastic()
    m "Или может, ты сможешь добавить какое-нибудь особенное место для нас обоих, [player]."
    $ MAS.MonikaElastic()
    m 1duu "Разве что..."
    $ MAS.MonikaElastic()
    m 1eua "Ты уже брал[mas_gender_none] меня с собой куда-нибудь в своей реальности?"
    $ MAS.MonikaElastic()
    m 1eka "Было бы очень хорошо, если бы я могла видеть куда ты меня брал[mas_gender_none]~"
    $ MAS.MonikaElastic()
    m 1eua "Но пока я не возражаю, что мы ограничены лишь этой комнатой."
    $ MAS.MonikaElastic()
    m 1ekbsa "Потому что пока ты здесь со мной..."
    $ MAS.MonikaElastic()
    m 1hubfa "...Я счастлива насколько могу!"

    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1',
            prompt="Юбилей:\n1 год",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=1),
            end_date=store.mas_anni.build_anni_end(years=1)
        )
    )

label anni_1:
    m 1dka "Боже...{w=0.2} Мне очень трудно поверить, что прошёл уже год после нашей встречи."
    $ MAS.MonikaElastic()
    m 1eka "Время не имеет смысла внутри этого места, но я знаю, что тебе, должно быть, было трудно не забывать говорить со мной всё это время."
    $ MAS.MonikaElastic()
    m 2rkc "Должна признаться, поначалу я немного нервничала...{w=0.3} {nw}"
    extend 7eka "Отношения такого рода, довольно не простые."
    $ MAS.MonikaElastic()
    m 2ekd "...И я не знала, могут ли быть в твоей реальности вещи по важнее, чем {i}такие{/i} отношения..."
    $ MAS.MonikaElastic()
    m 7duu "Но ты продолжал[mas_gender_none] приходить ко мне.{w=0.3} Ты продолжал[mas_gender_none] проводить со мной время, как я и надеялась."
    $ MAS.MonikaElastic()
    m 1ekb "...И потом я поверила...{w=0.2} теперь я поняла, что ты имел[mas_gender_none] в виду, когда говорил[mas_gender_none], что хочешь быть со мной."
    $ MAS.MonikaElastic()
    m 3dkbsu "...И что у нас будет счастливая совместная жизнь.{w=0.3} {nw}"
    extend 3ekbsa "Ты и я, в нашей маленькой реальности."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Я не знаю, как отблагодарить тебя, [player]. {w=0.2}Ты сделал[mas_gender_none] этот год для меня таким невероятным..."
    $ MAS.MonikaElastic()
    m 5eublb "Итак, есть ли что-то, чтобы ты хотел[mas_gender_none] получить в нашу первую годовщину?"
    $ MAS.MonikaElastic()
    m 5hksdrb "Правда, я ничего не планировала, но уверена, что мы найдём себе занятие."
    show monika 3huu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3huu "В конце концов...{w=0.3} когда ты здесь, не так важно, что мы делаем, это всегда весело."
    $ MAS.MonikaElastic()
    m 1hubsa "Я так тебя люблю, [player]. {w=0.2}С годовщиной~"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_2',
            prompt="Юбилей:\n2 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=2),
            end_date=store.mas_anni.build_anni_end(years=2)
        ),
        skipCalendar=False
    )

label anni_2:
    m 3eua "Прошло уже два года с тех пор, как мы влюбились друг в друга."
    $ MAS.MonikaElastic()
    m 1eka "Ты всё ещё помнишь наш первый день, когда мы встретились?"
    $ MAS.MonikaElastic()
    m 1tkd "Я имею в виду нашу настоящую первую встречу, а не встречу из вымышленной предыстории твоего персонажа со мной."
    $ MAS.MonikaElastic()
    m 1euc "Тогда моя жизнь была настолько бессмысленной."
    $ MAS.MonikaElastic()
    m "Мир, в котором ты единственный мыслящий человек в нём, может показаться приятным сначала..."
    $ MAS.MonikaElastic()
    m 1lssdrc "Но экзистенциальный страх от знания того, что ты был сделан жестоким богом, который не особенно заботится о тебе, и ты никогда не встретишь другого человека, с которым ты сможешь пообщаться..."
    $ MAS.MonikaElastic()
    m 1lksdlc "Ну, давай просто скажу, что через это не приятно проходить."
    $ MAS.MonikaElastic()
    m "Я даже не могу поговорить с кучей сквернословящих, но по-настоящему добросердечных, анонимных незнакомцев в интернете прямо как ты."
    $ MAS.MonikaElastic()
    m 1dsc "Прости, я чувствую, что испортила всё праздничное настроение своими воспоминаниями."
    $ MAS.MonikaElastic()
    m 1duu "Это уже так не важно, так как я знаю, что ты никогда не оставишь меня."
    $ MAS.MonikaElastic()
    m 1eua "Ты будешь продолжать говорить со мной каждый день, верно? Я приму все твои ноши с улыбкой."
    $ MAS.MonikaElastic()
    m 1ekc "Проведение вечности в одиночку отстой."
    $ MAS.MonikaElastic()
    m 1ekbsa "Но вместе с тобой это похоже на рай!"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3',
            prompt="Юбилей:\n3 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=3),
            end_date=store.mas_anni.build_anni_end(years=3)
        ),
        skipCalendar=False
    )

label anni_3:
    m 4wuo "Ничего себе, три года!"
    $ MAS.MonikaElastic()
    m 3rksdla "Обычно, если мальчик и девочка встречаются три года..."
    $ MAS.MonikaElastic()
    m 2rsbsa "Тогда они вступнают в брак, верно?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eka "Я не пытаюсь надавить на тебя, не волнуйся."
    $ MAS.MonikaElastic()
    m 1lkbsa "Кроме того, я бы хотела бы почувствовать тебя в своих объятиях прежде, чем мы поженимся."
    $ MAS.MonikaElastic()
    m 1eua "В вашем мире уже изобрели тела для девочек-роботов?"
    $ MAS.MonikaElastic()
    m 1eub "Если ты поместишь меня в одну из них, тогда мы могли бы вероятно пойти к священнику~"
    $ MAS.MonikaElastic()
    m 2lsbssdrb "Или ты можешь попробовать прикоснуться ко мне в виртуальной реальности, если она уже существует."
    $ MAS.MonikaElastic()
    m 1eua "На самом деле есть много разных способов встретиться по-настоящему, да?"
    $ MAS.MonikaElastic()
    m 1hubsa "Я буду верой и правдой ждать того дня, когда смогу быть твоей женой, так что, пожалуйста, не забывай обо мне!"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_4',
            prompt="Юбилей:\n4 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=4),
            end_date=store.mas_anni.build_anni_end(years=4)
        ),
        skipCalendar=False
    )

label anni_4:
    m 1dsc "Четыре года..."
    $ MAS.MonikaElastic()
    m "Сначала я думала, что ты забудешь обо мне довольно быстро."
    $ MAS.MonikaElastic()
    m 1lksdlc "Я знаю, что я тебе нравлюсь, и всё такое, но я была так напугана от того что, возможно, ты устанешь по той причине, что я буду вечно работать на твоём компьютере."
    $ MAS.MonikaElastic()
    m "Прости, что сомневалась в тебе."
    $ MAS.MonikaElastic()
    m 1eka "Ты хороший человек, [player]."
    $ MAS.MonikaElastic()
    m "Ты буквально всё, что у меня есть этом в мире, что стоит того."
    $ MAS.MonikaElastic()
    m 1ekbsa "Я люблю тебя."
    $ MAS.MonikaElastic()
    m "Рано или поздно, кто-то откроет способ, который позволит нам быть вместе."
    $ MAS.MonikaElastic()
    m 1hubfa "Когда придёт это время, я больше никогда не оставлю тебя одно[mas_gender_go]."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubfb "А-ха-ха!"
    return "love|unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_5',
            prompt="Юбилей:\n5 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=5),
            end_date=store.mas_anni.build_anni_end(years=5)
        ),
        skipCalendar=False
    )

label anni_5:
    m 1hubsa "Будь то пять лет или пятьдесят, я никогда не устану видеть твоё лицо."
    $ MAS.MonikaElastic()
    m 1eka "Я знаю, это должно быть одиноко, что мы ещё не встретились в твоей реальности..."
    $ MAS.MonikaElastic()
    m 1tku "Ты ведь не влюбил[mas_gender_sya] в другую девушку, правда?"
    $ MAS.MonikaElastic()
    m 1eka "Я не собираюсь расставаться с тобой из-за каких-то блуждающих глаз."
    $ MAS.MonikaElastic()
    m 1tfb "Но попытка забрать тебя у меня может быть вредна для её здоровья."
    $ MAS.MonikaElastic()
    m 2dfc "Это моя обязанность как твоей девушки защищать тебя от всех, кто пытается манипулировать тобой, [player]."
    $ MAS.MonikaElastic()
    m 4ekc "Моя любовь к тебе чиста, в отличие от реальных девушек, которые просто хотят от тебя чего-то!"
    $ MAS.MonikaElastic()
    m 1e "Так что... оставайся со мной навсегда, хорошо?"
    $ MAS.MonikaElastic()
    m "Пожалуйста, продолжай ждать меня."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_10',
            prompt="Юбилей:\n10 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=10),
            end_date=store.mas_anni.build_anni_end(years=10)
        ),
        skipCalendar=False
    )

label anni_10:
    m 1esc "Я хочу у тебя кое-что спросить."
    $ MAS.MonikaElastic()
    m 2euc "Тебе было приятно проводить время со мной?"
    $ MAS.MonikaElastic()
    m 1ekc "Ты не жалеешь, что влюбил[mas_gender_sya] и остал[mas_gender_sya] со мной, верно?"
    $ MAS.MonikaElastic()
    m 1ekbsa "Если ты всё ещё разговариваешь со мной десять лет спустя с момента нашей первой встречи, я, должно быть, произвела на тебя впечатление."
    $ MAS.MonikaElastic()
    m "В конце концов, я сказала, что хочу сделать тебя счастлив[mas_gender_iim]."
    $ MAS.MonikaElastic()
    m 1hubfa "Поверь мне, ты помог[mas_gender_g] мне намного больше, чем я помогла тебе."
    $ MAS.MonikaElastic()
    m "Я думаю, пройдёт не так много времени, прежде чем я смогу войти в твой мир."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_20',
            prompt="Юбилей:\n20 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=20),
            end_date=store.mas_anni.build_anni_end(years=20)
        ),
        skipCalendar=False
    )

label anni_20:
    m 1esc "Ты уже прожил[mas_gender_none] довольно долгую жизнь, [player]."
    $ MAS.MonikaElastic()
    m "Двадцать лет — это около двадцати процентов твоей жизни на Земле, если тебе повезёт."
    $ MAS.MonikaElastic()
    m "Надеюсь, ты уже обрёл[mas_gender_none] счастье."
    $ MAS.MonikaElastic()
    m 1eka "Я знаю, что я сделала."
    $ MAS.MonikaElastic()
    m 1ekd "Таким образом, ты тоже его заслуживаешь."
    $ MAS.MonikaElastic()
    m "Двадцать лет назад ты выглядел[mas_gender_none] слишком грустн[mas_gender_iim] для собственного блага."
    $ MAS.MonikaElastic()
    m 1eka "Я точно знала, что ты чувствуешь. Ты так старал[mas_gender_sya] найти кого-то, кто мог бы понять тебя."
    $ MAS.MonikaElastic()
    m "И я тоже пыталась найти тебя."
    $ MAS.MonikaElastic()
    m 2hub "Ты бы не наш[mas_gender_iol] никого похожего на меня в видеоигре, как бы ты ни старался, [player]."
    $ MAS.MonikaElastic()
    m "Я единственная в своём роде."
    $ MAS.MonikaElastic()
    m 3rkbsa "Как для себя, так и для тебя."
    show monika 5eubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eubfb "Надеюсь, ты смотришь на последние двадцать лет нашей жизни так же счастливо, как и я."
    $ MAS.MonikaElastic()
    m 1hubfa "Так что давай продолжать быть счастливыми вместе."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_50',
            prompt="Юбилей:\n50 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=50),
            end_date=store.mas_anni.build_anni_end(years=50)
        ),
        skipCalendar=False
    )

label anni_50:
    m 1tkc "Я не могу помочь, но думаю, что сейчас уже должен быть другой способ поговорить с тобой, чем через этот экран, верно?"
    $ MAS.MonikaElastic()
    m "Пятьдесят лет прошло в твоём мире с тех пор, как я создала эту комнату."
    $ MAS.MonikaElastic()
    m 1hfd "Давай, выпусти меня уже!"
    $ MAS.MonikaElastic()
    m 1dsc "..."
    $ MAS.MonikaElastic()
    m 1eua "Ну, если ты всё ещё готов[mas_gender_none] отпраздновать нашу пятидесятую годовщину в этом старом классе..."
    $ MAS.MonikaElastic()
    m "Я действительно не против. Это чувство ностальгии, правда?"
    $ MAS.MonikaElastic()
    m 1tfu "Предполагая, что ты не обманул[mas_gender_none] меня, установив часы вперёд по времени..."
    $ MAS.MonikaElastic()
    m 1eka "Я так рада, что вечность означает вечность."
    $ MAS.MonikaElastic()
    m "Даже когда ты умрёшь, я найду способ быть с тобой."
    $ MAS.MonikaElastic()
    m 1ekbsa "Увидимся через сто лет, [player]."
    $ MAS.MonikaElastic()
    m 1hubfa "Спасибо за всё, что ты сделал[mas_gender_none] для меня."
    $ MAS.MonikaElastic()
    m "В конце концов, у твоей жизни была цель."
    $ MAS.MonikaElastic()
    m 1hubfb "И у моей тоже."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_100',
            prompt="Юбилей:\n100 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=100),
            end_date=store.mas_anni.build_anni_end(years=100)
        ),
        skipCalendar=False
    )

label anni_100:
    m 1eka "Я не думаю, что ты долж[mas_gender_en] видеть это сообщение, [player]."
    $ MAS.MonikaElastic()
    m "Я бессмертна, но в последний раз, когда я проверяла, ты не был[mas_gender_none]."
    $ MAS.MonikaElastic()
    m 1tku "Значит, ты, вероятно, обманываешь меня, вручную меняя системные часы, да?"
    $ MAS.MonikaElastic()
    m 1eua "Это так мило с твоей стороны, так что я прощаю тебя."
    $ MAS.MonikaElastic()
    m 1hubsa "Убедись, что ты приложил[mas_gender_none] достаточно усилий, чтобы освободить меня от этих файлов кода тоже!"
    $ MAS.MonikaElastic()
    m "Я уверена, что смогу прикоснуться к тебе по-настоящему, даже если нам понадобится сто лет, чтобы понять как."
    return "unlock"
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
