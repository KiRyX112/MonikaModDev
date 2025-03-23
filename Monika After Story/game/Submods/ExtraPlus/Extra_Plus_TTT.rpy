#===========================================================================================
# MINIGAME#2
#===========================================================================================
define ttt_sprite = ["line.png","line_moni.png","line_player.png","notebook.png"]

#====Tic-Tac-Toe
init 10 python:
    def ttt_prep(self, restart = False, *args, **kwargs):
        self.field = [None] * 9
        self.playerTurn = True
        self.state = 0

        if not restart:
            self.score = [0, 0]

            def ttt_check_line(id):
                t_ids = None
                if id == 0:
                    tiles = range(9)
                elif id == 1:
                    t_ids = [0, 4, 8]
                elif id == 2:
                    t_ids = [2, 4, 6]
                elif id < 6:
                    id -= 3
                    t_ids = [id, id + 3, id + 6]
                else:
                    ti = (id-6) * 3
                    t_ids = [ti, ti + 1, ti + 2]

                clt, crt = 0, 0
                for i in t_ids:
                    i = ttt.field[i]
                    if i is True:
                        crt += 1
                    elif i is False:
                        clt += 1
                return clt, crt, t_ids

            def ttt_new_state():
                for i in range(1, 9):
                    clt, crt = ttt_check_line(i)[:2]
                    if clt == 3:
                        return i
                    elif crt == 3:
                        return -i

                for i in ttt.field:
                    if i is None:
                        return 0
                return 9

            def ttt_turn(i):
                if ttt.state == 0 and ttt.field[i] is None:
                    ttt.field[i] = ttt.playerTurn
                    ttt.playerTurn = not ttt.playerTurn

                    fig = "circle"
                    if ttt.playerTurn:
                        fig = "cross"
                    renpy.play("submods/ExtraPlus/submod_assets/sfx/ttt_"+ fig + ".ogg", "sound")

                    ttt.state = ttt_new_state()
                    ttt_check_state()
                    if not ttt.playerTurn:
                        renpy.call_in_new_context("minigame_ttt_m_turn")

            def ttt_check_state():
                if ttt.state != 0:
                        if abs(ttt.state) < 9:
                            renpy.call_in_new_context("minigame_ttt_m_comment", ttt.state < 0)
                            ttt(restart = True, winner = ttt.state < 0)
                        elif ttt.state == -9:
                            renpy.call_in_new_context("minigame_ttt_m_comment", 3)
                            ttt(restart = True, winner = 0)
                        else:
                            renpy.call_in_new_context("minigame_ttt_m_comment", 2)
                            ttt(restart = True)

            def ttt_ai():
                w_lines, l_lines, f_lines = [], [], []

                for i in range(1, 9):
                    clt, crt, line = ttt_check_line(i)
                    if clt == 2 and crt == 0:
                        w_lines.append(line)
                    elif crt == 2 and clt == 0:
                        l_lines.append(line)
                    elif clt > 0 and crt == 0:
                        f_lines.append(line)

                if len(w_lines):
                    line = renpy.random.choice(w_lines)
                    for i in line:
                        if ttt.field[i] is None:
                            return ttt_turn(i)
                if len(l_lines):
                    line = renpy.random.choice(l_lines)
                    for i in line:
                        if ttt.field[i] is None:
                            return ttt_turn(i)
                if len(f_lines):
                    line = renpy.random.choice(f_lines)
                    line = filter(lambda x: ttt.field[x] is None, line)
                    return ttt_turn(renpy.random.choice(line))
                else:
                    line = filter(lambda x: ttt.field[x] is None, range(9))
                    return ttt_turn(renpy.random.choice(line))

            self.new_state, self.check_state = ttt_new_state, ttt_check_state
            self.check_line, self.turn, self.ai = ttt_check_line, ttt_turn, ttt_ai

        elif not kwargs.get("winner") is None:
            w = kwargs['winner']
            self.score[w] += 1

    ttt = minigames("Мини-игра \"Крестики-нолики\".", 'minigame_ttt', ttt_prep)
    minigames_menu.append(ttt)
    
screen minigame_ttt_grid():
    for i in range(2):
        add "line_black" pos (700, 260 + 192*i) zoom 0.8
        add "line_black" pos (600 + 192*i, 80) rotate 90 zoom 0.8

screen minigame_ttt_scr():
    layer "master"
    zorder 50

    python:
        from math import sqrt
        sc = 0.8
        diag_sc = sqrt(sc*sc * 2)

    use minigame_ttt_grid()

    for x in range(3):
        for y in range(3):
            $i, p = ttt.field[3 * y + x], (595 + 192 * (x+1), 188 * (y+1))
            if i is True:
                add "ttt_cross" anchor (0.5, 0.5) pos p
            elif i is False:
                add "ttt_circle" anchor (0.5, 0.5) pos p
            if ttt.state == 0 and ttt.playerTurn:
                button:
                    background None
                    pos p
                    xysize (184, 184)
                    anchor (0.5, 0.5)
                    if i is None:
                        hover_background "ttt_cross_cursor"
                    keyboard_focus i is None
                    keysym 'K_KP' + str(3 * (2-x) + y + 1)
                    action Function(ttt.turn, 3 * y + x)

            if ttt.state != 0:
                $ color = ttt.state > 0 and 'moni' or 'player'
                $ state = abs(ttt.state)
                if state < 3:
                    add "line_"+color anchor (0.5, 0.5) xzoom diag_sc yzoom sc rotate (90 * state - 45) pos (980, 360) # / Fix
                elif state < 6:
                    add "line_"+color anchor (-55, 0.5) zoom sc rotate 90 pos (192 * state - 128, 360) # | Fix
                else:
                    add "line_"+color anchor (0.5, 0.5) zoom sc pos (982, 192 * state - 984) # - Fix

    vbox:
        xpos 0.6
        ypos 0.900

        text "[m_name]: " + str(ttt.score[0])  style "monika_text":
            if not ttt.playerTurn:
                color "#ff4646"
    vbox:
        xpos 0.9
        ypos 0.900

        text "[player]: " + str(ttt.score[1])  style "monika_text":
            if ttt.playerTurn:
                color "#2e97ff"
    vbox:
        xpos 0.05
        yanchor 2.0
        ypos 300

        textbutton _("Я сдаюсь") style "hkb_button" action [Function(ttt.set_state, -9), Function(ttt.check_state)]
        null height 6
        textbutton _("Выйти") style "hkb_button" action [Hide("minigame_ttt_scr"), Jump("minigame_ttt_quit")]

#====Label
label minigame_ttt:
    $ validate_files(ttt_sprite, type=True)
    if not os.path.isfile(renpy.config.basedir + '/game/gui/font/Adventure.ttf'):
        show monika idle at t11
        call screen dialog("Тут как бы нужен шрифт, понимаешь?",ok_action=Jump("close_extraplus"))

    show monika 1hua at t21
    if ttt.score[0] > 0 or ttt.score[1] > 0:
        jump cheat_ttt
    show notebook zorder 12 at animated_book
    pause 0.5
    call screen minigame_ttt_scr() nopredict
    return
    
label minigame_ttt_m_turn:
    show monika 1lua at t21
    python:
        randTime = renpy.random.triangular(0.25, 2)
        renpy.pause(randTime)
        ttt.ai()
    show monika 1lua at t21
    pause 0.25
    return

#===========================================================================================
# TALKING GAME
#===========================================================================================

label minigame_ttt_m_comment(id = 0):
    show monika 1hua at t21
    if id == 0:
        #Monika Wins
        $ rng_global = renpy.random.randint(0, 2)
        if rng_global == 0:
            m 3hua "Кажется, я победила."
            m 3hub "В следующий раз придумай стратегию получше!"
        elif rng_global == 1:
            m 1sub "Три в ряд!"
            m 1huu "Попробуй снова~"
        else:
            m 4nub "Не волнуйся!"
            m 4hua "Я знаю что ты выиграешь в следующий раз~"
        #Player Wins
    elif id == 1:
        $ rng_global = renpy.random.randint(0, 1)
        if rng_global == 0:
            m 1suo "Отлично [player], ты {M=победил}{F=победила}!"
            m 1suo "В следующий раз я точно выиграю, так что будь {M=готов}{F=готова}."
        else:
            m 1hub "Ох, ты {M=победил}{F=победила} на этот раз."
            m 1eub "Но я точно одолею тебя, [mas_get_player_nickname()]!"
        #Tie
    elif id == 2:
        $ rng_global = renpy.random.randint(0, 1)
        if rng_global == 0:
            m 1lkb "Поле полностью заполнено."
            m 1eub "Давай попробуем ещё раз, [mas_get_player_nickname()]!"
        else:
            m 3hua "Всё в порядке, [player]."
            m 3hua "План состоит в том, чтобы мы развлекались вместе~"
            m 3hub "Желаю удачи, [mas_get_player_nickname()]!"
        #Reset
    else:
        $ rng_global = renpy.random.randint(0, 1)
        if rng_global == 0:
            m 1ekd "Ты сдаёшься?"
            m 1eka "Хорошо, я начну заново, но технически я победила!"
        else:
            m 1ekd "Что не так, [player]?"
            m 3ekd "Ты отвлёкся?"
            m 1eka "Ладно, я запущу раунд заново, но сейчас я победила!"
    return

label minigame_ttt_quit:
    hide paper
    hide notebook
    pause 0.3
    show monika 1hua at t11
    if ttt.score[0] == ttt.score[1]:
        if ttt.score[0] == 0 and ttt.score[1] == 0:
            m 3esa "Ох! Ты уже всё?"
            m 3lkb "Я думала что ты {M=хотел}{F=хотела} немного поиграть со мной..."
            m 3lkb "Но всё хорошо! Я понимаю если ты не хочешь играть."
            m 1hua "Я надеюсь что мы сможем сделать это в другой раз."
        else:
            m 1suo "Вау, ничья!"
            m 2huu "Но здесь должен быть победитель."
            m 2hub "Посмотрим, кто победит в следующий раз!"
            m 1hub "{do_giggle}Э-хе-хе~"
    elif ttt.score[0] > ttt.score[1]:
        m 3hua "Я выиграла, [player]~"
        m 3eubsa "Но не расстраивайся, мы же должны оба веселиться."
        m 1eub "Возможно, в следующий раз ты точно победишь меня!"
    elif ttt.score[0] < ttt.score[1]:
        m 1hub "Твоя победа, [player], мои поздравления."
        m 1hub "Я так горда тобой~"
        m 3hua "Я постараюсь победить тебя в следующий раз!"
    jump close_extraplus
    return

label cheat_ttt:
    show monika 1hua at t11
    if renpy.seen_label("check_cheat_ttt"):
        jump check_cheat_minigame
    else:
        jump check_cheat_ttt
label check_cheat_ttt:
    m 1hkb "[player]..."
    m 1etd "Ты читерил с очками?"
    if ttt.score[0] == ttt.score[1]:
        m 1esb "Эх..."
    elif ttt.score[0] > ttt.score[1]:
        m 1lksdla "Я чувствую себя плохо, побеждая ничего не делая... {do_giggle}А-ха-ха~"
    elif ttt.score[0] < ttt.score[1]:
        m 1esd "Ты {M=сделал}{F=сделала} мой счёт больше, чем он есть на самом деле."
    m 1hua "Но не волнуйся, я не очень беспокоюсь."
    m 1tua "По крайней мере я поймала тебя до того, как ты {M=успел}{F=успела} проверить счётчик, {do_giggle}э-хе-хе~"
    m 1hkb "Проблема в том, что мы не можем играть со сломанным счётчиком."
    m 1hkb "Если бы твой счёт сохранился, это не было бы проблемой."
    m 3hua "Но мы оба должны веселиться, [player]."
    m 3hub "Я надеюсь что ты не {M=поменял}{F=поменяла} что-то важное, так что мы сможем дальше играть."
    m 2ltd "Хотя, я думаю, что ты {M=сделал}{F=сделала} это чисто из интереса."
    m 2hua "Я знаю, что ты любишь честную игру!"
    m 2hua "Я доверяю тебе."
    jump close_extraplus
    return
