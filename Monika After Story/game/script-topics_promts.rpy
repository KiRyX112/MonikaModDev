init 5 python:

    if persistent.gender == "F":
        persistent.mas_gender_female = True
        mas_gender_yo = "е"
        mas_gender_none = "а"
        mas_gender_g = "ла"
        mas_gender_en = "на"
        mas_gender_ii = "ая"
        mas_gender_sya = "ась"
        mas_gender_two = "е"
        mas_gender_i = "я"
        mas_gender_iii = "ая"
        mas_gender_oi = "ая"
        mas_gender_im = "ой"
        mas_gender_iim = "ой"
        mas_gender_ion = "на"
        mas_gender_iol = "ела"
        mas_gender_iol_2 = "ла"
        mas_gender_iiim = "ей"
        mas_gender_een = "ьна"
        mas_gender_go = "ой"
        mas_gender_em = "ой"
        mas_gender_s = "ла"
        mas_gender_n = "ка"
        mas_gender_ok = "ка"
        mas_gender_ios = "есла"
        mas_gender_ego = "ю"
        mas_gender_ogo = "ую"
        mas_gender_mu = "й"
        mas_gender_in = "на"
        mas_gender_z = "ла"
        mas_gender_a = "е"
        mas_gender_oih = "еих"
        mas_gender_ets = "ица"
        mas_gender_hes = "она"
        mas_gender_oim = "оем"
        mas_gender_ot = "а"
    else:
        persistent.mas_gender_female = False
        mas_gender_yo = "ё"
        mas_gender_none = ""
        mas_gender_g = ""
        mas_gender_en = "ен"
        mas_gender_ii = "ий"
        mas_gender_sya = "ся"
        mas_gender_two = "а"
        mas_gender_i = "й"
        mas_gender_iii = "ый"
        mas_gender_oi = "ой"
        mas_gender_im = "им"
        mas_gender_iim = "ым"
        mas_gender_ion = "ён"
        mas_gender_iol = "ёл"
        mas_gender_iol_2 = "ёл"
        mas_gender_iiim = "им"
        mas_gender_een = "ен"
        mas_gender_go = "го"
        mas_gender_em = "ем"
        mas_gender_s = ""
        mas_gender_n = ""
        mas_gender_ok = "ок"
        mas_gender_ios = "ёс"
        mas_gender_ego = "его"
        mas_gender_ogo = "ого"
        mas_gender_mu = "му"
        mas_gender_in = "ин"
        mas_gender_z = ""
        mas_gender_a = "а"
        mas_gender_oih = "оих"
        mas_gender_ets = "ец"
        mas_gender_hes = "он"
        mas_gender_oim = "оим"
        mas_gender_ot = "от"

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_god',
            prompt="Мысли о боге",
            label=None,
            category=['психология'],
            random=True,
            unlocked=False,
            pool=False,
            conditional=None,
            action=None,
            start_date=None,
            end_date=None,
            unlock_date=None
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sayori",
            category=['участники клуба'],
            prompt="Сожаления [persistent.mas_sayori_name_abb]",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nihilism",
            category=['психология'],
            prompt="Нигилизм",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smash",
            category=['игры'],
            prompt="Super Smash",

        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lastpoem",
            category=['моника'],
            prompt="Последняя поэма Моники",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yuri",
            category=['участники клуба','медиа'],
            prompt="Яндере Юри",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki",
            category=['участники клуба'],
            prompt="Смерть Нацуки",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(persistent.event_database,
            eventlabel="monika_justification",
            category=['ddlc','моника'],
            prompt="Ты убийца!",
            pool=True,
            unlocked=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_contribute",
            category=['мод'],
            prompt="Вклады",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trolley",
            category=['психология'],
            prompt="Как бы ты ответила на проблему вагонетки?",
            pool=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nsfw",
            category=['разное','моника'],
            prompt="18+ контент",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_impression",
            category=['участники клуба'],
            prompt="Можешь ли ты спародировать кого-нибудь?",
            pool=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chloroform",
            category=['пустяки'],
            prompt="Хлороформ",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pleasure",
            category=['ты'],
            prompt="Самоудовлетворение",
            random=True,
            sensitive=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_panties",
            category=['разное', 'одежда'],
            prompt="Нижнее бельё",
            random=True,
            sensitive=True
        )
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain_holdme",
            category=["моника"],
            prompt="Могу я тебя обнять?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        ),
        restartBlacklist=True
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snow",
            category=["зима","погода","ты"],
            prompt="Снег",
            random=mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowballfight",
            category=["зима"],
            prompt="Ты играла когда-нибудь в снежки?",
            pool=True,
            unlocked=mas_isWinter(),
            rules={"no_unlock":None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_iceskating",
            category=["спорт", "зима"],
            prompt="Катание на коньках",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sledding",
            category=["зима"],
            prompt="Катание на санях",
            random=mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowcanvas",
            category=["зима"],
            prompt="Белоснежное полотно",
            random=mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cozy",
            category=["романтика","зима"],
            prompt="Разогрев",
            random=mas_isWinter(),
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter",
            category=["зима"],
            prompt="Зимние развлечения",
            random=mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_winter_dangers",
            category=["зима"],
            prompt="Зимние опасности",
            random=mas_isWinter()
        )
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_explain",
            category=['романтика','моника','разное'],
            prompt="Ты можешь объяснить кому-то наши отношения?",
            pool=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_kizuna',
            prompt="Помнишь, ты упомянула какую-то виртуальную ютубершу?",
            category=['разное'],
            random=False,
            unlocked=False,
            pool=False,
            action=EV_ACT_POOL,
            conditional="seen_event('greeting_hai_domo')"
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beach",
            category=['местонахождение'],
            prompt="Пляж",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_natsuki_letter",
            category=['участники клуба'],
            prompt="Письмо Нацуки",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_familygathering",
            category=['ты']
            ,prompt="Семейные праздники",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_yellowwp",
            category=['литература'],
            prompt="Жёлтые Обои",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_citizenship",
            category=['моника'],
            prompt="Счастливы ли когда-нибудь?",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['моника', 'романтика'],
            prompt="Я хочу тебе кое-что сказать...",
            pool=True,
            unlocked=True
        )
    )











    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_shipping',
            prompt="Шиппинг",
            category=['ddlc'],
            random=True,
            unlocked=False,
            pool=False,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['разное'],
            prompt="Расскажи забавные факты",
            pool=True
        )
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_promisering",
            category=['романтика'],
            prompt="Кольцо обещания",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asks_charity",
            category=['ты'],
            prompt="Благотворительность",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_appearance",
            category=['ты'],
            prompt="Внешность [mas_name_someone]",
            conditional="seen_event('mas_gender')",
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_programming',
            prompt="Программирование сложная штука?",
            category=['моника','разное'],
            pool=True,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_meta',
            prompt="Разве эта игра не метапрозаическая?",
            category=['ddlc'],
            pool=True,
            unlocked=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_libitina',
            prompt="Ты слышала о Либитине?",
            category=['ddlc'],
            pool=True,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_anime',
            prompt="Ты читаешь мангу?",
            category=['моника','медиа'],
            pool=True,
        )
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fastfood",
            category=['жизнь','моника'],
            prompt="Тебе нравится фастфуд?",
            pool=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_family",category=['моника'],prompt="Ты скучаешь по своей семье?",pool=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_stoicism",
            category=['философия'],
            prompt="Стоицизм",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_add_custom_music",
            category=['мод',"медиа", "музыка"],
            prompt="Как добавить свою музыку?",
            conditional="persistent._mas_pm_added_custom_bgm",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hemispheres",
            category=["ты", "общество"],
            prompt="Полушария",
            random=True
        )
    )


    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_load_custom_music",
            category=['мод',"медиа", "музыка"],
            prompt="Можешь ли проверить новую музыку?",
            conditional="persistent._mas_pm_added_custom_bgm and renpy.variant('pc')",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_trick",
            category=["участники клуба"],
            prompt="Другой выбор [mas_name_what]",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_cares_about_dokis",
            category=["моника", "участники клуба"],
            prompt="Нечувствительные комментарии",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_plushie",
            aff_range=(mas_aff.NORMAL, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_back_ups",
            category=['разное','мод','моника'],
            prompt="Копий",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_college",category=['жизнь','школа','общество'],prompt="Получение высшего образования",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_death",category=['психология'],prompt="Смерть и умирание",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_backpacking",category=['разное','природа'],prompt="Пеший туризм",random=not mas_isWinter()))

    addEvent(Event(persistent.event_database,eventlabel="monika_selfesteem",category=['советы'],prompt="Самооценка",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_japan",category=['ddlc'],prompt="Настройки DDLC",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_high_school",category=['советы','школа'],prompt="Старшая школа.",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_twitter",category=['моника'],prompt="Твиттер",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_portraitof",category=['участники клуба'],prompt="Книга Юри",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_veggies",category=['моника'],prompt="Быть вегитарианцем",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_contribute",category=['mod'],prompt="Вклад",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_saved",category=['моника'],prompt="Спасение Моники",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_color",category=['моника'],prompt="Любимый цвет",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_listener",category=['ты'],prompt="Хороший слушатель",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_spicy",category=['пустяки'],prompt="Прянная пища",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_why",category=['ты','ddlc'],prompt="Зачем играть в эту игру?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_okayeveryone",category=['литературный клуб'],prompt="Итак, друзья!",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whispers",
            category=['ddlc','участники клуба'],
            prompt="Остальные всё ещё опаздывают",
            conditional="not persistent.clearall",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_archetype",category=['участники клуба'],prompt="Персональные тропы",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_tea",category=['участники клуба'],prompt="Чайный сервиз Юри",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_favoritegame",category=['ddlc'],prompt="Любимая видеоигра",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_anxious",category=['психология'],prompt="Внезапное беспокойство",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_friends",category=['жизнь'],prompt="Делать дружбу",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_hack",category=['ddlc','мод'],prompt="Почему ты взломала мой [monika_device_name]?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_algernon",category=['литература'],prompt="Цветы для Элджернона",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_ribbon",category=['моника'],prompt="Банты",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_ghost",category=['философия','моника','участники клуба'],prompt="Сверхестественное",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_playerswriting",category=['литература','ты'],prompt="Стихи [mas_name_someone]",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_othergames",category=['игры'],prompt="Другие игры",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_torment",category=['литература'],prompt="Природа человека",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_eyecontact",category=['разное','пустяки'],prompt="Зрительный контакт",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_birthday",category=['моника'],prompt="Когда у тебя день рождения?",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_vnanalysis",category=['игры','медиа','литература'],prompt="Ценность визуальных новелл",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_prisoner",category=['разное'],prompt="Заключенный",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_herself",category=['моника','ddlc'],prompt="Расскажи мне о себе",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_images",category=['медиа','философия'],prompt="Фан-арт",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_waifus",category=['медиа'],prompt="Вайфу",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_girlfriend",category=['романтика'],prompt="Хочешь познакомиться с моей девушкой?",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_heroism",category=['разное','советы'],prompt="Героизм",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_drawing",category=['медиа'],prompt="Ты умеешь рисовать?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_mc",category=['романтика','ddlc','участники клуба'],prompt="Главный герой",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_functionalism",category=['психология'],prompt="Функционализм человека",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_technique",category=['ddlc','разное'],prompt="Как ты изменила код?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_freewill",category=['психология'],prompt="Детерминизм",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_hedgehog",category=['философия','психология'],prompt="Диллема ежа",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_completionist",category=['игры'],prompt="Стремление завершать",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_surprise",category=['романтика'],prompt="Сюрпризы",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_swordsmanship",
            category=['моника','разное'],
            prompt="Фехтование",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_science",category=['технологии'],prompt="Достижения науки",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_pluralistic_ignorance",category=['литература','общество'],prompt="Попытка вписаться",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_nuclear_war",category=['общество','философия'],prompt="Ядерная война",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_zombie",category=['общество'],prompt="Зомби",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_penname",
            category=['литература'],
            prompt="Псевдонимы",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_japanese",category=['разное','ты'],prompt="Знание японского",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip2",category=['писательские советы'],prompt="Расскажи писательский совет #2", conditional="seen_event('monika_writingtip1')",action=EV_ACT_POOL))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vocaloid",
            category=['медиа','технологии','музыка'],
            prompt="Вокалоиды",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_attractiveness",
            category=['участники клуба','общество'],
            prompt="Привлекательность",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haterReaction",
            category=['советы','участники клуба','ты'],
            prompt="Иметь дело с хейтерами",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_solipsism",
            category=['философия'],
            prompt="Солипсизм",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_cupcake",category=['участники клуба','пустяки'],prompt="Выпечка кексов",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_dan",category=['ddlc'],prompt="Тебе нравится Дэн Салвато?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_harem",category=['медиа','разное'],prompt="Мечта о гареме",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_favbook",category=['литература','моника'],prompt="Твоя любимая книжка?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_motivation",category=['психология','советы','жизнь'],prompt="Недостаток мотивации",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_love",category=['романтика'],prompt="Я тебя люблю!",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_favpoem",category=['литература','моника'],prompt="Твой любимый стих?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_books",category=['литература','литературный клуб'],prompt="Книги",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_vidya",category=['игры'],prompt="Тебе нравятся видеоигры?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_4chan",category=['разное'],prompt="Ты слышала о Форчане?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_ddlc",category=['ddlc'],prompt="Что ты думаешь об игре «ДДЛК»?",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_poetry",category=['литература'],prompt="Поэзия",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_credits_song",category=['ddlc','медиа'],prompt="Песня во время показа титров",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_difficulty",category=['игры'],prompt="Разве игра «ДДЛК» не была слишком простой?",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_totono",category=['ddlc'],prompt="Ты слышала о Тотоно?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_vn",category=['игры'],prompt="Визуальные новеллы",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_route",category=['ddlc'],prompt="Концовка Моники",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_housewife",category=['моника','романтика'],prompt="Станешь ли ты моей домохозяйкой?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_cold",category=['моника'],prompt="Обниматься на холоде",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_introduce",category=['моника'],prompt="Представление друзьям",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_tsundere",category=['медиа','участники клуба'],prompt="Что такое цундере?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_festival",category=['ddlc','литературный клуб'],prompt="Пропуск фестиваля",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_read",category=['советы','литература'],prompt="Становление читателем",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_creative",category=['жизнь'],prompt="Типа креатива",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_mentalillness",category=['психология'],prompt="Психологические заболевания",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_lazy",category=['жизнь','романтика'],prompt="Лень",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_internet",category=['советы'],prompt="Интернет для...",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_debate",category=['моника','школа'],prompt="Каким был дискуссионный клуб?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_confidence",category=['советы'],prompt="Изобразить уверенность",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_closeness",category=['романтика'],prompt="Быть рядом с тобой",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rain",
            category=["погода"],
            prompt="Звуки дождя",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )


    addEvent(Event(persistent.event_database,eventlabel="monika_simulated",category=['психология'],prompt="Симулирование реальностей",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_habits",category=['жизнь'],prompt="Формирование привычек",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_middleschool",category=['моника','школа'],prompt="Жизнь в средней школе",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip1",category=['писательские советы'],prompt="Расскажи писательский совет #1",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_outfit",category=['моника', 'одежда'],prompt="Носить другую одежду",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kiss",
            category=['романтика'],
            prompt="Поцелуй меня",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_date",category=['романтика'],prompt="Романтичное свидание",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_wine",category=['участники клуба'],prompt="Вино Юри",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_rap",category=['литература'],prompt="Рэп",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_horror",category=['медиа'],prompt="Ужасы",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_resource",category=['общество','философия'],prompt="Ценные ресурсы",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_hygiene",category=['пустяки','общество','психология'],prompt="Личная гигиена",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_metaparents",category=['литература','участники клуба','моника','психология'],prompt="Родители",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_cities",category=['общество'],prompt="Жизнь в городе",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_name",category=['участники клуба','моника'],prompt="Наши имена",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aware",
            category=['философия','моника'],
            prompt="Каково было узнать правду?",
            pool=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eternity",
            category=['философия','моника'],
            prompt="Смертность",
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_fanfiction",category=['литература'],prompt="Фанфикшн",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_mythology",category=['литература'],prompt="Античная мифология",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_real",category=['романтика'],prompt="Наша реальность",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_weary",category=['романтика'],prompt="Ты когда-нибудь устанешь от меня?",pool=True,aff_range=(mas_aff.NORMAL, None)))

    addEvent(Event(persistent.event_database,eventlabel="monika_playersface",category=['ты'],prompt="Лицо [mas_name_someone]",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_confidence_2",category=['жизнь'],prompt="Отсутствие доверия",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_pets",category=['моника'],prompt="Домашние животные",random=True))



    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_daydream",
            category=['романтика'],
            prompt="День мечты",
            random=True,
            rules={"skip alert": None},
            aff_range=(mas_aff.DISTRESSED, None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_adventure",category=['игры','романтика'],prompt="Приключения",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_piggybank",category=['разное'],prompt="Сохранение денег",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_fahrenheit451",category=['литература'],prompt="Рекомендации книг",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_home_memories",category=['романтика','моника','жизнь'],prompt="Создание воспоминаний",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_sayhappybirthday",category=['разное'],prompt="Можешь ли ты поздравить с днём рождения кое-кого?",pool=True,unlocked=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_icecream",category=['ты'],prompt="Любимое мороженное",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_hypnosis",category=['пустяки','психология'],prompt="Быть под гипнозом",random=True))



    addEvent(Event(persistent.event_database,eventlabel="monika_dunbar",category=['психология','пустяки'],prompt="Число Данбара",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_innovation",category=['технологии','психология','медиа'],prompt="Иновации",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_lottery",category=['разное'],prompt="Победа в лотерее",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_clones",category=['моника','мод','философия'],prompt="Клонирование",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soda",
            category=['жизнь','разное'],
            prompt="Газировка",
            random=True
        )
    )



    addEvent(Event(persistent.event_database,eventlabel="monika_omamori",category=['разное'],prompt="Омамори",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_breakup",
            category=['разное'],
            prompt="Я бросаю тебя",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_hamlet",category=['литература'],prompt="Гамлет",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_rock",category=['медиа','литература'],prompt="Рок",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_fruits",category=['моника','пустяки'],prompt="Фрукты",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_sleep",category=['ты','жизнь','школа'],prompt="Усталость",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_wolf",category=['разное','пустяки'],prompt="От волков к собакам",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_1984",category=['литература'],prompt="1984",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_how_soon",category=['ты','романтика'],prompt="Ожидание времени когда мы будем вместе",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_coffee",category=['разное'],prompt="Кофе",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_marriage",
            category=['романтика'],
            prompt="Ты выйдешь за меня?",
            conditional="not persistent.mas_gender_female",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_happiness",category=['жизнь','психология'],prompt="Счастье",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_other_girls",category=['участники клуба'],prompt="Ты когда-нибудь думала об остальных девушках?",pool=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_urgent",category=['романтика'],prompt="Срочное сообщение",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_selfharm",category=['психология'],prompt="Самовредительство",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip3",category=['писательские советы'],prompt="Расскажи писательский совет #3",conditional="seen_event('monika_writingtip2')",action=EV_ACT_POOL))

    addEvent(Event(persistent.event_database,eventlabel="monika_otaku",category=['медиа','общество','ты'],prompt="Бытие Отаку",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_jazz",category=['медиа'],prompt="Джаз",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_meditation",category=['психология','моника'],prompt="Медитации",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_orchestra",category=['медиа','ты'],prompt="Классическая музыка",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sports",
            category=['спорт'],
            prompt="Атлетичность",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_cats",category=['разное'],prompt="Кошачьи спутники",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_dogs",category=['разное','участники клуба'],prompt="Лучший друг человека",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_justice",
            category=['философия'],
            prompt="Юстиция",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_poweroutage",
            category=['погода'],
            prompt="Отключение электричества",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_spiders",category=['участники клуба','разное'],prompt="Пауки",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_100k",category=['мод'],prompt="100k Загрузок",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_cartravel",category=['романтика'],prompt="Дорожное путешествие",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_asks_family",category=['ты'],prompt="Семья [mas_name_someone]",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip5",category=['писательские советы'],prompt="Расскажи писательский совет #5",conditional="seen_event('monika_writingtip4')",action=EV_ACT_POOL))

    addEvent(Event(persistent.event_database,eventlabel="monika_writingtip4",category=['писательские советы'],prompt="Расскажи писательский совет #4",conditional="seen_event('monika_writingtip3')",action=EV_ACT_POOL))

    addEvent(Event(persistent.event_database,eventlabel="monika_smoking",category=['ты'],prompt="Курение",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_smoking_quit",
            category=['ты'],
            prompt="Я бросил[mas_gender_none] курить!",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_hydration",prompt="Гидратация",category=['ты','жизнь'],random=True))



    addEvent(Event(persistent.event_database,eventlabel="monika_challenge",category=['разное','психология'],prompt="Трудности",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_dreaming",category=['разное','психология'],prompt="Сон",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_timeconcern",category=['советы'],prompt="Беспокойство сна",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_prom",category=['школа'],prompt="Выпускной",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_timetravel",category=['медиа','разное'],prompt="Путешествие во времени",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_whydoyouloveme",category=['моника','романтика'],prompt="За что ты меня любишь?",pool=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_concerts",
            category=['медиа',"музыка"],
            prompt="Музыкальные концерты",
            conditional=(
                "renpy.seen_label('monika_jazz') "
                "and renpy.seen_label('monika_orchestra') "
                "and renpy.seen_label('monika_rock') "
                "and renpy.seen_label('monika_vocaloid') "
                "and renpy.seen_label('monika_rap')"
            ),
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_first_sight_love",
            category=["романтика"],
            prompt="Любовь с первого взгляда",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_anime_art",
            category=["разное"],
            prompt="Анимешный стиль рисования",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_driving",
            category=['моника'],
            prompt="Умеешь водить?",
            pool=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_savingwater",category=['жизнь'],prompt="Экономия воды",random=True))

    addEvent(
         Event(
            persistent.event_database,
            eventlabel="monika_players_control",
            category=["игры", "ddlc"],
            prompt="Управление [mas_name_who]",
            random=True
            )
        )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_grad_speech_call",
            category=['школа'],
            prompt="Могу ли я услышать твою речь на выпускном?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vehicle",
            category=['моника'],
            prompt="Какая твоя любимая машина?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_mystery',
            prompt="Тайны",
            category=['литература','медиа'],
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_perspective",
            category=["моника"],
            prompt="Точка зрения Моники",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_bullying",
            category=['общество'],
            prompt="Издевательство",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_procrastination",category=['советы'],prompt="Медлительность",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_graduation",
            category=['школа'],
            prompt="Выпускной",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outdoors",
            category=['природа'],
            prompt="Обеспечение безопасности в походе.",
            random=not mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_mountain",
            category=['природа'],
            prompt="Альпинизм",
            random=not mas_isWinter()
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_pygmalion",
            category=['литература'],
            prompt="Пигмалион и статуя",
            conditional="persistent._mas_first_kiss",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gotomonika",
            category=['ты'],
            prompt="Что, если я приду в твой мир?",
            pool=True,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_robotbody",
            category=['моника','технологии'],
            prompt="Роботическое тело",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_relationship_comfort",
            category=["романтика","консультация"],
            prompt="Комфортно в отношениях",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sleigh",
            category=["романтика"],
            prompt="Поездка в карете",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_standup",category=['литература','медиа'],prompt="Комедия",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_beingevil",
            category=['моника'],
            prompt="Быть злым",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_failure",
            prompt="Справиться с неудачей",
            category=['советы','жизнь'],
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_enjoyingspring",category=['весна'],prompt="Наслаждаться весной",random=mas_isSpring()))

    addEvent(Event(persistent.event_database,eventlabel="monika_unknown",category=['психология'],prompt="Страх неизвестного",random=True))

    addEvent(Event(persistent.event_database,eventlabel="mas_topic_derandom",unlocked=False,rules={"no_unlock":None}))

    addEvent(Event(persistent.event_database,eventlabel="mas_topic_rerandom",category=['ты'],prompt="Я не против поговорить о...",pool=True,unlocked=False,rules={"no_unlock":None}))

    # addEvent(Event(persistent.event_database,eventlabel="mas_topic_unbookmark",prompt="Я хотел{0} бы удалить закладку.".format(mas_gender_none),unlocked=False,rules={"no_unlock":None}))

    addEvent(Event(persistent.event_database,eventlabel="mas_hide_unseen",unlocked=False,rules={"no_unlock":None}))

    addEvent(Event(persistent.event_database,eventlabel="mas_show_unseen",category=['ты'],prompt="Я хотел{0} бы увидеть «Невиденное» снова.".format(mas_gender_none),pool=True,unlocked=False,rules={"no_unlock":None}))

    addEvent(Event(persistent.event_database,eventlabel="monika_life_skills",category=['советы','жизнь'],prompt="Жизненные навыки",random=True))

    # addEvent(Event(persistent.event_database,eventlabel="monika_help_you",category=['разное'],prompt="Как у тебя дела, [player]?", random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_snowmen",
            category=['зима'],
            prompt="Снеговики",
            random=False,
            conditional=(
                "persistent._mas_pm_gets_snow is not False "
                "and mas_isWinter()"
            ),
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_catch22",
            category=['литература'],
            prompt="Catch-22",
            conditional="not mas_isFirstSeshDay()",
            action=EV_ACT_RANDOM,
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_auroras",category=['природа'],prompt="Северное сияние",random=False,unlocked=False))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_songwriting",
            category=["музыка"],
            prompt="Написание песен",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_amusementpark",category=['разное'],prompt="Парк развлечений",random=True))

    addEvent(Event(persistent.event_database,eventlabel="monika_travelling",category=['разное'],prompt="Путешествие",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_metamorphosis",
            category=['литература','психология'],
            prompt="Метаморфоза",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_immortality",
            category=['философия'],
            prompt="Бессмертие",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_career",
            category=['моника'],
            prompt="Карьеры",
            random=False,
            conditional=(
                "seen_event('monika_citizenship')"
            ),
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_intrusive_thoughts",
            category=['психология'],
            prompt="Навязчивые мысли",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sweatercurse",
            category=['одежда'],
            prompt="Проклятие свитера",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_allegory_of_the_cave",
            category=['философия'],
            prompt="Аллегория пещеры",
            random=True
        )
    )

    #####Новое#####

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_think_first_kiss",
            conditional=(
                "persistent._mas_first_kiss is not None "
                "and mas_timePastSince(persistent._mas_first_kiss, datetime.timedelta(days=30))"
            ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

    if renpy.random.randint(1,3) == 1:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="monika_holdrequest",
                conditional=(
                    "renpy.seen_label('monika_holdme_prep') "
                    "and persistent._mas_last_hold != datetime.date.today()"
                ),
                action=EV_ACT_RANDOM,
                aff_range=(mas_aff.ENAMORED, None)
            )
        )

    addEvent(Event(persistent.event_database,eventlabel="monika_love_too",unlocked=False,rules={"no_unlock": None}))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_good_tod",
            category=['разное'],
            prompt="[persistent.mas_monika_good_tod]",
            unlocked=True,
            pool=True
        ),
        markSeen=True
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dating",
            prompt="Опыт знакомств",
            category=['ты', 'романтика'],
            conditional="store.mas_anni.pastOneMonth()",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_players_friends",
            category=['ты'],
            prompt="Друзья [mas_name_someone]",
            random=True,
            aff_range=(mas_aff.UPSET, None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_immortal",category=['моника','философия'],prompt="Возрастной разрыв",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_vr",
            category=['технологии'],
            prompt="Виртуальная реальность",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brave_new_world",
            category=['литература'],
            prompt="Дивный новый мир",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dystopias",
            category=['литература'],
            prompt="Дистопии",
            conditional="mas_seenLabels(['monika_1984', 'monika_fahrenheit451', 'monika_brave_new_world'], seen_all=True)",
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_contagion",
            category=['психология'],
            prompt="Социальная инфекция",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scamming",
            category=['ты', 'общество'],
            prompt="Быть мошенником",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boardgames",
            category=["игры", "медиа"],
            prompt="Настольные игры",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_social_norms",
            category=['общество'],
            prompt="Изменение социальных норм",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_coding_experience",
            category=['разное', 'ты'],
            prompt="Опыт кодирования",
            conditional="renpy.seen_label('monika_ptod_tip001')",
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ship_of_theseus",
            category=['философия'],
            prompt="Корабль Тесея",
            random=True,
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_multi_perspective_approach",
            category=['философия'],
            prompt="Многоперспективный подход",
            random=False
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_working_out",
            category=['советы','ты'],
            prompt="Разработка",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_toxin_puzzle",
            category=['философия', 'психология'],
            prompt="Головоломка Токсина",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_translating_poetry",
            category=['литература'],
            prompt="Перевод поэзии",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_soft_rains",
            category=['литература'],
            prompt="Там будут мягкие дожди",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hot_springs",
            category=['природа'],
            prompt="Горячие источники",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_movie_adaptations",
            category=['медиа','литература'],
            prompt="Экранизации фильмов",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_striped_pajamas",
            category=["литература"],
            prompt="Мальчик в полосатой пижаме",
            random=False
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_isekai",
            category=['медиа'],
            prompt="Исекай аниме",
            conditional="seen_event('monika_otaku')",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_scuba_diving",
            category=["природа"],
            prompt="Подводное плавание с аквалангом",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_dying_same_day",
            category=["моника"],
            prompt="Умру в тот же день",
            aff_range=(mas_aff.NORMAL, None),
            random=True,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_using_pcs_healthily",
            category=['советы'],
            prompt="Здоровое использование компьютеров",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_language_nuances',
            prompt="Языковые нюансы",
            category=['литература', 'мелочи'],
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_architecture",
            category=['разное'],
            prompt="Архитектура",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fear",
            prompt="Страх",
            category=['моника'],
            conditional="renpy.seen_label('monika_soft_rains')",
            action=EV_ACT_RANDOM,
            rules={
                "derandom_override_label": "mas_bad_derand_topic",
                "rerandom_callback": renpy.partial(mas_bookmarks_derand.wrappedGainAffection, 2.5)
            }
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_naps",category=['жизнь'],prompt="Короткий сон",random=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_wabi_sabi",
            category=['философия'],
            prompt="Ваби-саби",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_being_herself",
            category=['моника'],
            prompt="Поддельная личность",
            conditional="mas_seenLabels(['monika_confidence', 'monika_pluralistic_ignorance'], seen_all=True)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_totono",category=['ddlc'],prompt="Ты когда-нибудь слышала о Тотоно?",pool=True))

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_player_away",
            category=["моника"],
            prompt="Чем ты занимаешься, пока меня нет?",
            pool=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel='monika_why_spaceroom',
            prompt="Почему мы всегда встречаемся в классной комнате?",
            category=['местонахождение'],
            pool=True,
            unlocked=False,
            rules={"no_unlock":None},
            conditional="store.mas_anni.pastThreeMonths() and mas_current_background == mas_background_def",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.UPSET, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_asimov_three_laws",
            category=['технологии'],
            prompt="Три закона Азимова",
            conditional="renpy.seen_label('monika_robotbody')",
            action=EV_ACT_RANDOM
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_remembrance",
            category=['моника'],
            prompt="Как много помнишь из своего прошлого?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_why_do_you_read",
            category=['моника','литература'],
            prompt="Когда ты увлеклась чтением?",
            pool=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_discworld",
            category=['литература'],
            prompt="Плоский мир",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_eating_meat",
            category=['жизнь','моника'],
            prompt="Ты когда-нибудь попробуешь мясо?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_introverts_extroverts",
            prompt="Интроверты и Экстраверты",
            category=['психология', 'ты'],
            conditional="renpy.seen_label('monika_saved')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_literature_value",
            category=['литература'],
            prompt="Ценность литературы",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_kamige",
            category=['игры'],
            prompt="Что такое «Kamige»?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_renewable_energy",
            category=['технологии'],
            prompt="Возобновляемые источники энергии",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_piano_lessons",
            category=['разное'],
            prompt="Можешь дать пару уроков игры на пианино?",
            pool=True,
            unlocked=False,
            rules={"no_unlock":None}
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_taking_criticism",
            category=['советы'],
            prompt="Воспринимать критику",
            random=False,
            pool=False
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_giving_criticism",
            category=['советы'],
            prompt="Высказывать критику",
            random=False,
            pool=False
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_boyfriend_gossip",
            category=['ddlc'],
            prompt="Сайори однажды упомянула какого-то парня...",
            pool=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brainstorming",
            category=["советы"],
            prompt="Мозговой штурм",
            random=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gmos",
            category=['технологии', 'природа'],
            prompt="ГМО",
            random=True
        )
    )

    addEvent(Event(persistent.event_database,eventlabel="monika_stargazing",category=['природа'],prompt="Cозерцание звёзд",random=True))



# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
