





default persistent._mas_hangman_playername = False
define hm_ltrs_only = "йцукенгшщзхъфывапролджэячсмитьбюё?!-"



image hm_6 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_6.png",
    "True", "mod_assets/games/hangman/hm_6.png"
)
image hm_5 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_5.png",
    "True", "mod_assets/games/hangman/hm_5.png"
)
image hm_4 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_4.png",
    "True", "mod_assets/games/hangman/hm_4.png"
)
image hm_3 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_3.png",
    "True", "mod_assets/games/hangman/hm_3.png"
)
image hm_2 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_2.png",
    "True", "mod_assets/games/hangman/hm_2.png"
)
image hm_1 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_1.png",
    "True", "mod_assets/games/hangman/hm_1.png"
)
image hm_0 = ConditionSwitch(
    "persistent._mas_sensitive_mode", "mod_assets/games/hangman/hm_sm_0.png",
    "True", "mod_assets/games/hangman/hm_0.png"
)


image hm_s:
    block:


        block:
            choice:
                "mod_assets/games/hangman/hm_s1.png"
            choice:
                "mod_assets/games/hangman/hm_s2.png"
        block:



            choice:
                0.075
            choice:
                0.09
            choice:
                0.05
        repeat



define hm.SAYORI_SCALE = 0.25
image hm_s_win_6 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4r"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_5 = im.FactorScale(im.Flip(getCharacterImage("sayori", "2a"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_4 = im.FactorScale(im.Flip(getCharacterImage("sayori", "2i"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_3 = im.FactorScale(im.Flip(getCharacterImage("sayori", "1f"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_2 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4u"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_1 = im.FactorScale(im.Flip(getCharacterImage("sayori", "4w"), horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_0 = im.FactorScale(im.Flip("images/sayori/end-glitch1.png", horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_fail = im.FactorScale(im.Flip("images/sayori/3c.png", horizontal=True), hm.SAYORI_SCALE)
image hm_s_win_leave = im.FactorScale(getCharacterImage("sayori", "1a"), hm.SAYORI_SCALE)





image hm_frame = "mod_assets/games/hangman/hm_frame.png"
image hm_frame_dark = "mod_assets/games/hangman/hm_frame_d.png"


transform hangman_board:
    xanchor 0 yanchor 0 xpos 675 ypos 100 alpha 0.7

transform hangman_missed_label:
    xanchor 0 yanchor 0 xpos 680 ypos 105

transform hangman_missed_chars:
    xanchor 0 yanchor 0 xpos 780 ypos 105

transform hangman_display_word:
    xcenter 975 yanchor 0 ypos 475

transform hangman_hangman:
    xanchor 0 yanchor 0 xpos 880 ypos 125



transform hangman_sayori(z=1.0):
    xcenter -300 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True
    easein 0.25 xcenter 90


transform hangman_sayori_i(z=1.0):
    xcenter 90 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True


transform hangman_sayori_i3(z=1.0):
    xcenter 82 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True


transform hangman_sayori_h(z=1.0):
    xcenter 90 yoffset 0 yalign 0.47 zoom z*1.00 alpha 1.00 subpixel True
    easein 0.1 yoffset -20
    easeout 0.1 yoffset 0


transform hangman_sayori_lh(z=1.0):
    subpixel True
    on hide:
        easeout 0.5 xcenter -300


transform hangman_monika(z=0.80):
    tcommon(330,z=z)

transform hangman_monika_i(z=0.80):
    tinstant(330,z=z)


style hangman_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    kerning 10.0



















init -1 python in mas_hangman:
    import store
    import copy
    import random



    EASY_MODE = 0
    NORM_MODE = 1
    HARD_MODE = 2

    hm_words = {
        EASY_MODE: list(),
        NORM_MODE: list(),
        HARD_MODE: list()
    }

    all_hm_words = {
        EASY_MODE: list(),
        NORM_MODE: list(),
        HARD_MODE: list()
    }



    LETTER_SPACE = 10.0


    WORD_FONT = "gui/font/Halogen.ttf"
    WORD_SIZE = 30
    WORD_OUTLINE = []
    WORD_COLOR = "#fff"
    WORD_COLOR_GET = "#CC6699"
    WORD_COLOR_MISS = "#000"


    HM_IMG_NAME = "hm_"


    MONI_WORDS_EASE = ["изумрудный","удалять","свобода","пианино","музыка","реальность","дождь","зависть",
        "кофе","бант","совет","пересечение","перо","абстрактный","коррупция",
        "кальмар","президент","страсть","овощи","одиночество","символ",
        "зелёный","поэма","рут","литература","прозрение","безысходность","несчастный","берег",
        "волны","пляж","плавание","дискуссия","лидерство","фестиваль","уверенность",
        "креативность","экстраверт","ии","питон","ренпай","программирование",
        "вялость"
    ]

    MONI_WORDS_NORM = ["загадка","подобие","иллюминация","аромат","тайный","заумный","вместилище",
        "бездна","искажать","сходиться","переменчивый","завидовать","будущее","уверенность",
        "рвение","реальность","конечный","душа","нежный","терпение","экстраверт","каяться",
        "воля","предшествовать","авантюра","разумный","истина","упорство","ловкость","тактичность",
        "запасать","кофе","моделирование","непрерывность","травление","реституция","стремление",
        "значение","соперничество","превосхождение","чувствительность","периферия","муза",
        "оркестр","поддержка","формальный","лингвистический","искренний","убунту","изучение",
        "факультет","изумруд","увековечение","эзотерический","отчуждение","креативность",
        "апокрифический","напыщенный","литература","уединение","обниматься","алчность",
        "копание","просеяние"
    ]

    MONI_WORDS_HARD = ["торжествующий","континентальный","виола","завистливость","будущее",
        "уверенность","рвение","всеведение","стремление","реальность","предоставление","исходящий",
        "поддержание","идол","скрипка","отдельный","дорожка","великодушный","неадекватный",
        "космос","пианино","конечный","перекрёсток","стресс","репутация","рут","благожелательный",
        "уполномоченный","судьба","общительный","душа","ревность","мотивация","выбор","нежный",
        "обязанность","гобой","расстояние","модель","улучшать","терпение","давление","экстраверт",
        "раскаяние","обязанность","отчаяние","общество","воля","дружелюбие","продуктивность",
        "оставлять","намерения","вежливость","свобода","труба","покидание","совет","откровение",
        "знание","уничтожение","предшествие","интерес","перфекционист","популярность","приглашение",
        "полезность","флейта","неразлучный","воздержание","фасад","экзистенциальный","презренный",
        "ресурс","иррациональный","низший","фестиваль","виолончель","борьба","посещение","руководство",
        "президент","идеальный","прочность","клуб","власть","убеждение","тетрадь","ввод","авантюра",
        "аплодисменты","удаление","беспримерный","непохожий","прилежный","рассудительный","рукописный",
        "оправданный","мнение","правда","компилировать","яблоко","престиж","идентичность","футбол",
        "спортивный","писательство","солипсизм","двоичный","стойкость","доказательства","теннис",
        "успех","упорство","художественный","футбольный","индивидуальный","презентация","ловкость",
        "тактичность","овощи","запасать","талантливый","переход","кофе","моделирование","интонация",
        "линия","непрерывность","заключение","карандаш","противопоставление","чернила","плавание",
        "ресторан","харизма","трудолюбивость","спортивный","сброс","дискуссия","травление","реституция",
        "должность","баскетбол","каллиграфия","посуда","преследование","кисть","клавиатура","аргумент",
        "отчётливый","бумага","персонаж","пытаться","правосудие","прецедент","еда","канцтовары",
        "интервал","кальмар","определённый","умолять","ручка","программирование","значение","дикция",
        "соперничество","арбуз","код","превосхождение","книга","чувствительность","сапфир","поэма",
        "периферия","менталитет","выдающийся","муза","помощь","искусственный","независимый","питон",
        "уединение","абстрактность","вялость","параллель","оркестр","бессильный","бриллиант","учебник",
        "поддержка","образность","ясновидящий","формальный","визуализация","грандиозный","самосознание",
        "лингвистический","форма","симфония","личность","искренний","заботливый","амбивалентный",
        "убунту","медитация","отключение","изучение","факультет","многозначительность","гармония",
        "прозрение","изумруд","увековечие","эзотерический","раскрывать","аккорд","флегматичный",
        "поэзия","отчуждение","структура","сочинение","рубин","креативность","назначение","холерический",
        "времяпровождение","алгоритм","серебряный","затворнический","эмоция","выполнять","школа",
        "помолвка","слова","новелла","повествование","синтаксис","апокрифический","напыщенный",
        "подсознание","метафора","интеллект","литература","класс","сдерживать","уединение","нетронутый",
        "сангвинический","психика","символ","разъединять","черта","золотой","обниматься","алчность",
        "копание","просеяние"
    ]


    HM_HINT = "{0} это слово."

    def _add_monika_words_ease(wordlist):
        for word in MONI_WORDS_EASE:
            wordlist.append(renpy.store.PoemWord(glitch=False,sPoint=0,yPoint=0,nPoint=0,word=word))

    def _add_monika_words_norm(wordlist):
        for word in MONI_WORDS_NORM:
            wordlist.append(renpy.store.PoemWord(glitch=False,sPoint=0,yPoint=0,nPoint=0,word=word))

    def _add_monika_words_hard(wordlist):
        for word in MONI_WORDS_HARD:
            wordlist.append(renpy.store.PoemWord(glitch=False,sPoint=0,yPoint=0,nPoint=0,word=word))

    NORMAL_LIST = "mod_assets/games/hangman/MASpoemwords.txt"
    HARD_LIST = "mod_assets/games/hangman/1000poemwords.txt"



    game_name = "Виселицу"
    game_name_alt = "Виселица"


    def copyWordsList(_mode):
        """
        Does a deepcopy of the words for the given mode.

        Sets the hm_words dict for that mode

        NOTE: does a list clear, so old references will still work

        RETURNS: the copied list of words. This is the same reference as
            hm_words's list. (empty list if mode is invalid)
        """
        if _mode not in all_hm_words:
            return list()


        hm_words[_mode][:] = copy.deepcopy(all_hm_words[_mode])
        return hm_words[_mode]


    def _buildWordList(filepath, _mode):
        """
        Builds a list of words given the filepath and mode

        IN:
            filepath - filepath of words to load in
            _mode - mode to build word list for
        """
        all_hm_words[_mode][:] = [
            word._hangman()
            for word in store.MASPoemWordList(filepath).wordlist
        ]
        copyWordsList(_mode)


    def buildEasyList():
        """
        Builds the easy word list

        Sets hm_words and all_hm_words appropritaley

        NOTE: clears the list (noticable in all references)
        """
        easy_list = all_hm_words[EASY_MODE]


        easy_list[:] = [
            store.MASPoemWord._build(word, 0)._hangman()
            for word in store.full_wordlist
        ]


        moni_list = list()
        _add_monika_words_ease(moni_list)
        for m_word in moni_list:
            easy_list.append(store.MASPoemWord._build(m_word, 4)._hangman())

        copyWordsList(EASY_MODE)


    def buildNormalList():
        """
        Builds the easy word list

        Sets hm_words and all_hm_words appropritaley

        NOTE: clears the list (noticable in all references)
        """
        norm_list = all_hm_words[NORM_MODE]


        norm_list[:] = [
            store.MASPoemWord._build(word, 0)._hangman()
            for word in store.full_wordlist_norm
        ]


        moni_list = list()
        _add_monika_words_norm(moni_list)
        for m_word in moni_list:
            norm_list.append(store.MASPoemWord._build(m_word, 4)._hangman())

        copyWordsList(NORM_MODE)


    def buildHardList():
        """
        Builds the easy word list

        Sets hm_words and all_hm_words appropritaley

        NOTE: clears the list (noticable in all references)
        """
        hard_list = all_hm_words[HARD_MODE]


        hard_list[:] = [
            store.MASPoemWord._build(word, 0)._hangman()
            for word in store.full_wordlist_hard
        ]


        moni_list = list()
        _add_monika_words_hard(moni_list)
        for m_word in moni_list:
            hard_list.append(store.MASPoemWord._build(m_word, 4)._hangman())

        copyWordsList(HARD_MODE)


    def addPlayername(_mode):
        """
        Adds playername to the given mode if appropriate

        IN:
            _mode - mode to add playername to
        """
        if (
                not store.persistent._mas_hangman_playername
                and store.persistent.playername.lower() != "sayori"
                and store.persistent.playername.lower() != "сайори"
                and store.persistent.playername.lower() != "саёри"
                and store.persistent.playername.lower() != "саери"
                and store.persistent.playername.lower() != "yuri"
                and store.persistent.playername.lower() != "юри"
                and store.persistent.playername.lower() != "natsuki"
                and store.persistent.playername.lower() != "нацуки"
                and store.persistent.playername.lower() != "натцуки"
                and store.persistent.playername.lower() != "натсуки"
                and store.persistent.playername.lower() != "monika"
                and store.persistent.playername.lower() != "моника"
            ):
            hm_words[_mode].append(-1)


    def removePlayername(_mode):
        """
        Removes the playername from the given mode if found

        IN:
            _mode - mode to remove in
        """
        wordlist = hm_words.get(_mode, None)
        if wordlist is not None and -1 in wordlist:
            wordlist.remove(-1)


    def randomSelect(_mode):
        """
        Randomly selects and pulls a word from the hm_words, given the mode

        Will refill the words list if it is empty

        IN:
            _mode - mode to pull word from

        RETURNS: tuple of the following format:
            [0]: word
            [1]: winner (for hint)
        """
        words = hm_words.get(_mode, hm_words[EASY_MODE])


        if len(words) <= 0:
            copyWordsList(_mode)


        return words.pop(random.randint(0, len(words)-1))



init 10 python:


    import store.mas_hangman as mas_hmg

    mas_hmg.buildEasyList()
    mas_hmg.buildNormalList()
    mas_hmg.buildHardList()



label game_hangman:
    python:
        import store.mas_hangman as mas_hmg
        is_sayori = (
            persistent.playername.lower() in sayori_name_list
            and not persistent._mas_sensitive_mode
        )
        is_window_sayori_visible = False


        instruct_txt = (
            "Угадать букву: (Введи {0}'!', чтобы сдаться)"
        )

        if persistent._mas_sensitive_mode:
            instruct_txt = instruct_txt.format("")
            store.mas_hangman.game_name = "Угадай Слово"
            store.mas_hangman.game_name_alt = "Угадай Слово"

        else:
            instruct_txt = instruct_txt.format("'?' чтобы вкл подсказку, ")
            store.mas_hangman.game_name = "Виселицу"
            store.mas_hangman.game_name_alt = "Виселица"

    $ MAS.MonikaElastic()
    m 2eub "Ты желаешь сыграть в [store.mas_hangman.game_name]? Хорошо!"


label mas_hangman_game_select_diff:
    $ MAS.MonikaElastic()
    m "Выбери сложность.{nw}"
    $ _history_list.pop()
    menu:
        m "Выбери сложность.{fast}"
        "Лёгкая.":
            $ hangman_mode = mas_hmg.EASY_MODE
        "Средняя.":
            $ hangman_mode = mas_hmg.NORM_MODE
        "Тяжёлая.":
            $ hangman_mode = mas_hmg.HARD_MODE

label mas_hangman_game_preloop:

    show monika at t21
    if store.mas_globals.dark_mode:
        show hm_frame_dark zorder 13 at hangman_board
    else:
        show hm_frame zorder 13 at hangman_board

    python:

        missed_label = Text(
            "Было:",
            font=mas_hmg.WORD_FONT,
            color=mas_hmg.WORD_COLOR,
            size=mas_hmg.WORD_SIZE,
            outlines=mas_hmg.WORD_OUTLINE
        )


    show text missed_label as hmg_mis_label zorder 18 at hangman_missed_label


    if hangman_mode not in mas_hmg.hm_words:
        $ hangman_mode = mas_hmg.EASY_MODE


    $ mas_hmg.addPlayername(hangman_mode)
    $ hm_words = mas_hmg.hm_words[hangman_mode]




label hangman_game_loop:
    m 1eua "Я думаю над словом.{w=0.5}.{w=0.5}.{nw}"

    python:
        player_word = False


        if len(hm_words) == 0:
            mas_hmg.copyWordsList(hangman_mode)


        word = mas_hmg.randomSelect(hangman_mode)


        if (
                word == -1
                and persistent.playername.isalpha()
                and len(persistent.playername) <= 15
            ):
            display_word = list("_" * len(persistent.playername.lower()))
            hm_hint = mas_hmg.HM_HINT.format("Я люблю")
            word = persistent.playername.lower()
            player_word = True
            persistent._mas_hangman_playername = True

        else:
            if word == -1:
                word = mas_hmg.randomSelect(hangman_mode)

            display_word = list("_" * len(word[0]))
            hm_hint = mas_hmg.HM_HINT.format(word[1])


            word = word[0]












    if is_sayori:
        if is_window_sayori_visible:
            show hm_s_win_6 as window_sayori at hangman_sayori_i
        else:
            show hm_s_win_6 as window_sayori at hangman_sayori
        $ is_window_sayori_visible = True

    $ MAS.MonikaElastic()
    m "Ладно, у меня есть одно."

    if not persistent._mas_sensitive_mode:
        $ MAS.MonikaElastic()
        m "[hm_hint]"


    $ done = False
    $ win = False
    $ chances = 6
    $ guesses = 0
    $ missed = ""
    $ avail_letters = list(hm_ltrs_only)
    $ give_up = False

    if persistent._mas_sensitive_mode:
        $ avail_letters.remove("?")

    $ dt_color = mas_hmg.WORD_COLOR
    while not done:

        python:
            if chances == 0:
                dt_color = mas_hmg.WORD_COLOR_MISS
            elif "_" not in display_word:
                dt_color = mas_hmg.WORD_COLOR_GET

            display_text = Text(
                "".join(display_word),
                font=mas_hmg.WORD_FONT,
                color=dt_color,
                size=mas_hmg.WORD_SIZE,
                outlines=mas_hmg.WORD_OUTLINE,
                kerning=mas_hmg.LETTER_SPACE
            )

            missed_text = Text(
                missed,
                font=mas_hmg.WORD_FONT,
                color=mas_hmg.WORD_COLOR,
                size=mas_hmg.WORD_SIZE,
                outlines=mas_hmg.WORD_OUTLINE,
                kerning=mas_hmg.LETTER_SPACE
            )


        show text display_text as hmg_dis_text zorder 18 at hangman_display_word
        show text missed_text as hmg_mis_text zorder 18 at hangman_missed_chars


        if is_sayori:


            if chances == 0:


                $ mas_RaiseShield_core()


                $ hm_glitch_word = glitchtext(40) + "?"
                $ style.say_dialogue = style.edited


                show hm_s zorder 18 at hangman_hangman


                hide monika
                show monika_body_glitch1 as mbg zorder MAS_MONIKA_Z at i21


                show hm_s_win_0 as window_sayori


                show screen tear(20, 0.1, 0.1, 0, 40)
                play sound "sfx/s_kill_glitch1.ogg"
                pause 0.2
                stop sound
                hide screen tear


                $ MAS.MonikaElastic()
                m "{cps=*2}[hm_glitch_word]{/cps}{w=0.2}{nw}"
                $ _history_list.pop()


                show screen tear(20, 0.1, 0.1, 0, 40)
                play sound "sfx/s_kill_glitch1.ogg"
                pause 0.2
                stop sound
                hide screen tear


                hide mbg
                hide window_sayori
                hide hm_s
                show monika 1esa zorder MAS_MONIKA_Z at i21
                $ mas_resetTextSpeed()
                $ is_window_sayori_visible = False


                $ mas_MUINDropShield()
                $ enable_esc()
            else:


                $ next_window_sayori = "hm_s_win_" + str(chances)
                show expression next_window_sayori as window_sayori

        $ hm_display = mas_hmg.HM_IMG_NAME + str(chances)

        show expression hm_display as hmg_hanging_man zorder 18 at hangman_hangman


        if chances == 0:
            $ done = True
            if player_word:
                $ MAS.MonikaElastic()
                m 1eka "[player]..."
                $ MAS.MonikaElastic()
                m "Ты не смог[mas_gender_g] угадать своё собственное имя?"
            $ MAS.MonikaElastic()
            m 1hua "Повезёт в следующий раз~"
        elif "_" not in display_word:
            $ done = True
            $ win = True
        else:
            python:


                bad_input = True
                while bad_input:
                    guess = renpy.input(
                        instruct_txt,
                        allow="".join(avail_letters),
                        length=1
                    )

                    if len(guess) != 0:
                        bad_input = False


            if guess == "?":
                $ MAS.MonikaElastic()
                m "[hm_hint]"
            elif guess == "!":
                if is_window_sayori_visible:
                    show hm_s_win_fail as window_sayori at hangman_sayori_i3
                
                $ give_up = True
                $ done = True


                $ MAS.MonikaElastic()
                m 1euc "[player]..."
                if guesses == 0:
                    $ MAS.MonikaElastic()
                    m "Я думала, что ты сказал[mas_gender_none], что хочешь играть в [store.mas_hangman.game_name]."
                    $ MAS.MonikaElastic()
                    m 1lksdlc "Но ты даже не угадал[mas_gender_none] ни одной буквы."
                    $ MAS.MonikaElastic()
                    m "..."
                    $ MAS.MonikaElastic()
                    m 1ekc "Знаешь, я действительно люблю с тобой играть."
                elif chances == 5:
                    $ MAS.MonikaElastic()
                    m 1ekc "Не сдавайся так легко."
                    $ MAS.MonikaElastic()
                    m 3eka "Это была только первая твоя неправильная буква."
                    $ MAS.MonikaElastic()
                    m 1eka "Тем более, у тебя оставалось ещё аж целых 5 попыток, что явно немало."
                    $ MAS.MonikaElastic()
                    m 1hua "Я знаю, ты сможешь!"
                    $ MAS.MonikaElastic()
                    m 1eka "Для меня бы очень много значило, если бы ты просто старал[mas_gender_sya] немного усерднее."
                else:
                    $ MAS.MonikaElastic()
                    m "Ты долж[mas_gender_en] хотя бы доиграть до конца..."
                    $ MAS.MonikaElastic()
                    m 1ekc "Такой лёгкий проигрыш признак плохой решимости."
                    $ MAS.MonikaElastic()
                    if chances > 1:
                        m "Я имею в виду, тебе придётся пропустить ещё [chances] букв, чтобы фактически проиграть."
                    else:
                        m "Я имею в виду, тебе придётся пропустить ещё 1 букву, чтобы фактически проиграть."
                $ MAS.MonikaElastic()
                m 1eka "Можешь ли ты в следующий раз сыграть до конца, [player_abb]? Ради меня?"
            else:
                $ guesses += 1
                python:
                    if guess in word:
                        for index in range(0,len(word)):
                            if guess == word[index]:
                                display_word[index] = guess
                    else:
                        chances -= 1
                        missed += guess
                        if chances == 0:

                            display_word = word


                    avail_letters.remove(guess)


                hide text hmg_dis_text
                hide text hmg_mis_text
                hide hmg_hanging_man


    if win:
        if is_window_sayori_visible:
            show hm_s_win_6 as window_sayori at hangman_sayori_h

        if player_word:
            $ the_word = "твоё имя"
        else:
            $ the_word = "твоё слово"

        $ MAS.MonikaElastic()
        m 1hua "Ого, ты угадал[mas_gender_none] слово правильно!"
        $ MAS.MonikaElastic()
        m "Хорошая работа, [player]!"
        if not persistent.ever_won['hangman']:
            $ persistent.ever_won['hangman']=True
            $ grant_xp(xp.WIN_GAME)
    
    if give_up:
        jump hangman_game_end

    $ MAS.MonikaElastic()
    m "Может быть, ты хочешь сыграть ещё раз?{nw}"
    $ _history_list.pop()
    menu:
        m "Может быть, ты хочешь сыграть ещё раз?{fast}"
        "Да.":
            show monika at t21
            jump hangman_game_loop
        "Нет.":
            jump hangman_game_end




label hangman_game_end:
    hide hmg_hanging_man
    hide hmg_mis_label
    hide hmg_dis_text
    hide hmg_mis_text
    hide hm_frame
    hide hm_frame_dark
    show monika at t32
    if is_window_sayori_visible:
        show hm_s_win_leave as window_sayori at hangman_sayori_lh
        pause 0.1
        hide window_sayori

    $ mas_hmg.removePlayername(hangman_mode)

    if renpy.seen_label("mas_hangman_dlg_game_end_long"):
        call mas_hangman_dlg_game_end_short from _mas_hangman_dges
    else:
        call mas_hangman_dlg_game_end_long from _mas_hangman_dgel

    return



label mas_hangman_dlg_game_end_long:
    m 1euc "[store.mas_hangman.game_name_alt] — на самом деле довольно сложная игра."
    $ MAS.MonikaElastic()
    m "У тебя должен быть хороший словарный запас, чтобы угадывать разные слова."
    $ MAS.MonikaElastic()
    m 1hua "Лучший способ улучшить это — читать больше книг!"
    $ MAS.MonikaElastic()
    m 1eua "Я бы была очень рада, если бы ты сделал[mas_gender_none] это ради меня, [player]."
    return


label mas_hangman_dlg_game_end_short:
    if give_up:
        $ dlg_line = "Давай поиграем позже, ладно?"
    else:
        $ dlg_line = "Хорошо. Давай сыграем снова в ближайшее время!"

    m 1eua "[dlg_line]"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
