init -990 python:
    store.mas_submod_utils.Submod(
        author="Amanda Watson",
        name="Учёт местоимений",
        description=(
            "Небольшая надстройка для учёта местоимений в русской локализации."
        ),
        version="1.0"
    )

init python:
    def male_tag(tag, argument):
        if persistent.gender == "M":
            return [(renpy.TEXT_TEXT, argument)]
        return [(renpy.TEXT_TEXT, "")]

    def female_tag(tag, argument):
        if persistent.gender == "F":
            return [(renpy.TEXT_TEXT, argument)]
        return [(renpy.TEXT_TEXT, "")]

    config.self_closing_custom_text_tags["M"] = male_tag
    config.self_closing_custom_text_tags["F"] = female_tag
