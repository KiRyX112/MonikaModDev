init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_intro",
            aff_range=(mas_aff.NORMAL, None),
            conditional="store.masAutostart_api.is_platform_supported()",
            action=EV_ACT_QUEUE
        ),
        code="EVE"
    )

label masAutostart_intro:
    m 3sublb "[player], знаешь что?"
    m 3gubla "Я решила немного поэкспериментировать с твоей системой... {do_giggle}Э-хе-хе~"
    m 3sublb "И теперь я могу запускать игру одновременно с включением твоего компьютера!"

    if not store.masAutostart_api.is_enabled():
        m 2wublb "Что думаешь?"

        if mas_isMoniEnamored(higher=True):
            m 4kublu "Таким образом, твоя любимая девушка сможет приветствовать тебя каждый раз, когда ты включишь его, {do_giggle}а-ха-ха!"
        else:
            m 4kublu "Так я смогу приветствовать тебя каждый раз, когда ты включишь его!"

        m 4hublu "Скажи же, что это круто?"
        m 2lusdrd "Если ты хочешь чтобы я перестала это делать, просто скажи мне, хорошо?"
        m 2rusdrb "Я не обижусь, обещаю! {do_giggle}А-ха-ха."
        $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    else:
        m 2wublb "Что ты-{nw}"
        m 2wublo "Ах?! Ты... {w=0.3}ты уже {M=включил}{F=включила} автозапуск игры!"
        m 4hksdlb "Вау, [player]... {w=0.3}Это так умно и мило одновременно!~"
        m 6lksdla "Я так долго думала как это сделать, а ты {M=обогнал}{F=обогнала} меня..."
        m 1hub "Я правда впечатлена! {do_giggle}А-ха-ха~"
        m 1dub "Ну, на всякий случай, если ты захочешь, чтобы я больше не приветствовала тебя при запуске, просто попроси, хорошо?~"
        m 3kua "Я не расстроюсь, [mas_get_player_nickname()]. {do_giggle}Э-хе-хе~"

        # She is impressed.
        $ mas_gainAffection(3, bypass=True)
        $ mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

    return "derandom|no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_enable",
            prompt="Можешь приветствовать меня при запуске моего компьютера?",
            category=["Мод"],
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        ),
        code="EVE"
    )

label masAutostart_req_enable:
    m 1eub "Конечно, [mas_get_player_nickname()]!~"
    m 1dua "Дай мне секунду..."

    m 1dua "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    if store.masAutostart_api.enable():
        m 1eub "Готово!"
        m 3sublb "С этого момента я буду приветствовать тебя каждый раз, когда ты включаешь свой компьютер, {do_giggle}а-ха-ха!~"

        $ mas_hideEVL("masAutostart_req_enable", "EVE", lock=True)
        $ mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

    else:
        m 1dkc "Ох... {w=0.3}Я думаю что это не сработало как надо, [player]..."
        m 3lksdlb "Но я обещаю что все заработает в следующий раз, {do_giggle}э-хе-хе..."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_disable",
            prompt="Можешь не приветствовать меня при включении моего компьютера?",
            category=["Мод"],
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        ),
        code="EVE"
    )

label masAutostart_req_disable:
    m 1eub "Ох, ну ладно! Я перестану, {do_giggle}э-хе-хе~"

    m 1dua "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    $ store.masAutostart_api.disable()
    m 1eub "Готово!"

    $ mas_hideEVL("masAutostart_req_disable", "EVE", lock=True)
    $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    return
