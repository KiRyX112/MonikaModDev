init -990 python in mas_submod_utils:
    Submod(
        author="Friends of Monika",
        name="Утилита для автозапуска",
        description="Моника будет встречать тебя с каждым включением ПК",
        version="1.1.9"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MAS Autostart Mod",
            user_name="friends-of-monika",
            repository_name="mas-autostart",
            extraction_depth=3
        )