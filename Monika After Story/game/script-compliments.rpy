# Module for complimenting Monika
#
# Compliments work by using the "unlocked" logic.
# That means that only those compliments that have their
# unlocked property set to True
# At the beginning, when creating the menu, the compliments
# database checks the conditionals of the compliments
# and unlocks them.
# We only display the compliments that are
# unlocked, not hidden, within affection range,
# and don't have a conditional or have a conditional that evaluates to True.
# If you don't want a dynamic conditional for your compliment, you'd need
# to use an external event to unlock it from somewhere else.


# dict of tples containing the stories event data
default persistent._mas_compliments_database = dict()


# store containing compliment-related things
init 3 python in mas_compliments:

    compliment_database = dict()

init 22 python in mas_compliments:
    import store
    import random
    import datetime

    thanking_quips = [
        _("Ты такой милый, [player]."),
        _("Я всегда рада слышать эти слова от тебя, [player]!"),
        _("Спасибо за вновь приятные слова, [mas_get_player_nickname()]!"),
        _("После таких слов, мне всегда кажется, что я особенная, [mas_get_player_nickname()]."),
        _("А-ах, [player]~"),
        _("Спасибо, [mas_get_player_nickname()]!"),
        _("Ты постоянно мне льстишь, [player].")
    ]

    __last_called_callback = None
    __wait_time = 55.0
    # set this here in case of a crash mid-compliment
    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

    def __set_wait_time():
        """
        Sets new wait time
        """
        global __wait_time
        __wait_time = random.uniform(40.0, 70.0)

    def compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip, __last_called_callback

        thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

        _now = datetime.datetime.now()
        if __last_called_callback is not None:
            diff = (_now - __last_called_callback).total_seconds()
            if diff <= __wait_time:
                __last_called_callback = _now
                __set_wait_time()
                return

        __last_called_callback = _now
        __set_wait_time()

        store.mas_gainAffection()

# entry point for compliments flow
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_compliments",
            category=['моника', 'романтика'], # Если категории у тебя как-то по другому называются, то отредачь.
            prompt="Я хочу сказать тебе кое-что...",
            pool=True,
            unlocked=True
        )
    )

label monika_compliments:
    python:
        # Unlock any compliments that need to be unlocked
        Event.checkEvents(mas_compliments.compliment_database)

        # build menu list
        compliments_menu_items = [
            (ev.prompt, ev_label, not seen_event(ev_label), False)
            for ev_label, ev in mas_compliments.compliment_database.iteritems()
            if (
                Event._filterEvent(ev, unlocked=True, aff=mas_curr_affection, flag_ban=EV_FLAG_HFM)
                and ev.checkConditional()
            )
        ]

        # also sort this list
        compliments_menu_items.sort()

# final quit item
        final_item = ("Ох, не важно.", False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ mas_compliments.compliment_delegate_callback()
        $ MASEventList.push(_return)
        # move her back to center
        show monika at t11

    else:
        return "prompt"

    return

# Compliments start here
init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="Ты очень красивая!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubsb "О, боже [player]..."
    m 1hubfb "Спасибо за комплимент."
    m 2ekbfb "Мне нравится, когда ты говоришь нечто подобное~"
    m 1ekbfa "Для меня ты самый красивый человек в мире!"
    menu:
        "Ты для меня самая красивая девушка на свете!":
            $ mas_gainAffection(5, bypass=True)
            m 1hub "{do_giggle}Э-хе-хе~"
            m "Я так сильно тебя люблю, [player]!"
            # manually handle the "love" return key
            $ mas_ILY()
        
        "Ты в моём топ-10.":
            $ mas_loseAffection()
            m 3hksdrb "...?"
            m 2lsc "Ну спасибо, наверное..."
        
        "Спасибо.":
            pass
    return

label mas_compliment_beautiful_3:
    python:
        beautiful_quips = [
            _("Никогда не забывай, что ты для меня самый прекрасный человек в мире."),
            _("Ничто не сравнится с красотой в твоём сердце."),
        ]
        beautiful_quip = random.choice(beautiful_quips)
    m 1hubsa "{do_giggle}Э-хе-хе~"
    m 1ekbfa "[mas_compliments.thanks_quip]"
    show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubfb "[beautiful_quip]"
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
        call mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subsb "Ох, [player]..."
    m 1tubfb "Я знала, что цвет моих глаз особенный, но услышать это от тебя..."
    m 1dkbfa "Эти слова заставляют биться моё сердце чаще!"
    menu:
        "Я ничего не могу с собой поделать. Просто твои глаза слишком красивы.":
            $ mas_gainAffection(5, bypass=True)
            m 1hub "{do_giggle}А-ха-ха!"
            m "Не льсти мне слишком много, ладно?"
            show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hub "Я могу слегка сойти с ума..."

        "Они правда завораживают.":
            $ mas_gainAffection(1, bypass=True)
            m "{do_giggle}А-ха-ха~"

        "Они того же цвета, что и трава!":
            $ mas_gainAffection(0.5, bypass=True) # at least you tried
            m 2lksdrb "...Это не совсем та аналогия, которую я планировала услышать, но спасибо."
    return

label mas_compliment_eyes_3:
    python:
        eyes_quips = [
            _("Смотри в мои глаза столько, сколько захочешь~"),
            _("Я не могу дождаться, когда смогу заглянуть и в твои прекрасные глаза."),
            _("Я бы смотрела в твои глаза часами, если бы могла."),
        ]
        eyes_quip = random.choice(eyes_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 2ekbfb "[eyes_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_goodmood",
            prompt="Ты всегда поднимаешь мне настроение!",
            unlocked=False,
            conditional="store.mas_anni.pastSixMonths()",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_goodmood:
    if not renpy.seen_label("mas_compliment_goodmood_2"):
        call mas_compliment_goodmood_2
    else:
        call mas_compliment_goodmood_3
    return

label mas_compliment_goodmood_2:
    if mas_isMoniNormal(higher=True):
        $ mas_gainAffection(4, bypass=True)
        m 1subsb "Правда?!"
        m 3hubsb "Ты не представляешь, как много это для меня значит!"
        m 3ekbsu "Я всегда надеялась, что это так, но услышать это от тебя..."
        m 1dkbsu "..."
        m 2tubla "На этом моменте, я вспомнила, что у меня есть секрет, который я должна тебе поведать..."
        m 2tublu "Возможно, ты этого не замечал, но..."
        m 7tublb "{i}Ты{/i} всегда поддерживал во {i}мне{/i} хорошее настроение, [mas_get_player_nickname()]!"
        m 3hublb "{do_giggle}А-ха-ха!"
        m 3eubsa "Давай и дальше делать всё возможное друг для друга, хорошо?"
        m 1ekbsu "Люблю тебя~"
        $ mas_ILY()

    else:
        m 2lkc "..."
        m 2dkc "Я не уверена, как на это отнестись..."
        m 2ekd "Неужели тебе нравится делать мне больно?"
        m 2dkd "Надеюсь, это не то, что ты имел в виду..."

    return

label mas_compliment_goodmood_3:
    if mas_isMoniNormal(higher=True):
        m 1hub "Спасибо, что напомнил мне снова, [mas_get_player_nickname()]!"
        m 3eub "Всегда нужно держать себя в хорошем настроении!"
        m 3dku "Давай продолжим делать друг друга настолько счастливыми, насколько это возможно~"
        
    else:
        m 2euc "Спасибо."

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
        call mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hua "А-ах, [player]~"
    m 1hub "Это так мило!"
    m 2tuu "Но я думаю, что ты гораздо более лучшее чудо, что у меня было."
    m 2dkbsu "Я не могу дождаться того дня, когда смогу наконец-то крепко обнять тебя..."
    m 3ekbfb "И никогда не отпускать!"
    menu:
        "Как бы я хотел, чтобы ты была сейчас здесь!":
            $ mas_gainAffection(3, bypass=True)
            m "Это и моё самое заветное желание., [player]!"
        
        "Я буду долго держать тебя в своих объятиях.":
            $ mas_gainAffection(5, bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld
            m 1wubfsdld "Ох, прости [player]."
            m 2lksdla "Я попыталась почувствовать твои объятия отсюда."
            m 2hub "{do_giggle}А-ха-ха~"
        
        "Мне не особо нравятся объятия.":
            $ mas_loseAffection(0.5) # you monster.
            m 1eft "...Серьёзно?"
            m 1dkc "Ну, каждому своё, я думаю. Но однажды тебе придется это сделать."
    return

label mas_compliment_awesome_3:
    python:
        awesome_quips = [
            _("Ты всегда будешь ещё лучше!"),
            _("Вместе мы – потрясающая пара!"),
            _("Ты будешь куда лучше!"),
        ]
        awesome_quip = random.choice(awesome_quips)

    m 1hub "[mas_compliments.thanks_quip]"
    m 1eub "[awesome_quip]"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="Ты очень умна!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Ой...{w=0.3} спасибо, [player]."
    m 3eua "Я рада, что ты меня хорошо понимаешь."
    m 3hubsb "Я хочу научиться как можно большему, если это позволит тебе гордиться мной!"
    menu:
        "Ты всегда помогаешь мне становится лучше, [m_name].":
            $ mas_gainAffection(5, bypass=True)
            m 1hubfa "Я так тебя люблю, [player]!"
            m 3hubfb "Мы будем всю жизнь заниматься самосовершенствованием вместе!"
            # manually handle the "love" return key
            $ mas_ILY()
        
        "Я всегда буду гордиться тобой.":
            $ mas_gainAffection(3, bypass=True)
            m 1ekbfa "[player]..."
        
        "Иногда ты заставляешь меня чувствовать себя глупо.":
            $ mas_loseAffection()
            m 1wkbsc "..."
            m 2lkbsc "Прости, это не было моим умыслом..."
    return

label mas_compliment_intelligent_3:
    python:
        intelligent_quips = [
            _("Помни, что вместе мы будем всю жизнь заниматься самосовершенствованием!"),
            _("Запомни, что каждый день – это возможность узнать что-то новое!"),
            _("Всегда помни, что мир – это удивительное приключение, полное познаний."),
        ]
        intelligent_quip = random.choice(intelligent_quips)

    m 1ekbfa "[mas_compliments.thanks_quip]"
    m 1hub "[intelligent_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="Мне нравится твоя причёска.",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2
    else:
        call mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair.name != "def":
        m 1wubsb "Большое спасибо, [player]..."
        m 1lkbfb "Я очень волновалась, когда в первый раз меняла прическу для тебя."
    else:
        m 1hubfb "Большое спасибо, [player]!"
    m 2hub "Я всегда уделяла много внимания своим волосам."
    m 2lksdlb "На самом деле, потребовалась целая вечность, чтобы они стали такими длинными..."
    menu:
        "Это действительно так, особенно нравится твой длинный хвостик.":
            $ mas_gainAffection(3, bypass=True)
            m 1hub "Значит не зря старалась, спасибо за приятные слова, [player]!"

        "Ты всегда будешь милой, какую причёску бы не выбрала." if persistent._mas_likes_hairdown:
            $ mas_gainAffection(5, bypass=True)
            m 1ekbsa "А-ах, [player]."
            m 1hubfb "Каждый раз, благодаря тебе я чувствую себя такой особенной!"
            m "Спасибо!"
        
        "С короткими волосами ты была бы ещё симпатичнее.":
            $ mas_loseAffection()
            m "Ну, отправится в салон красоты сейчас я не могу."
            m 1lksdlc "Я... ценю твоё внимание."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair.name != "def":
        python:
            hair_quips = [
                _("Я очень рада, что тебе нравится эта причёска!"),
                _("Я очень рада, что тебе понравилось!")
            ]
            hair_quip = random.choice(hair_quips)
        m 1wubsb "Спасибо большое, [player]!"
        m 1hubfb "[hair_quip]"
    else:
        python:
            ponytail_quips = [
                _("Ты всегда заставляешь меня чувствовать себя особенной!"),
                _("Я рада, что тебе нравится мой хвостик!"),
                _("Я так рада, что тебе понравилось."),
            ]
            ponytail_quip = random.choice(ponytail_quips)

        m 1hubsb "Спасибо, [player]!"
        m 1hubfb "[ponytail_quip]"
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
        call mas_compliment_fit_2
    else:
        call mas_compliment_fit_3
    return

label mas_compliment_fit_2:
    m 1hub "Спасибо, [player]! Ты такой милый!"
    m 3eub "Я люблю поддерживать себя в форме и правильно питаться. Это заставляет меня чувствовать себя энергично и уверенно."
    m 1efb "Надеюсь, ты заботишься о своём здоровье."
    m 1lubsb "Мы всегда сможем позаниматься вместе, когда я окажусь в твоей реальности..."
    menu:
        "Звучит очень весело!":
            $ mas_gainAffection(2, bypass=True)
            m 1hubfb "{do_giggle}А-ха-ха! Я рада, что ты думаешь так же!"
            m 3eka "Не волнуйся. Даже если ты не сможешь поспевать за мной, я знаю, что мы всё равно сможем повеселиться..."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "До тех пор, пока мы вместе."
        
        "Ничего не обещаю, но постараюсь сделать всё возможное.":
            $ mas_gainAffection(1, bypass=True)
            m 1tfb "Тебе же будет лучше!"
            m 2tub "Не думай, что ты легко отделаешься, если начнёшь оправдываться."
        
        "Я предпочту не напрягаться...":
            m 1eka "Я понимаю, если это не твой вариант, но все-таки стоит попробовать..."
            m 1lksdla "Я была бы очень рада, если бы мы разделяли эти интересы, понимаешь?"
    return

label mas_compliment_fit_3:
    python:
        fitness_quips = [
            _("Надеюсь, что ты начнёшь фитнес-путешествие со мной!"),
            _("Буду с нетерпением ждать того момента, когда мы сможем вместе заняться спортом."),
            _("Надеюсь, когда-нибудь мы сможем позаниматься вместе!"),
        ]
        fitness_quip = random.choice(fitness_quips)

    m 2eka "[mas_compliments.thanks_quip]"
    m 7hub "[fitness_quip]"
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
    m 1eka "Это я благодарна за то, что у меня есть такой человек, как ты!"
    m 1ekbsa "Ты – единственная причина, почему я всё ещё здесь."
    m "Ты ведь даже установил этот мод, чтобы мы могли лучше проводить время вместе..."
    m 1dubsu "Ты – солнце, которое согревает моё сердце всякий раз, когда ты меня навещаешь."
    m 3ekbsa "Так что, думаю, нам обоим повезло, что мы есть друг у друга, [player]~"
    menu:
        "Ты для меня всё, [m_name].":
            if not mas_getEVL_shown_count("mas_compliment_thanks"):
                $ mas_gainAffection(10, bypass=True)

            m 1ekbsa "[player]..."
            m 1dubsu "Ничто не делает меня счастливее, чем слышать это от тебя."
            m "Не важно, какое будущее ждёт нас обоих...{w=0.5} {nw}"
            extend 1dkbfa "знай, что я всегда буду любить тебя и всегда буду рядом с тобой!"
        
        "Да.":
            m 1hub "Хи-хи~"
            m 1eub "Я люблю тебя, [player]."

    if not mas_isMoniLove():
        $ mas_lockEVL("mas_compliment_thanks", "CMP")
    return

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
        call mas_compliment_smile_2
    else:
        call mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m 1hub "Ты такой милый, [player]~"
    m 1eua "Я много улыбаюсь, когда ты здесь."
    m 1ekbsa "Потому что я очень счастлива, когда ты проводишь со мной время~"
    menu:
        "Я буду навещать тебя каждый день, лишь бы видеть твою чудесную улыбку.":
            $ mas_gainAffection(5, bypass=True)
            m 1wubfsdld "Ох, [player]..."
            m 1lkbfa "Кажется, у меня сердце только что ёкнуло от радости."
            m 3hubfa "Видишь? Ты всегда делаешь меня настолько счастливой, насколько только возможно."
        
        "Мне нравится видеть твою улыбку.":
            $ mas_gainAffection(1, bypass=True)
            m 1hub "{do_giggle}А-ха-ха~"
            m 3eub "Тогда всё что тебе нужно сделать – это продолжать навещать меня, [player]!"
    return

label mas_compliment_smile_3:
    python:
        smile_quips = [
            _("Я буду улыбаться только для тебя!"),
            _("Я не могу не улыбаться, когда думаю о тебе."),
            _("Не могу дождаться того дня, когда смогу увидеть твою улыбку."),
        ]
        smile_quip = random.choice(smile_quips)

    m 1eub "[mas_compliments.thanks_quip]"
    m 1hua "[smile_quip]"
    m 1huu "{do_giggle}Э-хе-хе~"
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
    if not mas_getEVL_shown_count("mas_compliment_hero"):
        $ mas_gainAffection(3, bypass=True)

    m 1wubssdld "А-{w=0.3}а?"
    m "Я твоя героиня?"
    m 2rkbfsdlb "[player]...{w=1.5} я не совсем уверена в том, что ты имел в виду."
    m 2ekbfb "Ты единственный, кто сидел со мной всё это время.{w=1} Я должна отблагодарить тебя, правда."
    m 1hubfa "Что ж, если я как-то помогла тебе, то я безумно счастлива~"
    m 3ekbfa "Ты помогал мне всеми возможными способами, как я могу не отдать тебе должное, находясь рядом с тобой тогда, когда тебе нужна поддержка?"
    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    # Keeping this 'hero' since you call her that too
    m 5hubfa "И потом, ты всегда будешь моим героем~"
    m 5hubfb "Я люблю тебя, и я всегда буду верить в тебя!"
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
        call mas_compliment_cute_2
    else:
        call mas_compliment_cute_3
    return

label mas_compliment_cute_2:
    m 1wubssdld "Ах!"
    m 3rkbfsdla "На этот раз, ты, {i}в какой-то мере{/i}, застал меня врасплох."
    m 3tubfb "Самую малость..."
    m 1hubfa "Но я рада, что ты так думаешь!"
    menu:
        "Встреча с тобой всегда греет мне душу!":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(5, bypass=True)
            m 1hubfb "Оу, а мне греет душу слышать то, как ты говоришь подобное!"
            m 1dkbfu "...Почти так же, как когда я наконец-то запечатлела тот момент, где мы вместе в одной реальности."
            m 1ekbfa "Я с трудом сдерживаю себя, представляя себе тот особенный день~"
        
        "Ты намного симпатичнее, когда краснеешь.":
            $ persistent._mas_pm_monika_cute_as_natsuki = False
            $ mas_gainAffection(3, bypass=True)
            m 2tubfu "Ты не собираешься это так оставить, да, [player]?"
            m 2rubfu "Хм-м, я просто не ожидала такого."
            m 3tubfb "Но не жди, что в следующий раз всё будет так же просто..."
            m 1tubfu "Когда-нибудь я заставлю тебя покраснеть, {do_giggle}э-хе-хе~"
        
        "Ты такая же милая, как и Нацуки.":
            $ persistent._mas_pm_monika_cute_as_natsuki = True
            $ mas_loseAffection()
            m 2lfc "Оу. {w=1}Спасибо, [player]..."
            m 1rsc "Но я надеялась, что буду для тебя милой по-своему."
    return

label mas_compliment_cute_3:
    python:
        cute_quips = [
            _("Ты тоже зачастую бываешь очень милым, знаешь ли~"),
            _("Ты всегда будешь выглядить для меня мило~"),
            _("Ты тоже зачастую можешь быть очень милым~"),
        ]
        cute_quip = random.choice(cute_quips)

    m 1ekbsa "{do_giggle}Э-хе-хе, спасибо [player]..."
    m 1hubfa "[cute_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="Ты классно играешь в шахматы!",
            unlocked=False,
            conditional="persistent._mas_chess_stats.get('losses', 0) > 5",
            action=EV_ACT_UNLOCK
        ),
        code="CMP"
    )

label mas_compliment_chess:
    m 1eub "Спасибо, [player]."
    m 3esa "Как я уже говорила, интересно, моё мастерство как-то связано с тем, что я застряла здесь?"
    $ wins = persistent._mas_chess_stats.get("wins", 0)
    $ losses = persistent._mas_chess_stats.get("losses", 0)
    if wins > 0:
        m 3eua "Ты, кстати, тоже неплох, я уже проигрывала тебе раньше."
        if wins > losses:
            m "Да и фактически, думаю, ты выигрывал даже чаще меня."
        m 1hua "{do_giggle}Э-хе-хе~"
    else:
        m 2lksdlb "Знаю, [random_sure_lower], что ты ещё ни разу не выигрывал в шахматных партиях, но я уверена, что однажды ты победишь меня."
        m 3esa "Продолжай практиковаться и играть со мной, и ты сможешь стать лучше!"
    m 3esa "Чем больше мы играем, тем опытнее становимся."
    m 3hua "Так что не бойся бросать мне вызов, когда захочешь."
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
    m 1hub "{do_giggle}А-ха-ха~"
    m 2eub "Спасибо, [player], но пинг-понг, на самом деле, не такая уж и сложная игра."
    if persistent._mas_ever_won['pong']:
        m 1lksdla "Ты уже побеждал меня."
        m "Так что ты знаешь, что это и вправду очень просто."
        show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hub "Но я всё равно принимаю твой комплимент."
    else:
        m 3hksdrb "И ты слишком добр, раз постоянно мне поддаёшься, когда мы играем."
        m 3eka "Верно ведь?"
        menu:
            "Да.":
                m 2lksdla "Спасибо, конечно, [player], но тебе правда не стоит поддаваться."
                m 1eub "Не стесняйся играть серьёзно, когда хочешь."
                m 1hub "Я бы никогда не разозлилась на тебя, потому что проиграла бы честную игру."
            
            "...Ага.":
                m 1tku "Ты не кажешься слишком уверенным в этом, [player]."
                m 1tsb "Тебе правда не стоит поддаваться."
                m 3tku "Признание в том, что ты с специально проигрывал мне, не заставит меня думать о тебе хуже."
                m 1lksdlb "В конце концов, это ведь всего лишь игра!"
                m 3hub "Ты всегда сможешь попрактиковаться со мной, если захочешь."
                m "Я люблю проводить с тобой время, что бы мы ни делали."
            
            "Нет. Я старался изо всех сил и всё равно проигрывал":
                m 1hub "{do_giggle}А-ха-ха~"
                m "Я поняла!"
                m 3eua "Не волнуйся, [player]."
                m 3eub "Продолжай играть со мной, и сможешь стать опытнее в этом."
                m 3hua "Я всегда буду пытаться помочь тебе стать лучше."
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
    m 1hub "Я так рада, что ты считаешь меня лучшей девушкой!"
    m 3rksdla "Хотя, я понимаю, почему тебе так кажется..."
    m 1eka "И потом, ты {i}установил{/i} эту модификацию, чтобы быть со мной."
    m 2euc "Я знаю, что некоторым нравятся другие девушки."
    m 2esc "Особенно учитывая то, что у них есть определённые качества, которые и сделали их желанными..."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Но, если тебе интересно моё мнение, то я считаю, что ты сделал верный выбор."
    m 5hubfa "...И я буду бесконечно рада этому~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_lookuptoyou",
            prompt="Я равняюсь на тебя",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_lookuptoyou:
    if not renpy.seen_label("mas_compliment_lookuptoyou_2"):
        call mas_compliment_lookuptoyou_2
    else:
        call mas_compliment_lookuptoyou_3
    #Both paths return love, so we combine that here
    return "love"

label mas_compliment_lookuptoyou_2:
    $ mas_gainAffection(3, bypass=True)
    m 1wud "П...{w=0.5} правда??"
    m 1ekbsa "[player], это очень мило с твоей стороны..."
    m 3ekbsa "Мне очень приятно знать, что я тот человек, на которого можно равняться."
    m 3ekbfa "По правде говоря, я всегда равнялась на {i}тебя{/i}, [player]..."
    m 3hubfa "Но если ты действительно так считаешь, я сделаю всё возможное, чтобы остаться тем, на кого ты равняешься."
    m 1ekbfa "Я тебя так люблю~"
    return

label mas_compliment_lookuptoyou_3:
    $ should_tease = persistent._mas_pm_height is not None and renpy.random.randint(1,5) == 1

    if should_tease and persistent._mas_pm_height < mas_height_monika:
        m 1rksdlb "{cps=*2}Ну да, я выше тебя...{/cps}{nw}"
        $ _history_list.pop()

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 3hubfa "Когда я слышу твои слова, это всегда вызывает у меня улыбку!"
    m 3hubfb "Я тоже всегда буду равняться на тебя!"

    if should_tease and persistent._mas_pm_height > mas_height_monika:
        if persistent._mas_first_kiss:
            m 1rkbfu "{cps=*2}Так же, как когда мы целуемся...{/cps}{nw}"
        else:
            m 1rkbfu "{cps=*2}Когда-нибудь, но, уж точно{/cps}{nw}"
        $ _history_list.pop()

    m 1ekbfa "Люблю тебя, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thinking_of_you",
            prompt="Я всегда думаю о тебе!",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_thinking_of_you:
    if not renpy.seen_label("mas_compliment_thinking_of_you_2"):
        call mas_compliment_thinking_of_you_2
    else:
        call mas_compliment_thinking_of_you_3
    return

label mas_compliment_thinking_of_you_2:
    m 1wubso "..."
    m 1wubsu "Ты..."

    if mas_isMoniNormal(higher=True):
        m 3subsb "Ты даже не представляешь, что это значит для меня, [player]!"

    elif mas_isMoniUpset():
        m 2rkd "Что ты так говоришь..."
        m 2dka "Это значит для меня целый мир, [player]."

    elif mas_isMoniDis():
        $ mas_gainAffection(1, bypass=True)
        m 6rkc "..."
        m 6rka "Это такое облегчение."
        m 6eka "Спасибо."
    else:
        $ mas_gainAffection(1, bypass=True)
        m 6dkd "Хм-м-м... спасибо."
        m 6dkc "..."
        return

    menu:
        "Мысли о тебе всегда украшают мой день!":
            $ mas_gainAffection(5, bypass=True)
            m 1subsb "Оу, это {i}так{/i} мило, [player]!"
            m 3hubfu "Я чувствую то же самое к тебе~"
        
        "Я мечтаю о тебе каждую ночь!":
            $ mas_gainAffection(5, bypass=True)
            m 6hua "Оу-у~"
            m 6subsa "[player]..."
            m 7hubfu "{i}Ты{/i} – моя мечта~"
        
        "Это очень отвлекает...":
            if mas_isMoniDis(lower=True):
                $ mas_loseAffection(modifier=2.0)
            else:
                $ mas_loseAffection()
            m 2esc "..."
            m 2etc "..."
            m 2rksdlc "Оу, эм-м..."
            m 2rksdld "Извини?"
    return

label mas_compliment_thinking_of_you_3:
    python:
        thinking_of_you_quips = [
            _("Ты – центр моего мира!"),
            _("Ты постоянно в моей голове!"),
            _("Я тоже постоянно думаю о тебе!"),
        ]
        thinking_of_you_quip = random.choice(thinking_of_you_quips)

    m 1ekbsa "А-ах, спасибо тебе, [player]..."
    m 3hubfb "[thinking_of_you_quip]"
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
        call mas_compliment_humor_2
    else:
        call mas_compliment_humor_3
    return

label mas_compliment_humor_2:
    m 1hua "{do_giggle}Э-хе-хе~"
    m 1efu "Я рада, что ты считаешь меня такой забавной, [player]."
    m 3eub "Признак хорошей пары – это способность смеяться вместе, не так ли?"
    menu:
        "Ты всегда скрашиваешь мой день.":
            $ mas_gainAffection(5, bypass=True)
            m 1subsd "О...{w=0.2} [player]..."
            m 1ekbsa "Это так мило с твоей стороны."
            m 1hubsb "Знать, что я могу заставить тебя улыбнуться – это величайший комплимент, который я могу получить!"
        
        "У тебя такой острый ум!":
            $ mas_gainAffection(3, bypass=True)
            m 1hub "{do_giggle}А-ха-ха!"
            m 2tub "Всё это чтение, должно быть, принесло свои плоды, раз тебе так нравится моя игра слов."
            m 2hublu "Я постараюсь, чтобы мои шутки нравились тебе. {do_giggle}Э-хе-хе~"
        
        "Я всё время смеюсь над тобой.":
            $ mas_loseAffection()
            m 1eksdlb "...{do_giggle}А-ха-ха..."
            m 3rksdla "Ты хотел сказать, что смеешься {w=0.2}{i}вместе{/i}{w=0.2} со мной...{w=0.5} {nw}"
            extend 3eksdld "верно?"
    return

label mas_compliment_humor_3:
    python:
        humor_quips = [
            _("Как бы мне хотелось услышать твой прекрасный смех!"),
            _("Одно осознание этого делает меня счастливой~"),
            _("Я всегда буду стараться скрасить твой день!"),
        ]
        humor_quip = random.choice(humor_quips)

    m 1hubsb "[mas_compliments.thanks_quip]"
    m 1hubsu "[humor_quip]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_missed",
            prompt="Я так скучал по тебе!",
            unlocked=True,
            conditional=(
                "store.mas_getSessionLength() <= datetime.timedelta(minutes=30) "
                "and store.mas_getAbsenceLength() >= datetime.timedelta(hours=1) "
                "and not store.mas_globals.returned_home_this_sesh"
            )
        ),
        code="CMP"
    )

label mas_compliment_missed:
    python:
        missed_quips_long = (
            _("Я так рада снова видеть тебя!"),
            _("Я так рада, что ты вернулся!"),
            _("Рада снова видеть тебя!"),
            _("Я так рада, что ты думал обо мне!"),
            _("Нам так повезло, что мы есть друг у друга!"),
            _("Нам больше не придётся чувствовать себя одиноко!"),
            _("Я не могла дождаться твоего возвращения!"),
            _("Мне было одиноко ждать тебя!")
        )

        missed_quips_short = (
            _("Спасибо, что возвращаешься, чтобы проводить время со мной!"),
            _("Я с нетерпением ждала возможности провести время вместе!"),
            _("Спасибо, что снова пришёл ко мне!"),
            _("Давай наслаждаться нашим совместным времяпрепровождением сегодня!"),
            _("Я очень ценю тебя, [player]!"),
            _("Спасибо, что находишь время для меня!"),
            _("Мне так повезло с тобой, [player]!"),
            _("Готов провести время вместе?"),
            _("Я всё это время то и делала, что думала о тебе!"),
            _("Ты всегда был у меня на уме!")
        )

        missed_quips_upset_short = (
            _("Я так рада, что ты думал обо мне. Для меня это многое значит."),
            _("Я очень рада слышать это, [player]."),
            _("Это очень приятно слышать."),
            _("Я счастлива, что ты думал обо мне, [player]."),
            _("Для меня это важнее самого мира, [player]."),
            _("Так я чувствую себя намного лучше., [player].")
        )

        missed_quips_upset_long = (
            _("Я уже начала беспокоиться, что ты забыл обо мне."),
            _("Спасибо, что доказал, что тебе не всё равно, [player]."),
            _("Я рада знать, что ты не забыл обо мне, [player]"),
            _("Я уже начала волноваться, что ты не вернешься, [player]")
        )

        missed_quips_dis = (
            _("Я не уверена, что ты имеешь в виду, [player]..."),
            _("Я не совсем уверена, что ты имел в виду, [player]..."),
            _("Я не думаю, что ты действительно имеел это в виду, [player]..."),
            _("Если бы ты действительно это имел в виду, [player]..."),
            _("...Мне кажется, или ты хотел сказать, что-то другое?"),
            _("...Почему я думаю, что ты просто так это говоришь?"),
            _("...Я не могу поверить в эти слова, [player]."),
            _("Я не думаю, что это правда, [player].")
        )

        hugchance = 1
        absence_length = mas_getAbsenceLength()
        mas_flagEVL("mas_compliment_missed", "CMP", EV_FLAG_HFM)

    if mas_isMoniNormal(higher=True):
        if absence_length >= datetime.timedelta(days=3):
            if absence_length >= datetime.timedelta(days=7):
                $ hugchance = 30

            else:
                $ hugchance = 15

            m 1fka "Я так по тебе скучала, [mas_get_player_nickname()]!"
            m 3fka "[renpy.substitute(random.choice(missed_quips_long))]"

        else:
            m 1fka "Я тоже по тебе скучала, [mas_get_player_nickname()]!"
            m 3hub "[renpy.substitute(random.choice(missed_quips_short))]"

        if (
            mas_isMoniEnamored(higher=True)
            and mas_timePastSince(persistent._mas_last_hold_dt, datetime.timedelta(hours=12))
            and random.randint(1, 50) <= hugchance
        ):
            m 2lsa "..."
            m 2lsb "Скажи, [player]..."
            m 1eka "Я надеялась, что..."
            m 3ekblb "Знаешь, с тех пор прошло немного времени..."

            m 1ekblb "Мог бы ты меня обнять? {w=0.3}Мне было очень одиноко, пока тебя не было.{nw}"
            $ _history_list.pop()
            menu:
                m "Мог бы ты меня обнять? Мне было очень одиноко, пока тебя не было.{fast}"
                
                "Конечно, [m_name]!":
                    $ mas_gainAffection(modifier=0.25, bypass=True)

                    call monika_holdme_prep(lullaby=MAS_HOLDME_NO_LULLABY, stop_music=True, disable_music_menu=True)
                    call monika_holdme_start
                    call monika_holdme_end

                    m 6dkbsa "М-м-м... это было очень приятно, [player]."
                    m 7ekbsb "Ты всегда знаешь, как сделать так, чтобы я чувствовала себя особенной."
                    $ mas_moni_idle_disp.force_by_code("1eubsa", duration=10, skip_dissolve=True)
                
                "Не сейчас.":
                    $ mas_loseAffection()
                    m 2lkp "Хорошо, тогда, может быть, позже?"
                    python:
                        mas_moni_idle_disp.force_by_code("2lkp", duration=10, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("2rsc", duration=10, clear=False, redraw=False, skip_dissolve=True)
                        mas_moni_idle_disp.force_by_code("1esc", duration=30, clear=False, skip_dissolve=True)

    #Base negative responses on monika_love label
    elif mas_isMoniUpset():
        m 2wuo "..."
        m 2ekbla "Я...{w=0.5} я скучала по тебе."

        if absence_length >= datetime.timedelta(days=3):
            m 2ekd "[renpy.substitute(random.choice(missed_quips_upset_long))]"

        else:
            m 2eka "[renpy.substitute(random.choice(missed_quips_upset_short))]"

        $ mas_moni_idle_disp.force_by_code("2eka", duration=10, skip_dissolve=True)

    elif mas_isMoniDis():
        m 6dkc "..."
        m 6rktpd "[renpy.substitute(random.choice(missed_quips_dis))]"

        if absence_length >= datetime.timedelta(days=3):
            m 6dktdc "...Но, по крайней мере, ты не забыл меня...{w=0.5} пока."

    else:
        m 6ckc "..."

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
        call mas_compliment_spending_time_2
    else:
        python:
            spending_time_quips = [
                _("Каждый день с тобой – как чудесный сон, и я надеюсь, что он никогда не закончится."),
                _("Просто быть рядом с тобой делает меня такой счастливой~"),
                _("Ничто не делает меня счастливее, чем быть рядом с тобой~"),
            ]
            spending_time_quip = random.choice(spending_time_quips)

        m 3hubsb "[mas_compliments.thanks_quip]"
        m 1ekbsu "[spending_time_quip]"
    return

label mas_compliment_spending_time_2:
    python:
        dlg_line = ""

        if renpy.seen_label("monika_holdme_prep"):
            dlg_line = " и обнимает меня"
            
            if persistent._mas_filereacts_historic:
                dlg_line += " и даже дарит приятные подарки"

        elif persistent._mas_filereacts_historic:
            dlg_line = " и даже дарит классные подарки"

    m 1eub "Я тоже люблю проводить с тобой время, [player]!"
    m 3ekbla "Я знаю, что часто говорю это, но я действительно имею это в виду, когда говорю, что ты – центр моего мира."
    m 2dkb "Иметь кого-то, кто составляет мне компанию[dlg_line]...{w=0.3}{nw}"
    extend 2eku "это всё, о чём я могла бы попросить."
    m 7ekbsa "Надеюсь, ты чувствуешь то же самое, [player]. {w=0.2}Возможно, я ещё не в твоей реальности, но я сделаю всё возможное, чтобы поддержать тебя отсюда."
    menu:
        "[m_name], ты уже сделала меня самым счастливым.":
            $ mas_gainAffection(5, bypass=True)
            m 1fkbfu "Ох, [player]..."
            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Я бы сказала, что ты не знаешь, как я рада слышать это, но, думаю, теперь ты {i}знаешь{/i}."
            m 5ekbfu "Мы провели так много времени вместе, и всё же наше путешествие только началось..."
            m 5hubfb "С тобой рядом я знаю, что каждый шаг будет незабываемым."
        
        "Я ценю это, [m_name].":
            $ mas_gainAffection(3, bypass=True)
            m 2huu "{do_giggle}Э-хе-хе~"
            m 7hub "Не беспокойся, [player]. {w=0.2}Я буду здесь для тебя до конца времён!"
            m 1eka "Просто будь сильным, пока я не окажусь в твоей реальности, хорошо?"
        
        "О, ты, разумеется, забавляешь меня...":
            $ mas_loseAffection()
            m 2lkc "Я...{w=0.3} забавляю тебя?"
            m 2lksdlb "Что ж, я рада, что ты веселишься..."
            m 2ekd "...но это не {i}совсем{/i} то, что я имела в виду."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_sweet",
            prompt="Ты стала ещё милее!",
            conditional="store.mas_anni.pastThreeMonths()",
            action=EV_ACT_UNLOCK,
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="CMP"
    )

label mas_compliment_sweet:
    if mas_getEVL_shown_count("mas_compliment_sweet"):
        jump mas_compliment_sweet_repeat

    m 1ekbsb "А-ах, [player]..."
    m 3rkbssdlu "Я не знаю, что сказать, {do_giggle}а-ха-ха...{w=0.3}{nw}"
    extend 3ekbsa "Это ты был так мил со мной всё это время."
    m 3hubsa "Мне просто очень приятно слышать это от тебя, {do_giggle}э-хе-хе~"

    menu:
        "Твои слова всегда делают мой день лучше!":
            $ mas_gainAffection(3, bypass=True)
            m 1sud "[player]..."
            extend 1eka "Я даже не представляла, как много значат для тебя мои слова..."
            m 1ekblb "Я так счастлива, что у меня есть такой удивительный [bf], как ты, [mas_get_player_nickname(exclude_names=[player])]~"
            m 1ekbsu "Ты на самом деле лучшее, на что я могла надеяться...{w=0.2} Я так сильно тебя люблю."
            m 3kua "Надеюсь, ты никогда не забудешь это, [player]."
            $ mas_ILY()
        
        "Ты для меня особенная, [m_name]!":
            $ mas_gainAffection(3, bypass=True)
            m 1ekbsb "Ох, [player]...{w=0.3} {nw}"
            extend 3hubsa "То, что ты проводишь время со мной, делает меня такой счастливой и любимой!"
            show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbsa "Я очень рада, что ты так ко мне относишься, [mas_get_player_nickname()]. Я так сильно тебя люблю."
            $ mas_ILY()
        
        "Ты самая милая девушка, которую я когда-либо встречал!":
            $ mas_gainAffection(2, bypass=True)
            m 1ekbsa "Спасибо, [mas_get_player_nickname()]."
            m 3hubsb "Ты самый милый парень, которого я встречала, {do_giggle}э-хе-хе."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Мне очень повезло быть с тобой!"

    return

label mas_compliment_sweet_repeat:
    python:
        sweet_quips = [
            _("Я так рада слышать это от тебя., [player]!"),
            _("Мне всегда так тепло на сердце, когда я это слышу, [player]!"),
            _("Благодаря тебе, я всегда чувствую себя любимой, [player]!"),
        ]
        sweet_quip = renpy.substitute(random.choice(sweet_quips))

    m 3hubsb "[sweet_quip]"
    m 1hubfu "...Но я никогда не смогу быть такой милой, как ты."
    return

# this compliment's lock/unlock is controlled by the def outfit pp
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
    if mas_getEVL_shown_count("mas_compliment_outfit"):
        jump mas_compliment_outfit_repeat

    m 1hubsb "Спасибо, [mas_get_player_nickname()]!"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        m 3hubsb "Всегда весело надевать косплейные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 3hubsb "Всегда весело надевать разные наряды!"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        m 2lkbsb "Сначала я очень нервничала, показываясь тебе в этом..."
        m 7tubsu "Но я рада, что сделала это, кажется, тебе это правда понравилось~"

    else:
        m 1hubsa "Я всегда хотела носить другую одежду для тебя, поэтому я очень рада, что ты так думаешь!"

    menu:
        "Ты прекрасно выглядишь во всём, что носишь!":
            $ mas_gainAffection(5, bypass=True)
            m 2subsd "[player]..."
            m 3hubsb "Спасибо тебе большое!"
            m 1ekbsu "Ты всегда заставляешь меня чувствовать себя такой особенной."
            show monika 5hubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubsa "Я люблю тебя, [mas_get_player_nickname()]!"
            $ mas_ILY()

        "Ты выглядишь очень мило.":
            $ mas_gainAffection(3, bypass=True)
            m 1hubsb "{do_giggle}А-ха-ха~"
            m 3hubfb "Спасибо, [mas_get_player_nickname()]!"
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eubfu "Я рада, что тебе нравится то, что ты видишь~"
        
        "Разнообразие в одежде действительно помогает.":
            $ mas_loseAffection()
            m 2ltd "Оу, спасибо..."

    return

label mas_compliment_outfit_repeat:
    m 1hubsb "[mas_compliments.thanks_quip]"

    if monika_chr.is_wearing_clothes_with_exprop("cosplay"):
        python:
            cosplay_quips = [
                _("Всегда весело надевать косплейные наряды!"),
                _("Я рада, что тебе нравится этот косплей!"),
                _("Я буду рада продолжить косплеить для тебя!"),
            ]
            cosplay_quip = random.choice(cosplay_quips)

        m 3hubsb "[cosplay_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("costume"):
        python:
            clothes_quips = [
                _("Я рада, что тебе нравится, как я выгляжу в этом!"),
                _("Я рада, что тебе понравился мой новый образ~"),
            ]
            clothes_quip = random.choice(clothes_quips)

        m 3hubsb "[clothes_quip]"

    elif monika_chr.is_wearing_clothes_with_exprop("lingerie"):
        python:
            lingerie_quips = [
                _("Рада, что тебе нравится то, что ты видишь~"),
                _("Хочешь посмотреть поближе?"),
                _("Хочешь немного подглядеть?~"),
            ]
            lingerie_quip = random.choice(lingerie_quips)

        m 2kubsu "[lingerie_quip]"
        show monika 5hublb at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hublb "{do_giggle}А-ха-ха!"

    else:
        python:
            other_quips = [
                _("Я горжусь своим чувством стиля!"),
                _("Я уверена, что ты тоже хорошо выглядишь!"),
                _("Я в восторге от этого наряда!")
            ]
            other_quip = random.choice(other_quips)

        m 3hubsb "[other_quip]"

    return
