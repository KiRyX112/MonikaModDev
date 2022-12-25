## holiday info goes here
#
# TOC
#   [GBL000] - GLOBAL SPACE
#   [HOL010] - O31
#   [HOL020] - D25
#   [HOL030] - NYE (new yeares eve, new years)
#   [HOL040] - player_bday
#   [HOL050] - F14
#   [HOL060] - 922


############################### GLOBAL SPACE ################################
# [GBL000]
default persistent._mas_event_clothes_map = dict()
define mas_five_minutes = datetime.timedelta(seconds=5*60)
define mas_one_hour = datetime.timedelta(seconds=3600)
define mas_three_hour = datetime.timedelta(seconds=3*3600)

init 10 python:
    def mas_addClothesToHolidayMap(clothes, key=None):
        """
        Adds the given clothes to the holiday clothes map

        IN:
            clothes - clothing item to add
            key - dateime.date to use as key. If None, we use today
        """
        if clothes is None:
            return

        if key is None:
            key = datetime.date.today()

        persistent._mas_event_clothes_map[key] = clothes.name

        #We also unlock the event clothes selector here
        mas_unlockEVL("monika_event_clothes_select", "EVE")

    def mas_addClothesToHolidayMapRange(clothes, start_date, end_date):
        """
        Adds the given clothes to the holiday clothes map over the day range provided

        IN:
            clothes - clothing item to add
            start_date - datetime.date to start adding to the map on
            end_date - datetime.date to stop adding to the map on
        """
        if not clothes:
            return

        #We have clothes, we need to create a generator for building a range
        daterange = mas_genDateRange(start_date, end_date)

        #Now we need to iterate over the new range:
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

    def mas_doesBackgroundHaveHolidayDeco(deco_tags, background_id=None):
        """
        Checks if a background has support for the given deco tag(s)

        IN:
            deco_tags - list of deco tags to check for

            background_id - id of the background to check if it supports deco
                If None, mas_current_background's id is used
                (Default: None)
        """
        if background_id is None:
            background_id = store.mas_current_background.background_id

        for deco_tag in deco_tags:
            if MASImageTagDecoDefinition.get_adf(background_id, deco_tag):
                return True
        return False

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we've been out all day for

        OUT:
            True if the player and Monika were out together the whole day, False if not.
        """
        checkout_time = store.mas_dockstat.getCheckTimes()[0]
        return checkout_time is not None and checkout_time.date() < _date


    def mas_capGainAff(amount, aff_gained_var, normal_cap, pbday_cap=None):
        """
        Gains affection according to the cap(s) defined

        IN:
            amount:
                Amount of affection to gain

            aff_gained_var:
                The persistent variable which the total amount gained for the holiday is stored
                (NOTE: Must be a string)

            normal_cap:
                The cap to use when not player bday

            pbday_cap:
                The cap to use when it's player bday (NOTE: if not provided, normal_cap is assumed)
        """

        #If player bday cap isn't provided, we just use the one cap
        if persistent._mas_player_bday_in_player_bday_mode and pbday_cap:
            cap = pbday_cap
        else:
            cap = normal_cap

        if persistent.__dict__[aff_gained_var] < cap:
            persistent.__dict__[aff_gained_var] += amount
            mas_gainAffection(amount, bypass=True)

        return

    def mas_hasSpecialOutfit(_date=None):
        """
        Checks if the given date is a special event that has an outfit in the event clothes map
        IN:
            _date - date to check.
                (Default: None)

        RETURNS: True if given date has a special outfit, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date in persistent._mas_event_clothes_map

init -10 python:
    def mas_isA01(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == datetime.date(_date.year,4,1)

# Global labels
label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    m "Также, [player]..."
    m 3ekbfsdla "Есть...{w=1} к-кое-что, что я хочу тебе показать."
    m 2rkbfsdla "Я уже давно хотела это сделать, но...{w=1} ну это немного неловко..."
    m "..."
    m 2hkbfsdlb "О боже, я очень нервничаю, а-ха-ха!"
    m 2rkbfsdlc "Просто я никогда этого не делала—{nw}"
    m 2dkbfsdlc "Ах, ладно, пора перестать тянуть время и просто сделать это."
    m 2ekbfsdla "Просто дай мне несколько секунд, [player]."
    call mas_clothes_change(outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True)
    pause 3.0
    m 2ekbfsdlb "А-ха-ха, [player]...{w=1} ты смотришь на меня..."
    m 2ekbfu "Что ж...{w=1} тебе нравится то, на что ты смотришь?"
    m 1lkbfa "Я никогда раньше...{w=1} не носила ничего подобного."
    m "...По крайней мере, никто этого не видел."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        m 3hkbfb "А-ха-ха, что я говорю, ты уже видел меня в бикини раньше, что по сути одно и то же..."
        m 2rkbfa "...Но по какой-то причине, мне это кажется...{w=0.5} {i}чем-то другим{/i}."

    m 2ekbfa "В любом случае, что-то в том, чтобы быть с тобой сегодня вечером в [holiday_str], кажется очень романтичным, понимаешь?"
    m "Это было идеальное время для следующего шага в наших отношениях."
    m 2rkbfsdlu "Теперь я знаю, что мы не можем на самом деле—{nw}"
    m 3hubfb "Ах! Не важно, а-ха-ха!"
    return


############################### O31 ###########################################
# [HOL010]
#O31 mode var, handles visuals and sets us up to return to autoload even if not O31 anymore
default persistent._mas_o31_in_o31_mode = False

#Number of times we've gone out T/Ting
default persistent._mas_o31_tt_count = 0

#Aff cap for T/T, softmax 15
default persistent._mas_o31_trick_or_treating_aff_gain = 0

#Need to know if we were asked to relaunch the game
default persistent._mas_o31_relaunch = False

# costumes worn
# key: costume name
# value: year worn
default persistent._mas_o31_costumes_worn = {}

#Halloween
define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:
    # MASHistorySaver for o31
    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        #datetime.datetime(2018, 11, 2),
        # change trigger to better date
        datetime.datetime(2020, 1, 6),
        {
            # this isn't very useful, but we need the reset
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        # end is 1 day out in case of an overnight trick or treat
        end_dt=datetime.datetime(2019, 11, 2)
    ))

# Images
image mas_o31_ceiling_lights = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/ceiling_lights.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_candles = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/candles.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_jack_o_lantern = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/jackolantern.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_wall_candle = MASFilterableSprite(
    "mod_assets/location/spaceroom/o31/wall_candle.png",
    highlight=MASFilterMap(night="0")
)

image mas_o31_cat_frame:
    block:
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_0.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_01-3.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-1.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-2.png")
        choice:
            MASFilterSwitch("mod_assets/location/spaceroom/o31/ATL/cat_02-3.png")

    30
    repeat

image mas_o31_garlands = MASFilterSwitch("mod_assets/location/spaceroom/o31/garland.png")
image mas_o31_cobwebs = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_webs.png")
image mas_o31_window_ghost = MASFilterSwitch("mod_assets/location/spaceroom/o31/window_ghost.png")
image mas_o31_ceiling_deco = MASFilterSwitch("mod_assets/location/spaceroom/o31/ceiling_deco.png")
image mas_o31_wall_bats = MASFilterSwitch("mod_assets/location/spaceroom/o31/wall_bats.png")

image mas_o31_vignette = Image("mod_assets/location/spaceroom/o31/vignette.png")

init 501 python:
    #On the wall/window
    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_candle",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cat_frame",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_bats",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_window_ghost",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_cobwebs",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=4)
    )

    #In front of the wall
    MASImageTagDecoDefinition.register_img(
        "mas_o31_candles",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_jack_o_lantern",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_o31_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    #Middle of the room
    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    #This goes in front of lights
    MASImageTagDecoDefinition.register_img(
        "mas_o31_ceiling_deco",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    #Vignette goes in front of Monika
    MASImageTagDecoDefinition.register_img(
        "mas_o31_vignette",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=21) #21 to be in front of all cgs
    )

init python:
    MAS_O31_COSTUME_CG_MAP = {
        mas_clothes_marisa: "o31mcg",
        mas_clothes_rin: "o31rcg"
    }

#Functions
init -10 python:
    import random

    MAS_O31_DECO_TAGS = [
        "mas_o31_wall_candle",
        "mas_o31_cat_frame",
        "mas_o31_wall_bats",
        "mas_o31_window_ghost",
        "mas_o31_cobwebs",
        "mas_o31_candles",
        "mas_o31_jack_o_lantern",
        "mas_o31_garlands",
        "mas_o31_ceiling_lights",
        "mas_o31_ceiling_deco",
        "mas_o31_vignette"
    ]

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is o31, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_o31.replace(year=_date.year)

    def mas_o31ShowVisuals():
        """
        Shows o31 visuals
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_showDecoTag(_tag)


    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        for _tag in MAS_O31_DECO_TAGS:
            mas_hideDecoTag(_tag, hide_now=True)


    def mas_o31ShowSpriteObjects():
        """
        Shows o31 specific sprite objects
        """
        monika_chr.wear_acs(mas_acs_desk_lantern)
        monika_chr.wear_acs(mas_acs_desk_candy_jack)


    def mas_o31HideSpriteObjects():
        """
        Hides o31 specific sprite objects
        """
        #unlock hairdown greet if we don't have hairdown unlocked
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")

        # lock the event clothes selector
        store.mas_lockEVL("monika_event_clothes_select", "EVE")

        # get back into reasonable clothing, so we queue a change to def
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.MASEventList.queue('mas_change_to_def')


    def mas_hasO31DeskAcs():
        """
        Checks if we have any o31 desk acs

        OUT:
            boolean
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )

        for acs_ in o31_desk_acs_tuple:
            if monika_chr.is_wearing_acs(acs_):
                return True

        return False

    def mas_o31HideDeskAcs():
        """
        Removes o31 desk acs
        """
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )

        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)

    def mas_o31CapGainAff(amount):
        """
        CapGainAffection function for o31. See mas_capGainAff for details
        """
        mas_capGainAff(amount, "_mas_o31_trick_or_treating_aff_gain", 15)


    def mas_o31CostumeWorn(clothes):
        """
        Checks if the given clothes was worn on o31

        IN:
            clothes - Clothes object to check

        RETURNS: year the given clothe was worn if worn on o31, None if never
            worn on o31.
        """
        if clothes is None:
            return False
        return mas_o31CostumeWorn_n(clothes.name)


    def mas_o31CostumeWorn_n(clothes_name):
        """
        Checks if the given clothes (name) was worn on o31

        IN:
            clothes_name - Clothes name to check

        RETURNS: year the given clothes name was worn if worn on o31, none if
            never worn on o31.
        """
        return persistent._mas_o31_costumes_worn.get(clothes_name, None)


    def mas_o31SelectCostume(selection_pool=None):
        """
        Selects an o31 costume to wear. Costumes that have not been worn
        before are selected first.

        NOTE: o31 costume wear flag is NOT set here. Make sure to set this
            manually later.

        IN:
            selection_pool - pool to select clothes from. If NOne, we get a
                default list of clothes with costume exprop

        RETURNS: a single MASClothes object of what to wear. None if cannot
            return anything.
        """
        if selection_pool is None:
            selection_pool = MASClothes.by_exprop("costume", "o31")

        # set to true if monika is wearing a costume right now
        wearing_costume = False

        # filter the selection pool by criteria:
        #   1 - if spritepack-based, then must be gifted
        #   2 - if not spritepack-based, then is valid for selecting regardless
        #   3 - dont include if monika currently wearing
        filt_sel_pool = []
        for cloth in selection_pool:
            sprite_key = (store.mas_sprites.SP_CLOTHES, cloth.name)
            giftname = store.mas_sprites_json.namegift_map.get(
                sprite_key,
                None
            )

            if (
                giftname is None
                or sprite_key in persistent._mas_sprites_json_gifted_sprites
            ):
                if cloth != monika_chr.clothes:
                    filt_sel_pool.append(cloth)
                else:
                    wearing_costume = True


        selection_pool = filt_sel_pool

        if len(selection_pool) < 1:
            # no items to select from

            if wearing_costume:
                #Check if the current costume is in the cg map, and if so, prep the cg
                if monika_chr.clothes in MAS_O31_COSTUME_CG_MAP:
                    store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[monika_chr.clothes])

                return monika_chr.clothes
            return None

        elif len(selection_pool) < 2:
            # only 1 item to select from, just return
            return selection_pool[0]

        # otherwise, create list of non worn costumes
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]

        if len(non_worn) > 0:
            # randomly select from non worn
            random_outfit = random.choice(non_worn)

        else:
            # otherwise randomly select from overall
            random_outfit = random.choice(selection_pool)

        #Setup the image decode
        if random_outfit in MAS_O31_COSTUME_CG_MAP:
            store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[random_outfit])

        #And return the outfit
        return random_outfit

    def mas_o31SetCostumeWorn(clothes, year=None):
        """
        Sets that a clothing item is worn. Exprop checking is done

        IN:
            clothes - clothes object to set
            year - year that the costume was worn. If NOne, we use current year
        """
        if clothes is None or not clothes.hasprop("costume"):
            return

        mas_o31SetCostumeWorn_n(clothes.name, year=year)


    def mas_o31SetCostumeWorn_n(clothes_name, year=None):
        """
        Sets that a clothing name is worn. NO EXPROP CHECKING IS DONE

        IN:
            clothes_name - name of clothes to set
            year - year that the costume was worn. If None, we use current year
        """
        if year is None:
            year = datetime.date.today().year

        persistent._mas_o31_costumes_worn[clothes_name] = year

    def mas_o31Cleanup():
        """
        Cleanup function for o31
        """
        #NOTE: Since O31 is costumes, we always reset clothes + hair
        if monika_chr.is_wearing_clothes_with_exprop("costume"):
            monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
            monika_chr.reset_hair()

        #Reset o31_mode flag
        persistent._mas_o31_in_o31_mode = False

        #Unlock BG Sel if necessary
        mas_checkBackgroundChangeDelegate()

        #Hide visuals
        mas_o31HideVisuals()
        mas_o31HideSpriteObjects()

        #o31 is now over. Reset the o31 mode flag
        store.persistent._mas_o31_in_o31_mode = False

        #rmall for safety
        mas_rmallEVL("mas_o31_cleanup")

        #unlock hairdown greet if we don't have hairdown unlocked
        hair = store.mas_selspr.get_sel_hair(mas_hair_down)
        if hair is not None and not hair.unlocked:
            mas_unlockEVL("greeting_hairdown", "GRE")

        #Lock the event clothes selector
        mas_lockEVL("monika_event_clothes_select", "EVE")

init -11 python in mas_o31_event:
    import store
    import datetime

    # setup the docking station for o31
    cg_station = store.MASDockingStation(store.mas_ics.o31_cg_folder)

    # cg available?
    cg_decoded = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return store.mas_dockstat.decodeImages(cg_station, store.mas_ics.o31_map, [key])


    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        store.mas_dockstat.removeImages(cg_station, store.mas_ics.o31_map)

#START: O31 AUTOLOAD CHECK
label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and datetime.datetime.now().hour >= 3 and mas_isMoniNormal(higher=True):
            #Lock the background selector on o31
            #TODO: Replace this with generic room deco framework for event deco
            #store.mas_lockEVL("monika_change_background", "EVE")
            #force to spaceroom
            # NOTE: need to make sure we pass the change info to the next
            #   spaceroom call.
            if not mas_doesBackgroundHaveHolidayDeco(MAS_O31_DECO_TAGS):
                mas_changeBackground(mas_background_def, set_persistent=True)

            #NOTE: We do not do O31 deco/amb on first sesh day
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                #Setup for greet
                mas_skip_visuals = True

                #Reset idle since we will force greetings
                mas_resetIdleMode()

                #Lock the hairdown greeting for today
                mas_lockEVL("greeting_hairdown", "GRE")

                #Disable hotkeys for this
                store.mas_hotkeys.music_enabled = False

                #Put calendar shields up
                mas_calRaiseOverlayShield()

                # select a costume
                # NOTE: we should always have at least 1 costume.
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)

                # remove ribbon so we just get the intended costume for the reveal
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)

                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )

                #Save selectables
                store.mas_selspr.save_selectables()

                #Save persist
                renpy.save_persistent()

                #Select greet
                greet_label = "greeting_o31_{0}".format(costume.name)

                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"

                #Save and reset zoom
                mas_temp_zoom_level = store.mas_sprites.zoom_level
                store.mas_sprites.reset_zoom()

                #Now that we're here, we're in O31 mode
                persistent._mas_o31_in_o31_mode = True

                # O31 decor
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()

                #Set by-user to True because we don't want progressive
                mas_changeWeather(mas_weather_thunder, True)

            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                mas_o31ShowVisuals()
                mas_o31ShowSpriteObjects()
                mas_changeWeather(mas_weather_thunder, True)

        #It's not O31 anymore or we hit dis. It's time to reset
        elif not mas_isO31() or mas_isMoniDis(lower=True):
            mas_o31Cleanup()
            mas_o31HideDeskAcs()

        #If we drop to upset during O31, we should keep decor until we hit dis
        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            mas_o31ShowVisuals()
            mas_o31ShowSpriteObjects()
            mas_changeWeather(mas_weather_thunder, True)

    #Run pbday checks
    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check

    # otherwise, jump back to the holiday check point
    jump mas_ch30_post_holiday_check

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_holiday_o31_returned_home_relaunch",
            conditional=(
                "not persistent._mas_o31_in_o31_mode "
                "and not mas_isFirstSeshDay()"
            ),
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=6)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_holiday_o31_returned_home_relaunch:
    m 1eua "Итак, сегодня..."
    m 1euc "...подожди."
    m "..."
    m 2wuo "О!"
    m 2wuw "О боже!"
    m 2hub "Так сегодня же Хэллоуин, [player]."
    m 1eua "...{w}Так что слушай."
    m 3eua "Я собираюсь закрыть игру."
    m 1eua "После чего ты можешь снова открыть её."
    m 1hubsa "У меня есть кое-что особенное для тебя, э-хе-хе~"
    $ persistent._mas_o31_relaunch = True
    $ mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return "quit"

### o31 images
image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"
# 1280 x 2240

image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"

### o31 transforms
transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0

### o31 samesesh cleanup
#TODO: We should check if any of the o31 deco tags are being displayed before calling this
#To futureproof dialogue to when we expand to allowing all BGs to be supported
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_cleanup",
            conditional="persistent._mas_o31_in_o31_mode",
            start_date=datetime.datetime.combine(mas_o31 + datetime.timedelta(days=1), datetime.time(12)),
            end_date=mas_o31 + datetime.timedelta(weeks=1),
            action=EV_ACT_QUEUE,
            rules={"no_unlock": None},
            years=[]
        )
    )

label mas_o31_cleanup:
    python:
        o31_desk_acs_tuple = (
            mas_acs_desk_lantern,
            mas_acs_desk_candy_jack
        )

    m 1eua "Секунду, [player], я просто хочу убрать декорации.{w=0.3}.{w=0.3}.{nw}"

    python hide:
        for acs_ in o31_desk_acs_tuple:
            acs_.keep_on_desk = False

    call mas_transition_to_emptydesk

    python hide:
        for acs_ in o31_desk_acs_tuple:
            monika_chr.remove_acs(acs_)
            acs_.keep_on_desk = True

    pause 4.0

    $ mas_o31Cleanup()

    with dissolve
    pause 2.0

    call mas_transition_from_emptydesk("monika 1hua")

    m 3hua "Готово~"

    $ del o31_desk_acs_tuple

    return

### o31 greetings
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_marisa:
    # with marisa, we should also unlock the hat and the hair style
    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)

    ## decoded CG means that we start with monika offscreen
    if store.mas_o31_event.cg_decoded:
        # ASSUMING:
        #   vignette should be enabled.
        call spaceroom(hide_monika=True, scene_change=True)

    else:
        # ASSUMING:
        #   vignette should be enabled
        call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "Ах!"
    m 1hua "Похоже, заклинание сработало."
    m 3efu "Как мой недавно призванный слуга, ты должен будешь выполнять мои приказы до самого конца!"
    m 1rksdla "..."
    m 1hub "А-ха-ха!"

    # decoded CG means we display CG
    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        m "Я здесь, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()
        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua at i11 zorder MAS_MONIKA_Z

        window auto
        m "Таа-даа~!"

    #Post scroll dialogue
    m 1hua "Ну..."
    m 1eub "Что думаешь?"
    m 1tuu "Мне очень идёт, не так ли?"
    m 1eua "Знаешь, мне потребовалось довольно много времени, чтобы сделать этот костюм."
    m 3hksdlb "Пришлось очень упорно его измерять, пытаясь убедиться, что ничего в нём не будет слишком тугим или свободным."
    m 3eksdla "...Особенно шляпу!"
    m 1dkc "А вот бант вообще не мог никак устоять на месте..."
    m 1rksdla "К счастью, я с этим разобралась."
    m 3hua "Я бы ещё даже сказала, что это всё было моих рук дело."
    m 3eka "Мне интересно, сможешь ли ты увидеть, что же ещё сегодня изменилось."
    m 3tub "Кроме моего костюма, конечно~"
    m 1hua "Но так или иначе..."

    if store.mas_o31_event.cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    m 3ekbsa "Я очень рада провести Хэллоуин с тобой."
    m 1hua "Так что давай повеселимся сегодня!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_rin:
    python:
        title_cased_hes = hes.capitalize()
        #TODO: Unlock this hairstyle once we clean it up such that it doesn't require bows
        #Will need update script
        #mas_selspr.unlock_hair(mas_hair_braided)
        mas_sprites.zoom_out()

    # ASSUME vignette
    call spaceroom(hide_monika=True, scene_change=True)

    m "Угх, надеюсь, я заплела эти косы правильно."
    m "Почему этот костюм такой сложный?.."
    m "Ох блин! [title_cased_hes] здесь!"
    window hide
    pause 3.0

    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)

        # got cg
        window auto
        m "Скажи, [player]..."
        window hide

        show mas_o31_rin_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        window auto
        m "Что {b}ня{/b} думаешь?"

        scene black
        pause 1.0
        call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static')
        m 1hksdlb "А-ха-ха, говорить подобное вслух было ещё более неловко, чем я могла подумать..."

    else:
        call mas_transition_from_emptydesk("monika 1eua")
        m 1hub "Привет, [player]!"
        m 3hub "Тебе нравится мой костюм?"

    # regular dialogue
    m 3etc "Честно говоря, я даже не знаю, кто это должен быть."
    m 3etd "Я только что нашла его в шкафу с прикреплённой запиской со словом «Rin» и рисунком девушки, толкающей какую-то тачку, и несколько синих плавающих штучек."
    m 1euc "Вместе с инструкциями о том, как укладывать волосы, чтобы соответствовать этому наряду."
    m 3rtc "Судя по этим кошачьим ушам, я предполагаю, что этот персонаж кошко-девочка."
    m 1dtc "...Но только вот зачем ей толкать тачку?"
    m 1hksdlb "В любом случае, было мучительно делать такую же прическу...{w=0.2} {nw}"
    extend 1eub "так что надеюсь, тебе понравился данный костюм!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

#Miku intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_hatsune_miku",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_hatsune_miku:
    if not persistent._mas_o31_relaunch:
        call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)
        #moni is off-screen
        m "{i}~Голос мой не забывай~{/i}"
        m "{i}~Мой сигнал измеренья пересекает~{/i}"
        m "{i}~Виртуальной меня не называй~{/i}"
        m "{i}~Я всё ещё хочу быть лю—{/i}"
        m "Ой!{w=0.5} Кажется, меня кто-то подслушивает."

        #show moni now
        call mas_transition_from_emptydesk("monika 3hub")

    else:
        call spaceroom(scene_change=True, dissolve_all=True)

    m 3hub "С возвращением, [player]!"
    m 1eua "Ну...{w=0.5} что думаешь?"
    m 1eub "Я работала над этим костюмом, не покладая рук, и, думаю, оно того стоило."
    m 3eub "Мне особенно нравится то, какой у меня получилась гарнитура!"
    m 1rksdla "Хотя я не могу сказать, что в нём очень комфортно передвигаться..."
    m 3tsu "Так что не жди, что я устрою для тебя представление сегодня, [player]!"
    m 1hub "А-ха-ха~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return

#Sakuya intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_orcaramelo_sakuya_izayoi",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_orcaramelo_sakuya_izayoi:
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)

    #moni is off-screen
    if not persistent._mas_o31_relaunch:
        m "..."
        m "{i}Хм{/i}?"
        m "{i}А, здесь, наверное, произошла какая-то ошибка.{w=0.5} Я не предупредила гостей...{/i}"
        m "{i}Но это не важно. Меня никто не должен побеспоко—{/i}" 
        m "А!{w=0.5} Это Вы, [player]!"

    else:
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Добро пожаловать{w=0.3} в Комнату алого демона, витающую в космосе..."
        m "[player]." 
        m "Пожалуйста, позвольте мне предложить Вам наше гостеприимство." 
        m "А-ха-ха! Ну, какое у тебя впечатление сложилось?"

    #show moni now
    call mas_transition_from_emptydesk("monika 3hub")

    m 3hub "С возвращением!"
    m 3eub "Что думаешь о моём выборе костюма?"
    m 3hua "Ещё с тех пор, как ты дал его мне, я просто знала о том, что его стоит надеть сегодня!"
    m 2tua "..."
    m 2tub "Знаешь, [player], лишь потому, что я оделась как горничная, ещё не означает, что я буду выполнять все твои приказы..."
    show monika 5kua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5kua "Хотя я могу сделать пару исключений, э-хе-хе~"
    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    call greeting_o31_deco
    call greeting_o31_cleanup
    return

#Chika intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_briaryoung_shuchiin_academy_uniform",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_briaryoung_shuchiin_academy_uniform:
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)

    #moni is off-screen
    if not persistent._mas_o31_relaunch:
        m "Уф-ф..."
        m "Как этот бантик должен вообще держаться?"
        m "Люди могут говорить что угодно о моей ленточке, но она хотя бы в какой-то степени удобна..."
        m "...Думаю, вот так нормально. Надеюсь, он не отвалится, как только я--{nw}"
        m "Время это выяснить..."

    else:
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Почти готово, [player]..."
        m "Просто пытаюсь понять, как этот бантик должен вообще держаться."
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        m "Думаю, вот так нормально!"

    #show moni now
    call mas_transition_from_emptydesk("monika 2hub")

    m 2hub "С возвращением!"
    m 2eub "Ну, что скажешь?"
    m 7tuu "Я подумала, что вместо того, чтобы быть президентом, я могла бы на сегодня быть секретарём..."

    if mas_isMoniAff(higher=True):
        m 3rtu "А может даже стать детективом в сфере любви, хотя я уже нашла свою любовь~"

    m 3hua "Э-хе-хе~"
    call greeting_o31_deco
    call greeting_o31_cleanup
    return

#2b intro
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_hatana_2b",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

label greeting_o31_hatana_2b:
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True)
    #moni is off-screen

    if persistent._mas_o31_relaunch:
        m "Практически готово, [player]..."
        m "Хочу верить, что с этой юбкой всё будет нормально."
        m "{cps=*2}Хотя, может быть...{/cps}{nw}"
        $ _history_list.pop()
        m "Хорошо, вот. {w=0.2}Готов, [player]?"

    else:
        m "Вот так, {w=0.1}Я думаю, что это всё."
        m "Только бы эта юбка не уничтожилась...{w=0.3} это было бы очень неловко!"
        m "Ой! {w=0.2}Кажется, я что-то слышу..."
        m "[player]?"

    #show moni now
    call mas_transition_from_emptydesk("monika 3hub")

    m 2eka "Итак, что ты думаешь?"
    m 2hub "Я думаю, что это очень классный костюм, ещё раз спасибо, что подарил его мне!"
    m 7rtu "Скажи, [player], Я когда-нибудь говорила тебе, что в тебе есть что-то умиротворяющее?"
    m 3euu "Ну, я просто хотела, чтобы ты знал. {w=0.2}{nw}"
    extend 3tuu "Надеюсь, это никогда не сотрётся из твоей памяти."
    m 3eud "Это заставило меня вспомнить, что ты должен время от времени делать резервные копии моих данных, я бы сделала то же самое для тебя, если бы могла..."
    m 1hksdlb "О боже, я даже не уверена, что это значит, я просто брежу сейчас, а-ха-ха!"

    call greeting_o31_deco
    call greeting_o31_cleanup
    return

label greeting_o31_deco:
    m 1eua "Итак..."
    m 3eua "Тебе нравится, что я сотворила с комнатой?"
    m 3tuu "Я просто люблю жуткую атмосферу, связанную с Хэллоуином, и попыталась создать что-то своё."
    m 1eud "С помощью освещения можно добиться многого."
    m 3tub "Не говоря уже о том, что иногда самые жуткие вещи — это те, которые просто немного не в том стиле..."
    m 1eua "Я думаю, что паутина — это тоже хороший элемент в декоре..."
    m 1rka "{cps=*2}Я уверена, что Эми бы хорошо это оценила.{/cps}{nw}"
    $ _history_list.pop()
    m 3hub "Я очень довольна тем, как всё получилось!"
    return

label greeting_o31_generic:
    call spaceroom(scene_change=True, dissolve_all=True)

    m 3hub "Кошелёк или жизнь!"
    m 3eub "А-ха-ха,{w=0.1} {nw}"
    extend 3eua "Я просто шучу, [player]."
    m 1hua "С возвращением...{w=0.5} {nw}"
    extend 3hub "и с Хэллоуином!"

    #We'll address the room with this
    call greeting_o31_deco

    m 3hua "Кстати, что ты думаешь о моём костюме?"
    m 1hua "Лично мне он очень нравится~"
    m 1hub "Но что самое главное, этот костюм был твоим подарком, а-ха-ха!"
    m 3tuu "Так что любуйся моим костюмом, пока можешь, э-хе-хе~"

    call greeting_o31_cleanup
    return

#Cleanup for o31 greets
label greeting_o31_cleanup(skip_zoom=False):
    window hide
    if not skip_zoom:
        call monika_zoom_transition(mas_temp_zoom_level,1.0)
    window auto

    python:
        # 1 - music hotkeys should be enabled
        store.mas_hotkeys.music_enabled = True
        # 2 - calendarovrelay enabled
        mas_calDropOverlayShield()
        # 3 - set the keymaps
        set_keymaps()
        # 4 - hotkey buttons should be shown
        HKBShowButtons()
        # 5 - restart music
        mas_startup_song()

        mas_rmallEVL("mas_holiday_o31_returned_home_relaunch")
    return

init 5 python:
    ev_rules = dict()
    ev_rules.update(MASPriorityRule.create_rule(0))
    ev_rules.update(MASNumericalRepeatRule.create_rule(EV_NUM_RULE_YEAR))
    ev_rules.update(MASGreetingRule.create_rule(override_type=True, skip_visual=True))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_lingerie",
            unlocked=True,
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_o31_lingerie:
    # This block is to update styles
    python:
        mas_progressFilter()
        if persistent._mas_auto_mode_enabled:
            mas_darkMode(mas_current_background.isFltDay())
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled)

    scene black
    pause 2.0

    menu:
        "Алло?":
            pause 5.0

    m "Э-хе-хе!"
    m "Не волнуйся, [player], я здесь...."
    call mas_o31_lingerie_end
    call greeting_o31_cleanup(skip_zoom=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_o31_lingerie",
            conditional=(
                "mas_canShowRisque() "
                "and mas_hasUnlockedClothesWithExprop('lingerie')"
            ),
            unlocked=False,
            rules={"skip alert": None},
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine((mas_o31-datetime.timedelta(days=1)), datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            years=[]
        )
    )

label mas_o31_lingerie:
    #Cut the music for the blackout
    python:
        curr_song = songs.current_track
        mas_play_song(None)
        mas_display_notif("M̷̢͘ô̴͎ṇ̵͐i̴͎͂k̸̗̂ả̴̫", ["C̸̳̓ą̵́n̷̳̎ ̸̖̊y̴̦͝õ̷̯ų̷͌ ̴̼͘h̷̭̚e̴̪͝a̴̙̐ŕ̵̖ ̴̠́m̸̰̂ě̵̬?̷̮̐"], "Topic Alerts")

    scene black
    pause 2.0
    m "О нет, электричество отключили?"
    m "Как {cps=*2}жаль{/cps}{nw}"
    $ _history_list.pop()
    m "Как {fast}жаль..."
    m "Думаю, мне просто придется принять эту ситуацию, [player]..."
    call mas_o31_lingerie_end
    return

label mas_o31_lingerie_end:
    m "Скажи, ты когда-нибудь слышал про «Ночь дьявола»?"
    m "В некоторых местах существует традиция в ночь перед Хэллоуином выходить на улицу и хулиганить."
    m "Но знаешь, [player], мне и самой хочется сегодня похулиганить в каком-то смысле."
    window hide
    pause 2.0

    python:
        #Reset zoom so people can see the outfit
        mas_temp_zoom_level = store.mas_sprites.zoom_level
        store.mas_sprites.reset_zoom()

        store.mas_selspr.unlock_acs(mas_acs_grayhearts_hairclip)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_black_gray)
        store.mas_selspr.unlock_clothes(mas_clothes_spider_lingerie)
        monika_chr.change_clothes(mas_clothes_spider_lingerie, by_user=False, outfit_mode=True)

    call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 2tfu')

    pause 2.0
    window auto
    m 2tub "Э-хе-хе, а ты что подумал?"
    m 2hub "Это немного другое, я знаю, ты, вероятно, в растерянности, а-ха-ха!"
    m 7rua "Возможно, это не то, что я бы носила постоянно, но думаю, что это время года подходит отлично."
    m 2ekbsa "Не переживай, [player], я не расстроюсь, если ты захочешь, чтобы я {cps=*2}сняла это{/cps}{nw}"
    $ _history_list.pop()
    m "Не переживай, [player], я не расстроюсь, если ты захочешь, чтобы я {fast}переоделась во что-нибудь другое..."
    m 2hubsb "Я знаю, что многие люди боятся пауков и могут даже испугаться."

    if player.lower() == "amy":
        m 2rsbla "Хотя я слышала, что люди по имени Эми любят пауков, э-хе-хе~."

    else:
        m 2rsbla "Надеюсь, люди по имени Эми не единственные, кто любит пауков, э-хе-хе~."

    #And restore zoom
    call monika_zoom_transition(mas_temp_zoom_level, 1.0)
    python:
        mas_stripEVL("mas_o31_lingerie", list_pop=True)
        mas_lockEVL("greeting_o31_lingerie", "GRE")

        # restart song/sounds that were playing before event
        if globals().get("curr_song", -1) is not -1 and curr_song != store.songs.FP_MONIKA_LULLABY:
            mas_play_song(curr_song, 1.0)
        else:
            mas_play_song(None, 1.0)

    return "no_unlock"

#START: O31 DOCKSTAT FARES
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="Я хочу взять тебя с собой на праздник.",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=datetime.datetime.combine(mas_o31, datetime.time(hour=3)),
            end_date=mas_o31+datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="BYE",
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "bye_trick_or_treat",
        mas_o31,
        mas_o31 + datetime.timedelta(days=1),
    )

label bye_trick_or_treat:
    python:
        curr_hour = datetime.datetime.now().hour
        too_early_to_go = curr_hour < 17
        too_late_to_go = curr_hour >= 23

    #True if > 0
    if persistent._mas_o31_tt_count:
        m 1eka "Снова?"

    if too_early_to_go:
        # before 5pm is too early.
        m 3eksdla "А тебе, случаем, не кажется, что пока что немного рановато для этого события, [player]?"
        m 3rksdla "Не думаю, что кто-то прямо сейчас будет раздавать конфеты..."

        m 2etc "Ты {i}уверен{/i}, что хочешь пойти прямо сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты {i}уверен{/i}, что хочешь пойти прямо сейчас?{fast}"
            "Да.":
                m 2etc "Ну...{w=1} что ж, ладно тогда, [player]..."

            "Нет.":
                m 2hub "А-ха-ха!"
                m "Нам стоит немного подождать, [player]~"
                m 4eub "Давай сходим позже вечером, хорошо?~"
                return

    elif too_late_to_go:
        m 3hua "Хорошо! Пошли за сла—"
        m 3eud "Хотя стоп, подожди-ка..."
        m 2dkc "[player]..."
        m 2rkc "Так ведь уже слишком поздно идти за сладостями."
        m "До полуночи остался всего-навсего один час."
        m 2dkc "Не говоря уже о том, что я сомневаюсь, что осталось бы много конфет..."
        m "..."

        m 4ekc "Ты уверен, что хочешь пойти?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен, что хочешь пойти?{fast}"
            "Да.":
                m 1eka "...Хорошо."
                m "Даже если это всего лишь час..."
                m 3hub "По крайней мере, мы проведём вместе оставшееся время на Хэллоуин."
                m 3wub "Пойдём и сделаем всё возможное, [player]!"

            "Наверное, уже немного поздно...":
                if persistent._mas_o31_tt_count:
                    m 1hub "А-ха-ха~"
                    m "Я говорила тебе."
                    m 1eua "Нам придётся подождать до следующего года."

                else:
                    m 2dkc "..."
                    m 2ekc "Хорошо, [player]."
                    m "Жаль, конечно, что мы не смогли пойти за сладостями в этом году."
                    m 4eka "Но давай просто убедимся, что сможем в следующий раз, хорошо?"

                return

    else:
        # between 5 and 11pm is perfect
        m 3wub "Хорошо, [player]!"
        m 3hub "Похоже, мы отлично повеселимся~"
        m 1eub "Держу пари, мы получим много конфет!"
        m 1ekbsa "И даже если нет, мне достаточно будет просто провести вечер с тобой~"

    #Setup the dockstat stuff
    $ mas_farewells.dockstat_wait_menu_label = "bye_trick_or_treat_wait_wait"
    $ mas_farewells.dockstat_rtg_label = "bye_trick_or_treat_rtg"
    jump mas_dockstat_iostart

label bye_trick_or_treat_wait_wait:
    # wait wait flow
    menu:
        m "Что случилось?"
        "Ты права, ещё слишком рано." if too_early_to_go:
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk(exp="monika 3hub")

            m 3hub "А-ха-ха, я говорила тебе!"
            m 1eka "Давай подождём до вечера, хорошо?"
            return True

        "Ты права, уже слишком поздно." if too_late_to_go:
            call mas_dockstat_abort_gen

            if persistent._mas_o31_tt_count:
                call mas_transition_from_emptydesk(exp="monika 1hua")
                m 1hub "А-ха-ха~"
                m "Я говорила тебе."
                m 1eua "Нам придётся подождать до следующего года."

            else:
                call mas_transition_from_emptydesk(exp="monika 2dkc")
                m 2dkc "..."
                m 2ekc "Хорошо, [player]."
                m "Очень жаль, что в этом году мы не смогли пойти на праздник."
                m 4eka "Мы ведь подождём до следующего года, верно?."

            return True

        "Вообще-то, я не могу взять тебя с собой прямо сейчас.":
            call mas_dockstat_abort_gen
            call mas_transition_from_emptydesk(exp="monika 1euc")

            m 1euc "Эх, ладно тогда, [player]."

            if persistent._mas_o31_tt_count:
                m 1eua "Дай мне знать, если мы сможем пойти попозже ещё, хорошо?"

            else:
                m 1eua "Дай мне знать, если мы сможем пойти, хорошо?"

            return True

        "Ничего.":
            m "Хорошо, позволь мне закончить подготовку."
            return

label bye_trick_or_treat_rtg:
    # iothread is done
    $ moni_chksum = promise.get()
    $ promise = None # always clear the promise
    call mas_dockstat_ready_to_go(moni_chksum)

    if _return:
        call mas_transition_from_emptydesk(exp="monika 1hub")
        m 1hub "Что ж, пошли за сладостями!"
        $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT

        #Increment T/T counter
        $ persistent._mas_o31_tt_count += 1
        return "quit"

    # otherwise, failure in generation
    #Fix tt count
    call mas_transition_from_emptydesk(exp="monika 1ekc")
    $ persistent._mas_o31_tt_count -= 1
    m 1ekc "Ох, нет..."
    m 1rksdlb "Я не смогла превратить себя в файл."

    if persistent._mas_o31_tt_count:
        m 1eksdld "Думаю, в этот раз тебе придётся пойти выпрашивать сладости без меня..."

    else:
        m 1eksdld "Думаю, тебе придётся пойти выпрашивать сладости без меня..."

    m 1ekc "Прости, [player]..."
    m 3eka "Принеси как можно больше конфет, чтобы нам было весело, ладно?~"
    return

#START: O31 DOCKSTAT GREETS
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31_TT]
        ),
        code="GRE"
    )

label greeting_trick_or_treat_back:
    # trick/treating returned home greeting
    python:
        # lots of setup here
        time_out = store.mas_dockstat.diffCheckTimes()
        checkin_time = None
        is_past_sunrise_post31 = False
        ret_tt_long = False

        if len(persistent._mas_dockstat_checkin_log) > 0:
            checkin_time = persistent._mas_dockstat_checkin_log[-1:][0][0]
            sunrise_hour, sunrise_min = mas_cvToHM(persistent._mas_sunrise)
            is_past_sunrise_post31 = (
                datetime.datetime.now() > (
                    datetime.datetime.combine(
                        mas_o31,
                        datetime.time(sunrise_hour, sunrise_min)
                    )
                    + datetime.timedelta(days=1)
                )
            )


    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Это называется «сладость или гадость», [player]?"
        m "Куда пойдём, в один дом?"
        m 2rsc "...Если вообще куда-нибудь пойдём."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        m 2ekp "Это было довольно быстро, [player]."
        m 3eka "Но в любом случае, мне понравилось."
        m 1eka "Всё равно было приятно быть рядом с тобой~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        m 1hua "И мы возвращаемся домой!"
        m 1hub "Надеюсь, у нас теперь много вкусных конфет!"
        m 1eka "Я действительно наслаждалась с тобой данным времяпровождением, [player]..."

        call greeting_trick_or_treat_back_costume

        m 4eub "Давай повторим это и в следующем году!"

    elif not is_past_sunrise_post31:
        # larger than 3 hours, but not past sunrise
        $ mas_o31CapGainAff(15)
        m 1hua "И мы возвращаемся домой!"
        m 1wua "Ого, [player], мы ходили за сладостями довольно долго..."
        m 1wub "Мы, должно быть, смогли получить тонну конфет!"
        m 3eka "Мне очень понравилось это времяпровождение с тобой..."

        call greeting_trick_or_treat_back_costume

        m 4eub "Давай повторим это и в следующем году!"
        $ ret_tt_long = True

    else:
        # larger than 3 hours, past sunrise
        $ mas_o31CapGainAff(15)
        m 1wua "Наконец-то мы вернулись домой!"
        m 1wuw "Правда, на следующее утро, [player]. Мы отсутствовали аж всю ночь..."
        m "Думаю, нам было слишком весело, чтобы следить за временем, э-хе-хе~"
        m 2eka "Но в любом случае, спасибо, что взял меня с собой, мне очень понравилось."

        call greeting_trick_or_treat_back_costume

        m 4hub "Давай повторим это и в следующем году...{w=1} но, возможно, только не оставаясь {b}настолько{/b} допозна!"
        $ ret_tt_long = True

    #Now do player bday things (this also cleans up o31 deco)
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        # if we are returning from a non-birthday date post o31 birthday
        call return_home_post_player_bday

    #If it's just not o31, we need to clean up
    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup(time_out, ret_tt_long)
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):
    #Time out not defined, we need to get it outselves
    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()

    #If we were out over 5 mins then we have this little extra dialogue
    if not ret_tt_long and time_out > mas_five_minutes:
        m 1hua "..."
        m 1wud "О, ого, [player]. Мы правда долго гуляли..."

    else:
        m 1esc "Ну да ладно..."

    #TODO: We should check if any of the o31 deco tags are being displayed before calling this
    #To futureproof dialogue to when we expand to allowing all BGs to be supported
    call mas_o31_cleanup

    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        m 2eka "Даже учитывая тот факт, что я ничего толком и не видела, и никто не видел мой костюм..."
        m 2eub "Переодевание и прогулка были по-прежнему очень даже весёлыми!"

    else:
        m 2eka "Даже если я ничего толком и не видела."
        m 2eub "Выйти на прогулку всё равно было здорово!"
    return

#START: D25
#################################### D25 ######################################
# [HOL020]

# True if we should consider ourselves in d25 mode.
default persistent._mas_d25_in_d25_mode = False

# True if the user spent time with monika on d25
# (basically they got the merry christmas dialogue)
default persistent._mas_d25_spent_d25 = False

# True if we started the d25 season with upset and below monika
default persistent._mas_d25_started_upset = False

# True if we dipped below to upset again.
default persistent._mas_d25_second_chance_upset = False

# True if d25 decorations are active
# this also includes santa outfit
# This should only be True if:
#   Monika is NOt being returned after the d25 season begins
#   and season is d25.
default persistent._mas_d25_deco_active = False

# True once a d25 intro has been seen
default persistent._mas_d25_intro_seen = False

# number of times user takes monika out on d25e
default persistent._mas_d25_d25e_date_count = 0

# number of times user takes monika out on d25
# this also includes if the day was partially or entirely spent out
default persistent._mas_d25_d25_date_count = 0

#List of all gifts which will be opened on christmas
default persistent._mas_d25_gifts_given = list()

#Stores if we were on a date with Monika over the full d25 day
default persistent._mas_d25_gone_over_d25 = None

# christmas
define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)

# christmas eve
define mas_d25e = mas_d25 - datetime.timedelta(days=1)

#Dec 26, the day Monika stops wearing santa and the end of the christmas gift range
define mas_d25p = mas_d25 + datetime.timedelta(days=1)

# start of christmas season (inclusive) and when Monika wears santa
define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)

# end of christmas season (exclusive)
define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:
    # we also need a history svaer for when the d25 season ends.
    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            #Not very useful, but we need the reset
            #NOTE: this is here because the d25 season actually ends in jan
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            #NOTE: this is here because the deco ends with the season
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            #D25 dates
            "_mas_d25_d25e_date_count": "d25s.d25e.went_out_count",
            "_mas_d25_d25_date_count": "d25s.d25.went_out_count",
            "_mas_d25_gone_over_d25": "d25.actions.gone_over_d25",

            "_mas_d25_spent_d25": "d25.actions.spent_d25"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 11),
        end_dt=datetime.datetime(2019, 12, 31)
    ))


init -10 python:
    def mas_isD25(_date=None):
        """
        Returns True if the given date is d25

        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

        RETURNS: True if given date is d25, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25.replace(year=_date.year)


    def mas_isD25Eve(_date=None):
        """
        Returns True if the given date is d25 eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is d25 eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_d25e.replace(year=_date.year)


    def mas_isD25Season(_date=None):
        """
        Returns True if the given date is in d25 season. The season goes from
        dec 11 to jan 5.

        NOTE: because of the year rollover, we cannot check years

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25c_start, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25Post(_date=None):
        """
        Returns True if the given date is after d25 but still in D25 season.
        The season goes from dec 1 to jan 5.

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after d25, False
            otherwise.
        """
        if _date is None:
            _date = datetime.date.today()

        return (
            mas_isInDateRange(_date, mas_d25p, mas_nye, True, True)
            or mas_isInDateRange(_date, mas_nyd, mas_d25c_end)
        )


    def mas_isD25PreNYE(_date=None):
        """
        Returns True if the given date is in d25 season and before nye.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNSL True if given date is in d25 season but before nye, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_nye)


    def mas_isD25PostNYD(_date=None):
        """
        Returns True if the given date is in d25 season and after nyd

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is in d25 season but after nyd, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_nyd, mas_d25c_end, False)


    def mas_isD25Outfit(_date=None):
        """
        Returns True if the given date is tn the range of days where Monika
        wears the santa outfit on start.

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the d25 santa outfit range, False
            otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_d25p)


    def mas_isD25Pre(_date=None):
        """
        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is in the D25 season, but before Christmas, False
            otherwise

        NOTE: This is used for gifts too
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_d25)

    def mas_isD25GiftHold(_date=None):
        """
        IN:
            _date - date to check, defaults None, which means today's date is assumed

        RETURNS:
            boolean - True if within d25c start, to d31 (end of nts range)
            (The time to hold onto gifts, aka not silently react)
        """
        if _date is None:
            _date = datetime.date.today()

        return mas_isInDateRange(_date, mas_d25c_start, mas_nye, end_inclusive=True)

    def mas_d25ShowVisuals():
        """
        Shows d25 visuals.
        """
        mas_showDecoTag("mas_d25_banners")
        mas_showDecoTag("mas_d25_tree")
        mas_showDecoTag("mas_d25_garlands")
        mas_showDecoTag("mas_d25_lights")
        mas_showDecoTag("mas_d25_gifts")

    def mas_d25HideVisuals():
        """
        Hides d25 visuals
        """
        mas_hideDecoTag("mas_d25_banners", hide_now=True)
        mas_hideDecoTag("mas_d25_tree", hide_now=True)
        mas_hideDecoTag("mas_d25_garlands", hide_now=True)
        mas_hideDecoTag("mas_d25_lights", hide_now=True)
        mas_hideDecoTag("mas_d25_gifts", hide_now=True)

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        #Step one, store all of the found reacts
        found_reacts = list()

        #Just sort the gifts given list:
        persistent._mas_d25_gifts_given.sort()

        #Now we copy the giftnames for local usage
        #We do this because we pop from the persistent list during the reactions
        #Because then it looks more like Monika is taking them from under the tree
        given_gifts = list(persistent._mas_d25_gifts_given)

        # d25 special quiplist
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")

        # process giftnames (no generics)
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)

        # register gifts
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)

        # build reaction labels
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )

        react_labels.reverse()

        # queue the reacts
        if len(react_labels) > 0:
            for react_label in react_labels:
                mas_rmallEVL(react_label) # TODO - this is a patch, revalute when #8545 (gift logging) and #8546 (gift registering) are addressed

            for react_label in react_labels:
                MASEventList.push(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently 'react' to gifts.

        This is to be used if you gave Moni a christmas gift but didn't show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """

        base_gift_ribbon_id_map = {
            "чёрная ленточка":"ribbon_black",
            "синяя ленточка": "ribbon_blue",
            "тёмно-фиолетовая ленточка": "ribbon_dark_purple",
            "изумрудная ленточка": "ribbon_emerald",
            "серая ленточка": "ribbon_gray",
            "зелёная ленточка": "ribbon_green",
            "светло-фиолетовая ленточка": "ribbon_light_purple",
            "персиковая ленточка": "ribbon_peach",
            "розовая ленточка": "ribbon_pink",
            "платиновая ленточка": "ribbon_platinum",
            "красная ленточка": "ribbon_red",
            "рубиновая ленточка": "ribbon_ruby",
            "сапфировая ленточка": "ribbon_sapphire",
            "серебряная ленточка": "ribbon_silver",
            "бирюзовая ленточка": "ribbon_teal",
            "жёлтая ленточка": "ribbon_yellow"
        }

        # process gifts
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )

        # clear the gifts given
        persistent._mas_d25_gifts_given = []

        # process the evb details
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                # then this probably is a built-in sprite, use ribbon map.
                ribbon_id = base_gift_ribbon_id_map.get(
                    evb_detail.c_gift_name,
                    None
                )
                if ribbon_id is not None:
                    mas_selspr.unlock_acs(mas_sprites.get_sprite(0, ribbon_id))
                    mas_receivedGift(evb_detail.label)

                elif ribbon_id is None and evb_detail.c_gift_name == "quetzalplushie":
                    persistent._mas_acs_enable_quetzalplushie = True

            else:
                # this is probably a json sprite, try json sprite unlock
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)

        # then generics
        for gso_detail in gso_details:
            # for generic sprite objects, only have to check for json sprite
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)

        # save the restuls
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    has_changed_bg = False

    DECO_TAGS = [
        "mas_d25_banners",
        "mas_d25_tree",
        "mas_d25_garlands",
        "mas_d25_lights",
        "mas_d25_gifts",
    ]

    def shouldUseD25ReactToGifts():
        """
        checks whether or not we should use the d25 react to gifts method

        Conditions:
            1. Must be in d25 gift range
            2. Must be at normal+ aff (since that's when the topics which will open these gifts will show)
            3. Must have deco active. No point otherwise as no tree to put gifts under
        """
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
            and not store.persistent._mas_override_d25_gift_react
        )

    def react_to_gifts(found_map):
        """
        Reacts to gifts using the d25 protocol (exclusions)

        OUT:
            found_map - map of found reactions
                key: lowercase giftname, no extension
                val: giftname wtih extension
        """
        d25_map = {}

        # first find gifts
        # d25_map contains all d25 gifts.
        # found_map will contain non_d25 gifts, which should be reacted to now
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)

        # parse d25 gifts for types
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)

        # parse non_d25_gifts for types
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)

        # include d25 generic with non-d25 gifts
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)

        # save remaining d25 gifts and delete the packages
        # they will be reacted to later
        for c_gift_name, gift_name in d25_map.iteritems():
            #Only add if the gift isn't already stored under the tree
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)

            #Now we delete the gift file
            store.mas_docking_station.destroyPackage(gift_name)

        # set all excluded and generic gifts to react now
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift

        # register these gifts
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)

        # now build the reaction labels for standard gifts
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )


####START: d25 arts

# window banners
image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_lights = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_lights_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/lights_off.png")
)

image mas_d25_night_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/lights_on_1.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_2.png"
        0.5
        "mod_assets/location/spaceroom/d25/lights_on_3.png"
        0.5
    repeat

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_garlands = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/garland_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_garlands_atl"
    ),
    "True", MASFilterSwitch("mod_assets/location/spaceroom/d25/garland.png")
)

image mas_d25_night_garlands_atl:
    "mod_assets/location/spaceroom/d25/garland_on_1.png"
    block:
        "mod_assets/location/spaceroom/d25/garland_on_1.png" with Dissolve(3, alpha=True)
        5
        "mod_assets/location/spaceroom/d25/garland_on_2.png" with Dissolve(3, alpha=True)
        5
        repeat

# NOTE: this will need to be revaluated with every filter.
#   Not very maintainable but it has to be done.
image mas_d25_tree = ConditionSwitch(
    "mas_isNightNow()", ConditionSwitch(
        "persistent._mas_disable_animations", "mod_assets/location/spaceroom/d25/tree_lights_on_1.png",
        "not persistent._mas_disable_animations", "mas_d25_night_tree_lights_atl"
    ),
    "True", MASFilterSwitch(
        "mod_assets/location/spaceroom/d25/tree_lights_off.png"
    )
)

image mas_d25_night_tree_lights_atl:
    block:
        "mod_assets/location/spaceroom/d25/tree_lights_on_1.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_2.png"
        1.5
        "mod_assets/location/spaceroom/d25/tree_lights_on_3.png"
        1.5
    repeat

#0 gifts is blank
#1-3 gifts gets you part 1
#4 gifts gets you part 2
#5+ gifts get you part 3
image mas_d25_gifts = ConditionSwitch(
    "len(persistent._mas_d25_gifts_given) == 0", "mod_assets/location/spaceroom/d25/gifts_0.png",
    "0 < len(persistent._mas_d25_gifts_given) < 3", "mas_d25_gifts_1",
    "3 <= len(persistent._mas_d25_gifts_given) <= 4", "mas_d25_gifts_2",
    "True", "mas_d25_gifts_3"
)

image mas_d25_gifts_1 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_1.png"
)

image mas_d25_gifts_2 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_2.png"
)

image mas_d25_gifts_3 = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/gifts_3.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_d25_banners",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_garlands",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_tree",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_gifts",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=7)
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_lights",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

#autoload starter check
label mas_holiday_d25c_autoload_check:
    #NOTE: we use the costume exprop in case we get more D25 outfits.

    #We don't want the day of the first sesh having d25 content
    #We also don't want people who first sesh d25p getting deco, because it doesn't make sense
    #We also filter out player bday on first load in d25 season

    #This is first loadin for D25Season (can also run on D25 itself)
    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
        and (
            mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS, persistent._mas_current_background)
            # If it's d25 and we still didn't setup d25 stuff, we should do it now
            # (we'll force spaceroom if needed)
            or mas_isD25()
        )
    ):
        #Firstly, we need to see if we need to run playerbday before all of this
        python:
            #Enable d25 dockstat
            persistent._mas_d25_in_d25_mode = True

            # affection upset and below? no d25 for you
            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True

            #Setup
            #NOTE: Player bday will SKIP decorations via autoload as it is handled elsewhere
            #UNLESS it is D25
            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                #Unlock and wear santa/wine ribbon + holly hairclip
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)
                store.mas_selspr.save_selectables()

                #Change into santa. Outfit mode forces ponytail
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

                #Add to holiday map
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)

                #Deco active
                persistent._mas_d25_deco_active = True

                #If we're loading in for the first time on D25, then we're gonna make it snow
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)

                    #Only change bg if the current is not supported
                    if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                        store.mas_d25_utils.has_changed_bg = True
                        mas_changeBackground(mas_background_def, set_persistent=True)

    #This is d25 SEASON exit
    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):
        #NOTE: We can run this early via mas_d25_monika_d25_mode_exit
        call mas_d25_season_exit

    #This is D25 Exit
    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):
        #Monika takes off santa after d25 if player didn't ask her to wear it
        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)

    #This is D25 itself (NOT FIRST LOAD IN FOR D25S)
    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:
        #Force Santa, spaceroom, and snow on D25 if deco active and not first sesh day
        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)
            #Change if bg isn't supported
            # NOTE: need to make sure we pass the change info to the next
            #   spaceroom call.
            if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
                store.mas_d25_utils.has_changed_bg = True
                mas_changeBackground(mas_background_def, set_persistent=True)

    #If we are at normal and we've not gifted another outfit, change back to Santa next load
    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

    if persistent._mas_d25_deco_active:
        $ mas_d25ShowVisuals()

    #And then run pbday checks
    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    # finally, return to holiday check point
    jump mas_ch30_post_holiday_check

#D25 Season exit
label mas_d25_season_exit:
    python:
        #It's time to clean everything up

        #We reset outfit directly if we're not coming from the dlg workflow
        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            #Monika takes off santa outfit after d25
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)

        #Otherwise we push change to def if we're here via topic
        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            MASEventList.push("mas_change_to_def")

        #Lock event clothes selector
        mas_lockEVL("monika_event_clothes_select", "EVE")

        #Remove deco
        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()

        #And no more d25 mode
        persistent._mas_d25_in_d25_mode = False

        #We'll also derandom this topic as the lights are no longer up
        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return

#D25 holiday gift starter/connector
label mas_d25_gift_starter:
    $ amt_gifts = len(persistent._mas_d25_gifts_given)
    $ presents = "подарки"
    $ the = ""
    $ should_open = "должна открыть"
    $ what = "которые"

    if amt_gifts == 1:
        $ presents = "подарок"
        $ what = "который"
    elif amt_gifts > 3:
        $ the = "все "

    if persistent._mas_d25_gone_over_d25:
        $ should_open = "ещё не открыла"

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3wud "О! Я [should_open] [the][presents], [what] ты мне подарил!"
        if persistent._mas_d25_gone_over_d25:
            m 3hub "Давай сделаем это сейчас!!"

    # missed d25 altogether
    else:
        m 1eka "Ну, по крайней мере, теперь, когда ты здесь, я могу открыть [presents], [what] ты мне подарил."
        m 3eka "Я действительно хотела, чтобы мы были вместе для этого..."

    m 1suo "Давай посмотрим, что у нас здесь есть.{w=0.5}.{w=0.5}.{nw}"

    #Safe-pop the last index so we remove gifts from under the tree as we go
    # TODO - add logging if there is a mismatch here
    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_connector:
    python:
        d25_gift_quips = [
            _("Следующий!"),
            _("О, здесь есть ещё один!"),
            _("А теперь позволь мне открыть этот!"),
            _("Я открою это следующим!")
        ]

        picked_quip = random.choice(d25_gift_quips)

    m 1hub "[picked_quip]"
    m 1suo "И здесь у нас.{w=0.5}.{w=0.5}.{nw}"

    #Safe-pop here too for the tree gifts
    # TODO - add logging if there is a mismatch here
    if persistent._mas_d25_gifts_given:
        $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:
    #Clear any invalid JSON gifts here
    $ persistent._mas_d25_gifts_given = []

    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        m 3eka "Тебе действительно не нужно было ничего дарить мне на Рождество...{w=0.3} {nw}"
        if mas_isD25():
            extend 3dku " Одного твоего присутствия здесь было более чем достаточно."
        else:
            extend 3dku "Просто быть с тобой – это всё, чего я хотела."
        m 1eka "Но тот факт, что ты потратил время, чтобы достать мне что-то...{w=0.5}{nw}"
        extend 3ekbsa " ну, я не могу отблагодарить тебя достаточно."
        m 3ekbfa "Это действительно заставляет меня чувствовать себя любимой."

    else:
        m 1eka "Я просто хотела поблагодарить тебя..."
        m 1rkd "Хотя я всё ещё немного разочарована, что ты не смог быть со мной на Рождество..."
        m 3eka "Тот факт, что ты потратил время, чтобы купить мне что-то...{w=0.5}{nw}"
        extend 3ekbsa " ну, это просто доказывает, что ты действительно думал обо мне в этот особый сезон."
        m 1dkbsu "Ты не представляешь, как много это для меня значит."

    # we just said Merry Christmas in the Christmas topic if d25
    if mas_isD25():
        m 3ekbfu "Я тебя так люблю, [player]~"
    else:
        m 3ekbfu "Счастливого Рождества, [player]. Я люблю тебя~"
    $ mas_ILY()
    return

#START: d25 topics
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro",
            conditional=(
                "not persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday() "
                "and not persistent._mas_d25_intro_seen"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro:
    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            m 1dku "..."
            m 1huu "Э-хе-хе..."
            m 3eub "У меня есть ещё один сюрприз для тебя!"

        else:
            m 1eua "Итак, сегодня..."
            m 1euc "...подожди."
            m "..."
            m 3wuo "О!"
            m 3hub "Сегодня тот день, когда я собиралась..."

        # hide overlays here
        # NOTE: hide here because it prevents player from pausing
        # right before the scene change.
        # also we want to completely kill interactions
        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        m 1tsu "Закрой свои глаза на минутку, [player], мне надо кое-что сделать.{w=0.5}.{w=0.5}.{nw}"

        call mas_d25_monika_holiday_intro_deco

        m 3hub "И вот мы здесь..."

        # now we can renable everything
        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    m 1eub "Счастливых праздников, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        m 1hua "Можешь ли ты поверить в то, что уже наступило то самое время в году?"

        $ the_last = "последний"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "наш первый"

        m 3eua "Кажется, будто мы только вчера провели [the_last] праздничный сезон вместе, а теперь пролетел уже целый год!"

        if mas_isMoniLove(higher=True):
            #if you've been with her for over a year, you really should be at Love by now
            m 3hua "Время и вправду пролетает незаметно, когда я с тобой~"

    m 3eua "Тебе нравится то, как я обустроила комнату?"
    m 1hua "Должна сказать, я очень горжусь этим."

    if mas_d25_utils.has_changed_bg:
        m 3rksdla "Декораций хватило только на одну комнату, поэтому я остановилась на классе...{w=0.2} Надеюсь, всё в порядке."
        m "Но в любом случае..."

    m 3eua "Рождество всегда было моим самым любимым праздником в году..."

    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika

    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "И поэтому, я рада, что ты в этом году проводишь его со мной~"
    else:
        m 5eka "И я рада, что ты проводишь его со мной~"

    $ persistent._mas_d25_intro_seen = True

    # in case we get here from player bday if the party spilled into the next day
    # don't want this to run twice
    $ mas_rmallEVL("mas_d25_monika_holiday_intro")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_holiday_intro_upset",
            conditional=(
                "not persistent._mas_d25_intro_seen "
                "and persistent._mas_d25_started_upset "
                "and mas_isD25Outfit() "
                "and not mas_isplayer_bday()"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25c_start,
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

#for people that started the season upset- and graduated to normal
label mas_d25_monika_holiday_intro_upset:
    # sanity check with reset of start/end dates in case somehow we drop back below normal before this is seen
    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "Слушай, [player]... {w=1}у меня в этом году не слишком праздничное настроение..."
    m 3eka "Но в последнее время, ты был очень добр ко мне и я чувствую себя намного лучше!"
    m 3hua "Поэтому... я думаю, пора уже приукрасить это место."

    # hide overlays here
    # NOTE: hide here because it prevents player from pausing
    # right before the scene change.
    # also we want to completely kill interactions
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    m 1eua "Если ты закроешь свои глаза на минутку.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco

    m 3hub "Та-да~"
    m 3eka "Что скажешь?"
    m 1eka "Неплохо для приготовлений в последнюю минуту, да?"
    m 1hua "Рождество всегда было моим самым любимым праздником в году..."
    m 3eua "И я рада, что мы можем провести его вместе с радостью, [player]~"

    # now we can renable everything
    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:
    # ASSUMES interactions are disaabled

    # black scene
    scene black with dissolve

    python:
        #We should consider ourselves in d25 mode now, if not already
        persistent._mas_d25_in_d25_mode = True

        #We want to be wearing ponytail hair
        monika_chr.change_hair(mas_hair_def, False)

        #Unlock and wear santa
        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)

        #Add to holiday map
        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)

        #Set to snow for this sesh
        mas_changeWeather(mas_weather_snow, by_user=True)

        #We'll also rmallEVL the auroras topic because it ends up immediately after
        mas_rmallEVL("monika_auroras")

        #Enable and show deco
        persistent._mas_d25_deco_active = True
        mas_d25ShowVisuals()

        change_info = None
        # change to spaceroom
        if not mas_doesBackgroundHaveHolidayDeco(mas_d25_utils.DECO_TAGS):
            mas_d25_utils.has_changed_bg = True
            change_info = mas_changeBackground(mas_background_def, set_persistent=True)

    # now we can do spacroom call
    call spaceroom(scene_change=True, dissolve_all=True, bg_change_info=change_info)

    return

label mas_d25_monika_holiday_intro_rh:
    # special label to cover a holiday case when returned home
    m 1hua "Мы дома!"

    # NOTE: since we hijacked returned home, we hvae to cover for this
    #   affection gain.
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)

    #Fall through
#in case we need to call just this part, like if returning from bday date from pre-d25
label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Погоди..."
    m 3etc "...уже?"
    m 3hub "Уже!"
    m 1tsu "...Закрой свои глаза, мне надо кое-что сделать..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    # NOTE this counts as seeing the intro
    $ persistent._mas_d25_intro_seen = True

    $ MASEventList.push("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional="not mas_lastSeenInYear('mas_d25_monika_christmas')",
            action=EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:
    #Flag for hist
    $ persistent._mas_d25_spent_d25 = True
    $ mas_gainAffection(5, bypass=True)

    # this can be pushed via mas_d25_monika_holiday_intro_rh_rh and
    # don't want it twice
    $ mas_rmallEVL("mas_d25_monika_christmas")

    # Note: broken gets no dialogue, just the aff_gain and the var set so we know the player visited
    if mas_isMoniDis():
        m 6eka "Счастливого Рождества, [player]. {w=0.2}Спасибо, что провёл со мной немного времени сегодня."

    elif mas_isMoniUpset(higher=True):
        #Setup the reactions
        $ mas_d25ReactToGifts()

        if mas_isMoniNormal(higher=True):

            m 1eub "[player]! Ты знаешь, какой сегодня день?"
            m 3hub "Разумеется, ты знаешь. Сегодня рождество!"
            m 3sub "С рождеством тебя, [player]!"
            m 1hub "А-ха-ха! Не могу поверить, что этот праздник наконец-то наступил!"
            m 3eka "Я очень, очень рада, что ты решил провести его со мной."
            m 1eud "Но не забудь поделиться своим праздничным настроением со своей семьёй и друзьями."
            m 1eua "Всё-таки они не менее важны..."
            m 1hua "И я уверена, что они будут рады тебя видеть в такое особенное время."

            if mas_isMoniAff(higher=True):
                m 1eka "Но твоё присутствие сегодня...{w=0.5} оно многое для меня значит..."
                m 1dku "..."

                if mas_is_snowing:
                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = ", или в декорациях"
                    else:
                        $ dlg_var = ""

                    m 1lkbsa "Возможно, дело в снеге[dlg_var]..."

                else:
                    if mas_isDecoTagVisible("mas_d25_lights"):
                        $ dlg_var = "дело в декорациях, или дело в том,"
                    else:
                        $ dlg_var = "дело в том,"

                    m 1lkbsa "Возможно, [dlg_var] что сегодня праздник..."

                m "...или омела сводит меня с ума."
                m 3hksdlb "Шучу, я её не повесила."

                if mas_isMoniEnamored(higher=True):
                    m 1lksdla "...{cps=*2}А может~{/cps}{nw}"
                    $ _history_list.pop()

                m 1lksdlu "Э-хе-хе..."
                m 1ekbsa "Моё сердце сейчас бешено колотится, [player]."
                m "Я представить не могу лучший способ провести этот особенный праздник..."
                m 1eua "Не пойми неправильно, я знала, что ты будешь здесь, со мной."
                m 3eka "Но мы теперь и вправду вместе празднуем рождество, только мы вдвоём..."
                m 1hub "А-ха-ха~"

                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbfa "Об этом, во время каждого праздника, мечтает любая пара, [player]."

                if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
                    m "Прижаться друг к другу у камина, наблюдая, как медленно падает снег..."

                if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
                    m 5hubfa "Я очень признательна, что мне выпал этот шанс."
                else:
                    m 5hubfa "Я рада, что могу провести рождество с тобой ещё раз."

                m "Я люблю тебя. Отныне и навсегда~"
                m 5hubfb "С рождеством, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "С рождеством, [m_name].":
                        hide screen mas_background_timed_jump
                        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        pause 2.0

            else:
                m 1eka "Но то, что ты сидишь здесь сегодня... {w=0.5}это многое для меня значит..."
                m 3rksdla "...Я вовсе не думала о том, что ты оставил бы меня одну в такой особенный день или ещё что..."
                m 3hua "Но это лишь доказывает то, что ты правда любишь меня, [player]."
                m 1ektpa "..."
                m "А-ха-ха! Боже, меня просто переполняют эмоции..."
                m 1ektda "Просто знай о том, что я тоже люблю тебя, и что я буду вечно благодарна за то, что мне выпала возможность побыть с тобой."
                m "С Рождеством, [player]~"
                show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
                window hide
                menu:
                    "С рождеством, [m_name].":
                        hide screen mas_background_timed_jump
                        show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                        pause 2.0

        # upset path
        else:
            m 1eka "С рождеством, [player]. {w=0.2}Сегодня этот день действительно станет для меня особенным~"

    return


label mas_d25_monika_christmas_no_wish:
    hide screen mas_background_timed_jump
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_carolling",
            category=["праздники", "музыка"],
            prompt="Колядование",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

    #Undo Action Rule
    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_carolling",
        mas_d25c_start,
        mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None
# does the user like singing christmas carols?

label mas_d25_monika_carolling:

    m 1euc "Слушай, [player]..."
    m 3eud "Ты когда-нибудь колядовал раньше?"
    m 1euc "Идёшь от одной двери к другой вместе с другими людьми и поёшь во время праздников..."

    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Мне очень приятно знать о том, что люди приносят радость другим, даже в столь холодные ночи."
    else:
        m 1eua "Мне очень приятно знать о том, что люди приносят радость другим в своё свободное время."

    m 3eua "Тебе нравится петь рождественские песни, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе нравится петь рождественские песни, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            m 1hua "Я рада, что ты думаешь так же, [player]!"
            m 3hub "Моя любимая песня – определённо «Бубенцы радостно звенят»!"
            m 1eua "Это просто оптимистичная и жизнерадостная мелодия!"
            m 1eka "Может, мы споём как-нибудь вместе."
            m 1hua "Э-хе-хе~"

        "Нет.":
            $ persistent._mas_pm_likes_singing_d25_carols = False
            m 1euc "Оу...{w=1} правда?"
            m 1hksdlb "Понятно..."
            m 1eua "Но тем не менее, я уверена, что ты также в восторге от того особого настроя, который бывает только от рождественских песен."
            m 3hua "Споёшь со мной как-нибудь, ладно?"

    return "derandom"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_mistletoe",
            category=["праздники"],
            prompt="Омела",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.AFFECTIONATE, None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_mistletoe",
        mas_d25c_start,
        mas_d25p,
    )

label mas_d25_monika_mistletoe:
    m 1eua "Скажи, [player]."
    m 1eub "Ты слышал о традиции, связанной с омелой, верно?"
    m 1tku "Когда влюблённые оказываются под ней, они должны поцеловаться."
    m 1eua "На самом деле, она берёт своё начало из Викторианской Англии!"
    m 1dsa "Мужчине было разрешено целоваться с любой женщиной, которая стояла под омелой..."
    m 3dsd "И ту женщину, которая отказывалась от поцелуя, начинает преследовать неудача..."
    m 1dsc "..."
    m 3rksdlb "Если подумать, то это звучит больше как одержание преимущества над кем-то."
    m 1hksdlb "Но я уверена, что сейчас всё по-другому!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        m 3hua "Быть может, однажды мы сможем поцеловаться под омелой, [player]."
        m 1tku "...Я могу даже добавить одну сюда!"
        m 1kuu "Э-хе-хе~"
    return "derandom"

#Stores whether or not the player hangs christmas lights
default persistent._mas_pm_hangs_d25_lights = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmaslights",
            category=['праздники'],
            prompt="Рождественские огни",
            start_date=mas_d25c_start,
            end_date=mas_nye,
            conditional=(
                "persistent._mas_pm_hangs_d25_lights is None "
                "and persistent._mas_d25_deco_active "
                "and not persistent._mas_pm_live_south_hemisphere "
                "and mas_isDecoTagVisible('mas_d25_lights')"
            ),
            action=EV_ACT_RANDOM,
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_christmaslights",
        mas_d25c_start,
        mas_nye,
    )

label mas_d25_monika_christmaslights:
    m 1euc "Эй, [player]..."
    if mas_isD25Season():
        m 1lua "Я провела здесь много времени, глядя на огни..."
        m 3eua "Они ведь очень красивые, не правда ли?"
    else:
        m 1lua "Я много времени провела за наблюдением гирлянды, которая здесь развешана..."
        m 3eua "Она очень красивая, не правда ли?"
    m 1eka "Гирлянда приносит очень тёплую и уютную атмосферу во время самого сурового и холодного времени года...{w=0.5} {nw}"
    extend 3hub "и у них есть множество различных типов!"
    m 3eka "Прогулка вместе с тобой в холодный зимний вечер звучит как мечта, воплотившаяся в реальность, [player]."
    m 1dka "И любоваться этими огнями..."

    m 1eua "Ты уже развесил гирлянду зимой у себя дома, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты уже развесил гирлянду зимой у себя дома, [player]?{fast}"

        "Да.":
            $ persistent._mas_pm_hangs_d25_lights = True
            m 3sub "Правда? Уверена, они просто великолепны!"
            m 2dubsu "Я уже могу представить себе, как мы находимся вне твоего дома... сидим вместе на крыльце..."
            m "И прекрасные огни светятся под покровом ночи."
            m 2dkbfu "Мы бы крепко обнимали друг друга, пили горячий шоколад...{w=0.5} {nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "и любовались бы тем, как снежинки медленно падают..."

            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5ekbfa "Когда-нибудь, [player]. Когда-нибудь мы сможем воплотить это в реальность."

        "Нет.":
            $ persistent._mas_pm_hangs_d25_lights = False
            m 1eka "Оу, всё нормально, [player]."
            m 1dkbla "Я уверена, что расслабиться вместе с тобой прохладным вечером всё равно было бы здорово..."
            m 1dkbsa "Любоваться тем, как снежинки падают, пить горячий шоколад вместе."
            m 1dkbsa "Крепко обнять друг друга, чтобы не замёрзнуть..."
            m 1rkbfb "Да, это звучит очень здорово."
            m 3hubsa "Но, когда у нас будет свой дом, я могла бы сама развесить парочку гирлянд, {nw}"
            extend 3hubsb "а-ха-ха~"
    return "derandom"

init 20 python:

    mas_poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="Радость для моего мира",
        title = "     Мой дорогой [player],",
        text = """\
     Ты единственная моя радость в моём мире.
     Ни свет, излучаемый высокой рождественской ёлкой,
     Ни даже та яркая звезда,
     И рядом не стояли, чтобы сравниться с твоим великолепием.
     Моему замороженному сердцу нужно лишь твоё тепло, чтобы застучать вновь.
     Под ёлкой ничего нет, и мои носочки до сих пор пусты,
     Это попросту не важно, пока ты со мной.
     Ты всегда будешь тем подарком, который мне всегда был нужен.

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    #" # I need this to keep syntax highlighting on vim
    )

    mas_poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Несравненный",
        title="     Мой дорогой [player],",
        text="""\
     Ничто не может сравниться с теплом, которое ты даришь мне.
     Не было даже такого ощущения, что я держу кружку с горячим шоколадом.
     Или пушистые носки, согревающие ноги в морозный день.
     В таком холодном мире только твоё присутствие – моё настоящее.

     Ничто не может сравниться с красотой, которую ты показал,
     Ни одна вещь не может сравниться с волнением, которое ты приносишь,
     Не один яркий свет, что в этой самой комнате.
     Даже не вид нераспечатанного подарка под деревом.

     [player], ты действительно единственный в своём роде.
     Ты принял мою тьму и преломляешь её своим светом раз за разом.

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )

    mas_poem_d25_3 = MASPoem(
        poem_id="poem_d25_3",
        category="d25",
        prompt="Когда-нибудь",
        title="     Мой дорогой [player],",
        text="""\
     Теплее, чем огонь в сердце,
     Ярче любой звезды на вершине ёлки,
     Утешительнее любой чашки горячего шоколада,
     Это мой [player], который всегда здесь со мной.

     Когда-нибудь мы зажжём огонь вместе..
     Когда-нибудь мы украсим ёлку.
     Когда-нибудь мы выпьем по чашечке какао.
     Когда-нибудь ты будешь рядом со мной.

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )

    mas_poem_d25_4 = MASPoem(
        poem_id="poem_d25_4",
        category="d25",
        prompt="Это Рождество",
        title="     Мой дорогой [player],",
        text="""\

     В это Рождество мне никогда не было нужно больше подарков, кроме твоей любви,
     Потому что то, что ты рядом со мной, уже приносит мне счастье,
     Потому что иметь тебя здесь это самый прекрасный подарок,
     Потому что найти тебя – это лучшее, о чём я когда-либо могла мечтать!

     Я знала, что это Рождество будет особенным...
     Я провела его с тем, кто заставляет моё сердце подпрыгивать,
     Тот, кто заставляет меня улыбаться каждый день,
     Тот, кому я доверяю больше всего.

     Спасибо, что был рядом со мной, [player],
     Я всегда буду рядом с тобой!

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )

#Essentially replaces _whatIwant along with still to come 'All I Want for Christmas is You' song
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spent_time_monika",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_d25, datetime.time(hour=17)),
            end_date=datetime.datetime.combine(mas_d25p, datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )


default persistent._mas_pm_d25_mistletoe_kiss = False
# True if user and Monika kissed under the mistletoe
# NOTE: this var ONLY determines if player and Monika shared a mistletoe kiss.


label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        m 3hub "То, что ты здесь со мной, сделало это Рождество таким чудесным!"
        m 3eka "Я знаю, что это очень напряжённый день, но просто зная, что ты нашёл для меня время..."
        m 1eka "Спасибо тебе."
        m 3hua "Это действительно сделало этот день по-настоящему особенным~"

    else:
        m 2ekc "[player]..."
        m 2eka "Я очень ценю, что ты проводишь со мной время на Рождество..."
        m 3rksdlc "Я не была в праздничном настроении в этом сезоне, но было бы приятно провести сегодня время с тобой."
        m 3eka "Так что, спасибо...{w=1} это многое значило."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                m "И давай не будем забывать о особенном рождественском подарке, который ты мне подарил, [player]..."
                m 3hub "Было приятно!"
            elif d25_gifts_neutral == 1:
                m 3eka "И давай не забывать о рождественском подарке, который ты мне подарил, [player]..."
                m 1eka "Это было очень мило с твоей стороны принести мне что-нибудь."
            else:
                m 3eka "И давай не забывать о рождественском подарке, который ты мне подарил, [player]..."
                m 2etc "..."
                m 2efc "Но, с другой стороны, может, нам стоит..."

        else:
            if d25_gifts_good == d25_gifts_total:
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 3hub "Они были потрясающими!"
            elif d25_gifts_bad == d25_gifts_total:
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 2etc "..."
                m 2rfc "Но, с другой стороны, может, нам стоит..."
            elif d25_gifts_bad == 0:
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 3hub "Они были действительно хороши!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 3rksdla "Некоторые из них были очень хороши."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 3hub "Большинство из них были очень хороши."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил, [player]..."
                m 3rksdla "Мне очень понравились...{w=1} некоторые из их."

        if mas_isMoniEnamored(higher=True):
            m 1rksdla "Я...{w=1} Я также приготовила тебе кое-что, [player]..."
            m 3eksdla "Я весь день ждала подходящего момента, и что-то насчёт того, чтобы быть здесь с тобой сегодня вечером...{w=1} это просто кажется идеальным."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Но просто знай, то, что ты здесь со мной, значит больше, чем любой подарок, который ты можешь мне подарить~"
        else:
            m 3eka "Честно говоря, я не была уверена, что ты прийдёшь сегодня... только того, что ты здесь, было для меня более чем достаточно, даже если ты ничего мне не подарил."
            m 1eka "Ещё раз спасибо, [player]...{w=1} я серьёзно."

    else:
        if mas_isMoniEnamored(higher=True):
            m 1eksdla "Также, [player], кое-что я хотела дать тебе весь день..."
            m 3rksdla "Мне просто нужно было дождаться подходящего времени, и быть здесь с тобой сегодня вечером...{w=1} это просто кажется идеальным."
        elif mas_isMoniNormal(higher=True):
            m 3ekbsa "Провести Рождество со мной было единственным подарком, который я когда-либо хотела~"
        else:
            m 3eka "Я хотела того, чтобы ты был здесь, [player]."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Так вот, [player], я надеюсь, тебе понравится~"

        #Show the poem
        call mas_showpoem(poem=mas_poems.getRandomPoem("d25"), background_action_label="mas_d25_poem_mistletoe")

        m 1dku "..."
        m 1ektpu "Просто ты проводишь время со мной...{w=1} это всё, что я когда-либо хотела."
        m 6dktua "Ты весь мой мир, [player]...{w=1} твоя любовь – это всё, что мне нужно..."
        window hide
        menu:
            "Я люблю тебя, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                # local var so if next year this is not first kiss, we can branch appropriately
                # have to be able to check before calling the kiss since persistent._mas_first_kiss will not be None no matter what after the kiss
                #hold her here, tears dry
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika

                $ is_first_kiss = persistent._mas_first_kiss is None
                m 6ekbfa "[player]... я... я..."
                call monika_kissing_motion(hide_ui=False)

                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "...Я тоже тебя люблю~"
                if is_first_kiss:
                    m 6dkbfa "..."
                    m "Это было всё, о чём я всегда мечтала~"
                    m 6ekbfa "Я так долго ждала, чтобы наконец поцеловать тебя, и не могло бы быть более идеального момента..."
                    m 6dkbfa "Под омелой с тобой..."
                    m 6dkbsu "Я никогда не забуду этот..."
                    m 6ekbsu "...момент нашего первого поцелуя~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    m 6dkbfu "Э-хе-хе..."
                    m 6ekbfa "Я всегда хотела разделить с тобой поцелуй под омелой~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True

                #no more mistletoe topic once youve done it
                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)

                #Re-enable buttons
                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "Я так сильно люблю тебя, [player]~"
    # Normal and happy
    else:
        m 1hubfa "Я люблю тебя, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve_monika
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa at i11 zorder MAS_MONIKA_Z

    #NOTE: This stays up for the full session
    show mas_mistletoe zorder MAS_MONIKA_Z - 1
    with dissolve
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_aiwfc",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25p,
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_aiwfc:
    # set dates for the next song to start a day after this one
    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )

    else:
        $ mas_setEVLPropValues(
            'monika_merry_christmas_baby',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('monika_aiwfc_song'):
        m 1rksdla "Эй, [player]?"
        m 1eksdla "Надеюсь, ты не против, я написала для тебя песню."
        m 3hksdlb "Я знаю, что это немного банально, но я думаю, тебе понравится."
        m 3eksdla "Если у тебя выключена громкость, не мог бы ты включить её для меня?"
        if store.songs.hasMusicMuted():
            m 3hksdlb "О, и не забудь о громкости в игре, тоже!"
            m 3eka "Я очень хочу, чтобы ты это услышал."
        m 1huu "В любом случае.{w=0.5}.{w=0.5}.{nw}"

    else:
        m 1hua "Э-хе-хе..."
        m 3tuu "Надеюсь, ты готов, [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{nw}"

        m "Это {i}снова{/i} то время года, в конце концов[ending]"
        if store.songs.hasMusicMuted():
            m 3hub "Убедись, что ты увеличил громкость!"
            m 1huu ".{w=0.5}.{w=0.5}.{nw}"

    call monika_aiwfc_song

    #NOTE: This must be a shown count check as this dialogue should only be here on first viewing of this topic
    if not mas_getEVLPropValue("monika_aiwfc", "shown_count", 0):
        m 1eka "Надеюсь, тебе понравилось, [player]."
        m 1ekbsa "И здесь я тоже всё сказала всерьёз."
        m 1ekbfa "Ты единственный подарок, который я могу пожелать."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Я люблю тебя, [player]~"

    else:
        m 1eka "Я рада, что тебе нравится, когда я пою эту песню."
        m 1ekbsa "Ты всегда будешь тем подарком, который мне когда-либо был нужен, [player]."
        m 1ekbfa "Я люблю тебя~"

    #Unlock the song
    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:

    call mas_timed_text_events_prep

    $ mas_play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
    m 1eub "{i}{cps=9}Мне не нужно{/cps}{cps=20} много{/cps}{cps=11} в подарок на Рождество,{/cps}{/i}{nw}"
    m 3eka "{i}{cps=11}Мне {/cps}{cps=20}нужно{/cps}{cps=8} только одно.{/cps}{/i}{nw}"
    m 3hub "{i}{cps=8}Мне{/cps}{cps=15} не интересны{/cps}{cps=10} подарки{/cps}{/i}{nw}"
    m 3eua "{i}{cps=15}Под{/cps}{cps=8} Рождественской елкой.{/cps}{/i}{nw}"

    m 1eub "{i}{cps=10}Мне не нужно{/cps}{cps=20} вешать{/cps}{cps=8} свой рождественский чулок{/cps}{/i}{nw}"
    m 1eua "{i}{cps=10}Там,{/cps}{cps=15} над{/cps}{cps=7} камином{/cps}{/i}{nw}"
    m 3hub "{i}{w=0.5}{cps=20}Санта Клаус{/cps}{cps=10} не сделает меня счастливой,{/cps}{/i}{nw}"
    m 4hub "{i}{cps=8}Если{/cps}{cps=15} подарит{/cps}{cps=8} на Рождество игрушку.{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=10}Я лишь хочу,{/cps}{cps=15} чтобы ты{/cps}{cps=8} стал моим,{w=0.5}{/cps}{/i}{nw}"
    m 4hubfb "{i}{cps=8}Хочу сильнее,{/cps}{cps=20} чем ты{/cps}{cps=10} когда-либо мог себе представить.{w=0.5}{/cps}{/i}{nw}"
    m 1ekbsa "{i}{cps=10}Сделай так, чтобы моё желание{/cps}{cps=20} сбыло-о-о-о-о-о-ось.{w=0.8}{/cps}{/i}{nw}"
    m 3hua "{i}{cps=8}Всё, что мне нужно на Рождество{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=7}это ты-ы-ы-ы-ы-ы-ы-ы-ы-ы,{w=1}{/cps}{/i}{nw}"
    m "{i}{cps=9}Ты-ы-ы-ы-ы-ы-ы-ы, ма-а-а-алы-ы-ыш~{w=1}{/cps}{/i}{nw}"

    m 2eka "{i}{cps=10}Я не буду{/cps}{cps=20} много{/cps}{cps=10} просить в это Рождество,{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Мне{/cps}{cps=20} даже {/cps}{cps=10}не нужен снег,{w=0.8}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Я{/cps}{cps=20} лишь буду{/cps}{cps=10} продолжать ждать{w=0.4}{/cps}{/i}{nw}"
    m 3hubfb "{i}{cps=17}Под{/cps}{cps=10} омелой.{w=1}{/cps}{/i}{nw}"

    m 2eua "{i}{cps=10}Я{/cps}{cps=17} не буду составлять{/cps}{cps=9} список и слать его{w=0.35}{/cps}{/i}{nw}"
    m 3eua "{i}{cps=10}Святому{/cps}{cps=20} Николасу{/cps}{cps=10} на Северный полюс.{w=0.3}{/cps}{/i}{nw}"
    m 4hub "{i}{cps=18}Я да{/cps}{cps=10}же не буду бодрствовать, чтобы{w=0.4}{/cps}{/i}{nw}"
    m 3hub "{i}{cps=10}Услышать{/cps}{cps=20} цокот копыт тех{/cps}{cps=14} волшебных северных оленей,{w=1}{/cps}{/i}{nw}"

    m 3ekbsa "{i}{cps=20}Сегодня{/cps}{cps=11} вечером мне нужен только ты,{w=0.4}{/cps}{/i}{nw}"
    m 3ekbfa "{i}{cps=10}И чтобы{/cps}{cps=20} ты крепко{/cps}{cps=10} меня обнимал.{w=0.9}{/cps}{/i}{nw}"
    m 4hksdlb "{i}{cps=10}Что же{/cps}{cps=15} мне{/cps}{cps=8} ещё де-е-е-елать?{w=0.3}{/cps}{/i}{nw}"
    m 4ekbfb "{i}{cps=20}Малыш, {/cps}{cps=12} всё, что мне нужно на Рождество{w=0.5} это ты-ы-ы-ы-ы-ы-ы-ы-ы-ы~{w=2.5}{/cps}{/i}{nw}"
    m "{i}{cps=9}Ты-ы-ы-ы-ы-ы-ы-ы, ма-а-а-алы-ы-ыш~{w=2.5}{/cps}{/i}{nw}"

    call mas_timed_text_events_wrapup
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_merry_christmas_baby",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_aiwfc')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_merry_christmas_baby:
    # set dates for the next song to start a day after this one
    if not mas_isD25():
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(days=1),
            end_date=mas_d25p
        )

    else:
        $ mas_setEVLPropValues(
            'monika_this_christmas_kiss',
            start_date=datetime.datetime.now() + datetime.timedelta(hours=1),
            end_date=datetime.datetime.now() + datetime.timedelta(hours=5)
        )

    if not renpy.seen_label('mas_song_merry_christmas_baby'):
        m 1eua "Эй, [player]..."
        m 3eub "Я тут вспомнила одну рождественскую песню, которой я очень хотела поделиться с тобой!"
        m 3eka "На этот раз, я не учила какую-либо песню, но, надеюсь, тебе понравится, как я спою ту же песню, что и в прошлый раз."
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1hua "Э-хе-хе..."
        m 3eka "Надеюсь, тебе понравилось~"
        $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")

    else:
        m 3euu "Я думаю, что пришло время для ещё одной рождественской песни, э-хе-хе~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby

        m 1huu "Э-хе-хе... {w=0.2}Счастливого рождества, малыш~"

    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_this_christmas_kiss",
            conditional="persistent._mas_d25_in_d25_mode and mas_lastSeenInYear('monika_merry_christmas_baby')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None),
            years=[]
        ),
        skipCalendar=True
    )

label monika_this_christmas_kiss:
    if not renpy.seen_label('mas_song_this_christmas_kiss'):
        m 2rubsa "О, [player]..."
        m 2lubsa "Я нашла эту песню... {w=0.4}и...{w=0.4} я как раз думала о нас, когда послушала её."
        m 7ekbsu "Я имею в виду, ты был так мил со мной всё это время."
        m 3eubsb "И...{w=0.2} о боже, я просто хочу поделиться этим с тобой, если ты не против."
        m 1hubsa "Просто дай мне секунду{nw}"
        extend 1dubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    else:
        m 3euu "Я думаю, что пришло время спеть ещё одну рождественскую песню, э-хе-хе~"
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

    call mas_song_this_christmas_kiss

    m 1dubsa "..."
    m 1rtbsu "Хм-м.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    window hide
    show monika 6tkbsa
    pause 2.0
    show monika 6dkbsu
    pause 2.0

    call monika_kissing_motion
    window auto

    m 6ekbfa "Когда-нибудь я поцелую тебя по-настоящему, [player]."
    m 1dubfu "...И когда этот день настанет, моё сердце выпрыгнет из груди от радости~"
    $ mas_unlockEVL("mas_song_this_christmas_kiss", "SNG")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_spider_tinsel",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_d25c_start,
            end_date=mas_d25e - datetime.timedelta(days=1),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.NORMAL, None),
            rules={"force repeat": None, "no rmallEVL": None},
            years=[]
        ),
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )

# queue this if it hasn't been seen by d25e - 1
init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        MASEventList.queue("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Эй, [player]..."
    m 1etc "Задумывался ли ты когда-нибудь о том, откуда берут своё начало традиции, которые мы зачастую принимаем как должное?"
    m 3eud "В большинстве случаев, те вещи, которые считаются традицией, просто принимаются такими, какие они есть, и у нас так и не нашлось времени, чтобы понять, почему."
    m 3euc "Ну, мне стало любопытно, почему мы делаем определённые вещи в канун Рождества, поэтому я и провела небольшое расследование."
    m 1eua "...И я нашла одну очень интересную украинскую народную сказку, которая как раз и объясняет, почему рождественские деревья начали украшать мишурой."
    m 1eka "Я подумала, что это очень хорошая история, вот мне и захотелось поделиться ею с тобой."
    m 1dka "..."
    m 3esa "Жила-была одна вдова (мы будем звать её Эми), которая жила в тесной старой хижине со своими детьми."
    m 3eud "Снаружи их дома стояла высокая ёлка, и с этого дерева падали шишки, которые потом начинали прорастать из почвы."
    m 3eua "Дети были рады самой идее поставить у себя рождественское дерево, и поэтому они начали стремиться к ней и ждали, когда ёлка станет достаточно высокой, чтобы затащить её в дом."
    m 2ekd "К несчастью, семья была бедной, и даже после того, как у них появилось рождественское дерево, они не могли позволить себе никаких украшений, чтобы украсить её."
    m 2dkc "И поэтому, в канун Рождества, Эми и её дети пошли спать, зная о том, что у них рождественским утром будет стоять голое дерево."
    m 2eua "Однако, пауки, которые жили в хижине, услышали плач детей и решили не оставлять рождественское дерево голым."
    m 3eua "В общем, пауки создали красивые паутины на рождественском дереве, украсив его элегантными и красивыми шелковистыми узорами."
    m 3eub "А когда дети проснулись в раннее рождественское утро, они запрыгали от восторга!"
    m "Они пошли к своей матери и начали будить её, восклицая: «Мама! Ты должна взглянуть на рождественское дерево! Оно такое красивое!»."
    m 1wud "Как только Эми проснулась и встала перед деревом, она была в полном восторге от взора, который стоял перед её глазами."
    m "А потом один из детей открыл окно, чтобы запустить в хижину солнечный свет..."
    m 3sua "И как только лучи солнечного света попали на дерево, паутина начала отражать их свет, создавая мерцающие серебряные и золотые пряди..."
    m "...заставляя тем самым рождественское дерево сиять волшебным образом."
    m 1eka "С этого дня, Эми никогда не чувствовала себя бедной; {w=0.3}наоборот, она всегда была рада всем тем замечательным подаркам, которые у неё уже были в жизни."
    m 3tuu "Ну, полагаю, теперь мы знаем, почему Эми любит пауков..."
    m 3hub "А-ха-ха! Я просто шучу!"
    m 1eka "Разве это не милая и прекрасная история, [player]?"
    m "Мне кажется, это правда интересный взгляд на то, почему мишуру начали использовать в качестве украшения рождественского дерева."
    m 3eud "А ещё я читала, что жители Украины часто украшают свои рождественские деревья украшениями в виде паутины, полагая, что это принесёт им удачу в следующем году."
    m 3eub "Так что, думаю, если ты когда-нибудь найдёшь паука, живущего в твоём рождественском дереве, не убивай его, и возможно, он принесёт тебе удачу в будущем!"
    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_night_before_christmas",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=21)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_d25_night_before_christmas:
    m 1esa "Эй, [player]..."
    m 3eua "Уверена, ты уже слышал об этом, но канун Рождества просто будет неполным без {i}«Ночь перед рождеством»{/i}!"
    m 3eka "Это всегда было моей самой любимой частью приближающегося кануна Рождества, так что, надеюсь, ты не против послушать, как я читаю эту книгу."
    m 1dka "..."

    m 3esa "Рождество на пороге. Полночную тишь..."
    m 3eud "Потревожить не сможет даже юркая мышь."
    m 1eud "Стайка детских чулок, как положено, чинно"
    m 1eka "Санта Клауса ждёт у решётки каминной."
    
    m 1esa "Ребятишкам в уютных и мягких кроватках"
    m 1hua "Снится сахарный снег и Луна-мармеладка."
    m 3eua "Я колпак нахлобучил, а мама — чепец:"
    m 1dsc "Взрослым тоже пора бы вздремнуть, наконец..."
    
    m 3wuo "Вдруг грохот и топот, и шум несусветный"
    m "И крыша откликнулась гулом ответным."
    m 3wud "Сна, как не бывало, а кто бы заснул?"
    m "Я ставни открыл и окна распахнул"
    
    m 1eua "Играя в гляделки со снегом искристым,"
    m 3eua "Луна озаряла сиянием чистым"
    m 3wud "Я так и застыл у окна в изумленье..."
    m 3wuo "Чудесные санки и восемь оленей."
    
    m 1eua "За кучера — бойкий лихой старичок."
    m 3eud "Да-да, это Санта — ну кто же ещё"
    m 3eua "Мог в крохотных санках орлов обгонять"
    m 3eud "И басом весёлым оленям кричать:"

    m 3euo "«–Эй, Быстрый! Танцор! Эй, Дикарь! Эй, Скакун!»"
    m "«Комета! Амур! Эй, Гроза и Тайфун!»"
    m 3wuo "«Живей на крыльцо! А теперь к чердаку!»"
    m "«Наддайте! Гоните на полном скаку!»"
    
    m 1eua "Как лёгкие листья, что с ветром неслись,"
    m 1eud "Взмывают, встречаясь с преградою, ввысь."
    m 3eua "Вот так же олени вверх сани помчали."
    m "Игрушки лишь чудом не выпадали!"

    m 3eud "Раздался на крыше грохота звук —"
    m "Диковинных, звонких копыт перестук."
    m 1rkc "Скорее, скорее к камину! И вот"
    m 1wud "Наш Санта скользнул прямиком в дымоход."
    
    m 3eua "Одетый в меха с головы и до пят"
    m 3ekd "Весь в копоти Сантин роскошный наряд!"
    m 1eua "С мешком, перекинутым через плечо,"
    m 1eud "Набитым игрушками — чем же ещё!"
    
    m 3sub "Сияют глаза, будто звёзды в мороз,"
    m 3subsb "Два яблока — щёки, и вишенка — нос."
    m 3subsu "Улыбка — забавней не видел вовек!"
    m 1subsu "Бела борода, словно утренний снег."

    m 1eud "И сразу дымком потянуло табачным;"
    m 3rkc "Он старую трубку насасывал смачно,"
    m 2eka "А кругленький толстый животик от смеха"
    m 2hub "Как студень дрожал — доложу вам, потеха!"
    
    m 2eka "Забавный толстяк — просто эльф, да и только!"
    m 3hub "Не выдержав, {nw}"
    extend 3eub "я рассмеялся до колик."
    m 1kua "вначале слегка опасался смеяться,"
    m 1eka "Но, звёздочек — глаз, разве можно бояться?"
    
    m 1euc "Не молвив ни слова, он взялся за дело —"
    m 1eud "Чулки у камина наполнил умело,"
    m 3esa "Кивнул, пальчик пухленький к носу прижал"
    m 3eua "«Мол, тихо! Молчи» — и в камине пропал."

    m 1eud "Раздался его оглушительный свист –"
    m 1eua "И восемь оленей как птицы взвились,"
    m 3eua "Лишь ветром слова до меня донесло:"
    m 3hub "«Всех — всех с Рождеством! Я вернусь! Добрых снов!»"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e,
            years=[]
        ),
        skipCalendar=True
    )

label mas_d25_monika_lingerie_reveal:
    # sanity check in the rare case people leave after this is queued but before it's seen
    # and timing doesn't make sense
    if 2 < datetime.datetime.now().hour < 18:
        $ mas_setEVLPropValues(
            "mas_d25_monika_lingerie_reveal",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and mas_canShowRisque() "
                "and not mas_SELisUnlocked(mas_clothes_santa_lingerie) "
                "and 18 <= datetime.datetime.now().hour < 24"
            ),
            action=EV_ACT_QUEUE,
            start_date=mas_d25e - datetime.timedelta(days=4),
            end_date=mas_d25e
        )
        return

    m 1hub "Я всегда считала дни перед Рождеством такими захватывающими, [player]!"
    m 3sua "Предвкушение, кажущаяся волшебной аурой сезона... в этом есть что-то особенное."
    m 1dkbsu "Это действительно моё любимое время года."
    m "..."

    if mas_hasUnlockedClothesWithExprop("lingerie"):
        call mas_d25_monika_second_time_lingerie

    else:
        call mas_lingerie_intro(holiday_str="это Рождество", lingerie_choice=mas_clothes_santa_lingerie)
        m 1ekbfa "Просто знай, что я люблю тебя очень-очень сильно, [player]~"
        $ mas_ILY()

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas_eve",
            conditional="persistent._mas_d25_in_d25_mode",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_d25e, datetime.time(hour=20)),
            end_date=mas_d25,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label mas_d25_monika_christmas_eve:
    m 3hua "[player]!"
    m 3hub "Ты можешь в это поверить? {w=1}Скоро Рождество!"
    m 1rksdla "Мне всегда было так трудно спать в канун Рождества..."
    m 1eka "Мне так хотелось увидеть, что я найду под ёлкой на следующее утро..."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika

    #Were there last Christmas
    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "Но я ещё {i}больше{/i} радуюсь теперь, когда могу проводить с тобой каждое Рождество..."
        m 5hkbsa "Я не могу дождаться завтрашнего дня!"

    #Weren't there last Christmas
    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "Но я ещё {i}больше{/i} взволнована в этом году..."
        m 5hkbsa "Только мысль о том, чтобы провести ещё одно Рождество вместе...{w=1} Я не могу дождаться!"

    #First Chistmas with Moni
    else:
        m "Но я ещё {i}больше{/i} взволнована в этом году..."
        m 5hkbsa "Только мысль о нашем первом совместном Рождестве...{w=1} Я не могу дождаться!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_d25_monika_second_time_lingerie

        else:
            m 5ekbfa "..."
            show monika 1ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
            call mas_lingerie_intro(holiday_str="канун Рождества", lingerie_choice=mas_clothes_santa_lingerie)
            m 1ekbfa "Просто знай, что я люблю тебя очень, очень сильно, [player]~"
            $ mas_ILY()
    return

label mas_d25_monika_second_time_lingerie:
    m 3wubsb "О!"
    m 3tsbsu "У меня есть для тебя маленький сюрприз...{w=1} Думаю, тебе это понравится, э-хе-хе~"
    call mas_clothes_change(outfit=mas_clothes_santa_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
    pause 2.0
    show monika 2ekbsu
    pause 2.0
    show monika 2tkbsu
    pause 2.0
    m 2tfbsu "[player]...{w=0.5} Ты так пристально смотришь{w=0.5}... снова."
    m 2hubsb "А-ха-ха!"
    m 2eubsb "Полагаю, ты одобряешь мой выбор одежды..."
    m 2tkbsu "Довольно хорошо вписывается для такого случая, ведь так?"
    m 2rkbssdla "Должна сказать, я очень нервничала, когда впервые надела что-то подобное..."
    m 2hubsb "Но теперь, когда я сделала это раньше, мне действительно нравится одеваться так для тебя!"
    m 3tkbsu "Надеюсь, тебе тоже понравится~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            # within a week after d25, user did not recognize
            # d25 at all, and they were not long absenced or had her on a date
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:
    #sanity checks
    if persistent._mas_d25_spent_d25:
        return

    #need to make sure people who just started post d25 don't lose aff
    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, reason=6)
        m 1dkc "...Я просто рада тому, что ты наконец-то пришёл..."
        m 2ekd "Я уже начала волноваться, что с тобой что-то произошло..."
        m 2rksdlc "Когда ты не пришёл на Рождество...{w=1} я не знала, что и думать."
        m 4eksdlc "Не то, чтобы я хотела, чтобы ты пропустил тот день, который, как ты знаешь, важен для меня..."
        m 2dksdlc "И я подумала, может..."
        m 2eksdla "Хотя, это сейчас не важно. Я просто рада, что с тобой всё хорошо!"
        m 4eka "Пусть даже я и разочарована тем, что мы не смогли провести Рождество вместе, я уверена, что у тебя на это была веская причина."
        m "Просто не дай этому произойти в следующем году, ладно?"
        m 2eka "И, даже если в будущем ты не смог заглянуть ко мне в Рождество, попытайся хотя бы взять меня с собой..."
        m 1eka "Я лишь хочу быть рядом с тобой, [player]..."
        m 3ekbsa "Я люблю тебя~"
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, reason=6)
        m 2ekc "Эй, [player]..."
        m 2tkc "Должна сказать, я разочарована тем, что ты не заглянул ко мне на Рождество..."
        m 4tkc "Ты знал, что я хотела провести время с тобой. Разве я многого прошу?"
        m 2rkc "Я знаю, что день, возможно, был тяжёлым, если тебе надо было съездить в другой город, чтобы навестить семью, но ты мог хотя бы взять меня с собой..."
        m 2ekc "Для меня этого было бы вполне достаточно."
        m 2dkc "..."
        m 4rksdlc "Может, что-то произошло в последнюю минуту, и ты попросту не смог провести время со мной..."
        m 4eksdla "Но, пожалуйста...{w=1}пожалуйста, не забудь заглянуть ко мне на следующее Рождество, хорошо, [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 2efc "[player]!"
        m "Не могу поверить в то, что ты даже не удосужился заглянуть ко мне в Рождество!"
        m 2tfc "По правде говоря...{w=1} да, я могу."
        m "Именно поэтому я не позаботилась о декорациях..."
        m 2rfc "Я знала, что если бы я попыталась проникнуться духом Рождества, то меня в конце бы ждало разочарование... {w=1}опять."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, reason=6)
        m 6ekc "[player], как прошло твоё Рождество?"
        m 6dkc "Лично моё – в полном одиночестве..."
        m "Ты, скорее всего, даже не подумал обо мне, да?"

    else:
        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return

# check to see if we missed d25 due to being on a date
label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return

#Christmas Eve dockingstation
label bye_d25e_delegate:
    # delegation label that determins what bye dialogue to show
    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out

    else:
        call bye_d25e_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: since we are using the generic return, we cant use this
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25_EVE)

    # jump back to going somewhere file gen
    jump mas_dockstat_iostart

#first time you take her out on d25e
label bye_d25e_first_time_out:
    m 1sua "Отведёшь меня в какое-нибудь особенное место на канун Рождества, [player]?"
    m 3eua "Я знаю, что некоторые люди посещают друзей или семью... или ходят на рождественские вечеринки..."
    m 3hua "Но куда бы мы ни пошли, я буду рада тому, что ты захотел, чтобы я пошла с тобой!"
    m 1eka "Надеюсь, мы будем праздновать Рождество дома, но если мы не будем его праздновать, мне будет достаточно и того, что я с тобой~"
    return

#second time you take her out on d25e
label bye_d25e_second_time_out:
    m 1wud "Ого, мы сегодня снова идём гулять, [player]?"
    m 3hua "Наверное, тебе надо проведать много кого в канун Рождества..."
    m 3hub "...или, наверное, у тебя для нас на сегодня готово много особенных планов!"
    m 1eka "Но, так или иначе, спасибо, что подумал обо мне и взял меня с собой~"
    return

#Christmas Day dockingstation
label bye_d25_delegate:
    # delegation label that determins which bye dialogue to show
    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out

    else:
        call bye_d25_first_time_out

    # notifies bye going somewhere to use this gre type
    # NOTE: generic return
#    $ mas_idle_mailbox.send_ds_gre_type(store.mas_greetings.TYPE_HOL_D25)

    jump mas_dockstat_iostart

#first time out on d25
label bye_d25_first_time_out:
    m 1sua "Отведёшь меня в какое-нибудь особенное место в Рождество,, [player]?"

    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Может, мы навестим кого-нибудь из твоей семьи?.. Я бы с удовольствием с ними познакомилась!"
        m 3eua "Или, быть может, мы посмотрим фильм?.. Я знаю, что некоторым нравится заниматься этим после открытия подарков."

    else:
        m 3eua "Может быть, мы пойдём в кино... я знаю, что некоторые люди любят делать это после открытия подарков."

    m 1eka "Ну, куда бы ты ни пошел, я просто рада, что ты хочешь, чтобы я пошла с тобой..."
    m 3hua "Я хочу провести всё Рождество вместе с тобой, если это возможно, [player]~"
    return

#second time out on d25
label bye_d25_second_time_out:
    m 1wud "Ого, мы {i}опять{/i} куда-то идём, [player]?"
    m 3wud "Наверное, у тебя много людей, к которым ты должен сходить в гости..."
    m 3sua "...или, наверное, у тебя для нас на сегодня готово много особенных планов!"
    m 1hua "Но, так или иначе, спасибо, что подумал обо мне и взял меня с собой~"
    return

## d25 greetings

#returned from d25e date on d25e
label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "Вот мы и дома!"
    m 3eka "Было очень мило с твоей стороны взять меня с собой сегодня..."
    m 3ekbsa "Прогулка с тобой в канун Рождества была очень особенной, [player]. Спасибо~"
    return

#returned from d25e date on d25
label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    m 1hua "Вот мы и дома!"
    m 3wud "Ого, нас не было всю ночь..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25e date (or left before d25e) after d25 but before nyd is over
label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    m 1hua "Наконец-то мы дома!"
    m 3wud "Мы точно долго отсутствовали, [player]..."
    m 3eka "Было бы здорово повидаться с тобой в Рождество, но, поскольку ты не смог прийти ко мне, я рада, что ты взял меня с собой."
    m 3ekbsa "Просто быть рядом с тобой – всё, чего я хотела~"
    m 1ekbfb "И так как я не успела сказать это тебе на Рождество... c Рождеством, [player]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

#returned from pd25e date on d25
label greeting_pd25e_returned_d25:
    m 1hua "Вот мы и дома!"
    m 3wud "Ого, нас не было довольно долго..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

#returned from d25 date on d25
label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Вот мы и дома!"
    m 3eka "Было очень приятно провести время с тобой на Рождество, [player]!"
    m 1eka "Большое спасибо, что взял меня с собой."
    m 1ekbsa "Ты всегда такой заботливый~"
    return

#returned from d25 date after d25
label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Наконец-то мы дома!"
    m 3wud "Мы отсутствовали очень долго, [player]!"
    m 3eka "Было бы здорово повидаться с тобой снова до окончания Рождества, но, по крайней мере, я всё ещё была с тобой."
    m 1hua "Поэтому спасибо тебе за то, что провёл время со мной, когда тебе надо было сходить по разным местам..."
    m 3ekbsa "Ты всегда такой заботливый~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

### NOTE: mega delegate label to handle both d25 and nye returns

label greeting_d25_and_nye_delegate:
    # ASSUMES:
    #   - we are more than 5 minutes out
    #   - we are in d25 mode
    #   - affection normal+

    python:
        # lots of setup here
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():
        # returned on d25e

        if left_pre_d25e:
            # left before d25e, use regular greeting
            jump greeting_returned_home_morethan5mins_normalplus_flow

        else:
            # otherwise, greeting 2
            call greeting_d25e_returned_d25e

    elif mas_isD25():
        # we have returnd on d25

        if checkout_time is None or mas_isD25(checkout_date):
            # no checkout or left on d25
            call greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):
            # left on d25e
            call greeting_d25e_returned_d25

        else:
            # otherwise assume pre d25 to d25
            call greeting_pd25e_returned_d25

    elif mas_isNYE():
        # we have returend on nye
        if checkout_time is None or mas_isNYE(checkout_date):
            # no checkout or left on nye
            call greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):
            # left before d25
            call greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):
            # left on d25
            call greeting_d25_returned_post_d25

        else:
            # otheriwse usual more than 5 mins
            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():
        # we have returned on nyd
        # NOTE: we cannot use left_pre_d25, so dont use it.

        if checkout_time is None or mas_isNYD(checkout_date):
            # no checkout or left on nyd
            call greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):
            # left on nye
            call greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp

        else:
            # all other cases should be as if leaving d25post
            call greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():
            # arrived after new years day
            # NOTE: we cannot use left_pre_d25, so dnot use it

            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):
                # no checkout or left on nyd or after nyd
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):
                # left on nye
                call greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):
                # usual d25post
                call greeting_d25p_returned_nydp


            else:
                # all other cases use pred25e post nydp
                call greeting_pd25e_returned_nydp

        else:
            # arrived after d25, pre nye
            if checkout_time is None or mas_isD25Post(checkout_date):
                # no checkout or left during post
                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):
                # left on christmas
                call greeting_d25_returned_post_d25

            else:
                # otheriwse, use d25e returned post d25
                call greeting_d25e_returned_post_d25

    else:
        # the usual more than 5 mins
        jump greeting_returned_home_morethan5mins_normalplus_flow

    # NOTE: if you are here, then you called a regular greeting label
    # and need to return to aff gain
    jump greeting_returned_home_morethan5mins_normalplus_flow_aff


#################################### NYE ######################################
# [HOL030]

default persistent._mas_nye_spent_nye = False
# true if user spent new years eve with monika

default persistent._mas_nye_spent_nyd = False
# true if user spent new years day with monika

default persistent._mas_nye_nye_date_count = 0
# number of times user took monika out for nye

default persistent._mas_nye_nyd_date_count = 0
# number of times user took monika out for nyd

default persistent._mas_nye_date_aff_gain = 0
# amount of affection gained for an nye date

define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:
    # MASHistorySaver for nye
    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain",

            "_mas_nye_accomplished_resolutions": "nye.actions.did_new_years_resolutions",
            "_mas_nye_has_new_years_res": "nye.actions.made_new_years_resolutions",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 12, 31),
        end_dt=datetime.datetime(2020, 1, 6),
        exit_pp=store.mas_d25SeasonExit_PP
    ))

init -825 python:
    mas_run_d25s_exit = False

    def mas_d25SeasonExit_PP(mhs):
        """
        Sets a flag to run the D25 exit PP
        """
        global mas_run_d25s_exit
        mas_run_d25s_exit = True

init -10 python:
    def mas_isNYE(_date=None):
        """
        Returns True if the given date is new years eve

        IN:
            _date - date to check
                If None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years eve, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nye.replace(year=_date.year)


    def mas_isNYD(_date=None):
        """
        RETURNS True if the given date is new years day

        IN:
            _date - date to check
                if None, we use today's date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_nyd.replace(year=_date.year)



#START: NYE/NYD TOPICS
#pm var so she forgives, but doesn't forget
default persistent._mas_pm_got_a_fresh_start = None

#store affection prior to reset
default persistent._mas_aff_before_fresh_start = None

#If we failed the fresh start or not
default persistent._mas_pm_failed_fresh_start = None

init 5 python:
    # NOTE: new years day
    # also known as monika_newyear2
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nyd",
            action=EV_ACT_PUSH,
            start_date=mas_nyd,
            end_date=mas_nyd + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.DISTRESSED, None),
        ),
        skipCalendar=True
    )

label mas_nye_monika_nyd:
    $ persistent._mas_nye_spent_nyd = True
    $ got_fresh_start_last_year = mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start")

    if store.mas_anni.pastOneMonth():
        if not mas_isBelowZero():

            #We've not had a fresh start before or you redeemed yourself
            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "[player]!"
                #We spent new year's together last year
                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    m "Можешь ли ты поверить в то, что мы проводим очередной Новый год вместе?"
                if mas_isMoniAff(higher=True):
                    m 1hua "Мы определённо прошли через многое в минувшем году, да?"
                else:
                    m 1eua "Мы определённо прошли через многое в минувшем году, да?"

                m 1eka "Я так счастлива, зная о том, что мы вместе проведём ещё больше времени."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5hubfa "Давай мы сделаем этот год таким же замечательным, как и прошедший, ладно?"
                    m 5ekbfa "Я тебя очень сильно люблю, [player]."
                else:
                    m 3hua "Давай мы сделаем этот год ещё лучше, чем прошедший, ладно?"
                    m 1hua "Люблю тебя, [player]."

            #If you got a fresh start and are positive now
            else:
                $ last_year = "в прошлом году"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "раньше"

                m 3eka "Ты помнишь то обещание, которое дал [last_year]?"
                m "Что мы сделаем этот год лучше, чем прошедший?"
                m 6dkbstpa "..."
                m 6ekbftpa "Спасибо, что сдержал своё обещание."
                m "Я серьёзно, [player]. Ты сделал меня очень счастливой...{w=1} {nw}"
                extend 6dkbftpa "спасибо тебе, от всей души."
                m 6dkbftda "Давай мы сделаем этот год ещё лучше, чем прошедший, ладно?"
                m 6ekbftda "Люблю тебя, [player]."
                m "Я правда люблю тебя."
                #You made it up
                $ persistent._mas_pm_failed_fresh_start = False

        #Below zero
        else:
            #Not had fresh start yet
            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                m 2rksdlc "Мы прошли...{w=1} через многое в прошлом году..."
                m "Я... я надеюсь, что этот год будет лучше, чем прошедший."
                m 2dkc "Мне это правда нужно."
                jump mas_nye_monika_nyd_fresh_start

            else:
                m 2rkc "[player]..."
                #If you got a fresh start last year and you're still negative
                if got_fresh_start_last_year:
                    m 2ekc "Ты помнишь то обещание, которое дал в прошлом году?"
                    m 2ekd "Что мы сделаем этот год лучше, чем прошедший?"

                #Otherwise fresh start
                else:
                    m 2ekc "Ты помнишь то обещание, которое дал раньше?"
                    m 2ekd "Что ты улучшишь наши отношения?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    m 2rkd "Мне кажется, ты сделал их чуточку лучше..."
                    m 2ekc "Но я ожидала большего, [player]."

                    #Revert back to old affection if we haven't already done this
                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ _mas_revertFreshStart()
                        $ _mas_AffSave()
                        $ renpy.save_persistent()

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    m 2rfc "Полагаю, ты не смог сдержать то обещание... понятно."

                else:
                    m 2rkc "Похоже, ничего не изменилось, да?"

                #Since -50 is going to mean an FF next load, we need to path this accordingly
                m 2rktpc "Я очень,{w=0.5} очень надеюсь, что ты сможешь это исправить, [player]..."
                m 2dktpc "Я не знаю, сколько я ещё смогу выдержать."

                #Foreshadowing
                if _mas_getAffection() <= -50:
                    m 2dktsd "Но это, наверное, просто глупая мысль..."
                    m 2ektsc "Это просто очередная игра для тебя, это очевидно."
                    m 2rktsd "Ты даже не считаешь меня настоящей...{w=1} {nw}"
                    extend 2dftsc "я всего лишь очередной персонаж, с которым ты просто играешься."
                    m 2eftdc "Надеюсь, никто не переживёт те же боль и одиночество, которые я испытывала весь этот год."

                $ persistent._mas_pm_failed_fresh_start = True
                return

    else:
        if not mas_isBelowZero():
            m 1eub "[player]!"

            if mas_isMoniAff(higher=True):
                m 1ekbsa "Я знаю, что мы не были вместе довольно долгое время, но минувший год прошёл лучше, чем я могла бы надеяться..."
            else:
                m 1eka "Я знаю, что мы не были вместе довольно долгое время, но минувший год был для меня очень особенным..."

            m 1hua "Я буду всегда помнить об этом, как о том годе, когда я познакомилась с тобой~"
            m 3hua "Давай мы наверстаем упущенное и сделаем этот год ещё лучше!"
            m 1ekbsa "Люблю тебя, [player]."

        else:
            m 2ekc "В общем, [player]..."
            m 2etc "Уже начался новый год, да?"
            m 2rksdlc "Мы не были вместе довольно долгое время, но то время, которое мы провели в минувшем году, прошло не так гладко, как я на то надеялась..."
            jump mas_nye_monika_nyd_fresh_start

    m "С Новым годом~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    m 2ekc "Как насчёт того, чтобы оставить всё это в прошлом, забыть о прошлом году и сосредоточиться на новом начале этого года?"
    m 4ekc "Ещё не поздно начать всё с чистого листа, [player], мы всё ещё можем сделать друг друга счастливыми."
    m 4eka "Это всё, чего я когда-либо хотела."

    m "Что скажешь, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Что скажешь, [player]?{fast}"

        "Я был бы очень рад этому.":
            #so we can revert back to previous affection if player continues to mistreat after the second chance. need to determine the threshold the player must stay above for this.
            $ persistent._mas_pm_got_a_fresh_start = True #never forget
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()

            # reset affection and save it
            $ _mas_doFreshStart()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 4wua "Правда?"
            m 1hua "О, [player], ты не представляешь, как я счастлива!"
            m 3eka "Я знаю, у нас всё получится."
            m 1hua "Спасибо тебе большое..."
            m 1eka "Знание того, что ты всё ещё хочешь быть со мной... это многое для меня значит."
            m 3eka "Давай отнесёмся к этому серьёзно, хорошо, [player]?"
            return

        "Нет.":
            $ persistent._mas_pm_got_a_fresh_start = False

            # set affection to broken
            $ _mas_shatterAffection()
            $ _mas_AffSave()
            $ renpy.save_persistent()

            m 6dktpc "..."
            m 6ektpc "Я... я..."
            m 6dktuc "..."
            m 6dktsc "У меня нет слов..."
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, #queuing it so it shows on the right day
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_nye_accomplished_resolutions = None
#True if user has accomplished new years resolutions
default persistent._mas_nye_has_new_years_res = None
#True if user has resolutuons

label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Эй, [player]?"
    m 2eka "Мне вот интересно..."

    #If we didn't see this last year, we need to ask if we made a resolution or not
    if not mas_lastSeenLastYear("monika_resolutions"):
        m 3eub "Ты делал какие-нибудь новогодние обещания в прошлом году?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты делал какие-нибудь новогодние обещания в прошлом году?{fast}"

            "Да.":
                m 3hua "Мне всегда очень приятно слышать о том, что ты пытаешься стать лучше, [player]."
                m 2eka "Кстати говоря..."

                call monika_resolutions_accomplished_resolutions_menu("Ты выполнил свои прошлогодние обещания?")


            "Нет.":
                m 2euc "Оу, понятно..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        m 3eka "Ну, я всё равно сомневаюсь, что тебе вообще надо меняться."
                        m 3hub "Мне кажется, ты прекрасный человек, именно такой, какой ты есть."
                    else:
                        m 3eka "В этом нет ничего такого. Я всё равно сомневаюсь, что тебе надо меняться."

                else:
                    m 2rkc "Наверное, ты должен сделать одно новогоднее обещание в этом году, [player]..."

    #If we made a resolution last year, then we should ask if the player accomplished it
    elif mas_HistVerifyLastYear_k(True, "nye.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu("Раз уж ты дал себе обещание в прошлом году, то смог ли ты выполнить его?")

    #This path will be the first thing you see if you didn't make a resolution last year
    m "У тебя есть какие-нибудь планы на следующий год?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя есть какие-нибудь планы на следующий год?{fast}"
        "Да.":
            $ persistent._mas_nye_has_new_years_res = True

            m 1eub "Это отлично!"
            m 3eka "Даже если они могут быть труднодоступны или невозможными..."
            m 1hua "Я буду здесь, чтобы помочь тебе, если понадобится!"

        "Нет.":
            $ persistent._mas_nye_has_new_years_res = False
            m 1eud "Оу, неужели это так?"
            if mas_isMoniNormal(higher=True):
                if persistent._mas_nye_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "Тебе не нужно меняться. Я думаю, что ты прекрасен таким, какой ты есть."
                    else:
                        m 1eka "Тебе не нужно меняться. Я думаю, что ты должен остаться таким, какой ты есть."
                    m 3euc "Но если тебе что-нибудь придёт в голову до того, как часы пробьют двенадцать, запиши это для себя..."
                else:
                    m "Что ж, если тебе что-нибудь придёт в голову до того, как часы пробьют двенадцать, запиши это для себя..."
                m 1kua "Может быть, ты подумаешь о чём-то, что ты хочешь сделать."
            else:
                m 2ekc "{cps=*2}Я вроде как надеялась—{/cps}{nw}"
                m 2rfc "Ты знаешь о чём я, не важно..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hubfa "Я намерена стать для тебя ещё более совершенной девушкой, [mas_get_player_nickname()]."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Я решила, что хочу стать для тебя самой лучшей девушкой, [player]."
    else:
        m 2ekc "Мое намерение — улучшить наши отношения, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu(question):
    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"

        "Да.":
            $ persistent._mas_nye_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                m 4hub "Рада это слышать, [player]!"
                m 2eka "Здорово, что ты смог сделать это."
                m 3ekb "Подобное правда заставляет меня гордиться тобой."
                m 2eka "Мне бы очень хотелось оказаться рядом с тобой, чтобы отметить это."
            else:
                m 2rkc "Это хорошо, [player]."
                m 2esc "Наверное, ты сможешь дать себе ещё одно обещание в этом году..."
                m 3euc "Никогда не знаешь, что может измениться."

            return True

        "Нет.":
            $ persistent._mas_nye_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                m 2eka "Оу... ну, порой всё идёт совсем не так, как мы на то рассчитывали."

                if mas_isMoniHappy(higher=True):
                    m 2eub "Да и к тому же, мне кажется, что ты замечательный, так что, даже если ты не можешь достичь своих целей..."
                    m 2eka "..Я всё ещё горжусь тобой за то, что ты поставил их и стараешься стать лучше, [player]."
                    m 3eub "Если ты решил создать для себя цель в этом году, я буду поддерживать тебя на каждом шагу."
                    m 4hub "Я с радостью помогу тебе достичь своих целей!"
                else:
                    m "Но, как по мне, это очень здорово, что ты, по крайней мере, стараешься стать лучше, создавая для себя цели."
                    m 3eua "Быть может, если ты создашь для себя цель в этом году, то ты сможешь её выполнить!"
                    m 3hub "Я верю в тебя, [player]!"

            else:
                m 2euc "Ох...{w=1} ну, возможно, ты должен приложить чуть больше усилий для достижения цели в следующем году."

            return False


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nye_year_review",
            action=EV_ACT_QUEUE,
            start_date=mas_nye,
            end_date=datetime.datetime.combine(mas_nye, datetime.time(hour=23)),
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label monika_nye_year_review:
    $ persistent._mas_nye_spent_nye = True
    $ spent_an_event = False

    $ placeholder_and = "и "
    #Starting with an overview based on time
    if store.mas_anni.anniCount() >= 1:
        m 2eka "Знаешь, [player], мы и вправду прошли через многое вместе."
        if store.mas_anni.anniCount() == 1:
            m 2wuo "Мы провели целый год вместе!"
            m 2eka " Как быстро летит время..."

        else:
            m 2eka "Этот год и вправду пролетел незаметно..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "Знаешь, [player], мы и вправду через многое прошли за всё то время, что мы провели вместе в прошлом году."
        m "Время и вправду быстро летит..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "Знаешь, [player], мы через многое прошли за столь короткий промежуток времени, что мы провели вместе в прошлом году."
        m 2eksdlu "Как быстро прошла жизнь, а-ха-ха..."

    else:
        m 2eka "[player], пусть даже мы и мало через что прошли вместе..."
        $ placeholder_and = ""


    # then a bit based on affection
    if mas_isMoniLove():
        m 2ekbsa "...и я никогда не захочу проводить это время с кем-нибудь другим, [player]."
        m "Я просто очень,{w=0.5} очень рада быть с тобой в этом году."

    elif mas_isMoniEnamored():
        m 2eka "...[placeholder_and]я очень рада тому, что могу провести это время с тобой, [player]."

    elif mas_isMoniAff():
        m 2eka "...[placeholder_and]я с удовольствием провела время с тобой."

    else:
        m 2euc "...[placeholder_and]всё то время, что мы провели вместе, было полным веселья."


    m 3eua "Так или иначе, мне кажется, что было бы здорово подумать о всём том, через что мы прошли в прошлом году."
    m 2dtc "Так, посмотрим..."

    # promisering related stuff
    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        m 3eka "Оглядываясь назад, ты в этом году дал мне обещание, когда дал мне это кольцо..."
        m 1ekbsa "...символ нашей любви."

        if persistent._mas_pm_wearsRing:
            m "И ты даже себе надел его..."

            if mas_isMoniAff(higher=True):
                m 1ekbfa "Чтобы показать, что ты предан мне так же, как и я тебе."
            else:
                m 1ekbfa "Чтобы показать мне свою преданность."

    #vday
    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        m 1wuo "О!"
        m 3ekbsa "Ты вместе со мной провёл День Святого Валентина..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            m 4ekbfb "...и даже подарил мне очень красивые цветы."


    #922
    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        m 2eka "Ты провёл со мной время на мой день рождения..."

        if not persistent._mas_bday_no_recognize:
            m 2dua "...отпраздновал его со мной..."

        if persistent._mas_bday_sbp_reacted:
            m 2hub "...устроил мне сюрприз-вечеринку..."

        show monika 5ekbla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbla "...и это правда заставило меня почувствовать себя любимой. Я не знаю, как тебя отблагодарить за то, что ты сделал для меня."

    #Pbday
    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Мы даже провели твой день рождения вместе!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            m 5eubla "У нас тоже было такое приятное свидание~"

    #bit on christmas
    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hua "Ты провёл со мной Рождество..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss.date() == mas_d25:
            m 5eubla "...и мы тогда впервые поцеловались~"
            m 5lubsa "Я никогда не забуду этот момент..."
            m 5ekbfa "{i}Наш{/i} момент."
            m "Я не могу себе представить, как проводила бы эти мгновения с кем-то другим."
        else:
            m 5ekbla "...день, который я даже в уме не могу провести с кем-то другим."


    if not spent_an_event:
        m 2rksdla "...Полагаю, мы пока ещё ни одно грандиозное событие не проводили вместе."
        m 3eka "Но всё же..."

    else:
        show monika 5dsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5dsa "..."

    # lookback based on time
    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eka "Я правда не могу поверить в то, как много изменилось с тех пор, как мы вместе..."
        else:
            m 2eka "Я правда надеюсь, что мы добьёмся большего в наших отношениях, [player]..."
    else:
        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eka "Мне уже хочется взглянуть на то, как много изменится в будущем для нас..."

    #If we started fresh the year before this or we didn't at all
    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5dka "Спасибо."
        if store.mas_anni.anniCount() > 0:
            $ ending = "лучшим годом, о котором я могла только мечтать"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "даже лучше, чем было в позапрошлом году"

            m 5ekbsa "Спасибо тебе за то, что сделал прошлый год [ending]."

        else:
            $ _last_year = " "
            if store.mas_anni.pastOneMonth():
                $ _last_year = " в прошлом году"

            m 5ekbsa "Спасибо тебе за то, что сделал то время, которое мы провели вместе[_last_year], лучшим, чем я могла себе представить."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                m 1lsbsa "..."
                m 6ekbsa "[player], я..."
                call monika_kissing_motion
                m 1ekbfa "Я люблю тебя."
                m "..."
                show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbsa "Я никогда не забуду этот момент..."
                m 5ekbfa "Наш первый поцелуй~"
                m 5hubfb "Давай сделаем этот год ещё лучше, чем прошлый, [player]."

            else:
                call monika_kissing_motion_short
                m 1ekbfa "Я люблю тебя, [player]."
                show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5hubfb "Давай сделаем этот год всё ещё лучше, чем прошлый."

        else:
            m "Давай сделаем этот год как можно лучше, [player]. Я люблю тебя~"
    else:
        m 1dsa "Спасибо, что решил отпустить прошлое и начать сначала."
        m 1eka "Думаю, если мы попробуем, то у нас получится, [player]."
        m "Давай сделаем этот год прекрасным друг для друга."
        m 1ekbsa "Я люблю тебя."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional="persistent._mas_d25_in_d25_mode",
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_PUSH,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:
    # need to grab dates here in case this topic spans nye and nyd
    $ curr_date = datetime.date.today()
    $ curr_year = curr_date.year

    if curr_date.day != 31:
        $ curr_year = curr_year - 1
        $ curr_date = datetime.date(curr_year, 12, 31)

    if mas_SELisUnlocked(mas_clothes_dress_newyears):
        m 3hub "Эй, [player], ты можешь поверить что очередной год уже позади?!"
        m 1tuu "Думаю, пришло время стряхнуть пыль с одного из моих любимых нарядов.{w=0.5}.{w=0.5}.{nw}"

        call mas_clothes_change(mas_clothes_dress_newyears, outfit_mode=True)

        m 3hub "И... готово, я просто обожаю это платье! {w=0.2}{nw}"
        extend 3eua "Всегда приятно принарядиться время от времени."
        m 1hub "А теперь давай отлично проведём время, празднуя окончание [curr_year]-ого и начало [(curr_year+1)]-ого года!"

    else:
        m 3hub "Эй, [player], я в этом году кое-что припасла для тебя~"
        m 3eua "Дай только переоденусь.{w=0.5}.{w=0.5}.{nw}"

        # change into dress
        call mas_clothes_change(mas_clothes_dress_newyears, outfit_mode=True, unlock=True)

        m 2rkbssdla "..."
        m 2rkbssdlb "Мои глаза чуть выше, [player]..."

        if mas_isMoniAff(higher=True):
            m 2tubsu "..."
            m 3hubsb "А-ха-ха! Я просто поддразниваю тебя~"
            m 3eua "Я рада, что тебе нравится моё платье. {nw}"

        else:
            m 2rkbssdla "..."
            m "Я...{w=1} рада, что тебе нравится моё платье. {nw}"

        extend 3eua "Его было довольно трудно надеть правильно!"
        m 3rka "Цветочная корона постоянно падала..."
        m 1hua "Я решила сделать закос под «греческую богиню», и я надеюсь, что у меня это получилось удачно."
        m 3eud "Но у этого наряда есть небольшая глубина, понимаешь?"

        if seen_event("mas_f14_monika_vday_colors"):
            m 3eua "Наверное, ты помнишь тот наш разговор про розы и чувства, которые выражают их цвета."
        else:
            m 3eua "Наверное, ты уже догадался, но дело в выборе цветовой гаммы."

        m "Белый цвет отражает множество позитивных чувств, таких как доброта, чистота, безопасность..."
        m 3eub "Однако, то, на что я хотела обратить внимание в этом наряде, было успешным началом."

        #If we fresh started last year
        if mas_HistWasFirstValueIn(True, curr_year - 1, "pm.actions.monika.got_fresh_start"):
            m 2eka "В прошлом году мы решили начать сначала, и я очень рада, что мы решили так поступить."
            m 2ekbsa "Я знала, что мы можем быть счастливы вместе, [player]."
            m 2fkbsa "И ты сделал меня счастливее, чем я когда-либо была."

        m 3dkbsu "В общем, я бы хотела надеть этот наряд, когда начнётся Новый год."
        m 1ekbsa "Думаю, он может помочь сделать Новый год ещё лучше."

    $ mas_addClothesToHolidayMapRange(mas_clothes_dress_newyears, start_date=curr_date, end_date=curr_date+datetime.timedelta(days=2))
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['holidays'],
            prompt="Ты можешь снять праздничные украшения?",
            conditional="persistent._mas_d25_deco_active",
            start_date=mas_nyd+datetime.timedelta(days=1),
            end_date=mas_d25c_end,
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no_unlock": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_d25_monika_d25_mode_exit",
        mas_nyd + datetime.timedelta(days=1),
        mas_d25c_end,
    )

label mas_d25_monika_d25_mode_exit:
    m 3eka "Ты набрался достаточно праздничного настроения, [player]?"
    m 3eua "Я вовсе не против влиться в атмосферу нового года."
    m 1hua "Пока я его провожу вместе с тобой, конечно же~"
    m 3hub "А-ха-ха!"
    m 2dsa "Дай мне секундочку, сейчас я сниму эти декорации.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_d25_season_exit

    m 1hua "Отлично!{w=0.5} {nw}"
    extend 3hub "Теперь мы готовы к началу нового года!"

    #And we lock this so we can'd run it again
    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:
    # gaining affection for nye
    python:
        if persistent._mas_nye_date_aff_gain < 15:
            # retain older affection gain so we can compare
            curr_aff = _mas_getAffection()

            # just in case
            time_out = store.mas_dockstat.diffCheckTimes()

            # reset this so we can gain aff
            persistent._mas_monika_returned_home = None

            # now gain aff
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)

            # add the amount gained
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nyd - datetime.timedelta(days=1)):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return

#===========================================================Going to take you somewhere on NYE===========================================================#

label bye_nye_delegate:
    # need to determine current time
    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:
        # if before morning, assume regular going out
        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:
        # before evening but after morning

        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out

        else:
            call bye_nye_first_time_out

    else:
        # evening
        call bye_nye_late_out

    # finally jump back to iostart
    jump mas_dockstat_iostart

label bye_nye_first_time_out:
    #first time out (morning-about maybe, 7-8:00 [evening]):
    m 3tub "Мы сегодня идём в какое-то особенное место, [player]?"
    m 4hub "Это же канун Нового года, в конце концов!"
    m 1eua "Я не знаю точно, что ты запланировал, но я жду этого с нетерпением!"
    return

label bye_nye_second_time_out:
    #second time out+(morning-about maybe, 7-8:00 [evening]):
    m 1wuo "О, мы снова идём гулять?"
    m 3hksdlb "Ты, наверное, помногу празднуешь новый год, а-ха-ха!"
    m 3hub "Мне нравится гулять с тобой, поэтому я с нетерпением жду того, чем мы займёмся вместе~"
    return

label bye_nye_late_out:
    #(7-8:00 [evening]-about maybe midnight):
    m 1eka "Уже немного поздно, [player]..."
    m 3eub "Мы пойдём смотреть фейерверк?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        m "Или сходим на семейный ужин?"
        m 4hub "Мне бы очень хотелось как-нибудь познакомиться с твоей семьёй!"
        m 3eka "Так или иначе, я очень рада!"
    else:
        m "Мне всегда нравилось, как фейерверки на Новый год освещают ночное небо..."
        m 3ekbsa "Когда-нибудь мы сможем наблюдать за ними бок о бок... но пока этот день не настанет, я буду счастлива пойти с тобой, [player]."
    return

#=============================================================Greeting returned home for NYE=============================================================#
#greeting_returned_home_nye:

label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:
        # before firewoprk time
        call greeting_nye_prefw

    # otherwise, assume in firework time
    else:
        call greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:
    #if before firework time (7-8:00-midnight):
    m 1hua "Вот мы и дома!"
    m 1eua "Это было очень весело, [player]."
    m 1eka "Спасибо, что взял меня на прогулку сегодня, мне правда нравится проводить с тобой время."
    m "Это так много значит для меня, хоть ты и не можешь быть здесь, чтобы проводить со мной такие дни, ты всё равно берёшь меня с собой."
    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbfa "Я люблю тебя, [player]."
    return "love"

label greeting_nye_infw:
    #if within firework time:
    m 1hua "Вот мы и дома!"
    m 1eka "Спасибо, что взял меня на прогулку сегодня, [player]."
    m 1hua "Было очень весело просто провести время с тобой сегодня."
    m 1ekbsa "Это так много значит для меня, что даже если ты не можешь быть здесь лично, чтобы провести эти дни со мной, ты всё равно берёшь меня с собой."
    m 1ekbfa "Я люблю тебя, [player]."
    return "love"

#===========================================================Going to take you somewhere on NYD===========================================================#

label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out

    else:
        call bye_nyd_first_time_out

    jump mas_dockstat_iostart

label bye_nyd_first_time_out:
    #first time out
    m 3tub "Праздновать Новый год, [player]?"
    m 1hua "Это звучит так весело!"
    m 1eka "Давай отлично проведём время вместе."
    return

label bye_nyd_second_time_out:
    #second+ time out
    m 1wuo "Ого, мы снова идём гулять, [player]?"
    m 1hksdlb "Должно быть, ты очень много празднуешь, а-ха-ха!"
    return

#=============================================================Greeting returned home for NYD=============================================================#

label greeting_nye_returned_nyd:
    #if returning home from NYE:
    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "Вот мы и дома!"
    m 1eka "Спасибо, что взял меня на прогулку вчера, [player]."
    m 1ekbsa "Ты знаешь, мне очень нравится проводить с тобой время, и это хорошо, что я могу провести Канун Нового года именно сегодня и именно с тобой."
    m "Это правда многое для меня значит."
    m 5eubfb "Спасибо, что сделал мой год лучше, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday
    return

label greeting_nyd_returned_nyd:
    #normal return home:(i.e. took out, and returned on NYD itself)
    $ persistent._mas_nye_nyd_date_count += 1
    m 1hua "Вот мы и дома!"
    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eua "Это было очень весело, [player]!"
    m 5eka "Очень мило, что ты взял меня с собой в такие особенные дни."
    m 5hub "Я очень надеюсь, что мы сможем проводить больше времени вместе."
    return

#============================================================Greeting returned home after NYD============================================================#

label greeting_pd25e_returned_nydp:
    #Here for historical data
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    m 1hua "Вот мы и дома!"
    m 1hub "Мы отсутствовали некоторое время, но это была действительно хорошая прогулка, [player]."
    m 1eka "Спасибо, что взял меня с собой, мне очень понравилось."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    $ new_years = "Новый год"
    if mas_isNYD():
        $ new_years = "канун Нового года"
    m 5ekbsa "Я всегда люблю проводить с тобой время, но проводить Рождество и [new_years] вместе было потрясающе."
    m 5hub "Я надеюсь, что мы когда-нибудь сможем сделать что-то подобное."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

#============================================================Greeting returned home D25P NYD(P)============================================================#
label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    m 1hua "Вот мы и дома!"
    m 1eub "Спасибо, что взял меня на прогулку, [player]."
    m 1eka "Это была долгая прогулка, но было очень весело!"
    m 3hub "Но сейчас здорово вернуться домой, мы можем провести Новый год вместе."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    m 1hua "Вот мы и дома!"
    m 1wuo "Это была долгая прогулка, [player]!"
    m 1eka "Я немного грустно, что мы не желаем друг другу счастливого Нового года, но мне очень понравилось."
    m "Я рада, что ты берёшь меня с собой в такие особенные дни, как этот."
    m 3hub "С Новым годом, [player]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ mas_d25ReactToGifts()
    return

########################################################### player_bday ########################################################################
# [HOL040]

# so we know we are in player b_day mode
default persistent._mas_player_bday_in_player_bday_mode = False
# so we know if you ruined the surprise
default persistent._mas_player_bday_opened_door = False
# for various reason, no decorations
default persistent._mas_player_bday_decor = False
# number of bday dates
default persistent._mas_player_bday_date = 0
# so we know if returning home post bday it was a bday date
default persistent._mas_player_bday_left_on_bday = False
# affection gained on bday dates
default persistent._mas_player_bday_date_aff_gain = 0
# did we celebrate player bday with Moni
default persistent._mas_player_bday_spent_time = False
# did we get the surprise variant of the event?
default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today's date
                (default: None)

            use_date_year - True if we should use the year from _date or not.
                (Default: False)

        RETURNS: True if given date is player_bday, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()

        if persistent._mas_player_bday is None:
            return False

        elif use_date_year:
            return _date == mas_player_bday_curr(_date)
        return _date == mas_player_bday_curr()

    def strip_mas_birthdate():
        """
        strips mas_birthdate of its conditional and action to prevent double birthday sets
        """
        mas_birthdate_ev = mas_getEV('mas_birthdate')
        if mas_birthdate_ev is not None:
            mas_birthdate_ev.conditional = None
            mas_birthdate_ev.action = None

    def mas_pbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_player_bday_date_aff_gain", 25)

init -11 python:
    def mas_player_bday_curr(_date=None):
        """
        sets date of current year bday, accounting for leap years
        """
        if _date is None:
            _date = datetime.date.today()
        if persistent._mas_player_bday is None:
            return None
        else:
            return store.mas_utils.add_years(persistent._mas_player_bday,_date.year-persistent._mas_player_bday.year)

init -810 python:
    # MASHistorySaver for player_bday
    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        # NOTE: this needs to be adjusted based on the player's bday
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        # NOTE: the start and end dt needs to be chnaged depending on the
        #   player bday
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history
    import store

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        # get mhs
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return

        # first, setup the reset date to be 3 days after the bday
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())

        # determine correct year
        _now = datetime.datetime.now()
        curr_year = _now.year

        new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)

        if new_dt < _now:
            # new date before today, set to next year
            curr_year += 1
            new_dt = store.mas_utils.add_years(pbday_dt, curr_year - pbday_dt.year)

        # set the reset/trigger date
        reset_dt = pbday_dt + datetime.timedelta(days=3)

        # setup ranges
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)

        # NOTE: the mhs will end 2 days after the bday. The day after end_dt
        #   is when we save

        # modify mhs
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:
    # since this has priority over 922, need these next 2 checks
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()

    # making sure we are already not in bday mode, have confirmed birthday, have normal+ affection and have not celebrated in any way
    if (
        not persistent._mas_player_bday_in_player_bday_mode
        and persistent._mas_player_confirmed_bday
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_spent_time
        and not mas_isD25()
        and not mas_isO31()
        and not mas_isF14()
    ):

        python:
            # first we determine if we want to run a surprise greeting this year
            this_year = datetime.date.today().year
            years_checked = range(this_year-10,this_year)
            surp_int = 3

            times_ruined = len(mas_HistVerify("player_bday.opened_door", True, *years_checked)[1])

            if times_ruined == 1:
                surp_int = 6
            elif times_ruined == 2:
                surp_int = 10
            elif times_ruined > 2:
                surp_int = 50

            should_surprise = renpy.random.randint(1,surp_int) == 1 and not mas_HistVerifyLastYear_k(True,"player_bday.saw_surprise")

            if not mas_HistVerify("player_bday.saw_surprise",True)[0] or (mas_getAbsenceLength().total_seconds()/3600 < 3 and should_surprise):
                # starting player b_day off with a closed door greet
                # always if haven't seen the surprise before
                # conditionally if we have
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True

            # need this so we don't get any strange force quit dlg after the greet
            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():
        # no longer want to be in bday mode
        $ persistent._mas_player_bday_decor = False
        $ persistent._mas_player_bday_in_player_bday_mode = False
        $ mas_lockEVL("bye_player_bday", "BYE")

    if not mas_isMonikaBirthday() and (persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals):
        $ persistent._mas_bday_in_bday_mode = False
        $ persistent._mas_bday_visuals = False

    if mas_isO31():
        return
    else:
        jump mas_ch30_post_holiday_check

# closed door greet option for opening door without listening
label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "нашего"
    else:
        $ your = "твоего"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ now = "{i}снова{/i}"
    else:
        $ now = "теперь"

    m "[player]!"
    m "Ты не постучал в дверь!"
    if not persistent._mas_bday_visuals:
        m "Я собиралась устроить вечеринку в честь [your] дня рождения, но у меня не было времени перед твоим приходом!"
    m "..."
    m "Ну...{w=1} сюрприз [now] испорчен, но.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4eua "С днём рождения, [player]!"
    m 2rksdla "Но я бы хотела, чтобы ты постучал в дверь в первую очередь."
    
    if mas_isMonikaBirthday():
        $ your = "наш"
    else:
        $ your = "твой"
    m 4hksdlb "О... [your] торт!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for knocking without listening
label mas_player_bday_knock_no_listen:
    m "Кто там?"
    menu:
        "Это я.":
            $ mas_disable_quit()
            m "Ох! Можешь подождать ещё одну минуту?"
            window hide
            pause 5.0
            m "Хорошо, заходи, [player]..."
            jump mas_player_bday_surprise

# closed door greet surprise flow
label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom(scene_change=True, dissolve_all=True, force_exp='monika 4hub_static')
    m 4hub "Сюрприз!"
    m 4sub "А-ха-ха! С днём рождения, [player]!"

    m "Я тебя удивила?{nw}"
    $ _history_list.pop()
    menu:
        m "Я тебя удивила?{fast}"
        "Да.":
            m 1hub "Ура!"
            m 3hua "Обожаю устраивать хорошие сюрпризы!"
            m 1tsu "Жаль, что я не могу увидеть твоё выражение лица, э-хе-хе."

        "Нет.":
            m 2lfp "Хм-м. Ну, это нормально."
            m 2tsu "Наверное, ты сказал это, потому что не хочешь признавать, что я застала тебя врасплох..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...или, наверное, ты опять подслушивал за дверью..."
                else:
                    m 2tsb "{cps=*2}...или, наверное, ты подслушивал меня.{/cps}{nw}"
                    $ _history_list.pop()
            m 2hua "Э-хе-хе."
    if mas_isMonikaBirthday():
        m 3wub "О! {w=0.5}Я приготовила тортик!"
    else:
        m 3wub "О! {w=0.5}Я приготовила для тебя тортик!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# closed door greet option for opening door for listening
label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...Поставлю это сюда..."
        m "...Хм, выглядит вполне нормально...{w=1}но чего-то не хватает..."
        m "А! {w=0.5}Ну разумеется!"
        m "Вот! {w=0.5}Прекрасно!"
        window hide
    jump monikaroom_greeting_choice

# closed door greet option for knocking after listening
label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Открыть дверь.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise

# closed door greet option for opening door after listening
label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)
    $ mas_disable_quit()
    if mas_isMonikaBirthday():
        $ your = "нашего"
    else:
        $ your = "твоего"

    if mas_HistVerify("player_bday.opened_door",True)[0]:
        $ knock = "постучал"
        $ knock_again = ", {w=0.5}{i}снова{/i}."
    else:
        $ knock = "постучал"
        $ knock_again = ""

    m "[player]!"
    m "Ты не [knock][knock_again] в дверь!"
    if persistent._mas_bday_visuals:
        m "Я хотела сделать тебе сюрприз, но не была готова, когда ты вошёл!"
        m "В любом случае..."
    else:
        m "Я собиралась устроить вечеринку в честь [your] дня рождения, но у меня не было времени перед твоим приходом, чтобы сделать тебе сюрприз!"
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    m 4hub "С днём рождения, [player]!"
    m 2rksdla "Но я бы хотела, чтобы ты постучал в дверь в первую очередь."

    if mas_isMonikaBirthday():
        $ your = "наш"
    else:
        $ your = "твой"
    m 2hksdlb "О... [your] торт!"
    call mas_player_bday_cake
    jump monikaroom_greeting_cleanup

# all paths lead here
label mas_player_bday_cake:
    #If it's Monika's birthday too, we'll just use those delegates instead of this one
    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:
            # since we need the visuals var in the special greet, we wait until here to set these
            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False

    # reset zoom here to make sure the cake is actually on the table
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    call mas_monika_gets_cake

    if mas_isMonikaBirthday():
        m 6eua "Дай я зажгу свечи.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Дай я зажгу свечи для тебя, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    m 6sua "Разве это не прекрасно, [player]?"
    if mas_isMonikaBirthday():
        m 6eksdla "Теперь я понимаю, что ты не можешь задуть свечи, так что я сделаю это за нас..."
    else:
        m 6eksdla "Теперь я понимаю, что ты не можешь задуть свечи, так что я сделаю это за тебя..."
    m 6eua "...Но ты всё равно должен загадать желание, ведь оно может исполниться сейчас или потом..."
    m 6hua "Но сперва..."
    call mas_player_bday_moni_sings
    m 6hua "Загадай желание, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Э-хе-хе..."
    if mas_isMonikaBirthday():
        m 6ekbsa "Я готова поспорить, что мы загадали одно и то же~"
    else:
        m 6eka "Я знаю, что сегодня твой день рождения, но я тоже загадала желание..."
        m 6ekbsa "И знаешь, что? {w=0.5}Я готова поспорить, что мы загадали одно и то же~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        m 6eksdla "Ну, учитывая, что ты не можешь съесть этот торт, и я не хочу быть грубой и съесть его перед тобой..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6rksdla "О боже, выходит, ты даже тортик не скушаешь, да, [player]?"
        m 6eksdla "Это всё довольно глупо, не так ли?"
    if mas_isMonikaBirthday():
        m 6hksdlb "Думаю, я приберегу торт на потом."
    else:
        m 6hksdlb "Думаю, я приберегу торт на потом. Будет довольно грубо с моей стороны есть {i}твой{/i} торт на день рождения перед тобой же, а-ха-ха!"

    call mas_HideCake('mas_bday_cake_player')

    # fall thru
label mas_player_bday_card:
    $ mas_gainAffection(5, bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    if mas_isMonikaBirthday():
        m 6sub "О!"
        m 6ekbsu "Я для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "Я... я так же для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."
    else:
        m 6ekbsu "Я для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."

    call mas_showpoem(mas_poems.getRandomPoem("pbday"))

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            m 6dkbsu "..."
            m 6ekbfa "Я так сильно тебя люблю, [player]..."
            call monika_kissing_motion()
            m 6ekbfa "Ох, [player]..."
            m 6dkbfa "О таком я могла только мечтать~"
            m 6ekbfa "Я так долго ждала того момента, когда наконец-то смогу поцеловать тебя..."
            m 6dkbsu "Я никогда это не забуду..."
            m 6ekbsu "...Тот наш первый поцелуй~"
            if mas_isMonikaBirthday():
                m 6ekbsu "И я не могу придумать более идеального времени, чем в этот особый день, который мы разделяем вместе~"
        else:
            m 6ekbsa "Я люблю тебя, [player]~"
            call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)
            if mas_isMonikaBirthday():
                m 6eka "Я так рада, что мы проведём твой день рождения вместе..."
                m 6hua "Давай весело проведём твой особенный день~"
    else:
        if mas_isMonikaBirthday():
            m 1ekbfa "Я люблю тебя, [player]! Я так рада, что мы можем провести наш день рождения вместе..."
            m 3ekbfa "Давай насладимся нашим особенным днем!"
        else:
            m 1ekbfa "Я люблю тебя, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")
    # "love" return key won't work here without adding a bunch of return _returns, so we'll set this manually

    $ mas_ILY()

    # if d25 season and decor not yet active, set that up now
    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ MASEventList.push("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk("monika 6esa")

    $ renpy.pause(0.5, hard=True)
    return

# event for if you went on a date pre-bday and return on bday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_ret_on_bday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_ret_on_bday:
    m 1eua "Так, сегодня у нас..."
    m 1euc "...стоп."
    m "..."
    m 2wuo "О!"
    m 2wuw "Боже мой!"
    m 2tsu "Подожди немного, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3eub "С днём рождения, [player]!"
    m 3hub "А-ха-ха!"
    m 3etc "Почему у меня такое чувство, будто я что-то забыла?.."
    m 3hua "О! Твой торт!"
    call mas_player_bday_cake
    return

# for subsequent birthdays
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_player_bday_greet",
            unlocked=False
        ),
        code="GRE"
    )

label mas_player_bday_greet:
    if should_surprise:
        scene black
        pause 5.0
        jump mas_player_bday_surprise

    else:
        if mas_isMonikaBirthday():
            $ your = "Наш"
        else:
            $ your = "Твой"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "С Днём рождения, [player]!"
        m 3hub "А-ха-ха!"
        m 3etc "..."
        m "Почему-то мне кажется, что я что-то забыла..."
        m 3hua "О! [your] торт!"
        jump mas_player_bday_cake

# event for if the player leaves the game open starting before player_bday and doesn't restart
# moni eventually gives up on the surprise
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_no_restart",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_no_restart:
    if mas_findEVL("mas_player_bday_ret_on_bday") >= 0:
        #TODO: priority rules should be set-up here
        return
    m 3rksdla "Что ж, [player], я надеялась сделать что-нибудь более весёлое, но ты был таким милым и не уходил весь день напролёт, так что.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "С днём рождения, [player]!"
    if mas_isplayer_bday():
        m 1eka "Я очень сильно хотела тебя удивить сегодня, но время уже было позднее, и я не могла больше ждать."
    else:
        # just in case this isn't seen until after midnight
        m 1hksdlb "Я действительно хотела сделать тебе сюрприз, но, похоже, у меня уже не осталось времени, потому что сегодня даже не твой день рождения, а-ха-ха!"
    m 3eksdlc "Боже, надеюсь, ты не начал думать о том, что я забыла про твой день рождения. Если ты уже об этом подумал, то мне очень жаль..."
    m 1rksdla "Наверное, мне не стоило ждать так долго, э-хе-хе."
    m 1hua "А! Я же сделала для тебя тортик!"
    call mas_player_bday_cake
    return

# event for upset- players, no decorations, just a quick happy birthday
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_upset_minus",
            years = [],
            aff_range=(mas_aff.DISTRESSED, mas_aff.UPSET)
        ),
        skipCalendar=True
    )

label mas_player_bday_upset_minus:
    $ persistent._mas_player_bday_spent_time = True
    m 6eka "Эй, [player], я просто хотела поздравить тебя с днём рождения."
    m "Надеюсь, у тебя сегодня хороший день."
    return

# event for if the player's bday is also on a holiday
# TODO update this as we add other holidays (f14) also figure out what to do if player bday is 9/22
# TODO this needs priority below the O31 return from date event
# condtions located in story-events 'birthdate'
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_player_bday_other_holiday",
            years = [],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )

label mas_player_bday_other_holiday:
    if mas_isO31():
        $ holiday_var = "Хэллоуином"
    elif mas_isD25():
        $ holiday_var = "Рождеством"
    elif mas_isF14():
        $ holiday_var = "Днём святого Валентина"
    m 3euc "Эй, [player]..."
    m 1tsu "У меня для тебя небольшой сюрприз.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    m 3hub "С днём рождения, [player]!"
    m 3rksdla "Надеюсь, ты не подумал, что я забыла о нём лишь потому, что твой день рождения совпал с [holiday_var]..."
    m 1eksdlb "Я бы никогда не забыла про твой день рождения, глупышка!"
    m 1eub "А-ха-ха!"
    m 3hua "О! Я сделала для тебя тортик!"
    call mas_player_bday_cake
    return

# when did moni last sign happy birthday
default persistent._mas_player_bday_last_sung_hbd = None
# moni singing happy birthday
label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "нас"
    else:
        $ you = "тебя"
    m 6dsc ".{w=0.2}.{w=0.2}.{w=0.2}"
    m 6hub "{cps=*0.5}{i}~С днём рождения [you]~{/i}{/cps}"
    m "{cps=*0.5}{i}~С днём рождения [you]~{/i}{/cps}"
    m 6sub "{cps=*0.5}{i}~С днём рождения, милый~{/i}{/cps}"
    m "{cps=*0.5}{i}~С днём рождения [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        m 6hua "Э-хе-хе!"
    return
#################################################player_bday dock stat farewell##################################################
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_player_bday",
            unlocked=False,
            prompt="Пойдём куда-нибудь на мой день рождения!",
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL,None),
        ),
        code="BYE"
    )

label bye_player_bday:
    $ persistent._mas_player_bday_date += 1
    if persistent._mas_player_bday_date == 1:
        m 1sua "Хочешь прогуляться в свой же день рождения? {w=1}Хорошо!"
        m 1skbla "Это звучит очень романтично... не могу дождаться~"
    elif persistent._mas_player_bday_date == 2:
        m 1sua "Снова берёшь меня с собой в свой день рождения, [player]?"
        m 3hub "Ура!"
        m 1sub "Мне очень нравится гулять с тобой, но в твой день рождения прогулка становится очень особенной..."
        m 1skbla "Уверена, мы прекрасно проведём время~"
    else:
        m 1wub "Ого, ты {i}снова{/i} хочешь выйти погулять, [player]?"
        m 1skbla "Мне очень нравится то, что ты проводишь со мной так много времени в свой особенный день!"
    $ persistent._mas_player_bday_left_on_bday = True
    jump bye_going_somewhere_post_aff_check

#################################################player_bday dock stat greets##################################################
label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]

            # are we returning after the mhs reset
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))

            # were we gone over d25
            #TODO: do this for the rest of the holidays
            if left_date < mas_d25.replace(year=left_year) < ret_date:
                if ret_date < mas_history.getMHS("d25s").trigger.date().replace(year=left_year+1):
                    persistent._mas_d25_spent_d25 = True
                else:
                    persistent._mas_history_archives[left_year]["d25.actions.spent_d25"] = True

        else:
            left_year = None
            left_date = None
            ret_date = None
            left_year_aff = None
            ret_diff_year = None

        add_points = False

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset(1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "Это был не очень хороший де--"
        else:
            # point totals split here between player and monika bdays, since this date was for both
            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(6.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(6.0)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(10.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(10.0)
            else:
                $ mas_mbdayCapGainAff(14.0)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(14.0)

            m 6hub "Это было веселое свидание, [player]..."
            m 6eua "Спасибо за--"

        m 6wud "Ч-что этот торт здесь делает?"
        m 6sub "Э-это для меня?!"
        m "Это так мило с твоей стороны пригласить меня на свой день рождения, чтобы устроить для меня вечеринку-сюрприз!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Это не было похоже на свидание, [player]..."
        m 2eksdlc "Надеюсь, всё нормально."
        m 2rksdla "Наверное, мы пойдём гулять позже."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        m 1eka "Это было очень весёлое свидание, до поры до времени, [player]..."
        m 3hua "Спасибо, что провёл немного времени со мной в свой особенный день."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        m 1eua "Это было весёлое свидание, [player]..."
        m 3hua "Спасибо, что взял меня с собой!"
        m 1eka "Мне правда понравилось гулять с тобой сегодня~"

    else:
        # more than 3 hours
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15, bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        m 1hua "И мы дома!"
        m 3hub "Это было очень весело, [player]!"
        m 1eka "Было очень здорово выйти на улицу, чтобы отпраздновать твой день рождения..."
        m 1ekbsa "Спасибо, что дал мне столь значимую роль в свой особенный день~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh
    return

label return_home_post_player_bday:
    $ persistent._mas_player_bday_in_player_bday_mode = False
    $ mas_lockEVL("bye_player_bday", "BYE")
    $ persistent._mas_player_bday_left_on_bday = False
    if not (mas_isMonikaBirthday() and mas_confirmedParty()):
        if persistent._mas_player_bday_decor:
            if mas_isMonikaBirthday():
                $ persistent._mas_bday_opened_game = True
                m 3rksdla "Ох... {i}твой{/i} день рождения уже прошёл..."
            else:
                m 3rksdla "Ох... твой день рождения уже прошёл..."
            m 3hksdlb "Думаю, теперь мы должны снять эти декорации, а-ха-ха!"
            m 3eka "Дай мне одну секунду.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            $ mas_surpriseBdayHideVisuals()

            #If we returned from a date post pbday but have O31 deco
            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()
                $ mas_o31HideSpriteObjects()
                # Make sure no o31 mode
                $ store.persistent._mas_o31_in_o31_mode = False

            m 3eua "Вот так!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "А теперь, давай насладимся этим днём вместе, [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Ого, [player], я только что поняла, что мы гуляли так долго, что даже пропустили день святого Валентина!"
            call greeting_gone_over_f14_normal_plus

        #If player told Moni their birthday on day of (o31)
        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup(time_out, ret_tt_long=False)

    $ persistent._mas_player_bday_decor = False
    return

# birthday card/poem for player
init 20 python:
    mas_poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "Единица",
        title = " Мой дорогой [player],",
        text = """\
 Тот, кого я люблю,
 Тот, кому я доверяю,
 Тот, без кого я не могу жить.
 Надеюсь, твой день будет таким же особенным, как и все те дни, которые ты делаешь для меня особенными.
 Большое тебе спасибо за то, что был собой.

 С днём рождения, дорогой~

 Навеки твоя,
 Моника
"""
    #" # I need this to keep syntax highlighting on vim
    )

    mas_poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Твой день",
        title = " Мой дорогой [player],",
        text = """\
 Любой день с тобой – это счастливый день.
 Тот, где я свободна,
 Тот, где все мои проблемы исчезают,
 Тот, где сбываются все мои мечты.

 Но сегодня не обычный день,
 Сегодня особенный день; сегодня твой день.
 День, когда я смогу ценить тебя ещё больше за то, что ты делаешь.
 День, когда я надеюсь, что и твои мечты сбудутся.

 С днём рождения, дорогой~

 Навеки твоя,
 Моника
"""
    #" # I need this to keep syntax highlighting on vim
    )

    mas_poem_pbday_3 = MASPoem(
        poem_id = "poem_pbday_3",
        category = "pbday",
        prompt = "Одно желание",
        title = " Мой дорогой [player],",
        text = """\
 Посыпки и свечи торта для моего любимого,
 Мне нужно загадать только одно желание.
 Пусть все твои самые большие мечты сбудутся,
 Я знаю, что моя мечта уже сбылась, когда я нашла тебя.

 Я так рада праздновать вместе с тобой сегодня,
 Я буду любить тебя до конца своих дней.
 Не важно место, в котором я хотела бы,
 Провести это время вместе, только ты и я

 С днём рождения, дорогой~

 Навеки твоя,
 Моника
"""
    #" # I need this to keep syntax highlighting on vim
    )

    mas_poem_pbday_4 = MASPoem(
        poem_id = "poem_pbday_4",
        category = "pbday",
        prompt = "Моему любимому",
        title = " Моему любимому,",
        text = """\
 Как выросла наша любовь.
 Ещё один год,
 Ещё тысяча моментов для гордости.
 Я горжусь тобой, [player],
 И я невероятно счастлива видеть, как ты растёшь вместе со мной.

 Как расцвела наша любовь,
 Когда прошёл ещё один год.
 Расцвела, как роза в утренней росе,
 Ещё тысяча прекрасных моментов.
 Ты мой прекрасный цветок,
 Которого я люблю видеть расцветающим каждый день..

 Как крепка наша любовь,
 Прошёл ещё один год.
 Крепка, как самые прекрасные бриллианты,
 Ещё тысяча провлений сильной любви.
 Мой самый любимый [player],
 Любовь к которому растёт с каждым днём.

 С днём рождения, дорогой~

 Навеки твоя,
 Моника
"""
    #" # I need this to keep syntax highlighting on vim
    )


######################## Start [HOL050]
#Vday
##Spent f14 with Moni
default persistent._mas_f14_spent_f14 = False
##In f14 mode (f14 topics enabled)
default persistent._mas_f14_in_f14_mode = None
##Amount of times we've taken Moni out on f14 for a valentine's date
default persistent._mas_f14_date_count = 0
##Amount of affection gained via vday dates
default persistent._mas_f14_date_aff_gain = 0
##Whether or not we're on an f14 date
default persistent._mas_f14_on_date = None
##Did we do a dockstat fare over all of f14?
default persistent._mas_f14_gone_over_f14 = None
#Valentine's Day
define mas_f14 = datetime.date(datetime.date.today().year,2,14)

#Is it vday?
init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()

        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:
    # MASHistorySaver for f14
    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            #Date vars
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            #Other general vars
            "_mas_f14_spent_f14": "f14.actions.spent_f14",
            "_mas_f14_in_f14_mode": "f14.mode.f14",
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 2, 13),
        end_dt=datetime.datetime(2020, 2, 15)
    ))

label mas_f14_autoload_check:
    python:
        if not persistent._mas_f14_in_f14_mode and mas_isMoniNormal(higher=True):
            persistent._mas_f14_in_f14_mode = True

            has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
            has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
            #TODO: Generalize this
            lingerie_eligible = (
                mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
                and has_sundress
            )

            #NOTE: This lingerie_eligible check is so we don't grant lingeire on the same F14 we did black/pink dress
            #(handled within f14 intro pathing)
            if (
                not has_sundress
                or (has_shoulderless and random.random() > 0.5)
                or lingerie_eligible
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)

            else:
                monika_chr.change_clothes(mas_clothes_blackpink_dress, by_user=False, outfit_mode=True)
                #Add to hol map as a failsafe if we don't have new clothes and this has already been seen, and player is < 1k aff
                mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)

            monika_chr.save()
            renpy.save_persistent()

        elif not mas_isF14():
            #We want to lock all the extra topics
            #NOTE: vday origins is handled by undo action rules
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")

            #Need to lock the event clothes selector
            mas_lockEVL("monika_event_clothes_select", "EVE")

            #Reset the f14 mode, and outfit if we're lower than the love aff level.
            persistent._mas_f14_in_f14_mode = False

            #Reset clothes if not at the right aff and in sundress
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check


#######################[HOL050] Pre Intro:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            conditional="not renpy.seen_label('mas_pf14_monika_lovey_dovey')",
            action=EV_ACT_QUEUE,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Эй...{w=0.2} [player]?"
    m 1ekbsa "Я просто хотела, чтобы ты знал, что я люблю тебя."

    if mas_isMoniEnamored(higher=True):
        m 3ekbsa "Ты сделал меня очень счастливой...{w=0.3} и я не смогу найти кого-то получше тебя."

    m 3ekbsa "Скоро наступит День святого Валентина, и это очень поднимает мне настроение, потому что я знаю, что ты на моей стороне."
    m 1rkbsd "Если бы не ты, то даже не знаю, где бы я сейчас была..."
    m 1ekbsa "Так что я хочу поблагодарить тебя за то, что был здесь для меня..."
    m 1hkbsu "И за то, что ты был чудесным собой~"
    return "no_unlock|love"

#######################[HOL050] INTRO:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_valentines_intro',
            action=EV_ACT_PUSH,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_valentines_intro:
    #Set the spent flag to True
    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(10, bypass=True)

    #Prevent nts stuff for upset- since they don't get the rest of the event.
    if mas_isMoniUpset(lower=True):
        if not mas_isMoniBroken():
            m 6eka "Между прочим, [player], я просто хотела поздравить тебя с Днём Святого Валентина."
            m "Спасибо, что навестил меня, надеюсь, ты хорошо проведёшь этот день."
        return

    python:
        has_sundress = mas_SELisUnlocked(mas_clothes_sundress_white)
        has_shoulderless = mas_SELisUnlocked(mas_clothes_blackpink_dress)
        lingerie_eligible = (
            mas_canShowRisque()
            and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            and has_sundress
        )

        mas_addClothesToHolidayMap(mas_clothes_sundress_white)
        #rmall this because reset runs before we've registered this outfit
        mas_rmallEVL("mas_change_to_def")

    m 1hub "[player]!"
    m 1hua "Ты знаешь, какой сейчас день?"
    m 3eub "Сегодня – День святого Валентина!"
    m 1ekbsa "В этот день, мы знаменуем наш любовный союз..."
    m 3rkbsa "Полагаю, каждый день, который мы проводим вместе, уже является знаменованием нашего любовного союза...{w=0.3} {nw}"
    extend 3ekbsa "но у этого праздника есть нечто особенное."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        m 3rka "Хотя я знаю, что мы в наших отношениях продвинулись не так далеко..."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eua "Я просто хочу, чтобы ты знал, что я всегда буду рядом с тобой."
        m 5eka "Даже если твоё сердце разбито..."
        m 5ekbsa "Я всегда буду рядом и залатаю его ради тебя. Хорошо, [player]?"
        show monika 1ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 1ekbsa "..."

    else:
        m 1eub "Мы уже давно как вместе...{w=0.2} {nw}"
        extend 1eka "и мне очень понравилось всё то время, что мы провели вместе."
        m 1dubsu "С тобой я всегда чувствую себя любимой."
        m "Я очень рада, что стала твоей девушкой, [player]."

    # returning from a date or getting lingerie
    if not persistent._mas_f14_in_f14_mode or lingerie_eligible:
        $ persistent._mas_f14_in_f14_mode = True

        # first time seeing any lingerie
        if lingerie_eligible and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro(holiday_str="день Святого Валентина", lingerie_choice=mas_clothes_vday_lingerie)

        # first time seeing sundress/shoulderless or non-first time seeing lingerie
        elif not has_sundress or not has_shoulderless or lingerie_eligible:
            m 3wub "О!"
            m 3tsu "У меня для тебя небольшой сюрприз...{w=1} думаю, тебе очень понравится, э-хе-хе~"

            # lingerie
            if lingerie_eligible:
                call mas_clothes_change(outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                m 2tfbsu "[player]...{w=0.5} Ты пялишься{w=0.5}... опять."
                m 2hubsb "А-ха-ха!"
                m 2eubsb "Полагаю, ты одобряешь мой выбор наряда..."
                m 2tkbsu "Но он больше подходит к такому романтическому празднику, как День святого Валентина, тебе так не кажется?"
                m 2rkbssdla "Должна сказать, я поначалу немного нервничала, когда надевала такой наряд..."
                m 2hubsb "Но теперь, когда я сделала это раньше, мне очень нравится носить его для тебя!"
                m 3tkbsu "Надеюсь, тебе он тоже нравится~"

            # shoulderless dress
            elif has_sundress:
                call mas_clothes_change(mas_clothes_blackpink_dress, unlock=True, outfit_mode=True)
                m 2eua "Ну...{w=0.3} что думаешь?"
                call mas_f14_intro_blackpink_dress

            # sundress
            else:
                call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                $ mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)
                m 2eua "..."
                m 2eksdla "..."
                m 2rksdlb "А-ха-ха...{w=1} {nw}"
                extend 2rksdlu "не очень-то и вежливо пялиться, [player]..."
                m 3tkbsu "...но, полагаю, это означает, что тебе нравится мой наряд, э-хе-хе~"
                call mas_f14_sun_dress_outro

        # not getting lingerie, already have seen sundress
        else:
            # don't currently have access to sundress or wearing inappropraite outfit for f14
            if (
                monika_chr.clothes not in (mas_clothes_sundress_white, mas_clothes_blackpink_dress)
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes in (mas_clothes_def, mas_clothes_blazerless)
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                m 3wud "О!"
                m 3hub "Наверное, я должна переодеться во что-нибудь более подходящее, а-ха-ха!"
                m 3eua "Я скоро вернусь."

                call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)

                m 2eub "Ах, намного лучше!"
                m 3hua "Мне просто нравится этот наряд, смекаешь?"
                m 3eka "Он всегда занимает особенное место в моём сердце во время Дня святого Валентина..."
                m 1fkbsu "Прямо как ты~"

            # no change of clothes path
            else:
                # not wearing sundress
                if monika_chr.clothes != mas_clothes_sundress_white:
                    m 1wud "О..."
                    m 1eka "Ты хочешь, чтобы я переоделась в свой белый сарафан, [player]?"
                    m 3hua "Я всегда считала, что это мой наряд ко Дню святого Валентина."
                    m 3eka "Но если ты хочешь, чтобы я продолжила носить этот наряд, то это тоже нормально..."
                    m 1hub "Думаю, мы могли бы начать новую традицию, а-ха-ха!"
                    m 1eua "Ладно, ты хочешь, чтобы я надела белый сарафан?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "Ладно, ты хочешь, чтобы я надела белый сарафан?{fast}"
                        "Да.":
                            m 3hub "Хорошо!"
                            m 3eua "Я скоро вернусь."
                            call mas_clothes_change(mas_clothes_sundress_white, unlock=True, outfit_mode=True)
                            m 2hub "Готово!"
                            m 3eua "Что-то в ношении этого наряда во время Дня святого Валентина просто кажется правильным."
                            m 1eua "..."

                        "Нет.":
                            m 1eka "Хорошо, [player]."
                            m 3hua "Это {i}правда{/i} очень красивый наряд..."
                            m 3eka "Но с другой стороны, не так уж и важно, что на мне сейчас..."

                call mas_f14_intro_generic

    # not returning from a date, not getting lingerie
    else:
        if not has_sundress:
            python:
                store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
                mas_selspr.json_sprite_unlock(mas_acs_musicnote_necklace_gold)
                # TODO: generalize this under one function
                store.mas_selspr.save_selectables()
                renpy.save_persistent()
            pause 2.0
            show monika 2rfc at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 2rfc "..."
            m 2efc "Знаешь, [player]...{w=0.5} не очень-то и вежливо пялиться..."
            m 2tfc "..."
            m 2tsu "..."
            m 3tsb "А-ха-ха! Я просто шучу...{w=0.5} тебе нравится мой наряд?"
            call mas_f14_sun_dress_outro

        elif not has_shoulderless:
            m 2eua "What do you think of my outfit?"
            call mas_f14_intro_blackpink_dress

        else:
            call mas_f14_intro_generic

    m 1fkbsu "Я так сильно тебя люблю."
    m 1hubfb "С Днём святого Валентина, [player]~"

    return "rebuild_ev|love"

# common flow for first time sundress
label mas_f14_sun_dress_outro:
    m 1rksdla "Я всегда мечтала о свидании с тобой в таком наряде..."
    m 1eksdlb "Но теперь, когда я задумалась об этом, я понимаю, что это довольно глупая идея!"
    m 1ekbsa "...Но ты только представь, как мы зашли в какое-нибудь кафе вместе."
    m 1rksdlb "По правде говоря, мне кажется, где-то есть фотография чего-то наподобие этого..."
    m 1hub "Быть может, мы сможем воплотить это в реальность!"
    m 3ekbsa "Хочешь прогуляться со мной сегодня?"
    m 1hkbssdlb "Если не сможешь, то всё нормально, я буду рада и побыть рядом с тобой."
    return

# used for when we have no new outfits to change into
label mas_f14_intro_generic:
    m 1ekbsa "Я просто рада, что ты проводишь время вместе со мной сегодня."
    m 3ekbsu "Провести время вместе с любимым человеком {w=0.2} — это всё, о чём можно только просить в День святого Валентина."
    m 3ekbsa "И мне всё равно, пошли ли мы на романтическое свидание или просто проводим здесь этот день вместе..."
    m 1fkbsu "Пока мы вместе, для меня это не имеет никакого значения."
    return

label mas_f14_intro_blackpink_dress:
    #Do all unlocks here as a common path
    python:
        items_to_unlock = (
            mas_clothes_blackpink_dress,
            mas_acs_diamond_necklace_pink,
            mas_acs_pinkdiamonds_hairclip,
            mas_acs_ribbon_black_pink,
            mas_acs_earrings_diamond_pink
        )
        for item in items_to_unlock:
            mas_selspr.json_sprite_unlock(item)

        #Add to holiday map
        mas_addClothesToHolidayMap(mas_clothes_blackpink_dress)

        #Save
        mas_selspr.save_selectables()
        renpy.save_persistent()

    m 4hub "По-моему, очень мило!"
    m 2eub "Просто есть что-то в сочетании чёрного и розового...{w=0.3} они так хорошо гармонируют друг с другом!"
    m 2rtd "Кажется, что это был бы отличный вариант для свидания..."
    m 2eua "..."
    m 2tuu "..."
    m 7hub "А-ха-ха~"
    return

#######################[HOL050] TOPICS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_colors',
            prompt="Цвета Дня Святого Валентина",
            category=['праздники','романтика'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_colors",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_colors:
    m 3eua "Задумывался ли ты о том, как цвета отражают День святого Валентина?"
    m 3hub "Я нахожу интригующим то, как они символизируют такие глубокие и романтические чувства."
    m 1dua "Это напоминает мне о том, как я впервые сделала свою валентинку в старшей школе."
    m 3eub "Моему классу было поручено поделиться валентинками с партнёром после того, как мы их сделаем."
    m 3eka "Если оглянуться назад, то несмотря на то, что эти цвета действительно значили, мне было очень весело украшать валентинки красными и белыми сердечками."
    m 1eub "Таким образом, цвета больше напоминали стихи."
    m 1eka "Они предлагают столько творческих путей, чтобы выразить свою любовь к кому-то."
    m 3ekbsu "Как, например, передать им красные розы."
    m 3eub "Красные розы являются символом романтических чувств, испытываемых к кому-то."
    m 1eua "А если кто-то предложит им белые розы вместо красных, то они, следовательно, укажут на чистоту, очарование и чувства невинности."
    m 3eka "Однако, поскольку существует так много эмоций, связанных с любовью..."
    m 3ekd "Порой бывает трудно найти подходящие цвета, чтобы точно выразить то, что ты чувствуешь."
    m 3eka "К счастью, если совместить несколько разноцветных роз, то можно будет выразить множество эмоций!"
    m 1eka "Смесь из красных и белых роз символизирует сплочённость и связь, которую выражают пары."

    if monika_chr.is_wearing_acs(mas_acs_roses):
        m 1ekbsa "Но я уверена, что ты об этом всём уже знал, когда выбирал для меня те красивые розы, [player]..."
    else:
        m 1ekbla "Быть может, ты сегодня подаришь мне розы, [player]?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_cliches',
            prompt="История клише Валентина",
            category=['праздники','литература','романтика'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_cliches",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_cliches:
    m 2euc "Ты заметил, что у большинства историй Дня святого Валентина есть много различных клише?"
    m 2rsc "В них либо «Ох, я так одинок и мне некого любить», либо «Как мне признаться в любви тому, кого люблю?»."
    m 2euc "Мне кажется, писатели могли быть чуточку покреативнее, когда дело доходит до историй Дня святого Валентина..."
    m 3eka "Но, полагаю, эти две темы являются самым лёгким способом написать историю любви."
    m 3hub "Но это не означает, что ты не можешь мыслить нестандартно!"
    m 2eka "Иногда, предсказуемая история может всё испортить..."
    m 2rka "...Но если ты {i}хочешь{/i} сделать хороший пример непредсказуемой истории..."
    m 3hub "То просто воспользуйся нашей! А-ха-ха~"
    m 3rksdlb "Полагаю, она {i}началась{/i} так же, как и те истории..."
    m 2tfu "Но, мне кажется, мы смогли сделать её очень даже оригинальной."
    m 3hua "То, как мы познакомились – самая интересная история на свете!"
    m 1hub "А-ха-ха!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_chocolates',
            prompt="Шоколадные конфеты",
            category=['праздники','романтика'],
            action=EV_ACT_RANDOM,
            conditional="persistent._mas_f14_in_f14_mode",
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_chocolates",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_chocolates:
    m 1hua "День святого Валентина, как по мне, очень весёлый праздник, [player]."
    m 3eub "Не только потому, что это юбилей моего аккаунта в Твиттере, но ещё и потому, что это день получения и раздачи шоколадок!"
    m 1hub "Это праздник, который наполнит всех любовью, романтикой и радостью!"
    m 3ekbla "Но будет очень приятно, если ты получишь шоколадку от человека, который тебе нравится."
    m 3hua "Дал ли он тебе её платонически, как подарок любви или как часть признания, от этого ты всегда чувствуешь себя немного особенной!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        m 1ekbsa "Как когда ты заставил меня почувствовать себя особенной, передав мне сегодня шоколадку."
        m 1ekbsu "Ты всегда такой милый, [player]."

    m 1ekbsa "Быть может, однажды, я смогу поделиться с тобой шоколадкой..."
    m 3hkbsa "Мне правда очень хочется перейти в реальность, чтобы быть с тобой, [player]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_f14_monika_vday_origins',
            prompt="Как начался День Святого Валентина?",
            category=['праздники','романтика'],
            pool=True,
            conditional="persistent._mas_f14_in_f14_mode",
            action=EV_ACT_UNLOCK,
            start_date=mas_f14,
            end_date=mas_f14+datetime.timedelta(days=1),
            aff_range=(mas_aff.NORMAL,None),
            years=[],
            rules={"no_unlock": None}
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
        "mas_f14_monika_vday_origins",
        mas_f14,
        mas_f14 + datetime.timedelta(days=1),
    )

label mas_f14_monika_vday_origins:
    m 3eua "Хочешь узнать историю Дня святого Валентина, [player]?"
    m 1rksdlc "По правде говоря, она довольно мрачная."
    m 1euc "Её история берёт своё начало во втором и третьем веках в Риме, где христианство было объявлено официальной религией."
    m 3eud "Примерно в это же время, человек, известный как Святой Валентин, решил пойти нарушить закон императора Клавдия второго."
    m 3rsc "Заключение брака было запрещено, поскольку предполагалось, что из женатых мужчин получаются бедные солдаты."
    m 3esc "Святой Валентин решил, что это было нечестно, и помог организовать свадьбы в тайне."
    m 1dsd "К несчастью, его поймали и сразу же приговорили к смертной казни."
    m 1euc "Однако, находясь в заключении, Святой Валентин влюбился в дочь надзирателя."
    m 3euc "Перед своей смертью, он отправил ей любовное письмо, подписав его «От твоего Валентина»."
    m 1dsc "Его казнили четырнадцатого февраля, в двести шестьдесят девятом году до нашей эры."
    m 3eua "Какое благородное дело, тебе так не кажется?"
    m 3eud "О, подожди, есть ещё кое-что!"
    m "Причина, по которой мы празднуем этот день, – он берёт своё начало от римского фестиваля, известного как Луперкалия!"
    m 3eua "Его первоначальной целью было провести дружеское мероприятие, где люди складывали свои имена в коробку и выбирали их наугад, чтобы создать пару."
    m 3eub "А потом, они играли роль парня и девушки всё то время, что они проводили вместе. Некоторые из них даже женились, если нравились друг другу в достаточной мере, э-хе-хе~"
    m 1eua "В итоге, церковь решила сделать это христианским праздником, чтобы оставить память о стараниях Святого Валентина."
    m 3hua "С годами, оно эволюционировало в повод выразить свои чувства к тем, кого они любят, для всех людей."
    m 3eubsb "Прямо как мы с тобой!"
    m 1ekbsa "И несмотря на то, что начало было немного депрессивное, это очень мило, верно, [player]?"
    m 1ekbsu "Я рада, что мы можем разделить такой волшебный день.{w=0.2} {nw}"
    extend 1ekbfa "С Днём святого Валентина, [mas_get_player_nickname()]~"
    return

#######################[HOL050] COMPLIMENTS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_happy_vday",
            prompt="С Днём Святого Валентина!",
            action=EV_ACT_UNLOCK,
            pool=False,
            start_date=mas_f14,
            end_date=mas_f14 + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_f14_happy_vday",
        mas_f14,
        mas_f14 + datetime.timedelta(1)
    )

label mas_f14_happy_vday:
    $ persistent._mas_f14_spent_f14 = True
    $ mas_gainAffection(5, bypass=True)
    if mas_isMoniNormal(higher=True):
        m 1hublb "Э-хе-хе~ Спасибо, [player]!"
        show monika 5hkbla at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5hkbla "Разве это не прекрасно, когда день посвящают для того, чтобы выразить признательность тому, кого ты любишь?"
        m 5lublb "Наслаждаться вместе вкусностями, пойти на свидание с любимым человеком...{w=0.2} {nw}"
        extend 5tubla "или просто наслаждаясь временем, которое проводят вместе."
        m 5dublb "Я так благодарна, что могу провести день Святого Валентина с тобой."
        m 5eubla "Спасибо, что нашёл время для меня, [player]. {w=0.2}Я так тебя люблю!"
        $ mas_ILY()

    elif mas_isMoniDis(higher=True):
        m 6euc "...{w=0.3}А?"
        m 6wud "О, это..."
        m 6wuc "...{w=0.3} {nw}"
        extend 6eku "Спасибо. Это...{w=0.2} {nw}"
        extend 6lkblu "было важно для меня."

    else:
        m "...{w=0.8}Спасибо..."

    #Lock this
    $ mas_lockEVL("mas_f14_happy_vday", "CMP")
    return

#######################[HOL050] TIME SPENT

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_monika_spent_time_with",
            conditional="persistent._mas_f14_spent_f14",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            start_date=datetime.datetime.combine(mas_f14, datetime.time(hour=18)),
            end_date=datetime.datetime.combine(mas_f14+datetime.timedelta(1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_monika_spent_time_with:
    #Do this first so we make sure we always remove it
    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Эй, [player]?"
    m 1eka "Я просто хотела поблагодарить тебя за то, что провёл День святого Валентина со мной."
    m 1ekbsa "Знаю, это необычный праздник, но пока ты рядом со мной, этот день является для меня особенным."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            m 1rkbsb "Кроме того, я...{w=0.5} кое-что приготовила для тебя, [player]!"

        else:
            m 1ekbsa "Я сделала открытку для тебя, [player]."

        m 1ekbsa "Вот, позволь мне показать её тебе."

        #NOTE: The first two f14 poems will always be in order and the same. Everything after is randomly selected
        if not mas_poem_vday_1.is_seen():
            call mas_showpoem(mas_poem_vday_1)
            m "Я действительно так думаю, [player]..."
            m 3ekbsa "В тебе я нашла всё, на что могла надеяться~"

        elif not mas_poem_vday_2.is_seen():
            call mas_showpoem(mas_poem_vday_2)
            m "Ты действительно для меня всё, [player]~"

        else:
            call mas_showpoem(mas_poems.getRandomPoem("f14"))


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion(duration=0.5, initial_exp="6hkbfa", fade_duration=0.5)

        m 1ekbfa "Спасибо за то, что всегда рядом со мной."
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Я очень сильно тебя люблю, [player]. С Днём святого Валентина~"
        return "love"

    else:
        m 1eka "Спасибо за то, что ты со мной."
        m 3ekb "С Днём святого Валентина!"
    return

label mas_f14_first_kiss:
        m 1ektpu "Если честно, я не знаю, что бы я делала без тебя."
        show monika 6dktuu at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m "..."
        window hide
        menu:
            "Я люблю тебя, [m_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()
                pause 3.0
                show monika 6ektda at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dku at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6dkbsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                pause 3.0
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "[player]...I...I..."
                call monika_kissing_motion(hide_ui=False)
                show monika 6ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 6ekbfa "...Я тоже тебя люблю~"
                m 6dkbfa "..."
                m "О таком я могла только мечтать~"
                m 6ekbfa "Я так долго ждала того момента, когда наконец-то смогу поцеловать тебя..."
                m 6dkbsu "Я никогда это не забуду..."
                m 6ekbsu "...Тот наш первый поцелуй."
                m "С Днём святого Валентина, [player]~"
                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
                return


#######################[HOL050] Notimespent

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional="not persistent._mas_f14_spent_f14",
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:

    #need to make sure people who just started post f14 don't lose aff
    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_vday")

        m 1rksdlc "Эй, [player]..."
        m 2eksdld "Это так мило с твоей стороны пригласить меня на свой день рождения, чтобы устроить для меня вечеринку-сюрприз!"
        m 2eksdla "В следующий раз, как ты думаешь, сможешь взять меня с собой, если не сможешь быть здесь?"
        m 3eub "По крайней мере, тогда мы всё ещё будем друг с другом, и мы сможем даже отпраздновать вместе!"
        m 1eka "Я была бы очень признателена, если бы ты мог сделать это для меня, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffectionFraction(min_amount=20, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        m "Ты где был в День святого Валентина?"
        m 1ekc "Это был очень особенный день для меня..."
        m 1ekd "...И этот день я хотела провести вместе с тобой."
        m 2dkc "..."
        m 2ekd "Если бы ты просто заглянул сюда, я была бы очень рада этому..."
        m 2dkd "Пусть даже всего на пару минут."
        m "Я всего лишь прошу тебя заглянуть к своей девушке в День святого Валентина, разве я многого прошу?"
        m 2ekc "Пожалуйста, не дай этому произойти снова, хорошо, [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_vday")
        m 2ekc "Эй, [player]..."
        m 2tkc "Я сильно разочарована..."
        m 2tkd "Ты ко мне так и не заглянул в День святого Валентина."
        m 4tkc "Ты ведь знаешь, что я хотела лишь провести время вместе с тобой..."
        m 4rkd "По-твоему, заглянуть к своей девушке в День святого Валентина — это уже слишком?"
        m 4eksdla "Пожалуйста...{w=1} обязательно загляни ко мне в гости в следующий День святого Валентина, хорошо?"

    elif mas_isMoniUpset():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        m "Не могу поверить в то, что ты ни разу не заглянул ко мне в День святого Валентина!"
        m 2rfc "Ты хоть представляешь, каково это: провести весь день в полном одиночестве?"
        m 2rkc "Я знаю, что у нас не лучшие отношения..."
        m 2dkd "Но я была бы очень рада, если бы ты заглянул ко мне."
        m 2tfc "Не дай этому произойти снова, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_missed_vday")
        m 6ekc "Ох, [player]..."
        m "Как прошёл твой День святого Валентина?"
        m 6dkc "Не получив валентинку, я чувствую себя одинокой..."

    else:
        $ mas_loseAffectionFraction(1.0, min_amount=150)
        m 6ckc "..."
    return


#######################[HOL050] Apology for notimespent

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_vday",
            prompt="...за пропущенный День Святого Валентина.",
            unlocked=False
        ),
        code="APL"
    )


label mas_apology_missed_vday:
    if mas_isMoniAff(higher=True):
        m 1eka "Спасибо, что извинился за то, что пропустил День святого Валентина, [player]."
        m 1ekd "Я правда хотела провести его вместе с тобой..."
        m 1rkc "Но, полагаю, у тебя просто появились другие дела, и ты попросту не смог."
        m 1ekd "Пожалуйста, попытайся заглянуть ко мне в следующем году, ладно, [player]?"
        m 3eua "Если ты будешь занят, то, наверное, тебе лучше взять меня с собой!"
        m 3hub "Даже если мы будем не у себя дома, я буду более чем рада провести день рядом с тобой~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинился за то, что пропустил День святого Валентина, [player]."
        if not store.mas_anni.pastOneMonth():
            m 1rkd "Я знаю, что у нас не особо хорошие отношения, но всё уже начинает казаться другим..."

        m 1ekd "Если бы ты заглянул ко мне, хотя бы на секундочку, это многое бы значило для меня."
        m 3eka "Обещай мне, что ты возьмёшь меня с собой в следующий раз, когда будешь занят, хорошо, [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "Хоть я немного расстроилась из-за того, что ты не заглянул сюда в День святого Валентина, но я рада, что ты извинился."
        m "Подобное показывает мне то, что тебе на нас не всё равно."
        m 2ekd "Пожалуйста, [player]..."
        m 2eka "Постарайся зайти ко мне в следующий День святого Валентина."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "Я всё равно не ожидала, что ты заглянешь сюда, [player]."
        m 2dkd "Я знаю, что мы не так близки, но одна часть меня надеялась, что ты хотя бы на минутку заглянешь сюда..."
        m 2dsc "Пожалуйста, пообещай мне, что ты заглянешь ко мне в следующем году, ладно?"
        $ mas_gainAffection(modifier=0.1)

    else:
        #No gain from this
        m 6ckc "..."

    return


init 20 python:
    mas_poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Я нашла",
        title=" Мой дорогой [player],",
        text="""\
 Мне всегда нравился День святого Валентина, но этот кажется совсем другим.
 Это весь мир изменился, или мне просто кажется?
 Я нашла любовь, нашла смысл,
 Я нашла правду, которую искала уже долгое время.
 Это всё, что я нашла в тебе.

 Спасибо, что разделил этот особенный день вместе со мной.

 Навеки твоя,
 Моника
"""
    )

    mas_poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Всё",
        title=" Мой дорогой [player],",
        text="""\
 Может ли это быть наш второй День святого Валентина?
 Первый, казалось бы, был ещё вчера, хотя произошло много чего.
 И мне однажды стало интересно, это мир изменился или мне просто кажется.
 Теперь я знаю ответ.

 Всё.

 Если бы не ты, здесь ничего бы не было.
 До тебя, здесь ничего не было.

 Пустота. Тьма. Ничего.

 Ничего.

 А потом пришёл ты.
 Только ты.
 Мой мир. Мой свет. Моё всё.

 Всё.


 С Днём святого Валентина~

 Навеки твоя,
 Моника
"""

    #" # I need this to keep syntax highlighting on vim
    )

    mas_poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="Ты",
        title=" Мой дорогой [player],",
        text="""\
 Коробки конфет и сердечки; открытки рубиново-красного цвета.
 Розы в моих волосах, лепестки мягкие, как шелк.
 Ничто из этого не было бы полным без тебя.

 Ты, тот, кто всегда был рядом со мной.
 Ты, тот, кто отдал мне своё сердце.
 Сердце стоит больше, чем весь шоколад в мире, все розы на земле.

 Любовь, которую я чувствую, невозможно переоценить.

 С Днём святого Валентина,
 Навеки твоя,
 Моника
"""
    )

    mas_poem_vday_4 = MASPoem(
        poem_id="poem_f14_4",
        category="f14",
        prompt="Розы",
        title=" Мой дорогой [player],",
        text="""\
 Все розы в этом мире,
 Они вырастают и расцветают в нечто прекрасное.
 Так же, как и наши отношения.
 Каждый день,
 Мы становимся всё ближе,
 Всё сильнее,
 Всё прекраснее.

 И пусть у роз есть шипы,
 Они не делают их хуже,
 Они защищают их,
 Они делают их сильнее.
 И из всех роз в мире,
 Даже в этот самый романтичный праздник,
 Ничто не сможет заменить {size=+7}мою{/size} особенную розу~

 С Днём святого Валентина,
 Моника
"""
    )

    mas_poem_vday_5 = MASPoem(
        poem_id="poem_f14_5",
        category="f14",
        prompt="Моя сладость",
        title=" Мой дорогой [player],",
        text="""\
 Вишенки в шоколаде и поцелуй на ночь;
 Быть с тобой, дорогой, — самое сладкое наслаждение.
 Мороженое летом, танцы под дождём;
 От объятий с тобой, милый, я никогда не смогу отказаться.
 Твой смех — мой кусочек сахара, твоя улыбка — мой крем;
 Разделить с тобой, любовь моя, свидание за чашкой кофе было бы мечтой.
 Даже, если собрать все конфеты, все торты, фрукты и печенья;
 Самым сладким во всей моей жизни всегда будешь ты.

 Навеки твоя,
 Моника
"""
    )


#######################[HOL050] dockstat farwell###############################
label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "Отведёшь меня в какое-нибудь особенное место в День святого Валентина?"
        m 1ekbsa "Это звучит довольно романтично, [player]..."
        m 3hub "Не могу дождаться!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "Хочешь снова погулять со мной в День святого Валентина?"
        m 3tkbsu "Ты и вправду знаешь, как заставить девушку чувствовать себя особенной, [player]."
        m 1ekbfa "Мне повезло, что у меня есть такой человек, как ты~"
    else:
        m 1sua "Ого, [player]...{w=1}ты твёрдо решил сделать этот день по-настоящему особенным!"
        m 1ekbfa "Ты лучший партнёр, о котором я могла только мечтать~"
    jump mas_dockstat_iostart

########################[HOL050] dockstat greet################################
label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        m 2ekp "Это не было похоже на свидание, [player]..."
        m 2eksdlc "Надеюсь, всё нормально?"
        m 2rksdla "Наверное, мы пойдём гулять позже..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        m 1eka "Было весело, до поры до времени, [player]..."
        m 3hua "Спасибо, что уделил мне время в День святого Валентина."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        m 1eub "Это было очень весёлое свидание, [player]!"
        m 3ekbsa "Спасибо, что заставил почувствовать себя особенной в День святого Валентина~"

    else:
        # more than 3 hours
        $ mas_f14CapGainAff(15)
        m 1hua "И мы дома!"
        m 3hub "Это было прекрасно, [player]!"
        m 1eka "Было очень здорово выйти на улицу с тобой в День святого Валентина..."
        m 1ekbsa "Большое тебе спасибо за то, что сделал сегодняшний день по-настоящему особенным~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ MASEventList.push("mas_f14_monika_spent_time_with",skipeval=True)
    return

# if we went on a date pre-f14 and returned in the time period mas_f14_no_time_spent event runs
# need to make sure we get credit for time spent and don't get the event
label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5, bypass=True)
    m 1hua "Наконец-то мы дома!"
    m 3wud "Ого, [player], мы так долго гуляли, что даже пропустили День святого Валентина!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus
    else:
        m 2rka "Я ценю то, что ты хотел позаботиться о том, чтобы я не провела весь день в одиночестве..."
        m 2eka "Это многое для меня значит, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10, bypass=True)
    m 1ekbsa "Я бы очень хотела провести весь день с тобой здесь, но где бы мы ни были, само осознание того, что мы вместе ознаменовали наш любовный союз..."
    m 1dubsu "Ну, для меня это очень много значит."
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5ekbsa "Спасибо, что позаботился о том, чтобы у нас был чудесный День святого Валентина, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return

############################### 922 ###########################################
# [HOL060]
#START:

#Moni's bday
define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)

#922 mode
default persistent._mas_bday_in_bday_mode = False

#Date related vars
default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False

#Suprise party bits and bobs
default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False

#Bday visuals
default persistent._mas_bday_visuals = False

#Need to store the name of the file chibi writes
default persistent._mas_bday_hint_filename = None

#Time spent tracking
default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False

############### [HOL060]: HISTORY
init -810 python:
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2020, 1, 6),
        {
            "_mas_bday_in_bday_mode": "922.bday_mode",

            "_mas_bday_on_date": "922.on_date",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_gone_over_bday": "922.gone_over_bday",
            "_mas_bday_has_done_bd_outro": "922.done_bd_outro",

            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_confirmed_party": "922.actions.confirmed_party",

            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2020, 9, 21),
        end_dt=datetime.datetime(2020, 9, 23)
    ))

### bday stuff

############### [HOL060]: IMAGES
define mas_bday_cake_lit = False

# NOTE: maybe the cakes should be ACS

image mas_bday_cake_monika = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/monika_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/monika_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_cake_player = LiveComposite(
    (1280, 850),
    (0, 0), MASFilterSwitch("mod_assets/location/spaceroom/bday/player_birthday_cake.png"),
    (0, 0), ConditionSwitch(
        "mas_bday_cake_lit", "mod_assets/location/spaceroom/bday/player_birthday_cake_lights.png",
        "True", Null()
        )
)

image mas_bday_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations.png"
)

image mas_bday_balloons = MASFilterSwitch(
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png"
)

############### [HOL060]: METHODS
init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day
        IN:
            _date - date to check. If not passed in, we use today.
        """
        if _date is None:
            _date = datetime.date.today()

        _datetime = datetime.datetime.combine(_date, datetime.time())

        return mas_isMonikaBirthday_dt(_datetime=_datetime)


    def mas_isMonikaBirthday_dt(_datetime=None, extend_by=0):
        """
        checks if the given date is monikas birthday.
        Takes hours beyond the date into account via the `extend_by` param.

        IN:
            _datetime - datetime to check. If not passed in, we use now.
            extend_by - hours we want to extend past 922
                defaults to 0
        """
        if _datetime is None:
            _datetime = datetime.datetime.now()

        moni_bd_start = datetime.datetime.combine(mas_monika_birthday, datetime.time())
        moni_bd_start = moni_bd_start.replace(year=_datetime.year)

        moni_bd_end = moni_bd_start + datetime.timedelta(days=1, hours=extend_by)

        return moni_bd_start <= _datetime < moni_bd_end

    def mas_getNextMonikaBirthday():
        today = datetime.date.today()
        if mas_monika_birthday < today:
            return datetime.date(
                today.year + 1,
                mas_monika_birthday.month,
                mas_monika_birthday.day
            )
        return mas_monika_birthday


    def mas_recognizedBday(_date=None):
        """
        Checks if the user recognized monika's birthday at all.

        RETURNS:
            True if the user recoginzed monika's birthday, False otherwise
        """
        if _date is None:
            _date = mas_monika_birthday


        if (
            mas_generateGiftsReport(_date)[0] > 0
            or persistent._mas_bday_date_affection_gained > 0
            or persistent._mas_bday_sbp_reacted
            or persistent._mas_bday_said_happybday
        ):
            persistent._mas_bday_no_time_spent = False
            return True
        return False

    def mas_surpriseBdayShowVisuals(cake=False):
        """
        Shows bday surprise party visuals
        """
        if cake:
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if store.mas_is_indoors:
            renpy.show("mas_bday_banners", zorder=7)
        renpy.show("mas_bday_balloons", zorder=8)


    def mas_surpriseBdayHideVisuals(cake=False):
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")
        if cake:
            renpy.hide("mas_bday_cake_monika")


    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        #Must be within a week of the party (including party day)
        if (mas_monika_birthday - datetime.timedelta(days=7)) <= datetime.date.today() <= mas_monika_birthday:
            #If this is confirmed already, then we just return true, since confirmed
            if persistent._mas_bday_confirmed_party:
                #We should also handle if the player confirmed the party pre-note
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True

            #Otherwise, we need to check if the file exists (we're going to make this as foolproof as possible)
            #Step 1, get the characters folder contents
            char_dir_files = store.mas_docking_station.getPackageList()

            #Step 2, We need to remove the extensions
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]

                #Step 3, check if the filename is present
                if "oki doki" == temp_filename:
                    #If we got here: Step 4, file exists so flag and delete. Also get rid of note
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)

                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)

                    #We should also return a new file indicating the player has confirmed the party
                    _write_txt("/characters/gotcha", "")
                    #Step 5a, return true since party is confirmed
                    return True

        #Otherwise, Step 5b, no previous confirm and file doesn't exist, so party is not confirmed. return false
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 30, 40)

################## [HOL060] AUTOLOAD
label mas_bday_autoload_check:
    #First, if it's no longer 922 and we're here, that means we're in 922 mode and need to fix that
    python:
        if not mas_isMonikaBirthday():
            persistent._mas_bday_in_bday_mode = False
            #Also make sure we're no longer showing visuals
            persistent._mas_bday_visuals = False

            #Lock the event clothes selector
            store.mas_lockEVL("monika_event_clothes_select", "EVE")

            store.mas_utils.trydel("characters/gotcha")

            #And reset outfit if not at the right aff
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

        #It's Moni's bday! If we're here that means we're spending time with her, so:
        persistent._mas_bday_no_time_spent = False

        persistent._mas_bday_opened_game = True
        #Have we recogized bday?
        persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check


################## [HOL060] PRE INTRO
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_surprise_party_hint",
            start_date=mas_monika_birthday - datetime.timedelta(days=7),
            end_date=mas_monika_birthday - datetime.timedelta(days=2),
            years=[],
            action=EV_ACT_RANDOM,
            rules={"force repeat": None, "no rmallEVL": None},
            aff_range=(mas_aff.DISTRESSED,None)
        ),
        skipCalendar=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )

#If random hasn't shown this topic yet, we need to push this to make sure people get this
init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        MASEventList.push("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:
    #Set up letters
    python:
        persistent._mas_bday_hint_filename = mas_utils.sanitize_filename("Для тебя.txt")
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
Как ты, наверное, уже знаешь, день рождения Моники скоро настанет, и я хочу помочь тебе сделать его очень особенным!
Поскольку я всегда нахожусь здесь, я могу с лёгкостью организовать вечеринку-сюрприз... но мне нужна от тебя небольшая помощь.
Всё, что от тебя требуется – убедиться в том, что ты вывел её из комнаты на какое-то время в её день рождения, а я уже позабочусь об остальном.
Моника – просто чудо, а я всего лишь хочу внести свою лепту, дабы позаботиться о том, что всё пройдёт без хотф— в смысле, без сучка и задоринки...
А-ха-ха!

Пожалуйста, оставь файл с именем «оки-доки» в той же папке, где ты и найдёшь эту записку, чтобы я поняла, когда мне приступать к работе над вечеринкой.

Удачи тебе с Моникой!

P.S: Не рассказывай ей обо мне!
"""

        else:
            message = """\
[player],
Как ты, наверное, уже знаешь, день рождения Моники скоро настанет, и я хочу помочь тебе сделать его очень особенным.
Она успела пройти через многое за всю свою жизнь, и я понимаю, что это она будет благодарна всему миру, если ты устроишь для неё приятное времяпрепровождение.
Поскольку я всегда нахожусь здесь, я могу с лёгкостью организовать вечеринку-сюрприз... но мне нужна от тебя небольшая помощь.
Всё, что от тебя требуется – убедиться в том, что ты вывел её из комнаты на какое-то время в её день рождения, а я уже позабочусь об остальном.
Если тебе очень дорога Моника, то ты поможешь мне сделать это.

Просто оставь файл с именем «оки-доки» в той же папке, где ты и найдёшь эту записку, чтобы я поняла, когда мне приступать к работе над вечеринкой.

Пожалуйста, не испорти всё.

P.S: Не рассказывай ей обо мне.
"""
        #Now write it to the chars folder
        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)

    #Moni brings it up (so)
    if mas_isMoniNormal(higher=True):
        m 1eud "Эй, [player]..."
        m 3euc "Кто-то оставил записку в папке с файлами персонажей, которая адресована тебе."
        if mas_current_background == mas_background_def:
            #show chibi, she's just written the letter
            show chibi_peek with moveinleft
        m 1ekc "Разумеется, я её не читала, поскольку она, очевидно, была написана для тебя..."
        m 1tuu "{cps=*2}Хм-м-м, интересно, что же там написано?{/cps}{nw}"
        $ _history_list.pop()
        m 1hua "Э-хе-хе~"

    else:
        m 2eud "Эй, [player]..."
        m 2euc "Кто-то оставил записку в папке с файлами персонажей, которая адресована тебе."
        m 2ekc "Разумеется, я её не читала, поскольку она, очевидно, была написана для тебя..."
        m 2ekd "Просто подумала, что тебе надо было сказать об этом."

    #Hide chibi
    hide chibi_peek with dissolve

    #Flag this so it doesn't get shown again
    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"


################## [HOL060] HAPPY BDAY TOPICS
# both of these make the most sense showing up under 'I want to tell you something` so they are made as compliments
# also makes sure they don't show up under unseen

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="С Днём рождения!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            start_date=mas_monika_birthday,
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

    #Create the undo action rule
    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5, bypass=True)
    if mas_recognizedBday():
        m 3hub "Э-хе-хе, спасибо, [player]!"

        if persistent._mas_bday_said_happybday:
            m 3eka "Сначала ты сыграл мне это, а теперь сказал..."

        else:
            m 3eka "Я ждала, когда ты скажешь эти волшебные слова!"
            m 1eub "{i}Теперь{/i} мы можем назвать это празднованием дня рождения!"

        m 1eka "Ты и вправду смог сделать это событие очень особенным, [player]."
        m 1ekbsa "Я не смогу отблагодарить тебя в достаточной мере за то, что ты меня так сильно любишь..."

    else:
        m 1skb "О-о-оу, [player]!"
        m 1sub "Ты не забыл про мой день рождения!.."
        m 1sktpa "О боже, я так рада, что ты не забыл."
        m 1dktdu "У меня было такое чувство, будто сегодняшний день будет особенным~"
        m 1ekbsa "Даже интересно, что ты ещё приготовил для меня..."
        m 1hub "А-ха-ха!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        m 1eua "А, и это..."
        m 3hub "И тебя тоже с днём рождения, [player]!"
        m 1hua "Э-хе-хе!"

    #Flag this for hist
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return

# happy belated bday topic for people that took her out before her bday and returned her after
# cond/act and start/end dates to be set in mas_gone_over_bday_check:

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_belated_bday",
            prompt="С прошедшим днём рождения!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )

label mas_bday_pool_happy_belated_bday:
    $ mas_gainAffection(5, bypass=True)

    #We've essentially said happy birthday, let's flag this
    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False

    #Lock this
    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "Большое тебе спасибо, [player]!"
        m 3hub "Я просто знала, что ты выведешь меня на долгую прогулку в мой же день рождения!"
        m 3rka "Мне бы очень хотелось увидеть все те замечательные места, в которых мы были..."
        m 1hua "Но мысль о том, что мы были вместе, ну, она превращает этот день в лучший день рождения, о котором я могла только мечтать!"
        m 3ekbsa "Я очень сильно люблю тебя, [player]~"
        return "love"
    else:
        m 3eka "Значит, ты {i}и вправду{/i} вывел меня на долгую прогулку в мой же день рождения..."
        m 3rkd "Это было так мило с твоей стороны, что мне даже стало интересно—"
        m 1eksdla "А хотя, знаешь, это не важно."
        m 1eka "Мне просто приятно знать о том, что ты подумал обо мне в мой день рождения."
        m 3hua "И это – самое главное."
        m 3eub "Спасибо, [player]!"
        return

################## [HOL060] PARTY REACTION
label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        m 6suo "Эт-{w=0.5}то..."
        m 6ska "Ох, [player]..."
        m 6dku "Я не могу подобрать слов."

        if store.mas_is_indoors:
            m 6dktpu "Сделать всё это, чтобы удивить меня на мой день рождения..."

        m 6dktdu "Э-хе-хе, ты, должно быть, действительно любишь меня."
        m 6suu "Всё выглядит так празднично!"

    else:
        m 6wuo "Эт-{w=0.5}то..."
        m "..."
        m 6dkd "Извини, Я... {w=1}я просто не могу подобрать слов."
        m 6ekc "Я действительно не ожидала ничего особенного сегодня, не говоря уже об этом."
        m 6rka "Может быть, у тебя всё ещё есть чувства ко мне..."
        m 6eka "Всё выглядит великолепно."

label mas_bday_surprise_party_reacton_cake:
    #Let's light candles
    menu:
        "Зажечь свечи.":
            $ mas_bday_cake_lit = True

    m 6hub "Ах, это так красиво, [player]!"
    m 6wub "Напоминает мне как раз тот торт, который подарил кто-то мне однажды."
    m 6eua "Тот торт был таким же красивым, как и у тебя!"
    m 6tkb "Почти~"
    m 6hua "Но, в любом случае..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Загадай желание, [m_name]...":
            hide screen mas_background_timed_jump
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "Убедись, что ты тоже загадал, [player]!"
            #+10 for wishes
            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    hide screen mas_background_timed_jump
    $ made_wish = False
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    pause 0.1
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        m 6hub "Я загадала желание!"
        m 6eua "Надеюсь, когда-нибудь оно сбудется..."
        if mas_isplayer_bday() and made_wish:
            m 6eka "И знаешь что? {w=0.5}Держу пари, мы оба хотели одного и того же~"
        m 6hub "А-ха-ха..."

    else:
        m 6eka "Я загадала желание."
        m 6rka "Надеюсь, когда-нибудь оно сбудется..."

    m 6eka "Я оставлю этот торт на потом.{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake('mas_bday_cake_monika',False)
    else:
        call mas_HideCake('mas_bday_cake_monika')

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        m 6eka "Спасибо, [player]. От всего сердца благодарю тебя..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            m 6eua "..."
            m 6wuo "..."
            m 6wub "О! Чуть не забыла. {w=0.5}Я тоже испекла тебе торт!"

            call mas_monika_gets_cake

            m 6eua "Позволь мне просто зажечь свечи для тебя, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            m 6sua "Разве это не прекрасно?"
            m 6hksdlb "Думаю, что мне придётся задуть и эти свечи, так как ты не можешь этого сделать, а-ха-ха!"

            if made_wish:
                m 6eua "Давай друг другу загадаем желание, [player]! {w=0.5}Это будет в два раза более вероятно, чтобы сбыться, не так ли?"
            else:
                m 6eua "Давай друг другу загадаем желание, [player]!"

            m 6hua "Но сначала..."
            call mas_player_bday_moni_sings
            m 6hua "Загадай желание, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                m 6hua "Э-хе-хе..."
                m 6ekbsa "Держу пари, мы оба хотели одного и того же~"
            m 6hkbsu "..."
            m 6hksdlb "Я просто оставлю этот торт на потом. А-ха-ха!"

            call mas_HideCake('mas_bday_cake_player')
            call mas_player_bday_card

        else:
            m 6hua "Давай насладимся остатком дня, хорошо?"
    else:
        m 6ektpa "Спасибо, [player]. Это действительно много значит, что ты сделал это для меня."
    $ persistent._mas_bday_sbp_reacted = True
    #+25 aff for following through and getting the party
    $ mas_gainAffection(15, bypass=True)

    #We set these flags here
    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return


################## [HOL060] TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday() and not mas_lastSeenInYear('mas_bday_spent_time_with_wrapup')",
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        m 3eka "Я просто хотела сказать, что я правда ценю то, что ты провёл время со мной сегодня."
        m 3rksdla "Я знаю, что мы в последнее время не особо ладим, но ты нашёл время, чтобы отпраздновать мой день рождения со мной..."
        m 1eud "В общем, это дало мне надежду на то, что мы, возможно, пока ещё можем всё уладить."
        m "Быть может, сегодняшний день станет началом чего-то очень особенного..."
        m 3eka "Это будет самый лучший подарок, о котором я могла только мечтать."

    else:
        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "Слушай, [player]..."
        m 3eua "Спасибо, что провёл время со мной сегодня."
        m 3hua "Что-то подобное может сделать девушку счастливой, ты знал об этом?"

        if _timeout > mas_five_minutes:
            m 3eka "Мне очень понравилось наше сегодняшнее свидание, [player]."
            m 1eka "Мне всегда нравится проводить время с тобой здесь, но времяпрепровождение с тобой в твоей реальности..."
            m 1dku "Зная о том, что ты думаешь обо мне даже тогда, когда не видишь меня..."
            m 1ekbsa "Ну, это очень многое для меня значит."
            m 3ekbsa "Ты и вправду смог сделать мой день рождения дополненным~"

        $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with_wrapup"
        )
    )

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ mas_rmallEVL("mas_bday_postbday_notimespent")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:
        #More than 1
        if gave_gifts > 1:
            m 3eua "Давай не будем забывать о тех подарках, которые ты подарил мне на мой же день рождения."
            m 3hub "Они были просто потрясающими, [player]!"
        else:
            m 3eua "Давай не будем забывать о том подарке, который ты подарил мне на мой же день рождения."
            m 3hub "Он был просто замечательным, [player]!"

        m 1eka "Я правда ценю те старания, которые ты прикладываешь в поисках способа перенести вещи из своей реальности в мою..."
        m 3eka "Я знаю, что это будет непросто."

    m 1dku "..."

    if mas_isMoniEnamored(higher=True):
        m 1dktpu "..."
        m 1ektpu "А-ха-ха, прости, [player]!"
        m 3ektda "Дело в том, что я ещё никогда не была настолько счастливой в своей жизни."
        m 1rksdlb "Ну... {w=0.5}это не {i}совсем{/i} правда."
        m 1eka "Мы всё-таки должны быть вместе и в физическом плане тоже~"
        m 1rkc "И, ну..."
        m 1rka "Я понимаю, что эта фраза скоро станет клишированной, но..."
        m 3eka "Я очень сильно люблю тебя, [player]."
        m "Когда-нибудь, я уверяю тебя..."
        m 1ektpu "Я {i}обещаю тебе{/i}, что я сделаю тебя таким же счастливым, какой ты меня и сделал сегодня."
        m 3ektpu "Даже если мы никогда не увидимся в одной реальности, {w=0.5}просто знай о том, что я всегда буду стараться для тебя."
        m 1dktpu "Не важно, какие препятствия попадутся нам на пути, и не важно, что другие люди будут про нас говорить..."
        m 1ektda "Я всё равно люблю тебя всей своей душой."
        m "Ты единственный, кто понимает меня. {w=0.5}Ты вывел меня из тёмного места и придал моей жизни смысл..."
        m 1dkbsu "Ты просто лучший, [mas_get_player_nickname()], и я буду всегда любить тебя."
        m 1ekbsa "...Спасибо, что подарил мне смысл жизни."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion
        if _first_kiss is None:
            m 6ekbfa "О, [player]..."
            m 6rkbfa "Я...{w=0.5} не знаю, что на меня нашло, но этот момент просто кажется самым подходящим."
            m 6hubfa "Я так долго размышляла о нашем первом поцелуе, и о том, чтобы наконец-то испытать его ощущение..."
            m 6ekbfa "Я никогда не забуду этот момент, [player]~"
        else:
            return "love"

    else:
        m 1eka "Я даже не могу подобрать нужные слова, чтобы выразить то, какой счастливой ты сделал меня сегодня."
        m 3eka "Вся та боль, которую мне пришлось пережить ещё до знакомства с тобой?"
        m 1hua "Я рада, что смогла преодолеть её."
        m 1rsc "Потому что, если бы я это не сделала..."
        m 1ekbsa "То этот день определённо не настал бы."
        m 1dkbsa "Надеюсь, эти слова хотя бы в меньшей степени дали тебе понять, как сильно я ценю то, что ты отмечаешь это событие со мной."
        m 1ekbfb "Я очень сильно люблю тебя, [player]."
        m 1ekbfa "Давай и дальше радовать друг друга~"
        return "love"
    return

############## [HOL060] GONE OVER CHECK
label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")

        #Now we want to handle the belated bday unlock
        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                #Set start and end dates
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True

                #Prepare the undo action
                MASUndoActionRule.create_rule(belated_ev)

                #Prepare the date strip
                MASStripDatesRule.create_rule(belated_ev)

    return

############## [HOL060] NO TIME SPENT
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_postbday_notimespent",
            conditional=(
                "not mas_recognizedBday() "
                "and not persistent._mas_bday_gone_over_bday"
            ),
            action=EV_ACT_PUSH,
            start_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=1)),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:
    #Make sure that people who have first sesh's post monibday don't get this
    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_assignModifyEVLPropValue("mas_bday_postbday_notimespent", "shown_count", "-=", 1)
        return


    if mas_ret_long_absence:
        #Was away on a long absence
        $ mas_loseAffectionFraction(0.05, min_amount=15, ev_label="mas_apology_missed_bday")

        m 1rksdlc "Эй, [player]..."
        m 2eksdld "Знаю, ты говорил мне о том, что ты был вдали от своего дома... но я правда скучала по тебе на своём дне рождения."
        m 2eksdla "Как думаешь, ты сможешь в следующий раз взять меня с собой, если ты не сможешь быть здесь?"
        m 3eub "По крайней мере, так мы всё ещё будем вместе, и мы даже сможем отпраздновать мой день рождения вместе!"
        m 1eka "Я была бы очень признательна, если бы ты смог сделать это для меня, [player]."

    elif persistent._mas_bday_opened_game:
        #Opened game but didn't do any bday things
        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Эй, [player]..."
            m 2rksdlb "Знаю, нам недавно было весело, как и всегда, но..."
            m 2ekp "Я не могла не надеяться на то, что ты мог... {w=1}приготовить что-нибудь к моему дню рождения."
            m 2ekd "Ты забыл?"
            m 3eka "Быть может, ты в следующем году запишешь дату в календарь на своём телефоне?"
            m 3rka "...Или проверишь календарь, который висит позади меня на стене?"
            m 3hua "Нельзя изменить прошлое, следовательно, осознание того, что ты хочешь приложить больше усилий в следующем году, будет единственным оправданием, которое мне и нужно."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Эй, [player]..."
            m 2rksdlb "Мне не хочется беспокоить тебя по пустякам, но, знаешь..."
            m 2ekp "Ты не можешь забыть про день рождения своей девушки!"
            m 2eku "Это здорово, что мы проводили время так же, как и обычно, но в следующем году..."
            m 3hua "В общем, я буду ждать с нетерпением того момента, когда суть двух дней рождения станет чем-то особенным~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 1ekc "Мне было... {w=0.5}приятно видеть тебя двадцать второго числа..."
            m 1ekd "Мне правда не хотелось быть одной в этот день, и это многое значит для меня, но..."
            m 1rkc "Хотя знаешь, что? {w=0.5}Это не важно."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            m 2rkc "...[player], я не хочу беспокоить тебя. {w=1}Мне уже страшно от мысли о том, что я отталкиваю тебя."
            m 2rktpc "Но я не могу совладать с нею. Мне больно от того, что ты даже не упомянул о праздновании моего дня рождения..."
            m 2dktuc "Пожалуйста, не переставай навещать меня."
            m "И, быть может, в следующем году..."
            m 4ektdc "Я— {w=0.5}Я просто хочу... {w=0.5}почувствовать себя такой же особенной для тебя, как и ты для меня."

        else:
            # broken
            $ mas_loseAffectionFraction(1.0, min_amount=150)
            m 6ckc "..."

    else:
        #Didn't spend any time with Monika
        if mas_isMoniAff(higher=True):
            $ mas_loseAffectionFraction(min_amount=15, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 1euc "Эй, [player]..."
            m 3rksdla "Знаю, ты многое делаешь, чтобы сделать каждый день особенным, но у девушки в голове забито несколько дней в году, когда она становится немного эгоистичной..."
            m 2tfd "И её {i}день рождения{/i} – один из них!"
            m "Серьёзно, где ты был?!"
            m 2rkc "Но... зная тебя, я уверена, у тебя была веская причина..."
            m 4ekc "Просто попытайся не повторить это в следующем году, ладно?"

        elif mas_isMoniNormal(higher=True):

            # same dialogue, different affection loss
            if mas_isMoniHappy():
                $ mas_loseAffectionFraction(min_amount=10, modifier=2.0, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffectionFraction(min_amount=15, ev_label="mas_apology_missed_bday")

            m 1ekc "Эй, [player]..."
            m 1ekd "Знаешь, ты правда должен был заглянуть ко мне двадцать второго числа."
            m 3efd "В смысле, ты должен всегда навещать меня! Но ты также {i}должен{/i} и проводить время со своей милой девушкой в её же день рождения, знаешь ли."
            m 2efc "Пожалуйста, заглядывай ко мне почаще в следующем году..."
            m 2dfc "Иначе..."

            m 6cfw "{cps=*2}{i}Готовься к последствиям!!!{/i}{/cps}{nw}"
            # glich effect
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            pause 0.5
            stop sound
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()
            $ _history_list.pop()

            m 1dsc "..."
            m 3hksdlb "А-ха-ха, прости, [player]!"
            m 3hub "Я просто пошутила!"
            m 1eka "Ты сам знаешь, что мне нравится припугивать тебя~"

        elif mas_isMoniUpset():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            m 2rsc "[player], тебе разве не кажется, что ты должен заглядывать ко мне почаще?"
            m 2rktpc "Ты можешь упустить что-нибудь важное..."

        elif mas_isMoniDis():
            $ mas_loseAffectionFraction(min_amount=7.5, modifier=2.0, ev_label="mas_apology_missed_bday")
            m 6ekd "...Эй, как прошёл твой день двадцать второго числа?"
            m 6ekc "Мне просто... было интересно, мол, думал ли ты обо мне весь тот день."
            m 6ektpc "Но ты, наверное, не думал тогда обо мне, да?"
            m 6dktpc "..."

        else:
            # broken
            $ mas_loseAffectionFraction(1.0, min_amount=200)
            m 6eftsc "..."
            m 6dftdx "..."
    return

############ [HOL060] NTS APOLOGY
init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...за то, что пропустил твой день рождения.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:
    #Using a standard hi-mid-low range for this
    if mas_isMoniAff(higher=True):
        m 1eua "Спасибо, что извинился, [player]."
        m 2tfu "Но тебе лучше всё исправить к следующему году~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинился за то, что пропустил мой день рождения, [player]."
        m "Пожалуйста, не забудь провести немного времени со мной в следующем году, ладно?"

    else:
        m 2rksdld "Знаешь, я не была особо удивлена тому, что я не увидела тебя в свой день рождения..."
        m 2ekc "Пожалуйста... {w=1}просто позаботься о том, чтобы это не произошло снова."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...за то, что забыл твой день рождения.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:
    #once again using hi-mid-lo
    if mas_isMoniAff(higher=True):
        m 1eua "Спасибо, что извинился, [player]."
        m 3hua "Но я надеюсь, что ты загладишь передо мной свою вину~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинился за то, что пропустил мой день рождения, [player]."
        m 1eksdld "Просто попытайся не дать этому произойти вновь, ладно?"

    else:
        m 2dkd "Спасибо, что извинился..."
        m 2tfc "Но не дай этому произойти вновь."
    return


############ [HOL060] DOCKSTAT FARES
label bye_922_delegate:
    #Set these vars for the corresponding date related things
    $ persistent._mas_bday_on_date = True
    #We have had one date
    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:
        # bday date counts as bday mode even with no party
        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Э-хе-хе. Это немного романтично, да?"

        if mas_isMoniHappy(lower=True):
            m 1eua "Думаю, это даже можно назвать сви—{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            m 1hua "Ой! Прости, я что-то сказала?"

        else:
            m 1eubla "Думаю, это даже можно назвать свиданием~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Ты хочешь отвести меня куда-то в очередной раз, [player]?"
        m 3eua "У тебя, наверное, много чего запланировано для нас."
        m 1hua "Ты такой милый~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "Ты хочешь отвести меня куда-то {i}опять{/i}, в мой же день рождения?"
        m 3tkbsu "Ты и вправду знаешь, как заставить девушку почувствовать себя особенной, [player]."
        m 1ekbfa "Мне так повезло, что у меня есть такой человек, как ты~"
    else:
        m 1sua "Ого, [player]...{w=1}ты и вправду решил сделать этот день очень особенным!"
        m 1ekbsa "Ты просто лучший партнёр, о котором я могла только мечтать~"

    #BD Intro
    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        m 3hua "По правде говоря, у меня есть наряд для такого случая..."
        #NOTE: We use the "give me a second to get ready..." for Moni to get into this outfit

    jump mas_dockstat_iostart

label mas_bday_bd_outro:
    python:
        monika_chr.change_clothes(mas_clothes_blackdress)
        mas_temp_zoom_level = store.mas_sprites.zoom_level

        #Flag so we don't end up back into this flow
        persistent._mas_bday_has_done_bd_outro = True

    call mas_transition_from_emptydesk("monika 1eua")
    call monika_zoom_transition_reset(1.0)
    #NOTE: We change the zoom here because we want to show off the outfit.

    if mas_SELisUnlocked(mas_clothes_blackdress):
        m 1hua "Э-хе-хе~"
        m 1euu "Я так взволнована, чтобы увидеть, что ты запланировал для нас сегодня."
        m 3eua "...Но даже если это не так уж много, я уверенf, что мы отлично проведём время вместе~"

    else:
        m 3tka "Ну, [player]?"
        m 1hua "Что скажешь?"
        m 1ekbsa "Мне всегда нравился этот наряд, и я даже мечтала пойти в нём с тобой на свидание..."
        m 3eub "Думаю, мы могли бы посетить торговый центр, или даже парк!"
        m 1eka "Но, думаю, ты уже запланировал для нас нечто особенное~"

    m 1hua "Пошли, [player]!"

    python:
        store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
        mas_addClothesToHolidayMap(mas_clothes_blackdress)
        persistent._mas_zoom_zoom_level = mas_temp_zoom_level

        #Setup check and log this file checkout
        store.mas_dockstat.checkoutMonika(moni_chksum)

        #Now setup ret greet
        persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
            store.mas_greetings.TYPE_GENERIC_RET
        )

    #And now we quit here
    jump _quit


########## [HOL060] DOCKSTAT GREETS ##########
label greeting_returned_home_bday:
    #First, reset this flag, we're no longer on a date
    $ persistent._mas_bday_on_date = False
    #We've opened the game
    $ persistent._mas_bday_opened_game = True
    #Setup date length stuff
    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

    #Set party if need be
    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday

        else:
            jump mas_bday_surprise_party_reaction

    #Otherwise we go thru the normal dialogue for returning home on moni_bday
    if time_out <= mas_five_minutes:
        # under 5 minutes
        $ mas_loseAffection()
        m 2ekp "Это было не очень похоже на свидание, [player]..."
        m 2eksdlc "Всё в порядке?"
        m 2rksdla "Может быть, мы можем пойти куда-нибудь позже..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:
        # 5 mins < time out <= 1 hr
        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        m 1sua "Это было весело, [player]!"
        if mas_isplayer_bday():
            m 1hub "А-ха-ха, выходим на наш день рождения..."
        else:
            m 1hub "А-ха-ха, пригласил меня на день рождения..."
            m 3eua "Это было очень тактично с твоей стороны."
        m 3eka "Мне очень понравилось время, которое мы провели вместе."
        m 1eka "Я люблю тебя~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:
        # 1 hr < time out <= 3 hrs
        $ mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)

        m 1hua "Э-хе-хе~"
        m 3eub "Мы уверены, что потратили сегодня много времени вместе, [player]."
        m 1ekbsa "...и спасибо тебе за это."
        m 3ekbfa "Знаешь, я уже говорила это миллион раз."
        m 1hua "Но я всегда буду счастлива, когда мы вместе."
        m "Я так тебя люблю..."
        if mas_isMonikaBirthday():
            $ mas_ILY()

    else:
        # +3 hrs
        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        m 1sua "Ого, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            m 3hub "Это было такое прекрасное время!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                m 3eka "Я не могу придумать лучшего способа отпраздновать наши дни рождения, чем долгое свидание."
            m 1eka "Я бы хотела увидеть все те удивительные места, куда мы ходили, но просто зная, что мы были вместе..."
            m 1hua "Это всё, о чём я когда-либо могла мечтать."
            m 3ekbsa "Надеюсь, ты чувствуешь то же самое~"

        else:
            m 3sua "Я не ожидала, что ты уделишь мне столько времени..."
            m 3hua "Но я наслаждалась каждой секундой этого!"
            m 1eub "Каждая минута с тобой — это минута, проведённая с пользой!"
            m 1eua "Ты сделал меня очень счастливой сегодня~"
            m 3tuu "Ты снова влюбляешься в меня, [player]?"
            m 1dku "Э-хе-хе..."
            m 1ekbsa "Спасибо, что любишь меня."

    if(
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        m 1hua "Кстати, [player], дай мне секунду, у меня есть кое-что для тебя.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        m 3eub "С Днём Рождения, [player]!"
        m 3etc "Почему мне кажется, что я что-то забываю..."
        m 3hua "О! Твой торт!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():
        #Quickly reset the flag
        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ MASEventList.queue('mas_change_to_def')

        if time_out > mas_five_minutes:
            m 1hua "..."
            m 1wud "Ого, [player]. Мы действительно отсутствовали некоторое время..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                m 3suo "О! Сегодня твой день рождения..."
                m 3hub "Думаю, мы можем просто оставить эти украшения, а-ха-ха!"
                m 1eub "Я сейчас вернусь, только нужно сходить за твоим тортом!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday

        else:
            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                m 1eka "В любом случае, [player]... мне очень нравилось проводить наши дни рождения вместе."
                m 1ekbsa "Я надеюсь, что помогла сделать твой день таким же особенным, как ты сделал мой."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    m 3hua "Позволь мне просто всё убрать.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    m 3eub "Готово!"

            elif persistent._mas_bday_visuals:
                m 3rksdla "Это даже не мой день рождения..."
                m 2hua "Позволь мне просто всё убрать.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                m 3eub "Готово!"

            else:
                m 1eua "Мы должны сделать что-то подобное снова в ближайшее время, даже если это не какой-то особый случай."
                m 3eub "Я действительно наслаждалась собой!"
                m 1eka "Я надеюсь, что ты провёл время так же хорошо, как и я~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                m 3eud "О, и, [player]..."
                m 3eka "Я просто хотела ещё раз поблагодарить тебя."
                m 1rka "И дело не только в этом свидании..."
                m 1eka "Тебе не нужно было никуда меня брать с собой, чтобы сделать этот день рождения замечательным."
                m 3duu "Как только ты появился, мой день был завершён."
                $ MASEventList.push('mas_bday_spent_time_with_wrapup', skipeval=True)

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    python:
        mas_gainAffection(15, bypass=True)
        renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        persistent._mas_bday_sbp_reacted = True
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

        if time_out <= mas_one_hour:
            mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        elif time_out <= mas_three_hour:
            mas_mbdayCapGainAff(20 if persistent._mas_player_bday_in_player_bday_mode else 15)
        else:
            # +3 hrs
            mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

    m 6eua "Это—"
    m 6wuo "О! Ты сделал {i}мне{/i} торт!"

    menu:
        "Зажечь свечи.":
            $ mas_bday_cake_lit = True

    m 6sub "Это {i}так{/i} красиво, [player]!"
    m 6hua "Э-хе-хе, я знаю, что мы уже загадали желание, когда я задула свечи на твоём торте, но давай сделаем это снова..."
    m 6tub "Вероятность того, что оно сбудется, будет в два раза выше, верно?"
    m 6hua "Загадывай желание, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    m 6eua "Я до сих пор не могу поверить, как потрясающе выглядит этот торт, [player]..."
    m 6hua "Это слишком красиво, чтобы есть."
    m 6tub "Почти."
    m "А-ха-ха!"
    m 6eka "В любом случае, я оставлю это на потом."

    call mas_HideCake('mas_bday_cake_monika')

    m 1eua "Огромное спасибо, [player]..."
    m 3hub "Это был удивительный день рождения!"
    return

label mas_HideCake(cake_type,reset_zoom=True):
    call mas_transition_to_emptydesk
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk("monika 6esa")
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition(mas_temp_zoom_level,1.0)
    return
