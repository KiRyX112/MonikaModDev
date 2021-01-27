default color_overlay_on = False
default persistent.seen_color_menu = False
default persistent.show_message = True

init python:

    def MSRColorShowButtons():

        config.overlay_screens.append("msr_color_overlay")

    def mas_MSRColorIsVisible1():

        return "msr_color_overlay" in config.overlay_screens

    def mas_MSRColorIsVisible2():

        return "msr_color_overlay2" in config.overlay_screens

    def MSRColorHideButtons():

        if mas_MSRColorIsVisible1():
            config.overlay_screens.remove("msr_color_overlay")
            renpy.hide_screen("msr_color_overlay")

        if mas_MSRColorIsVisible2():
            config.overlay_screens.remove("msr_color_overlay2")
            renpy.hide_screen("msr_color_overlay2")

    def MSRShowMessage():
        renpy.show_screen("msr_message_overlay")

screen msr_timer():
    timer 4.0 action [Function(MSRShowMessage), SetField(persistent, "show_message", True)]

screen msr_message_overlay():

    zorder 40

    if not color_overlay_on:
        if (persistent.show_message) and (monika_chr.clothes == orcaramelo_sweater_shoulderless or monika_chr.clothes == orcaramelo_sweater_shoulderless_red or monika_chr.clothes == orcaramelo_sweater_shoulderless_orange or monika_chr.clothes == orcaramelo_sweater_shoulderless_green or monika_chr.clothes == orcaramelo_sweater_shoulderless_blue or monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue or monika_chr.clothes == orcaramelo_sweater_shoulderless_purple or monika_chr.clothes == orcaramelo_sweater_shoulderless_pink):
            if (not persistent._mas_dark_mode_enabled and not persistent._mas_auto_mode_enabled) or (persistent._mas_auto_mode_enabled and mas_current_background.isFltDay()):
                frame at mas_buttons_message_move(0.05, 490):
                    xpos 0.05

                    yanchor 1.0
                    ypos 490
                    ypadding 5
                    xsize 120

                    background "mod_assets/msr_images/message_background.png"
                    text "{size=-6}Эта кнопка меняет цвет костюма, чтобы спрятать это меню нажмите C.{/size}":
                        outlines []
                        size 17
                        color "#000000"
            else:
                frame at mas_buttons_message_move(0.05, 490):
                    xpos 0.05

                    yanchor 1.0
                    ypos 490
                    ypadding 5
                    xsize 120

                    background "mod_assets/msr_images/message_background_d.png"
                    text "{size=-6}Эта кнопка меняет цвет костюма, чтобы спрятать это меню нажмите C.{/size}":
                        outlines []
                        size 17
                        color "#000000"

screen msr_color_overlay():

    zorder 50

    key "noshift_С" action If(color_overlay_on,
                            true=SetVariable("color_overlay_on", False),
                            false=SetVariable("color_overlay_on", True))
    key "noshift_с" action If(color_overlay_on,
                            true=SetVariable("color_overlay_on", False),
                            false=SetVariable("color_overlay_on", True))
    key "noshift_C" action If(color_overlay_on,
                            true=SetVariable("color_overlay_on", False),
                            false=SetVariable("color_overlay_on", True))
    key "noshift_c" action If(color_overlay_on,
                            true=SetVariable("color_overlay_on", False),
                            false=SetVariable("color_overlay_on", True))

    if not color_overlay_on:
        if not persistent.seen_color_menu:
            if (persistent.show_message) and (monika_chr.clothes == orcaramelo_sweater_shoulderless or monika_chr.clothes == orcaramelo_sweater_shoulderless_red or monika_chr.clothes == orcaramelo_sweater_shoulderless_orange or monika_chr.clothes == orcaramelo_sweater_shoulderless_green or monika_chr.clothes == orcaramelo_sweater_shoulderless_blue or monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue or monika_chr.clothes == orcaramelo_sweater_shoulderless_purple or monika_chr.clothes == orcaramelo_sweater_shoulderless_pink):
                if (not persistent._mas_dark_mode_enabled and not persistent._mas_auto_mode_enabled) or (persistent._mas_auto_mode_enabled and mas_current_background.isFltDay()):
                    frame at mas_buttons_message_move(0.05, 490):
                        xpos 0.05

                        yanchor 1.0
                        ypos 490
                        ypadding 5
                        xsize 120

                        background "mod_assets/msr_images/message_background.png"
                        text "{size=-6}Эта кнопка меняет цвет костюма, чтобы спрятать это меню нажмите C.{/size}":
                            outlines []
                            size 17
                            color "#000000"
                else:
                    frame at mas_buttons_message_move(0.05, 490):
                        xpos 0.05

                        yanchor 1.0
                        ypos 490
                        ypadding 5
                        xsize 120

                        background "mod_assets/msr_images/message_background_d.png"
                        text "{size=-6}Эта кнопка меняет цвет костюма, чтобы спрятать это меню нажмите C.{/size}":
                            outlines []
                            size 17
                            color "#000000"

        vbox at mas_buttons_move(0.05, 550):
            xpos 0.05

            yanchor 1.0
            ypos 550
            if (not persistent._mas_dark_mode_enabled and not persistent._mas_auto_mode_enabled) or (persistent._mas_auto_mode_enabled and mas_current_background.isFltDay()):
                if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background.png"
                        hover_background "mod_assets/hkb_hover_background.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

            else:
                if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

                elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                    imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                        idle_background "mod_assets/hkb_idle_background_d.png"
                        hover_background "mod_assets/hkb_hover_background_d.png"
                        hovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_message_overlay"), Show("msr_timer")],
                                        false=NullAction())
                        unhovered If(persistent.seen_color_menu,
                                        true=[Hide("msr_timer"), Hide("msr_message_overlay"), SetField(persistent, "show_message", False)],
                                        false=NullAction())
                        action [SetVariable("color_overlay_on", True),
                            Function(mas_extra_menu.msr_color_overlay_action)]

screen msr_color_overlay2():

    zorder 50

    vbox at mas_buttons_color_move(0.05, 520):
        xpos 0.05

        yanchor 1.0
        ypos 520
        if (not persistent._mas_dark_mode_enabled and not persistent._mas_auto_mode_enabled) or (persistent._mas_auto_mode_enabled and mas_current_background.isFltDay()):
            if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

        else:
            if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_pink_action)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_red_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_orange_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_yellow_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_green_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_blue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_darkblue_action)]

                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_sweater_purple_action)]

    vbox:

        xpos 0.05

        yanchor 1.0
        ypos 550
        if (not persistent._mas_dark_mode_enabled and not persistent._mas_auto_mode_enabled) or (persistent._mas_auto_mode_enabled and mas_current_background.isFltDay()):
            if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background.png"
                    hover_background "mod_assets/hkb_hover_background.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

        else:
            if monika_chr.clothes == orcaramelo_sweater_shoulderless:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_yellow_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_red:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_red_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_orange:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_orange_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_green:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_green_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_blue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_blue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_darkblue:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_darkblue_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_purple:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_purple_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]

            elif monika_chr.clothes == orcaramelo_sweater_shoulderless_pink:
                imagebutton auto "mod_assets/msr_images/color_sweater/hkb_%s_sweater_pink_d.png" hover_sound "gui/sfx/hover.ogg" activate_sound "gui/sfx/select.ogg":
                    idle_background "mod_assets/hkb_idle_background_d.png"
                    hover_background "mod_assets/hkb_hover_background_d.png"
                    action [SetVariable("color_overlay_on", False),
                        Function(mas_extra_menu.msr_color_overlay_return)]
