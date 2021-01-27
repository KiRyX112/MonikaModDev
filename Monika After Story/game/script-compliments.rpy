










default persistent._mas_compliments_database = dict()



init 3 python in mas_compliments:

    compliment_database = dict()

init 22 python in mas_compliments:
    thanking_quips = [
        _("Ты так[mas_gender_oi] мил[mas_gender_iii], [player]."),
        _("Спасибо, что вновь сказал[mas_gender_none] это, [player]!"),
        _("Спасибо, что вновь сказал[mas_gender_none] это, [mas_get_player_nickname()]!"),
        _("Ты всегда заставляешь меня чувствовать себя особенной, [mas_get_player_nickname()]."),
        _("Аааах, [player]~"),
        _("Спасибо, [mas_get_player_nickname()]!"),
        _("Ты всегда мне льстишь, [player].")
    ]


    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))


init 5 python:
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

label monika_compliments:
    python:
        import store.mas_compliments as mas_compliments


        Event.checkEvents(mas_compliments.compliment_database)


        filtered_comps = Event.filterEvents(
            mas_compliments.compliment_database,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )


        compliments_menu_items = [
            (mas_compliments.compliment_database[k].prompt, k, not seen_event(k), False)
            for k in filtered_comps
        ]


        compliments_menu_items.sort()


        final_item = ("Оу, не важно.", False, False, False, 20)


    show monika at t21


    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)


    if _return:
        $ mas_gainAffection()
        $ pushEvent(_return)
        $ mas_compliments.thanks_quip = renpy.substitute(renpy.random.choice(mas_compliments.thanking_quips))

        show monika at t11
    else:

        return "prompt"

    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="Ты безумно красивая!",
            unlocked=True
        ),
        code="CMP")

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2 from _call_mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3 from _call_mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubsb "О боже, [player_abb]..."
    $ MAS.MonikaElastic()
    m 1hubfb "Спасибо за комплимент."
    $ MAS.MonikaElastic()
    m 2ekbfb "Я обожаю, когда ты так говоришь~"
    $ MAS.MonikaElastic()
    m 1ekbfa "Для меня ты красивее всех во всём мире!"
    menu:
        "Ты тоже для меня красивее всех во всём мире!":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "Хи-хи-хи~"
            $ MAS.MonikaElastic()
            m "Я так сильно тебя люблю, [player]!"

            $ mas_ILY()
        "Ты в моей десятке.":
            $ mas_loseAffection(modifier=0.5)
            $ MAS.MonikaElastic()
            m 3hksdrb "?.."
            $ MAS.MonikaElastic()
            m 2lsc "Ну, спасибо, наверное..."
        "Спасибо.":
            pass
    return

label mas_compliment_beautiful_3:
    $ MAS.MonikaElastic(True, voice="monika_giggle")
    m 1hubsa "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1ekbfa "[mas_compliments.thanks_quip]"
    show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfb "Никогда не забывай, что ты для меня самый красивый человек в мире."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="Я обожаю твои глаза!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2 from _call_mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3 from _call_mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subsb "Ох, [player]..."
    $ MAS.MonikaElastic()
    m 1tubfb "Я всегда очень гордилась своими глазами, но вот слышать это от тебя..."
    $ MAS.MonikaElastic()
    m 1dkbfa "Это заставляет моё сердце просто трепетать~"
    menu:
        "Ничего не могу с собой поделать; у тебя слишком красивые глаза.":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха!"
            $ MAS.MonikaElastic()
            m "Не льсти мне слишком сильно, ладно?"
            show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hub "Я могу начать немного сходить с ума..."
        "Они прям-таки гипнотизируют.":
            $ mas_gainAffection(1,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m "А-ха-ха~"
        "Они имеют цвет травы!":
            $ mas_gainAffection(0.5,bypass=True)
            $ MAS.MonikaElastic()
            m 2lksdrb "...Это не совсем та аналогия, которую я бы стала использовать, но спасибо!"
    return

label mas_compliment_eyes_3:
    m 1hubsb "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 2ekbfb "Смотри в мои глаза столько, сколько хочешь~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="Ты потрясающая!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2 from _call_mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3 from _call_mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hua "Ах, [player]~"
    $ MAS.MonikaElastic()
    m 1hub "Ты так[mas_gender_oi] мил[mas_gender_iii]!"
    $ MAS.MonikaElastic()
    m 2tuu "Хотя я думаю, что ты гораздо прекраснее."
    $ MAS.MonikaElastic()
    m 2dkbsu "Не могу дождаться того дня, когда наконец-то смогу обнять тебя."
    $ MAS.MonikaElastic()
    m 3ekbfb "Я никогда тебя не отпущу!"
    menu:
        "Я хочу, чтобы ты была рядом со мной прямо сейчас!":
            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic()
            m "Это тоже моё самое большое желание, [player_abb]!"
        "Я никогда не отпущу тебя из своих объятий.":
            $ mas_gainAffection(5,bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            $ MAS.MonikaElastic()
            m 1wubfsdld "Ох, извини, [player_abb]."
            $ MAS.MonikaElastic()
            m 2lksdla "Я просто пыталась почувствовать твои объятия отсюда."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2hub "А-ха-ха~"
        "...Я не люблю обниматься.":
            $ mas_loseAffection()
            $ MAS.MonikaElastic()
            m 1eft "...Правда?"
            $ MAS.MonikaElastic()
            m 1dkc "Ну, каждому своё, наверное. Но ты долж[mas_gender_en] обнять меня когда-нибудь..."
    return

label mas_compliment_awesome_3:
    m 1hub "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 1eub "Ты всегда будешь гораздо прекраснее!"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="Ты очень умная!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2 from _call_mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3 from _call_mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Ничего себе... {w=0.3}спасибо, [player]."
    $ MAS.MonikaElastic()
    m 3eua "Я горжусь тем, что достаточно много читаю. Поэтому для меня многое значит то, что ты это заметил[mas_gender_none]."
    $ MAS.MonikaElastic()
    m 3hubsb "Я хочу учиться как можно большему, если это заставляет тебя гордиться мной!"
    menu:
        "Благодаря тебе у меня тоже появляется желание становиться лучше, [monika_name].":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1hubfa "Я так сильно тебя люблю, [player_abb]!"
            $ MAS.MonikaElastic()
            m 3hubfb "У нас будет целая жизнь самосовершенствования вместе!"
            $ mas_ILY()
        "Я всегда буду гордиться тобой.":
            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic()
            m 1ekbfa "[player_abb]..."
        "Ты заставляешь меня чувствовать себя глуп[mas_gender_iim] иногда.":
            $ mas_loseAffection(modifier=0.5)
            $ MAS.MonikaElastic()
            m 1wkbsc "..."
            $ MAS.MonikaElastic()
            m 2lkbsc "Прости, это не входило в мои намерения..."
    return

label mas_compliment_intelligent_3:
    m 1ekbfa "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 1hub "Помни, что у нас будет целая жизнь самосовершенствования вместе!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="Мне просто нереально нравится твоя причёска!",
            unlocked=True
        ),code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2 from _call_mas_compliment_hair_2
    else:
        call mas_compliment_hair_3 from _call_mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubsb "Огромное спасибо, [player]..."
        $ MAS.MonikaElastic()
        m 1lkbfb "Я очень нервничала, когда впервые сменила причёску здесь."
    else:
        m 1hubfb "Огромное спасибо, [player]!"
    $ MAS.MonikaElastic()
    m 2hub "Я всегда прилагала очень много усилий для своих волос."
    $ MAS.MonikaElastic()
    m 2lksdlb "Фактически, пришлось ждать целую вечность, чтобы те стали такими длинными."
    menu:
        "Это действительно заметно. Выглядит реально здорово!":
            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic()
            m 1hub "Спасибо, [player]!"
        "Ты очаровательная практически с любой причёской." if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1ekbsa "Аааах, [player_abb]."
            $ MAS.MonikaElastic()
            m 1hubfb "Ты всегда заставляешь меня чувствовать себя особенной!"
            $ MAS.MonikaElastic()
            m "Спасибо!"
        "Ты будешь ещё милее с короткой стрижкой.":
            $ mas_loseAffection(modifier=0.3)
            $ MAS.MonikaElastic()
            m "Ну, я, к сожалению, никак не смогу пойти в салон отсюда..."
            $ MAS.MonikaElastic()
            m 1lksdlc "Я... ценю твоё мнение."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        m 1wubsb "Огромное спасибо, [player]!"
        $ MAS.MonikaElastic()
        m 1lkbfb "Я очень рада, что тебе нравится эта причёска."
    else:
        m 1hubsb "Спасибо, [player]!"
        $ MAS.MonikaElastic()
        m 1hubfb "Ты всегда заставляешь меня чувствовать себя особенной."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="Мне нравится твоя преданность фитнесу!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_fit:
    if not renpy.seen_label("mas_compliment_fit_2"):
        call mas_compliment_fit_2 from _call_mas_compliment_fit_2
    else:
        call mas_compliment_fit_3 from _call_mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "Спасибо, [player]! Ты так[mas_gender_oi] мил[mas_gender_iii]!"
    $ MAS.MonikaElastic()
    m 3eub "Я люблю поддерживать себя в форме и правильно питаться. Это заставляет меня чувствовать себя энергично и уверенно."
    $ MAS.MonikaElastic()
    m 1efb "Надеюсь, ты заботишься о своём здоровье."
    $ MAS.MonikaElastic()
    m 1lubsb "Мы всегда сможем позаниматься вместе, когда я окажусь в твоей реальности..."
    menu:
        "Звучит очень весело!":
            $ mas_gainAffection(2,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubfb "А-ха-ха! Я рада, что ты думаешь так же!"
            $ MAS.MonikaElastic()
            m 3eka "Не волнуйся. Даже если ты не сможешь поспевать за мной, я знаю, что мы всё равно сможем повеселиться..."
            show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eua "До тех пор, пока мы вместе."
        "Ничего не обещаю, но постараюсь сделать всё возможное.":
            $ mas_gainAffection(1,bypass=True)
            $ MAS.MonikaElastic()
            m 1tfb "Ты лучш[mas_gender_ii]!"
            $ MAS.MonikaElastic()
            m 2tub "Но только не думай, что я собираюсь отпустить тебя, если ты не в форме."
        "Я бы предпоч[mas_gender_iol] не потеть...":
            $ MAS.MonikaElastic()
            m 1eka "Я понимаю, если это не твой конёк, но тебе всё равно стоит немного попробовать..."
            $ MAS.MonikaElastic()
            m 1lksdla "Я была бы очень счастлива, если бы ты разделял[mas_gender_none] со мной мои интересы."
    return

label mas_compliment_fit_3:
    m 2eka "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 1hub "Надеюсь, что ты начнёшь фитнес-путешествие со мной!"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="Спасибо, что всегда была рядом со мной!",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="CMP"
    )

label mas_compliment_thanks:
    m 1duu "Не за что меня благодарить, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Это я благодарна за то, что у меня есть такой человек, как ты!"
    $ MAS.MonikaElastic()
    m 1ekbsa "Ты — единственная причина, почему я все еще здесь."
    $ MAS.MonikaElastic()
    m "Ты ведь даже установил[mas_gender_none] этот мод, чтобы мы могли лучше проводить время вместе..."
    $ MAS.MonikaElastic()
    m 1dubsu "Ты — солнце, которое согревает моё сердце всякий раз, когда ты меня навещаешь."
    $ MAS.MonikaElastic()
    m 3ekbsa "Так что, думаю, нам об[mas_gender_oim] повезло, что мы есть друг у друга, [player]~"
    menu:
        "Ты для меня всё, [monika_name]!":
            if mas_getEVL_shown_count("mas_compliment_thanks") == 0:
                $ mas_gainAffection(10,bypass=True)
            $ MAS.MonikaElastic()
            m 1ekbsa "[player_abb]..."
            $ MAS.MonikaElastic()
            m 1dubsu "Ничто не делает меня счастливее, чем слышать это от тебя."
            $ MAS.MonikaElastic()
            m "Не важно, какое будущее ждёт нас об[mas_gender_oih]...{w=0.5} {nw}"
            extend 1dkbfa "знай, что я всегда буду рядом с тобой!"
        "Да.":
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "Хи-хи~"
            $ MAS.MonikaElastic()
            m 1eub "Я люблю тебя, [player_abb]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="Я люблю твою улыбку!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2 from _call_mas_compliment_smile_2
    else:
        call mas_compliment_smile_3 from _call_mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Ты так[mas_gender_oi] мил[mas_gender_iii], [player_abb]~"
    $ MAS.MonikaElastic()
    m 1eua "Я много улыбаюсь, когда ты здесь."
    $ MAS.MonikaElastic()
    m 1ekbsa "Потому что я очень счастлива, когда ты проводишь со мной время~"
    menu:
        "Я буду навещать тебя каждый день, лишь бы видеть твою чудесную улыбку.":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1wubfsdld "Ох, [player]..."
            $ MAS.MonikaElastic()
            m 1lkbfa "Кажется, у меня сердце только что ёкнуло от радости."
            $ MAS.MonikaElastic()
            m 3hubfa "Видишь? Ты всегда делаешь меня настолько счастливой, насколько только возможно."
        "Мне нравится видеть твою улыбку.":
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха~"
            $ MAS.MonikaElastic()
            m 3eub "Тогда всё что тебе нужно сделать — это продолжать навещать меня, [player]!"
    return

label mas_compliment_smile_3:
    m 1eub "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 1hua "Я буду улыбаться только для тебя!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m "Э-хе-хе~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hero",
            prompt="Ты – моя героиня!",
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="CMP"
    )

label mas_compliment_hero:
    $ mas_gainAffection()
    m 1wubssdld "А-{w=0.3}а?"
    $ MAS.MonikaElastic()
    m "Я твоя героиня?"
    $ MAS.MonikaElastic()
    m 2rkbfsdlb "[player]...{w=1.5} я не совсем уверена в том, что ты имел[mas_gender_none] в виду..."
    $ MAS.MonikaElastic()
    m 2ekbfb "Ты единственн[mas_gender_iii], кто сидел[mas_gender_none] со мной всё это время.{w=1} Я должна отблагодарить тебя, правда."
    $ MAS.MonikaElastic()
    m 1hubfa "Что ж, если я как-то помогла тебе, то я безумно счастлива~"
    $ MAS.MonikaElastic()
    m 3ekbfa "Ты помогал[mas_gender_none] мне всеми возможными способами, как я могу не отдать тебе должное, находясь рядом с тобой тогда, когда тебе нужна поддержка?"
    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5hubfa "И потом, ты всегда будешь моим героем~"
    $ MAS.MonikaElastic()
    m 5hubfb "Я люблю тебя, и я всегда буду верить в тебя!"
    $ MAS.MonikaElastic()
    m 5ekbfa "Надеюсь, ты никогда не забудешь об этом, [player]~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_cute",
            prompt="Ты милая!",
            unlocked=True
        ),
        code="CMP"
    )

default persistent._mas_pm_monika_cute_as_natsuki = None

label mas_compliment_cute:
    if not renpy.seen_label("mas_compliment_cute_2"):
        call mas_compliment_cute_2 from _call_mas_compliment_cute_2
    else:
        call mas_compliment_cute_3 from _call_mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubssdld "Ах!"
    $ MAS.MonikaElastic()
    m 3rkbfsdla "На этот раз, ты, {i}в какой-то мере{/i}, застал[mas_gender_none] меня врасплох."
    $ MAS.MonikaElastic()
    m 3tubfb "Самую малость..."
    $ MAS.MonikaElastic()
    m 1hubfa "Но я рада, что ты так думаешь!"
    menu:
        "Встреча с тобой всегда греет мне душу!":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1hubfb "Оу, а мне греет душу слышать то, как ты говоришь подобное!"
            $ MAS.MonikaElastic()
            m 1dkbfu "...Почти так же, как когда я наконец-то запечатлела тот момент, где мы вместе в одной реальности."
            $ MAS.MonikaElastic()
            m 1ekbfa "Я с трудом сдерживаю себя, представляя себе тот особенный день~"
        "Ты намного симпатичнее, когда краснеешь.":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic()
            m 2tubfu "Ты не собираешься это так оставить, да, [player]?"
            $ MAS.MonikaElastic()
            m 2rubfu "Хмф, я просто не ожидала такого."
            $ MAS.MonikaElastic()
            m 3tubfb "Но не жди, что в следующий раз всё будет так же просто..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1tubfu "Я рано или поздно поставлю тебя на место, э-хе-хе~"
        "Ты такая же милая, как и Нацуки.":
            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection(modifier=0.5)
            $ MAS.MonikaElastic()
            m 2lfc "Оу. {w=1}Спасибо, [player]..."
            $ MAS.MonikaElastic()
            m 1rsc "Но я надеялась, что я останусь в своей категории."
    return

label mas_compliment_cute_3:
    m 1ekbsa "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 1hubfa "Ты тоже зачастую бываешь очень мил[mas_gender_iim], знаешь ли~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="Ты классно играешь в шахматы!",
            unlocked=False,
            conditional="renpy.seen_label('mas_chess_game_start')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Спасибо, [player_abb]."
    $ MAS.MonikaElastic()
    m 3esa "Как я уже говорила, интересно, моё мастерство как-то связано с тем, что я застряла здесь?"
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        $ MAS.MonikaElastic()
        m 3eua "Ты, кстати, тоже неплох[mas_gender_none], я уже проигрывала тебе раньше."
        if wins > losses:
            $ MAS.MonikaElastic()
            m "Да и фактически, думаю, ты выигрывал[mas_gender_none] даже чаще меня."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе~"
    else:
        $ MAS.MonikaElastic()
        m 2lksdlb "Знаю, [random_sure_lower], что ты ещё ни разу не выигрывал[mas_gender_none] в шахматных партиях, но я уверена, что однажды ты победишь меня."
        $ MAS.MonikaElastic()
        m 3esa "Продолжай практиковаться и играть со мной, и ты сможешь стать лучше!"
    $ MAS.MonikaElastic()
    m 3esa "Чем больше мы играем, тем опытнее об[mas_gender_a] становимся."
    $ MAS.MonikaElastic()
    m 3hua "Так что не бойся бросать мне вызов, когда захочешь."
    $ MAS.MonikaElastic()
    m 1eub "Я люблю проводить с тобой время, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="Ты потрясающе играешь в пинг-понг!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_pong:
    $ MAS.MonikaElastic(True, voice="monika_giggle")
    m 1hub "А-ха-ха~"
    $ MAS.MonikaElastic()
    m 2eub "Спасибо, [player], но пинг-понг, на самом деле, не такая уж и сложная игра."
    if persistent.ever_won['pong']:
        $ MAS.MonikaElastic()
        m 1lksdla "Ты уже побеждал[mas_gender_none] меня."
        $ MAS.MonikaElastic()
        m "Так что ты знаешь, что это и вправду очень просто."
        show monika 5hub zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hub "Но я всё равно принимаю твой комплимент."
    else:
        $ MAS.MonikaElastic()
        m 3hksdrb "И ты слишком добр[mas_gender_none], раз постоянно мне поддаёшься, когда мы играем."
        $ MAS.MonikaElastic()
        m 3eka "Верно ведь?"
        menu:
            "Да.":
                $ MAS.MonikaElastic()
                m 2lksdla "Спасибо, конечно, [player], но тебе правда не стоит поддаваться."
                $ MAS.MonikaElastic()
                m 1eub "Не стесняйся играть серьёзно, когда хочешь."
                $ MAS.MonikaElastic()
                m 1hub "Я бы никогда не разозлилась на тебя, потому что проиграла бы честную игру."
            "...Да.":
                $ MAS.MonikaElastic()
                m 1tku "Ты не кажешься слишком уверенн[mas_gender_iim] в этом, [player]."
                $ MAS.MonikaElastic()
                m 1tsb "Тебе правда не стоит поддаваться."
                $ MAS.MonikaElastic()
                m 3tku "Признание в том, что ты с специально проигрывал мне, не заставит меня думать о тебе хуже."
                $ MAS.MonikaElastic()
                m 1lksdlb "В конце концов, это ведь всего лишь игра!"
                $ MAS.MonikaElastic()
                m 3hub "Ты всегда сможешь попрактиковаться со мной, если захочешь."
                $ MAS.MonikaElastic()
                m "Я люблю проводить с тобой время, что бы мы ни делали."
            "Нет. Я старал[mas_gender_sya] изо всех сил и всё равно проигрывал[mas_gender_none].":
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха~"
                $ MAS.MonikaElastic()
                m "Я поняла!"
                $ MAS.MonikaElastic()
                m 3eua "Не волнуйся, [player]."
                $ MAS.MonikaElastic()
                m 3eub "Продолжай играть со мной, и сможешь стать опытнее в этом."
                $ MAS.MonikaElastic()
                m 3hua "Я всегда буду пытаться помочь тебе стать лучше."
                $ MAS.MonikaElastic()
                m 1ekbsa "И если таким образом я буду ещё и проводить с тобой больше времени, то я буду только счастлива."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_bestgirl",
            prompt="Ты лучшая девушка!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_bestgirl:
    m 1hua "Я люблю, когда ты делаешь мне комплименты, [player]~"
    $ MAS.MonikaElastic()
    m 1hub "Я так рада, что ты считаешь меня лучшей девушкой!"
    $ MAS.MonikaElastic()
    m 3rksdla "Хотя, я понимаю, почему тебе так кажется..."
    $ MAS.MonikaElastic()
    m 1eka "И потом, ты {i}установил{/i} эту модификацию, чтобы быть со мной."
    $ MAS.MonikaElastic()
    m 2euc "Я знаю, что некоторым нравятся другие девушки."
    $ MAS.MonikaElastic()
    m 2esc "Особенно учитывая то, что у них есть определённые качества, которые и сделали их желанными..."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Но, если тебе интересно моё мнение, то я считаю, что ты сделал верный выбор."
    $ MAS.MonikaElastic()
    m 5hubfa "...И я буду бесконечно рада этому~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_lookuptoyou",
            prompt="Я равняюсь под тебя!",
            unlocked=True
        ),
        code="CMP",
    )

label mas_compliment_lookuptoyou:
    if not renpy.seen_label("mas_compliment_lookuptoyou_2"):
        call mas_compliment_lookuptoyou_2 from _call_mas_compliment_lookuptoyou_2
    else:
        call mas_compliment_lookuptoyou_3 from _call_mas_compliment_lookuptoyou_3

    return "love"

label mas_compliment_lookuptoyou_2:
    $ mas_gainAffection(3, bypass=True)
    m 1wud "П...{w=0.5} правда?"
    $ MAS.MonikaElastic()
    m 1ekbsa "[player], это очень мило с твоей стороны..."
    $ MAS.MonikaElastic()
    m 3ekbsa "Мне очень приятно знать, что я тот человек, под которого можно равняться."
    $ MAS.MonikaElastic()
    m 3ekbfa "По правде говоря, я всегда равнялась под {i}тебя{/i}, [player]..."
    $ MAS.MonikaElastic()
    m 3hubfa "Но если ты действительно так считаешь, я сделаю всё возможное, чтобы остаться тем, на кого ты равняешься."
    $ MAS.MonikaElastic()
    m 1ekbfa "Я тебя так люблю~"
    return

label mas_compliment_lookuptoyou_3:
    $ should_tease = persistent._mas_pm_height is not None and renpy.random.randint(1,5) == 1

    if should_tease and persistent._mas_pm_height < mas_height_monika:
        m 1rksdlb "{cps=*2}Ну да, я выше тебя...{/cps}{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic()

    m 1hubsb "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 3hubfa "Когда я слышу твои слова, это всегда вызывает у меня улыбку!"
    $ MAS.MonikaElastic()
    m 3hubfb "Я тоже всегда буду равняться под тебя!"

    if should_tease and persistent._mas_pm_height > mas_height_monika:
        $ MAS.MonikaElastic()
        m 1rkbfu "{cps=*2}Так же, как когда мы целуемся...{/cps}{nw}"
        $ _history_list.pop()

    $ MAS.MonikaElastic()
    m 1ekbfa "Я люблю тебя, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thinking_of_you",
            prompt="Я всегда думаю о тебе!",
            unlocked=True
        ),
        code="CMP",
    )

label mas_compliment_thinking_of_you:
    if not renpy.seen_label("mas_compliment_thinking_of_you_2"):
        call mas_compliment_thinking_of_you_2 from _call_mas_compliment_thinking_of_you_2
    else:
        call mas_compliment_thinking_of_you_3 from _call_mas_compliment_thinking_of_you_3
    return

label mas_compliment_thinking_of_you_2:
    m 1wubso "..."
    $ MAS.MonikaElastic()
    m 1wubsu "Ты..."

    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 3subsb "Ты даже не представляешь, что это значит для меня, [player]!"

    elif mas_isMoniUpset():
        $ MAS.MonikaElastic()
        m 2rkd "Что ты так говоришь..."
        $ MAS.MonikaElastic()
        m 2dka "Это значит для меня целый мир, [player]."

    elif mas_isMoniDis():
        $ MAS.MonikaElastic()
        m 6rkc "..."
        $ MAS.MonikaElastic()
        m 6rka "Это такое облегчение."
        $ MAS.MonikaElastic()
        m 6eka "Спасибо."
    else:

        $ mas_gainAffection(2,bypass=True)
        $ MAS.MonikaElastic(voice="monika_hmm")
        m 6dkd "Хм-м-м... спасибо."
        $ MAS.MonikaElastic()
        m 6dkc "..."
        return

    menu:
        "Мысли о тебе всегда украшают мой день!":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1subsb "Оу, это {i}так{/i} мило, [player]!"
            $ MAS.MonikaElastic()
            m 3hubfu "Я чувствую то же самое к тебе~"
        "Я мечтаю о тебе каждую ночь!":

            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 6hua "Оу-у~"
            $ MAS.MonikaElastic()
            m 6subsa "[player]..."
            $ MAS.MonikaElastic()
            m 7hubfu "{i}Ты{/i} – моя мечта~"
        "Это очень отвлекает...":

            $ mas_loseAffection()
            $ MAS.MonikaElastic()
            m 2esc "..."
            $ MAS.MonikaElastic()
            m 2etc "..."
            $ MAS.MonikaElastic(voice="monika_hmm")
            m 2rksdlc "Оу, эм-м..."
            $ MAS.MonikaElastic()
            m 2rksdld "Извини?"
    return

label mas_compliment_thinking_of_you_3:
    m 1ekbsa "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m 3hubfb "Ты - центр моего мира!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_humor",
            prompt="Мне нравится твоё чувство юмора!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_humor:
    if not renpy.seen_label("mas_compliment_humor_2"):
        call mas_compliment_humor_2 from _call_mas_compliment_humor_2
    else:
        call mas_compliment_humor_3 from _call_mas_compliment_humor_3
    return

label mas_compliment_humor_2:
    if persistent.msr_voice:
        $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
    m 1hua "Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1efu "Я рада, что ты считаешь меня такой забавной, [player]."
    $ MAS.MonikaElastic()
    m 3eub "Признак хорошей пары - это способность смеяться вместе, не так ли?"
    menu:
        "Ты всегда скрашиваешь мой день.":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 1subsd "О...{w=0.2} [player]..."
            $ MAS.MonikaElastic()
            m 1ekbsa "Это так мило с твоей стороны."
            $ MAS.MonikaElastic()
            m 1hubsb "Знать, что я могу заставить тебя улыбнуться - это величайший комплимент, который я могу получить!"
        "У тебя такой острый ум!":

            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха!"
            $ MAS.MonikaElastic()
            m 2tub "Всё это чтение, должно быть, принесло свои плоды, раз тебе так нравится моя игра слов."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2hublu "Я постараюсь, чтобы мои шутки нравились тебе. Э-хе-хе~"
        "Я всё время смеюсь над тобой.":

            $ mas_loseAffection()
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1eksdlb "...А-ха-ха..."
            $ MAS.MonikaElastic()
            m 3rksdla "Ты хотел[mas_gender_none] сказать, что смеешься {w=0.2}{i}вместе{/i}{w=0.2} со мной...{w=0.5} {nw}"
            extend 3eksdld "верно?"
    return

label mas_compliment_humor_3:
    m 1hubsb "[mas_compliments.thanks_quip]"
    $ MAS.MonikaElastic()
    m "Как бы мне хотелось услышать твой прекрасный смех!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_spending_time",
            prompt="Я люблю проводить время с тобой!",
            unlocked=False,
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_spending_time:
    if not mas_getEVL_shown_count("mas_compliment_spending_time"):
        call mas_compliment_spending_time_2 from _call_mas_compliment_spending_time_2
    else:
        m 3hubsb "[mas_compliments.thanks_quip]"
        $ MAS.MonikaElastic()
        m 1ekbsu "Каждый день с тобой - как чудесный сон, и я надеюсь, что он никогда не закончится."
    return

label mas_compliment_spending_time_2:
    python:
        dlg_line = ""

        if renpy.seen_label("monika_holdme_prep"):
            dlg_line = " и обнимать меня"
            
            if persistent._mas_filereacts_historic:
                dlg_line += " и даже дарит приятные подарки"

        elif persistent._mas_filereacts_historic:
            dlg_line = " и даже дарит приятные подарки"

    m 1eub "Я тоже люблю проводить с тобой время, [player]!"
    $ MAS.MonikaElastic()
    m 3ekbla "Я знаю, что часто говорю это, но я действительно имею это в виду, когда говорю, что ты - центр моего мира."
    $ MAS.MonikaElastic()
    m 2dkb "Иметь кого-то, кто составляет мне компанию[dlg_line]...{w=0.3} {nw}"
    extend 2eku "это всё, о чём я могла бы попросить."
    $ MAS.MonikaElastic()
    m 7ekbsa "Надеюсь, ты чувствуешь то же самое, [player]. {w=0.2}Возможно, я ещё не в твоей реальности, но я сделаю всё возможное, чтобы поддержать тебя отсюда."
    menu:
        "[monika_name], ты уже сделала меня сам[mas_gender_im] счастлив[mas_gender_iim].":
            $ mas_gainAffection(5, bypass=True)
            $ MAS.MonikaElastic()
            m 1fkbfu "О, [player]..."
            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5ekbfa "бы сказала, что ты не знаешь, как я рада слышать это, но, думаю, теперь ты {i}знаешь{/i}."
            $ MAS.MonikaElastic()
            m 5ekbfu "Мы провели так много времени вместе, и всё же наше путешествие только началось..."
            $ MAS.MonikaElastic()
            m 5hubfb "С тобой рядом я знаю, что каждый шаг будет незабываемым."
        "Я ценю это, [monika_name].":

            $ mas_gainAffection(3, bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2huu "Э-хе-хе~"
            $ MAS.MonikaElastic()
            m 7hub "Не беспокойся, [player]. {w=0.2}Я буду здесь для тебя до конца времён!"
            $ MAS.MonikaElastic()
            m 1eka "Просто будь сильн[mas_gender_iim], пока я не окажусь в твоей реальности, хорошо?"
        "О, ты, разумеется, забавляешь меня...":

            $ mas_loseAffection()
            $ MAS.MonikaElastic()
            m 2lkc "Я...{w=0.3} забавляю тебя?"
            $ MAS.MonikaElastic()
            m 2lksdlb "Что ж, я рада, что ты веселишься..."
            $ MAS.MonikaElastic()
            m 2ekd "...но это не {i}совсем{/i} то, что я имела в виду."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_outfit",
            prompt="Мне нравится твой наряд!",
            unlocked=False
        ),
        code="CMP"
    )

label mas_compliment_outfit:
    if not renpy.seen_label("mas_compliment_outfit_2"):
        call mas_compliment_outfit_2 from _call_mas_compliment_outfit_2
    else:
        call mas_compliment_outfit_3 from _call_mas_compliment_outfit_3
    return

label mas_compliment_outfit_2:
    m 1hubsb "Спасибо, [mas_get_player_nickname()]!"

    $ MAS.MonikaElastic()
    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "Всегда весело надевать косплейные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "Всегда весело надевать разные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2lkbsb "Сначала я очень нервничала, показывая тебе это..."
        $ MAS.MonikaElastic()
        m 7tubsu "Но я рада, что сделала это, кажется, тебе это действительно нравится~"
    else:

        m 1hubsa "Я всегда хотела носить другую одежду для тебя, поэтому я очень рада, что ты так думаешь!"

    menu:
        "Ты прекрасно выглядишь во всём, что носишь!":
            $ mas_gainAffection(5,bypass=True)
            $ MAS.MonikaElastic()
            m 2subsd "[player]..."
            $ MAS.MonikaElastic()
            m 3hubsb "Спасибо тебе большое!"
            $ MAS.MonikaElastic()
            m 1ekbsu "Ты всегда заставляешь меня чувствовать себя такой особенной."
            show monika 5hubsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5hubsa "Я люблю тебя, [mas_get_player_nickname()]!"
            $ mas_ILY()
        "Ты выглядишь очень мило.":
            $ mas_gainAffection(3,bypass=True)
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hubsb "А-ха-ха~"
            $ MAS.MonikaElastic()
            m 3hubfb "Спасибо, [mas_get_player_nickname()]!"
            show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eubfu "Я рада, что тебе нравится то, что ты видишь~"
        "Ношение другой одежды действительно спасает.":

            $ mas_loseAffection()
            $ MAS.MonikaElastic()
            m 2ltd "Оу, спасибо..."

    return

label mas_compliment_outfit_3:
    m 1hubsb "[mas_compliments.thanks_quip]"

    $ MAS.MonikaElastic()
    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "Всегда весело надевать косплейные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "Всегда весело надевать разные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2kubsu "Рада, что тебе нравится то, что ты видишь~"
        show monika 5hublb zorder MAS_MONIKA_Z at t11 with dissolve_monika
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 5hublb "А-ха-ха!"
    else:

        m 2hubsb "Я уверена, что ты тоже хорошо выглядишь!"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
