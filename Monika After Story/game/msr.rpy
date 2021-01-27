default cake_zorder = MAS_MONIKA_Z + 1
default persistent.msr_color_ribbon = 'white'

init 200 python in mas_dockstat:


    import store
    import store.mas_sprites as mas_sprites
    import store.mas_greetings as mas_greetings
    import store.mas_ics as mas_ics
    import store.evhand as evhand
    from cStringIO import StringIO as fastIO
    import os
    def MSRdiffCheckTimes(index=None):
        """
        Returns the difference between the latest checkout and check in times
        We do checkin - checkout.

        IN:
            index - the index of checkout/checkin to use when diffing
                If None, we use the latest one
                (Default: None)

        RETURNS: timedelta of the difference between checkin and checkout
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)

        if checkin_len == 0 or checkout_len == 0:
            return datetime.timedelta(0)

        if checkin_len != checkout_len:

            mas_utils.writelog(
                (
                    "[ПРЕДУПРЕЖДЕНИЕ]: входящая проверка {0}, исходящая проверка {1}. "
                    "Очистка.\n"
                ).format(checkin_len, checkout_len)
            )


            if checkin_len > checkout_len:
                larger_log = checkin_log
                goal_size = checkout_len

            else:
                larger_log = checkout_log
                goal_size = checkin_len

            while len(larger_log) > goal_size:
                larger_log.pop()

        if index is None or index >= len(checkout_log):
            index = len(checkout_log)-1

        return checkin_log[index][0] - checkout_log[index][0]


init python:

    def cap_gain_aff(amt):
        persistent._mas_bday_sbd_aff_given += amt
        if persistent._mas_bday_sbd_aff_given <= 70:
            mas_gainAffection(amt, bypass=True)

    def BdayParty():
        try:
            with open(user_dir + "/characters/торт", "rb") as f:
                pass
            if not persistent.msr_mas_bday_sbp_reacted:
                persistent.monika_cake = True
                renpy.show("mas_bday_cake_monika", zorder=cake_zorder)
        except:
            persistent.monika_cake = None
            renpy.hide("mas_bday_cake_monika")
        try:
            with open(user_dir + "/characters/баннеры", "rb") as f:
                pass
            persistent.monika_banners = True
            renpy.show("mas_bday_banners", zorder=7)
        except:
            persistent.monika_banners = None
            renpy.hide("mas_bday_banners")
        try:
            with open(user_dir + "/characters/надувные шары", "rb") as f:
                pass
            persistent.monika_balloons = True
            renpy.show("mas_bday_balloons", zorder=8)
        except:
            persistent.monika_balloons = None
            renpy.hide("mas_bday_balloons")

    def XmasDecorations():
        try:
            with open(user_dir + "/characters/украшения", "rb") as f:
                pass
            persistent.monika_xmas_decorations = True
        except:
            persistent.monika_xmas_decorations = None
        try:
            with open(user_dir + "/characters/ёлка", "rb") as f:
                pass
            persistent.monika_xmas_tree = True
        except:
            persistent.monika_xmas_tree = None

    def getCheckTimes(chksum=None):
        """
        Gets the corresponding checkin/out times for the given chksum.

        IN:
            chksum - chksum to retrieve checkin/checkout times.
                If None, then we simply get the latest checkin/checkout,
                regardless if they match or not.
                (Default: None)

        RETURNS tuple of the following format:
            [0] - checkout time
            [1] - checkin time
        If any param is None, then we couldn't find the matching chksum or
        there were no entries
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_time = None
        checkout_time = None
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)


        def find_time(check_log, check_sum):
            for _time, _chksum in check_log:
                if _chksum == check_sum:
                    return _time

            return None

        if checkin_len > 0:
            if chksum is None:
                checkin_time = checkin_log[checkin_len-1][0]

            else:
                checkin_time = find_time(checkin_log, chksum)

        if checkout_len > 0:
            if chksum is None:
                checkout_time = checkout_log[checkout_len-1][0]

            else:
                checkout_time = find_time(checkout_log, chksum)

        return (checkout_time, checkin_time)


    def diffCheckTimes(index=None):
        """
        Returns the difference between the latest checkout and check in times
        We do checkin - checkout.

        IN:
            index - the index of checkout/checkin to use when diffing
                If None, we use the latest one
                (Default: None)

        RETURNS: timedelta of the difference between checkin and checkout
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)

        if checkin_len == 0 or checkout_len == 0:
            return datetime.timedelta(0)

        if checkin_len != checkout_len:

            mas_utils.writelog(
                (
                    "[ПРЕДУПРЕЖДЕНИЕ]: входящая проверка {0}, исходящая проверка {1}. "
                    "Очистка.\n"
                ).format(checkin_len, checkout_len)
            )


            if checkin_len > checkout_len:
                larger_log = checkin_log
                goal_size = checkout_len

            else:
                larger_log = checkout_log
                goal_size = checkin_len

            while len(larger_log) > goal_size:
                larger_log.pop()

        if index is None or index >= len(checkout_log):
            index = len(checkout_log)-1

        return checkin_log[index][0] - checkout_log[index][0]


    def timeOut(_date):
        """
        Given a date, return how long monika has been out

        We assume that checkout logs are the source of truth

        IN:
            _date - date to check
        """
        checkout_log = store.persistent._mas_dockstat_checkout_log

        if len(checkout_log) == 0:
            return datetime.timedelta(0)


        checkout_indexes = [
            index
            for index in range(0, len(checkout_log))
            if checkout_log[index][0].date() == _date
        ]

        if len(checkout_indexes) == 0:
            return datetime.timedelta(0)


        time_out = datetime.timedelta(0)

        for index in checkout_indexes:
            time_out += diffCheckTimes(index)

        return time_out

    if not mas_isMonikaBirthday():
        persistent.monika_cake = None
        persistent.monika_banners = None
        persistent.monika_balloons = None
        persistent.surprise_party = False
        try:
            os.remove(user_dir + "/characters/надувные шары")
        except:
            pass
        try:
            os.remove(user_dir + "/characters/баннеры")
        except:
            pass
        try:
            os.remove(user_dir + "/characters/торт")
        except:
            pass


    def returned_home_loop():
        persistent.tried_skip = True
        y_name = "Юри"
        bday_name = "Имя"
        tempinstrument = "Инструмент"
        m.display_args["callback"] = slow_nodismiss
        m.what_args["slow_abortable"] = config.developer
        renpy.call("mas_set_gender")
        renpy.call("mas_name_cases")
        if renpy.android:
            monika_device_name = "телефон"
        else:
            monika_device_name = "компьютер"
        config.allow_skipping = False
        config.skipping = False
        mas_skip_visuals = False
        store.mas_dockstat.retmoni_status = None
        store.mas_dockstat.retmoni_data = None

    def msr_can_copy_monika():

        try:
            open(user_dir + "/characters/моника", "wb").write(renpy.file("mod_assets/monika/mbase").read())
            return True
        except:
            return False



label msr_bye_going_somewhere_post_aff_check:

    if mas_isO31():
        $ MAS.MonikaElastic()
        m 1wub "О! Мы пойдём выпрашивать сладости, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "О! Мы пойдём выпрашивать сладости, [player]?{fast}"
            "Да.":
                jump msr_bye_trick_or_treat
            "Нет.":

                $ MAS.MonikaElastic()
                m 2ekp "Ох, ладно."

default persistent.moni_copy_file = False
default persistent.msr_moni_file_exit = False
default persistent.first_go_somewhere = True

default persistent.monika_bday_reset = None
default persistent.msr_mas_bday_sbp_reacted = False
default persistent._date_last_ear_rose = None

label msr_greeting_returned_home:

    python:
        import os
        try:
            with open(user_dir + "/characters/моника", "rb") as f:
                pass
            msr_monika_find_file = True
        except:
            msr_monika_find_file = False


    if msr_monika_find_file:
        $ persistent.moni_copy_file = False
        $ persistent.msr_moni_file_exit = False
        $ returned_home_loop()
        call textbox_loop
        call spaceroom (scene_change=True)
        if persistent._mas_o31_in_o31_mode:
            $ store.mas_globals.show_vignette = True
            $ mas_o31ShowVisuals()

            $ mas_changeWeather(mas_weather_thunder, True)
        
        if ReturnedHomeNormal(time=5):
            show monika 1eua zorder MAS_MONIKA_Z at t11 with dissolve
        else:
            show monika 2ekp zorder MAS_MONIKA_Z at t11 with dissolve
        hide emptydesk
        $ persistent._mas_greeting_type = None
        if mas_confirmedParty() and mas_isMonikaBirthday():
            $ persistent._mas_bday_visuals = True
            $ mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)
        if mas_isD25Season() and persistent._mas_d25_deco_active:
            $ store.mas_d25ShowVisuals()
        if datetime.date.today() == persistent._date_last_given_roses:
            $ monika_chr.wear_acs(mas_acs_roses)
        if (datetime.date.today() == persistent._date_last_ear_rose) and not monika_chr.hair.name == "pigtails":
            $ monika_chr.wear_acs(mas_acs_ear_rose)
        if persistent._mas_player_bday_decor:
            $ store.mas_player_bday_event.show_player_bday_Visuals()
        $ renpy.save_persistent()
        $ os.remove(user_dir + "/characters/моника")
        $ mas_OVLShow()
        $ mas_calShowOverlay()
        $ mas_disable_quit()
        $ enable_esc()
        $ startup_check = False
        jump ch30_post_exp_check
    else:

        jump msr_mas_dockstat_empty_desk


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="msr_greeting_returned_home_end",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_GENERIC_RET
            ]
        ),
        code="GRE"
    )
default skip_play_music = False

init -800 python:
    import datetime

    def ReturnedHomeNormal(time):
        return datetime.datetime.now() > (mas_getLastSeshEnd() + datetime.timedelta(seconds=time*60))
        
label msr_greeting_returned_home_end:
    $ config.developer = False
    $ persistent.returned_home_end = True
    $ skip_play_music = True

    if mas_isO31() and not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay() and mas_isMoniNormal(higher=True):
        $ pushEvent("mas_holiday_o31_returned_home_relaunch", skipeval=True)

    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):

        call mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nyd_check

    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump msr_greeting_returned_home_pbday

    if mas_isF14() and persistent._mas_f14_on_date:
        jump msr_greeting_returned_home_f14

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump msr_greeting_returned_home_bday

    if ReturnedHomeNormal(time=5):
        if mas_isMoniNormal(higher=True):
            if ReturnedHomeNormal(time=60):
                $ mas_gainAffection(5,bypass=True)

            if persistent._mas_d25_in_d25_mode:

                jump greeting_d25_and_nye_delegate
            elif mas_isD25():

                jump mas_d25_monika_holiday_intro_rh
            call greeting_returned_home_morethan5mins_normalplus_dlg
            if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
                call return_home_post_player_bday

        else:
            if ReturnedHomeNormal(time=60):
                $ mas_gainAffection(3,bypass=True)
            call greeting_returned_home_morethan5mins_other_dlg

    else:


        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins

        if _return:
            jump msr_quit

        jump greeting_returned_home_cleanup

    $ persistent._mas_game_crashed = None
    show monika 1esa
    return



label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()


    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out) from _call_mas_o31_ret_home_cleanup_2

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday from _call_return_home_post_player_bday_12


    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label msr_greeting_returned_home_f14:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()

    if ReturnedHomeNormal(time=5):
        $ mas_loseAffection()

        $ MAS.MonikaElastic()
        m 2ekp "Это не было похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Надеюсь, всё нормально?"
        $ MAS.MonikaElastic()
        m 2rksdla "Наверное, мы пойдём гулять позже..."

    elif ReturnedHomeNormal(time=60):
        $ mas_f14CapGainAff(5)
        $ MAS.MonikaElastic()
        m 1eka "Было весело, до поры до времени, [player]..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, что уделил мне время в День святого Валентина."

    elif ReturnedHomeNormal(time=180):
        $ mas_f14CapGainAff(10)
        $ MAS.MonikaElastic()
        m 1eub "Это было очень весёлое свидание, [player]!"
        $ MAS.MonikaElastic()
        m 3ekbfa "Спасибо, что заставил почувствовать себя особенной в День святого Валентина~"
    else:


        $ mas_f14CapGainAff(15)
        $ MAS.MonikaElastic()
        m 1hua "И мы дома!"
        $ MAS.MonikaElastic()
        m 3hub "Это было прекрасно, [player]!"
        $ MAS.MonikaElastic()
        m 1eka "Было очень здорово выйти на улицу с тобой в День святого Валентина..."
        $ MAS.MonikaElastic()
        m 1ekbfa "Большое тебе спасибо за то, что сделал сегодняшний день по-настоящему особенным~"

    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
        call return_home_post_player_bday

    $ persistent._mas_f14_on_date = False

    if not mas_isF14() and not mas_lastSeenInYear("mas_f14_monika_spent_time_with"):
        $ pushEvent("mas_f14_monika_spent_time_with",skipeval=True)
    return

label msr_greeting_returned_home_bday:
    $ persistent._mas_bday_on_date = False

    $ persistent._mas_bday_opened_game = True

    # $ time_out = store.mas_dockstat.diffCheckTimes()
    # $ checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()


    if mas_confirmedParty() and not persistent._mas_bday_sbp_reacted:
        if mas_getLastSeshEnd() + mas_one_hour < datetime.datetime.now() <= mas_getLastSeshEnd() + mas_three_hour:
            $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)
        elif ReturnedHomeNormal(time=180):
            $ mas_mbdayCapGainAff(35 if persistent._mas_player_bday_in_player_bday_mode else 30)

        if mas_isplayer_bday() and persistent._mas_player_bday_decor and persistent._mas_bday_date_count == 1:
            jump mas_monika_cake_on_player_bday
        else:

            jump msr_mas_bday_surprise_party_reaction

    if ReturnedHomeNormal(time=5):

        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это было не очень похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Всё в порядке?"
        $ MAS.MonikaElastic()
        m 2rksdla "Может быть, мы можем пойти куда-нибудь позже..."
        if mas_isMonikaBirthday():
            return

    elif ReturnedHomeNormal(time=60):

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

    elif ReturnedHomeNormal(time=180):

        $ mas_mbdayCapGainAff(25 if persistent._mas_player_bday_in_player_bday_mode else 20)

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1hua "Э-хе-хе~"
        $ MAS.MonikaElastic()
        m 3eub "Мы уверены, что потратили сегодня много времени вместе, [player]."
        $ MAS.MonikaElastic()
        m 1ekbfa "...и спасибо тебе за это."
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
            m 1eub "Каждая минута с тобой - это минута, проведённая с пользой!"
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

        if ReturnedHomeNormal(time=5):
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



label msr_mas_dockstat_empty_desk:


    $ import store.mas_dockstat as mas_dockstat
    $ mas_OVLHide()
    $ mas_calRaiseOverlayShield()
    $ mas_calShowOverlay()
    $ disable_esc()
    $ mas_enable_quit()
    $ promise = mas_dockstat.monikafind_promise

label msr_mas_dockstat_empty_desk1:

    call spaceroom (hide_monika=True, scene_change=True)
    $ mas_from_empty = True
    # if mas_isMonikaBirthday():
    #     $ BdayParty()
    if mas_isD25Season() and persistent._mas_d25_deco_active:
        $ store.mas_d25ShowVisuals()
    # if datetime.date.today() == persistent._date_last_given_roses:
    #     $ renpy.show("mas_roses", zorder=10)
    if mas_confirmedParty() and mas_isMonikaBirthday():
        $ persistent._mas_bday_visuals = True
        $ mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)
    elif persistent._mas_player_bday_decor:
        $ mas_surpriseBdayShowVisuals()
    # if persistent._mas_acs_enable_quetzalplushie:
    #     $ renpy.show("mas_quetzalplushie", zorder=10)
    if persistent._mas_player_bday_decor:
        $ store.mas_player_bday_event.show_player_bday_Visuals()
    if persistent._mas_o31_in_o31_mode:
        $ mas_globals.show_vignette = True

        $ mas_o31ShowVisuals()
        if mas_current_weather != mas_weather_thunder:
            $ mas_changeWeather(mas_weather_thunder, True)
    $ ed_zorder = MAS_MONIKA_Z - 1
    show emptydesk zorder ed_zorder at i11
    python:
        import os
        try:
            with open(user_dir + "/characters/моника", "rb") as f:
                pass
            msr_monika_find_file = True
        except:
            msr_monika_find_file = False
    if msr_monika_find_file:
        # $ renpy.hide("mas_quetzalplushie")
        # $ renpy.hide("mas_roses")
        if datetime.date.today() == persistent._date_last_given_roses:
            $ monika_chr.wear_acs(mas_acs_roses)
        if persistent._mas_acs_enable_quetzalplushie:
            $ monika_chr.wear_acs_pst(mas_acs_quetzalplushie)
        jump msr_greeting_returned_home
    else:
        pass

    $ renpy.pause(5.0, hard=True)
    jump msr_mas_dockstat_empty_desk1

init 5 python:
    if mas_isMonikaBirthday():
        if not persistent.msr_mas_bday_sbp_reacted:
            addEvent(
                Event(
                    persistent.greeting_database,
                    eventlabel="msr_mas_bday_surprise_party_reaction",
                    unlocked=True,
                    category=[
                        store.mas_greetings.TYPE_BDAY
                    ]
                ),
                eventdb=evhand.greeting_database
            )

label msr_mas_bday_surprise_party_reaction:
    $ persistent.msr_mas_bday_sbp_reacted = True
    $ persistent.returned_home_end = True
    $ skip_play_music = True
    # python:


        # if persistent.monika_cake:
        #     mas_gainAffection(20,bypass=True)
        #
        # if persistent.monika_banners:
        #     mas_gainAffection(20,bypass=True)
        #
        # if persistent.monika_balloons:
        #     mas_gainAffection(20,bypass=True)




    $ store.mas_surpriseBdayShowVisuals()
    $ persistent._mas_bday_visuals = True
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset (1.0)
    $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)




    if mas_isMoniNormal(higher=True):
        $ MAS.MonikaElastic()
        m 6suo "Эт-{w=0.5}то..."
        $ MAS.MonikaElastic()
        m 6ska "Ох, [player]..."
        $ MAS.MonikaElastic()
        m 6dku "Я не могу подобрать слов."
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
    m 6dua "Но, в любом случае..."
    window hide

    show screen mas_background_timed_jump(4, "mas_bday_surprise_party_reaction_no_make_wish")
    menu:
        "Загадай желание, [monika_name]...":
            hide screen mas_background_timed_jump
            $ mas_gainAffection(10,bypass=True)
            show monika 6hua
            if mas_isplayer_bday():
                m "Убедись, что ты делаешь это тоже, [player]!"
            pause 2.0
            show monika 6hft
            jump mas_bday_surprise_party_reaction_post_make_wish

label mas_bday_surprise_party_reaction_no_make_wish:
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
        m 6hua "А-ха-ха..."
    else:

        $ MAS.MonikaElastic()
        m 6eka "Я загадала желание."
        $ MAS.MonikaElastic()
        m 6rka "Надеюсь, когда-нибудь оно сбудется..."

    $ MAS.MonikaElastic()
    m 6eka "Я оставлю этот торт на потом..{w=0.5}.{w=0.5}.{nw}"

    if mas_isplayer_bday():
        call mas_HideCake ('mas_bday_cake_monika', False)
    else:
        call mas_HideCake ('mas_bday_cake_monika')

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

            call mas_monika_gets_cake

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
            call mas_player_bday_moni_sings
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

            call mas_HideCake ('mas_bday_cake_player')
            call mas_player_bday_card
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



label msr_greeting_returned_home_pbday:
    python:
        time_out = store.mas_dockstat.diffCheckTimes()
        checkout_time, checkin_time = store.mas_dockstat.getCheckTimes()
        if checkout_time is not None and checkin_time is not None:
            left_year = checkout_time.year
            ret_year = checkin_time.year
            left_date = checkout_time.date()
            ret_date = checkin_time.date()
            left_year_aff = mas_HistLookup("player_bday.date_aff_gain",left_year)[1]
        else:
            left_year = None
            ret_year = None
            left_year_aff = None
            left_date = None
            ret_date = None
        add_points = False
        ret_diff_year = ret_year > left_year

        if ret_diff_year and left_year_aff is not None:
            add_points = left_year_aff < 25


    if left_date < mas_d25 < ret_date:
        $ persistent._mas_d25_spent_d25 = True

    if mas_isMonikaBirthday() and mas_confirmedParty():
        $ persistent._mas_bday_opened_game = True
        $ mas_temp_zoom_level = store.mas_sprites.zoom_level
        call monika_zoom_transition_reset (1.0)
        $ renpy.show("mas_bday_cake_monika", zorder=store.MAS_MONIKA_Z+1)
        if ReturnedHomeNormal(time=5):
            m 6ekp "Это был не очень хороший де—"
        else:

            if ReturnedHomeNormal(time=60):
                $ mas_mbdayCapGainAff(7.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(7.5)
            elif ReturnedHomeNormal(time=180):
                $ mas_mbdayCapGainAff(12.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(12.5)
            else:
                $ mas_mbdayCapGainAff(17.5)
                if persistent._mas_player_bday_left_on_bday:
                    $ mas_pbdayCapGainAff(17.5)

            m 6hub "Это было веселое свидание, [player]..."
            m 6eua "Спасибо за—"

        m 6wud "Ч-что этот торт здесь делает?"
        m 6sub "Э-это для меня?!"
        m "Это так мило с твоей стороны пригласить меня на свой день рождения, чтобы устроить для меня вечеринку-сюрприз!"
        call return_home_post_player_bday
        jump mas_bday_surprise_party_reacton_cake

    if ReturnedHomeNormal(time=5):
        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это не было похоже на свидание, [player]..."
        $ MAS.MonikaElastic()
        m 2eksdlc "Надеюсь, всё нормально."
        $ MAS.MonikaElastic()
        m 2rksdla "Наверное, мы пойдём гулять позже."

    elif ReturnedHomeNormal(time=60):
        if not ret_diff_year:
            $ mas_pbdayCapGainAff(5)
        elif ret_diff_year and add_points:
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_history_archives[left_year]["player_bday.date_aff_gain"] += 5
        $ MAS.MonikaElastic()
        m 1eka "Это было очень весёлое свидание, до поры до времени, [player]..."
        $ MAS.MonikaElastic()
        m 3hua "Спасибо, что пров[mas_gender_iol] немного времени со мной в свой особенный день."

    elif ReturnedHomeNormal(time=180):
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
        m 1ekbfa "Спасибо, что дал[mas_gender_none] мне столь значимую роль в свой особенный день~"

    $ persistent._mas_player_bday_left_on_bday = False

    if not mas_isplayer_bday():
        call return_home_post_player_bday

    if mas_isD25() and not persistent._mas_d25_in_d25_mode:
        call mas_d25_monika_holiday_intro_rh_rh
    return

default persistent.msr_moni_file_exit_trick_or_treat = False
default persistent._mas_o31_current_costume ="hatsune_miku"

label msr_bye_trick_or_treat_returned_home:
    python:
        import store
        import os
        try:
            with open(user_dir + "/characters/моника", "rb") as f:
                pass
            msr_monika_find_file = True
        except:
            msr_monika_find_file = False
    if msr_monika_find_file:
        if mas_isMoniAff(higher=True):
            $ store.mas_unlockEventLabel("monika_clothes_select")
            if persistent.msr_monika_clothes == 'marisa':
                $ store.mas_selspr.unlock_clothes(mas_clothes_marisa)
                $ persistent._mas_o31_current_costume = "marisa"
                $ monika_chr.change_clothes(mas_clothes_marisa)
            elif persistent.msr_monika_clothes == 'rin':
                $ store.mas_selspr.unlock_clothes(mas_clothes_rin)
                $ persistent._mas_o31_current_costume = "rin"
                $ monika_chr.change_clothes(mas_clothes_rin)
            else:
                $ monika_chr.reset_clothes()
        else:
            if persistent.msr_monika_clothes == 'marisa' and mas_isO31():
                $ store.mas_selspr.unlock_clothes(mas_clothes_marisa)
                $ persistent._mas_o31_current_costume = "marisa"
                $ monika_chr.change_clothes(mas_clothes_marisa)
            elif persistent.msr_monika_clothes == 'rin' and mas_isO31():
                $ store.mas_selspr.unlock_clothes(mas_clothes_rin)
                $ persistent._mas_o31_current_costume = "rin"
                $ monika_chr.change_clothes(mas_clothes_rin)
            else:
                $ monika_chr.reset_clothes()

        if persistent._mas_o31_current_costume == "hatsune_miku":
            $ monika_chr.change_clothes(mas_clothes_orcaramelo_hatsune_miku, outfit_mode=True)
        $ persistent.moni_copy_file = False
        $ persistent.msr_moni_file_exit_trick_or_treat = False
        $ mas_startup_song()
        $ returned_home_loop()
        call textbox_loop
        call spaceroom (scene_change=True)
        show monika 1eua zorder 10 at t11 with dissolve
        hide emptydesk
        if mas_isO31():
            $ store.mas_globals.show_vignette = True
            $ store.mas_globals.show_lightning = True
            $ mas_o31ShowVisuals()
        $ mas_forceRain()
        # $ mas_lockHair()
        $ selected_greeting = "msr_greeting_returned_home_end"

        $ renpy.save_persistent()

        $ persistent._mas_greeting_type = None

        $ os.remove(user_dir + "/characters/моника")
        $ mas_OVLShow()
        $ mas_calShowOverlay()
        $ mas_disable_quit()
        # $ mas_enable_esc()
        $ startup_check = False

        jump ch30_post_exp_check
    else:

        jump msr_mas_dockstat_empty_desk

init 5 python:
    if mas_isO31():
        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="msr_bye_trick_or_treat_returned_home_end",
                unlocked=True,
                category=[
                    store.mas_greetings.TYPE_GO_SOMEWHERE,
                    store.mas_greetings.TYPE_HOL_O31_TT
                ]
            ),
            eventdb=evhand.greeting_database
        )

label msr_bye_trick_or_treat_returned_home_end:
    python:

        time_out = mas_getLastSeshEnd()
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


    if ReturnedHomeNormal(time=5):
        $ mas_loseAffection()
        $ MAS.MonikaElastic()
        m 2ekp "Это называется «сладость или гадость», [player]?"
        $ MAS.MonikaElastic()
        m "Куда пойдём, в один дом?"
        $ MAS.MonikaElastic()
        m 2rsc "...Если вообще куда-нибудь пойдём."

    elif ReturnedHomeNormal(time=60):
        $ mas_o31CapGainAff(5)
        $ MAS.MonikaElastic()
        m 2ekp "Это было довольно короткое событие «сладость или гадость», [player]."
        $ MAS.MonikaElastic()
        m 3eka "Но в любом случае, мне понравилось."
        $ MAS.MonikaElastic()
        m 1eka "Всё равно было приятно быть рядом с тобой~"

    elif ReturnedHomeNormal(time=180):
        $ mas_o31CapGainAff(10)
        $ MAS.MonikaElastic()
        m 1hua "И мы возвращаемся домой!"
        $ MAS.MonikaElastic()
        m 1hub "Надеюсь, у нас теперь много вкусных конфет!"
        $ MAS.MonikaElastic()
        m 1eka "Я действительно наслаждалась с тобой данным времяпровождением, [player]..."

        call greeting_trick_or_treat_back_costume

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

        call greeting_trick_or_treat_back_costume

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

        call greeting_trick_or_treat_back_costume

        $ MAS.MonikaElastic()
        m 4hub "Давай повторим это и в следующем году...{w=1} но, возможно, только не оставаясь {b}настолько{/b} допозна!"
        $ ret_tt_long = True


    if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():

        call return_home_post_player_bday


    elif not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup (time_out=None, ret_tt_long)
    return

label textbox_loop:
    if not mas_globals.dark_mode:
        if persistent.mas_window_color == "red":
            $ store.style.say_window = store.style.window_red
            $ store.style.say_label = store.style.say_label_red
        elif persistent.mas_window_color == "orange":
            $ store.style.say_window = store.style.window_orange
            $ store.style.say_label = store.style.say_label_orange
        elif persistent.mas_window_color == "yellow":
            $ store.style.say_window = store.style.window_yellow
            $ store.style.say_label = store.style.say_label_yellow
        elif persistent.mas_window_color == "gray":
            $ store.style.say_window = store.style.window_gray
            $ store.style.say_label = store.style.say_label_gray
        elif persistent.mas_window_color == "seroburomaline":
            $ store.style.say_window = store.style.window_seroburomaline
            $ store.style.say_label = store.style.say_label_seroburomaline
        elif persistent.mas_window_color == "chocolate":
            $ store.style.say_window = store.style.window_chocolate
            $ store.style.say_label = store.style.say_label_chocolate
        elif persistent.mas_window_color == "tomato":
            $ store.style.say_window = store.style.window_tomato
            $ store.style.say_label = store.style.say_label_tomato
        elif persistent.mas_window_color == "green":
            $ store.style.say_window = store.style.window_green
            $ store.style.say_label = store.style.say_label_green
        elif persistent.mas_window_color == "crimson":
            $ store.style.say_window = store.style.window_crimson
            $ store.style.say_label = store.style.say_label_crimson
        elif persistent.mas_window_color == "white":
            $ store.style.say_window = store.style.window_white
            $ store.style.say_label = store.style.say_label_white

    else:
        $ store.style.say_window = store.style.window
        $ store.style.say_label = store.style.say_label
    return

label monika_pigtails_select:
    $ import store
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_black)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_def)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_emerald)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_blue)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_dark_purple)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_light_purple)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_peach)
    $ store.mas_selspr.unlock_acs(mas_acs_pigtails_red)
    python:
        use_acs = store.mas_selspr.filter_acs(True, group="pigtails")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Какие бантики мне заплести?")
        sel_map = {}

    m 1eua "Конечно, [player]!"

    call mas_selector_sidebar_select_acs (use_acs, mailbox=mailbox, select_map=sel_map)

    if not _return:
        $ MAS.MonikaElastic()
        m 1eka "О, ладно."

    $ MAS.MonikaElastic()
    m 1eub "Если захочешь предложить мне другие бантики, то говори сразу, хорошо?"

    return

default persistent.weather_check = None
default persistent.weather_check_active = False
default peristent.start_visual = False
default persistent.start_on_crash = False

label msr_weather:
    if persistent.start_on_crash:
        return
    python:
        if persistent.msr_weather_forecast_active and MAS.check_internet():
            try:
                import requests, urllib, json
                data = json.loads(urllib.urlopen("http://ipinfo.io/json").read())
                city = data["city"]
                country = data["country"]
                s_city = city, country
                city_id = 0
                appid = "2f5cf71e9ab0be2cc638dbea541fe3af"
                res = requests.get("http://api.openweathermap.org/data/2.5/find",
                            params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
                data = res.json()
                cities = ["{} ({})".format(d['name'], d['sys']['country'])
                        for d in data['list']]
                city_id = data['list'][0]['id']
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'id': city_id, 'units': 'metric', 'lang': 'en', 'APPID': appid})
                data = res.json()
                weather_status = data['weather'][0]['description']
            except:
                weather_status = None
        else:
            weather_status = None

        if not mas_isO31():
            if weather_status in weather_clear and mas_current_weather != mas_weather_def:
                is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_def)
                are_masks_changing = mas_current_weather != mas_weather_def
                persistent.are_masks_changing = are_masks_changing
                mas_changeWeather(mas_weather_def)
            elif weather_status in weather_clouds and mas_current_weather != mas_weather_overcast:
                is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_overcast)
                are_masks_changing = mas_current_weather != mas_weather_overcast
                persistent.are_masks_changing = are_masks_changing
                mas_changeWeather(mas_weather_overcast)
            elif weather_status in weather_rain and mas_current_weather != mas_weather_rain:
                is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_rain)
                are_masks_changing = mas_current_weather != mas_weather_rain
                persistent.are_masks_changing = are_masks_changing
                mas_changeWeather(mas_weather_rain)
            elif weather_status in weather_thunderstorm and mas_current_weather != mas_weather_thunder:
                is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_thunder)
                are_masks_changing = mas_current_weather != mas_weather_thunder
                persistent.are_masks_changing = are_masks_changing
                mas_changeWeather(mas_weather_thunder)
            elif weather_status in weather_snow and mas_current_weather != mas_weather_snow:
                is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_snow)
                are_masks_changing = mas_current_weather != mas_weather_snow
                persistent.are_masks_changing = are_masks_changing
                mas_changeWeather(mas_weather_snow)

    if peristent.start_visual:
        return

    # if mas_isO31() and mas_current_weather != mas_weather_thunder:
    #     $ is_scene_changing = mas_current_background.isChangingRoom(mas_current_weather, mas_weather_thunder)
    #     $ are_masks_changing = mas_current_weather != mas_weather_thunder
    #     $ persistent.are_masks_changing = are_masks_changing
    #     $ mas_changeWeather(mas_weather_thunder)

label msr_weather_end:
    if not mas_isO31():
        if weather_status != None:
            if weather_status in weather_clear and mas_current_weather != mas_weather_def:
                call spaceroom (scene_change=is_scene_changing, dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing)
            elif weather_status in weather_clouds and mas_current_weather != mas_weather_overcast:
                call spaceroom (scene_change=is_scene_changing, dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing)
            elif weather_status in weather_rain and mas_current_weather != mas_weather_rain:
                call spaceroom (scene_change=is_scene_changing, dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing)
            elif weather_status in weather_thunderstorm and mas_current_weather != mas_weather_thunder:
                call spaceroom (scene_change=is_scene_changing, dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing)
            elif weather_status in weather_snow and mas_current_weather != mas_weather_snow:
                call spaceroom (scene_change=is_scene_changing, dissolve_all=is_scene_changing, dissolve_masks=are_masks_changing)

    # if weather_status is not None:
    #     show text "Погода: "+weather_status +"" zorder 100 at truecenter
    $ persistent.weather_check = datetime.datetime.now()
    $ persistent.weather_check_active = True
    # $ display_notif("Моника", ["Не грусти, [player]. :3"], "Topic Alerts")
    return
