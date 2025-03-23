init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_renai_circulation",
            prompt="Циркуляция Ренаи",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_renai_circulation:
    m 1hubsb "{i}~Спасибо вам, Звёзды, за то что дали мне~{/i}"
    m 1ekbsa "{i}~Наилучший подарок, что может быть~{/i}"
    m 1dkbsa "{i}~И мне всё равно, если судьба играет со мной~{/i}"
    m 1hubsb "{i}~Я всё равно счастлива~{/i}"
    m 1hubsa "{do_giggle}А-ха-ха~"
    m 1eubsb "В Японской версии припева этой песни в первой строке говорится что-то вроде \"Спасибо, Бог, что дал мне\"."
    m 1rubsd "Я всё ещё скептически отношусь к тому, есть ли на этом свете Бог.."
    m 1hubsa "Но если он есть, то я счастлива что он дал мне тебя."
    m 1esbsb "Даже если это была просто игра судьбы."
    m 1hubsa "Но я знаю, что это не так."
return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_guilty_kiss",
            prompt="Поцелуй Вины",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_guilty_kiss:
    m 1efbsa "{i}~Тебе не убежать!~{/i}"
    m 3hubsb "{i}~В затворнический мир, где нас только двое~{/i}"
    m 1tfbsu "{i}~Нет нужды ни в ком другом~{/i}"
    m 1hubsb "{i}~Я хочу, чтобы ты попробовал сказать, что любишь меня... Я хочу~{/i}"
    m 1hubsa "{do_giggle}А-ха-ха~"
    m 1eubsb "Разве эта песня не напоминает тебе о том, что произошло между нами?"
    m 5hubsa "Мы действительно закрылись в мире, где есть только мы двое~"
return