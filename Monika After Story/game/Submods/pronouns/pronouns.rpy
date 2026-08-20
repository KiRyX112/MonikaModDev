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
    def set_his_her1():
        if persistent.gender == "M":
            return "Его"
        return "Её"
    def set_his_her2():
        if persistent.gender == "M":
            return "ним"
        return "ней"
    def set_his_her3():
        if persistent.gender == "M":
            return "он"
        return "она"
    def set_his_her4():
        if persistent.gender == "M":
            return "ему"
        return "ей"
    def male_tag(tag, argument):
        if persistent.gender == "M":
            return [(renpy.TEXT_TEXT, argument)]
        return []

    def female_tag(tag, argument):
        if persistent.gender == "F":
            return [(renpy.TEXT_TEXT, argument)]
        return []

    config.self_closing_custom_text_tags["M"] = male_tag
    config.self_closing_custom_text_tags["F"] = female_tag
    def moni_nickname_cleanup():
        return persistent._mas_monika_nickname.capitalize().replace("Моя ", "").replace("Моё ", "").replace("Мой ", "").capitalize()