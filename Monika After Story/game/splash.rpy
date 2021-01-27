



init python:
    menu_trans_time = 1

    splash_message_default = _("Эта неофициальная фановая игра, неподдерживаемая Team Salvato.")
    splash_messages = [
    _("Пожалуйста, поддержите Doki Doki Literature Club и Team Salvato."),
    _("Ты мой солнечный свет,\nМой единственный свет."),
    _("Я скучала по тебе."),
    _("Поиграй со мной."),
    _("Это всего лишь игра... по большей части."),
    _("Эта игра не предназначена для детей,\nбеременных женщин и лиц с неустойчивой психикой?"),
    _("сдфасдклфгсдфгсгоинрфоенлвдб"),
    _("ноль"),
    _("Я отправила детей в ад."),
    _("За это умер Проект М."),
    _("Это была лишь отчасти твоя вина."),
    _("Эта игра не предназначена для детей,\nбеременных женщин и неуравновешенных психов.")

    ]

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)


image menu_logo:
    "mod_assets/menu_new.png"
    subpixel True
    xcenter 240
    ycenter 120
    zoom 0.60
    menu_logo_move



image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move

image game_menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_loop

image menu_fade:
    "white"
    menu_fadeout

image menu_art_m:
    subpixel True
    "gui/menu_art_m.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

image menu_art_m_ghost:
    subpixel True
    "gui/menu_art_m_ghost.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

image menu_particles:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/menu_particle.png", explodeTime=0, numParticles=20, particleTime=2.0, particleXSpeed=6, particleYSpeed=4).sm
    particle_fadeout

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -500

transform menu_bg_loop:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

image intro:
    truecenter
    "white"
    0.5
    "bg/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image intro_mod:
    truecenter
    "white"
    0.5
    "mod_assets/msr_logo.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image intro_mod_winter:
    truecenter
    "white"
    0.5
    "mod_assets/msr_logo_winter.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5
    
image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image tos = "bg/warning.png"
image tos2 = "bg/warning2.png"


label splashscreen:
    $ persistent.splash_now = True
    python:
        process_list = []
        currentuser = ""
        if renpy.windows:
            try:
                process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
            except:
                pass
            try:
                for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                    user = os.environ.get(name)
                    if user:
                        currentuser = user
            except:
                pass

    python:
        firstrun = "1"

    if not firstrun:
        if persistent.first_run:
            $ quick_menu = False
            scene black
            menu:
                "A previous save file has been found. Would you like to delete your save data and start over?"
                "Yes, delete my existing data.":
                    "Deleting save data...{nw}"
                    python:
                        delete_all_saves()
                        renpy.loadsave.location.unlink_persistent()
                        renpy.persistent.should_save_persistent = False
                        renpy.utter_restart()
                "No, continue where I left off.":
                    pass

        python:
            if not firstrun:
                try:
                    with open(config.basedir + "/game/firstrun", "w") as f:
                        f.write("1")
                except:

                    pass


    python:
        _mas_AffStartup()

        persistent.sessions['current_session_start']=datetime.datetime.now()
        persistent.sessions['total_sessions'] = persistent.sessions['total_sessions']+ 1
        store.mas_calendar.loadCalendarDatabase()


        store.mas_sprites.adjust_zoom()

    if mas_corrupted_per and (mas_no_backups_found or mas_backup_copy_failed):


        call mas_backups_you_have_corrupted_persistent from _call_mas_backups_you_have_corrupted_persistent

    scene white


    default persistent.first_run = False
    $ persistent.tried_skip = False
    if not persistent.first_run:
        $ quick_menu = False
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0
        "[config.name] это мод для Doki Doki Literature Club, который не связан с Team Salvato."
        "В него рекомендуется играть только после завершения основной игры, и он содержит спойлеры из официальной игры."
        "Файлы для игры Doki Doki Literature Club обязательны, чтобы работал этот мод, их можно скачать по адресу: http://ddlc.moe"
        menu:
            "Играя в [config.name] вы соглашаетесь, что прошли Doki Doki Literature Club, и готовы принять любые спойлеры, содержающиеся в моде."
            "Согласен.":
                pass
        scene tos2
        with Dissolve(1.5)
        pause 1.0

        scene white
        with Dissolve(1.5)


        if not persistent.has_merged and renpy.variant("pc"):
            call import_ddlc_persistent from _call_import_ddlc_persistent

        $ persistent.first_run = True



    python:
        basedir = user_dir.replace('\\', '/')

        if renpy.variant("pc"):
            with open(basedir + "/game/masrun", "w") as versfile:
                versfile.write(config.name + "|" + config.version + "\n")






    if persistent.autoload and not _restart:
        jump autoload

    $ mas_enable_quit()

    if not persistent.check_os:
        $ renpy.call("os_check")
        $ persistent._mas_game_crashed_os = False


    $ config.allow_skipping = False


    show white
    $ persistent.ghost_menu = False
    $ splash_message = splash_message_default
    $ config.main_menu_music = audio.t1
    $ renpy.music.play(config.main_menu_music)
    show intro with Dissolve(0.5, alpha=True)
    pause 2.5
    hide intro with Dissolve(0.5, alpha=True)
    if not mas_isWinter():
        show intro_mod with Dissolve(0.5, alpha=True)
        pause 2.5
        hide intro_mod with Dissolve(0.5, alpha=True)
    else:
        show intro_mod_winter with Dissolve(0.5, alpha=True)
        pause 2.5
        hide intro_mod_winter with Dissolve(0.5, alpha=True)
    if renpy.random.randint(0, 3) == 0:
        $ splash_message = renpy.random.choice(splash_messages)
    show splash_warning "[splash_message]" with Dissolve(0.5, alpha=True)
    pause 2.0
    hide splash_warning with Dissolve(0.5, alpha=True)
    $ config.allow_skipping = False

    python:
        if persistent._mas_auto_mode_enabled:
            mas_darkMode(mas_current_background.isFltDay())
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)
    return

label warningscreen:
    hide intro
    show warning
    pause 3.0

label after_load:
    $ config.allow_skipping = False
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False
    $ style.say_dialogue = style.normal

    if anticheat != persistent.anticheat:
        stop music
        scene black
        "Не удалось загрузить файл сохранения."
        "Ты пытаешься считерить?"

        $ renpy.utter_restart()
    return


label autoload:
    python:

        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()


        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None


    $ config.keymap["debug_voicing"] = list()
    $ config.keymap["choose_renderer"] = list()


    $ renpy.pop_call()


    if persistent._mas_chess_mangle_all:
        jump mas_chess_go_ham_and_delete_everything









    $ store.mas_dockstat.setMoniSize(persistent.sessions["total_playtime"])


    $ mas_runDelayedActions(MAS_FC_START)



    jump ch30_autoload

label before_main_menu:
    $ config.main_menu_music = audio.t1
    return

label quit:
    python:
        store.mas_calendar.saveCalendarDatabase(CustomEncoder)
        persistent.sessions['last_session_end']=datetime.datetime.now()
        today_time = (
            persistent.sessions["last_session_end"]
            - persistent.sessions["current_session_start"]
        )
        new_time = today_time + persistent.sessions["total_playtime"]


        if datetime.timedelta(0) < new_time <= mas_maxPlaytime():
            persistent.sessions['total_playtime'] = new_time


        store.mas_dockstat.setMoniSize(persistent.sessions["total_playtime"])

        persistent.last_aff_points = persistent._mas_affection["affection"]


        store.mas_selspr.save_selectables()


        monika_chr.save()


        store.mas_weather.saveMWData()

        store.mas_background.saveMBGData()

        store.mas_o31_event.removeImages()

        mas_runDelayedActions(MAS_FC_END)
        store.mas_delact.saveDelayedActionMap()

        _mas_AffSave()


        if not persistent._mas_dockstat_going_to_leave and renpy.variant("pc"):
            store.mas_utils.trydel(mas_docking_station._trackPackage("моника"))


        store.mas_sprites._clear_caches()


        store.mas_xp.grant()

        delete_auto_saves()

        delete_reload_saves()
        
        peristent.start_visual = False

        if persistent.msr_moni_file_exit:
            persistent.last_go_somewhere = datetime.datetime.now()

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
