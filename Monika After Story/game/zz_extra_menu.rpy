

default persistent.mas_window_color = "default"
default persistent.mas_mouse_color = "default"
default persistent.mas_sayori_name_abb = "Сайори"
default persistent.player_abbreviated_name = False
default persistent.aff_indicator_sistem = False
default persistent.aff_indicator_show = True
default persistent.msr_animations = False
default persistent.random_emotions = False
default persistent.monika_name_abb_first = True
default persistent.msr_bg_animations = False
default persistent.random_consents = False
default persistent.msr_elastic_sprite = False
default persistent.msr_voice = False
default persistent.hide_monika = False
default persistent.msr_weather_forecast_active = False
default persistent.bang_dream_songs_active = False

define numbers_three_list = [".99", ".98", ".97", ".96", ".95", ".94", ".93", ".92", ".91", ".90", ".89", ".88", ".87", ".86", ".85", ".84",
    ".83", ".82", ".81", ".80", ".79", ".78", ".76", ".76", ".75", ".74", ".73", ".72", ".71", ".70", ".69", ".68", ".67", ".66",
    ".65", ".64", ".63", ".62", ".61", ".60", ".59", ".58", ".57", ".56", ".55", ".54", ".53", ".52", ".51", ".50", ".49", ".48",
    ".47", ".46", ".45", ".44", ".43", ".42", ".41", ".40", ".39", ".38", ".37", ".36", ".35", ".34", ".33", ".32", ".31", ".30",
    ".29", ".28", ".27", ".26", ".25", ".24", ".23", ".22", ".21", ".20", ".19", ".18", ".17", ".16", ".15", ".14", ".13", ".12",
    ".11", ".10", ".09", ".08", ".07", ".06", ".05", ".04", ".03", ".02", ".01", ".00"]

define numbers_two_list = [".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9"]

transform up_poem_anim(yal=0.0):
    yoffset -300
    alpha 0.0
    easein 1.0 yoffset yal alpha 1.0
    on idle:
        zoom 1.0
    on hide:
        yoffset yal
        alpha 1.0
        easein 1.0 yoffset -250 alpha 0.0

transform down_anim(yal):
    on show:
        yoffset 300
        alpha 0.0
        easein 2.0 yoffset yal alpha 1.0
    on hide:
        yoffset yal
        alpha 1.0
        easein 2.0 yoffset 300 alpha 0.0

image light_monika_room_day_anim:
    contains:
        "mod_assets/extra/anim_bg/monika_day_room_anim.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat

image light_monika_room_day_anim_xmas:
    contains:
        "mod_assets/extra/anim_bg/monika_day_room_anim_xmas.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat

image light_monika_room_evening_anim:
    contains:
        "mod_assets/extra/anim_bg/monika_room_anim.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat

image light_monika_room_evening_anim_xmas:
    contains:
        "mod_assets/extra/anim_bg/monika_room_anim_xmas.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat

image light_monika_room_rain_anim:
    contains:
        "mod_assets/extra/anim_bg/monika_day_room_rain_anim.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat

image light_monika_room_rain_anim_xmas:
    contains:
        "mod_assets/extra/anim_bg/monika_day_room_rain_anim_xmas.png"
        alpha 0
        parallel:
            ease 7.0 alpha 0.8
            pause 12
            ease 7.0 alpha 0.05
            pause 5
            repeat
    contains:
        "dust5"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust6"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust7"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust8"
        alpha 0.1
        parallel:
            ease 7.0 alpha 1.0
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust11"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
    contains:
        "dust12"
        alpha 0.1
        parallel:
            ease 7.0 alpha 0.7
            pause 12
            ease 7.0 alpha 0.01
            pause 5
            repeat
image dust1:
    "images/cg/y_cg2_dust1.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        10.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 14.0 xoffset -100 yoffset 100
        repeat
image dust2:
    "images/cg/y_cg2_dust2.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        28.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 32.0 xoffset -100 yoffset 100
        repeat
image dust3:
    "images/cg/y_cg2_dust3.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        13.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 17.0 xoffset -100 yoffset 100
        repeat

image dust4:
    "images/cg/y_cg2_dust4.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        15.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 19.0 xoffset -100 yoffset 100
        repeat

image dust5:
    "images/cg/y_cg2_dust5.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        10.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 14.0 xoffset -100 yoffset 100
        repeat
image dust6:
    "images/cg/y_cg2_dust6.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        28.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 32.0 xoffset -100 yoffset 100
        repeat
image dust7:
    "images/cg/y_cg2_dust7.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        13.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 17.0 xoffset -100 yoffset 100
        repeat

image dust8:
    "images/cg/y_cg2_dust8.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        15.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 19.0 xoffset -100 yoffset 100
        repeat

image dust9:
    "images/cg/y_cg2_dust9.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        10.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 14.0 xoffset -100 yoffset 100
        repeat
image dust10:
    "images/cg/y_cg2_dust10.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        28.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 32.0 xoffset -100 yoffset 100
        repeat
image dust11:
    "images/cg/y_cg2_dust11.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        13.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 17.0 xoffset -100 yoffset 100
        repeat

image dust12:
    "images/cg/y_cg2_dust12.png"
    subpixel True
    parallel:
        alpha 1.00
        6.0
        linear 1.0 alpha 0.35
        1.0
        linear 1.0 alpha 1.0
        repeat
    parallel:
        alpha 0
        linear 2.0 alpha 1.0
        15.0
        linear 2.0 alpha 0
        repeat
    parallel:
        xoffset 100 yoffset -100
        linear 19.0 xoffset -100 yoffset 100
        repeat

transform bg_alpha(a=1.0):
    alpha a

transform mas_bg_zoom_e(z=1.0, zz=1.0, t=0.0, x=0.5, xx=0.5, y=0.5, yy=0.5, a=1.0):
    zoom z xalign x yalign y alpha a
    ease t zoom zz xalign xx yalign yy

transform mas_screen_normal:
    linear 2.0 xalign 0.5 yalign 0.5

transform mas_bg_alpha(a=1.0):
    alpha a

transform mas_super_shake:
    block:
        parallel:
            parallel:
                choice:
                    xanchor 0.2
                choice:
                    xanchor 0.3
                choice:
                    xanchor 0.4
                choice:
                    xanchor 0.5
                choice:
                    xanchor 0.6
                choice:
                    xanchor 0.7
                choice:
                    xanchor 0.8
            parallel:
                choice:
                    yanchor 0.2
                choice:
                    yanchor 0.3
                choice:
                    yanchor 0.4
                choice:
                    yanchor 0.5
                choice:
                    yanchor 0.6
                choice:
                    yanchor 0.7
                choice:
                    yanchor 0.8
        parallel:
            choice:
                rotate -2
            choice:
                rotate -0.5
            choice:
                rotate 0
            choice:
                rotate 0.5
            choice:
                rotate 2
        pause 0.04
        repeat 10
    block:
        parallel:
            parallel:
                choice:
                    xanchor 0.499
                choice:
                    xanchor 0.5
                choice:
                    xanchor 0.501
            parallel:
                choice:
                    yanchor 0.499
                choice:
                    yanchor 0.5
                choice:
                    yanchor 0.501
        parallel:
            choice:
                rotate -0.2
            choice:
                rotate -0.1
            choice:
                rotate 0
            choice:
                rotate 0.1
            choice:
                rotate 0.2
        pause 0.04
        repeat

transform mas_null_transform:
    pause 0.1

transform mas_shake(t1=mas_null_transform, t2=mas_null_transform, t3=mas_null_transform, t4=mas_null_transform, t5=mas_null_transform, t6=mas_null_transform):
    parallel:
        t1
    parallel:
        t2
    parallel:
        t3
    parallel:
        t4
    parallel:
        t5
    parallel:
        t6

transform mas_xypos(xp=0.5, yp=1.0, time=0.0):
    ease time xpos xp ypos yp

transform mas_super_effect:
    xalign 0.5 yalign 0.5 zoom 1.1
    parallel:
        ease 2.0 xpos 0.505
        ease 2.0 xpos 0.4915
        ease 2.0 xpos 0.5115
        ease 2.0 xpos 0.495
        repeat
    parallel:
        ease 1.9 ypos 0.52
        ease 1.9 ypos 0.489
        ease 1.9 ypos 0.52
        ease 1.9 ypos 0.489
        repeat
    parallel:
        ease 2.25 rotate -0.5
        ease 2.25 rotate -0.57
        ease 2.25 rotate -0.2
        ease 2.25 rotate 0.17
        ease 2.25 rotate 0.5
        ease 2.25 rotate 0.2
        ease 2.25 rotate 0.57
        repeat
    parallel:
        pause 1.15
        ease 0.25 zoom 1.2
        ease 0.5 zoom 1.1
        repeat
    parallel:
        pause 1.15
        ease 0.25 rotate 2.9
        ease 0.25 rotate 1.0
        ease 0.25 rotate 0.0
        repeat

transform mas_screen_attack:
    xalign 0.5 yalign 0.5
    parallel:
        ease 0.25 zoom 1.2
        ease 0.5 zoom 1.0
    parallel:
        ease 0.25 rotate -1.9
        ease 0.25 rotate 1.0
        ease 0.25 rotate 0.0

transform mas_bg_zoom_e(z=1.0, zz=1.0, t=0.0, x=0.5, xx=0.5, y=0.5, yy=0.5, a=1.0):
    zoom z xalign x yalign y alpha a
    ease t zoom zz xalign xx yalign yy

transform mas_bg_alpha(a=1.0):
    alpha a

transform mas_screen_dizziness:
    xalign 0.5 yalign 0.5
    parallel:
        ease 2.0 xpos 0.505
        ease 2.0 xpos 0.4975
        ease 2.0 xpos 0.5095
        ease 2.0 xpos 0.495
        repeat
    parallel:
        ease 1.9 ypos 0.5
        ease 1.9 ypos 0.489
        ease 1.9 ypos 0.5
        ease 1.9 ypos 0.489
        repeat
    parallel:
        ease 2.25 rotate -0.3
        ease 2.25 rotate -0.17
        ease 2.25 rotate -0.2
        ease 2.25 rotate 0.17
        ease 2.25 rotate 0.3
        ease 2.25 rotate 0.2
        ease 2.25 rotate 0.17
        repeat
    parallel:
        ease 2.15 zoom 0.99
        ease 2.15 zoom 1.03
        ease 2.15 zoom 0.99
        ease 2.15 zoom 1.02
        ease 2.15 zoom 0.99
        ease 2.15 zoom 1.03
        ease 2.15 zoom 1.01
        ease 2.15 zoom 0.99
        ease 2.15 zoom 1.03
        repeat

define flash = Fade(0.3, 0, 0.75, color="#fff")
define mas_aff_indicator_update = True
define natsuki_name_list = ["natsuki", "нацуки", "натсуки", "натцуки"]
define yuri_name_list = ["yuri", "юри", "юрец"]
define sayori_name_list = ["sayori", "саёри", "сайори", "саери"]
define monika_name_list = ["monika", "моника", "moni", "мони", "моня", "монька", "монечка", "моничка"]
define girls_names_list = ["natsuki", "нацуки", "натсуки", "натцуки", "yuri", "юри", "юрец", "sayori", "саёри", "сайори", "саери"]
define msr_d01 = datetime.date(datetime.date.today().year, 12, 1)
define msr_f28 = datetime.date(datetime.date.today().year, 2, 25)

style indicator_text:
    color "#000000"
    font "gui/font/comic.ttf"
    size 12
    outlines []

style aff_bar:
    left_bar Frame("mod_assets/overlays/aff_exp_full.png", 0, 0)
    right_bar Frame("mod_assets/overlays/aff_exp_empty.png", 0, 0)
    xmaximum 220
    ymaximum 33

style aff_bar2:
    left_bar Frame("mod_assets/overlays/aff_exp_empty.png", 0, 0)
    right_bar Frame("mod_assets/overlays/aff_exp_no_full.png", 0, 0)
    xmaximum 220
    ymaximum 33

init -15 python in MSR:
    import store

    Show, Hide = [], []

    class TheMainDistributorValuesDefinitionsAndClass(object):
        IN = []
        TYPE = [
            Show,
            Hide
            ]

        __author__ = u"MSR"
        __RenPy_version__ = (7, 0, 0, 196)

        import store.MSR as MSR

    def ShowAllVariables():
        """
        TYPE:
            Show
        """
        renpy.call("msr_show_all_variables")

    def ShowAffIndicator():
        """
        TYPE:
            Show
        """
        renpy.show_screen("affection_indicator")

    def HideAffIndicator():
        """
        TYPE:
            Hide
        """
        renpy.hide_screen("affection_indicator")

    def ShowRandomConsents():
        """
        TYPE:
            Show
        """
        if store.persistent.random_consents:
            store.random_sure = store.random.choice(["Разумеется", "Обязательно", "Несомненно", "Непременно", "Конечно", "Без проблем",
                                                    "Безусловно", "Естественно", "Без вопросов", "Ещё бы", "Нет вопросов", "Нет проблем",
                                                    "Спору нет", "Без сомнения", "Без всякого сомнения", "Однозначно", "Безоговорочно"])
            store.random_sure_lower = store.random.choice(["разумеется", "обязательно", "несомненно", "непременно", "конечно", "без проблем",
                                                    "безусловно", "естественно", "без вопросов", "ещё бы", "нет вопросов", "нет проблем",
                                                    "спору нет", "без сомнения", "без всякого сомнения", "однозначно", "безоговорочно"])
        else:
            store.random_sure = "Конечно"
            store.random_sure_lower = "конечно"

    def ShowDizzinessScreens():
        if store.persistent.msr_animations:
            renpy.show_layer_at(store.mas_screen_dizziness, layer='screens')

    def ShowNormalScreens():
        if store.persistent.msr_animations:
            renpy.show_layer_at(store.mas_screen_normal, layer='screens')

    def MasterBgZoomE(z=1.0, zz=1.0, t=0.0, x=0.5, xx=0.5, y=0.5, yy=0.5, a=1.0):
        if store.persistent.msr_animations:
            renpy.show_layer_at(store.mas_bg_zoom_e(z, zz, t, x, xx, y, yy, a), layer='master')

    def MusicVolume(v=1.0):
        if store.persistent.msr_animations:
            renpy.music.set_volume(v, channel="music")


transform sprite_jump(ystretch=0.01, xstretch=0.005, time=.4):
    parallel:
        yzoom 1.0
        easein time*0.25 yzoom 1.0+ystretch xzoom 1.0-xstretch
        easeout time*0.25 yzoom 1.0 xzoom 1.0
        easein time*0.25 yzoom 1.0-ystretch xzoom 1.0+xstretch
        easeout time*0.25 yzoom 1.0 xzoom 1.0

label monika_say:
    if persistent.image != None and store.persistent.hide_monika == False:
        if persistent.at != None:
            if not renpy.showing("monika " + persistent.image):
                $ renpy.show("monika " + persistent.image, zorder=10, at_list=[persistent.at])
        else:
            if store.persistent.msr_elastic_sprite == True:
                if not renpy.showing("monika " + persistent.image):
                    $ renpy.show("monika " + persistent.image, zorder=10, at_list=[sprite_jump])
            else:
                if not renpy.showing("monika " + persistent.image):
                    $ renpy.show("monika " + persistent.image, zorder=10)
    $ renpy.say(m, persistent.what, interact=True)
    return

label monika_elastic:
    if persistent.at:
        show monika zorder 10 at t11
    else:
        if persistent.msr_elastic_sprite:
            show monika zorder 10 at sprite_jump

init 1 python in MAS:
    import store
    import math
    import types
    import os
    # import requests, urllib, json
    import store.songs as songs

    # store.persistent.msr_weather_forecast_active = False
    def check_internet():
        url='http://www.google.com/'
        timeout=5
        try:
            internet = requests.get(url, timeout=timeout)
            return True
        except:
            return False

    def Say(who, image, what, at=None, interact=True, voice=None):


        if voice != None and store.persistent.msr_voice == True:
            renpy.music.play("sfx/" + str(voice) + ".ogg", channel="sound")

        store.persistent.image = image
        store.persistent.at = at
        store.persistent.what = what

        renpy.call("monika_say")

    def MonikaElastic(at=None, voice=None):
        if voice != None and store.persistent.msr_voice == True:
            renpy.music.play("sfx/" + str(voice) + ".ogg", channel="sound")
        store.persistent.at = at
        renpy.call("monika_elastic")
    
    # def ChangeClothes(outfit=None, outfit_mode=False, exp="monika 2eua", restore_zoom=True, unlock=False):
        
    #     # if outfit is None:
    #     #     outfit = store.mas_clothes_def

    #     # store._window_hide(None)

    #     # renpy.call("mas_transition_to_emptydesk")

    #     # renpy.pause(2.0)

    #     # if store.monika_chr.is_wearing_clothes_with_exprop("costume") and outfit == store.mas_clothes_def or outfit == store.mas_clothes_blazerless:
    #     #     store.monika_chr.reset_hair()

    #     # store.monika_chr.change_clothes(outfit, outfit_mode=outfit_mode)
    #     # if unlock:
    #     #     store.mas_selspr.unlock_clothes(outfit)
    #     #     store.mas_selspr.save_selectables()
    #     # store.monika_chr.save()
    #     # renpy.save_persistent()

    #     # renpy.pause(2.0)

    #     # renpy.call("mas_transition_from_emptydesk", exp)
    #     renpy.call("mas_clothes_change_new", outfit, outfit_mode, exp, restore_zoom, unlock)


    def play_custom_music(song,
    fadein=0.0, loop=True):

        renpy.music.play(
            song,
            channel="music",
            loop=loop,
            synchro_start=True,
            fadein=fadein
        )

        store.persistent.current_track = song



init 10000 python in mas_extra_menu:
    import store




    def red_window_action():
        store.style.say_window = store.style.window_red
        store.style.say_label = store.style.say_label_red
        store.persistent.mas_window_color = "red"

    def orange_window_action():
        store.style.say_window = store.style.window_orange
        store.style.say_label = store.style.say_label_orange
        store.persistent.mas_window_color = "orange"

    def yellow_window_action():
        store.style.say_window = store.style.window_yellow
        store.style.say_label = store.style.say_label_yellow
        store.persistent.mas_window_color = "yellow"

    def gray_window_action():
        store.style.say_window = store.style.window_gray
        store.style.say_label = store.style.say_label_gray
        store.persistent.mas_window_color = "gray"

    def seroburomaline_window_action():
        store.style.say_window = store.style.window_seroburomaline
        store.style.say_label = store.style.say_label_seroburomaline
        store.persistent.mas_window_color = "seroburomaline"

    def chocolate_window_action():
        store.style.say_window = store.style.window_chocolate
        store.style.say_label = store.style.say_label_chocolate
        store.persistent.mas_window_color = "chocolate"

    def tomato_window_action():
        store.style.say_window = store.style.window_tomato
        store.style.say_label = store.style.say_label_tomato
        store.persistent.mas_window_color = "tomato"

    def green_window_action():
        store.style.say_window = store.style.window_green
        store.style.say_label = store.style.say_label_green
        store.persistent.mas_window_color = "green"

    def crimson_window_action():
        store.style.say_window = store.style.window_crimson
        store.style.say_label = store.style.say_label_crimson
        store.persistent.mas_window_color = "crimson"

    def white_window_action():
        store.style.say_window = store.style.window_white
        store.style.say_label = store.style.say_label_white
        store.persistent.mas_window_color = "white"

    def default_window_action():
        store.style.say_window = store.style.window
        store.style.say_label = store.style.say_label_white
        store.persistent.mas_window_color = "default"



    def red_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse1.png", 0, 0)]}
        store.persistent.mas_mouse_color = "red"

    def yellow_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse2.png", 0, 0)]}
        store.persistent.mas_mouse_color = "yellow"

    def orange_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse3.png", 0, 0)]}
        store.persistent.mas_mouse_color = "orange"

    def gray_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse4.png", 0, 0)]}
        store.persistent.mas_mouse_color = "gray"

    def blue_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse5.png", 0, 0)]}
        store.persistent.mas_mouse_color = "blue"

    def purple_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse6.png", 0, 0)]}
        store.persistent.mas_mouse_color = "purple"

    def chocolate_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse7.png", 0, 0)]}
        store.persistent.mas_mouse_color = "chocolate"

    def pink_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse8.png", 0, 0)]}
        store.persistent.mas_mouse_color = "pink"

    def green_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse9.png", 0, 0)]}
        store.persistent.mas_mouse_color = "green"

    def blue2_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse10.png", 0, 0)]}
        store.persistent.mas_mouse_color = "blue2"

    def white_mouse_action():
        store.config.mouse = {'default' : [("mod_assets/extra/cursors/mouse11.png", 0, 0)]}
        store.persistent.mas_mouse_color = "white"

    def default_mouse_action():
        store.config.mouse = None
        store.persistent.mas_mouse_color = "default"



    def textbox_choice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("textbox_choice")

    def textbox_choice_return():
        renpy.hide_screen("textbox_choice")
        renpy.show_screen("extra_menu")

    def cursor_choice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("cursor_choice")

    def cursor_choice_return():
        renpy.hide_screen("cursor_choice")
        renpy.show_screen("extra_menu")

    def sayori_name_choice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("sayori_name_choice")

    def sayori_name_choice_return():
        renpy.hide_screen("sayori_name_choice")
        renpy.show_screen("extra_menu")

    def names_say_choice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("names_say_choice")

    def names_say_choice_return():
        renpy.hide_screen("names_say_choice")
        renpy.show_screen("extra_menu")

    def abbreviated_name_choice_return():
        store.persistent.player_abbreviated_name = True
        renpy.hide_screen("names_say_choice_message")
        renpy.show_screen("names_say_choice")

    def random_emotions_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("random_emotions_choice")

    def random_emotions_return():
        renpy.hide_screen("random_emotions_choice")
        renpy.show_screen("extra_menu")

    def extra_menu_pool_action():
        renpy.hide_screen("extra_menu")
        renpy.jump("mas_extra_menu_pool")

    def mas_extra_menu_return():
        renpy.hide_screen("extra_menu")

    def names_say_choice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("names_say_choice")

    def names_say_choice_quit():
        renpy.hide_screen("names_say_choice")
        renpy.hide_screen("extra_menu")

    def player_abbreviated_name_true():
        store.persistent.player_abbreviated_name = True

    def player_abbreviated_name_false():
        store.persistent.player_abbreviated_name = False

    def animation_bg_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("anim_bg_choice")

    def animation_bg_return():
        renpy.hide_screen("anim_bg_choice")
        renpy.show_screen("extra_menu")

    def winter_action():
        renpy.show_screen("winter_choice")
        renpy.hide_screen("extra_menu")

    def winter_return():
        renpy.hide_screen("winter_choice")
        renpy.show_screen("extra_menu")

    def winter_choice_true():
        store.persistent.winter_mode = True

    def winter_choice_false():
        store.persistent.winter_mode = False

    def random_emotions_action():
        renpy.show_screen("random_emotions")
        renpy.hide_screen("extra_menu")

    def random_emotions_return():
        renpy.hide_screen("random_emotions")
        renpy.show_screen("extra_menu")

    def affection_indicator_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("set_affection_indicator_choice")

    def affection_indicator_return():
        renpy.hide_screen("set_affection_indicator_choice")
        renpy.show_screen("extra_menu")

    def random_consents_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("random_consents_choice")

    def random_consents_return():
        renpy.hide_screen("random_consents_choice")
        renpy.show_screen("extra_menu")

    def msr_animations_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("msr_animations_choice")

    def msr_animations_return():
        renpy.hide_screen("msr_animations_choice")
        renpy.show_screen("extra_menu")

    def msr_elastic_sprite_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("msr_elastic_sprite_choice")

    def msr_elastic_sprite_return():
        renpy.hide_screen("msr_elastic_sprite_choice")
        renpy.show_screen("extra_menu")

    def msr_voice_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("msr_voice_choice")

    def msr_voice_return():
        renpy.hide_screen("msr_voice_choice")
        renpy.show_screen("extra_menu")

    # def msr_weather_forecast_action():
    #     renpy.hide_screen("extra_menu")
    #     renpy.show_screen("msr_weather_forecast_choice")

    # def msr_weather_forecast_return():
    #     renpy.hide_screen("msr_weather_forecast_choice")
    #     renpy.show_screen("extra_menu")

    def msr_bang_dream_songs_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("msr_bang_dream_songs_choice")

    def msr_bang_dream_songs_return():
        renpy.hide_screen("msr_bang_dream_songs_choice")
        renpy.show_screen("extra_menu")
    
    def msr_custom_bg_action():
        renpy.hide_screen("extra_menu")
        renpy.show_screen("msr_custom_bg_choice")

    def msr_custom_bg_return():
        renpy.hide_screen("msr_custom_bg_choice")
        renpy.show_screen("extra_menu")


    def play_music(song, fadein=0.0, loop=True, set_per=False):

        renpy.music.play(
            song,
            channel="music",
            loop=loop,
            synchro_start=True,
            fadein=fadein
        )

        store.persistent.current_track = song

        store.persistent.custom_music = song

    def msr_color_menu():
        if store.color_overlay_on:
            store.color_overlay_on = False
        else:
            store.color_overlay_on = True

    def msr_color_overlay_action():
        store.persistent.show_message = False
        store.persistent.seen_color_menu = True
        renpy.hide_screen("msr_color_overlay")
        renpy.show_screen("msr_color_overlay2")

    def msr_color_overlay_return():
        store.persistent.show_message = False
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_red_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_red)
        store.persistent.color_sweater = "red"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_orange_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_orange)
        store.persistent.color_sweater = "orange"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_yellow_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless)
        store.persistent.color_sweater = "yellow"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_green_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_green)
        store.persistent.color_sweater = "green"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_blue_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_blue)
        store.persistent.color_sweater = "blue"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_darkblue_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_darkblue)
        store.persistent.color_sweater = "darkblue"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_purple_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_purple)
        store.persistent.color_sweater = "purple"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")

    def msr_color_sweater_pink_action():
        store.monika_chr.change_clothes(store.orcaramelo_sweater_shoulderless_pink)
        store.persistent.color_sweater = "pink"
        renpy.hide_screen("msr_color_overlay2")
        renpy.show_screen("msr_color_overlay")




default persistent.color_sweater = "yellow"

transform showwindow:
    ypos 0.2 alpha 0.0
    ease 1.0 ypos 0.0 alpha 1.0

transform showwindow_fast:
    ypos 0.2 alpha 0.0
    ease 0.5 ypos 0.0 alpha 1.0

transform hidewindow_fast:
    xpos 0.0 ypos 0.0 alpha 1.0
    ease 0.5 xpos 0.0 ypos 0.2 alpha 0.0

transform hidewindow:
    xpos 0.0 ypos 0.0 alpha 1.0
    ease 1.0 xpos 0.0 ypos 0.2 alpha 0.0

transform mas_window_move:
    on show:
        xpos 0.5 ypos 815 alpha 0.0
        ease 1.0 ypos 715 alpha 1.0
    on hide:
        xpos 0.5 ypos 715 alpha 1.0
        ease 1.0 ypos 815 alpha 0.0
    on auto:
        xpos 0.5 ypos 815 alpha 0.0
        ease 1.0 ypos 715 alpha 1.0
init -3 python:


    layout.MAS_NAME_ABB = (
        "Запускает менюшку, в котором можно включить уникальное произношение имени для Моники."
    )

    layout.MAS_WINDOW = (
        "Запускает менюшку с выбором цвета диалогового окна."
    )

    layout.MAS_CURSOR = (
        "Запускает менюшку с выбором курсора."
    )

    layout.MAS_SAYORI_NAME_ABB = (
        "Запускает менюшку с выбором имени Сайори/Саёри."
    )

    layout.MSR_ANIM_BG = (
        "Запускает менюшку с выбором живых фонов."
    )

    layout.MSR_WINTER_MODE = (
        "Режим в котором можно включить зиму."
    )

    layout.MAS_RANDOM_EMOTIONS = (
        "Менюшка в которой можно включить рандомные эмоции."
    )

    layout.MSR_AFF_INDICATOR = (
        "Менюшка, в которой можно включать и отключать индикатор привязанности."
    )

    layout.MSR_RANDOM_CONSENTS = (
        "Запускает менюшку, в котором можно включить/отключить ответы Моники как: "
        "«Разумеется», «Безусловно», «Конечно», «Без проблем», «Непременно» в тех месте, где они использовались, но теперь уже рандомно."
    )

    layout.MSR_ANIMATIONS = (
        "Запускает меню, в котором можно включить/отключить небольшие анимации от Курильни Маунти. Топики, в которых те уже доступны: "
        "«Ценность визуальных новелл», «Зрительный контакт»"
    )

    layout.MSR_ELASTIC_SPRITE = (
        "Запускает меню, в котором можно включить/отключить эластичность спрайта Моники"
    )

    layout.MSR_VOICE = (
        "Запускает меню, в котором можно включить/отключить голос Моники"
    )

    # layout.MSR_WEATHER_FORECAST = (
    #     "Запускает меню, в котором можно включить/отключить изменение погоды по прогнозу"
    #     "(пока эта функция работает, топик о смене погоды пропадёт)"
    # )

    layout.MSR_BANG_DREAM_SONGS = (
        "Запускает меню, в котором можно выбрать песню из игры BanG Dream!"
    )

    layout.MSR_CUSTOM_BG = (
        "Запускает меню, в котором можно изменить фон"
    )

default persistent.extra_menu_page = 1

screen extra_menu():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190


    $ disp_month = datetime.date.today().strftime("%B")

    default tooltip = Tooltip("")

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing
            yalign 0.15


            if persistent.extra_menu_page == 1:
                textbutton _("{size=-6}Меню инструментов{/size}") action Function(mas_extra_menu.extra_menu_pool_action)

                if not mas_globals.dark_mode:
                    textbutton _("{size=-6}|MSR| Сменить диалоговое окно{/size}"):
                        action Function(mas_extra_menu.textbox_choice_action)
                        hovered tooltip.Action(layout.MAS_WINDOW)
                if renpy.variant("pc"):
                    textbutton _("{size=-6}|MSR| Сменить курсор{/size}"):
                        action Function(mas_extra_menu.cursor_choice_action)
                        hovered tooltip.Action(layout.MAS_CURSOR)
                textbutton _("{size=-6}|MSR| Сменить стиль произношения имён{/size}"):
                    action Function(mas_extra_menu.names_say_choice_action)
                    hovered tooltip.Action(layout.MAS_NAME_ABB)
                textbutton _("{size=-6}|MSR| Рандомные эмоции{/size}"):
                    action Function(mas_extra_menu.random_emotions_action)
                    hovered tooltip.Action(layout.MAS_RANDOM_EMOTIONS)
                textbutton _("{size=-6}|MSR| Живая анимация задних фонов{/size}"):
                    action Function(mas_extra_menu.animation_bg_action)
                    hovered tooltip.Action(layout.MSR_ANIM_BG)
                textbutton _("{size=-6}|MSR| Индикатор привязанности{/size}"):
                    action Function(mas_extra_menu.affection_indicator_action)
                    hovered tooltip.Action(layout.MSR_AFF_INDICATOR)
                textbutton _("{size=-6}|MSR| Рандомные согласия{/size}"):
                    action Function(mas_extra_menu.random_consents_action)
                    hovered tooltip.Action(layout.MSR_RANDOM_CONSENTS)
                textbutton _("{size=-6}|MSR| Анимации для некоторых топиков{/size}"):
                    action Function(mas_extra_menu.msr_animations_action)
                    hovered tooltip.Action(layout.MSR_ANIMATIONS)
                textbutton _("{size=-6}|MSR| Эластичность спрайта Моники{/size}"):
                    action Function(mas_extra_menu.msr_elastic_sprite_action)
                    hovered tooltip.Action(layout.MSR_ELASTIC_SPRITE)
                textbutton _("{size=-6}|MSR| Голос Моники{/size}"):
                    action Function(mas_extra_menu.msr_voice_action)
                    hovered tooltip.Action(layout.MSR_VOICE)

            else:

                # if MAS.check_internet():
                #     textbutton _("{size=-6}|MSR| Изменение погоды по прогнозу{/size}"):
                #         action Function(mas_extra_menu.msr_weather_forecast_action)
                #         hovered tooltip.Action(layout.MSR_WEATHER_FORECAST)
                # else:
                #     textbutton _("{size=-6}|MSR| Изменение погоды по прогнозу погоды{/size}"):
                #         action Show(screen="dialog", message="Эта функция работает только когда включён интернет!", ok_action=Hide("dialog"))

                if persistent.bang_dream_songs_active:
                    textbutton _("{size=-6}|MSR| Песни BanG Dream!{/size}"):
                        action Function(mas_extra_menu.msr_bang_dream_songs_action)
                        hovered tooltip.Action(layout.MSR_BANG_DREAM_SONGS)

                textbutton _("{size=-6}|MSR| Кастомизация фона{/size}"):
                    action Function(mas_extra_menu.msr_custom_bg_action)
                    hovered tooltip.Action(layout.MSR_CUSTOM_BG)
                    
                textbutton _("")
                if renpy.variant("pc"):
                    textbutton _("")
                textbutton _("")
                textbutton _("")
                textbutton _("")
                textbutton _("")
                textbutton _("")
                textbutton _("")



    vbox:

        yalign 1.0
        if persistent.extra_menu_page < 2:
            textbutton _("Далее >>>"):
                style "extra_menu_return_button"
                # action Return(persistent.extra_menu_page + 1)
                action SetField(persistent, "extra_menu_page", persistent.extra_menu_page+1)
        if persistent.extra_menu_page > 1:
            textbutton _("<<< Назад"):
                style "extra_menu_return_button"
                action SetField(persistent, "extra_menu_page", persistent.extra_menu_page-1)
        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu_return)

    text tooltip.value:
        yalign 0.93
        xalign 0.8
        xmaximum 500
        xanchor 0.5
        style "main_menu_version"

    label "Экстра меню"

default persistent.snow_fall = False




default persistent.msr_current_track = None
image extra_menu_music_frame = "mod_assets/extra/extra_menu_music_frame.png"
image extra_menu_music_frame_d = "mod_assets/extra/extra_menu_music_frame_d.png"
image extra_menu_music_icon_1 = "mod_assets/extra/extra_menu_music_icon_1.png"
image extra_menu_music_icon_2 = "mod_assets/extra/extra_menu_music_icon_2.png"
image extra_menu_music_icon_3 = "mod_assets/extra/extra_menu_music_icon_3.png"
image extra_menu_music_text_def = "mod_assets/extra/extra_menu_music_text_def.png"
image extra_menu_music_text_def_d = "mod_assets/extra/extra_menu_music_text_def_d.png"
image extra_menu_music_text_1 = "mod_assets/extra/extra_menu_music_text_1.png"
image extra_menu_music_text_1_d = "mod_assets/extra/extra_menu_music_text_1_d.png"
image extra_menu_music_text_2 = "mod_assets/extra/extra_menu_music_text_2.png"
image extra_menu_music_text_2_d = "mod_assets/extra/extra_menu_music_text_2_d.png"
image extra_menu_music_text_3 = "mod_assets/extra/extra_menu_music_text_3.png"
image extra_menu_music_text_3_d = "mod_assets/extra/extra_menu_music_text_3_d.png"





screen msr_bang_dream_songs_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"


    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")



        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        if renpy.music.get_playing(channel='music') == persistent.msr_current_track:
            python:
                if persistent.msr_current_track == songs.FP_ROKU_CHOUNEN_PIANO_COVER:
                    ui.add("extra_menu_music_icon_1", at=up_poem_anim)

                elif persistent.msr_current_track == songs.FP_NEO_ASPECT_PIANO_COVER:
                    ui.add("extra_menu_music_icon_2", at=up_poem_anim)

                elif persistent.msr_current_track == songs.FP_R_PIANO_COVER:
                    ui.add("extra_menu_music_icon_3", at=up_poem_anim)

                if not mas_globals.dark_mode:
                    ui.add("extra_menu_music_frame", at=up_poem_anim)
                else:
                    ui.add("extra_menu_music_frame_d", at=up_poem_anim)

                if not mas_globals.dark_mode:
                    ui.add("extra_menu_music_text_def", at=up_poem_anim)
                else:
                    ui.add("extra_menu_music_text_def_d", at=up_poem_anim)

                if persistent.msr_current_track == songs.FP_ROKU_CHOUNEN_PIANO_COVER:
                    if not mas_globals.dark_mode:
                        ui.add("extra_menu_music_text_1", at=up_poem_anim)
                    else:
                        ui.add("extra_menu_music_text_1_d", at=up_poem_anim)

                elif persistent.msr_current_track == songs.FP_NEO_ASPECT_PIANO_COVER:
                    if not mas_globals.dark_mode:
                        ui.add("extra_menu_music_text_2", at=up_poem_anim)
                    else:
                        ui.add("extra_menu_music_text_2_d", at=up_poem_anim)

                elif persistent.msr_current_track == songs.FP_R_PIANO_COVER:
                    if not mas_globals.dark_mode:
                        ui.add("extra_menu_music_text_3", at=up_poem_anim)
                    else:
                        ui.add("extra_menu_music_text_3_d", at=up_poem_anim)


        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            if os.path.isfile(user_dir + "/game/" + songs.FP_ROKU_CHOUNEN_PIANO_COVER):
                textbutton _("Roku Chounen to Ichiya Monogatari\n(Piano Cover)"):
                    action [Play("music", songs.FP_ROKU_CHOUNEN_PIANO_COVER), SetField(persistent, "msr_current_track", songs.FP_ROKU_CHOUNEN_PIANO_COVER)]
            else:
                textbutton _("Песня отсутствует"):
                    action NullAction()

            if os.path.isfile(user_dir + "/game/" + songs.FP_NEO_ASPECT_PIANO_COVER):
                textbutton _("Neo Aspect (Piano Cover)"):
                    action [Play("music", songs.FP_NEO_ASPECT_PIANO_COVER), SetField(persistent, "msr_current_track", songs.FP_NEO_ASPECT_PIANO_COVER)]
            else:
                textbutton _("Песня отсутствует"):
                    action NullAction()

            if os.path.isfile(user_dir + "/game/" + songs.FP_R_PIANO_COVER):
                textbutton _("R (Piano Cover)"):
                    action [Play("music", songs.FP_R_PIANO_COVER), SetField(persistent, "msr_current_track", songs.FP_R_PIANO_COVER)]
            else:
                textbutton _("Песня отсутствует"):
                    action NullAction()

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_bang_dream_songs_return)
    label "Песни из BanG Dream!"

screen msr_weather_forecast_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(persistent, "msr_weather_forecast_active", True)
            textbutton _("Нет"):
                action SetField(persistent, "msr_weather_forecast_active", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_weather_forecast_return)
    if persistent.msr_weather_forecast_active:
        label "{size=-12}Разрешить изменение погоды по прогнозу?\n(Сейчас: включены){/size}"
    else:
        label "{size=-12}Разрешить изменение погоды по прогнозу?\n(Сейчас: отключены){/size}"

screen msr_animations_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(persistent, "msr_animations", True)
            textbutton _("Нет"):
                action SetField(persistent, "msr_animations", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_animations_return)
    if persistent.msr_animations:
        label "{size=-12}Разрешить анимации?\n(Сейчас: включены){/size}"
    else:
        label "{size=-12}Разрешить анимации?\n(Сейчас: отключены){/size}"

screen msr_elastic_sprite_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(store.persistent, "msr_elastic_sprite", True)
            textbutton _("Нет"):
                action SetField(store.persistent, "msr_elastic_sprite", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_elastic_sprite_return)
    if persistent.msr_elastic_sprite:
        label "{size=-12}Разрешить эластичность спрайта?\n(Сейчас: включена){/size}"
    else:
        label "{size=-12}Разрешить эластичность спрайта?\n(Сейчас: отключена){/size}"

screen msr_voice_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(store.persistent, "msr_voice", True)
            textbutton _("Нет"):
                action SetField(store.persistent, "msr_voice", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_voice_return)
    if persistent.msr_voice:
        label "{size=-12}Разрешить голос Моники?\n(Сейчас: включён){/size}"
    else:
        label "{size=-12}Разрешить голос Моники?\n(Сейчас: отключён){/size}"

screen random_consents_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(persistent, "random_consents", True)
            textbutton _("Нет"):
                action SetField(persistent, "random_consents", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.random_consents_return)
    if persistent.random_consents:
        label "{size=-12}Разрешить рандомные согласия?\n(Сейчас: включены){/size}"
    else:
        label "{size=-12}Разрешить рандомные согласия?\n(Сейчас: отключены){/size}"

default persistent.last_aff_points = 0
default persistent.aff_cheet_count = 1

init 30 python:
    if renpy.variant('pc'):
        persistent.aff_points = persistent._mas_affection["affection"]
        if (persistent.aff_points > persistent.last_aff_points) and (persistent.last_aff_points != None):
            try:
                mas_setAffection(persistent.last_aff_points)
                mas_setAffection(persistent.last_aff_points - persistent.aff_cheet_count * 10)
                persistent.aff_cheet_count = persistent.aff_cheet_count + 1
            except:
                pass


screen affection_indicator():

    zorder 90

    python:

        persistent.aff_points = persistent._mas_affection["affection"]
        persistent.aff_check = persistent.aff_points

        if persistent.aff_points <= -100:
            mas_screen_aff_group = "разбитое сердце"

        elif -100 <= persistent.aff_points <= -75:
            mas_screen_aff_group = "несчастная"

        elif -75 < persistent.aff_points <= -30:
            mas_screen_aff_group = "грустная"

        elif -30 < persistent.aff_points < 30:
            mas_screen_aff_group = "нормальная"

        elif 30 <= persistent.aff_points < 100:
            mas_screen_aff_group = "счастливая"

        elif 100 <= persistent.aff_points < 400:
            mas_screen_aff_group = "привязанная"

        elif 400 <= persistent.aff_points < 1000:
            mas_screen_aff_group = "влюблённая"

        elif persistent.aff_points >= 1000:
            mas_screen_aff_group = "сильная любовь"

        if persistent.aff_points <= -30:
            aff_icon_suffix = "_gray"
        else:
            aff_icon_suffix = ""

        aff_points_text = str(persistent.aff_points)

        if aff_points_text[-3:] in numbers_three_list:
            aff_points_text = aff_points_text[:len(aff_points_text)-3]
        elif aff_points_text[-2:] in numbers_two_list:
            aff_points_text = aff_points_text[:len(aff_points_text)-2]

        if persistent.aff_indicator_sistem:
            ui.add("mod_assets/extra/indicator/aff_text_overlay.png", xalign=0.0235, yalign=0.06, at=mas_indicator_move(0.0235, 0.06))
            ui.add("mod_assets/extra/indicator/aff_points_overlay.png", xalign=0.0235, yalign=0.01, at=mas_indicator_move(0.0235, 0.01))

            ui.add("mod_assets/extra/indicator/aff_hearth_icon" + aff_icon_suffix + ".png", xalign=-0.01, yalign=-0.008, at=mas_indicator_move(-0.01, -0.008))
            ui.add("mod_assets/extra/indicator/aff_rose_icon" + aff_icon_suffix + ".png", xalign=0.001, yalign=0.057, at=mas_indicator_move(0.001, 0.057))

            ui.text("Привязанность: %s" % (mas_screen_aff_group), xalign=0.036, yalign=0.072, style="indicator_text", at=mas_indicator_move(0.036, 0.072))
            ui.text("Очки: %s" % (aff_points_text), xalign=0.032, yalign=0.023, style="indicator_text", at=mas_indicator_move(0.032, 0.023))

screen set_affection_indicator_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Да"):
                action SetField(persistent, "aff_indicator_sistem", True)
            textbutton _("Нет"):
                action SetField(persistent, "aff_indicator_sistem", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.affection_indicator_return)
    if persistent.aff_indicator_sistem:
        label "{size=-12}Включить индикатор?\n(Сейчас: включён){/size}"
    else:
        label "{size=-12}Включить индикатор?\n(Сейчас: отключён){/size}"

screen random_emotions():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Включить"):
                action SetField(persistent, "random_emotions", True)
            textbutton _("Выключить"):
                action SetField(persistent, "random_emotions", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.random_emotions_return)
    if persistent.random_emotions:
        label "{size=-12}Рандомные эмоции\n(Сейчас: Включены){/size}"
    else:
        label "{size=-12}Рандомные эмоции\n(Сейчас: Выключены){/size}"

screen winter_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Включить"):
                action Function(mas_extra_menu.winter_choice_true)
            textbutton _("Выключить"):
                action Function(mas_extra_menu.winter_choice_false)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.winter_return)
    if persistent.winter_mode:
        label "{size=-12}Зимний режим\n(Сейчас: Включён){/size}"
    else:
        label "{size=-12}Зимний режим\n(Сейчас: Выключен){/size}"

screen textbox_choice():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Красное"):
                action Function(mas_extra_menu.red_window_action)
            textbutton _("Оранжевое"):
                action Function(mas_extra_menu.orange_window_action)
            textbutton _("Жёлтое"):
                action Function(mas_extra_menu.yellow_window_action)
            textbutton _("Серое"):
                action Function(mas_extra_menu.gray_window_action)
            textbutton _("Фиолетовое"):
                action Function(mas_extra_menu.seroburomaline_window_action)
            textbutton _("Шоколадное"):
                action Function(mas_extra_menu.chocolate_window_action)
            textbutton _("Томатное"):
                action Function(mas_extra_menu.tomato_window_action)
            textbutton _("Зелёное"):
                action Function(mas_extra_menu.green_window_action)
            textbutton _("Малиновое"):
                action Function(mas_extra_menu.crimson_window_action)
            textbutton _("Прозрачное белое"):
                action Function(mas_extra_menu.white_window_action)

    vbox:

        yalign 1.0

        textbutton _("По умолчанию"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.default_window_action)

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.textbox_choice_return)
    label "Диалоговое окно"

screen anim_bg_choice():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Включить"):
                action SetField(persistent, "msr_bg_animations", True)
            textbutton _("Выключить"):
                action SetField(persistent, "msr_bg_animations", False)

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.animation_bg_return)
    if persistent.msr_bg_animations:
        label "{size=-12}Анимация живых фонов\n(Сейчас: Включена){/size}"
    else:
        label "{size=-12}Анимация живых фонов\n(Сейчас: Выключена){/size}"
screen cursor_choice():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Красный"):
                action Function(mas_extra_menu.red_mouse_action)
            textbutton _("Жёлтый"):
                action Function(mas_extra_menu.yellow_mouse_action)
            textbutton _("Оранжевый"):
                action Function(mas_extra_menu.orange_mouse_action)
            textbutton _("Серый"):
                action Function(mas_extra_menu.gray_mouse_action)
            textbutton _("Синий"):
                action Function(mas_extra_menu.blue_mouse_action)
            textbutton _("Фиолетовый"):
                action Function(mas_extra_menu.purple_mouse_action)
            textbutton _("Шоколадный"):
                action Function(mas_extra_menu.chocolate_mouse_action)
            textbutton _("Розовый"):
                action Function(mas_extra_menu.pink_mouse_action)
            textbutton _("Зелёный"):
                action Function(mas_extra_menu.green_mouse_action)
            textbutton _("Голубой"):
                action Function(mas_extra_menu.blue2_mouse_action)
            textbutton _("Белый"):
                action Function(mas_extra_menu.white_mouse_action)

    vbox:

        yalign 1.0

        textbutton _("По умолчанию"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.default_mouse_action)

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.cursor_choice_return)
    label "Курсор"

screen sayori_name_choice():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Сайори"):
                action SetField(persistent, "mas_sayori_name_abb", "Сайори")
            textbutton _("Саёри"):
                action SetField(persistent, "mas_sayori_name_abb", "Саёри")

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.sayori_name_choice_return)
    label "{size=-12}Произношение имени\n(Сейчас: [persistent.mas_sayori_name_abb]){/size}"

screen names_say_choice():
    modal True

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Обычный"):
                action SetField(persistent, "player_abbreviated_name", False)
            textbutton _("Улучшенный"):
                action SetField(persistent, "player_abbreviated_name", True)
    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.names_say_choice_return)


    if persistent.player_abbreviated_name:
        label "{size=-12}Стиль произношения имён\n(Сейчас: улучшенный){/size}"
    else:
        label "{size=-12}Стиль произношения имён\n(Сейчас: обычный){/size}"

screen msr_custom_bg_choice():
    modal True

    key "noshift_Э" action Return
    key "noshift_э" action Return
    key "noshift_'" action Return

    zorder 190

    style_prefix "extra_menu"

    frame:
        style ("extra_menu_outer_frame" if not mas_globals.dark_mode else "extra_menu_outer_frame_dark")

        hbox:

            frame:
                style "extra_menu_navigation_frame"

            frame:
                style "extra_menu_content_frame"

                transclude

        vbox:
            style_prefix "extra_menu"

            xpos gui.navigation_xpos
            spacing gui.navigation_spacing

            textbutton _("Оригинал"):
                action SetField(persistent, "msr_custom_bg", "original")
            textbutton _("Кастомный №1"):
                action SetField(persistent, "msr_custom_bg", "custom1")
            textbutton _("Кастомный №2"):
                action SetField(persistent, "msr_custom_bg", "custom2")
            textbutton _("Кастомный №2.1"):
                action SetField(persistent, "msr_custom_bg", "custom21")
            textbutton _("Кастомный №3"):
                action SetField(persistent, "msr_custom_bg", "custom3")
            textbutton _("Кастомный №4"):
                action SetField(persistent, "msr_custom_bg", "custom4")

    vbox:

        yalign 1.0

        textbutton _("Вернуться"):
            style "extra_menu_return_button"
            action Function(mas_extra_menu.msr_custom_bg_return)
    if persistent.msr_custom_bg == 'original':
        label "{size=-12}Кастомизация фона\n(Сейчас: Оригинал){/size}"
    elif persistent.msr_custom_bg == 'custom1':
        label "{size=-12}Кастомизация фона\n(Сейчас: Кастомный №1){/size}"
    elif persistent.msr_custom_bg == 'custom2':
        label "{size=-12}Кастомизация фона\n(Сейчас: Кастомный №2){/size}"
    elif persistent.msr_custom_bg == 'custom21':
        label "{size=-12}Кастомизация фона\n(Сейчас: Кастомный №2.1){/size}"
    elif persistent.msr_custom_bg == 'custom3':
        label "{size=-12}Кастомизация фона\n(Сейчас: Кастомный №3){/size}"
    elif persistent.msr_custom_bg == 'custom4':
        label "{size=-12}Кастомизация фона\n(Сейчас: Кастомный №4){/size}"

style extra_menu_return_button_text is navigation_button_text
style extra_menu_prev_button_text is navigation_button_text:
    min_width 135
    text_align 1.0
style extra_menu_outer_frame is game_menu_outer_frame
style extra_menu_outer_frame_dark is game_menu_outer_frame
style extra_menu_navigation_frame is game_menu_navigation_frame
style extra_menu_content_frame is game_menu_content_frame
style extra_menu_viewport is game_menu_viewport
style extra_menu_side is game_menu_side
style extra_menu_label is game_menu_label
style extra_menu_label_dark is game_menu_label_dark
style extra_menu_label_text is game_menu_label_text
style extra_menu_label_text_dark is game_menu_label_text_dark

style extra_menu_return_button is return_button:
    xminimum 0
    xmaximum 200
    xfill False

style extra_menu_prev_button is return_button:
    xminimum 0
    xmaximum 135
    xfill False

style extra_menu_outer_frame:
    background "mod_assets/extra/extra_menu_frame.png"

style extra_menu_outer_frame_dark:
    background "mod_assets/extra/extra_menu_frame_d.png"

style extra_menu_button is navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style extra_menu_button_text is navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/Halogen.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

init -1 style extra_menu_button_dark is navigation_button_dark:
    size_group "navigation"
    properties gui.button_properties("navigation_button_dark")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

init -1 style extra_menu_button_text_dark is navigation_button_text_dark:
    properties gui.button_text_properties("navigation_button_dark")
    font "gui/font/RifficFree-Bold.ttf"
    color "#FFD9E8"
    outlines [(4, "#DE367E", 0, 0), (2, "#DE367E", 2, 2)]
    hover_outlines [(4, "#FF80B7", 0, 0), (2, "#FF80B7", 2, 2)]
    insensitive_outlines [(4, "#FFB2D4", 0, 0), (2, "#FFB2D4", 2, 2)]

style msr_extra_menu_return_button_text is navigation_button_text
style msr_extra_menu_prev_button_text is navigation_button_text:
    min_width 135
    text_align 1.0
style msr_extra_menu_outer_frame is game_menu_outer_frame
style msr_extra_menu_navigation_frame is game_menu_navigation_frame
style msr_extra_menu_content_frame is game_menu_content_frame
style msr_extra_menu_viewport is game_menu_viewport
style msr_extra_menu_side is game_menu_side
style msr_extra_menu_label is game_menu_label
style msr_extra_menu_label_text is game_menu_label_text

style msr_extra_menu_return_button is return_button:
    xminimum 0
    xmaximum 200
    xfill False

style msr_extra_menu_prev_button is return_button:
    xminimum 0
    xmaximum 135
    xfill False

style msr_extra_menu_outer_frame:
    background "mod_assets/extra/extra_menu_frame.png"

style msr_extra_menu_button is navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style msr_extra_menu_button_text is navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/Halogen.ttf"
    color "#fff"
    outlines [(4, "#2D7D34", 0, 0), (2, "#2D7D34", 2, 2)]
    hover_outlines [(4, "#2AAA34", 0, 0), (2, "#2AAA34", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]


transform mas_console_move(x, y):
    on show:
        xpos x-500 ypos y alpha 0.0
        ease 1.0 xpos x alpha 1.0
    on hide:
        xalign x ypos y alpha 1.0
        ease 1.0 xpos x-500 alpha 0.0

transform mas_buttons_move(x, y):
    on show:
        xpos x ypos y+100 alpha 0.0 yanchor 1.0
        ease 1.0 ypos y alpha 1.0
    on hide:
        xpos x ypos y alpha 1.0 yanchor 1.0
        ease 1.0 ypos y+100 alpha 0.0

transform mas_buttons_color_move(x, y):
    on show:
        xpos x ypos y+30 alpha 0.0 yanchor 1.0
        ease 1.0 ypos y alpha 1.0
    on hide:
        xpos x ypos y alpha 1.0 yanchor 1.0
        ease 1.0 ypos y+30 alpha 0.0

transform mas_buttons_message_move(x, y):
    on show:
        xpos x ypos y+60 alpha 0.0 yanchor 1.0
        ease 1.0 ypos y alpha 1.0
    on hide:
        xpos x ypos y alpha 1.0 yanchor 1.0
        ease 1.0 ypos y+60 alpha 0.0

transform mas_indicator_move(x, y):
    on show:
        xpos x ypos y-100 alpha 0.0 yanchor 1.0
        ease 1.0 ypos y alpha 1.0
    on hide:
        xpos x ypos y alpha 1.0 yanchor 1.0
        ease 1.0 ypos y-100 alpha 0.0

transform mas_xypos(xp=0.5, yp=1.0, time=0.0):
    ease time xpos xp ypos yp

label msr_show_all_variables:
    $ MSR.ShowAffIndicator()
    $ MSR.ShowRandomConsents()

    if not mas_globals.dark_mode:
        if persistent.mas_window_color == "red":
            $ style.say_window = style.window_red
            $ style.say_label = style.say_label_red
        elif persistent.mas_window_color == "orange":
            $ style.say_window = style.window_orange
            $ style.say_label = style.say_label_orange
        elif persistent.mas_window_color == "yellow":
            $ style.say_window = style.window_yellow
            $ style.say_label = style.say_label_yellow
        elif persistent.mas_window_color == "gray":
            $ style.say_window = style.window_gray
            $ style.say_label = style.say_label_gray
        elif persistent.mas_window_color == "seroburomaline":
            $ style.say_window = style.window_seroburomaline
            $ style.say_label = style.say_label_seroburomaline
        elif persistent.mas_window_color == "chocolate":
            $ style.say_window = style.window_chocolate
            $ style.say_label = style.say_label_chocolate
        elif persistent.mas_window_color == "tomato":
            $ style.say_window = style.window_tomato
            $ style.say_label = style.say_label_tomato
        elif persistent.mas_window_color == "green":
            $ style.say_window = style.window_green
            $ style.say_label = style.say_label_green
        elif persistent.mas_window_color == "crimson":
            $ style.say_window = style.window_crimson
            $ style.say_label = style.say_label_crimson
        elif persistent.mas_window_color == "white":
            $ style.say_window = style.window_white
            $ style.say_label = style.say_label_white
        else:
            $ style.say_window = style.window
            $ style.say_label = style.say_label
    else:
        $ store.style.say_window = store.style.window
        $ store.style.say_label = store.style.say_label_white




    if persistent.mas_mouse_color == "red":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse1.png", 0, 0)]}
    elif persistent.mas_mouse_color == "yellow":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse2.png", 0, 0)]}
    elif persistent.mas_mouse_color == "orange":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse3.png", 0, 0)]}
    elif persistent.mas_mouse_color == "gray":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse4.png", 0, 0)]}
    elif persistent.mas_mouse_color == "blue":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse5.png", 0, 0)]}
    elif persistent.mas_mouse_color == "purple":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse6.png", 0, 0)]}
    elif persistent.mas_mouse_color == "chocolate":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse7.png", 0, 0)]}
    elif persistent.mas_mouse_color == "pink":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse8.png", 0, 0)]}
    elif persistent.mas_mouse_color == "green":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse9.png", 0, 0)]}
    elif persistent.mas_mouse_color == "blue2":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse10.png", 0, 0)]}
    elif persistent.mas_mouse_color == "white":
        $ config.mouse = {'default' : [("mod_assets/extra/cursors/mouse11.png", 0, 0)]}
    else:
        $ config.mouse = None




    $ mas_attempts_parody = 0
    $ mas_attempts_parody_sayori = False
    $ mas_attempts_parody_yuri = False
    $ mas_attempts_parody_natsuki = False
    $ mas_parody_all = False


    $ page_name_value = FilePageNameInputValue(pattern=u'Страница {}')
    $ monika_name = persistent._mas_monika_nickname
    $ y_name = "Юри"
    $ bday_name = "Имя"
    $ tempinstrument = "Инструмент"
    $ player_abb = player
    call mas_set_gender
    call mas_name_cases
    if renpy.android:
        $ monika_device_name = "телефон"
    else:
        $ monika_device_name = "компьютер"

    if renpy.seen_label('preferredname'):
        $ evhand.event_database["monika_changename"].unlocked = True

    if not persistent.mas_chess_unlocked_ch30_autoload:
        $ persistent.mas_chess_unlocked_ch30_autoload = True
        $ persistent._mas_chess_timed_disable = None
    if renpy.seen_label('unlock_chess'):
        $ mas_unlockGame("шахматы")
    if renpy.seen_label('unlock_piano'):
        $ mas_unlockGame("пианино")

    if persistent._mas_player_bday == "Имя":
        $ persistent._mas_player_bday == None
        $ persistent._mas_mood_bday_last = None
        $ persistent._mas_mood_bday_lies = 0
        $ persistent._mas_mood_bday_locked = False

    if not persistent.mas_rain_unlocked_ch30_autoload:
        if renpy.seen_label('monika_rain'):
            $ persistent.mas_rain_unlocked_ch30_autoload = True
            $ mas_is_raining = False
            $ persistent._mas_likes_rain = True
            $ lockEventLabel("monika_rain_stop")
            $ unlockEventLabel("monika_rain_holdme")
            $ unlockEventLabel("monika_rain_start")
            $ unlockEventLabel("monika_rain")





    return
