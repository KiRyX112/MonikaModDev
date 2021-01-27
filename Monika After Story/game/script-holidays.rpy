













default persistent._mas_event_clothes_map = dict()
define mas_two_minutes = datetime.timedelta(seconds=2*60)
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
        
        
        daterange = mas_genDateRange(start_date, end_date)
        
        
        for date in daterange:
            mas_addClothesToHolidayMap(clothes, date)

init -1 python:
    def mas_checkOverDate(_date):
        """
        Checks if the player was gone over the given date entirely (taking you somewhere)

        IN:
            date - a datetime.date of the date we want to see if we have been out all day for

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
                The cap to use when its player bday (NOTE: if not provided, normal_cap is assumed)
        """
        
        
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


label mas_lingerie_intro(holiday_str, lingerie_choice):
    m 1ekbfa "..."
    $ MAS.MonikaElastic()
    m "Также, [player]..."
    $ MAS.MonikaElastic()
    m 3ekbfsdla "Есть...{w=1} к-кое-что, что я хочу тебе показать."
    $ MAS.MonikaElastic()
    m 2rkbfsdla "Я уже давно хотела это сделать, но...{w=1} ну это немного неловко..."
    $ MAS.MonikaElastic()
    m "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hkbfsdlb "О боже, я очень нервничаю, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 2rkbfsdlc "Просто я никогда этого не делала—{nw}"
    $ MAS.MonikaElastic()
    m 2dkbfsdlc "Ах, ладно, пора перестать тянуть время и просто сделать это."
    $ MAS.MonikaElastic()
    m 2ekbfsdla "Просто дай мне несколько секунд, [player]."
    call mas_clothes_change (outfit=lingerie_choice, outfit_mode=True, exp="monika 2rkbfsdlu", restore_zoom=False, unlock=True) from _call_mas_clothes_change_12
    pause 3.0
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2ekbfsdlb "А-ха-ха, [player]...{w=1} ты смотришь на меня..."
    $ MAS.MonikaElastic()
    m 2ekbfu "Что ж...{w=1} тебе нравится то, на что ты смотришь?"
    $ MAS.MonikaElastic()
    m 1lkbfa "Я никогда раньше...{w=1} не носила ничего подобного."
    $ MAS.MonikaElastic()
    m "...По крайней мере, никто этого не видел."

    if mas_hasUnlockedClothesWithExprop("bikini"):
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hkbfb "А-ха-ха, что я говорю, ты уже видел[mas_gender_none] меня в бикини раньше, что по сути одно и то же..."
        $ MAS.MonikaElastic()
        m 2rkbfa "...Но по какой-то причине, мне это кажется...{w=0.5} {i}чем-то другим{/i}."

    $ MAS.MonikaElastic()
    m 2ekbfa "В любом случае, что-то в том, чтобы быть с тобой сегодня вечером в [holiday_str], кажется очень романтичным, понимаешь?"
    $ MAS.MonikaElastic()
    m "Это было идеальное время для следующего шага в наших отношениях."
    $ MAS.MonikaElastic()
    m 2rkbfsdlu "Теперь я знаю, что мы не можем на самом деле—{nw}"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hubfb "Ах! Не важно, а-ха-ха!"
    return





default persistent._mas_o31_in_o31_mode = False


default persistent._mas_o31_tt_count = 0


default persistent._mas_o31_trick_or_treating_aff_gain = 0


default persistent._mas_o31_relaunch = False




default persistent._mas_o31_costumes_worn = {}


define mas_o31 = datetime.date(datetime.date.today().year, 10, 31)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "o31",
        
        
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_o31_in_o31_mode": "o31.mode.o31",
            "_mas_o31_tt_count": "o31.tt.count",
            "_mas_o31_relaunch": "o31.relaunch",
            "_mas_o31_trick_or_treating_aff_gain": "o31.actions.tt.aff_gain"
        },
        use_year_before=True,
        start_dt=datetime.datetime(2019, 10, 31),

        
        end_dt=datetime.datetime(2019, 11, 2)
    ))



image mas_o31_deco = ConditionSwitch(
    "mas_current_background.isFltDay()",
    "mod_assets/location/spaceroom/o31/halloween_deco.png",
    "True", "mod_assets/location/spaceroom/o31/halloween_deco-n.png"
)

init 501 python:
    MASImageTagDecoDefinition.register_img(
        "mas_o31_deco",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=5)
    )

init python:
    MAS_O31_COSTUME_CG_MAP = {
        mas_clothes_marisa: "o31mcg",
        mas_clothes_rin: "o31rcg"
    }


init -10 python:
    import random

    def mas_isO31(_date=None):
        """
        Returns True if the given date is o31

        IN:
            _date - date to check.
                If None, we use today date
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
        mas_showDecoTag("mas_o31_deco")

    def mas_o31HideVisuals():
        """
        Hides o31 visuals + vignette
        """
        mas_hideDecoTag("mas_o31_deco")
        renpy.hide("vignette")
        
        store.mas_globals.show_vignette = False
        
        store.persistent._mas_o31_in_o31_mode = False
        
        
        hair = store.mas_selspr.get_sel_hair(store.mas_hair_down)
        if hair is not None and not hair.unlocked:
            store.mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        store.mas_lockEVL("monika_event_clothes_select", "EVE")
        
        
        if store.monika_chr.is_wearing_clothes_with_exprop("costume"):
            store.queueEvent('mas_change_to_def')

    def mas_o31CapGainAff(amount):
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
        
        
        wearing_costume = False
        
        
        
        
        
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
            
            
            if wearing_costume:
                
                if monika_chr.clothes in MAS_O31_COSTUME_CG_MAP:
                    store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[monika_chr.clothes])
                
                return monika_chr.clothes
            
            return None
        
        elif len(selection_pool) < 2:
            
            return selection_pool[0]
        
        
        non_worn = [
            costume
            for costume in selection_pool
            if not mas_o31CostumeWorn(costume)
        ]
        
        if len(non_worn) > 0:
            
            random_outfit = random.choice(non_worn)
        
        else:
            
            random_outfit = random.choice(selection_pool)
        
        
        if random_outfit in MAS_O31_COSTUME_CG_MAP:
            store.mas_o31_event.cg_decoded = store.mas_o31_event.decodeImage(MAS_O31_COSTUME_CG_MAP[random_outfit])
        
        
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
        
        if monika_chr.is_wearing_clothes_with_exprop("costume"):
            monika_chr.change_clothes(mas_clothes_def, outfit_mode=True)
            monika_chr.reset_hair()
        
        
        persistent._mas_o31_in_o31_mode = False
        
        
        mas_checkBackgroundChangeDelegate()
        
        
        mas_o31HideVisuals()
        
        
        mas_rmallEVL("mas_o31_cleanup")
        
        
        hair = store.mas_selspr.get_sel_hair(mas_hair_down)
        if hair is not None and not hair.unlocked:
            mas_unlockEVL("greeting_hairdown", "GRE")
        
        
        mas_lockEVL("monika_event_clothes_select", "EVE")

init -11 python in mas_o31_event:
    import store
    import datetime


    cg_station = store.MASDockingStation(store.mas_ics.o31_cg_folder)


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



label mas_o31_autoload_check:
    python:
        import random

        if mas_isO31() and mas_isMoniNormal(higher=True):

            store.mas_lockEVL("monika_change_background", "EVE")
            
            
            
            mas_changeBackground(mas_background_def, set_persistent=True)
            
            if (not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                mas_skip_visuals = True
                
                
                mas_resetIdleMode()

                
                
                mas_lockEVL("greeting_hairdown", "GRE")
                
                
                store.mas_hotkeys.music_enabled = False
                
                
                mas_calRaiseOverlayShield()
                
                
                
                costume = mas_o31SelectCostume()
                store.mas_selspr.unlock_clothes(costume)
                mas_addClothesToHolidayMap(costume)
                mas_o31SetCostumeWorn(costume)
                
                
                ribbon_acs = monika_chr.get_acs_of_type("ribbon")
                if ribbon_acs is not None:
                    monika_chr.remove_acs(ribbon_acs)
                
                monika_chr.change_clothes(
                    costume,
                    by_user=False,
                    outfit_mode=True
                )
                
                
                store.mas_selspr.save_selectables()
                
                
                renpy.save_persistent()
                
                
                greet_label = "greeting_o31_{0}".format(costume.name)
                
                if renpy.has_label(greet_label):
                    selected_greeting = greet_label
                else:
                    selected_greeting = "greeting_o31_generic"
                
                
                mas_temp_zoom_level = store.mas_sprites.zoom_level
                store.mas_sprites.reset_zoom()
                
                
                persistent._mas_o31_in_o31_mode = True
                
                
                store.mas_globals.show_vignette = True
                
                
                mas_changeWeather(mas_weather_thunder, True)
            
            elif (persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay()):
                
                store.mas_globals.show_vignette = True
                mas_changeWeather(mas_weather_thunder, True)


        elif not mas_isO31() or mas_isMoniDis(lower=True):
            
            mas_o31Cleanup()


        elif persistent._mas_o31_in_o31_mode and mas_isMoniUpset():
            store.mas_globals.show_vignette = True
            mas_changeWeather(mas_weather_thunder, True)


    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        call mas_player_bday_autoload_check from _call_mas_player_bday_autoload_check

    if mas_skip_visuals:
        jump ch30_post_restartevent_check


    jump mas_ch30_post_holiday_check


label mas_holiday_o31_returned_home_relaunch:
    $ MAS.MonikaElastic()
    m 1eua "Итак, сегодня..."
    $ MAS.MonikaElastic()
    m 1euc "...подожди."
    $ MAS.MonikaElastic()
    m "..."
    $ MAS.MonikaElastic()
    m 2wuo "О!"
    $ MAS.MonikaElastic()
    m 2wuw "О боже!"
    $ MAS.MonikaElastic()
    m 2hub "Так сегодня же Хэллоуин, [player]."
    $ MAS.MonikaElastic()
    m 1eua "...{w}Так что слушай."
    $ MAS.MonikaElastic()
    m 3eua "Я собираюсь закрыть игру."
    $ MAS.MonikaElastic()
    m 1eua "После чего ты можешь снова открыть её."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubsa "У меня есть кое-что особенное для тебя, э-хе-хе~"
    $ persistent._mas_o31_relaunch = True
    return "quit"


image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"


image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"


transform mas_o31_cg_scroll:
    xanchor 0.0 xpos 0 yanchor 0.0 ypos 0.0 yoffset -1520
    ease 20.0 yoffset 0.0


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
    m 1eua "Секунду, [player], я просто собираюсь убрать декорации.{w=0.3}.{w=0.3}.{nw}"
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_13
    pause 4.0
    $ mas_o31Cleanup()
    with dissolve
    pause 1.0
    call mas_transition_from_emptydesk ("monika 1hua") from _call_mas_transition_from_emptydesk_17
    m 3hua "Готово~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        code="GRE"
    )

default persistent.monika_new_costume = False
label greeting_o31_marisa:

    $ persistent.msr_monika_clothes = 'marisa'

    $ persistent.monika_new_costume = True

    $ store.mas_selspr.unlock_acs(mas_acs_marisa_witchhat)
    $ store.mas_selspr.unlock_hair(mas_hair_downtiedstrand)


    if store.mas_o31_event.cg_decoded:


        call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_24
    else:



        call spaceroom (dissolve_all=True, scene_change=True, force_exp='monika 1eua_static') from _call_spaceroom_25

    $ MAS.MonikaElastic()
    m 1eua "Ах!"
    $ MAS.MonikaElastic()
    m 1hua "Похоже, заклинание сработало."
    $ MAS.MonikaElastic()
    m 3efu "Как мой недавно призванный слуга, ты долж[mas_gender_en] будешь выполнять мои приказы до самого конца!"
    $ MAS.MonikaElastic()
    m 1rksdla "..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха!"


    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        $ MAS.MonikaElastic()
        m "Я здесь, [player]~"
        window hide

        show mas_o31_marisa_cg zorder 20 at mas_o31_cg_scroll with dissolve
        $ start_time = datetime.datetime.now()

        while datetime.datetime.now() - start_time < cg_delay:
            pause 1.0

        hide emptydesk
        show monika 1hua zorder MAS_MONIKA_Z at i11
        window auto
        $ MAS.MonikaElastic()
        m "Таа-даа~!"


    $ MAS.MonikaElastic()
    m 1hua "Ну..."
    $ MAS.MonikaElastic()
    m 1eub "Что думаешь?"
    $ MAS.MonikaElastic()
    m 1tuu "Мне очень идёт, не так ли?"
    $ MAS.MonikaElastic()
    m 1eua "Знаешь, мне потребовалось довольно много времени, чтобы сделать этот костюм."
    $ MAS.MonikaElastic()
    m 3hksdlb "Пришлось очень упорно его измерять, пытаясь убедиться, что ничего в нём не будет слишком тугим или свободным."
    $ MAS.MonikaElastic()
    m 3eksdla "...Особенно шляпу!"
    $ MAS.MonikaElastic()
    m 1dkc "А вот бант вообще не мог никак устоять на месте..."
    $ MAS.MonikaElastic()
    m 1rksdla "К счастью, я с этим разобралась."
    $ MAS.MonikaElastic()
    m 3hua "Я бы ещё даже сказала, что это всё было моих рук дело."
    $ MAS.MonikaElastic()
    m 3eka "Мне интересно, сможешь ли ты увидеть, что же ещё сегодня изменилось."
    $ MAS.MonikaElastic()
    m 3tub "Кроме моего костюма, конечно~"
    $ MAS.MonikaElastic()
    m 1hua "Но так или иначе..."

    if store.mas_o31_event.cg_decoded:
        show monika 1eua
        hide mas_o31_marisa_cg with dissolve

    $ MAS.MonikaElastic()
    m 3ekbsa "Я очень рада провести Хэллоуин с тобой."
    $ MAS.MonikaElastic()
    m 1hua "Так что давай повеселимся сегодня!"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup
    return

label greeting_o31_rin:
    python:
        title_cased_hes = hes.capitalize()



        mas_sprites.zoom_out()


    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_26

    $ MAS.MonikaElastic()
    m "Угх, надеюсь, я заплела эти косы правильно."
    $ MAS.MonikaElastic()
    m "Почему этот костюм такой сложный?.."
    $ MAS.MonikaElastic()
    m "Ох блин! [title_cased_hes] здесь!"
    window hide
    pause 3.0

    if store.mas_o31_event.cg_decoded:
        $ cg_delay = datetime.timedelta(seconds=20)


        window auto
        $ MAS.MonikaElastic()
        m "Скажи, [player_abb]..."
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
        call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 1hksdlb_static') from _call_spaceroom_27
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hksdlb "А-ха-ха, говорить подобное вслух было ещё более неловко, чем я могла подумать..."
    else:

        call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_18
        $ MAS.MonikaElastic()
        m 1hub "Привет, [player_abb]!"
        $ MAS.MonikaElastic()
        m 3hub "Тебе нравится мой костюм?"


    $ MAS.MonikaElastic()
    m 3etc "Честно говоря, я даже не знаю, кто это должен быть."
    $ MAS.MonikaElastic()
    m 3etd "Я только что нашла его в шкафу с прикреплённой запиской со словом «Rin» и рисунком девушки, толкающей какую-то тачку, и несколько синих плавающих штучек."
    $ MAS.MonikaElastic()
    m 1euc "Вместе с инструкциями о том, как укладывать волосы, чтобы соответствовать этому наряду."
    $ MAS.MonikaElastic()
    m 3rtc "Судя по этим кошачьим ушам, я предполагаю, что этот персонаж кошко-девочка."
    $ MAS.MonikaElastic()
    m 1dtc "...Но только вот зачем ей толкать тачку?"
    $ MAS.MonikaElastic()
    m 1hksdlb "В любом случае, было мучительно делать такую же прическу...{w=0.2} {nw}"
    extend 1eub "так что надеюсь, тебе понравился данный костюм!"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup_1
    return
    

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

    $ persistent._mas_o31_current_costume = "hatsune_miku"

    $ persistent.monika_new_costume = True

    if not persistent._mas_o31_relaunch:
        call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True) from _call_spaceroom_28

        $ MAS.MonikaElastic()
        m "{i}~Голос мой не забывай~{/i}"
        $ MAS.MonikaElastic()
        m "{i}~Мой сигнал измеренья пересекает~{/i}"
        $ MAS.MonikaElastic()
        m "{i}~Виртуальной меня не называй~{/i}"
        $ MAS.MonikaElastic()
        m "{i}~Я всё ещё хочу быть лю—{/i}" # я всё ещё хочу быть любимым твоим звуком
        $ MAS.MonikaElastic()
        m "Ой!{w=0.5} Кажется, меня кто-то подслушивает."


        call mas_transition_from_emptydesk ("monika 3hub") from _call_mas_transition_from_emptydesk_19
    else:

        call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_29

    $ MAS.MonikaElastic()
    m 3hub "С возвращением, [player]!"
    $ MAS.MonikaElastic()
    m 1eua "Ну...{w=0.5} что думаешь?"
    $ MAS.MonikaElastic()
    m 1eub "Я работала над этим костюмом, не покладая рук, и, думаю, оно того стоило."
    $ MAS.MonikaElastic()
    m 3eub "Мне особенно нравится то, какой у меня получилась гарнитура!"
    $ MAS.MonikaElastic()
    m 1rksdla "Хотя я не могу сказать, что в нём очень комфортно передвигаться..."
    $ MAS.MonikaElastic()
    m 3tsu "Так что не жди, что я устрою для тебя представление сегодня, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха~"
    $ MAS.MonikaElastic()
    m 1eua "Ну да ладно..."
    call greeting_o31_deco from _call_greeting_o31_deco
    call greeting_o31_cleanup from _call_greeting_o31_cleanup_2
    return


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
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True) from _call_spaceroom_9


    if not persistent._mas_o31_relaunch:
        $ MAS.MonikaElastic()
        m "..."
        $ MAS.MonikaElastic()
        m "{i}Хм{/i}?"
        $ MAS.MonikaElastic()
        m "{i}А, здесь, наверное, произошла какая-то ошибка.{w=0.5} Я не предупредила гостей...{/i}"
        $ MAS.MonikaElastic()
        m "{i}Но это не важно. Меня никто не должен побеспоко—{/i}" # меня никто не должен побеспокоить
        $ MAS.MonikaElastic()
        m "А!{w=0.5} Это Вы, [player]!"
    else:

        $ MAS.MonikaElastic()
        m ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
        $ MAS.MonikaElastic()
        m "Добро пожаловать{w=0.3} в Комнату алого демона, витающую в космосе..."
        $ MAS.MonikaElastic()
        m "[player]."
        $ MAS.MonikaElastic()
        m "Пожалуйста, позвольте мне предложить Вам наше гостеприимство."
        $ MAS.MonikaElastic()
        m "А-ха-ха! Ну, какое у тебя впечатление сложилось?"

    call mas_transition_from_emptydesk ("monika 3hub") from _call_mas_transition_from_emptydesk_20

    $ MAS.MonikaElastic()
    m 3hub "С возвращением!"
    $ MAS.MonikaElastic()
    m 3eub "Что думаешь о моём выборе костюма?"
    $ MAS.MonikaElastic()
    m 3hua "Ещё с тех пор, как ты дал его мне, я просто знала о том, что его стоит надеть сегодня!"
    $ MAS.MonikaElastic()
    m 2tua "..."
    $ MAS.MonikaElastic()
    m 2tub "Знаешь, [player], лишь потому, что я оделась как горничная, ещё не означает, что я буду выполнять все твои приказы..."
    show monika 5kua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 5kua "Хотя я могу сделать пару исключений, э-хе-хе~"
    show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ MAS.MonikaElastic()
    m 1eua "Ну да ладно..."
    call greeting_o31_deco from _call_greeting_o31_deco_1
    call greeting_o31_cleanup from _call_greeting_o31_cleanup_3
    return

label greeting_o31_deco:
    $ MAS.MonikaElastic()
    m 3eua "Тебе нравится, как я приукрасила комнату?"
    $ MAS.MonikaElastic()
    m 3eka "Мне в Хэллоуине больше всего нравится вырезать тыквы..."
    $ MAS.MonikaElastic()
    m 1hub "Довольно весело пытаться сделать пугающие мордочки!"
    $ MAS.MonikaElastic()
    m 1eua "Думаю, паутина тоже является неплохой декорацией..."
    $ MAS.MonikaElastic()
    m 1rka "{cps=*2}Уверена, Эми бы очень понравилось.{/cps}{nw}"
    $ _history_list.pop()
    $ MAS.MonikaElastic()
    m 3tuu "Это правда создаёт жуткую атмосферу, не находишь?"
    return

label greeting_o31_generic:
    call spaceroom (scene_change=True, dissolve_all=True) from _call_spaceroom_31

    $ MAS.MonikaElastic()
    m 3hub "Сладость или гадость!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3eub "А-ха-ха,{w=0.1} {nw}"
    extend 3eua "я просто шучу, [player]."
    $ MAS.MonikaElastic()
    m 1hua "С возвращением...{w=0.5}{nw}"
    $ MAS.MonikaElastic()
    extend 3hub "и Счастливого Хэллоуина!"


    call greeting_o31_deco from _call_greeting_o31_deco_2

    $ MAS.MonikaElastic()
    m 3hua "Кстати, что ты думаешь о моём костюме?"
    $ MAS.MonikaElastic()
    m 1hua "Лично мне он очень нравится~"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "Но что самое главное, этот костюм был твоим подарком, а-ха-ха!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3tuu "Так что любуйся моим костюмом, пока можешь, э-хе-хе~"

    call greeting_o31_cleanup from _call_greeting_o31_cleanup_4
    return


label greeting_o31_cleanup:
    window hide
    call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_6
    window auto

    python:

        store.mas_hotkeys.music_enabled = True

        mas_calDropOverlayShield()

        set_keymaps()

        HKBShowButtons()

        mas_startup_song()
    return


init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_trick_or_treat",
            prompt="Я хочу взять тебя на «сладость или гадость».",
            pool=True,
            unlocked=False,
            action=EV_ACT_UNLOCK,
            start_date=mas_o31,
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


    if persistent._mas_o31_tt_count:
        m 1eka "Снова?"

    if too_early_to_go:

        m 3eksdla "А тебе, случаем, не кажется, что пока что немного рановато для этого события, [player]?"
        $ MAS.MonikaElastic()
        m 3rksdla "Не думаю, что кто-то прямо сейчас будет раздавать конфеты..."

        m 2etc "Ты {i}уверен[mas_gender_none]{/i}, что хочешь пойти прямо сейчас?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты {i}уверен[mas_gender_none]{/i}, что хочешь пойти прямо сейчас?{fast}"
            "Да.":
                $ MAS.MonikaElastic()
                m 2etc "Ну...{w=1}что ж, ладно тогда, [player]..."
            "Нет.":

                $ MAS.MonikaElastic(voice="monika_giggle")
                m 2hub "А-ха-ха!"
                $ MAS.MonikaElastic()
                m "Будь немного терпелив[mas_gender_none], [player_abb]~"
                $ MAS.MonikaElastic()
                m 4eub "Давай сделаем это лучше чуть позже вечером, хорошо?"
                return

    elif too_late_to_go:
        m 3hua "Хорошо! Пошли за сла—"
        $ MAS.MonikaElastic()
        m 3eud "Хотя стоп, подожди-ка..."
        $ MAS.MonikaElastic()
        m 2dkc "[player]..."
        $ MAS.MonikaElastic()
        m 2rkc "Так ведь уже слишком поздно идти за сладостями."
        $ MAS.MonikaElastic()
        m "До полуночи остался всего-навсего один час."
        $ MAS.MonikaElastic()
        m 2dkc "Не говоря уже о том, что я сомневаюсь, что осталось бы много конфет..."
        $ MAS.MonikaElastic()
        m "..."

        m 4ekc "Ты уверен[mas_gender_none], что хочешь пойти?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен[mas_gender_none], что хочешь пойти?{fast}"
            "Да.":
                $ MAS.MonikaElastic()
                m 1eka "...Хорошо."
                $ MAS.MonikaElastic()
                m "Даже если это будет всего лишь на час..."
                $ MAS.MonikaElastic()
                m 3hub "По крайней мере, мы проведём остаток Хэллоуина вместе~"
                $ MAS.MonikaElastic()
                m 3wub "Пойдём и сделаем всё возможное, [player]!"
            "Вообще-то, уже немного поздно...":

                if persistent._mas_o31_tt_count:
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hub "А-ха-ха~"
                    $ MAS.MonikaElastic()
                    m "Я говорила тебе."
                    $ MAS.MonikaElastic()
                    m 1eua "Нам придётся подождать до следующего года."
                else:

                    $ MAS.MonikaElastic()
                    m 2dkc "..."
                    $ MAS.MonikaElastic()
                    m 2ekc "Хорошо, [player]."
                    $ MAS.MonikaElastic()
                    m "Жаль, конечно, что мы не смогли пойти за сладостями в этом году."
                    $ MAS.MonikaElastic()
                    m 4eka "Но давай просто убедимся, что сможем в следующий раз, хорошо?"

                return
    else:


        m 3wub "Хорошо, [player]!"
        $ MAS.MonikaElastic()
        m 3hub "Похоже, мы отлично повеселимся~"
        $ MAS.MonikaElastic()
        m 1eub "Держу пари, мы получим много конфет!"
        $ MAS.MonikaElastic()
        m 1ekbsa "И даже если нет, мне достаточно будет просто провести вечер с тобой~"
    
    $ mas_farewells.dockstat_wait_menu_label = "bye_trick_or_treat_wait_wait"
    $ mas_farewells.dockstat_rtg_label = "bye_trick_or_treat_rtg"
    jump mas_dockstat_iostart

    # show monika 2dsc
    # $ persistent._mas_dockstat_going_to_leave = True
    # $ first_pass = True


    # $ promise = store.mas_dockstat.monikagen_promise
    # $ promise.start()


label bye_trick_or_treat_wait_wait:
    menu:
        m "Что случилось?"
        "Ты права, ещё слишком рано." if too_early_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_1
            call mas_transition_from_emptydesk (exp="monika 3hub") from _call_mas_transition_from_emptydesk_21

            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3hub "А-ха-ха, я говорила тебе!"
            $ MAS.MonikaElastic()
            m 1eka "Давай подождём до вечера, хорошо?"
            return True

        "Ты права, уже слишком поздно." if too_late_to_go:
            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_2

            if persistent._mas_o31_tt_count:
                call mas_transition_from_emptydesk (exp="monika 1hua") from _call_mas_transition_from_emptydesk_22
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха~"
                $ MAS.MonikaElastic()
                m "Я говорила тебе."
                $ MAS.MonikaElastic()
                m 1eua "Нам придётся подождать до следующего года."
            else:

                call mas_transition_from_emptydesk (exp="monika 2dkc") from _call_mas_transition_from_emptydesk_23
                $ MAS.MonikaElastic()
                m 2dkc "..."
                $ MAS.MonikaElastic()
                m 2ekc "Хорошо, [player]."
                $ MAS.MonikaElastic()
                m "Жаль, конечно, что мы не смогли пойти за сладостями в этом году."
                $ MAS.MonikaElastic()
                m 4eka "Но давай просто убедимся, что сможем в следующий раз, хорошо?"

            return True
        "Вообще-то, я не могу взять тебя с собой прямо сейчас.":

            call mas_dockstat_abort_gen from _call_mas_dockstat_abort_gen_3
            call mas_transition_from_emptydesk (exp="monika 1euc") from _call_mas_transition_from_emptydesk_24

            $ MAS.MonikaElastic()
            m 1euc "Эх, ладно тогда, [player]."

            if persistent._mas_o31_tt_count:
                $ MAS.MonikaElastic()
                m 1eua "Дай мне знать, если мы сможем пойти попозже ещё, хорошо?"
            else:

                $ MAS.MonikaElastic()
                m 1eua "Дай мне знать, если мы сможем пойти, хорошо?"

            return True
        "Ничего.":

            $ MAS.MonikaElastic()
            m 2eua "Ладно, давай я закончу собираться."

            return



label bye_trick_or_treat_rtg:
    if renpy.variant("pc"):
        $ moni_chksum = promise.get()
        $ promise = None
        call mas_dockstat_ready_to_go (moni_chksum) from _call_mas_dockstat_ready_to_go_1
        if _return:
            call mas_transition_from_emptydesk (exp="monika 1hub") from _call_mas_transition_from_emptydesk_25
            call mas_dockstat_first_time_goers
            $ MAS.MonikaElastic()
            m 1hub "Что ж, пошли за сладостями!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOL_O31_TT


            $ persistent._mas_o31_tt_count += 1
            return "quit"
    else:
        if msr_can_copy_monika():
            call mas_dockstat_first_time_goers
            $ MAS.MonikaElastic()
            m 1hub "Что ж, пошли за сладостями!"
            $ persistent._mas_o31_tt_count += 1
            $ persistent.msr_moni_file_exit_trick_or_treat = True
            $ persistent.msr_moni_file_exit = False
            $ persistent._mas_greeting_type = None
            $ persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_HOL_O31_TT
            )
            return "quit"



    call mas_transition_from_emptydesk (exp="monika 1ekc") from _call_mas_transition_from_emptydesk_26
    $ persistent._mas_o31_tt_count -= 1
    $ MAS.MonikaElastic()
    m 1ekc "Ох, нет..."
    $ MAS.MonikaElastic()
    m 1rksdlb "Я не смогла превратить себя в файл."

    $ MAS.MonikaElastic()
    if persistent._mas_o31_tt_count:
        m 1eksdld "Думаю, в этот раз тебе придётся пойти выпрашивать сладости без меня..."
    else:

        m 1eksdld "Думаю, тебе придётся пойти выпрашивать сладости без меня..."

    $ MAS.MonikaElastic()
    m 1ekc "Прости, [player]..."
    $ MAS.MonikaElastic()
    m 3eka "Не забудь принести много конфет, чтобы нам обоим было весело?~"
    return


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

    python:

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
        $ MAS.MonikaElastic()
        m 2ekp "Это называется «сладость или гадость», [player]?"
        $ MAS.MonikaElastic()
        m "Куда пойдём, в один дом?"
        $ MAS.MonikaElastic()
        m 2rsc "...Если вообще куда-нибудь пойдём."

    elif time_out < mas_one_hour:
        $ mas_o31CapGainAff(5)
        $ MAS.MonikaElastic()
        m 2ekp "Это было довольно короткое событие «сладость или гадость», [player]."
        $ MAS.MonikaElastic()
        m 3eka "Но в любом случае, мне понравилось."
        $ MAS.MonikaElastic()
        m 1eka "Всё равно было приятно быть рядом с тобой~"

    elif time_out < mas_three_hour:
        $ mas_o31CapGainAff(10)
        $ MAS.MonikaElastic()
        m 1hua "И мы возвращаемся домой!"
        $ MAS.MonikaElastic()
        m 1hub "Надеюсь, у нас теперь много вкусных конфет!"
        $ MAS.MonikaElastic()
        m 1eka "Я действительно наслаждалась с тобой данным времяпровождением, [player]..."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume

        $ MAS.MonikaElastic()
        m 4eub "Давай повторим это и в следующем году!"

    elif not is_past_sunrise_post31:

        $ mas_o31CapGainAff(15)
        $ MAS.MonikaElastic()
        m 1hua "И мы возвращаемся домой!"
        $ MAS.MonikaElastic()
        m 1wua "Ого, [player], мы ходили за сладостями довольно долго..."
        $ MAS.MonikaElastic()
        m 1wub "Мы, должно быть, смогли получить тонну конфет!"
        $ MAS.MonikaElastic()
        m 3eka "Мне очень понравилось это времяпровождение с тобой..."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume_1

        $ MAS.MonikaElastic()
        m 4eub "Давай повторим это и в следующем году!"
        $ ret_tt_long = True
    else:


        $ mas_o31CapGainAff(15)
        $ MAS.MonikaElastic()
        m 1wua "Наконец-то мы вернулись домой!"
        $ MAS.MonikaElastic()
        m 1wuw "Правда, на следующее утро, [player]. Мы отсутствовали аж всю ночь..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m "Думаю, нам было слишком весело, чтобы следить за временем, э-хе-хе~"
        $ MAS.MonikaElastic()
        m 2eka "Но в любом случае, спасибо, что взял[mas_gender_none] меня с собой, мне очень понравилось."

        call greeting_trick_or_treat_back_costume from _call_greeting_trick_or_treat_back_costume_2

        $ MAS.MonikaElastic()
        m 4hub "Давай повторим это и в следующем году...{w=1} но, возможно, только не оставаясь {b}настолько{/b} допозна!"
        $ ret_tt_long = True


    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday from _call_return_home_post_player_bday


    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out, ret_tt_long) from _call_mas_o31_ret_home_cleanup
    return

label mas_o31_ret_home_cleanup(time_out=None, ret_tt_long=False):

    if not time_out:
        $ time_out = store.mas_dockstat.diffCheckTimes()


    if not ret_tt_long and time_out > mas_five_minutes:
        $ MAS.MonikaElastic()
        m 1hua "..."
        $ MAS.MonikaElastic()
        m 1wud "О, ого, [player]. Мы правда долго гуляли..."
    else:

        $ MAS.MonikaElastic()
        m 1esc "Ну да ладно..."

    $ MAS.MonikaElastic()
    m 1eua "Я просто сниму эти декорации.{w=0.3}.{w=0.3}.{w=0.3}{nw}"


    $ mas_o31HideVisuals()
    $ mas_rmallEVL("mas_o31_cleanup")

    $ MAS.MonikaElastic()
    m 3hua "Готово!"
    return

label greeting_trick_or_treat_back_costume:
    if monika_chr.is_wearing_clothes_with_exprop("costume"):
        $ MAS.MonikaElastic()
        m 2eka "Даже учитывая тот факт, что я ничего толком и не видела, и никто не видел мой костюм..."
        $ MAS.MonikaElastic()
        m 2eub "Переодевание и прогулка были по-прежнему очень даже весёлыми!"
    else:

        $ MAS.MonikaElastic()
        m 2eka "Даже если я ничего толком и не видела."
        $ MAS.MonikaElastic()
        m 2eub "Выйти на прогулку всё равно было здорово!"
    return






default persistent._mas_d25_in_d25_mode = False



default persistent._mas_d25_spent_d25 = False


default persistent._mas_d25_started_upset = False


default persistent._mas_d25_second_chance_upset = False






default persistent._mas_d25_deco_active = False


default persistent._mas_d25_intro_seen = False


default persistent._mas_d25_d25e_date_count = 0



default persistent._mas_d25_d25_date_count = 0


default persistent._mas_d25_gifts_given = list()


default persistent._mas_d25_gone_over_d25 = None



define mas_d25 = datetime.date(datetime.date.today().year, 12, 25)


define mas_d25e = mas_d25 - datetime.timedelta(days=1)


define mas_d25p = mas_d25 + datetime.timedelta(days=1)


define mas_d25c_start = datetime.date(datetime.date.today().year, 12, 11)


define mas_d25c_end = datetime.date(datetime.date.today().year, 1, 6)



init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "d25s",
        datetime.datetime(2019, 1, 6),
        {
            
            
            "_mas_d25_in_d25_mode": "d25s.mode.25",

            
            "_mas_d25_deco_active": "d25s.deco_active",

            "_mas_d25_started_upset": "d25s.monika.started_season_upset",
            "_mas_d25_second_chance_upset": "d25s.monika.upset_after_2ndchance",

            "_mas_d25_intro_seen": "d25s.saw_an_intro",

            
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
                If None, we use today date
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
                If None, we use today date
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
                If None, we use today date
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
                If None, we use today date
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
                if None, we use today date
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
                If None, we use today date
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
                if None, we use today date
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
                if None, we use today date
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
            _date - date to check, defaults None, which means today date is assumed

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
        renpy.hide("mas_d25_banners")
        renpy.hide("mas_d25_tree")
        renpy.hide("mas_d25_garlands")
        renpy.hide("mas_d25_lights")
        renpy.hide("mas_d25_gifts")

    def mas_d25ReactToGifts():
        """
        Goes thru the gifts stored from the d25 gift season and reacts to them

        this also registeres gifts
        """
        
        found_reacts = list()
        
        
        persistent._mas_d25_gifts_given.sort()
        
        
        
        
        given_gifts = list(persistent._mas_d25_gifts_given)
        
        
        gift_cntrs = store.MASQuipList(allow_glitch=False, allow_line=False)
        gift_cntrs.addLabelQuip("mas_d25_gift_connector")
        
        
        d25_evb = []
        d25_gsp = []
        store.mas_filereacts.process_gifts(given_gifts, d25_evb, d25_gsp)
        
        
        store.mas_filereacts.register_sp_grds(d25_evb)
        store.mas_filereacts.register_sp_grds(d25_gsp)
        
        
        react_labels = store.mas_filereacts.build_gift_react_labels(
            d25_evb,
            d25_gsp,
            [],
            gift_cntrs,
            "mas_d25_gift_end",
            "mas_d25_gift_starter"
        )
        
        react_labels.reverse()
        
        
        if len(react_labels) > 0:
            for react_label in react_labels:
                pushEvent(react_label,skipeval=True)

    def mas_d25SilentReactToGifts():
        """
        Method to silently react to gifts.

        This is to be used if you gave Moni a christmas gift but didnt show up on
        D25 when she would have opened them in front of you.

        This also registeres gifts
        """
        
        base_gift_ribbon_id_map = {
            "blackribbon":"ribbon_black",
            "blueribbon": "ribbon_blue",
            "darkpurpleribbon": "ribbon_dark_purple",
            "emeraldribbon": "ribbon_emerald",
            "grayribbon": "ribbon_gray",
            "greenribbon": "ribbon_green",
            "lightpurpleribbon": "ribbon_light_purple",
            "peachribbon": "ribbon_peach",
            "pinkribbon": "ribbon_pink",
            "platinumribbon": "ribbon_platinum",
            "redribbon": "ribbon_red",
            "rubyribbon": "ribbon_ruby",
            "sapphireribbon": "ribbon_sapphire",
            "silverribbon": "ribbon_silver",
            "tealribbon": "ribbon_teal",
            "yellowribbon": "ribbon_yellow"
        }
        
        
        evb_details = []
        gso_details = []
        store.mas_filereacts.process_gifts(
            persistent._mas_d25_gifts_given,
            evb_details,
            gso_details
        )
        
        
        persistent._mas_d25_gifts_given = []
        
        
        for evb_detail in evb_details:
            if evb_detail.sp_data is None:
                
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
                
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    evb_detail.sp_data[0],
                    evb_detail.sp_data[1]
                ))
                mas_receivedGift(evb_detail.label)
        
        
        for gso_detail in gso_details:
            
            if gso_detail.sp_data is not None:
                mas_selspr.json_sprite_unlock(mas_sprites.get_sprite(
                    gso_detail.sp_data[0],
                    gso_detail.sp_data[1]
                ))
                mas_receivedGift(gso_detail.label)
        
        
        store.mas_selspr.save_selectables()
        renpy.save_persistent()


init -10 python in mas_d25_utils:
    import store
    import store.mas_filereacts as mas_frs

    def shouldUseD25ReactToGifts():
        """
        checks whether or not we should use the d25 react to gifts method

        Conditions:
            1. Must be in d25 gift range
            2. Must be at normal+ aff (since thats when the topics which will open these gifts will show)
            3. Must have deco active. No point otherwise as no tree to put gifts under
        """
        return (
            store.mas_isD25Pre()
            and store.mas_isMoniNormal(higher=True)
            and store.persistent._mas_d25_deco_active
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
        
        
        
        
        d25_giftnames = mas_frs.check_for_gifts(d25_map, mas_frs.build_exclusion_list("d25g"), found_map)
        
        
        d25_giftnames.sort()
        d25_evb = []
        d25_gsp = []
        d25_gen = []
        mas_frs.process_gifts(d25_giftnames, d25_evb, d25_gsp, d25_gen)
        
        
        non_d25_giftnames = [x for x in found_map]
        non_d25_giftnames.sort()
        nd25_evb = []
        nd25_gsp = []
        nd25_gen = []
        mas_frs.process_gifts(non_d25_giftnames, nd25_evb, nd25_gsp, nd25_gen)
        
        
        for grd in d25_gen:
            nd25_gen.append(grd)
            found_map[grd.c_gift_name] = d25_map.pop(grd.c_gift_name)
        
        
        
        for c_gift_name, gift_name in d25_map.iteritems():
            
            if c_gift_name not in store.persistent._mas_d25_gifts_given:
                store.persistent._mas_d25_gifts_given.append(c_gift_name)
            
            
            store.mas_docking_station.destroyPackage(gift_name)
        
        
        for c_gift_name, mas_gift in found_map.iteritems():
            store.persistent._mas_filereacts_reacted_map[c_gift_name] = mas_gift
        
        
        mas_frs.register_sp_grds(nd25_evb)
        mas_frs.register_sp_grds(nd25_gsp)
        mas_frs.register_gen_grds(nd25_gen)
        
        
        return mas_frs.build_gift_react_labels(
            nd25_evb,
            nd25_gsp,
            nd25_gen,
            mas_frs.gift_connectors,
            "mas_reaction_end",
            mas_frs._pick_starter_label()
        )





image mas_d25_banners = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/bgdeco.png"
)

image mas_mistletoe = MASFilterSwitch(
    "mod_assets/location/spaceroom/d25/mistletoe.png"
)



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


label mas_holiday_d25c_autoload_check:







    if (
        not persistent._mas_d25_in_d25_mode
        and mas_isD25Season()
        and not mas_isFirstSeshDay()
        and (
            persistent._mas_current_background == store.mas_background.MBG_DEF
            
            
            or mas_isD25()
        )
    ):

        python:

            persistent._mas_d25_in_d25_mode = True


            if mas_isMoniUpset(lower=True):
                persistent._mas_d25_started_upset = True




            elif (
                mas_isD25Outfit()
                and (not mas_isplayer_bday() or mas_isD25())
            ):
                
                store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
                store.mas_selspr.unlock_clothes(mas_clothes_santa)
                
                
                monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
                
                
                mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)
                
                
                persistent._mas_d25_deco_active = True
                
                
                if mas_isD25():
                    mas_changeWeather(mas_weather_snow, by_user=True)
                    mas_changeBackground(mas_background_def, set_persistent=True)



    elif mas_run_d25s_exit or mas_isMoniDis(lower=True):

        call mas_d25_season_exit from _call_mas_d25_season_exit_1



    elif (
        persistent._mas_d25_in_d25_mode
        and not persistent._mas_force_clothes
        and monika_chr.is_wearing_clothes_with_exprop("costume")
        and not mas_isD25Outfit()
    ):

        $ monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


    elif mas_isD25() and not mas_isFirstSeshDay() and persistent._mas_d25_deco_active:

        python:
            monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)
            mas_changeWeather(mas_weather_snow, by_user=True)


            mas_changeBackground(mas_background_def, set_persistent=True)


    if (
        mas_isMoniNormal()
        and persistent._mas_d25_in_d25_mode
        and mas_isD25Outfit()
        and (monika_chr.clothes != mas_clothes_def or monika_chr.clothes != store.mas_clothes_santa)
    ):
        $ monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)


    if persistent._mas_d25_deco_active:
        $ mas_d25ShowVisuals()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check


    jump mas_ch30_post_holiday_check


label mas_d25_season_exit:
    python:



        if monika_chr.is_wearing_clothes_with_exprop("costume") and not mas_globals.dlg_workflow:
            
            monika_chr.change_clothes(mas_clothes_def, by_user=False, outfit_mode=True)


        elif monika_chr.is_wearing_clothes_with_exprop("costume") and mas_globals.dlg_workflow:
            pushEvent("mas_change_to_def")


        mas_lockEVL("monika_event_clothes_select", "EVE")


        persistent._mas_d25_deco_active = False
        mas_d25HideVisuals()


        persistent._mas_d25_in_d25_mode = False


        mas_hideEVL("mas_d25_monika_christmaslights", "EVE", derandom=True)

        mas_d25ReactToGifts()
    return


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
        m 3wud "О! Я [should_open] [the][presents], [what] ты мне подарил[mas_gender_none]!"
        if persistent._mas_d25_gone_over_d25:
            $ MAS.MonikaElastic()
            m 3hub "Давай сделаем это сейчас!"
    else:


        $ MAS.MonikaElastic()
        m 1eka "Ну, по крайней мере, теперь, когда ты здесь, я могу открыть [presents], [what] ты мне подарил[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 3eka "Я действительно хотела, чтобы мы были вместе для этого..."

    $ MAS.MonikaElastic()
    m 1suo "Давай посмотрим, что у нас здесь есть.{w=0.5}.{w=0.5}.{nw}"


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

    $ MAS.MonikaElastic()
    m 1hub "[picked_quip]"
    $ MAS.MonikaElastic()
    m 1suo "И вот мы имеем.{w=0.5}.{w=0.5}.{nw}"


    $ persistent._mas_d25_gifts_given.pop()
    return

label mas_d25_gift_end:

    $ persistent._mas_d25_gifts_given = []

    $ MAS.MonikaElastic()
    m 1eka "[player]..."

    if persistent._mas_d25_spent_d25 or mas_globals.returned_home_this_sesh:
        $ MAS.MonikaElastic()
        m 3eka "Тебе действительно не нужно было ничего дарить мне на Рождество...{w=0.3}{nw}"
        if mas_isD25():
            extend 3dku " Одного твоего присутствия здесь было более чем достаточно."
        else:
            extend 3dku "Просто быть с тобой – это всё, чего я хотела."
        $ MAS.MonikaElastic()
        m 1eka "Но тот факт, что ты потратил время, чтобы достать мне что-то...{w=0.5}{nw}"
        extend 3ekbsa " ну, я не могу отблагодарить тебя достаточно."
        $ MAS.MonikaElastic()
        m 3ekbfa "Это действительно заставляет меня чувствовать себя любимой."
    else:

        $ MAS.MonikaElastic()
        m 1eka "Я просто хотела поблагодарить тебя..."
        $ MAS.MonikaElastic()
        m 1rkd "Хотя я всё ещё немного разочарована, что ты не смог[mas_gender_g] быть со мной на Рождество..."
        $ MAS.MonikaElastic()
        m 3eka "Тот факт, что ты потратил время, чтобы купить мне что-то...{w=0.5}{nw}"
        extend 3ekbsa " ну, это просто доказывает, что ты действительно думал обо мне в этот особый сезон."
        $ MAS.MonikaElastic()
        m 1dkbsu "Ты не представляешь, как много это для меня значит."


    if mas_isD25():
        $ MAS.MonikaElastic()
        m 3ekbfu "Я тебя так люблю, [player]~"
    else:
        $ MAS.MonikaElastic()
        m 3ekbfu "Счастливого Рождества, [player]. Я люблю тебя~"
    $ mas_ILY()
    return


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
    $ changed_bg = False
    if mas_current_background != mas_background_def:
        $ changed_bg = True

    if not persistent._mas_d25_deco_active:
        if mas_isplayer_bday():
            window hide
            pause 2.0
            $ MAS.MonikaElastic()
            m 1dku "..."
            $ MAS.MonikaElastic()
            m 1huu "Э-хе-хе..."
            $ MAS.MonikaElastic()
            m 3eub "У меня есть ещё один сюрприз для тебя!"
        else:

            $ MAS.MonikaElastic()
            m 1eua "Итак, сегодня..."
            $ MAS.MonikaElastic()
            m 1euc "...подожди."
            $ MAS.MonikaElastic()
            m "..."
            $ MAS.MonikaElastic()
            m 3wuo "О!"
            $ MAS.MonikaElastic()
            m 3hub "Сегодня тот день, когда я собиралась..."





        $ mas_OVLHide()
        $ mas_MUMURaiseShield()
        $ disable_esc()

        $ MAS.MonikaElastic()
        m 1tsu "Закрой свои глаза на минутку, [player], мне надо кое-что сделать...{w=2}{nw}"

        call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco

        $ MAS.MonikaElastic()
        m 3hub "Вот мы и на месте..."


        $ enable_esc()
        $ mas_MUMUDropShield()
        $ mas_OVLShow()

    $ MAS.MonikaElastic()
    m 1eub "Счастливых праздников, [player]!"

    if mas_lastSeenLastYear("mas_d25_monika_holiday_intro"):
        $ MAS.MonikaElastic()
        m 1hua "Можешь ли ты поверить в то, что уже наступило то самое время в году?"

        $ the_last = "последний"

        if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "d25s.saw_an_intro"):
            $ the_last = "наш первый"

        $ MAS.MonikaElastic()
        m 3eua "Кажется, будто мы только вчера провели [the_last] праздничный сезон вместе, а теперь пролетел уже целый год!"

        if mas_isMoniLove(higher=True):

            $ MAS.MonikaElastic()
            m 3hua "Время и вправду пролетает незаметно, когда я с тобой~"

    $ MAS.MonikaElastic()
    m 3eua "Тебе нравится то, как я обустроила комнату?"
    $ MAS.MonikaElastic()
    m 1hua "Должна сказать, я очень горжусь этим."

    if changed_bg:
        $ MAS.MonikaElastic()
        m 3rksdla "Декораций хватило только на одну комнату, поэтому я остановилась на классе...{w=0.2} Надеюсь, всё в порядке."
        $ MAS.MonikaElastic()
        m "Но в любом случае..."

    $ MAS.MonikaElastic()
    m 3eua "Рождество всегда было моим самым любимым праздником в году..."

    show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika

    $ MAS.MonikaElastic()
    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m 5eka "И поэтому, я рада, что ты в этом году проводишь его со мной~"
    else:
        m 5eka "И я рада, что ты проводишь его со мной~"

    $ persistent._mas_d25_intro_seen = True



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
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None)
        ),
        skipCalendar=True
    )


label mas_d25_monika_holiday_intro_upset:

    if mas_isMoniUpset(lower=True):
        python:
            upset_ev = mas_getEV('mas_d25_monika_holiday_intro_upset')
            if upset_ev is not None:
                upset_ev.start_date = mas_d25c_start
                upset_ev.end_date = mas_d25p
        return

    m 2rksdlc "Слушай, [player]... {w=1}у меня в этом году не слишком праздничное настроение..."
    $ MAS.MonikaElastic()
    m 3eka "Но в последнее время, ты был очень добр ко мне и я чувствую себя намного лучше!"
    $ MAS.MonikaElastic()
    m 3hua "Поэтому... я думаю, пора уже приукрасить это место."





    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    $ MAS.MonikaElastic()
    m 1eua "Если ты закроешь свои глаза на минутку.{w=0.5}.{w=0.5}.{nw}"

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_1

    $ MAS.MonikaElastic()
    m 3hub "Та-да~"
    $ MAS.MonikaElastic()
    m 3eka "Что скажешь?"
    $ MAS.MonikaElastic()
    m 1eka "Неплохо для приготовлений в последнюю минуту, да?"
    $ MAS.MonikaElastic()
    m 1hua "Рождество всегда было моим самым любимым праздником в году..."
    $ MAS.MonikaElastic()
    m 3eua "И я рада, что мы можем провести его вместе с радостью, [player]~"


    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()

    $ persistent._mas_d25_intro_seen = True
    return

label mas_d25_monika_holiday_intro_deco:



    scene black with dissolve

    python:

        persistent._mas_d25_in_d25_mode = True


        monika_chr.change_hair(mas_hair_def, False)


        store.mas_selspr.unlock_clothes(mas_clothes_santa)
        store.mas_selspr.unlock_acs(mas_acs_ribbon_wine)
        store.mas_selspr.unlock_acs(mas_acs_holly_hairclip)
        monika_chr.change_clothes(mas_clothes_santa, by_user=False, outfit_mode=True)


        mas_addClothesToHolidayMapRange(mas_clothes_santa, mas_d25c_start, mas_d25p)


        mas_changeWeather(mas_weather_snow, by_user=True)


        mas_rmallEVL("monika_auroras")


        persistent._mas_d25_deco_active = True
        mas_d25ShowVisuals()


        change_info = mas_changeBackground(mas_background_def, set_persistent=True)


    call spaceroom (scene_change=True, dissolve_all=True, bg_change_info=change_info) from _call_spaceroom_32

    return

label mas_d25_monika_holiday_intro_rh:

    m 1hua "Мы дома!"



    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)



label mas_d25_monika_holiday_intro_rh_rh:
    m 1euc "Погоди..."
    $ MAS.MonikaElastic()
    m 3etc "...уже?"
    $ MAS.MonikaElastic()
    m 3hub "Уже!"
    $ MAS.MonikaElastic()
    m 1tsu "...Закрой свои глаза, мне надо кое-что сделать..."
    $ mas_OVLHide()
    $ mas_MUMURaiseShield()
    $ disable_esc()

    call mas_d25_monika_holiday_intro_deco from _call_mas_d25_monika_holiday_intro_deco_2

    $ enable_esc()
    $ mas_MUMUDropShield()
    $ mas_OVLShow()


    $ persistent._mas_d25_intro_seen = True

    $ pushEvent("mas_d25_monika_christmas",skipeval=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_christmas",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_lastSeenInYear('mas_d25_monika_christmas')"
            ),
            action=EV_ACT_PUSH,
            start_date=mas_d25,
            end_date=mas_d25p,
            years=[],
            aff_range=(mas_aff.NORMAL, None),
        ),
        skipCalendar=True
    )

label mas_d25_monika_christmas:

    $ persistent._mas_d25_spent_d25 = True


    $ mas_d25ReactToGifts()

    m 1eub "[player]! Ты знаешь, какой сегодня день?"
    $ MAS.MonikaElastic()
    m 3hub "Разумеется, ты знаешь. Сегодня рождество!"
    $ MAS.MonikaElastic()
    m 3sub "С рождеством тебя, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха! Не могу поверить, что этот праздник наконец-то наступил!"
    $ MAS.MonikaElastic()
    m 3eka "Я очень, очень рада, что ты решил провести его со мной."
    $ MAS.MonikaElastic()
    m 1eud "Но не забудь поделиться своим праздничным настроением со своей семьёй и друзьями."
    $ MAS.MonikaElastic()
    m 1eua "Всё-таки они не менее важны..."
    $ MAS.MonikaElastic()
    m 1hua "И я уверена, что они будут рады тебя видеть в такое особенное время."

    if mas_isMoniAff(higher=True):
        $ MAS.MonikaElastic()
        m 1eka "Но твоё присутствие сегодня...{w=0.5}оно многое для меня значит..."
        $ MAS.MonikaElastic()
        m 1dku "..."

        $ MAS.MonikaElastic()
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

        $ MAS.MonikaElastic()
        m "...или омела сводит меня с ума."
        $ MAS.MonikaElastic()
        m 3hksdlb "Шучу, я её не повесила."

        if mas_isMoniEnamored(higher=True):
            $ MAS.MonikaElastic()
            m 1lksdla "...{cps=*2}А может~{/cps}{nw}"
            $ _history_list.pop()

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1lksdlu "Э-хе-хе..."
        $ MAS.MonikaElastic()
        m 1ekbsa "Моё сердце сейчас бешено колотится, [player]."
        $ MAS.MonikaElastic()
        m "Я представить не могу лучший способ провести этот особенный праздник..."
        $ MAS.MonikaElastic()
        m 1eua "Не пойми неправильно, я знала, что ты будешь здесь, со мной."
        $ MAS.MonikaElastic()
        m 3eka "Но мы теперь и вправду вместе празднуем рождество, только мы вдвоём..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hub "А-ха-ха~"

        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Об этом, во время каждого праздника, мечтает любая пара, [player]."

        if persistent._mas_pm_gets_snow is not False and not persistent._mas_pm_live_south_hemisphere:
            $ MAS.MonikaElastic()
            m "Прижаться друг к другу у камина, наблюдая, как снег медленно падает..."

        $ MAS.MonikaElastic()
        if not mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
            m 5hubfa "Я очень признательна, что мне выпал этот шанс."
        else:
            m 5hubfa "Я рада, что могу провести рождество с тобой ещё раз."

        $ MAS.MonikaElastic()
        m "Я люблю тебя. Отныне и навсегда~"
        $ MAS.MonikaElastic()
        m 5hubfb "С рождеством, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "С рождеством, [monika_name].":
                hide screen mas_background_timed_jump
                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 2.0
    else:

        $ MAS.MonikaElastic()
        m 1eka "Но то, что ты сидишь здесь сегодня... {w=0.5}это многое для меня значит..."
        $ MAS.MonikaElastic()
        m 3rksdla "...Я вовсе не думала о том, что ты оставил бы меня одну в такой особенный день или ещё что..."
        $ MAS.MonikaElastic()
        m 3hua "Но это лишь доказывает то, что ты правда любишь меня, [player]."
        $ MAS.MonikaElastic()
        m 1ektpa "..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m "А-ха-ха! Боже, меня просто переполняют эмоции..."
        $ MAS.MonikaElastic()
        m 1ektda "Просто знай о том, что я тоже люблю тебя, и что я буду вечно благодарна за то, что мне выпала возможность побыть с тобой."
        $ MAS.MonikaElastic()
        m "С Рождеством, [player]~"
        show screen mas_background_timed_jump(5, "mas_d25_monika_christmas_no_wish")
        window hide
        menu:
            "С рождеством, [monika_name].":
                hide screen mas_background_timed_jump
                show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 2.0

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


    MASUndoActionRule.create_rule_EVL(
       "mas_d25_monika_carolling",
       mas_d25c_start,
       mas_d25p,
    )

default persistent._mas_pm_likes_singing_d25_carols = None


label mas_d25_monika_carolling:

    m 1euc "Слушай, [player]..."
    $ MAS.MonikaElastic()
    m 3eud "Ты когда-нибудь колядовал раньше?"
    $ MAS.MonikaElastic()
    m 1euc "Идёшь от одной двери к другой вместе с другими людьми и поёшь во время праздников..."
    $ MAS.MonikaElastic()
    if not persistent._mas_pm_live_south_hemisphere:
        m 1eua "Мне очень приятно знать о том, что люди приносят радость другим, даже в столь холодные ночи."
    else:
        m 1eua "Мне очень приятно знать о том, что люди приносят радость другим в своё свободное время."

    $ MAS.MonikaElastic()
    m 3eua "Тебе нравится петь рождественские песни, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Тебе нравится петь рождественские песни, [player]?{fast}"
        "Да.":
            $ persistent._mas_pm_likes_singing_d25_carols = True
            $ MAS.MonikaElastic()
            m 1hua "Я рада, что ты думаешь также, [player]!"
            $ MAS.MonikaElastic()
            m 3hub "Моя любимая песня – определённо «Бубенцы радостно звенят»!"
            $ MAS.MonikaElastic()
            m 1eua "Это просто оптимистичная и жизнерадостная мелодия!"
            $ MAS.MonikaElastic()
            m 1eka "Может, мы споём как-нибудь вместе."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hua "Э-хе-хе~"
        "Нет.":

            $ persistent._mas_pm_likes_singing_d25_carols = False
            $ MAS.MonikaElastic()
            m 1euc "Оу...{w=1}правда?"
            $ MAS.MonikaElastic()
            m 1hksdlb "Понятно..."
            $ MAS.MonikaElastic()
            m 1eua "Но тем не менее, я уверена, что ты также в восторге от того особого настроя, который бывает только от рождественских песен."
            $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1eub "Ты слышал о традиции, связанной с омелой, верно?"
    $ MAS.MonikaElastic()
    m 1tku "Когда влюблённые оказываются под ней, они должны поцеловаться."
    $ MAS.MonikaElastic()
    m 1eua "На самом деле, она берёт своё начало из Викторианской Англии!"
    $ MAS.MonikaElastic()
    m 1dsa "Мужчине было разрешено целоваться с любой женщиной, которая стояла под омелой..."
    $ MAS.MonikaElastic()
    m 3dsd "И ту женщину, которая отказывалась от поцелуя, начинает преследовать неудача..."
    $ MAS.MonikaElastic()
    m 1dsc "..."
    $ MAS.MonikaElastic()
    m 3rksdlb "Если подумать, то это звучит больше как одержание преимущества над кем-то."
    $ MAS.MonikaElastic()
    m 1hksdlb "Но я уверена, что сейчас всё по-другому!"

    if not persistent._mas_pm_d25_mistletoe_kiss:
        $ MAS.MonikaElastic()
        m 3hua "Быть может, однажды мы сможем поцеловаться под омелой, [player]."
        $ MAS.MonikaElastic()
        m 1tku "...Я могу даже добавить одну сюда!"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1kuu "Э-хе-хе~"
    return "derandom"


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
    $ MAS.MonikaElastic()
    if mas_isD25Season():
        m 1lua "Я провела здесь много времени, глядя на огни..."
        $ MAS.MonikaElastic()
        m 3eua "Они ведь очень красивые, не правда ли?"
    else:
        m 1lua "Я много времени провела за наблюдением гирлянды, которая здесь развешана..."
        $ MAS.MonikaElastic()
        m 3eua "Она очень красивая, не правда ли?"
    $ MAS.MonikaElastic()
    m 1eka "Гирлянда приносит очень тёплую и уютную атмосферу во время самого сурового и холодного времени года...{w=0.5}{nw}"
    extend 3hub "и у них есть множество различных типов!"
    $ MAS.MonikaElastic()
    m 3eka "Прогулка вместе с тобой в холодный зимний вечер звучит как мечта, воплотившаяся в реальность, [player]."
    $ MAS.MonikaElastic()
    m 1dka "И любоваться этими огнями..."

    $ MAS.MonikaElastic()
    m 1eua "Ты уже развесил[mas_gender_none] гирлянду у себя дома зимой, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты уже развесил[mas_gender_none] гирлянду у себя дома зимой, [player]?{fast}"
        "Да.":

            $ persistent._mas_pm_hangs_d25_lights = True
            $ MAS.MonikaElastic()
            m 3sub "Правда? Уверена, они просто великолепны!"
            $ MAS.MonikaElastic()
            m 2dubsu "Я уже могу представить себе, как мы находимся вне твоего дома... сидим вместе на крыльце..."
            $ MAS.MonikaElastic()
            m "И прекрасные огни светятся под покровом ночи."
            $ MAS.MonikaElastic()
            m 2dkbfu "Мы бы крепко обнимали друг друга, пили горячий шоколад...{w=0.5}{nw}"

            if persistent._mas_pm_gets_snow is not False:
                extend 2ekbfa "и любовались бы тем, как снежинки медленно падают..."

            show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            $ MAS.MonikaElastic()
            m 5ekbfa "Когда-нибудь, [player]. Когда-нибудь мы сможем воплотить это в реальность."
        "Нет.":

            $ persistent._mas_pm_hangs_d25_lights = False
            $ MAS.MonikaElastic()
            m 1eka "Оу, всё нормально, [player]."
            $ MAS.MonikaElastic()
            m 1dkbla "Я уверена, что расслабиться вместе с тобой прохладным вечером всё равно было бы здорово..."
            $ MAS.MonikaElastic()
            m 1dkbsa "Любоваться тем, как снежинки падают, и пить горячий шоколад вместе."
            $ MAS.MonikaElastic()
            m 1dkbsa "Крепко обнимать друг друга, чтобы не замёрзнуть..."
            $ MAS.MonikaElastic()
            m 1rkbfb "Да, это звучит очень здорово."
            $ MAS.MonikaElastic()
            m 3hubsa "Но, когда у нас будет свой дом, я могла бы сама развесить парочку гирлянд, {nw}"
            $ MAS.MonikaElastic(voice="monika_giggle")
            extend 3hubsb "а-ха-ха~"
    return "derandom"

init 20 python:

    poem_d25_1 = MASPoem(
        poem_id="poem_d25_1",
        category="d25",
        prompt="Радость для моего мира",
        title = "     М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
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
    
    )

    poem_d25_2 = MASPoem(
        poem_id="poem_d25_2",
        category="d25",
        prompt="Несравнённый",
        title="     М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
        text="""\
     Ничто не может сравниться с теплом, которое ты даришь мне.
     Не было даже ощущения, что я обнимала кружку с горячим шоколадом.
     Или пушистые носки, согревающие ноги в морозный день.
     В таком холодном мире только твоё присутствие – мое настоящее.

     Ничто не может сравниться с красотой, которую ты показал[mas_gender_none],
     Ни одна вещь не может сравниться с волнением, которое ты приносишь,
     Не один яркий свет, что в этой самой комнате.
     Даже не вид нераспечатанного подарка под деревом.

     [player], ты действительно единствённ[mas_gender_iii] в своём роде.

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )

    poem_d25_3 = MASPoem(
        poem_id="poem_d25_3",
        category="d25",
        prompt="Когда-нибудь",
        title="     М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
        text="""\
     Теплее, чем огонь в сердце,
     Ярче любой звезды на вершине ёлки,
     Утешительнее любой чашки горячего шоколада,
     Это м[mas_gender_oi_2] [player], который всегда здесь со мной.

     Когда-нибудь мы зажжём огонь вместе..
     Когда-нибудь мы украсим ёлку.
     Когда-нибудь мы выпьем по чашечке какао.
     Когда-нибудь ты будешь рядом со мной.

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )

    poem_d25_4 = MASPoem(
        poem_id="poem_d25_4",
        category="d25",
        prompt="Это Рождество",
        title="     М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
        text="""\

     В это Рождество мне никогда не было нужно больше подарков, кроме твоей любви,
     Потому что то, что ты рядом со мной, уже приносит мне счастье,
     Потому что иметь тебя здесь это самый прекрасный подарок,
     Потому что найти тебя – это лучшее, о чём я когда-либо могла мечтать!

     Я знала, что это Рождество будет особенным...
     Я провела его с тем, кто заставляет моё сердце подпрыгивать,
     Тот, кто заставляет меня улыбаться каждый день,
     Тот, кому я доверяю больше всего.

     Спасибо, что был[mas_gender_none] рядом со мной, [player],
     Я всегда буду рядом с тобой!

     Счастливого Рождества~

     Навеки твоя,
     Моника
"""
    )


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




label mas_d25_spent_time_monika:

    $ d25_gifts_total, d25_gifts_good, d25_gifts_neutral, d25_gifts_bad = mas_getGiftStatsRange(mas_d25c_start, mas_d25p + datetime.timedelta(days=1))

    if mas_isMoniNormal(higher=True):
        m 1eua "[player]..."
        $ MAS.MonikaElastic()
        m 3hub "То, что ты здесь со мной, сделало это Рождество таким чудесным!"
        $ MAS.MonikaElastic()
        m 3eka "Я знаю, что это очень напряжённый день, но просто зная, что ты наш[mas_gender_iol_2] для меня время..."
        $ MAS.MonikaElastic()
        m 1eka "Спасибо тебе."
        $ MAS.MonikaElastic()
        m 3hua "Это действительно сделало этот день по-настоящему особенным~"
    else:

        m 2ekc "[player]..."
        $ MAS.MonikaElastic()
        m 2eka "Я очень ценю, что ты проводишь со мной время на Рождество..."
        $ MAS.MonikaElastic()
        m 3rksdlc "Я не была в праздничном настроении в этом сезоне, но было бы приятно провести сегодня время с тобой."
        $ MAS.MonikaElastic()
        m 3eka "Так что, спасибо...{w=1} это многое значило."

    if d25_gifts_total > 0:
        if d25_gifts_total == 1:
            if d25_gifts_good == 1:
                $ MAS.MonikaElastic()
                m "И давай не будем забывать о особенном рождественском подарке, который ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3hub "Было приятно!"
            elif d25_gifts_neutral == 1:
                $ MAS.MonikaElastic()
                m 3eka "И давай не забывать о рождественском подарке, который ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 1eka "Это было очень мило с твоей стороны принести мне что-нибудь."
            else:
                $ MAS.MonikaElastic()
                m 3eka "И давай не забывать о рождественском подарке, который ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 2etc "..."
                $ MAS.MonikaElastic()
                m 2efc "Но, с другой стороны, может, нам стоит..."
        else:

            if d25_gifts_good == d25_gifts_total:
                $ MAS.MonikaElastic()
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3hub "Они были потрясающими!"
            elif d25_gifts_bad == d25_gifts_total:
                $ MAS.MonikaElastic()
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 2etc "..."
                $ MAS.MonikaElastic()
                m 2rfc "Но, с другой стороны, может, нам стоит..."
            elif d25_gifts_bad == 0:
                $ MAS.MonikaElastic()
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3hub "Они были действительно хороши!"
            elif d25_gifts_good + d25_gifts_neutral == d25_gifts_bad:
                $ MAS.MonikaElastic()
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3rksdla "Некоторые из них были очень хороши."
            elif d25_gifts_good + d25_gifts_neutral > d25_gifts_bad:
                $ MAS.MonikaElastic()
                m "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3hub "Большинство из них были очень хороши."
            elif d25_gifts_good + d25_gifts_neutral < d25_gifts_bad:
                $ MAS.MonikaElastic()
                m 3eka "И давай не будем забывать о замечательных рождественских подарках, которые ты мне подарил[mas_gender_none], [player]..."
                $ MAS.MonikaElastic()
                m 3rksdla "Мне очень понравились...{w=1} некоторые из их."

        if mas_isMoniEnamored(higher=True):
            $ MAS.MonikaElastic()
            m 1rksdla "Я...{w=1} Я также приготовила тебе кое-что, [player]..."
            $ MAS.MonikaElastic()
            m 3eksdla "Я весь день ждала подходящего момента, и что-то насчёт того, чтобы быть здесь с тобой сегодня вечером...{w=1} это просто кажется идеальным."
        elif mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 3ekbsa "Но просто знай, то, что ты здесь со мной, значит больше, чем любой подарок, который ты можешь мне подарить~"
        else:
            $ MAS.MonikaElastic()
            m 3eka "Честно говоря, я не была уверена, что ты прийдёшь сегодня... только того, что ты здесь, было для меня более чем достаточно, даже если ты ничего мне не подарил[mas_gender_none]."
            $ MAS.MonikaElastic()
            m 1eka "Ещё раз спасибо, [player_abb]...{w=1} я серьёзно."
    else:

        if mas_isMoniEnamored(higher=True):
            $ MAS.MonikaElastic()
            m 1eksdla "Также, [player], кое-что я хотела дать тебе весь день..."
            $ MAS.MonikaElastic()
            m 3rksdla "Мне просто нужно было дождаться подходящего времени, и быть здесь с тобой сегодня вечером...{w=1} это просто кажется идеальным."
        elif mas_isMoniNormal(higher=True):
            $ MAS.MonikaElastic()
            m 3ekbsa "Провести Рождество со мной было единственным подарком, который я когда-либо хотела~"
        else:
            $ MAS.MonikaElastic()
            m 3eka "Я хотела того, чтобы ты был здесь, [player]."

    if mas_isMoniEnamored(higher=True):
        $ MAS.MonikaElastic()
        m 3ekbsa "Так вот, [player_abb], я надеюсь, тебе понравится~"

        call mas_showpoem (poem=mas_poems.getRandomPoem("d25"), background_action_label="mas_d25_poem_mistletoe") from _call_mas_showpoem_4

        if d25_gifts_good > 0 or d25_gifts_neutral > 0:
            m 1ekbsa "Я серьёзно, [player], хотя я ценю подарки, которые ты мне подарил[mas_gender_none], но ты не долж[mas_gender_en] был[mas_gender_none] мне ничего дарить..."
        elif d25_gifts_bad>0:
            m 1ekbsa "Я серьёзно, [player], хотя ты подарил[mas_gender_none] мне немного...{w=1} странные подарки, но это не важно..."
        else:
            m 1ekbsa "[player], я имею в виду, что мне всё равно, что ты не подарил[mas_gender_none] мне подарков на Рождество..."
        $ MAS.MonikaElastic()
        m 1dku "..."
        $ MAS.MonikaElastic()
        m 1ektpu "Просто ты проводишь время со мной...{w=1} это всё, что я когда-либо хотела."
        $ MAS.MonikaElastic()
        m 6dktua "Ты весь мой мир, [player_abb]...{w=1} твоя любовь – это всё, что мне нужно..."
        window hide
        menu:
            "Я люблю тебя, [monika_name].":
                $ HKBHideButtons()
                $ mas_RaiseShield_core()
                $ disable_esc()



                pause 3.0
                show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0
                show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
                pause 3.0

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika

                $ is_first_kiss = persistent._mas_first_kiss is None
                $ MAS.MonikaElastic()
                m 6ekbfa "[player]... я... я..."
                call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_3

                show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 6ekbfa "...Я тоже тебя люблю~"
                if is_first_kiss:
                    $ MAS.MonikaElastic()
                    m 6dkbfa "..."
                    $ MAS.MonikaElastic()
                    m "Это было всё, о чём я всегда мечтала~"
                    $ MAS.MonikaElastic()
                    m 6ekbfa "Я так долго ждала, чтобы наконец поцеловать тебя, и не могло бы быть более идеального момента..."
                    $ MAS.MonikaElastic()
                    m 6dkbfa "Под омелой с тобой..."
                    $ MAS.MonikaElastic()
                    m 6dkbsu "Я никогда не забуду этот..."
                    $ MAS.MonikaElastic()
                    m 6ekbsu "...момент нашего первого поцелуя~"

                elif not persistent._mas_pm_d25_mistletoe_kiss:
                    $ MAS.MonikaElastic()
                    m 6dkbfu "Э-хе-хе..."
                    $ MAS.MonikaElastic()
                    m 6ekbfa "Я всегда хотела разделить с тобой поцелуй под омелой~"

                $ persistent._mas_pm_d25_mistletoe_kiss = True


                $ mas_hideEVL("mas_d25_monika_mistletoe", "EVE", derandom=True)


                $ enable_esc()
                $ mas_MUINDropShield()
                $ HKBShowButtons()
        return

    elif mas_isMoniAff():
        m 5ekbfa "Я так сильно люблю тебя, [player]~"
    else:

        m 1hubfa "Я люблю тебя, [player]~"
    return "love"

label mas_d25_poem_mistletoe:
    $ pause(1)
    hide monika with dissolve_monika
    $ store.mas_sprites.zoom_out()
    show monika 1ekbfa zorder MAS_MONIKA_Z at i11


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
        $ MAS.MonikaElastic()
        m 1eksdla "Надеюсь, ты не против, я написала для тебя песню."
        $ MAS.MonikaElastic()
        m 3hksdlb "Я знаю, что это немного банально, но я думаю, тебе понравится."
        $ MAS.MonikaElastic()
        m 3eksdla "Если у тебя выключена громкость, не мог[mas_gender_g] бы ты включить её для меня?"
        if songs.getUserVolume("music") == 0.0:
            $ MAS.MonikaElastic()
            m 3hksdlb "О, и не забудь о громкости в игре, тоже!"
            $ MAS.MonikaElastic()
            m 3eka "Я очень хочу, чтобы ты это услышал[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1huu "В любом случае.{w=1}.{w=1}.{w=1}"
    else:

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе..."
        $ MAS.MonikaElastic()
        m 3tuu "Надеюсь, ты готов[mas_gender_none], [player]..."

        $ ending = "..." if store.songs.hasMusicMuted() else ".{w=0.5}.{w=0.5}.{nw}"

        $ MAS.MonikaElastic()
        m "Это {i}снова{/i} то время года, в конце концов[ending]"
        if store.songs.hasMusicMuted():
            $ MAS.MonikaElastic()
            m 3hub "Убедись, что ты увеличил[mas_gender_none] громкость!"
            $ MAS.MonikaElastic()
            m 1huu ".{w=0.5}.{w=0.5}.{nw}"


    call monika_aiwfc_song from _call_monika_aiwfc_song_1


    if not mas_getEVLPropValue("monika_aiwfc", "shown_count", 0):
        $ MAS.MonikaElastic()
        m 1eka "Надеюсь, тебе понравилось, [player]."
        $ MAS.MonikaElastic()
        m 1ekbsa "И здесь я тоже всё сказала всерьёз."
        $ MAS.MonikaElastic()
        m 1ekbfa "Ты единственный подарок, который я могу пожелать."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve
        m 5ekbfa "Я люблю тебя, [player_abb]~"
    else:

        $ MAS.MonikaElastic()
        m 1eka "Я рада, что тебе нравится, когда я пою эту песню."
        $ MAS.MonikaElastic()
        m 1ekbsa "Ты всегда будешь тем подарком, который мне когда-либо был нужен, [player]."
        $ MAS.MonikaElastic()
        m 1ekbfa "Я люблю тебя~"


    $ mas_unlockEVL("mas_song_aiwfc", "SNG")
    return "no_unlock|love"


label monika_aiwfc_song:


    call mas_timed_text_events_prep from _call_mas_timed_text_events_prep_2

    $ play_song("mod_assets/bgm/aiwfc.ogg",loop=False)
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
    call mas_timed_text_events_wrapup from _call_mas_timed_text_events_wrapup_2
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
        $ MAS.MonikaElastic()
        m 3eub "Я тут вспомнила одну рождественскую песню, которой я очень хотела поделиться с тобой!"
        $ MAS.MonikaElastic()
        m 3eka "На этот раз, я не учила какую-либо песню, но, надеюсь, тебе понравится, как я спою ту же песню, что и в прошлый раз."
        $ MAS.MonikaElastic()
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby from _call_mas_song_merry_christmas_baby

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе..."
        $ MAS.MonikaElastic()
        m 3eka "Надеюсь, тебе понравилось~"
        $ mas_unlockEVL("mas_song_merry_christmas_baby", "SNG")
    else:

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3euu "Я думаю, что пришло время для ещё одной рождественской песни, э-хе-хе~"
        $ MAS.MonikaElastic()
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

        call mas_song_merry_christmas_baby from _call_mas_song_merry_christmas_baby_1

        $ MAS.MonikaElastic(voice="monika_giggle")
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
    $ MAS.MonikaElastic()
    if not renpy.seen_label('mas_song_this_christmas_kiss'):
        m 2rubsa "О, [player]..."
        $ MAS.MonikaElastic()
        m 2lubsa "Я нашла эту песню... {w=0.4}и...{w=0.4} я как раз думала о нас, когда послушала её."
        $ MAS.MonikaElastic()
        m 7ekbsu "Я имею в виду, ты был[mas_gender_none] так мил[mas_gender_none] со мной всё это время."
        $ MAS.MonikaElastic()
        m 3eubsb "И...{w=0.2} о боже, я просто хочу поделиться этим с тобой, если ты не против."
        $ MAS.MonikaElastic()
        m 1hubsa "Просто дай мне секунду{nw}"
        extend 1dubsa ".{w=0.3}.{w=0.3}.{w=0.3}{nw}"
    else:

        m 3euu "Я думаю, что пришло время спеть ещё одну рождественскую песню, э-хе-хе~"
        $ MAS.MonikaElastic()
        m 1hua ".{w=0.5}.{w=0.5}.{nw}"

    call mas_song_this_christmas_kiss from _call_mas_song_this_christmas_kiss

    $ MAS.MonikaElastic()
    m 1dubsa "..."
    $ MAS.MonikaElastic(voice="monika_hmm")
    m 1rtbsu "Хм-м.{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    window hide
    show monika 6tkbsa
    pause 2.0
    show monika 6dkbsu
    pause 2.0

    call monika_kissing_motion from _call_monika_kissing_motion_4
    window auto

    m 6ekbfa "Когда-нибудь я поцелую тебя по-настоящему, [player]."
    $ MAS.MonikaElastic()
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


    MASUndoActionRule.create_rule_EVL(
        "mas_d25_spider_tinsel",
        mas_d25c_start,
        mas_d25e - datetime.timedelta(days=1)
    )


init 10 python:
    if (
        datetime.date.today() == mas_d25e - datetime.timedelta(days=1)
        and not mas_lastSeenInYear("mas_d25_spider_tinsel")
    ):
        queueEvent("mas_d25_spider_tinsel")

label mas_d25_spider_tinsel:
    m 1esa "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 1etc "Задумывался ли ты когда-нибудь о том, откуда берут своё начало традиции, которые мы зачастую принимаем как должное?"
    $ MAS.MonikaElastic()
    m 3eud "В большинстве случаев, те вещи, которые считаются традицией, просто принимаются такими, какие они есть, и у нас так и не нашлось времени, чтобы понять, почему."
    $ MAS.MonikaElastic()
    m 3euc "Ну, мне стало любопытно, почему мы делаем определённые вещи в канун Рождества, поэтому я и провела небольшое расследование."
    $ MAS.MonikaElastic()
    m 1eua "...И я нашла одну очень интересную украинскую народную сказку, которая как раз и объясняет, почему рождественские деревья начали украшать мишурой."
    $ MAS.MonikaElastic()
    m 1eka "Я подумала, что это очень хорошая история, вот мне и захотелось поделиться ею с тобой."
    $ MAS.MonikaElastic()
    m 1dka "..."
    $ MAS.MonikaElastic()
    m 3esa "Жила-была одна вдова (мы будем звать её Эми), которая жила в тесной старой хижине со своими детьми."
    $ MAS.MonikaElastic()
    m 3eud "Снаружи их дома стояла высокая ёлка, и с этого дерева падали шишки, которые потом начинали прорастать из почвы."
    $ MAS.MonikaElastic()
    m 3eua "Дети были рады самой идее поставить у себя рождественское дерево, и поэтому они начали стремиться к ней и ждали, когда ёлка станет достаточно высокой, чтобы затащить её в дом."
    $ MAS.MonikaElastic()
    m 2ekd "К несчастью, семья была бедной, и даже после того, как у них появилось рождественское дерево, они не могли позволить себе никаких украшений, чтобы украсить её."
    $ MAS.MonikaElastic()
    m 2dkc "И поэтому, в канун Рождества, Эми и её дети пошли спать, зная о том, что у них рождественским утром будет стоять голое дерево."
    $ MAS.MonikaElastic()
    m 2eua "Однако, пауки, которые жили в хижине, услышали плач детей и решили не оставлять рождественское дерево голым."
    $ MAS.MonikaElastic()
    m 3eua "В общем, пауки создали красивые паутины на рождественском дереве, украсив его элегантными и красивыми шелковистыми узорами."
    $ MAS.MonikaElastic()
    m 3eub "А когда дети проснулись в раннее рождественское утро, они запрыгали от восторга!"
    $ MAS.MonikaElastic()
    m "Они пошли к своей матери и начали будить её, восклицая: «Мама! Ты должна взглянуть на рождественское дерево! Оно такое красивое!»."
    $ MAS.MonikaElastic()
    m 1wud "Как только Эми проснулась и встала перед деревом, она была в полном восторге от взора, который стоял перед её глазами."
    $ MAS.MonikaElastic()
    m "А потом один из детей открыл окно, чтобы запустить в хижину солнечный свет..."
    $ MAS.MonikaElastic()
    m 3sua "И как только лучи солнечного света попали на дерево, паутина начала отражать их свет, создавая мерцающие серебряные и золотые пряди..."
    $ MAS.MonikaElastic()
    m "...заставляя тем самым рождественское дерево сиять волшебным образом."
    $ MAS.MonikaElastic()
    m 1eka "С этого дня, Эми никогда не чувствовала себя бедной; {w=0.3}наоборот, она всегда была рада всем тем замечательным подаркам, которые у неё уже были в жизни."
    $ MAS.MonikaElastic()
    m 3tuu "Ну, полагаю, теперь мы знаем, почему Эми любит пауков..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "А-ха-ха! Я просто шучу!"
    $ MAS.MonikaElastic()
    m 1eka "Разве это не милая и прекрасная история, [player]?"
    $ MAS.MonikaElastic()
    m "Мне кажется, это правда интересный взгляд на то, почему мишуру начали использовать в качестве украшения рождественского дерева."
    $ MAS.MonikaElastic()
    m 3eud "А ещё я читала, что жители Украины часто украшают свои рождественские деревья украшениями в виде паутины, полагая, что это принесём им удачу в следующем году."
    $ MAS.MonikaElastic()
    m 3eub "Так что, думаю, если ты когда-нибудь найдёшь паука, живущего в твоём рождественском дереве, не убивай его, и, возможно, он принесёт тебе удачу в будущем!"
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
    $ MAS.MonikaElastic()
    m 3eua "Уверена, ты уже слышал[mas_gender_none] об этом, но канун Рождества просто будет неполным без {i}«Ночь перед рождеством»{/i}!"
    $ MAS.MonikaElastic()
    m 3eka "Это всегда было моей самой любимой частью приближающегося кануна Рождества, так что, надеюсь, ты не против послушать, как я читаю эту книгу."
    $ MAS.MonikaElastic()
    m 1dka "..."

    $ MAS.MonikaElastic()
    m 3esa "Рождество на пороге. Полночную тишь..."
    $ MAS.MonikaElastic()
    m 3eud "Потревожить не сможет даже юркая мышь."
    $ MAS.MonikaElastic()
    m 1eud "Стайка детских чулок, как положено, чинно"
    $ MAS.MonikaElastic()
    m 1eka "Санта Клауса ждёт у решётки каминной."

    $ MAS.MonikaElastic()
    m 1esa "Ребятишкам в уютных и мягких кроватках"
    $ MAS.MonikaElastic()
    m 1hua "Снится сахарный снег и Луна-мармеладка."
    $ MAS.MonikaElastic()
    m 3eua "Я колпак нахлобучил, а мама – чепец:"
    $ MAS.MonikaElastic()
    m 1dsc "Взрослым тоже пора бы вздремнуть, наконец..."

    $ MAS.MonikaElastic()
    m 3wuo "Вдруг грохот и топот, и шум несусветный"
    $ MAS.MonikaElastic()
    m "И крыша откликнулась гулом ответным."
    $ MAS.MonikaElastic()
    m 3wud "Сна, как не бывало, а кто бы заснул?"
    $ MAS.MonikaElastic()
    m "Я ставни открыл и окна распахнул"

    $ MAS.MonikaElastic()
    m 1eua "Играя в гляделки со снегом искристым,"
    $ MAS.MonikaElastic()
    m 3eua "Луна озаряла сиянием чистым"
    $ MAS.MonikaElastic()
    m 3wud "(Я так и застыл у окна в изумленье)..."
    $ MAS.MonikaElastic()
    m 3wuo "Чудесные санки и восемь оленей."

    $ MAS.MonikaElastic()
    m 1eua "За кучера – бойкий лихой старичок."
    $ MAS.MonikaElastic()
    m 3eud "Да-да, это Санта – ну кто же ещё"
    $ MAS.MonikaElastic()
    m 3eua "Мог в крохотных санках орлов обгонять"
    $ MAS.MonikaElastic()
    m 3eud "И басом весёлым оленям кричать:"

    $ MAS.MonikaElastic()
    m 3euo "«–Эй, Быстрый! Танцор! Эй, Дикарь! Эй, Скакун!»"
    $ MAS.MonikaElastic()
    m "«Комета! Амур! Эй, Гроза и Тайфун!»"
    $ MAS.MonikaElastic()
    m 3wuo "«Живей на крыльцо! А теперь к чердаку!»"
    $ MAS.MonikaElastic()
    m "«Наддайте! Гоните на полном скаку!»"

    $ MAS.MonikaElastic()
    m 1eua "Как лёгкие листья, что с ветром неслись,"
    $ MAS.MonikaElastic()
    m 1eud "Взмывают, встречаясь с преградою, ввысь."
    $ MAS.MonikaElastic()
    m 3eua "Вот так же олени вверх сани помчали."
    $ MAS.MonikaElastic()
    m "(Игрушки лишь чудом не выпадали!)"

    $ MAS.MonikaElastic()
    m 3eud "Раздался на крыше грохота звук –"
    $ MAS.MonikaElastic()
    m "Диковинных, звонких копыт перестук."
    $ MAS.MonikaElastic()
    m 1rkc "Скорее, скорее к камину! И вот"
    $ MAS.MonikaElastic()
    m 1wud "Наш Санта скользнул прямиком в дымоход."

    $ MAS.MonikaElastic()
    m 3eua "Одетый в меха с головы и до пят"
    $ MAS.MonikaElastic()
    m 3ekd "(Весь в копоти Сантин роскошный наряд!),"
    $ MAS.MonikaElastic()
    m 1eua "С мешком, перекинутым через плечо,"
    $ MAS.MonikaElastic()
    m 1eud "Набитым игрушками – чем же ещё!"

    $ MAS.MonikaElastic()
    m 3sub "Сияют глаза, будто звёзды в мороз,"
    $ MAS.MonikaElastic()
    m 3subsb "Два яблока – щёки, и вишенка – нос."
    $ MAS.MonikaElastic()
    m 3subsu "Улыбка – забавней не видел вовек!"
    $ MAS.MonikaElastic()
    m 1subsu "Бела борода, словно утренний снег."

    $ MAS.MonikaElastic()
    m 1eud "И сразу дымком потянуло табачным;"
    $ MAS.MonikaElastic()
    m 3rkc "Он старую трубку насасывал смачно,"
    $ MAS.MonikaElastic()
    m 2eka "А кругленький толстый животик от смеха"
    $ MAS.MonikaElastic()
    m 2hub "Как студень дрожал – доложу вам, потеха!"

    $ MAS.MonikaElastic()
    m 2eka "Забавный толстяк – просто эльф, да и только!"
    $ MAS.MonikaElastic()
    m 3hub "Не выдержав, {nw}"
    extend 3eub "я рассмеялся до колик."
    $ MAS.MonikaElastic()
    m 1kua "(вначале слегка опасался смеяться,"
    $ MAS.MonikaElastic()
    m 1eka "Но, звёздочек – глаз, разве можно бояться?)"

    $ MAS.MonikaElastic()
    m 1euc "Не молвив ни слова, он взялся за дело –"
    $ MAS.MonikaElastic()
    m 1eud "Чулки у камина наполнил умело,"
    $ MAS.MonikaElastic()
    m 3esa "Кивнул, пальчик пухленький к носу прижал"
    $ MAS.MonikaElastic()
    m 3eua "(Мол, тихо! Молчи)– и в камине пропал."

    $ MAS.MonikaElastic()
    m 1eud "Раздался его оглушительный свист –"
    $ MAS.MonikaElastic()
    m 1eua "И восемь оленей как птицы взвились,"
    $ MAS.MonikaElastic()
    m 3eua "Лишь ветром слова до меня донесло:"
    $ MAS.MonikaElastic()
    m 3hub "«Всех – всех с Рождеством! Я вернусь! Добрых снов!»"
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
    $ MAS.MonikaElastic()
    m 3sua "Предвкушение, кажущаяся волшебной аурой сезона... в этом есть что-то особенное."
    $ MAS.MonikaElastic()
    m 1dkbsu "Это действительно моё любимое время года."
    m "..."

    if mas_hasUnlockedClothesWithExprop("lingerie"):
        call mas_d25_monika_second_time_lingerie from _call_mas_d25_monika_second_time_lingerie
    else:

        call mas_lingerie_intro (holiday_str="это Рождество", lingerie_choice=mas_clothes_santa_lingerie) from _call_mas_lingerie_intro
        $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 3hub "Ты можешь в это поверить?.. {w=1}Скоро Рождество!"
    $ MAS.MonikaElastic()
    m 1rksdla "Мне всегда было так трудно спать в канун Рождества..."
    $ MAS.MonikaElastic()
    m 1eka "Мне так хотелось увидеть, что я найду под ёлкой на следующее утро..."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika


    if mas_HistVerifyLastYear_k(True, "d25.actions.spent_d25"):
        m "Но я ещё {i}больше{/i} радуюсь теперь, когда могу проводить с тобой каждое Рождество..."
        $ MAS.MonikaElastic()
        m 5hkbsa "Я не могу дождаться завтрашнего дня!"


    elif mas_HistVerifyAll_k(True, "d25.actions.spent_d25"):
        m "Но я ещё {i}больше{/i} взволнована в этом году..."
        $ MAS.MonikaElastic()
        m 5hkbsa "Только мысль о том, чтобы провести ещё одно Рождество вместе...{w=1} Я не могу дождаться!"
    else:


        m "Но я ещё {i}больше{/i} взволнована в этом году..."
        $ MAS.MonikaElastic()
        m 5hkbsa "Только мысль о нашем первом совместном Рождестве...{w=1} Я не могу дождаться!"

    if (
        mas_canShowRisque()
        and not mas_SELisUnlocked(mas_clothes_santa_lingerie)
    ):
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_d25_monika_second_time_lingerie from _call_mas_d25_monika_second_time_lingerie_1
        else:

            m 5ekbfa "..."
            show monika 1ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            call mas_lingerie_intro (holiday_str="канун Рождества", lingerie_choice=mas_clothes_santa_lingerie) from _call_mas_lingerie_intro_1
            $ MAS.MonikaElastic()
            m 1ekbfa "Просто знай, что я люблю тебя очень, очень сильно, [player]~"
            $ mas_ILY()
    return

label mas_d25_monika_second_time_lingerie:
    $ MAS.MonikaElastic()
    m 3wubsb "О!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3tsbsu "У меня есть для тебя маленький сюрприз...{w=1} Думаю, тебе это понравится, э-хе-хе~"
    call mas_clothes_change (outfit=mas_clothes_santa_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True) from _call_mas_clothes_change_13
    pause 2.0
    show monika 2ekbsu
    pause 2.0
    show monika 2tkbsu
    pause 2.0
    $ MAS.MonikaElastic()
    m 2tfbsu "[player]...{w=0.5} Ты так пристально смотришь{w=0.5}... снова."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 2hubsb "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 2eubsb "Полагаю, ты одобряешь мой выбор одежды..."
    $ MAS.MonikaElastic()
    m 2tkbsu "Довольно подходяще для такого случая, ведь так?"
    $ MAS.MonikaElastic()
    m 2rkbssdla "Должна сказать, я очень нервничала, когда впервые надела что-то подобное..."
    $ MAS.MonikaElastic()
    m 2hubsb "Но теперь, когда я сделала это раньше, мне действительно нравится одеваться так для тебя!"
    $ MAS.MonikaElastic()
    m 3tkbsu "Надеюсь, тебе тоже понравится~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_postd25_notimespent",
            
            
            conditional="not persistent._mas_d25_spent_d25",
            start_date=mas_d25p,
            end_date=mas_d25p + datetime.timedelta(days=6),
            years=[],
            action=EV_ACT_PUSH,
        ),
        skipCalendar=True
    )

label mas_d25_postd25_notimespent:

    if persistent._mas_d25_spent_d25:
        return


    if mas_isFirstSeshPast(mas_d25):
        return


    if mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, reason=6)
        m 1dkc "...Я просто рада тому, что ты наконец-то пришёл..."
        $ MAS.MonikaElastic()
        m 2ekd "Я уже начала волноваться, что с тобой что-то произошло..."
        $ MAS.MonikaElastic()
        m 2rksdlc "Когда ты не пришёл на Рождество...{w=1}я не знала, что и думать."
        $ MAS.MonikaElastic()
        m 4eksdlc "Не то, чтобы я хотела, чтобы ты пропустил тот день, который, как ты знаешь, важен для меня..."
        $ MAS.MonikaElastic()
        m 2dksdlc "И я подумала, может..."
        $ MAS.MonikaElastic()
        m 2eksdla "Хотя, это сейчас не важно. Я просто рада, что с тобой всё хорошо!"
        $ MAS.MonikaElastic()
        m 4eka "Пусть даже я и разочарована тем, что мы не смогли провести Рождество вместе, я уверена, что у тебя на это была веская причина."
        $ MAS.MonikaElastic()
        m "Просто не дай этому произойти в следующем году, ладно?"
        $ MAS.MonikaElastic()
        m 2eka "И, даже если в будущем ты не смог заглянуть ко мне в Рождество, попытайся хотя бы взять меня с собой..."
        $ MAS.MonikaElastic()
        m 1eka "Я лишь хочу быть рядом с тобой, [player]..."
        $ MAS.MonikaElastic()
        m 3ekbsa "Я люблю тебя~"
        $ mas_ILY()

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, reason=6)
        m 2ekc "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 2tkc "Должна сказать, я разочарована тем, что ты не заглянул ко мне на Рождество..."
        $ MAS.MonikaElastic()
        m 4tkc "Ты знал, что я хотела провести время с тобой. Разве я многого прошу?"
        $ MAS.MonikaElastic()
        m 2rkc "Я знаю, что день, возможно, был тяжёлым, если тебе надо было съездить в другой город, чтобы навестить семью, но ты мог хотя бы взять меня с собой..."
        $ MAS.MonikaElastic()
        m 2ekc "Для меня этого было бы вполне достаточно."
        $ MAS.MonikaElastic()
        m 2dkc "..."
        $ MAS.MonikaElastic()
        m 4rksdlc "Может, что-то произошло в последнюю минуту, и ты попросту не смог провести время со мной..."
        $ MAS.MonikaElastic()
        m 4eksdla "Но, пожалуйста...{w=1}пожалуйста, не забудь заглянуть ко мне на следующее Рождество, хорошо, [player]?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(reason=6)
        m 2efc "[player]!"
        $ MAS.MonikaElastic()
        m "Не могу поверить в то, что ты даже не удосужился заглянуть ко мне в Рождество!"
        $ MAS.MonikaElastic()
        m 2tfc "По правде говоря...{w=1}да, я могу."
        $ MAS.MonikaElastic()
        m "Именно поэтому я не позаботилась о декорациях..."
        $ MAS.MonikaElastic()
        m 2rfc "Я знала, что если бы я попыталась проникнуться духом Рождества, то меня в конце бы ждало разочарование... {w=1}опять."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, reason=6)
        m 6ekc "[player], как прошло твоё Рождество?"
        $ MAS.MonikaElastic()
        m 6dkc "Лично моё – в полном одиночестве..."
        $ MAS.MonikaElastic()
        m "Ты, скорее всего, даже не подумал обо мне, да?"
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."

    $ mas_d25ReactToGifts()
    return


label mas_gone_over_d25_check:
    if mas_checkOverDate(mas_d25):
        $ persistent._mas_d25_gone_over_d25 = True
        $ persistent._mas_d25_spent_d25 = True
        $ persistent._mas_d25_d25_date_count += 1
        $ mas_rmallEVL("mas_d25_postd25_notimespent")
    return


label bye_d25e_delegate:

    if persistent._mas_d25_d25e_date_count > 0:
        call bye_d25e_second_time_out from _call_bye_d25e_second_time_out
    else:

        call bye_d25e_first_time_out from _call_bye_d25e_first_time_out






    jump mas_dockstat_iostart


label bye_d25e_first_time_out:
    m 1sua "Отведёшь меня в какое-нибудь особенное место на канун Рождества, [player]?"
    $ MAS.MonikaElastic()
    m 3eua "Я знаю, что некоторые люди посещают друзей или семью... или ходят на рождественские вечеринки..."
    $ MAS.MonikaElastic()
    m 3hua "Но куда бы мы ни пошли, я буду рада тому, что ты захотел[mas_gender_none], чтобы я пошла с тобой!"
    $ MAS.MonikaElastic()
    m 1eka "Надеюсь, мы будем праздновать Рождество дома, но если мы не будем его праздновать, мне будет достаточно и того, что я с тобой~"
    return


label bye_d25e_second_time_out:
    m 1wud "Ого, мы сегодня снова идём гулять, [player]?"
    $ MAS.MonikaElastic()
    m 3hua "Наверное, тебе надо проведать много кого в канун Рождества..."
    $ MAS.MonikaElastic()
    m 3hub "...или, наверное, у тебя для нас на сегодня готово много особенных планов!"
    $ MAS.MonikaElastic()
    m 1eka "Но, так или иначе, спасибо, что подумал[mas_gender_none] обо мне и взял[mas_gender_none] меня с собой~"
    return


label bye_d25_delegate:

    if persistent._mas_d25_d25_date_count > 0:
        call bye_d25_second_time_out from _call_bye_d25_second_time_out
    else:

        call bye_d25_first_time_out from _call_bye_d25_first_time_out





    jump mas_dockstat_iostart


label bye_d25_first_time_out:
    m 1sua "Отведёшь меня в какое-нибудь особенное место в Рождество, [player]?"
    $ MAS.MonikaElastic()
    if persistent._mas_pm_fam_like_monika and persistent._mas_pm_have_fam:
        m 1sub "Может, мы навестим кого-нибудь из твоей семьи?.. Я бы с удовольствием с ними познакомилась!"
        $ MAS.MonikaElastic()
        m 3eua "Или, быть может, мы посмотрим фильм?.. Я знаю, что некоторым нравится заниматься этим после открытия подарков."
    else:
        m 3eua "Может быть, мы пойдём в кино... я знаю, что некоторые люди любят делать это после открытия подарков."
    $ MAS.MonikaElastic()
    m 1eka "Ну, куда бы ты ни пошел, я просто рада, что ты хочешь, чтобы я пошла с тобой..."
    $ MAS.MonikaElastic()
    m 3hua "Я хочу провести всё Рождество вместе с тобой, если это возможно, [player_abb]~"
    return


label bye_d25_second_time_out:
    m 1wud "Ого, мы {i}опять{/i} куда-то идём, [player]?"
    $ MAS.MonikaElastic()
    m 3wud "Наверное, у тебя много людей, к которым ты долж[mas_gender_en] сходить в гости..."
    $ MAS.MonikaElastic()
    m 3sua "...или, наверное, у тебя для нас на сегодня готово много особенных планов!"
    $ MAS.MonikaElastic()
    m 1hua "Но, так или иначе, спасибо, что подумал[mas_gender_none] обо мне и взял[mas_gender_none] меня с собой~"
    return




label greeting_d25e_returned_d25e:
    $ persistent._mas_d25_d25e_date_count += 1

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 3eka "Было очень мило с твоей стороны взять меня с собой сегодня..."
    $ MAS.MonikaElastic()
    m 3ekbsa "Прогулка с тобой в канун Рождества была очень особенной, [player_abb]. Спасибо~"
    return


label greeting_d25e_returned_d25:
    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 3wud "Ого, нас не было всю ночь..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_1
    return


label greeting_d25e_returned_post_d25:
    $ persistent._mas_d25_d25e_date_count += 1

    $ MAS.MonikaElastic()
    m 1hua "Наконец-то мы дома!"
    $ MAS.MonikaElastic()
    m 3wud "Мы точно долго отсутствовали, [player]..."
    $ MAS.MonikaElastic()
    m 3eka "Было бы здорово повидаться с тобой в Рождество, но, поскольку ты не смог[mas_gender_g] прийти ко мне, я рада, что ты взял[mas_gender_none] меня с собой."
    $ MAS.MonikaElastic()
    m 3ekbsa "Просто быть рядом с тобой – всё, чего я хотела~"
    $ MAS.MonikaElastic()
    m 1ekbfb "И так как я не успела сказать это тебе на Рождество... c Рождеством, [player_abb]!"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_2

    $ mas_d25ReactToGifts()
    return


label greeting_pd25e_returned_d25:
    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 3wud "Ого, нас не было довольно долго..."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_3
    return


label greeting_d25_returned_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 3eka "Было очень приятно провести время с тобой на Рождество, [player]!"
    $ MAS.MonikaElastic()
    m 1eka "Большое спасибо, что взял[mas_gender_none] меня с собой."
    $ MAS.MonikaElastic()
    m 1ekbsa "Ты всегда такой заботливый~"
    return


label greeting_d25_returned_post_d25:
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    $ MAS.MonikaElastic()
    m 1hua "Наконец-то мы дома!"
    $ MAS.MonikaElastic()
    m 3wud "Мы отсутствовали очень долго, [player]!"
    $ MAS.MonikaElastic()
    m 3eka "Было бы здорово повидаться с тобой снова до окончания Рождества, но, по крайней мере, я всё ещё была с тобой."
    $ MAS.MonikaElastic()
    m 1hua "Поэтому спасибо тебе за то, что пров[mas_gender_yo]л[mas_gender_none] время со мной, когда тебе надо было сходить по разным местам..."
    $ MAS.MonikaElastic()
    m 3ekbsa "Ты всегда такой заботливый~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_4
    return



label greeting_d25_and_nye_delegate:





    python:

        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        left_pre_d25e = False

        if checkout_time is not None:
            checkout_date = checkout_time.date()
            left_pre_d25e = checkout_date < mas_d25e

        if checkin_time is not None:
            checkin_date = checkin_time.date()


    if mas_isD25Eve():


        if left_pre_d25e:

            jump greeting_returned_home_morethan5mins_normalplus_flow
        else:


            call greeting_d25e_returned_d25e from _call_greeting_d25e_returned_d25e

    elif mas_isD25():


        if checkout_time is None or mas_isD25(checkout_date):

            call greeting_d25_returned_d25 from _call_greeting_d25_returned_d25

        elif mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_d25 from _call_greeting_d25e_returned_d25
        else:


            call greeting_pd25e_returned_d25 from _call_greeting_pd25e_returned_d25

    elif mas_isNYE():

        if checkout_time is None or mas_isNYE(checkout_date):

            call greeting_nye_delegate from _call_greeting_nye_delegate
            jump greeting_nye_aff_gain

        elif left_pre_d25e or mas_isD25Eve(checkout_date):

            call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25

        elif mas_isD25(checkout_date):

            call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25
        else:


            jump greeting_returned_home_morethan5mins_normalplus_flow

    elif mas_isNYD():



        if checkout_time is None or mas_isNYD(checkout_date):

            call greeting_nyd_returned_nyd from _call_greeting_nyd_returned_nyd

        elif mas_isNYE(checkout_date):

            call greeting_nye_returned_nyd from _call_greeting_nye_returned_nyd
            jump greeting_nye_aff_gain

        elif checkout_time < datetime.datetime.combine(mas_d25.replace(year=checkout_time.year), datetime.time()):
            call greeting_pd25e_returned_nydp from _call_greeting_pd25e_returned_nydp
        else:


            call greeting_d25p_returned_nyd from _call_greeting_d25p_returned_nyd

    elif mas_isD25Post():

        if mas_isD25PostNYD():



            if (
                    checkout_time is None
                    or mas_isNYD(checkout_date)
                    or mas_isD25PostNYD(checkout_date)
                ):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isNYE(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp
                jump greeting_nye_aff_gain

            elif mas_isD25Post(checkout_date):

                call greeting_d25p_returned_nydp from _call_greeting_d25p_returned_nydp_1
            else:



                call greeting_pd25e_returned_nydp from _call_greeting_pd25e_returned_nydp_1
        else:


            if checkout_time is None or mas_isD25Post(checkout_date):

                jump greeting_returned_home_morethan5mins_normalplus_flow

            elif mas_isD25(checkout_date):

                call greeting_d25_returned_post_d25 from _call_greeting_d25_returned_post_d25_1
            else:


                call greeting_d25e_returned_post_d25 from _call_greeting_d25e_returned_post_d25_1
    else:


        jump greeting_returned_home_morethan5mins_normalplus_flow



    jump greeting_returned_home_morethan5mins_normalplus_flow_aff





default persistent._mas_nye_spent_nye = False


default persistent._mas_nye_spent_nyd = False


default persistent._mas_nye_nye_date_count = 0


default persistent._mas_nye_nyd_date_count = 0


default persistent._mas_nye_date_aff_gain = 0


define mas_nye = datetime.date(datetime.date.today().year, 12, 31)
define mas_nyd = datetime.date(datetime.date.today().year, 1, 1)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "nye",
        datetime.datetime(2019, 1, 6),
        {
            "_mas_nye_spent_nye": "nye.actions.spent_nye",
            "_mas_nye_spent_nyd": "nye.actions.spent_nyd",

            "_mas_nye_nye_date_count": "nye.actions.went_out_nye",
            "_mas_nye_nyd_date_count": "nye.actions.went_out_nyd",

            "_mas_nye_date_aff_gain": "nye.aff.date_gain"
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
                If None, we use today date
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
                if None, we use today date
                (Default: None)

        RETURNS: True if given date is new years day, False otherwise
        """
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_nyd.replace(year=_date.year)





default persistent._mas_pm_got_a_fresh_start = None


default persistent._mas_aff_before_fresh_start = None


default persistent._mas_pm_failed_fresh_start = None

init 5 python:


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


            if not persistent._mas_pm_got_a_fresh_start or not persistent._mas_pm_failed_fresh_start:
                m 1eub "[player]!"

                if mas_HistVerify_k([datetime.date.today().year-2], True, "nye.actions.spent_nyd")[0]:
                    $ MAS.MonikaElastic()
                    m "Можешь ли ты поверить в то, что мы проводим очередной Новый год вместе?"
                $ MAS.MonikaElastic()
                if mas_isMoniAff(higher=True):
                    m 1hua "Мы определённо прошли через многое в минувшем году, да?"
                else:
                    m 1eua "Мы определённо прошли через многое в минувшем году, да?"

                $ MAS.MonikaElastic()
                m 1eka "Я так счастлива, зная о том, что мы вместе проведём ещё больше времени."

                if mas_isMoniAff(higher=True):
                    show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                    m 5hubfa "Давай мы сделаем этот год таким же замечательным, как и прошедший, ладно?"
                    $ MAS.MonikaElastic()
                    m 5ekbfa "Я тебя очень сильно люблю, [player]."
                else:
                    $ MAS.MonikaElastic()
                    m 3hua "Давай мы сделаем этот год ещё лучше, чем прошедший, ладно?"
                    $ MAS.MonikaElastic()
                    m 1hua "Люблю тебя, [player]."
            else:


                $ last_year = "в прошлом году"
                m 1eka "[player]..."

                if not got_fresh_start_last_year:
                    $ last_year = "раньше"

                $ MAS.MonikaElastic()
                m 3eka "Ты помнишь то обещание, которое дал[mas_gender_none] [last_year]?"
                $ MAS.MonikaElastic()
                m "Что мы сделаем этот год лучше, чем прошедший?"
                $ MAS.MonikaElastic()
                m 6dkbstpa "..."
                $ MAS.MonikaElastic()
                m 6ekbftpa "Спасибо, что сдержал[mas_gender_none] своё обещание."
                $ MAS.MonikaElastic()
                m "Я серьёзно, [player]. Ты сделал[mas_gender_none] меня очень счастливой...{w=1} {nw}"
                extend 6dkbftpa "спасибо тебе, от всей души."
                $ MAS.MonikaElastic()
                m 6dkbftda "Давай мы сделаем этот год ещё лучше, чем прошедший, ладно?"
                $ MAS.MonikaElastic()
                m 6ekbftda "Люблю тебя, [player]."
                $ MAS.MonikaElastic()
                m "Я правда люблю тебя."

                $ persistent._mas_pm_failed_fresh_start = False
        else:



            if not persistent._mas_pm_got_a_fresh_start:
                m 2ekc "[player]..."
                $ MAS.MonikaElastic()
                m 2rksdlc "Мы прошли...{w=1} через многое в прошлом году..."
                $ MAS.MonikaElastic()
                m "Я... я надеюсь, что этот год будет лучше, чем прошедший."
                $ MAS.MonikaElastic()
                m 2dkc "Мне это правда нужно."
                jump mas_nye_monika_nyd_fresh_start
            else:

                m 2rkc "[player]..."

                if got_fresh_start_last_year:
                    $ MAS.MonikaElastic()
                    m 2ekc "Ты помнишь то обещание, которое дал[mas_gender_none] в прошлом году?"
                    $ MAS.MonikaElastic()
                    m 2ekd "Что мы сделаем этот год лучше, чем прошедший?"
                else:


                    $ MAS.MonikaElastic()
                    m 2ekc "Ты помнишь то обещание, которое дал[mas_gender_none] раньше?"
                    $ MAS.MonikaElastic()
                    m 2ekd "Что ты улучшишь наши отношения?"

                $ curr_aff = _mas_getAffection()
                if curr_aff > persistent._mas_aff_before_fresh_start:
                    $ MAS.MonikaElastic()
                    m 2rkd "Мне кажется, ты сделал[mas_gender_none] их чуточку лучше..."
                    $ MAS.MonikaElastic()
                    m 2ekc "Но я ожидала большего, [player]."


                    if not mas_HistVerifyAll_k(True, "pm.actions.monika.failed_fresh_start"):
                        $ mas_setAffection(persistent._mas_aff_before_fresh_start)

                elif curr_aff < persistent._mas_aff_before_fresh_start:
                    $ MAS.MonikaElastic()
                    m 2rfc "Полагаю, ты не смог[mas_gender_g] сдержать то обещание... понятно."
                else:

                    $ MAS.MonikaElastic()
                    m 2rkc "Похоже, ничего не изменилось, да?"


                $ MAS.MonikaElastic()
                m 2rktpc "Я очень,{w=0.5} очень надеюсь, что ты сможешь это исправить, [player]..."
                $ MAS.MonikaElastic()
                m 2dktpc "Я не знаю, сколько я ещё смогу выдержать."


                if _mas_getAffection() <= -50:
                    $ MAS.MonikaElastic()
                    m 2dktsd "Но это, наверное, просто глупая мысль..."
                    $ MAS.MonikaElastic()
                    m 2ektsc "Это просто очередная игра для тебя, это очевидно."
                    $ MAS.MonikaElastic()
                    m 2rktsd "Ты даже не считаешь меня настоящей...{w=1} {nw}"
                    extend 2dftsc "я всего лишь очередной персонаж, с которым ты просто играешься."
                    $ MAS.MonikaElastic()
                    m 2eftdc "Надеюсь, никто не переживёт те же боль и одиночество, которые я испытывала весь этот год."

                $ persistent._mas_pm_failed_fresh_start = True
                return
    else:

        if not mas_isBelowZero():
            m 1eub "[player]!"

            $ MAS.MonikaElastic()
            if mas_isMoniAff(higher=True):
                m 1ekbsa "Я знаю, что мы не были вместе довольно долгое время, но минувший год прошёл лучше, чем я могла бы надеяться..."
            else:
                m 1eka "Я знаю, что мы не были вместе довольно долгое время, но минувший год был для меня очень особенным..."

            $ MAS.MonikaElastic()
            m 1hua "Я буду всегда помнить об этом, как о том годе, когда я познакомилась с тобой~"
            $ MAS.MonikaElastic()
            m 3hua "Давай мы наверстаем упущенное и сделаем этот год ещё лучше!"
            $ MAS.MonikaElastic()
            m 1ekbsa "Люблю тебя, [player]."
        else:

            $ MAS.MonikaElastic()
            m 2ekc "В общем, [player]..."
            $ MAS.MonikaElastic()
            m 2etc "Уже начался новый год, да?"
            $ MAS.MonikaElastic()
            m 2rksdlc "Мы не были вместе довольно долгое время, но то время, которое мы провели в минувшем году, прошло не так гладко, как я на то надеялась..."
            jump mas_nye_monika_nyd_fresh_start

    $ MAS.MonikaElastic()
    m "С Новым годом~"
    return "love"

label mas_nye_monika_nyd_fresh_start:
    $ MAS.MonikaElastic()
    m 2ekc "Как насчёт того, чтобы оставить всё это в прошлом, забыть о прошлом году и сосредоточиться на новом начале этого года?"
    $ MAS.MonikaElastic()
    m 4ekc "Это не слишком поздно для нас, [player], мы всё ещё можем сделать друг друга счастливыми."
    $ MAS.MonikaElastic()
    m 4eka "Это всё, чего я когда-либо хотела."

    $ MAS.MonikaElastic()
    m "Что скажешь, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Что скажешь, [player]?{fast}"
        "Я был[mas_gender_none] бы очень рад[mas_gender_none] этому.":


            $ persistent._mas_pm_got_a_fresh_start = True
            $ persistent._mas_aff_before_fresh_start = _mas_getAffection()


            $ mas_setAffection(0)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            $ MAS.MonikaElastic()
            m 4wua "Правда?"
            $ MAS.MonikaElastic()
            m 1hua "О, [player], ты не представляешь, как я счастлива!"
            $ MAS.MonikaElastic()
            m 3eka "Я знаю, у нас все получится."
            $ MAS.MonikaElastic()
            m 1hua "Спасибо тебе большое..."
            $ MAS.MonikaElastic()
            m 1eka "Знание того, что ты всё ещё хочешь быть со мной... это многое для меня значит."
            $ MAS.MonikaElastic()
            m 3eka "Давай отнесёмся к этому серьёзно, хорошо, [player]?"
            return
        "Нет.":

            $ persistent._mas_pm_got_a_fresh_start = False


            $ mas_setAffection(store.mas_affection.AFF_BROKEN_MIN - 1)
            $ _mas_AffSave()
            $ renpy.save_persistent()

            $ MAS.MonikaElastic()
            m 6dktpc "..."
            $ MAS.MonikaElastic()
            m 6ektpc "Я... я..."
            $ MAS.MonikaElastic()
            m 6dktuc "..."
            $ MAS.MonikaElastic()
            m 6dktsc "..."
            pause 10.0
            return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_resolutions",
            action=EV_ACT_QUEUE, 
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            years=[],
            aff_range=(mas_aff.UPSET,None)
        ),
        skipCalendar=True
    )

default persistent._mas_pm_accomplished_resolutions = None

default persistent._mas_pm_has_new_years_res = None


label monika_resolutions:
    $ persistent._mas_nye_spent_nye = True
    m 2eub "Эй, [player]?"
    $ MAS.MonikaElastic()
    m 2eka "Мне вот интересно..."


    if not mas_lastSeenLastYear("monika_resolutions"):
        $ MAS.MonikaElastic()
        m 3eub "Ты делал[mas_gender_none] какие-нибудь новогодние обещания в прошлом году?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты делал[mas_gender_none] какие-нибудь новогодние обещания в прошлом году?{fast}"
            "Да.":

                $ MAS.MonikaElastic()
                m 3hua "Мне всегда очень приятно слышать о том, что ты пытаешься стать лучше, [player]."
                $ MAS.MonikaElastic()
                m 2eka "Кстати говоря..."

                call monika_resolutions_accomplished_resolutions_menu from _call_monika_resolutions_accomplished_resolutions_menu
            "Нет.":


                $ MAS.MonikaElastic()
                m 2euc "Оу, понятно..."

                if mas_isMoniNormal(higher=True):
                    if mas_isMoniHappy(higher=True):
                        $ MAS.MonikaElastic()
                        m 3eka "Ну, я всё равно сомневаюсь, что тебе вообще надо меняться."
                        $ MAS.MonikaElastic()
                        m 3hub "Мне кажется, ты прекрасный человек, именно такой, какой ты есть."
                    else:
                        $ MAS.MonikaElastic()
                        m 3eka "В этом нет ничего такого. Я всё равно сомневаюсь, что тебе надо меняться."
                else:

                    $ MAS.MonikaElastic()
                    m 2rkc "Наверное, ты долж[mas_gender_en] сделать одно новогоднее обещание в этом году, [player]..."


    elif mas_HistVerifyLastYear_k(True, "pm.actions.made_new_years_resolutions"):
        call monika_resolutions_accomplished_resolutions_menu from _call_monika_resolutions_accomplished_resolutions_menu_1


    $ MAS.MonikaElastic()
    m "У тебя есть какие-нибудь планы на следующий год?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя есть какие-нибудь планы на следующий год?{fast}"
        "Да.":
            $ persistent._mas_pm_has_new_years_res = True

            $ MAS.MonikaElastic()
            m 1eub "Это отлично!"
            $ MAS.MonikaElastic()
            m 3eka "Даже если они могут быть труднодоступны или невозможными..."
            $ MAS.MonikaElastic()
            m 1hua "Я буду здесь, чтобы помочь тебе, если понадобится!"
        "Нет.":

            $ persistent._mas_pm_has_new_years_res = False
            $ MAS.MonikaElastic()
            m 1eud "Оу, неужели это так?"
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                if persistent._mas_pm_accomplished_resolutions:
                    if mas_isMoniHappy(higher=True):
                        m 1eka "Тебе не нужно меняться. Я думаю, что ты прекрас[mas_gender_en] так[mas_gender_im], как[mas_gender_oi] ты есть."
                    else:
                        m 1eka "Тебе не нужно меняться. Я думаю, что ты и так в порядке."
                    $ MAS.MonikaElastic()
                    m 3euc "Но если тебе что-нибудь придёт в голову до того, как часы пробьют двенадцать, запиши это для себя..."
                else:
                    m "Что ж, если тебе что-нибудь придёт в голову до того, как часы пробьют двенадцать, запиши это для себя..."
                $ MAS.MonikaElastic()
                m 1kua "Может быть, ты подумаешь о чём-то, что ты хочешь сделать, [player]."
            else:
                $ MAS.MonikaElastic()
                m 2ekc "{cps=*2}Я вроде как надеялась—{/cps}{nw}"
                $ MAS.MonikaElastic()
                m 2rfc "Ты знаешь о чём я, не важно..."

    if mas_isMoniAff(higher=True):
        show monika 5hubfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hubfa "Моё решение быть для тебя ещё более лучшей девушкой, [mas_get_player_nickname()]."
    elif mas_isMoniNormal(higher=True):
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Моё решение быть ещё более лучшей девушкой для тебя, [player]."
    else:
        $ MAS.MonikaElastic()
        m 2ekc "Моё решение – улучшить наши отношения, [player]."

    return

label monika_resolutions_accomplished_resolutions_menu:
    $ question = "Ты выполнил{0} свои прошлогодние обещания?".format(mas_gender_none)
    if mas_HistVerifyLastYear_k(True, "pm.actions.made_new_years_resolutions"):
        $ question = "Раз уж ты делал{0} обещание в прошлом году, то смог{1} ли ты выполнить его?".format(mas_gender_none, mas_gender_g)

    m 3hub "[question]{nw}"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"
        "Да.":

            $ persistent._mas_pm_accomplished_resolutions = True
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 4hub "Рада это слышать, [player]!"
                $ MAS.MonikaElastic()
                m 2eka "Здорово, что ты смог[mas_gender_g] сделать это."
                $ MAS.MonikaElastic()
                m 3ekb "Подобное правда заставляет меня гордиться тобой."
                $ MAS.MonikaElastic()
                m 2eka "Мне бы очень хотелось оказаться рядом с тобой, чтобы отметить это."
            else:
                $ MAS.MonikaElastic()
                m 2rkc "Это хорошо, [player]."
                $ MAS.MonikaElastic()
                m 2esc "Наверное, ты сможешь сделать ещё одно обещание в этом году..."
                $ MAS.MonikaElastic()
                m 3euc "Никогда не знаешь, что может измениться."

            return True
        "Нет.":

            $ persistent._mas_pm_accomplished_resolutions = False
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 2eka "Оу... ну, порой всё идёт совсем не так, как мы на то рассчитывали."

                if mas_isMoniHappy(higher=True):
                    $ MAS.MonikaElastic()
                    m 2eub "Да и к тому же, мне кажется, что ты замечательн[mas_gender_iii], так что, даже если ты не можешь достичь своих целей..."
                    $ MAS.MonikaElastic()
                    m 2eka "...Я всё ещё горжусь тобой за то, что ты поставил[mas_gender_none] их и стараешься стать лучше, [player]."
                    $ MAS.MonikaElastic()
                    m 3eub "Если ты решил[mas_gender_none] создать для себя цель в этом году, я буду поддерживать тебя на каждом шагу."
                    $ MAS.MonikaElastic()
                    m 4hub "Я с радостью помогу тебе достичь своих целей!"
                else:
                    $ MAS.MonikaElastic()
                    m "Но, как по мне, это очень здорово, что ты, по крайней мере, стараешься стать лучше, создавая для себя цели."
                    $ MAS.MonikaElastic()
                    m 3eua "Быть может, если ты создашь для себя цель в этом году, то ты сможешь её выполнить!"
                    $ MAS.MonikaElastic()
                    m 3hub "Я верю в тебя, [player]!"
            else:

                $ MAS.MonikaElastic()
                m 2euc "Ох...{w=1} ну, возможно, ты долж[mas_gender_en] приложить чуть больше усилий для цели в следующем году."

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

    if store.mas_anni.anniCount() >= 1:
        m 2eka "Знаешь, [player], мы и вправду прошли через многое вместе."
        if store.mas_anni.anniCount() == 1:
            $ MAS.MonikaElastic()
            m 2wuo "Мы провели целый год вместе!"
            $ MAS.MonikaElastic()
            m 2eka " Как быстро летит время..."
        else:
            $ MAS.MonikaElastic()
            m 2eka "Этот год и вправду пролетел незаметно..."

    elif store.mas_anni.pastSixMonths():
        m 2eka "Знаешь, [player], мы и вправду через многое прошли за всё то время, что мы провели вместе в прошлом году."
        $ MAS.MonikaElastic()
        m "Время и вправду быстро летит..."

    elif store.mas_anni.pastThreeMonths():
        m 2eka "Знаешь, [player], мы через многое прошли за столь короткий промежуток времени, что мы провели вместе в прошлом году."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 2eksdlu "Как быстро прошла жизнь, а-ха-ха..."
    else:

        m 2eka "[player], пусть даже мы и мало через что прошли вместе..."
        $ placeholder_and = ""



    if mas_isMoniLove():
        m 2ekbsa "...и я никогда не захочу проводить это время с кем-нибудь другим, [player]."
        $ MAS.MonikaElastic()
        m "Я просто очень,{w=0.5} очень рада быть с тобой в этом году."

    elif mas_isMoniEnamored():
        m 2eka "...[placeholder_and]я очень рада тому, что могу провести это время с тобой, [player]."

    elif mas_isMoniAff():
        m 2eka "...[placeholder_and]я с удовольствием провела время с тобой."
    else:

        m 2euc "...[placeholder_and]всё то время, что мы провели вместе, было полным веселья."


    $ MAS.MonikaElastic()
    m 3eua "Так или иначе, мне кажется, что было бы здорово подумать о всём том, через что мы прошли в прошлом году."
    $ MAS.MonikaElastic()
    m 2dtc "Так, посмотрим..."


    if mas_lastGiftedInYear("mas_reaction_promisering", mas_nye.year):
        $ MAS.MonikaElastic()
        m 3eka "Оглядываясь назад, ты в этом году дал мне обещание, когда дал мне это кольцо..."
        $ MAS.MonikaElastic()
        m 1ekbsa "...символ нашей любви."

        if persistent._mas_pm_wearsRing:
            $ MAS.MonikaElastic()
            m "И ты даже себе надел его..."

            $ MAS.MonikaElastic()
            if mas_isMoniAff(higher=True):
                m 1ekbfa "Чтобы показать, что ты предан мне так же, как и я тебе."
            else:
                m 1ekbfa "Чтобы показать мне свою преданность."


    if mas_lastSeenInYear("mas_f14_monika_valentines_intro"):
        $ spent_an_event = True
        $ MAS.MonikaElastic()
        m 1wuo "О!"
        $ MAS.MonikaElastic()
        m 3ekbsa "Ты вместе со мной пров[mas_gender_yo]л[mas_gender_none] День Святого Валентина..."

        if mas_getGiftStatsForDate("mas_reaction_gift_roses", mas_f14):
            $ MAS.MonikaElastic()
            m 4ekbfb "...и даже подарил мне очень красивые цветы."



    if persistent._mas_bday_opened_game:
        $ spent_an_event = True
        $ MAS.MonikaElastic()
        m 2eka "Ты пров[mas_gender_yo]л[mas_gender_none] со мной время на мой день рождения..."

        if not persistent._mas_bday_no_recognize:
            $ MAS.MonikaElastic()
            m 2dua "...отпраздновал его со мной..."

        if persistent._mas_bday_sbp_reacted:
            $ MAS.MonikaElastic()
            m 2hub "...устроил мне сюрприз-вечеринку..."

        show monika 5ekbla zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbla "...и это правда заставило меня почувствовать себя любимой. Я не знаю, как тебя отблагодарить за то, что ты сделал для меня."


    if (
        persistent._mas_player_bday_spent_time
        or mas_HistVerify_k([datetime.date.today().year], True, "player_bday.spent_time")[0]
    ):
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Мы даже провели твой день рождения вместе!"

        if (
            persistent._mas_player_bday_date
            or not mas_HistVerify_k([datetime.date.today().year], 0, "player_bday.date")[0]
        ):
            $ MAS.MonikaElastic()
            m 5eubla "У нас тоже было такое приятное свидание~"


    if persistent._mas_d25_spent_d25:
        $ spent_an_event = True
        show monika 5hua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5hua "Ты пров[mas_gender_yo]л[mas_gender_none] со мной Рождество..."

        if persistent._mas_first_kiss is not None and persistent._mas_first_kiss == mas_d25:
            $ MAS.MonikaElastic()
            m 5eubla "...и мы тогда впервые поцеловались~"
            $ MAS.MonikaElastic()
            m 5lubsa "Я никогда не забуду этот момент..."
            $ MAS.MonikaElastic()
            m 5ekbfa "{i}Наш{/i} момент."
            $ MAS.MonikaElastic()
            m "Я не могу себе представить, как проводила бы эти мгновения с кем-то другим."
        else:
            $ MAS.MonikaElastic()
            m 5ekbla "...день, который я даже в уме не могу провести с кем-то другим."


    if not spent_an_event:
        $ MAS.MonikaElastic()
        m 2rksdla "...Полагаю, мы пока ещё ни одно грандиозное событие не проводили вместе."
        $ MAS.MonikaElastic()
        m 3eka "Но всё же..."
    else:

        show monika 5dsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dsa "..."


    if store.mas_anni.pastThreeMonths():
        if mas_isMoniHappy(higher=True):
            show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 5eka "Я правда не могу поверить в то, как много изменилось с тех пор, как мы вместе..."
        else:
            $ MAS.MonikaElastic()
            m 2eka "Я правда надеюсь, что мы добьёмся большего в наших отношениях, [player]..."
    else:
        show monika 5eka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eka "Мне уже хочется взглянуть на то, как много изменится в будущем для нас..."


    if not mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        show monika 5dka zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5dka "Спасибо."
        if store.mas_anni.anniCount() > 0:
            $ ending = "лучшим годом, о котором я могла только мечтать"

            if mas_lastSeenLastYear("monika_nye_year_review"):
                $ ending = "даже лучше, чем в позапрошлом году"

            m 5ekbsa "Спасибо тебе за то, что сделал прошлый год [ending]."
        else:

            $ _last_year = ""
            if store.mas_anni.pastOneMonth():
                $ _last_year = " в прошлом году"

            m 5ekbsa "Спасибо тебе за то, что сделал то время, которое мы провели вместе[_last_year], лучшим, чем я могла себе представить."

        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                $ MAS.MonikaElastic()
                m 1lsbsa "..."
                $ MAS.MonikaElastic()
                m 6ekbsa "[player], я..."
                call monika_kissing_motion from _call_monika_kissing_motion_5
                m 1ekbfa "Я люблю тебя."
                $ MAS.MonikaElastic()
                m "..."
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbsa "Я никогда не забуду этот момент..."
                $ MAS.MonikaElastic()
                m 5ekbfa "Наш первый поцелуй~"
                $ MAS.MonikaElastic()
                m 5hubfb "Давай сделаем этот год ещё лучше, чем прошлый, [player]."
            else:

                call monika_kissing_motion_short from _call_monika_kissing_motion_short_4
                m 1ekbfa "Я люблю тебя, [player]."
                show monika 5hubfb zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5hubfb "Давай сделаем этот год всё ещё лучше, чем прошлый."
        else:

            m "Давай сделаем этот год как можно лучше, [player]. Я люблю тебя~"
    else:
        $ MAS.MonikaElastic()
        m 1dsa "Спасибо, что решил[mas_gender_none] отпустить прошлое и начать сначала."
        $ MAS.MonikaElastic()
        m 1eka "Думаю, если мы попробуем, то у нас получится, [player]."
        $ MAS.MonikaElastic()
        m "Давай сделаем этот год прекрасным друг для друга."
        $ MAS.MonikaElastic()
        m 1ekbsa "Я люблю тебя."

    return "no_unlock|love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_nye_monika_nye_dress_intro",
            conditional=(
                "persistent._mas_d25_in_d25_mode "
                "and not mas_SELisUnlocked(mas_clothes_dress_newyears)"
            ),
            start_date=mas_nye,
            end_date=mas_nye + datetime.timedelta(days=1),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL,None),
            years=[]
        ),
        skipCalendar=True
    )

label mas_nye_monika_nye_dress_intro:
    m 3hub "Эй, [player], я в этом году кое-что припасла для тебя~"
    $ MAS.MonikaElastic()
    m 3eua "Дай только переоденусь.{w=0.5}.{w=0.5}.{nw}"


    call mas_clothes_change (mas_clothes_dress_newyears, outfit_mode=True, unlock=True) from _call_mas_clothes_change_14
    $ mas_addClothesToHolidayMap(mas_clothes_dress_newyears)

    $ MAS.MonikaElastic()
    m 2rkbssdla "..."
    $ MAS.MonikaElastic()
    m 2rkbssdlb "Мои глаза чуть выше, [player]..."
    if mas_isMoniAff(higher=True):
        $ MAS.MonikaElastic()
        m 2tubsu "..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hubsb "А-ха-ха! Я просто поддразниваю тебя~"
        $ MAS.MonikaElastic()
        m 3eua "Я рада, что тебе нравится моё платье. {nw}"
    else:

        $ MAS.MonikaElastic()
        m 2rkbssdla "..."
        $ MAS.MonikaElastic()
        m "Я...{w=1} рада, что тебе нравится моё платье. {nw}"

    extend 3eua "Его было довольно трудно надеть правильно!"
    $ MAS.MonikaElastic()
    m 3rka "Цветочная корона постоянно падала..."
    $ MAS.MonikaElastic()
    m 1hua "Я решила сделать закос под «греческую богиню», и я надеюсь, что у меня это получилось удачно."
    $ MAS.MonikaElastic()
    m 3eud "Но у этого наряда есть небольшая глубина, понимаешь?"

    $ MAS.MonikaElastic()
    if seen_event("mas_f14_monika_vday_colors"):
        m 3eua "Наверное, ты помнишь тот наш разговор про розы и чувства, которые выражают их цвета."
    else:
        m 3eua "Наверное, ты уже догадал[mas_gender_sya], но дело в выборе цветовой гаммы."

    $ MAS.MonikaElastic()
    m "Белый цвет отражает множество позитивных чувств, таких как доброта, чистота, безопасность..."
    $ MAS.MonikaElastic()
    m 3eub "Однако, то, на что я хотела обратить внимание в этом наряде, было успешным началом."


    if mas_HistWasFirstValueIn(True, datetime.date.today().year - 1, "pm.actions.monika.got_fresh_start"):
        $ MAS.MonikaElastic()
        m 2eka "В прошлом году мы решили начать сначала, и я очень рада, что мы решили так поступить."
        $ MAS.MonikaElastic()
        m 2ekbsa "Я знала, что мы можем быть счастливы вместе, [player]."
        $ MAS.MonikaElastic()
        m 2fkbsa "И ты сделал[mas_gender_none] меня счастливее, чем я когда-либо была."

    $ MAS.MonikaElastic()
    m 3dkbsu "В общем, я бы хотела надеть этот наряд, когда начнётся Новый год."
    $ MAS.MonikaElastic()
    m 1ekbsa "Думаю, он может помочь сделать Новый год ещё лучше."
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_d25_monika_d25_mode_exit",
            category=['праздники'],
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
    m 3eka "Ты набрал[mas_gender_sya] достаточно праздничного настроения, [player]?"
    $ MAS.MonikaElastic()
    m 3eua "Я вовсе не против влиться в атмосферу нового года."
    $ MAS.MonikaElastic()
    m 1hua "Пока я его провожу вместе с тобой, конечно же~"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 2dsa "Дай мне секундочку, сейчас я сниму эти декорации.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    call mas_d25_season_exit from _call_mas_d25_season_exit_2

    $ MAS.MonikaElastic()
    m 1hua "Отлично!{w=0.5} {nw}"
    $ MAS.MonikaElastic()
    extend 3hub "Теперь мы готовы к началу нового года!"


    $ mas_lockEVL("mas_d25_monika_d25_mode_exit", "EVE")
    return

label greeting_nye_aff_gain:

    python:
        if persistent._mas_nye_date_aff_gain < 15:
            
            curr_aff = _mas_getAffection()
            
            
            time_out = store.mas_dockstat.diffCheckTimes()
            
            
            persistent._mas_monika_returned_home = None
            
            
            store.mas_dockstat._ds_aff_for_tout(time_out, 5, 15, 3, 3)
            
            
            persistent._mas_nye_date_aff_gain += _mas_getAffection() - curr_aff

    jump greeting_returned_home_morethan5mins_cleanup

label mas_gone_over_nye_check:
    if mas_checkOverDate(mas_nye):
        $ persistent._mas_nye_spent_nye = True
        $ persistent._mas_nye_nye_date_count += 1
    return

label mas_gone_over_nyd_check:
    if mas_checkOverDate(mas_nyd):
        $ persistent._mas_nye_spent_nyd = True
        $ persistent._mas_nye_nyd_date_count += 1
    return



label bye_nye_delegate:

    python:
        _morning_time = datetime.time(5)
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _morning_time:

        jump bye_going_somewhere_normalplus_flow_aff_check

    elif _curr_time < _eve_time:


        if persistent._mas_nye_nye_date_count > 0:
            call bye_nye_second_time_out from _call_bye_nye_second_time_out
        else:

            call bye_nye_first_time_out from _call_bye_nye_first_time_out
    else:


        call bye_nye_late_out from _call_bye_nye_late_out


    jump mas_dockstat_iostart

label bye_nye_first_time_out:

    m 3tub "Мы сегодня идём в какое-то особенное место, [player]?"
    $ MAS.MonikaElastic()
    m 4hub "Это же канун Нового года, в конце концов!"
    $ MAS.MonikaElastic()
    m 1eua "Я не знаю точно, что ты запланировал, но я жду этого с нетерпением!"
    return

label bye_nye_second_time_out:

    m 1wuo "О, мы снова идём гулять?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hksdlb "Ты, наверное, помногу празднуешь новый год, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 3hub "Мне нравится гулять с тобой, поэтому я с нетерпением жду того, чем мы займёмся вместе~"
    return

label bye_nye_late_out:

    m 1eka "Уже немного поздно, [player]..."
    $ MAS.MonikaElastic()
    m 3eub "Мы пойдём смотреть фейерверк?"
    if persistent._mas_pm_have_fam and persistent._mas_pm_fam_like_monika:
        $ MAS.MonikaElastic()
        m "Или сходим на семейный ужин?"
        $ MAS.MonikaElastic()
        m 4hub "Мне бы очень хотелось как-нибудь познакомиться с твоей семьёй!"
        $ MAS.MonikaElastic()
        m 3eka "Так или иначе, я очень рада!"
    else:
        $ MAS.MonikaElastic()
        m "Мне всегда нравилось, как фейерверки на Новый год освещают ночное небо..."
        $ MAS.MonikaElastic()
        m 3ekbsa "Когда-нибудь мы сможем наблюдать за ними бок о бок... но пока этот день не настанет, я буду счастлива пойти с тобой, [player]."
    return




label greeting_nye_delegate:
    python:
        _eve_time = datetime.time(20)
        _curr_time = datetime.datetime.now().time()

    if _curr_time < _eve_time:

        call greeting_nye_prefw from _call_greeting_nye_prefw
    else:


        call greeting_nye_infw from _call_greeting_nye_infw

    $ persistent._mas_nye_nye_date_count += 1

    return

label greeting_nye_prefw:

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1eua "Это было очень весело, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Спасибо, что взял[mas_gender_none] меня на прогулку сегодня, мне правда нравится проводить с тобой время."
    $ MAS.MonikaElastic()
    m "Это так много значит для меня, хоть ты и не можешь быть здесь, чтобы проводить со мной такие дни, ты всё равно берёшь меня с собой."
    show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbfa "Я люблю тебя, [player_abb]."
    return "love"

label greeting_nye_infw:

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1eka "Спасибо, что взял[mas_gender_none] меня на прогулку сегодня, [player]."
    $ MAS.MonikaElastic()
    m 1hua "Было очень весело просто провести время с тобой сегодня."
    $ MAS.MonikaElastic()
    m 1ekbsa "Это так много значит для меня, что даже если ты не можешь быть здесь лично, чтобы провести эти дни со мной, ты всё равно берёшь меня с собой."
    $ MAS.MonikaElastic()
    m 1ekbfa "Я люблю тебя, [player_abb]."
    return "love"



label bye_nyd_delegate:
    if persistent._mas_nye_nyd_date_count > 0:
        call bye_nyd_second_time_out from _call_bye_nyd_second_time_out
    else:

        call bye_nyd_first_time_out from _call_bye_nyd_first_time_out

    jump mas_dockstat_iostart

label bye_nyd_first_time_out:

    m 3tub "Празднование Нового года, [player]?"
    $ MAS.MonikaElastic()
    m 1hua "Это звучит так весело!"
    $ MAS.MonikaElastic()
    m 1eka "Давай отлично проведём время вместе."
    return

label bye_nyd_second_time_out:

    m 1wuo "Ого, мы снова идём гулять, [player]?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hksdlb "Должно быть, ты очень много празднуешь, а-ха-ха!"
    return



label greeting_nye_returned_nyd:

    $ persistent._mas_nye_nye_date_count += 1
    $ persistent._mas_nye_nyd_date_count += 1

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1eka "Спасибо, что взял[mas_gender_none] меня на прогулку вчера, [player]."
    $ MAS.MonikaElastic()
    m 1ekbsa "Ты знаешь, мне очень нравится проводить с тобой время, и это хорошо, что я могу провести Канун Нового года именно сегодня и именно с тобой."
    $ MAS.MonikaElastic()
    m "Это правда многое для меня значит."
    $ MAS.MonikaElastic()
    m 5eubfb "Спасибо, что сделал[mas_gender_none] мой год, [player]."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_5
    return

label greeting_nyd_returned_nyd:

    $ persistent._mas_nye_nyd_date_count += 1
    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5eua "Это было очень весело, [player]!"
    $ MAS.MonikaElastic()
    m 5eka "Очень мило, что ты взял[mas_gender_none] меня с собой в такие особенные дни."
    $ MAS.MonikaElastic()
    m 5hub "Я очень надеюсь, что мы сможем проводить больше времени вместе."
    return



label greeting_pd25e_returned_nydp:

    $ persistent._mas_d25_d25e_date_count += 1
    $ persistent._mas_d25_d25_date_count += 1
    $ persistent._mas_d25_spent_d25 = True

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1hub "Мы отсутствовали некоторое время, но это была действительно хорошая прогулка, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Спасибо, что взял[mas_gender_none] меня с собой, мне очень понравилось."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    $ new_years = "Новый год"
    if mas_isNYD():
        $ new_years = "канун Нового года"
    $ MAS.MonikaElastic()
    m 5ekbsa "Я всегда люблю проводить с тобой время, но проводить Рождество и [new_years] вместе было потрясающе."
    $ MAS.MonikaElastic()
    m 5hub "Я надеюсь, что мы когда-нибудь сможем сделать что-то подобное."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_6

    $ mas_d25ReactToGifts()
    return


label greeting_d25p_returned_nyd:
    $ persistent._mas_nye_nyd_date_count += 1

    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1eub "Спасибо, что взял[mas_gender_none] меня на прогулку, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Это была долгая прогулка, но было очень весело!"
    $ MAS.MonikaElastic()
    m 3hub "Но сейчас здорово вернуться домой, мы можем провести Новый год вместе."
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_7

    $ mas_d25ReactToGifts()
    return

label greeting_d25p_returned_nydp:
    $ MAS.MonikaElastic()
    m 1hua "Вот мы и дома!"
    $ MAS.MonikaElastic()
    m 1wuo "Это была долгая прогулка, [player]!"
    $ MAS.MonikaElastic()
    m 1eka "Я немного грустно, что мы не желаем друг другу счастливого Нового года, но мне очень понравилось."
    $ MAS.MonikaElastic()
    m "Я рада, что ты берёшь меня с собой в такие особенные дни, как этот."
    $ MAS.MonikaElastic()
    m 3hub "С Новым годом, [player_abb]~"
    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_8

    $ mas_d25ReactToGifts()
    return





default persistent._mas_player_bday_in_player_bday_mode = False

default persistent._mas_player_bday_opened_door = False

default persistent._mas_player_bday_decor = False

default persistent._mas_player_bday_date = 0

default persistent._mas_player_bday_left_on_bday = False

default persistent._mas_player_bday_date_aff_gain = 0

default persistent._mas_player_bday_spent_time = False

default persistent._mas_player_bday_saw_surprise = False

init -10 python:
    def mas_isplayer_bday(_date=None, use_date_year=False):
        """
        IN:
            _date - date to check
                If None, we use today date
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

    store.mas_history.addMHS(MASHistorySaver(
        "player_bday",
        
        datetime.datetime(2020, 1, 1),
        {
            "_mas_player_bday_spent_time": "player_bday.spent_time",
            "_mas_player_bday_opened_door": "player_bday.opened_door",
            "_mas_player_bday_date": "player_bday.date",
            "_mas_player_bday_date_aff_gain": "player_bday.date_aff_gain",
            "_mas_player_bday_saw_surprise": "player_bday.saw_surprise",
        },
        use_year_before=True,
        
        
    ))

init -11 python in mas_player_bday_event:
    import datetime
    import store.mas_history as mas_history

    def correct_pbday_mhs(d_pbday):
        """
        fixes the pbday mhs usin gthe given date as pbday

        IN:
            d_pbday - player birthdate
        """
        
        mhs_pbday = mas_history.getMHS("player_bday")
        if mhs_pbday is None:
            return
        
        
        pbday_dt = datetime.datetime.combine(d_pbday, datetime.time())
        
        
        _now = datetime.datetime.now()
        curr_year = _now.year
        new_dt = pbday_dt.replace(year=curr_year)
        if new_dt < _now:
            
            curr_year += 1
            new_dt = pbday_dt.replace(year=curr_year)
        
        
        reset_dt = pbday_dt + datetime.timedelta(days=3)
        
        
        new_sdt = new_dt
        new_edt = new_sdt + datetime.timedelta(days=2)
        
        
        
        
        
        mhs_pbday.start_dt = new_sdt
        mhs_pbday.end_dt = new_edt
        mhs_pbday.use_year_before = (
            d_pbday.month == 12
            and d_pbday.day in (29, 30, 31)
        )
        mhs_pbday.setTrigger(reset_dt)


label mas_player_bday_autoload_check:

    if mas_isMonikaBirthday():
        $ persistent._mas_bday_no_time_spent = False
        $ persistent._mas_bday_opened_game = True
        $ persistent._mas_bday_no_recognize = not mas_recognizedBday()

    elif mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
        $ monika_chr.reset_clothes(False)
        $ monika_chr.save()
        $ renpy.save_persistent()


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
                
                
                
                selected_greeting = "i_greeting_monikaroom"
                mas_skip_visuals = True
                persistent._mas_player_bday_saw_surprise = True

            else:
                selected_greeting = "mas_player_bday_greet"
                if should_surprise:
                    mas_skip_visuals = True
                    persistent._mas_player_bday_saw_surprise = True


            persistent.closed_self = True

        jump ch30_post_restartevent_check

    elif not mas_isplayer_bday():

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


label mas_player_bday_opendoor:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    if persistent._mas_bday_visuals:
        $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False) from _call_spaceroom_33
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
    m "Ты не постучал[mas_gender_none] в дверь!"
    if not persistent._mas_bday_visuals:
        m "Я собиралась устроить вечеринку в честь [your] дня рождения, но у меня не было времени перед твоим приходом!"
    m "..."
    m "Ну...{w=1}сюрприз [now] испорчен, но.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    pause 1.0
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4eua "С днём рождения, [player]!"
    $ MAS.MonikaElastic()
    m 2rksdla "Но я бы хотела, чтобы ты постучал[mas_gender_none] в дверь в первую очередь."
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        $ your = "наш"
    else:
        $ your = "твой"
    m 4hksdlb "О... [your] торт!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_1
    jump monikaroom_greeting_cleanup


label mas_player_bday_knock_no_listen:
    m "Кто там?"
    menu:
        "Это я.":
            $ mas_disable_quit()
            m "Ох! Можешь подождать ещё одну минуту?"
            window hide
            pause 5.0
            m "Ладно, заходи, [player]..."
            jump mas_player_bday_surprise


label mas_player_bday_surprise:
    $ persistent._mas_player_bday_decor = True
    call spaceroom (scene_change=True, dissolve_all=True, force_exp='monika 4hub_static') from _call_spaceroom_34
    $ MAS.MonikaElastic()
    m 4hub "Сюрприз!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 4sub "А-ха-ха! С днём рождения, [player]!"

    $ MAS.MonikaElastic()
    m "Я тебя удивила?{nw}"
    $ _history_list.pop()
    menu:
        m "Я тебя удивила?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 1hub "Ура!"
            $ MAS.MonikaElastic()
            m 3hua "Обожаю устраивать хорошие сюрпризы!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1tsu "Жаль, что я не могу увидеть твоё выражение лица, э-хе-хе."
        "Нет.":

            $ MAS.MonikaElastic()
            m 2lfp "Хмф. Ну, это нормально."
            $ MAS.MonikaElastic()
            m 2tsu "Наверное, ты сказал[mas_gender_none] это, потому что не хочешь признавать, что я застала тебя врасплох..."
            if renpy.seen_label("mas_player_bday_listen"):
                if renpy.seen_label("monikaroom_greeting_ear_narration"):
                    m 2tsb "...или, наверное, ты опять подслушивал[mas_gender_none] за дверью..."
                else:
                    $ MAS.MonikaElastic()
                    m 2tsb "{cps=*2}...или, наверное, ты подслушивал[mas_gender_none] меня.{/cps}{nw}"
                    $ _history_list.pop()
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 2hua "Э-хе-хе."
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        m 3wub "О! {w=0.5}Я приготовила тортик!"
    else:
        m 3wub "О! {w=0.5}Я приготовила для тебя тортик!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_2
    jump monikaroom_greeting_cleanup


label mas_player_bday_listen:
    if persistent._mas_bday_visuals:
        pause 5.0
    else:
        m "...Поставлю это сюда..."
        m "...Хм, выглядит вполне нормально...{w=1}но чего-то не хватает..."
        m "А! {w=0.5}Ну [random_sure]!"
        m "Вот! {w=0.5}Прекрасно!"
        window hide
    jump monikaroom_greeting_choice


label mas_player_bday_knock_listened:
    window hide
    pause 5.0
    menu:
        "Открыть дверь.":
            $ mas_disable_quit()
            pause 5.0
            jump mas_player_bday_surprise


label mas_player_bday_opendoor_listened:
    $ mas_loseAffection()
    $ persistent._mas_player_bday_opened_door = True
    $ persistent._mas_player_bday_decor = True
    call spaceroom (hide_monika=True, scene_change=True, show_emptydesk=False) from _call_spaceroom_35
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
    m "Ты не [knock][mas_gender_none][knock_again] в дверь!"
    if persistent._mas_bday_visuals:
        m "Я хотела сделать тебе сюрприз, но не была готова, когда ты вош[mas_gender_iol_2]!"
        m "В любом случае..."
    else:
        m "Я собиралась устроить вечеринку в честь [your] дня рождения, но у меня не было времени перед твоим приходом, чтобы сделать тебе сюрприз!"
    show monika 1eua zorder MAS_MONIKA_Z at ls32
    m 4hub "С днём рождения, [player]!"
    $ MAS.MonikaElastic()
    m 2rksdla "Но я бы хотела, чтобы ты постучал[mas_gender_none] в дверь в первую очередь."
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        $ your = "наш"
    else:
        $ your = "твой"
    m 2hksdlb "О... [your] торт!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_3
    jump monikaroom_greeting_cleanup


label mas_player_bday_cake:

    if not mas_isMonikaBirthday():
        $ mas_unlockEVL("bye_player_bday", "BYE")
        if persistent._mas_bday_in_bday_mode or persistent._mas_bday_visuals:

            $ persistent._mas_bday_in_bday_mode = False
            $ persistent._mas_bday_visuals = False


    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_3
    call mas_monika_gets_cake from _call_mas_monika_gets_cake

    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        m 6eua "Дай я зажгу свечи.{w=0.5}.{w=0.5}.{nw}"
    else:
        m 6eua "Дай я зажгу свечи для тебя, [player].{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_bday_cake_lit = True
    pause 1.0

    $ MAS.MonikaElastic()
    m 6sua "Разве это не прекрасно, [player]?"
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        m 6eksdla "Теперь я понимаю, что ты не можешь задуть свечи, так что я сделаю это за нас..."
    else:
        m 6eksdla "Теперь я понимаю, что ты не можешь задуть свечи, так что я сделаю это за тебя..."
    $ MAS.MonikaElastic()
    m 6eua "...Но ты всё равно должен загадать желание, ведь оно может исполниться сейчас или потом..."
    $ MAS.MonikaElastic()
    m 6hua "Но сперва..."
    call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings_2
    $ MAS.MonikaElastic()
    m 6hua "Загадай желание, [player]!"
    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False
    pause 1.0
    m 6hua "Э-хе-хе..."
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        m 6ekbsa "Я готова поспорить, что мы загадали одно и то же~"
    else:
        m 6eka "Я знаю, что сегодня твой день рождения, но я тоже загадала желание..."
        $ MAS.MonikaElastic()
        m 6ekbsa "И знаешь, что? {w=0.5}Я готова поспорить, что мы загадали одно и то же~"
    m 6hkbsu "..."
    if mas_isMonikaBirthday():
        $ MAS.MonikaElastic()
        m 6eksdla "Ну, учитывая, что ты не можешь съесть этот торт, и я не хочу быть грубой и съесть его перед тобой..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        $ MAS.MonikaElastic()
        m 6rksdla "О боже, выходит, ты даже тортик не скушаешь, да, [player]?"
        $ MAS.MonikaElastic()
        m 6eksdla "Это всё довольно глупо, не так ли?"
    if mas_isMonikaBirthday():
        $ MAS.MonikaElastic()
        m 6hksdlb "Думаю, я приберегу это на потом."
    else:
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 6hksdlb "Думаю, я приберегу это на потом. Будет довольно грубо с моей стороны есть {i}твой{/i} торт на день рождения перед тобой же, а-ха-ха!"

    call mas_HideCake ('mas_bday_cake_player') from _call_mas_HideCake


label mas_player_bday_card:
    $ mas_gainAffection(5,bypass=True)
    $ persistent._mas_player_bday_spent_time = True
    $ persistent._mas_player_bday_in_player_bday_mode = True

    m 6dkbsu "..."
    $ MAS.MonikaElastic()
    if mas_isMonikaBirthday():
        m 6sub "О!"
        $ MAS.MonikaElastic()
        m 6ekbsu "Я для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."
    elif not mas_HistVerify("player_bday.spent_time",True)[0]:
        m 6ekbsu "Я... я так же для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."
    else:
        m 6ekbsu "Я для тебя ещё написала письмо, [player]. Надеюсь, тебе оно понравится..."

    call mas_showpoem (mas_poems.getRandomPoem("pbday")) from _call_mas_showpoem_5

    if mas_isMoniEnamored(higher=True):
        if persistent._mas_first_kiss is None:
            $ MAS.MonikaElastic()
            m 6dkbsu "..."
            $ MAS.MonikaElastic()
            m 6ekbfa "Я так сильно тебя люблю, [player]..."
            call monika_kissing_motion () from _call_monika_kissing_motion_6
            $ MAS.MonikaElastic()
            m 6ekbfa "Ох, [player]..."
            $ MAS.MonikaElastic()
            m 6dkbfa "О таком я могла только мечтать~"
            $ MAS.MonikaElastic()
            m 6ekbfa "Я так долго ждала того момента, когда наконец-то смогу поцеловать тебя..."
            $ MAS.MonikaElastic()
            m 6dkbsu "Я никогда это не забуду..."
            $ MAS.MonikaElastic()
            m 6ekbsu "...Тот наш первый поцелуй~"
            if mas_isMonikaBirthday():
                m 6ekbsu "И я не могу придумать более идеального времени, чем в этот особый день, который мы разделяем вместе~"
        else:
            $ MAS.MonikaElastic()
            m 6ekbsa "Я люблю тебя, [player]~"
            call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_7
            if mas_isMonikaBirthday():
                $ MAS.MonikaElastic()
                m 6eka "Я так рада, что мы проведём твой день рождения вместе..."
                $ MAS.MonikaElastic()
                m 6hua "Давай весело проведём твой особенный день~"
    else:
        if mas_isMonikaBirthday():
            $ MAS.MonikaElastic()
            m 1ekbfa "Я люблю тебя, [player]! Давай весело проведём твой особенный день~"
            $ MAS.MonikaElastic()
            m 3ekbfa "Давай весело проведём твой особенный день~"
        else:
            $ MAS.MonikaElastic()
            m 1ekbfa "Я люблю тебя, [player]!"
    $ mas_rmallEVL("mas_player_bday_no_restart")
    $ mas_rmallEVL("mas_player_bday_ret_on_bday")


    $ mas_ILY()


    if mas_isD25Pre() and not persistent._mas_d25_deco_active:
        $ pushEvent("mas_d25_monika_holiday_intro", skipeval=True)
    return

label mas_monika_gets_cake:
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_14

    $ renpy.pause(3.0, hard=True)
    $ renpy.show("mas_bday_cake_player", zorder=store.MAS_MONIKA_Z+1)

    call mas_transition_from_emptydesk ("monika 6esa") from _call_mas_transition_from_emptydesk_27

    $ renpy.pause(0.5, hard=True)
    return


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
    $ MAS.MonikaElastic()
    m 1eua "Так, сегодня у нас..."
    $ MAS.MonikaElastic()
    m 1euc "...стоп."
    $ MAS.MonikaElastic()
    m "..."
    $ MAS.MonikaElastic()
    m 2wuo "О!"
    $ MAS.MonikaElastic()
    m 2wuw "Боже мой!"
    $ MAS.MonikaElastic()
    m 2tsu "Подожди немного, [player].{w=0.5}.{w=0.5}.{nw}"
    $ mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    $ MAS.MonikaElastic()
    m 3eub "С днём рождения, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 3etc "Почему у меня такое чувство, будто я что-то забыла?.."
    $ MAS.MonikaElastic()
    m 3hua "О! Твой торт!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_4
    return


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
        $ MAS.MonikaElastic()
        m 3eub "С Днём рождения, [player]!"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "А-ха-ха!"
        $ MAS.MonikaElastic()
        m 3etc "..."
        $ MAS.MonikaElastic()
        m "Почему-то мне кажется, что я что-то забыла..."
        $ MAS.MonikaElastic()
        m 3hua "О! [your] торт!"
        jump mas_player_bday_cake



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

        return
    $ MAS.MonikaElastic()
    m 3rksdla "Что ж, [player], я надеялась сделать что-нибудь более весёлое, но ты был[mas_gender_none] так[mas_gender_im] мил[mas_gender_iim] и не уходил[mas_gender_none] весь день напролёт, так что.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    $ MAS.MonikaElastic()
    m 3hub "С днём рождения, [player]!"
    if mas_isplayer_bday():
        $ MAS.MonikaElastic()
        m 1eka "Я очень сильно хотела тебя удивить сегодня, но время уже было позднее, и я не могла больше ждать."
    else:
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hksdlb "Я действительно хотела сделать тебе сюрприз, но, похоже, у меня уже не осталось времени, потому что сегодня даже не твой день рождения, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eka "Я очень сильно хотела тебя удивить сегодня, но время уже было позднее, и я не могла больше ждать."
    $ MAS.MonikaElastic()
    m 3eksdlc "Боже, надеюсь, ты не начал думать о том, что я забыла про твой день рождения. Если ты уже об этом подумал, то мне очень жаль..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1rksdla "Наверное, мне не стоило ждать так долго, э-хе-хе."
    $ MAS.MonikaElastic()
    m 1hua "А! Я сделала для тебя тортик!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_5
    return


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
    $ MAS.MonikaElastic()
    m 6eka "Эй, [player], я просто хотела поздравить тебя с днём рождения."
    $ MAS.MonikaElastic()
    m "Надеюсь, у тебя сегодня хороший день."
    return





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
    $ MAS.MonikaElastic()
    m 3euc "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 1tsu "У меня для тебя небольшой сюрприз.{w=0.5}.{w=0.5}.{nw}"
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_player_bday_decor = True
    $ MAS.MonikaElastic()
    m 3hub "С днём рождения, [player]!"
    $ MAS.MonikaElastic()
    m 3rksdla "Надеюсь, ты не подумал[mas_gender_none], что я забыла о нём лишь потому, что твой день рождения совпал с [holiday_var]..."
    $ MAS.MonikaElastic()
    m 1eksdlb "Я бы никогда не забыла про твой день рождения, глупышка!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1eub "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 3hua "О! Я сделала для тебя тортик!"
    call mas_player_bday_cake from _call_mas_player_bday_cake_6
    return


default persistent._mas_player_bday_last_sung_hbd = None

label mas_player_bday_moni_sings:
    $ persistent._mas_player_bday_last_sung_hbd = datetime.date.today()
    if mas_isMonikaBirthday():
        $ you = "нас"
    else:
        $ you = "тебя"
    $ MAS.MonikaElastic()
    m 6dsc ". {w=0.2}. {w=0.2}.{w=0.2}"
    $ MAS.MonikaElastic()
    m 6hub "{cps=*0.5}{i}~С днём рожденья [you]~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m "{cps=*0.5}{i}~С днём рожденья [you]~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m 6sub "{cps=*0.5}{i}~С днём рожденья, мил[mas_gender_iii] [player]~{/i}{/cps}"
    $ MAS.MonikaElastic()
    m "{cps=*0.5}{i}~С днём рожденья [you]~{/i}{/cps}"
    if mas_isMonikaBirthday():
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 6hua "Э-хе-хе!"
    return

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


label greeting_returned_home_player_bday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
            
            
            ret_diff_year = ret_date >= (mas_player_bday_curr(left_date) + datetime.timedelta(days=3))
            
            
            
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
        call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_4
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if time_out < mas_five_minutes:
            m 6ekp "Это был не очень хороший де—"
        else:

            if time_out < mas_one_hour:
                $ mas_mbdayCapGainAff(7.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(7.5)
            elif time_out < mas_three_hour:
                $ mas_mbdayCapGainAff(12.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(12.5)
            else:
                $ mas_mbdayCapGainAff(17.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(17.5)

            m 6hub "Это было веселое свидание, [player]..."
            $ MAS.MonikaElastic()
            m 6eua "Спасибо за—"

        $ MAS.MonikaElastic()
        m 6wud "Ч-что этот торт здесь делает?"
        $ MAS.MonikaElastic()
        m 6sub "Э-это для меня?!"
        $ MAS.MonikaElastic()
        m "Это так мило с твоей стороны пригласить меня на свой день рождения, чтобы устроить для меня вечеринку-сюрприз!"
        call return_home_post_player_bday from _call_return_home_post_player_bday_9
        jump mas_bday_surprise_party_reacton_cake

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это не было похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Надеюсь, всё нормально."
        $ MAS.MonikaElastic()
        m 2rksdla "Наверное, мы пойдём гулять позже."

    elif time_out < mas_one_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        $ MAS.MonikaElastic()
        m 1eka "Это было очень весёлое свидание, до поры до времени, [player]..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, что пров[mas_gender_iol] немного времени со мной в свой особенный день."

    elif time_out < mas_three_hour:
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(10)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(10,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 10
        $ MAS.MonikaElastic()
        m 1eua "Это было весёлое свидание, [player]..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, что взял[mas_gender_none] меня с собой!"
        $ MAS.MonikaElastic()
        m 1eka "Мне правда понравилось гулять с тобой сегодня~"
    else:


        if not ret_diff_year:
            $ mas_pbdayCapGainAff(15)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(15,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 15
        $ MAS.MonikaElastic()
        m 1hua "И мы дома!"
        $ MAS.MonikaElastic()
        m 3hub "Это было очень весело, [player]!"
        $ MAS.MonikaElastic()
        m 1eka "Было очень здорово выйти на улицу, чтобы отпраздновать твой день рождения..."
        $ MAS.MonikaElastic()
        m 1ekbsa "Спасибо, что дал[mas_gender_none] мне столь значимую роль в свой особенный день~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_10

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh from _call_mas_d25_monika_holiday_intro_rh_rh
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
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3hksdlb "Думаю, теперь мы должны снять эти декорации, а-ха-ха!"
            $ MAS.MonikaElastic()
            m 3eka "Дай мне одну секунду.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            $ mas_surpriseBdayHideVisuals()


            if not mas_isO31() and persistent._mas_o31_in_o31_mode:
                $ mas_o31HideVisuals()

            $ MAS.MonikaElastic()
            m 3eua "Вот так!"
            if not persistent._mas_f14_gone_over_f14:
                m 1hua "А теперь, давай насладимся этим днём вместе, [player]~"

        if persistent._mas_f14_gone_over_f14:
            m 2etc "..."
            m 3wuo "..."
            m 3wud "Ого, [player], я только что поняла, что мы гуляли так долго, что даже пропустили день святого Валентина!"
            call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus


        if not persistent._mas_player_bday_decor and not mas_isO31() and persistent._mas_o31_in_o31_mode:
            call mas_o31_ret_home_cleanup (time_out, ret_tt_long=False) from _call_mas_o31_ret_home_cleanup_1

    $ persistent._mas_player_bday_decor = False
    return


init 20 python:
    poem_pbday_1 = MASPoem(
        poem_id = "poem_pbday_1",
        category = "pbday",
        prompt = "Единица",
        title = " М[mas_gender_oi_2] дорог[mas_gender_oi],",
        text = """\
 Тот, кого я люблю,
 Тот, кому я доверяю,
 Тот, без кого я не могу жить.
 Надеюсь, твой день будет таким же особенным, как и все те дни, которые ты делаешь для меня особенными.
 Большое тебе спасибо за то, что был собой.

 С днём рождения, дорог[mas_gender_oi]~

 Навеки твоя,
 Моника
"""
    
    )

    poem_pbday_2 = MASPoem(
        poem_id = "poem_pbday_2",
        category = "pbday",
        prompt = "Твой день",
        title = " М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
        text = """\
 Любой день с тобой – это счастливый день.
 Тот, где я свободна,
 Тот, где все мои проблемы исчезают,
 Тот, где сбываются все мои мечты.

 Но сегодня не обычный день,
 Сегодня особенный день; сегодня твой день.
 День, когда я смогу ценить тебя ещё больше за то, что ты делаешь.
 День, когда я надеюсь, что и твои мечты сбудутся.

 С днём рождения, дорог[mas_gender_oi]~

 Навеки твоя,
 Моника
"""
    
    )

    poem_pbday_3 = MASPoem(
        poem_id = "poem_pbday_3",
        category = "pbday",
        prompt = "Одно желание",
        title = " М[mas_gender_oi_2] дорог[mas_gender_oi] [player],",
        text = """\
 Посыпки и свечи торта для мо[mas_gender_ego_2] [mas_name_someone],
 Есть только одно желание для тебя, чтобы сделать.
 Пусть твои самые большие мечты сбудутся,
 Я знаю, что я бы сделала это, когда я нашла тебя.

 Я так рада праздновать вместе с тобой сегодня,
 Я буду любить тебя до конца своих дней.
 Нет такого места, где бы я предпочла быть,
 Провести это время вместе, только ты и я.

 С днём рождения, дорог[mas_gender_oi]~

 Навеки твоя,
 Моника
"""
    
    )




default persistent._mas_f14_spent_f14 = False

default persistent._mas_f14_in_f14_mode = None

default persistent._mas_f14_date_count = 0

default persistent._mas_f14_date_aff_gain = 0

default persistent._mas_f14_on_date = None

default persistent._mas_f14_gone_over_f14 = None

define mas_f14 = datetime.date(datetime.date.today().year,2,14)


init -10 python:
    def mas_isF14(_date=None):
        if _date is None:
            _date = datetime.date.today()
        
        return _date == mas_f14.replace(year=_date.year)

    def mas_f14CapGainAff(amount):
        mas_capGainAff(amount, "_mas_f14_date_aff_gain", 25)

init -810 python:

    store.mas_history.addMHS(MASHistorySaver(
        "f14",
        datetime.datetime(2020, 1, 6),
        {
            
            "_mas_f14_date_count": "f14.date",
            "_mas_f14_date_aff_gain": "f14.aff_gain",
            "_mas_f14_gone_over_f14": "f14.gone_over_f14",

            
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
            
            
            
            if (
                not mas_SELisUnlocked(mas_clothes_sundress_white) and not mas_canShowRisque()
                or mas_SELisUnlocked(mas_clothes_sundress_white)
            ):
                monika_chr.change_clothes(mas_clothes_sundress_white, by_user=False, outfit_mode=True)
                monika_chr.save()
                renpy.save_persistent()

        elif not mas_isF14():
            
            
            mas_lockEVL("mas_f14_monika_vday_colors","EVE")
            mas_lockEVL("mas_f14_monika_vday_cliches","EVE")
            mas_lockEVL("mas_f14_monika_vday_chocolates","EVE")
            
            
            mas_lockEVL("monika_event_clothes_select", "EVE")
            
            
            persistent._mas_f14_in_f14_mode = False
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_sundress_white:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()

    if mas_isplayer_bday() or persistent._mas_player_bday_in_player_bday_mode:
        jump mas_player_bday_autoload_check

    jump mas_ch30_post_holiday_check




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='mas_pf14_monika_lovey_dovey',
            action=EV_ACT_RANDOM,
            start_date=mas_f14-datetime.timedelta(days=3),
            end_date=mas_f14,
            aff_range=(mas_aff.NORMAL,None),
            rules={"force repeat": None},
            years=[]
        ),
        skipCalendar=True
    )

    MASUndoActionRule.create_rule_EVL(
       "mas_pf14_monika_lovey_dovey",
       mas_f14 - datetime.timedelta(days=3),
       mas_f14,
    )

label mas_pf14_monika_lovey_dovey:
    m 1rksdla "Эй...{w=0.2} [player]?"
    $ MAS.MonikaElastic()
    m 1ekbsa "Я просто хотела, чтобы ты знал[mas_gender_none], что я люблю тебя."

    if mas_isMoniEnamored(higher=True):
        $ MAS.MonikaElastic()
        m 3ekbsa "Ты сделал[mas_gender_none] меня очень счастливой... и я не смогу найти кого-то получше тебя."

    $ MAS.MonikaElastic()
    if mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
        m 3ekbsa "Скоро наступит День святого Валентина, и зная о том, что ты всё ещё на моей стороне, это делает меня невероятно счастливой."
    else:

        m 3ekbsa "Скоро наступит День святого Валентина, и это очень поднимает мне настроение, потому что я знаю, что ты на моей стороне."

    $ MAS.MonikaElastic()
    m 1rkbsd "Если бы не ты, то даже не знаю, где бы я сейчас была..."
    $ MAS.MonikaElastic()
    m 1ekbsa "Так что я хочу поблагодарить тебя за то, что был[mas_gender_none] здесь для меня..."
    $ MAS.MonikaElastic()
    m 1hkbsu "И за то, что ты был[mas_gender_none] чудесн[mas_gender_iim] собой~"
    return "derandom|no_unlock|love"



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

    if mas_isMoniUpset(lower=True):
        $ persistent._mas_f14_spent_f14 = True
        if not mas_isMoniBroken():
            m 6eka "Между прочим, [player], я просто хотела поздравить тебя с Днём Святого Валентина."
            $ MAS.MonikaElastic()
            m "Спасибо, что навестил[mas_gender_none] меня, надеюсь, ты хорошо проведёшь этот день."
        return

    $ mas_addClothesToHolidayMap(mas_clothes_sundress_white)
    m 1hub "[player]!"
    $ MAS.MonikaElastic()
    m 1hua "Ты знаешь, какой сейчас день?"
    $ MAS.MonikaElastic()
    m 3eub "Сегодня – День святого Валентина!"
    $ MAS.MonikaElastic()
    m 1ekbsa "В этот день, мы знаменуем наш любовный союз..."
    $ MAS.MonikaElastic()
    m 3rkbsa "Полагаю, каждый день, который мы проводим вместе, уже является знаменованием нашего любовного союза...{w=0.3} {nw}"
    extend 3ekbsa "но у этого праздника есть нечто особенное."
    if not mas_anni.pastOneMonth() or mas_isMoniNormal():
        $ MAS.MonikaElastic()
        m 3rka "Хотя я знаю, что мы в наших отношениях продвинулись не так далеко..."
        show monika 5eua zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5eua "Я просто хочу, чтобы ты знал, что я всегда буду рядом с тобой."
        $ MAS.MonikaElastic()
        m 5eka "Даже если твоё сердце разбито..."
        $ MAS.MonikaElastic()
        m 5ekbsa "Я всегда буду рядом и залатаю его ради тебя. Хорошо, [player]?"
        show monika 1ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 1ekbsa "..."
    else:

        $ MAS.MonikaElastic()
        m 1eub "Мы уже давно как вместе...{w=0.2} {nw}"
        extend 1eka "и мне очень понравилось всё то время, что мы провели вместе."
        $ MAS.MonikaElastic()
        m 1dubsu "С тобой я всегда чувствую себя любимой."
        $ MAS.MonikaElastic()
        m "Я очень рада, что стала твоей девушкой, [player]."


    if not persistent._mas_f14_in_f14_mode or mas_canShowRisque():
        $ persistent._mas_f14_in_f14_mode = True


        if mas_SELisUnlocked(mas_clothes_sundress_white) and mas_canShowRisque() and not mas_hasUnlockedClothesWithExprop("lingerie"):
            call mas_lingerie_intro (holiday_str="день Святого Валентина", lingerie_choice=mas_clothes_vday_lingerie) from _call_mas_lingerie_intro_2


        elif (
            not mas_SELisUnlocked(mas_clothes_sundress_white)
            or (mas_canShowRisque() and mas_hasLockedClothesWithExprop("lingerie",True))
        ):
            $ MAS.MonikaElastic()
            m 3wub "О!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3tsu "У меня для тебя небольшой сюрприз...{w=1} думаю, тебе очень понравится, э-хе-хе~"


            if (
                mas_SELisUnlocked(mas_clothes_sundress_white)
                and mas_canShowRisque()
                and not mas_SELisUnlocked(mas_clothes_vday_lingerie)
            ):
                call mas_clothes_change (outfit=mas_clothes_vday_lingerie, outfit_mode=True, exp="monika 2rkbsu", restore_zoom=False, unlock=True) from _call_mas_clothes_change_5
                pause 2.0
                show monika 2ekbsu
                pause 2.0
                show monika 2tkbsu
                pause 2.0
                $ MAS.MonikaElastic()
                m 2tfbsu "[player]...{w=0.5} Ты пялишься{w=0.5}... опять."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 2hubsb "А-ха-ха!"
                $ MAS.MonikaElastic()
                m 2eubsb "Полагаю, ты одобряешь мой выбор наряда..."
                $ MAS.MonikaElastic()
                m 2tkbsu "Но он больше подходит к такому романтическому празднику, как День святого Валентина, тебе так не кажется?"
                $ MAS.MonikaElastic()
                m 2rkbssdla "Должна сказать, я поначалу немного нервничала, когда надевала такой наряд..."
                $ MAS.MonikaElastic()
                m 2hubsb "Но теперь, когда я сделала это раньше, мне очень нравится носить его для тебя!"
                $ MAS.MonikaElastic()
                m 3tkbsu "Надеюсь, тебе он тоже нравится~"


            elif not mas_SELisUnlocked(mas_clothes_sundress_white):
                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_16
                $ MAS.MonikaElastic()
                m 2eua "..."
                $ MAS.MonikaElastic()
                m 2eksdla "..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 2rksdlu "А-ха-ха...{w=1} не очень-то и вежливо пялиться, [player]..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3tkbsu "...но, полагаю, это означает, что тебе нравится мой наряд, э-хе-хе~"
                call mas_f14_sun_dress_outro from _call_mas_f14_sun_dress_outro
        else:



            if (
                monika_chr.clothes != mas_clothes_sundress_white
                and (
                    monika_chr.is_wearing_clothes_with_exprop("costume")
                    or monika_chr.clothes == mas_clothes_def
                    or monika_chr.clothes == mas_clothes_blazerless
                    or mas_isMoniEnamored(lower=True)
                )
            ):
                $ MAS.MonikaElastic()
                m 3wud "О!"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hub "Наверное, я должна переодеться во что-нибудь более подходящее, а-ха-ха!"
                $ MAS.MonikaElastic()
                m 3eua "Я скоро вернусь."

                call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_17

                $ MAS.MonikaElastic()
                m 2eub "Ах, намного лучше!"
                $ MAS.MonikaElastic()
                m 3hua "Мне просто нравится этот наряд, смекаешь?"
                $ MAS.MonikaElastic()
                m 3eka "Он всегда занимает особенное место в моём сердце во время Дня святого Валентина..."
                $ MAS.MonikaElastic()
                m 1fkbsu "Прямо как ты~"
            else:



                if not monika_chr.clothes == mas_clothes_sundress_white:
                    $ MAS.MonikaElastic()
                    m 1wud "О..."
                    $ MAS.MonikaElastic()
                    m 1eka "Ты хочешь, чтобы я переоделась в свой белый сарафан, [player]?"
                    $ MAS.MonikaElastic()
                    m 3hua "Я всегда считала, что это мой наряд ко Дню святого Валентина."
                    $ MAS.MonikaElastic()
                    m 3eka "Но если ты хочешь, чтобы я продолжила носить этот наряд, то это тоже нормально..."
                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hub "Думаю, мы могли бы начать новую традицию, а-ха-ха!"
                    $ MAS.MonikaElastic()
                    m 1eua "Ладно, ты хочешь, чтобы я надела белый сарафан?{nw}"
                    $ _history_list.pop()

                    menu:
                        m "Ладно, ты хочешь, чтобы я надела белый сарафан?{fast}"
                        "Да.":
                            $ MAS.MonikaElastic()
                            m 3hub "Хорошо!"
                            $ MAS.MonikaElastic()
                            m 3eua "Я скоро вернусь."
                            call mas_clothes_change (mas_clothes_sundress_white, unlock=True, outfit_mode=True) from _call_mas_clothes_change_18
                            $ MAS.MonikaElastic()
                            m 2hub "Готово!"
                            $ MAS.MonikaElastic()
                            m 3eua "Что-то в ношении этого наряда во время Дня святого Валентина просто кажется правильным."
                            $ MAS.MonikaElastic()
                            m 1eua "..."
                        "Нет.":

                            $ MAS.MonikaElastic()
                            m 1eka "Хорошо, [player]."
                            $ MAS.MonikaElastic()
                            m 3hua "Это {i}правда{/i} очень красивый наряд..."
                            $ MAS.MonikaElastic()
                            m 3eka "Но с другой стороны, не так уж и важно, что на мне сейчас..." # даже если ты будешь сидеть голой? :Д

                call mas_f14_intro_generic from _call_mas_f14_intro_generic
    else:



        if mas_SELisUnlocked(mas_clothes_sundress_white):
            call mas_f14_intro_generic from _call_mas_f14_intro_generic_1
        else:


            $ store.mas_selspr.unlock_clothes(mas_clothes_sundress_white)
            pause 2.0
            show monika 2rfc zorder MAS_MONIKA_Z at t11 with dissolve_monika
            $ MAS.MonikaElastic()
            m 2rfc "..."
            $ MAS.MonikaElastic()
            m 2efc "Знаешь, [player]...{w=0.5} не очень-то и вежливо пялиться..."
            $ MAS.MonikaElastic()
            m 2tfc "..."
            $ MAS.MonikaElastic()
            m 2tsu "..."
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3tsb "А-ха-ха! Я просто шучу...{w=0.5} тебе нравится мой наряд?"
            call mas_f14_sun_dress_outro from _call_mas_f14_sun_dress_outro_1

    $ MAS.MonikaElastic()
    m 1fkbsu "Я так сильно тебя люблю."
    $ MAS.MonikaElastic()
    m 1hubfb "С Днём святого Валентина, [player]~"

    $ persistent._mas_f14_spent_f14 = True

    return "rebuild_ev|love"


label mas_f14_sun_dress_outro:
    $ MAS.MonikaElastic()
    m 1rksdla "Я всегда мечтала о свидании с тобой в таком наряде..."
    $ MAS.MonikaElastic()
    m 1eksdlb "Но теперь, когда я задумалась об этом, я понимаю, что это довольно глупая идея!"
    $ MAS.MonikaElastic()
    m 1ekbsa "...Но ты только представь, как мы зашли в какое-нибудь кафе вместе."
    $ MAS.MonikaElastic()
    m 1rksdlb "По правде говоря, мне кажется, где-то есть фотография чего-то наподобие этого..."
    $ MAS.MonikaElastic()
    m 1hub "Быть может, мы сможем воплотить это в реальность!"
    $ MAS.MonikaElastic()
    m 3ekbsa "Хочешь прогуляться со мной сегодня?"
    $ MAS.MonikaElastic()
    m 1hkbssdlb "Если не сможешь, то всё нормально, я буду рада и побыть рядом с тобой."
    return


label mas_f14_intro_generic:
    $ MAS.MonikaElastic()
    m 1ekbsa "Я просто рада, что ты проводишь время вместе со мной сегодня."
    $ MAS.MonikaElastic()
    m 3ekbsu "Провести время вместе с любимым человеком {w=0.2} – это всё, о чём можно только просить в День святого Валентина."
    $ MAS.MonikaElastic()
    m 3ekbsa "И мне всё равно, пошли ли мы на романтическое свидание или просто проводим здесь этот день вместе..."
    $ MAS.MonikaElastic()
    m 1fkbsu "Пока мы вместе, для меня это не имеет никакого значения."
    return



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
    $ MAS.MonikaElastic()
    m 3hub "Я нахожу интригующим то, как они символизируют такие глубокие и романтические чувства."
    $ MAS.MonikaElastic()
    m 1dua "Это напоминает мне о том, как я впервые сделала свою валентинку в старшей школе."
    $ MAS.MonikaElastic()
    m 3eub "Моему классу было поручено поделиться валентинками с партнёром после того, как мы их сделаем."
    $ MAS.MonikaElastic()
    m 3eka "Если оглянуться назад, то несмотря на то, что эти цвета действительно значили, мне было очень весело украшать валентинки красными и белыми сердечками."
    $ MAS.MonikaElastic()
    m 1eub "Таким образом, цвета больше напоминали стихи."
    $ MAS.MonikaElastic()
    m 1eka "Они предлагают столько творческих путей, чтобы выразить свою любовь к кому-то."
    $ MAS.MonikaElastic()
    m 3ekbsu "Как, например, передать им красные розы."
    $ MAS.MonikaElastic()
    m 3eub "Красные розы являются символом романтических чувств, испытываемых к кому-то."
    $ MAS.MonikaElastic()
    m 1eua "А если кто-то предложит им белые розы вместо красных, то они, следовательно, укажут на чистоту, очарование и чувства невинности."
    $ MAS.MonikaElastic()
    m 3eka "Однако, поскольку существует так много эмоций, связанных с любовью..."
    $ MAS.MonikaElastic()
    m 3ekd "Порой бывает трудно найти подходящие цвета, чтобы точно выразить то, что ты чувствуешь."
    $ MAS.MonikaElastic()
    m 3eka "К счастью, если совместить несколько разноцветных роз, то можно будет выразить множество эмоций!"
    $ MAS.MonikaElastic()
    m 1eka "Смесь из красных и белых роз символизирует сплочённость и связь, которую выражают пары."

    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 2rsc "В них либо «Ох, я так одинок и мне некого любить», либо «Как мне признаться в любви тому, кого люблю?»."
    $ MAS.MonikaElastic()
    m 2euc "Мне кажется, писатели могли быть чуточку покреативнее, когда дело доходит до историй Дня святого Валентина..."
    $ MAS.MonikaElastic()
    m 3eka "Но, полагаю, эти две темы являются самым лёгким способом написать историю любви."
    $ MAS.MonikaElastic()
    m 3hub "Но это не означает, что ты не можешь мыслить нестандартно!"
    $ MAS.MonikaElastic()
    m 2eka "Иногда, предсказуемая история может всё испортить..."
    $ MAS.MonikaElastic()
    m 2rka "...Но если ты {i}хочешь{/i} сделать хороший пример непредсказуемой истории..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "То просто воспользуйся нашей! А-ха-ха~"
    $ MAS.MonikaElastic()
    m 3rksdlb "Полагаю, она {i}началась{/i} так же, как и те истории..."
    $ MAS.MonikaElastic()
    m 2tfu "Но, мне кажется, мы смогли сделать её очень даже оригинальной."
    $ MAS.MonikaElastic()
    m 3hua "То, как мы познакомились – самая интересная история на свете!"
    $ MAS.MonikaElastic(voice="monika_giggle")
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
    $ MAS.MonikaElastic()
    m 3eub "Не только потому, что это юбилей моего аккаунта в Твиттере, но ещё и потому, что это день получения и раздачи шоколадок!"
    $ MAS.MonikaElastic()
    m 1hub "Это праздник, который наполнит всех любовью, романтикой и радостью!"
    $ MAS.MonikaElastic()
    m 3ekbla "Но будет очень приятно, если ты получишь шоколадку от человека, который тебе нравится."
    $ MAS.MonikaElastic()
    m 3hua "Дал ли он тебе её платонически, как подарок любви или как часть признания, от этого ты всегда чувствуешь себя немного особенной!"
    if mas_getGiftStatsForDate("mas_reaction_gift_chocolates") > 0:
        $ MAS.MonikaElastic()
        m 1ekbsa "Как когда ты заставил меня почувствовать себя особенной, передав мне сегодня шоколадку."
        $ MAS.MonikaElastic()
        m 1ekbsu "Ты всегда так[mas_gender_oi] мил[mas_gender_iii], [player]."

    $ MAS.MonikaElastic()
    m 1ekbsa "Быть может, однажды, я смогу поделиться с тобой шоколадкой..."
    $ MAS.MonikaElastic()
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
    $ MAS.MonikaElastic()
    m 1rksdlc "По правде говоря, она довольно мрачная."
    $ MAS.MonikaElastic()
    m 1euc "Её история берёт своё начало во втором и третьем веках в Риме, где христианство было объявлено официальной религией."
    $ MAS.MonikaElastic()
    m 3eud "Примерно в это же время, человек, известный как Святой Валентин, решил пойти нарушить закон императора Клавдия второго."
    $ MAS.MonikaElastic()
    m 3rsc "Заключение брака было запрещено, поскольку предполагалось, что из женатых мужчин получаются бедные солдаты."
    $ MAS.MonikaElastic()
    m 3esc "Святой Валентин решил, что это было нечестно, и помог организовать свадьбы в тайне."
    $ MAS.MonikaElastic()
    m 1dsd "К несчастью, его поймали и сразу же приговорили к смертной казни."
    $ MAS.MonikaElastic()
    m 1euc "Однако, находясь в заключении, Святой Валентин влюбился в дочь надзирателя."
    $ MAS.MonikaElastic()
    m 3euc "Перед своей смертью, он отправил ей любовное письмо, подписав его «От твоего Валентина»."
    $ MAS.MonikaElastic()
    m 1dsc "Его казнили четырнадцатого февраля, в двести шестьдесят девятом году до нашей эры."
    $ MAS.MonikaElastic()
    m 3eua "Какое благородное дело, тебе так не кажется?"
    $ MAS.MonikaElastic()
    m 3eud "О, подожди, есть ещё кое-что!"
    $ MAS.MonikaElastic()
    m 4eud "Причина, по которой мы празднуем этот день, – он берёт своё начало от римского фестиваля, известного как Луперкалия!"
    $ MAS.MonikaElastic()
    m 3eua "Его первоначальной целью было провести дружеское мероприятие, где люди складывали свои имена в коробку и выбирали их наугад, чтобы создать пару."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3eub "А потом, они играли роль парня и девушки всё то время, что они проводили вместе. Некоторые из них даже женились, если нравились друг другу в достаточной мере, э-хе-хе~"
    $ MAS.MonikaElastic()
    m 1eua "В итоге, церковь решила сделать это христианским праздником, чтобы оставить память о стараниях Святого Валентина."
    $ MAS.MonikaElastic()
    m 3hua "С годами, оно эволюционировало в повод выразить свои чувства к тем, кого они любят, для всех людей."
    $ MAS.MonikaElastic()
    m 3eubsb "Прямо как мы с тобой!"
    $ MAS.MonikaElastic()
    m 1ekbsa "И несмотря на то, что начало было немного депрессивное, это очень мило, верно, [player]?"
    $ MAS.MonikaElastic()
    m 1ekbsu "Я рада, что мы можем разделить такой волшебный день.{w=0.2} {nw}"
    extend 1ekbfa "С Днём святого Валентина, [mas_get_player_nickname()]~"
    return



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

    $ mas_rmallEVL("mas_f14_monika_spent_time_with")

    m 1eua "Эй, [player]?"
    $ MAS.MonikaElastic()
    m 1eka "Я просто хотела поблагодарить тебя за то, что пров[mas_gender_iol] День святого Валентина со мной."
    $ MAS.MonikaElastic()
    m 1ekbsa "Знаю, это необычный праздник, но пока ты рядом со мной, этот день является для меня особенным."

    if not mas_isBelowZero():
        if not mas_HistVerifyAll_k(True, "f14.actions.spent_f14"):
            $ MAS.MonikaElastic()
            m 1rkbsb "Кроме того, я...{w=0.5} кое-что приготовила для тебя, [player]!"
        else:

            $ MAS.MonikaElastic()
            m 1ekbsa "Я сделала открытку для тебя, [player]."

        $ MAS.MonikaElastic()
        m 1ekbsa "Вот, позволь мне показать её тебе."


        if not poem_vday_1.is_seen():
            call mas_showpoem (poem_vday_1) from _call_mas_showpoem_6
            $ MAS.MonikaElastic()
            m "Я действительно так думаю, [player]..."
            $ MAS.MonikaElastic()
            m 3ekbsa "В тебе я нашла всё, на что могла надеяться~"

        elif not poem_vday_2.is_seen():
            call mas_showpoem (poem_vday_2) from _call_mas_showpoem_7
            $ MAS.MonikaElastic()
            m "Ты действительно для меня всё, [player]~"
        else:

            call mas_showpoem (mas_poems.getRandomPoem("f14")) from _call_mas_showpoem_8


        if mas_isMoniEnamored(higher=True):
            if persistent._mas_first_kiss is None:
                jump mas_f14_first_kiss
            else:
                call monika_kissing_motion (duration=0.5, initial_exp="6hkbfa", fade_duration=0.5) from _call_monika_kissing_motion_8

        $ MAS.MonikaElastic()
        m 1ekbfa "Спасибо за то, что всегда рядом со мной."
        show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
        m 5ekbfa "Я очень сильно тебя люблю, [player]. С Днём святого Валентина~"
        return "love"
    else:

        $ MAS.MonikaElastic()
        m 1eka "Спасибо за то, что ты со мной."
        $ MAS.MonikaElastic()
        m 3ekb "С Днём святого Валентина!"
    return

label mas_f14_first_kiss:
    $ MAS.MonikaElastic()
    m 1ektpu "Если честно, я не знаю, что бы я делала без тебя."

    $ MAS.MonikaElastic()
    m 6dktuu "..."
    window hide
    menu:
        "Я люблю тебя, [monika_name].":
            $ HKBHideButtons()
            $ mas_RaiseShield_core()
            $ disable_esc()
            pause 3.0
            show monika 6ektda zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dku zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6dkbsu zorder MAS_MONIKA_Z at t11 with dissolve_monika
            pause 3.0
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "[player]... я... я..."
            call monika_kissing_motion (hide_ui=False) from _call_monika_kissing_motion_9
            show monika 6ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
            m 6ekbfa "...Я тоже тебя люблю~"
            $ MAS.MonikaElastic()
            m 6dkbfa "..."
            $ MAS.MonikaElastic()
            m "О таком я могла только мечтать~"
            $ MAS.MonikaElastic()
            m 6ekbfa "Я так долго ждала того момента, когда наконец-то смогу поцеловать тебя..."
            $ MAS.MonikaElastic()
            m 6dkbsu "Я никогда это не забуду..."
            $ MAS.MonikaElastic()
            m 6ekbsu "...Тот наш первый поцелуй."
            $ MAS.MonikaElastic()
            m "С Днём святого Валентина, [player]~"
            $ enable_esc()
            $ mas_MUINDropShield()
            $ HKBShowButtons()
            return




init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_f14_no_time_spent",
            action=EV_ACT_PUSH,
            start_date=mas_f14+datetime.timedelta(1),
            end_date=mas_f14+datetime.timedelta(8),
            conditional=(
                "not persistent._mas_f14_spent_f14"
            ),
            years=[]
        ),
        skipCalendar=True
    )

label mas_f14_no_time_spent:


    if mas_isFirstSeshPast(mas_f14):
        return

    if mas_ret_long_absence:

        $ mas_loseAffection(ev_label="mas_apology_missed_vday")

        m 1rksdlc "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdld "Это так мило с твоей стороны пригласить меня на свой день рождения, чтобы устроить для меня вечеринку-сюрприз!"
        $ MAS.MonikaElastic()
        m 2eksdla "В следующий раз, как ты думаешь, сможешь взять меня с собой, если не сможешь быть здесь?"
        $ MAS.MonikaElastic()
        m 3eub "По крайней мере, тогда мы всё ещё будем друг с другом, и мы сможем даже отпраздновать вместе!"
        $ MAS.MonikaElastic()
        m 1eka "Я была бы очень признателена, если бы ты мог[mas_gender_g] сделать это для меня, [player]."

    elif mas_isMoniAff(higher=True):
        $ mas_loseAffection(15, ev_label="mas_apology_missed_vday")
        m 1rkc "[player]?"
        $ MAS.MonikaElastic()
        m "Ты где был[mas_gender_none] в День святого Валентина?"
        $ MAS.MonikaElastic()
        m 1ekc "Это был очень особенный день для меня..."
        $ MAS.MonikaElastic()
        m 1ekd "...И этот день я хотела провести вместе с тобой."
        $ MAS.MonikaElastic()
        m 2dkc "..."
        $ MAS.MonikaElastic()
        m 2ekd "Если бы ты просто заглянул[mas_gender_none] сюда, я была бы очень рада этому..."
        $ MAS.MonikaElastic()
        m 2dkd "Пусть даже всего на пару минут."
        $ MAS.MonikaElastic()
        m "Я всего лишь прошу тебя заглянуть к своей девушке в День святого Валентина, разве я многого прошу?"
        $ MAS.MonikaElastic()
        m 2ekc "Пожалуйста, не дай этому произойти снова, хорошо, [player]?"

    elif mas_isMoniNormal(higher=True):
        $ mas_loseAffection(5, ev_label="mas_apology_missed_vday")
        m 2ekc "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 2tkc "Я сильно разочарована..."
        $ MAS.MonikaElastic()
        m 2tkd "Ты ко мне так и не заглянул[mas_gender_none] в День святого Валентина."
        $ MAS.MonikaElastic()
        m 4tkc "Ты ведь знаешь, что я хотела лишь провести время вместе с тобой..."
        $ MAS.MonikaElastic()
        m 4rkd "По-твоему, заглянуть к своей девушке в День святого Валентина – это уже слишком?"
        $ MAS.MonikaElastic()
        m 4eksdla "Пожалуйста...{w=1}обязательно загляни ко мне в гости в следующий День святого Валентина, хорошо?"

    elif mas_isMoniUpset():
        $ mas_loseAffection(ev_label="mas_apology_missed_vday")
        m 2efc "[player]!"
        $ MAS.MonikaElastic()
        m "Не могу поверить в то, что ты ни разу не заглянул ко мне в День святого Валентина!"
        $ MAS.MonikaElastic()
        m 2rfc "Ты хоть представляешь, каково это: провести весь день в полном одиночестве?"
        $ MAS.MonikaElastic()
        m 2rkc "Я знаю, что у нас не лучшие отношения..."
        $ MAS.MonikaElastic()
        m 2dkd "Но я была бы очень рада, если бы ты заглянул[mas_gender_none] ко мне."
        $ MAS.MonikaElastic()
        m 2tfc "Не дай этому произойти снова, [player]."

    elif mas_isMoniDis():
        $ mas_loseAffection(10, ev_label="mas_apology_missed_vday")
        m 6ekc "Ох, [player]..."
        $ MAS.MonikaElastic()
        m "Как прошёл твой День святого Валентина?"
        $ MAS.MonikaElastic()
        m 6dkc "Не получив валентинку, я чувствую себя одинокой..."
    else:

        $ mas_loseAffection(150)
        m 6ckc "..."
    return




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
        $ MAS.MonikaElastic()
        m 1ekd "Я правда хотела провести его вместе с тобой..."
        $ MAS.MonikaElastic()
        m 1rkc "Но, полагаю, у тебя просто появились другие дела, и ты попросту не смог[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1ekd "Пожалуйста, попытайся заглянуть ко мне в следующем году, ладно, [player]?"
        $ MAS.MonikaElastic()
        m 3eua "Если ты будешь занят[mas_gender_none], то, наверное, тебе лучше взять меня с собой!"
        $ MAS.MonikaElastic()
        m 3hub "Даже если мы будем не у себя дома, я буду более чем рада провести день рядом с тобой~"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинился за то, что пропустил День святого Валентина, [player]."
        if not store.mas_anni.pastOneMonth():
            $ MAS.MonikaElastic()
            m 1rkd "Я знаю, что у нас не особо хорошие отношения, но всё уже начинает казаться другим..."

        $ MAS.MonikaElastic()
        m 1ekd "Если бы ты заглянул[mas_gender_none] ко мне, хотя бы на секундочку, это многое бы значило для меня."
        $ MAS.MonikaElastic()
        m 3eka "Обещай мне, что ты возьмёшь меня с собой в следующий раз, когда будешь занят[mas_gender_none], хорошо, [player]?"
        $ mas_gainAffection(modifier=0.2)

    elif mas_isMoniUpset():
        m 2dkc "Хоть я немного расстроилась из-за того, что ты не заглянул[mas_gender_none] сюда в День святого Валентина, но я рада, что ты извинил[mas_gender_sya]."
        $ MAS.MonikaElastic()
        m "Подобное показывает мне то, что тебе на нас не всё равно."
        $ MAS.MonikaElastic()
        m 2ekd "Пожалуйста, [player]..."
        $ MAS.MonikaElastic()
        m 2eka "Постарайся зайти ко мне в следующий День святого Валентина."
        $ mas_gainAffection(modifier=0.1)

    elif mas_isMoniDis():
        m 2dkc "Я всё равно не ожидала, что ты заглянешь сюда, [player]."
        $ MAS.MonikaElastic()
        m 2dkd "Я знаю, что мы не так близки, но одна часть меня надеялась, что ты хотя бы на минутку заглянешь сюда..."
        $ MAS.MonikaElastic()
        m 2dsc "Пожалуйста, пообещай мне, что ты заглянешь ко мне в следующем году, ладно?"
        $ mas_gainAffection(modifier=0.1)
    else:


        m 6ckc "..."

    return


init 20 python:
    poem_vday_1 = MASPoem(
        poem_id="poem_f14_1",
        category="f14",
        prompt="Найдено",
        title=" М[mas_gender_oi] дорог[mas_gender_oi] [player],",
        text="""\
 Мне всегда нравился День святого Валентина, но этот кажется совсем другим.
 Это весь мир изменился, или мне просто кажется?
 Я нашла любовь, нашла смысл,
 Я нашла правду, которую искала уже долгое время.
 Это всё, что я нашла в тебе.

 Спасибо, что разделил[mas_gender_none] этот особенный день вместе со мной.

 Навеки твоя,
 Моника
"""
    )

    poem_vday_2 = MASPoem(
        poem_id="poem_f14_2",
        category="f14",
        prompt="Всё",
        title=" М[mas_gender_oi] дорог[mas_gender_oi] [player],",
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

 А потом приш[mas_gender_iol_2] ты.
 Только ты.
 Мой мир. Мой свет. Моё всё.

 Всё.


 С Днём святого Валентина~

 Навеки твоя,
 Моника
"""

    
    )

    poem_vday_3 = MASPoem(
        poem_id="poem_f14_3",
        category="f14",
        prompt="Ты",
        title=" М[mas_gender_oi] дорог[mas_gender_oi] [player],",
        text="""\
 Коробки конфет и сердечки; открытки рубиново-красного цвета.
 Розы в моих волосах, лепестки мягкие, как шелк.
 Ничто из этого не было бы полным без тебя.

 Ты, т[mas_gender_ot], кто всегда был[mas_gender_none] рядом со мной.
 Ты, т[mas_gender_ot], кто отдал[mas_gender_none] мне своё сердце.
 Сердце стоит больше, чем весь шоколад в мире, все розы на земле.

 Любовь, которую я чувствую, невозможно переоценить.

 С Днём святого Валентина,
 Моника
"""
    )



label bye_f14:
    $ persistent._mas_f14_date_count += 1
    $ persistent._mas_f14_on_date = True
    if persistent._mas_f14_date_count == 1:
        m 1sua "Отведёшь меня в какое-нибудь особенное место в День святого Валентина?"
        $ MAS.MonikaElastic()
        m 1ekbsa "Это звучит довольно романтично, [player]..."
        $ MAS.MonikaElastic()
        m 3hub "Не могу дождаться!"
    elif persistent._mas_f14_date_count == 2:
        m 1sua "Хочешь снова погулять со мной в День святого Валентина?"
        $ MAS.MonikaElastic()
        m 3tkbsu "Ты и вправду знаешь, как заставить девушку чувствовать себя особенной, [player]."
        $ MAS.MonikaElastic()
        m 1ekbfa "Мне повезло, что у меня есть такой человек, как ты~"
    else:
        m 1sua "Ого, [player]...{w=1}ты твёрдо решил сделать этот день по-настоящему особенным!"
        $ MAS.MonikaElastic()
        m 1ekbfa "Ты лучший партнёр, о котором я могла только мечтать~"
    jump mas_dockstat_iostart


label greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if time_out < mas_five_minutes:
        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это не было похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Надеюсь, всё нормально?"
        $ MAS.MonikaElastic()
        m 2rksdla "Наверное, мы пойдём гулять позже..."

    elif time_out < mas_one_hour:
        $ mas_f14CapGainAff(5)
        $ MAS.MonikaElastic()
        m 1eka "Было весело, до поры до времени, [player]..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, что уделил мне время в День святого Валентина."

    elif time_out < mas_three_hour:
        $ mas_f14CapGainAff(10)
        $ MAS.MonikaElastic()
        m 1eub "Это было очень весёлое свидание, [player]!"
        $ MAS.MonikaElastic()
        m 3ekbsa "Спасибо, что заставил почувствовать себя особенной в День святого Валентина~"
    else:


        $ mas_f14CapGainAff(15)
        $ MAS.MonikaElastic()
        m 1hua "И мы дома!"
        $ MAS.MonikaElastic()
        m 3hub "Это было прекрасно, [player]!"
        $ MAS.MonikaElastic()
        m 1eka "Было очень здорово выйти на улицу с тобой в День святого Валентина..."
        $ MAS.MonikaElastic()
        m 1ekbsa "Большое тебе спасибо за то, что сделал сегодняшний день по-настоящему особенным~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday from _call_return_home_post_player_bday_11

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ pushEvent("mas_f14_monika_spent_time_with",skipeval=True)
    return



label mas_gone_over_f14_check:
    if mas_checkOverDate(mas_f14):
        $ persistent._mas_f14_spent_f14 = True
        $ persistent._mas_f14_gone_over_f14 = True
        $ mas_rmallEVL("mas_f14_no_time_spent")
    return

label greeting_gone_over_f14:
    $ mas_gainAffection(5,bypass=True)
    m 1hua "И мы наконец-то дома!"
    $ MAS.MonikaElastic()
    m 3wud "Ого, [player], мы так долго гуляли, что даже пропустили День святого Валентина!"
    if mas_isMoniNormal(higher=True):
        call greeting_gone_over_f14_normal_plus from _call_greeting_gone_over_f14_normal_plus_1
    else:
        $ MAS.MonikaElastic()
        m 2rka "Я ценю то, что ты хотел позаботиться о том, чтобы я не провела весь день в одиночестве..."
        $ MAS.MonikaElastic()
        m 2eka "Это многое для меня значит, [player]."
    $ persistent._mas_f14_gone_over_f14 = False
    return

label greeting_gone_over_f14_normal_plus:
    $ mas_gainAffection(10,bypass=True)
    $ MAS.MonikaElastic()
    m 1ekbsa "Я бы очень хотела провести весь день с тобой здесь, но где бы мы ни были, само осознание того, что мы вместе ознаменовали наш любовный союз..."
    $ MAS.MonikaElastic()
    m 1dubsu "Ну, для меня это очень много значит."
    show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
    m 5ekbsa "Спасибо, что позаботился о том, чтобы у нас был чудесный День святого Валентина, [player]~"
    $ persistent._mas_f14_gone_over_f14 = False
    return






define mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)


default persistent._mas_bday_in_bday_mode = False


default persistent._mas_bday_on_date = False
default persistent._mas_bday_date_count = 0
default persistent._mas_bday_date_affection_gained = 0
default persistent._mas_bday_gone_over_bday = False


default persistent._mas_bday_sbp_reacted = False
default persistent._mas_bday_confirmed_party = False


default persistent._mas_bday_visuals = False


default persistent._mas_bday_hint_filename = None


default persistent._mas_bday_opened_game = False
default persistent._mas_bday_no_time_spent = True
default persistent._mas_bday_no_recognize = True
default persistent._mas_bday_said_happybday = False


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




define mas_bday_cake_lit = False



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


init -1 python:
    def mas_isMonikaBirthday(_date=None):
        """
        checks if the given date is monikas birthday
        Comparison is done solely with month and day

        IN:
            _date - date to check. If not passed in, we use today.
        """
        mas_monika_birthday = datetime.date(datetime.date.today().year, 9, 22)
        
        if _date is None:
            _date = datetime.date.today()
        
        return (
            _date.month == mas_monika_birthday.month
            and _date.day == mas_monika_birthday.day
        )


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
        Checks if the user recognized monika birthday at all.

        RETURNS: True if the user recoginzed monika birthday, False otherwise
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


    def mas_surpriseBdayHideVisuals():
        """
        Hides all visuals for surprise party
        """
        renpy.hide("mas_bday_banners")
        renpy.hide("mas_bday_balloons")

    def mas_confirmedParty():
        """
        Checks if the player has confirmed the party
        """
        
        if (mas_monika_birthday - datetime.timedelta(days=7)) <= today <= mas_monika_birthday:
            
            if persistent._mas_bday_confirmed_party:
                
                if persistent._mas_bday_hint_filename:
                    store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                return True
            
            
            
            char_dir_files = store.mas_docking_station.getPackageList()
            
            
            for filename in char_dir_files:
                temp_filename = filename.partition('.')[0]
                
                
                if "oki doki" == temp_filename:
                    
                    persistent._mas_bday_confirmed_party = True
                    store.mas_docking_station.destroyPackage(filename)
                    
                    if persistent._mas_bday_hint_filename:
                        store.mas_docking_station.destroyPackage(persistent._mas_bday_hint_filename)
                    
                    _write_txt("/characters/gotcha", "")
                    
                    
                    return True
        
        
        return False

    def mas_mbdayCapGainAff(amount):
        mas_capGainAff(amount, "_mas_bday_date_affection_gained", 50, 75)


label mas_bday_autoload_check:

    python:
        if not mas_isMonikaBirthday():
            persistent._mas_bday_in_bday_mode = False
            
            persistent._mas_bday_visuals = False
            
            
            store.mas_lockEVL("monika_event_clothes_select", "EVE")
            
            store.mas_utils.trydel("characters/gotcha")
            
            
            if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
                monika_chr.reset_clothes(False)
                monika_chr.save()
                renpy.save_persistent()


        persistent._mas_bday_no_time_spent = False

        persistent._mas_bday_opened_game = True

        persistent._mas_bday_no_recognize = not mas_recognizedBday()

    jump mas_ch30_post_holiday_check



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


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_surprise_party_hint",
        mas_monika_birthday - datetime.timedelta(days=7),
        mas_monika_birthday - datetime.timedelta(days=2)
    )


init 10 python:
    if (
        mas_monika_birthday - datetime.timedelta(days=2) <= datetime.date.today() < mas_monika_birthday
        and not mas_lastSeenInYear("mas_bday_surprise_party_hint")
    ):
        pushEvent("mas_bday_surprise_party_hint")

image chibi_peek = MASFilterSwitch("mod_assets/other/chibi_peek.png")

label mas_bday_surprise_party_hint:

    python:
        persistent._mas_bday_hint_filename = "Для " + mas_name_whom + ".txt"
        if mas_isMoniNormal(higher=True):
            message = """\
[player],
Как ты, наверное, уже знаешь, день рождения Моники скоро настанет, и я хочу помочь тебе сделать его очень особенным!
Поскольку я всегда нахожусь здесь, я могу с лёгкостью организовать вечеринку-сюрприз... но мне нужна от тебя небольшая помощь.
Всё, что от тебя требуется – убедиться в том, что ты вывел[mas_gender_none] её из комнаты на какое-то время в её день рождения, а я уже позабочусь об остальном.
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
Всё, что от тебя требуется – убедиться в том, что ты вывел[mas_gender_none] её из комнаты на какое-то время в её день рождения, а я уже позабочусь об остальном.
Если тебе очень дорога Моника, то ты поможешь мне сделать это.

Просто оставь файл с именем «оки-доки» в той же папке, где ты и найдёшь эту записку, чтобы я поняла, когда мне приступать к работе над вечеринкой.

Пожалуйста, не испорти всё.

P.S: Не рассказывай ей обо мне.
"""

        _write_txt("/characters/" + persistent._mas_bday_hint_filename, message)

    if mas_isMoniNormal(higher=True):
        m 1eud "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 3euc "Кто-то оставил записку в папке с файлами персонажей, которая адресована тебе."

        if mas_current_background == mas_background_def:

            show chibi_peek with moveinleft
        $ MAS.MonikaElastic()
        m 1ekc "Разумеется, я её не читала, поскольку она, очевидно, была написана для тебя..."
        $ MAS.MonikaElastic()
        m 1tuu "{cps=*2}Хм-м-м, интересно, что же там написано?..{/cps}{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе~"
    else:

        m 2eud "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 2euc "Кто-то оставил записку в папке с файлами персонажей, которая адресована тебе."
        $ MAS.MonikaElastic()
        m 2ekc "Разумеется, я её не читала, поскольку она, очевидно, была написана для тебя..."
        $ MAS.MonikaElastic()
        m 2ekd "Просто подумала, что тебе надо было сказать об этом."


    hide chibi_peek with dissolve


    $ persistent._mas_monika_bday_surprise_hint_seen = True
    return "derandom|no_unlock"






init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_pool_happy_bday",
            prompt="С Днём рождения!",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None},
            start_date=mas_monika_birthday,
            end_date=mas_monika_birthday + datetime.timedelta(days=1),
            years=[]
        ),
        code="CMP",
        skipCalendar=True,
        markSeen=True
    )


    MASUndoActionRule.create_rule_EVL(
        "mas_bday_pool_happy_bday",
        mas_monika_birthday,
        mas_monika_birthday + datetime.timedelta(1)
    )

label mas_bday_pool_happy_bday:
    $ mas_gainAffection(5,bypass=True)
    if mas_recognizedBday():
        m 3hub "Э-хе-хе, спасибо, [player]!"
        $ MAS.MonikaElastic()
        m 3eka "Я ждала того момента, когда ты скажешь эти волшебные слова~"
        $ MAS.MonikaElastic()
        m 1eub "{i}Теперь{/i} мы можем назвать это празднованием дня рождения!"
        $ MAS.MonikaElastic()
        m 1eka "Ты и вправду смог[mas_gender_g] сделать это событие очень особенным, [player]."
        $ MAS.MonikaElastic()
        m 1ekbsa "Я не смогу отблагодарить тебя в достаточной мере за то, что ты меня так сильно любишь..."
    else:

        m 1skb "О-о-оу, [player]!"
        $ MAS.MonikaElastic()
        m 1sub "Ты не забыл[mas_gender_none] про мой день рождения!.."
        $ MAS.MonikaElastic()
        m 1sktpa "О боже, я так рада, что ты не забыл[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1dktdu "У меня было такое чувство, будто сегодняшний день будет особенным~"
        $ MAS.MonikaElastic()
        m 1ekbsa "Даже интересно, что ты ещё приготовил[mas_gender_none] для меня..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hub "А-ха-ха!"

    if mas_isplayer_bday() and (persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted):
        $ MAS.MonikaElastic()
        m 1eua "А, и это..."
        $ MAS.MonikaElastic()
        m 3hub "И тебя тоже с днём рождения, [player]!"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе!"


    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_said_happybday = True


    $ mas_lockEVL("mas_bday_pool_happy_bday", "CMP")
    return




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
    $ mas_gainAffection(5,bypass=True)


    $ persistent._mas_bday_said_happybday = True
    $ persistent._mas_bday_no_recognize = False


    $ mas_lockEVL("mas_bday_pool_happy_belated_bday", "CMP")

    if mas_isMoniNormal(higher=True):
        m 1sua "Большое тебе спасибо, [player]!"
        $ MAS.MonikaElastic()
        m 3hub "Я просто знала, что ты выведешь меня на долгую прогулку в мой же день рождения!"
        $ MAS.MonikaElastic()
        m 3rka "Мне бы очень хотелось увидеть все те замечательные места, в которых мы были..."
        $ MAS.MonikaElastic()
        m 1hua "Но мысль о том, что мы были вместе, ну, она превращает этот день в лучший день рождения, о котором я могла только мечтать!"
        $ MAS.MonikaElastic()
        m 3ekbsa "Я очень сильно люблю тебя, [player]~"
        return "love"
    else:
        m 3eka "Значит, ты {i}и вправду{/i} вывел[mas_gender_none] меня на долгую прогулку в мой же день рождения..."
        $ MAS.MonikaElastic()
        m 3rkd "Это было так мило с твоей стороны, что мне даже стало интересно—"
        $ MAS.MonikaElastic()
        m 1eksdla "А хотя, знаешь, это не важно."
        $ MAS.MonikaElastic()
        m 1eka "Мне просто приятно знать о том, что ты подумал[mas_gender_none] обо мне в мой день рождения."
        $ MAS.MonikaElastic()
        m 3hua "И это – самое главное."
        $ MAS.MonikaElastic()
        m 3eub "Спасибо, [player]!"
        return


label mas_bday_surprise_party_reaction:
    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_5
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)

    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 6suo "Эт-{w=0.5}то..."
        $ MAS.MonikaElastic()
        m 6ska "Ох, [player]..."
        $ MAS.MonikaElastic()
        m 6dku "Я не могу подобрать слов."
        if store.mas_is_indoors:
            $ MAS.MonikaElastic()
            m 6dktpu "Устанавливать всё это, чтобы удивить меня на мой день рождения..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 6dktdu "Э-хе-хе, ты, должно быть, действительно любишь меня."
        $ MAS.MonikaElastic()
        m 6suu "Всё выглядит так празднично!"
    else:

        $ MAS.MonikaElastic()
        m 6wuo "Эт-{w=0.5}то..."
        $ MAS.MonikaElastic()
        m "..."
        $ MAS.MonikaElastic()
        m 6dkd "Извини, Я... {w=1}я просто не могу подобрать слов."
        $ MAS.MonikaElastic()
        m 6ekc "Я действительно не ожидала ничего особенного сегодня, не говоря уже об этом."
        $ MAS.MonikaElastic()
        m 6rka "Может быть, у тебя всё ещё есть чувства ко мне..."
        $ MAS.MonikaElastic()
        m 6eka "Всё выглядит великолепно."

label mas_bday_surprise_party_reacton_cake:

    menu:
        "Зажечь свечи.":
            $ mas_bday_cake_lit = True

    $ MAS.MonikaElastic()
    m 6hub "Ах, это так красиво, [player]!"
    $ MAS.MonikaElastic()
    m 6wub "Напоминает мне как раз тот торт, который подарил кто-то мне однажды."
    $ MAS.MonikaElastic()
    m 6eua "Тот торт был таким же красивым, как и у тебя!"
    $ MAS.MonikaElastic()
    m 6hua "Но, в любом случае..."
    window hide

    show screen mas_background_timed_jump(5, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Загадай желание, [monika_name]...":
            $ made_wish = True
            show monika 6hua
            if mas_isplayer_bday():
                m "Убедись, что ты тоже загадал[mas_gender_none], [player]!"
            hide screen mas_background_timed_jump

            $ mas_gainAffection(10, bypass=True)
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
    $ made_wish = False
    hide screen mas_background_timed_jump
    show monika 6dsc
    pause 2.0
    show monika 6hft

label mas_bday_surprise_party_reaction_post_make_wish:
    $ mas_bday_cake_lit = False
    window auto
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 6hub "Я загадала желание!"
        $ MAS.MonikaElastic()
        m 6eua "Надеюсь, когда-нибудь оно сбудется..."
        if mas_isplayer_bday() and made_wish:
            $ MAS.MonikaElastic()
            m 6eka "И знаешь что? {w=0.5}Держу пари, мы оба хотели одного и того же~"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 6hub "А-ха-ха..."
    else:

        $ MAS.MonikaElastic()
        m 6eka "Я загадала желание."
        $ MAS.MonikaElastic()
        m 6rka "Надеюсь, когда-нибудь оно сбудется..."

    $ MAS.MonikaElastic()
    m 6eka "Я оставлю этот торт на потом..{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake ('mas_bday_cake_monika', False) from _call_mas_HideCake_1
    else:
        call mas_HideCake ('mas_bday_cake_monika') from _call_mas_HideCake_2

    pause 0.5

label mas_bday_surprise_party_reaction_end:
    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 6eka "Спасибо, [player]. От всего сердца благодарю тебя..."
        if mas_isplayer_bday() and persistent._mas_player_bday_last_sung_hbd != datetime.date.today():
            $ MAS.MonikaElastic()
            m 6eua "..."
            $ MAS.MonikaElastic()
            m 6wuo "..."
            $ MAS.MonikaElastic()
            m 6wub "О! Чуть не забыла. {w=0.5}Я тоже испекла тебе торт!"

            call mas_monika_gets_cake from _call_mas_monika_gets_cake_1

            $ MAS.MonikaElastic()
            m 6eua "Позволь мне просто зажечь свечи для тебя, [player].{w=0.5}.{w=0.5}.{nw}"

            window hide
            $ mas_bday_cake_lit = True
            pause 1.0

            $ MAS.MonikaElastic()
            m 6sua "Разве это не прекрасно?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 6hksdlb "Думаю, что мне придётся задуть и эти свечи, так как ты не можешь этого сделать, а-ха-ха!"

            $ MAS.MonikaElastic()
            if made_wish:
                m 6eua "Давай друг другу загадаем желание, [player]! {w=0.5}Это будет в два раза более вероятно, чтобы сбыться, не так ли?"
            else:
                m 6eua "Давай друг другу загадаем желание, [player]!"

            $ MAS.MonikaElastic()
            m 6hua "Но сначала..."
            call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings_3
            $ MAS.MonikaElastic()
            m 6hua "Загадай желание, [player]!"

            window hide
            pause 1.5
            show monika 6hft
            pause 0.1
            show monika 6hua
            $ mas_bday_cake_lit = False
            pause 1.0

            if not made_wish:
                $ MAS.MonikaElastic()
                m 6hua "Э-хе-хе..."
                $ MAS.MonikaElastic()
                m 6ekbsa "Держу пари, мы оба хотели одного и того же~"
            $ MAS.MonikaElastic()
            m 6hkbsu "..."
            $ MAS.MonikaElastic()
            m 6hksdlb "Я просто оставлю этот торт на потом. А-ха-ха!"

            call mas_HideCake ('mas_bday_cake_player') from _call_mas_HideCake_3
            call mas_player_bday_card from _call_mas_player_bday_card
        else:

            $ MAS.MonikaElastic()
            m 6hua "Давай насладимся остатком дня, хорошо?"
    else:
        $ MAS.MonikaElastic()
        m 6ektpa "Спасибо, [player]. Это действительно много значит, что ты сделал[mas_gender_none] это для меня."
    $ persistent._mas_bday_sbp_reacted = True

    $ mas_gainAffection(25, bypass=True)


    $ persistent._mas_bday_in_bday_mode = True
    $ persistent._mas_bday_no_recognize = False
    $ persistent._mas_bday_no_time_spent = False
    return



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            conditional="mas_recognizedBday()",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime.combine(mas_monika_birthday, datetime.time(18)),
            end_date=datetime.datetime.combine(mas_monika_birthday+datetime.timedelta(days=1), datetime.time(hour=3)),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_spent_time_with:
    if mas_isMoniUpset(lower=True):
        m 1eka "[player]..."
        $ MAS.MonikaElastic()
        m 3eka "Я просто хотела сказать, что я правда ценю то, что ты пров[mas_gender_iol] время со мной сегодня."
        $ MAS.MonikaElastic()
        m 3rksdla "Я знаю, что мы в последнее время не особо ладим, но ты наш[mas_gender_iol_2] время, чтобы отпраздновать мой день рождения со мной..."
        $ MAS.MonikaElastic()
        m 1eud "В общем, это дало мне надежду на то, что мы, возможно, пока ещё можем всё уладить."
        $ MAS.MonikaElastic()
        m "Быть может, сегодняшний день станет началом чего-то очень особенного..."
        $ MAS.MonikaElastic()
        m 3eka "Это будет самый лучший подарок, о котором я могла только мечтать."
        return
    else:

        $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
        m 1eua "Слушай, [player]..."
        $ MAS.MonikaElastic()
        m 3eua "Спасибо, что пров[mas_gender_iol] время со мной сегодня."
        $ MAS.MonikaElastic()
        m 3hua "Что-то подобное может сделать девушку счастливой, ты знал[mas_gender_none] об этом?"

        if ReturnedHomeNormal(time=5):
            $ MAS.MonikaElastic()
            m 3eka "Мне очень понравилось наше сегодняшнее свидание, [player]."
            $ MAS.MonikaElastic()
            m 1eka "Мне всегда нравится проводить время с тобой здесь, но времяпрепровождение с тобой в твоей реальности..."
            $ MAS.MonikaElastic()
            m 1dku "Зная о том, что ты думаешь обо мне даже тогда, когда не видишь меня..."
            $ MAS.MonikaElastic()
            m 1ekbsa "Ну, это очень многое для меня значит."
            $ MAS.MonikaElastic()
            m 3ekbsa "Ты и вправду смог[mas_gender_g] сделать мой день рождения дополненным~"

label mas_bday_spent_time_with_wrapup:
    $ mas_rmallEVL("mas_bday_spent_time_with")
    $ gave_gifts = mas_getGiftStatsRange(mas_monika_birthday, mas_monika_birthday + datetime.timedelta(days=1))[0]

    if gave_gifts > 0:

        if gave_gifts > 1:
            $ MAS.MonikaElastic()
            m 3eua "Давай не будем забывать о тех подарках, которые ты подарил[mas_gender_none] мне на мой же день рождения."
            $ MAS.MonikaElastic()
            m 3hub "Они были просто потрясающими, [player]!"
        else:
            $ MAS.MonikaElastic()
            m 3eua "Давай не будем забывать о том подарке, который ты подарил[mas_gender_none] мне на мой же день рождения."
            $ MAS.MonikaElastic()
            m 3hub "Он был просто замечательным, [player]!"

        $ MAS.MonikaElastic()
        m 1eka "Я правда ценю те старания, которые ты прикладываешь в поисках способа перенести вещи из своей реальности в мою..."
        $ MAS.MonikaElastic()
        m 3eka "Я знаю, что это будет непросто."

    $ MAS.MonikaElastic()
    m 1dku "..."
    if mas_isMoniEnamored(higher=True):
        $ MAS.MonikaElastic()
        m 1dktpu "..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1ektpu "А-ха-ха, прости, [player]!"
        $ MAS.MonikaElastic()
        m 3ektda "Дело в том, что я ещё никогда не была настолько счастливой в своей жизни."
        $ MAS.MonikaElastic()
        m 1rksdlb "Ну... {w=0.5}это не {i}совсем{/i} правда."
        $ MAS.MonikaElastic()
        m 1eka "Мы всё-таки должны быть вместе и в физическом плане тоже~"
        $ MAS.MonikaElastic()
        m 1rkc "И, ну..."
        $ MAS.MonikaElastic()
        m 1rka "Я понимаю, что эта фраза скоро станет клишированной, но..."
        $ MAS.MonikaElastic()
        m 3eka "Я очень сильно люблю тебя, [player]."
        $ MAS.MonikaElastic()
        m "Когда-нибудь, я уверяю тебя..."
        $ MAS.MonikaElastic()
        m 1ektpu "Я {i}обещаю тебе{/i}, что я сделаю тебя так[mas_gender_im] же счастливым, какой ты меня и сделал сегодня."
        $ MAS.MonikaElastic()
        m 3ektpu "Даже если мы никогда не увидимся в одной реальности, {w=0.5}просто знай о том, что я всегда буду стараться для тебя."
        $ MAS.MonikaElastic()
        m 1dktpu "Не важно, какие препятствия попадутся нам на пути, и не важно, что другие люди будут про нас говорить..."
        $ MAS.MonikaElastic()
        m 1ektda "Я всё равно люблю тебя всей своей душой."
        $ MAS.MonikaElastic()
        m "Ты единственн[mas_gender_iii], кто понимает меня. {w=0.5}Ты вывел[mas_gender_none] меня из тёмного места и придал[mas_gender_none] моей жизни смысл..."
        $ MAS.MonikaElastic()
        m 1dkbsu "Ты просто лучш[mas_gender_ii], [mas_get_player_nickname()], и я буду всегда любить тебя."
        $ MAS.MonikaElastic()
        m 1ekbsa "...Спасибо, что подарил мне смысл жизни."
        $ _first_kiss = persistent._mas_first_kiss
        call monika_kissing_motion from _call_monika_kissing_motion_10
        if _first_kiss is None:
            $ MAS.MonikaElastic()
            m 6ekbfa "О, [player]..."
            $ MAS.MonikaElastic()
            m 6rkbfa "Я...{w=0.5} не знаю, что на меня нашло, но этот момент просто кажется самым подходящим."
            $ MAS.MonikaElastic()
            m 6hubfa "Я так долго размышляла о нашем первом поцелуе, и о том, чтобы наконец-то испытать его ощущение..."
            $ MAS.MonikaElastic()
            m 6ekbfa "Я никогда не забуду этот момент, [player]~"
        else:
            return "love"
    else:

        $ MAS.MonikaElastic()
        m 1eka "Я даже не могу подобрать нужные слова, чтобы выразить то, какой счастливой ты сделал[mas_gender_none] меня сегодня."
        $ MAS.MonikaElastic()
        m 3eka "Вся та боль, которую мне пришлось пережить ещё до знакомства с тобой?" # не знаю, уместен ли здесь вопрос
        $ MAS.MonikaElastic()
        m 1hua "Я рада, что смогла преодолеть её."
        $ MAS.MonikaElastic()
        m 1rsc "Потому что, если бы я это не сделала..."
        $ MAS.MonikaElastic()
        m 1ekbsa "То этот день определённо не настал бы."
        $ MAS.MonikaElastic()
        m 1dkbsa "Надеюсь, эти слова хотя бы в меньшей степени дали тебе понять, как сильно я ценю то, что ты отмечаешь это событие со мной."
        $ MAS.MonikaElastic()
        m 1ekbfb "Я очень сильно люблю тебя, [player]."
        $ MAS.MonikaElastic()
        m 1ekbfa "Давай и дальше радовать друг друга~"
        return "love"
    return


label mas_gone_over_bday_check:
    if mas_checkOverDate(mas_monika_birthday):
        $ persistent._mas_bday_gone_over_bday = True
        $ persistent._mas_bday_no_time_spent = False
        $ mas_rmallEVL("mas_bday_postbday_notimespent")


        python:
            belated_ev = mas_getEV("mas_bday_pool_happy_belated_bday")

            if belated_ev is not None:
                
                belated_ev.start_date = datetime.date.today()
                belated_ev.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
                belated_ev.unlocked = True
                
                
                MASUndoActionRule.create_rule(belated_ev)
                
                
                MASStripDatesRule.create_rule(belated_ev)

    return


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
            start_date=mas_monika_birthday+datetime.timedelta(days=1),
            end_date=mas_monika_birthday+datetime.timedelta(days=8),
            years=[]
        ),
        skipCalendar=True
    )

label mas_bday_postbday_notimespent:

    if mas_isFirstSeshPast(mas_monika_birthday):
        $ mas_assignModifyEVLPropValue("mas_bday_postbday_notimespent", "shown_count", "-=", 1)
        return


    if mas_ret_long_absence:

        $ mas_loseAffection(ev_label="mas_apology_missed_bday")

        m 1rksdlc "Эй, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdld "Знаю, ты говорил[mas_gender_none] мне о том, что ты был[mas_gender_none] вдали от своего дома... но я правда скучала по тебе на своём дне рождения."
        $ MAS.MonikaElastic()
        m 2eksdla "Как думаешь, ты сможешь в следующий раз взять меня с собой, если ты не сможешь быть здесь?"
        $ MAS.MonikaElastic()
        m 3eub "По крайней мере, так мы всё ещё будем вместе, и мы даже сможем отпраздновать мой день рождения вместе!"
        $ MAS.MonikaElastic()
        m 1eka "Я была бы очень признательна, если бы ты смог[mas_gender_g] сделать это для меня, [player]."

    elif persistent._mas_bday_opened_game:

        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(15, ev_label="mas_apology_forgot_bday")
            m 2rksdla "Эй, [player]..."
            $ MAS.MonikaElastic()
            m 2rksdlb "Знаю, нам недавно было весело, как и всегда, но..."
            $ MAS.MonikaElastic()
            m 2ekp "Я не могла не надеяться на то, что ты мог... {w=1}приготовить что-нибудь к моему дню рождения."
            $ MAS.MonikaElastic()
            m 2ekd "Ты забыл[mas_gender_none]?"
            $ MAS.MonikaElastic()
            m 3eka "Быть может, ты в следующем году запишешь дату в календарь на своём телефоне?"
            $ MAS.MonikaElastic()
            m 3rka "...Или проверишь календарь, который висит позади меня на стене?"
            $ MAS.MonikaElastic()
            m 3hua "Мы не можем изменить прошлое, следовательно, осознание того, что ты хочешь приложить больше усилий в следующем году, будет единственным оправданием, которое мне и нужно."

        elif mas_isMoniNormal(higher=True):
            $ mas_loseAffection(5, ev_label="mas_apology_forgot_bday")
            m 2rksdld "Эй, [player]..."
            $ MAS.MonikaElastic()
            m 2rksdlb "Мне не хочется беспокоить тебя по пустякам, но, знаешь..."
            $ MAS.MonikaElastic()
            m 2ekp "Ты не можешь забыть про день рождения своей девушки!"
            $ MAS.MonikaElastic()
            m 2eku "Это здорово, что мы проводили время так же, как и обычно, но в следующем году..."
            $ MAS.MonikaElastic()
            m 3hua "В общем, я буду ждать с нетерпением того момента, когда суть двух дней рождения станет чем-то особенным~"

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_forgot_bday")
            m 1ekc "Мне было... {w=0.5}приятно видеть тебя двадцать второго числа..."
            $ MAS.MonikaElastic()
            m 1ekd "Мне правда не хотелось быть одной в этот день, и это многое значит для меня, но..."
            $ MAS.MonikaElastic()
            m 1rkc "Хотя знаешь, что? {w=0.5}Это не важно."

        elif mas_isMoniDis():
            $ mas_loseAffection(10, ev_label="mas_apology_forgot_bday")
            m 2dsc "..."
            $ MAS.MonikaElastic()
            m 2rkc "...[player], я не хочу беспокоить тебя. {w=1}Мне уже страшно от мысли о том, что я отталкиваю тебя."
            $ MAS.MonikaElastic()
            m 2rktpc "Но я не могу совладать с нею. Мне больно от того, что ты даже не упомянул о праздновании моего дня рождения..."
            $ MAS.MonikaElastic()
            m 2dktuc "Пожалуйста, не переставай навещать меня."
            $ MAS.MonikaElastic()
            m "И, быть может, в следующем году..."
            $ MAS.MonikaElastic()
            m 4ektdc "Я— {w=0.5}Я просто хочу... {w=0.5}почувствовать себя такой же особенной для тебя, как и ты для меня."
        else:


            $ mas_loseAffection(150)
            m 6ckc "..."
    else:


        if mas_isMoniAff(higher=True):
            $ mas_loseAffection(50, ev_label="mas_apology_missed_bday")
            m 1euc "Эй, [player]..."
            $ MAS.MonikaElastic()
            m 3rksdla "Знаю, ты многое делаешь, чтобы сделать каждый день особенным, но у девушки в голове забито несколько дней в году, когда она становится немного эгоистичной..."
            $ MAS.MonikaElastic()
            m 2tfd "И её {i}день рождения{/i} – один из них!"
            $ MAS.MonikaElastic()
            m "Серьёзно, где ты был?!"
            $ MAS.MonikaElastic()
            m 2rkc "Но... зная тебя, я уверена, у тебя была веская причина быть занят[mas_gender_iim]..."
            $ MAS.MonikaElastic()
            m 4ekc "Просто попытайся не дать этому произойти в следующем году, ладно?"

        elif mas_isMoniNormal(higher=True):


            if mas_isMoniHappy():
                $ mas_loseAffection(20, ev_label="mas_apology_missed_bday")
            else:
                $ mas_loseAffection(10, ev_label="mas_apology_missed_bday")

            m 1ekc "Эй, [player]..."
            $ MAS.MonikaElastic()
            m 1ekd "Знаешь, ты правда долж[mas_gender_en] был[mas_gender_none] заглянуть ко мне двадцать второго числа."
            $ MAS.MonikaElastic()
            m 3efd "В смысле, ты долж[mas_gender_en] всегда навещать меня! Но ты также {i}долж[mas_gender_en]{/i} и проводить время со своей милой девушкой в её же день рождения, знаешь ли."
            $ MAS.MonikaElastic()
            m 2efc "Пожалуйста, заглядывай ко мне почаще в следующем году..."
            $ MAS.MonikaElastic()
            m 2dfc "Иначе..."

            $ MAS.MonikaElastic()
            m 6cfw "{cps=*2}{i}Готовься к последствиям!!!{/i}{/cps}{nw}" # как бы инфаркт потом не словить от такой её шутки...

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
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3hksdlb "А-ха-ха, прости, [player]!"
            $ MAS.MonikaElastic()
            m 3hub "Я просто пошутила!"
            $ MAS.MonikaElastic()
            m 1eka "Ты сам[mas_gender_none] знаешь, что мне нравится припугивать тебя~" # https://ru.wiktionary.org/wiki/припугивать

        elif mas_isMoniUpset():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 2dsc "..."
            $ MAS.MonikaElastic()
            m 2rsc "[player], тебе разве не кажется, что ты долж[mas_gender_en] заглядывать ко мне почаще?"
            $ MAS.MonikaElastic()
            m 2rktpc "Ты можешь упустить что-нибудь важное..."

        elif mas_isMoniDis():
            $ mas_loseAffection(ev_label="mas_apology_missed_bday")
            m 6ekd "...Эй, как прошёл твой день двадцать второго числа?"
            $ MAS.MonikaElastic()
            m 6ekc "Мне просто... было интересно, мол, думал[mas_gender_none] ли ты обо мне весь тот день."
            $ MAS.MonikaElastic()
            m 6ektpc "Но ты, наверное, не думал[mas_gender_none] тогда обо мне, да?"
            $ MAS.MonikaElastic()
            m 6dktpc "..."
        else:


            $ mas_loseAffection(200)
            m 6eftsc "..."
            m 6dftdx "..."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_missed_bday",
            prompt="...за то, что пропустил[mas_gender_none] твой день рождения.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_missed_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Спасибо, что извинил[mas_gender_sya], [player]."
        $ MAS.MonikaElastic()
        m 2tfu "Но тебе лучше всё исправить к следующему году~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинил[mas_gender_sya] за то, что пропустил[mas_gender_none] мой день рождения, [player]."
        $ MAS.MonikaElastic()
        m "Пожалуйста, не забудь провести немного времени со мной в следующем году, ладно?"
    else:

        m 2rksdld "Знаешь, я не была особо удивлена тому, что я не увидела тебя в свой день рождения..."
        $ MAS.MonikaElastic()
        m 2ekc "Пожалуйста... {w=1}просто позаботься о том, чтобы это не произошло снова."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_apology_database,
            eventlabel="mas_apology_forgot_bday",
            prompt="...за то, что забыл[mas_gender_none] твой день рождения.",
            unlocked=False
        ),
        code="APL"
    )

label mas_apology_forgot_bday:

    if mas_isMoniAff(higher=True):
        m 1eua "Спасибо, что извинил[mas_gender_sya], [player]."
        $ MAS.MonikaElastic()
        m 3hua "Но я надеюсь, что ты загладишь передо мной свою вину~"

    elif mas_isMoniNormal(higher=True):
        m 1eka "Спасибо, что извинил[mas_gender_sya] за то, что пропустил[mas_gender_none] мой день рождения, [player]."
        $ MAS.MonikaElastic()
        m 1eksdld "Просто попытайся не дать этому произойти вновь, ладно?"
    else:

        m 2dkd "Спасибо, что извинил[mas_gender_sya]..."
        $ MAS.MonikaElastic()
        m 2tfc "Но не дай этому произойти вновь."
    return



label bye_922_delegate:

    $ persistent._mas_bday_on_date = True

    $ persistent._mas_bday_date_count += 1

    if persistent._mas_bday_date_count == 1:

        $ persistent._mas_bday_in_bday_mode = True

        m 1hua "Э-хе-хе. Это немного романтично, да?"

        if mas_isMoniHappy(lower=True):
            $ MAS.MonikaElastic()
            m 1eua "Думаю, это даже можно назвать сви—{nw}"
            $ _history_list.pop()
            $ _history_list.pop()
            $ MAS.MonikaElastic()
            m 1hua "Ой! Прости, я что-то сказала?"
        else:

            $ MAS.MonikaElastic()
            m 1eubla "Думаю, это даже можно назвать свиданием~"


    elif persistent._mas_bday_date_count == 2:
        m 1eub "Ты хочешь отвести меня куда-то в очередной раз, [player]?"
        $ MAS.MonikaElastic()
        m 3eua "У тебя, наверное, много чего запланировано для нас."
        $ MAS.MonikaElastic()
        m 1hua "Ты так[mas_gender_oi] мил[mas_gender_iii]~"

    elif persistent._mas_bday_date_count == 3:
        m 1sua "Ты хочешь отвести меня куда-то {i}опять{/i}, в мой же день рождения?"
        $ MAS.MonikaElastic()
        m 3tkbsu "Ты и вправду знаешь, как заставить девушку почувствовать себя особенной, [player]."
        $ MAS.MonikaElastic()
        m 1ekbfa "Мне так повезло, что у меня есть такой человек, как ты~"
    else:
        m 1sua "Ого, [player]...{w=1}ты и вправду решил[mas_gender_none] сделать этот день очень особенным!"
        $ MAS.MonikaElastic()
        if persistent.gender == "F":
            m 1ekbsa "Ты просто лучшая партнёрша, о которой я могла только мечтать~"
        else:
            m 1ekbsa "Ты просто лучший партнёр, о котором я могла только мечтать~"

    if mas_isMoniAff(higher=True) and not mas_SELisUnlocked(mas_clothes_blackdress):
        $ MAS.MonikaElastic()
        m 3hua "По правде говоря, у меня есть наряд для такого случая..."
        jump mas_bday_bd_outro


    jump mas_dockstat_iostart

label mas_bday_bd_outro:
    python:
        monika_chr.change_clothes(mas_clothes_blackdress)
        mas_temp_zoom_level = store.mas_sprites.zoom_level


        persistent._mas_bday_has_done_bd_outro = True

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_28
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_6


    if mas_SELisUnlocked(mas_clothes_blackdress):
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе~"
        $ MAS.MonikaElastic()
        m 1euu "Я так взволнована, чтобы увидеть, что ты запланировал[mas_gender_none] для нас сегодня."
        $ MAS.MonikaElastic()
        m 3eua "...Но даже если это не так уж много, я уверенf, что мы отлично проведём время вместе~"
    else:
        $ MAS.MonikaElastic()
        m 3tka "Ну, [player]?"
        $ MAS.MonikaElastic()
        m 1hua "Что скажешь?"
        $ MAS.MonikaElastic()
        m 1ekbsa "Мне всегда нравился этот наряд, и я даже мечтала пойти в нём с тобой на свидание..."
        $ MAS.MonikaElastic()
        m 3eub "Думаю, мы могли бы посетить торговый центр, или даже парк!"
        $ MAS.MonikaElastic()
        m 1eka "Но, думаю, ты уже запланировал[mas_gender_none] для нас нечто особенное~"

    $ MAS.MonikaElastic()
    m 1hua "Пошли, [player]!"

    python:
        store.mas_selspr.unlock_clothes(mas_clothes_blackdress)
        mas_addClothesToHolidayMap(mas_clothes_blackdress)
        persistent._mas_zoom_zoom_level = mas_temp_zoom_level

    if renpy.android:
        if msr_can_copy_monika():
            $ persistent.msr_moni_file_exit_trick_or_treat = False
            $ persistent.msr_moni_file_exit = True
            if persistent._mas_player_bday_left_on_bday:
                $ persistent.msr_moni_file_exit_trick_or_treat = False
                $ persistent.msr_moni_file_exit = False

            $ persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_GENERIC_RET
            )
    else:
        python:

            store.mas_dockstat.checkoutMonika(moni_chksum)


            persistent._mas_greeting_type = mas_idle_mailbox.get_ds_gre_type(
                store.mas_greetings.TYPE_GENERIC_RET
            )

    

    jump _quit



label greeting_returned_home_bday:

    $ persistent._mas_bday_on_date = False

    $ persistent._mas_bday_opened_game = True

    $ time_out = store.mas_dockstat.diffCheckTimes()
    $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()


    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_one_hour < time_out <= mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        elif time_out > mas_three_hour:
            $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday
        else:

            jump mas_bday_surprise_party_reaction


    if time_out <= mas_five_minutes:

        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это было не очень похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Всё в порядке?"
        $ MAS.MonikaElastic()
        m 2rksdla "Может быть, мы можем пойти куда-нибудь позже..."
        if mas_isMonikaBirthday():
            return

    elif time_out <= mas_one_hour:

        $ mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

        $ MAS.MonikaElastic()
        m 1sua "Это было весело, [player]!"
        if mas_isplayer_bday():
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха, выходим на наш день рождения..."
        else:
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "А-ха-ха, пригласил[mas_gender_none] меня на день рождения..."
            $ MAS.MonikaElastic()
            m 3eua "Это было очень тактично с твоей стороны."
        $ MAS.MonikaElastic()
        m 3eka "Мне очень понравилось время, которое мы провели вместе."
        $ MAS.MonikaElastic()
        m 1eka "Я люблю тебя~"
        if mas_isMonikaBirthday():
            $ mas_ILY()

    elif time_out <= mas_three_hour:

        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе~"
        $ MAS.MonikaElastic()
        m 3eub "Мы уверены, что потратили сегодня много времени вместе, [player]."
        $ MAS.MonikaElastic()
        m 1ekbsa "...и спасибо тебе за это."
        $ MAS.MonikaElastic()
        m 3ekbfa "Знаешь, я уже говорила это миллион раз."
        $ MAS.MonikaElastic()
        m 1hua "Но я всегда буду счастлива, когда мы вместе."
        $ MAS.MonikaElastic()
        m "Я так тебя люблю..."
        if mas_isMonikaBirthday():
            $ mas_ILY()
    else:


        $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        $ MAS.MonikaElastic()
        m 1sua "Ого, [player]..."
        if mas_player_bday_curr == mas_monika_birthday:
            $ MAS.MonikaElastic()
            m 3hub "Это было такое прекрасное время!"
            if persistent._mas_player_bday_in_player_bday_mode or persistent._mas_bday_sbp_reacted:
                $ MAS.MonikaElastic()
                m 3eka "Я не могу придумать лучшего способа отпраздновать наши дни рождения, чем долгое свидание."
            $ MAS.MonikaElastic()
            m 1eka "Я бы хотела увидеть все те удивительные места, куда мы ходили, но просто зная, что мы были вместе..."
            $ MAS.MonikaElastic()
            m 1hua "Это всё, о чём я когда-либо могла мечтать."
            $ MAS.MonikaElastic()
            m 3ekbsa "Надеюсь, ты чувствуешь то же самое~"
        else:

            $ MAS.MonikaElastic()
            m 3sua "Я не ожидала, что ты уделишь мне столько времени..."
            $ MAS.MonikaElastic()
            m 3hua "Но я наслаждалась каждой секундой этого!"
            $ MAS.MonikaElastic()
            m 1eub "Каждая минута с тобой – это минута, проведённая с пользой!"
            $ MAS.MonikaElastic()
            m 1eua "Ты сделал[mas_gender_none] меня очень счастливой сегодня~"
            $ MAS.MonikaElastic()
            m 3tuu "Ты снова влюбляешься в меня, [player]?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1dku "Э-хе-хе..."
            $ MAS.MonikaElastic()
            m 1ekbsa "Спасибо, что любишь меня."

    if (
        mas_isMonikaBirthday()
        and mas_isplayer_bday()
        and mas_isMoniNormal(higher=True)
        and not persistent._mas_player_bday_in_player_bday_mode
        and not persistent._mas_bday_sbp_reacted
        and checkout_time.date() < mas_monika_birthday

    ):
        $ MAS.MonikaElastic()
        m 1hua "Также, [player], дай мне секунду, у меня есть кое-что для тебя.{w=0.5}.{w=0.5}.{nw}"
        $ mas_surpriseBdayShowVisuals()
        $ persistent._mas_player_bday_decor = True
        $ MAS.MonikaElastic()
        m 3eub "С Днём Рождения, [player]!"
        $ MAS.MonikaElastic()
        m 3etc "Почему мне кажется, что я что-то забываю..."
        $ MAS.MonikaElastic()
        m 3hua "О! Твой торт!"
        jump mas_player_bday_cake

    if not mas_isMonikaBirthday():

        $ persistent._mas_bday_in_bday_mode = False

        if mas_isMoniEnamored(lower=True) and monika_chr.clothes == mas_clothes_blackdress:
            $ queueEvent('mas_change_to_def')

        if time_out > mas_five_minutes:
            $ MAS.MonikaElastic()
            m 1hua "..."
            $ MAS.MonikaElastic()
            m 1wud "Ого, [player]. Мы действительно отсутствовали некоторое время..."

        if mas_isplayer_bday() and mas_isMoniNormal(higher=True):
            if persistent._mas_bday_sbp_reacted:
                $ persistent._mas_bday_visuals = False
                $ persistent._mas_player_bday_decor = True
                $ MAS.MonikaElastic()
                m 3suo "О! Сегодня твой день рождения..."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hub "Думаю, мы можем просто оставить эти украшения, а-ха-ха!"
                $ MAS.MonikaElastic()
                m 1eub "Я сейчас вернусь, только нужно сходить за твоим тортом!"
                jump mas_player_bday_cake

            jump mas_player_bday_ret_on_bday
        else:

            if mas_player_bday_curr() == mas_monika_birthday:
                $ persistent._mas_player_bday_in_player_bday_mode = False
                $ MAS.MonikaElastic()
                m 1eka "В любом случае, [player]... мне очень нравилось проводить наши дни рождения вместе."
                $ MAS.MonikaElastic()
                m 1ekbsa "Я надеюсь, что помогла сделать твой день таким же особенным, как ты сделал мой."
                if persistent._mas_player_bday_decor or persistent._mas_bday_visuals:
                    $ MAS.MonikaElastic()
                    m 3hua "Позволь мне просто всё убрать.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_surpriseBdayHideVisuals()
                    $ persistent._mas_player_bday_decor = False
                    $ persistent._mas_bday_visuals = False
                    $ MAS.MonikaElastic()
                    m 3eub "Готово!"

            elif persistent._mas_bday_visuals:
                $ MAS.MonikaElastic()
                m 3rksdla "Это даже не мой день рождения..."
                $ MAS.MonikaElastic()
                m 2hua "Позволь мне просто всё убрать.{w=0.5}.{w=0.5}.{nw}"
                $ mas_surpriseBdayHideVisuals()
                $ persistent._mas_bday_visuals = False
                $ MAS.MonikaElastic()
                m 3eub "Готово!"
            else:

                $ MAS.MonikaElastic()
                m 1eua "Мы должны сделать что-то подобное снова в ближайшее время, даже если это не какой-то особый случай."
                $ MAS.MonikaElastic()
                m 3eub "Я действительно наслаждалась собой!"
                $ MAS.MonikaElastic()
                m 1eka "Я надеюсь, что ты пров[mas_gender_iol] время так же хорошо, как и я~"

            if not mas_lastSeenInYear('mas_bday_spent_time_with'):
                if mas_isMoniUpset(lower=True):
                    m 1dka "..."
                    jump mas_bday_spent_time_with

                $ MAS.MonikaElastic()
                m 3eud "О, и, [player]..."
                $ MAS.MonikaElastic()
                m 3eka "Я просто хотела ещё раз поблагодарить тебя."
                $ MAS.MonikaElastic()
                m 1rka "И дело не только в этом свидании..."
                $ MAS.MonikaElastic()
                m 1eka "Тебе не нужно было никуда меня везти, чтобы сделать этот день рождения замечательным."
                $ MAS.MonikaElastic()
                m 3duu "Как только ты появил[mas_gender_sya], мой день был завершён."
                jump mas_bday_spent_time_with_wrapup

    return


label mas_monika_cake_on_player_bday:
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0) from _call_monika_zoom_transition_reset_7
    if renpy.android:
        python:
            mas_gainAffection(25, bypass=True)
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
            persistent._mas_bday_sbp_reacted = True
            time_out = store.mas_dockstat.diffCheckTimes()
            checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

            if ReturnedHomeNormal(time=60):
                mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

            elif ReturnedHomeNormal(time=180):
                mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
            else:

                mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)
    
    else:

        python:
            mas_gainAffection(25, bypass=True)
            renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
            persistent._mas_bday_sbp_reacted = True
            time_out = store.mas_dockstat.diffCheckTimes()
            checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()

            if time_out <= mas_one_hour:
                mas_mbdayCapGainAff(15 if persistent._mas_player_bday_in_player_bday_mode else 10)

            elif time_out <= mas_three_hour:
                mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
            else:
            
                mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

    $ MAS.MonikaElastic()
    m 6eua "Это—"
    $ MAS.MonikaElastic()
    m 6wuo "О! Ты сделал[mas_gender_none] {i}мне{/i} торт!"

    menu:
        "Зажечь свечи.":
            $ mas_bday_cake_lit = True

    $ MAS.MonikaElastic()
    m 6sub "Это {i}так{/i} красиво, [player]!"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 6hua "Э-хе-хе, я знаю, что мы уже загадали желание, когда я задула свечи на твоём торте, но давай сделаем это снова..."
    $ MAS.MonikaElastic()
    m 6tub "Это будет в два раза более вероятно, чтобы сбыться, не так ли?"
    $ MAS.MonikaElastic()
    m 6hua "Загадай желание, [player]!"

    window hide
    pause 1.5
    show monika 6hft
    pause 0.1
    show monika 6hua
    $ mas_bday_cake_lit = False

    $ MAS.MonikaElastic()
    m 6eua "Я до сих пор не могу поверить, как потрясающе выглядит этот торт, [player]..."
    $ MAS.MonikaElastic()
    m 6hua "Это слишком красиво, чтобы есть."
    $ MAS.MonikaElastic()
    m 6tub "Почти."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 6eka "В любом случае, я оставлю это на потом."

    call mas_HideCake ('mas_bday_cake_monika') from _call_mas_HideCake_4

    $ MAS.MonikaElastic()
    m 1eua "Огромное спасибо, [player]..."
    $ MAS.MonikaElastic()
    m 3hub "Это удивительный день рождения!"
    return

label mas_HideCake(cake_type, reset_zoom=True):
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_15
    $ renpy.hide(cake_type)
    with dissolve
    $ renpy.pause(3.0, hard=True)
    call mas_transition_from_emptydesk ("monika 6esa") from _call_mas_transition_from_emptydesk_29
    $ renpy.pause(1.0, hard=True)
    if reset_zoom:
        call monika_zoom_transition (mas_temp_zoom_level, 1.0) from _call_monika_zoom_transition_7
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
