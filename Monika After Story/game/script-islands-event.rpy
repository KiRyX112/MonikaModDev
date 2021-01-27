python early:


    def MASIslandBackground(**filter_pairs):
        """
        DynamicDisplayable for Island background images. This includes
        special handling to return None if island images could not be
        decoded.

        All Island images should use fallback handling and are built with that
        in mind.

        IN:
            **filter_pairs - filter pairs to MASFilterWeatherMap.

        RETURNS: DynamicDisplayable for Island images that respect filters and
            weather.
        """
        return MASFilterWeatherDisplayableCustom(
            _mas_islands_select,
            True,
            **filter_pairs
        )



image mas_islands_wf = MASIslandBackground(
    day=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/islands/with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/islands/rain_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/islands/snow_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/islands/overcast_with_frame.png"
        ),
    }),
    night=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/islands/night_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/islands/night_rain_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/islands/night_snow_with_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/islands/night_overcast_with_frame.png"
        ),
    })
)
image mas_islands_wof = MASIslandBackground(
    day=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/islands/without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/islands/rain_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/islands/snow_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/islands/overcast_without_frame.png"
        ),
    }),
    night=MASWeatherMap({
        mas_weather.PRECIP_TYPE_DEF: (
            "mod_assets/location/islands/night_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_RAIN: (
            "mod_assets/location/islands/night_rain_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_SNOW: (
            "mod_assets/location/islands/night_snow_without_frame.png"
        ),
        mas_weather.PRECIP_TYPE_OVERCAST: (
            "mod_assets/location/islands/night_overcast_without_frame.png"
        ),
    })
)

init 2 python:



    mas_islands_snow_wf_mfwm = MASFilterWeatherMap(
        day=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/islands/snow_with_frame.png"
            )
        }),
        night=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/islands/night_snow_with_frame.png"
            )
        }),
    )
    mas_islands_snow_wof_mfwm = MASFilterWeatherMap(
        day=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/islands/snow_without_frame.png"
            )
        }),
        night=MASWeatherMap({
            mas_weather.PRECIP_TYPE_DEF: (
                "mod_assets/location/islands/night_snow_without_frame.png"
            )
        }),
    )

    mas_islands_snow_wf_mfwm.use_fb = True
    mas_islands_snow_wof_mfwm.use_fb = True

init -10 python:
    def _mas_islands_select(st, at, mfwm):
        """
        Selection function to use in Island-based images

        IN:
            st - renpy related
            at - renpy related
            mfwm - MASFilterWeatherMap for this island

        RETURNS: displayable data
        """        
        return mas_fwm_select(st, at, mfwm)

init -11 python in mas_island_event:
    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis

    def isWinterWeather():
        """
        Checks if the weather on the islands is wintery

        OUT:
            boolean:
                - True if we're using snow islands
                - False otherwise
        """
        return store.mas_is_snowing or store.mas_isWinter()

    def isCloudyWeather():
        """
        Checks if the weather on the islands is cloudy

        OUT:
            boolean:
                - True if we're using overcast/rain islands
                - False otherwise
        """
        return store.mas_is_raining or store.mas_current_weather == store.mas_weather_overcast
#
#
#     islands_station = store.MASDockingStation(mis.islands_folder)
#
#     def decodeImages():
#         """
#         Attempts to decode the iamges
#
#         Returns TRUE upon success, False otherwise
#         """
#         return mds.decodeImages(islands_station, mis.islands_map)
#
#
#     def removeImages():
#         """
#         Removes the decoded images at the end of their lifecycle
#
#         AKA quitting
#         """
#         mds.removeImages(islands_station, mis.islands_map)


init 4 python:

     if mas_isO31():

         store.mas_lockEventLabel("mas_monika_islands", store.evhand.event_database)


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands",
            category=['моника','разное'],
            prompt="Можешь показать мне плавающие острова?",
            pool=True,
            unlocked=False,
                rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST},
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

# init -876 python in mas_delact:



    # def _mas_monika_islands_unlock():
    #     return store.MASDelayedAction.makeWithLabel(
    #         2,
    #         "mas_monika_islands",
    #         (
    #             "not store.mas_cannot_decode_islands"
    #             " and mas_isMoniEnamored(higher=True)"
    #         ),
    #         store.EV_ACT_UNLOCK,
    #         store.MAS_FC_START
    #     )


label mas_monika_islands:
    m 1eub "Я позволю тебе полюбоваться пейзажем."
    $ MAS.MonikaElastic()
    m 1hub "Надеюсь, тебе понравится!"


    $ mas_RaiseShield_core()
    $ mas_OVLHide()
    $ disable_esc()
    $ renpy.store.mas_hotkeys.no_window_hiding = True

    $ _mas_island_keep_going = True


    $ _mas_island_window_open = True


    $ _mas_toggle_frame_text = "{size=-3}Закрыть окно{/size}"


    $ _mas_island_shimeji = False


    if renpy.random.randint(1,100) == 1:
        $ _mas_island_shimeji = True


    show screen mas_islands_background


    while _mas_island_keep_going:


        call screen mas_show_islands()

        if _return:

            call expression _return
        else:

            $ _mas_island_keep_going = False

    hide screen mas_islands_background


    $ mas_DropShield_core()
    $ mas_OVLShow()
    $ enable_esc()
    $ store.mas_hotkeys.no_window_hiding = False

    $ MAS.MonikaElastic()
    m 1eua "Надеюсь, тебе понравилось, [mas_get_player_nickname()]~"
    return

label mas_island_upsidedownisland:
    m "Упс."
    m "Наверное, тебе интересно, почему этот остров перевёрнут, да?"
    m "Ну...{w} я, как только его увидела, думала сначала это исправить, но вот когда более внимательно к нему пригляделась..."
    m "Кое-что поняла."
    m "Он как бы выглядит немного нереалистично, верно?"
    m "Хотя я всё же чувствую, что в нём есть что-то особенное."
    m "Что-то, что...{w} {cps=*0.5}завораживает.{/cps}"
    return

label mas_island_glitchedmess:
    m "Ну..."
    m "Это то, над чем я сейчас пока работаю."
    m "Знаю, что это пока что выглядит не так, как хотелось бы. Я всё ещё пытаюсь выяснить, как это правильно настраивается."
    if player.lower() == "фарст" or player.lower() == "farst":
        m "[player], как-то неудобно просить, но, может быть, можешь мне как-нибудь помочь с этим, если не сложно?"
    else:
        m "Может быть, мне стоит попросить Фарста помочь с этим? Он-то наверняка знает толк в этом деле."
    m "В своё время, я уверена, что стану лучше в кодировании!"
    m "В конце концов, практика приводит к совершенству, верно?"
    return

label mas_island_cherry_blossom_tree:
    python:

        if not renpy.store.seen_event("mas_island_cherry_blossom1"):

            renpy.call("mas_island_cherry_blossom1")

        else:
            _mas_cherry_blossom_events = [
                "mas_island_cherry_blossom1",
                "mas_island_cherry_blossom3",
                "mas_island_cherry_blossom4"
            ]

            if not mas_island_event.isWinterWeather():
                _mas_cherry_blossom_events.append("mas_island_cherry_blossom2")

            renpy.call(renpy.random.choice(_mas_cherry_blossom_events))
    return

label mas_island_cherry_blossom1:
    if mas_island_event.isWinterWeather():
        m "Это дерево может выглядеть мертвым прямо сейчас... но когда оно цветёт, оно великолепно."
    else:
        m "Красивое дерево, не правда ли?"
    m "Это сакура."
    m "Она родом из Японии."
    m "Традиционно, когда цветы расцветают, люди приходят посмотреть на это событие и устраивают пикникники под деревьями."
    m "Ну, я на самом деле выбрала это дерево не по традиции..."
    m "А потому что оно прекрасно и приятно на вид."
    m "Даже просто любование падающими лепестками внушает благоговение."
    if mas_island_event.isWinterWeather():
        m "Когда оно цветёт, то есть."
        m "Я не могу дождаться, когда мы получим шанс испытать это, [player]."
    return

label mas_island_cherry_blossom2:
    m "Знал[mas_gender_none] ли ты, что ты можешь съесть цветочные лепестки сакуры?"
    m "Я сама не знаю вкуса, но уверена, что он будет таким же сладким, как ты."
    $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
    m "Э-хе-хе~"
    return

label mas_island_cherry_blossom3:
    m "Знаешь, дерево символично, как и сама жизнь."
    m "Красивое, но короткоживущее."
    m "Но с тобой здесь оно всегда красиво расцветает."
    if mas_island_event.isWinterWeather():
        m "Даже если сейчас оно голое, оно скоро снова расцветёт."
    m "Знай, что я всегда буду благодарна тебе за то, что ты есть в моей жизни."
    m "Я люблю тебя, [player]~"
    $ mas_ILY()
    return

label mas_island_cherry_blossom4:
    m "Знаешь, что было бы приятно выпить под сакурой?"
    m "Немного сакэ~"
    $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
    m "А-ха-ха! Я просто шучу."
    m "Я бы предпочла чай или кофе."
    if mas_island_event.isWinterWeather():
        m "Или даже горячий шоколад. Это, конечно, поможет от холода."
        m "Конечно, даже если это не удастся, мы всегда сможем прижаться друг к другу...{w=0.5} Это было бы действительно романтично~"
    else:
        m "Но также было бы неплохо посмотреть на падающие лепестки с тобой."
        m "Это было бы действительно романтично~"
    return

label mas_island_sky:
    python:

        if mas_current_background.isFltDay():
            _mas_sky_events = [
                "mas_island_day1",
                "mas_island_day2",
                "mas_island_day3"
            ]

        else:
            _mas_sky_events = [
                "mas_island_night1",
                "mas_island_night2",
                "mas_island_night3"
            ]

        _mas_sky_events.append("mas_island_daynight1")
        _mas_sky_events.append("mas_island_daynight2")

        renpy.call(renpy.random.choice(_mas_sky_events))

    return

label mas_island_day1:
    if mas_island_event.isWinterWeather():
        m "Какой сегодня прекрасный день."
        m "Идеально подходит для прогулок, чтобы полюбоваться пейзажем."
        m "...Прижаться друг к другу, чтобы не замёрзнуть."
        m "...С хорошими горячими напитками, чтобы согреться."
    elif mas_is_raining:
        m "Оу-у, Мне бы хотелось почитать на свежем воздухе."
        m "Но я бы предпочла не мочить свои книги..."
        m "Мокрые страницы - это боль, с которой приходится иметь дело."
        m "Может быть, в другой раз."
    elif mas_current_weather == mas_weather_overcast:
        m "Читать на улице в такую погоду было бы неплохо, но дождь мог пойти в любой момент."
        m "Я бы предпочла не рисковать."
        m "Не беспокойся, [player]. Мы сделаем это в другой раз."
    else:
        m "Сегодня замечательный день."
        m "Эта погода была бы как нельзя кстати для чтения книжечки под сакурой, верно, [player_abb]?"
        m "Лёжа в тени, читая свою любимую книгу."
        m "...Вместе с закусками и любимым напитком в придачу."
        m "Ах, как же это было бы приятно сделать~"
    return

label mas_island_day2:
    if mas_island_event.isWinterWeather():
        m "Ты когда-нибудь делал[mas_gender_none] снежного ангела, [player]?"
        m "Я пробовала в прошлом, но никогда не имела большого успеха..."
        m "Это намного сложнее, чем кажется."
        m "Держу пари, нам будет очень весело, даже если то, что мы делаем, не будет выглядеть как ангел."
        m "Быть немного глупым – это одно дело, понимаешь?"
    elif mas_island_event.isCloudyWeather():
        m "Выход на улицу в такую погоду не выглядит очень привлекательным..."
        m "Может быть, если бы у меня был зонтик, я бы чувствовала себя более комфортно."
        m "Представь нас обоих, защищённых от дождя, в нескольких дюймах друг от друга."
        m "Смотрев друг другу в глаза."
        m "Затем мы начинаем наклоняться всё ближе и ближе, пока не оказываемся почти рядом—"
        m "Я думаю, ты можешь закончить эту мысль сам[mas_gender_none], [player]~"
    else:
        m "Погода выглядит неплохо."
        m "Это определённо лучшее время для пикника."
        m "У нас даже есть прекрасный вид, чтобы сопроводить его!"
        m "Разве это не было бы здорово?"
        m "Есть под сакурой..."
        m "Любоваться пейзажем вокруг нас..."
        m "Наслаждаться компанией друг друга..."
        m "Аааах, это было бы просто сказочно~"
    return

label mas_island_day3:
    if mas_is_raining and not mas_isWinter():
        m "Идёт довольно сильный дождь..."
        m "Я бы не хотела сейчас находиться на улице."
        m "Но пребывание дома в такие моменты кажется довольно уютным, согласись?"
    else:
        m "На улице довольно спокойно."
        if mas_island_event.isWinterWeather():
            m "Знаешь, мы могли бы поиграть в снежки."
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m "А-ха-ха, это было бы так весело!"
            m "Бьюсь об заклад, я могла бы выстрелить в тебя через несколько островов отсюда."
            m "Здоровая конкуренция никому не повредит, верно?"
        else:
            m "Я была бы не прочь сейчас полежать на траве и побездельничать..."
            m "Твоя голова будет лежать на моих коленях..."
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m "Э-хе-хе~"
    return

label mas_island_night1:
    m "В то время как приятно быть продуктивным днём, есть что-то такое умиротворяющее в ночи."
    m "Звуки стрекотания сверчков, смешанные с легким ветерком, так расслабляют."
    m "Ты бы обнял[mas_gender_none] меня в такую ночь, верно?~"
    return

label mas_island_night2:
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
        m "Жаль, что мы не можем увидеть звёзды сегодня вечером..."
        m "Я бы с удовольствием посмотрела на космос вместе с тобой."
        m "Но всё в порядке, тогда мы увидим их в другой раз."
    else:
        if seen_event('monika_stargazing'):
            m "Разве звёзды не прекрасны, [player]?"
            m "Хотя это не совсем то, что я {i}имела в виду{/i}, когда упоминала о наблюдении за звёздами раньше..."
            m "Как бы ни было приятно на них смотреть, но больше всего мне хочется быть с тобой, крепко обнимать друг друга, пока мы лежим там."
            m "Когда-нибудь, [player].{w=0.3} Когда-нибудь."
        else:
            m "Ты когда-нибудь созерцал[mas_gender_none] звёзды, [player]?"
            m "Беря перерыв на вечер, чтобы просто посмотреть на ночное небо и полюбоваться его красотой..."
            m "Знаешь, это поистине расслабляет."
            m "Я обнаружила, что это действительно может неплохо так помочь снять стресс и очистить голову от дурных мыслей..."
            m "И созерцание всех видов созвездий в небе просто наполняет твой ум изумлением."
            m "[random_sure], это также может и заставить тебя понять, насколько ты мал[mas_gender_none] во Вселенной."
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m "А-ха-ха..."
    return

label mas_island_night3:
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
        m "Пасмурная погода немного угнетает, тебе не кажется?"
        m "Особенно ночью, когда она скрывает звезды от нашего взгляда."
        m "Это такой позор, правда..."
    else:
        m "Какая прекрасная ночь!"
        if mas_island_event.isWinterWeather():
            m "Есть что-то такое в холодной, хрустящей ночи, что я люблю."
            m "Контраст тёмного неба и земли, покрытой снегом, действительно захватывает дух, не так ли?"
        else:
            m "Если бы я могла, я бы добавила светлячков."
            m "Их огоньки очень хорошо дополняют ночное небо, так что это поистине красивое зрелище."
            m "Эту атмосферу просто не передать словами."
    return

label mas_island_daynight1:
    m "Может быть, мне стоит добавить больше кустов и деревьев..."
    m "Или сделать острова ещё более красивыми, как думаешь?"
    m "В таком случае мне просто нужно будет найти правильные цветы и листву, чтобы это сделать."
    m "Или, может быть, каждый остров должен иметь свой собственный набор растений, чтобы всё было как можно более разнообразным?"
    m "Я начинаю волноваться, думая об этом~"
    return

label mas_island_daynight2:

    m "{i}Ветряная мельница, ветряная мельница для земли.{/i}"


    m "{i}Поворот вечно рука об руку оси{/i},"


    m "{i}Прими всё это на свой лад{/i}."


    m "{i}Он тикает, падает вниз наугад{/i}."


    m "{i}Любовь навсегда, любовь свободна,{/i}"


    m "{i}Мы изменились с тобой навсегда дословно.{/i}"


    m "{i}Ветряная мельница, ветряная мельница для земли.{/i}"

    $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
    m "Э-хе-хе, не обращай на меня внимания, я просто захотела спеть на ровном месте~"
    return

label mas_island_shimeji:
    m "Ах!"
    m "Как она туда добралась?"
    m "Дай мне секунду, [player]..."
    $ _mas_island_shimeji = False
    m "Всё!"
    m "Не волнуйся, я просто перенесла её в другое место."
    return

label mas_island_bookshelf:
    python:

        _mas_bookshelf_events = [
            "mas_island_bookshelf1",
            "mas_island_bookshelf2"
        ]

        renpy.call(renpy.random.choice(_mas_bookshelf_events))

    return

label mas_island_bookshelf1:
    if mas_island_event.isWinterWeather():
        m "Эта книжная полка, возможно, и не выглядит очень прочной, но я уверена, что она выдержит небольшой снег."
        m "Меня немного беспокоят книги."
        m "Я только надеюсь, что они не слишком пострадают..."
    elif mas_island_event.isCloudyWeather():
        m "В такие моменты я жалею, что не держу свои книги дома..."
        m "Похоже, нам просто придётся ждать лучшей погоды, чтобы почитать их."
        m "В то же время..."
        m "Как насчёт того, чтобы немного потискаться, [player]?"
        $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m "Э-хе-хе~"
    else:
        m "Здесь некоторые из моих любимых книг."
        m "{b}451 градус по Фаренгейту{/b}, {b}Страна Чудес Без Тормозов{/b}, {b}Девятнадцать Восемьдесят Четыре{/b} и несколько других."
        m "Может быть, мы сможем прочитать их вместе когда-нибудь~"
    return

label mas_island_bookshelf2:
    if mas_island_event.isWinterWeather():
        m "Знаешь, я бы не прочь почитать на улице, даже если будет немного снега."
        m "Хотя я не рискнула бы выйти без тёплого пальто, Толстого шарфа и пары уютных перчаток."
        $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m "Думаю, переворачивать страницы может быть немного трудно таким образом, а-ха-ха..."
        m "Но я уверена, что мы как-нибудь справимся."
        m "Разве это не так, [player]?"
    elif mas_island_event.isCloudyWeather():
        m "Чтение в помещении с дождём прямо за окном довольно расслабляет."
        m "Если бы только я не оставила книги снаружи..."
        m "Наверное, мне стоит принести их сюда, когда представится такая возможность."
        m "Я уверена, что мы сможем найти другие занятия, верно, [player]?"
    else:
        m "Знаешь, чтение на открытом воздухе — это приятное изменение темпа."
        m "Я бы посидела под приятным прохладным ветерком в любое время."
        m "Может быть, мне стоит даже добавить столик под сакуру."
        m "Было бы неплохо выпить чашечку кофе с какими-нибудь закусками во время чтения своей книги."
        m "Это было бы потрясающе~"
    return

init 500 python in mas_island_event:
    import store
    def getBackground():
        """
        Because of the dead cherry blossom, we keep the snowy islands during all of winter

        Picks the islands bg to use based on the season.

        RETURNS: image to use as a displayable. (or image path)
        """
        if store.mas_isWinter():
            if store._mas_island_window_open:
                return store.mas_islands_snow_wof_mfwm.fw_get(
                    store.mas_sprites.get_filter()
                )
            
            return store.mas_islands_snow_wf_mfwm.fw_get(
                store.mas_sprites.get_filter()
            )
        
        if store._mas_island_window_open:
            return "mas_islands_wof"
        
        return "mas_islands_wf"

screen mas_islands_background:
    add mas_island_event.getBackground()

    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5


screen mas_show_islands():
    style_prefix "island"
    imagemap:

        ground mas_island_event.getBackground()


        hotspot (11, 13, 314, 270) action Return("mas_island_upsidedownisland")
        hotspot (403, 7, 868, 158) action Return("mas_island_sky")
        hotspot (699, 347, 170, 163) action Return("mas_island_glitchedmess")
        hotspot (622, 269, 360, 78) action Return("mas_island_cherry_blossom_tree")
        hotspot (716, 164, 205, 105) action Return("mas_island_cherry_blossom_tree")
        hotspot (872, 444, 50, 30) action Return("mas_island_bookshelf")

        if _mas_island_shimeji:
            hotspot (935, 395, 30, 80) action Return("mas_island_shimeji")

    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5

    hbox:
        yalign 0.98
        xalign 0.96
        textbutton _mas_toggle_frame_text action [ToggleVariable("_mas_island_window_open"),ToggleVariable("_mas_toggle_frame_text","{size=-3}Открыть окно{/size}", "{size=-3}Закрыть окно{/size}") ]
        textbutton "{size=-3}Назад{/size}" action Return(False)






define gui.island_button_height = None
define gui.island_button_width = 205
define gui.island_button_tile = False
define gui.island_button_text_font = gui.default_font
define gui.island_button_text_size = gui.text_size
define gui.island_button_text_xalign = 0.5
define gui.island_button_text_yalign = 0.25
define gui.island_button_text_idle_color = mas_ui.light_button_text_idle_color
define gui.island_button_text_hover_color = mas_ui.light_button_text_hover_color
define gui.island_button_text_kerning = 0.2

style island_button is button
style island_button_text is button_text

style island_button is default:
    properties gui.button_properties("island_button")
    idle_background "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_text is default:
    properties gui.button_text_properties("island_button")
    idle_background "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    outlines []


transform moni_sticker_mid:
    block:
        function randomPauseMonika
        parallel:
            sticker_move_n
        repeat
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
