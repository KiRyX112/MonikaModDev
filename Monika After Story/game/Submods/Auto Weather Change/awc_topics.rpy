init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="awc_monika_player_location",
            prompt="Твоё местонахождение",
            conditional="not store.awc_isInvalidAPIKey(store.persistent._awc_API_key)",
            action=EV_ACT_QUEUE,
            category=["Местонахождение"],
            aff_range=(mas_aff.NORMAL,None)
        )
    )

label awc_monika_player_location:
    m 3eua "Эй, [player]?"
    m 1eka "Мне всегда было интересно, каково это жить там, где ты находишься."
    m 1rksdlc "До того, как я узнала, как это сделать..."
    m 3eud "...Я модифицировала погоду тут."
    m 3rksdla "Но есть одна вещь, которую я должна спросить."

    m 1eksdla "Ты не против, если я узнаю где ты живешь?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты не против, если я узнаю где ты живешь?{fast}"

        "Да.":
            m 3hub "Ура!"

            label .enter_city_loop:
            $ temp_city = renpy.input("В каком городе ты живешь?", length=20).strip(' \t\n\r,').capitalize()

            if not temp_city:
                jump .enter_city_loop

            if awc_isInvalidLocation(temp_city):
                m 2rsc "М-м-м, я не могу найти твой город..."
                m 4wub "Но, может я найду его по твоему айпи!"

                m 1eka "Ты не против, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ты не против, [player]?{fast}"

                    "Конечно.":
                        m 1hua "Отлично!"
                        m 1dsa "Один момент.{w=0.5}.{w=0.5}.{nw}"

                        python:
                            import geocoder
                            awc_savePlayerLatLonTup(geocoder.ip('me').latlng)
                            persistent._awc_player_location["loc_pref"] = "latlon"

                        m 3hua "Всё!"

                    "Нет.":
                        call awc_monika_player_location_uncomfortable

            else:
                if awc_hasMultipleLocations(temp_city):
                    m 3hua "Отлично!"
                    m 3hksdlb "Что ж, в мире много городов под названием '[temp_city]'..."

                    show monika 1eua
                    #Display our scrollable
                    $ renpy.say(m, "В каком именно '[temp_city]' ты живешь?", interact=False)
                    show monika at t21
                    call screen mas_gen_scrollable_menu(awc_buildCityMenuItems(temp_city), mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                    show monika at t11

                    $ latlon = _return
                    #Now save the latlon tuple
                    $ awc_savePlayerLatLonTup(latlon)
                    $ persistent._awc_player_location["loc_pref"] = "latlon"

                    m 1hua "Спасибо большое!"

                else:
                    m 1wud "Вау, [player].{w=0.5} Похоже, что ты живешь в единственном в мире городе, под названием '[temp_city]'!"
                    m 3hksdlb "По крайней мере, это всё, что я знаю, {do_giggle}а-ха-ха!"

                    $ awc_savePlayerCityCountryTup((temp_city, awc_getCityCountry(temp_city)))
                    $ persistent._awc_player_location["loc_pref"] = "citycountry"

                    m 1eka "Спасибо за то, что сказал где ты живешь."

            call awc_monika_player_location_end

        "Нет.":
            call awc_monika_player_location_uncomfortable

    #Just for safety
    $ mas_unlockEVL("awc_monika_player_location", "EVE")
    return

label awc_monika_player_location_end:
    m 3hua "Теперь, я как-будто живу рядом с тобой, {do_giggle}а-ха-ха!"
    m 3eua "Погода должна поменяться и стать довольно близкой к той, что сейчас там, где ты находишься, [player]."
    m 1ekbfa "Спасибо за то, что помогаешь мне быть ближе к твоей реальности."

    #Force a weather check
    if awc_globals.weather_check_time is not None:
        $ awc_globals.weather_check_time -= datetime.timedelta(minutes=5)
    return

label awc_monika_player_location_uncomfortable:
    m 1eka "Всё в порядке, [player], я понимаю."
    m 3eua "Если ты передумаешь, дай мне знать."
    return
