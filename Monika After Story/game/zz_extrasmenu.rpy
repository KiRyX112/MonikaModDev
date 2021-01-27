














init python:
    import store
    import os
    # import requests, urllib, json

    def mas_open_extra_menu():
        """
        Jumps to the extra menu workflow
        """
        if not os.path.exists(user_dir + "/game/mod_assets/extra/songs/"):
            persistent.bang_dream_songs_active = False
        else:
            persistent.bang_dream_songs_active = True

        renpy.show_screen("extra_menu")

    def mas_extra_menu_return():
        if not persistent.msr_bg_animations:
            renpy.hide("light_monika_room_day_anim")
            renpy.hide("light_monika_room_evening_anim")
            renpy.hide("light_monika_room_rain_anim")
        renpy.hide_screen("extra_menu")
        if mas_isMorning() and not mas_is_raining and persistent.msr_bg_animations:
            renpy.show("light_monika_room_day_anim", zorder=8, at_list=[bg_alpha(0.5)])
        elif not mas_isMorning() and not mas_is_raining and persistent.msr_bg_animations:
            renpy.show("light_monika_room_evening_anim", zorder=8, at_list=[bg_alpha(0.4)])
        elif mas_is_raining and persistent.msr_bg_animations:
            renpy.show("light_monika_room_rain_anim", zorder=8, at_list=[bg_alpha(0.4)])
        consonants = [u'б', u'в', u'г', u'д', u'ж', u'з', u'й', u'к', u'л', u'м', u'н', u'п', u'р', u'с', u'т', u'ф', u'х', u'ц', u'ч', u'ш', u'щ', u'ь']
        combinations = [u'жа', u'ша', u'ща', u'ца']
        combinations_abb = [u'жа', u'ша', u'ща', u'ца', u'ба', u'ва', u'ва', u'да', u'за', u'ка', u'ла', u'ма', u'на', u'па', u'ра', u'са', u'та', u'фа', u'ха', u'ча']
        combinations_special = [u'ка', u'ха']
        last_symb = player[-1]
        last_symb2 = player[-2:]
        last_symb3 = player[-3:]
        if not persistent.player_abbreviated_name:
            player_abb = player
        else:
            if persistent.playername.lower() == "артём" or persistent.playername.lower() == "артем":
                player_abb = "Тём"
            elif persistent.playername.lower() == "семён" or persistent.playername.lower() == "семен":
                player_abb = "Сём"
            elif persistent.playername.lower() == "вероника":
                player_abb = "Ника"
            elif persistent.playername.lower() == "даниил" or persistent.playername.lower() == "данил":
                player_abb = "Дань"
            elif persistent.playername.lower() == "тимофей":
                player_abb = "Тим"
            elif persistent.playername.lower() == "тимур":
                player_abb = "Тим"
            elif persistent.playername.lower() == "алексей":
                player_abb = "Лёш"
            elif persistent.playername.lower() == "максим":
                player_abb = "Макс"
            elif persistent.playername.lower() == "дмитрий":
                player_abb = "Дим"
            elif persistent.playername.lower() == "сергей":
                player_abb = "Серёж"
            elif persistent.playername.lower() == "роман":
                player_abb = "Ром"
            elif persistent.playername.lower() == "ольга":
                player_abb = "Оль"
            elif persistent.playername.lower() == "антон":
                player_abb = "Антош"
            elif persistent.playername.lower() == "михаил" or persistent.playername.lower() == "миха" or persistent.playername.lower() == "мишка":
                player_abb = "Миш"
            elif persistent.playername.lower() == "павел":
                player_abb = "Паш"
            elif persistent.playername.lower() == "пётр" or persistent.playername.lower() == "петр":
                player_abb = "Петь"
            elif persistent.playername.lower() == "кирилл":
                player_abb = "Кирь"
            elif persistent.playername.lower() == "филипп":
                player_abb = "Филь"
            elif persistent.playername.lower() == "евгений":
                player_abb = "Жень"
            elif persistent.playername.lower() == "борис":
                player_abb = "Борь"





            elif last_symb2 in combinations_abb:
                if last_symb3 != "ика":
                    player_abb = player[:len(player)-1]
            elif last_symb == u'я' and last_symb2 != u'ия' and last_symb2 != u'ая' and last_symb2 != u'уя' and last_symb2 != u'ея' and last_symb2 != u'оя' and last_symb2 != u'юя' and last_symb2 != u'ья':
                player_abb = player[:len(player)-1]+u'ь'
            elif last_symb == u'т':
                player_abb = player+u'ик'
            elif last_symb == u'м':
                player_abb = player+u'ка'
            elif last_symb == u'а':
                player_abb = player[:len(player)-1]+u'уля'
            else:
                player_abb = player





















































init -1 python in mas_extramenu:
    import store


    menu_visible = False


label mas_extra_menu_pool:
    $ store.mas_extramenu.menu_visible = True
    $ prev_zoom = store.mas_sprites.zoom_level


    $ mas_RaiseShield_core()

    if not persistent._mas_opened_extra_menu:
        call mas_extra_menu_firsttime from _call_mas_extra_menu_firsttime

    $ persistent._mas_opened_extra_menu = True

    show screen mas_extramenu_area
    jump mas_idle_loop

label mas_extra_menu_close:
    $ store.mas_extramenu.menu_visible = False
    hide screen mas_extramenu_area

    if store.mas_sprites.zoom_level != prev_zoom:
        call mas_extra_menu_zoom_callback from _call_mas_extra_menu_zoom_callback


    if store.mas_globals.in_idle_mode:
        $ mas_coreToIdleShield()
    else:
        $ mas_DropShield_core()

    show monika idle

    jump ch30_loop

label mas_idle_loop:
    pause 10.0
    $ renpy.not_infinite_loop(60)
    jump mas_idle_loop

default persistent._mas_opened_extra_menu = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_extra_menu_firsttime",
            prompt="Можешь объяснить мне работу меню инструментов?",
            category=["разное"]
        )
    )

label mas_extra_menu_firsttime:
    if not persistent._mas_opened_extra_menu:
        m 1hua "Добро пожаловать в меню инструментов, [player]!"

    $ MAS.MonikaElastic()
    m 1eua "Здесь я добавляю вещи, которые не являются какими-либо играми. Например, специальные взаимодействия, которые ты сможешь сделать с помощью мыши."


    if not persistent._mas_opened_extra_menu:
        $ MAS.MonikaElastic()
        m 1hua "Пришло время посмотреть, что же есть в этом меню!"

    $ mas_setEVLPropValues(
        "mas_extra_menu_firsttime",
        unlocked=True,
        pool=True
    )


    call mas_extra_menu_zoom_intro from _call_mas_extra_menu_zoom_intro

    return




label mas_extra_menu_zoom_intro:
    $ MAS.MonikaElastic()
    m 1eua "Одна вещь, которую я добавила — это способ для тебя настраивать твоё поле зрения, так что теперь ты сможешь сидеть ближе или дальше от меня."
    $ MAS.MonikaElastic()
    m 1eub "Ты сможешь настроить всё это с помощью ползунка в разделе «Масштаб» в меню инструментов."
    return

default persistent._mas_pm_zoomed_out = False
default persistent._mas_pm_zoomed_in = False
default persistent._mas_pm_zoomed_in_max = False

label mas_extra_menu_zoom_callback:
    $ import store.mas_sprites as mas_sprites
    $ aff_larger_than_zero = _mas_getAffection() > 0


    if mas_sprites.zoom_level < mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_out
            ):

            call mas_extra_menu_zoom_out_first_time from _call_mas_extra_menu_zoom_out_first_time
            $ persistent._mas_pm_zoomed_out = True

    elif mas_sprites.zoom_level == mas_sprites.max_zoom:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in_max
            ):

            call mas_extra_menu_zoom_in_max_first_time from _call_mas_extra_menu_zoom_in_max_first_time
            $ persistent._mas_pm_zoomed_in_max = True
            $ persistent._mas_pm_zoomed_in = True

    elif mas_sprites.zoom_level > mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in
            ):

            call mas_extra_menu_zoom_in_first_time from _call_mas_extra_menu_zoom_in_first_time
            $ persistent._mas_pm_zoomed_in = True

    return

label mas_extra_menu_zoom_out_first_time:
    $ MAS.MonikaElastic()
    m 1ttu "Надоело сидеть близко?"
    $ MAS.MonikaElastic()
    m "Или, может быть, ты просто хочешь увидеть верхнюю часть моей головы?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе~"
    return

label mas_extra_menu_zoom_in_first_time:
    $ MAS.MonikaElastic()
    m 1ttu "Хочешь присесть поближе?"
    $ MAS.MonikaElastic()
    m 1hua "Я не против."
    return

label mas_extra_menu_zoom_in_max_first_time:
    $ MAS.MonikaElastic()
    m 6wuo "[player]!"
    $ MAS.MonikaElastic()
    m 6rkbfd "Когда твоё лицо так близко..."
    $ MAS.MonikaElastic()
    m 6ekbfd "Я чувствую..."
    show monika 6hkbfa
    pause 2.0
    $ MAS.MonikaElastic()
    m 6hubfa "Тепло..."
    return

label mas_extra_menu_boop_intro:
    m 1eua "boop intro"
    return

default persistent._mas_pm_boop_stats = {}







style mas_mbs_vbox is vbox:
    spacing 0

style mas_mbs_button is generic_button_light


style mas_mbs_button_dark is generic_button_dark


style mas_mbs_button_text is generic_button_text_light

style mas_mbs_button_text_dark is generic_button_text_dark































































style mas_extra_menu_frame:
    background Frame("mod_assets/frames/trans_pink2pxborder100.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_frame_dark:
    background Frame("mod_assets/frames/trans_pink2pxborder100_d.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_label_text is hkb_button_text:
    color "#FFFFFF"

style mas_extra_menu_label_text_dark is hkb_button_text_dark:
    color "#FD5BA2"

style mas_adjust_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjustable_button is generic_button_light:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_dark is generic_button_dark:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_text is generic_button_text_light:
    kerning 0.2

style mas_adjustable_button_text_dark is generic_button_text_dark:
    kerning 0.2

screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")


        textbutton _("Закрыть"):
            area (60, 596, 120, 35)
            style "hkb_button"
            action Jump("mas_extra_menu_close")


        frame:
            area (195, 450, 80, 255)
            style "mas_extra_menu_frame"
            has vbox:
                spacing 2
            label "Зум":
                text_style "mas_extra_menu_label_text"
                xalign 0.5


            textbutton _("Сброс"):
                style "mas_adjustable_button"
                selected False
                xsize 72
                ysize 35
                xalign 0.3
                action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)


            bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                style "mas_adjust_vbar"
                xalign 0.5
            $ store.mas_sprites.adjust_zoom()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
