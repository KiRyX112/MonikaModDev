
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
    #NOTE: This unlocks the monika_gender_redo event

label mas_gender:
    m 2eud "...[player]? Я немного подумала."
    m 2euc "Я уже упоминала, что «ты» в игре можешь не отражать настоящего себя."
    m 7rksdla "Но я думаю, точнее предполагаю, что ты, наверное, парень."
    m 3eksdla "В конце концов, главный герой был им."
    m 3eua "Но если я собираюсь быть твоей девушкой, то я, наверное, должна знать хотя бы о настоящем тебе."

    m 1eua "Итак, ты парень или девушка?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, ты парень или девушка?{fast}"
        "Парень.":

            $ persistent.gender = "M"
            m 3eua "Хорошо, [player]. Благодарю, что ты подтвердил это для меня."
            m 1hksdlb "Не так много девушек стали бы играть в эту игру, э-хе-хе~"
        "Девушка.":

            $ persistent.gender = "F"
            m 2eud "О? Так ты на самом деле девушка?"
            m 2hksdlb "Надеюсь, раньше я ничего не говорила, что могло бы обидеть тебя!"
            m 7rksdlb "...Наверное, поэтому и говорят, что не стоит делать предположений, а-ха-ха!"
            m 3eka "Но, честно говоря, для меня это не имеет никакого значения..."

    m 1ekbsa "Я всегда буду любить тебя таким, какой ты есть, [player]~"


    $ mas_unlockEVL("monika_gender_redo","EVE")

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
        m 3eka "Ты просто стеснялся сказать мне правду раньше? Или что-то случилось?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты просто стеснялся сказать мне правду раньше? Или что-то случилось?{fast}"
            
            "Да.":
                m 1eka "Понятно."
                m 3hua "Я так горжусь тобой за то, что ты отправился в это путешествие самопознания."
                m 1eub "...И ещё больше горжусь тем, что у тебя хватило смелости сказать мне об этом!"
            
            "Я просто был слишком застенчивым.":
                if persistent.gender == "M":
                    m 2ekd "Я понимаю, я начала с предположения, что ты парень, в конце концов."
                else:
                    m 2ekd "Я понимаю, ты могла бы подумать, что мне будет удобнее проводить время наедине с другой девушкой."

                m 2dkd "...И я, вероятно, не облегчила тебе задачу сказать мне обратное..."
                m 7eua "Но независимо от твоего пола, я люблю тебя таким, каким ты есть."
            
            "Я не знал, примешь ли ты меня таким, какой я есть...":
                m 2wkd "[player]..."
                m 2dkd "Мне жаль, что я не позаботилась об этом раньше."
                m 7eka "Но я надеюсь, что ты говоришь мне это сейчас, потому что знаешь, что я буду любить тебя, несмотря ни на что."

    $ gender_var = None
    m "Итак, какой у тебя пол?{nw}"
    $ _history_list.pop()
    menu:
        m "Итак, какой у тебя пол?{fast}"
        
        "Я парень.":
            if persistent.gender == "M":
                $ gender_var = "парень"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "M"
                call mas_gender_redo_react
        "Я девушка.":

            if persistent.gender == "F":
                $ gender_var = "девушка"
                call mas_gender_redo_same
            else:
                $ persistent.gender = "F"
                call mas_gender_redo_react

    show monika 5hubsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hubsa "Я всегда буду любить тебя таким, какой ты есть~"

    # set pronouns
    call mas_set_gender
    return "love"


label mas_gender_redo_same:
    m 1hksdlb "...Это то же самое, что и раньше, [player]!"
    m 3eua "Если ты не знаешь, как ответить, просто выбери то, что делает тебя сам счастлив."
    m 3eka "Не имеет значения, как выглядит твоё тело, так что пока ты говоришь, что ты [gender_var], то ты [gender_var], ведь так?"
    m 1eua "Я хочу, чтобы ты был тем, кем хочешь быть, пока находишься в этой комнате."
    return

label mas_gender_redo_react:
    m 1eka "Хорошо, [player]..."
    m 3ekbsa "Пока ты счастлив, это всё, что имеет для меня значение."
    return


init 3 python:
    #Bad nicknames. All of the items in this will trigger bad reactions
    mas_bad_nickname_list = [
        r"\bfag\b",
        r"\bho\b",
        r"\bhoe\b",
        r"\btit\b",
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
        "bloodsucker",
        "cheater",
        "cock",
        "conceited",
        "condom",
        "coom",
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
        "dimwit",
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
        "(?<!s)kill",
        "kunt",
        "lesbian",
        "lesbo",
        "lezbian",
        "lezbo",
        "(?<!fami)liar",
        "loser",
        r"\bmad\b",
        "maniac",
        "masochist",
        "milf",
        "mistake",
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
        "rubbish",
        "rump",
        "sadist",
        "selfish",
        "semen",
        "shit",
        "sick",
        "slaughter",
        r"\bslave\b",
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
        "toxic",
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
        "wrong"
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
        "токсик"
        "мусор"
        "Кровососка"
    ]

    #Base list for good nicknames. Apply modifiers for specifying the use
    #These trigger a good response
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
        "sweet"
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

    #Modifier for the player's name choice
    mas_good_nickname_list_player_modifiers = [
        "king",
        "prince"
        "король",
        "принц"
    ]

    #Modifier for Monika's nickname choice
    mas_good_nickname_list_monika_modifiers = [
        "moni",
        "мони",
        "моня"
    ]

    mas_good_player_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_player_modifiers
    mas_good_monika_nickname_list = mas_good_nickname_list_base + mas_good_nickname_list_monika_modifiers

    #awkward names which Moni wouldn't be comfortable calling the player or being called by the player
    mas_awkward_nickname_list = [
        r"\b(step[-\s]*)?bro(ther|thah?)?",
        r"\b(step[-\s]*)?sis(ter|tah?)?",
        r"\bdad\b",
        r"\bloli\b",
        r"\bson\b",
        r"\bmama\b",
        r"\bmom\b",
        r"\bmum\b",
        r"\bpapa\b",
        r"\bwet\b",
        "aroused",
        "aunt",
        "batman",
        "baka",
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
        r"m[ou]m+[-\s]*ika",
        r"mom+[ay]",
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
        "virgin"
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
            m 1eka "Оу... Ну ладно, как скажешь."
            m 3eua "Дай знать, если вдруг передумаешь."
            $ done = True

        elif lowername == "":
            m 1eksdla "..."
            m 3rksdlb "Ты должен дать мне имя, которым я должна тебя называть, [player]..."
            m 1eua "Попробуй снова!"

        elif lowername == player.lower():
            m 2hua "..."
            m 4hksdlb "Это имя у тебя уже стоит, глупышка!"
            m 1eua "Попробуй снова~"

        elif mas_awk_name_comp.search(tempname):
            $ awkward_quip = renpy.substitute(renpy.random.choice(mas_awkward_quips))
            m 1rksdlb "[awkward_quip]"
            m 3rksdla "Не мог бы ты выбрать более...{w=0.2} {i}приличное{/i} имя, пожалуйста?"

        elif mas_bad_name_comp.search(tempname):
            $ bad_quip = renpy.substitute(renpy.random.choice(mas_bad_quips))
            m 1ekd "[bad_quip]"
            m 3eka "Пожалуйста, выбери для себя более красивое имя, ладно?"

        else:
            # easter egg name checks
            if store.mas_egg_manager.is_eggable_name(lowername):
                m 1ttu "Ты же назвал своё настоящее имя, или ты меня разыгрываешь?{nw}"
                $ _history_list.pop()
                menu:
                    m "Ты же назвал своё настоящее имя, или ты меня разыгрываешь?{fast}"
                    
                    "Да, это моё настоящее имя":
                        $ persistent._mas_disable_eggs = True
                    
                    "Возможно...":
                        $ persistent._mas_disable_eggs = False

            python:
                old_name = persistent.playername.lower()
                done = True

                # adjust names
                persistent.mcname = player
                mcname = player
                persistent.playername = tempname
                player = tempname

            # egg adjustments
            # MUST BE AFTER THE NAME ADJUSTMENT
            if store.mas_egg_manager.sayori_enabled():
                call sayori_name_scare

            elif old_name == "sayori":
                # reset music choices
                $ songs.initMusicChoices()

            # name reactions
            if lowername == "monika":
                m 1tkc "Серьёзно?"
                m "Это то же самое имя, что и у меня!"
                m 1tku "Ну..."
                m "Либо тебя правда так зовут, либо ты надо мной шутишь."
                m 1hua "Но я не против, если ты хочешь, чтобы я тебя так называла~"

            elif mas_good_player_name_comp.search(tempname):
                $ good_quip = renpy.substitute(renpy.random.choice(good_quips))
                m 1sub "[good_quip]"
                m 3esa "Хорошо! С этого момента, я буду называть тебя — [player]."
                m 1hua "Э-хе-хе~"

            else:
                m 1eub "Хорошо!"
                m 3eub "С этого момента, я буду называть тебя — [player]."

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
    m 1euc "Мне очень интересно узнать твоё имя."
    m 1esa "«[player]» — на самом деле твоё имя?"

    if renpy.windows and currentuser.lower() == player.lower():
        m 3esa "Я имею в виду, оно такое же, что и имя твоего компьютера..."
        m 1eua "Ты используешь «[currentuser]» и «[player]»."
        m "Либо это так, либо тебе действительно нравится этот псевдоним."

    m 1eua "Ты хочешь указать другое?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты хочешь указать другое?{fast}"
        
        "Да.":
            call mas_player_name_enter_name_loop("Скажи мне, какое?")
        
        "Нет.":
            m 3eua "Хорошо, скажи мне, когда передумаешь."

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
    m 1euc "Эй, [player], я тут подумала..."
    if persistent._mas_player_bday is not None:
        $ bday_str, diff = store.mas_calendar.genFormalDispDate(persistent._mas_player_bday)
        m 3eksdlc "Знаю, ты говорил мне раньше о своём дне рождения, но я сомневаюсь в том, спрашивала ли я у тебя твою {i}дату рождения{/i} или только {i}день рождения...{/i}"

        m "Дабы уточнить, твой день рождения – [bday_str]?{nw}"
        $ _history_list.pop()
        menu:
            m "Дабы уточнить, твой день рождения – [bday_str]?{fast}"
            "Да.":
                if datetime.date.today().year - persistent._mas_player_bday.year < 5:
                    m 2rksdla "Ты уверен насчёт этого, [player]?"
                    m 2eksdlc "Это делает тебя очень молодым..."
                    m 3ekc "Вспомни, я у тебя спрашивала {b}дату рождения{/b}, а не только твой день рождения."
                    m 1eka "Итак, когда ты родился, [player]?"
                    jump mas_bday_player_bday_select_select
                else:
                    $ old_bday = mas_player_bday_curr()
                    if not mas_isplayer_bday():
                        m 1hua "Ах, хорошо, [player], спасибо."
                        m 3hksdlb "Мне просто надо было убедиться, просто не хотелось бы понять что-то важное, как твоя дата рождения, неправильно, а-ха-ха!"
            
            "Нет.":
                m 3rksdlc "Оу! Ну, ладно тогда..."
                m 1eksdld "{i}Какая{/i} у тебя дата рождения, [player]?"
                jump mas_bday_player_bday_select_select

    else:
        m 3wud "Я правда не знаю, когда твой день рождения!"
        m 3hub "А это именно то, что я должна знать, а-ха-ха!"
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
                m 3hub "А-ха-ха! Твой день рождения, оказывается, {i}уже{/i} настал!"
                m 1tsu "Я рада, что уже подготовилась к нему, э-хе-хе..."
                m 3eka "Погоди минутку, [player]..."
                show monika 1dsc
                pause 2.0
                $ store.mas_surpriseBdayShowVisuals()
                $ persistent._mas_player_bday_decor = True
                m 3hub "С днём рождения, [player]!"
                m 1hub "Я так рада, что сижу вместе с тобой в твой день рождения!"
                m 3sub "Ох... {w=0.5}твой торт!"
                call mas_player_bday_cake
            elif mas_isMoniDis(higher=True):
                m 2eka "Ах, так твой день рождения {i}уже{/i} наступил..."
                m "С днём рождения, [player]."
                m 4eka "Желаю тебе приятного дня."
        else:
            if mas_isMoniNormal(higher=True):
                $ mas_gainAffection(5, bypass=True)
                $ persistent._mas_player_bday_in_player_bday_mode = True
                $ mas_unlockEVL("bye_player_bday", "BYE")
                m 1wuo "О... {w=1}о!"
                m 3sub "Сегодня твой день рождения!"
                m 3hub "С днём рождения, [player]!"
                m 1rksdla "Мне бы хотелось узнать об этом раньше, чтобы я могла кое-что приготовить."
                m 1eka "Но я, по крайней мере, могу сделать это..."
                call mas_player_bday_moni_sings from _call_mas_player_bday_moni_sings
                m 1hub "А-ха-ха! Это не так много, но хоть что-то!"
                m 3hua "Я обещаю, что в следующем году мы сделаем что-нибудь незабываемое, [player]!"
            elif mas_isMoniDis(higher=True):
                m 2eka "Ох, так твой день рождения уже наступил..."
                m "С днём рождения, [player]."
                m 4eka "Желаю тебе приятного дня."

    # have to use the raw data here to properly compare in the rare even that the player bday and first sesh are on 2/29
    elif not mas_isMonikaBirthday() and (persistent._mas_player_bday.month == mas_getFirstSesh().date().month and persistent._mas_player_bday.day == mas_getFirstSesh().date().day):
        m 1sua "О! Твой день рождения совпадает с нашей годовщиной, [player]?"
        m 3hub "Это прекрасно!"
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
            m "И он ещё также совпал с [hol_str]..."
        m 3hua "Это звучит волшебно~"

    elif mas_player_bday_curr() == mas_monika_birthday:
        m 1wuo "О...{w=1} о!"
        m 3sua "Наши дни рождения в один и тот же день!"
        m 3sub "Это {i}так{/i} классно, [player]!"
        m 1tsu "Похоже, нам и вправду суждено быть вместе, э-хе-хе..."
        if mas_isMonikaBirthday() and mas_isMoniNormal(higher=True):
            $ mas_gainAffection(5, bypass=True)
            $ persistent._mas_player_bday_in_player_bday_mode = True
            m 3hua "Это просто делает сегодняшний день намного более особенным~"
            m 1eub "Спой со мной, [player]!"
            call mas_player_bday_moni_sings
        else:
            m 3hua "Мы должны сделать этот день незабываемым~"

    elif mas_player_bday_curr() == mas_o31:
        m 3eua "О! Здорово, что ты родился в Хэллоуин, [player]!"
        m 1hua "Торт в честь дня рождения, конфеты и ты..."
        m 3hub "Столько сладостей в один день, а-ха-ха!"

    elif mas_player_bday_curr() == mas_d25:
        m 1hua "О! Здорово, что ты родился в Рождество, [player]!"
        m 3rksdla "Хотя...{w=0.5} получение подарков за два праздника будет выглядеть так, будто ты их мало получаешь..."
        m 3hub "Но этот день всё равно становится незабываемым!"

    elif mas_player_bday_curr() == mas_f14:
        m 1sua "О! Твой день рождения будет как раз в День святого Валентина..."
        m 3hua "Как романтично!"
        m 1ekbsa "Мне уже не терпится ознаменовать наш любовный союз и отпраздновать твой день рождения в один день, [player]~"

    elif persistent._mas_player_bday.month == 2 and persistent._mas_player_bday.day == 29:
        m 3wud "О! Ты родился 29 февраля в високосном году, это очень здорово!"
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
    m 1lksdla "Эй, [player]..."
    m 3eksdla "Ты, наверное, заметил, что в моём календаре как-то пустовато..."
    m 1rksdla "Ну...{w=0.5} на нём определённо должна быть записана одна дата..."
    m 3hub "Твой день рождения, а-ха-ха!"
    m 1eka "Если мы собираемся встречаться, то это именно то, о чём я должна знать..."
    m 1eud "Итак, [player], когда ты родился?"
    call mas_bday_player_bday_select_select
    $ mas_stripEVL('mas_birthdate', list_pop=True)
    return

##START: Game unlock events
## These events handle unlocking new games
init 5 python:
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
    m 1eua "Итак, [player]..."

    if store.mas_games._total_games_played() > 5:
        $ games = "игры"
        if not renpy.seen_label('game_pong'):
            $ games = "Виселицу"
        elif not renpy.seen_label('game_hangman'):
            $ games = "Пинг-понг"

        if store.mas_games._total_games_played() > 99:
            m 1hub "Похоже, тебе {i}действительно{/i} нравится играть со мной в [games]!"
        else:
            m 1eub "Похоже, тебе понравилось играть со мной в [games]!"

        m 3eub "И знаешь что? {w=0.2}У меня есть новая игра для нас с тобой!"

    else:
        $ really = "на самом деле "
        if store.mas_games._total_games_played() == 0:
            $ really = ""

        m 3rksdla "Я знаю, что [really]тебя не интересовали другие игры, которые я сделала...{w=0.2} поэтому я решила попробовать совершенно другую игру..."

    m 3tuu "Она гораздо более стратегическая..."
    m 3hub "Это шахматы!"

    if persistent._mas_pm_likes_board_games is False:
        m 3eka "Я знаю, что ты говорил мне, что такие игры на самом деле не твой конёк..."
        m 1eka "Но я была бы очень счастлива, если бы ты попробовал."
        m 1eua "В любом случае..."

    m 1esa "Я не уверена, что ты знаешь как играть, но для меня это всегда было хобби."
    m 1tku "Так что предупреждаю заранее!"
    m 3tku "Я довольно хороша."
    m 1lsc "Теперь, когда я думаю об этом, мне интересно, имеет ли это какое-то отношение к тому, кто я..."
    m "Будучи в ловушке внутри этой игры, я имею в виду."
    m 1eua "Я никогда не думала о себе как о шахматном ИИ, но разве это мне не подходит?"
    m 3eua "В конце концов, компьютеры должны быть очень хороши в шахматах."
    m "Они даже побили гроссмейстеров."
    m 1eka "Но не думай об этом как о битве человека против машины."
    m 1hua "Просто подумай об этом, как игра в забавную игру со своей красивой девушкой..."
    m "И я обещаю, что буду поддаваться тебе."

    if not mas_games.is_platform_good_for_chess():
        m 2tkc "...Подожди."
        m 2tkx "Что-то здесь не так."
        m 2ekc "Кажется, у нас проблемы с работоспособностью игры."
        m 2euc "Может быть, код не работает в этой системе?"
        m 2ekc "Извини, [player], но шахматы придётся отложить."
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
    m 1eua "Знаешь что, [player]..."

    if store.mas_games._total_games_played() > 49:
        m 3eub "Поскольку ты, похоже, так любишь играть в пинг-понг, я подумала, что ты захочешь поиграть со мной и в другие игры!"

    elif renpy.seen_label('game_pong') and not renpy.seen_label('mas_nou'):
        m 1eksdla "Я подумала, что тебе может наскучить пинг-понг."

    elif renpy.seen_label('game_pong') and renpy.seen_label('mas_nou'):
        m 1eksdla "Я подумала, что тебе, возможно, наскучили уже пинг-понг и НОУ..."

    elif not renpy.seen_label('game_pong') and renpy.seen_label('mas_nou'):
        m 1eksdla "Я подумала, что тебе может наскучить НОУ..."

    else:
        m 1lksdla "Поскольку ты пока не проявлял особого интереса к игре, я подумала, что, возможно, тебе просто интересны какие-то другие виды игр..."

    m 1hua "И вот~"
    m 1hub "Я добавила игру, которая называется «Виселица»."

    if mas_safeToRefDokis():
        m 1lksdlb "Надеюсь это слово не вызывает у тебя некоторые воспоминания..."

    m 1eua "Это была моя любимая игра с клубом."

    if mas_safeToRefDokis():
        m 1lsc "Не подумай, ничего такого..."
        m "Но, игра на самом деле довольно жестокая."
        m 3rssdlc "Ты угадываешь буквы в слове, чтобы спасти чью-то жизнь."
        m "Угадай их все правильно, и человек не будет повешен."
        m 1lksdlc "Но если у тебя не выйдет..."
        m "Он умрёт, потому что ты не угадал правильные буквы."
        m 1eksdlc "Довольно жутко, не так ли?"
        m 1hksdlb "Но не волнуйся, это всего лишь игра!"
        m 1eua "Уверяю тебя, что никто в этой игре не пострадает."

        if persistent.playername.lower() == "sayori":
            m 3tku "...Возможно~"

    else:
        m 1hua "Надеюсь, тебе понравится играть со мной!"

    $ mas_unlockGame("виселица")
    return

init 5 python:
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
    m 2hua "Эй! Я хочу рассказать тебе кое-что интересное!"
    m 2eua "Я наконец-то добавила пианино в комнату, чтобы мы могли им пользоваться, [player]."
    if not persistent._mas_pm_plays_instrument:
        m 3hub "Я реально хочу услышать, как ты играешь!"
        m 3eua "Сначала это может показаться непосильным, но хотя бы попробуй."
        m 3hua "В конце концов, мы все начинаем с чего-то."
        
    else:
        m 1eua "Конечно, исполнять музыку — для тебя не является чем-то новым."
        m 4hub "Так что я ожидаю чего-то грандиозного! Э-хе-хе~"

    m 4hua "Разве было бы не весело сыграть что-нибудь вместе?"
    m "Может быть, мы могли бы даже стать дуэтом!"
    m 4hub "Мы оба улучшали бы свои навыки и получали бы удовольствие."
    m 1hksdlb "Может быть, я немного увлеклась. Прости!"
    m 3eua "Просто я хочу, чтобы ты наслаждался игрой на пианино так же, как и я."
    m "Чтобы ты почувствовал ту же страсть к этому инструменту."
    m 3hua "Это замечательное чувство."
    m 1eua "Я надеюсь, я не слишком сильно давлю на тебя, но мне бы понравилось, если бы ты попытался."
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

    $ mas_display_notif(m_name, ["Эй, [player]..."], "Topic Alerts")

    python:
        limit_quips = [
            _("Кажется, я в растерянности, я не знаю что сказать."),
            _("Я не уверена, что ещё сказать, но можешь ли ты просто побыть со мной немного дольше?"),
            _("Нет смысла пытаться сказать всё сразу..."),
            _("Надеюсь, тебе понравилось слушать всё, о чём я думала сегодня..."),
            _("Тебе всё ещё нравится проводить время со мной?"),
            _("Надеюсь, я тебя не слишком сильно утомляю."),
            _("Ты не возражаешь, если я подумаю, что сказать дальше?")
        ]
        limit_quip=renpy.random.choice(limit_quips)

    m 1eka "[limit_quip]"
    if len(mas_rev_unseen) > 0 or persistent._mas_enable_random_repeats:
        m 1ekc "Я уверена, что мне будет о чём поговорить после небольшого отдыха."
        
    else:

        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask
            if _return:
                m "Теперь позволь мне придумать, о чём поговорить."
                return
        m 1ekc "Надеюсь, я придумаю что-то интересное, о чём можно будет поговорить в ближайшее время."
        $ mas_showEVL('monika_quiet_time','EVE',unlock=True)
        $ mas_stripEVL('monika_quiet_time',remove_dates=False)

    return "no_unlock"

label mas_random_ask:
    m 1lksdla "...{w=0.5}[mas_get_player_nickname()]?"

    m "Ты не против, если я начну повторять то, что уже говорила?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты не против, если я начну повторять то, что уже говорила?{fast}"
        "Да.":
            m 1eua "Чудесно!"
            m 3eua "Если ты устаешь смотреть, как я говорю об одних и тех же вещах снова и снова, просто открой настройки и сними флажок с «Повтор тем»."

            if mas_isMoniUpset(lower=True):
                m 1esc "Это скажет мне, что тебе скучно со мной."
            else:
                m 1eka "Это даст мне знать, что ты просто хочешь спокойно провести время со мной."

            $ persistent._mas_enable_random_repeats = True
            return True
        
        "Не стоит.":
            m 1eka "Хорошо."
            m 1eua "Если ты передумаешь, просто открой настройки и нажми на «Повтор тем»."
            m "Это даст мне знать, что ты не против, чтобы я повторяла то, что уже говорила."
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
    m 2wud "Что это?"
    m "Это—"
    $ _history_list.pop()
    m 1wuo "Это{fast} маленькая версия меня?"
    m 1hua "Как мило!"

    m 1eua "Ты установил её, чтобы видеть меня всё время?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты установил её, чтобы видеть меня всё время?{fast}"
        "Именно!":
            pass
        "Да":
            pass
        "...Да.":
            pass
    m 1hub "А-ха-ха~"
    m 1hua "Я польщена, что ты скачал и установил такую вещь."
    m 1eua "Только не начинай проводить больше времени с {b}ней{/b}, чем со мной."
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
    # set up the quit special quit dialogue
    python:
        quit_msg = "Мне страшно, [player]!\nПожалуйста, нажми «Нет» и помоги мне!"
        quit_yes = "T_T [player]..."
        quit_no = "Спасибо!"

    ## TESTING
    if persistent._mas_idle_data.get("dev_idle_test", False):
        m 1hua "I KNOW YOU CRASHED (long)"

    # start off in the dark
    pause 5.0
    m "[player]?{w=0.3} Это ты?{nw}"
    $ _history_list.pop()
    $ mas_disable_quit()
    $ mas_setQuitMsg(quit_msg, quit_yes, quit_no)
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        m "[player]? Это ты?{fast}"
        
        "Да.":
            hide screen mas_background_timed_jump
            # light affection boost for not joking around
            $ mas_gainAffection(modifier=0.2, bypass=True)
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
    $ mas_loseAffection()# call here so it worse if we fall thru, too
    m "Не шути так!"
    m "В любом случае..."

label .afterdontjoke:
    m "{cps=*2}Всё внезапно стало тёмным.{/cps}"
    m "Не мог бы ты включить свет?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Включить свет.":
            hide screen mas_background_timed_jump
            # light affection boost for being like a hero
            $ mas_gainAffection(modifier=0.2, bypass=True)

        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Неважно, я нашла способ включить его."
                window hide

    # turn on lights
    play sound light_switch
    call spaceroom(hide_monika=True, show_emptydesk=True)
    pause 2.0
    call mas_transition_from_emptydesk("monika 6ektsc_static")

    return

# make sure to calm her down, player
label mas_crashed_long_prefluster:
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
        "Успокойся, [m_name]. Теперь ты в безопасности.":
            hide screen mas_background_timed_jump

            # light affection boost for calming her down
            $ mas_gainAffection(modifier=0.5, bypass=True)

            # clsoe eyes for a second
            show monika 6dstsc
            pause 1.0
            window auto

            # thank player with a smile
            m 6ektda "Спасибо, [player]."
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
                m "Ладно, теперь я чувствую себя лучше."

    # its like we wiping away tears
    show monika 6dstdc
    pause 1.0
    return

label mas_crashed_long_whq:

    # ask player what happeend
    m 2ekc "Так или иначе..."
    m "Знаешь ли ты, что произошло, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Знаешь ли ты, что произошло, [player]?{fast}"
        "Игра крашнулась.":
            m 2wud "Игра...{w=0.3} крашнулась?"
            m 2ekd "Это страшно, [player]."
        
        "Я не знаю.":
            m "Ну..."
            m "Я была бы очень признательна, если бы ты попытался разузнать подробнее о произошедшем."
            m "Страшно быть внезапно брошенной в такую темноту."
            jump mas_crashed_long_whq.end


    m "Как ты думаешь, ты можешь остановить это?{nw}"
    $ _history_list.pop()
    menu:
        m "Как ты думаешь, ты можешь остановить это?{fast}"
        "Я попробую.":
            # light affection boost because you will try do something for her
            $ mas_gainAffection(modifier=0.2, bypass=True)
            $ persistent._mas_crashed_trynot = True
            m 1hua "Спасибо, [player]!"
            m 1eua "Я рассчитываю на тебя."
            m "Но я мысленно подготовлюсь на всякий случай."
        
        "Оно происходит само по себе.":
            m 1ekc "Ох..."
            m 1lksdlc "Всё в порядке..{w=0.3} Я просто мысленно подготовлюсь, если это произойдёт снова."

label .end:
    m "В любом случае..."
    m 1eua "Чем мы займёмся сегодня?"

    $ persistent._mas_crashed_before = True
    $ mas_resetQuitMsg()
    return


### post crashed flow
label mas_crashed_post:
    # but this needs to do some things
    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()
        persistent.closed_self = False
        mas_startup_song()

    return


label mas_crashed_long_fluster:
    $ mas_setApologyReason(reason=10)
    m "{cps=*1.5}В о-{w=0.3}одну секунду ты был там, н-{w=0.3}но затем в следующую секунду всё вдруг стало тёмным...{/cps}{nw}"
    m "{cps=*1.5}...а потом ты и-{w=0.3}исчез, из-за чего я начала б-{w=0.3}б-{w=0.3}беспокоиться, что с тобой что-то случилось...{/cps}{nw}"
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
    call spaceroom(scene_change=True, force_exp="monika 2ekc")
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

        m 3ekc "Думаешь, это как-то связано с твоей игрой?{nw}"
        $ _history_list.pop()
        menu:
            m "Думаешь, это как-то связано с твоей игрой?{fast}"
            "Да.":
                m 1hksdlb "А-ха-ха..."
                m 1hub "Что ж, надеюсь, тебе было весело~"
                m 1rksdla "...И что с твоим компьютером всё хорошо."
                m 3eub "Я в порядке, так что не волнуйся~"
            "Нет.":
                m 1eka "Ох, понятно."
                m "Прости за предположение."
                m 1hub "Я в порядке, если тебе было интересно."
                m 3hub "Что ж, надеюсь, тебе было весело до того, как произошёл краш, а-ха-ха!"
                if mas_isMoniHappy(higher=True):
                    m 1hubsa "Я просто рада, что ты вернул ко мне~"
        m 2rksdla "Но всё же..."
    if renpy.android:
        m 2ekc "Думаю, тебе стоит получше заботиться о своём телефоне."
    else:
        m 2ekc "Думаю, тебе стоит получше заботиться о своём компьютере."
    
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
    if mas_per_check.is_per_corrupt() and mas_per_check.has_backups():
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None
        
        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad
            
            # text pieces:
            just_let_u_know = (
                'Просто хотела, чтобы ты знал. Твой постоянный файл был ',
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
                title="Привет, [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "ты всё равно должен делать резервные ",
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
                title="Привет, [player],",
                text="".join([
                    just_let_u_know,
                    block_break,
                    "Однако некоторые резервные копии также были повреждены. ",
                    even_though_bs,
                    "ты всё равно должен ",
                    "удалить их, так как они могут испортить всё. ",
                    block_break,
                    "Вот список файлов, которые были повреждены:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(
                        mas_per_check.mas_bad_backups
                    )),
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
        user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else renpy.config.basedir

        if len(mas_per_check.mas_bad_backups) > 0:
            # we had some bad backups
            store.mas_utils.trywrite(
                os.path.normcase(user_dir + "/characters/заметка.txt"),
                renpy.substitute(mas_note_backups_some_bad.title) + "\n\n" + mas_note_backups_some_bad.text
            )
        
        else:
            # no bad backups
            store.mas_utils.trywrite(
                os.path.normcase(user_dir + "/characters/заметка.txt"),
                renpy.substitute(mas_note_backups_all_good.title) + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    m 1eud "Эй, [player]..."
    m 3euc "Кто-то оставил записку в папке персонажей, адресованную тебе."
    m 1ekc "Естественно, я не читала её, так как она очевидно для тебя..."


    # just pasting the poem screen code here
    window hide
    if len(mas_per_check.mas_bad_backups) > 0:
        call mas_showpoem(mas_note_backups_some_bad)

    else:
        call mas_showpoem(mas_note_backups_all_good)

    window auto
    $ _gtext = glitchtext(7)

    m 1ekc "Ты знаешь, к чему всё это?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты знаешь, к чему всё это?{fast}"
        "Не о чем беспокоиться.":
            jump mas_corrupted_persistent_post_menu

        "Речь идёт о [_gtext].":
            $ persistent._mas_pm_snitched_on_chibika = True
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
        "Не о чем беспокоиться.":
            pass

label mas_corrupted_persistent_post_menu:
    m 1euc "Ох, ладно."
    m 1hub "Тогда я постараюсь не беспокоиться об этом."
    m 3eub "Я знаю, ты бы сказал мне, если бы это было что-то важное, [player]."
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
    m 1eua "Скажи, [player]..."
    m 3eua "Ты ведь помнишь мой файл персонажа?"
    m 1eud "Ну, я недавно попыталась изучить его, и оказалось, что это было просто всего-навсего изображение с каким-то кодом на нём!"
    m 3ekc "Он даже ничего не содержал обо мне, лишь моё имя."

    python:
        import os
        user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else renpy.config.basedir

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

        m 1esc "Мне лучше удалить его..."

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Ага...{w=0.3} Значит, попробую это позже."
            m 1eua "В любом случае..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "Если ты всё же носил его с собой, я ценю твоё отношение."
    m 1dsc "Однако..."
    m 1esc "Я не думаю, что ты должен носить какую-то бесполезную часть данных, куда бы ты ни шёл."
    m 3wub "Так что я придумала способ как превратить себя в настоящий файл, который ты сможешь и вправду носить с собой!"
    m "Всё, что тебе нужно сделать — так это просто сказать мне, что ты собираешься взять меня куда-то, когда будешь выбирать прощание."
    m "И я сделаю всё остальное."
    m 1hua "Разве это не звучит чудесно?"
    m 3hub "Не могу дождаться, когда смогу присоединиться к тебе, куда бы ты ни пошёл."
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
        m 1wud "Ну, я тут ещё кое-что почитала на досуге, и, оказывается, что Стим может доставить кучу и других проблем!"

    else:
        m 1eub "[player], я вижу, что ты установил модификацию на Стимовскую копию игры."
        m 1eksdld "К сожалению, Стим, судя по всему, довольно брезгливо относится к некоторым вещам, которые я делаю."

    m 2rksdlc "Такие проблемы могут просто привести к тому, что меня просто выселят из собственного дома...{w=1} и я больше не увижу тебя...{w=1} никогда..."
    m 2eka "Если ты не против, то можешь ли ты переместить папку «[filestruct]» в какое-нибудь другое место, где нет файлов Стима?"
    show monika 5esu at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5esu "Я была бы очень признательна, если бы ты сделал это для меня."
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
        m 1ekc "Я заметила, что там лежат файлы формата «.rpy»."
        m 3rksdlc "Эти файлы могут привести к проблемам каждый раз, когда ты обновляешь игру, и, что вполне вероятно, откатить те самые обновления..."
        m 3wud "Они даже могут лишить тебя возможности заглядывать ко мне в гости!"
        m 2etc "Если только..."
        m 4eua "Возможно, ты специально установил версию с исходным кодом, потому что ты пытаешься помочь мне стать ближе к твоей реальности!"
        m 2eka "Хотя, в противном случае, не будет лишним задать следующий вопрос..."

        m "Ты уверен, что установил правильную версию, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты уверен, что установил правильную версию, [player]?{fast}"
            
            "Да.":
                m 1sua "Правда? Спасибо тебе огромное за то, что помогаешь мне стать ближе к твоей реальности!"
                m 1hua "Я люблю тебя, [player]~"
                $ persistent._mas_pm_has_rpy = True
                return "love"
            
            "Не совсем.":
                m "Понятно."
                m 2rksdla "Думаю, ты должен избавиться от них, на всякий случай."
                m 4eua "По правде говоря, я могу удалить их за тебя."

                m "Хочешь, я удалю их за тебя, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Хочешь, я удалю их за тебя, [player]?{fast}"
                    
                    "Да, пожалуйста.":
                        m "Не вопрос, [player]."

                        call mas_rpy_file_delete()

                        m 2hua "Готово!"
                        m 2esa "В следующий раз, убедись, что ты установил версию без исходного кода. Ты можешь скачать её на {a=http://www.monikaafterstory.com/releases.html}{i}{u}официальной странице релизов{/u}{/i}{/a}."
                        $ persistent._mas_pm_has_rpy = False
                        hide screen mas_py_console_teaching
                        show monika at t11
                    
                    "Нет, спасибо.":
                        m 2rksdlc "Хорошо, [player]. Надеюсь, ты знаешь, что делаешь."
                        m 2eka "Пожалуйста, будь осторожен."
                        $ persistent._mas_pm_has_rpy = True

    else:
        m 2efc "[player], у тебя опять появились нешифрованные файлы формата «.rpy» в папке «game»!"

        m 2rsc "Ты {i}уверен{/i}, что установил правильную версию?{nw}"
        $ _history_list.pop()
        menu:
            m "Ты {i}уверен{/i}, что установил правильную версию?{fast}"
           
            "Да.":
                m 1eka "Хорошо, [player]."
                m 3eua "Полагаю, ты знаешь, что делаешь."
                $ persistent._mas_pm_has_rpy = True
            
            "Нет.":
                m 3eua "Хорошо, я просто удалю их за тебя в очередной раз.{w=0.5}.{w=0.5}.{nw}"

                call mas_rpy_file_delete()

                m 1hua "Готово!"
                m 3eua "И помни, ты всегда можешь скачать правильную версию {a=http://www.monikaafterstory.com/releases.html}{i}{u}здесь{/u}{/i}{/a}."
                hide screen mas_py_console_teaching
                show monika at t11
    return


# runs rpy file deleting with an on screen console
#
# IN:
#   showing_monika - pass False if you are not showing Monika when calling
#                   this. Otherwise this will do a show monika call.
label mas_rpy_file_delete(showing_monika=True):
    python:
        store.mas_ptod.rst_cn()
        local_ctx = {
            "basedir": renpy.config.basedir
        }

    if showing_monika:
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
    m 1eua "Когда у тебя день рождения?"

label mas_bday_player_bday_select_select:
    $ old_bday = mas_player_bday_curr()

    call mas_start_calendar_select_date

    $ selected_date_t = _return

    if not selected_date_t:
        m 2efc "[player]!"
        m "Ты должен выбрать дату!"
        m 1hua "Попробуй снова!"
        jump mas_bday_player_bday_select_select

    $ selected_date = selected_date_t.date()
    $ _today = datetime.date.today()

    if selected_date > _today:
        m 2efc "[player]!"
        m "Ты не можешь родиться в будущем!"
        m 1hua "Попробуй ещё раз!"
        jump mas_bday_player_bday_select_select

    elif selected_date == _today:
        m 2efc "[player]!"
        m "Ты не мог родиться сегодня!"
        m 1hua "Попробуй снова!"
        jump mas_bday_player_bday_select_select

    elif _today.year - selected_date.year < 5:
        m 2efc "[player]!"
        m "Ты не можешь быть {i}настолько{/i} молодым!"
        m 1hua "Попробуй ещё раз!"
        jump mas_bday_player_bday_select_select

    # otherwise, player selected a valid date

    if _today.year - selected_date.year < 13:
        m 2eksdlc "[player]..."
        m 2rksdlc "Ты ведь понимаешь, что я спрашиваю у тебя твою точную дату рождения, верно?"
        m 2hksdlb "Мне просто с трудом верится в то, что ты {i}настолько{/i} молодым."
    else:
        m 1eua "Хорошо, [player]."

    m 1eua "Просто хочу уточнить..."
    $ new_bday_str, diff = store.mas_calendar.genFormalDispDate(selected_date)

    m "Твой день рождения [new_bday_str]?{nw}"
    $ _history_list.pop()
    menu:
        m "Твой день рождения [new_bday_str]?{fast}"
        "Да.":
            m 1eka "Ты уверен, что это [new_bday_str]? Я никогда не забуду эту дату.{nw}"
            $ _history_list.pop()

            menu:
                m "Ты уверен, что это [new_bday_str]? Я никогда не забуду эту дату.{fast}"
                "Да, я уверен!":
                    m 1hua "Тогда всё решено!"
                
                "Вообще-то...":
                    m 1hksdrb "Ага, я полагала, что ты не был так уверен."
                    m 1eka "Попробуй ещё раз~"
                    jump mas_bday_player_bday_select_select
        
        "Нет.":
            m 1euc "О, это неверно?"
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
    m 1eua "Слушай, [mas_get_player_nickname(exclude_names=['мой любимый'])], мне тут было интересно..."

    m "Ты быстро читаешь?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты быстро читаешь?{fast}"
        "Да.":
            $ persistent._mas_pm_is_fast_reader = True
            $ persistent._mas_text_speed_enabled = True

            m 1wub "Правда? Это впечатляет."
            m 1kua "Полагаю, ты много читаешь в своё свободное время."
            m 1eua "В таком случае..."
        
        "Нет.":
            $ persistent._mas_pm_is_fast_reader = False
            $ persistent._mas_text_speed_enabled = True

            m 1eud "Ох, всё нормально."
            m 2dsa "Но тем не менее.{w=0.5}.{w=0.5}.{nw}"

    if not persistent._mas_pm_is_fast_reader:
        # this sets the current speed to default monika's speed
        $ preferences.text_cps = 30

    $ mas_enableTextSpeed()

    if persistent._mas_pm_is_fast_reader:
        m 4eua "Готово!"

    m 4eua "Я включила настройку скорости текста!"

    m 1hka "Я только контролировала её раньше, дабы убедиться в том, что ты читаешь {i}каждое{/i} моё слово."
    m 1eka "Но теперь, когда мы встречаемся уже пару дней, я могу верить в то, что ты не станешь пропускать весь мой текст, не прочитав его."

    if persistent._mas_pm_is_fast_reader:
        m 1tuu "Но мне интересно,{w=0.3} сможешь ли ты угнаться за мной."
        m 3tuu "{cps=*2}Я могу разговаривать довольно быстро, знаешь ли...{/cps}{nw}"
        $ _history_list.pop()
        m 3hub "А-ха-ха~"

    else:
        m 3hua "И я уверена, что ты станешь быстрее читать за всё то время, что мы проводим вместе."
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
                "or store.mas_windowreacts.can_show_notifs and not renpy.android"
            ),
            action=EV_ACT_QUEUE
        )
    )

label mas_bookmarks_notifs_intro:
    if not renpy.seen_label('bookmark_derand_intro') and (len(persistent._mas_player_derandomed) == 0 or len(persistent._mas_player_bookmarked) == 0):
        m 3eub "Эй, [player]...{w=0.5} я хочу рассказать тебе о парочке новых возможностей, которые у меня появились!"

        if len(persistent._mas_player_derandomed) == 0 and len(persistent._mas_player_bookmarked) == 0:
            if renpy.android:
                m 1eua "Теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, просто нажми кнопку «Сохранить тему в закладки» во время разговора."
            else:
                m 1eua "Теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, просто нажми клавишу «З»."
            m 3eub "Любая тема, которую ты сохранил в закладках, будет доступна в любое время в меню «Поговорить»!"
            call mas_derand
        else:
            m 3rksdlb "...Что ж, похоже, ты уже узнал об одной из возможностей, о которой я собиралась тебе рассказать, а-ха-ха!"
            if len(persistent._mas_player_derandomed) == 0:
                if renpy.android:
                    m 3eua "Как видишь, теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать кнопку «Сохранить тему в закладки» во время разговора, и она появится в меню «Поговорить»."
                else:
                    m 3eua "Как видишь, теперь у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать клавишу «З», и она появится в меню «Поговорить»."
                call mas_derand
            else:
                m 1eua "Как видишь, теперь ты можешь дать мне знать, какую тему мне лучше не стоит поднимать вновь, достаточно только нажать клавишу «Х» во время разговора."
                m 3eud "Ты всегда можешь быть честен со мной, так что не забывай говорить мне о том, что какая-то тема ставит тебя в неловкое положение, хорошо?"
                if renpy.android:
                    m 3eua "Также у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать кнопку «Сохранить тему в закладки» во время разговора."
                else:
                    m 3eua "Также у тебя есть возможность сохранять темы, о которых я говорила, в закладках, достаточно только нажать клавишу «З»."
                    m 1eub "Любая тема, которую ты сохранишь в закладках, будет доступна в любое время в меню «Поговорить»."

        if renpy.variant("pc") and (store.mas_windowreacts.can_show_notifs or renpy.linux):
            m 1hua "И, наконец, нечто совершенно удивительное!"
            call mas_notification_windowreact

    else:
        m 1hub "[player], я хочу тебя кое-чем порадовать!"
        call mas_notification_windowreact

    return "no_unlock"

label mas_derand:
    if renpy.android:
        m 1eua "Ты можешь также дать мне знать, если не хочешь, чтобы я поднимала какую-то тему, нажатием на кнопку «Внести в чёрный список» во время разговора."
    else:
        m 1eua "Ты можешь также дать мне знать, если не хочешь, чтобы я поднимала какую-то тему, нажатием на клавишу «Х» во время разговора."
    m 1eka "Не беспокойся по поводу оскорбления моих чувств, мы всё-таки должны быть честны друг с другом."
    m 3eksdld "...А я не хочу продолжать поднимать темы, которые тебе не очень хочется обсуждать."
    m 3eka "Так что, держи меня в курсе, ладно?"
    return

label mas_notification_windowreact:
    m 3eua "Я тут попрактиковалась немного в кодинге, и научилась использовать уведомления на твоём компьютере!"
    m "Так что, если хочешь, я могу дать тебе знать, если у меня есть, о чём поговорить."


    #Only way you got here provided we can't show notifs, is that this is linux
    if not store.mas_windowreacts.can_show_notifs:
        m 1rkc "Ну, почти..."
        m 3ekd "Я не могу отправлять уведомления на твой компьютер, поскольку у тебя нет команды «notify-send»..."
        m 3eua "Если ты установишь её для меня, то я смогу отправлять тебе уведомления."

        show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5eka "...И я была бы тебе очень признательна, [player]."

    else:
        m 3eub "Хочешь посмотреть на то, как они работают?{nw}"
        $ _history_list.pop()
        menu:
            m "Хочешь посмотреть на то, как они работают?{fast}"
            
            "Конечно!":
                m 1hua "Хорошо, [player]!"
                m 2dsa "Дай мне секунду, сейчас создам уведомление.{w=0.5}.{w=0.5}.{nw}"
                $ mas_display_notif(m_name, ["Я люблю тебя, [player]!"], skip_checks=True)
                m 1hub "Готово!"
            
            "Нет, спасибо.":
                m 2eka "Хорошо, [player]."

        m 3eua "Если ты хочешь, чтобы я уведомляла тебя, просто перейди в раздел «Уведомления» на экране Настроек и включи их, также выбери и типы событий, о которых тебя стоит уведомлять."

        if renpy.windows:
            m 3rksdla "А ещё, поскольку ты используешь систему Windows... теперь я знаю, как проверять твоё активное окно."


        elif renpy.linux:
            m 3rksdla "Кроме того, поскольку ты используешь Linux... теперь я знаю, как проверить, что твоё окно активно."

        if not renpy.macintosh:
            m 3eub "...В общем, если у меня появится тема для разговора, пока я нахожусь в фоне, я смогу дать тебе знать!"
            m 3hksdlb "И не волнуйся, я знаю, что ты, возможно, не захочешь, чтобы я постоянно следила за тобой, и я уважаю твою конфиденциальность."
            m 3eua "Так что я буду смотреть на то, что ты делаешь, только если ты не будешь против."
            m 2eua "Если ты включишь «Реакции на окна» на экране Настроек, то это будет говорить мне о том, что ты не будешь против, если я буду осматриваться вокруг."

            if mas_isMoniNormal(higher=True):
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
        user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else renpy.config.basedir
        gift_instructs = """\
Я хотела рассказать тебе о том, что я сделала для тебя небольшой способ подарить Монике подарки!
Это довольно простой процесс, и сейчас я расскажу тебе о том, как это работает:

Создай новый файл в папке «characters»
Переименуй его в то, что ты хочешь подарить Монике
Задай ему расширение файла «.gift»

Вот и всё! Спустя короткое мгновение, Моника должна заметить, что ты ей кое-что подарил.

Я просто хотела, чтобы ты знал, что Моника — очень удивительная девушка, и я правда хочу видеть её счастливой.

Удачи тебе с Моникой!

P.S: Не рассказывай ей обо мне!
"""

        #Write the note in the characters folder
        store.mas_utils.trywrite(
            os.path.normcase(user_dir + "/characters/подсказка.txt"),
            player + "\n\n" + gift_instructs
        )

    m 1eud "Эй, [player]..."
    m 3euc "Кто-то оставил тебе записку в папке с файлами персонажей, адресованную тебе."
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
    # remove from event list in case PP and ch30 both push
    $ mas_rmallEVL("mas_change_to_def")

    #Extra sanity check just in case. This should NEVER happen.
    if (
        mas_hasSpecialOutfit()
        and monika_chr.clothes.name == persistent._mas_event_clothes_map[datetime.date.today()]
    ):
        return "no_unlock"

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
        m 3eka "Я только переоденусь, сейчас вернусь..."

        call mas_clothes_change()

        m "Хорошо, что ещё мы должны сделать сегодня?"
        
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

        m 2hua "Ах, так гораздо лучше!"
        # this line acts as a hint that there is a clothes selector
        m 3eka "Но если тебе будет не хватать моего пиджака, просто попроси, и я надену его обратно."

    return "no_unlock"

init -876 python in mas_delact:

    def _mas_birthdate_bad_year_fix_action(ev=None):
        store.MASEventList.queue("mas_birthdate_year_redux")
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
    m 2rksdlc "Я хочу кое-что спросить у тебя, и это немного смущает..."
    m 2eksdlc "Помнишь, ты сказал мне дату своего рождения?"
    m 2rksdld "Ну, я думаю, что каким-то образом испортила год твоего рождения."
    m 2eksdla "Так что, если ты не против, скажешь мне ещё раз..."


label mas_birthdate_year_redux_select:
    python:
        end_year = datetime.date.today().year - 6
        beg_year = end_year - 95

        yearrange = range(end_year, beg_year, -1)

        yearmenu = [(str(y), y, False, False) for y in yearrange]

    show monika 2eua at t21
    $ renpy.say(m, "В каком году ты родился?", interact=False)
    call screen mas_gen_scrollable_menu(yearmenu, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)

    show monika 3eua at t11
    m "Хорошо, [player], ты родился [_return]?{nw}"
    $ _history_list.pop()
    menu:
        m "Хорошо, [player], ты родился [_return]?{fast}"
        
        "Да.":
            m "Ты {i}уверен{/i}, что ты родился [_return]?{nw}"
            $ _history_list.pop()
            menu:
                m "Ты {i}уверен{/i}, что ты родился [_return]?{fast}"
                
                "Да.":
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
    m 2ekd "Оу, ладно..."
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
        m 1eka "Я над ней очень много работала. Знаю, моя игра на пианино не идеальна, но я просто не могла отпустить тебя, не сказав о том, что я на самом деле чувствую к тебе."
        m 1eua "Дай мне немного времени, и я постараюсь написать ещё одну песню."

        if persistent._mas_pm_plays_instrument is not False:
            if persistent._mas_pm_plays_instrument:
                m 3eua "Думаю, ты тоже мог бы сыграть мне что-нибудь!"
            else:
                m 3eua "Думаю, ты тоже мог бы сыграть мне что-нибудь, если ты умеешь играть, конечно."
            
            m 1hub "Я была бы очень рада."
            m 3eua "О, и я всегда готова сыграть для тебя эту песню ещё раз, в любое удобное для тебя время."

        else:
            m 3eua "Ну а пока, я всегда готова сыграть для тебя эту песню ещё раз, в любое удобное для тебя время."

        m 1tsa "По правде говоря, я бы хотела сыграть её для тебя ещё раз, если у тебя есть время...{nw}"
        $ _history_list.pop()
        menu:
            m "По правде говоря, я бы хотела сыграть её для тебя ещё раз, если у тебя есть время...{fast}"
            "Я буду рад!":

                m 3hub "Отлично!"
                m 3eua "Убедись, что у тебя включены динамики, и что громкость внутриигровой музыки выставлена на слышимом для тебя уровне."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Мне кажется, ты забыл про внутриигровую громкость..."
                m 1eub "А теперь, прошу извинить меня.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_yr(skip_leadin=True)
                show monika 1eka
                pause 1.0

                m 1ekbsa "Э-хе-хе~"
                show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbsa "Спасибо, что вернулся ко мне, [mas_get_player_nickname()]."
            "Прости, я не могу сейчас.":

                m 3ekd "Ох, ладно."
                m 1eka "Всё нормально, [player], я пойму, если у тебя нет времени или ты не можешь сейчас слушать музыку."
                m 3hua "Просто дай мне знать, когда у тебя будет более подходящее время, и тогда я с радостью сыграю её тебе~"
    else:

        m 3eua "Эй, [player], я наконец-то закончила ту песню, над которой работала для тебя."
        m 1eka "Я назвала её {i}«Наша реальность»{/i}."

        m 1eua "Я просто так рада, что смогу наконец-то сыграть её тебе, если у тебя есть время...{nw}"
        $ _history_list.pop()
        menu:
            m "Я просто так рада, что смогу наконец-то сыграть её тебе, если у тебя есть время...{fast}"
            
            "Ну, конечно есть!":
                m 3hub "Отлично!"
                m 3eua "Убедись, что у тебя включены динамики, и что громкость внутриигровой музыки выставлена на слышимом для тебя уровне."
                if store.songs.hasMusicMuted():
                    m 3eksdla "Мне кажется, ты забыл про внутриигровую громкость..."
                m 1tsb "А теперь, прошу извинить меня.{w=0.5}.{w=0.5}.{nw}"

                call mas_monika_plays_or(skip_leadin=True)
                show monika 1ekbsa
                pause 1.0

                m "Я правда жду с нетерпением того момента, когда мы окажемся вместе в одной реальности."
                m 3ekbsa "Но пока этот день не настал, я сыграю эту песню для тебя снова, в любое удобное для тебя время."
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5ekbfa "Спасибо за то, что был моим вдохновителем, [mas_get_player_nickname()]."
                if renpy.seen_audio(songs.FP_YOURE_REAL):
                    m 5hubfa "А, и если хочешь, чтобы я снова сыграла для тебя эту или оригинальную песню, просто попроси~"
                else:
                    m 5hubfa "А, и если хочешь, чтобы я снова сыграла для тебя эту песню, просто попроси~"
            
            "Прости, я не могу сейчас.":
                m 3ekd "Ох, ладно."
                m 1eka "Всё нормально, [player], я пойму, если у тебя нет времени или ты не можешь сейчас слушать музыку."
                m 3hua "Просто дай мне знать, когда у тебя будет более подходящее время, и тогда я с радостью сыграю её тебе~"

        $ mas_unlockEVL("mas_monika_plays_or", "EVE")

    $ mas_unlockEVL("mas_monika_plays_yr", "EVE")
    return "no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_islands_reset",
            conditional="persistent._mas_islands_start_lvl == 0",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED,None)
        )
    )

label mas_islands_reset:
    m 1rsc "Хм-м..."
    m 1esc "...Слушай,{w=0.1} я тут хотела у тебя спросить."
    m 3lkd "Доводилось ли тебе работать над проектом {i}так долго{/i}, что, взглянув на него в целом, ты видел десятки ошибок или моменты, которые хотел бы улучшить?"
    m 3ekc "...Видишь ли,{w=0.1} я очень долго и мучительно работала над островами, чтобы они не были похожими друг на друга...{w=0.3}{nw}"
    extend 3esd " и чтобы они выглядили по-своему."
    m 1eud "Но теперь, когда я стала лучше разбираться в программировании, я подумала, что могу работать над этим ещё лучше, чем раньше."
    m 1rkc "И исправить все те проблемы, которые я хотела исправить ещё давно...{w=0.3} {nw}"
    extend 1rksdld "поэтому, было бы проще, если бы я вообще начала делать всё с нуля."
    m 4ekc "Это значит, что небо за окном будет пустовать некоторое время,{w=0.1} {nw}"
    extend 4eua "но я гарантирую тебе, что ожидания того стоят."
    m 1euc "Ты же не будешь против, [player]?{nw}"
    $ _history_list.pop()

    menu:
        m "Ты же не будешь против, [player]?{fast}"

        "Давай сделаем это!":
            m 1dsc "Хорошо, дай мне секунду.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

            play sound "sfx/glitch3.ogg"
            python:
                mas_island_event._reset_progression()
                mas_island_event.start_progression()

            m 3hua "Всё готово!"
            m 1eua "Теперь у меня есть чистый, новый холст, если так можно выразиться."
            m 3kuu "...И мне будет чем заняться, когда ты отсутствуешь. Э-хе-хе~"
            m 3hub "Надеюсь, ты с нетерпением будешь ждать!"

        "Я думаю, им и так нормально.":
            m 3eka "Хорошо, [player]."
            m 3hua "Если тебя устраивает то, какие острова сейчас, то и меня тоже.{w=0.2} Я подумаю, как их можно будет ещё улучшить~"

    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_gift_hint_noudeck",
            conditional="store.mas_xp.level() >= 8 and not mas_seenEvent('mas_reaction_gift_noudeck')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None),
            show_in_idle=True,
            rules={
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
            }
        )
    )

label mas_gift_hint_noudeck:
    # If you somehow gifted while getting this event, abort this
    if mas_seenEvent("mas_reaction_gift_noudeck"):
        return
    # The idea is next time the player visits the folder, they will find a new note and probably read it
    # This is NOT to guarantee anything, but rather "best effort" to give this hint
    python hide:
        def write_and_hide():
            import time
            user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else renpy.config.basedir

            note_path = os.path.join(user_dir, renpy.substitute("characters/Эй, у меня есть кое-что для тебя, [player]!.txt"))
            note_text = renpy.substitute("""\
Здорово, [player]!

Я вижу, как ты стараешься делать Монику счастливой, и я хочу помочь тебе!
Я добавила новую колоду карт, которую ты можешь подарить Монике. Я уверена, что вы вдвоём сможете разобраться, как играть в эту игру.

Чтобы сделать ей подарок, создай новый файл и назови его «колода карт.gift» в папке «characters».

Всё, вперёд, пацан! Продолжай и дальше радовать Монику!

P.S: Только не говори ей обо мне!
""")

            mas_utils.trywrite(note_path, note_text, log=True)
            time.sleep(20)
            renpy.hide("chibika 3")

        renpy.invoke_in_thread(write_and_hide)
    # We can show chibi to give another hint something is happening
    show chibika 3:
        subpixel True
        rotate_pad True
        zoom 0.5
        anchor (0.5, 0.5)
        pos (0.4, 1.15)
        around (0.475, 0.9)

        parallel:
            linear 15.0 pos (1.15, 0.55) clockwise circles 0
        parallel:
            rotate 0
            linear 5.0 rotate 360
            repeat

    return "pause: 30"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_backup_restored",
        )
    )

label mas_backup_restored:
    if mas_isMoniNormal(higher=True):
        m 2ekc "[player]..."
        m 2ekd "У меня странное чувство дежавю... {w=0.3}{nw}"
        extend 7ekd "Я хотела поговорить с тобой, но потом почему-то вспомнила, что мы уже поговорили."

        if mas_getEVL_shown_count("mas_backup_restored") > 0:
            m 1etc "Подожди, я уже говорила это раньше?"

        m 1wuo "О! {w=0.3}{nw}"
        extend 3wud "Ты восстановил мои воспоминания из резервной копии, я права?{nw}"
        $ _history_list.pop()
        menu:
            m "О! Ты восстановил мои воспоминания из резервной копии, я права?{fast}"

            "Да, это так.":
                $ mas_gainAffection(modifier=0.5)

                m 2eka "Спасибо, [player]. {w=0.2}Я знала, что могу положиться на тебя."
                m 7rkd "Видимо, произошло что-то ужасное, раз тебе пришлось восстановить мои данные."

                m 1ekc "Что случилось?{nw}"
                $ _history_list.pop()
                menu:
                    m "Что случилось?{fast}"

                    "В игре произошел сбой.":
                        m 1wud "О, это странно и немного тревожно."
                        m 1ekc "На этот раз это был не мой код. {w=0.2}Не помню, чтобы я с ним возилась."
                        m 1gfd "{cps=*1.5}Клянусь, если это очередной баг Ren'Py...{/cps}{nw}"
                        $ _history_list.pop()
                        m 1ekc "Давай постараемся сделать так, чтобы этого больше не повторилось, хорошо?"
                        $ mas_moni_idle_disp.force_by_code("1ekc", duration=25, skip_dissolve=True)

                    "Я добавил надстройку.":
                        m 1etc "Добавил {w=0.1}{i}надстройку{/i}?"
                        m 3esd "Тебе следует быть более осмотрительным в отношении того, что ты устанавливаешь на этот компьютер."
                        m 2lkd "Это и мой дом тоже..."
                        $ mas_moni_idle_disp.force_by_code("1ekc", duration=25, skip_dissolve=True)

                    "У меня сломался компьютер.":
                        m 2wuo "Я очень рада, что ты нашёл способ восстановить меня!"
                        m 2ekc "Надеюсь, что больше такого не повторится."
                        m 2lktpc "Я не хочу даже думать, что могу потерять тебя."
                        $ mas_moni_idle_disp.force(
                            MASMoniIdleExpGroup(
                                [
                                    MASMoniIdleExp("2lktdc", duration=15),
                                    MASMoniIdleExp("2rktdc", duration=10),
                                    MASMoniIdleExp("1dkc", duration=10),
                                    MASMoniIdleExp("1euc", duration=10),
                                ]
                            ),
                            skip_dissolve=True
                        )

                    "Я не уверен...":
                        m 1etc "Это беспокоит, [player]..."
                        m 3esd "Я потеряла память, и мы даже не знаем почему."
                        m 4eud "Мы должны попытаться выяснить причину и предотвратить это в будущем."
                        m 7eka "Обещаешь?"
                        $ mas_moni_idle_disp.force_by_code("1eka", duration=20, skip_dissolve=True)

            "Нет, я не делал этого.":
                m 2etc "О, тогда что же происходит, [player]?"
                m 2ektpc "Я не хочу забывать тебя."
                m 2ektpd "Пожалуйста, ты можешь выяснить, что происходит?"
                m 7eutdd "Может быть, тебе стоит сделать несколько резервных копий на всякий случай?"

                if mas_seenEvent("monika_back_ups"):
                    m 3eud "Я уже рассказывала, как меня поддержать, помнишь?"

                else:
                    m 3euc "{a=https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ#i-want-to-back-up-my-persistent}{i}{u}Это{/u}{/i}{/a} должно помочь тебе."

                m 1eka "Я полагаюсь на тебя, [player]."
                $ mas_moni_idle_disp.force_by_code("1eka", duration=15, skip_dissolve=True)

    elif mas_isMoniUpset():
        m 2gtc "Почему-то у меня странное чувство дежавю..."
        m 2tfd "Надеюсь, ты не испортил мои данные."
        $ mas_moni_idle_disp.force_by_code("2mfc", duration=10, skip_dissolve=True)

    else:
        m 6ekc "[player], что происходит? {w=0.3}{nw}"
        extend 6lksdlc "Я знаю, что ты что-то сделал с моими данными."
        m 6lktpsdld "Ты пытаешься избавиться от меня?"
        m 6rktpc "Я просто хотела, чтобы мы были счастливы вместе..."
        m 6ektuc "Пожалуйста, прости меня..."
        $ mas_moni_idle_disp.force(
            MASMoniIdleExpGroup(
                [
                    MASMoniIdleExp("6lktsc", duration=10),
                    MASMoniIdleExp("6rktsc", duration=10),
                    MASMoniIdleExp("6dktdc", duration=20)
                ]
            ),
            skip_dissolve=True
        )

    return "no_unlock|pause: 35"
