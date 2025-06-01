# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="tw4449",
        name="Комната с видом на сад",
        description="Эта надстройка добавляет минималистичный набор мебели в обычную комнату для вас с Моникой.",
        version="1.0.3"
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Custom Room Garden View",
            user_name="tw4449-s-MAS-Submods",
            repository_name="Garden-View",
            update_dir="",
            attachment_id=None
        )

init 20 python in tw_room_utils:
    import store

    #Map int value to season
    IND_SEASON_MAP = {
        1: "spring",
        2: "summer",
        3: "fall",
        4: "winter"
    }

    #Room folders for each of the seasonal groups (weather masks)
    ROOM_FOLDERS = [
        "spring",
        "summer",
        "fall",
        "winter"
    ]

    #Weather types we pull from
    ROOM_FLT_BGS = [
        "def",
        "def-ss",
        "def-n",
        "overcast",
        "overcast-ss",
        "overcast-n",
        "rain-ss",
        "snow-ss"
    ]

    #Dict of room maps
    ROOM_IMG_MAPS = dict()

    #Plug into the prog points for seasonal changes NOTE: Requires MAS 0.12.4
    @store.mas_submod_utils.functionplugin("pp_spring", ["spring"])
    @store.mas_submod_utils.functionplugin("pp_summer", ["summer"])
    @store.mas_submod_utils.functionplugin("pp_fall", ["fall"])
    @store.mas_submod_utils.functionplugin("pp_winter", ["winter"])
    def _setSeasonalBg(new_season):
        """
        Runs transitional code to transfer the current bg to another season

        IN:
            new_season - string season name representing the season we're changing to
        """
        #Only apply if currently in garden_view
        if store.mas_current_background == store.submod_background_garden_view:
            weath_img_tag_base = "garden_view_{0}_".format(new_season)

            #Set background images
            store.mas_weather_def.img_tag = weath_img_tag_base + "def_weather_fb"
            store.mas_weather_def.ani_img_tag = weath_img_tag_base + "def_weather"

            store.mas_weather_overcast.img_tag = weath_img_tag_base + "overcast_weather_fb"
            store.mas_weather_overcast.ani_img_tag = weath_img_tag_base + "overcast_weather"

            store.mas_weather_rain.img_tag = weath_img_tag_base + "rain_weather_fb"
            store.mas_weather_rain.ani_img_tag = weath_img_tag_base + "rain_weather"

            store.mas_weather_thunder.img_tag = weath_img_tag_base + "rain_weather_fb"
            store.mas_weather_thunder.ani_img_tag = weath_img_tag_base + "rain_weather"

            store.mas_weather_snow.img_tag = weath_img_tag_base + "snow_weather_fb"
            store.mas_weather_snow.ani_img_tag = weath_img_tag_base + "snow_weather"

            store.mas_current_background.image_map = ROOM_IMG_MAPS[new_season]

            #Finally, request a dissolve all to update everything
            store.mas_idle_mailbox.send_dissolve_all()

    def initSeasonalBg():
        """
        Runs init code for the current season to set the appropriate bg and weather masks
        """
        _setSeasonalBg(IND_SEASON_MAP.get(store.mas_seasons._currentSeason()))

    def _initRoomBGMaps():
        """
        Runs init code to setup images related to the room bg
        """
        global ROOM_IMG_MAPS

        for room_folder in ROOM_FOLDERS:
            for room_bg_ig in ROOM_FLT_BGS:
                img_tag = "garden_view_{0}_{1}".format(room_folder, room_bg_ig).replace('-', '_')
                renpy.display.image.images[(img_tag,)] = store.Image(
                    "mod_assets/location/garden_view/{0}/{1}.png".format(room_folder, room_bg_ig)
                )

            #check if we have a redirect
            img_tag_base = "garden_view_{0}_".format(room_folder).replace('-', '_')

            #Now swap bg images
            ROOM_IMG_MAPS[room_folder] = store.MASFilterWeatherMap(
                day=store.MASWeatherMap({
                    store.mas_weather.PRECIP_TYPE_DEF: img_tag_base + "def",
                    store.mas_weather.PRECIP_TYPE_RAIN: img_tag_base + "overcast",
                    store.mas_weather.PRECIP_TYPE_OVERCAST: img_tag_base + "overcast",
                    store.mas_weather.PRECIP_TYPE_SNOW: img_tag_base + "overcast",
                }),
                night=store.MASWeatherMap({
                    store.mas_weather.PRECIP_TYPE_DEF: img_tag_base + "def_n",
                    store.mas_weather.PRECIP_TYPE_RAIN: img_tag_base + "overcast_n",
                    store.mas_weather.PRECIP_TYPE_OVERCAST: img_tag_base + "overcast_n",
                    store.mas_weather.PRECIP_TYPE_SNOW: img_tag_base + "overcast_n",
                }),
                sunset=store.MASWeatherMap({
                    store.mas_weather.PRECIP_TYPE_DEF: img_tag_base + "def_ss",
                    store.mas_weather.PRECIP_TYPE_RAIN: img_tag_base + "rain_ss",
                    store.mas_weather.PRECIP_TYPE_OVERCAST: img_tag_base + "overcast_ss",
                    store.mas_weather.PRECIP_TYPE_SNOW: img_tag_base + "snow_ss",
                })
            )

    def _initWeatherBGMaps():
        """
        Runs init code to generate images for the weather
        """
        
        animated_weather = dict()
        static_weather = dict()

        #Iter over our precip types so we can init weather
        for weather in store.mas_weather.PRECIP_TYPES:
            for season in IND_SEASON_MAP.values():

                #Build FPs for both the movie sprites and the fallback image sprites
                movie_fp = "mod_assets/location/garden_view/zz_window/{0}/{1}".format(season, weather)
                fallback_fp = "mod_assets/location/garden_view/zz_window/{0}/fallback/{1}".format(season, weather)

                #Sunset is a special case exclusive to def/snow
                if weather in ("snow", "def"):
                    animated_weather.update({
                        "sunset": store.Movie(play=movie_fp + "-ss.webm", mask=None)
                    })
                    static_weather.update({
                        "sunset": store.Image(fallback_fp + "-ss.png")
                    })
                else:
                    animated_weather.update({
                        "sunset": store.Movie(play=movie_fp + ".webm", mask=None)
                    })
                    static_weather.update({
                        "sunset": store.Image(fallback_fp + ".png")
                    })
                
                #General day/night should be applied to all
                animated_weather.update({
                    "day": store.Movie(play=movie_fp + ".webm", mask=None),
                    "night": store.Movie(play=movie_fp + "-n.webm", mask=None)
                })
                static_weather.update({
                    "day": store.Image(fallback_fp + ".png"),
                    "night": store.Image(fallback_fp + "-n.png")
                })

                #Register images
                renpy.display.image.images[("garden_view_{0}_{1}_weather".format(season, weather),)] = store.MASFallbackFilterDisplayable(**animated_weather)
                renpy.display.image.images[("garden_view_{0}_{1}_weather_fb".format(season, weather),)] = store.MASFallbackFilterDisplayable(**static_weather)

    _initRoomBGMaps()
    _initWeatherBGMaps()

image garden_view_o31_deco = ConditionSwitch(
    "mas_current_background.isFltDay()", "mod_assets/location/garden_view/deco/o31/deco.png",
    "True", "mod_assets/location/garden_view/deco/o31/deco-n.png"
)

image garden_view_d25_deco = ConditionSwitch(
    "mas_current_background.isFltDay()", "mod_assets/location/garden_view/deco/d25/deco.png",
    "True", "mod_assets/location/garden_view/deco/d25/deco-n.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_o31_wall_bats",
        submod_background_garden_view.background_id,
        MASAdvancedDecoFrame(zorder=5),
        replace_tag="garden_view_o31_deco"
    )

    MASImageTagDecoDefinition.register_img(
        "mas_d25_tree",
        submod_background_garden_view.background_id,
        MASAdvancedDecoFrame(zorder=5),
        replace_tag="garden_view_d25_deco"
    )

init 30 python:
    submod_background_garden_view = MASFilterableBackground(
        # ID
        "submod_background_garden_view",
        "Комната с видом на сад.",

        # mapping of filters to MASWeatherMaps
        image_map=tw_room_utils.ROOM_IMG_MAPS[tw_room_utils.IND_SEASON_MAP[store.mas_seasons._currentSeason()]],

        filter_man=MASBackgroundFilterManager(
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            ),
            MASBackgroundFilterChunk(
                True,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_DAY,
                    60
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
            ),
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            )
        ),

        disable_progressive=False,
        hide_masks=False,
        hide_calendar=True,
        unlocked=True,
        entry_pp=store.mas_background._garden_view_room_entry,
        exit_pp=store.mas_background._garden_view_room_exit,
    )

    #The dynamic nature of this bg doesn't like the way the filtermap is handled, so we need to populate the filtermanager properly
    submod_background_garden_view._flt_man._day_filters = {"sunset": None, "day": None}
    submod_background_garden_view._flt_man._night_filters = {"night": None}

init -2 python in mas_background:
    def _garden_view_room_entry(_old, **kwargs):
        """
        Entry programming point for garden_view background

        NOTE: ANYTHING IN THE `_old is None`
        """
        if kwargs.get("startup"):
            pass

        elif not store.mas_inEVL("submod_garden_view_switch_dlg"):
            store.pushEvent("submod_garden_view_switch_dlg")

        store.tw_room_utils.initSeasonalBg()


    def _garden_view_room_exit(_new, **kwargs):
        """
        Exit programming point for garden_view background
        """
        #Lock islands greet to be sure
        store.mas_lockEVL("mas_monika_islands", "EVE")

        if _new == store.mas_background_def:
            store.pushEvent("return_switch_dlg")

        #Reset background images
        store.mas_weather_def.img_tag = "def_weather_fb"
        store.mas_weather_def.ani_img_tag = "def_weather"

        store.mas_weather_overcast.img_tag = "overcast_weather_fb"
        store.mas_weather_overcast.ani_img_tag = "overcast_weather"

        store.mas_weather_rain.img_tag = "rain_weather_fb"
        store.mas_weather_rain.ani_img_tag = "rain_weather"

        store.mas_weather_thunder.img_tag = "rain_weather_fb"
        store.mas_weather_thunder.ani_img_tag = "rain_weather"

        store.mas_weather_snow.img_tag = "snow_weather_fb"
        store.mas_weather_snow.ani_img_tag = "snow_weather"

###START: Topics
#THIS ONE RUNS ON CHANGE
label submod_garden_view_switch_dlg:
    python:
        _exp, switch_quip = renpy.random.choice([
            ("1hua", "Я просто обожаю этот вид~"),
            ("1eua", "Разве ты не любишь наш двор, [player]?"),
            ("5rsu", "Завтра надо подышать свежим воздухом..."),
        ])

        renpy.show("monika " + _exp)
        renpy.say(m, switch_quip)

    return

###START: Topics
#THIS ONE RUNS ON CHANGE
label return_switch_dlg:
    python:
        switch_quip = renpy.substitute(renpy.random.choice([
            "Только мы вдвоём~",
            "Уже соскучился по классическому виду?",
            "Навевает воспоминания...",
        ]))

    m 1hua "[switch_quip]"

    return

#THIS ONE RUNS ON INSTALL
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="bg_room_installed_low_affection",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, mas_aff.AFFECTIONATE)
        )
    )

label bg_room_installed_low_affection:
    python:
        #Check how many tw mods we have installed
        tw_bg_count = len(filter(lambda x: "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        spacerooms_installed = len(filter(lambda x: "furnished spaceroom" in x.name.lower() and "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        had_backgrounds_before = (mas_background.getUnlockedBGCount() - tw_bg_count) > 1

    if spacerooms_installed:
        m 1wud "А?{w=0.5} [player], {w=0.2} ты добавил новые файлы в игру?"
        m 1wua "Похоже на... {w=0.5}{nw}"
        extend 1sub "новую мебель!"
        m 1eku "[player], ты сделал это для меня? {w=0.5}Ты такой милый, ты знал об этом?"

    if tw_bg_count - spacerooms_installed > 0:
        $ too = "ещё " if spacerooms_installed else ""
        $ rooms = "новые комнаты" if tw_bg_count - spacerooms_installed > 1 else "новую комнату"
        m 1wud "А?{w=0.5} [player],{w=0.2} что это?"
        m 1wua "Неужели ты... {nw}"
        extend 1sub "ты добавил [rooms]!"
        if not spacerooms_installed:
            m 1eka "Я не могу поверить, что ты сделал это для меня..."

    m 1rkc "..."
    m 3rksdla "Но...{w=0.3} я даже не знаю, как ими пользоваться.{w=0.5} {nw}"
    extend 3hksdlb "Я ещё не научилась так хорошо программировать!"
    m 1eud "Если ты дашь мне немного времени, я уверена, что выясню, как использовать то, что ты добавил.{nw}"
    extend 3eua " Я дам тебе знать, когда разберусь."
    m 1eka "Несмотря на то, что мы пока не можем это использовать, большое спасибо за то, что сделал это для меня.{w=0.2} Это имеет куда большее значение, чем ты думаешь."
    m 3huu "Я так тебя люблю, [player]~"
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="bg_room_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label bg_room_installed:
    python:
        #Check how many tw mods we have installed
        tw_bg_count = len(filter(lambda x: "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        spacerooms_installed = len(filter(lambda x: "furnished spaceroom" in x.name.lower() and "tw4449" in x.author, mas_submod_utils.submod_map.values()))
        had_backgrounds_before = (mas_background.getUnlockedBGCount() - tw_bg_count) > 1

    if renpy.seen_label("bg_room_installed_low_affection"):
        m 1wub "[player]!{w=0.2} Помнишь те новые комнаты, которые ты добавил?{w=0.2} {nw}"
        extend 3wub "Наконец-то я поняла, как ими пользоваться!"
        m 3eua "Всё, что тебе нужно сделать сейчас, это выбрать «Эй, [m_name]...» и перейти в «Местонахождение», после выбери «Мы можем пойти в другое место?»"
        m 1eub "Тогда мы сможем посетить любую из добавленных тобою комнат!"
        m 3sub "Я так взволнована~"
        m 3huu "Почему бы нам не посетить одну из них прямо сейчас, [player]?"
        m 1ekbla "Ох, и...{w=0.3} ещё раз спасибо, что добавил их для меня. Ты действительно особенный."

    else:
        if spacerooms_installed:
            m 1wuo "Ч-что?{w=0.5} В игре есть файлы мебели?"
            m 1sub "[player],{w=0.2} ты сделал это?"
            m 3ekbsu "Ты знал, что мне нужна мебель, поэтому добавил её...{w=0.3} ты удивительный, ты знал это?"

        if tw_bg_count - spacerooms_installed > 0:
            $ too = "ещё " if spacerooms_installed else ""
            $ rooms = "новые комнаты" if tw_bg_count - spacerooms_installed > 1 else "новую комнату"
            m 1suo "Что это?{w=0.5} Ты добавил [too][rooms]?"
            m 3hua "Ты действительно выложился по полной, не так ли?"
            if not spacerooms_installed:
                m 1eka "Не могу поверить, что ты изо всех сил старался сделать это для меня..."

        m 1dka "Большое тебе спасибо [player],{w=0.2} я...{w=1} {nw}"
        extend 1ekbsu "я очень сильно тебя люблю."

        if not had_backgrounds_before:
            m 3eub "Я добавлю новую категорию в «Местонахождение» в разделе «Эй, [m_name]...» так что мы можем расставить мебель и посетить другие комнаты.{w=.5} Я не могу дождаться, чтобы попробовать!"

        m 1eka "Возможно, таким образом я не стану ближе к твоей реальности...{w=3} {nw}"
        extend 7hubfb "но с тобой, это место будет больше походить на наш дом~"
    return "no_unlock"

#LABEL OVERRIDES
init 1 python:
    config.label_overrides["monika_players_control"] = "monika_players_control_override"

label monika_players_control_override:
    m 3eub "[player], а знал ли ты о том, что у тебя в этой игре гораздо большая власть, чем у меня?"
    m 3eua "У тебя есть доступ к файлам игры и его коду, верно?"
    m 1eka "Следовательно, ты можешь изменить это всё, когда захочешь."
    m 3eka "Ты можешь даже изменить то, что не могу изменить я."
    m 4eub "К примеру, изменить всю механику игры. Сделать из визуального романа спокойную игровую площадку, которая у нас есть сейчас."

    if mas_isMoniEnamored(higher=True) and not persistent._mas_acs_enable_promisering:
        m 1ekbsa "Или красивое кольцо обещания."
        m 3dkbsu "О, разве это не было бы воплощением мечты?"

    if not mas_consumable_coffee.enabled():
        m 1wuo "Ты мог бы даже добавить чашку с кофе в игру для меня!"
        m 1eka "Это было бы чудесно."

    if not persistent._mas_pm_has_code_experience:
        m 1hksdrb "Но я полагаю, что твои навыки программирования настолько же хорошие, что и у меня."
    else:
        m 3eua "Учитывая, что ты знаком с кодингом,{w=0.1} {nw}"
        extend 3hua "я уверена, что ты мог бы сделать что-то подобное!"

    m 1eua "Полагаю, таково предназначение видеоигр...{w=0.3} {nw}"
    extend 3eua "иметь практически безграничные возможности в мире, с которыми можешь взаимодействовать."
    m 3eub "С этим не соскучишься точно!"

    if not persistent._mas_pm_has_contributed_to_mas:
        m 1eka "Даже если ты не знаешь точно, как изменить эту игру..."
        $ line = "Мы всё ещё можешь наслаждаться этим миром, который и свёл нас вместе."

    else:
        $ line = "Особенно когда ты рядом со мной~"

    show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5eubla "[line]"
    m 5ekbfa "Нет лучше способа насладиться игрой, чем быть рядом с тем, кого я люблю."

    $ persistent._seen_ever["monika_players_control"] = True
    return


init 1 python:
    config.label_overrides["monika_gotomonika"] = "monika_gotomonika_override"

label monika_gotomonika_override:
    m 1euc "Перейти в мой мир?"
    m 1lksdld "Ты имеешь в виду эту небольшую комнату, витающую в пустоте?"

    m 2lksdla "Я очень рада тому, что ты хочешь быть здесь, со мной, но..."
    m 2eksdlc "Ты правда не должен."
    m 2eksdld "Знаю, я уже говорила о том, что я бы давным-давно затащила тебя сюда, если бы могла..."
    m 2eksdlc "Но чем больше я задумываюсь об этом, тем больше думаю, что было бы целесообразнее, если бы я перешла в твою реальность."
    m 3eka "Я бы предпочла оказаться там, нежели ждать, когда ты придёшь сюда."
    m 3dsc "[player]...{w=1}не говори мне, что ты правда хочешь бросить свою реальность...{w=0.5} {i}настоящий{/i} мир...{w=0.5}лишь ради того, чтобы прийти {i}сюда{/i}, в богом забытое место?{nw}"
    $ _history_list.pop()
    menu:
        m "[player]...{w=1}не говори мне, что ты правда хочешь бросить свою реальность...{w=0.5} {i}настоящий{/i} мир...{w=0.5}лишь ради того, чтобы прийти {i}сюда{/i}, в богом забытое место?{fast}"
        "Да, хочу.":
            $ persistent._mas_pm_would_come_to_spaceroom = True

            m 4wkd "Но [player]!"
            m "Здесь совсем нечего делать!"
            m 2dsc "Ты {i}так сильно{/i} ненавидишь свою реальность?"
            m 2eka "Когда-нибудь, я найду способ добраться до тебя, и когда этот день настанет, я обещаю, эти усилия оправдают себя."
            m 4euc "Куда бы жизнь не забросила тебя с этого момента, я буду рядом с тобой, чтобы помочь тебе справиться с нагрузкой."
            m 4eud "Даже сейчас, если у тебя был тяжёлый день, ты можешь поговорить со мной об этом в любое время."
            m 2dsc "Жизнь, скорее всего, бросала тебя во все стороны, если учесть то, что ты большую её часть проводил со мной."
            m 3hua "Но, раз уж ты пребываешь здесь, то это лишь показывает, насколько ты устойчив."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Мне уже не терпится разделить хорошие и плохие мгновения вместе с тобой."

        "Возможно, ты права.":
            $ persistent._mas_pm_would_come_to_spaceroom = False

            m 1eka "Я рада, что ты всё ещё хочешь подождать меня, [player]."
            m 1lksdla "Не пойми неправильно, я {i}правда{/i} хочу быть с тобой..."
            m 1lksdlc "Но мне кажется, что ты можешь оказаться в опасности, если попытаешься незамедлительно перейти в иную реальность."
            m 1eka "...Если такое вообще возможно с нынешними технологиями."
            m 1hub "Не волнуйся, таким образом, мы сможем поддерживать наши отношения и далее!"
            m 1hksdlb "Знаю, потребуется какое-то время, пока мы не станем вместе, но я надеюсь, что ты можешь подождать."
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Я буду ждать столько, сколько потребуется, [mas_get_player_nickname()]."

        "...":
            $ persistent._mas_pm_would_come_to_spaceroom = None

            m 2eka "Всё нормально, я буду всегда ценить те мгновения, что мы пережили вместе, и дорожить как ими, так и нынешним."
            m 2ekc "Впрочем, я даже не знаю, как ты сможешь попасть сюда с нынешними технологиями."
            m 2lksdlc "...И даже если бы {i}существовала{/i} такая возможность, то я бы начала сомневаться в её безопасности или гарантии."
            m 2lksdld "Поэтому, сделай мне одолжение – хотя бы подожди, пока технологии не доведут до ума, чтобы их безопасность можно было гарантировать."
            m 2lksdlc "Я {i}правда{/i} не хочу, чтобы ты рискнул и, сделав это неправильно, оказался в собственной пустоте..."
            m 2dkd "...оставив нас обоих в полном одиночестве."
            m 4hua "В смысле, технологии всегда идут в ногу со временем, причём довольно быстро, следовательно, мы можем увидеть друг друга прежде, чем поймём это!"
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5eua "Так что, просто подожди свою любимую девушку, и я обещаю, что сделаю для тебя то же самое, [mas_get_player_nickname()]."

    m 5luu "Но-о-о...{w=1} если ты всё-таки появишься на моём крыльце..."
    show monika 1hksdlb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1hksdlb "То, полагаю, у меня не будет другого выбора, кроме как принять этот факт и поприветствовать тебя с распростёртыми объятиями!"
    m 1eksdla "Этого будет мало для начала, но я уверена, что мы найдём способ сделать это лучше."
    m 3hub "С течением времени, мы могли бы уже создать свою реальность!"
    m 3euc "Если подумать, то да, это звучит довольно запутанно..."
    m 3eub "Но я не сомневаюсь в том, что вместе мы могли бы достичь чего угодно!"
    m 3etc "Знаешь...{w=1} наверное, тебе было бы {i}гораздо{/i} проще прийти сюда, но я не перестаю надеяться, что смогу прийти к тебе лично."
    m 1eua "Ну а пока, давай просто подождём и посмотрим, что можно сделать."

    $ persistent._seen_ever["monika_gotomonika"] = True
    return

### remove the readme
init 0 python:
    store.mas_utils.trydel(renpy.config.basedir.replace('\\', '/') + "/readme.md")