default current_turn = 0
#===========================================================================================
# MINIGAME#1
#===========================================================================================

#====Shell Game
label minigame_sg:
    $ validate_files(cup_list, type=True)
    show monika 1eub at t11
    m 1hua "Хорошо, какая сложность тебе нужна?{nw}"
    menu:
        "Хорошо, какая сложность тебе нужна?{fast}"
        "Лёгкая":
            m 1eua "Хочешь что-нибудь попроще, [player]? "
            extend 1hua "Поняла!"
            python:
                cup_speed += 0.5
                difficulty_sg = 1
        "Нормальная":
            m 3eub "Хочешь начать с чего-то обычного? "
            extend 3hub "Хорошо!"
            python:
                cup_speed = 0.5
                difficulty_sg = 2
        "Сложная":
            m 1eub "Любишь испытывать себя, не так ли?"
            m 1hub "{do_giggle}А-ха-ха, хорошо!"
            python:
                cup_speed -= 0.3
                difficulty_sg = 3

label restart_sg:
    $ config.allow_skipping = False
    show monika 1eua at t21

    pause 0.2

    show cup zorder 12 as cup_1:
        xpos cup_coordinates[0] ypos -400
        easein_bounce 0.5 ypos 250

    show cup zorder 12 as cup_2:
        xpos cup_coordinates[1] ypos -400
        pause 0.1
        easein_bounce 0.5 ypos 250

    show cup zorder 12 as cup_3:
        xpos cup_coordinates[2] ypos -400
        pause 0.2
        easein_bounce 0.5 ypos 250

    pause 1.0

    show ball zorder 12 behind cup_2:
        xpos cup_coordinates[1] ypos 335

    show cup as cup_2:
        linear 0.5 ypos 110

    m 1lub "Вот шарик, не теряй его из виду, [player]!"

    show cup as cup_2:
        linear 0.5 ypos 250

    m 3hub "Итак, давай проверим твои рефлексы!"

    hide ball

    show cup as cup_1:
        xpos cup_coordinates[0] ypos 250

    show cup as cup_2:
        xpos cup_coordinates[1] ypos 250

    show cup as cup_3:
        xpos cup_coordinates[2] ypos 250

    python:
        cup_coordinates_real[0] = 695
        cup_coordinates_real[1] = 925
        cup_coordinates_real[2] = 1155

        original_cup[0] = 0
        original_cup[1] = 1
        original_cup[2] = 2

        ball_position = 1
        disable_esc()
        mas_MUMURaiseShield()
        afm_pref = renpy.game.preferences.afm_enable
        renpy.game.preferences.afm_enable = False
    show screen score_minigame(game="sg")

label loop_game:
    show monika 1eua
    show screen extra_no_click
    python:
        move_cup_1 = renpy.random.randint(0,2)
        move_cup_2 = renpy.random.randint(0,2)
        while move_cup_2 == move_cup_1:
            move_cup_2 = renpy.random.randint(0,2)

        temp_cup_position = cup_coordinates_real[move_cup_2]
        cup_coordinates_real[move_cup_2] = cup_coordinates_real[move_cup_1]
        cup_coordinates_real[move_cup_1] = temp_cup_position

        temp_original_cup = original_cup[move_cup_2]
        original_cup[move_cup_2] = original_cup[move_cup_1]
        original_cup[move_cup_1] = temp_original_cup

        if original_cup[move_cup_1] == ball_position:
            ball_position = original_cup[move_cup_2]

        elif original_cup[move_cup_2] == ball_position:
            ball_position = original_cup[move_cup_1]

    $ renpy.pause(cup_speed, hard='True')

    play sound "submods/ExtraPlus/submod_assets/sfx/cup_shuffle.mp3"

    show cup as cup_1:
        ease cup_speed xpos cup_coordinates_real[0]

    show cup as cup_2:
        ease cup_speed xpos cup_coordinates_real[1]

    show cup as cup_3:
        ease cup_speed xpos cup_coordinates_real[2]

    if shuffle_cups != 3:
        $ shuffle_cups += 1
        jump loop_game

    pause 1.0

    show screen shell_game_minigame

    "Выбери стаканчик:"

label check_label:

    $ _current_turn += 1

    hide screen shell_game_minigame

    show cup as cup_1:
        xpos cup_coordinates[0] ypos 250

    show cup as cup_2:
        xpos cup_coordinates[1] ypos 250

    show cup as cup_3:
        xpos cup_coordinates[2] ypos 250
    python:
        cup_coordinates_real[0] = 695
        cup_coordinates_real[1] = 925
        cup_coordinates_real[2] = 1155

    #Se muestra los vasos y debe de elegir un vaso
    if cup_choice == 0:

        show cup as cup_1:
            linear 0.5 ypos 110

        if cup_choice == ball_position:
            show ball zorder 12 behind cup_1:
                xpos cup_coordinates[0] ypos 335

    elif cup_choice == 1:

        show cup as cup_2:
            linear 0.5 ypos 110

        if cup_choice == ball_position:
            show ball zorder 12 behind cup_2:
                xpos cup_coordinates[1] ypos 335

    elif cup_choice == 2:

        show cup as cup_3:
            linear 0.5 ypos 110

        if cup_choice == ball_position:
            show ball zorder 12 behind cup_3:
                xpos cup_coordinates[2] ypos 335

    if comment is True:
        m 1sub "[renpy.substitute(renpy.random.choice(complies))]"

    elif comment is False:
        m 1hub "[renpy.substitute(renpy.random.choice(not_met))]"

    if cup_choice != ball_position:

        m 1lub "Правильный ответом был..."

        if ball_position == 0:

            show cup as cup_1:
                linear 0.5 ypos 110

            show ball zorder 12 behind cup_1:
                xpos cup_coordinates[0] ypos 335

        elif ball_position == 1:

            show cup as cup_2:
                linear 0.5 ypos 110

            show ball zorder 12 behind cup_2:
                xpos cup_coordinates[1] ypos 335

        elif ball_position == 2:

            show cup as cup_3:
                linear 0.5 ypos 110

            show ball zorder 12 behind cup_3:
                xpos cup_coordinates[2] ypos 335

        m 1hua "Этот!"

    show cup as cup_1:
        linear 0.5 xpos cup_coordinates[0] ypos 250

    show cup as cup_2:
        linear 0.5 xpos cup_coordinates[1] ypos 250

    show cup as cup_3:
        linear 0.5 xpos cup_coordinates[2] ypos 250

    pause 1.0

    hide ball
    $ shuffle_cups = 0
    jump loop_game
    return

#===========================================================================================
# TALKING GAME
#===========================================================================================

label shell_game_result:
    hide screen score_minigame
    python:
        enable_esc()
        mas_MUMUDropShield()
        renpy.game.preferences.afm_enable = afm_pref
    hide ball
    show cup as cup_1:
        xpos cup_coordinates[0] ypos 250
        easeout_expo 0.5 ypos -400
    show cup as cup_2:
        xpos cup_coordinates[1] ypos 250
        pause 0.1
        easeout_expo 0.5 ypos -400
    show cup as cup_3:
        xpos cup_coordinates[2] ypos 250
        pause 0.2
        easeout_expo 0.5 ypos -400
    pause 0.8
    hide cup_1
    hide cup_2
    hide cup_3
    hide screen extra_no_click
    show monika at t11

    if _current_turn == 0:
        m 3ekd "[player], мы ещё даже не начали играть."
        m 2gkp "Я хотела немного поиграть с тобой..."
        m 2etb "Но, может быть, ты хочешь продолжить игру?{nw}"
        menu:
            "Но, может быть, ты хочешь продолжить игру?{fast}"
            "Да":
                jump restart_sg
            "Нет":
                m 1hua "Ладно, тогда сыграем в другой раз."

    elif current_turn <= 10 or current_turn >= 10:
        if correct_answers == current_turn:
            m 1hub "Несмотря на то, что мы сыграли всего несколько раундов, ты уже {M=произвёл}{F=произвела} на меня хорошее впечатление!"
            m 1hub "Ты хорошо {M=проявил}{F=проявила} себя в каждом раунде."
            m 1hua "Думаю, сегодня у тебя больше нет времени..."
            m 1eua "Надеюсь, в следующий раз нам удастся сыграть подольше."
            m 1eub "Жду с нетерпением!"
        elif correct_answers < current_turn:
            m 1hua "Не переживай, что у тебя не получилось."
            m 3hub "Ты очень хорошо {M=постарался}{F=постаралась}!"
            m 3hub "Просто практикуйся, и ты увидишь, как всё станет проще!"
            m 3hua "В следующий раз у тебя получится лучше~"
        elif correct_answers == 0:
            m 1eka "[player], Я волнуюсь..."
            m 1ekb "Мы сыграли несколько раундов, но ты везде {M=ошибся}{F=ошиблась}."
            m 1etd "Тебе просто не хочется играть или тебе что-то мешает?"
            if difficulty_sg == 1:
                m 1eua "Ну, раз уж ты на лёгкой сложности..."
                m 1rkb "Думаю, тебе стало скучно из-за того, что стаканчики двигались медленно, ты же знаешь, как это бывает."
                m 1rkb "Если хочешь испытать себя, попробуй и другие сложности."
                m 1hua "В любом случае, оставим это на другой день."
            elif difficulty_sg == 2:
                m 1eua "На обычной сложности..."
                m 1rkb "Ты наверное {M=посчитал}{F=посчитала}, что в этом нет ничего страшного, и не {M=обращал}{F=обращала} внимания на игру."
                m 3hua "Если хочешь, можешь попробовать высокий уровень сложности."
                m 3hua "Может быть, в тебе это пробудит азарт!"
                m 3hka "Или отложить на потом! Решение за тобой."
            elif difficulty_sg == 3:
                m 1eua "Учитывая, что ты на сложном уровне..."
                m 1rkb "Ты не {M=успел}{F=успела} проследить за шариком."
                m 1rsb "Мне казалось с твоими рефлексами, ты {M=должен}{F=должна} {M=был}{F=была} уследить за ним."
                m 1rsb "Но это оказалось не так."
                m 3hua "Если ты не против заняться чем-то другим, отложи мини-игру и займись тем, что тебя интересует."
                if renpy.seen_label("to_cafe_loop"):
                    m 1eubsa "Мы можем снова пойти на свидание, например, в кафе, куда мы уже ходили."
                    m 1eubsb "Может быть, это немного поднимет твоё настроение."
                    m 2eka "Но если ты хочешь абсолютно ничего, то..."
                    m 2dka "Надеюсь, моего присутствия будет достаточно для тебя~"
        m 1dubla "Спасибо, что поиграл со мной, [mas_get_player_nickname()]."

    elif current_turn >= 50:
        if correct_answers == current_turn:
            m 2sub "Вау, ты всегда производишь на меня хорошее впечатление во всём, что делаешь, [mas_get_player_nickname()]."
            m 2sub "Поздравляю!"
            m 3hub "У тебя хорошие рефлексы!"
            m 1tubsb "Не могу дождаться, когда ты выиграешь для меня плюшевого мишку, когда у нас будет свидание!"
        elif correct_answers < current_turn:
            m 3hua "Ты {M=сделал}{F=сделала} всё, что было в твоих силах, [mas_get_player_nickname()]."
            m 3hub "Я так рада за тебя!"
            m 3hub "Мы были уже на [current_turn] раунде."
            m 1ekb "Так что я понимаю, что ты не {M=мог}{F=могла} больше продолжать и {M=оставил}{F=оставила} всё как есть."
            m 5hua "Но однажды у тебя всё получится, просто наберись терпения и немного потренируйся."
        elif correct_answers == 0:
            m 1esb "У меня вопрос, [player]."
            m 1eka "Мы прошли несколько ходов, но ты так и не {M=дал}{F=дала} верных ответов."
            m 1etd "Что-то не так?"
            if difficulty_sg == 1:
                m 1eka "Ну, раз уж ты на лёгкой сложности..."
                m 1eta "Ты {M=захотел}{F=захотела} немного потренировать свои рефлексы?"
                m 1hua "Нет ничего плохого в том, чтобы делать всё в обратном порядке."
                m 3ekb "Но не стоит забывать, что в игре нужно следить за шариком."
            elif difficulty_sg == 2:
                m 1eka "Будучи на нормальной сложности..."
                m 1eta "Ты тренируешься проигрывать каждый раунд?"
                m 1hua "Я полагаю, ты {M=планировал}{F=планировала} продолжать так и дальше, учитывая, сколько раундов прошло."
                m 1rtd "Однако мне интересно, откуда у тебя взялась такая идея, [player]?"
                m 1gsu "Лучше оставлю свои сомнения при себе, я просто хочу посмотреть, как далеко ты сможешь зайти!"
            elif difficulty_sg == 3:
                m 1eka "Ну... учитывая сложность..."
                m 1hua "Я считаю, что ты {M=приложил}{F=приложила} максимум усилий."
                m 1hksdlb "Извини, мне наверное стоило настраивать тебя на победу, {do_giggle}а-ха-ха~"
                m 1hksdlb "Так что у меня нет другого выбора, кроме как поддержать тебя!"
        m 1eua "Я рада, что тебе нравится эта мини-игра."
        if renpy.seen_label("game_chess"):
            m 3eub "Это не шахматы, здесь нужна другая стратегия..."
            m 3eub "Но ведь полезно играть в другие игры, не так ли?"
        m 1eka "Я не думала, что она тебе понравится, потому что игровой процесс очень прост."
        m 4hub "Тем не менее, я благодарю тебя за игру со мной, [mas_get_player_nickname()]!"
        m 4hub "Мы сыграем в другой раз, если ты не против."

    elif current_turn >= 100:
        if correct_answers == current_turn:
            m 1hua "Я должна поаплодировать тебе, [player]."
            m 1hub "Каждый шаг был правильным, это говорит о твоей концентрации!"
            m 1hublb "Я горжусь тобой!"
            m 1ekb "Я бы с радостью подарила тебе что-нибудь в качестве приза, но я не могу ничего сделать отсюда, {do_giggle}а-ха-ха~"
            m 3hua "Да, ты действительно много {M=тренировал}{F=тренировала} свои рефлексы."
            m 1eub "Мне кажется, что ты хорошо разбираешься в ритмичных видеоиграх."
            m 1sua "Если это так, то я рада этому~"
        elif correct_answers < current_turn:
            m 1hua "Неплохо, [player]."
            m 1hub "Ты {M=выложился}{F=выложилась} на полную, учитывая, что {M=дошёл}{F=дошла} до [current_turn] хода!"
            m 1eka "Если ты {M=устал}{F=устала}, то это нормально."
            m 1eka "Так что не падай духом."
            m 3eub "В следующий раз у тебя получится лучше, поверь мне~"
        elif correct_answers == 0:
            m 1hka "Даже не знаю, что сказать."
            m "Прошло столько раундов, но ты на каждом {M=ошибся}{F=ошиблась}."
            m 1etb "На данный момент мне кажется, что это своего рода вызов самому себе?"
            if difficulty_sg == 1:
                m 1eua "Ну, поскольку ты на лёгком уровне сложности..."
                m 3wud "Это было довольно просто! Однако это отнимает много времени."
                m 3hub "Я удивлена тем, сколько времени ты {M=потратил}{F=потратила}!"
            elif difficulty_sg == 2:
                m 1eua "Будучи на нормальной сложности..."
                m 3eub "У тебя была возможность угадать хотя бы одну."
                m 1hub "Хотелось бы сейчас увидеть твоё лицо, {do_giggle}а-ха-ха~"
            elif difficulty_sg == 3:
                m 1eua "Учитывая, что ты находишься на сложном уровне..."
                m 1sub "Я поражаюсь тому, с какой самоотдачей ты это делаешь."
                m 1hub "Ты действительно {M=отнесся}{F=отнеслась} к этому серьёзно, в смысле специально не {M=справился}{F=справилась}, {do_giggle}э-хе-хе~"
        m 1hubsa "Спасибо, что {M=нашёл}{F=нашла} время поиграть со мной, мне было очень весело!"
        m 3eka "И ещё, отдохни немного, мы играли довольно долго..."
        m 3hub "Ты {M=заслужил}{F=заслужила} это!"
        m 1dub "Я всегда беспокоюсь о твоём здоровье, [mas_get_player_nickname()]."
        m 1dua "И не беспокойся обо мне, я буду ждать тебя."

    window hide
    python:
        cup_speed = 0.5
        current_turn = 0
        correct_answers = 0
    jump close_extraplus
    return

label cheat_sg:
    show monika 1hua at t11
    if renpy.seen_label("check_cheat_sg"):
        jump check_cheat_minigame
    else:
        jump check_cheat_sg
#А как так то?
label check_cheat_sg:
    m 1hub "Я удивлена, что ты {M=модифицировал}{F=модифицировала} эту мини-игру, {do_giggle}а-ха-ха~"
    m 3esb "В конце концов, это прогрессивная игра, в которой нет победителя."
    m 3nub "Но ты можешь поспорить!"
    m 1eua "Цель мини-игр — развлечься на некоторое время."
    m 1etb "Почему бы нам не попробовать снова?"
    m 1eud "Ну или, можем сыграть в другое время, если угодно."
    m 1hua "Не имеет значения, что мы делаем, если ты рядом, то мне всегда будет радостно делать это вместе с тобой."
    m 1hua "{do_giggle}Э-хе-хе~"
    jump close_extraplus
    return
