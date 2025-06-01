init -990 python in mas_submod_utils:
    awc_submod = Submod(
        author="multimokia and Legendkiller21",
        name="Автоматическая погода",
        description="Эта надстройка позволяет погоде и времени суток в классе Моники совпадать с вашей.",
        version="2.0.7",
        settings_pane="auto_atmos_change_settings"
    )

init -989 python in awc_utils:
    import store

    #Register the updater if needed
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod=store.mas_submod_utils.awc_submod,
            user_name="multimokia",
            repository_name="MAS-Submod-Auto-Atmos-Change",
            tag_formatter=lambda x: x[x.index('_') + 1:],
            update_dir="",
            attachment_id=None,
        )
