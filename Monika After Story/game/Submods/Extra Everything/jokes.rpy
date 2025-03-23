#init 5 python: #Саша, почини пожалуйста
   # addEvent(Event(persistent.event_database,eventlabel="monika_randomjokes",category=["разное"],prompt="Расскажешь шутку?",pool=True,unlocked=True))

label monika_randomjokes:
    $ joke = renpy.random.randint(1)

    m 1eua "Хочешь чтобы я рассказала тебе шутку, [player]?"
    m 1eub "Дай-ка подумать."
    m 1duc "М-м-м..."
    m 3eub "Я знаю одну!"

    if joke == 1:
        m 1eua "Ты знаешь адвоката который выиграл дело благодаря вину?"
        m 1tub "Он сказал что его клиент был {i}не-вино-вен!{/i}"
        m 1hua "{do_giggle}Э-хе-хе~"
    if joke == 2:
        m 1eua "Почему цифра 6 боится цифры 7?"
        m 1tub "Потому что {i}7 съела 9!{/i}"
        m 1hua "{do_giggle}Э-хе-хе~"
return