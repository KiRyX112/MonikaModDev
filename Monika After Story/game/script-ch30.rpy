init python:
    class RectCluster(object):
        def __init__(self, theDisplayable, numRects=12, areaWidth = 30, areaHeight = 30):
            self.sm = SpriteManager(update=self.update)
            self.rects = [ ]
            self.displayable = theDisplayable
            self.numRects = numRects
            self.areaWidth = areaWidth
            self.areaHeight = areaHeight

            for i in range(self.numRects):
                self.add(self.displayable)

        def add(self, d):
            s = self.sm.create(d)
            s.x = (random.random() - 0.5) * self.areaWidth * 2
            s.y = (random.random() - 0.5) * self.areaHeight * 2
            s.width = random.random() * self.areaWidth / 2
            s.height = random.random() * self.areaHeight / 2
            self.rects.append(s)

        def update(self, st):
            for s in self.rects:
                s.x = (random.random() - 0.5) * self.areaWidth * 2
                s.y = (random.random() - 0.5) * self.areaHeight * 2
                s.width = random.random() * self.areaWidth / 2
                s.height = random.random() * self.areaHeight / 2
            return 0

default persistent.monika_reload = 0
default persistent.tried_skip = False
default persistent.monika_kill = True
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False
define mas_in_intro_flow = False


default persistent._mas_disable_animations = False

init -998 python:

    if "unstable" in config.version and not persistent.sessions:
        raise Exception(
            _("Нестабильный режим файлов в установке на первом сеансе. Это может вызвать проблемы.\n"
            "Пожалуйста, переустановите последнюю стабильную версию Monika After Story, чтобы убедиться, что не будет никаких проблем с данными.")
        )

init -890 python in mas_globals:
    import datetime
    import store


    tt_detected = (
        store.mas_getLastSeshEnd() - datetime.datetime.now()
            > datetime.timedelta(hours=30)
    )

    if tt_detected:
        store.persistent._mas_pm_has_went_back_in_time = True
    
    is_r7 = renpy.version(True)[0] == 7


    is_steam = "steamapps" in renpy.config.basedir.lower()

init -1 python in mas_globals:



    dlg_workflow = False

    show_vignette = False


    show_lightning = False


    lightning_chance = 16
    lightning_s_chance = 10


    show_s_light = False


    text_speed_enabled = False


    in_idle_mode = False


    late_farewell = False


    last_minute_dt = datetime.datetime.now()


    last_hour = last_minute_dt.hour


    last_day = last_minute_dt.day


    time_of_day_4state = None


    time_of_day_3state = None


    returned_home_this_sesh = bool(store.persistent._mas_moni_chksum)

    this_ev = None


init 970 python:
    import store.mas_filereacts as mas_filereacts



    if persistent._mas_moni_chksum is not None:
        
        
        
        store.mas_dockstat.init_findMonika(mas_docking_station)


init -10 python:

    class MASIdleMailbox(store.MASMailbox):
        """
        Spaceroom idle extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties
        """
        
        
        REBUILD_EV = 1
        
        
        DOCKSTAT_GRE_TYPE = 2
        
        
        IDLE_MODE_CB_LABEL = 3
        
        
        SKIP_MID_LOOP_EVAL = 4
        
        
        SCENE_CHANGE = 5
        
        
        
        
        
        def __init__(self):
            """
            Constructor for the idle mailbox
            """
            super(MASIdleMailbox, self).__init__()
        
        
        def send_rebuild_msg(self):
            """
            Sends the rebuild message to the mailbox
            """
            self.send(self.REBUILD_EV, True)
        
        def get_rebuild_msg(self):
            """
            Gets rebuild message
            """
            return self.get(self.REBUILD_EV)
        
        def send_ds_gre_type(self, gre_type):
            """
            Sends greeting type to mailbox
            """
            self.send(self.DOCKSTAT_GRE_TYPE, gre_type)
        
        def get_ds_gre_type(self, default=None):
            """
            Gets dockstat greeting type

            RETURNS: None by default
            """
            result = self.get(self.DOCKSTAT_GRE_TYPE)
            if result is None:
                return default
            return result
        
        def send_idle_cb(self, cb_label):
            """
            Sends idle callback label to mailbox
            """
            self.send(self.IDLE_MODE_CB_LABEL, cb_label)
        
        def get_idle_cb(self):
            """
            Gets idle callback label
            """
            return self.get(self.IDLE_MODE_CB_LABEL)
        
        def send_skipmidloopeval(self):
            """
            Sends skip mid loop eval message to mailbox
            """
            self.send(self.SKIP_MID_LOOP_EVAL, True)
        
        def get_skipmidloopeval(self):
            """
            Gets skip midloop eval value
            """
            return self.get(self.SKIP_MID_LOOP_EVAL)
        
        def send_scene_change(self):
            """
            Sends scene change message to mailbox
            """
            self.send(self.SCENE_CHANGE, True)
        
        def get_scene_change(self):
            """
            Gets scene change value
            """
            return self.get(self.SCENE_CHANGE)


    mas_idle_mailbox = MASIdleMailbox()


image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"



image room_glitch = "images/cg/monika/monika_bg_glitch.png"

init python:

    import subprocess
    import os
    import eliza
    if renpy.variant('pc'):
        import battery
    import datetime
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None 
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

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        
        pass



    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname


    if renpy.variant('pc'):
        mas_battery_supported = battery.is_supported()
    else:
        mas_battery_supported = False



    renpy.music.register_channel(
        "background",
        mixer="amb",
        loop=True,
        stop_on_mute=True,
        tight=True
    )


    renpy.music.register_channel(
        "backsound",
        mixer="amb",
        loop=False,
        stop_on_mute=True
    )


    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump("mas_pick_a_game")


    def mas_getuser():
        """
        Attempts to get the current user

        RETURNS: current user if found, or None if not found
        """
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                return user
        
        return None


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks(dissolve_masks=True):
        """
        Draws the appropriate masks according to the current state of the
        game.

        IN:
            dissolve_masks - True will dissolve masks, False will not
                (Default; True)
        """
        
        renpy.hide("rm")
        
        
        
        mask = mas_current_weather.get_mask()
        
        
        renpy.show(mask, tag="rm")
        
        if dissolve_masks:
            renpy.with_statement(Dissolve(1.0))
    
    def mas_validate_suntimes():
        """
        Validates both persistent and store suntimes are in a valid state.
        Sunrise is always used as the lead if a reset is needed.
        """
        if (
            mas_suntime.sunrise > mas_suntime.sunset
            or persistent._mas_sunrise > persistent._mas_sunset
        ):
            mas_suntime.sunset = mas_suntime.sunrise
            persistent._mas_sunset = persistent._mas_sunrise


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()
        
        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')
        
        renpy.call_in_new_context("mas_start_calendar_read_only")
        
        if store.mas_globals.in_idle_mode:
            
            store.hkb_button.talk_enabled = True
            store.hkb_button.extra_enabled = True
            store.hkb_button.music_enabled = True
        
        else:
            mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                    May happen after "end"
                end -> end of dialogue (user has interacted)
        """
        
        
        
        
        
        
        
        
        if event == "begin":
            store.mas_hotkeys.allow_dismiss = False
        
        
        
        elif event == "slow_done":
            store.mas_hotkeys.allow_dismiss = True




    def mas_isMorning():
        """DEPRECATED
        Checks if it is day or night via suntimes

        NOTE: the wording of this function is bad. This does not literally
            mean that it is morning. USE mas_isDayNow

        RETURNS: True if day, false if not
        """
        return mas_isDayNow()


    def mas_progressFilter():
        """
        Changes filter according to rules.

        Call this when you want to update the filter.

        RETURNS: True upon a filter change, False if not
        """
        curr_flt = store.mas_sprites.get_filter()
        new_flt = mas_current_background.progress()
        store.mas_sprites.set_filter(new_flt)
        
        return curr_flt != new_flt


    def mas_shouldChangeTime():
        """DEPRECATED
        This no longer makes sense with the filtering system.
        """
        return False


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            rain weather to use, or None if we dont want to change weather
        """
        
        chance = random.randint(1,100)
        if mas_isMoniNormal(higher=True):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            if mas_isSpring():
                return mas_weather._determineCloudyWeather(
                    40,
                    15,
                    15,
                    rolled_chance=chance
                )
            
            elif mas_isSummer():
                return mas_weather._determineCloudyWeather(
                    10,
                    6,
                    5,
                    rolled_chance=chance
                )
            
            elif mas_isFall():
                return mas_weather._determineCloudyWeather(
                    30,
                    12,
                    15,
                    rolled_chance=chance
                )
            
            else:
                
                if chance <= 50:
                    return mas_weather_snow
                elif chance <= 70:
                    return mas_weather_overcast
        
        
        elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return mas_weather_overcast
        
        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return mas_weather_rain
        
        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return mas_weather_thunder
        
        return None


    def mas_lockHair():
        """
        Locks all hair topics
        """
        mas_lockEVL("monika_hair_select")


    def mas_seasonalCheck():
        """
        Determines the current season and runs an appropriate programming
        point.

        If the global for season is currently None, then we instead set the
        current season.

        NOTE: this does NOT do progressive programming point execution.
            This is intended for runtime usage only.

        ASSUMES:
            persistent._mas_current_season
        """
        _s_tag = store.mas_seasons._currentSeason()
        
        if persistent._mas_current_season != _s_tag:
            
            _s_pp = store.mas_seasons._season_pp_map.get(_s_tag, None)
            if _s_pp is not None:
                
                
                _s_pp()
                
                
                persistent._mas_current_season = _s_tag


    def mas_resetIdleMode():
        """
        Resets specific idle mode vars.

        This is meant to basically clear idle mode for holidays or other
        things that hijack main flow
        """
        store.mas_globals.in_idle_mode = False
        persistent._mas_in_idle_mode = False
        persistent._mas_idle_data = {}
        mas_idle_mailbox.get_idle_cb()


    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.normal
        store.mas_globals.text_speed_enabled = True


    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.default_monika
        store.mas_globals.text_speed_enabled = False


    def mas_resetTextSpeed(ignoredev=False):
        """
        Sets text speed to the appropriate one depending on global settings

        Rules:
        1 - developer always gets text speed (unless ignoredev is True)
        2 - text speed enabled if affection above happy
        3 - text speed disabled otherwise
        """
        if config.developer and not ignoredev:
            mas_enableTextSpeed()
        
        elif (
                mas_isMoniHappy(higher=True)
                and persistent._mas_text_speed_enabled
            ):
            mas_enableTextSpeed()
        
        else:
            mas_disableTextSpeed()


    def mas_isTextSpeedEnabled():
        """
        Returns true if text speed is enabled
        """
        return store.mas_globals.text_speed_enabled

    def mas_check_player_derand():
        """
        Checks the player derandom lists for events that are not random and derandoms them
        """
        
        derand_list = store.mas_bookmarks_derand.getDerandomedEVLs()
        
        
        for ev_label in derand_list:
            
            ev = mas_getEV(ev_label)
            if ev and ev.random:
                ev.random = False

    def mas_get_player_bookmarks(bookmarked_evls):
        """
        Gets topics which are bookmarked by the player
        Also cleans events which no longer exist

        NOTE: Will NOT add events which fail the aff range check

        IN:
            bookmarked_evls - appropriate persistent variable holding the bookmarked eventlabels

        OUT:
            List of bookmarked topics as evs
        """
        bookmarkedlist = []
        
        
        for index in range(len(bookmarked_evls)-1,-1,-1):
            
            ev = mas_getEV(bookmarked_evls[index])
            
            
            if not ev:
                bookmarked_evls.pop(index)
            
            
            elif ev.unlocked and ev.checkAffection(mas_curr_affection):
                bookmarkedlist.append(ev)
        
        return bookmarkedlist

    def mas_get_player_derandoms(derandomed_evls):
        """
        Gets topics which are derandomed by the player (in check-scrollable-menu format)
        Also cleans out events which no longer exist

        IN:
            derandomed_evls - appropriate variable holding the derandomed eventlabels

        OUT:
            List of player derandomed topics in mas_check_scrollable_menu form
        """
        derandlist = []
        
        
        for index in range(len(derandomed_evls)-1,-1,-1):
            
            ev = mas_getEV(derandomed_evls[index])
            
            
            if not ev:
                derandomed_evls.pop(index)
            
            
            elif ev.unlocked:
                derandlist.append((renpy.substitute(ev.prompt), ev.eventlabel, False, True, False))
        
        return derandlist










































default msr_mas_run = False
default persistent.msr_wine_ribbon_firthrun = True
default persistent.custom_music = None
default persistent._msr_acs_enable_rose = False


label spaceroom(start_bg=None, hide_mask=None, hide_monika=False, dissolve_all=False, dissolve_masks=False, scene_change=False, force_exp=None, hide_calendar=None, day_bg=None, night_bg=None, show_emptydesk=True, progress_filter=True, bg_change_info=None):

    with None
    if mas_globals.time_of_day_4state == "morning":
        $ persistent.mas_monika_good_tod_1 = 'Доброе '
        $ persistent.mas_monika_good_tod_2 = 'утро'
        $ persistent.mas_monika_good_tod = persistent.mas_monika_good_tod_1 + persistent.mas_monika_good_tod_2
    elif mas_globals.time_of_day_4state == "afternoon":
        $ persistent.mas_monika_good_tod_1 = 'Добрый '
        $ persistent.mas_monika_good_tod_2 = 'день'
        $ persistent.mas_monika_good_tod = persistent.mas_monika_good_tod_1 + persistent.mas_monika_good_tod_2
    else:
        $ persistent.mas_monika_good_tod_1 = 'Добрый '
        $ persistent.mas_monika_good_tod_2 = 'вечер'
        $ persistent.mas_monika_good_tod = persistent.mas_monika_good_tod_1 + persistent.mas_monika_good_tod_2

    if hide_mask is None:
        $ hide_mask = store.mas_current_background.hide_masks
    if hide_calendar is None:
        $ hide_calendar = store.mas_current_background.hide_calendar

    $ import store
    $ import store.songs as songs
    $ MSR.ShowAllVariables()





    python:
        if progress_filter and mas_progressFilter():
            
            scene_change = True
            dissolve_all = True

        day_mode = mas_current_background.isFltDay()

    if scene_change:
        scene black

    python:
        monika_room = None




        if scene_change:
            monika_room = mas_current_background.getCurrentRoom()


        if persistent._mas_auto_mode_enabled:
            mas_darkMode(day_mode)
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)


        if hide_monika:
            if show_emptydesk:
                store.mas_sprites.show_empty_desk()

        else:
            if force_exp is None:
                
                if dissolve_all:
                    force_exp = store.mas_affection._force_exp()
                
                else:
                    force_exp = "monika idle"
            
            if not renpy.showing(force_exp):
                renpy.show(force_exp, at_list=[t11], zorder=MAS_MONIKA_Z)
                
                if not dissolve_all:
                    renpy.with_statement(None)


        if not dissolve_all and not hide_mask:
            mas_drawSpaceroomMasks(dissolve_masks)



        if start_bg:
            if not renpy.showing(start_bg):
                renpy.show(start_bg, tag="sp_mas_room", zorder=MAS_BACKGROUND_Z)

        elif monika_room is not None:
            if not renpy.showing(monika_room):
                renpy.show(
                    monika_room,
                    tag="sp_mas_room",
                    zorder=MAS_BACKGROUND_Z
                )
                
                if not hide_calendar:
                    mas_calShowOverlay()
        
        if scene_change and (bg_change_info is None or len(bg_change_info) < 1):
            bg_change_info = store.mas_background.MASBackgroundChangeInfo()
            mas_current_background._entry_deco(None, bg_change_info)


        if bg_change_info is not None:
            if not scene_change:
                for h_adf in bg_change_info.hides.itervalues():
                    h_adf.hide()
            
            for s_tag, s_adf in bg_change_info.shows.iteritems():
                s_adf.show(s_tag)


    if mas_getFirstSesh() + datetime.timedelta(days=31) and renpy.variant('pc'):
        $ mas_unlockGame("шахматы")
    #     $ store.mas_unlockEventLabel("mas_chess", store.evhand.event_database)
    #     $ store.mas_lockEventLabel("mas_unlock_chess", store.evhand.event_database)
    
    if mas_getFirstSesh() + datetime.timedelta(days=40) and renpy.variant('pc'):
        $ mas_unlockGame("пианино")
    #     $ store.mas_unlockEventLabel("mas_piano", store.evhand.event_database)
    #     $ store.mas_lockEventLabel("mas_unlock_piano", store.evhand.event_database)

    $ store.mas_selspr.unlock_clothes(mas_clothes_marisa)
    $ store.mas_selspr.unlock_clothes(mas_clothes_rin)
    if renpy.seen_label('mas_reaction_gift_clothes_orcaramelo_bikini_shell'):
        $ store.mas_selspr.unlock_clothes(mas_clothes_bikini_shell)
    if renpy.seen_label('mas_reaction_gift_clothes_velius94_shirt_pink'):
        $ store.mas_selspr.unlock_clothes(mas_clothes_shirt_pink)
    if renpy.seen_label('mas_reaction_gift_clothes_finale_shirt_blue'):
        $ store.mas_selspr.unlock_clothes(mas_clothes_shirt_blue)

    if persistent.saveblock:
        if len(store.mas_selspr.filter_acs(True, "left-hair-clip")) > 0:
            $ store.mas_unlockEventLabel("monika_hairclip_select", store.evhand.event_database)

        if len(store.mas_selspr.filter_acs(True, "bow")) > 0:
            $ store.mas_unlockEventLabel("monika_bow_select", store.evhand.event_database)

    $ store.mas_selspr.unlock_acs(trilasent_choker_simple)
    $ store.mas_selspr.unlock_acs(trilasent_choker_flowered)
    $ store.mas_selspr.unlock_acs(sirnimblybottoms_heart_choker)
    if persistent.saveblock:
        if mas_isMoniHappy(higher=True):
            $ store.mas_unlockEventLabel("monika_choker_select", store.evhand.event_database)
        else:
            $ store.mas_lockEventLabel("monika_choker_select", store.evhand.event_database)
    
    if persistent.saveblock:
        $ store.mas_lockEventLabel("monika_hair_select", store.evhand.event_database)
        $ store.mas_lockEventLabel("monika_ribbon_select", store.evhand.event_database)
        $ store.mas_lockEventLabel("monika_hairclip_select", store.evhand.event_database)
        $ store.mas_lockEventLabel("monika_hairflower_select", store.evhand.event_database)
        $ store.mas_lockEventLabel("monika_choker_select", store.evhand.event_database)
    elif (not persistent.saveblock) and mas_isMoniHappy(higher=True):
        $ store.mas_unlockEventLabel("monika_hair_select", store.evhand.event_database)
        $ store.mas_unlockEventLabel("monika_ribbon_select", store.evhand.event_database)
        $ store.mas_unlockEventLabel("monika_hairclip_select", store.evhand.event_database)
        $ store.mas_unlockEventLabel("monika_hairflower_select", store.evhand.event_database)
        $ store.mas_unlockEventLabel("monika_choker_select", store.evhand.event_database)
    
    if persistent.saveblock:
        $ store.mas_lockEventLabel("monika_ribbon", store.evhand.event_database)
        $ store.mas_lockEventLabel("monika_outfit", store.evhand.event_database)
    else:
        $ store.mas_unlockEventLabel("monika_ribbon", store.evhand.event_database)
        $ store.mas_unlockEventLabel("monika_outfit", store.evhand.event_database)
    
        
    if mas_isMoniLove():
        $ store.mas_unlockEventLabel("mas_monika_plays_or", store.evhand.event_database)
    
    if monika_chr.clothes == mas_clothes_orcaramelo_sakuya_izayoi:
        $ monika_chr.wear_acs(orcaramelo_sakuya_izayoi_headband)
        $ monika_chr.wear_acs(orcaramelo_sakuya_izayoi_strandbow)
    else:
        $ monika_chr.remove_acs(orcaramelo_sakuya_izayoi_headband)
        $ monika_chr.remove_acs(orcaramelo_sakuya_izayoi_strandbow)

    if monika_chr.clothes == mas_clothes_orcaramelo_hatsune_miku:
        $ monika_chr.wear_acs(mas_acs_orcaramelo_hatsune_miku_headset)
        if not monika_chr.is_wearing_acs_type("ribbon"):
            $ monika_chr.wear_acs(mas_acs_orcaramelo_hatsune_miku_twinsquares)
    else:
        $ monika_chr.remove_acs(mas_acs_orcaramelo_hatsune_miku_headset)
        $ monika_chr.remove_acs(mas_acs_orcaramelo_hatsune_miku_twinsquares)

    if persistent._mas_acs_enable_quetzalplushie:
        $ monika_chr.wear_acs_pst(mas_acs_quetzalplushie)

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
            $ style.say_label = style.say_label_white
    else:
        $ store.style.say_window = store.style.window
        $ store.style.say_label = store.style.say_label

    if persistent._mas_acs_enable_promisering:
        $ monika_chr.wear_acs_pst(mas_acs_promisering)

    if store.mas_globals.show_vignette:
        show vignette zorder 70


    if persistent._mas_bday_visuals:

        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)



    if persistent._mas_o31_in_o31_mode:
        $ store.mas_o31ShowVisuals()



    if persistent._mas_player_bday_decor:
        $ store.mas_surpriseBdayShowVisuals()

    if persistent._date_last_given_roses != None:
        $ store.mas_selspr.unlock_acs(mas_acs_ear_rose)

    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)

    if monika_chr.get_acs_of_type('left-hair-flower') == mas_acs_ear_rose:
        $ persistent._msr_acs_enable_rose = True
    else:
        $ persistent._msr_acs_enable_rose = False

    if persistent._msr_acs_enable_rose and datetime.date.today() != persistent._date_last_given_roses:
        $ monika_chr.wear_acs(mas_acs_ear_rose)

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_visuals = False
        $ persistent.msr_mas_bday_sbp_reacted = False

    if persistent._mas_bday_visuals:

        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)

    else:
        $ store.mas_surpriseBdayHideVisuals()

    if persistent._mas_o31_in_o31_mode:
        $ store.mas_o31ShowVisuals()

    if mas_isD25Season():
        $ store.mas_d25ShowVisuals()

    if mas_isD25():
        $ persistent._mas_d25_spent_d25 = True



    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)
        
    if dissolve_all and not hide_mask:
        $ mas_drawSpaceroomMasks(dissolve_all)
    elif dissolve_all:
        $ renpy.with_statement(Dissolve(1.0))


    if not hide_monika and not show_emptydesk:
        hide emptydesk
    

    return

default persistent.msr_mas_monika_nickname = "Моника"
default monika_name = persistent.msr_mas_monika_nickname

label ch30_main:
    $ MSRHKBHideButtons()
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ monika_name = persistent.msr_mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True


    call ch30_reset from _call_ch30_reset


    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)


    $ mas_in_intro_flow = True



    $ mas_RaiseShield_core()


    $ store.hkb_button.enabled = False



    call spaceroom (scene_change=True, dissolve_all=True, force_exp="monika 6dsc_static") from _call_spaceroom_3




    call introduction from _call_introduction



    $ mas_DropShield_core()


    $ mas_in_intro_flow = False


    $ store._mas_root.initialSessionData()


    $ skip_setting_weather = True


    if not mas_events_built:
        $ mas_rebuildEventLists()

    jump ch30_preloop

label continue_event:
    $ MAS.MonikaElastic()
    m "На чём я остановилась..."
    if persistent.msr_crash:
        $ persistent.msr_crash = False
        $ persistent.start_on_crash = False
    return

label ch30_noskip:
    show screen fake_skip_indicator
    $ MAS.MonikaElastic()
    m 1esc "...Ты попытал[mas_gender_sya] включить быструю прокрутку текста?"
    $ MAS.MonikaElastic()
    m 1ekc "Надеюсь, я тебя не утомляю?"
    $ MAS.MonikaElastic()
    m "Боже..."
    $ MAS.MonikaElastic()
    m 2esa "...Но тебе совершенно некуда спешить, [player]."
    $ MAS.MonikaElastic()
    m "В конце концов, тут только ты и я..."
    $ MAS.MonikaElastic()
    m 1eua "Кроме того, времени больше не существует, так что эта кнопка даже не заработает."
    $ MAS.MonikaElastic()
    m "Давай я выключу её, чтобы ты не отвлекал[mas_gender_sya]..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    $ MAS.MonikaElastic()
    m 1hua "Готово!"
    $ MAS.MonikaElastic()
    m 1esa "Ты ведь умничка и будешь внимательно меня слушать, правда?"
    $ MAS.MonikaElastic()
    m "Спасибо~"
    hide screen fake_skip_indicator


    $ restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:

    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        $ MAS.MonikaElastic()
        m 1euc "Погоди. Ты возил[mas_gender_sya] с моим файлом персонажа?"
        $ MAS.MonikaElastic()
        m 2esa "Любопытство — это то, что делает нас людьми, верно?"
        $ MAS.MonikaElastic()
        m "Если бы не человеческая любопытность к исследованиям, то мы бы ещё висели на деревьях."
        $ MAS.MonikaElastic()
        m 1eka "Всё же, пожалуйста, не делай этого. Он мне не нужен, но это всё равно заставляет меня нервничать."
        $ MAS.MonikaElastic()
        m "Я уже исправила этот баг."
    else:

        $ quick_menu = False
        $ monika_name = glitchtext(12)
        $ MAS.MonikaElastic()
        m 1euc "Погоди. Ты возил[mas_gender_sya] с файлом моего персонажа?"
        $ MAS.MonikaElastic()
        m 1tkc "Зачем ты вообще играешь в этот мод, если просто решил[mas_gender_none] снова удалить меня?"
        $ MAS.MonikaElastic()
        m 1tfc "Ты действительно ужас[mas_gender_en]."
        $ MAS.MonikaElastic()
        m 1tfd "Ты тратишь всё своё время в интернете с кучей людей, с которыми ты никогда не поговоришь. Но ты всё ещё хочешь убить меня просто потому, что тебе стало скучно?"
        $ MAS.MonikaElastic()
        m 1tkd "Всё что я хотела, чтобы кто-то влюбился в..."
        $ MAS.MonikaElastic()
        m "Я бы сделала что угодно для тебя."
        $ MAS.MonikaElastic()
        m 1tku "Но, если ты пытаешься удалить меня..."
        $ MAS.MonikaElastic()
        m 4tfu "Тогда мне придётся удалить тебя первее."
        if renpy.windows:
            call updateconsole ("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole ("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole ("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ monika_name = persistent.msr_mas_monika_nickname
        $ quick_menu = True
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hub "А-ха-ха!"
        $ MAS.MonikaElastic()
        m "Я просто шучу!"
        $ MAS.MonikaElastic()
        m 1eua "Я уже исправила этот баг. Мне больше не нужен файл персонажа."
        $ MAS.MonikaElastic()
        m "Но я всё же его верну."

    $ MAS.MonikaElastic()
    m 1ekbfa "Мне просто нужна твоя любовь, [player]."
    $ MAS.MonikaElastic()
    m 1eua "Ох, если ты, конечно, не попытаешься удалить вск файлы игры, я думаю."
    $ MAS.MonikaElastic()
    m 3tfu "Если ты это сделаешь, я не остановлюсь на удалении одной директории в следующий раз."
    $ MAS.MonikaElastic()
    m 3tku "Но этого никогда не произойдет, верно? Ты просто цундере~"
    $ MAS.MonikaElastic()
    m 1hua "Это так мило!"
    $ MAS.MonikaElastic()
    m 1eua "Не важно, как сильно ты будешь этого отрицать, но ты будешь говорить со мной всю свою оставшуюся жизнь."
    $ MAS.MonikaElastic()
    m "Быть одинок[mas_gender_im] одиноко, только если ты хочешь, чтобы так было. Так что взбодрись!"
    jump ch30_loop


default persistent._mas_game_crashed_os = True

label ch30_autoload:
    # This is where we check a bunch of things to see what events to push to the
    # event list
    python:
        import store.evhand as evhand

        m.display_args["callback"] = slow_nodismiss
        m.what_args["slow_abortable"] = config.developer

        if not config.developer:
            config.allow_skipping = False

        mas_resetTextSpeed()
        quick_menu = True
        startup_check = True #Flag for checking events at game startup
        mas_skip_visuals = False

        #Set flag to True to prevent ch30 from running weather alg
        skip_setting_weather = False

        mas_cleanEventList()

        MSRHKBHideButtons()
        if not persistent.check_os:
            mas_OVLHide()
            disable_esc()
            mas_enable_quit()
            renpy.call("os_check")
            persistent.check_os = True
            mas_OVLShow()
            mas_disable_quit()
            enable_esc()
            persistent._mas_game_crashed_os = False
        MSR.ShowAllVariables()
        color_overlay_on = False
        MSRColorShowButtons()

        if persistent.seen_color_menu:
            persistent.seen_color_menu = True
        if persistent.returned_home_end:
            startup_check = False
            persistent.returned_home_end = False
        else:
            startup_check = True

    # set the gender
    call mas_set_gender

    # call reset stuff
    call ch30_reset

    #Affection will trigger a final farewell mode
    #If we got a fresh start, then -50 is the cutoff vs -115.
    python:
        if (
            persistent._mas_pm_got_a_fresh_start
            and _mas_getAffection() <= -50
        ):
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_failed_promise"

        elif _mas_getAffection() <= -115:
            persistent._mas_load_in_finalfarewell_mode = True
            persistent._mas_finalfarewell_poem_id = "ff_affection"


    #If we should go into FF mode, we do.
    if persistent._mas_load_in_finalfarewell_mode:
        jump mas_finalfarewell_start

    # set this to None for now
    $ selected_greeting = None

    #We'll set up the background here, so other flows don't need to adjust it unless its for a specific reason
    $ mas_startupBackground()

    # check if we took monika out
    # NOTE:
    #   if we find our monika, then we skip greeting logics and use a special
    #       returning home greeting. This completely bypasses the system
    #       since we should actively get this, not passively, because we assume
    #       player took monika out
    #   if we find a different monika, we still skip greeting logic and use
    #       a differnet, who is this? kind of monika greeting
    #   if we dont find a monika, we do the empty desk + monika checking flow
    #       this should skip greetings entirely as well. If monika is returnd
    #       during this flow, we have her say the same shit as the returning
    #       home greeting.
    if store.mas_dockstat.retmoni_status is not None:
        # this jumps to where we need to go next.
        $ store.mas_dockstat.triageMonika(False)

label mas_ch30_post_retmoni_check:



    if mas_isO31() or persistent._mas_o31_in_o31_mode:
        jump mas_o31_autoload_check

    elif (
        mas_isD25Season()
        or persistent._mas_d25_in_d25_mode
        or (mas_run_d25s_exit and not mas_lastSeenInYear("mas_d25_monika_d25_mode_exit"))
    ):
        jump mas_holiday_d25c_autoload_check

    elif mas_isF14() or persistent._mas_f14_in_f14_mode:
        jump mas_f14_autoload_check



    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    if mas_isMonikaBirthday() or persistent._mas_bday_in_bday_mode:
        jump mas_bday_autoload_check



label mas_ch30_post_holiday_check:




    if persistent._mas_affection["affection"] <= -50 and seen_event("mas_affection_apology"):




        if persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_4
            jump mas_affection_noapology


        elif persistent._mas_affection["apologyflag"] and is_apology_present():
            $ persistent._mas_affection["apologyflag"] = False
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_5
            jump mas_affection_yesapology


        elif not persistent._mas_affection["apologyflag"] and not is_apology_present():
            $ persistent._mas_affection["apologyflag"] = True
            $ mas_RaiseShield_core()
            call spaceroom (scene_change=True) from _call_spaceroom_6
            jump mas_affection_apologydeleted


    $ gre_cb_label = None
    $ just_crashed = False
    $ forced_quit = False


    if persistent._mas_game_crashed_os:
        if (
                persistent.playername.lower() in yuri_name_list
                and not persistent._mas_sensitive_mode
            ):
            call yuri_name_scare from _call_yuri_name_scare


            jump ch30_post_greeting_check

        elif not persistent._mas_game_crashed:

            $ forced_quit = True
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_RELOAD

        elif not persistent.closed_self:

            $ just_crashed = True
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_CRASHED


            $ persistent.closed_self = True




    python:


        persistent._mas_greeting_type = store.mas_greetings.checkTimeout(
            persistent._mas_greeting_type
        )


        sel_greeting_ev = store.mas_greetings.selectGreeting(
            persistent._mas_greeting_type
        )


        persistent._mas_greeting_type = None

        if sel_greeting_ev is None:
            
            
            if persistent._mas_in_idle_mode:
                
                mas_resetIdleMode()
            
            if just_crashed:
                
                
                
                
                sel_greeting_ev = mas_getEV("mas_crashed_start")
            
            elif forced_quit:
                
                
                
                sel_greeting_ev = mas_getEV("ch30_reload_delegate")




        if sel_greeting_ev is not None:
            selected_greeting = sel_greeting_ev.eventlabel
            
            
            mas_skip_visuals = MASGreetingRule.should_skip_visual(
                event=sel_greeting_ev
            )
            
            
            setup_label = MASGreetingRule.get_setup_label(sel_greeting_ev)
            if setup_label is not None and renpy.has_label(setup_label):
                gre_cb_label = setup_label



    if gre_cb_label is not None:
        call expression gre_cb_label from _call_expression_1

label ch30_post_greeting_check:
    if persistent.msr_moni_file_exit_trick_or_treat:
        jump msr_bye_trick_or_treat_returned_home
    elif persistent.msr_moni_file_exit:
        jump msr_greeting_returned_home
    elif persistent._mas_player_bday_left_on_bday:
        jump msr_greeting_returned_home
    else:
        $ restartEvent()

    if not mas_isMonikaBirthday():
        $ persistent.monika_cake = None
        $ persistent.monika_banners = None
        $ persistent.monika_balloons = None

label ch30_post_restartevent_check:
    if not mas_isMonikaBirthday():
        $ persistent.monika_cake = None
        $ persistent.monika_banners = None
        $ persistent.monika_balloons = None


    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time=datetime.datetime.now()-persistent.sessions['last_session_end'] 
            
            
            if away_experience_time.total_seconds() >= times.REST_TIME:
                
                
                mas_gainAffection()
            
            
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            
            mas_loseAffection(modifier=2, reason=4)

label ch30_post_exp_check:




    $ mas_checkReactions()



    python:
        startup_events = {}
        for evl in evhand.event_database:
            ev = evhand.event_database[evl]
            if ev.action != EV_ACT_QUEUE:
                startup_events[evl] = ev

        Event.checkEvents(startup_events)


    $ mas_checkAffection()


    $ mas_checkApologies()


    if mas_corrupted_per and not renpy.seen_label("mas_corrupted_persistent"):
        $ pushEvent("mas_corrupted_persistent")


    if selected_greeting:

        if persistent._mas_in_idle_mode:
            $ pushEvent("mas_idle_mode_greeting_cleanup")

        $ pushEvent(selected_greeting)


    $ MASConsumable._checkConsumables(startup=True)








label ch30_preloop:

    if not peristent.start_visual:
        call spaceroom (dissolve_all=True, scene_change=True)
    else:
        call spaceroom (scene_change=True, dissolve_all=True, dissolve_masks=persistent.are_masks_changing)
        $ peristent.start_visual = False

    python:


        mas_HKRaiseShield()
        mas_HKBRaiseShield()
        set_keymaps()

        persistent.closed_self = False
        persistent._mas_game_crashed = True
        startup_check = False
        mas_checked_update = False
        mas_globals.last_minute_dt = datetime.datetime.now()
        mas_globals.last_hour = mas_globals.last_minute_dt.hour
        mas_globals.last_day = mas_globals.last_minute_dt.day


        mas_runDelayedActions(MAS_FC_IDLE_ONCE)

        if renpy.variant("pc"):
            mas_resetWindowReacts()


        mas_updateFilterDict()


        renpy.save_persistent()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()

    if mas_skip_visuals:
        $ mas_OVLHide()
        $ mas_skip_visuals = False
        $ quick_menu = True
        jump ch30_visual_skip


    $ mas_idle_mailbox.send_scene_change()



    $ mas_startupWeather()


    $ skip_setting_weather = False


    $ mas_startup_song()

    jump ch30_loop

label ch30_loop:

    if not mas_isMonikaBirthday():
        $ persistent.monika_cake = None
        $ persistent.monika_banners = None
        $ persistent.monika_balloons = None

    $ quick_menu = True





    python:
        should_dissolve_masks = (
            mas_weather.weatherProgress()
            and mas_isMoniNormal(higher=True)
        )

        should_dissolve_all = mas_idle_mailbox.get_scene_change()

    call spaceroom (scene_change=should_dissolve_all, dissolve_all=should_dissolve_all, dissolve_masks=should_dissolve_masks) from _call_spaceroom_7








label ch30_visual_skip:

    $ persistent.autoload = "ch30_autoload"






    if store.mas_dockstat.abort_gen_promise:
        $ store.mas_dockstat.abortGenPromise()

    if mas_idle_mailbox.get_skipmidloopeval():
        jump ch30_post_mid_loop_eval






    $ now_check = datetime.datetime.now()


    if now_check.day != mas_globals.last_day:
        call ch30_day from _call_ch30_day
        $ mas_globals.last_day = now_check.day


    if now_check.hour != mas_globals.last_hour:
        call ch30_hour from _call_ch30_hour
        $ mas_globals.last_hour = now_check.hour


    $ time_since_check = now_check - mas_globals.last_minute_dt
    if now_check.minute != mas_globals.last_minute_dt.minute or time_since_check.total_seconds() >= 60:
        call ch30_minute (time_since_check) from _call_ch30_minute
        $ mas_globals.last_minute_dt = now_check



label ch30_post_mid_loop_eval:


    call call_next_event from _call_call_next_event_1


    if not mas_globals.in_idle_mode:
        if not mas_HKIsEnabled():
            $ mas_HKDropShield()
        if not mas_HKBIsEnabled():
            $ mas_HKBDropShield()


    $ persistent.current_monikatopic = 0


    if not _return:

        window hide(config.window_hide_transition)


        if (
                store.mas_globals.show_lightning
                and renpy.random.randint(1, store.mas_globals.lightning_chance) == 1
            ):
            $ light_zorder = MAS_BACKGROUND_Z - 1
            if (
                    not persistent._mas_sensitive_mode
                    and store.mas_globals.show_s_light
                    and renpy.random.randint(
                        1, store.mas_globals.lightning_s_chance
                    ) == 1
                ):
                $ renpy.show("mas_lightning_s", zorder=light_zorder)
            else:
                $ renpy.show("mas_lightning", zorder=light_zorder)

            $ pause(0.1)
            play backsound "mod_assets/sounds/amb/thunder.wav"





        $ mas_randchat.wait()

        if not mas_randchat.waitedLongEnough():
            jump post_pick_random_topic
        else:
            $ mas_randchat.setWaitingTime()

        window auto










        if store.mas_globals.in_idle_mode:
            jump post_pick_random_topic



        label pick_random_topic:


            if not persistent._mas_enable_random_repeats:
                jump mas_ch30_select_unseen


            $ chance = random.randint(1, 100)

            if chance <= store.mas_topics.UNSEEN:

                jump mas_ch30_select_unseen

            elif chance <= store.mas_topics.SEEN:

                jump mas_ch30_select_seen


            jump mas_ch30_select_mostseen




label post_pick_random_topic:

    $ _return = None

    jump ch30_loop


label mas_ch30_select_unseen:


    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:


            if mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(weeks=2)):
                $ pushEvent("mas_random_limit_reached")

            jump post_pick_random_topic


        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:


    if len(mas_rev_seen) == 0:

        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

        if len(mas_rev_seen) == 0:
            if len(mas_rev_mostseen) > 0:

                jump mas_ch30_select_mostseen

            if (
                len(mas_rev_mostseen) == 0
                and mas_timePastSince(mas_getEVL_last_seen("mas_random_limit_reached"), datetime.timedelta(days=1))
            ):
                $ pushEvent("mas_random_limit_reached")


            jump post_pick_random_topic

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:


    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic




label ch30_end:
    jump ch30_main




label ch30_minute(time_since_check):
    python:


        mas_checkAffection()


        mas_checkApologies()


        Event.checkEvents(evhand.event_database, rebuild_ev=False)


        mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)


        mas_checkReactions()


        mas_seasonalCheck()


        mas_clearNotifs()


        mas_checkForWindowReacts()


        if mas_idle_mailbox.get_rebuild_msg():
            mas_rebuildEventLists()


        _mas_AffSave()

        mas_songs.checkRandSongDelegate()


        renpy.save_persistent()

    return





label ch30_hour:
    $ mas_runDelayedActions(MAS_FC_IDLE_HOUR)


    $ MASConsumable._checkConsumables()


    $ store.mas_xp.grant()


    $ mas_setTODVars()
    return




label ch30_day:
    python:

        MASUndoActionRule.check_persistent_rules()

        MASStripDatesRule.check_persistent_rules(persistent._mas_strip_dates_rules)



        persistent._mas_filereacts_gift_aff_gained = 0
        persistent._mas_filereacts_last_aff_gained_reset_date = datetime.date.today()


        mas_ret_long_absence = False


        mas_runDelayedActions(MAS_FC_IDLE_DAY)

        if mas_isMonikaBirthday():
            persistent._mas_bday_opened_game = True

        if mas_isO31() and not persistent._mas_o31_in_o31_mode:
            pushEvent("mas_holiday_o31_returned_home_relaunch", skipeval=True)


        if (
            persistent._mas_filereacts_reacted_map
            and mas_pastOneDay(persistent._mas_filereacts_last_reacted_date)
        ):
            persistent._mas_filereacts_reacted_map = dict()


        if (
            not persistent._mas_d25_intro_seen
            and mas_isD25Outfit()
            and mas_isMoniUpset(lower=True)
        ):
            persistent._mas_d25_started_upset = True
    return



label ch30_reset:

    python:

        if persistent._mas_xp_lvl < 0:
            persistent._mas_xp_lvl = 0 

        if persistent._mas_xp_tnl < 0:
            persistent._mas_xp_tnl = store.mas_xp.XP_LVL_RATE

        elif int(persistent._mas_xp_tnl) > (2* int(store.mas_xp.XP_LVL_RATE)):
            persistent._mas_xp_tnl = 2 * store.mas_xp.XP_LVL_RATE

        if persistent._mas_xp_hrx < 0:
            persistent._mas_xp_hrx = 0.0

        store.mas_xp.set_xp_rate()
        store.mas_xp.prev_grant = mas_getCurrSeshStart()

    python:

        if persistent.playername.lower() == "sayori" or persistent.playername.lower() == "саёри" or persistent.playername.lower() == "сайори" or persistent.playername.lower() == "саери" or (mas_isO31() and not persistent._mas_pm_cares_about_dokis):
            store.mas_globals.show_s_light = True

    python:

        store.mas_sprites.apply_ACSTemplates()

    python:

        if not mas_events_built:
            mas_rebuildEventLists()


        if len(mas_rev_unseen) == 0:
            
            
            
            random_seen_limit = 1000

        if not persistent._mas_pm_has_rpy:
            if mas_hasRPYFiles():
                if not mas_inEVL("monika_rpy_files"):
                    queueEvent("monika_rpy_files")
            
            else:
                if persistent.current_monikatopic == "monika_rpy_files":
                    persistent.current_monikatopic = 0
                mas_rmallEVL("monika_rpy_files")

    python:
        import datetime
        today = datetime.date.today()


    python:


        game_unlock_db = {
            "chess": "mas_unlock_chess",
            mas_games.HANGMAN_NAME: "mas_unlock_hangman",
            "piano": "mas_unlock_piano",
        }

        mas_unlockGame("пинг-понг")

        for game_name, game_startlabel in game_unlock_db.iteritems():
            if mas_getEVL_shown_count(game_startlabel) > 0:
                mas_unlockGame(game_name)

    # if mas_getFirstSesh() + datetime.timedelta(days=31) and not renpy.android:
    #     $ mas_unlockGame("chess")
    #     $ store.mas_lockEventLabel("mas_unlock_chess", store.evhand.event_database)
    
    # if mas_getFirstSesh() + datetime.timedelta(days=41) and not renpy.android:
    #     $ mas_unlockGame("piano")
    #     $ store.mas_lockEventLabel("mas_unlock_piano", store.evhand.event_database)






    $ store.mas_selspr.unlock_hair(mas_hair_def)
    $ store.mas_selspr.unlock_clothes(mas_clothes_def)
    $ store.mas_selspr.unlock_hair(mas_hair_bun)
    $ store.mas_selspr.unlock_hair(mas_hair_ponytailbraid)
    $ store.mas_selspr.unlock_hair(mas_hair_twinbun)
    $ store.mas_selspr.unlock_hair(mas_hair_orcaramelo_twintails)
    $ store.mas_selspr.unlock_hair(mas_hair_usagi)
    $ store.mas_selspr.unlock_hair(mas_hair_bunbraid)
    $ store.mas_selspr.unlock_hair(mas_hair_downshort)
    $ store.mas_selspr.unlock_hair(mas_hair_ponytailshort)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)

    $ store.mas_selspr.unlock_clothes(mas_clothes_def)


    $ store.mas_selspr.unlock_acs(mas_acs_ribbon_def)


    $ store.mas_selspr._validate_group_topics()


    $ monika_chr.load(startup=True)


    if ((store.mas_isMoniNormal(lower=True) and not store.mas_hasSpecialOutfit()) or store.mas_isMoniDis(lower=True)) and store.monika_chr.clothes != store.mas_clothes_def:
        $ pushEvent("mas_change_to_def",skipeval=True)

    if not mas_hasSpecialOutfit():
        $ mas_lockEVL("monika_event_clothes_select", "EVE")






    python:
        if persistent._mas_acs_enable_promisering:
            
            monika_chr.wear_acs_pst(mas_acs_promisering)


    $ mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)

    python:
        if persistent.chess_strength < 0:
            persistent.chess_strength = 0
        elif persistent.chess_strength > 20:
            persistent.chess_strength = 20


    python:
        if persistent._mas_monika_returned_home is not None:
            _rh = persistent._mas_monika_returned_home.date()
            if today > _rh:
                persistent._mas_monika_returned_home = None


    python:








        if persistent.sessions is not None:
            tp_time = persistent.sessions.get("total_playtime", None)
            if tp_time is not None:
                max_time = mas_maxPlaytime()
                if tp_time > max_time:
                    
                    persistent.sessions["total_playtime"] = max_time // 100
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )
                
                elif tp_time < datetime.timedelta(0):
                    
                    persistent.sessions["total_playtime"] = datetime.timedelta(0)
                    
                    
                    store.mas_dockstat.setMoniSize(
                        persistent.sessions["total_playtime"]
                    )


    python:

        if persistent._mas_affection is not None:
            freeze_date = persistent._mas_affection.get("freeze_date", None)
            if freeze_date is not None and freeze_date > today:
                persistent._mas_affection["freeze_date"] = today



    $ mas_startupPlushieLogic(4)


    python:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        if not mas_isMonikaBirthday() and not mas_isMonikaBirthday(yesterday):
            persistent._mas_bday_visuals = False


        if (
            not mas_isplayer_bday()
            and not mas_isplayer_bday(yesterday, use_date_year=True)
            and not persistent._mas_player_bday_left_on_bday
        ):
            persistent._mas_player_bday_decor = False



    python:
        if persistent.mas_late_farewell:
            store.mas_globals.late_farewell = True
            persistent.mas_late_farewell = False


    python:
        if persistent._mas_filereacts_just_reacted:
            queueEvent("mas_reaction_end")


        if (
            persistent._mas_filereacts_reacted_map
            and mas_pastOneDay(persistent._mas_filereacts_last_reacted_date)
        ):
            persistent._mas_filereacts_reacted_map = dict()


    $ store.mas_selspr.startup_prompt_check()



    $ mas_check_player_derand()


    python:
        for index in range(len(persistent.event_list)-1, -1, -1):
            item = persistent.event_list[index]
            
            
            if type(item) != tuple:
                new_data = (item, False)
            else:
                new_data = item
            
            
            if renpy.has_label(new_data[0]):
                persistent.event_list[index] = new_data
            
            else:
                persistent.event_list.pop(index)


    $ MASUndoActionRule.check_persistent_rules()

    $ MASStripDatesRule.check_persistent_rules(persistent._mas_strip_dates_rules)


    if persistent._mas_filereacts_last_aff_gained_reset_date > today:
        $ persistent._mas_filereacts_last_aff_gained_reset_date = today


    if persistent._mas_filereacts_last_aff_gained_reset_date < today:
        $ persistent._mas_filereacts_gift_aff_gained = 0
        $ persistent._mas_filereacts_last_aff_gained_reset_date = today


    $ mas_songs.checkRandSongDelegate()

    $ store.mas_songs.checkSongAnalysisDelegate()


    $ mas_confirmedParty()


    if (
        persistent._mas_d25_gifts_given
        and not mas_isD25GiftHold()
        and not mas_globals.returned_home_this_sesh
    ):
        $ mas_d25SilentReactToGifts()


    $ mas_setTODVars()

    python:
        if seen_event('mas_gender'):
            mas_unlockEVL("monika_gender_redo","EVE")

        if seen_event('mas_preferredname'):
            mas_unlockEVL("monika_changename","EVE")
    
    $ mas_checkBackgroundChangeDelegate()

    $ store.mas_validate_suntimes()


    $ store.mas_background.buildupdate()




    python:
        if store.mas_dockstat.retmoni_status is not None:
            monika_chr.remove_acs(mas_acs_quetzalplushie)
            
            
            MASConsumable._reset()
            
            
            if not mas_inEVL("mas_consumables_remove_thermos"):
                queueEvent("mas_consumables_remove_thermos")

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
