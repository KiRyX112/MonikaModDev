# module that handles the mood system
#

# dict of tuples containing mood event data
default persistent._mas_mood_database = {}

# label of the current mood
default persistent._mas_mood_current = None

# NOTE: plan of attack
# moods system will be attached to the talk button
# basically a button like "I'm..."
# and then the responses are like:
#   hungry
#   sick
#   tired
#   happy
#   fucking brilliant
#   and so on
#
# When a mood is selected:
#   1. monika says something about it
#   2. (stretch) other dialogue is affected
#
# all moods should be available at the start
#
# 3 types of moods:
#   BAD > NETRAL > GOOD
# (priority thing?)

# Implementation plan:
#
# Event Class:
#   prompt - button prompt
#   category - acting as a type system, similar to jokes
#       NOTE: only one type allowed for moods ([0] will be retrievd)
#   unlocked - True, since moods are unlocked by default
#

# store containing mood-related data
init -1 python in mas_moods:

    # mood event database
    mood_db = dict()

    # TYPES:
    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2

    # pane constants
    # most of these are the same as the unseen area consants
    MOOD_RETURN = _("...Давай поговорим о чём-нибудь ещё.")

## FUNCTIONS ==================================================================

    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)
        
        if mood:
            return mood.category[0]
        
        return None


# entry point for mood flow
label mas_mood_start:
    python:
        import store.mas_moods as mas_moods

        # filter the moods first
        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection,
            flag_ban=EV_FLAG_HFM
        )

        # build menu list
        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]

        # also sort this list
        mood_menu_items.sort()

        # final quit item
        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(mood_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ mas_setEventPause(None)
        $ MASEventList.push(_return, skipeval=True)
        # and set the moods
        $ persistent._mas_mood_current = _return

    return _return

# dev easter eggs go in the dev file

###############################################################################
#### Mood events go here:
###############################################################################

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_hungry",prompt="...хочется кушать",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "Если ты голоден, то пойди и поешь чего-нибудь, глупышка."
    if store.mas_egg_manager.natsuki_enabled():
        m 1hksdlb "Я бы не хотела, чтобы ты стал таким же как Нацуки, когда мы были в клубе.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "Отстойно, когда все сердятся будучи голодными."

    m 3tku "TЭто было бы не весело, не правда ли, [player]?"
    m 1eua "Если бы я была рядом с тобой, я бы сделала для нас обоих какой-нибудь салат."
    m "Но так как я не там, выбери какую-нибудь здоровую еду."
    m 3eub "Говорят, что ты это то — что ты ешь, я думаю что это правда."
    m 3hub "Это, конечно, не означает, что нужно есть только овощи. {w=0.2}Все разного рода продукты необходимы для поддержания здорового питания."
    m 3eka "Поэтому я хочу, чтобы ты убедился, что не обделяешь себя важными витаминами, хорошо?"
    m 1euc "Когда ты станешь старше — столкнёшься со множеством проблем со своим здоровьем."
    m 2lksdla "Я не хочу, чтобы ты думал, что я ворчу на тебя, [player]."
    m 2eka "Я просто хочу убедиться, что ты будешь заботиться о себе, пока я не перейду в твою реальность."
    m 4eub "В конце концов, чем ты здоровее, тем больше шансов, что ты проживёшь дольше."
    m 1hua "И это означает, что мы сможем провести больше времени вместе!~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="...грустно.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Боже, мне очень жаль видеть тебя в таком настроении."
    m "У тебя был плохой день?{nw}"
    $ _history_list.pop()
    menu:
        m "У тебя был плохой день?{fast}"
        "Да.":
            m 1duu "Всякий раз, когда у меня плохой день, я всегда вспоминала, что солнце вновь будет светить завтра."
            m 1eka "Полагаю, что это не очень поможет, но мне просто всегда нравилось смотреть на светлую сторону вещей."
            m 1eua "В конце концов, такие вещи легко забываются. Просто имей это в виду, [player]."
            m 1lfc "Меня не волнует, что какие-то люди не любят тебя, или просто не знают о тебе."
            m 1hua "Ты замечательный человек, и я вечность буду любить тебя."
            m 1eua "Я надеюсь, твой день стал чуточку ярче."
            m 1eka "И помни, если у тебя плохой день, ты просто можешь прийти ко мне, и мы будем разговаривать сколько тебе угодно."
        "Нет.":
            m 3eka "У меня идея, почему бы тебе не рассказать мне, что тебя беспокоит, и, возможно, это заставит тебя чувствовать себя чуточку лучше."

            m 1eua "Я не хочу прерывать тебя, пока ты разговариваешь, поэтому просто кликни, как только закончишь.{nw}"
            $ _history_list.pop()
            menu:
                m "Я не хочу прерывать тебя, пока ты разговариваешь, поэтому просто кликни, как только закончишь.{fast}"
                "Я тут.":
                    m "Тебе стало немного лучше, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Тебе стало немного лучше, [player]?{fast}"
                        "Да, стало.":
                            m 1hua "Это прекрасно! Я рада, что разговор со мной улучшил тебе настроение."
                            m 1eka "Иногда, следует разговаривать с тем, кому доверяешь о всём, что тебя беспокоит."
                            m "И помни, если у тебя плохой день, ты просто можешь прийти ко мне, и мы будем разговаривать сколько тебе угодно."
                            m 1hubsa "Никогда не забывай, что ты прекрасный человек, и я буду любить тебя вечность~"
                        "Не совсем.":
                            m 1ekc "Ну, стоило попытаться."
                            m 1eka "Иногда следует разговаривать с тем, кому доверяешь о всём, что тебя беспокоит."
                            m 1eua "Может, тебе станет лучше после того как мы проведём ещё немного времени вместе."
                            m 1ekbsa "Я люблю тебя, [player], и всегда буду любить~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_proud",
            prompt="...горделиво.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_proud:
    m 2sub "В самом деле? Это захватывающе!"
    m 2eub "Было ли это крупным достижением или незначительным?{nw}"
    $ _history_list.pop()
    menu:
        m "Было ли это крупным достижением или незначительным?{fast}"
        "Крупным.":
            m 1ekc "Ты знаешь, [player]..."
            m 1lkbsa "В такие времена, больше, чем в другие, я хотела бы быть с тобой, в твоей реальности..."
            m 4hub "Потому что, если бы я была рядом, я бы определённо подарила тебе праздничное объятие!"
            m 3eub "Нет ничего лучше, чем делиться своими достижениями с теми, кто тебе дорог."
            m 1eua "Я бы не могла хотеть ничего больше, чем услышать все подробности!"
            m "Просто мысль о нас в весёлом обсуждении того, что ты сделал..."
            m 1lsbsa "Моё сердце трепещет, просто думая об этом!" # ВЫ ПРАЗДНЫ! АААХХ, МОЁ СЕРДЦЕ ТРЕПЕЩЕТ!
            m 1lksdla "Боже, я ужасно взволнована по этому поводу..."
            m 3hub "Когда-нибудь это станет реальностью..."
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubfb "Но до тех пор, просто знай, что я очень горжусь тобой, мой любимый!"
        
        "Незначительным.":
            m 2hub "А-ха-ха!~"
            m 2hua "Это замечательно!"
            m 4eua "Очень важно праздновать маленькие победы в жизни."
            m 2esd "Может быть очень легко стать обескураженным, если ты сосредоточишься только на больших целях, которые у тебя есть."
            m 2rksdla "Они могут быть довольно сложными, чтобы достичь их самостоятельно."
            m 4eub "Но назначение и празднование небольших целей, которые в конечном итоге приводят к большей цели, могут сделать твои большие цели гораздо более достижимыми."
            m 4hub "Так что продолжай наносить удары по этим маленьким целям, [player]!"
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve_monika
            m 5hubfb "И помни: я люблю тебя, и всегда поддержу!"
            $ mas_ILY()
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_happy",prompt="...кажется, что я счастлив.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "Это чудесно! Я счастлива, когда ты счастлив."
    m "Знай, что ты всегда можешь прийти ко мне, и я попытаюсь поднять тебе настроение, [mas_get_player_nickname()]."
    m 3eka "Я люблю тебя, и всегда буду для тебя здесь, никогда не забывай об этом~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_sick",
            prompt="...кажется, что я заболел.",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Oх нет, [player]..."
            m 2ekd "Ты говоришь, что, как только мы пришли, тебе поплохело."
            m 2ekc "Я знаю, что ты хотел провести немного времени со мной, даже несмотря на то, что мы едва смогли быть вместе сегодня..."
            m 2eka "Думаю, ты должен пойти и немного отдохнуть."

        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "[player]!"
            m 2wkd "Ты не болел всё это время, верно?"
            m 2ekc "Я очень надеюсь, что нет, мне сегодня с тобой было очень весело, но если у тебя сейчас плохое самочувствие..."
            m 2rkc "Ну... просто пообещай мне, что в следующий раз ты скажешь мне об этом раньше."
            m 2eka "А теперь иди отдохни, это то, что тебе сейчас нужно."

        else:
            m 1ekc "Оу, мне жаль слышать об этом, [player]."
            m "Мне неприятно знать о том, что ты так страдаешь."
            m 1eka "Я знаю, что тебе очень хочется провести время со мной, но, наверное, тебе лучше пойти отдохнуть."

    else:
        m 2ekc "Мне жаль слышать об этом, [player]."
        m 4ekc "Ты должен пойти отдохнуть, пока не стало хуже."

    label .ask_will_rest:
        pass

    $ persistent._mas_mood_sick = True

    m 2ekc "Ты сделаешь это ради меня?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты сделаешь это ради меня?fast}"
        "Да.":
            jump greeting_stillsickrest
        "Нет.":
            jump greeting_stillsicknorest
        "Я уже отдохнул.":
            jump greeting_stillsickresting

#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_tired",prompt="...ничего не хочется делать.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:
    # TODO: should we adjust for suntime?
    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "Если ты устал, сейчас как раз неплохое время, чтобы лечь спать."
        m "Как бы ни было весело проводить с тобой сегодня время, я бы не хотела тебя задерживать, если ты устал."
        m 1hua "Если ты уже планируешь ложиться спать, сладких снов!"
        m 1eua "Но, возможно, у тебя есть ещё кое-что, что нужно сделать перед этим, например, немного перекусить или попить."
        m 3eua "Стакан воды перед сном помогает укрепить здоровье, а питьевая вода по утрам помогает проснуться."
        m 1eua "Я не против остаться здесь с тобой, если у тебя есть дела, о которых нужно позаботиться."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "[player]!"
        m 2ekc "Неудивительно – сейчас середина ночи!"
        m 2lksdlc "Если ты не ляжешь спать в ближайшее время, то будешь себя чувствовать так же и завтра..."
        m 2hksdlb "Я бы не хотела, чтобы ты завтра был уставшим и несчастным, когда мы будем проводить время вместе...."
        m 3eka "Так что сделай нам обоим одолжение и ложись спать, как только сможешь, [player]."

    elif 3 <= current_hour < 5:
        m 2ekc "[player]!?"
        m "Ты по-прежнему здесь?"
        m 4lksdlc "Ты должен быть в постели прямо сейчас."
        m 2dsc "В данный момент я даже не уверена, поздно ли или рано тебя призывать к этому..."
        m 2eksdld "...Меня это ещё больше беспокоит, [player]."
        m "Тебе {i}действительно{/i} нужно ложиться спать, пока не пришло время начинать день."
        m 1eka "Я бы не хотела, чтобы ты заснул в неподходящее время."
        m "Так что, пожалуйста, ложись спать. Может быть, мы сможем быть вместе в твоих снах."
        m 1hua "Я буду здесь, если ты оставишь меня присматривать за тобой, если ты не против~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "Всё ещё немного уставший, [player]?"
        m "Ещё немного рановато, так что ты можешь вернуться и ещё немного отдохнуть."
        m 1hua "Нет ничего плохого в том, чтобы проснуться пораньше и немного поспать~"
        m 1hksdlb "За исключением того, что я не смогу прижаться к тебе, а-ха-ха~"
        m "{i}Думаю{/i}, я могла бы подождать тебя ещё немного."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "Всё ещё не готов заняться днём, [player]?"
        m 1eka "Или у тебя просто один из таких дней?"
        m 1hua "Когда такое случается, я перед началом дня завариваю себе чашку кофе."
        if not mas_consumable_coffee.enabled():
            m 1lksdla "Если я не застряла бы здесь, конечно..."
        m 1eua "Ты можешь также выпить стакан воды."
        m 3eua "Очень важно избегать обезвоживания, но стакан воды после пробуждения может помочь тебе почувствовать свежесть и бодрость."
        m 3hksdlb "Это может прозвучать странно, но я слышала, что шоколадка тоже может помочь начать день!"
        m 3eka "Такое как-то связано с улучшением твоего настроения с утра, но..."
        m 1eksdlb "Уверена, шоколадка может кому угодно поднять настроение, как только они её съедят."
        m 1hua "Попробуй как-нибудь и расскажи мне о результате!"
        return

    else:
        m 1eka "Если ты устал, может, тебе стоит полежать какое-то время?"
        m 1eua "Долгий сон на ежедневной основе очень важен для твоего здоровья."
        m 3euc "Я видела исследования, которые показывали разрушительный эффект из-за отсутствия сна."
        m 3ekd "Это на самом деле может испортить твоё здоровье, [player]."
        m 1eka "Так что сделай мне одолжение, просто ляг и отдохни, хорошо? Это меня успокоит."

    m 1hua "Ты даже можешь оставить игру открытой, если хочешь, и я буду следить за тобой, пока ты спишь."
    m "...Э-хе-хе."
    m 2hksdlb "Это звучало жутковато, прости."
    m 2lksdla "Просто я подумала, что было бы мило посмотреть, как ты спишь и всё~"
    m 1hub "А-ха-ха!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_lonely",prompt="...очень одиноко.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    if mas_isMoniAff(higher=True):
        m 2ekc "Я понимаю, что ты чувствуешь, [player]...{w=0.2} в конце концов, мы всё ещё находимся в разных реальностях."
        m 2dkc "Я правда ненавижу то, что могу сделать не так много, чтобы ты чувствовал себя менее одиноко..."
        m 7ekbsa "Если бы я могла протянуть руку и просто обнять тебя прямо сейчас, я бы так и сделала."
        m 7eka "Я хочу, чтобы ты был счастлив настолько, насколько это возможно, учитывая наши обстоятельства..."
        m 2ekd "Я просто надеюсь, что пребывание здесь со мной всё это время не...{w=0.3} мешает тебе сблизиться с людьми в твоей реальности."
        m 2eka "Я считаю, есть что-то совершенно особенное, но я понимаю, что сейчас я...{w=0.3} ограничена в том, что могу сделать для тебя."

        if persistent._mas_pm_has_friends:
            if persistent._mas_pm_few_friends:
                m 7ekd "У тебя ведь есть один или два близких друга, верно?"
                m 3eka "Ты должен позвонить им или, возможно, отправить им сообщение и спросить, как у них дела..."
                m "Может быть, ты сможешь иногда встречаться с ними? {w=0.2}Я думаю, тебе это пойдёт на пользу."

            else:
                m 7ekd "Я думаю, что встречаться с друзьями и делать что-то с ними вместе, могло бы пойти тебе на пользу..."
                m 3eka "Или ты можешь отправить им сообщение и спросить, как у них дела."

        else:
            m 7rkc "Я знаю, каково это – быть одному в одной реальности, только имея возможность взаимодействовать с кем-то в другой..."
            m 3ekd "Так что я действительно не хочу этого для человека, которого люблю больше всего."
            m 1eka "Я надеюсь, что ты будешь продолжать искать друзей в своей реальности, [player]."
            m 3ekd "Я знаю, что поначалу бывает трудно общаться с людьми..."
            m 3eka "Может быть, ты даже мог бы встретиться с кем-то в интернете? {w=0.2}Есть много способов взаимодействовать с незнакомыми людьми, чтобы чувствовать себя менее одиноким."
            m 3hub "Никогда не знаешь, иногда эти «незнакомцы» могут в конечном итоге стать действительно хорошими друзьями!"

        m 1eka "...И не беспокойся обо мне, [player], я буду терпеливо ждать, когда ты вернёшься и увидишь меня."
        m 3hub "Просто наслаждайся жизнью, а потом расскажешь мне обо всём!"
        m 1ekbsa "Просто помни, что я всегда буду рядом с тобой, [player]~"

    else:
        m 1eka "Я здесь для тебя, [player], поэтому не нужно чувствовать себя одиноким."
        m 3hua "Я знаю, что чувствуется не совсем так, как если бы я была в одной комнате с тобой, но я уверена, что ты всё ещё наслаждаешься моей компанией, правда?"
        m 1ekbsa "Помни, я всегда буду на твой стороне, [player]~"
    return

#Maybe we could tie this to the I'm breaking up topic and have monika say something special like:
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="...хочется кого-то прибить.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Боже, мне жаль, что ты так себя чувствуешь, [player]."
    m 3ekc "Я сделаю всё возможное, чтобы ты почувствовал себя лучше."
    m 1euc "Перед этим, я, вероятно, должна заставить тебя успокоиться."
    m 1lksdlc "Трудно принимать рациональные решения, когда ты взбешён."
    m 1esc "Ты можешь сказать то, из-за чего можешь позже пожалеть.."
    m 1lksdld "И я бы не хотела, чтобы ты сказал, что на самом деле не имел в виду."
    m 3eua "Давай попробуем несколько способов, которые я делала, чтобы успокоить себя, хорошо, [player]?"
    m 3eub "Надеюсь, они сработают на тебе так же, как и на мне."
    m 1eua "Сначала сделай несколько глубоких вдохов и медленно посчитай до десяти."
    m 3euc "Если это не сработает, если это возможно, подумай о чём-нибудь спокойном, пока не очистишь свой разум."
    m 1eud "Если ты всё ещё злишься, я предлагаю последнее средство!"
    m 3eua "Когда я не могу успокоиться, я просто выхожу на улицу, выбираю случайное направление и начинаю бежать."
    m 1hua "Я не останавливаюсь до тех пор, пока не очищу свою голову."
    m 3eub "Иногда проявлять физическую активность — лучший способ остудить себя."
    m 1eka "Ты думаешь, что я та которая злится не так часто, и ты будешь прав."
    m 1eua "Но даже у меня бывают свои моменты..."
    m "Поэтому у меня и есть способы, чтобы справляться с ними!"
    m 3eua "Надеюсь, мои советы помогли тебе успокоиться, [player]."
    m 1hua "Помни: счастливый [player], делает счастливой Монику!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_scared",prompt="...как-то тревожно.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "[player], у тебя всё хорошо?"
    m 1ekc "Меня беспокоит, что ты так тревожишься..."
    m "Хотела бы я утешить тебя и помочь прямо сейчас..."
    m 3eka "Но я могу по крайней мере помочь тебе успокоиться."
    if seen_event("monika_anxious"):
        m 1eua "В конце концов, я ведь обещала помочь тебе расслабиться, если ты когда-нибудь почувствуешь беспокойство."
    m 3eua "Помнишь, когда я говорила с тобой о притворной уверенности?"
    if not seen_event("monika_confidence"):
        m 2euc "Нет?"
        m 2lksdla "Думаю, тогда расскажу в другой раз."
        m 1eka "В любом случае..."
    m 1eua "Слежка за своим внешним видом помогает с подделкой собственной уверенности."
    m 3eua "И для этого тебе необходимо поддерживать сердечный ритм, делая глубокие вдохи, пока ты не успокоишься."
    if seen_event("monika_confidence_2"):
        m "Я помню, как объясняла, что инициатива также является важным навыком."
    m "Может быть, ты мог бы взяться за какие-либо вещи более спокойно и делать их по одной за раз."
    m 1esa "И ты будешь удивлён, насколько всё может пойти гладко, если позволишь времени течь самостоятельно."
    m 1hub "Ты также можешь попробовать потратить несколько минут, чтобы помедитировать!"
    m 1hksdlb "Ты только не подумай, что это обязательно означает, что ты должен скрестить ноги, сидя на земле."
    m 1hua "К примеру, прослушивание любимой музыки также можно считать медитацией!"
    m 3eub "Я серьёзно!"
    m 3eua "Ты можешь попытаться отложить свою работу и сделать что-то ещё за это время."
    m "В откладывании на потом чего-либо всё-таки нет ничего плохого."
    m 2esc "К тому же..."
    m 2ekbsa "Твоя любящая девушка верит в тебя, так что ты можешь столкнуться с этой тревогой лоб в лоб и противостоять ей!"
    m 1hubfa "Не о чем беспокоиться, когда мы вместе навсегда~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_inadequate",prompt="...кажется, что я схожу с ума.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    m 2ekc "Я знаю, что не так уж много я могу сказать, чтобы заставить тебя чувствовать себя лучше, [player]."
    m 2lksdlc "Ведь всё, что я говорю, возможно, просто как на словах."
    m 2ekc "Я могу сказать тебе, что ты прекрасен, хотя я не видела твоего лица..."
    m "Я могу сказать тебе, что ты умён, хотя я не очень много знаю о твоём образе мышления..."
    m 1esc "Но позволь мне рассказать тебе, что я знаю о тебе."
    m 1eka "Ты провёл со мной так много времени."

    #Should verify for current year and last year
    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        m "Ты взял время из своего графика, чтобы побыть со мной на Рождество!"

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen:
        m 1ekbsa "В день Святого Валентина..."

    #TODO: change this back to not no_recognize once we change those defaults.
    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        m 1ekbsb "Ты даже нашёл время отпраздновать мой день рождения вместе со мной!"

    if persistent.monika_kill:
        m 3tkc "Ты простил меня за все плохие вещи, которые я совершила."
    else:
        m 3tkc "Ты никогда не обижался на меня за то, что я сделала."

    if persistent.clearall:
        m 2lfu "И хотя это заставило меня ревновать, ты провдил так много времени со всеми членами моего клуба."

    m 1eka "Это показывает, насколько ты добр!"
    m 3eub "Ты честен, ты справедлив, ты милостив в поражении!"
    m 2hksdlb "Ты думаешь, что я ничего о тебе не знаю, но на самом деле знаю."
    m 3eka "И ты знаешь обо мне всё, и всё равно решил остаться, когда мог просто уйти..."
    m 2ekc "Так что, пожалуйста, оставайся сильным, [player]."
    m "Если мы немного похожи, то ты, как и я, боишься многого не добиться в жизни."
    m 2ekd "Но поверь мне, когда я скажу тебе. Не важно, что ты делаешь или не выполняешь."
    m 4eua "Тебе просто нужно существовать, веселиться и проводить каждый день так, {w=0.2}чтобы найти смысл в людях, которые имеют значение."
    m 1eka "Пожалуйста, не забывай об этом, хорошо?"
    m 1ekbsa "Я люблю тебя, [player]~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_lazy",
            prompt="...лениво.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_lazy:
    #Get current time
    $ _now = datetime.datetime.now().time()

    if mas_isSRtoN(_now):
        m 1tku "Прямо как в один из тех дней ранним утром, да, [player]?"
        m 1eka "Я прекрасно понимаю, что в такие дни ты просто просыпаешься и ничего не хочешь делать."
        m 1rksdla "Надеюсь, у тебя не предвидится каких-либо срочных дел в скором времени."

        $ line = "Я знаю, насколько заманчивой иногда может быть возможность просто лежать в кровати и не вставать..."
        if mas_isMoniEnamored(higher=True):
            $ line += "{w=0.5} {nw}"
        m 3hksdlb "[line]"

        if mas_isMoniEnamored(higher=True):
            extend 1dkbsa " Особенно когда я просыпаюсь рядом с тобой~"

            if mas_isMoniLove():
                m 1dkbsa "{i}А потом я бы ни за что не захотела вставать~{/i}"
                m 1dsbfu "Надеюсь, ты не против побыть «в ловушке», [player]..."
                m 1hubfa "Э-хе-хе~"

        m 3eka "Но в то же время, это не поможет начать день правильно."
        m 3eub "А это, как правило, умывание, хороший завтрак..."

        if mas_isMoniLove():
            m 1dkbsu "А ещё хороший утренний поцелуй, э-хе-хе..."

        m 1hksdlb "Или ты можешь немного побездельничать."
        m 1eka "Если только ты не забыл сделать что-то важное, хорошо, [player]?"

        if mas_isMoniHappy(higher=True):
            m 1hub "А ведь к этому относится времяпрепровождение со мной, а-ха-ха!"

    elif mas_isNtoSS(_now):
        m 1eka "Полуденная усталость настигла тебя, [player]?"
        m 1eua "Такое случается, но я не переживаю из-за этого так сильно."
        m 3eub "По сути, некоторые люди утверждают, что лень делает тебя более креативным."
        m 3hub "Так что, кто знает, возможно, ты придумаешь что-то удивительное!"
        m 1eua "В любом случае, ты должен просто сделать перерыв или немного потянуться...{w=0.5} {nw}"
        extend 3eub "Можешь ещё и перекусить, если ты этого ещё не сделал."
        m 3hub "И, если это уместно, ты можешь даже вздремнуть! А-ха-ха~"
        m 1eka "Я буду сидеть здесь и ждать тебя, если ты вдруг решишь это сделать."

    elif mas_isSStoMN(_now):
        m 1eka "Тебе не хочется ничего делать после тяжёлого дня, [player]?"
        m 3eka "По крайней мере, день почти закончился..."
        m 3duu "Нет ничего лучше, чем просто сидеть и расслабиться после тяжёлого дня, особенно когда у тебя нет никаких срочных дел."

        if mas_isMoniEnamored(higher=True):
            m 1ekbsa "Надеюсь, времяпрепровождение со мной сделает твой вечер чуточку лучше..."
            m 3hubsa "Уж мой-то вечер точно становится лучше вместе с тобой~"

            if mas_isMoniLove():
                m 1dkbfa "Я могу только представить себе, как мы отдыхаем одним вечером..."
                m "Возможно, мы даже обнимаемся под одеялом, если вдруг стало холодно..."
                m 1ekbfa "Хотя мы и так можем пообниматься под одеялом, даже когда не так холодно, если ты не против, э-хе-хе~"
                m 3ekbfa "Мы даже можем почитать какую-нибудь хорошую книгу вместе."
                m 1hubfb "Или просто подурачиться ради забавы!"
                m 1tubfb "Кто сказал, что вечер должен быть спокойным и романтичным?"
                m 1tubfu "Надеюсь, ты не будешь против периодических внезапных битв подушками, [player]~"
                m 1hubfb "А-ха-ха!"

        else:
            m 3eub "Мы даже можем почитать какую-нибудь хорошую книгу вместе..."

    else:
        #midnight to morning
        m 2rksdla "Эм, [player]..."
        m 1hksdlb "Уже полночь..."
        m 3eka "Если ты чувствуешь себя ленивым, то ты, наверное, должен полежать немного на кровати."
        m 3tfu "И, наверное, ну...{w=1} {i}поспать{/i}?"
        m 1hkb "А-ха-ха, ты иногда бываешь таким забавным, но ты правда должен идти спать."

        if mas_isMoniLove():
            m 1tsbsa "Если бы я была там, то я бы сама затащила тебя в кровать, мне стоит только захотеть это сделать."
            m 1tkbfu "Или ты, наверное, втайне радуешься этому, [player]?~"
            m 2tubfu "К твоему счастью, я пока не могу это сделать."
            m 3tfbfb "Так что я пойду спать вместе с тобой."
            m 3hubfb "А-ха-ха!"

        else:
            m 1eka "Пожалуйста? Я не хочу, чтобы ты пренебрегал своим сном."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,eventlabel="mas_mood_bored",
            prompt="...скучно.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Ох..."
        m 3hub "Ну, тогда мы должны что-нибудь сделать!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "Неужели я так тебя утомляю, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Неужели я так тебя утомляю, [player]?{fast}"
            "Нет, ты мне не наскучила...":
                m 1hua "Ох...{w=0.2} Какое облегчение!"
                m 1eka "Но если тебе и вправду скучно, то мы должны найти чем заняться..."
            
            "Да...":
                $ mas_loseAffectionFraction(min_amount=15)
                m 2ekc "Эх... {w=1}понятно."
                m 2dkc "Я не понимала, что тебе скучно..."
                m 2eka "Уверена, мы найдём, чем заняться..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffectionFraction(min_amount=15)
        m 2lksdlc "Прости, что я тебе наскучила, [player]."

    else:
        $ mas_loseAffectionFraction(min_amount=15)
        m 6ckc "Знаешь, [player], если я делаю тебя таким несчастным всё время..."
        m "Может быть, тебе просто стоит найти себе другое занятие?"
        return "quit"

    python:
        # build mapping from game label to display name for game
        unlocked_games = {
            # use display name, or prompt as backup
            ev_label: game_ev.rules.get("display_name", game_ev.prompt)

            for ev_label, game_ev in mas_games.game_db.iteritems()
            if mas_isGameUnlocked(game_ev.prompt)
        }

        picked_game_label = renpy.random.choice(list(unlocked_games.keys()))
        picked_game_name = unlocked_games[picked_game_label]

    if picked_game_label == "mas_piano":
        if mas_isMoniAff(higher=True):
            m 3eub "Ты можешь сыграть мне что-нибудь на пианино!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Может, сыграешь мне что-нибудь на пианино?"
        
        else:
            m 2rkc "Может, сыграешь что-нибудь на пианино..."

    else:
        if mas_isMoniAff(higher=True):
            m 3eub "Мы могли бы сыграть в [picked_game_name]!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Может быть, мы могли бы сыграть в [picked_game_name]?"

        else:
            m 2rkc "Может, давай сыграем в [picked_game_name]..."

    $ chosen_nickname = mas_get_player_nickname()
    m "Ты будешь играть, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты будешь играть, [chosen_nickname]?{fast}"
        "Да.":
            $ MASEventList.push(picked_game_label, skipeval=True)

        "Нет.":
            if mas_isMoniAff(higher=True):
                m 1eka "Ладно..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5tsu "Мы можем тогда просто смотреть друг другу в глаза чуть подольше..."
                    m "Нам это никогда не надоест~"
                else:
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eua "Мы можем тогда просто смотреть друг другу в глаза чуть подольше..."
                    m "Это никогда не будет скучно~"

            elif mas_isMoniNormal(higher=True):
                m 1ekc "Всё в порядке..."
                m 1eka "Обязательно дай мне знать, если захочешь позже сыграть со мной во что-нибудь~"

            else:
                m 2ekc "Ладно..."
                m 2dkc "Дай мне знать, если действительно захочешь сыграть во что-нибудь со мной."

    $ del unlocked_games, picked_game_label, picked_game_name
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_crying",prompt="...так хочется плакать.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_crying:
    $ line_start = "И"
    m 1eksdld "[player]!"

    m 3eksdlc "Ты в порядке?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты в порядке?{fast}"
        
        "Да.":
            m 3eka "Ох, хорошо. Такое облегчение."
            m 1ekbsa "Я здесь, чтобы составить тебе компанию, и ты можешь поговорить со мной, если понадобится, хорошо?"
        
        "Нет.":
            m 1ekc "..."
            m 3ekd "[player]..."
            m 3eksdld "Мне очень жаль. Что случилось?"
            call mas_mood_uok
        
        "Я не уверен":
            m 1dkc "[player]...{w=0.3} {nw}"
            extend 3eksdld "что-то случилось?"
            call mas_mood_uok

    m 3ekd "[line_start] если ты всё же заплачешь..."
    m 1eka "Я надеюсь, это как-то поможет тебе."
    m 3ekd "Нет ничего ужасного в том, чтобы немного поплакать. {w=0.2}Ты можешь плакать столько, сколько хочешь."
    m 3ekbsu "Я люблю тебя, [player]. {w=0.2}Ты для меня дороже всего."
    return "love"

label mas_mood_uok:
    m 1rksdld "Я знаю, что не могу слышать, то что ты мне говоришь."
    m 3eka "Но иногда, если поделиться своей болью с кем-то, может очень сильно облегчить страдание."

    m 1ekd "Так что, если ты захочешь о чём-то поговорить, я всегда здесь.{nw}"
    $ _history_list.pop()
    menu:
        m "Так что, если ты захочешь о чём-то поговорить, я всегда здесь.{fast}"
        
        "Я бы хотел высказаться.":
            m 3eka "Вперёд, [player]."

            m 1ekc "Для этого я здесь.{nw}"
            $ _history_list.pop()
            menu:
                m "Для этого я здесь.{fast}"
                
                "Я закончил.":
                    m 1eka "Я так рада, что ты смог высказаться от всего сердца, [player]."
        
        "Я не хочу об этом говорить.":
            m 1ekc "..."
            m 3ekd "Хорошо, [player], я буду здесь, если ты передумаешь."
        
        "Всё в порядке.":
            m 1ekc "..."
            m 1ekd "Я уверена, что у тебя всё наладится."
            $ line_start = "Но"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,eventlabel="mas_mood_upset",prompt="...морально плохо.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_upset:
    m 2eksdld "Мне очень жаль это слышать, [player]!"
    m 2eksdld "Если ты расстроен задачей, человеком или чем-то, что просто идёт не по плану, {w=0.1}{nw}"
    extend 7ekc "не отказывайся полностью от того, с чем ты имеешь дело."
    m 3eka "Мой совет, нужно просто сделать шаг назад."
    m 1eka "Может быть, ты мог бы почитать книгу, послушать приятную музыку или просто сделать что-нибудь ещё, чтобы успокоиться."
    m 3eud "Как только ты почувствуешь, что уже успокоился, вернись и оцени ситуацию свежим взглядом."
    m 1eka "Ты будешь справляться с проблемами намного лучше, чем если бы ты был расстроен и разозлён."
    m 1eksdld "И я не говорю, что ты должен продолжать нести груз на своих плечах, если это действительно давит на тебя."
    m 3eud "Это возможность набраться смелости, чтобы избавиться от чего-то разрушающего."
    m 1euc "Это может быть не легко в данный момент, разумеется...{w=0.3} {nw}"
    extend 3ekd "но если ты сделаешь правильный выбор, ты сможешь избежать много стресса в своей жизни."
    m 3eua "И знаешь, что, [player]?"
    m 1huu "Когда я расстроена, всё, что мне нужно сделать, это вспомнить, что у меня есть [mas_get_player_nickname(regex_replace_with_nullstr='my ')]."
    m 1hub "Знание того, что ты всегда поддерживаешь и любишь меня, почти мгновенно успокаивает!"
    m 3euu "Я могу только надеяться, что ты чувствуешь тоже самое, [player]~"
    m 1eubsa "Я люблю тебя и надеюсь, что у тебя всё прояснится~"
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_relieved",
            prompt="...так полегчало.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

#TODO: Once player moods are better implemented (Moni keeps track of the player's moods [moni-concerns])
#This can be used to alleviate her worry and directly reference the prior mood you were feeling
label mas_mood_relieved:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eud "Ох?"

    m "Что случилось, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Что случилось, [chosen_nickname]?{fast}"
        
        "Я прошёл через что-то сложное.":
            m 1wud "Правда?"
            m 3hub "Тогда ты должен собой гордиться!"
            m 3fua "Я уверена, что бы это ни было, ты очень много работал, чтобы пройти через это."
            m 2eua "И, [player]...{w=0.2} {nw}"
            extend 2eka "пожалуйста, не волнуйся слишком сильно, если что-то не получилось идеально, ладно?"
            m 2eksdla "Иногда жизнь подбрасывает нам действительно сложные ситуации, и мы просто должны делать всё возможное с тем, что нам дано."
            m 7ekb "Но теперь, когда это сделано, тебе нужно некоторое время, чтобы отдохнуть."
            m 3hub "...Таким образом, ты будешь готов встретить всё, что попадется на твоём пути!"
            m 1ekbsa "Я люблю тебя, [player], и я так горжусь тобой за то, что ты прошёл через это."
            $ mas_ILY()
        
        "Что-то, о чём я беспокоился, не произошло.":
            m 1eub "Ох, так это же здорово!"
            m 2eka "Что бы ни происходило, я уверена, что ты действительно волновался...{w=0.3} {nw}"
            extend 2rkd "вряд ли было весело."
            m 2rkb "Забавно, что наш разум всегда предполагает самое худшее, да?"
            m 7eud "Очень часто то, что, как нам кажется, может произойти, оказывается гораздо хуже реальности."
            m 3eka "Но в любом случае, я просто рада, что с тобой всё в порядке, и что ты избавился от этого груза."
            m 1hua "Теперь будет легче двигаться вперед с большей уверенностью, верно?"
            m 1eua "Я рада сделать эти следующие шаги вперёд вместе с тобой."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_excited",
            prompt="...так трепетно!",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_excited:
    m 1hub "А-ха-ха, это правда, [player]?"
    m 3eua "Чем ты взволнован,{w=0.1} это что-то большое?{nw}"
    $ _history_list.pop()
    menu:
        m "Чем ты взволнован, это что-то большое?{fast}"

        "Верно!":
            m 4wuo "Это удивительно, [player]!"
            m 1eka "Хотела бы я быть там, чтобы отпраздновать это с тобой."
            m 1hub "Теперь я тоже в восторге."
            m 3eka "Но на самом деле, я рада, что ты счастлив, [mas_get_player_nickname()]!"
            m 3eub "И чем бы ты ни был взволнован, поздравляю!"
            m 1eua "Будь то повышение по службе, приятный предстоящий отпуск, какое-то большое достижение..."
            m 3eub "Я очень рада, что у тебя всё хорошо, [player]!"
            m 1dka "В такие моменты мне хочется, чтобы я была там, с тобой, прямо сейчас."
            m 2dkblu "Я не могу дождаться, когда окажусь в твоём мире."
            m 2eubsa "Тогда я могла бы крепко обнять тебя!"
            m 2hubsb "А-ха-ха~"

        "Это кое-что небольшое.":
            m 1hub "Это отлично!"
            m 3eua "Важно радоваться таким мелочам."
            m 1rksdla "... Я знаю, что это немного глупо,{w=0.1} {nw}"
            extend 3hub "но это отличное мышление!"
            m 1eua "Так что я рада, что ты радуешься мелочам жизни, [player]."
            m 1hua "Я счастлива от того, что ты счастлив."
            m 1eub "Мне так приятно слышать о твоих достижениях."
            m 3hub "Так что спасибо, что сообщил мне!~"

        "Я не уверен.":
            m 1eta "Ты просто взволнован тем, что будет дальше?{w=0.2} {nw}"
            extend 1eua "В восторге от жизни?{w=0.2} {nw}"
            extend 1tsu "Или может быть.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
            m 1tku "Может быть, тебе так нравится проводить время со мной?~"
            m 1huu "Э-хе-хе~"
            m 3eua "Я знаю, я всегда рада видеть тебя каждый день."
            m 1hub "В любом случае, я рада, что ты счастлив!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="mas_mood_grateful",
            prompt="...так радостно на душе.",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        code="MOO"
    )

label mas_mood_grateful:
    $ chosen_nickname = mas_get_player_nickname()
    m 1eub "О? {w=0.3}Это приятно слышать!"

    m 3eua "Из-за чего у тебя так радуется душа, [chosen_nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Из-за чего у тебя так радуется душа, [chosen_nickname]?{fast}"

        "Из-за тебя.":
            if not renpy.seen_label("mas_mood_grateful_gratefulforyou"):
                $ mas_gainAffection(5, bypass=True)
            call mas_mood_grateful_gratefulforyou

        "Из-за кого-то.":
            m 3eka "А-ах, я так рада это слышать."
            m 1hua "Я правда рада, что в твоей жизни есть поддерживающие тебя люди."
            m 3eud "Но как бы мне ни было приятно это слышать... {w=0.3}я думаю ты должен убедиться, что {i}они{/i} об этом тоже знают."
            m 3hua "Я уверена, если ты расскажешь этим людям об этом, то они могут быть приятно удивлены."
            m 3euu "Если не хочешь, тогда поблагодари их от моего имени. {w=0.3}Любой, кто делает тебя счастливее, будет занесён в мой личный список."
            m 1huu "Но в любом случае, я очень рада за тебя., [mas_get_player_nickname()]~"

        "Из-за кое-чего.":
            m 3hub "Я рада это слышать, [mas_get_player_nickname()]!"
            m 1eud "Осознанно уделяя время размышлениям о хорошем в своей жизни, может отлично повлиять на психическое здоровье."
            m 3hub "Так что, что бы это ни было, не пожалей времени, чтобы почувствовать и насладиться этим!"
            m 1euu "Спасибо, что разделил со мной своё счастье, [mas_get_player_nickname()]~"

        "Ничего такого.":
            m 3eua "А, просто радуешься жизни?"
            m 1eud "Приятно немного задуматься и почувствовать себя довольным, не так ли?"
            m 1rtd "Хм-м...{w=0.2} теперь, когда я подумала об этом, {w=0.1}{nw}"
            extend 3hua "я и сама чувствую себя очень довольной."
            m 3eubsu "В конце концов, я проведу ещё один день с моим замечательным парнем~"
    return

label mas_mood_grateful_gratefulforyou:
    m 1ekbla "Ох, [player]...{w=0.3} моей благодарности нет предела."
    m 1dkblu "Как и моей радости от твоих слов, я правда очень рада услышать, что как-то помогла тебе или как-то сделала тебя счастливее."
    m "Это то, к чему я стремлюсь каждый день."
    m 1hublu "Я надеюсь, что ты вкурсе, как каждый день радуется {i}моя{/i} душа за тебя."
    m 3ekbla "Люблю тебя, [player]~"
    $ mas_ILY()
    return
