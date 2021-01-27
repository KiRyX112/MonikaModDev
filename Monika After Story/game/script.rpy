





label start:


    $ anticheat = persistent.anticheat


    $ chapter = 0


    $ _dismiss_pause = config.developer


    $ s_name = "Сайори"
    $ monika_name = "Моника"
    $ n_name = "Нацуки"
    $ y_name = "Юри"

    $ style.say_dialogue = style.normal
    $ quick_menu = True

    $ allow_skipping = True
    $ config.allow_skipping = True

    #Jump to the space room.
    if persistent.autoload:
        #Stop the title screen music
        stop music
        jump ch30_preloop
    jump ch30_main

label endgame(pause_length=4.0):
    $ quick_menu = False
    stop music fadeout 2.0
    scene black
    show end
    with dissolve_scene_full
    pause pause_length
    $ quick_menu = True
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
