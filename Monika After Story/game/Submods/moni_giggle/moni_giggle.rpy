init -990 python:
    store.mas_submod_utils.Submod(
        author="Amanda Watson",
        name="Смех Моники",
        description=(
            "Небольшая надстройка для озвучивания смеха Моники во время её диалогов."
        ),
        version="1.0",
        settings_pane="giggle_settings"
    )

init python:
    def giggle_tag(tag, argument):
        if persistent.monika_should_giggle:
            renpy.music.play(audio.moni_giggle, "sound")
        return [(renpy.TEXT_TEXT, "")]

    config.self_closing_custom_text_tags["do_giggle"] = giggle_tag

define audio.moni_giggle = "Submods/moni_giggle/giggle.ogg"

default persistent.monika_should_giggle = True

screen giggle_settings():
    vbox:
        style_prefix "check"
        textbutton (_("Включён") if persistent.monika_should_giggle else _("Выключен")) action ToggleVariable("persistent.monika_should_giggle", True, False)
