init python:
    class Poem:
        def __init__(self, author="", title="", text="", yuri_2=False, yuri_3=False):
            self.author = author
            self.title = title
            self.text = text
            self.yuri_2 = yuri_2
            self.yuri_3 = yuri_3

    poem_m1 = Poem(
    author = "monika",
    title = "Дыра в стене",
    text = """\
Это не могла сделать я.
Видишь, шпаклёвка выступает сюда?
Шумный сосед? Парень сердитый? Мне не узнать. И дом был закрытый.
Я внутрь заглянуть решила, чтобы узнать, в чём же причина.
О нет! Я ослепла! Испорчена, как фотоплёнка от солнечного света.
Но уже слишком поздно.
Выжженную в сетчатке глаз картину бессмысленную забыть невозможно.
Всего лишь маленькая дырочка, - она не была слишком яркой.
Но была глубокой такой, что меня поглотила залпом.
Тянулась, бесконечно уходя, во все и вся.
Дыра возможностей, которым нет конца.
И я осознала, что смотрела не внутрь.
Я выглянула наружу, поняв всё про себя.
А он с другой стороны глядел на меня."""
    )

    poem_m21 = Poem(
    author = "monika",
    title = "Дыра в стене",
    text = """\
Однако он смотрел не на меня.
Запутанная, я отчаянно оглядываюсь вокруг себя.
Но мои обожжённые глаза не смогут больше различать цвета.
Есть ли другие в этой комнате? Они ведь тоже говорят, да?
Или это просто стихи на плоских бумаги листах,
Чьи звуки безумного скрипа творят какофонию у меня в ушах?
Комната начинает сужаться.
Всё меньше пространства оставляться.
Воздух, не доходя до лёгких, рассеивается, удушаться.
Я в панике мечусь. Выход найти хочу.
Он прямо здесь. Под рукой.

Подавив страхи все, я перо беру и пишу стих свой."""
    )

    poem_m3 = Poem(
    author = "monika",
    title = "Леди Которая Знает Всё",
    text = """\
Есть одна повесть, что как мир стара.
То сказ о странствующей леди, передающийся из уст в уста.
Леди, которой всё известно.
Леди, которая нашла ответы на вопросы повсеместные,
Весь смысл бытия,
Всю жизни суть,
Всё, что когда-то отыскать пытались.

И вот он я,


              перо


Потерянная жертва беззащитная, гонимая потоками ветров.

День за днём я ищу её без отдыха и снов.
Ищу, почти надежду потеряв, зная, что верою в легенды я не прав.
Но, когда прахом обратились все мои попытки,
Когда у остальных я наблюдал лишь спины да затылки,
Легенда - моя единственная надежда не растаявшая, - последняя тусклая звезда, в чёрном небе мерцающая.

И вот однажды ветер перестал.
Я опускаться быстро стал.
Я падал неизвестности навстречу, как мне казалось, целую вечность.
Как писчее перо по бумаге плывя.
Сухо выводящее безликие слова.

Тут меня двумя пальцами поймала чья-то рука.
Прекрасной леди принадлежала она.
Я взглянул в глаза деве и утонул в её взгляда бездне.

Леди Которая Знает Всё догадалась о моих мыслях.
Прежде чем я спросил, она прошептала пусто и близко:
«Я нашла все ответы, но цена им ничто.
Нет в мире смысла.
И цели давно.
Мы лишь невозможное пытаемся найти.
Я не легенда,
Её не существует, и нам не по пути».

Лёгким дыханием она меня обратно в полёт отправила, а там порыв ветра меня подобрал, унося в далёкие дали."""
    )

    poem_m2 = Poem(
    author = "monika",
    title = "Спаси меня",
    text = """\
Цвета, они не останавливаются.
Яркие, прекрасные цвета
Мерцают, взрываются, пронзают
Красный, зелёный, синий
Бесконечная
какофония
Бессмысленного
шума

Шум, он не прекращается.
Безумные, грохочущие волны
Пищат, визжат, пронзают
Синус, косинус, тангенс
    Как играть с пластинкой на диджей-вертушке
        Как проигрывать винил на холодной пицце
Бесконечный
стих
Бессмыслицы\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
Загрузи меня
"""
    )

    poem_m4 = Poem(
    author = "monika",
    title = "Счастливый конец",
    text = """\
С пером в руке я нахожу в себе силы.
А мужеством моя единственная любовь меня наделила.
Давай же вместе разберём этот мир, он и так разрушен,
И напишем роман из фантазий, какой нам двоим будет нужен.

Со взмахом пера путь находит свой заблудшая душа
В мире возможностей бескрайних узреть этот особый день тебе пора.

В конце концов,
Не всё хорошее должно заканчиваться."""
    )

image paper = "images/bg/poem.jpg"
image paper_glitch = LiveComposite((1280, 720), (0, 0), "paper_glitch1", (0, 0), "paper_glitch2")
image paper_glitch1 = "images/bg/poem-glitch1.png"
image paper_glitch2:
    "images/bg/poem-glitch2.png"
    block:
        yoffset 0
        0.05
        yoffset 20
        0.05
        repeat


transform paper_in:
    truecenter
    alpha 0
    linear 1.0 alpha 1

transform paper_out:
    alpha 1
    linear 1.0 alpha 0

screen poem(currentpoem, paper="paper"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        if currentpoem.author == "yuri":
            if currentpoem.yuri_2:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "yuri_text"
            elif currentpoem.yuri_3:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "yuri_text_3"
            else:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "yuri_text"
        elif currentpoem.author == "sayori":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "sayori_text"
        elif currentpoem.author == "natsuki":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "natsuki_text"
        elif currentpoem.author == "monika":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "monika_text"
        null height 100
    vbar value YScrollValue(viewport="vp") style "poem_vbar"



style poem_vbox:
    xalign 0.5
style poem_viewport:
    xanchor 0
    xsize 720
    xpos 280
style poem_vbar is vscrollbar:
    xpos 1000
    yalign 0.5

    ysize 700





style yuri_text:
    font "gui/font/y1.ttf"
    size 32
    color "#000"
    outlines []

style yuri_text_2:
    font "gui/font/y2.ttf"
    size 40
    color "#000"
    outlines []

style yuri_text_3:
    font "gui/font/y3.ttf"
    size 18
    color "#000"
    outlines []
    kerning -8
    justify True

style natsuki_text:
    font "gui/font/n1.ttf"
    size 28
    color "#000"
    outlines []
    line_leading 1

style sayori_text:
    font "gui/font/s1.ttf"
    size 34
    color "#000"
    outlines []

style monika_text:
    font "gui/font/m1.ttf"
    size 34
    color "#000"
    outlines []

label showpoem(poem=None, music=True, track=None, revert_music=True, img=None, where=i11, paper=None):
    if poem == None:
        return
    play sound page_turn
    if music:
        $ currentpos = get_pos()
        if track:
            $ audio.t5b = "<from " + str(currentpos) + " loop 4.444>" + track
        elif poem == poem_m5:
            $ audio.t5b = "<from " + str(currentpos) + " loop 4.444>mod_assets/bgm/5_monika2.ogg"
        else:
            $ audio.t5b = "<from " + str(currentpos) + " loop 4.444>bgm/5_" + poem.author + ".ogg"
        stop music fadeout 2.0
        $ renpy.music.play(audio.t5b, channel="music_poem", fadein=2.0, tight=True)
    window hide
    if paper:
        show screen poem(poem, paper=paper)
    else:
        show screen poem(poem)
    if not persistent.first_poem:
        $ persistent.first_poem = True
        show expression "gui/poem_dismiss.png" as poem_dismiss:
            xpos 1050 ypos 590
    with Dissolve(1)
    $ pause()
    if img:
        $ renpy.hide(poem.author)
        $ renpy.show(img, at_list=[where])
    hide screen poem
    hide poem_dismiss
    with Dissolve(.5)
    window auto
    if music and revert_music:
        $ currentpos = get_pos(channel="music_poem")
        $ audio.t5c = "<from " + str(currentpos) + " loop 4.444>bgm/5.ogg"
        stop music_poem fadeout 2.0
        $ renpy.music.play(audio.t5c, fadein=2.0)
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
