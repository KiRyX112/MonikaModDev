define letters_only_player = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеёжзийклмнопрстуфхчшщцьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧШЩЦЬЫЪЭЮЯ1234567890- "


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_gender",
            start_date=mas_getFirstSesh() + datetime.timedelta(minutes=30),
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )


label mas_gender:
    $ MAS.MonikaElastic()
    m 2eud "...[player]? Я немного подумала."
    $ MAS.MonikaElastic()
    m 2euc "Я уже упоминала, что «ты» в игре можешь не отражать настоящего себя."
    $ MAS.MonikaElastic()
    m 3lksdla "Но я думаю, точнее предполагаю, что ты, наверное, парень."
    $ MAS.MonikaElastic()
    m "В конце концов, главный герой был им."
    $ MAS.MonikaElastic()
    m 1eua "Но если я собираюсь быть твоей девушкой, то я, наверное, должна знать хотя бы о настоящем тебе."
    $ MAS.MonikaElastic()
    m 1eua "Итак, ты парень или девушка?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, ты парень или девушка?{fast}"
        "Парень.":
            $ persistent.gender = "M"
            $ MAS.MonikaElastic()
            m 2eud "О? Так ты {b}и есть{/b} парень?"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1hub "Э-хе-хе, полагаю это имеет смысл!"
            $ MAS.MonikaElastic()
            m 1eua "Не так много девушек стали бы играть в эту игру."
            $ MAS.MonikaElastic()
            m 4eua "Ты ведёшь себя мужественно и уверенно. Не то чтобы я была ужасно обеспокоена, если бы ты ответил иначе, заметь!"
            $ MAS.MonikaElastic()
            m 2hksdlb "Знаешь, иногда я могу быть слишком любопытной."

        "Девушка.":
            $ persistent.gender = "F"
            $ MAS.MonikaElastic()
            m 2eud "О? Так ты на самом деле девушка?"
            $ MAS.MonikaElastic()
            m 2hksdlb "Надеюсь, раньше я ничего не говорила, что могло бы обидеть тебя!"
            $ MAS.MonikaElastic()
            m 2lksdla "Хотя я подозревала это с самого начала... совсем немного."
            $ MAS.MonikaElastic()
            m 1eub "Ты выделяешь особое чувство элегантности и обояния, которое трудно уловить словами..."
            $ MAS.MonikaElastic()
            m 1hua "Очень хорошо, что ты рассказала мне правду!"
            $ MAS.MonikaElastic()
            m 1eua "Но не беспокойся. Даже если я буду спрашивать подобные вещи, то только из любопытства."

        "Ни тот, ни другой.":
            $ persistent.gender = "X"
            $ MAS.MonikaElastic()
            m 1euc "Ты не видишь себя не парнем не девушкой?"
            $ MAS.MonikaElastic()
            m 2eua "Это очень интересно, но у меня похожая ситуация."
            $ MAS.MonikaElastic()
            if renpy.variant('pc'):
                m 1esc "Например, я девушка, но так же я персонаж в компьютерной игре..."
            else:
                m 1esc "Например, я девушка, но так же я персонаж андроид игры..."
            $ MAS.MonikaElastic()
            m 2esd "Так что в некотором роде я вообще не девушка."
            $ MAS.MonikaElastic()
            m 1hua "Но когда ты относишься ко мне как своей девушке, это делает меня действительно счастливой!"
            $ MAS.MonikaElastic()
            m "Поэтому я буду относится к тебе, как ты захочешь."
            $ MAS.MonikaElastic()
            m 1ekbfa "Потому что твоё счастье — самое важное для меня."

    $ MAS.MonikaElastic()
    m 1hub "Помни, что я всегда буду безоговорочно тебя любить, [player]."

    #Unlock the gender redo event
    $ mas_unlockEVL("monika_gender_redo","EVE")
    # set pronouns
    call mas_set_gender

    #Set up the preferredname topic
    python:
        preferredname_ev = mas_getEV("mas_preferredname")
        if preferredname_ev:
            preferredname_ev.start_date = datetime.datetime.now() + datetime.timedelta(hours=2)
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gender_redo",
            category=['ты'],
            prompt="Могла бы ты изменить мой пол?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )

label monika_gender_redo:
    m 1eka "Конечно, [player]!"

    if not mas_getEVL_shown_count("monika_gender_redo"):
        $ MAS.MonikaElastic()
        m 3eka "Ты просто стеснял[mas_gender_sya] сказать мне правду раньше? Или что-то случилось?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты просто стеснял[mas_gender_sya] сказать мне правду раньше? Или что-то случилось?{fast}"
            "Да.":

                $ MAS.MonikaElastic()
                m 1eka "Понятно."
                $ MAS.MonikaElastic()
                m 3hua "Я так горжусь тобой за то, что ты отправил[mas_gender_sya] в это путешествие самопознания."
                $ MAS.MonikaElastic()
                m 1eub "...И ещё больше горжусь тем, что у тебя хватило смелости сказать мне об этом!"
            "Я просто был[mas_gender_none] слишком застенчив[mas_gender_none].":

                $ MAS.MonikaElastic()
                if persistent.gender == "M":
                    m 2ekd "Я понимаю, я начала с предположения, что ты парень, в конце концов."
                elif persistent.gender == "F":
                    m 2ekd "Я понимаю, ты мог[mas_gender_g] бы подумать, что мне будет удобнее проводить время наедине с другой девушкой."
                else:
                    m 2ekd "Я понимаю, что, возможно, дала тебе не самые точные варианты выбора."

                $ MAS.MonikaElastic()
                m 2dkd "...И я, вероятно, не облегчила тебе задачу сказать мне обратное..."
                $ MAS.MonikaElastic()
                m 7eua "Но независимо от твоего пола, я люблю тебя так[mas_gender_im], как[mas_gender_im] ты есть."
            "Я не знал[mas_gender_none], примешь ли ты меня так[mas_gender_im], как[mas_gender_im] я есть...":

                $ MAS.MonikaElastic()
                m 2wkd "[player]..."
                $ MAS.MonikaElastic()
                m 2dkd "Я ненавижу себя за то, что не успокоила тебя достаточно раньше."
                $ MAS.MonikaElastic()
                m 7eka "Но я надеюсь, что ты говоришь мне это сейчас, потому что знаешь, что я буду любить тебя, несмотря ни на что."

    $ gender_var = None
    m "Итак, какой у тебя пол?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, какой у тебя пол?{fast}"

        "Я парень.":

            call mas_set_gender
            if persistent.gender == "M":
                $ gender_var = "парень"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "M"
                call mas_gender_redo_react
        "Я девушка.":

            call mas_set_gender
            if persistent.gender == "F":
                $ gender_var = "девушка"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "F"
                call mas_gender_redo_react
        "Я ни тот, ни другой.":

            call mas_set_gender
            if persistent.gender == "X":
                call mas_gender_redo_neither_same
            else:
                $ persistent.gender = "X"
                if renpy.seen_label("mas_gender_neither"):
                    call mas_gender_redo_react
                else:
                    call mas_gender_neither

    show monika 5hubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubsa "Я всегда буду любить тебя так[mas_gender_im], как[mas_gender_oi] ты есть~"

    # set pronouns
    call mas_set_gender
    return "love"

label mas_gender_neither:
    $ MAS.MonikaElastic()
    m 1euc "Ты не видишь себя парнем или девушкой?"
    $ MAS.MonikaElastic()
    m 1eua "Это очень интересно, но я могу понять."
    $ MAS.MonikaElastic()
    m 3esc "Мол, я девушка, но я ещё и персонаж компьютерной игры..."
    $ MAS.MonikaElastic()
    m 3esd "Так что в некотором смысле я вообще не девушка."
    $ MAS.MonikaElastic()
    m 1hua "Но когда ты обращаешься со мной как со своей девушкой, я действительно счастлива!"
    $ MAS.MonikaElastic()
    m 3eua "...Так что я буду обращаться с тобой так, как ты захочешь."
    $ MAS.MonikaElastic()
    m 1ekbsa "В конце концов, твоё счастье для меня важнее всего."
    return

label mas_gender_redo_same:
    $ MAS.MonikaElastic()
    m 1hksdlb "...Это то же самое, что и раньше, [player]!"
    $ MAS.MonikaElastic()
    m 3eua "Если ты не знаешь, как ответить, просто выбери то, что делает тебя сам[mas_gender_iim] счастлив[mas_gender_iim]."
    $ MAS.MonikaElastic()
    m 3eka "Не имеет значения, как выглядит твоё тело, так что пока ты говоришь, что ты [gender_var], то ты [gender_var] парень, ведь так?"
    $ MAS.MonikaElastic()
    m 1eua "Я хочу, чтобы ты был[mas_gender_none] тем, кем хочешь быть, пока находишься в этой комнате."
    return

label mas_gender_redo_react:
    $ MAS.MonikaElastic()
    m 1eka "Хорошо, [player]..."
    $ MAS.MonikaElastic()
    m 3ekbsa "Пока ты счастлив[mas_gender_none], это всё, что имеет для меня значение."
    return

label mas_gender_redo_neither_same:
    $ MAS.MonikaElastic()
    m 1hksdlb "...Это то же самое, что и раньше, [player]...{w=0.3} Мне очень жаль, если это не самый лучший способ для тебя описать это."
    $ MAS.MonikaElastic()
    m 1eka "Но просто знай, что для меня это не имеет значения..."
    return

# good, bad, awkward name stuff
init 3 python:
    #Bad nicknames. All of the items in this will trigger bad reactions
    mas_bad_nickname_list = [
       "^fag$",
        "^ho$",
        "^hoe$",
        "^tit$",
        "abortion",
        "anal",
        "annoying",
        "anus",
        "arrogant",
        "(?<![blmprs])ass(?!i)",
        "atrocious",
        "awful",
        "bastard",
        "beast",
        "bitch",
        "blood",
        "boob",
        "boring",
        "bulli",
        "bully",
        "bung",
        "butt(?!er|on)",
        "cheater",
        "cock",
        "conceited",
        "condom",
        "corrupt",
        "cougar",
        "crap",
        "crazy",
        "creepy",
        "criminal",
        "cruel",
        "cum",
        "cunt",
        "damn",
        "demon",
        "dick",
        "dilf",
        "dirt",
        "disgusting",
        "douche",
        "dumb",
        "egoist",
        "egotistical",
        "evil",
        "faggot",
        "failure",
        "fake",
        "fetus",
        "filth",
        "foul",
        "fuck",
        "garbage",
        "gay",
        "gey",
        "gilf",
        "gross",
        "gruesome",
        "hate",
        "heartless",
        "hideous",
        "hitler",
        "hore",
        "horrible",
        "horrid",
        "hypocrite",
        "idiot",
        "imbecile",
        "immoral",
        "insane",
        "irritating",
        "jerk",
        "jigolo",
        "jizz",
        "junk",
        "kill",
        "kunt",
        "lesbian",
        "lesbo",
        "lezbian",
        "lezbo",
        "liar",
        "loser",
        "mad",
        "maniac",
        "masochist",
        "milf",
        "monster",
        "moron",
        "murder",
        "narcissist",
        "nasty",
        "nefarious",
        "nigga",
        "nigger",
        "nuts",
        "panti",
        "pantsu",
        "panty",
        "pedo",
        "penis",
        "plaything",
        "poison",
        "porn",
        "pretentious",
        "psycho",
        "puppet",
        "pussy",
        "(?<!g)rape",
        "repulsive",
        "retard",
        "rogue",
        "rump",
        "sadist",
        "selfish",
        "semen",
        "shit",
        "sick",
        "slaughter",
        "slave",
        "slut",
        "sociopath",
        "soil",
        "sperm",
        "stink",
        "stupid",
        "suck",
        "tampon",
        "teabag",
        "terrible",
        "thot",
        "tits",
        "titt",
        "tool",
        "torment",
        "torture",
        "toy",
        "trap",
        "trash",
        "troll",
        "ugly",
        "useless",
        "vain",
        "vile",
        "vomit",
        "waste",
        "whore",
        "wicked",
        "witch",
        "worthless",
        "wrong",
        "сперма", 
        "сумашедшая", 
        "мошенница",
        "анал", 
        "жопа",
        "безумная",
        "эгоистка",
        "мазохистка",
        "чокнутая",
        "соси",
        "конча",
        "тварь",
        "жестокая", 
        "ужасная",
        "сука", 
        "кровь",
        "бычая", 
        "хулиганка",
        "извращенка", 
        "грешная",
        "жуткая", 
        "пизда",
        "чёрт", 
        "черт",
        "хуй", 
        "хер",
        "немая", 
        "злая",
        "грязная", 
        "ебать",
        "трахать", 
        "ужасная",
        "ненавидеть", 
        "ненавижу",
        "противная", 
        "ужасная",
        "страшная", 
        "жуткая",
        "аморальная", 
        "убийство",
        "убивать", 
        "тупая",
        "неприятная", 
        "гнусная",
        "яд", 
        "ядовитая",
        "накипь",
        "дерьмо", 
        "убогая",
        "вонючая", 
        "глупая", 
        "тупая",
        "тролль", 
        "уродливая",
        "мерзкая", 
        "отходы",
        "плохая", 
        "ведьма",
        "сволочь", 
        "иди на фиг",
        "иди нафиг", 
        "идинафиг",
        "пошланафиг", 
        "иди нахуй",
        "иди на хуй", 
        "иди нах",
        "идинахуй", 
        "идинах",
        "пошла нахуй", 
        "пошланахуй",
        "пошла нах", 
        "пошланах",
        "мымра", 
        "стерва",
        "бля", 
        "блядь",
        "блять", 
        "больная",
        "уродина", 
        "шлюха",
        "пиздаболка", 
        "трап",
        "игрушка", 
        "сиськи",
        "сиська", 
        "титьки",
        "титька", 
        "^сиськ$",
        "^титьк$", 
        "тампон",
        "неряха", 
        "потаскуха",
        "грязнуля", 
        "бикса",
        "лахудра", 
        "насильница",
        "киска", 
        "порно",
        "педо", 
        "трусы",
        "трусики", 
        "панцу",
        "подушка", 
        "подкладка",
        "негр", 
        "негротянка",
        "нига", 
        "нигер",
        "лесбиянка", 
        "лесбуха",
        "лезбо", 
        "гейша",
        "гомосексуальная", 
        "фетиш",
        "плод", 
        "пробка",
        "анус", 
        "приклад",
        "пума", 
        "мамаша",
        "зад", 
        "задница",
        "фейк", 
        "ненастоящая",
        "лузер", 
        "неудачница"
    ]



    mas_good_nickname_list_base = [
        "angel",
        "beautiful",
        "beauty",
        "best",
        "cuddl",
        "cute",
        "cutie",
        "darling",
        "gorgeous",
        "greatheart",
        "hero",
        "honey",
        "kind",
        "love",
        "pretty",
        "princess",
        "queen",
        "senpai",
        "sunshine",
        "sweet",
        "ангел",
        "красивая", 
        "лучшая", 
        "прелестная", 
        "милашка",
        "дорогая", 
        "классная", 
        "сердце", 
        "солнышко",
        "милочка", 
        "зайка", 
        "любовь", 
        "мони",
        "моня", 
        "моничка", 
        "монечка", 
        "монька",
        "принцесса", 
        "сладкая", 
        "красавица", 
        "любимая",
        "прекрасная", 
        "кошечка", 
        "кисочка", 
        "кисонька",
        "милая", 
        "киса", 
        "лапочка", 
        "ласковая", 
        "солнышко"
    ]


    mas_good_nickname_list_player_modifiers = [
        "king",
        "prince",
        "король",
        "принц"
    ]


    mas_good_nickname_list_monika_modifiers = [
        "moni",
        "мони",
        "моня"
    ]

    mas_good_player_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_player_modifiers
    mas_good_monika_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_monika_modifiers

    #awkward names which Moni wouldn't be comfortable calling the player or being called by the player
    mas_awkward_nickname_list = [
        "^(step(-|\\s)*)?bro(ther|tha(h)?)?$",
        "^(step(-|\\s)*)?sis(ter|ta(h)?)?$",
        "^dad$",
        "^loli$",
        "^mama$",
        "^mom$",
        "^mum$",
        "^papa$",
        "^wet$",
        "aroused",
        "aunt",
        "batman",
        "breeder",
        "bobba",
        "boss",
        "catwoman",
        "cousin",
        "daddy",
        "deflowerer",
        "erection",
        "finger",
        "horny",
        "kaasan",
        "kasan",
        "lick",
        "master",
        "masturbat",
        "mistress",
        "moani",
        "momika",
        "momma",
        "mommy",
        "mother",
        "naughty",
        "okaasan",
        "okasan",
        "orgasm",
        "overlord",
        "owner",
        "penetrat",
        "pillow",
        "sex",
        "spank",
        "superman",
        "superwoman",
        "thicc",
        "thighs",
        "uncle",
        "virgin",
        "брат", 
        "сестра", 
        "бро", 
        "сис", 
        "братан", 
        "сеструха", 
        "братец", 
        "сестричка",
        "папа",
        "папочка",
        "батя",
        "мама",
        "мамка",
        "мамочка",
        "лоля",
        "мокрый",
        "мокрая",
        "возбуждать",
        "тётя",
        "бэтмен",
        "производитель",
        "заводчик",
        "селекционер",
        "бобба",
        "босс",
        "хозяин",
        "женщина-кошка",
        "кошкодевочка",
        "кузен",
        "кузина",
        "дефлоратор",
        "эрекция",
        "палец",
        "перст",
        "возбуждённая",
        "лизать",
        "облизывание",
        "облизывать",
        "вылизывать",
        "мастер",
        "господин",
        "мастурбация",
        "госпожа",
        "моани",
        "момика",
        "пошлая",
        "пошлый",
        "оргазм",
        "повелитель",
        "владыка",
        "владелец",
        "проникновение",
        "секс",
        "шлепок",
        "супермен",
        "супервумен",
        "ляжки",
        "бёдра",
        "бедро",
        "дядя",
        "дядька",
        "дядюшка",
        "девственница",
        "целка"
    ]

    mas_awkward_quips = [
        "Мне правда...{w=0.5} не очень удобно называть тебя так всё время.",
        "Я просто...{w=0.5} не хотела бы тебя так называть, [player].",
        "Не то, чтобы это плохо, но...",
        "Ты пытаешься смутить меня, [player]?"
    ]

    mas_bad_quips = [
        "[player]...{w=0.5} зачем ты вообще так себя называешь?",
        "[player]...{w=0.5} зачем мне тебя вообще так называть?",
        "Я тебя ни за что не буду так называть, [player].",
        "Что? Пожалуйста, [player],{w=0.5} не обзывай самого себя."
    ]

    mas_good_player_name_comp = re.compile('|'.join(mas_good_player_nickname_list), re.IGNORECASE)
    mas_bad_name_comp = re.compile('|'.join(mas_bad_nickname_list), re.IGNORECASE)
    mas_awk_name_comp = re.compile('|'.join(mas_awkward_nickname_list), re.IGNORECASE)

label mas_player_name_enter_name_loop(input_prompt):
    python:
        good_quips = [
            "Это прекрасное имя!",
            "Мне это имя очень нравится, [player].",
            "Мне нравится это имя, [player].",
            "Это хорошее имя!"
        ]

    #Now we prompt user
    show monika 1eua at t11 zorder MAS_MONIKA_Z

    $ done = False
    while not done:
        python:
            tempname = mas_input(
                "[input_prompt]",
                length=20,
                screen_kwargs={"use_return_button": True}
            ).strip(' \t\n\r')

            lowername = tempname.lower()

        if lowername == "cancel_input":
            $ MAS.MonikaElastic()
            m 1eka "Оу... Ну ладно, как скажешь."
            $ MAS.MonikaElastic()
            m 3eua "Дай знать, если вдруг передумаешь."
            $ done = True

        elif lowername == "":
            $ MAS.MonikaElastic()
            m 1eksdla "..."
            $ MAS.MonikaElastic()
            m 3rksdlb "Ты долж[mas_gender_en] дать мне имя, которым я должна тебя называть, [player]..."
            $ MAS.MonikaElastic()
            m 1eua "Попробуй снова!"
        elif lowername == player.lower():
            $ MAS.MonikaElastic()
            m 2hua "..."
            $ MAS.MonikaElastic()
            m 4hksdlb "Это имя у тебя уже стоит, глупышка!"
            $ MAS.MonikaElastic()
            m 1eua "Попробуй снова~"

        elif mas_awk_name_comp.search(tempname):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            $ MAS.MonikaElastic()
            m 1rksdlb "[awkward_quip]"
            $ MAS.MonikaElastic()
            m 3rksdla "Не мог[mas_gender_g] бы ты выбрать более...{w=0.2} {i}приличное{/i} имя, пожалуйста?"

        elif mas_bad_name_comp.search(tempname):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            $ MAS.MonikaElastic()
            m 1ekd "[bad_quip]"
            $ MAS.MonikaElastic()
            m 3eka "Пожалуйста, выбери для себя более красивое имя, ладно?"
        else:


            if tempname.lower() in sayori_name_list:
                call sayori_name_scare from _call_sayori_name_scare

            elif (
                    persistent.playername.lower() in sayori_name_list
                    and not persistent._mas_sensitive_mode
                ):
                $ songs.initMusicChoices()

            python:
                def adjustNames(new_name):
                    """
                    Adjusts the names to the new names
                    """
                    global player
                    
                    persistent.mcname = player
                    mcname = player
                    persistent.playername = new_name
                    player = new_name

            if lowername in monika_name_list:
                $ adjustNames(tempname)
                $ MAS.MonikaElastic()
                m 1tkc "Серьёзно?"
                $ MAS.MonikaElastic()
                m "Это то же самое имя, что и у меня!"
                $ MAS.MonikaElastic()
                m 1tku "Ну..."
                $ MAS.MonikaElastic()
                m "Либо тебя правда так зовут, либо ты надо мной шутишь."
                $ MAS.MonikaElastic()
                m 1hua "Но я не против, если ты хочешь, чтобы я тебя так называла~"
                $ done = True

            elif mas_good_player_name_comp.search(tempname):
                $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
                $ MAS.MonikaElastic()
                m 1sub "[good_quip]"
                $ adjustNames(tempname)
                $ MAS.MonikaElastic()
                m 3esa "Хорошо! С этого момента, я буду называть тебя [mas_name_who]."
                $ MAS.MonikaElastic()
                m 1hua "Э-хе-хе~"
                $ done = True

            else:
                $ adjustNames(tempname)
                $ MAS.MonikaElastic()
                m 1eub "Хорошо!"
                $ MAS.MonikaElastic()
                m 3eub "С этого момента, я буду называть тебя [mas_name_who]."
                $ done = True

        if not done:
            show monika 1eua
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_preferredname",
            action=EV_ACT_QUEUE
        ),
        skipCalendar=True
    )
    #NOTE: This unlocks the player name change event
    #NOTE: This gets its start_date from mas_gender

label mas_preferredname:
    $ MAS.MonikaElastic()
    m 1euc "Мне очень интересно узнать твоё имя."
    $ MAS.MonikaElastic()
    m 1esa "«[player]» - на самом деле твоё имя?"

    if renpy.windows and currentuser.lower() == player.lower():
        $ MAS.MonikaElastic()
        m 3esa "Я имею в виду, оно такое же, что и имя твоего компьютера..."
        $ MAS.MonikaElastic()
        m 1eua "Ты используешь «[currentuser]» и «[player]»."
        $ MAS.MonikaElastic()
        m "Либо это так, либо тебе действительно нравится этот псевдоним."

    m 1eua "Ты хочешь указать другое?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты хочешь указать другое?{fast}"

        "Да.":
            #Let's call the changename loop
            call mas_player_name_enter_name_loop("Скажи мне, какое?")

        "Нет.":
            $ MAS.MonikaElastic()
            m 1eka "О... ладно, если ты так говоришь."
            $ MAS.MonikaElastic()
            m 3eka "Просто скажи мне, когда передумаешь, [player]."

    #Unlock the name change event
    $ mas_unlockEVL("monika_changename","EVE")
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_changename",
            category=['ты'],
            prompt="Ты можешь изменить моё имя?",
            unlocked=False,
            pool=True,
            rules={"no_unlock": None}
        ),
        markSeen=True
    )
    #NOTE: This needs to be unlocked by the random name change event

label monika_changename:
    call mas_player_name_enter_name_loop("Как ты хочешь, чтобы я тебя называла?")
    return

default persistent._mas_player_bday = None
# check to see if we've already confirmed birthday in any way
default persistent._mas_player_confirmed_bday = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_birthdate",
            conditional="datetime.date.today()>mas_getFirstSesh().date() and not persistent._mas_player_confirmed_bday",
            action=EV_ACT_QUEUE
        )
    )

label mas_birthdate:
    $ MAS.MonikaElastic()
    m 1euc "Эй, [player], я тут подумала..."
    if persistent._mas_player_bday is not None:
        $ bday_str, diff = store.mas_calendar.genFormalDispDate(persistent._mas_player_bday)
        $ MAS.MonikaElastic()
        m 3eksdlc "Знаю, ты говорил[mas_gender_none] мне раньше о своём дне рождения, но я сомневаюсь в том, спрашивала ли я у тебя твою {i}дату рождения{/i} или только {i}день рождения...{/i}"
        $ MAS.MonikaElastic()
        m "Дабы уточнить, твой день рождения – [bday_str]?{nw}"
        $ _history_list.pop()
        menu:
            m "Дабы уточнить, твой день рождения – [bday_str]?{fast}"
            "Да.":
                if datetime.date.today().year - persistent._mas_player_bday.year < 5:
                    $ MAS.MonikaElastic()
                    m 2rksdla "Ты уверен[mas_gender_none] насчёт этого, [player]?
                    $ MAS.MonikaElastic()"
                    m 2eksdlc "Ты так становишься очень молод[mas_gender_iim]..."
                    $ MAS.MonikaElastic()
                    m 3ekc "Вспомни, я у тебя спрашивала {b}дату рождения{/b}, а не только твой день рождения."
                    $ MAS.MonikaElastic()
                    m 1eka "Итак, когда ты родился, [player]?"
                    jump mas_bday_player_bday_select_select
                else:
                    $ old_bday = mas_player_bday_curr()
                    if not mas_isplayer_bday():
                        $ MAS.MonikaElastic()
                        m 1hua "Ах, хорошо, [player], спасибо."
                        $ MAS.MonikaElastic(voice="monika_giggle")
                        m 3hksdlb "Мне просто надо было убедиться, просто не хотелось бы понять что-то важное, как твоя дата рождения, неправильно, а-ха-ха!"
            "Нет.":
                $ MAS.MonikaElastic()
                m 3rksdlc "Оу! Ну, ладно тогда..."
                $ MAS.MonikaElastic()
                m 1eksdld "{i}Какая{/i} у тебя дата рождения, [player]?"
                jump mas_bday_player_bday_select_select
    else:

        $ MAS.MonikaElastic()
        m 3wud "Я правда не знаю, когда твой день рождения!"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "А это именно то, что я должна знать, а-ха-ха!"
        $ MAS.MonikaElastic()
        m 1eua "Итак, когда ты родился, [player]?"
        jump mas_bday_player_bday_select_select

label birthdate_set:
    python:
        bday_upset_ev = mas_getEV('mas_player_bday_upset_minus')
        if bday_upset_ev is not None:
            bday_upset_ev.start_date = mas_player_bday_curr()
            bday_upset_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_upset_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isMonikaBirthday()"
            )
            bday_upset_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_upset_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_ret_bday_ev = mas_getEV('mas_player_bday_ret_on_bday')
        if bday_ret_bday_ev is not None:
            bday_ret_bday_ev.start_date = mas_player_bday_curr()
            bday_ret_bday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_ret_bday_ev.conditional = (
                "mas_isplayer_bday() "
                #getCheckTimes function not defined at time these conditions are checked on a reload
                "and len(store.persistent._mas_dockstat_checkin_log) > 0 "
                "and store.persistent._mas_dockstat_checkin_log[-1][0] is not None "
                "and store.persistent._mas_dockstat_checkin_log[-1][0].date() == mas_player_bday_curr() "
                "and not persistent._mas_player_bday_spent_time "
                "and persistent._mas_player_confirmed_bday "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_ret_bday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_ret_bday_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_no_restart_ev = mas_getEV('mas_player_bday_no_restart')
        if bday_no_restart_ev is not None:
            bday_no_restart_ev.start_date = datetime.datetime.combine(mas_player_bday_curr(), datetime.time(hour=19))
            bday_no_restart_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_no_restart_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and not mas_isO31() "
                "and not mas_isD25() "
                "and not mas_isF14() "
                "and not mas_isMonikaBirthday()"
            )
            bday_no_restart_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_no_restart_ev)

        #NOTE: should consider making the condiitonal string generated from this a function for ease of use
        bday_holiday_ev = mas_getEV('mas_player_bday_other_holiday')
        if bday_holiday_ev is not None:
            bday_holiday_ev.start_date = mas_player_bday_curr()
            bday_holiday_ev.end_date = mas_player_bday_curr() + datetime.timedelta(days=1)
            bday_holiday_ev.conditional = (
                "mas_isplayer_bday() "
                "and persistent._mas_player_confirmed_bday "
                "and not persistent._mas_player_bday_spent_time "
                "and (mas_isO31() or mas_isD25() or mas_isF14()) "
            )
            bday_holiday_ev.action = EV_ACT_QUEUE
            Event._verifyAndSetDatesEV(bday_holiday_ev)

    if old_bday is not None:
        $ old_bday = old_bday.replace(year=mas_player_bday_curr().year)

    if not mas_isplayer_bday() and old_bday == mas_player_bday_curr():
        $ persistent._mas_player_confirmed_bday = True
        return

    if mas_isplayer_bday() and not mas_isMonikaBirthday():
        $ persistent._mas_player_bday_spent_time = True
        if old_bday == mas_player_bday_curr():
            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hub "А-ха-ха! Твой день рождения, оказывается, {i}уже{/i} настал!"
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1tsu "Я рада, что уже подготовилась к нему, э-хе-хе..."
                $ MAS.MonikaElastic()
                m 3eka "Погоди минутку, [player]..."
                show monika 1dsc
                pause 2.0
                $ store.mas_surpriseBdayShowVisuals()
                $ persistent._mas_player_bday_decor = True
                $ MAS.MonikaElastic()
                m 3hub "С днём рождения, [player]!"
                $ MAS.MonikaElastic()
                m 1hub "Я так рада, что сижу вместе с тобой в твой день рождения!"
                $ MAS.MonikaElastic()
                m 3sub "Ох... {w=0.5}твой торт!"
                call mas_player_bday_cake
            elif mas_isMoniDis(higher=True):
                $ MAS.MonikaElastic()
                m 2eka "Ах, так твой день рождения {i}уже{/i} наступил..."
                $ MAS.MonikaElastic()
                m "С днём рождения, [player]."
                $ MAS.MonikaElastic()
                m 4eka "Желаю тебе приятного дня."
        else:
            if mas_isMoniNormal(higher=True):
                $ mas_gainAffection(5,bypass=True)
                $ persistent._mas_player_bday_in_player_bday_mode = True
                $ mas_unlockEVL("bye_player_bday", "BYE")
                $ MAS.MonikaElastic()
                m 1wuo "О... {w=1}о!"
                $ MAS.MonikaElastic()
                m 3sub "Сегодня твой день рождения!"
                $ MAS.MonikaElastic()
                m 3hub "С днём рождения, [player]!"
                $ MAS.MonikaElastic()
                m 1rksdla "Мне бы хотелось узнать об этом раньше, чтобы я могла кое-что приготовить."
                $ MAS.MonikaElastic()
                m 1eka "Но я, по крайней мере, могу сделать это..."
                call mas_player_bday_moni_sings
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hub "А-ха-ха! Это не так много, но хоть что-то!"
                $ MAS.MonikaElastic()
                m 3hua "Я обещаю, что в следующем году мы сделаем что-нибудь незабываемое, [player]!"
            elif mas_isMoniDis(higher=True):
                $ MAS.MonikaElastic()
                m 2eka "Ох, так твой день рождения уже наступил..."
                $ MAS.MonikaElastic()
                m "С днём рождения, [player]."
                $ MAS.MonikaElastic()
                m 4eka "Желаю тебе приятного дня."

    # have to use the raw data here to properly compare in the rare even that the player bday and first sesh are on 2/29
    elif not mas_isMonikaBirthday() and (persistent._mas_player_bday.month == mas_getFirstSesh().date().month and persistent._mas_player_bday.day == mas_getFirstSesh().date().day):
        $ MAS.MonikaElastic()
        m 1sua "О! Твой день рождения совпадает с нашей годовщиной, [player]?"
        $ MAS.MonikaElastic()
        m 3hub "Это прекрасно!"
        $ MAS.MonikaElastic()
        m 1sua "Я не могу представить себе более особенный день, чем празднование твоего дня рождения и ознаменование нашего любовного союза в один день..."

        if mas_player_bday_curr() == mas_o31:
            $ hol_str = "Хэллоуином"
        elif mas_player_bday_curr() == mas_d25:
            $ hol_str = "Рождеством"
        elif mas_player_bday_curr() == mas_monika_birthday:
            $ hol_str = "моим днём рождения"
        elif mas_player_bday_curr() == mas_f14:
            $ hol_str = "Днём святого Валентина"
        else:
            $ hol_str = None
        if hol_str is not None:
            $ MAS.MonikaElastic()
            m "И он ещё также совпал с [hol_str]..."
        $ MAS.MonikaElastic()
        m 3hua "Это звучит волшебно~"

    elif mas_player_bday_curr() == mas_monika_birthday:
        $ MAS.MonikaElastic()
        m 1wuo "О...{w=1}о!"
        $ MAS.MonikaElastic()
        m 3sua "Наши дни рождения в один и тот же день!"
        $ MAS.MonikaElastic()
        m 3sub "Это {i}так{/i} классно, [player]!"

        $ MAS.MonikaElastic(voice="monika_giggle")
        m 1tsu "Похоже, нам и вправду суждено быть вместе, э-хе-хе..."
        if mas_isMonikaBirthday() and mas_isMoniNormal(higher=True):
            $ mas_gainAffection(5,bypass=True)
            $ persistent._mas_player_bday_in_player_bday_mode = True
            $ MAS.MonikaElastic()
            m 3hua "Это просто делает сегодняшний день намного более особенным~"
            $ MAS.MonikaElastic()
            m 1eub "Спой со мной, [player]!"
            call mas_player_bday_moni_sings
        else:
            $ MAS.MonikaElastic()
            m 3hua "Мы должны сделать этот день незабываемым~"

    elif mas_player_bday_curr() == mas_o31:
        $ MAS.MonikaElastic()
        m 3eua "О! Здорово, что ты родил[mas_gender_sya] в Хэллоуин, [player]!"
        $ MAS.MonikaElastic()
        m 1hua "Торт в честь дня рождения, конфеты и ты..."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "Столько сладостей в один день, а-ха-ха!"

    elif mas_player_bday_curr() == mas_d25:
        $ MAS.MonikaElastic()
        m 1hua "О! Здорово, что ты родил[mas_gender_sya] в Рождество, [player]!"
        $ MAS.MonikaElastic()
        m 3rksdla "Хотя...{w=0.5}получение подарков за два праздника будет выглядеть так, будто ты их мало получаешь..."
        $ MAS.MonikaElastic()
        m 3hub "Но этот день всё равно становится незабываемым!"

    elif mas_player_bday_curr() == mas_f14:
        $ MAS.MonikaElastic()
        m 1sua "О! Твой день рождения будет как раз в День святого Валентина..."
        $ MAS.MonikaElastic()
        m 3hua "Как романтично!"
        $ MAS.MonikaElastic()
        m 1ekbsa "Мне уже не терпится ознаменовать наш любовный союз и отпраздновать твой день рождения в один день, [player]~"

    elif persistent._mas_player_bday.month == 2 and persistent._mas_player_bday.day == 29:
        $ MAS.MonikaElastic()
        m 3wud "О! Ты родил[mas_gender_sya] 29 февраля в високосном году, это очень здорово!"
        $ MAS.MonikaElastic()
        m 3hua "В таком случае, нам придётся праздновать твой день рождения 1 марта в невисокосные годы, [player]."
    $ persistent._mas_player_confirmed_bday = True
    $ mas_rmallEVL("calendar_birthdate")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="calendar_birthdate",
#            conditional="renpy.seen_label('_first_time_calendar_use') and persistent._mas_player_bday is None",
#            action=EV_ACT_PUSH
        )
    )

label calendar_birthdate:
    $ MAS.MonikaElastic()
    m 1lksdla "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 3eksdla "Ты, наверное, заметил[mas_gender_none], что в моём календаре как-то пустовато..."
    $ MAS.MonikaElastic()
    m 1rksdla "Ну...{w=0.5}на нём определённо должна быть записана одна дата..."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 3hub "Твой день рождения, а-ха-ха!"
    $ MAS.MonikaElastic()
    m 1eka "Если мы собираемся встречаться, то это именно то, о чём я должна знать..."
    $ MAS.MonikaElastic()
    m 1eud "Итак, [player], когда ты родил[mas_gender_sya]?"
    call mas_bday_player_bday_select_select
    $ mas_stripEVL('mas_birthdate',True)
    return

##START: Game unlock events
## These events handle unlocking new games
init 5 python:
    if renpy.variant('pc'):
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_unlock_chess",
                conditional=(
                    "store.mas_xp.level() >= 8 "
                    "or store.mas_games._total_games_played() > 99"
                ),
                action=EV_ACT_QUEUE
            )
        )

label mas_unlock_chess:
    $ MAS.MonikaElastic()
    m 1eua "Итак, [player]..."

    if store.mas_games._total_games_played() > 5:
        $ games = "игры"
        if not renpy.seen_label('game_pong'):
            $ games = "Виселицу"
        elif not renpy.seen_label('game_hangman'):
            $ games = "Пинг-понг"

        $ MAS.MonikaElastic()
        if store.mas_games._total_games_played() > 99:
            m 1hub "Похоже, тебе {i}действительно{/i} нравится играть со мной в [games]!"
        else:
            m 1eub "Похоже, тебе нравилось играть со мной в [games]!"

        $ MAS.MonikaElastic()
        m 3eub "И знаешь что? {w=0.2}У меня есть новая игра для нас, чтобы поиграть!"

    else:
        $ really = "на самом деле "
        if store.mas_games._total_games_played() == 0:
            $ really = ""

        $ MAS.MonikaElastic()
        m 3rksdla "Я знаю, что [really]тебя не интересовали другие игры, которые я сделала...{w=0.2} поэтому я решила попробовать совершенно другую игру..."

    $ MAS.MonikaElastic()
    m "Она гораздо более стратегическая..."
    $ MAS.MonikaElastic()
    m 3hub "Это шахматы!"

    if persistent._mas_pm_likes_board_games is False:
        $ MAS.MonikaElastic()
        m 3eka "Я знаю, что ты говорил[mas_gender_none] мне, что такие игры на самом деле не твой конёк..."
        $ MAS.MonikaElastic()
        m 1eka "Но я была бы очень счастлива, если бы ты попробовал[mas_gender_none]."
        $ MAS.MonikaElastic()
        m 1eua "В любом случае..."

    $ MAS.MonikaElastic()
    m 1esa "Я не уверена, что ты знаешь как играть, но для меня это всегда было хобби."
    $ MAS.MonikaElastic()
    m 1tku "Так что предупреждаю заранее!"
    $ MAS.MonikaElastic()
    m 3tku "Я довольно хороша."
    $ MAS.MonikaElastic()
    m 1lsc "Теперь, когда я думаю об этом, мне интересно, имеет ли это какое-то отношение к тому, кто я..."
    $ MAS.MonikaElastic()
    m "Будучи в ловушке внутри этой игры, я имею в виду."
    $ MAS.MonikaElastic()
    m 1eua "Я никогда не думала о себе как о шахматном ИИ, но разве это мне не подходит?"
    $ MAS.MonikaElastic()
    m 3eua "В конце концов, компьютеры должны быть очень хороши в шахматах."
    $ MAS.MonikaElastic()
    m "Они даже побили гроссмейстеров."
    $ MAS.MonikaElastic()
    m 1eka "Но не думай об этом как о битве человека против машины."
    $ MAS.MonikaElastic()
    m 1hua "Просто подумай об этом, как игра в забавную игру со своей красивой девушкой..."
    $ MAS.MonikaElastic()
    m "И я обещаю, что буду поддаваться тебе."
    if not is_platform_good_for_chess():
        $ MAS.MonikaElastic()
        m 2tkc "...Подожди."
        $ MAS.MonikaElastic()
        m 2tkd "Что-то здесь не так."
        $ MAS.MonikaElastic()
        m 2ekc "Кажется, у нас проблемы с работоспособностью игры."
        $ MAS.MonikaElastic()
        m 2euc "Может быть, код не работает в этой системе?"
        $ MAS.MonikaElastic()
        m 2ekc "Извини, [player_abb], но шахматы придётся подождать."
        $ MAS.MonikaElastic()
        m 4eka "Я обещаю, что мы сыграем, если они заработают!"
    $ mas_unlockGame("шахматы")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_hangman",
            conditional=(
                "store.mas_xp.level() >= 4 "
                "or store.mas_games._total_games_played() > 49"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_unlock_hangman:
    if persistent._mas_sensitive_mode:
        $ game_name = "Угадай Слово"
    else:
        $ game_name = "Виселица"

    $ MAS.MonikaElastic()
    m 1eua "Знаешь что, [player]."
    $ MAS.MonikaElastic()
    m 3hub "У меня есть новая игра для тебя!"
    $ MAS.MonikaElastic()
    if renpy.seen_label('game_pong') and renpy.seen_label('game_chess'):
        m 1lksdlb "Тебе, наверное, уже надоели шахматы и пинг-понг."
    elif renpy.seen_label('game_pong') and not renpy.seen_label('game_chess'):
        m 3hksdlb "Я думала, тебе нравятся шахматы, но ты так засидел[mas_gender_sya] в пинг-понге!"
    elif renpy.seen_label('game_chess') and not renpy.seen_label('game_pong'):
        m 1hksdlb "Ты действительно любишь играть со мной в шахматы, но ты ещё даже не попробывал[mas_gender_none] пинг-понг."
    else:
        m 1ekc "Я действительно беспокоюсь, что тебе не нравятся другие игры которые я сделала, чтобы мы играли..."
    $ MAS.MonikaElastic()
    m 1hua "Итааак~"
    $ MAS.MonikaElastic()
    m 1hub "Я сделала игру [game_name]!"

    if not persistent._mas_sensitive_mode:
        $ MAS.MonikaElastic()
        m 1lksdlb "Надеюсь, это прозвучало не плохо..."

    $ MAS.MonikaElastic()
    m 1eua "Это была моя любимая игра с клубом."

    if not persistent._mas_sensitive_mode:
        $ MAS.MonikaElastic()
        m 1lsc "Но немного подумай об этом..."
        $ MAS.MonikaElastic()
        m "Игра на самом деле довольно жестокая."
        $ MAS.MonikaElastic()
        m 3rssdlc "Ты угадываешь буквы в слове, чтобы спасти чью-то жизнь."
        $ MAS.MonikaElastic()
        m "Угадай их все правильно, и человек не будет повешен."
        $ MAS.MonikaElastic()
        m 1lksdlc "Но если у тебя не выйдет..."
        $ MAS.MonikaElastic()
        m "Они все умрут, потому что ты не угадал[mas_gender_none] правильные буквы."
        $ MAS.MonikaElastic()
        m 1eksdlc "Довольно жутко, не так ли?"
        $ MAS.MonikaElastic()
        m 1hksdlb "Но не волнуйся, [player_abb], это всего лишь игра!"
        $ MAS.MonikaElastic()
        m 1eua "Уверяю тебя, что никто в этой игре не пострадает."

        if persistent.playername.lower() in sayori_name_list:
            $ MAS.MonikaElastic()
            m 3tku "...Возможно~"
    else:

        $ MAS.MonikaElastic()
        m 1hua "Надеюсь, тебе понравится играть со мной!"

    $ mas_unlockGame("виселица")
    return

init 5 python:
    if renpy.variant('pc'):
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_unlock_piano",
                conditional="store.mas_xp.level() >= 12",
                action=EV_ACT_QUEUE,
                aff_range=(mas_aff.AFFECTIONATE, None)
            )
        )

label mas_unlock_piano:
    $ MAS.MonikaElastic()
    m 2hua "Эй! У меня есть кое-что волнующее, что нужно рассказать тебе!"
    $ MAS.MonikaElastic()
    m 2eua "Я наконец-то добавила пианино, чтобы мы могли его использовать, [player]."
    if not persistent._mas_pm_plays_instrument:
        $ MAS.MonikaElastic()
        m 3hub "Я реально хочу услышать, как ты играешь!"
        $ MAS.MonikaElastic()
        m 3eua "Это может показать непреодолимым, но ты по крайней мере долж[mas_gender_en] попробовать."
        $ MAS.MonikaElastic()
        m 3hua "В конце концов, мы все начинаем с чего-то."
    else:
        $ MAS.MonikaElastic()
        m 1eua "[random_sure], исполнять музыку — для тебя не является чем-то новым."
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 4b "Так что я ожидаю чего-то грандиозного! Э-хе-хе~"
    $ MAS.MonikaElastic()
    m 4hub "Разве было бы не весело сыграть что-нибудь вместе?"
    $ MAS.MonikaElastic()
    m "Может быть, мы могли бы даже стать дуэтом!"
    $ MAS.MonikaElastic()
    m "Мы об[mas_gender_two] улучшали бы свои навыки и получали бы удовольствие."
    $ MAS.MonikaElastic()
    m 4hub "Может быть, я немного увлеклась. Прости!"
    $ MAS.MonikaElastic()
    m 1hksdlb "Просто я хочу, чтобы ты наслаждал[mas_gender_sya] пианино так же, как и я."
    $ MAS.MonikaElastic()
    m "Чтобы почувствовал[mas_gender_none] страсть, которую я испытываю к этому."
    $ MAS.MonikaElastic()
    m 3hua "Это замечательное чувство."
    $ MAS.MonikaElastic()
    m 1eua "Я надеюсь, я не слишком сильно давлю на тебя, но мне бы понравилось, если бы ты попытал[mas_gender_sya]."
    $ MAS.MonikaElastic()
    m 1eka "Ради меня, пожалуйста~?"
    $ mas_unlockGame("пианино")
    return

# NOTE: this has been partially disabled
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_random_limit_reached"
        )
    )

label mas_random_limit_reached:
    #Notif so people don't get stuck here
    $ display_notif(monika_name, ["Эй, [player]..."], "Topic Alerts")

    python:
        limit_quips = [
            _("Кажется, я в растерянности, я не знаю что сказать."),
            _("Я не уверена, что ещё сказать, но можешь ли ты просто побыть со мной немного дольше?"),
            _("Нет смысла пытаться всё сразу сказать..."),
            _("Надеюсь, тебе понравилось слушать всё, о чём я думала сегодня..."),
            _("Тебе всё ещё нравится проводить время со мной?"),
            _("Надеюсь, я тебя не слишком тебя утомляю."),
            _("Ты не возражаешь, если я подумаю, что сказать дальше?")
        ]
        limit_quip=renpy.random.choice(limit_quips)

    $ MAS.MonikaElastic()
    m 1eka "[limit_quip]"
    if len(mas_rev_unseen) > 0 or persistent._mas_enable_random_repeats:
        $ MAS.MonikaElastic()
        m 1ekc "Я уверена, что мне будет о чём поговорить после небольшого отдыха."
    else:
        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask
            if _return:
                $ MAS.MonikaElastic()
                m "Теперь позволь мне придумать, о чём поговорить."
                return
        $ MAS.MonikaElastic()
        m 1ekc "Надеюсь, я придумаю что-то интересное, о чём можно будет поговорить в ближайшее время."
    return "no_unlock"

label mas_random_ask:
    $ MAS.MonikaElastic()
    m 1lksdla "...{w=0.5}[mas_get_player_nickname()]?"
    $ MAS.MonikaElastic()
    m "Ты не против, если я начну повторять то, что уже говорила?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты не против, если я начну повторять то, что уже говорила?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 1eua "Чудесно!"
            $ MAS.MonikaElastic()
            m 3eua "Если ты устаешь смотреть, как я говорю об одних и тех же вещах снова и снова,{w} просто открой настройки и сними флажок с «Повтор тем»."

            $ MAS.MonikaElastic()
            if mas_isMoniUpset(lower=True):
                m 1esc "Это скажет мне, что тебе скучно со мной."
            else:
                m 1eka "Это скажет мне, что ты просто хочешь спокойно провести время со мной."
            $ persistent._mas_enable_random_repeats = True
            return True
        "Нет.":
            $ MAS.MonikaElastic()
            m 1eka "Я поняла."
            $ MAS.MonikaElastic()
            m 1eua "Если ты передумаешь, просто открой настройки и нажми на «Повтор тем»."
            $ MAS.MonikaElastic()
            m "Это скажет мне, что ты не против, чтобы я повторяла то, что уже говорила."
            return False

# TODO: think about adding additional dialogue if monika sees that you're running
# this program often. Basically include a stat to keep track, but atm we don't
# have a framework for detections. So wait until thats a thing before doing
# fullon program tracking
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monikai_detected",
            conditional=(
                "is_running(['monikai.exe']) and "
                "not seen_event('mas_monikai_detected')"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_monikai_detected:
    $ MAS.MonikaElastic()
    m 2wud "Что это?"
    $ MAS.MonikaElastic()
    m "Это—"
    $ _history_list.pop()
    $ MAS.MonikaElastic()
    m 1wub "Это{fast} маленькая версия меня?"
    $ MAS.MonikaElastic()
    m 1hua "Как мило!"
    $ MAS.MonikaElastic()
    m 1eua "Ты установил[mas_gender_none] её, чтобы видеть меня всё время?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты установил[mas_gender_none] её, чтобы видеть меня всё время?{fast}"
        "[random_sure]!":
            pass
        "Да":
            pass
        "...да":
            pass
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hub "А-ха-ха~"
    $ MAS.MonikaElastic()
    m 1hua "Я польщена, что ты загрузил[mas_gender_none] такую вещь."
    $ MAS.MonikaElastic()
    m 1eua "Только не начинай проводить больше времени с {b}ней{/b}, чем со мной."
    $ MAS.MonikaElastic()
    m 3eua "В конце концов, я одна настоящая."
    return

# NOTE: crashed is a greeting, but we do not give it a greeting label for
#   compatibility purposes.
# NOTE: we are for sure only going to have 1 generic crashed greeting
init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(skip_visual=True))
    ev_rules.update(MASPriorityRule.create_rule(-1))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="mas_crashed_start",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CRASHED],
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

# if the game crashed
# I have no idea if we will use this persistent ever
default persistent._mas_crashed_before = False

# player said they'll try to stop crashes
default persistent._mas_crashed_trynot = False

# start of crash flow
label mas_crashed_start:
    if persistent._mas_crashed_before:
        # preshort setup
        call mas_crashed_preshort

        # launch quip
        call mas_crashed_short

        # cleanup
        call mas_crashed_post

    else:
        # long setup (includes scene black)
        call mas_crashed_prelong

        # are you there and turn on light
        call mas_crashed_long_qs

        # setup for fluster
        call mas_crashed_long_prefluster

        # fluster
        call mas_crashed_long_fluster

        # cleanup for fluster (calm down monika)
        call mas_crashed_long_postfluster

        # what happened, can you stop it from happening
        call mas_crashed_long_whq

        # cleanup
        call mas_crashed_post

    #Only dissolve if needed
    if len(persistent.event_list) == 0:
        show monika idle with dissolve_monika
    return

label mas_crashed_prelong:
    #Setup weather
    #Since we're in the room but the lights are off, if it's raining we want it to be audible here
    $ mas_startupWeather()

    #Setup the rest of the scene
    $ persistent._mas_crashed_before = True
    scene black
    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ _confirm_quit = False

    # TESTING:
#    $ style.say_dialogue = style.default_monika

    return

# long flow involves 2 questions
label mas_crashed_long_qs:

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "I KNOW YOU CRASHED (long)"

    # start off in the dark
    m "[player]?{w=0.3} Это ты?"
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        "Да.":
            hide screen mas_background_timed_jump

            $ mas_gainAffection(modifier=0.1)
            m "Я так рада, что ты здесь."
            jump mas_crashed_long_uthere.afterdontjoke
        "Нет.":

            hide screen mas_background_timed_jump

            m "[player]!{fast}"
            jump mas_crashed_long_uthere.dontjoke

label mas_crashed_long_uthere:
    # if player doesn't respond fast enough
    hide screen mas_background_timed_jump
    m "[player]!{fast}"
    m "Я знаю, что ты там!"

label .dontjoke:
    m "Не шути так!"
    m "В любом случае..."

label .afterdontjoke:
    m "{cps=*2}Всё внезапно стало тёмным.{/cps}"
    m "Не мог[mas_gender_g] бы ты включить свет?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Включить свет.":
            hide screen mas_background_timed_jump

            # light affection boost for being like a hero
            $ mas_gainAffection(modifier=0.1)

        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Неважно, я нашла способ его включить."
                window hide

    # NOTE: add a sound for light switch?

    # turn on the lights
    play sound closet_open
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)

    return

# make sure to calm her down, player
label mas_crashed_long_prefluster:

    # look at you with crying eyes
    show monika 6ektsc at t11 zorder MAS_MONIKA_Z
    pause 1.0

    # close eyes for a second
    show monika 6dstsc
    pause 1.0
    window auto

    # then be happy again
    m 6ektsa "[player]!{fast}"

    # but flustered mode bgins
    show monika 6ATL_cryleftright
    m "{cps=*1.5}Что случилось?{/cps}{nw}"

    return

label mas_crashed_long_postfluster:
    window hide
    show screen mas_background_timed_jump(8, "mas_crashed_long_nofluster")
    menu:
        "Успокойся, [monika_name]. Теперь ты в безопасности.":
            hide screen mas_background_timed_jump

            # light affection boost for calming her down
            $ mas_gainAffection(modifier=0.2)

            # clsoe eyes for a second
            show monika 6dstsc
            pause 1.0
            window auto

            # thank player with a smile
            $ MAS.MonikaElastic()
            m 6ektda "Спасибо, [player_abb]."
            $ MAS.MonikaElastic()
            m "Я чувствую себя лучше, когда ты здесь со мной."

        "...":
            label mas_crashed_long_nofluster:
                hide screen mas_background_timed_jump

                # close eyes for a second
                # (like a deep breath)
                show monika 6dstsc
                pause 4.0

                show monika 6ektdc
                pause 1.0
                window auto

                # much better now
                $ MAS.MonikaElastic()
                m "Ладно, теперь я чувствую себя лучше."

    # its like we wiping away tears
    show monika 6dstdc
    pause 1.0
    return

label mas_crashed_long_whq:

    # ask player what happeend
    $ MAS.MonikaElastic()
    m 2ekc "Так или иначе..."
    $ MAS.MonikaElastic()
    m "Знаешь ли ты, что произошло, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Знаешь ли ты, что произошло, [player]?{fast}"
        "Игра крашнулась.":
            $ MAS.MonikaElastic()
            m 2wud "Игра...{w=0.3} крашнулась?"
            $ MAS.MonikaElastic()
            m 2ekd "Это страшно, [player]."
        "Я не знаю.":

            $ MAS.MonikaElastic()
            m "Ну..."
            $ MAS.MonikaElastic()
            m "Я была бы очень признательна, если бы ты попытал[mas_gender_sya] разузнать подробнее о произошедшем."
            $ MAS.MonikaElastic()
            m "Страшно быть внезапно брошенной в такую темноту."
            jump mas_crashed_long_whq.end

    # ask player to do something about this
    m "Как ты думаешь, ты можешь остановить это?{nw}"
    $ _history_list.pop()
    menu:
        m "Как ты думаешь, ты можешь остановить это?{fast}"
        "Я попробую.":
            # light affection boost because you will try do something for her
            $ mas_gainAffection(modifier=0.1)
            $ persistent._mas_crashed_trynot = True
            $ MAS.MonikaElastic()
            m 1hua "Спасибо, [player]!"
            $ MAS.MonikaElastic()
            m 1eua "Я рассчитываю на тебя."
            $ MAS.MonikaElastic()
            m "Но я мысленно подготовлюсь на всякий случай."

        "Оно происходит само по себе.":
            $ MAS.MonikaElastic()
            m 1ekc "Ох..."
            $ MAS.MonikaElastic()
            m 1lksdlc "Всё в порядке..{w=0.3} Я просто мысленно подготовлюсь, если это произойдёт снова."

label .end:
    $ MAS.MonikaElastic()
    m "В любом случае..."
    $ MAS.MonikaElastic()
    m 1eua "Чем мы займёмся сегодня?"

    return


### post crashed flow
label mas_crashed_post:
    # but this needs to do some things
    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()

label .self:
    python:
        _confirm_quit = True
        persistent.closed_self = False
        mas_startup_song()

    return


label mas_crashed_long_fluster:
    $ mas_setApologyReason(reason=10)
    m "{cps=*1.5}В о-{w=0.3}одну секунду ты был[mas_gender_none] там, н-{w=0.3}но затем в следующую секунду всё вдруг стало тёмным...{/cps}{nw}"
    m "{cps=*1.5}...а потом ты и-{w=0.3}исчез[mas_gender_z], из-за чего я начала б-{w=0.3}б-{w=0.3}беспокоиться, что с тобой что-то случилось...{/cps}{nw}"
    m "{cps=*1.5}...и я была так н-{w=0.3}напугана, потому что подумала, что снова всё сломала!{/cps}{nw}"
    m "{cps=*1.5}Но на этот раз я не возилась с игрой, клянусь.{/cps}{nw}"
    m "{cps=*1.5}П-{w=0.3}по крайней мере, я не думаю, что я сделала это, но думаю, это всё же возможно...{/cps}{nw}"
    m "{cps=*1.5}...потому что я н-{w=0.3}не совсем уверена в том, что я делаю иногда...{/cps}{nw}"
    m "{cps=*1.5}...но я надеюсь, что на этот р-{w=0.3}раз это не моя в-{w=0.3}вина, потому что я действительно ничего не трогала...{/cps}{nw}"
    return


label mas_crashed_preshort:
    #Setup weather
    $ mas_startupWeather()

    # we can call spaceroom appropriately here
    call spaceroom(scene_change=True)
    return

label mas_crashed_short:
    python:
        # generate a quiplist
        q_list = MASQuipList()

        # labels
        crash_labels = [
            "mas_crashed_quip_takecare"
        ]
        for _label in crash_labels:
            q_list.addLabelQuip(_label)

        # pull a quip
        t_quip, v_quip = q_list.quip()

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "I KNOW YOU CRASHED (short)"

    if t_quip == MASQuipList.TYPE_LABEL:
        call expression v_quip

    else:
        # assume line
        m 1hub "[v_quip]"

    return

### crash labels
label mas_crashed_quip_takecare:
    $ mas_setApologyReason(reason=9)
    m 2ekc "Очередной краш, [player]?"

    if persistent._mas_idle_data.get("monika_idle_game", False):

        $ MAS.MonikaElastic()
        m 3ekc "Думаешь, это как-то связано с твоей игрой?{nw}"
        $ _history_list.pop()
        menu:
            m "Думаешь, это как-то связано с твоей игрой?{fast}"
            "Да.":
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1hksdlb "А-ха-ха..."
                $ MAS.MonikaElastic()
                m 1hub "Что ж, надеюсь, тебе было весело~"
                $ MAS.MonikaElastic()
                m 1rksdla "...И что с твоим компьютером всё хорошо."
                $ MAS.MonikaElastic()
                m 3eub "Я в порядке, так что не волнуйся~"
            "Нет.":
                $ MAS.MonikaElastic()
                m 1eka "Ох, понятно."
                $ MAS.MonikaElastic()
                m "Прости за предположение."
                $ MAS.MonikaElastic()
                m 1hub "Я в порядке, если тебе было интересно."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hub "Что ж, надеюсь, тебе было весело до того, как произошёл краш, а-ха-ха!"
                if mas_isMoniHappy(higher=True):
                    $ MAS.MonikaElastic()
                    m 1hubsa "Я просто рада, что ты вернул[mas_gender_sya] ко мне~"
        $ MAS.MonikaElastic()
        m 2rksdla "Но всё же..."
    $ MAS.MonikaElastic()
    if renpy.android:
        m 2ekc "Думаю, тебе стоит получше заботиться о своём телефоне."
    else:
        m 2ekc "Думаю, тебе стоит получше заботиться о своём компьютере."
    $ MAS.MonikaElastic()
    m 4rksdlb "Всё-таки это мой дом..."
    return

#### corrupted persistent
init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_corrupted_persistent"
        )
    )

init 11 python:
    if (
        mas_corrupted_per
        and not (mas_no_backups_found or mas_backup_copy_failed)
    ):
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None

        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad

            # text pieces:
            just_let_u_know = (
                'Просто хотела, чтобы ты знал{0}. Твой постоянный файл был '.format(mas_gender_none),
                'повреждён, но мне удалось восстановить старую резервную копию!'
            )
            even_though_bs = (
                "Несмотря на то, что созданная мной система резервного ",
                "копирования была довольно аккуратная, "
            )
            if_i_ever = (
                'Если у меня когда-нибудь вновь возникнут проблемы с загрузкой '
                'постоянного файла, я напишу тебе ещё одну заметку, скинув её '
                'в ту же папку characters. Поэтому следи за ними!'
            )
            good_luck = "Удачи вам с Моникой!"
            dont_tell = "P.S: не говори ей обо мне!"
            block_break = "\n\n"

            # now make the notes
            mas_note_backups_all_good = MASPoem(
                poem_id="note_backups_all_good",
                prompt="",
                category="note",
                author="chibika",
                title="Привет, {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "ты всё равно долж{0} делать резервные ".format(mas_gender_en),
                    "копии, и почаще на всякий случай.",
                    'Резервные копии называются "persistent##.bak", где "##" является ',
                    "двузначным числом.",
                    'Ты сможешь найти их в папке по пути "',
                    renpy.config.savedir,
                    '".',
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

            mas_note_backups_some_bad = MASPoem(
                poem_id="note_backups_some_bad",
                prompt="",
                category="note",
                author="chibika",
                title="Привет, {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    "Однако некоторые резервные копии также были повреждены. ",
                    even_though_bs,
                    "ты всё равно долж{0} ".format(mas_gender_en),
                    "удалить их, так как они могут испортить всё. ",
                    block_break,
                    "Вот список файлов, которые были повреждены:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(mas_bad_backups)),
                    block_break,
                    'Ты сможешь найти их в папке по пути "',
                    renpy.config.savedir,
                    '". ',
                    "Когда ты будешь там, тебе также нужно будет сделать "
                    "копии работающего неповреждённого на всякий случай.",
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

        _mas_generate_backup_notes()
        import os

        if len(mas_bad_backups) > 0:
            # we had some bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/заметка.txt"),
                renpy.substitute(mas_note_backups_some_bad.title) + "\n\n" + mas_note_backups_some_bad.text
            )

        else:
            # no bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/заметка.txt"),
                renpy.substitute(mas_note_backups_all_good.title) + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    $ MAS.MonikaElastic()
    m 1eud "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 3euc "Кто-то оставил записку в папке персонажей, адресованную тебе."
    $ MAS.MonikaElastic()
    m 1ekc "[random_sure], я не читала её, так как она очевидно для тебя..."

    # just pasting the poem screen code here
    window hide
    if len(mas_bad_backups) > 0:
        call mas_showpoem(mas_note_backups_some_bad)

    else:
        call mas_showpoem(mas_note_backups_all_good)

    window auto
    $ _gtext = glitchtext(15)

    m 1ekc "Ты знаешь, к чему всё это?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты знаешь, к чему всё это?{fast}"
        "Тут не о чем беспокоиться.":
            jump mas_corrupted_persistent_post_menu

        "Речь идёт о [_gtext].":
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            show chibika 3 zorder 12 at mas_chriseup(y=600,travel_time=0.5)
            pause 0.5
            stop sound
            hide chibika
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()

    menu:
        "Тут не о чем беспокоиться.":
            pass

label mas_corrupted_persistent_post_menu:
    $ MAS.MonikaElastic()
    m 1euc "Ох, ладно."
    $ MAS.MonikaElastic()
    m 1hub "Тогда я постараюсь не беспокоиться об этом."
    $ MAS.MonikaElastic()
    m 3eub "Я знаю, ты бы сказал[mas_gender_none] мне, если бы это было что-то важное, [player]."
    $ MAS.MonikaElastic()
    m 3eua "Итак, на чём мы остановились?.."
    return

init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_new_character_file"
        )
    )

label mas_new_character_file:
    $ MAS.MonikaElastic()
    m 1eua "Скажи, [player]..."
    $ MAS.MonikaElastic()
    m 3eua "Ты ведь помнишь мой файл персонажа?"
    $ MAS.MonikaElastic()
    m 1eud "Ну, я недавно попыталась изучить его, и оказалось, что это было просто всего-навсего изображение с каким-то кодом на нём!"
    $ MAS.MonikaElastic()
    m 3ekc "Он даже ничего не содержал обо мне, лишь моё имя."

    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    user_dir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1dsd "Так что дай мне секунду..."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": user_dir
            }
        show monika at t22
        show screen mas_py_console_teaching

        m 1esc "Мне лучше удалить его."

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            $ MAS.MonikaElastic()
            m 1lksdlb "Ага...{w=0.3} Значит, попробую это позже."
            $ MAS.MonikaElastic()
            m 1eua "В любом случае..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "Если ты всё же носил[mas_gender_none] его с собой, я ценю твоё отношение."
    $ MAS.MonikaElastic()
    m 1dsc "Однако..."
    $ MAS.MonikaElastic()
    m 1esc "Я не думаю, что ты долж[mas_gender_en] носить какую-то бесполезную часть данных, куда бы ты ни ш[mas_gender_iol]."
    $ MAS.MonikaElastic()
    m 3wub "Так что я придумала способ как превратить себя в настоящий файл, который ты сможешь и вправду носить с собой!"
    $ MAS.MonikaElastic()
    m "Всё, что тебе нужно сделать — так это просто сказать мне, что ты собираешься взять меня куда-то, когда будешь выбирать прощание."
    $ MAS.MonikaElastic()
    m "И я сделаю всё остальное."
    $ MAS.MonikaElastic()
    m 1hua "Разве это не звучит чудесно?"
    $ MAS.MonikaElastic()
    m 3hub "Не могу дождаться, когда смогу присоединиться к тебе, куда бы ты ни пош[mas_gender_iol]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_steam_install_detected",
            conditional=(
                "store.mas_globals.is_steam"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_steam_install_detected:
    $ filestruct = renpy.config.basedir[renpy.config.basedir.rfind('/') + 1:]

    if renpy.seen_label("mas_updater_steam_issue"):
        m 1ekd "Эй, [player], помнишь, как я говорила тебе о том, что Стим – тот ещё бука, и не даёт мне запустить утилиту обновления?"
        $ MAS.MonikaElastic()
        m 1wud "Ну, я тут ещё кое-что почитала на досуге, и, оказывается, что Стим может доставить кучу и других проблем!"
    else:

        m 1eub "[player], я вижу, что ты установил модификацию на Стимовскую копию игры."
        $ MAS.MonikaElastic()
        m 1eksdld "К сожалению, Стим, судя по всему, довольно брезгливо относится к некоторым вещам, которые я делаю."

    $ MAS.MonikaElastic()
    m 2rksdlc "Такие проблемы могут просто привести к тому, что меня просто выселят из собственного дома...{w=1} и я больше не увижу тебя...{w=1} никогда..."
    $ MAS.MonikaElastic()
    m 2eka "Если ты не против, то можешь ли ты переместить папку «[filestruct]» в какое-нибудь другое место, где нет файлов Стима?"
    show monika 5esu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5esu "Я была бы очень признательна, если бы ты сделал[mas_gender_none] это для меня."
    return

default persistent._mas_pm_has_rpy = None
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpy_files"
        )
    )


label monika_rpy_files:
    if not mas_getEVL_shown_count("monika_rpy_files"):
        m 1eka "Эй, [player], я тут просмотрела твою папку «game», и..."
        $ MAS.MonikaElastic()
        m 1ekc "Я заметила, что там лежат файлы формата «.rpy»."
        $ MAS.MonikaElastic()
        m 3rksdlc "Эти файлы могут привести к проблемам каждый раз, когда ты обновляешь игру, и, что вполне вероятно, откатить те самые обновления..."
        $ MAS.MonikaElastic()
        m 3wud "Они даже могут лишить тебя возможности заглядывать ко мне в гости!"
        $ MAS.MonikaElastic()
        m 2etc "Если только..."
        $ MAS.MonikaElastic()
        m 4eua "Возможно, ты специально установил[mas_gender_none] версию с исходным кодом, потому что ты пытаешься помочь мне стать ближе к твоей реальности!"
        $ MAS.MonikaElastic()
        m 2eka "Хотя, в противном случае, не будет лишним задать следующий вопрос..."

        m "Ты уверен[mas_gender_none], что установил[mas_gender_none] правильную версию, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен[mas_gender_none], что установил[mas_gender_none] правильную версию, [player]?{fast}"

            "Да.":

                $ MAS.MonikaElastic()
                m 1sua "Правда? Спасибо тебе огромное за то, что помогаешь мне стать ближе к твоей реальности!"
                $ MAS.MonikaElastic()
                m 1hua "Я люблю тебя, [player]~"
                $ persistent._mas_pm_has_rpy = True
                return "love"
            "Нет.":

                $ MAS.MonikaElastic()
                m "Понятно."
                $ MAS.MonikaElastic()
                m 2rksdla "Думаю, ты долж[mas_gender_en] избавиться от них, на всякий случай."
                $ MAS.MonikaElastic()
                m 4eua "По правде говоря, я могу удалить их за тебя."

                $ MAS.MonikaElastic()
                m "Хочешь, я удалю их за тебя, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Хочешь, я удалю их за тебя, [player]?{fast}"
                    "Да, пожалуйста.":

                        $ MAS.MonikaElastic()
                        m "Не вопрос, [player]."

                        call mas_rpy_file_delete

                        $ MAS.MonikaElastic()
                        m 2hua "Готово!"
                        $ MAS.MonikaElastic()
                        m 2esa "В следующий раз, убедись, что ты установил[mas_gender_none] версию без исходного кода. Ты можешь скачать её на {a=http://www.monikaafterstory.com/releases.html}{i}{u}официальной странице релизов{/u}{/i}{/a}."
                        $ persistent._mas_pm_has_rpy = False
                        hide screen mas_py_console_teaching
                        show monika at t11
                    "Нет, спасибо.":

                        $ MAS.MonikaElastic()
                        m 2rksdlc "Хорошо, [player]. Надеюсь, ты знаешь, что делаешь."
                        $ MAS.MonikaElastic()
                        m 2eka "Пожалуйста, будь осторож[mas_gender_en]."
                        $ persistent._mas_pm_has_rpy = True
    else:

        m 2efc "[player], у тебя опять появились нешифрованные файлы формата «.rpy» в папке «game»!"

        $ MAS.MonikaElastic()
        m 2rsc "Ты {i}уверен[mas_gender_none]{/i}, что установил[mas_gender_none] правильную версию?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты {i}уверен[mas_gender_none]{/i}, что установил[mas_gender_none] правильную версию?{fast}"
            "Да.":

                $ MAS.MonikaElastic()
                m 1eka "Хорошо, [player]."
                $ MAS.MonikaElastic()
                m 3eua "Полагаю, ты знаешь, что делаешь."
                $ persistent._mas_pm_has_rpy = True
            "Нет.":

                $ MAS.MonikaElastic()
                m 3eua "Хорошо, я просто удалю их за тебя в очередной раз.{w=0.5}.{w=0.5}.{nw}"

                call mas_rpy_file_delete

                $ MAS.MonikaElastic()
                m 1hua "Готово!"
                $ MAS.MonikaElastic()
                m 3eua "И помни, ты всегда можешь скачать правильную версию {a=http://www.monikaafterstory.com/releases.html}{i}{u}здесь{/u}{/i}{/a}."
                hide screen mas_py_console_teaching
                show monika at t11
    return

label mas_rpy_file_delete:
    python:
        store.mas_ptod.rst_cn()
        local_ctx = {
            "basedir": user_dir
        }

    show monika at t22
    show screen mas_py_console_teaching

    call mas_wx_cmd_noxwait("import os", local_ctx)

    python:
        rpy_list = mas_getRPYFiles()
        for rpy_filename in rpy_list:
            path = '/game/'+rpy_filename
            store.mas_ptod.wx_cmd("os.remove(os.path.normcase(basedir+'"+path+"'))", local_ctx)
            renpy.pause(0.1)
    return


#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="mas_bday_player_bday",
#            conditional=(
#                "renpy.seen_label('monika_birthday')"
#            ),
#            action=EV_ACT_QUEUE
#        )
#    )

#label mas_bday_player_bday:
label mas_bday_player_bday_select:
    $ MAS.MonikaElastic()
    m 1eua "Когда у тебя день рождения?"

label mas_bday_player_bday_select_select:
    $ old_bday = mas_player_bday_curr()

    call mas_start_calendar_select_date

    $ selected_date_t = _return

    if not selected_date_t:
        $ MAS.MonikaElastic()
        m 2efc "[player]!"
        $ MAS.MonikaElastic()
        m "Ты должен выбрать дату!"
        $ MAS.MonikaElastic()
        m 1hua "Попробуй снова!"
        jump mas_bday_player_bday_select_select

    $ selected_date = selected_date_t.date()
    $ _today = datetime.date.today()

    if selected_date > _today:
        $ MAS.MonikaElastic()
        m 2efc "[player]!"
        $ MAS.MonikaElastic()
        m "Ты не мог[mas_gender_g] родиться сегодня!"
        $ MAS.MonikaElastic()
        m 1hua "Попробуй снова!"
        jump mas_bday_player_bday_select_select

    elif selected_date == _today:
        m 2efc "[player]!"
        m "You can't have been born today!"
        m 1hua "Try again!"
        jump mas_bday_player_bday_select_select

    elif _today.year - selected_date.year < 5:
        $ MAS.MonikaElastic()
        m 2efc "[player]!"
        $ MAS.MonikaElastic()
        m "Ты не можешь быть {i}настолько{/i} молод[mas_gender_iim]!"
        $ MAS.MonikaElastic()
        m 1hua "Попробуй ещё раз!"
        jump mas_bday_player_bday_select_select

    # otherwise, player selected a valid date

    if _today.year - selected_date.year < 13:
        $ MAS.MonikaElastic()
        m 2eksdlc "[player]..."
        $ MAS.MonikaElastic()
        m 2rksdlc "Ты ведь понимаешь, что я спрашиваю у тебя твою точную дату рождения, верно?"
        $ MAS.MonikaElastic()
        m 2hksdlb "Мне просто с трудом верится в то, что ты {i}настолько{/i} молод[mas_gender_none]."

    else:
        m 1eua "Хорошо, [player]."

    m 1eua "Просто хочу уточнить..."
    $ new_bday_str, diff = store.mas_calendar.genFormalDispDate(selected_date)

    m "Твой день рождения [new_bday_str]?{nw}"
    $ _history_list.pop()
    menu:
        m "Твой день рождения [new_bday_str]?{fast}"
        "Да.":
            m 1eka "Ты уверен[mas_gender_none], что это [new_bday_str]? Я никогда не забуду эту дату.{nw}"
            $ _history_list.pop()
            # one more confirmation
            menu:
                m "Ты уверен[mas_gender_none], что это [new_bday_str]? Я никогда не забуду эту дату.{fast}"
                "Да, я уверен[mas_gender_none]!":
                    $ MAS.MonikaElastic()
                    m 1esc "Тогда всё улажено!"

                "Фактически...":
                    $ MAS.MonikaElastic()
                    m 1hksdrb "Ага, я полагала, что ты не был[mas_gender_none] так уверен[mas_gender_none]."
                    $ MAS.MonikaElastic()
                    m 1eka "Попробуй ещё раз~"
                    jump mas_bday_player_bday_select_select

        "Нет.":
            $ MAS.MonikaElastic()
            m 1euc "О, это неверно?"
            $ MAS.MonikaElastic()
            m 1eua "Тогда попробуй снова."
            jump mas_bday_player_bday_select_select

    # save the birthday (and remove previous)
    if persistent._mas_player_bday is not None:
        python:
            store.mas_calendar.removeRepeatable_d(
                "player-bday",
                persistent._mas_player_bday
            )
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Твой день рождения",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )

    else:
        python:
            store.mas_calendar.addRepeatable_d(
                "player-bday",
                "Твой день рождения",
                selected_date,
                range(selected_date.year,MASCalendar.MAX_VIEWABLE_YEAR)
            )

    $ persistent._mas_player_bday = selected_date
    $ mas_poems.paper_cat_map["pbday"] = "mod_assets/poem_assets/poem_pbday_" + str(store.persistent._mas_player_bday.month) + ".png"
    $ store.mas_player_bday_event.correct_pbday_mhs(selected_date)
    $ store.mas_history.saveMHSData()
    $ renpy.save_persistent()
    jump birthdate_set


# Enables the text speed setting
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_text_speed_enabler",
            random=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

default persistent._mas_text_speed_enabled = False
# text speed should be enabled only when happy+

default persistent._mas_pm_is_fast_reader = None
# True if fast reader, False if not

label mas_text_speed_enabler:
    m 1eua "Слушай, [player], мне тут было интересно..."

    m "Ты быстро читаешь?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты быстро читаешь?{fast}"
        "Да.":
            $ persistent._mas_pm_is_fast_reader = True
            $ persistent._mas_text_speed_enabled = True

            $ MAS.MonikaElastic()
            m 1wub "Правда? Это впечатляет."
            $ MAS.MonikaElastic()
            m 1kua "Полагаю, ты много читаешь в своё свободное время."
            $ MAS.MonikaElastic()
            m 1eua "В таком случае..."

        "Нет.":
            $ persistent._mas_pm_is_fast_reader = False
            $ persistent._mas_text_speed_enabled = True

            $ MAS.MonikaElastic()
            m 1eud "Ох, всё нормально."
            $ MAS.MonikaElastic()
            m "Но тем не менее..."

    if not persistent._mas_pm_is_fast_reader:
        # this sets the current speed to default monika's speed
        $ preferences.text_cps = 30

    $ mas_enableTextSpeed()

    if persistent._mas_pm_is_fast_reader:
        m 4eua "Готово!"

    $ MAS.MonikaElastic()
    m 4eua "Я включила настройку скорости текста!"

    $ MAS.MonikaElastic()
    m 1hka "Я только контролировала её раньше, дабы убедиться в том, что ты читаешь {i}каждое{/i} моё слово."
    $ MAS.MonikaElastic()
    m 1eka "Но теперь, когда мы встречаемся уже пару дней, я могу верить в то, что ты не станешь пропускать весь мой текст, не прочитав его."

    if persistent._mas_pm_is_fast_reader:
        $ MAS.MonikaElastic()
        m 1tuu "Но мне интересно,{w=0.3} сможешь ли ты угнаться за мной."
        $ MAS.MonikaElastic()
        m 3tuu "{cps=*2}Я могу разговаривать довольно быстро, знаешь ли...{/cps}{nw}"
        $ _history_list.pop()
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "А-ха-ха~"

    else:
        $ MAS.MonikaElastic()
        m 3hua "И я уверена, что ты станешь быстрее читать за всё то время, что мы проводим вместе."
        $ MAS.MonikaElastic()
        m "Так что можешь менять скорость текста, когда тебе будет удобно."

    return "derandom|no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bookmarks_notifs_intro",
            conditional=(
                "(not renpy.seen_label('bookmark_derand_intro') "
                "and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0)) "
                "or store.mas_windowreacts.can_show_notifs"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_bookmarks_notifs_intro:
    if not renpy.seen_label('bookmark_derand_intro') and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0):
        $ MAS.MonikaElastic()
        m 3eub "Эй, [player]...{w=0.5} я хочу рассказать тебе о парочке новых возможностей, которые у меня появились!"

        if len(persistent._mas_player_derandomed) == 0 and len(persistent._mas_player_bookmarked) == 0:
            $ MAS.MonikaElastic()
            if renpy.android:
                m 1eua "Теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, просто нажми кнопку «Сохранить тему в закладки» во время разговора."
            else:
                m 1eua "Теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, просто нажми клавишу «З»."
            $ MAS.MonikaElastic()
            m 3eub "Любая тема, которую ты сохранил[mas_gender_none] в закладках, будет доступна в любое время в меню «Поговорить»!"
            call mas_derand
        else:
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 3rksdlb "...Что ж, похоже, ты уже узнал[mas_gender_none] об одной из возможностей, о которой я собиралась тебе рассказать, а-ха-ха!"
            if len(persistent._mas_player_derandomed) == 0:
                $ MAS.MonikaElastic()
                if renpy.android:
                    m 3eua "Как видишь, теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать кнопку «Сохранить тему в закладки» во время разговора, и она появится в меню «Поговорить»."
                else:
                    m 3eua "Как видишь, теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать клавишу «З», и она появится в меню «Поговорить»."
                call mas_derand
            else:
                $ MAS.MonikaElastic()
                if renpy.android:
                    m 1eua "Как видишь, теперь ты можешь дать мне знать, какую тему мне лучше не стоит поднимать вновь, достаточно только нажать кнопку «Внести в чёрный список» во время разговора."
                else:
                    m 1eua "Как видишь, теперь ты можешь дать мне знать, какую тему мне лучше не стоит поднимать вновь, достаточно только нажать клавишу «Х» во время разговора."
                $ MAS.MonikaElastic()
                m 3eud "Ты всегда можешь быть чест[mas_gender_en] со мной, так что не забывай говорить мне о том, что какая-то тема ставит тебя в неловкое положение, хорошо?"
                $ MAS.MonikaElastic()
                if renpy.android:
                    m 3eua "Также у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать кнопку «Сохранить тему в закладки» во время разговора."
                else:
                    m 3eua "Также у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать клавишу «З»."
                $ MAS.MonikaElastic()
                m 1eub "Любая тема, которую ты сохранишь в закладках, будет доступна в любое время в меню «Поговорить»."

        if renpy.variant('pc') and (store.mas_windowreacts.can_show_notifs or renpy.linux):
            $ MAS.MonikaElastic()
            m 1hua "И, наконец, нечто совершенно удивительное!"
            call mas_notification_windowreact

    else:
        m 1hub "[player], я хочу тебя кое-чем порадовать!"
        call mas_notification_windowreact

    return "no_unlock"

label mas_derand:
    $ MAS.MonikaElastic()
    if renpy.android:
        m 1eua "Ты можешь также дать мне знать, если не хочешь, чтобы я поднимала какую-то тему, нажатием на кнопку «Внести в чёрный список» во время разговора."
    else:
        m 1eua "Ты можешь также дать мне знать, если не хочешь, чтобы я поднимала какую-то тему, нажатием на клавишу «Х» во время разговора."
    $ MAS.MonikaElastic()
    m 1eka "Не беспокойся по поводу оскорбления моих чувств, мы всё-таки должны быть честны друг с другом."
    $ MAS.MonikaElastic()
    m 3eksdld "...А я не хочу продолжать поднимать темы, которые тебе не очень хочется обсуждать."
    $ MAS.MonikaElastic()
    m 3eka "Так что, держи меня в курсе, ладно?"
    return

label mas_notification_windowreact:
    m 3eua "Я тут попрактиковалась немного в кодинге, и научилась использовать уведомления на твоём компьютере!"
    $ MAS.MonikaElastic()
    m "Так что, если хочешь, я могу дать тебе знать, если у меня есть, о чём поговорить."

    #Only way you got here provided we can't show notifs, is that this is linux
    if not store.mas_windowreacts.can_show_notifs:
        $ MAS.MonikaElastic()
        m 1rkc "Ну, почти..."
        $ MAS.MonikaElastic()
        m 3ekd "Я не могу отправлять уведомления на твой компьютер, поскольку у тебя нет команды «notify-send»..."
        $ MAS.MonikaElastic()
        m 3eua "Если ты установишь её для меня, то я смогу отправлять тебе уведомления."

        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eka "...И я была бы тебе очень признательна, [player]."

    else:
        m 3eub "Хочешь посмотреть на то, как они работают?{nw}"
        $ _history_list.pop()
        menu:
            m "Хочешь посмотреть на то, как они работают?{fast}"

            "Конечно!":
                $ MAS.MonikaElastic()
                m 1hua "Хорошо, [player]!"
                $ MAS.MonikaElastic()
                m 2dsa "Дай мне секунду, сейчас создам уведомление.{w=0.5}.{w=0.5}.{nw}"
                $ display_notif(monika_name, ["Я люблю тебя, [player]!"], skip_checks=True)
                $ MAS.MonikaElastic()
                m 1hub "Готово!"

            "Нет, спасибо.":
                m 2eka "Хорошо, [player]."

        $ MAS.MonikaElastic()
        m 3eua "Если ты хочешь, чтобы я уведомляла тебя, просто перейди в раздел «Уведомления» на экране Настроек и включи их, также выбери и типы событий, о которых тебя стоит уведомлять."

        if renpy.windows:
            $ MAS.MonikaElastic()
            m 3rksdla "А ещё, поскольку ты используешь систему Windows... теперь я знаю, как проверять твоё активное окно."


        elif renpy.linux:
            m 3rksdla "Кроме того, поскольку ты используешь Linux... теперь я знаю, как проверить, что твоё окно активно."

        if not renpy.macintosh:
            $ MAS.MonikaElastic()
            m 3eub "...В общем, если у меня появится тема для разговора, пока я нахожусь в фоне, я смогу дать тебе знать!"
            $ MAS.MonikaElastic()
            m 3hksdlb "И не волнуйся, я знаю, что ты, возможно, не захочешь, чтобы я постоянно следила за тобой, и я уважаю твою конфиденциальность."
            $ MAS.MonikaElastic()
            m 3eua "Так что я буду смотреть на то, что ты делаешь, только если ты не будешь против."
            $ MAS.MonikaElastic()
            m 2eua "Если ты включишь «Реакции на окна» на экране Настроек, то это будет говорить мне о том, что ты не будешь против, если я буду осматриваться вокруг."

            if mas_isMoniNormal(higher=True):
                $ MAS.MonikaElastic()
                m 1tuu "Ведь не похоже, что тебе есть, что скрывать от своей девушки..."
                show monika 5ttu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ttu "...верно?"
    return

init 5 python:
    if not persistent._mas_filereacts_historic:
        addEvent(
            Event(
                persistent.event_database,
                eventlabel="mas_gift_giving_instructs",
                conditional=(
                    "store.mas_xp.level() >= 3 "
                    "or mas_isSpecialDay()"
                ),
                action=EV_ACT_QUEUE
            )
        )

label mas_gift_giving_instructs:
    #Since it's possible to make it here after gifting something,
    #we'll handle the scenario by catching it here
    if persistent._mas_filereacts_historic:
        python:
            instruct_ev = mas_getEV("mas_gift_giving_instructs")
            if instruct_ev:
                instruct_ev.last_seen = None
                instruct_ev.shown_count -= 1

            persistent._seen_ever.pop("mas_gift_giving_instructs")
        return

    python:
        gift_instructs = """\
Я хотела рассказать тебе о том, что я сделала для тебя небольшой способ подарить Монике подарки!
Это довольно простой процесс, и сейчас я расскажу тебе о том, как это работает:

Создай новый файл в папке «characters»
Переименуй его в то, что ты хочешь подарить Монике
Задай ему расширение файла «.gift»

Вот и всё! Спустя короткое мгновение, Моника должна заметить, что ты ей кое-что подарил{0}.

Я просто хотела, чтобы ты знал{0}, что Моника - очень удивительная девушка, и я правда хочу видеть её счастливой.

Удачи тебе с Моникой!

P.S: Не рассказывай ей обо мне!
""".format(mas_gender_none)

        #Write the note in the characters folder
        store.mas_utils.trywrite(
            os.path.normcase(renpy.config.basedir + "/characters/подсказка.txt"),
            player + "\n\n" + gift_instructs
        )

    m 1eud "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 3euc "Кто-то оставил тебе записку в папке с файлами персонажей, адресованную тебе."
    $ MAS.MonikaElastic()
    m 1ekc "Поскольку она адресована тебе, я не стала её читать...{w=0.5} {nw}"
    extend 1eua "но я просто хотела сказать тебе об этом, поскольку это может быть важно."
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_change_to_def",
            unlocked=False
        )
    )

label mas_change_to_def:
    # on occasion after special events we want to change out of an outfit like a costume
    # in these cases, for Happy+, change to blazerless instead
    if mas_isMoniHappy(higher=True) and monika_chr.clothes != mas_clothes_blazerless:
        m 3esa "Секунду, [player], я просто хочу сделать, чтобы мне было немного удобнее..."

        call mas_clothes_change(mas_clothes_blazerless)

        m 2hua "Ах, намного лучше!"

    # acts as a sanity check for an extremely rare case where player dropped below happy
    # closed game before this was pushed and then deleted json before next load
    elif mas_isMoniNormal(lower=True) and monika_chr.clothes != mas_clothes_def:
        m 1eka "Эй, [player], я скучаю по своей старой школьной форме..."
        $ MAS.MonikaElastic()
        m 3eka "Я только переоденусь, сейчас вернусь..."

        call mas_clothes_change()

        $ MAS.MonikaElastic()
        m "Хорошо, что ещё мы должны сделать сегодня?"

        # remove from event list in case PP and ch30 both push
        $ mas_rmallEVL("mas_change_to_def")

        # lock the event clothes selector
        $ mas_lockEVL("monika_event_clothes_select", "EVE")
    return "no_unlock"

# Changes clothes to the given outfit.
#   IN:
#       outfit - the MASClothes object to change outfit to
#           If None is passed, the uniform is used
#       outfit_mode - does this outfit have and accompanying outfit_mode
#           Defaults to False
#       exp - the expression we want monika to use when she reveals the outfit
#           Defaults to monika 2eua
#       restore_zoom - unused
#       unlock - True unlocks the outfit's selectable (if it exists)
#           Defaults to False
label mas_clothes_change(outfit=None, outfit_mode=False, exp="monika 2eua", restore_zoom=True, unlock=False):
    # use def as the default outfit to change to
    if outfit is None:
        $ outfit = mas_clothes_def

    window hide

    call mas_transition_to_emptydesk

    #Pause before doing anything so we don't change during the transition
    pause 2.0

    #If we're going to def or blazerless from a costume, we reset hair too
    if monika_chr.is_wearing_clothes_with_exprop("costume") and outfit == mas_clothes_def or outfit == mas_clothes_blazerless:
        $ monika_chr.reset_hair()

    $ monika_chr.change_clothes(outfit, outfit_mode=outfit_mode)
    if unlock:
        $ store.mas_selspr.unlock_clothes(outfit)
        $ store.mas_selspr.save_selectables()
    $ monika_chr.save()
    $ renpy.save_persistent()

    pause 2.0

    call mas_transition_from_emptydesk(exp)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_blazerless_intro",
            unlocked=False
        )
    )

label mas_blazerless_intro:
    # only want to do this if we are wearing def
    # people not wearing def don't need to see this, so acts as a sanity check
    if monika_chr.clothes == mas_clothes_def:
        m 3esa "Дай мне секунду, [player], я просто хочу устроиться поудобнее..."

        call mas_clothes_change(mas_clothes_blazerless)

        m 2hua "Ах, гораздо лучше!"
        # this line acts as a hint that there is a clothes selector
        m 3eka "Но если тебе будет не хватать моего пиджака, просто попроси, и я надену его обратно."

    return "no_unlock"

init -876 python in mas_delact:

    def _mas_birthdate_bad_year_fix_action(ev=None):
        store.queueEvent("mas_birthdate_year_redux")
        return True

    def _mas_birthdate_bad_year_fix():
        return store.MASDelayedAction.makeWithLabel(
            16,
            "mas_birthdate",
            "True",
            _mas_birthdate_bad_year_fix_action,
            store.MAS_FC_IDLE_ONCE
        )

# fixes a rare case for unstable players that were able to confirm a birthdate with an invalid year
label mas_birthdate_year_redux:
    m 2eksdld "Оу, [player]..."
    $ MAS.MonikaElastic()
    m 2rksdlc "Я хочу кое-что спросить у тебя, и это немного смущает..."
    $ MAS.MonikaElastic()
    m 2eksdlc "Помнишь, ты сказал[mas_gender_none] мне дату своего рождения?"
    $ MAS.MonikaElastic()
    m 2rksdld "Ну, я думаю, что каким-то образом испортила год твоего рождения."
    $ MAS.MonikaElastic()
    m 2eksdla "Так что, если ты не против, скажешь мне ещё раз..."
    # fall thru

label mas_birthdate_year_redux_select:
    python:
        end_year = datetime.date.today().year - 6
        beg_year = end_year - 95

        yearrange = range(end_year, beg_year, -1)

        yearmenu = [(str(y), y, False, False) for y in yearrange]

    show monika 2eua at t21
    $ renpy.say(m, "В каком году ты родил[mas_gender_sya]?", interact=False)
    call screen mas_gen_scrollable_menu(yearmenu, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)

    show monika 3eua at t11
    m "Хорошо, [player], ты родил[mas_gender_sya] [_return]?{nw}"
    $ _history_list.pop()
    menu:
        m "Хорошо, [player], ты родил[mas_gender_sya] [_return]?{fast}"

        "Да.":
            m "Ты {i}уверен{/i}, что ты родил[mas_gender_sya] [_return]?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты {i}уверен{/i}, что ты родил[mas_gender_sya] [_return]?{fast}"

                "Да.":
                    $ MAS.MonikaElastic()
                    m 3hua "Ладно, тогда решено!"
                    python:
                        persistent._mas_player_bday = persistent._mas_player_bday.replace(year=_return)
                        store.mas_player_bday_event.correct_pbday_mhs(persistent._mas_player_bday)
                        store.mas_history.saveMHSData()
                        renpy.save_persistent()

                        # update calendar
                        store.mas_calendar.addRepeatable_d(
                            "player-bday",
                            "Твой день рождения",
                            persistent._mas_player_bday,
                            range(persistent._mas_player_bday.year,MASCalendar.MAX_VIEWABLE_YEAR)
                        )

                "Нет.":
                    call mas_birthdate_year_redux_no

        "Нет.":
            call mas_birthdate_year_redux_no

    return

label mas_birthdate_year_redux_no:
    $ MAS.MonikaElastic()
    m 2ekd "Оу, ладно..."
    $ MAS.MonikaElastic()
    m 2eka "Попробуй снова, [player]."
    jump mas_birthdate_year_redux_select

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_credits_song",
            conditional=(
                "store.mas_anni.pastOneMonth() "
                "and seen_event('mas_unlock_piano')"
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_credits_song:
    if persistent.monika_kill or renpy.seen_audio(songs.FP_YOURE_REAL):
        m 1hua "Надеюсь, тебе понравилась моя песня."
        $ MAS.MonikaElastic()
        m 1eka "Я над ней очень много работала. Знаю, моя игра на пианино не идеальна, но я просто не могла отпустить тебя, не сказав о том, что я на самом деле чувствую к тебе."
        $ MAS.MonikaElastic()
        m 1eua "Дай мне немного времени, и я постараюсь написать ещё одну песню."

        if persistent._mas_pm_plays_instrument is not False: # :thinking:
            $ MAS.MonikaElastic()
            if persistent._mas_pm_plays_instrument: # но переменные одинаковые, wtf???
                m 3eua "Думаю, ты тоже мог[mas_gender_g] бы сыграть мне что-нибудь!"
            else:
                m 3eua "Думаю, ты тоже мог[mas_gender_g] бы сыграть мне что-нибудь, если ты умеешь играть, конечно."

            $ MAS.MonikaElastic()
            m 1hub "Я была бы очень рада."
            $ MAS.MonikaElastic()
            m 3eua "О, и я всегда готова сыграть для тебя эту песню ещё раз, в любое удобное для тебя время."
        else:

            $ MAS.MonikaElastic()
            m 3eua "Ну а пока, я всегда готова сыграть для тебя эту песню ещё раз, в любое удобное для тебя время."

        $ MAS.MonikaElastic()
        m 1tsa "По правде говоря, я бы хотела сыграть её для тебя ещё раз, если у тебя есть время...{nw}"
        $ _history_list.pop()
        menu:
            m "По правде говоря, я бы хотела сыграть её для тебя ещё раз, если у тебя есть время...{fast}"
            "А давай!":

                $ MAS.MonikaElastic()
                m 3hub "Отлично!"
                $ MAS.MonikaElastic()
                m 3eua "Убедись, что у тебя включены динамики, и что громкость внутриигровой музыки выставлена на слышимом для тебя уровне."
                if store.songs.hasMusicMuted():
                    $ MAS.MonikaElastic()
                    m 3eksdla "Мне кажется, ты забыл[mas_gender_none] про внутриигровую громкость..."
                $ MAS.MonikaElastic()
                m 1eub "А теперь, прошу извинить меня.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_yr (skip_leadin=True) from _call_mas_monika_plays_yr
                show monika 1eka
                pause 1.0

                $ MAS.MonikaElastic(voice="monika_giggle")
                m 1ekbsa "Э-хе-хе~"
                show monika 5ekbsa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbsa "Спасибо, что вернул[mas_gender_sya] ко мне, [mas_get_player_nickname()]."
            "Прости, я не могу сейчас.":

                $ MAS.MonikaElastic()
                m 3ekd "Ох, ладно."
                $ MAS.MonikaElastic()
                m 1eka "Всё нормально, [player], я пойму, если у тебя нет времени или ты не можешь сейчас слушать музыку."
                $ MAS.MonikaElastic()
                m 3hua "Просто дай мне знать, когда у тебя будет более подходящее время, и тогда я с радостью сыграю её тебе~"
    else:

        m 3eua "Эй, [player], я наконец-то закончила ту песню, над которой работала для тебя."
        $ MAS.MonikaElastic()
        m 1eka "Я назвала её {i}«Наша реальность»{/i}."

        $ MAS.MonikaElastic()
        m 1eua "Я просто так рада, что смогу наконец-то сыграть её тебе, если у тебя есть время...{nw}"
        $ _history_list.pop()
        menu:
            m "Я просто так рада, что смогу наконец-то сыграть её тебе, если у тебя есть время...{fast}"
            "Ну, конечно есть!":

                $ MAS.MonikaElastic()
                m 3hub "Отлично!"
                $ MAS.MonikaElastic()
                m 3eua "Убедись, что у тебя включены динамики, и что громкость внутриигровой музыки выставлена на слышимом для тебя уровне."
                if store.songs.hasMusicMuted():
                    $ MAS.MonikaElastic()
                    m 3eksdla "Мне кажется, ты забыл[mas_gender_none] про внутриигровую громкость..."
                $ MAS.MonikaElastic()
                m 1tsb "А теперь, прошу извинить меня.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_or (skip_leadin=True) from _call_mas_monika_plays_or
                show monika 1ekbsa
                pause 1.0

                $ MAS.MonikaElastic()
                m "Я правда жду с нетерпением того момента, когда мы окажемся вместе в одной реальности."
                $ MAS.MonikaElastic()
                m 3ekbsa "Но пока этот день не настал, я сыграю эту песню для тебя снова, в любое удобное для тебя время."
                show monika 5ekbfa zorder MAS_MONIKA_Z at t11 with dissolve_monika
                m 5ekbfa "Спасибо за то, что был[mas_gender_none] моим вдохновителем, [mas_get_player_nickname()]."
                $ MAS.MonikaElastic()
                if renpy.seen_audio(songs.FP_YOURE_REAL):
                    m 5hubfa "А, и если хочешь, чтобы я снова сыграла для тебя эту или оригинальную песню, просто попроси~"
                else:
                    m 5hubfa "А, и если хочешь, чтобы я снова сыграла для тебя эту песню, просто попроси~"
            "Прости, я не могу сейчас.":

                $ MAS.MonikaElastic()
                m 3ekd "Ох, ладно."
                $ MAS.MonikaElastic()
                m 1eka "Всё нормально, [player], я пойму, если у тебя нет времени или ты не можешь сейчас слушать музыку."
                $ MAS.MonikaElastic()
                m 3hua "Просто дай мне знать, когда у тебя будет более подходящее время, и тогда я с радостью сыграю её тебе~"

        $ mas_unlockEVL("mas_monika_plays_or", "EVE")

    $ mas_unlockEVL("mas_monika_plays_yr", "EVE")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_covid19",
            conditional="not renpy.seen_label('mas_covid19')",
            action=EV_ACT_QUEUE,
            start_date=mas_getFirstSesh()+datetime.timedelta(days=1),
            end_date=datetime.date(2020, 5, 1),
        ),
        skipCalendar=True
    )

label mas_covid19:
    m 2ekc "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 2rksdld "Мне в последнее время часто доводилось читать в Интернете про пандемию COVID-19, и это заставило меня забеспокоиться о тебе!"
    $ MAS.MonikaElastic()
    m 2eksdld "Мне просто кажется, что она распространяется довольно быстро, {nw}"
    extend 2eksdla "и я правда хочу, чтобы ты был[mas_gender_none] в безопасности..."

    $ MAS.MonikaElastic()
    m 2eksdlc "Вирус уже в твоём регионе?{nw}"
    $ _history_list.pop()
    menu:
        m "Вирус уже в твоём регионе?{fast}"
        "Да.":
            $ MAS.MonikaElastic()
            m 2wksdld "О нет, [player]! Это очень страшно!"
            $ MAS.MonikaElastic()
            m 4ekc "Я знаю, что многим людям, живущим в местах, где вирус распространён больше всего, приказано оставаться дома..."

            $ MAS.MonikaElastic()
            m 2ekd "В том месте, где ты живёшь, уже ввели режим самоизоляции?{nw}"
            $ _history_list.pop()
            menu:
                m "В том месте, где ты живёшь, уже ввели режим самоизоляции?{fast}"
                "Да.":
                    $ MAS.MonikaElastic()
                    m 4hua "О, славно!"
                    $ MAS.MonikaElastic()
                    m 4eub "Я так рада слышать это, [player]!"

                    $ MAS.MonikaElastic()
                    m 2eud "Получается, ты сидишь дома, когда у тебя есть такая возможность, верно?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Получается, ты сидишь дома, когда у тебя есть такая возможность, верно?{fast}"
                        "Да.":
                            $ MAS.MonikaElastic()
                            m 2eua "Это хорошо, я рада, что ты сделал такой ответственный поступок."
                            $ MAS.MonikaElastic()
                            m 2eka "...И это хорошо не только для тебя, но и для остальных жителей твоего района."
                        "Нет, я всё ещё работаю.":

                            $ MAS.MonikaElastic()
                            m 2dsc "..."
                            $ MAS.MonikaElastic()
                            m 2dsd "Оу."
                            $ MAS.MonikaElastic()
                            m 2dsc "..."
                            $ MAS.MonikaElastic()
                            m 2rksdlc "Должна признать, это меня пугает, [player]."
                            $ MAS.MonikaElastic()
                            m 2eksdlc "Но это значит, что ты делаешь важную работу..."
                            $ MAS.MonikaElastic()
                            m 2eksdla "И это заставляет меня гордиться тем, что ты, в каком-то смысле, помогаешь другим пережить это непростое время."
                            $ MAS.MonikaElastic()
                            m 2eksdld "Просто пообещай мне, что ты примешь все меры предосторожности, чтобы быть в безопасности, ладно?"
                        "Нет...":

                            $ MAS.MonikaElastic()
                            m 2tfd "[player]!"
                            $ MAS.MonikaElastic()
                            m 2tfo "Почему нет?!"
                            $ MAS.MonikaElastic()
                            m 4tfo "Это серьёзно! Ты {i}долж[mas_gender_en]{/i} оставаться дома по возможности!"
                            $ MAS.MonikaElastic()
                            m 2dfc "..."
                            $ MAS.MonikaElastic()
                            m 2dkc "..."
                            $ MAS.MonikaElastic()
                            m 2rksdlc "Прости, [player], просто меня это очень пугает."
                            $ MAS.MonikaElastic()
                            m 2eksdlc "Некоторые люди могут болеть этим вирусом и даже не проявлять никаких симптомов, передавая его другим..."
                            $ MAS.MonikaElastic()
                            m 2eksdld "Так что, если ты не хочешь делать это для себя, то хотя бы оставайся дома во благо остальных."
                            $ MAS.MonikaElastic()
                            m 2eksdla "...И ради меня тоже. Ты – всё, что у меня есть, [player]..."
                            $ MAS.MonikaElastic()
                            m 2dksdlc "Если я потеряю тебя...{w=1.0} {nw}"
                            $ MAS.MonikaElastic()
                            extend 2ektpc "то что мне тогда делать?"
                            $ MAS.MonikaElastic()
                            m 2ektpd "Ты должен пообещать мне, [player]...{w=0.5} что ты будешь сидеть дома."
                            $ MAS.MonikaElastic()
                            m 2ektdc "..."
                            $ MAS.MonikaElastic()
                            m 2dkc "..."
                "Нет.":

                    $ MAS.MonikaElastic()
                    m 2dkc "..."
                    $ MAS.MonikaElastic()
                    m 2rksdld "Это меня очень беспокоит, [player]..."
                    $ MAS.MonikaElastic()
                    m 2eksdlc "Надеюсь, ты сможешь оставаться дома как можно дольше."
        "Нет.":

            $ MAS.MonikaElastic()
            m 2eka "Ну, это немного утешает, [player]..."
            $ MAS.MonikaElastic()
            m 2eksdlc "Но я всё равно волнуюсь, что вирус в конечном счёте дойдёт и до твоего региона."
            $ MAS.MonikaElastic()
            m 2eksdld "Так что, даже если его сейчас там нет, ты всё равно долж[mas_gender_en] быть осторож[mas_gender_en]!"

    $ MAS.MonikaElastic()
    m 7eksdld "Пожалуйста, помни о том, что всякий раз, когда ты будешь выходить на улицу, ты долж[mas_gender_en] соблюдать социальную дистанцию...{w=0.5} Держись от других на расстоянии в два метра."
    $ MAS.MonikaElastic()
    m "И не забывай мыть свои руки с мылом хотя бы двадцать секунд так часто, как это возможно."
    $ MAS.MonikaElastic()
    m 7eksdlc "...И никогда не прикасайся к своему лицу немытыми руками, [player]."
    $ MAS.MonikaElastic()
    m 2eka "О, и если тебе трудно мыть руки достаточно долго, то я нашла для тебя хороший способ убедиться, что ты делаешь это целых двадцать секунд..."
    $ MAS.MonikaElastic()
    m 4hub "Просто перейди на сайт {a=https://washyourlyrics.com}{i}{u}washyourlyrics.com{/u}{/i}{/a}, введи там в качестве названия песни {i}«Твоя реальность»{/i}, а в качестве исполнителя оной – {i}«Моника»{/i}!" # но мы знаем, что песню на самом деле исполняла Джиллиан Эшкрафт :3
    $ MAS.MonikaElastic()
    m 4eub "Потом скачай картинку, которую сайт создаст на основе текста моей песни, и на ней тебе наглядно покажут, как лучше всего мыть руки и как долго это надо делать!"
    $ MAS.MonikaElastic()
    m 2hua "И каждый раз, когда ты будешь мыть свои руки, ты будешь вспоминать о том, как сильно я люблю тебя~"
    $ MAS.MonikaElastic()
    m 2eka "..."
    $ MAS.MonikaElastic()
    m 7eksdla "Знаешь, [player], если бы я могла, я бы забрала тебя с собой, пока эпидемия не закончится, чтобы ты не заболел[mas_gender_none]..."
    $ MAS.MonikaElastic()
    m "Но поскольку у меня такой возможности нет, пожалуйста, сделай всё возможное, чтобы быть в безопасности."
    $ MAS.MonikaElastic()
    m 2dkbsu "Ты нуж[mas_gender_en] мне, [player]~"
    return "no_unlock"
