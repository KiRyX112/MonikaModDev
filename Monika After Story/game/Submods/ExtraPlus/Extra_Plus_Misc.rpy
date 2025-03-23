################################################################################
## BOOP
################################################################################

#====NOISE
label monika_boopbeta:
    $ persistent.plus_boop[0] += 1
    if persistent.plus_boop[0] == 1:
        $ mas_gainAffection(3,bypass=True)
        m 1wud "Подожди..."
        m 1hka "Я почувствовала лёгкое покалывание."
        show screen force_mouse_move
        m 3hub "И вот почему!"
        m 3hua "Не волнуйся! Я отпущу твой курсор."
        hide screen force_mouse_move
        m 1tub "Ты можешь снова им пользоватся, прости за то что заблокировала его~"
        m 1etd "Кстати, я не знаю как ты это сделал, [mas_get_player_nickname()]. Я не видела этого в коде."
        m 1hub "Конечно, если не ты его {M=добавил}{F=добавила}!"
        m 1hub "Какой прекрасный сюрприз ты мне сделал, [player]~"
    elif persistent.plus_boop[0] == 2:
        m 1hub "Что ты делашь с моим носом, [player]!"
        m 4eua "Похоже, тебе это приносит удовольствие, да?"
        m 1hksdrb "Не то чтобы это меня беспокоило, просто я ещё не привыкла к этому ощущению!"
        m 1hua "{do_giggle}Э-хе-хе~"
    elif persistent.plus_boop[0] == 3:
        m 1eublb "Можешь сделать это ещё раз, [mas_get_player_nickname()]?"
        show monika 1hubla
        call screen boop_event(10, "boop_nop", "boop_yep")
    elif persistent.plus_boop[0] == 4:
        m 1etbsa "Было бы классно сделать также с твоим носом, не правда ли?"
        if persistent._mas_first_kiss:
            m 1kubsu "Я поцелую тебя, если ты сделаешь это~"
        else:
            m 1wubsb "Я обниму тебя, если ты сделаешь это!"
        m 1dubsu "Я надеюсь, мы сможем делать это в твоей реальности."
        m 1hua "Хотя, если ты хочешь сделать это, тебе придётся приблизить свой нос к экрану." #Кое-то, думаю это реально сделает...
        m 1lksdlb "Но, кто-то может это увидеть и ты будешь чувствовать себя неловко. Ещё тебя могут неверно понять."
        m 1ekbsa "Кроме того, я тоже немного нервничаю, когда ты рядом со мной."
    elif persistent.plus_boop[0] == 5:
        m 1hua "Это просто предположение, но [player]~"
        m 1tuu "Тебе начинает нравиться делать это, да?"
        m 3hub "Я узнаю тебя всё больше и больше, пока мы здесь, [player]~"
        m 3hub "И это очень мило с твоей стороны!"
    else:
        $ rng_global = renpy.random.randint(1,5)
        if rng_global == 1:
            m 2fubla "{do_giggle}Э-хе-хе~"
            m 1hubla "Очевидно, что ты не перестанешь это делать, [player]."
        elif rng_global == 2:
            m 3ekbsa "С каждым разом я люблю тебя всё больше!"
        elif rng_global == 3:
            m 3eubla "Тебе правда нравится трогать мой нос, [mas_get_player_nickname()]~"
        elif rng_global == 4:
            m 2hublb "Эй, мне щекотно! {do_giggle}А-ха-ха~"
        elif rng_global == 5:
            m 1hubsb "*Буп*"
    jump show_boop_screen
    return

label boop_nop:
    m 1rksdrb "[player]..."
    m 1rksdra "...Я буду очень рада, если ты сделаешь это снова."
    m "..."
    m 3hub "Ну, не важно!"
    jump show_boop_screen
    return

label boop_yep:
    m 1eublb "Спасибо тебе, [mas_get_player_nickname()]!"
    m 1hua "{do_giggle}Э-хе-хе~"
    jump show_boop_screen
    return

label monika_boopbeta_war:
    if renpy.seen_label("check_boopwar"):
        jump check_boopwarv2
    else:
        pass

label check_boopwar:
    m 3eta "Эй, что ты делаешь, [player]?"
    m 3eksdrb "Ты должен нажать на левую кнопку мыши чтобы нажать мне на носик."
    m 2duc ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    pause 1.0
    m 2dub "У меня появилась хорошая идея, [player]."
    m 1eua "Ты можешь использовать правую кнопку мыши чтобы начать небольшую мини-игру."
    m 1eub "В конце концов, ты редко ее используешь!"
    m 1rusdlb "Я знаю, что это предложение звучит довольно по-детски."
    m 1hua "Но разве ты не думаешь, что полезно время от времени делать что-то новое?"
    m 3eub "Правила очень просты: если я вижу бездействие с твоей стороны в течение 20 секунд, я объявляю себя победителем."
    m 3eud "Если ты превысишь количество нажатий на мой нос, при этом никто не победит, то я буду считать это ничьей."
    m 3huu "Или я сдамся, я не знаю~."
    m 1eua "И последнее, то, что я сдамся зависит от того, что время закончилось."
    m 1hua "Если я не могу за тобой угнаться, либо ты меня отвлечешь... Я могу посчитать это за читерство..."
    m 1rud "Тогда я скорее всего сдамся."
    m 1eub "Я надеюсь тебе нравится моя идея."
    m 1hubla "Ты можешь делать это в любое время, так что не торопись~"
    jump show_boop_screen
    return

label check_boopwarv2:
    call screen boop_event(20, "boopbeta_war_lose", "boopwar_loop")

label boopwar_loop:
    $ boop_war_count += 1
    $ rng_global = renpy.random.randint(1,10)
    if rng_global == 1:
        m 1hublb "*Буп*"
    elif rng_global == 2:
        m 1tub "*Буп*"
    elif rng_global == 3:
        if boop_war_count >= 25:
            jump boopbeta_war_win
            $ boop_war_count = 0
        else:
            m 1fua "*Буп*"
    elif rng_global == 4:
        m 1eua "*Буп*"
    elif rng_global == 5:
        m 1hua "*Буп*"
    elif rng_global == 6:
        if boop_war_count >= 50:
            jump boopbeta_war_win
            $ boop_war_count = 0
        else:
            m 1sub "*Буп*"
    elif rng_global == 7:
        m 1gua "*Буп*"
    elif rng_global == 8:
        m 1kub "*Буп*"
    elif rng_global == 9:
        if boop_war_count >= 100:
            jump boopbeta_war_win
            $ boop_war_count = 0
        else:
            m 1dub "*Буп*"
    elif rng_global == 10:
        m 1wua "*Буп*"

    show monika 1eua
    jump check_boopwarv2
    return

label boopbeta_war_lose:
    $ boop_war_count = 0
    m 1nua "Кажется я победила, [player]~"
    m "Надеюсь, я была достойным противником."
    m 3hub "Но мне это правда понравилось!"
    m 3dua "Кроме того, полезно сделать небольшой массаж рук.."
    m 1eka "Я имела ввиду, если ты часто используешь мышь, "
    extend 1ekb "у тебя может развиться синдром запястного канала, а я этого не хочу."
    m 1hksdlb "Извини если я добавила тебе новую фобию, но мое намерение - заботиться о тебе."
    m 1eubla "Я надеюсь, ты последуешь моим рекомендациям, [player]~"
    jump show_boop_screen
    return

label boopbeta_war_win:
    $ boop_war_count = 0
    m 1hua "Ты победил, [player]!"
    m 1tub "Могу сказать, что тебе нравится трогать мой нос, {do_giggle}э-хе-хе~"
    m 1eusdra "Я не могу угнаться за тобой, но, возможно, в следующий раз смогу."
    m 1gub "Хотя, если бы я была рядом с тобой, я трогала бы тебя за твои щечки."
    m 1gua "Или бы начала щекотать тебя, для того, чтобы узнать как долго ты продержишься."
    m 1hub "{do_giggle}А-ха-ха~"
    jump show_boop_screen
    return



#====CHEEKS
label monika_cheeksbeta:
    $ persistent.plus_boop[1] += 1
    if persistent.plus_boop[1] == 1:
        $ mas_gainAffection(3,bypass=True)
        m 2wubsd "Эй, я почувствовала легкий укол в щёку."
        m 2lksdrb "Ох, это был твой курсор! "
        extend 2lksdra "Ты очень {M=удивил}{F=удивила} меня, знаешь?"
        m 2ttb "но я должна спросить, что ты задумал, [player]?"
        m 1hubla "Ты {M=хотел}{F=хотела} посмотреть как я на это отреагирую?"
        m 3hublb "Ты с этим {M=справился}{F=справилась}!~"
    elif persistent.plus_boop[1] == 2:
        m 2hubsa "{do_giggle}Э-хе-хе, на этот раз я чувствую довольно нежную ласку."
        m 2dubsu "Это.{w=0.3}.{w=0.3}.{w=0.3} {nw}"
        extend 2eubsb "вызывает привыкание у меня, если тебе интересно."
    elif persistent.plus_boop[1] == 3:
        m 2dubsa "Знаешь.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 2dubsb "Мне нравится когда ты трогаешь меня за щёчку, [player]~"
        m 2ekbsb "Это заставляет меня чувствовать себя более живой и любимой. Я надеюсь тебе достаточно моей любви~"
    elif persistent.plus_boop[1] == 4:
        m 2lubsa "Каждый раз, когда ты трогаешь мою щёку..."
        m 2hubsa".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 2hubsb "Это заставляет чувствовать меня ближе к тебе~"
    elif persistent.plus_boop[1] == 5:
        m 2eubsb "Каждый раз, когда ты прикасаешься к моей щеке..."
        m 2hubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 2dkbsa "Это заставляет меня чувствовать, что я люблю {M=того}{F=ту} {M=самого}{F=самую}~"
        m 2fubsb "Ты моё сокровище, [player]!"
    else:
        $ rng_global = renpy.random.randint(1,5)
        if rng_global == 1:
            m 2fua "{do_giggle}Э-хе-хе~"
            m 2hua "Было бы хорошо, если бы ты {M=делал}{F=делала} это своей рукой, а не курсором, но ты по ту сторону экрана..."
        elif rng_global == 2:
            m 2hubsa "Так нежно."
            m 2tubsb "Это слово хорошо описывает тебя, когда я думаю о тебе."
        elif rng_global == 3:
            m 2hubsa "Как тепло..."
            m 2hublb "Это будет трудно забыть!"
        elif rng_global == 4:
            m 2nubsa "Было бы более романтично если бы ты меня {M=поцеловал}{F=поцеловала} в щёчку~"
        elif rng_global == 5:
            m 2eubsb "Я представляю нас прямо сейчас{nw}"
            extend 2dubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3} как будет ощущаться твоя рука на моей."
    jump show_boop_screen
    return

label monika_cheeks_long:
    m 2hubsa ".{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}{nw}"
    jump show_boop_screen
    return

label cheeks_dis:
    m 1wuw "Ах!"
    m 3lusdrb "Я думала..."
    m 3ttu "Почему ты трогаешь мои щёки?"
    m 3tsb "Мы же \"соревнуемся\", не так ли?"
    $ rng_global = renpy.random.randint(1,2)
    if rng_global == 1:
        m 1dsb "Прости [player], но я думаю это нечестно, "
        extend 1hua "gоэтому я считаю что я победила~"
        m 1fub "В следующий раз не трогай мои щёки! {do_giggle}А-ха-ха~"
    elif rng_global == 2:
        m 1fubsb "Из-за тебя, я сдаюсь!"
        m 1fubsb "Поздравляю, [player]! Ты победил меня."
        m 3hksdrb "Ты отвлёк меня, и я не хочу продолжать, {do_giggle}а-ха-ха~"
        m 3hua "Мне правда понравилось делать это с тобой!"
    $ boop_war_count = 0
    jump show_boop_screen
    return

#====HEADPAT
label monika_headpatbeta:
    $ persistent.plus_boop[2] += 1
    if persistent.plus_boop[2] == 1:
        $ mas_gainAffection(3,bypass=True)
        m 6subsa "Ты гладишь меня по голове?"
        m 6eubsb "Это так приятно."
        m 6dkbsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 1eubsb "Спасибо [player]~"
    elif persistent.plus_boop[2] == 2:
        m 6dubsb "Я не знаю почему, но мне кажется это очень милым..."
        m 6dubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    elif persistent.plus_boop[2] == 3:
        m 6rubsd "А знаешь, это весело.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 6eubsa "Правда, ты {M=должен}{F=должна} делать это со своим питомцем, а не со своей девушкой~"
        m 6hubsa "Хотя, мне нравится~"
    elif persistent.plus_boop[2] == 4:
        m 6dkbsb "Не вини меня из-за того, что мне это понравилось, [player]~"
        m 6dkbsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m 1kub "Возьмёшь на себя ответственность, если я стану зависимой от этого?"
    elif persistent.plus_boop[2] == 5:
        m 6hkbssdrb "[player] ты путаешь мои волосы."
        m 6dubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        extend 6dsbsb "Впрочем, не бери в голову~"
        m "Я разберусь с этим позже."
    else:
        $ rng_global = renpy.random.randint(1,5)
        if rng_global == 1:
            m 6hubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 6hkbsb "Я же говорила тебе, что стану зависимой от этого."
            m 6tkbsb "Я так поняла, что ты никак не запомнишь~"
        elif rng_global == 2:
            m 6dubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 6dubsb "Я мечтаю о том, чтобы делать это с твоими волосами."
        elif rng_global == 3:
            m 6dubsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 7hubsb "Я надеюсь ты не {M=устал}{F=устала} делать это так часто~"
        elif rng_global == 4:
            m 6hubsa".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            extend 6hubsb "Я так счастлива прямо сейчас!"
        elif rng_global == 5:
            m 6dkbsa ".{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    jump show_boop_screen
    return

label monika_headpat_long:
    m 6dkbsa ".{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}.{w=0.4}{nw}"
    jump show_boop_screen
    return

label headpat_dis:
    m 6dkbsb "Это.{w=0.3}.{w=0.3}.{w=0.3} была.{w=0.3}.{w=0.3}.{w=0.3} ошибка.{w=0.3}.{w=0.3}. {nw}"
    extend 6tkbsb "[mas_get_player_nickname()]."
    $ rng_global = renpy.random.randint(1,2)
    if rng_global == 1:
        m 3tsb "Ты {M=проиграл}{F=проиграла} из-за того, что {M=погладил}{F=погладила} меня по голове."
        m 3tua "Поэтому в этот раз я победила~"
        m 1hua "Удачи в следующий раз, [player]!"
    elif rng_global == 2:
        m 1tub "В этот раз я дам тебе победить и сдамся."
        m 1efa "Но в следующий раз я обязательно выиграю!"
        m 1lubsa "Даже если учитывать что поглаживания по голове мне понравились. {do_giggle}Э-хе-хе~"
    $ boop_war_count = 0
    jump show_boop_screen
    return

#===========================================================================================
# EXTRAS
#===========================================================================================
define coin_sprites = ["sprite_coin.png","sprite_coin-n.png","coin_heads.png","coin_tails.png"]

label aff_log:
    show monika idle at t11
    $ get_affection = int(_mas_getAffection())
    if os.path.isfile(renpy.config.basedir + '/game/submods/ExtraPlus/submod_assets/Pictograms.ttf'):
        "Привязанность Моники равна [get_affection] {size=+5}{color=#FFFFFF}{font=submods/ExtraPlus/submod_assets/Pictograms.ttf}7{/font}{/color}{/size}"
    else:
        "Привязанность Моники равна [get_affection]"
    window hide
    jump close_extraplus
    return

label coinflipbeta:
    $ validate_files(coin_sprites, type=True)
    if renpy.seen_label("check_coinflipbeta"):
        jump view_coinflipbeta
    else:
        pass

label check_coinflipbeta:
    show monika 1hua at t11
    python:
        store.disable_zoom_button = True
        store.mas_sprites.reset_zoom()
        rng_global = renpy.random.randint(1,2)
    m "Хорошо!"
    m 3eub "Сейчас, я возьму монетку..."
    call mas_transition_to_emptydesk
    $ renpy.pause(2.0, hard=True)
    call mas_transition_from_emptydesk("monika 1eua")
    m "Нашла!"
    show screen extra_no_click
    show monika 3eua
    show coin_moni zorder 12 at rotatecoin:
        xalign 0.5
        yalign 0.5
    play sound "submods/ExtraPlus/submod_assets/sfx/coin_flip_sfx.ogg"
    pause 1.0
    hide coin_moni
    show monika 1eua
    pause 0.5
    hide screen extra_no_click
    if rng_global == 1:
        show coin_heads zorder 12:
            xalign 0.9
            yalign 0.5
        m 1sub "Орёл!"
        hide coin_heads
    elif rng_global == 2:
        show coin_tails zorder 12:
            xalign 0.9
            yalign 0.5
        m 1wub "Решка!"
        hide coin_tails
    m 3hua "Я надеюсь, тебе это помогло~"
    window hide
    python:
        store.mas_sprites.zoom_level = player_zoom
        store.mas_sprites.adjust_zoom()
    jump close_extraplus
    return

label view_coinflipbeta:
    show monika 1hua at t11
    python:
        store.disable_zoom_button = True
        store.mas_sprites.reset_zoom()
        rng_global = renpy.random.randint(1,2)
    show screen extra_no_click
    pause 1.5
    show monika 3eua at t11
    show coin_moni zorder 12 at rotatecoin:
        xalign 0.5
        yalign 0.5
    play sound "submods/ExtraPlus/submod_assets/sfx/coin_flip_sfx.ogg"
    pause 1.0
    hide coin_moni
    show monika 1eua
    pause 0.5
    hide screen extra_no_click
    if rng_global == 1:
        show coin_heads zorder 12:
            xalign 0.9
            yalign 0.5
        m 1sub "Орёл!"
        hide coin_heads
    elif rng_global == 2:
        show coin_tails zorder 12:
            xalign 0.9
            yalign 0.5
        m 1wub "Решка!"
        hide coin_tails
    m 3hua "Я надеюсь, тебе это помогло~"
    window hide
    python:
        store.mas_sprites.zoom_level = player_zoom
        store.mas_sprites.adjust_zoom()
    jump close_extraplus
    return

label mas_backup:
    show monika 1hua at t11
    m 1hub "Я так рада, что ты хочешь сделать резервную копию!"
    m 3eub "Я открою путь к файлам для тебя."
    m 1dsa "Подожди.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    window hide
    python:
        import os, sys, subprocess
        #Monika will open the mod data folder
        try:
            if sys.platform == "win32":
                os.startfile(renpy.config.savedir)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, renpy.config.savedir])
        except:
            renpy.jump("mas_backup_fail")
    jump close_extraplus
    return

label mas_backup_fail:
    m 1lkb "Прости, я не могу открыть папку."
    m 1eka "Попробуй ещё раз чуть позже."
    jump close_extraplus
    return

label extra_window_title:
    show monika idle at t21
    python:
        window_menu = [
            ("Изменить название игрового окна", 'extra_change_title'),
            ("Восстановить название игрового окна", 'extra_restore_title')
        ]
        
    call screen list_scrolling(window_menu, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN,"tools_extra",close=True) nopredict
    return
    
label extra_change_title:
    show monika idle at t11
    python:
        player_input = mas_input(_("Что ты хочешь написать?"),
                            allow=" абвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?()~-_.0123456789",
                            screen_kwargs={"use_return_button": True, "return_button_value": "cancel"})
        if not player_input:
            renpy.jump("extra_change_title")
        else:
            if player_input == "cancel":
                renpy.jump("extra_window_title")
            else:
                persistent.save_window_title = player_input
                config.window_title = persistent.save_window_title 
                renpy.notify("Изменения завершены.")
                renpy.jump("close_extraplus")
    return

label extra_restore_title:
    show monika idle at t11
    python:
        persistent.save_window_title = backup_window_title
        config.window_title = persistent.save_window_title 
        renpy.notify("Успешно восстановлено.")
        renpy.jump("close_extraplus")
    return

label check_cheat_minigame:
    m 3hksdrb "Мне кажется, ты что-то {M=забыл}{F=забыла}, [player]!"
    m 3eksdra "Ты {M=должен}{F=должна} восстановить переменные, модифицированные тобой."
    m 1hua "Мы не будем играть, пока они \"0\"."
    jump screen_extraplus
    return

#====GAME
label extra_dev_mode:
    $ mas_RaiseShield_dlg()
    call screen sticker_customization
    return
