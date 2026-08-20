init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=["Pinterest"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Что-то новое сегодня, [player]?",
            "Что-нибудь интересное, [player]?",
            "Смотришь всё, что тебе нравится?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=["Duolingo"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Учишься по-новому говорить «Я люблю тебя», [player]?",
            "Изучаешь новый язык, [player]?",
            "Какой язык ты изучаешь, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=["- Wikipedia"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "Изучаешь, что-нибудь новое, [player]?",
        "Проводишь небольшое иследование, [player]?"
    ]


    python:
        wind_name = mas_getActiveWindowHandle()
        try:
            cutoff_index = wind_name.index(" - Wikipedia")
            
            
            
            wiki_article = wind_name[:cutoff_index]
            
            
            wiki_article = re.sub("\\s*\\(.+\\)$", "", wiki_article)
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nОчень интересно, [player]."))

        except ValueError:
            pass

    $ wrs_success = mas_display_notif(
        m_name,
        wikipedia_reacts,
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_virtualpiano",
            category=["^Virtual Piano"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_virtualpiano:
    python:
        virtualpiano_reacts = [
            "Ах-х, ты хочешь сыграть со мной?\nТы такой милый~",
            "Сыграй, что-нибудь для меня, [player]!"
        ]

        if mas_isGameUnlocked("пианино"):
            virtualpiano_reacts.append("Тебе нужно пианино побольше, я права?\nА-ха-ха~")

        wrs_success = mas_display_notif(
            m_name,
            virtualpiano_reacts,
            'Window Reactions'
        )

        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_virtualpiano')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=["- YouTube"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Что ты смотришь, [mas_get_player_nickname()]?",
            "Смотришь, что-нибудь интересное, [mas_get_player_nickname()]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=[r"(?i)(((r34|rule\s?34).*monika)|(post \d+:[\w\s]+monika)|(monika.*(r34|rule\s?34)))"],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    python:
        mas_display_notif(m_name, ["Эй, [player]...на что ты такое смотришь там?"],'Window Reactions')

        choice = random.randint(1,10)

        if choice == 1 and mas_isMoniNormal(higher=True):
            MASEventList.queue('monika_nsfw')

        elif choice == 2 and mas_isMoniAff(higher=True):
            MASEventList.queue('monika_pleasure')

        else:
            if mas_isMoniEnamored(higher=True):
                if choice < 4:
                    exp_to_force = "1rsbssdlu"
                elif choice < 7:
                    exp_to_force = "2tuu"
                else:
                    exp_to_force = "2ttu"
            else:
                if choice < 4:
                    exp_to_force = "1rksdlc"
                elif choice < 7:
                    exp_to_force = "2rssdlc"
                else:
                    exp_to_force = "2tssdlc"
            
            mas_moni_idle_disp.force_by_code(exp_to_force, duration=5)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=["MonikaModDev"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "О-у-у-у, ты делаешь, что-то для меня?\nТы такой милый~",
            "Ты делаешь всё, что бы я могла попасть в твою реальность?\nТы такой милый, [player]~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=["/ Twitter"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("Я люблю тебя, [mas_get_player_nickname(exclude_names=['любимый', 'мой любимый'])].")
        temp_len = len(temp_line)


        ily_quips_map = {
            "Смотришь, чем бы мог со мной поделиться, [player]?": False,
            "Хочешь чем-то поделиться со мной, [player]?": False,
            "280 символов? А мне нужно только [temp_len]...\n[temp_line]": True
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = mas_display_notif(
            m_name,
            [quip],
            'Window Reactions'
        )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None



















label mas_wrs_monikatwitter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Ты здесь, чтобы признаться в любви ко мне перед всем миром, [player]?",
            "Ты не шпионишь за мной, м?\nА-ха-ха, просто шучу~",
            "Мне всё равно, сколько у меня подписчиков, пока у меня есть ты~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=["- 4chan"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:

    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Так это то место, где всё началось, да?\nЭто... правда нечто.",
            "Надеюсь, ты не будешь весь день спорить с другими пользователями, [player].",
            "Я слышала, здесь есть темы, посвященные Литературному клубу.\nПередай им от меня привет~",
            "Я буду следить за досками, которые ты просматриваешь, если у тебя появятся какие-либо идеи, а-ха-ха!",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=["- pixiv"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:

    python:
        pixiv_quips = [
            "Интересно, рисовали ли люди меня...\nМожешь посмотреть некоторые?\nНе забудь сохранить понравившиеся~",
            "Это довольно интересное место... так много опытных людей размещают свои работы.",
        ]


        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Это довольно интересное место... так много опытных людей размещают свои работы.\nТы случайно, не один из них, [player]?",
            ])
            
            
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "Ты здесь, что бы разместить свой рисунок меня, [player]?",
                    "Публикуешь, что-то, что ты нарисовал со мной?",
                ])

        wrs_success = mas_display_notif(
            m_name,
            pixiv_quips,
            'Window Reactions'
        )


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=[r"(?i)reddit"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Ты нашёл хорошие посты, [player]?",
            "Просматриваешь Reddit? Просто убедись, что ты не тратишь весь день на просмотр мемов, хорошо?",
            "Интересно, есть ли какие-нибудь сабреддиты, посвящённые мне...\nА-ха-ха, просто шучу, [player].",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=["MyAnimeList"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Может быть, когда-нибудь мы сможем вместе посмотреть аниме, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("Итак, ты любишь аниме и мангу, [player]?")

        wrs_success = mas_display_notif(m_name, myanimelist_quips, 'Window Reactions')


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=["DeviantArt"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Здесь так много талантливых людей!",
            "Я хотела бы научиться рисовать когда-нибудь...",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=["Netflix"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Я бы хотела посмотреть романтический фильм с тобой [player]!",
            "Что ты смотришь сегодня, [player]?",
            "Что ты собираешься смотреть [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=["- Twitch"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Смотришь стрим, [player]?",
            "Не возражаешь, если я посмотрю с тобой?",
            "Что мы сегодня смотрим, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_word_processor",
            category=['Google Docs|LibreOffice Writer|Microsoft Word'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_word_processor:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Пишешь какую-то историю?",
            "Делаешь заметки, [player]?",
            "Пишешь стих?",
            "Пишешь кому-то любовное письмо?~"
        ],
        'Window Reactions'
    )

    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_word_processor')
    return



init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_vkgroup",
            category=['rg', 'smoking', 'room'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_vkgroup:
    $ wrs_success = display_notif(
        m_name,
        [
            "О, это же те самые ребята!",
            "Интересно, когда новая версия?",
            "Я благодарна им, за то, что они делают для меня."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_vkgroup')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_crunchyroll",
            category=[r"(?i)crunchyroll"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_crunchyroll:
    python:
        if persistent._mas_pm_watch_mangime is False:
            crunchyroll_quips = [
                "О! Так ты любишь аниме, [player]?",
                "Приятно видеть, что ты расширяешь свой кругозор.",
                "Хм, интересно, что привлекло твоё внимание?",
            ]

        else:
            crunchyroll_quips = [
                "Какое аниме мы смотрим сегодня, [player]?",
                "Смотришь аниме, [player]?",
                "Я не могу дождаться, чтобы посмотреть аниме с тобой!~",
            ]

        wrs_success = mas_display_notif(m_name, crunchyroll_quips, 'Window Reactions')

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_crunchyroll')
    return
