


init python:


    def HKBHideButtons():



        if mas_HKBIsVisible():
            config.overlay_screens.remove("hkb_overlay")
            renpy.hide_screen("hkb_overlay")


    def MSRHKBHideButtons():

        if mas_MSRHKBIsVisible():
            config.overlay_screens.remove("msr_hkb_overlay")
            renpy.hide_screen("msr_hkb_overlay")

    def HKBShowButtons():



        if not mas_HKBIsVisible():
            config.overlay_screens.append("hkb_overlay")

    def MSRHKBShowButtons():


        if not mas_MSRHKBIsVisible():
            config.overlay_screens.append("msr_hkb_overlay")


    def mas_HKBRaiseShield():
        """RUNTIME ONLY
        Disables the hotkey buttons
        """
        store.hkb_button.talk_enabled = False
        store.hkb_button.extra_enabled = False
        store.hkb_button.music_enabled = False
        store.hkb_button.play_enabled = False


    def mas_HKBDropShield():
        """RUNTIME ONLY
        Enables the hotkey buttons
        """
        store.hkb_button.talk_enabled = True
        store.hkb_button.extra_enabled = True
        store.hkb_button.music_enabled = True
        store.hkb_button.play_enabled = True


    def mas_HKBIsEnabled():
        """
        RETURNS: True if all the buttons are enabled, False otherwise
        """
        return (
            store.hkb_button.talk_enabled
            and store.hkb_button.music_enabled
            and store.hkb_button.play_enabled
            and store.hkb_button.extra_enabled
        )


    def mas_HKBIsVisible():
        """
        RETURNS: True if teh Hotkey buttons are visible, False otherwise
        """
        return "hkb_overlay" in config.overlay_screens

    def mas_MSRHKBIsVisible():
        """
        RETURNS: True if teh Hotkey buttons are visible, False otherwise
        """
        return "msr_hkb_overlay" in config.overlay_screens


    def MovieOverlayHideButtons():



        if "movie_overlay" in config.overlay_screens:
            config.overlay_screens.remove("movie_overlay")
            renpy.hide_screen("movie_overlay")


    def MovieOverlayShowButtons():



        config.overlay_screens.append("movie_overlay")


init -1 python in hkb_button:


    talk_enabled = True


    extra_enabled = True


    music_enabled = True


    play_enabled = True


    movie_buttons_enabled = False






style hkb_vbox is vbox:
    spacing 5

style hkb_button is generic_button_light:
    xysize (120, 35)
    padding (5, 5, 5, 5)

style hkb_button_dark is generic_button_dark:
    xysize (120, 35)
    padding (5, 5, 5, 5)

style hkb_button_text is generic_button_text_light:
    kerning 0.2

style hkb_button_text_dark is generic_button_text_dark:
    kerning 0.2

style hkb_big_vbox is vbox
style hkb_big_button is button
style hkb_big_button_text is button_text

style hkb_big_vbox:
    spacing 0

style hkb_big_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_idle_background_big.png"
    hover_background "mod_assets/hkb_hover_background_big.png"
    ypadding 5

    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style hkb_big_button_text is default:
    properties gui.button_text_properties("hkb_button")
    color "#000000"
    outlines []


define gui.hkb_big_dark_button_width = 120
define gui.hkb_big_dark_button_height = None
define gui.hkb_big_dark_button_tile = False

define gui.hkb_big_dark_button_text_font = gui.default_font
define gui.hkb_big_dark_button_text_size = gui.text_size
define gui.hkb_big_dark_button_text_xalign = 0.5

define gui.hkb_big_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.hkb_big_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color
define gui.hkb_big_dark_button_text_kerning = 0.2



style hkb_big_dark_vbox is vbox
style hkb_big_dark_button is button
style hkb_big_dark_button_text is button_text

style hkb_big_vbox:
    spacing 0

style hkb_big_dark_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_idle_background_big_d.png"
    hover_background "mod_assets/hkb_hover_background_big_d.png"
    ypadding 5

    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style hkb_big_dark_button_text is default:
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    outlines []
    kerning 0.2
    xalign 0.5
    yalign 0.5
    font gui.default_font
    size gui.text_size

style hkbd_big_vbox is vbox
style hkbd_big_button is button
style hkbd_big_button_text is button_text

style hkbd_big_vbox:
    spacing 0

style hkbd_big_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_disabled_background_big.png"
    hover_background "mod_assets/hkb_disabled_background_big.png"

style hkbd_big_button_text is default:

    font gui.default_font
    size gui.text_size
    idle_color "#000"
    hover_color "#000"
    kerning 0.2
    outlines []

style hkb_big_text is default:
    xalign 0.5
    size gui.text_size
    font gui.default_font
    color "#000"
    kerning 0.2
    outlines []

screen hkb_overlay():
    zorder 50

    style_prefix "hkb"

    if persistent.saveblock:
        vbox at mas_buttons_move(0.05, 685):
            xpos 0.05

            yanchor 1.0
            ypos 685


            if store.hkb_button.talk_enabled:
                textbutton _("{size=-6}Поговорить{/size}") action Function(show_dialogue_box)
            else:
                textbutton _("{size=-6}Поговорить{/size}")

            if store.hkb_button.music_enabled:
                textbutton _("{size=-6}Музыка{/size}") action Function(select_music)
            else:
                textbutton _("{size=-6}Музыка{/size}")
    
    else:
        vbox at mas_buttons_move(0.05, 715):
            xpos 0.05

            yanchor 1.0
            ypos 715


            if store.hkb_button.talk_enabled:
                textbutton _("{size=-6}Поговорить{/size}") action Function(show_dialogue_box)
            else:
                textbutton _("{size=-6}Поговорить{/size}")

            if store.hkb_button.music_enabled:
                textbutton _("{size=-6}Музыка{/size}") action Function(select_music)
            else:
                textbutton _("{size=-6}Музыка{/size}")

            if store.hkb_button.play_enabled:
                textbutton _("{size=-6}Играть{/size}") action Function(pick_game)
            else:
                textbutton _("{size=-6}Играть{/size}")

            if store.hkb_button.music_enabled:
                textbutton _("{size=-6}Экстра{/size}") action Function(mas_open_extra_menu)
            else:
                textbutton _("{size=-6}Экстра{/size}")


screen msr_hkb_overlay():

    zorder 50
    style_prefix ("hkb_big" if not mas_globals.dark_mode else "hkb_big_dark")
    if str(persistent.current_monikatopic).startswith("monika_") and not str(persistent.current_monikatopic).endswith("_select"):
        if mas_getEV(persistent.current_monikatopic).random:
            vbox at mas_buttons_move(0.85, 720):
                xpos 0.85

                yanchor 1.0
                ypos 720




                if persistent.current_monikatopic not in persistent._mas_player_bookmarked:
                    textbutton _("{size=-9}Сохранить\n тему\n в закладки{/size}") action Function(_mas_hk_bookmark_topic)
                elif persistent.current_monikatopic in persistent._mas_player_bookmarked:
                    textbutton _("{size=-9}Удалить\n тему\n из закладок{/size}") action Function(_mas_hk_bookmark_topic)

                if mas_findEVL("mas_topic_derandom") < 0:
                    textbutton _("{size=-9}Внести\n в чёрный список{/size}") action Function(_mas_hk_derandom_topic)
                else:
                    textbutton _("{size=-9}Убрать\n из чёрного списка{/size}") action Function(_mas_hk_derandom_topic)

        else:
            vbox at mas_buttons_move(0.85, 690):
                xpos 0.85

                yanchor 1.0
                ypos 690




                if persistent.current_monikatopic not in persistent._mas_player_bookmarked:
                    textbutton _("{size=-9}Сохранить\n тему\n в закладки{/size}") action Function(_mas_hk_bookmark_topic)
                elif persistent.current_monikatopic in persistent._mas_player_bookmarked:
                    textbutton _("{size=-9}Удалить\n тему\n из закладок{/size}") action Function(_mas_hk_bookmark_topic)


screen movie_overlay():

    zorder 50
    style_prefix "hkb"

    vbox:
        xalign 0.95
        yalign 0.95

        if watchingMovie:
            textbutton _("Пауза") action Jump("mm_movie_pausefilm")
        else:
            textbutton _("Пауза")
        if watchingMovie:
            textbutton _("Время") action Jump("mm_movie_settime")
        else:
            textbutton _("Время")
            
init python:
    HKBShowButtons()
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
