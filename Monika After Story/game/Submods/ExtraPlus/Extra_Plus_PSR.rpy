#===========================================================================================
# MINIGAME#3
#===========================================================================================
define psr_sprites = ["card_back.png","paper.png","rock.png","scissors.png"]

#====Rock Paper Scissors
label minigame_psr:
    python:
        validate_files(psr_sprites, type=True)
        mas_MUMURaiseShield()
    if moni_wins > 0 or player_wins > 0:
        jump cheat_psr
    show monika 1hua at t21
    show card_back zorder 12:
        xalign 0.7
        yalign 0.1
        yoffset -900
        easein 0.5 yoffset 0
    show e_rock zorder 12:
        xalign 0.5
        yalign 0.7
        yoffset 900
        easein 0.5 yoffset 0
    pause 0.1
    show e_paper zorder 12:
        xalign 0.7
        yalign 0.7
        yoffset 900
        easein 0.5 yoffset 0
    pause 0.2
    show e_scissors zorder 12:
        xalign 0.9
        yalign 0.7
        yoffset 900
        easein 0.5 yoffset 0
    pause 0.3
    hide card_back
    hide e_rock
    hide e_paper
    hide e_scissors
    show screen score_minigame(game="psr")
    call screen PSR_mg
    return

label psr_loop:
    $ rng_global = renpy.random.randint(1,3)
    show card_back zorder 12:
        xalign 0.7
        yalign 0.1
    if your_choice == 1:
        show e_rock zorder 12:
            yoffset -20
            xalign 0.5
            yalign 0.7
        show e_paper zorder 12:
            xalign 0.7
            yalign 0.7
        show e_scissors zorder 12:
            xalign 0.9
            yalign 0.7
        m 1eub "Камень,{w=0.3} Ножницы,{w=0.3} Бумага{w=0.3}!{nw}"
        hide card_back with dissolve
        if rng_global == 1:
            show e_rock zorder 12 as e_rock_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 3hub "Камень не бьёт камень, {do_giggle}а-ха-ха~"
            m 1hua "Ничья."

        elif rng_global == 2:
            show e_paper zorder 12 as e_paper_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1dub "Бумага побеждает камень."
            m 1tub "Прости, [player], ты {M=проиграл}{F=проиграла}!"
            $ moni_wins += 1

        elif rng_global == 3:
            show e_scissors zorder 12 as e_scissors_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1hksdrb "Камень бьёт ножницы."
            m 1hua "Ты {M=победил}{F=победила}, [player]!"
            $ player_wins += 1

    elif your_choice == 2:
        show e_rock zorder 12:
            xalign 0.5
            yalign 0.7
        show e_paper zorder 12:
            yoffset -20
            xalign 0.7
            yalign 0.7
        show e_scissors zorder 12:
            xalign 0.9
            yalign 0.7
        m 1eub "Камень,{w=0.3} Ножницы,{w=0.3} Бумага{w=0.3}!{nw}"
        hide card_back with dissolve
        if rng_global == 1:
            show e_rock zorder 12 as e_rock_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1lkb "Бумага победила камень."
            m 1lub "Победа за тобой, [player]."
            $ player_wins += 1

        elif rng_global == 2:
            show e_paper zorder 12 as e_paper_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1eub "Мы оба выбрали бумагу!"
            m 1tua "Хорошо, ничья, хватит читать мои мысли, [mas_get_player_nickname()]~"
            m 1hub "{do_giggle}А-ха-ха~"

        elif rng_global == 3:
            show e_scissors zorder 12 as e_scissors_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 3eub "Ножницы режут бумагу."
            m 3hua "Извини, [player], победа за мной."
            $ moni_wins += 1

    elif your_choice == 3:
        show e_rock zorder 12:
            xalign 0.5
            yalign 0.7
        show e_paper zorder 12:
            xalign 0.7
            yalign 0.7
        show e_scissors zorder 12:
            yoffset -20
            xalign 0.9
            yalign 0.7
        m 1eub "Камень,{w=0.3} Ножницы,{w=0.3} Бумага{w=0.3}!{nw}"
        hide card_back with dissolve
        if rng_global == 1:
            show e_rock zorder 12 as e_rock_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1mub "Скажи \"Прощай!\" своим ножницам, [player]~"
            m "Ты не победишь меня! {do_giggle}А-ха-ха~"
            $ moni_wins += 1

        elif rng_global == 2:
            show e_paper zorder 12 as e_paper_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 1hssdrb "Ножницы победили бумагу."
            m 1eua "Победа присуждается тебе!"
            $ player_wins += 1

        elif rng_global == 3:
            show e_scissors zorder 12 as e_scissors_1 with dissolve:
                xalign 0.7
                yalign 0.1
            m 2hkb "Двое ножниц равны ничье, [player]!"
            m 2hub "Хотя, так мило, что ты выбрал то же, что и я, {do_giggle}э-хе-хе~"
    show monika 1hua at t21
    $ your_choice = 0
    jump hide_images_psr
    return

label psr_quit:
    $ mas_MUINDropShield()
    hide screen score_minigame
    show card_back zorder 12 as v1:
        xalign 0.7
        yalign 0.1
    show e_rock zorder 12 as r1:
        xalign 0.5
        yalign 0.7
    show e_paper zorder 12 as r2:
        xalign 0.7
        yalign 0.7
    show e_scissors zorder 12 as r3:
        xalign 0.9
        yalign 0.7

    show card_back zorder 12:
        xalign 0.7
        yalign 0.1
        easeout 0.6 yoffset -1300
    show e_rock zorder 12:
        xalign 0.5
        yalign 0.7
        easeout 0.6 yoffset 1300
    hide e_rock as r1
    hide card_back as v1
    pause 0.1

    show e_paper zorder 12:
        xalign 0.7
        yalign 0.7
        easeout 0.6 yoffset 1300
    hide e_paper as r2
    pause 0.2

    show e_scissors zorder 12:
        xalign 0.9
        yalign 0.7
        easeout 0.6 yoffset 1300
    hide e_scissors as r3
    pause 0.3

    hide card_back
    hide e_rock
    hide e_paper
    hide e_scissors
    $ your_choice = 0
    jump psr_result
    return

#===========================================================================================
# TALKING GAME
#===========================================================================================

label psr_result:
    show monika 1hua at t11
    #Tie
    if moni_wins == player_wins:
        if moni_wins == 0 and player_wins == 0:
            m 1etd "Не хочешь играть в \"Камень, Ножницы, Бумага\"?"
            m 1eka "Я надеялась, что мы сыграем..."
            m 3hua "Но не волнуйся, я пойму, если сейчас ты не в настроении для этого."
            m 3hub "Так что, мы можем сыграть позже!"
        else:
            m 1sua "Ах, похоже это ничья."
            m 1tua "Это потому-что влюбленные мыслят одинаково!"
            m 1hub "{do_giggle}Э-хе-хе~"
            m 3hua "Но мы не должны играть в ничью, [player]."
            m 3hub "Посмотрим, кто победит в следующий раз, удачи!"

    #Monika wins
    elif moni_wins > player_wins:
        m 3eub "На этот раз я победила, [player]~"
        m 3eub "Я просто везучая."
        m 3eubsa "Но не расстраивайся, главное чтобы нам обоим было весело."
        m 1hub "В следующий раз ты победишь, я верю в тебя!"
    #Player wins
    elif moni_wins < player_wins:
        m 1hub "Твоя взяла, [player], поздравляю."
        m 1hub "Я так горжусь тобой~"
        m 2tub "Но будь {M=готов}{F=готова}, в следующий раз я прочитаю твои мысли."
        m 2hub "И обязательно выиграю!"
        m 2hua "Так что будь {M=осторожен}{F=осторожна}, когда мы будем играть."
        m 2hua "{do_giggle}Э-хе-хе~"
    python:
        moni_wins = 0
        player_wins = 0
    jump close_extraplus
    return

label cheat_psr:
    show monika 1hua at t11
    if renpy.seen_label("check_cheat_psr"):
        jump check_cheat_minigame
    else:
        jump check_cheat_psr
  #А как такие фокусы делать?      
label check_cheat_psr:
    m 1hkb "Хм-м, честно говоря, я не знаю как реагировать на то, что ты {M=сделал}{F=сделала}."
    if moni_wins == player_wins:
        m 3eua "Даже когда у нас ничья."
    elif moni_wins > player_wins:
        m 3lkb "Ах, так жаль что ты {M=проиграл}{F=проиграла}..."
    elif moni_wins < player_wins:
        m 1hsb "Ты {M=победил}{F=победила}, даже не начиная играть."
    m 1hua "Я не думаю что тебе стоит это делать..."
    m 1dua "И я не вижу необходимости говорить о том, является ли модификация мини-игры неправильной или нет."
    m 2fub "В конце концов, у меня такое чувство, что ты {M=сделал}{F=сделала} это больше из любопытства, чем для того, чтобы получить лёгкую победу."
    m 1etd "Я уверена что ты думаешь, что я злюсь?"
    m 3hub "Конечно нет!"
    m 3dub "Представь себе, злиться из-за того, что ты играешь нечестно в мини-игре."
    m 1eua "Что ж, я надеюсь что ты не сделаешь так же и в других играх."
    m 1hubsb "Так что просто веселись честно и справедливо!"
    jump close_extraplus
    return
