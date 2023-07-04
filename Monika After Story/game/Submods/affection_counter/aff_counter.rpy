
init -990 python:
    store.mas_submod_utils.Submod(
        author="Amanda Watson",
        name="Счётчик привязанности",
        description=(
            "Небольшая надстройка, которая, собственно, отображает счётчик и описание степени привязанности."
        ),
        version="1.0",
        settings_pane="aff_settings"
    )

init python:
    def count_affection(st, at):
        my_aff = int(_mas_getAffection())
        if my_aff < -100:
            my_aff = -100
        elif my_aff > 1000:
            my_aff = 1000
        # d = Text(f"Очки: {my_aff}", style="indicator_text") <-- не трогай, это на Новый год! :Д
        d = Text("Очки: " + str(my_aff), style="indicator_text")
        return d, 0.1

    def count_affection_desc(st, at):
        if _mas_getAffection() <= -100:
            c_aff_desc = "разбитое сердце"
        elif -100 <= _mas_getAffection() <= -75:
            c_aff_desc = "несчастная"
        elif -75 < _mas_getAffection() <= -30:
            c_aff_desc = "грустная"
        elif -30 < _mas_getAffection() < 30:
            c_aff_desc = "нормальная"
        elif 30 <= _mas_getAffection() < 100:
            c_aff_desc = "счастливая"
        elif 100 <= _mas_getAffection() < 400:
            c_aff_desc = "привязанная"
        elif 400 <= _mas_getAffection() < 1000:
            c_aff_desc = "влюблённая"
        else:
            c_aff_desc = "сильная любовь"
        # d = Text(f"Привязанность: {c_aff_desc}", style="indicator_text") <-- не трогай, это на Новый год! :Д
        d = Text("Привязанность: " + c_aff_desc, style="indicator_text")
        return d, 0.1

image aff_count = DynamicDisplayable(count_affection)
image aff_desc = DynamicDisplayable(count_affection_desc)

default persistent.should_show_counter = True

style indicator_text is default:
    color "#000"
    size 12
    outlines []
    xpos 22

style indicator_count_frame:
    background Frame("Submods/affection_counter/aff_points_overlay.png")
    xysize(104, 34)
style indicator_desc_frame:
    background Frame("Submods/affection_counter/aff_text_overlay.png")
    xysize(232, 34)

image aff_heart_icon_normal = "Submods/affection_counter/aff_heart_icon.png"
image aff_rose_icon_normal = "Submods/affection_counter/aff_rose_icon.png"
image aff_heart_icon_gray:
    "aff_heart_icon_normal"
    matrixcolor SaturationMatrix(0)
image aff_rose_icon_gray:
    "aff_rose_icon_normal"
    matrixcolor SaturationMatrix(0)

image aff_heart_icon = ConditionSwitch(
    "_mas_getAffection() <= -30", "aff_heart_icon_gray",
    "True", "aff_heart_icon_normal"
)
image aff_rose_icon = ConditionSwitch(
    "_mas_getAffection() <= -30", "aff_rose_icon_gray",
    "True", "aff_rose_icon_normal"
)

screen aff_screen():
    if persistent.should_show_counter:
        vbox:
            pos(30, 26)
            spacing 2
            frame:
                style "indicator_count_frame"
                add "aff_count"
            frame:
                style "indicator_desc_frame"
                add "aff_desc"
        vbox:
            pos(20, 20)
            spacing 4
            add "aff_heart_icon"
            add "aff_rose_icon"

screen aff_settings():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"

        # textbutton f"{'Скрыть' if persistent.should_show_counter else 'Показать'}" <-- не трогай, это на Новый год! :Д

        textbutton ("Скрыть" if persistent.should_show_counter else "Показать") action If(
            persistent.should_show_counter, SetVariable("persistent.should_show_counter", False), SetVariable("persistent.should_show_counter", True)
        )

init python:
    config.overlay_screens.append("aff_screen")
