













init 4 python in mas_gtod:

    import datetime
    import store.evhand as evhand

    M_GTOD = "monika_gtod_tip{:0>3d}"

    def has_day_past_tip(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """
        
        tip_ev = evhand.event_database.get(
            M_GTOD.format(tip_num),
            None
        )
        
        return (
            tip_ev is not None
            and tip_ev.last_seen is not None
            and tip_ev.timePassedSinceLastSeen_d(datetime.timedelta(days=1))
        )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip000",
            category=["советы по грамматике"],
            prompt="Можешь научить меня грамматике?",
            pool=True,
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST}
        )
    )

label monika_gtod_tip000:
    m 3eub "Конечно, я обучу тебя грамматике, [player]!"
    $ MAS.MonikaElastic()
    m 3hua "Я так рада тому, что ты хочешь улучшить свои писательские навыки."
    $ MAS.MonikaElastic()
    m 1eub "По правде говоря, я читала пару книг про правописание, и, думаю, мы можем обсудить несколько интересных тем!"
    $ MAS.MonikaElastic()
    m 1rksdla "Должна признать...{w=0.5}как-то странно обсуждать что-то специфичное, как грамматику."
    $ MAS.MonikaElastic()
    m 1rksdlc "Знаю, это не самая интересная вещь, которая приходит людям на ум."
    $ MAS.MonikaElastic()
    m 3eksdld "...Наверное, ты думаешь о строгих учителях, или даже о высокомерных редакторах..."
    $ MAS.MonikaElastic()
    m 3eka "Но я считаю, что в освоении написания и красноречивом передаче своего посыла есть определённая красота."
    $ MAS.MonikaElastic()
    m 1eub "И поэтому...{w=0.5}начиная с сегодняшнего дня, я расскажу тебе грамматический совет дня от Моники!"
    $ MAS.MonikaElastic()
    m 1hua "Давай улучшим наш стиль письма вместе, [mas_get_player_nickname()]~"
    $ MAS.MonikaElastic()
    m 3eub "Мы начнём с формулировки, основных схем построения предложений!"


    $ mas_hideEVL("monika_gtod_tip000", "EVE", lock=True, depool=True)


    $ tip_label = "monika_gtod_tip001"
    $ mas_showEVL(tip_label, "EVE", unlock=True, _pool=True)
    $ pushEvent(tip_label,skipeval=True)
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip001",
            category=["советы по грамматике"],
            prompt="Формулировки"
        )
    )

label monika_gtod_tip001:
    m 3eud "Возможно, ты уже знаешь об этом, но формулировка является группой слов, у которых есть подлежащее и сказуемое, или только основа."
    $ MAS.MonikaElastic()
    m 1euc "В основном, формулировки делятся на независимые и зависимые формы."
    $ MAS.MonikaElastic()
    m 1esd "Независимые формулировки могут сами образовывать предложения, например: {b}«я написала это»{/b}."
    $ MAS.MonikaElastic()
    m 3euc "Зависимые формы, с другой стороны, не могут образовать предложение, и они, как правило, являются частями более длинного предложения."
    $ MAS.MonikaElastic()
    m 3eua "Примером такой формы может послужить фраза {b}«тот, кто спас её»{/b}."
    $ MAS.MonikaElastic()
    m 3eud "Здесь есть подлежащее {b}«кто»{/b} и сказуемое {b}«спас»{/b}, но сама формулировка не может сама по себе являться предложением."
    $ MAS.MonikaElastic()
    m 1ekbsa "...{w=0.5}Думаю, ты знаешь, как закончить это предложение, [player]~"
    $ MAS.MonikaElastic()
    m 3eub "Ладно, на сегодня урок окончен. Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip002",
            category=["советы по грамматике"],
            prompt="Связи запятыми и пунктуация",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(1)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip002:
    m 1eua "Помнишь, как мы разговаривали о формулировках, [player]?"
    $ MAS.MonikaElastic()
    m 1eud "Есть одна очень распространённая ошибка, которую допускают писатели, когда связывают их."
    $ MAS.MonikaElastic()
    m 3esc "Когда ты связываешь две независимые формулировки вместе, это – связь запятыми."
    $ MAS.MonikaElastic()
    m 3esa "Вот пример: {w=0.5}{b}«Я зашла в парк, я взглянула на небо, я увидела множество звёзд»{/b}."
    $ MAS.MonikaElastic()
    m 1eua "На первый взгляд, это не кажется проблемой, но ты только представь, как к этому предложению добавляется всё больше и больше формулировок..."
    $ MAS.MonikaElastic()
    m 3wud "В результате получается полная неразбериха!"
    $ MAS.MonikaElastic()
    m 1esd "{b}«Я зашла в парк, я взглянула на небо, я увидела множество звёзд, я увидела пару созвездий, и одно из них было похоже на краба...». {w=0.5}Это может продолжаться до бесконечности."
    $ MAS.MonikaElastic()
    m 1eua "Лучший способ не допустить эту ошибку – разделить независимые формулировки точками, союзами или точками с запятой."
    $ MAS.MonikaElastic()
    m 1eud "Союз, в основном, является словом, которое ты используешь для связи двух формулировок или предложений."
    $ MAS.MonikaElastic()
    m 3eub "Сами по себе они являются довольно интересной темой, мы перейдём к их изучению в будущем совете!"
    $ MAS.MonikaElastic()
    m 3eud "Ладно, давай возьмём тот пример, что мы придумали раньше, и добавим к нему союз и точку, чтобы сделать наше предложение более эффективным..."
    $ MAS.MonikaElastic()
    m 1eud "«Я зашла в парк и взглянула на небо, и там я увидела множество звёзд»."
    $ MAS.MonikaElastic()
    m 3hua "Намного лучше, соглас[mas_gender_en]?"
    $ MAS.MonikaElastic()
    m 1eub "Это всё на сегодня, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip003",
            category=["советы по грамматике"],
            prompt="Союзы",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(2)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip003:
    m 1eub "Итак, [player]! Думаю, пришла пора поговорить нам о...{w=0.5} союзах!"
    $ MAS.MonikaElastic()
    m 3esa "Как я уже говорила раньше, союзы являются словами или фразами, которые соединяют два предложения вместе."
    $ MAS.MonikaElastic()
    m 3wud "Если подумать, то это довольно обширная категория! В ней так много слов, которые мы можем использовать для достижения этого."
    $ MAS.MonikaElastic()
    m 1euc "Только представь разговор без союзов..."
    $ MAS.MonikaElastic()
    m 1esc "Это было бы скучно. {w=0.3}У тебя было бы неспокойное звучание. {w=0.3}Эти предложения связаны меж собой. {w=0.3}Мы должны их соединить."
    $ MAS.MonikaElastic()
    m 3eua "Как видишь, союзы прекрасно подходят для объединения идей, и в то же время, они придают твоему стилю письма спокойное звучание и большую схожесть с реальной манерой речи."
    $ MAS.MonikaElastic()
    m 1eua "А теперь, давай вернёмся к нашему прошлому примеру, но на этот раз мы применим союзы..."
    $ MAS.MonikaElastic()
    m 1eub "{b}«Это было бы скучно, да и у тебя было бы неспокойное звучание. Поскольку эти предложения связаны меж собой, мы должны их соединить»{/b}."
    $ MAS.MonikaElastic()
    m 3hua "Намного лучше, соглас[mas_gender_en]?"
    $ MAS.MonikaElastic()
    m 1esa "Так или иначе, есть три типа союзов: {w=0.5}cоединительные, сравнительные и подчинительные."
    $ MAS.MonikaElastic()
    m 1hksdla "Их названия могут звучать немного обескураживающе, но я уверяю, что в них окажется гораздо больше смысла, как только мы пройдёмся по ним. Я буду давать тебе примеры по ходу дела."
    $ MAS.MonikaElastic()
    m 1esd "Соединительные формулировки связывают два слова, фразы или формулировки такого же «ранга» вместе. Это лишь означает, что они должны быть одного типа... слова со словами, или формулировки с формулировками."
    $ MAS.MonikaElastic()
    m 3euc "В некоторые распространённые примеры входят следующие союзы: {w=0.5}{b}«и»{/b}, {b}«или»{/b}, {b}«но»{/b}, {b}«так»{/b} и {b}«пока»{/b}."
    $ MAS.MonikaElastic()
    m 3eub "Ты можешь связать независимые формулировки, {i}и{/i} ты сможешь избежать применения связей запятыми!"
    $ MAS.MonikaElastic()
    m 1esd "Сравнительные союзы являются формой союзов, применяемой для связывания идей."
    $ MAS.MonikaElastic()
    m 3euc "Есть несколько распространённых пар: {w=0.5}«{b}либо{/b}/{b}или{/b}», «{b}оба{/b}/{b}и{/b}» и «{b}независимо от того{/b}/{b}или{/b}»."
    $ MAS.MonikaElastic()
    m 3eub "{i}Независимо от того{/i}, осознал ты это {i}или{/i} нет, мы используем их всё время... прямо как в этом предложении!"
    $ MAS.MonikaElastic()
    m 1esd "Кроме того, подчинительные союзы соединяют вместе независимые и зависимые формулировки."
    $ MAS.MonikaElastic()
    m 3eub "Как ты понимаешь, есть много способов сделать это!"
    $ MAS.MonikaElastic()
    m 3euc "Сюда входят следующие примеры: {w=0.5}{b}«хотя»{/b}, {b}«до тех пор»{/b}, {b}«с тех пор, как»{/b}, {b}«пока»{/b} и {b}«раз уж»{/b}."
    $ MAS.MonikaElastic()
    m 3eub "И {i}раз уж{/i} их существует целое множество, эта категория союзов является самой широкой!"
    $ MAS.MonikaElastic()
    m 3tsd "О, и ещё кое-что... {w=0.5}есть довольно распространённое заблуждение касающееся того, что ты не должен начинать предложения с союзов."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "Раз уж я показала тебе те два примера, ты определённо можешь это сделать, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 1rksdla "Но их использованием лучше пренебречь. Иначе у тебя получится неестественное звучание."
    $ MAS.MonikaElastic()
    m 1eub "Думаю, на сегодня этого будет достаточно, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip004",
            category=["советы по грамматике"],
            prompt="Точки с запятыми",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(3)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip004:
    m 1eua "Сегодня мы поговорим о довольно редком и самом распространённом заблуждении, связанным с знаком препинания..."
    $ MAS.MonikaElastic()
    m 3eub "Точка с запятой!"
    $ MAS.MonikaElastic()
    m 3eua "О точке с запятой написали парочку интересных вещей, в их числе и этот рассказ от Льюиса Томаса..."
    $ MAS.MonikaElastic()
    m 1esd "{i}«Бывает, глядишь мельком на точки с запятой приход, пара линий стремится вдаль, и это словно восхождение на крутую тропу через лес, и в глаза деревянная скамья бросается, что стоит на изгибе дороги...»."
    $ MAS.MonikaElastic()
    m 1esa "{i}«...место, где ты можешь присесть на минутку и дыхание перевести»{/i}."
    $ MAS.MonikaElastic()
    m 1hua "Я правда ценю то, как ярко он описал такой простой предмет, как знак препинания!"
    $ MAS.MonikaElastic()
    m 1euc "Некоторые люди считают, что ты можешь использовать точку с запятой как альтернативу двоеточию, в то время как остальные используют его в качестве точки..."
    $ MAS.MonikaElastic()
    m 1esd "Если ты помнишь наш разговор про формулировки, двоеточие предназначено для соединения двух независимых формулировок."
    $ MAS.MonikaElastic()
    m 3euc "Например, если бы я хотела свести два предложения, а именно – {b}«ты здесь»{/b} и {b}«я счастлива»{/b}, вместе, то я бы записала их следующим образом..."
    $ MAS.MonikaElastic()
    m 3eud "{b}«Ты здесь; я счастлива»{/b}, а не {b}«Ты здесь и я счастлива»{/b} или {b}«Ты здесь. Я счастлива»{/b}."
    $ MAS.MonikaElastic()
    m 1eub "Все три предложения несут в себе один и тот же посыл, но, по сравнению с ними, {b}«Ты здесь; я счастлива»{/b} связывает две формулировки, достигнув золотой середины."
    $ MAS.MonikaElastic()
    m 1esa "В конце концов, это всегда зависит от предложений, которые ты хочешь связать, но я считаю, что Томас удачно высказался по этому поводу, если сравнивать их с точками или запятыми."
    $ MAS.MonikaElastic()
    m 1eud "В отличие от точки, которая раскрывает совершенно иное предложение, или запятой, которая показывает тебе, что в одном и том же предложении есть нечто большее..."
    $ MAS.MonikaElastic()
    m 3eub "Точка с запятой является чем-то посередине, или, как говорил Томас – {i}«место, где ты можешь присесть на минутку и дыхание перевести»{/i}."
    $ MAS.MonikaElastic()
    m 1esa "По крайней мере, это даёт тебе совершенно иной выбор; надеюсь, теперь ты найдёшь лучшее применение точке с запятой во время написания текста..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе."
    $ MAS.MonikaElastic()
    m 1eub "Ладно, на сегодня это всё, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip005",
            category=["советы по грамматике"],
            prompt="Субъекты и объекты",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(4)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip005:
    m 1eua "Сегодня мы поговорим о субъектах и объектах, [player]."
    $ MAS.MonikaElastic()
    m 1eud "Помнишь, как я говорила о формулировках с подлежащим и сказуемым?"
    $ MAS.MonikaElastic()
    m 3eub "Объект – это человек или предмет, к которому обращается подлежащее!"
    $ MAS.MonikaElastic()
    m 1eua "То есть, в предложении {b}«Мы вместе смотрели на фейерверки»{/b} объектом будут являться...{w=0.5}{b}«фейерверки»{/b}."
    $ MAS.MonikaElastic()
    m 3esd "О, следует также учесть, что для сформирования полных предложений упоминание объектов не является обязательным..."
    $ MAS.MonikaElastic()
    m 1eua "Предложение вполне может состоять только из следующих слов: {b}«Мы смотрели»{/b}."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hksdlb "Это полное предложение... хоть и самое неоднозначное, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eud "И нигде не сказано о том, что объект должен упоминаться в последнюю очередь, но я расскажу об этом в подробностях позже."
    $ MAS.MonikaElastic()
    m 3esa "Просто помни о том, что субъект выполняет действие, а с объектом взаимодействуют."
    $ MAS.MonikaElastic()
    m 1eub "Ладно, это всё на сегодня..."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none], [player]! Я люблю..."
    $ MAS.MonikaElastic()
    m 1eua "..."
    $ MAS.MonikaElastic()
    m 1tuu "..."
    $ MAS.MonikaElastic()
    m 3hub "Тебя!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip006",
            category=["советы по грамматике"],
            prompt="Активный и пассивный залоги",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(5)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip006:
    m 1eud "[player], ты знаешь о залогах в письме?"
    $ MAS.MonikaElastic()
    m 3eua "Есть как активный залог, так и пассивный."
    $ MAS.MonikaElastic()
    m 3euc "Если ты помнишь наш разговор о субъектах и объектах, большое отличие между двумя залогами заключается в том, что идёт первым: субъект или объект."
    $ MAS.MonikaElastic()
    m 1esd "Предположим, субъектом является {b}«Сайори»{/b}, а объектом – {b}«кекс»{/b}."
    $ MAS.MonikaElastic()
    m 3eud "Вот предложение в активном залоге: {w=0.5}{b}«Сайори съела последний кекс»{/b}."
    $ MAS.MonikaElastic()
    m 3euc "А вот оно же, но в пассивном залоге: {w=0.5}{b}«Последний кекс был съеден»{/b}."
    $ MAS.MonikaElastic()
    m 1eub "Как видишь, ты можешь использовать пассивный залог, чтобы скрыть субъект, хоть он и остался по-прежнему в полном предложении."
    $ MAS.MonikaElastic()
    m 1tuu "Это правда; ты {i}можешь{/i} использовать пассивный залог, чтобы не выдать себя! {w=0.5}Впрочем, у него есть и другие виды применения."
    $ MAS.MonikaElastic()
    m 3esd "К примеру, в некоторых профессиях, люди должны использовать пассивный залог, чтобы не упоминать свою личность."
    $ MAS.MonikaElastic()
    m 3euc "Учёные описывают эксперименты фразой {b}«результаты были записаны...»{/b}, поскольку самой главной частью является их работа, а не тот, кто сделал её."
    $ MAS.MonikaElastic()
    m 1esa "Так или иначе, в основном, активный залог используют для читабельности и, ну, знаешь, чтобы прямо сказать о том, кто и что сделал."
    $ MAS.MonikaElastic()
    m 1eub "Думаю, этого будет достаточно на сегодня, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip007",
            category=["советы по грамматике"],
            prompt="Кто против Который",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(6)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip007:
    m 1eua "Сегодня мы поговорим об использовании {b}«кто»{/b} и {b}«который»{/b}."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "В большинстве случаев, похоже, люди просто используют {b}«кто»{/b}, не имея никакого желания понять разницу, а-ха-ха."
    $ MAS.MonikaElastic()
    m 1esd "Разница в том, что {b}«кто»{/b} отсылается на субъект, а {b}«который»{/b} – на объект."
    $ MAS.MonikaElastic()
    m 3eub "Оказывается, выяснить, когда надо использовать то или иное слово, довольно просто!"
    $ MAS.MonikaElastic()
    m 1euc "{b}«Кто»{/b} соответствует словам «{b}он{/b}/{b}она{/b}/{b}они{/b}», в то время как {b}«который»{/b} соответствует «{b}ему{/b}/{b}ей{/b}/{b}им{/b}»."
    $ MAS.MonikaElastic()
    m 3eud "Просто замени возможное {b}«кто»{/b} или {b}«который»{/b} на «{b}он{/b}/{b}она{/b}/{b}они{/b}» или «{b}ему{/b}/{b}ей{/b}/{b}им{/b}»."
    $ MAS.MonikaElastic()
    m 1eua "Всего одна замена должна нести в себе смысл, и это подскажет тебе, какое слово использовать!"
    $ MAS.MonikaElastic()
    m 3eua "Давай, в качестве примера, возьмём название моего стихотворения, {i}«Леди, которая знает всё»{/i}."
    $ MAS.MonikaElastic()
    m 3esd "Если мы взглянем на формулировку {b}«которая знает всё»{/b} и поменяем слово {b}«которая»{/b}, то мы получим..."
    $ MAS.MonikaElastic()
    m 1esd "{b}«Она знает всё»{/b} или {b}«ей всё известно»{/b}."
    $ MAS.MonikaElastic()
    m 3euc "Более осмысленной кажется фраза {b}«она знает всё»{/b}, следовательно, правильно будет {b}«которая знает всё»{/b}."
    $ MAS.MonikaElastic()
    m 1hksdla "Кто сказал, что писать тексты сложно?"
    $ MAS.MonikaElastic()
    m 1eub "Это всё на сегодня, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip08",
            category=["советы по грамматике"],
            prompt="Оксфордская запятая",
            pool=True,
            conditional="store.mas_gtod.has_day_past_tip(7)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_gtod_tip08:
    m 3eud "А знал[mas_gender_none] ли ты о том, что одна дискуссия, касающаяся расположения конкретной запятой в списке из трёх элементов, не утихает и по сей день?"
    $ MAS.MonikaElastic()
    m 3eub "Её называют Оксфордской – или серийной – запятой, и она стала известной благодаря полному изменению смысла предложения!"
    $ MAS.MonikaElastic()
    m 1esa "Позволь мне показать тебе, что я имею в виду..."
    $ MAS.MonikaElastic()
    m 1hub "С Оксфордской запятой, я бы сказала следующее: {b}«Я люблю [mas_name_whom], читать, и писать»{/b}."
    $ MAS.MonikaElastic()
    m 1eua "Без Оксфордской запятой, я бы сказала следующее: {b}«Я люблю [mas_name_whom], читать и писать»{/b}."
    $ MAS.MonikaElastic()
    m 3eud "Путаница заключается в том, что я имею в виду: люблю ли я три разные вещи, или я люблю только тебя, когда ты читаешь и пишешь."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "Разумеется, оба варианта здесь справедливы, поэтому никакой путаницы для меня здесь не возникает, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eua "Это всё на сегодня, [player]."
    $ MAS.MonikaElastic()
    m 3hub "Спасибо, что выслушал[mas_gender_none]!"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
