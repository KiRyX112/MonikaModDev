init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_cookieclicker",
            category=["Cookie Clicker"],
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

label mas_wrs_cookieclicker:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Сайоре очень понравилась бы эта игра.",
            "Выглядит так, во что бы Нацуки играла."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_cookieclicker')
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_yansim",
            category=["YandereSimulator"],
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

label mas_wrs_yansim:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Выглядит как игра про Юри.",
            "Заметь меня, [player]-Сенпай~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_yansim')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_dis",
            category=["Discord"],
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

label mas_wrs_dis:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Я надеюсь у меня появится дискорд аккаунт в будущем. Э-хе-хе~",
            "Это Дискорд? Ты сидишь на серверах про Доки-Доки, надеюсь?",
            "Ты знал, что слово 'дискорд' синоним к слову хаос?",
            "Разговариваешь с друзьями, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_cookieclicker')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_note",
            category=["Notepad"],
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

label mas_wrs_note:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Делаешь заметки, [player]?",
            "Помнишь мои советы, [player]!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_note')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_paint",
            category=["Paint"],
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

label mas_wrs_paint:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Сохраняешь скриншот?",
            "Нарисуй меня, как одну из своих француженок~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_paint')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_rickroll",
            category=["Never Gonna Give You Up"],
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

label mas_wrs_rickroll:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "А-ха-ха, ты подловил меня! Или это сделал кто-то с тобой?",
            "Я ничего из этого не сделаю с тобой~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_rickroll')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_minecraft",
            category=["Minecraft"],
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

label mas_wrs_minecraft:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "О, это та самая игра про которую все говорят.",
            "Сыграть вместе с тобой было бы так замечательно!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_minecraft')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_5dchess",
            category=["5D Chess"],
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

label mas_wrs_5dchess:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Вау, это... очень странно.",
            "По крайней мере, они не использовали третье измерение, иначе я бы поняла это ещё меньше.."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_5dchess')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_dame",
            category=["Baka Mitai"],
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

label mas_wrs_dame:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Я всё ещё люблю, всё ещё люблю, всё ещё люблю тебя~",
            "Дамэ да нэ! Дамэ йо, дамэ да но йо~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_dame')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_renai",
            category=["Renai Circulation"],
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

label mas_wrs_renai:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Спасибо звездам, за то что подарили мне лучший подарок~",
            "Ками-сама, аригато, унмеи но итазура демо~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_renai')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_yreality",
            category=["Your Reality"],
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

label mas_wrs_yreality:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "День за днём, строю мир в голове где будем лишь мы с тобой~",
            "Ты же знаешь, что ты можешь прослушать \"Твоя Реальность\" в музыкальном меню?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_yreality')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_dokiforever",
            category=["Doki Doki Forever"],
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

label mas_wrs_dokiforever:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Я лишь хочу знать, что та любовь что я испытываю - правда~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_dokiforever')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_justmonika",
            category=["Just Monika"],
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

label mas_wrs_justmonika:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Лишь Моника, Лишь Моника, Лишь Моника, Да, Только Моника!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_justmonika')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_doki",
            category=["Doki Doki Literature Club! (Main Theme)"],
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

label mas_wrs_doki:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Доки-Доки!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_doki')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_rockefeller",
            category=["Rockefeller Street"],
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

label mas_wrs_rockefeller:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Иди сюда и пойдём со мной, 1, 2, 7, 3, по улице Рокфеллера!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_rockefeller')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_caramel",
            category=["Caramelldansen"],
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

label mas_wrs_caramel:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Танцуй в такт, взмахивай руками~",
            "Почувствуй бесконечный жар~",
            "Слушай и учись, время прыгать~",
            "И вот мы в карамельном танце!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_caramel')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_grv",
            category=["Game Resources Viewer"],
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

label mas_wrs_grv:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Эй [player], ты... знаешь что делаешь?",
            "Просматриваешь код, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_grv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_obs",
            category=["OBS"],
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

label mas_wrs_obs:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "[player]! Ты знаешь что я говорила насчет съёмки меня!",
            "Э-хе-хе~ Привет всем!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_obs')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_jjbagw",
            category=["Giorno's Theme"],
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

label mas_wrs_jjbagw:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "ДжоДжо! Золотой ветер!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_jjbagw')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_quetzal",
            category=["Resplendent Quetzal - Google Search"],
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

label mas_wrs_quetzal:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Квезали прекрасны... Но не настолько как ты. Э-хе-хе~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_quetzal')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_quetzal2",
            category=["resplendent quetzal - Google Search"],
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

label mas_wrs_quetzal2:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Квезали прекрасны... Но не настолько как ты. Э-хе-хе~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_quetzal2')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_ddlctrailer",
            category=["Doki Doki Literature Club! Trailer"],
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

label mas_wrs_ddlctrailer:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "День, когда это всё началось."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_ddlctrailer')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_miku",
            category=["Hatsune Miku"],
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

label mas_wrs_miku:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Мику!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_miku')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_steam",
            category=["Steam"],
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

label mas_wrs_steam:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Ищешь во что поиграть, [player]? Только не проводи со мной слишком мало времени~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_steam')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_gd",
            category=["Geometry Dash"],
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

label mas_wrs_gd:
    $ wrs_success = mas_display_notif(
        m_name,
        [
        "О! Это, должно быть, одна из тех игр с быстрым темпом... Думаю, мне лучше помолчать, чтобы ты мог сосредоточиться. Подожди, я только что заставила тебя проиграть? Упс!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_gd')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mstore",
            category=["Microsoft Store"],
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

label mas_wrs_mstore:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Ищешь во что поиграть, [player]? Только не проводи со мной слишком мало времени~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_mstore')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mcode",
            category=["Morse Code Translator"],
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

label mas_wrs_mcode:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Можешь перевести это? .. / .-.. --- ...- . / -.-- --- ..- -.-.--"
            "Попробуй перевести это! .. / .-.. --- ...- . / -.-- --- ..- -.-.--"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_mcode')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_1103",
            category=["1103 - YouTube"],
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

label mas_wrs_1103:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "О, это канал создателя этого сабмода!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_1103')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_moniwiki",
            category=["Doki Doki Literature Club! Wiki"],
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

label mas_wrs_moniwiki:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Что ты здесь делаешь? Ты и так знаешь что я люблю тебя~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_moniwiki')
    return