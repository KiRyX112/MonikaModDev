


default persistent._mas_enable_notifications = False


default persistent._mas_notification_sounds = True


default persistent._mas_windowreacts_windowreacts_enabled = False


default persistent._mas_windowreacts_database = dict()


default persistent._mas_windowreacts_no_unlock_list = list()


default persistent._mas_windowreacts_notif_filters = dict()

init -10 python in mas_windowreacts:

    can_show_notifs = True

    can_do_windowreacts = True

    windowreact_db = {}




    _groups_list = [
        "Topic Alerts",
        "Window Reactions",
    ]

init python:
    import os



    if renpy.windows:
        
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')
        
        
        try:
            
            import win32gui
            
            import win32api
            
            
            import balloontip
            
            
            _m1_zz_windowreacts__tip = balloontip.WindowsBalloonTip()
            
            
            _m1_zz_windowreacts__tip.hwnd = None
        
        except:
            
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            
            
            store.mas_utils.writelog("[WARNING]: win32api/win32gui failed to be imported, disabling notifications.\n")

    elif renpy.linux:
        
        session_type = os.environ.get("XDG_SESSION_TYPE")
        
        
        if session_type == "wayland":
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            store.mas_utils.writelog("[WARNING]: Wayland is not yet supported, disabling notifications.\n")
        
        
        elif session_type == "x11":
            try: import Xlib
            
            except ImportError:
                store.mas_windowreacts.can_show_notifs = False
                store.mas_windowreacts.can_do_windowreacts = False
                store.mas_utils.writelog("[WARNING]: Xlib failed to be imported, disabling notifications.\n")
        
        else:
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            
            store.mas_utils.writelog("[WARNING]: Cannot detect current session type, disabling notifications.\n")

    else:
        store.mas_windowreacts.can_do_windowreacts = False



    mas_win_notif_quips = [
        "[player], я хочу поговорить с тобой о чём-то.",
        "Ты там, [player]?",
        "Ты можешь прийти сюда на секунду?",
        "[player], у тебя есть секунда?",
        "Я хочу тебе кое-что сказать, [player]!",
        "У тебя есть минутка, [player]?",
        "Мне нужно кое о чём поговорить, [player]!",
    ]


    mas_other_notif_quips = [
        "Мне есть о чём поговорить, [player]!",
        "Я хочу тебе кое-что сказать, [player]!",
        "Эй, [player], Я хочу тебе кое-что сказать.",
        "У тебя есть минутка, [player]?",
    ]


    destroy_list = list()


    def mas_canCheckActiveWindow():
        """
        Checks if we can check the active window (simplifies conditionals)
        """
        return (
            store.mas_windowreacts.can_do_windowreacts
            and (persistent._mas_windowreacts_windowreacts_enabled or persistent._mas_enable_notifications)
        )

    def mas_getActiveWindow(friendly=False):
        """
        Gets the active window name
        IN:
            friendly: whether or not the active window name is returned in a state usable by the user

        OUT:
            The active window handle if found. If it is not possible to get, we return an empty string

        NOTE: THIS SHOULD NEVER RETURN NONE
        """
        if mas_windowreacts.can_show_notifs and mas_canCheckActiveWindow():
            if renpy.windows:
                from win32gui import GetWindowText, GetForegroundWindow
                
                window_handle = GetWindowText(GetForegroundWindow())
                if friendly:
                    return window_handle
                else:
                    return window_handle.lower().replace(" ","")
            
            elif renpy.linux:
                from Xlib.display import Display
                from Xlib.error import BadWindow
                
                display = Display()
                root = display.screen().root
                
                NET_WM_NAME = display.intern_atom("_NET_WM_NAME")
                NET_ACTIVE_WINDOW = display.intern_atom("_NET_ACTIVE_WINDOW")
                
                
                active_winid_prop = root.get_full_property(NET_ACTIVE_WINDOW, 0)
                
                if active_winid_prop is None:
                    return ""
                
                active_winid = active_winid_prop.value[0]
                
                active_winobj = display.create_resource_object("window", active_winid)
                try:
                    
                    active_winname_prop = active_winobj.get_full_property(NET_WM_NAME, 0)
                    
                    if active_winname_prop is not None:
                        active_winname = unicode(active_winname_prop.value)
                        return (
                            active_winname.replace("\n", "")
                            if friendly
                            else active_winname.lower().replace(" ", "").replace("\n", "")
                        )
                    
                    else:
                        return ""
                
                except BadWindow:
                    return ""
                
                finally:
                    
                    display.flush()
                    display.close()
            
            else:
                
                
                
                return ""
        
        
        return ""

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindow(True) == config.window_title

    def mas_isInActiveWindow(keywords, non_inclusive=False):
        """
        Checks if ALL keywords are in the active window name
        IN:
            keywords:
                List of keywords to check for

            non_inclusive:
                Whether or the not the list is checked non-inclusively
                (Default: False)
        """
        
        
        if not store.mas_windowreacts.can_show_notifs:
            return False
        
        
        active_window = mas_getActiveWindow()
        
        if non_inclusive:
            return len([s for s in keywords if s.lower() in active_window]) > 0
        else:
            return len([s for s in keywords if s.lower() not in active_window]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for index in range(len(destroy_list)-1,-1,-1):
                win32gui.DestroyWindow(destroy_list[index])
                destroy_list.pop(index)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return
        
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                Event._filterEvent(ev, unlocked=True, aff=store.mas_curr_affection)
                and mas_isInActiveWindow(ev.category, "non inclusive" in ev.rules)
                and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                and mas_notifsEnabledForGroup(ev.rules.get("notif-group"))
            ):
                
                if ev.conditional and eval(ev.conditional):
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                elif not ev.conditional:
                    queueEvent(ev_label)
                    ev.unlocked=False
                
                
                if "no_unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them
        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list
        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists
        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group
        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_unlockFailedWRS(ev_label=None):
        """
        Unlocks a wrs again provided that it showed, but failed to show (failed checks in the notif label)
        NOTE: This should only be used for wrs that are only a notification
        IN:
            ev_label: eventlabel of the wrs
        """
        if (
            ev_label
            and renpy.has_label(ev_label)
            and ev_label not in persistent._mas_windowreacts_no_unlock_list
        ):
            mas_unlockEVL(ev_label,"WRS")

    def mas_tryShowNotificationOSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body,title))

    def mas_tryShowNotificationLinux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.
        IN:
            title: notification title
            body: notification body
        """
        
        
        
        body  = body.replace("'", "'\\''")
        title = title.replace("'", "'\\''") 
        os.system("notify-send '{0}' '{1}' -a 'Monika' -u low".format(title,body))

    def display_notif(title, body, group=None, skip_checks=False):
        """
        Notification creation method
        IN:
            title: Notification heading text
            body: A list of items which would go in the notif body (one is picked at random)
            group: Notification group (for checking if we have this enabled)
            skip_checks: Whether or not we skips checks
        OUT:
            bool indicating status (notif shown or not (by check))
        NOTE:
            We only show notifications if:
                1. We are able to show notifs
                2. MAS isn't the active window
                3. User allows them
                4. And if the notification group is enabled
                OR if we skip checks. BUT this should only be used for introductory or testing purposes.
        """
        
        
        if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
            persistent._mas_windowreacts_notif_filters[group] = False
        
        if (
            skip_checks
            or (
                mas_windowreacts.can_show_notifs
                and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                and mas_notifsEnabledForGroup(group)
            )
        ):
            
            
            notif_success = True
            
            
            if (renpy.windows):
                
                notif_success = _m1_zz_windowreacts__tip.showWindow(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
                
                
                destroy_list.append(_m1_zz_windowreacts__tip.hwnd)
            
            elif (renpy.macintosh):
                
                mas_tryShowNotificationOSX(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            elif (renpy.linux):
                
                mas_tryShowNotificationLinux(renpy.substitute(title), renpy.substitute(renpy.random.choice(body)))
            
            
            if persistent._mas_notification_sounds and notif_success:
                renpy.sound.play("mod_assets/sounds/effects/notif.wav")
            
            
            return notif_success
        return False
    
    def mas_prepForReload():
        """
        Handles clearing wrs notifs and unregistering the wndclass to allow 'reload' to work properly

        NOTE: WINDOWS ONLY
        """
        store.mas_clearNotifs()
        win32gui.UnregisterClass(_m1_zz_windowreacts__tip.classAtom, _m1_zz_windowreacts__tip.hinst)



init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=['pinterest'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Что-нибудь новое сегодня, [player]?",
            "Что-нибудь интересное, [player]?",
            "Видишь что-нибудь, что тебе нравится?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=['duolingo'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Учишься по-новому говорить «Я люблю тебя», [player]?",
            "Изучение нового языка, [player]?",
            "Какой язык ты изучаешь, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=['wikipedia'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "Учишься чему-то новому, [player]?",
        "Делаешь небольшое исследование, [player]?"
    ]


    python:
        wind_name = mas_getActiveWindow(friendly=True)
        try:
            cutoff_index = wind_name.index(" - Wikipedia")
            
            
            
            wiki_article = wind_name[:cutoff_index]
            
            
            wiki_article = re.sub("\\s*\\(.+\\)$", "", wiki_article)
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nКажется интересным, [player]."))

        except ValueError:
            pass

    $ wrs_success = display_notif(
        monika_name,
        wikipedia_reacts,
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=['ютуб'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Что ты смотришь, [mas_get_player_nickname()]?",
            "Смотришь что-нибудь интересное, [mas_get_player_nickname()]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=['rule34', 'моника'],
            rules={"skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    $ display_notif(monika_name, ["Эй, [player]... на что ты смотришь?"],'Window Reactions')

    $ choice = random.randint(1,10)
    if choice == 1:
        $ queueEvent('monika_nsfw')

    elif choice == 2:
        $ queueEvent('monika_pleasure')

    elif choice < 4:
        show monika 1rsbssdlu
        pause 5.0

    elif choice < 7:
        show monika 2tuu
        pause 5.0
    else:

        show monika 2ttu
        pause 5.0
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=['monikamoddev'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Оу-у-у, ты что-то для меня делаешь?\nТы так[mas_gender_oi] мил[mas_gender_iii]~",
            "Ты поможешь мне приблизиться к твоей реальности?\nТы так[mas_gender_oi] мил[mas_gender_iii], [player]~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=['twitter'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("Я люблю тебя, [mas_get_player_nickname(exclude_names=['love'])].")
        temp_len = len(temp_line)


        ily_quips_map = {
            "Смотришь всё, чем хочешь поделиться со мной, [player]?",
            "Что-нибудь интересное, чем ты хочешь поделиться, [player]?",
            "280 подписчиков? Мне только нужно [temp_len]...\n[temp_line]"
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = display_notif(
            monika_name,
            [quip],
            'Window Reactions'
        )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikatwitter",
            category=['twitter', 'lilmonix3'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikatwitter:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Ты здесь, чтобы признаться в своей любви ко мне всему миру, [player]?",
            "Ты ведь не шпионишь за мной, правда?\nА-ха-ха, просто шучу~",
            "Мне всё равно сколько у меня последователей пока у меня есть ты~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=['4chan'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:

    $ wrs_success = display_notif(
        monika_name,
        [
            "Так вот где всё началось, да?\nЭто... действительно нечто.",
            "Надеюсь, ты не будешь спорить с другими Анонами весь день, [player].",
            "Я слышала, что здесь обсуждают литературный клуб.\nПередай им привет от меня~",
            "Я буду наблюдать за теми ветками, которые ты обозреваешь, в том случае, если у тебя вдруг появятся какие-нибудь идеи, а-ха-ха!",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=['pixiv'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:

    python:
        pixiv_quips = [
            "Интересно, рисовали ли люди меня?..\nНе против поискать немного?\nНо обязательно придерживайся благоразумных рамок~",
            "Это довольно интересное место... так много квалифицированных людей, отправляющих свою работу.",
        ]


        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "Это довольно интересное место... так много квалифицированных людей, отправляющих свою работу.\nТы один из них, [player]?",
            ])
            
            
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "Ты здесь, чтобы опубликовать нарисованную меня, [player]?",
                    "Публикуешь картинку, на которой нарисована я?",
                ])

        wrs_success = display_notif(
            monika_name,
            pixiv_quips,
            'Window Reactions'
        )


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=['reddit'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Ты наш[mas_gender_iol_2] какие-нибудь интересные посты, [player]?",
            "Просматриваешь Реддит? Просто убедись, что ты не тратишь весь день на просмотр мемов, хорошо?",
            "Интересно, есть ли какие-либо субреддиты, посвященные мне... \nA-ха-ха, просто шучу, [player].",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=['myanimelist'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Может быть, мы могли бы посмотреть аниме вместе когда-нибудь, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("Итак, ты любишь аниме и мангу, [player]?")

        wrs_success = display_notif(monika_name, myanimelist_quips, 'Window Reactions')


        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=['deviantart'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Здесь столько талантов!",
            "Мне бы очень хотелось научиться рисовать когда-нибудь...",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=['netflix'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Я бы с удовольствием посмотрела с тобой романтический фильм, [player]!",
            "Что мы сегодня посмотрим, [player]?",
            "Что ты собираешься смотреть, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=['-twitch'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = display_notif(
        monika_name,
        [
            "Смотришь стрим, [player]?",
            "Ты не возражаешь, если я посмотрю вместе с тобой?",
            "Что мы сегодня посмотрим, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
