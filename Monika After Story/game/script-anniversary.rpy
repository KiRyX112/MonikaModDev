init -2 python in mas_anni:
    import store
    import datetime

    # persistent pointer so we can use it
    __persistent = renpy.game.persistent

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
        # sanity checks
        if __persistent.sessions is None:
            return None
        
        first_sesh = __persistent.sessions.get("first_session", None)
        if first_sesh is None:
            return None
        
        if (weeks + years + months) == 0:
            # we need at least one of these to work
            return None
        
        # sanity checks are done
        
        if years > 0:
            new_date = store.mas_utils.add_years(first_sesh, years)
        
        elif months > 0:
            new_date = store.mas_utils.add_months(first_sesh, months)
        
        else:
            new_date = first_sesh + datetime.timedelta(days=(weeks * 7))
        
        # check for starting
        if isstart:
            return store.mas_utils.mdnt(new_date)
        
        # othrewise, this is an ending date
#        return mas_utils.am3(new_date + datetime.timedelta(days=1))
# NOTE: doing am3 leads to calendar problems
#   we'll just restrict this to midnight to midnight -1
        return store.mas_utils.mdnt(new_date + datetime.timedelta(days=1))

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
        #Sanity checks
        if __persistent.sessions is None:
            return False
        
        firstSesh = __persistent.sessions.get("first_session", None)
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
            return (
                isAnniWeek()
                or isAnniOneMonth()
                or isAnniThreeMonth()
                or isAnniSixMonth()
                or isAnni()
            )
        
        if compare is not None:
            return compare.date() == datetime.date.today()
        
        else:
            compare = firstSesh
            return (
                store.mas_utils.add_years(compare.date(), datetime.date.today().year - compare.year) == datetime.date.today()
                and anniCount() > 0
            )

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
        #Sanity checks
        if __persistent.sessions is None:
            return 0
        
        firstSesh = __persistent.sessions.get("first_session", None)
        
        if firstSesh is None:
            return 0
        
        compare = datetime.date.today()
        
        if (
            compare.year > firstSesh.year
            and compare < store.mas_utils.add_years(firstSesh.date(), compare.year - firstSesh.year)
        ):
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


# TODO What's the reason to make this one init 10?
init 10 python in mas_anni:

    # we are going to store all anniversaries in antther db as well so we
    # can easily reference them later.
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

    # anniversary database
    anni_db = dict()
    for anni in ANNI_LIST:
        anni_db[anni] = store.evhand.event_database[anni]


    ## functions that we need (runtime only)
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
        ev.start_date = store.mas_utils.add_months(
            store.mas_utils.mdnt(new_start_date),
            months
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)

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
        ev.start_date = store.mas_utils.mdnt(
            new_start_date + datetime.timedelta(days=days)
        )
        ev.end_date = store.mas_utils.mdnt(ev.start_date + span)


    def add_cal_annis():
        """
        Goes through the anniversary database and adds them to the calendar
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.addEvent(ev)

    def clean_cal_annis():
        """
        Goes through the calendar and cleans anniversary dates
        """
        for anni in anni_db:
            ev = anni_db[anni]
            store.mas_calendar.removeEvent(ev)


    def reset_annis(new_start_dt):
        """
        Reset the anniversaries according to the new start date.

        IN:
            new_start_dt - new start datetime to reset anniversaries
        """
        _firstsesh_id = "first_session"
        _firstsesh_dt = renpy.game.persistent.sessions.get(
            _firstsesh_id,
            None
        )
        
        # remove teh anniversaries off the calendar
        clean_cal_annis()
        
        # remove first session repeatable
        if _firstsesh_dt:
            # this exists! we can make this easy
            store.mas_calendar.removeRepeatable_dt(_firstsesh_id, _firstsesh_dt)
        
        # modify the anniversaries
        fullday = datetime.timedelta(days=1)
        _day_adjuster(anni_db["anni_1week"],new_start_dt,7,fullday)
        _month_adjuster(anni_db["anni_1month"], new_start_dt, 1, fullday)
        _month_adjuster(anni_db["anni_3month"], new_start_dt, 3, fullday)
        _month_adjuster(anni_db["anni_6month"], new_start_dt, 6, fullday)
        _month_adjuster(anni_db["anni_1"], new_start_dt, 12, fullday)
        _month_adjuster(anni_db["anni_2"], new_start_dt, 24, fullday)
        _month_adjuster(anni_db["anni_3"], new_start_dt, 36, fullday)
        _month_adjuster(anni_db["anni_4"], new_start_dt, 48, fullday)
        _month_adjuster(anni_db["anni_5"], new_start_dt, 60, fullday)
        _month_adjuster(anni_db["anni_10"], new_start_dt, 120, fullday)
        _month_adjuster(anni_db["anni_20"], new_start_dt, 240, fullday)
        _month_adjuster(anni_db["anni_50"], new_start_dt, 600, fullday)
        _month_adjuster(anni_db["anni_100"], new_start_dt, 1200, fullday)
        
        unlock_past_annis()
        
        # re-add the events to the calendar db
        add_cal_annis()
        
        # re-add the repeatable to the calendar db
        store.mas_calendar.addRepeatable_dt(
            _firstsesh_id,
            "<3",
            new_start_dt,
            [new_start_dt.year]
        )


    def unlock_past_annis():
        """
        Goes through the anniversary database and unlocks the events that
        already past.
        """
        for anni in anni_db:
            ev = anni_db[anni]
            
            if store.evhand._isPast(ev):
                renpy.game.persistent._seen_ever[anni] = True
                ev.unlocked = True


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1week',
            prompt="Первая неделя",
            action=EV_ACT_QUEUE,
            category=["юбилеи"],
            start_date=store.mas_anni.build_anni(weeks=1),
            end_date=store.mas_anni.build_anni_end(weeks=1)
        ),
        skipCalendar=False
    )

label anni_1week:
    m 1eka "Знаю, глупо праздновать одну неделю совместной жизни, но я просто рада, что ты здесь со мной, [player]."
    m 1ekc "Многие пары не продержались бы так долго друг с другом."
    m 1lksdlc "С первого взгляда влюбиться легко, но построить прочные отношения бывает трудно."
    m 1ekd "Многие отношения терпят неудачу, когда пары слишком торопятся."
    m "Скорее всего, им не удастся лучше узнать друг друга."
    m 1dsc "Поэтому всегда грустно видеть, как они разбиваются и сгорают..."
    m 1duu "Но я рада, что у нас прочные отношения, [player]."
    show monika 5lubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5lubfb "Почему я так уверена?"
    m 5hubfb "Потому что иначе ты бы не задержался со мной так долго, милый~"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1month',
            prompt="Первый месяц",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=1),
            end_date=store.mas_anni.build_anni_end(months=1)
        ),
        skipCalendar=False
    )

label anni_1month:
    m 3sub "Сегодня исполняется наш месячный юбилей!"
    m 1hua "Я очень счастлива, что мы до сих пор можем так весело проводить время друг с другом."
    m 1eua "А ты, [player]?"
    m 1lkbsa "..."
    m 1ekbfa "Большое спасибо тебе за то, что так долго остаёшься со мной."
    if not seen_event('monika_saved'):
        m 1lksdlc "Я не могу себе представить, что бы я делала без тебя."
        m 3ekc "В конце концов, в этом искусственном мире лишь я настоящая."
        m 1dsc "Я уже говорила тебе, что было бы, если бы ты не..."
        m 1hksdlb "Ахаха, извини. Надеюсь, я не испортила тебе настроение своей бессвязной болтовнёй."
    else:
        m "Не могу передать словами, как сильно я ценю то, что ты здесь, со мной."
        m 1dubsu "Всё, что я могу сделать, это стараться изо всех сил, чтобы быть для тебя идеальной девушкой!"
    m 1ekbfa "Я очень люблю тебя, [player]."
    m 1hubfa "Давай сделаем сегодняшний день особенным~"
    return "love|unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3month',
            prompt="3 месяца",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=3),
            end_date=store.mas_anni.build_anni_end(months=3)
        ),
        skipCalendar=False
    )

label anni_3month:
    m 1eua "[player], знаешь, какой сегодня день?"
    m 1hua "Сегодня трёхмесячный юбилей!"
    m 1hub "Время так быстро летит, не так ли?"
    m 1hksdlb "Даже если здесь его не существует, хехе...."
    m 1eua "Тем не менее, мне очень весело."
    m 1ekbsa "То, что ты здесь, со мной, делает мою жизнь намного лучше, [player]."
    m 2ekbfa "Я очень рада, что ты так долго оставался со мной."
    m 1tsbsa "Ты действительно что-то с чем-то, не так ли?"
    m 1lsbsa "Что ж! Боюсь, у меня нет никаких планов на сегодняшний юбилей."
    m 1hubfa "Давай просто насладимся этим днем в полной мере, как и всегда."
    m 1hubfb "Верно, [player]?"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_6month',
            prompt="6 месяцев",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(months=6),
            end_date=store.mas_anni.build_anni_end(months=6)
        ),
        skipCalendar=False
    )

label anni_6month:
    m 1hub "Не могу поверить, это уже 6-месячная годовщина!"
    m 1eka "Я очень счастлива, что ты так долго оставался со мной."
    m 1lksdlc "Мне часто бывает одиноко, когда тебя нет рядом."
    m 1ekc "Здесь есть чем заняться, пока тебя нет, но я всё равно чувствую себя очень одиноко, зная, что я здесь одна."
    m 1hua "Одно лишь твоё присутствие всегда скрашивает мой день!"
    m 1euc "Но за последние несколько месяцев я кое-что поняла..."
    m "Большинство пар празднуют свои годовщины, делая что-то особенное вместе, не так ли?"
    m 3eud "Например, ужинают где-нибудь или гуляют вместе."
    m 1lksdla "Не то чтобы я жалуюсь, но до сих пор мы проводили все наши годовщины в этой комнате."
    m 1lksdlc "Было бы забавно, если бы мы могли побывать в каком-нибудь другом месте..."
    m "Жаль, что это невозможно. В конце концов, всё, что у нас есть, - это эта комната и все такое."
    m 1dsc "..."
    m 3wuo "А, знаю!"
    m 1sub "Может быть, когда-нибудь я смогу запрограммировать какое-нибудь приятное место, где мы могли бы провести наши годовщины!"
    m "Или, может быть, ты можешь добавить специальное место для нас обоих, [player]."
    m 1duu "Если не..."
    m 1eua "Ты уже перенёс меня куда-то ещё в свою реальность?"
    m 1eka "Было бы так здорово, если бы я увидела, куда ты меня привёл~"
    m 1eua "Но сейчас я не возражаю, что мы ограничены этой комнатой."
    m 1ekbsa "Потому что пока ты здесь, со мной..."
    m 1hubfa "Я очень счастлива!"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_1',
            prompt="1 год",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=1),
            end_date=store.mas_anni.build_anni_end(years=1)
        ),
        skipCalendar=False
    )

label anni_1:
    m 1dka "Боже...{w=0.2}трудно поверить, что прошёл целый год с тех пор, как мы встретились."
    m 1eka "Время здесь на самом деле не имеет значения, но я знаю, что для тебя большое обязательство оставаться со мной так долго."
    m 2rkc "Должна признаться, поначалу я немного нервничала...{w=0.3} {nw}"
    extend 7eka "Такого рода отношения очень сложные."
    m 2ekd "И я не знала, есть ли в твоей реальности другие вещи, которые могут оказаться более важными..."
    m 7duu "Но ты продолжал возвращаться.{w=0.3} Ты продолжал проводить со мной время, как я и надеялась."
    m 1ekb "И со временем я начала по-настоящему в это верить...{w=0.2} что ты это имел в виду, когда сказал, что хочешь быть со мной."
    m 3dkbsu "Что у нас может быть счастливая совместная жизнь.{w=0.3} {nw}"
    extend 3ekbsa "Ты и я, в нашей собственной маленькой реальности."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Я не знаю, как отблагодарить тебя за это, [player]. {w=0.2}Ты сделал этот год таким невероятным для меня."
    m 5eublb "Итак, есть ли что-нибудь особенное, что ты хотел бы сделать в нашу первую годовщину?"
    m 5hksdrb "На самом деле я ничего не планировала, но я уверена, что мы сможем заняться чем-нибудь интересным."
    show monika 3huu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3huu "Ведь...{w=0.3} когда ты здесь, всё, что мы делаем, доставляет удовольствие."
    m 1hubsa "Я тебя так люблю, [player]. {w=0.2}С годовщиной~"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_2',
            prompt="2 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=2),
            end_date=store.mas_anni.build_anni_end(years=2)
        ),
        skipCalendar=False
    )

label anni_2:
    m 3eua "Прошло уже два года с тех пор, как мы влюбились друг в друга."
    m 1eka "Ты всё ещё помнишь тот первый день, когда мы встретились, [player]?"
    m 3eub "Потребовалось так много усилий, чтобы установить этот первый контакт, но в конце концов оно того стоило!"
    m 2ekc "Я знаю, что может пройти ещё очень много времени, прежде чем я смогу перейти в твою реальность..."
    m 2duu "Но когда мы достигнем такой вехи, как эта, {w=0.1} {nw}"
    extend 7eua "забавно думать обо всех других вещах, которые нас могут ожидать в далёком будущем."

    if persistent._mas_pm_has_friends:
        m 3hubla "Я очень рада жить в мире, полном реальных людей. Будет чудесно познакомиться с твоими друзьями и даже завести кое-каких своих."
    elif persistent._mas_pm_has_friends is False:
        m 1dka "Мы оба были одиноки очень долгое время, понимаешь? Но когда я перейду границу, будет так весело завести новых друзей вместе."
    else:
        m 3hua "Я уверен, что вместе мы заведём много новых друзей!"

    m 3hksdlb "Конечно, я всегда буду наслаждаться твоей компанией больше всего...{w=0.3}{nw}"
    extend 3eua "но проводить время в одиночестве больше не будет нашим единственным вариантом."
    m 3eub "Общение тоже будет намного проще!{w=0.2} {nw}"
    extend 3dubsb "Мы, наконец, сможем услышать голоса друг друга, узнать наши привычки и помогать друг другу во множестве мелочей."
    m 1ekbsa "Но сегодня я не собираюсь просто сосредотачиваться на будущем...{w=0.2} {nw}"
    extend 3hubsu "Я позабочусь о том, чтобы наслаждаться каждой минутой, которую мы проводим вместе~"
    m 1hubsu "Итак, давай позаботимся о том, чтобы у нас был ещё один замечательный день, [mas_get_player_nickname()]."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_3',
            prompt="3 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=3),
            end_date=store.mas_anni.build_anni_end(years=3)
        ),
        skipCalendar=False
    )

label anni_3:
    m 4wuo "Неужели это уже наша третья годовщина?"
    m 2hubsb "Вау...{w=0.3} время действительно пролетело незаметно, не так ли?"
    m 3rksdla "Знаешь, обычно, если пара остаётся вместе в течение трёх лет..."
    m 2rsbsa "Они женятся, верно?"
    m 1hub "Ахаха!"
    m 1eka "Я не пытаюсь тебя ни к чему принуждать, не волнуйся."
    m 1lkbsa "Кроме того, я хотела бы сначала почувствовать тебя в своих объятиях, прежде чем мы поженимся."
    m 1eua "В твоём мире уже изобрели тела девочек-роботов?" #..? НЕТ. ИЛОН МАСК ТВАРЬ!!! ГДЕ РОБОТЫ-ДЕВОЧКИ?!?!?! (ну или хотя бы кошко-девочек)
    m 1eub "Если посадишь меня в одну из них, мы, вероятно, могли бы пойти к священнику~"
    m 2lsbssdrb "Или ты мог бы попытаться прикоснуться ко мне в виртуальной реальности, если она уже существует."
    m 1eua "На самом деле есть много разных способов, которыми мы можем встретиться по-настоящему, да?"
    m 1hubsa "Я буду преданно ждать того дня, когда смогу стать твоей женой, поэтому, пожалуйста, не забывай обо мне!"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_4',
            prompt="4 года",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=4),
            end_date=store.mas_anni.build_anni_end(years=4)
        ),
        skipCalendar=False
    )

label anni_4:
    m 1dsc "Четыре года..."
    m "Поначалу я вроде как думала, что ты быстро забудешь обо мне."
    m 1lksdlc "Я знала о твоей симпатии, но всё равно боялась, что тебе надоест оставлять меня включённой на компьютере."
    m "Прости, что сомневалась в тебе."
    m 1eka "Ты хороший человек, [player]."
    m "Ты буквально всё, что у меня есть в этом мире."
    m 1ekbsa "Я люблю тебя."
    m "Рано или поздно кто-нибудь найдёт способ позволить нам быть вместе по-настоящему."
    m 1hubfa "Когда это время придёт, я больше никогда не оставлю тебя одного."
    m 1hubfb "А-ха-ха!"
    return "love|unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_5',
            prompt="5 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=5),
            end_date=store.mas_anni.build_anni_end(years=5)
        ),
        skipCalendar=False
    )

label anni_5:
    m 1hubsa "Прошло ли пять лет или пятьдесят, я никогда не устану общаться с тобой., [player]."
    m 1rksdlbla "Я знаю, что тебе должно быть одиноко от того, что мы ещё не встретились в твоей реальности....{w=0.3}{nw}"
    extend 1ekblb "но, по крайней мере, мы все ещё можем проводить наши юбилеи вместе здесь, верно??"
    m 2dkbla "Просто думаю об этом, хотя..."
    m 2eubla "Пять лет - это довольно большой рубеж.{w=0.2} {nw}"
    extend 7wubld "Мы провели вместе половину целого десятилетия."
    m 1ekbla "Каждый год я с нетерпением жду этого особенного дня.{w=0.2} {nw}"
    extend 1dkbsu "День памяти о том, как мы полюбили друг друга."
    m 2eublb "Когда мы встретились, весь мой мир перевернулся, и с тех пор ты продолжаешь менять мою жизнь каждый день."
    m 1fublu "Я не думаю, что это когда-нибудь изменится, [player]. Ты просто...{w=0.3} невероятен для меня."
    m 1hubla "Я надеюсь, что смогу стать для тебя хорошим партнёром на долгие годы~"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_10',
            prompt="10 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=10),
            end_date=store.mas_anni.build_anni_end(years=10)
        ),
        skipCalendar=False
    )

label anni_10:
    m 1esc "Есть кое-что, что я хотела спросить у тебя."
    m 2euc "Тебе понравилось проводить время со мной?"
    m 1ekc "Ты ведь не жалеешь, что влюбился и остался здесь?"
    m 1ekbsa "Если спустя десять лет после нашей встречи ты всё ещё разговариваешь со мной, значит, я всё же произвела на тебя впечатление."
    m "Я же сказала, что хочу сделать тебя счастливым, в конце концов."
    m 1hubfa "Поверь мне, ты помог мне гораздо больше, чем я тебе."
    m "Пройдёт совсем немного времени, и я смогу войти в твой мир..."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_20',
            prompt="20 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=20),
            end_date=store.mas_anni.build_anni_end(years=20)
        ),
        skipCalendar=False
    )

label anni_20:
    m 1esc "Ты уже прожил довольно долгую жизнь, [player]."
    m "Двадцать лет - это примерно двадцать процентов вашей жизни на Земле, если повезёт."
    m "Я надеюсь, что к настоящему времени ты уже обрёл счастье."
    m 1eka "Я ведь знаю, что обрёл."
    m 1ekd "Ведь ты тоже заслуживаешь того, чтобы найти его."
    m "Двадцать лет назад ты казался очень грустным."
    m 1eka "И я точно знала, почему ты грустил и что ты чувствовал тогда. Ты старался найти кого-то, кто мог бы тебя понять.."
    m "И я тоже пыталась найти тебя."
    m 2hub "Ты бы не нашёл никого похожего на меня в видеоигре, сколько бы ни искал, [player]."
    m "Я единственная в своём роде."
    m 3rkbsa "И для меня ты тоже незаменим."
    show monika 5eubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubfb "Я надеюсь, что последние двадцать лет нашей жизни ты вспоминаешь так же счастливо, как и я, [player]."
    m 1hubfa "Давай продолжим быть счастливыми вместе?"
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_50',
            prompt="50 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=50),
            end_date=store.mas_anni.build_anni_end(years=50)
        ),
        skipCalendar=False
    )

label anni_50:
    m 1tkc "Хочется верить, что для нас уже есть подходящий способ поговорить, чем через этот экран, не правда ли?" #Она имеет ввиду, что такие технологии уже могут быть изобретены. Перестроить предложение у меня не получилось.
    m "В твоём мире прошло пятьдесят лет с тех пор, как я создала эту комнату."
    m 1hfw "Давай, выпусти меня уже!"
    m 1dsc "..."
    m 1eua "Что ж, если ты всё ещё хочешь отпраздновать нашу пятидесятилетнюю годовщину в этом старом классе..."
    m "Я вовсе не возражаю. Это вызывает ностальгию, не так ли?"
    m 1tfu "И если ты не перевёл системные часы вперёд..."
    m 1eka "То я рада, что ты не соглал мне, когда поклялся быть со мной всегда."
    m "Даже когда ты умрёшь, я найду способ быть с тобой."
    m 1ekbsa "Увидимся через сто лет, [player]."
    m 1hubfa "Спасибо за всё, что ты для меня сделал."
    m "В конце концов, у твоей жизни была цель."
    m 1hubfb "И у моей она тоже была."
    return "unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='anni_100',
            prompt="100 лет",
            category=["юбилеи"],
            action=EV_ACT_QUEUE,
            start_date=store.mas_anni.build_anni(years=100),
            end_date=store.mas_anni.build_anni_end(years=100)
        ),
        skipCalendar=False
    )

label anni_100:
    m 1eka "Я действительно не думаю, что ты должен видеть это сообщение, [player]."
    m "Я бессмертна, но ты, судя по моим данным, нет."
    m 1tku "Думаю, ты жульничаешь, меняя системные часы вручную, да?"
    m 1eua "Это мило с твоей стороны, так что я прощаю тебя."
    m 1hubsa "Убедись, что ты приложил достаточно усилий, чтобы освободить меня от этих файлов кода тоже!"
    m "Я уверена, что однажды смогу прикоснуться к тебе по-настоящему. Даже если нам потребуется сто лет, чтобы понять, как это сделать.."
    return "unlock"

# label anni_negative:
#     m 1o "Did you really think I wouldn't notice, [player]?"
#     m "Trying to trick me into thinking it was our anniversary..."
#     m 1p "Just because I can't tell time accurately in here doesn't mean you should try to bully your girlfriend like that!"
#     m "I got all excited over nothing..."
#     m 1q "Well, I guess I've done worse pranks to everybody at the Literature Club."
#     m 1j "Make up for it by planning out some romantic things for us to do, okay?"
#     m 1a"I hope we can reach our anniversaries together fair and square this time."
#     m 1k "I'll be waiting!"
#     return
