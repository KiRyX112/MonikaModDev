#===========================================================================================
# RETURN_LABELS
#===========================================================================================

label view_extraplus:
    python:
        store.player_zoom = store.mas_sprites.zoom_level
        store.disable_zoom_button = False
        mas_RaiseShield_dlg()
        extra_button_zoom()
        Extraplus_show()
    return

label screen_extraplus:
    show monika idle at t11
    python:
        store.disable_zoom_button = False
        Extraplus_show()
    return
    
label close_extraplus:
    show monika idle at t11
    python:
        store.mas_sprites.zoom_level = store.player_zoom
        mas_DropShield_dlg()
        disable_button_zoom()
    jump ch30_visual_skip
    return

label close_dev_extraplus:
    show monika idle at t11
    python:
        mas_DropShield_dlg()
        disable_button_zoom()
    jump ch30_visual_skip
    return

label show_boop_screen:
    show monika staticpose at t11
    python:
        store.disable_zoom_button = True
        store.mas_sprites.reset_zoom()
    call screen boop_revamped
    return

label return_boop_screen:
    python:
        store.disable_zoom_button = False
        store.mas_sprites.zoom_level = store.player_zoom
        store.mas_sprites.adjust_zoom()
    jump screen_extraplus
    return

label close_boop_screen:
    show monika idle at t11
    python:
        store.disable_zoom_button = False
        store.mas_sprites.zoom_level = store.player_zoom
        store.mas_sprites.adjust_zoom()
        disable_button_zoom()
    jump ch30_visual_skip
    return

label hide_images_psr:
    hide e_rock
    hide e_paper
    hide e_scissors
    hide e_rock_1
    hide e_paper_1
    hide e_scissors_1
    $ rps_your_choice = 0
    call screen PSR_mg
    return

label extra_restore_bg(label="ch30_visual_skip"):
    python:
        mas_extra_location(locate=False)
        disable_button_zoom()
        HKBHideButtons()
    hide monika
    scene black
    with dissolve
    pause 2.0
    call spaceroom(scene_change=True)
    python:
        HKBShowButtons()
        renpy.jump(label)
    return

#===========================================================================================
# Label
#===========================================================================================

#====Cafe

label go_to_cafe:
    python:
        check_file_status(cafe_sprite, '/game/submods/ExtraPlus/submod_assets/backgrounds')
        mas_extra_location(locate=True)
        extra_seen_background("cafe_sorry_player", "gtcafev2", "check_label_cafe")

label check_label_cafe:
    pass

label gtcafe:
    show monika 1eua at t11
    if mas_isDayNow():
        m 3sub "Хочешь сходить в кафе?"
        m 3hub "Рада это слышать, [player]!"
        m 1hubsa "Это будет очень здорово!"
        m 1hubsb "Пошли, [mas_get_player_nickname()]~"
        jump cafe_init

    elif mas_isNightNow():
        m 3sub "Ох, ты хочешь сходить в кафе?"
        m 3hub "Так мило, что ты хочешь сделать это ночью."
        m 1eubsa "Я уверена, это свидание будет замечательным!"
        m 1hubsb "Пошли [mas_get_player_nickname()]~"
        jump cafe_init
    else:
        m 1eub "В другой раз, [mas_get_player_nickname()]."
        jump screen_extraplus
    return

label gtcafev2:
    show monika 1eua at t11
    if mas_isDayNow():
        m 3wub "Хочешь сходить в кафе снова?"
        m 2hub "В прошлый раз мне так понравилось!"
        m 2eubsa "Я рада это слышать, [player]!"
        m 1hubsb "Пошли, [mas_get_player_nickname()]~"
        jump cafe_init
    elif mas_isNightNow():
        m 3wub "Ох, так ты хочешь сходить в кафе снова?"
        m 2hub "В прошлый раз было так романтично~"
        m 2eubsa "Я только рада сходить туда снова [player]!"
        m 1hubsb "Пошли [mas_get_player_nickname()]~"
        jump cafe_init
    else:
        m 1eub "В другой раз, [mas_get_player_nickname()]."
        jump screen_extraplus
    return

label cafe_talk:
    show monika staticpose at t21
    python:
        store.disable_zoom_button = True
        cafe_menu = [
            ("Как дела?", 'extra_talk_feel'),
            ("Какая у тебя главная амбиция?", 'extra_talk_ambition'),
            ("Наше общение довольно ограничено, не так ли?", 'extra_talk_you'),
            ("Какой ты видишь себя через 10 лет?", 'extra_talk_teen'),
            ("Какое у тебя самое лучшее воспоминание?", 'extra_talk_memory'),
            ("У тебя есть какие-нибудь фобии?", 'extra_talk_phobia')
        ]

        items = [
            ("Может вернёмся?", 'cafe_leave', 20),
            ("Не важно", 'to_cafe_loop', 0)
        ]
    call screen extra_gen_list(cafe_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=False)
    return

label to_cafe_loop:
    show monika staticpose at t11
    $ store.disable_zoom_button = False
    call screen dating_loop(extraplus_acs_emptyplate, extraplus_acs_emptycup, "cafe_talk", "monika_no_dessert", "monika_boopcafebeta", boop_enable=True)
    return

label cafe_leave:
    show monika 1hua at t11
    m 1eta "Ох, так ты хочешь вернуться?"
    m 1eub "Хорошо!"
    m 3hua "Но перед этим..."
    jump cafe_hide_acs

label comment_cafe:
    m 1hubsa "Спасибо за приглашение."
    m 1eubsb "Приятно проводить время вдвоем таким образом!"
    m 1eubsa "Я так рада, что встретила тебя и тому, что ты до сих пор со мной."
    m 1ekbsa "Я люблю тебя, [mas_get_player_nickname()]!"
    $ mas_DropShield_dlg()
    $ mas_ILY()
    jump ch30_visual_skip
    return

#====Restaurant====#

label go_to_restaurant:
    python:
        check_file_status(restaurant_sprite, '/game/submods/ExtraPlus/submod_assets/backgrounds')
        mas_extra_location(locate=True)
        extra_seen_background("restaurant_sorry_player", "gtrestaurantv2", "check_label_restaurant")

label check_label_restaurant:
    pass

label gtrestaurant:
    show monika 1eua at t11
    if mas_isDayNow():
        m 3sub "Ох,{w=0.3} ты хочешь сводить меня в ресторан?"
        m 3hub "Я так рада это слышать,{w=0.3} [player]!"
        m "Это очень мило с твоей стороны."
        if mas_anni.isAnni():
            m "Ещё и на нашу годовщину,{w=0.3} в такой день, [player]~!"
            $ persistent._extraplusr_hasplayergoneonanniversary == True
        m 1hubsa "Это будет замечательно!"
        m 1hubsb "Хорошо,{w=0.3} пошли [mas_get_player_nickname()]~"
        jump restaurant_init

    elif mas_isNightNow():
        m 3sub "Ох,{w=0.3} ты хочешь сводить меня в ресторан?"
        m "Это так мило с твоей стороны."
        if mas_anni.isAnni():
            m "Ещё и на нашу годовщину,{w=0.3} в такой день [player]~!"
            $ persistent._extraplusr_hasplayergoneonanniversary == True
        m 1hubsb "Пошли [mas_get_player_nickname()]~"
        jump restaurant_init
    else:
        m 1eub "В другой раз,{w=0.3} [mas_get_player_nickname()]."
        jump screen_extraplus
    return

label gtrestaurantv2:
    show monika 1eua at t11
    if mas_isDayNow():
        m 3wub "Ох, так ты хочешь сводить меня в ресторан снова?"
        if persistent._extraplusr_hasplayergoneonanniversary == True:
            m "Ммм~ Я всё ещё думаю о том, как ты сводил меня туда в нашу годовщину,"
            extend " Я думаю это было так романтично~"
            m "Так что, я рада что мы идём туда вновь~!"
        else: 
            m 2hub "В прошлый раз мне было очень весело!"
            m 2eubsa "Я так рада, [player]!"
        m 1hubsb "Пошли [mas_get_player_nickname()]~"
        jump restaurant_init

    elif mas_isNightNow():
        m 3wub "Ох, так ты хочешь сходить в ресторан снова?"
        if persistent._extraplusr_hasplayergoneonanniversary == True:
            m "Ммм~{w=0.3} Я всё ещё думаю о том, как ты сводил меня туда в нашу годовщину,"
            extend "Ты правда знаешь как сделать эту ночь замечательной!"
            m "Так что, я рада сходить туда вновь~!"
        else: 
            m 2hub "В прошлый раз это было так романтично~"
            m 2eubsa "Так что, я рада сходить туда вновь [player]!"
        m 1hubsb "Пошли [mas_get_player_nickname()]~"
        jump restaurant_init
    else:
        m 1eub "В другой раз, [mas_get_player_nickname()]."
        jump screen_extraplus
    return

label restaurant_talk:
    show monika staticpose at t21
    python:
        store.disable_zoom_button = True
        restaurant_menu = [
            ("Как твои дела, [m_name]?", 'extra_talk_doing'),
            ("Где бы ты хотела жить?", 'extra_talk_live'),
            ("Что бы ты поменяла в самой себе?", 'extra_talk_change'),
            ("Если бы ты была супер героем, какой силой ты бы обладала?", 'extra_talk_superhero'),
            ("Какой твой девиз по жизни?", 'extra_talk_motto'),
            ("Без чего ты бы не прожила ни дня?", 'extra_talk_without'),
            ("Как думаешь, стакан наполовину полон или пуст?", 'extra_talk_glass'),
            ("Что раздражает тебя больше всего?", 'extra_talk_annoy'),
            ("Опиши себя в трёх словах.", 'extra_talk_3words'),
            ("Что первое призодит людям в голову при мысли о тебе?", 'extra_talk_pop'),
            ("Каким животным ты бы была?", 'extra_talk_animal'),
        ]

        items = [
            ("Может вернёмся?", 'restaurant_leave', 20),
            ("Не важно", 'to_restaurant_loop', 0)
        ]
    call screen extra_gen_list(restaurant_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=False)
    return

label to_restaurant_loop:
    show monika staticpose at t11
    $ store.disable_zoom_button = False
    call screen dating_loop(extraplus_acs_pudding, extraplus_acs_icecream, "restaurant_talk", "monika_no_food", "monika_booprestaurantbeta", boop_enable=True)
    return

label restaurant_leave:
    show monika 1hua at t11
    m 1eta "Ох,{w=0.3} ты хочешь уйти?"
    m 1eub "Хорошо!"
    m 3hua "Но перед этим..."
    jump restaurant_hide_acs

#===========================================================================================
# Others
#===========================================================================================
#====Cafe====#

label monika_no_dessert:
    show monika staticpose at t11
    if monika_chr.is_wearing_acs(extraplus_acs_fruitcake):
        python:
            monika_chr.remove_acs(extraplus_acs_fruitcake)
            monika_chr.wear_acs(extraplus_acs_emptyplate)
        m 1hua "Так, я съела свой фруктовый пирог."
        m 1eub "Мне очень понравилось~"
    elif monika_chr.is_wearing_acs(extraplus_acs_chocolatecake):
        python:
            monika_chr.remove_acs(extraplus_acs_chocolatecake)
            monika_chr.wear_acs(extraplus_acs_emptyplate)
        m 1hua "Так, я съела свой шоколадный торт."
        m 1sua "Он был таким сладким~"
    if monika_chr.is_wearing_acs(extraplus_acs_coffeecup):
        python:
            monika_chr.remove_acs(extraplus_acs_coffeecup)
            monika_chr.wear_acs(extraplus_acs_emptycup)
        m 3dub "Кофе, кстати, тоже был хорош."
    if dessert_player == True:
        m 1etb "А ты доел свой десерт?{nw}"
        $ _history_list.pop()
        menu:
            m "А ты доел свой десерт?{fast}"
            "Да":
                m 1hubsa "{do_giggle}Э-хе-хе~"
                m 1hubsb "Надеюсь тебе понравилось!"
            "Пока нет":
                m 1eubsa "Хорошо, не спеши."
                m 1eubsb "Я подожду~"
    else:
        m 1ekc "Ты сказал мне не волноваться об этом."
        m 1ekb "Но, я надеюсь, что у тебя была чашка кофе."
    m 1hua "Дай знать если захочешь вернуться."
    jump to_cafe_loop
    return

label cafe_hide_acs:
    #Code inspired by YandereDev
    if monika_chr.is_wearing_acs(extraplus_acs_fruitcake):
        if monika_chr.is_wearing_acs(extraplus_acs_coffeecup) or monika_chr.is_wearing_acs(extraplus_acs_emptycup):
            m 3eub "Мне нужно убрать это подальше."
            m 3eub "К тому же, я должна убрать эту чашку, скоро вернусь."
            python:
                monika_chr.remove_acs(extraplus_acs_fruitcake)
                monika_chr.remove_acs(extraplus_acs_coffeecup)
                monika_chr.remove_acs(extraplus_acs_emptycup)
        else:
            m 3eub "Мне нужно убрать это подальше, скоро вернусь."
            $ monika_chr.remove_acs(extraplus_acs_fruitcake)

    elif monika_chr.is_wearing_acs(extraplus_acs_chocolatecake):
        if monika_chr.is_wearing_acs(extraplus_acs_coffeecup) or monika_chr.is_wearing_acs(extraplus_acs_emptycup):
            m 3eua "Я должна убрать этот торт подальше."
            m 3eua "К тому же, я должна убрать эту чашку, скоро вернусь."
            python:
                monika_chr.remove_acs(extraplus_acs_chocolatecake)
                monika_chr.remove_acs(extraplus_acs_coffeecup)
                monika_chr.remove_acs(extraplus_acs_emptycup)
        else:
            m 3eua "Я должна убрать этот торт подальше, скоро буду."
            $ monika_chr.remove_acs(extraplus_acs_chocolatecake)

    elif monika_chr.is_wearing_acs(extraplus_acs_emptyplate):
        if monika_chr.is_wearing_acs(extraplus_acs_coffeecup) or monika_chr.is_wearing_acs(extraplus_acs_emptycup):
            m 3hua "Мне нужно убрать это."
            m 3hua "К тому же, я должна убрать эту чашку, скоро вернусь."
            python:
                monika_chr.remove_acs(extraplus_acs_emptyplate)
                monika_chr.remove_acs(extraplus_acs_coffeecup)
                monika_chr.remove_acs(extraplus_acs_emptycup)
        else:
            m 3hua "Мне нужно убрать это, подожди пару секунд."
            $ monika_chr.remove_acs(extraplus_acs_emptyplate)

    call mas_transition_to_emptydesk
    pause 2.0
    call mas_transition_from_emptydesk("monika 1eua")
    m 1hua "Хорошо, пошли, [player]!"
    call extra_restore_bg("comment_cafe")
    return

#====Restaurant====#

label monika_no_food:
    show monika staticpose at t11
    if monika_chr.is_wearing_acs(extraplus_acs_pasta):
        python:
            monika_chr.remove_acs(extraplus_acs_pasta)
            monika_chr.wear_acs(extraplus_acs_remptyplate)
        m 1hua "Так, я съела свою пасту."
        m 1eub "Это было очень вкусно~"
        m "Я схожу за десертом. Скоро буду!"
        $ monika_chr.remove_acs(extraplus_acs_remptyplate)
        call mas_transition_to_emptydesk
        pause 2.0
        $ monika_chr.wear_acs(extraplus_acs_icecream)
        call mas_transition_from_emptydesk("monika 1eua")

    elif monika_chr.is_wearing_acs(extraplus_acs_pancakes):
        python:
            monika_chr.remove_acs(extraplus_acs_pancakes)
            monika_chr.wear_acs(extraplus_acs_remptyplate)
        m 1hua "Так, я доела панкейки."
        m 1sua "Они были такие вкусные~"
        m "Я схожу за десертом. Скоро буду!"
        $ monika_chr.remove_acs(extraplus_acs_remptyplate)
        call mas_transition_to_emptydesk
        pause 2.0
        $ monika_chr.wear_acs(extraplus_acs_pudding)
        call mas_transition_from_emptydesk("monika 1eua")

    elif monika_chr.is_wearing_acs(extraplus_acs_waffles):
        python:
            monika_chr.remove_acs(extraplus_acs_waffles)
            monika_chr.wear_acs(extraplus_acs_remptyplate)
        m 1hua "Так, я съела свои вафли."
        m 1sua "Они были невероятно вкусные~"
        m "Я схожу за десертом. Скоро буду!"
        $ monika_chr.remove_acs(extraplus_acs_remptyplate)
        call mas_transition_to_emptydesk
        pause 2.0
        $ monika_chr.wear_acs(extraplus_acs_pudding)
        call mas_transition_from_emptydesk("monika 1eua")

    if food_player == True:
        m 1etb "Кстати, а ты доел свою еду?{nw}"
        $ _history_list.pop()
        menu:
            m "Кстати, а ты доел свою еду?{fast}"
            "Да":
                m 1hubsa "{do_giggle}Э-хе-хе~"
                m 1hubsb "Надеюсь тебе понравилось!"
            "Ещё нет":
                m 1eubsa "Всё хорошо, не спеши."
                m 1eubsb "Я подожду~"
    else:
        m 1ekc "Ты говорил мне не беспокоится."
        m 1ekb "По крайней мере, я надеюсь, что у тебя есть напиток."
    m 1hua "Дай знать, если захочешь вернуться."
    jump to_restaurant_loop
    return

label restaurant_hide_acs:
    #Code inspired by YandereDev
    if monika_chr.is_wearing_acs(extraplus_acs_candles):
        if monika_chr.is_wearing_acs(extraplus_acs_pasta) or monika_chr.is_wearing_acs(extraplus_acs_icecream):
            m 3eub "Мне нужно убрать эти свечи."
            m "Нельзя недооценить опасность огня!"
            m 3eub "Также, мне необходимо убрать тарелку подальше."
            python:
                monika_chr.remove_acs(extraplus_acs_candles)
                monika_chr.remove_acs(extraplus_acs_pasta)
                monika_chr.remove_acs(extraplus_acs_icecream)

        else:
            m 3eub "Мне нужно убрать эти свечи."
            m "Нельзя недооценить опасность огня!"
            $ monika_chr.remove_acs(extraplus_acs_candles)

    elif monika_chr.is_wearing_acs(extraplus_acs_flowers):
        m 3eua "Сейчас, я уберу эти цветы."
        python:
            monika_chr.remove_acs(extraplus_acs_flowers)

    elif not monika_chr.is_wearing_acs(extraplus_acs_flowers):
        if monika_chr.is_wearing_acs(extraplus_acs_pancakes) or monika_chr.is_wearing_acs(extraplus_acs_pudding) or monika_chr.is_wearing_acs(extraplus_acs_waffles):
            m 3eua "Я должна убрать эту тарелку."
            python:
                monika_chr.remove_acs(extraplus_acs_waffles)
                monika_chr.remove_acs(extraplus_acs_pancakes)
                monika_chr.remove_acs(extraplus_acs_pudding)

    call mas_transition_to_emptydesk
    pause 2.0
    call mas_transition_from_emptydesk("monika 1eua")
    m 1hua "Хорошо, пошли, [player]!"
    call extra_restore_bg
    return


################################################################################
## MENUS
################################################################################

label plus_walk:
    show monika idle at t21
    python:
        walk_menu = [
            ("Кафе", 'go_to_cafe'),
            ("Ресторан", 'go_to_restaurant')
        ]
        store.disable_zoom_button = True
        m_talk = renpy.substitute(renpy.random.choice(date_talk))
        renpy.say(m, m_talk, interact=False)
        items = [
            ("Не важно", 'screen_extraplus', 20)
        ]
    call screen extra_gen_list(walk_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return

label plus_minigames:
    show monika idle at t21
    python:
        global ttt
        minigames_menu = [
            minigames("Игра в наперстки", 'minigame_sg', None),
            minigames("Камень, ножницы, бумага", 'minigame_psr', None)
        ]
        ttt = minigames("Крестики-нолики", 'minigame_ttt', ttt_prep)
        minigames_menu.append(ttt)
        
        store.disable_zoom_button = True
        m_talk = renpy.substitute(renpy.random.choice(minigames_talk))
        renpy.say(m, m_talk, interact=False)
        items = [
            ("Не важно", 'screen_extraplus', 20)
        ]
    call screen extra_gen_list(minigames_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return

label plus_tools:
    show monika idle at t21
    python:
        tools_menu = [
           #("Уровень привязанности", 'aff_log'),
           #("Редактор подарков", 'plus_make_gift'), #Предать анафеме эту кнопочку
            ("Поменять имя окна", 'extra_window_title'),
           #("[m_name], я хочу сделать сохранение", 'mas_backup'),
            ("[m_name], можешь подкинуть монетку?", 'coinflip')
            
        ]
        if renpy.has_screen("chibika_chill") and os.path.exists(renpy.config.basedir + "/game/submods/ExtraPlus/submod_assets/sprites/accessories/0/"):
            tools_menu.append(("Привет, [player]!", 'extra_dev_mode'))
        store.disable_zoom_button = True
        items = [
          #("Github Repository", 'github_submod', 20),
            ("Не важно", 'screen_extraplus', 0)
        ]
    call screen extra_gen_list(tools_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return

################################################################################
## GIFTS
################################################################################

label plus_make_gift:
    show monika idle at t21
    python:
        gift_menu = [
            ("Кастомизированный подарок", 'plus_make_file'),
            ("Продукты", 'plus_groceries'),
            ("Объекты", 'plus_objects'),
            ("Ленточки", 'plus_ribbons')
        ]

        items = [
            ("Не важно", 'plus_tools', 20)
        ]
    call screen extra_gen_list(gift_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return

label plus_make_file:
    show monika idle at t11

    python:
        makegift = mas_input(
            prompt=("Enter the name of the gift."),
            allow=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789",
            screen_kwargs={"use_return_button": True, "return_button_value": "cancel"},
        )

        if not makegift:
            renpy.jump("plus_make_file")
        elif makegift == "cancel":
            renpy.jump("plus_make_gift")
        else:
            filepath = os.path.join(renpy.config.basedir, 'characters', makegift + ".gift")
            with open(filepath, "a"):
                pass  # just create an empty file
            renpy.notify("Has been successfully created.")
            renpy.jump("plus_make_gift")
            
    return

label plus_groceries:
    show monika idle at t21
    python:
        groceries_menu = [
            extra_gift("Coffee", 'coffee.gift'),
            extra_gift("Chocolates", 'chocolates.gift'),
            extra_gift("Cupcake", 'cupcake.gift'),
            extra_gift("Fudge", 'fudge.gift'),
            extra_gift("Hot Chocolate", 'hotchocolate.gift'),
            extra_gift("Candy", 'candy.gift'),
            extra_gift("Candy Canes", 'candycane.gift'),
            extra_gift("Candy Corn", 'candycorn.gift'),
            extra_gift("Christmas Cookies", 'christmascookies.gift')
        ]

        items = [
            ("Nevermind", 'plus_make_gift', 20)
        ]
    call screen extra_gen_list(groceries_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return

label plus_objects:
    show monika idle at t21
    python:
        objects_menu = [
            extra_gift("Promise Ring", 'promisering.gift'),
            extra_gift("Roses", 'roses.gift'),
            extra_gift("Quetzal Plushie", 'quetzalplushie.gift'),
            extra_gift("Thermos Mug", 'justmonikathermos.gift')
        ]

        items = [
            ("Nevermind", 'plus_make_gift', 20)
        ]
    call screen extra_gen_list(objects_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return
            
label plus_ribbons:
    show monika idle at t21
    python:
        ribbons_menu = [
            extra_gift("Black Ribbon", 'blackribbon.gift'),
            extra_gift("Blue Ribbon", 'blueribbon.gift'),
            extra_gift("Dark Purple Ribbon", 'darkpurpleribbon.gift'),
            extra_gift("Emerald Ribbon", 'emeraldribbon.gift'),
            extra_gift("Gray Ribbon", 'grayribbon.gift'),
            extra_gift("Green Ribbon", 'greenribbon.gift'),
            extra_gift("Light Purple Ribbon", 'lightpurpleribbon.gift'),
            extra_gift("Peach Ribbon", 'peachribbon.gift'),
            extra_gift("Pink Ribbon", 'pinkribbon.gift'),
            extra_gift("Platinum Ribbon", 'platinumribbon.gift'),
            extra_gift("Red Ribbon", 'redribbon.gift'),
            extra_gift("Ruby Ribbon", 'rubyribbon.gift'),
            extra_gift("Sapphire Ribbon", 'sapphireribbon.gift'),
            extra_gift("Silver Ribbon", 'silverribbon.gift'),
            extra_gift("Teal Ribbon", 'tealribbon.gift'),
            extra_gift("Yellow Ribbon", 'yellowribbon.gift')
        ]

        items = [
            ("Nevermind", 'plus_make_gift', 20)
        ]
    call screen extra_gen_list(ribbons_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, items, close=True)
    return