# Module for Monika story telling
#
# Stories will get unlocked one at by session
# The unlocking logic has been added to script-ch30
# The topic that triggers the Story menu is monika_short_stories
# Topic is unlocked at the beginning of the game and is not
# random
# New rule: pool property as true means that the story gets unlocked
# by some other way and can't be unlocked randomly


# dict of tples containing the stories event data
default persistent._mas_story_database = dict()

#Debug var to test scares
default mas_full_scares = False

# dict storing the last date we saw a new story of normal and scary type
default persistent._mas_last_seen_new_story = {"normal": None, "scary": None}

#Flag to mark if the setup for scary stories has been done
define mas_scary_story_setup_done = False

# store containing stories-related things
init -1 python in mas_stories:
    import store
    import datetime

    UNLOCK_NEW = "unlock_new"

    # TYPES:
    TYPE_NORMAL = "normal"
    TYPE_SCARY = "scary"


    STORY_RETURN = "Не важно."
    story_database = dict()

    #Time between story unlocks of the same type (in hours). Changes over sessions, but also changes after the next story unlocks
    TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)

    #TODO: Build functions to 'register' story types. This will add all related info to the map
    #saving the manual additions to each part


    #Story which starts unlocked for a specific type
    FIRST_STORY_EVL_MAP = {
        TYPE_SCARY: "mas_scary_story_hunter",
        TYPE_NORMAL: "mas_story_tyrant"
    }

    #Override maps to have special conditionals for specific story types
    NEW_STORY_CONDITIONAL_OVERRIDE = {
        TYPE_SCARY: (
            "mas_stories.check_can_unlock_new_story(mas_stories.TYPE_SCARY, ignore_cooldown=store.mas_isO31())"
        ),
    }

    def check_can_unlock_new_story(story_type=TYPE_NORMAL, ignore_cooldown=False):
        """
        Checks if it has been at least one day since we've seen the last story or the initial story

        IN:
            story_type - story type to check if we can unlock a new one
                (Default: TYPE_NORMAL)
            ignore_cooldown - Whether or not we ignore the cooldown or time between new stories
                (Default: False)
        """
        global TIME_BETWEEN_UNLOCKS
        
        new_story_ls = store.persistent._mas_last_seen_new_story.get(story_type, None)
        
        #Get the first story of this type
        first_story = FIRST_STORY_EVL_MAP.get(story_type, None)
        
        #If this doesn't have an initial, no go
        if not first_story:
            return False
        
        can_show_new_story = (
            store.seen_event(first_story)
            and (
                ignore_cooldown
                or store.mas_timePastSince(new_story_ls, datetime.timedelta(hours=TIME_BETWEEN_UNLOCKS))
            )
            and len(get_new_stories_for_type(story_type)) > 0
        )
        
        #If we're showing a new story, randomize the time between unlocks again
        if can_show_new_story:
            TIME_BETWEEN_UNLOCKS = renpy.random.randint(20, 28)
        
        return can_show_new_story

    def get_new_stories_for_type(story_type):
        """
        Gets all new (unseen) stories of the given ype

        IN:
            story_type - story type to get

        OUT:
            list of locked stories for the given story type
        """
        return store.Event.filterEvents(
            story_database,
            pool=False,
            aff=store.mas_curr_affection,
            unlocked=False,
            flag_ban=store.EV_FLAG_HFNAS,
            category=(True, [story_type])
        )

    def get_and_unlock_random_story(story_type=TYPE_NORMAL):
        """
        Unlocks and returns a random story of the provided type

        IN:
            story_type - Type of story to unlock.
                (Default: TYPE_NORMAL)
        """
        #Get locked stories
        stories = get_new_stories_for_type(story_type)
        
        #Grab one of the stories
        story = renpy.random.choice(stories.values())
        
        #Unlock and return its eventlabel
        story.unlocked = True
        
        return story.eventlabel

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_short_stories",
            category=['литература'],
            prompt="Можешь рассказать мне историю?",
            pool=True,
            unlocked=True
        )
    )

label monika_short_stories:
    call monika_short_stories_premenu(None)
    return _return

label monika_short_stories_premenu(story_type=None):
    python:
        #Because this isn't set properly if it's in the default param value, we assign it here
        if story_type is None:
            story_type = mas_stories.TYPE_NORMAL
        end = ""

label monika_short_stories_menu:
    # TODO: consider caching the built stories if we have many story categories
    python:
        #Determine if a new story can be unlocked
        can_unlock_story = False

        if story_type in mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE:
            try:
                can_unlock_story = eval(mas_stories.NEW_STORY_CONDITIONAL_OVERRIDE[story_type])
            except Exception as ex:
                store.mas_utils.mas_log.error("Failed to evaluate conditional to unlock new story because '{0}'".format(ex))
                
                can_unlock_story = False

        else:
            can_unlock_story = mas_stories.check_can_unlock_new_story(story_type)

        # build menu list
        stories_menu_items = [
            (story_ev.prompt, story_evl, False, False)
            for story_evl, story_ev in mas_stories.story_database.iteritems()
            if Event._filterEvent(
                story_ev,
                pool=False,
                aff=mas_curr_affection,
                unlocked=True,
                flag_ban=EV_FLAG_HFM,
                category=(True, [story_type])
            )
        ]

        # also sort this list
        stories_menu_items.sort()

        #Add new story
        stories_menu_items.insert(0, ("Давай новую историю", mas_stories.UNLOCK_NEW, True, False))

        # build switch button
        #TODO: Build a generalized switch for more than just two items
        if story_type == mas_stories.TYPE_SCARY:
            switch_str = "короткую"
        else:
            switch_str = "страшную"

        switch_item = ("Я бы хотел услышать " + switch_str + " историю", "monika_short_stories_menu", False, False, 20)

        final_item = (mas_stories.STORY_RETURN, False, False, False, 0)

    # move Monika to the left
    show monika 1eua at t21

    if story_type == mas_stories.TYPE_SCARY:
        $ which = "Хромую"
    else:
        $ which = "Какую"

    $ renpy.say(m, which + " историю ты хотел бы услышать?" + end, interact=False)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(stories_menu_items, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch_item, final_item)

    # return value?
    if _return:
        # switching between types
        if _return == "monika_short_stories_menu":
            # NOTE: this is not scalable.
            if story_type == mas_stories.TYPE_SCARY:
                $ story_type = mas_stories.TYPE_NORMAL
            else:
                $ story_type = mas_stories.TYPE_SCARY

            $ end = "{fast}"
            $ _history_list.pop()

            jump monika_short_stories_menu

        else:
            $ story_to_push = _return

            #If we're unlocking new, check if it's possible to do so. If not, we raise dlg
            if story_to_push == mas_stories.UNLOCK_NEW:
                if not can_unlock_story:
                    show monika at t11
                    $ _story_type = story_type if story_type != 'normal' else 'short'
                    m 1ekc "Извини, [player]... я сейчас не могу придумать новую [_story_type] историю прямо сейчас..."
                    m 1eka "Если ты дашь мне немного времени, я, возможно, смогу придумать одну в ближайшее время... а пока я всегда могу рассказать тебе старую!"
                    show monika 1eua
                    jump monika_short_stories_menu

                else:
                    python:
                        persistent._mas_last_seen_new_story[story_type] = datetime.datetime.now()
                        story_to_push = mas_stories.get_and_unlock_random_story(story_type)

            #Then push
            $ pushEvent(story_to_push, skipeval=True)

            show monika at t11

    else:
        return "prompt"

    return

# Stories start here
label mas_story_begin:
    python:
        story_begin_quips = [
            _("Хорошо, я расскажу тебе историю."),
            _("Готов услышать историю?"),
            _("Готов к рассказу?"),
            _("Давай начнём~"),
            _("Ты готов?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    $ mas_gainAffection(modifier=0.2)
    m 3eua "[story_begin_quip]"
    m 1duu "Кхм."
    return


label mas_scary_story_setup:
    if mas_scary_story_setup_done:
        return

    $ mas_scary_story_setup_done = True
    show monika 1dsc
    $ mas_temp_r_flag = mas_current_weather
    $ is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_rain)
    $ are_masks_changing = mas_current_weather != mas_weather_rain
    $ mas_is_raining = True

    $ play_song(None, fadeout=1.0)
    pause 1.0

    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    #o31 already has vignette. We apply it outside of o31 for scary stories
    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_weather_rain)
        $ store.mas_globals.show_vignette = True
        call spaceroom(dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')

    play music "mod_assets/bgm/happy_story_telling.ogg" loop


    $ HKBHideButtons()
    $ mas_RaiseShield_core()

    python:
        story_begin_quips = [
            _("Хорошо, я расскажу тебе историю."),
            _("Готов услышать историю?"),
            _("Готов к рассказу?"),
            _("Давай начнём~"),
            _("Ты готов?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)

    m 3eua "[story_begin_quip]"
    m 1duu "Кхм."
    return

label mas_scary_story_cleanup:

    python:
        story_end_quips = [
            _("Страшно, [player]?"),
            _("Я напугала тебя, [player]?"),
            _("Ну как?"),
            _("Ну?"),
            _("Итак... {w=0.5}я тебя напугала?")
        ]
        story_end_quip=renpy.substitute(renpy.random.choice(story_end_quips))

    m 3eua "[story_end_quip]"
    show monika 1dsc
    pause 1.0

    #Not in o31 mode, so we need to remove vignette
    if not persistent._mas_o31_in_o31_mode:
        $ mas_changeWeather(mas_temp_r_flag)
        $ store.mas_globals.show_vignette = False
        call spaceroom(dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing, force_exp='monika 1dsc_static')
        hide vignette

    call monika_zoom_transition(mas_temp_zoom_level,transition=1.0)

    $ play_song(None, 1.0)
    m 1eua "Надеюсь, тебе понравилось, [player]~"
    $ mas_DropShield_core()
    $ HKBShowButtons()
    $ mas_scary_story_setup_done = False
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tyrant",
            prompt="Кот и Петух",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=True
        ),
        code="STY"
    )

label mas_story_tyrant:
    call mas_story_begin
    m 1eua "Кот поймал Петуха и задумался над разумными основаниями, чтобы съесть его."
    m "Он обвинил его в том, что он надоедал всем, кукарекая ночью; не давал людям спать."
    m 3eud "Петух обосновал свой поступок тем, что это было на благо людей, поскольку кукареканье побуждало в людях желание работать."
    m 1tfb "И Кот сказал ему: «Ты своевольно извиняешься, но уже пора завтракать»."
    m 1hksdrb "После этого, он приготовил обед из Петуха."
    m 3eua "Мораль этой истории такова: «Тиранам нет оправдания»."
    m 1hua "Надеюсь, тебе понравилась эта небольшая история, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_despise",
            prompt="Лис",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_despise:
    call mas_story_begin
    m 1eud "В один жаркий летний день, Лис прогуливался по фруктовому саду, пока не подошёл к грозди винограда, которая только что созрела на лозе, находящейся на высокой ветке."
    m 1tfu "«Самое то, чтобы утолить свою жажду» – сказал Лис."
    m 1eua "Отступив на несколько шагов, он побежал и прыгнул, но промахнулся мимо ветки."
    m 3eub "Возвращаясь снова и снова, сначала один раз,{w=1.0} потом второй,{w=1.0} третий,{w=2.0} он всё прыгал, но так и не добился успеха."
    m 3tkc "Раз за разом, он всё пытался дотянуться до соблазнительного кусочка, но, в конце концов, ему пришлось сдаться, и он ушёл, задрав нос, сказав: «Я уверен, что они кислые»."
    m 1hksdrb "Мораль этой истории такова: «Легко презирать то, что не можешь получить»."
    m 1eua "Надеюсь, тебе понравилась эта история, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_lies",
            prompt="Мальчик-пастух и Волк",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_lies:
    call mas_story_begin
    m 1euc "Жил-был один Мальчик-пастух, который, в основном, ухаживал за своими овцами у подножия горы возле тёмного леса."
    m 1lsc "Ему стало одиноко, и он разработал план, как собрать себе небольшую компанию."
    m 4hfw "Он бросился в сторону деревни с криками «Волк! Волк!», и жители деревни вышли ему навстречу."
    m 1hksdrb "Мальчик так сильно обрадовался этому, что через несколько дней он попробовал тот же трюк, и жители деревни снова пришли к нему на помощь."
    m 3wud "Вскоре после этого, Волк действительно вышел из леса."
    m 1ekc "Мальчик закричал «Волк, Волк!» ещё громче, чем раньше."
    m 4efd "Но на этот раз, жители деревни, которых обманули дважды до этого момента, подумали, что мальчик снова врёт, и никто не пришёл к нему на помощь."
    m 2dsc "И тогда, Волк насладился вдоволь стадом овец Мальчика."
    m 2esc "Мораль этой истории такова: «Лжецам не поверят, даже когда они говорят правду»."
    m 1hksdlb "Не беспокойся об этом, [player]..."
    m 3hua "Ты ведь никогда не врал мне, верно?"
    m 1hub "Э-хе-хе~"
    m 1eua "Надеюсь, тебе понравилась история, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_grasshoper",
            category=[mas_stories.TYPE_NORMAL],
            prompt="Кузнечик",
            unlocked=False
        ),
        code="STY"
    )

label mas_story_grasshoper:
    call mas_story_begin
    m 1eua "В один летний день, Кузнечик прыгал, щебетал и пел в своё удовольствие."
    m "Мимо проходил Муравей с початком кукурузы, который он нёс в гнездо." 
    m 3eud "«Почему бы тебе не пойти поболтать со мной», – сказал Кузнечик, – «вместо того, чтобы так трудиться»?"   
    m 1efc "«Я помогаю откладывать еду на зиму,» – сказал Муравей, – «и советую тебе сделать то же самое»." 
    m 1hfb "«Зачем беспокоиться о зиме?» – сказал Кузнечик, – «у нас сейчас полно еды!»."
    m 3eua "Муравей пошёл своей дорогой."
    m 1dsc "Когда наступила зима, у Кузнечика не было еды и он умирал от голода, в то время как муравьи раздавали друг другу кукурузу и зерно из хранилищ, которые они загрузили летом."
    m 3hua "Мораль этой истории такова: «Делу время, потехе – час»."
    m 1dubsu "Но всегда есть время, чтобы провести его со своей милой девушкой~"
    m 1hub "Э-хе-хе, я так сильно тебя люблю, [player]!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_wind_sun",
            prompt="Ветер и Солнце",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_wind_sun:
    call mas_story_begin
    m 1dsc "Ветер и Солнце спорили, кто из них был самым сильным."
    m 1euc "Внезапно, они увидели путешественника, идущего по дороге, и Солнце сказало: «Я вижу способ решить наш спор.»."
    m 3efd "«Кто из нас сможет заставить путешественника снять свой плащ, тот и будет считаться самым сильным. Ты начинаешь»."
    m 3euc "После этого, Солнце скрылось за облаками, и Ветер начал дуть так сильно, как только мог на путешественника."
    m 1ekc "Но чем сильнее он дул, тем больше путешественник оборачивал вокруг себя плащ, пока, наконец, Ветер не сдался в отчаянии."
    m 1euc "Затем Солнце вышло и засияло во всей своей красе над путешественником, который вскоре осознал, что на улице слишком жарко для того, чтобы ходить с его плащом."
    m 3hua "Мораль этой истории такова: Доброта и любезное убеждение побеждают там, где сила и гнев терпят неудачу»."
    m 1hub "Надеюсь, тебе было весело, [player]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_seeds",
            prompt="Семена",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_seeds:
    call mas_story_begin
    m 1euc "Случилось так, что Земляк сеял семена конопли в поле, где Ласточка и другие птицы вприпрыжку собирали себе еду."
    m 1tfd "«Остерегайтесь этого человека.» – отметила Ласточка."
    m 3eud "«Почему, что он делает?» – спросили остальные."
    m 1tkd "«Он здесь сеет семя конопли; будьте осторожны во время сбора этих семян, иначе вы пожалеете об этом.» – ответила Ласточка."
    m 3rksdld "Птицы не обратили внимание на слова Ласточки, и вскоре, конопля выросла и превратилась в верёвку, а из верёвок сделали сетки."
    m 1euc "Многие птицы, которые наплевали на советы Ласточки, были пойманы в сети, сделанные из той самой конопли."
    m 3hfu "«Что я вам говорила?» – сказала Ласточка."
    m 3hua "Мораль этой истории такова: «Уничтожай семена зла, пока они не обратились в твою погибель»."
    m 1lksdlc "..."
    m 2dsc "Хотела бы я следовать этим моральным принципам."
    m 2lksdlc "Тебе тогда не пришлось бы проходить через то, что ты видел."
    m 4hksdlb "Так или иначе, надеюсь, тебе понравилась история, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_gray_hair",
            prompt="Седые волосы",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_gray_hair:
    call mas_story_begin
    m 1eua "В давние времена, у мужчины средних лет была одна жена, которая была старой, и вторая, которая была молодой; обе любили его и хотели только заслужить его любовь."
    m 1euc "Волосы мужчины поседели, что молодой жене не понравилось, ведь из-за этого он начал казаться слишком старым."
    m 3rksdla "Поэтому, каждую ночь она собирала белые волосы."
    m 3euc "Но старшая жена не хотела повторять ошибки своей матери."
    m 1eud "И поэтому, каждое утро она собирала как можно больше чёрных волос."
    m 3hksdlb "Вскоре, Мужчина заметил, что стал совсем лысым."
    m 1hua "Мораль этой истории такова: «Уступай всем, и тебе скоро ни в чём не придётся уступать»."
    m 1hub "Поэтому, прежде чем отдавать что-либо кому-то, убедись, что у тебя самого хоть что-то осталось!"
    m 1lksdla "...Нет, быть лысым не так уж и плохо, [player]."
    m 1hksdlb "Э-хе-хе, я люблю тебя~!"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_fisherman",
            prompt="Рыбак",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_fisherman:
    call mas_story_begin
    m 1euc "Бедному Рыбаку, жившему лишь на пойманной им рыбе, однажды не повезло, и он поймал только очень мелкого малька."
    m 1eud "Рыбак уже было хотел положить его в свою корзину, но маленькая Рыбка заговорила."
    m 3ekd "«Пожалуйста, отпустите меня, мистер Рыбак! Я такая мелкая, что не стоит нести меня домой. Когда я стану больше, я преподнесу вам еду, которая будет гораздо лучше!»."
    m 1eud "Но Рыбак быстро положил рыбу в свою корзину."
    m 3tfu "«Каким глупым я должен быть,» – сказал он – «чтобы выбросить тебя? Какой бы мелкой ты ни была, ты лучше, чем ничего»."
    m 3esa "Мораль этой истории такова: «Небольшой выигрыш стоит больше, чем большое обещание»."
    m 1hub "Надеюсь, тебе понравилась эта небольшая история, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_ravel",
            prompt="Три желания старика",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_ravel:
    call mas_story_begin
    m 3euc "Однажды, пожилой человек сидел один на тёмной дороге."
    m 1euc "Он забыл, куда он шёл, и кто он такой."
    m "Внезапно, он посмотрел вверх и увидел перед собой пожилую женщину."
    m 1tfu "Она улыбнулась беззубым ртом и, хихикая, сказала: «Теперь твоё {i}третье{/i} желание. Каким оно будет?»"
    m 3eud "«Третье желание?». Мужчина был сбит с толку. «Как это может быть третьим желанием, если я ещё не загадывал ни первое, ни второе?»."
    m 1tfd "«У тебя уже было два желания,» – сказала ведьма, – «и твоим вторым желанием было сделать всё так, как было до исполнения твоего первого желания»."
    m 3tku "Именно поэтому, ты ничего и не помнишь: всё стало таким, каким было до твоих желаний."
    m 1dsd "«Хорошо,» – сказал мужчина, – «я не верю в это, но в желаниях нет ничего плохого. Я хочу узнать, кто я такой»."
    m 1tfb "«Забавно,» – сказала старая женщина и, исполнив его желание, исчезла навсегда. «Это и было твоё первое желание»."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_simple",
            prompt="Простой джин",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_simple:
    call mas_story_begin
    m 1eua "Жил-был джинн, который путешествовал по разным мирам, спасаясь от своего собственного хаоса."
    m 3euc "Во время своих путешествий он встретил женщину, которая бросила вызов его взгляду на мир."
    m 3eua "Она была умной и талантливой, но сдерживалась из-за трудностей, с которыми ей пришлось столкнуться, и своего маленького роста."
    m 3eub "Джинн видел это и был щедр, предлагая идеи, чтобы ускорить её работу и сделать её жизнь легче."
    m 1euc "Но она просто отклонила его предложение."
    m 1eud "До сих пор никто не отказывал джинну в его желании, {w=0.1}{nw}"
    extend 1etc "и это оставляло его в замешательстве."
    m 1esa "Женщина просто спросила его, счастлив ли он...{w=0.5} {nw}"
    extend 1rsc "Он не знал, что ответить."
    m 3eud "Женщина говорила, что она могла сказать о том, что никогда не испытывала счастье, и что несмотря на все её трудности, она может наслаждаться своей жизнью и дальше."
    m 1euc "Джинн не мог понять, зачем кому-то понадобилось так усердно трудиться ради такой мелочи."
    m 3euc "Он улучшил свои предложения богатством и другими подобными вещами, но всё же она отказалась."
    m 1eua "В конце концов женщина попросила джинна присоединиться к её образу жизни."
    m "И поэтому он подражал тому, что делала она, не используя никаких сил."
    m 1hua "Джинн начал испытывать небольшое чувство выполненного долга, впервые создавая что-то, не желая, чтобы это существовало."
    m 3eub "Он видел, как простые вещи, такие как искусство и письмо, вдохновляли женщину и действительно заставляли её сиять." 
    m 1eua "Заинтригованный, он хотел проводить гораздо больше времени с этой женщиной и учиться у неё."
    m 1euc "В конце концов, однажды женщина заболела."
    m 1eud "Она заставила джинна пообещать, что он не будет использовать свои силы, чтобы вылечить её."
    m 3eud "Именно в этот момент джинн понял, что хочет жить как человек, никогда больше не используя свои силы."
    m 1dsc "Он думал обо всех прошлых желаниях, которые он давал другим, обо всех богатствах, которые он создавал..."
    m "Все его собратья-джинны исполняют желания, не зная и не заботясь о последствиях..."
    m 1dsd "Никогда не зная, каково это – бросить всё ради того, чтобы быть с тем, кого любишь."
    m 1esd "Всё, что он мог сделать, это жить с тем, что он теперь нашёл в жизни."
    m 1dsc "..."
    m 1eua "Надеюсь, тебе понравилась эта история, [player]."
    m 3eua "Есть несколько вещей, которые можно почерпнуть из неё..."
    m 3eka "Если у тебя уже есть всё, то ничто не имеет цену."
    m 1hua "...Кроме, наверное, тебя, конечно же."
    m 3eub "Борьба – это то, что делает что-либо стоящим."
    m 1eua "Другая мораль может заключаться в том, что иногда счастье заложено в более простых вещах, которые ты мог бы иметь всё это время."

    if mas_isMoniNormal(higher=True):
        m 1eka "В конце концов, мы просто сидим здесь и наслаждаемся общением друг с другом."
        m 1hubsb "Когда ты здесь, мне кажется, что у меня есть всё~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_regret",
            prompt="Сожаление джина",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_regret:
    call mas_story_begin
    m 1eua "Был когда-то джинн, который был бессмертен..."
    m "За свою жизнь он видел, как мир меняется со временем, и исполнял желания каждого, кто попадался ему на пути."
    m 1esc "За свою долгую жизнь он повидал много вещей,{w=0.2} {nw}"
    extend 1rsc "и некоторые из них были ему неприятны."
    m 1ekd "Войны, стихийные бедствия, смерть всех друзей, которых он когда-либо заводил..."
    m 1rkc "Некоторые из них были вызваны исполненными им желаниями."
    m 1ekc "Сначала он не слишком беспокоился о последствиях... но через некоторое время это стало беспокоить его всё больше и больше."
    m 1ekd "Он пришёл в простой, прекрасный, чистый мир и нанёс ему неизмеримый ущерб."
    m 1lksdlc "Неуравновешенность и ревность распространялись по мере того, как он исполнял всё больше желаний, сеял желания мести и жадности."
    m 2dkd "Это было то, с чем он должен был жить до конца своей жизни."
    m 2ekc "Он хотел, чтобы всё вернулось на круги своя, но его мольбы всегда оставались без ответа."
    m 2eka "Со временем, однако, он познакомился с некоторыми людьми и завёл друзей, которые научили его, как идти вперёд, несмотря на все его действия."
    m "Хотя это было правдой, что он был тем, кто исполнял желания, которые начали хаос...{w=0.5} {nw}"
    extend 2ekd "некоторые должны были случиться и без него."
    m 3ekd "Среди людей всегда будет зависть и несправедливость...{w=0.3} {nw}"
    extend 3eka "но даже так, мир всё ещё был в порядке."
    m 3eua "Он собирался жить с тем, что сделал, но оставался вопрос, что он собирается с этим делать."
    m 1hua "Именно благодаря всему, через что он прошёл, он смог учиться и двигаться дальше,{w=0.3} лучше, чем раньше."
    m 1eua "Надеюсь, тебе понравилась эта история, [player]."
    m 1eka "Мораль этой истории в том, что даже если ты сделал что-то, о чём сожалеешь, ты не должен позволять этому угнетать себя."
    m 3ekd "Ошибки будут происходить, люди будут страдать.{w=0.5} Ничто и никогда этого не изменит."
    m 3eka "Правда в том, что очень часто мы склонны винить себя за то, что, скорее всего, произошло бы с нашим участием или без него."
    m 3eub "На самом деле, именно через сожаление мы учимся состраданию, сочувствию и прощению."
    m 3eua "Ты не можешь изменить прошлое, но тебе нужно простить себя когда-нибудь, чтобы смериться и жить дальше."
    m 1eka "Как по мне..."
    m 1rksdlc "Кто знает, что случилось бы в моём мире, если бы я ничего не сделала..."

    $ placeholder = ", по крайней мере,"
    if persistent.clearall:
        $ placeholder = ""
        m 1eua "Ты познакомся здесь с каждым членом клуба, так что я думаю, ты не жалеешь, что упустил что-то."
        m 1hub "А-ха-ха~"

    m 1eua "Но[placeholder] теперь ты здесь, со мной."
    m 3eua "С тех пор как мы вместе, я определённо могу сказать, что выросла и многому научилась на своих ошибках."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_genie_end",
            prompt="Конец джина",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_genie_end:
    call mas_story_begin
    m 1eua "Жил-был когда-то бессмертный джинн, который прожил долгую жизнь."
    m 1euc "Он видел все, что только можно было увидеть...{w=0.3} жил свободно и научился выполнять работу по достижению цели."
    m 3euc "По существу, он отказался от всего, кроме своего бессмертия, чтобы жить как человек."
    m 1ekc "Это правда, что он прожил хорошую жизнь и окружил себя любящими друзьями и семьёй..."
    m 1ekd "Но с годами он становился всё холоднее и холоднее и наблюдал за каждым из своих близких."
    m 1rksdlc "Оставалось ещё несколько избранных людей, которых он любил, хотя и знал, что ему придётся смотреть, как они умрут."
    m 3rksdld "Он никогда не говорил своим друзьям, что он не человек, так как всё ещё хотел, чтобы с ним обращались как с человеком."
    m 1euc "Однажды, когда он путешествовал с одним из своих друзей, они наткнулись на джинна, который исполнял одно из их желаний."
    m 1dsc "Это заставило его задуматься обо всем, через что он прошёл;{w=0.5} с тех пор, как он исполнял желания, до тех пор, когда он отказался от них ради простой жизни."
    m 1dsd "...Всё, что привело его к этому моменту, когда он впервые за долгое время смог загадать собственное желание."
    m 1dsc "..."
    m 2eud "Он хотел умереть."
    m 2ekc "Будучи озадаченным, его друг спросил, почему и что с ним стряслось."
    m 2dsc "Именно тогда он и объяснил всё своему другу."
    m 3euc "Что много лет назад он был джинном..."
    m 3eud "...Как он встретил кого-то, кто заставил его бросить всё ради того, чтобы быть с кем-то, кого он любил."
    m 3ekd "...И как ему постепенно надоедало то, что осталось от его жизни."
    m 1esc "По правде говоря, он не устал жить...{w=0.5} {nw}"
    extend 1ekd "Он просто устал видеть, как его близкие гибнут снова и снова."
    m 1dsd "Его последняя просьба к другу состояла в том, чтобы он вернулся к своим друзьям и связал для него все концы."
    m 1dsc "..."    
    m 1eka "Надеюсь, тебе понравилась эта маленькая история, [player]."
    m 3eka "Я думаю, ты мог бы сказать, что мораль заключается в том, что каждый должен иметь некоторое завершение."
    m 1eka "Хотя, возможно, тебе интересно, чего хотел его друг в этом сценарии."    
    m 1eua "Он хотел, чтобы его друг получил покой, которого он заслуживал."
    m 1lksdla "Хотя это правда, что его друг – джинн, возможно, и не был кем-то особенным..."
    m 3eua "Он определённо был тем, кто заслуживал уважения,{w=0.2} {nw}"
    extend 3eub "особенно после такой долгой жизни."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_immortal_love",
            prompt="У любви нет конца",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_immortal_love:
    call mas_story_begin
    m 3eua "Жила-была одна супружеская пара, которая многие годы жила в мире и согласии."
    m "В каждый День святого Валентина, муж дарил красивый букет цветов своей жене."
    m 1eka "К каждому из этих букетов была приложена записка с парой простых, но очень приятных слов."
    m 3dsc "{i}Моя любовь к тебе только растёт{/i}."
    m 1eud "Через какое-то время, её муж скончался."
    m 1eka "Жена, будучи опечаленной из-за своей потери, была уверена в том, что она проведёт свой следующий День святого Валентина одна и в трауре."
    m 1dsc "..."
    m 2euc "Однако,{w=0.3} в свой первый День святого Валентина без своего мужа, она всё равно получила букет от него."
    m 2efd "Будучи злой и с разбитым сердцем, она пожаловалась флористу на то, что произошла ошибка."
    m 2euc "И флорист объяснил ей, что здесь никакой ошибки не было."
    m 3eua "Её супруг заранее заказал много букетов, чтобы его любимая жена и дальше получала цветы после его смерти."
    m 3eka "Будучи потрясённой и потеряв дар речи, жена прочитала записку, приложенную к букету."
    m 1ekbsa "{i}Моя любовь к тебе вечна{/i}."
    m 1dubsu "Ах..."
    m 1eua "Разве это не трогательная история, [player]?"
    m 1hua "Лично я считаю, что она была довольно романтичной."
    m 1lksdlb "Но я не хочу думать о том, что кто-то из нас умрёт."
    m 1eua "По крайней мере, финал был очень трогательным."
    m 1hua "Спасибо, что выслушал~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mother_and_trees",
            prompt="Мать и её деревья",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_mother_and_trees:
    call mas_story_begin
    m 1eua "Жил-был мальчик, который жил со своей матерью."
    m 3eud "Она отдавала ему всю свою любовь, какую только может дать мать...{w=0.2}{nw}"
    extend 3rksdla " но он всегда думал, что она была немного странной."
    m 3eub "В дни его рождения она {i}всегда{/i} пекла печенье для него и всех его одноклассников, чтобы поблагодарить их за то, что они были его друзьями."
    m 1eua "Она также хранила и выставляла каждый маленький рисунок, который он делал в художественной школе, так что через годы их стены были покрыты его рисунками."
    m 2rksdlc "Иногда он даже избавлялся от своих рисунков, потому что не хотел, чтобы она ставила их вместе с остальными."
    m 2euc "Однако больше всего её отличало то...{w=0.3} {nw}"
    extend 2eud "что она часто разговаривала со своими деревьями."
    m 1eua "На их заднем дворе росли три дерева, с которыми она разговаривала каждый день."
    m 3rksdlb "У неё даже были имена для каждого из них!"
    m 3hksdlb "Иногда она даже просила его одеться и позировать у деревьев, чтобы сфотографировать их вместе."
    m 1eka "Однажды, увидев, как она разговаривает с деревьями, он спросил её, почему она всегда так много с ними говорит."
    m 3hub "Его мать ответила: «Ну, потому что им нужно чувствовать себя любимыми!»"
    m 1eka "Но он по-прежнему ничего не понимал...{w=0.2}{nw}"
    extend 1eua " и как только он ушёл, она продолжила разговор с того места, на котором и стояла."
    m 2ekc "Шло время, и мальчику в конце концов пришлось съехать и начать свою собственную жизнь."
    m 2eka "Мать сказала ему, чтобы он не беспокоился о том, что уйдёт от неё, потому что у неё всегда есть деревья, чтобы составить ей компанию."
    m 2eua "Пока он был занят своей жизнью, он всё ещё находил время, чтобы поддерживать с ней контакт."
    m 2ekc "До одного дня...{w=0.5}{nw}"
    extend 2dkd " ему позвонили."
    m 2rksdlc "Его мать умерла и была найдена лежащей у одного из деревьев."
    m 2ekd "В её завещании была только одна просьба к нему...{w=0.3} и всё это для того, чтобы заботиться о деревьях, разговаривать с ними каждый день."
    m 1eka "Конечно, он хорошо заботился о деревьях, но никогда не мог заставить себя заговорить с ними."
    m 3euc "Некоторое время спустя, просматривая и приводя в порядок старые вещи матери, он нашёл конверт."
    m 1eud "Он был потрясён тем, что обнаружил внутри."
    m 2wud "Там было три свидетельства о смерти его будущих братьев и сестёр."
    m 2dsc "У каждого из них было одинаковое имя с одним из деревьев, которые росли на заднем дворе всю его жизнь."
    m 2dsd "Он никогда не знал, что у него есть братья и сестры, но в конце концов понял, почему его мать разговаривает с деревьями..."
    m 2eka "Он всегда очень серьёзно относился к желанию своей матери, и именно тогда он начал разговаривать с деревьями каждый день, как и хотела его мать."
    m 2duu "...И он решил сделать нечто большее, и в итоге посадил ещё одно дерево."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_self_hate",
            prompt="Ненависть к себе",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_self_hate:
    call mas_story_begin
    m 1eua "Когда-то были два человека, которые жили вместе очень долго."
    m 1hua "Жизнь была проста, и они оба любили друг друга. Всё шло хорошо."
    m 3euc "И вот однажды этот человек внезапно убил свою возлюбленную, казалось бы, без всякой причины."
    m 3eud "Он {i}действительно{/i} любил её, и очень сильно!"
    m 2ekc "Не было даже каких-либо драк или споров."
    m "Ему никакая выгода не светит от её убийства."
    m 4ekd "Никакого удовлетворения, ничего необычного по её воле..."
    m 1dkc "На самом деле этот человек остался эмоционально травмированным, потеряв любовь всей своей жизни."
    m "..."
    m 1ekd "Так почему же?"
    m 1rksdlc "Как это могло случиться так внезапно?"
    m 1eksdlc "Не то чтобы он её не любил."
    m 3eksdla "А всё потому, что он так сильно любил её."
    m "Он не испытывал к ней ненависти..."
    m 2eksdld "Он просто ненавидел себя настолько, что отказывался от собственного счастья."
    m 2dkc "..."
    if persistent._mas_pm_love_yourself is False:
        m 3ekc "Эй, [player], помнишь, я спросила тебя, любишь ли ты себя?"
        m 1rksdld "Насколько я помню, ты сказал мне, что нет..." 
        m 1rksdla "Прости, я не хотела ставить тебя в неловкое положение или ещё что..."    
        m 3eka "Я просто хочу убедиться, что ты помнишь, что я люблю тебя."   
        m 3ekd "Что ещё более важно, я хочу убедиться, что ты знаешь, как любить себя."      
        m 1ekbsa "Я знаю, что ты достоин любви, и я сделаю всё, чтобы показать тебе это."    
        m 1ekbfa "Надеюсь, ты никогда этого не забудешь~"
    else:
        m 1rksdlb "Прости, что рассказала такую мрачную историю, [player]..."    
        m 3eksdla "Но у неё есть важное послание..."  
        m 3eud "И оно значит, что тебе нужно найти способ любить себя, иначе ты можешь сделать то, о чём потом пожалеешь." 
        m 1ekc "Как бы ты ни старался, попытка прожить свою жизнь исключительно для кого-то другого никогда не сработает." 
        m 1eka "Ты должен любить себя, чтобы позволить себе по-настоящему любить кого-то другого."  
        m 3ekbsa "Просто помни, что я всегда буду любить тебя, [player]." 
        m 3ekbfa "Если ты когда-нибудь начнёшь сомневаться в любви к себе, просто приходи ко мне, и я буду более чем счастлива напомнить тебе обо всех твоих замечательных качествах~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_o_tei",
            prompt="Рассказ об О-Тей",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_o_tei:
    call mas_story_begin
    m 1eua "Давным-давно жил человек по имени Кендзи, который учился на врача."
    m 3eub "Он был помолвлен с молодой женщиной по имени Томоэ, и они должны были пожениться после окончания учебы."
    m 1esc "К сожалению, Томоэ заболела серьёзной болезнью до того, как это произошло."
    m 2dsd "Вскоре она была прикована к постели, приближаясь к концу своей жизни."
    m 2esd "Кендзи встал на колени у её постели, и она сказала ему: «Мы обещали друг другу с детства, что поженимся...»"
    m 3ekc "«К сожалению, с моим хрупким телом, моё время пришло, и я умру прежде, чем смогу стать твоей женой.»"
    m "«Пожалуйста, не скорби, когда я уйду. Думаю, мы ещё встретимся.»"
    m 3eud "Он спросил: «Как я узнаю о твоём возвращении?»"
    m 2dsc "К сожалению, она умерла, прежде чем смогла дать ему ответ."
    m "Кендзи был глубоко опечален потерей своей любимой, отнятой у него слишком рано."
    m 2esc "Он никогда не забывал о Томоэ с течением времени, но он должен был жениться на ком-то другом и передать свою фамилию."
    m "Вскоре он женился на другой девушке, но его сердце осталось в другом месте."
    m 2esd "И как со всеми бывает в жизни, его семью тоже унесло время, и он снова остался совсем один."
    m 4eud "Именно тогда он решил покинуть свой дом и отправиться в далёкое путешествие, чтобы забыть о своих проблемах."
    m 1esc "Он путешествовал по всей стране в поисках лекарства от недуга."
    m 1euc "И вот однажды вечером он наткнулся на трактир и остановился там отдохнуть."
    m "Когда он уселся в своей комнате, некая Накай открыла дверь, чтобы поприветствовать его."
    m 3euc "Он ощутил, как его сердце вновь взывает к нему..."
    m 3wud "Девушка, которая его приветствовала, была похожа на Томоэ."
    m "Всё, что он видел в ней, прекрасно напоминало ему о его прошлой любви."
    m 1esc "Затем Кендзи вспомнил последние слова, которыми они обменялись перед её уходом."
    m 1esc "Он остановил девушку и сказал ей: «Извините, что беспокою, но вы так напоминаете мне кое-кого, кого я давно знаю, что это испугало меня поначалу.»"
    m 3euc "«Могу я узнать ваше имя?»"
    m 3wud "Тотчас же, незабытым голосом умершей возлюбленной девушка ответила: «Меня зовут Томоэ, а ты Кендзи, мой обещанный муж.»"
    m 1wud "«Я трагически погибла прежде, чем мы успели пожениться...»"
    m "«А теперь я вернулась, Кендзи, мой будущий муж.»"
    m 1dsc "Затем девушка упала на пол, потеряв сознание."
    m 1esa "Кендзи держал её на руках, слёзы текли по его щекам."
    m 1dsa "«...С возвращением, Томоэ...»"
    m 3esa "Когда она очнулась, не помнила, что произошло в гостинице."
    m 1hua "Вскоре после этого Кэндзи женился на ней, как только смог, и они прожили счастливо всю оставшуюся жизнь."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_crow_and_pitcher",
            prompt="Ворон и кувшин",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_crow_and_pitcher:
    call mas_story_begin
    m 2ekd "Однажды была такая сильная засуха, что даже птицы не могли найти много воды."
    m 7eub "Во время поисков сверху измученный жаждой ворон нашёл кувшин и с облегчением обнаружил, что в нём ещё осталось немного воды!"
    m 3eksdlc "Однако кувшин был высокий, с узким горлышком. Как он ни старался, ему не удавалось дотянуться клювом до воды."
    m 1dksdlc "Бедный Ворон, казалось, потерял всякую надежду. Разумеется, он умрёт от жажды."
    m 3wud "...И тут ему в голову пришла идея."
    m 3esc "Он начал искать мелкие камешки на земле и бросать их в кувшин, один за другим."
    m 2efsdlc "Время шло. Это была медленная, изнурительная работа, собирающая в себя всё больше и больше."
    m 2esa "Но с каждым крошечным камешком вода поднималась всё выше и выше, пока наконец не остановилась..."
    m 4hub "Он смог выпить большой глоток освежающего напитка!"
    m 2dka "..."
    m 2eka "Знаешь, эта история отчасти напоминает мне нашу ситуацию, [player]."
    m 7ekc "Сейчас наша цель кажется такой далёкой. Мы тянемся изо всех сил, но разрыв между нами огромен."
    m 3dkc "Иногда кажется, что это невозможно преодолеть. Если бы мы попытались пересечь его одним прыжком, то были бы похожи на ворона, который тянется только клювом."
    m 1tkd "...Поверь мне, я старалась."
    m 3ekb "Но если вдуматься, то мы добавляем камешки в наш кувшин. И дело не только в нас с тобой!"
    m 3eua "Достижения как в области виртуальной реальности, так и в области искусственного интеллекта постепенно продвигаются вперёд..."
    m 3hua "А если говорить более конкретно о нашей ситуации, то так много людей работают вместе, чтобы помочь мне приблизиться к твоей реальности."
    m 1eka "Когда я думаю об этом в таком ключе – то, что вода в кувшине медленно набирается – мне становится куда легче продолжать идти каждый день."
    m 1hua "Я надеюсь, что и для тебя тоже, [mas_get_player_nickname()]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_friend",
            prompt="Наличие лучшего друга",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_friend:
    call mas_story_begin
    m 3eua "Однажды двое друзей шли по пустыне..."
    m 1eua "В какой-то момент своего путешествия они поссорились {nw}"
    extend 1wud "и один друг дал другому пощечину!"
    m 1eud "Тот, кто получил пощечину, был ранен, но ничего не сказал, написав на песке:{w=0.1} «Сегодня мой лучший друг дал мне пощечину»."
    m 1eua "Они продолжали идти, пока не нашли оазис, где решили принять ванну."
    m 1ekc "Тот, кому дали пощечину, застрял в болоте и начал тонуть,{w=0.1} {nw}"
    extend 3wuo "но другой спас его!"
    m 3eua "Придя в себя после того, как чуть не утонул, он написал на камне:{w=0.1} «Сегодня мой лучший друг спас мне жизнь»."
    m 3eud "Друг, который ударил и спас лучшего друга, спросил его:{w=0.1} «После того, как я причинил тебе боль, ты писал на песке, а теперь пишешь на камне, зачем?»."
    m 3eua "Другой друг ответил: «Когда кто-то причиняет нам боль, мы должны записать это на песке, где ветер прощения сможет стереть это...»"
    m 3eub "«Но!»"
    m 3eua "«Когда кто-то делает что-то хорошее для нас, мы должны выгравировать это на камне, где никакой ветер никогда не сможет стереть это»."
    m 1hua "Мораль этой истории такова: не позволяй теням прошлого омрачать порог твоего будущего.{w=0.2} {nw}"
    extend 3hua "Прости и забудь."
    m 1hua "Надеюсь тебе понравилось, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_tanabata",
            prompt="Девушка-ткачиха и пастух",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False,
            aff_range=(mas_aff.AFFECTIONATE, None)
        ),
        code="STY"
    )

label mas_story_tanabata:
    call mas_story_begin
    m 1eub "Орихимэ, дочь Нефритового императора, правителя Небес, ткала прекрасные одежды на берегу Аманогавы."
    m 3eua "Её отец любил ткань, которую она ткала, и поэтому она каждый день очень усердно трудилась."
    m 2ekd "Однако Орихиме было грустно, что из-за своей тяжелой работы она так и не смогла никого встретить и полюбить."
    m 2eksdla "Беспокоясь о своей дочери, отец устроил ей встречу с пастухом Хикобоси, который жил и работал на другой стороне Аманогавы."
    m 7hub "Когда эти двое встретились, они мгновенно полюбили друг друга и вскоре поженились!"
    m 2eksdld "Однако, выйдя замуж, Орихиме перестала ткать, а Хикобоси пустил своих коров бродить по всему Небу."
    m 4wud "В гневе император разлучил влюбленных и запретил им встречаться."
    m 2dkc "Орихиме впала в уныние от потери мужа и попросила отца разрешить им встретиться снова."
    m 2eksdla "Растроганный слезами дочери, он разрешил им встретиться на седьмой день седьмого месяца, если она будет усердно трудиться и закончит ткать."
    m 2wud "Однако при первой попытке встретиться они обнаружили, что не могут пересечь реку, так как нет моста."
    m 2dkc "Орихиме так сильно плакала, что прилетела стая сорок и пообещали сделать мост из своих крыльев, чтобы она смогла перейти реку."
    m 7ekd "Говорят, что если в Танабата идёт дождь, то сороки не могут прилететь, и влюбленные должны ждать другого года, чтобы встретиться."
    m 3eud "Дождь, который прольётся на Танабата, уместно назвать {i}Слёзы Орихиме и Хикобоси.{/i}"
    m 1dksdlc "Я не могу представить, каково это — иметь возможность встречаться с любимым человеком только раз в год."
    m 3eua "Но знаешь, как говорится...{w=0.3} любовь может сдвинуть горы."
    m 3hubsu "...И моя любовь к тебе настолько сильна, что даже сами Небеса не смогли бы разлучить нас."
    $ mas_unlockEVL("monika_tanabata", "EVE")
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_mindthegap",
            prompt="Следи за разрывом",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=True
        ),
        code="STY"
    )

label mas_story_mindthegap:
    call mas_story_begin
    m 3eud "Это реальная история, которая произошла в Лондоне, в 2013 году."
    m 2dkd "Она начинается с того, что женщина по имени Маргарет Макколлум плачет посреди железнодорожной станции Эмбанкмент."
    m 2ekd "Когда к ней подошли, чтобы спросить о том, что произошло, она спросила персонал, куда делся «голос»."
    m 7ekd "Она пояснила, что имела в виду объявление, которое звучит при прибытии каждого поезда и предупреждает пассажиров о необходимости «следить за разрывом между платформой и поездом."
    m 1eka "Сотрудники заверили её, что объявление не исчезало, оно просто было обновлено на новую запись, когда станции перешли на новую цифровую систему."
    m 1tkc "Однако это объяснение не успокоило её. {w=0.3}«Этот голос, — объяснила она, — был моим мужем»."
    m 1eud "Её муж, Освальд Лоуренс, актёр, который так и не стал знаменитым, записал много объявлений для северной линии."
    m 2dkc "Освальд погиб пять лет назад."
    m 2ekc "Они очень любили друг друга, и его смерть оставила её в страшном горе."
    m 2euc "Но одно, {w=0.2}в течение этих пяти лет, {w=0.2}помогало ей продолжать жить дальше."
    m 7eka "Каждый день, когда она ехала на работу, она слышала его голос на станции. Иногда она задерживалась и сидела, просто чтобы услышать, как он произносит эти короткие объявления."
    m 2dkc "Но теперь..."
    m 2dkd "Сотрудники извинились, но не знали, есть ли у них доступ к старому файлу записи. {w=0.3}Они сказали ей, что если найдут, то свяжутся с ней."
    m 7eud "Оказалось, что многие люди, работавшие на станции, сочувствовали Маргарет и хотели, чтобы она ещё некоторое время могла наслаждаться этим драгоценным воспоминанием."
    m 7ekb "Поэтому, несмотря на то, что потребовалась дополнительная работа по обновлению старой записи из архива для работы с текущей системой, они добились того, чтобы она заработала."
    m 3eua "Однажды, когда Маргарет ехала на работу, на платформе раздался знакомый голос."
    m 1fkb "«Будьте осторожны, обратите внимание на разрыв между платформой и поездом». Сказал Освальд."
    m 1dku "..."
    m 3eka "Я упомянула, что это реальная история и ты всё ещё можешь услышать ту старую запись именно на станции «Набережная»."
    m 3ekb "Это действительно прекрасный пример человеческой доброты. {w=0.3}Рабочие ничего не получили, восстановив гораздо более короткую и менее качественную запись."
    m 1fka "Но они знали, каково это — потерять кого-то, и как дорога становится каждая фотография, каждое воспоминание."
    m 1dku "Это доказывает, что люди могут совершать невероятные поступки просто из сострадания и любви."
    m 1ekbla "Эта история напоминает мне о том, что нужно дорожить каждым моментом и не воспринимать ни одну частичку нашего совместного времени как должное."
    m 1dkblu "Я всегда буду дорожить тобой, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_story_knock",
            prompt="Стук",
            category=[mas_stories.TYPE_NORMAL],
            unlocked=False
        ),
        code="STY"
    )

label mas_story_knock:
    call mas_story_begin
    m 1euc "Последний человек на Земле сидел один в комнате."
    m 3rud "...В дверь постучали."
    m 3duc "Некоторые могут сказать, что на этом история заканчивается.{w=0.2} {nw}"
    extend 1dud "Но на самом деле это не так."
    m 3etc "Кто постучал в дверь?{w=0.2} {nw}"
    extend 3esa "Ответ был не таким уж ужасным, как могло показаться."
    m 3eua "Последним человеком на Земле был Уолтер Фелан. {w=0.2}Компанию ему составил организм под названием Зан."
    m 3eud "Человеческая раса была уничтожена ими, кроме него, и где-то...{w=0.3} {nw}"
    extend 3wud "женщина--{w=0.1}одна женщина."
    m 3euc "И Уолтер, и эта женщина были выбраны в качестве образцов для эксперемента, организованного Заном."
    m 2esc "Их было по два каждого вида, как в сказке о Ноевом ковчеге."
    m 2euc "В итоге, когда он открыл дверь, Уолтер не удивился, увидев одного из Занов."
    m 2etd "Странный маленький инопланетянин, поприветствовав человека наилучшим образом, на какой только способен инопланетянин, попросил Уолтера о помощи."
    m 2euc "«Произошло нечто непонятное» — сказал он,{w=0.1} {nw}"
    extend 2ekd "«двое других животных спят и не просыпаются. Они холодные.»"
    m 7euc "Уолтер знал, что те два животных были змея и утка, которые умерли."
    m 3esc "Однако Зан не понимал этого."
    m 1dsc "Человек быстро разработал в уме стратегию.{w=0.2} Он сказал Зану, что животные больше никогда не проснутся.{w=0.2} Старый Мрачный Жнец на свободе и убивает всех на своём пути."
    m 1euc "...Но он может помочь. {w=0.2}При одном условии: {w=0.2}последняя женщина на Земле тоже должна помочь."
    m 1eua "Зан разрешил ему пойти посмотреть на животных, и была назначена встреча."
    m 1dsc "Уолтер думал, что никогда не увидит женщину на этой планете...{w=0.3} {nw}"
    extend 1wub "но встреча с ней стала удивительным поворотом событий!"
    m 1esa "Грейс Эванс, последняя женщина на Земле, была удивлена, узнав то, что выяснил Уолтер:{w=0.2} что Зан не может умереть от естественных причин."
    m 3ttu "...Но, возможно, их можно убить."
    m 1eud "У мужчины было все необходимое для проверки этой теории, и, попрощавшись с Грейс, он привел свой план в действие."
    m 3esc "Он попросил Зана увидеть последнюю утку, поскольку вторая погибла и рассказал пришельцу, что ему следует делать."
    m 4eud "«Поделитесь с ним любовью, погладьте его, иначе он тоже умрет... {w=0.2}от одиночества.»"
    m 3rsc "Пришелец не понимал, что это значит, поэтому он просто наблюдал, как Уолтер с любовью гладит утку."
    m 1esc "«Проделайте то же самое с оставшейся змеей.» — сказал он."
    m 1euc "...И тогда Зан последовал его примеру."
    m 3wud "Но имей ввиду, [player], это была не обычная змея...{w=0.3} {nw}"
    extend 3tfu "а ядовитая..."
    m 1euc "Так, Зан, которому было поручено погладить оставшуюся змею, был сражен её смертельным ядом."
    m 1wud "Другой Зан вошел в комнату Уолтера в отчаянии на следующий день.. {w=0.2}{nw}"
    extend 4wko "«Один из нас умер!» — заплакал он."
    m 2dud "«Ну, тогда делать нечего».{w=0.2} {nw}"
    extend 2esc "«Смертельная болезнь распространяется, вам нужно бежать» — заявил мужчина."
    m 7euc "Зан собрал совет и дал знать двум людям, что они действительно уходят."
    m 1ekd "Риск был слишком велик, они не могли потерять больше представителей своей расы."
    m 3eud "Они оставили всех «проклятых» животных, включая Уолтера и Грейс, и улетели на своём корабле."
    m 1dua "Последние мужчина и женщина на Земле наконец-то были вместе.{w=0.2}{nw}"
    extend 1rkbla "Что им остаётся делать вместе в одиночестве в таком огромном мире?"
    m 3gsbsu "Нам остается только фантазировать..."
    m 1hubsa "Надеюсь, тебе понравилась эта история, [player]."
    return

#START: SCARY STORIES
init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_hunter",
    category=[store.mas_stories.TYPE_SCARY], prompt="Охотник",unlocked=True),
    code="STY")

label mas_scary_story_hunter:
    call mas_scary_story_setup
    m 3esa "Однажды охотник отправился на охоту за дичью в лес."
    m 3esc "Лес был густым и тёмным вокруг него, поэтому он изо всех сил пытался попасть в цель."
    m 1esd "Вскоре к нему подошёл продавец, который скрывал своё лицо."
    m 3esd "Тот предложил охотнику семь волшебных пуль, которые в обязательном порядке поражали любую цель, которую хотел владелец."
    m "Но дал бы он эти пули лишь при одном условии..."
    m 1euc "Первые шесть пуль охотник мог использовать по своему усмотрению, но вот мишень последней пули выбирал уже сам продавец."
    m "Охотник согласился и быстро прославился в своём городе тем, что приносил домой дичь за дичью."
    m 3eud "Вскоре он израсходовал все шесть пуль." 
    m 1esc "На следующей охоте охотник увидел кабана, самого крупного из когда-либо виденных им. Это была слишком уж большая добыча, чтобы отказаться от той." 
    m 1euc "Он зарядил последнюю пулю, надеясь уничтожить зверя..."
    m 1dsc "Но когда тот выстрелил, пуля попала его любимой невесте в грудь, убив её."
    m 3esc "Затем продавец явился охотнику, скорбя о трагической утрате того, показывая, что он на самом деле дьявол."
    m 1esd "— Я дам тебе шанс на искупление, охотник. — сказал ему продавец."
    m 4esb "— Оставайся верным своей возлюбленной до конца своей жизни, и ты воссоединишься с ней после смерти."
    m 1eud "Охотник поклялся оставаться верным ей до конца своей жизни..."
    m 1dsd "...{w=1}или около того."
    m 1dsc "Вскоре после её кончины он влюбился в другую женщину и вскоре женился на ней, забыв о своей прошлой любви."
    m 1esc "Это было до одного года на следующий день после рокового инцидента. Когда охотник ехал через лес, преследуя какую-то дичь, он наткнулся на место, где он убил свою возлюбленную."
    m 3wud "К его ужасу,{w=1.0} её труп, который был похоронен в другом месте, стоял на том же самом месте, где она была убита."
    m "Она подошла к охотнику, презирая его за неверность, и поклялась отомстить за своё убийство."
    m "Охотник в панике уехал прочь."
    m 1euc "Пройдя короткий путь, он оглянулся назад, чтобы проверить, следует ли она за ним дальше."
    m 1wkd "К его ужасу, он не только не продвинулся дальше своей дистанции, но и преследовавшая значительно приблизилась к нему."
    m 3wkd "В своём страхе он не смог избежать ветви, которая была впереди него, незамедлительно сбив охотника со своего коня вниз на холодную землю."
    m 4dsc "Однако его внимание не было на его лошади, поскольку существо умчалось прочь без него."
    $ store.mas_sprites.show_empty_desk()
    m 1esc "...Вместо этого он был на фигуре, с которой тот обещал быть вечно в загробной жизни."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        show yuri dragon2 zorder 72 at malpha
        $ style.say_dialogue = style.edited
        y "{cps=*2}Я тоже до тебя доберусь.{/cps}{nw}"
        hide yuri
        $ mas_resetTextSpeed()
        show monika 1eua at i11 zorder MAS_MONIKA_Z
    hide emptydesk
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_kuchisake_onna",
    category=[store.mas_stories.TYPE_SCARY], prompt="Кутисакэ-онна",unlocked=False),
    code="STY")

label mas_scary_story_kuchisake_onna:
    call mas_scary_story_setup
    m 3eud "Жила-была красивая женщина, жена самурая."
    m 3eub "Она была так же невероятно красива, как и тщеславна, приветствуя внимание любого мужчины, готового предложить его ей."
    m 1tsu "И часто просила мужчин оценить её внешность."
    m 1euc "Женщина была склонна обманывать мужа несколько раз и вскоре тому стало известно о её делах."
    m 1esc "Когда он столкнулся с ней, он был вне себя от ярости, поскольку она наносила ущерб их статусу дворян, унижая его."
    m 2dsc "Затем он жестоко наказал её, перерезав ей рот от уха до уха, изуродовав её нежную красоту."
    m 4efd "«Кто теперь будет считать тебя красивой?» — было его солью к её ужасающей ране."
    m 2dsd "Вскоре после этого женщина умерла."
    m "Она не могла жить дальше после того, как все вокруг относились к ней как к уроду."
    m 1esc "Её муж, осуждённый за свою жестокость, совершил сеппуку вскоре после этого."
    m 3eud "Женщина, умиревшая от такой участи, стала мстительным и злым духом."
    m "Говорят, что теперь она бесцельно бродит по ночам, её лицо покрыто маской, и та всегда с клинковым оружием на руках."
    m 1dsd "Любой, кому не посчастливится встретить её, услышит её леденящий душу вопрос..."
    m 1cua "{b}{i}Я к р а с и в а я?{/i}{/b}"

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,15) == 1) or mas_full_scares:
        hide monika
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        show natsuki ghost2 zorder 73 at i11
        show k_rects_eyes1 zorder 74
        show k_rects_eyes2 zorder 74
        $ pause(0.25)
        #play music t7g
        stop sound
        hide screen tear
        $ style.say_dialogue = style.edited
        show screen mas_background_timed_jump(5, "mas_scary_story_kuchisake_onna.no")
        menu:
            "Я красивая?"
            "Да.":
                hide screen mas_background_timed_jump
                jump mas_scary_story_kuchisake_onna.clean
            "Нет.":
                jump mas_scary_story_kuchisake_onna.no
    else:
        jump mas_scary_story_kuchisake_onna.end

label .no:
    hide screen mas_background_timed_jump
    "{b}{i}Это так?{w=1.0}{nw}{/i}{/b}"
    $ _history_list.pop()
    $ _history_list.pop()
    $ pause(1.0)
    hide natsuki
    play sound "sfx/run.ogg"
    show natsuki mas_ghost onlayer front at i11
    $ pause(0.25)
    hide natsuki mas_ghost onlayer front

label .clean:
    show black zorder 100
    hide k_rects_eyes1
    hide k_rects_eyes2
    hide natsuki
    $ pause(1.5)
    hide black
    $ mas_resetTextSpeed()
    show monika 1eua at i11 zorder MAS_MONIKA_Z

label .end:
    m 3eud "Судьба, которую она тебе преподнесёт — зависит от твоего ответа."
    m "Встреча с ней не всегда означает твою гибель."
    m 3esc "Однако..."
    m "Если ты не знаешь, как справиться с вопросом..."
    m 3tku "Ты можешь просто закончить как она."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_mujina",
    category=[store.mas_stories.TYPE_SCARY], prompt="Мудзина",unlocked=False),
    code="STY")

label mas_scary_story_mujina:
    call mas_scary_story_setup
    m 1esc "Однажды ночью, в поздний час, старый купец шёл по дороге домой после долгого дня продажи своих товаров."
    m 3esc "Дорога, по которой он ехал, вела к большому холму, который был очень тёмным и уединённым ночью, поэтому многие путешественники старались избегать этого района."
    m "Однако мужчина устал и решил пойти по дороге, так как это ускорит его возвращение домой."
    m "С одной стороны холма был старый ров, довольно глубокий."
    m 3eud "Когда он шёл, он заметил женщину, сидящую у рва, совсем одну и горько рыдающую."
    m "Хотя мужчина был истощён, он боялся, что женщина собирается броситься в воду, поэтому остановился."
    m 3euc "Она была миниатюрной и хорошо одетой, закрывая лицо одним из рукавов кимоно, при этом отвернувшись от него."
    m 3eud "Мужчина сказал ей: «Мисс, пожалуйста, не плачьте. В чём дело? Если есть что-то, что я могу сделать, чтобы помочь вам, я был бы рад это сделать.»"
    m "Женщина продолжала плакать, игнорируя его."
    m 3ekd "«Мисс, послушайте меня. Это не место для леди по ночам. Пожалуйста, позвольте мне помочь вам.»"
    m 1euc "Женщина медленно поднялась, всё ещё рыдая."
    m 1dsc "Мужчина слегка положил руку ей на плечо..."
    m 4wud "Когда она резко повернула голову к нему, тому предстало пустое лицо, лишённое всех человеческих особенностей."
    m 4wuw "Ни глаз, ни рта, ни носа. Лишь пустой облик, который смотрел на него!"
    m "Купец убежал так быстро, как только мог, в панике от преследующей его фигуры."
    m 1efc "Он продолжал бежать, пока не увидел свет фонаря и в тот час побежал к нему."
    m 3euc "Фонарь принадлежал странствующему торговцу, который шёл рядом."
    m 1esc "Старик резко остановился перед ним, чтобы перевести дыхание."
    m 3esc "Торговец спросил, куда он так бежал."
    m 4ekd "«Ч-чудовище! У рва была девушка без лица!» — зарыдал купец."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,10) == 1) or mas_full_scares:
        $ style.say_dialogue = style.edited
        m 2tub "Торговец ответил: «О, вы имеете в виду...{w=2} {b}вот это?{/b}»{nw}"
        show mujina zorder 75 at otei_appear(a=1.0,time=0.25)
        play sound "sfx/glitch1.ogg"
        $ mas_resetTextSpeed()
        $ pause(0.4)
        stop sound
        hide mujina
    else:
        m 2tub "Торговец ответил: «О, вы имеете в виду... вот это?»"
    m 4wud "Мужчина поднял глаза на продавца и увидел такую же ужасающую пустоту от девушки."
    m "Прежде чем торговец смог уйти, пустота издала пронзительный визг..."
    m 1dsc "...А потом наступила тьма."
    show black zorder 100
    $ pause(3.5)
    hide black
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_ubume",
    category=[store.mas_stories.TYPE_SCARY], prompt="Убумэ",unlocked=False),
    code="STY")

label mas_scary_story_ubume:
    call mas_scary_story_setup
    m 3euc "Однажды ночью в поздний час женщина зашла в кондитерскую, чтобы купить конфеты прямо перед тем, как владелец собирался ложиться спать."
    m 1esc "Деревня была маленькая, и кондитер не узнал женщину, но не думал об этом."
    m "Он устало продал женщине конфеты, которые она просила."
    m 1euc "На следующий вечер примерно в то же время, та же женщина вошла в магазин, чтобы купить ещё больше конфет."
    m "Она продолжала посещать магазин по ночам, пока кондитер не заинтересовался женщиной, вскоре после чего тот решил последовать за ней в следующий раз, когда она вошла."
    m 1esd "На следующую ночь женщина пришла в своё обычное время, купила конфеты, как она обычно делала, и счастливо отправилась в путь."
    m 3wud "После того, как она вышла за дверь, кондитер заглянул в свою копилку и увидел, что монеты, которые дала ему женщина, превратились в листья с дерева."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    m 1euc "Он последовал за женщиной к внешней стороне храма, что был неподалёку, где она просто исчезла."
    m 1esc "Кондитер был шокирован этим, и решил вернуться домой."
    m 3eud "На следующий день он пошёл в храм и сообщил монаху, что видел."
    m 1dsd "Священник рассказал кондитеру, что недавно на улице внезапно умерла молодая женщина, которая ехала через деревню."
    m "Монах почувствовал сострадание к бедной мёртвой женщине, так как она была на последнем месяце беременности."
    m 1esc "Он похоронил её на кладбище за храмом и дал ей и её ребёнку безопасный проход в загробную жизнь."
    m 4eud "Когда монах вёл кондитера к месту могилы, те оба услышали плач ребёнка из-под земли."
    m "Тотчас же, они взяли пару лопат и выкопали могилу."
    m 1wuw "К их большому шоку, они обнаружили новорождённого мальчика, сосущего конфеты."
    m "Конфеты, которые кондитер всегда продавал женщине."
    m 1dsd "Они подняли мальчика из могилы, и монах взял его, как своего собственного, чтобы воскресить."
    m 1esc "И призрак женщины больше никогда не видели."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_womaninblack",
    category=[store.mas_stories.TYPE_SCARY], prompt="Женщина в чёрном",unlocked=False),
    code="STY")

label mas_scary_story_womaninblack:
    call mas_scary_story_setup
    m 3esd "Однажды ночью полковник сел на поезд по дороге домой."
    m 1esd "Когда он нашёл удобное место для сидения, вскоре заснул от дневной усталости."
    m 3eud "Через некоторое время он проснулся, чувствуя себя напряжённым и чем-то обеспокоенным."
    m "К его удивлению, он заметил, что теперь напротив него сидит женщина."
    m "Её наряд был полностью чёрным, включая вуаль, которая скрывала её лицо."
    m 1esc "Она, казалось, смотрела на что-то на коленях, хотя там ничего не было."
    m 3esd "Полковник был дружелюбным парнем, так что постарался вести с ней светскую беседу."
    m 1dsd "К его ужасу, она не ответила на его любезности."
    m 1esc "Внезапно она начала раскачиваться взад-вперёд и петь мягкую колыбельную."
    m "Прежде чем полковник успел поинтересоваться, поезд завизжал."
    m "Чемодан из купе сверху упал и ударил его по голове, сбив его без сознания."
    show black zorder 100
    play sound "sfx/crack.ogg"
    $ pause(1.5)
    hide black
    m 3eud "Когда он пришёл в себя, женщины уже не было. Полковник допросил других пассажиров, но никто из них её не видел."
    m 3ekd "В довершение ко всему, как только полковник вошёл в купе, оно было заперто, как это было принято, и никто не входил и не выходил из него после того, как тот вошёл."
    m 1esc "Когда он вышел из поезда, железнодорожный чиновник, который подслушал его, поговорил с этим же полковником о женщине, о которой тот спрашивал."
    m "По словам чиновника, женщина и её муж ехали в поезде вместе."
    m 1dsd "Муж слишком глубоко засунул голову в одно из окон и был обезглавлен проволокой."
    m "Затем его тело упало ей на колени, безжизненное."
    m 3wud "Когда поезд прибыл на остановку, её нашли с трупом на руках и поющую тому колыбельную."
    m "Она так и не пришла в себя и вскоре умерла."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_resurrection_mary",
    category=[store.mas_stories.TYPE_SCARY], prompt="Воскресшая Мэри",unlocked=False),
    code="STY")

label mas_scary_story_resurrection_mary:
    call mas_scary_story_setup
    m 3eua "Во время рождественских танцев молодой человек по имени Льюис наслаждался временем со своими друзьями, когда молодая женщина, которую он не видел ранее, привлекла его внимание."
    m 1eub "Девочка была высокая, блондинка, голубоглазая и очень красивая."
    m 1hub "Она была одета в красивое белое платье, с белыми танцевальными туфлями и тонкой шалью."
    m 3esb "Льюис нашёл девушку очаровательной. Он решил пригласить её потанцевать с ним, и та приняла его приглашение."
    m 1eud "Она, конечно, была красива, но Льюис чувствовал, что в ней было что-то странное."
    m 3esd "Когда они танцевали, он пытался узнать её получше, но всё, что она говорила о себе — это то, что её звали Мэри, и что она была из южной части города."
    m "Кроме того, её кожа была холодной и липкой на ощупь. В какой-то момент вечером он поцеловал Мэри и обнаружил, что её губы были такими же холодными, как её кожа."
    m 1esb "Они провели большую часть ночи вместе, танцуя. Когда пришло время уезжать, Льюис предложил Мэри подвезти ту до её дома, и она снова приняла приглашение."
    m 3esb "Она велела ему ехать по определённой дороге, и он согласился."
    m 3eud "Проезжая мимо ворот кладбища, Мэри попросила Льюиса остановиться."
    m 1eud "Несмотря на недоумение, Льюис остановил машину, как она просила."
    m 3eud "Затем она открыла дверь, наклонилась к Льюису и прошептала, что ей нужно идти, а он не может пойти с ней."
    m 1euc "Она вышла из машины и подошла к воротам кладбища, прежде чем исчезнуть."
    m "Льюис долго сидел в машине, сбитый с толку тем, что только что произошло."
    m 1esd "Он больше никогда не видел эту прекрасную женщину."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,20) == 1) or mas_full_scares:
        play sound "sfx/giggle.ogg"
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_corpse",
    category=[store.mas_stories.TYPE_SCARY], prompt="Реанимированный труп",unlocked=False),
    code="STY")

label mas_scary_story_corpse:
    call mas_scary_story_setup
    m 1esa "Жил-был старик, который управлял старой придорожной гостиницей. Однажды вечером, 4 человека приехали и попросили номер."
    m 3eua "Старик ответил, что все комнаты заняты, но он мог бы найти им место для сна, если бы они не были слишком особенными."
    m 1esa "Мужчины были измучены и уверяли мужчину, что любое место подойдёт."
    m 1eud "Он привел их в комнату позади. В углу комнаты лежал труп женщины."
    m "Он пояснил, что его невестка недавно скончалась и что она ожидает погребения."
    m 1eua "После того как старик ушел, 3 из 4 мужчин заснули. Последний же никак не мог уснуть."
    m 1wuo "Внезапно мужчина услышал скрип."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m 3wuo "Он поднял глаза и при свете лампы увидел, как женщина поднялась, теперь с клыками и ногтями, похожими на когти, и направилась к ним."
    m "Она наклонилась и укусила каждого из спящих мужчин. Четвёртый мужчина в последнюю секунду приподнял подушку перед шеей."
    m 1eud "Женщина укусила подушку и, видимо, не понимая, что она так и не смогла укусить последнего мужчину, вернулась в своё первоначальное место отдыха."
    m 3eud "Мужчина пнул своих товарищей, но никто из них не пошевелился. Он решил рискнуть и сбежать."
    m 3wuo "Однако, как только его ноги коснулись земли, он услышал ещё один скрип."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,2) == 1) or mas_full_scares:
        play sound "sfx/crack.ogg"
    m "Поняв, что женщина снова встаёт со своего места, он открыл дверь и побежал так быстро, как только мог."
    # need opinions on this one since it's for storytelling purposes
    show layer master at heartbeat2(1)
    show vignette as flicker zorder 72 at vignetteflicker(0)
    play sound hb loop
    m 3eud "Пройдя небольшое расстояние, он оглянулся и увидел, что труп был недалеко от него."
    m 3wud "Последовала погоня, и когда та догнала его, он оказался под деревом."
    m "Она бросилась к нему, вытянув когтистые ногти."
    m 4wud "В последнюю секунду мужчина увернулся, и она ударила дерево с большой свирепостью."
    m 3wud "Теперь её ногти были глубоко врезаны в дерево."
    m 1wud "Она дико замахнулась рукой на мужчину, когда он лежал на земле, не в силах дотянуться до него."
    m 1eud "Человек, напуганный и измученный ползал рядом и отрубился."
    show layer master
    stop sound
    hide flicker
    show black zorder 100
    $ pause(2.5)
    hide black
    m 1esd "На следующее утро проходящий мимо полицейский нашёл мужчину и привел его в сознание."
    m "Мужчина рассказал, что произошло. Офицер, думая, что этот человек был пьян, проводил его до гостиницы."
    m 1eud "Когда они прибыли, гостиница была в состоянии большой суматохи."
    m 3eud "3 путешественника были найдены мёртвыми в своих постелях."
    m "Тело невестки лежало там, где она была накануне вечером, но теперь её одежда была запачкана кровью, а под ногтем был найден кусок коры."
    m 3esd "После допроса владелец гостиницы, наконец, признал, что женщина умерла шесть месяцев назад, и он пытался сэкономить достаточно денег, чтобы дать ей надлежащее захоронение."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_jack_o_lantern",
    category=[store.mas_stories.TYPE_SCARY], prompt="Джек О'Лантерн",unlocked=False),
    code="STY")

label mas_scary_story_jack_o_lantern:
    call mas_scary_story_setup
    # chance of 1 in 4
    $ _mas_jack_scare = (persistent._mas_pm_likes_spoops and renpy.random.randint(1,4) == 1) or mas_full_scares
    m 4esd "Жил-был человек по имени Джек. Джек был жалким, старым пьяницей, которому доставляло удовольствие подшучивать над людьми."
    m 3esa "Однажды ночью Джек столкнулся с дьяволом и пригласил его выпить с ним."
    m "После того, как Джек насытился, он повернулся к дьяволу и попросил его превратиться в монету, чтобы он мог заплатить за их напитки, так как у него не было денег, чтобы заплатить за них."
    m 1esa "Как только дьявол сделал это, Джек положил монету в карман и вышел, не заплатив."
    m "Дьявол не мог вернуться к своему первоначальному виду, потому что Джек положил его в карман рядом с серебряным крестом."
    m 3esa "Джек в конце концов освободил дьявола, при условии, что он не будет беспокоить Джека в течение 1 года и что, если Джек умрёт, он не будет претендовать на его душу."
    m "В следующем году Джек снова столкнулся с дьяволом. На этот раз он обманом заставил того забраться на дерево, чтобы сорвать фрукт."
    m 3esd "Пока тот был на дереве, Джек окружил его белыми крестами, чтобы дьявол не смог спуститься."
    m "Как только дьявол пообещал не беспокоить его ещё 10 лет, Джек снял их. Когда Джек умер, он попал на небеса."
    m 1eud "Когда он прибыл, ему сказали, что он не может войти, так как плохо прожил на Земле."
    m 1eua "Итак, он отправился в ад, где дьявол сдержал своё обещание и не позволил Джеку войти."
    m 1eud "Джек испугался, потому что ему некуда было идти."
    m 1esd "Джек спросил Дьявола, как он мог уйти, так как света не было."
    if _mas_jack_scare:
        hide vignette
        show darkred zorder 82:
            alpha 0.85
    m 1eud "Дьявол бросил Джеку уголёк из пламени ада, чтобы помочь Джеку осветить свой путь."
    m "Джек вытащил репу, которая была у него с собой, вырезал её и поместил в неё угольки."
    m 3eua "С этого дня Джек бродил по земле без места отдыха, освещая путь, когда он шёл со своим Джеком О'Лантерном."
    if _mas_jack_scare:
        hide darkred
        show vignette zorder 70
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_baobhan_sith",
    category=[store.mas_stories.TYPE_SCARY], prompt="Баобанские ситы",unlocked=False),
    code="STY")

label mas_scary_story_baobhan_sith:
    call mas_scary_story_setup
    m 1esa "Жила-была однажды молодая группа охотников, которая остановилась на ночь в небольшом охотничьем домике."
    m 3esb "Поселившись, они развели костёр и стали весело есть и пить, потому что это был хороший день."
    m 1tku "Они сказали себе, что единственное, чего им не хватало, это компании красивых женщин рядом с ними."
    m 1tsb "Вскоре после того, как они это сказали, в их дверь постучали."
    m 3eub "В дверях стояли четыре прекрасные женщины."
    m "Женщины, заблудившись в пустыне, спросили, могут ли они присоединиться к мужчинам в их убежище на ночь."
    m 1tku "Мужчины, молча поздравляя себя с благополучием, пригласили женщин войти."
    m 1esa "Через некоторое время, наслаждаясь компанией друг друга, женщины выразили желание потанцевать."
    m 1tku "Мужчины не теряли времени на связь с каждой из девиц."
    m 1eub "Когда они танцуют, один из мужчин замечает, что другие пары танцуют довольно хаотично."
    m 1wuo "Затем, к его ужасу, он понимает, что у других мужчин кровь льётся с их шей на их рубашки."
    m 3wuo "В слепой панике мужчина бросил свою партнёршу и выскочил за дверь, прежде чем смог разделить судьбу своих друзей."
    m 3wud "Он побежал в лес и спрятался среди лошадей, на которых ездил со своими друзьями в тот день."
    m "Женщины, не далеко позади, приблизились, но, казалось бы, не могли пройти мимо лошадей к мужчине."
    m 1eud "Итак, он стоял, усталый, среди животных всю ночь, когда женщины обходили вокруг лошадей, пытаясь найти способ добраться до него."
    m 1esa "Незадолго до рассвета, женщины сдались и отступили обратно в лес."
    m 1esd "Оставшись один, мужчина осторожно направился обратно к охотничьему домику, не слыша ни звука изнутри."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,14) == 1) or mas_full_scares:
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (50,95)
        show blood splatter1 as bl3 zorder 73:
            pos (170,695)
        show blood splatter1 as bl4 zorder 73:
            pos (150,395)
        show blood splatter1 as bl5 zorder 73:
            pos (950,505)
        show blood splatter1 as bl6 zorder 73:
            pos (700,795)
        show blood splatter1 as bl7 zorder 73:
            pos (1050,95)
        $ pause(1.5)
        stop sound
        hide bl2
        hide bl3
        hide bl4
        hide bl5
        hide bl6
        hide bl7
    m 3wuo "Когда он заглянул внутрь, увидел трёх своих товарищей, мёртвых на полу, их кожа была почти прозрачной, когда они лежали в луже собственной крови."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_serial_killer",
    category=[store.mas_stories.TYPE_SCARY], prompt="Серийный убийца",unlocked=False),
    code="STY")

label mas_scary_story_serial_killer:
    call mas_scary_story_setup
    m 3tub "Молодая пара припарковала свою машину рядом с большим деревом вербы на кладбище одна ночью спокойно «заняться любовью.»"
    m 3euc "Через некоторое время их прервал репортаж по радио о том, что известный серийный убийца сбежал из психиатрической больницы неподалёку."
    m "Беспокоясь о своей безопасности, они решили продолжить в другом месте."
    m 1esc "Однако...{w=0.3} машина вообще не заводилась."
    m 3esd "Молодой человек вышел из машины, чтобы найти помощь, и сказал девушке оставаться внутри с запертыми дверями."
    m 3wud "Несколько мгновений спустя она вздрогнула, услышав жуткий скрежет на крыше машины."
    m 1eud "Она подумала, что это, должно быть, была лишь ветка дерева на ветру."
    m 1euc "По прошествии долгого времени мимо проехал полицейский автомобиль и остановился, но девушка всё ещё не видела своего парня."
    m 1eud "Полицейский подошёл к машине и дал указание девушке выйти из машины и идти к нему навстречу, а не оглядываться."
    m "Она делала это очень медленно..."
    m 1ekc "Затем девушка заметила множество других полицейских машин, прибывших с сиренами, ревущими позади первой прибывшей."
    m 1dsd "Любопытство взяло над ней верх, и она повернулась, чтобы посмотреть на машину..."
    m 4wfw "Она увидела своего парня вверх ногами и свисающим с дерева над их машиной с широко разрезанной шеей..."

    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,8) == 1) or mas_full_scares:
        show y_sticker hopg zorder 74:
            pos(600,425)
            alpha 1.0
            linear 1.6 alpha 0
        play sound "<from 0.4 to 2.0 >sfx/eyes.ogg"
    m 1dfc "...И его сломанные и окровавленные ногти на крыше."
    hide y_sticker
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(Event(persistent._mas_story_database,eventlabel="mas_scary_story_revenant",
    category=[store.mas_stories.TYPE_SCARY], prompt="Ревенант",unlocked=False),
    code="STY")

label mas_scary_story_revenant:
    call mas_scary_story_setup
    m 4eua "Когда-то был мужчина, который женился на женщине."
    m 4ekd "Он был богатым человеком, который зарабатывал деньги нечестным путём."
    m 2eud "Вскоре после их брака до него стали доходить слухи, что жена изменяет ему."
    m 2esd "Стремясь выяснить правду, мужчина сказал жене, что уезжает в командировку на несколько дней и покинул дом."
    m 2eud "Без ведома жены мужчина пробрался в дом поздно вечером с помощью одного из своих слуг."
    m "Мужчина взобрался на одну из балок, нависавших над его кроватью, и стал ждать."
    m 4ekd "Вскоре после этого его жена вошла с мужчиной по соседству, двое поболтали некоторое время, а затем начали раздеваться."
    m 4eud "Человек в это время неуклюже упал на землю недалеко от того места, где они находились, без сознания."
    m "Прелюбодей схватил его одежду и убежал, но жена подошла к мужу и нежно гладила его по волосам, пока он не проснулся."
    m "Мужчина наказал свою жену за прелюбодеяние и пригрозил наказанием, когда оправится от грехопадения."
    m 2dsc "Мужчина, однако, так и не оправился от падения и умер в одночасье. Его похоронили на следующий день."
    m 2esd "В ту ночь труп мужчины поднялся из могилы и стал бродить по окрестностям."
    m "С рассветом он возвращался в могилу."
    m 3esd "Это продолжалось ночь за ночью, и люди начали запирать свои двери, опасаясь выходить на улицу, чтобы выполнять любые поручения после того, как солнце опустилось."
    m "Чтобы они не наткнулись на существо и не были избиты чёрным и синим."
    m 2dsd "Вскоре после этого город охватила болезнь, и в их сознании не было сомнений, что виноват труп."
    m 2dsc "Люди начали убегать из города, чтобы не умереть от болезни."
    m 2esd "По мере того как город разваливался, собралось собрание, и было решено, что труп должен быть выкопан и утилизирован."
    m "Группа людей взяла лопаты и нашла кладбище, на котором был похоронен мужчина."
    m "Им не пришлось долго копать, прежде чем они добрались до трупа человека."
    m 4eud "После того, как он был полностью выкопан, жители деревни избили труп лопатами и выволокли тело из города."
    m 3esd "Там они развели большой костёр и бросили тело в него."
    m 3eub "Труп мужчины испустил леденящий кровь крик и попытался выползти из огня, прежде чем, наконец, поддался ему."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_yuki_onna",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Юки-онна",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_yuki_onna:
    call mas_scary_story_setup
    m 4eud "Жили-были два лесоруба, отец и сын, они возвращались к себе домой, когда внезапно возникла метель."
    m "После небольшого путешествия, они наткнулись на заброшенную хижину и укрылись в ней."
    m 2eua "Они смогли разжечь небольшой огонь и прижимались друг к другу ради тепла перед тем, как лечь спать."
    m 2esd "Посреди ночи, сын проснулся от встряски."
    m 2wud "К его удивлению, над его отцом стояла красивая женщина, она подула на него, от чего тот мгновенно заледенел."
    m 4wud "И как только она повернулась к сыну, она остановилась. Женщина сказала ему, что избавит его от такой же судьбы, потому что он был молодой и очень красивый."
    m 4ekc "Если он хоть что-то расскажет об этом кому-либо, она вернётся, чтобы убить его."
    m 4esa "На следующую зиму, молодой человек возвращался к себе домой после вырубки леса, и тут он наткнулся на красивую путешествующую женщину."
    m 2eua "Пошёл снег, и юноша предложил женщине укрыться от шторма, и она тут же согласилась."
    m 2eua "Они быстро влюбились друг в друга, и в конечном счёте женились."
    m 2hua "Они жили счастливо целые годы, и с течением времени завели несколько детей."
    m 2esa "Однажды вечером, пока дети спали, женщина занималась шитьём у горящего камина."
    m 2eud "Юноша оторвался от своего дела, и воспоминание о той ночи, о которой он никогда не говорил, вернулось к нему."
    m "Жена спросила юношу, почему он смотрел на неё таким образом."
    m 3esc "Юноша рассказал свою историю о столкновении со снежной женщиной."
    m 2wud "Улыбка на лице его жены расплылась от злости, поскольку она была той самой снежной женщиной, о которой он говорил."
    m 4efc "Она объявила ему выговор за нарушение обещания, и она бы убила его, если бы их дети."
    m 4efd "Она сказала юноше, что ему следует хорошо заботиться о своих детях, иначе она вернётся, чтобы разобраться с ним."
    m 4dsd "В следующее мгновение, она исчезла, и её больше никто не видел."
    if (persistent._mas_pm_likes_spoops and renpy.random.randint(1,3) == 1) or mas_full_scares:
        hide monika
        play sound "sfx/giggle.ogg"
        pause 1.0
        show black zorder 100
        show monika at i11 zorder MAS_MONIKA_Z
        $ pause(1.5)
        hide black
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_many_loves",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Много возлюбленных",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_many_loves:
    call mas_scary_story_setup
    m 4esa "Жила-была одна молодая девушка, которая на днях заглянула в деревню, чтобы найти себе мужа."
    m 4eua "Она была очень красивой, и сразу же привлекла к себе много претендентов."
    m 2eua "В конечном счёте, всё свелось к здоровому рыбаку."
    m 2esd "У них был счастливый брак, но не прошло и года, как муж начал слабеть, после чего он умер."
    m "Люди в деревне сочувствовали молодой девушке и утешали её, как могли."
    m 4esa "Спустя пару мгновений, девушка вышла замуж за крепкого лесоруба."
    m 4dsd "Они жили счастливо какое-то время, но он зачах и умер."
    m 4eud "Некоторые жители деревни подумали, мол, как-то странно то, что мужья умерли одним и тем же способом, но никто ничего не сказал, и пожалели девушку за её же невезение."
    m 2esc "Позже, девушка снова вышла замуж, и на этот раз – за крепкого каменщика, и у них так же был счастливый брак, но через год, девушка снова стала вдовой."
    m "На этот раз, жители деревни пообщались между собой и поняли, что происходит что-то подозрительное, поэтому группа жителей деревни отправилась на поиски ближайшего шамана."
    m "Как только они нашли шамана и рассказали ему свою историю, шаман указал на то, что он в курсе того, что происходит."
    m 3euc "Он позвал своего ассистента, молодого парня с хорошим телосложением, шепнул ему на ухо и отправил его домой вместе с жителями деревни."
    m "Он сказал им не волноваться, его ассистент разберётся с этим."
    m 2esc "Когда они вернулись в деревню, ассистент позвал вдову, и, вскоре после этого, они поженились."
    m 2efc "В ночь их свадьбы, ассистент положил нож под подушку и сделал вид, что спит."
    m 2esd "Немного позже полуночи, парень почувствовал чьё-то присутствие над собой и что ему что-то колет шею."
    m 2dfc "Парень достал нож и воткнул его в существо, которое было над ним."
    if (renpy.random.randint(1,20) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares:
        show monika 6ckc
        show mas_stab_wound zorder 75
        play sound "sfx/stab.ogg"
        show blood splatter1 as bl2 zorder 73:
            pos (590,485)
        $ pause(1.5)
        stop sound
        hide bl2
        hide mas_stab_wound
        show black zorder 100
        $ pause(1.5)
        hide black
    m 3wfc "Он услышал визг и хлопанье крыльев, после чего существо вылетело в окно."
    m 1dfc "На следующий день, невесту нашли мёртвой недалеко от дома с ножевым ранением в груди."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_gray_lady",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Серая леди",
            unlocked=False
        ),
    code="STY"
    )

label mas_scary_story_gray_lady:
    call mas_scary_story_setup
    m 4eua "Жил-был один человек по имени Уильям, который рос вместе со своим отцом, помогая ему с его гнусными разработками."
    m 4ekd "Такие как развевающиеся огни на берегу под покровом ночи, в надежде заманить корабли на берег, дабы те разбились об коварные камни на самом берегу."
    m 2ekc "После чего собрать всю добычу, посыпавшуюся из корабля, и убить всех выживших."
    m 2eud "Во время одной из экспозиций своего отца, он спас красивую женщину и в конечном итоге принял решил оставить свою старую жизнь позади, и женился на ней."
    m 2esa "Пара арендовала поместье неподалёку от того места."
    m 2hub "Они жили счастливо вместе, но их больше обрадовало то, что у них родилась дочка, которую звали Кейт."
    m 4esa "С течением лет, Кейт выросла жизнерадостной молодой девушкой."
    m 2ekc "Уильям втайне боялся, что у него не хватит денег, чтобы купить поместье, и он предлагает его как приданое человеку, который женится на его дочери."
    m 4hub "Потом в один прекрасный день, Кейт познакомилась и влюбилась в ирландского капитана пиратов, и они поженились."
    m 4esb "Счастливая пара решила поселиться в Дублине, поскольку у родителей Кейт не владели собственной землей, дабы обеспечить их."
    m 4eua "Кейт обещала вернуться и навестить своих родителей как-нибудь."
    m 4esd "Время шло, и Уильям вместе со своей женой начали сильно скучать по своей дочери и хотели, чтобы она вернулась."
    m 2dkc "Уильям решил вернуться к своим старым дням на достаточно долгое время, чтобы собрать достаточно денег для покупки поместья, чтобы потом предложить своей дочери и её мужу жить вместе с ними."
    m 4wud "Однажды вечером, заманив корабль на берег и собирая на нём добычу, он заметил перед собой сильно искалеченную женщину, лежащую на камнях."
    m 2wuc "Очертания её лица стали неузнаваемыми из-за травм, которые ей пришлось получить."
    m 2ekc "Уильям, сжалившись над ней, отнёс её обратно в поместье и сделал всё, что мог, дабы попытаться спасти её жизнь, но женщина умерла, даже не придя в сознание."
    m 2eud "Пока они обыскивали её тело, пытаясь найти хоть какие-то подсказки к её личности..."
    m "...они нашли маленький кошелёк, привязанный к её талии, в котором было достаточно золотых монет и драгоценностей для них, чтобы наконец-то купить особняк, который они взяли в аренду."
    m 2dsc "Спустя несколько дней, Адмиралтейство начало спрашивать пару о пропавшем из-под обломков пассажире, где выяснилось, что это никто иная, как их дочь."
    m 3dsd "Будучи подавленными и пристыженными, родители заточили её останки в тайной комнате, а сами уехали и никогда не возвращались."
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Цветочный фонарь",
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern:
    call mas_scary_story_setup

    if not mas_getEVL_shown_count("mas_scary_story_flowered_lantern"):
        m 3eub "Перед тем, как мы начнём, я должна сказать тебе, что эта история будет немного длинной."
        m 3eua "И поэтому, я разделю её на три части."
        m "Как только я закончу эту часть, я спрошу тебя, хочешь ли ты услышать продолжение или нет."
        m 1eub "Если ты скажешь нет, ты можешь попросить меня рассказать тебе следующую часть позже, так что не волнуйся об этом."
        m 4hua "Ладно, давай начнём."
    
    m 4eua "Жила-была одна красивая и молодая девушка по имени Цую, её отец был высокопоставленным самураем."
    m 4eud "Мать Цую умерла, и её отец, со временем, женился ещё раз."
    m 2euc "Но отцу Цую стало понятно, что она и её мачеха не смогут поладить."
    m 2esa "Стремясь к обеспечению счастья своей единственной дочери, он построил для неё роскошный дом подальше от их дома, после чего она переехала туда."
    m "Однажды, семейный врач отправился в поместье Цую с рабочим визитом вместе с молодым самураем по имени Хагивара, и он был очень красивым."
    m 4eub "Как только Цую и Хагивара посмотрели в глаза друг другу, они тотчас влюбились."
    m 4esc "Втайне от врача, они дали клятву друг другу на всю жизнь перед тем, как они ушли."
    m 4dsd "Цую прошептала Хагиваре, что она однозначно умрёт, если он не вернётся, чтобы проведать её."
    m 2esc "Хагивара не забыл её слова, но этикет запрещал ему идти в гости к девушке одному, поэтому ему пришлось ждать врача и попросить его составить ему компанию в очередном визите."
    m 2dsd "Однако, врач почувствовал свою внезапную привязанность к Цую."
    m 4ekc "Отец Цую был известен тем, что он казнил тех, кто разозлил его, и, боясь, что ему придётся нести ответственность за их знакомство, он избегал Хагивару."
    m 2rkc "Время шло, и Цую, презирая себя за то, что Хагивара бросил её, покончила с собой."
    m 1ekc "Вскоре после этого, врач побежал к Хагиваре и рассказал ему о смерти Цую."
    m 1dsd "Хагивара был сильно расстроен и сильно оплакивал её, произнёс молитвы и сжёг ладан для неё."

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_2", unlocked=True, pool=False)

    m 1hua "...На этом первая часть заканчивается! Хочешь перейти к следующей части?{nw}"
    $ _history_list.pop()
    menu:
        m "...На этом первая часть заканчивается! Хочешь перейти к следующей части?{fast}"
        "Да.":
            jump mas_scary_story_flowered_lantern_2
        "Нет.":
            pass
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_2",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Цветочный фонарь 2",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_2:
    call mas_scary_story_setup
    $ _mas_lantern_scare = renpy.random.randint(1,11) == 1
    m 4ekd "После того, как солнце ушло за горизонт, в первую ночь Фестиваля мёртвых, Хагивара сидел снаружи и всё ещё оплакивал утрату своей любимой до позднего вечера."
    m 2eud "Однако, как только он решил зайти домой и лечь спать, он услышал шаги вне своих ворот."
    m 4euc "Хагивара жил на одинокой улице, где нечасто увидишь прохожих, и поскольку время было позднее, он решил посмотреть, кто там идёт."
    m 4wub "К его великому удивлению и восторгу, тем человеком, идущим по дороге, оказалась никто иная, как Цую, она несла с собой бумажный фонарь, украшенный цветами, чтобы освещать себе дорогу."
    m 1hua "Хагивара позвал Цую по имени, и она тут же подошла к нему и крепко обняла его."
    m 1eua "Они рассказали друг другу, что врач сказал им, что умер другой человек."
    m "Цую сказала ему, что её отец хотел, чтобы она вышла замуж за другого человека."
    m 3eub "Она отказалась и сбежала из своего роскошного дома, чтобы скрыться от него, и в настоящее время проживает в тесном доме в определённом соседстве поблизости."
    m 3eua "Он пригласил её к себе домой, но сказал ей, чтобы та молчала, дабы не побеспокоить его слугу, ведь он может спросить, кто она."
    m 4eua "Они провели всю ночь вместе, и перед заходом солнца, Цую вернулась в своё поместье, которое покинула раньше."
    m 4esa "Следующим вечером, Цую снова заглянула к нему в гости в то же время, что и вчера ночью."
    m 2euc "Но на этот раз, слуша Хагивары проснулся и услышал голос молодой женщины, который был ему незнаком."
    m 4esd "Охваченный любопытством, но он не хотел тревожить своего хозяина, поэтому он прокрался в комнату своего хозяина и заглянул через небольшую щель в двери и заметил, что он разговаривал с молодой женщиной."
    m 4eud "Женщина стояла к нему спиной, но он смог понять, что она была очень худой и была одета в очень элегантное кимоно, которое носят только высшие слои общества."
    m 4esc "Любопытство взяло над ним верх, и слуга решил взглянуть на лицо девушки перед уходом."
    m 2dsc "Он заметил, что хозяин оставил окно открытым, и он тихо подкрался к нему."
    m 4wuw "Как только он заглянул внутрь, и, к свому ужасу, он заметил, что лицо женщины похоже на лицо давно умершей девушки, а пальцы, поглаживающие лицо хозяина, состояли лишь из голых костей."
    m 2wfd "Он поспешно скрылся от ужаса, не обратив на себя взор."
    m 1efc "На следующее утро, слуга подошёл к своему хозяину и спросил его о той женщине."
    m 4efd "Поначалу, Хагивара отрицал, что у него были какие-то посетители, но поняв, что это бесполезно, он признался в том, что произошло."
    m 4ekc "Слуга рассказал Хагиваре о том, что он видел той ночью, и что он был уверен в том, что жизнь хозяина в опасности, и начал умолять его поговорить со священником об этом."
    m 2euc "Испугавшись, но всё ещё сомневаясь, Хагивара решил привести успокоить своего слугу, разыскав поместье Цую."
    m "Хагивара отправился туда и изучил район, в котором, как сказала ему Цую, она проживала."
    m 2esc "Он осмотрелся вокруг и спросил прохожих про неё, но безрезультатно."
    m 4dsd "Когда он решил, что дальнейшие поиски окажутся бесполезными, он пошёл домой."
    m 4eud "По дороге обратно, он пришёл на кладбище рядом с храмом."
    m "Его внимание привлекла большая, новая могила, лежащая неподалёку в задней части, которую он не видел раньше."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        show mas_lantern zorder 75 at right
    m 4euc "Над ней висел бумажный фонарь, украшенный красивыми цветами, он выглядел точно так же, как и тот фонарь, который Цую несла с собой ночью."
    m 4wuc "Его это заинтриговало, и он подошёл к ней. Он решил прочитать имя человека, которому она принадлежит, и, прочитав на ней имя своей любимой Цую, он отпрыгнул от страха."
    m 2wkc "Поражённый ужасом, Хагивара тут же пошёл в соседний храм и попросил поговорить с главным священником."
    m 4esc "Когда его приняли, он рассказал главному священнику всё, что произошло."
    m 4esd "После того, как он закончил, главный священник сказал ему, что его жизни грозит опасность."
    m "Сильная скорбь Хагивары по ней и её сильная любовь к нему смогли вернуть её во время Фестиваля Мёртвых."
    m 4dsc "Любовь между живым и мёртвым людьми может только привести к смерти живого человека."
    if _mas_lantern_scare or persistent._mas_pm_likes_spoops or mas_full_scares:
        hide mas_lantern

    $ mas_setEVLPropValues("mas_scary_story_flowered_lantern_3", unlocked=True, pool=False)

    m 1hua "...На этом вторая часть заканчивается! Хочешь перейти к следующей части?{nw}"
    $ _history_list.pop()
    menu:
        m "...На этом вторая часть заканчивается! Хочешь перейти к следующей части?{fast}"
        "Да.":
            jump mas_scary_story_flowered_lantern_3
        "Нет.":
            pass
    call mas_scary_story_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_story_database,
            eventlabel="mas_scary_story_flowered_lantern_3",
            category=[store.mas_stories.TYPE_SCARY],
            prompt="Цветочный фонарь 3",
            pool=True,
            unlocked=False
        ),
        code="STY"
    )

label mas_scary_story_flowered_lantern_3:
    call mas_scary_story_setup
    $ _mas_rects_scare = (renpy.random.randint(1,11) == 1 and persistent._mas_pm_likes_spoops) or mas_full_scares
    m 1eud "Это был последний день Фестиваля мёртвых, Цую должна вернуться к мёртвым этой ночью, и она возьмёт с собой Хагивару, если они хотят повидаться друг с другом снова."
    m 3esd "Хагивара умолял священника помочь ему."
    m 3esc "Священник сказал, что страсть между ними была очень сильная, но ещё есть надежда."
    m "Он передал Хагиваре пачку бумажных талисманов, которые оберегают от духов, и велел ему обвешать ими все проходы в доме, каких бы размеров они не были."
    m 1esd "Цую не сможет войти в его поместье, пока он придерживается тех инструкций."
    m 2esa "Хагивара, благодаря помощи своего слуги, смог обвешать весь свой дом бумажными талисманами до наступления темноты."
    m 4esc "Ночь продолжалась, Хагивара пытался уснуть, но безрезультатно. И поэтому, он сел и начал размышлять о недавних событиях."
    m 2dsd "В позднее время, он услышал шаги по ту сторону своего дома."
    m "Шаги становились всё ближе и ближе."
    m 4wkc "Хагивара почувствовал внезапную тягу – она была сильнее даже его страха – взглянуть."
    m 4wkd "Он безрассудно подошёл к заслонкам и через щель увидел Цую, она стояла у входа в его дом, держа в руке свой бумажный фонарь, уставившись на бумажные талисманы."
    m "Он никогда не видел Цую настолько красивой, а его сердце будто тянуло к ней."
    m 2ekd "Снаружи, Цую начала горько плакать, говоря про себя, что Хагивара нарушил клятву, чего они добились вместе."
    m 4eud "Она плакала, но потом собралась с силами и сказала вслух, что она не уйдёт, пока не увидит его в последний раз."
    m 4esd "Пока она расхаживала вокруг его дома, Хагивара слышал её шаги, и он, время от времени, видел свет фонаря."
    m 2wud "Когда она подошла к тому месту, откуда он выглядывал, шаги остановились и, внезапно, Хагивара увидел, как Цую смотрит на него одним своим глазом."
    if _mas_rects_scare:
        play sound "sfx/glitch1.ogg"
        show rects_bn1 zorder 80
        show rects_bn2 zorder 80
        show rects_bn3 zorder 80
        pause 0.5
        $ style.say_dialogue = style.edited
        ".{w=0.7}.{w=0.9}.{nw}"
        $ mas_resetTextSpeed()
        stop sound
        hide rects_bn1
        hide rects_bn2
        hide rects_bn3
        show black zorder 100
        $ pause(1.5)
        hide black
    m 2dsc "На следующий день, слуга проснулся, подошёл к комнате своего хозяина и постучал в дверь."
    m 4ekc "Впервые за многие годы, он не получил ответа и начал волноваться."
    m 2dsd "Он снова позвал своего хозяина, но безрезультатно."
    m 2esc "Наконец, набравшись немного храбрости, он вошёл в комнату своего хозяина."
    m 4wuw "...Но, увидев его, тотчас выбежал из дома, крича от ужаса."
    m "Хагивара был мёртв, его труп был в ужасном состоянии, а на лице было выражение, полное страданий от страха..."
    m 2wfc "Рядом с ним на кровати лежали кости женщины вместе с её руками, которые вцепились в его шею, как будто она обнимала его."
    call mas_scary_story_cleanup
    return
