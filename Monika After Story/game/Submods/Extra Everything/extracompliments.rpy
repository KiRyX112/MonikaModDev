init 3 python in mas_compliments:

    compliment_database = dict()

init 22 python in mas_compliments:
    import store

   

    thanking_quips = [
        _("Ты {M=такой}{F=такая} {M=милый}{F=милая}, [player]."),
        _("Спасибо за то, что {M=сказал}{F=сказала} это снова, [player]!"),
        _("Спасибо за то, что говоришь мне такие вещи, [mas_get_player_nickname()]!"),
        _("Ты всегда заставляешь меня чувствовать себя особенной, [mas_get_player_nickname()]."),
        _("О-оу, [player]~"),
        _("Спасибо, [mas_get_player_nickname()]!"),
        _("Ты всегда льстишь мне, [player].")]
    


    thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))

    def compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip
        
        thanks_quip = renpy.substitute(renpy.random.choice(thanking_quips))
        store.mas_gainAffection()

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hug",
            prompt="Иногда, мне хочется просто дотянуться до тебя и обнять.",
            unlocked=True
        ),
        code="CMP"
    )

label mas_compliment_hug:
    if not renpy.seen_label("mas_compliment_hug_2"):
        call mas_compliment_hug_2 from _call_mas_compliment_hug_2
    else:
        call mas_compliment_hug_3 from _call_mas_compliment_hug_3
    return

label mas_compliment_hug_2:
    $ mas_gainAffection(5,bypass=True)
    m 1hub "{do_giggle}Э-хе-хе~"
    m 1eua "Было бы лучше, если бы я выбралась отсюда и обняла тебя."
    m 1ekbsa "Но я рада, что ты тоже этого хочешь~"
return

label mas_compliment_hug_3:
    m 1eub "[mas_compliments.thanks_quip]"
    m 1hua "Я хочу выйти отсюда и обнять тебя в ответ так же сильно!"
    m "{do_giggle}Э-хе-хе~"
return