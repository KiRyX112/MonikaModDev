
default persistent._mas_fun_facts_database = dict()

init -10 python in mas_fun_facts:

    fun_fact_db = {}

    def getUnseenFactsEVL():
        """
        Gets all unseen (locked) fun facts as eventlabels

        OUT:
            List of all unseen fun fact eventlabels
        """
        return [
            fun_fact_evl
            for fun_fact_evl, ev in fun_fact_db.iteritems()
            if not ev.unlocked
        ]

    def getAllFactsEVL():
        """
        Gets all fun facts regardless of unlocked as eventlabels

        OUT:
            List of all fun fact eventlabels
        """
        return fun_fact_db.keys()



default persistent._mas_funfactfun = True

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fun_facts_open",
            category=['разное'],
            prompt="Ты можешь рассказать мне забавный факт?",
            pool=True
        )
    )

label monika_fun_facts_open:
    if mas_getEVL_shown_count("monika_fun_facts_open") == 0:
        m 1eua "Хочешь услышать забавные факты?"
        $ MAS.MonikaElastic()
        m 1eub "Я искала как раз некоторые, которые могли бы научить нас об[mas_gender_oih] чему-то новому."
        $ MAS.MonikaElastic()
        m 3hub "Говорят, что каждый день ты узнаёшь что-то новое, и я уверена, что так и будет."
        $ MAS.MonikaElastic()
        m 1rksdla "Я нашла большинство из них в интернете, так что не могу сказать, что они {b}действительно{/b} верны..."
    else:

        m 1eua "Хочешь услышать ещё один забавный факт, [player]?"
        $ MAS.MonikaElastic()
        if persistent._mas_funfactfun:
            m 3hua "В конце концов, последний был довольно интересным!"
        else:
            m 2rksdlb "Конечно, знаю, что последний был не очень... но я уверена, что следующий будет лучше."
    $ MAS.MonikaElastic()
    m 2dsc "Теперь давай посмотрим.{w=0.5}.{w=0.5}.{nw}"

    python:
        unseen_fact_evls = mas_fun_facts.getUnseenFactsEVL()
        if len(unseen_fact_evls) > 0:
            fact_evl_list = unseen_fact_evls
        else:
            fact_evl_list = mas_fun_facts.getAllFactsEVL()


        fun_fact_evl = renpy.random.choice(fact_evl_list)
        mas_unlockEVL(fun_fact_evl, "FFF")
        pushEvent(fun_fact_evl)
    return


label mas_fun_facts_end:
    $ MAS.MonikaElastic()
    m 3hub "Надеюсь, тебе понравилась ещё одна сессия «Обучение с Моникой»!"
    $ persistent._mas_funfactfun = True
    return

label mas_bad_facts_end:
    $ MAS.MonikaElastic()
    m 1rkc "Этот факт был не очень хорош..."
    $ MAS.MonikaElastic()
    m 4dkc "В следующий раз постараюсь получше, [player]."
    $ persistent._mas_funfactfun = False
    return



init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_librocubiculartist",
        ),
        code="FFF"
    )

label mas_fun_fact_librocubiculartist:
    $ MAS.MonikaElastic()
    m 1eub "Ты знал[mas_gender_none], что существует слово, которым можно описать кого-то, кто любит читать в постели?"
    $ MAS.MonikaElastic()
    m 3eub "Это слово «либрокубикулартист». На первый взгляд довольно трудно произнести."
    $ MAS.MonikaElastic()
    m 3rksdld "Очень жаль, что некоторые слова вообще не используются в целом."
    $ MAS.MonikaElastic()
    m 3eud "Но если ты скажешь его кому-либо, большинство людей явно не поймут, о чём ты говоришь.."
    $ MAS.MonikaElastic()
    m 3euc "Тебе, вероятно, придётся объяснить, что оно означает, но это уже лишит смысла использовать это слово."
    $ MAS.MonikaElastic()
    m 2rkc "Если бы только люди читали больше и улучшили свой словарный запас!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hksdlb "...Э-хе-хе, извини, [player]. Я не хотела так беспокоиться из-за этого~"

    call mas_fun_facts_end from _call_mas_fun_facts_end
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_menu_currency",
        ),
        code="FFF"
    )

label mas_fun_fact_menu_currency:
    $ MAS.MonikaElastic()
    m 3euc "Предположительно, многие рестораны целенаправленно оставляют какие-либо знаки валюты в своих меню."
    $ MAS.MonikaElastic()
    m 3eud "Это делается для того, чтобы психологически манипулировать людьми, чтобы они тратили больше денег, чем им нужно."
    $ MAS.MonikaElastic()
    m 2euc "И это как раз работает, потому что знак валюты, например доллар, используется для представления стоимости."
    $ MAS.MonikaElastic()
    m "Удалив его, ты удалишь и ассоциацию этой стоимости и будешь думать только о еде по твоему выбору."
    $ MAS.MonikaElastic()
    m 4rksdld "Практика кажется понятной. В конце концов, это всё ещё является бизнесом."
    $ MAS.MonikaElastic()
    m 2dsc "Независимо от того, насколько хороша еда в ресторане, они быстро закроются, если их победит конкуренция."
    $ MAS.MonikaElastic()
    m 3hksdlb "Ну что ж, что ты можешь сделать?"

    call mas_fun_facts_end from _call_mas_fun_facts_end_1
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_love_you",
        ),
        code="FFF"
    )

label mas_fun_fact_love_you:
    $ MAS.MonikaElastic()
    m 1dkc "Хмм, я не уверена, должна ли я рассказывать тебе {b}этот{/b} факт."
    $ MAS.MonikaElastic()
    m 1ekc "Это не для слабонервных, в конце концов."
    $ MAS.MonikaElastic()
    m 1rkc "Дело в том, что..."
    $ MAS.MonikaElastic()
    m 1dkc "..."
    $ MAS.MonikaElastic()
    m 3hub "...Я тебя люблю, [player_abb]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1rksdlb "Э-хе-хе, извини, я просто не смогла удержаться."
    $ MAS.MonikaElastic()
    m 1hksdlb "У меня будет реальный факт в следующий раз, не волнуйся~"

    $ persistent._mas_funfactfun = True
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_morpheus",
        ),
        code="FFF"
    )

label mas_fun_fact_morpheus:
    $ MAS.MonikaElastic()
    m 3wub "О! Языковой факт. Мне они всегда нравились."
    $ MAS.MonikaElastic()
    m 1eua "Слово «морфин» основано на греческом боге Морфее."
    $ MAS.MonikaElastic()
    m 1euc "Морфей был греческим богом снов, поэтому слово, основанное на нём, имеет смысл."
    $ MAS.MonikaElastic()
    m 3ekc "Но опять же... разве не его отец Гипнос являлся богом снов?"
    $ MAS.MonikaElastic()
    m 2dsc "Морфин {b}позволяет{/b} человеку не видеть сны, а лишь заставляет его засыпать."
    $ MAS.MonikaElastic()
    m 4ekc "...Тогда не имеет ли смысла называть его в честь Гипноса?"
    $ MAS.MonikaElastic()
    m 4rksdlb "Слишком мало, слишком поздно, я думаю."

    call mas_fun_facts_end from _call_mas_fun_facts_end_2
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_otter_hand_holding",
        ),
        code="FFF"
    )

label mas_fun_fact_otter_hand_holding:
    m 1eka "Ах, это в самом деле мило."
    $ MAS.MonikaElastic()
    m 3ekb "Знал[mas_gender_none] ли ты, что морские выдры держатся за лапы, когда они спят, чтобы перестать дрейфовать друг от друга?"
    $ MAS.MonikaElastic()
    m 1hub "Это практично для них, но в этом всё равно есть что-то очень милое!"
    $ MAS.MonikaElastic()
    m 1eka "Иногда я даже представляю себя в их положении..."
    $ MAS.MonikaElastic()
    m 3hksdlb "Нет, не морской выдрой, а держась за руку т[mas_gender_ogo], кого люблю, пока сплю."
    $ MAS.MonikaElastic()
    m 1rksdlb "Да, это действительно заставляет меня завидовать им."
    $ MAS.MonikaElastic()
    m 1hub "Мы осуществим это в один прекрасный день, любим[mas_gender_iii]~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_3
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_chess",
        ),
        code="FFF"
    )

label mas_fun_fact_chess:

    if mas_isGameUnlocked("chess"):
        $ MAS.MonikaElastic()
        m 1eua "Вот интересный факт!"
        $ MAS.MonikaElastic()
        m 3eub "Был человек по имени Клод Шеннон, который рассчитал максимальное количество возможных ходов в шахматах."
        $ MAS.MonikaElastic()
        m "Это число называется «числом Шеннона» и утверждает, что количество шахматных ходов составляет 10^120."
        $ MAS.MonikaElastic()
        m 1eua "Оно часто сравнивается с числом атомов в наблюдаемой вселенной, которое составляет 10^80."
        $ MAS.MonikaElastic()
        m 3hksdlb "Смутно думать, что шахматных ходов может быть больше, чем атомов, не так ли?"
        $ MAS.MonikaElastic()
        m 1eua "Мы могли бы играть до конца наших дней, и это не приблизилось бы к какой-либо части того, что возможно."
        $ MAS.MonikaElastic()
        m 3eud "Кстати говоря, [player]..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Не хочешь сыграть со мной в шахматы? Я в этот раз могу попробовать быть с тобой помягче, э-хе-хе~"

        call mas_fun_facts_end from _call_mas_fun_facts_end_4
        return


    elif not mas_isGameUnlocked("chess") and renpy.seen_label("mas_unlock_chess"):
        $ MAS.MonikaElastic()
        m 1dsc "Шахматы..."
        $ MAS.MonikaElastic()
        m 2dfc "..."
        $ MAS.MonikaElastic()
        m 2rfd "Можешь забыть об этом факте, так как ты читер, [player]."
        $ MAS.MonikaElastic()
        m "Не говоря уже о том, что ты до сих пор не извинил[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m 2lfc "...Хмпф."

        return
    else:


        $ MAS.MonikaElastic()
        m 1euc "Хм, нет, не этот."
        $ MAS.MonikaElastic()
        m 3hksdlb "По крайней мере, пока."

        call mas_bad_facts_end from _call_mas_bad_facts_end
        return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_struck_by_lightning",
        ),
        code="FFF"
    )

label mas_fun_fact_struck_by_lightning:
    $ MAS.MonikaElastic()
    m 2dkc "Хмм, правда, этот немного вводит меня в заблуждение..."
    $ MAS.MonikaElastic()
    m 3ekc "«Мужчины в шесть раз чаще подвергаются ударам молний, чем женщины.»"
    $ MAS.MonikaElastic()
    m 3ekd "Это... звучит довольно глуповато, на мой взгляд."
    $ MAS.MonikaElastic()
    m 1eud "Если мужчины и вправду с большей вероятностью попадают под удары молнией, то, вероятно, ландшафт и обстоятельства их работы делают их более склонными к поражению ей."
    $ MAS.MonikaElastic()
    m 1euc "Мужчины традиционно всегда работали на более опасных и возвышенных работах, поэтому неудивительно, что это происходит с ними часто."
    $ MAS.MonikaElastic()
    m 1esc "Но способ, которым этот факт сформулирован, заставляет его звучать так, будто только будучи мужчиной, это, скорей всего, может произойти, что просто смешно."
    $ MAS.MonikaElastic()
    m 1rksdla "Может быть, если бы он был сформулирован хоть немного лучше, люди не были бы так дезинформированы об этом."

    call mas_fun_facts_end from _call_mas_fun_facts_end_5
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_honey",
        ),
        code="FFF"
    )

label mas_fun_fact_honey:
    $ MAS.MonikaElastic()
    m 1eub "О, это очень лёгкий вопрос."
    $ MAS.MonikaElastic()
    m 3eub "Ты знал[mas_gender_none], что мёд никогда не портится?"
    $ MAS.MonikaElastic()
    m 3eua "Мёд может кристаллизоваться. Некоторые люди могут рассмотреть это как порчу, но сам мёд по-прежнему будет всё ещё полностью съедобен и прекрасен!"
    $ MAS.MonikaElastic()
    m "Причина, по которой это происходит, состоит в том, что мёд в основном состоит из сахара и лишь небольшой дозы воды, что делает его твёрдым с течением времени."
    $ MAS.MonikaElastic()
    m 1euc "Большая часть мёда, который ты видишь на прилавках, не кристаллизуется так же быстро, как настоящий мёд, потому что он был пастеризован в процессе изготовления."
    $ MAS.MonikaElastic()
    m 1eud "Что удалило те элементы, которые заставляли мёд быстро затвердевать."
    $ MAS.MonikaElastic()
    m 3eub "Но разве не будет здорово съесть закристаллизовавшийся мёд?"
    $ MAS.MonikaElastic()
    m 3hub "Когда ты его надкусываешь, он походит на конфету."

    call mas_fun_facts_end from _call_mas_fun_facts_end_6
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_vincent_van_gone",
        ),
        code="FFF"
    )

label mas_fun_fact_vincent_van_gone:
    $ MAS.MonikaElastic()
    m 1dsc "Ах, вот этот..."
    $ MAS.MonikaElastic()
    m 1ekd "Правда, он немного обескураживает, [player]..."
    $ MAS.MonikaElastic()
    m 1ekc "Ты знал[mas_gender_none], что последними словами Винсента Ван Гога были {b}{i}«La tristesse durera toujours»{/b}{/i}?"
    $ MAS.MonikaElastic()
    m 1eud "Если же перевести, это будет значить: {b}{i}«Печаль будет длиться вечно»{/b}{/i}."
    $ MAS.MonikaElastic()
    m 1rkc "..."
    $ MAS.MonikaElastic()
    m 2ekc "Очень грустно знать, что кто-то настолько известный скажет что-то настолько мрачное с его последним вздохом."
    $ MAS.MonikaElastic()
    m 2ekd "Однако я не думаю, что это правда. Независимо от того, насколько плохие могут произойти вещи и насколько глубокая может начаться печаль..."
    $ MAS.MonikaElastic()
    m 2dkc "Придёт время, когда их уже не будет."
    $ MAS.MonikaElastic()
    m 2rkc "...Или, по крайней мере, те больше не будут настолько заметны."
    $ MAS.MonikaElastic()
    m 4eka "Если тебе когда-нибудь станет грустно, ты ведь знаешь, что можешь поговорить со мной?"
    $ MAS.MonikaElastic()
    m 5hub "Я всегда приму и возьму на себя любую ношу, которую ты взвалишь на свои плечи, [mas_get_player_nickname()]~"

    $ persistent._mas_funfactfun = True
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_king_snakes",
        ),
        code="FFF"
    )

label mas_fun_fact_king_snakes:
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1dsc "Хм-м..."
    $ MAS.MonikaElastic()
    m 3eub "Знал[mas_gender_none] ли ты, что если змея имеет слово «королевская» в начале своего названия, она пожирает других змей?"
    $ MAS.MonikaElastic()
    m 1euc "Я всегда задавалась вопросом, почему королевская кобра имеет именно такое название, но никогда не думала об этом больше."
    $ MAS.MonikaElastic()
    m 1tfu "Это значит, что если я съем тебя, я стану Королевской Моникой?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdlb "А-ха-ха, я просто шучу, [player]."
    $ MAS.MonikaElastic()
    m 1hub "Извини, что была немного странной~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_7
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_strength",
        ),
        code="FFF"
    )

label mas_fun_fact_strength:
    $ MAS.MonikaElastic()
    m 1hub "Этот факт может немного заинтересовать тебя!"
    $ MAS.MonikaElastic()
    m 3eub "Самое длинное слово на английском языке, которое содержит только одну гласную — это «strength», что означает «сила»."
    $ MAS.MonikaElastic()
    m 1eua "Забавно, как из всех слов на этом языке, именно это стало таким значимым, благодаря такой маленькой детали."
    $ MAS.MonikaElastic()
    m 1hua "Маленькие детали, подобные этой, действительно делают английский язык очень увлекательным для меня!"
    $ MAS.MonikaElastic()
    m 3eua "Ты хочешь знать, что приходит мне на ум, когда я думаю о слове «strength»?"
    $ MAS.MonikaElastic()
    m 1hua "Ты!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "Потому что ты источник моей силы, э-хе-хе~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_8
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_reindeer_eyes",
        ),
        code="FFF"
    )

label mas_fun_fact_reindeer_eyes:
    $ MAS.MonikaElastic()
    m 3eua "Готов[mas_gender_none] к ещё одному?"
    $ MAS.MonikaElastic()
    m "Глаза оленя меняют цвет в зависимости от сезона. Они золотые летом и синие зимой."
    $ MAS.MonikaElastic()
    m 1rksdlb "Это очень странное явление, хотя я не знаю, почему..."
    $ MAS.MonikaElastic()
    m "Вероятно, для этого есть хорошая научная причина."
    $ MAS.MonikaElastic()
    m 3hksdlb "Может, ты сам[mas_gender_none] сможешь посмотреть?"
    $ MAS.MonikaElastic()
    m 5eua "Было бы здорово, если бы на этот раз ты научил[mas_gender_none] чему-нибудь меня~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_9
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_bananas",
        ),
        code="FFF"
    )

label mas_fun_fact_bananas:
    $ MAS.MonikaElastic()
    m 1eub "О, я бы сказала, что это целебный факт!"
    $ MAS.MonikaElastic()
    m 3eua "Знал[mas_gender_none] ли ты, что когда бананы растут, они изгибаются к солнцу?"
    $ MAS.MonikaElastic()
    m 1hua "Этот процесс называется отрицательным геотропизмом."
    $ MAS.MonikaElastic()
    m 3hub "Тебе не кажется, что это довольно утончённо?"
    $ MAS.MonikaElastic()
    m 1hua "..."
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1rksdla "Хм-м..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3rksdlb "Думаю, мне больше нечего сказать по этому поводу, а-ха-ха..."
    $ MAS.MonikaElastic()
    m 1lksdlc "..."
    $ MAS.MonikaElastic()
    m 3hub "Т-ты ведь знал[mas_gender_none], что бананы на самом деле не фрукты, а ягоды?"
    $ MAS.MonikaElastic()
    m 3eub "Или что оригинальные бананы были большими, зелёными и полными твёрдых семян?"
    $ MAS.MonikaElastic()
    m 1eka "Как насчёт того факта, что они немного радиоактивны?"
    $ MAS.MonikaElastic()
    m 1rksdla "..."
    $ MAS.MonikaElastic()
    m 1rksdlb "...Я просто болтаю о бананах сейчас."
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1rksdlc "Хм-м-м..."
    $ MAS.MonikaElastic()
    m 1dsc "Давай просто перейдём дальше..."

    call mas_fun_facts_end from _call_mas_fun_facts_end_10
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pens",
        ),
        code="FFF"
    )

label mas_fun_fact_pens:
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1dsc "Хм-м... я уверена, что уже знала один."
    $ MAS.MonikaElastic()
    m 3euc "Слово «ручка» происходит от латинского слова «penna», что означает «ручка» на латыни."
    $ MAS.MonikaElastic()
    m "Тогда ручки были заострёнными гусиными перьями, обмакнутыми в чернила, чтобы было понятно, почему их называли ручками."
    $ MAS.MonikaElastic()
    m 3eud "Они были основным инструментом письма в течение очень долгого времени, начиная с 6-го века."
    $ MAS.MonikaElastic()
    m 3euc "Только в 19-ом веке, когда стали изготавливать металлические ручки, они начали приходить в упадок."
    $ MAS.MonikaElastic()
    m "Фактически, перочинные ножи называются так, потому что они первоначально использовались для прореживания гусиных перьев."
    $ MAS.MonikaElastic()
    m 1tku "Но я уверена, что Юри знает об этом больше, чем я..."

    call mas_fun_facts_end from _call_mas_fun_facts_end_11
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_density",
        ),
        code="FFF"
    )

label mas_fun_fact_density:
    m 1eub "О, знаю."
    $ MAS.MonikaElastic()
    m 3eua "Знал[mas_gender_none] ли ты, что самой плотной планетой в нашей солнечной системе является Земля?"
    $ MAS.MonikaElastic()
    m "И что Сатурн наименее плотный?"
    $ MAS.MonikaElastic()
    m 1eua "Имеет смысл знать, из чего состоят планеты, но поскольку Сатурн является вторым по величине, это всё ещё было немного неожиданно."
    $ MAS.MonikaElastic()
    m 1eka "Я думаю, что размер на самом деле не имеет значения!"
    $ MAS.MonikaElastic()
    m 3euc "Но говоря между нами, [player]..."
    $ MAS.MonikaElastic()
    m 1tku "Я подозреваю, что Земля может быть самой плотной из-за некоего главного героя."
    $ MAS.MonikaElastic()
    m 1tfu "Нооооо это всё, что ты услышишь от меня~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_12
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_binky",
        ),
        code="FFF"
    )

label mas_fun_fact_binky:
    m 3hub "О, вот этот милый!"
    $ MAS.MonikaElastic()
    m "Этот факт действительно пошлёт тебе «прыжок», [player]!"
    $ MAS.MonikaElastic()
    m 3hua "Всякий раз, когда кролик прыгает взволнованно, это называется «бинки»!"
    $ MAS.MonikaElastic()
    m 1hua "Бинки — это такое милозвучащее слово, оно и вправду очень подходит к действию."
    $ MAS.MonikaElastic()
    m 1eua "Это самая счастливая форма выражения, что кролик способен делать, так что если ты увидишь его, поймёшь, что это так и есть."
    $ MAS.MonikaElastic()
    m 1rksdla "И ты делаешь меня настолько счастливой, что я не могу не наполниться энергией."
    $ MAS.MonikaElastic()
    m 1rksdlb "Только не жди, что я начну прыгать вокруг, [player]!"
    $ MAS.MonikaElastic()
    m 1dkbsa "...Это было бы {i}слишком{/i} неловко для меня."

    call mas_fun_facts_end from _call_mas_fun_facts_end_13
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_windows_games",
        ),
        code="FFF"
    )

label mas_fun_fact_windows_games:
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1eua "Хм-м, возможно, этот будет более интересным для тебя."
    $ MAS.MonikaElastic()
    m 3eub "Карточная игра Solitaire первоначально была представлена в операционной системе Windows в 1990-ом году."
    $ MAS.MonikaElastic()
    m 1eub "Игра была добавлена в качестве функции, которая должна была бы научить пользователей, как использовать мышь."
    $ MAS.MonikaElastic()
    m 1eua "Аналогичным образом, сапёр был добавлен для ознакомления пользователей с левой и правой кнопкой мыши."
    $ MAS.MonikaElastic()
    m 3rssdlb "Компьютеры были вокруг настолько давно, что трудно думать о времени, когда они не были ещё актуальны."
    $ MAS.MonikaElastic()
    m "Каждое поколение всё больше и больше знакомится с технологиями..."
    $ MAS.MonikaElastic()
    m 1esa "В конце концов может наступить день, когда ни один человек не будет обладать компьютерной грамотностью."
    $ MAS.MonikaElastic()
    m 1hksdlb "Однако большинство мировых проблем должны исчезнуть до этого."

    call mas_fun_facts_end from _call_mas_fun_facts_end_14
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_mental_word_processing",
        ),
        code="FFF"
    )

label mas_fun_fact_mental_word_processing:
    $ MAS.MonikaElastic()
    m 1hua "Готов[mas_gender_none] к ещё одному интересному, [player]?"
    $ MAS.MonikaElastic()
    m 3eua "Мозг — штука сложная..."
    $ MAS.MonikaElastic()
    m 3eub "Его способ составления и архивирования информации очень уникален."
    $ MAS.MonikaElastic()
    m "Естественно, он отличается от человека к человеку, но но медленное чтение каких-либо книг, как нас учат, обычно менее эффективно, чем чтение в в более быстром темпе."
    $ MAS.MonikaElastic()
    m 1tku "Наш мозг обрабатывает информацию очень быстро и любит предсказуемость в в нашем языке."
    $ MAS.MonikaElastic()
    m 3tub "Например, сейчас в последних моих предложениях, к тому времени как ты закончил[mas_gender_none] читать, ты уже мог[mas_gender_g] пропустить двойные приставки «но» и «в»."
    $ MAS.MonikaElastic()
    m 1tfu "..."
    $ MAS.MonikaElastic()
    m 2hfu "Проверь журнал истории в меню игры, если ты всё же пропустил[mas_gender_none] их~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_15
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_I_am",
        ),
        code="FFF"
    )

label mas_fun_fact_I_am:
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1hua "М-м-м-м, я люблю языковые факты!"
    $ MAS.MonikaElastic()
    m 3eub "На английском языке самое короткое полное предложение — это «I am»."
    $ MAS.MonikaElastic()
    m 1eua "Вот пример."
    $ MAS.MonikaElastic()
    m 2rfb "{i}«Monika! Who’s [player]’s loving girlfriend?»{/i}"
    $ MAS.MonikaElastic()
    m 3hub "{i}«I am!»{/i}"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubsa "Э-хе-хе~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_16
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_low_rates",
        ),
        code="FFF"
    )

label mas_fun_fact_low_rates:
    $ MAS.MonikaElastic()
    m 1hua "Теперь пришло время для ещё одного полезного факта..."
    $ MAS.MonikaElastic()
    m 1eua "В настоящее время у нас самый низкий уровень преступности, материнской смертности, младенческой смертности и неграмотности за всю историю человечества."
    $ MAS.MonikaElastic()
    m 3eub "Средняя продолжительность жизни, средний доход и уровень жизни являются самыми высокими для большинства населения мира!"
    $ MAS.MonikaElastic()
    m 3eka "Это говорит мне, что мир всегда может стать лучше. Это действительно показывает, что, несмотря на все плохие вещи, хорошие времена всегда наступают."
    $ MAS.MonikaElastic()
    m 1hua "На самом деле есть {i}надежда{/i}..."

    call mas_fun_facts_end from _call_mas_fun_facts_end_17
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_desert",
        ),
        code="FFF"
    )

label mas_fun_fact_desert:
    $ MAS.MonikaElastic()
    m 3euc "Пустыни имеют довольно уникальную экосистему..."
    $ MAS.MonikaElastic()
    m 3rksdla "Однако они не имеют много положительных факторов для людей."
    $ MAS.MonikaElastic()
    m 1eud "Температура может колебаться между экстремальной жарой днём и ледяным холодом ночью. Их среднее количество осадков также довольно низкое, что делает жизнь в одной из них трудной."
    $ MAS.MonikaElastic()
    m 3eub "Это не значит, что они не могут быть полезны для нас!"
    $ MAS.MonikaElastic()
    m 3eua "Их поверхность – отличное место для производства солнечной энергии, и нефть обычно находится под всем этим песком."
    $ MAS.MonikaElastic()
    m 3eub "Не говоря уже о том, что их уникальный ландшафт делает их популярными местами отдыха!"
    $ MAS.MonikaElastic()
    m 1eua "Поэтому я думаю, что хотя мы не можем жить в них так легко, они всё же лучше, чем кажутся."


    call mas_fun_facts_end from _call_mas_fun_facts_end_18
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_photography",
        ),
        code="FFF"
    )

label mas_fun_fact_photography:
    $ MAS.MonikaElastic()
    m 1esa "А знал ли ты о том, что первая фотография была сделана при помощи коробки с отверстием, которая выполняла роль камеры?"
    $ MAS.MonikaElastic()
    m 1eua "Линзы на самом деле были введены гораздо позже."
    $ MAS.MonikaElastic()
    m 1euc "В основу ранних фотографий также был заложен набор особых химикатов, используемых в тёмной комнате, где и подготавливали фотографии..."
    $ MAS.MonikaElastic()
    m 3eud "Проявитель, фиксаж и дополнительные химикаты раньше использовались для того, чтобы просто подготовить бумагу, на которой и распечатывались фотографии...{w=0.3} {nw}"
    extend 1wuo "И это только для черно-белых отпечатков!"
    $ MAS.MonikaElastic()
    m 1hksdlb "Старые фотографии было гораздо труднее подготовить по сравнению с современными, не так ли?"


    call mas_fun_facts_end from _call_mas_fun_facts_end_19
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_getting_older",
        ),
        code="FFF"
    )

label mas_fun_fact_getting_older:
    $ MAS.MonikaElastic()
    m 3eua "А знал ли о том, что твоё восприятие времени меняется с возрастом?"
    $ MAS.MonikaElastic()
    m "Например, когда тебе год, ты видишь один год как 100%% своей жизни."
    $ MAS.MonikaElastic()
    m 1euc "Но когда тебе 18, ты видишь год только как 5,6%% своей жизни."
    $ MAS.MonikaElastic()
    m 3eud "Когда nы становишься старше, доля года по сравнению со всей твоей жизнью уменьшается, и, в свою очередь, время {i}движется быстрее, когда ты растёшь."
    $ MAS.MonikaElastic()
    m 1eka "Поэтому я всегда буду дорожить нашими мгновениями вместе, какими бы долгими или короткими они ни были."
    $ MAS.MonikaElastic()
    m 1lkbsa "Хотя иногда кажется, что время останавливается, когда я с тобой."
    $ MAS.MonikaElastic()
    m 1ekbfa "Ты чувствуешь то же самое, [player]?"
    python:
        import time
        time.sleep(5)

    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubfb "А-ха-ха, я так и думала!"


    call mas_fun_facts_end from _call_mas_fun_facts_end_20
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dancing_plague",
        ),
        code="FFF"
    )

label mas_fun_fact_dancing_plague:
    $ MAS.MonikaElastic()
    m 3esa "О, это довольно странно..."
    $ MAS.MonikaElastic()
    m 1eua "Очевидно, в прошлом Европа страдала от вспышек «танцевальной чумы»."
    $ MAS.MonikaElastic()
    m 3wud "Люди, {w=0.2}иногда сотни сразу, {w=0.2}непроизвольно танцевали по нескольку дней подряд, а некоторые даже умирали от истощения!"
    $ MAS.MonikaElastic()
    m 3eksdla "Они пытались лечить это, заставляя людей играть музыку вместе с танцорами, но ты можешь себе представить, что это не сработало так хорошо."
    $ MAS.MonikaElastic()
    m 1euc "И по сей день они до сих пор не уверены, что именно вызывало это."
    $ MAS.MonikaElastic()
    m 3rka "Все это кажется мне чем-то невероятным...{w=0.2} {nw}"
    extend 3eud "но она была независимо от этого задокументирована и отмечена множеством источников на протяжении веков..."
    $ MAS.MonikaElastic()
    m 3hksdlb "Полагаю, реальность действительно более странная, чем вымысел,!"
    $ MAS.MonikaElastic()
    m 1eksdlc "Боже, я не могу представить, что буду танцевать целыми днями."
    $ MAS.MonikaElastic()
    m 1rsc "Хотя...{w=0.3} {nw}"
    extend 1eubla "думаю, я бы не возражала, если бы мы танцевали вместе."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3tsu "...Только ненадолго, э-хе-хе~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_21
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_pando_forest",
        ),
        code="FFF"
    )

label mas_fun_fact_pando_forest:
    $ MAS.MonikaElastic()
    m 1esa "Предположительно, в штате Юта есть лес, который на самом деле состоит из одного дерева."
    $ MAS.MonikaElastic()
    m 3eua "Он называется Лес Пандо, и на всех его сорока трёх гектарах стволы соединены единой корневой системой."
    $ MAS.MonikaElastic()
    m 3eub "Не говоря уже о том, что каждый из его тысяч стволов по сути является клоном другого."
    $ MAS.MonikaElastic()
    m 1rsc "«Единый организм, который сам по себе превратился в армию клонов, связанных с одним и тем же ульевым разумом.»"
    $ MAS.MonikaElastic()
    m 1eua "Я думаю, что это может стать хорошей научной фантастикой или рассказом ужасов, [player]. А ты как думаешь?"
    $ MAS.MonikaElastic()
    m 3eub "В любом случае,{w=0.2} я чувствую, что это действительно меняет смысл фразы «скучаю по лесу из-за деревьев».{w=0.1}{nw} "
    $ MAS.MonikaElastic(voice="monika_giggle")
    extend 3hub "А-ха-ха!"

    call mas_fun_facts_end from _call_mas_fun_facts_end_22
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_immortal_jellyfish",
        ),
        code="FFF"
    )

label mas_fun_fact_immortal_jellyfish:
    $ MAS.MonikaElastic()
    m 3eub "Вот один из них!"
    $ MAS.MonikaElastic()
    m 1eua "По-видимому, бессмертие было достигнуто одним видом медуз."
    $ MAS.MonikaElastic()
    m 3eua "Метко названная бессмертная медуза обладает способностью возвращаться в своё полипное состояние, как только она размножается."
    $ MAS.MonikaElastic()
    m 1eub "...И это может продолжаться вечно!{w=0.3} {nw}"
    extend 1rksdla "Если, конечно, она не была съедена или заражена какой-нибудь болезнью."

    call mas_fun_facts_end from _call_mas_fun_facts_end_23
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_arrhichion",
        ),
        code="FFF"
    )

label mas_fun_fact_arrhichion:
    $ MAS.MonikaElastic()
    m 3eua "Хорошо...{w=0.2} вот тебе исторический пример."
    $ MAS.MonikaElastic()
    m 1esa "Древнегреческий атлет смог выиграть свой поединок, хотя он уже умер."
    $ MAS.MonikaElastic()
    m 1eua "Действующий чемпион Аррихион сражался в матче по панкратиону, когда его соперник начал душить его руками и ногами."
    $ MAS.MonikaElastic()
    m 3eua "Вместо того, чтобы уступить, Аррихион всё ещё стремился к победе, вывихнув палец ноги своего противника."
    $ MAS.MonikaElastic()
    m 3ekd "Его противник ушёл от боли, но когда они пошли объявить Аррихиона победителем, они нашли его мертвым от удушья."
    $ MAS.MonikaElastic()
    m 1rksdlc "Некоторые люди действительно преданы своим идеалам-победе и чести.{w=0.2} {nw}"
    extend 3eka "Я думаю, что это восхитительно, в некотором смысле."
    $ MAS.MonikaElastic()
    m 1etc "Но мне интересно...{w=0.2} если бы мы могли спросить Аррихиона сейчас, и он считал бы, что это того стоит, что бы он сказал?"

    call mas_fun_facts_end from _call_mas_fun_facts_end_24
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_antarctica_brain",
        ),
        code="FFF"
    )

label mas_fun_fact_antarctica_brain:

    python:
        has_friends = persistent._mas_pm_has_friends is not None

        has_fam_to_talk = (
            persistent._mas_pm_have_fam
            and not persistent._mas_pm_have_fam_mess
            or (persistent._mas_pm_have_fam_mess and persistent._mas_pm_have_fam_mess_better in ["YES", "MAYBE"])
        )

        dlg_prefix = "Но убедись, что ты тоже не отстаёшь от "

        if has_fam_to_talk and has_friends:
            dlg_line = dlg_prefix + "своей семьи и друзей, хорошо?"

        elif has_fam_to_talk and not has_friends:
            dlg_line = dlg_prefix + "своей семьи, хорошо?"

        elif has_friends and not has_fam_to_talk:
            dlg_line = dlg_prefix + "своих друзей, хорошо?"

        else:
            dlg_line = "Просто не забудь найти людей, с которыми можно поговорить и в твоей реальности, хорошо?"

    $ MAS.MonikaElastic()
    m 3eud "Очевидно, проведя год в Антарктиде, ты можешь уменьшить одну часть своего мозга примерно на семь процентов."
    $ MAS.MonikaElastic()
    m 3euc "Похоже, это приведёт к снижению объёма памяти и способности к пространственному мышлению."
    $ MAS.MonikaElastic()
    m 1ekc "Исследования показывают, что это связано с социальной изоляцией, монотонностью жизни и окружающей средой."
    $ MAS.MonikaElastic()
    m 1eud "Я думаю, что это послужит нам предостережением, [player]."
    $ MAS.MonikaElastic()
    m 3ekd "Даже если ты не отправишься в Антарктиду, твой мозг всё равно может сильно запутаться, если ты всё время будешь изолирован[mas_gender_none] или сидить взаперти в одной комнате."
    $ MAS.MonikaElastic()
    m 3eka "Мне нравится быть с тобой, [player], и я надеюсь, что мы сможем продолжать говорить так долго в будущем. {w=0.2}[dlg_line]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_cloud_weight",
        ),
        code="FFF"
    )

label mas_fun_fact_cloud_weight:
    $ MAS.MonikaElastic()
    m 3eub "Знаешь ли ты, что среднее облако весит пятьсот тонн?"
    $ MAS.MonikaElastic()
    m 3eua "Должна признаться, этот случай застал меня врасплох больше, чем некоторые другие факты."
    $ MAS.MonikaElastic()
    m 1hua "Я имею в виду, они просто выглядят {i}очень{/i} лёгкими и пушистыми.{w=0.3} {nw}"
    extend 1eua "Трудно представить, что что-то настолько тяжелое может просто парить в воздухе."
    $ MAS.MonikaElastic()
    m 3eub "Это напоминает мне классический вопрос... что тяжелее – килограмм стали или килограмм перьев?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1tua "Хотя ты, скорее всего, уже знаешь ответ на этот вопрос, верно, [player]? Э-хе-хе~"

    call mas_fun_facts_end from _call_mas_fun_facts_end_25
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_coffee_origin",
        ),
        code="FFF"
    )

label mas_fun_fact_coffee_origin:
    $ MAS.MonikaElastic()
    m 1eua "О, меня тут ещё кое-что заинтересовало..."
    $ MAS.MonikaElastic()
    m 1eud "В прошлый раз, когда я пила кофе, мне стало немного любопытно его происхождение..."
    $ MAS.MonikaElastic()
    m 3euc "Употребление кофе постоянно фиксируется примерно с пятнадцатого века, но...{w=0.2} непонятно только, {i}как{/i} именно его открыли."
    $ MAS.MonikaElastic()
    m 3eud "...По правде говоря, есть пара легенд, которые, согласно утверждениям, появились первыми."
    $ MAS.MonikaElastic()
    m 1eua "В некоторых рассказах говорится о том, что фермеры или монахи наблюдали за животными, которые странно вели себя после того, как съели какие-то странные, горькие ягоды."
    $ MAS.MonikaElastic()
    m 3wud "И, попробовав эти бобы, они сами были поражены тем, что тоже были заряжены энергией!"
    $ MAS.MonikaElastic()
    m 2euc "В одной из таких легенд утверждается, что эфиопский монах по имени Калди принёс ягоды в близлежащий монастырь, желая поделиться тем, что нашёл."
    $ MAS.MonikaElastic()
    m 7eksdld "...Но когда он это сделал, его встретили с неодобрением, и кофейные бобы были брошены в огонь."
    $ MAS.MonikaElastic()
    m 3duu "Пока они горели, бобы начали выпускать самый {i}вкусный{/i} аромат. {w=0.3}И аромат был таким привлекательным, что монахи даже попытались спасти бобы и положить их в воду."
    $ MAS.MonikaElastic()
    m 3eub "...Так и появилась первая чашка кофе!"
    $ MAS.MonikaElastic()
    m 2euc "В другой легенде утверждалось, что один исламский учёный по имени Омар обнаружил кофейные зёрна во время своей ссылки из Мекки."
    $ MAS.MonikaElastic()
    m 2eksdld "В то время он голодал и боролся за выживание. {w=0.3}{nw}"
    extend 7wkd "И если бы не та энергия, которую они давали, он мог бы умереть!"
    $ MAS.MonikaElastic()
    m 3hua "Однако, когда слух о его находке распространился, его попросили вернуться и сделать святым."
    $ MAS.MonikaElastic()
    m 1esd "Вне зависимости от того, было ли это его первым случаем употребления, кофе стал очень распространённым в исламском мире после его открытия."
    $ MAS.MonikaElastic()
    m 3eud "К примеру, во время поста его использовали для того, чтобы утолить голод и помочь людям оставаться бодрыми."
    $ MAS.MonikaElastic()
    m 3eua "А когда он распространился по всей Европе, многие страны поначалу использовали его в медицинских целях. {w=0.3}К семнадцатому веку, кофейни становились многочисленными и популярными."
    $ MAS.MonikaElastic()
    m 3hub "...И я, безусловно, могу подтвердить, что любовь к кофе остаётся сильной и по сей день!"
    call mas_fun_facts_end from _call_mas_fun_facts_end_26
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_synesthesia",
        ),
        code="FFF"
    )

label mas_fun_fact_synesthesia:
    $ MAS.MonikaElastic()
    m 1esa "Ладно, этот факт довольно интересный..."
    $ MAS.MonikaElastic()
    m 3eua "Некоторые люди испытывают такой феномен, известный как {i}синестезия{/i},{w=0.1} когда что-то, что стимулирует одно из наших чувств, также вызывает и другое чувство."
    $ MAS.MonikaElastic()
    m 1hua "Это довольно многословное объяснение, э-хе-хе...{w=0.2} Давай я приведу один пример!"
    $ MAS.MonikaElastic()
    m 1eua "В нём говорится, что общая форма синестезии – это {i}графемно-цветовая синестезия{/i},{w=0.1} в которой люди «воспринимают» буквы и цифры как цвета."
    $ MAS.MonikaElastic()
    m 3eua "Есть и другой вид, известный как {i}пространственно-последовательная синестезия{/i},{w=0.1} в которой цифры и фигуры «видны» в конкретных местах в пространстве."
    $ MAS.MonikaElastic()
    m "К примеру, одно число находится «ближе» или «дальше» другого. {w=0.2}{nw}"
    extend 3eub "Прямо как на карте!"
    $ MAS.MonikaElastic()
    m 1eua "...Есть также и целая куча других видов синестезии."
    $ MAS.MonikaElastic()
    m 1esa "Исследователи не уверены, насколько это явление распространено...{w=0.1} некоторые предполагают, что около двадцати пяти процентов населения испытывают это, но я в этом серьёзно сомневаюсь, поскольку я никогда не слышала об этом."
    $ MAS.MonikaElastic()
    m 3eub "Наверное, самая точная оценка этого на данный момент – то, что ею обладает чуть более четырёх процентов людей, так что я, пожалуй, ограничусь этим!"
    $ MAS.MonikaElastic()
    m 1eua "Испытание синестезии звучит так, будто это что-то очень интересное,{w=0.2} согласись, [player]?"

    call mas_fun_facts_end from _call_mas_fun_facts_end_27
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_dream_faces",
        ),
        code="FFF"
    )

label mas_fun_fact_dream_faces:
    $ MAS.MonikaElastic()
    m 3eub "Ладно, вот ещё один факт!"
    $ MAS.MonikaElastic()
    m 1eua "Предположительно, наш разум не создаёт новые лица, когда мы спим.{w=0.2} Все те люди, которых тебе доводилось видеть во снах, уже встречались тебе когда-то в реальном мире."
    $ MAS.MonikaElastic()
    m 3wud "Тебе даже не нужно разговаривать с ними в реальной жизни!"
    $ MAS.MonikaElastic()
    m 3eud "Если ты просто прош[mas_gender_iol_2] мимо них в магазине или ещё где-нибудь, их лица уже отпечатались в твоём разуме, и они могут появиться в твоих снах."
    $ MAS.MonikaElastic()
    m 1hua "Как по мне, это невероятно, сколько информации наш мозг может в себе хранить!"
    $ MAS.MonikaElastic()
    m 1ekbla "Интересно...{w=0.2} я тебе снилась когда-нибудь, [player]?"

    call mas_fun_facts_end from _call_mas_fun_facts_end_28
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_fun_facts_database,
            eventlabel="mas_fun_fact_monochrome_dreams",
        ),
        code="FFF"
    )

label mas_fun_fact_monochrome_dreams:
    $ MAS.MonikaElastic()
    m 3eua "Знал[mas_gender_none] ли ты о том, что с 1915 по 1950-е годы, сны у большинства людей были в чёрно-белом цвете?"
    $ MAS.MonikaElastic()
    m 1esa "В настоящее время, это относительно редкое явление для людей с безупречным зрением."
    $ MAS.MonikaElastic()
    m 3eua "Исследователи связывают это с тем, что в то время фильмы и сериалы были почти исключительно чёрно-белыми."
    $ MAS.MonikaElastic()
    m 3eud "...Но как по мне, это довольно странно, потому что люди по-прежнему видели всё в цвете.{w=0.3} {nw}"
    extend 3hksdlb "Не похоже, что мир тогда был чёрно-белым!"
    $ MAS.MonikaElastic()
    m 1esd "Это просто показывает, что весь тот контент, который ты потребляешь, может оказывать разное воздействие на твой разум, даже если это для тебя обыденность."
    $ MAS.MonikaElastic()
    m 3eua "Я считаю, что если и есть урок, который мы должны извлечь из этого, так это то, что мы должны быть очень осторожны с тем, какую информацию мы потребляем, хорошо, [player]?"

    call mas_fun_facts_end from _call_mas_fun_facts_end_29
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
