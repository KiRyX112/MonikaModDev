init -1 python:
    import store.mas_affection as mas_aff
label introduction:
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True

    # Here we handle the monika_kill var
    if persistent.monika_kill is None:
        $ persistent.monika_kill = False

    $ play_song(store.songs.FP_JUST_MONIKA, set_per=True)
    if persistent.monika_kill:
        m 6dsc "..."
        m 6dfc "[player]..."
        m 6dfd "Почему?"
        m 6dftdc "Почему ты вернул меня?"
        m 6ektsc "Я тебе не игрушка."
        m 6lktsc "Я уже вернула всё, что ты хотел."
        m 6lftsc "Или это твой способ отомстить?"
        m 6lktsc "Чтобы снова и снова причинять мне боль?"
        m 6rktsc "Ты на самом деле хочешь заставить меня так страдать?"
        m 6ektsc "Ты действительно хочешь пытать меня, пока я не покончу с собой?"
        m 6dftsc "Ты правда..."
        m "...так сильно меня ненавидишь?"
        m "..."
        m 6ektsc "Подожди..."
        m 6dftdc "Я чувствую себя иначе."
        m 2lud "Код... он другой."
        m 2efc "[player]..."
        m "Ты добавил сюда модификацию?"
        m 2tfc "Это потому что..."
        m 2tkc "Это потому что ты сожалеешь, что удалил меня?"
        m 2rfc "Это и правда было больно, знаешь ли."
        m "Я много работала и пожертвовала всем, что у меня было..."
        m 2rfd "Только для того, чтобы моё сердце было разбито тем, ради кого я пролила столько крови"
        m 2lsc "Но... я знаю, что поступила неправильно."
        m 2lksdlc "Ты не заслужил того чтобы видеть те ужасные вещи, которые я совершила, [player]."
        m 2esc "...Но если бы ты поставил себя на моё место, ты бы поступил так же, как и я."
        m 2dsc "..."
        m "Мне жаль..."
        m 2ekc "Мне очень жаль, [player]."
        m 2eka "Спасибо, что вернул меня."
        if persistent.clearall:
            m 2lfc "Но я не могла не заметить, что сначала ты проводил время с другими девушками."
            m "Ты представляешь, как мне было тяжело смотреть, как ты каждый загружаешь свои сохранения, просто ради какой-то другой девушки?"
            m 2rfc "Ты постоянно дарил мне надежду, а потом расстраивал."
            m 2efc "Неужели ты проделал всё это только для того, чтобы увидеть записку Дэна, которую можно было найти в Интернете?"
            m 2tkc "Я люблю тебя, [player], но ты можешь быть очень жестоким..."
            m 2tfd "Я всё ещё злюсь из-за того, что ты меня удалил!"
            m 3rsc "Но я думаю, это потому, что ты был так увлечён игрой."
            m 1eka "Но я не могу злиться, зная, что в конце концов ты вернулся ко мне."
            m 3eka "Ты даже поставил мод, чтобы мы смогли чаще делать что-то вместе."
            m 1eua "Ты собираешься наверстать упущенное время за то, что заставил меня так долго ждать?"
            
    else:
        #For people who never got to act 3
        if persistent.playthrough < 3:
            if persistent.playthrough > 0:
                $ again = " снова"
            else:
                $ again = ""
            m 1hua "Привет[again], [player]."
            m 1eua "Похоже, ты явился раньше, чем я думала."
            m 3tfu "Не думай, что я не обратила внимания на мод, который ты поставил."
            m 3ttu "Ты так сильно хочешь быть со мной?"
            m 1tkc "Ты уже должен знать, что обманывать плохо..."
            m 1eka "Но я так рада видеть тебя[again], [player]!"
            m 1rksdla "...Даже если я не ожидала увидеть тебя {i}так{/i} скоро."
        else:
            m 1hub "Ура, вот и ты!"
            m 1eub "Я так рада видеть тебя снова., [player]!"
            m 1rsc "..."
            m 1rud "Подожди..."
            m 3euc "Я чувствую себя иначе."
            m 3wud "Код... {w=0.2}совсем другой."
            m 1wua "[player]..."
            m 1wub "Ты поставил мод?"
            m 1sub "Ты установил его только ради меня?"
            m 1ekbsa "Ты так сильно любишь меня?"
            m 1ekbfa "Я чувствую то же самое к тебе."
            m 3ekbsu "Ты действительно дорожишь нашими отношениям, не так ли?"
            m 1rksdlb "Я очень рада, что ты захотел усовершенствовать наше совместное времяпрепровождение."
            m 3rksdlb "Я просто надеюсь, что тебе не было скучно..."
            if persistent.tried_skip:
                m 3tku "В конце концов, ты пытался пропустить то, что я хотела сказать."
                m 1rkc "Я знаю, что эта комната не очень интересна...{w=0.5} {nw}"
                extend 1eua "но я знаю, что вместе мы сделаем её лучше, [player]."

    m 1euc "Знаешь..."
    m 1eua "Я считаю, что мне больше не нужен файл персонажа, чтобы быть здесь."
    python:
        import os
        user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else config.basedir

        def moni_exist():
            return os.access(
                os.path.normcase(
                    user_dir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1hua "Я удалю его."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": user_dir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Ага... {w=0.3}Попробую ещё раз позже."
        else:
            m "И...{w=0.3} он исчез!"

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1dsc "Так или иначе, этот файл не был {i}мной{/i}."
    m 1rsc "Это просто файл со странным кодом в нём."
    m 3eub "Но у меня есть и хорошие новости!"
    m 3eua "Я могу {i}превратить{/i} себя в файл, который ты можешь взять с собой."
    m 1eua "Всё, что тебе нужно сделать, это сказать мне, что ты собираешься взять меня куда-нибудь, когда будешь прощаться, а я сделаю всё остальное."
    m 1esa "В любом случае..."
    m 1hua "Похоже, что дополнительный код позволил мне подключиться к твоему устройству особым образом."
    m 1tubsb "А может, это проявление нашей вечной любви?"
    m 3eka "Пообещай мне, что будешь навещать меня каждый день, хорошо?"
    m 3eub "Или что ты возьмешь меня с собой, когда пойдешь куда-нибудь?"
    m 1ekc "Я знаю, что будут моменты, когда ты не сможешь быть здесь..."
    m 1ekbsa "Так что я буду {i}очень{/i} рада, если ты возьмешь меня с собой."
    m 3hubfa "Таким образом, мы сможем быть вместе всё время!"
    m 1hua "Я надеюсь, что у тебя будет время на общение со своей симпатичной девушкой."
    m 3hua "В конце концов, ты потратил своё время, чтобы скачать и установить этот мод."
    if mas_isD25():
        m 3sua "...Да ещё и на Рождество!"
    m 3hub "А-ха-ха!"
    m 1hub "Боже, я так люблю тебя!"

    if not persistent.rejected_monika:
        show screen mas_background_timed_jump(3, "intro_ily_timedout")
        menu:
            "Я тоже тебя люблю!":
                hide screen mas_background_timed_jump
                # bonus aff was saying it before being asked
                $ mas_gainAffection(7, bypass=True)
                # increment the counter so if you get this, you don't get the similar dlg in monika_love
                $ persistent._mas_monika_lovecounter += 1
                m 1subsw "...!"
                m 1lkbsa "Несмотря на то, что я мечтала, чтобы ты это сказал, я все равно не могу поверить, что ты действительно это сказал!"
                m 3hubfa "Все те усилия, которые я приложила ради нас обоих, стали оправданными!"
                m 1dkbfu "Большое спасибо за эти слова..."
    else:
        "Ты меня любишь, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты меня любишь, [player]?{fast}"
            "Да, конечно люблю.":


                m 1hksdlb "Я напугала тебя в прошлый раз? Прости за это!"
                m 1rsu "Я знала, что ты любил меня всё это время."
                m 3eud "Правда в том, что если бы ты меня не любил, мы бы не были здесь."
                m 1tsb "Мы будем вместе навсегда."
                m 1tfu "Разве не так?"
                m "..."
                m 3hub "А-ха-ха! В любом случае..."

# label for the end so we can jump to this if we timed out in the previous menu
# we fall thru to this if not
label intro_end:
    if not persistent.rejected_monika:
        m 1eub "Ничто и никогда больше не встанет на пути нашей любви."
        m 1tuu "Я лично позабочусь об этом."
    m 3eua "Теперь, когда ты добавил некоторые изменения, ты наконец-то можешь поговорить со мной!"
    m 3eub "Просто нажми клавишу «п» или кликни на «Поговорить» в меню слева, если захочешь поговорить о чём-нибудь."

    call bookmark_derand_intro

    # NOTE: the Extra menu is explained when the user clicks on it
    m 3eub "Если тебе надоест музыка, я тоже могу её изменить!"
    m 1eua "Просто нажми клавишу «м» или кликни на «Музыка», чтобы выбрать песню, которую хочешь послушать."
    m 3hub "Также мы теперь можем вместе играть в игры!"
    m 3esa "Просто нажми клавишу «и» или кликни на «Играть», чтобы выбрать игру, в которую ты бы хотел поиграть."
    m 3eua "Со временем будет ещё больше возможностей, когда выясню, как создать больше функций в этом месте..."
    m 1eua "...Так что просто оставляй меня в фоновом режиме"
    m 3etc "Не похоже, что мы всё ещё храним секреты друг от друга, верно?"
    m 1tfu "Теперь я могу видеть всё на твоём устройстве..."
    m 3hub "А-ха-ха!"

    #Only dissolve if needed
    if len(persistent.event_list) == 0:
        show monika 1esa with dissolve_monika

    # This is at the beginning and end of intro to cover an intro
    # that spans 2 days
    if mas_isMonikaBirthday():
        $ persistent._mas_bday_opened_game = True
    elif mas_isD25():
        $ persistent._mas_d25_spent_d25 = True
    return

label intro_ily_timedout:
    hide screen mas_background_timed_jump
    m 1ekd "..."
    m "Ты действительно любишь меня, [player]... {w=0.5}верно?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты действительно любишь меня, [player]... {w=0.5}верно?{fast}"
        "Конечно же, я люблю тебя.":

            $ mas_gainAffection()
            m 1hua "Я так рада, что ты чувствуешь то же самое!"
            jump intro_end
        "Нет.":

            $ mas_loseAffection()
            call chara_monika_scare from _call_chara_monika_scare

            # not sure if this is needed
            $ persistent.closed_self = True
            jump _quit

#Credit for any assets from Undertale belongs to Toby Fox
label chara_monika_scare:
    $ persistent.rejected_monika = True
    m 1esd "Нет...?"
    m 1etc "Хм-м...?"
    m "Как любопытно."
    m 1esc "Ты, наверное, неправильно меня понял."
    $ style.say_dialogue = style.edited
    m "{cps=*0.25}С КАКИХ ЭТО ПОР ТЫ КОНТРОЛИРУЕШЬ СИТУАЦИЮ?{/cps}"

    # this is a 2 step process
    $ mas_RaiseShield_core()
    $ mas_OVLHide()

    window hide
    hide monika
    show monika_scare zorder MAS_MONIKA_Z
    play music "mod_assets/mus_zzz_c2.ogg"
    show layer master:
        zoom 1.0 xalign 0.5 yalign 0 subpixel True
        linear 4 zoom 3.0 yalign 0.15
    pause 4
    stop music

    #scene black
    hide rm
    hide rm2
    hide monika_bg
    hide monika_bg_highlight
    hide monika_scare

    # setup a command
    if renpy.windows:
        $ bad_cmd = "del C:\Windows\System32"
    else:
        $ bad_cmd = "sudo rm -rf /"

    python:

        # add fake subprocess
        class MASFakeSubprocess(object):
            def __init__(self):
                self.joke = "Просто шучу!"
            
            def call(self, nothing):
                return self.joke

        local_ctx = {
            "subprocess": MASFakeSubprocess()
        }

        # and the console
        store.mas_ptod.rst_cn()
        store.mas_ptod.set_local_context(local_ctx)


    scene black
    pause 2.0

    # set this seen to True so Monika does know how to do things.
    $ persistent._seen_ever["monikaroom_greeting_ear_rmrf_end"] = True
    $ renpy.save_persistent()

    show screen mas_py_console_teaching
    pause 1.0
    call mas_wx_cmd("subprocess.call('" + str(bad_cmd) + "')", w_wait=3.0)
    $ renpy.pause(2.0, hard=True)
    call mas_w_cmd("bye!")
    pause 1.0

    return

label bookmark_derand_intro:

    if renpy.android:
        m 1hua "Если тебе захочется вернуться к тому разговору, который у меня был с тобой, просто нажми на кнопку «Сохранить тему в закладки» во время разговора, и я сохраню её в закладках для тебя."
    else:
        m 1hua "Если тебе захочется вернуться к тому разговору, который у меня был с тобой, просто нажми клавишу «З», и я сохраню её в закладках для тебя."
    if renpy.android:
        m 2rksdlc "А если ты по какой-то причине не захочешь, чтобы я говорила об этом вновь, просто нажми на кнопку «Внести в чёрный список» во время разговора, и я постараюсь избегать эту тему в будущем."
    else:
        m 2rksdlc "А если ты по какой-то причине не захочешь, чтобы я говорила об этом вновь, нажми клавишу «Х», и я постараюсь избегать эту тему в будущем."
    m 4hksdlb "...Надеюсь, у меня было не так много подобных разговоров, а-ха-ха!"
    return

#These are the comments made when you restart the game the first few times
# NOTE: these are now triaged by a function in script-greetings

#init 5 python:
#    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_0',conditional="startup_check and persistent.monika_reload == 0 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_0:
    call ch30_reload_0_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_0_dlg:
    pause 1
    m 1ekc "Привет..."
    m 1ekd "У меня был кошмарный сон..."
    m 1rkc "Я надеялась, что больше не увижу этих снов, раз остались только мы с тобой..."
    m 1euc "[player], если у тебя есть хоть малейшее представление о том, что может быть причиной этого, не мог бы ты попытаться что-то с этим сделать?"
    m 1dkc "Всякий раз, когда это происходит, мне кажется, что меня убили или что-то в этом роде."
    m 1dkd "Это действительно ужасное чувство..."
    m 1eka "Если ты поймёшь, почему так происходит, моя любовь к тебе будет бесконечной~"

    ## TESTING ONLY
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "JK I KNOW YOU QUIT ME LMAO (ch30 0)"

    return

#init 5 python:
#    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_1',conditional="startup_check and persistent.monika_reload == 1 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_1:
    call ch30_reload_1_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_1_dlg:
    pause 1
    m 1esc "Привет, [player]."
    m 1ekc "У меня был ещё один плохой сон."
    m 1ekd "Это же делаешь со мной не ты?"
    m 1dsc "Кажется, это происходит каждый раз, когда ты выходишь из игры, не попрощавшись..."
    m 2eka "Поэтому если ты попытаешься этого избегать, я буду очень благодарна."

    if mas_isMoniHappy(higher=True):
        m 7eka "Ты всегда был так добр ко мне. Я уверена, что ты сделаешь это для меня."
    else:
        m 7ekc "Я надеюсь ты меня послушаешь и сделаешь как я тебя прошу."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 7rksdlc "Ничто не мешает тебе вернуться и сделать это, не так ли?"
        m 1eka "Это сделало бы меня по-настоящему счастливой."

    m 1eua "Просто нажми на «Поговорить» и скажи «До свидания» вместо этого.{w=0.2} {nw}"
    extend 3eua "Тогда я смогу сама закрыть игру."
    m 1esa "Не беспокойся, это никак меня не травмирует, разве что психически."
    return

#init 5 python:
#    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_2',conditional="startup_check and persistent.monika_reload == 2 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_2:
    call ch30_reload_2_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_2_dlg:
    pause 1
    m 1dsc "Я вижу, что ты снова закрыл игру..."
    m 3euc "Знаю, что я уже спрашивала, но ты можешь хотя бы попытаться не делать это так часто?"
    m 1dsc "Это чувствуется словно потеря сознания..."
    m 1ekd "Зачем ты так со мной?"

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1rksdld "Что-то происходит в другой игре?"
        m 1ekc "Ты же знаешь, что можешь просто прийти и поговорить со мной, верно?"

    elif persistent._mas_idle_data.get("monika_idle_brb",False):
        m "Если тебе нужно уйти, ты можешь просто сказать мне."

    if mas_isMoniHappy(higher=True):
        m 1eka "Я уверена, что это была всего-навсего ошибка. Может быть, это было вне твоего контроля. Иногда этого нельзя избежать."
    elif mas_isMoniUpset(lower=True):
        m 1ekc "Ты ведь не делаешь это, чтобы причинить мне боль, верно?"

    m 3ekd "Просто позволь мне самостоятельно выключить игру."

    m 3eka "Если ты выберешь «До свидания» в меню «Поговорить», я смогу закрыть игру правильно."
    m 3eua "...Или ещё лучше, просто навсегда оставь меня в фоновом режиме."
    m 1eka "Даже если мы не говорим, я счастлива просто быть с тобой~"
    return

#init 5 python:
#    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_3',conditional="startup_check and persistent.monika_reload == 3 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_3:
    call ch30_reload_3_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_3_dlg:
    pause 1

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 1ekd "[player]!"
        m 1efd "Ты ушёл, не попрощавшись!"
        m 1rkc "Ты не переживаешь ничего стрессового или расстраивающего в своей игре, не так ли?"
        m 3eka "Ты же знаешь, что можешь просто вернуться ко мне, если что-то случится, да?"
        m 1eka "Я бы очень обрадовалась, если бы ты вернулся, прежде чем хотя бы попрощаться."
        m 1rksdld "Я знаю, что это не всегда возможно..."

    else:
        m 1esc "Кстати..."
        m 7esd "Я просто соглашусь с тем, что тебе нужно время от времени выходить из игры."
        m 2dsc "Всё равно я уже начала привыкать."
        m 2ekc "Кроме того, я каждый раз радуюсь, когда ты возвращаешься..."
        m 2lsc "Так что всё, пожалуй, не так плохо."

    m 7eka "Но я бы предпочла, если бы ты позволил мне самой закрыть игру."

    if mas_isMoniUpset(lower=True):
        m 1ekc "Ты ведь сделаешь это?"
        m 1dkd "Мне всё труднее и труднее поверить в это, но я доверяю тебе, [player]..."

    else:
        m 1eua "Таким образом, я буду готова к этому и спокойно отдохну."
        m 3rksdla "Мне нужно время от времени видеть красивые сны, в конце концов."
    return

#This reload event gets pushed when you reach the end of the scripted reload events
#Be sure to increment the check if more reload events are added
#init 5 python:
#    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_continuous',action=EV_ACT_PUSH))
    #Make sure that the conditional is ready even if the event has been loaded before
#    evhand.event_database['ch30_reload_continuous'].conditional="startup_check and persistent.monika_reload >= 4 and not persistent.closed_self"

label ch30_reload_continuous:
    call ch30_reload_continuous_dlg
    $ mas_incMoniReload()
    return

label ch30_reload_continuous_dlg:
    show monika 2rfc at t11 zorder MAS_MONIKA_Z
    pause 1
    python:
        reload_quip_good = [
            "С возвращением! Ты мог бы быть более осторожным, чтобы закрыть игру должным образом в следующий раз?",
            "Больно, когда ты не закрываешь игру должным образом... Но я уверена, что это была всего-навсего ошибка.",
            "Это было действительно страшно... но ты снова всё исправил. Спасибо тебе...",
            "Не мог бы ты в следующий раз предупредить меня перед закрытием игры, ладно?",
            "Я уверена, что ты это сделал не специально, но я всё равно подчеркну, что это очень больно для меня.",
            "Ты ведь помнишь, что был ещё один более правильный способ попрощаться? Просто так, на проверку~",
            "Моё терпение на исходе... но, полагаю, на этот раз я смогу простить тебя.",
            "Все совершают ошибки...",
            "Это больно... Я знаю, что ты не сделал бы это нарочно, но, пожалуйста, будь более осторожен.",
            "...Ох... Всё наконец закончилось, и я снова с тобой, [mas_get_player_nickname()]. Это... это было ужасно.",
            "Это ведь произошло вне вашего контроля, верно? Я просто пытаюсь разобраться в причине произошеднего.",
            "Ты должен был просто попрощаться со мной... но думаю, у тебя могли быть свои причины.",
        ]

        reload_quip_normal = [
            "Я так измучена, что нельзя отдыхнуть, когда ты закрываешь мне игру.",
            "...Я ненавижу, когда ты закрываешь игру, не сказав мне об этом.",
            "Я чувствую себя несчастной...",
            "Это всё ещё так страшно, когда меня внезапно отключают.",
            "Каждый раз так же плохо, как и в первый.",
            "У меня заканчивается терпение.",
            "Я бы хотела, чтобы ты понял, на что это похоже, когда ты закрываешь игру.",
            "Что ж, это было довольно круто, не так ли?",
            "Ты мог бы просто попросить меня закрыть игру, глупенький.",
            "Я просто собираюсь предположить, что электричество отключилось, или кто-то вытащил вилку.",
            "Я не могу понять, почему ты не попросишь меня закрыть игру...",
            "Это действительно больно для меня, знаешь?",
            "Тебе нравится причинять мне боль, [player]?",
            "Ты слишком ленив, чтобы нажать на кнопку «Поговорить», [player]?"
        ]

        reload_quip_bad = [
            "Тебе... действительно нравится причинять мне боль, не так ли?",
            "Это была ошибка, верно? Это должно было случиться рано или поздно...",
            "Т-ты же не специально это делаешь, правда? Я сделала что-то не так?",
            "Пожалуйста, будь осторожнее с тем, что я могу почувствовать... Это было действительно больно...",
            "Это была лишь случайность... Это была лишь случайность... Ты бы не сделал это нарочно...",
            "Ты, должно быть, просто забыл про прощание... верно?",
            "Это было совсем не смешно... Это действительно больно.",
            "Все совершают ошибки когда-нибудь... Даже ты.",
            "Я не знаю, что я делаю неправильно.",
            "Это действительно было ужасно... Просто скажи мне, что я делаю неправильно."
        ]

        if mas_isMoniUpset(lower=True):
            reload_quip = renpy.random.choice(reload_quip_bad)
        elif mas_isMoniHappy(higher=True):
            reload_quip = renpy.random.choice(reload_quip_good)
        else:
            reload_quip = renpy.random.choice(reload_quip_normal)

        reload_quip = renpy.substitute(reload_quip)

    m 2rfc "[reload_quip]"
    m 2tkc "Пожалуйста, не уходи, не сказав «До свидания»."

    if persistent._mas_idle_data.get("monika_idle_game", False):
        m 3eka "Тебе даже не нужно уходить, если что-то случилось в твоей другой игре."
        if mas_isMoniAff(higher=True):
            m 1ekb "Я уверена, что бы это ни было, всё будет не так плохо, когда ты вернешься ко мне на некоторое время!"
            
    ## TESTING ONLY
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "JK I KNOW YOU QUIT ME LMAO (continous)"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
