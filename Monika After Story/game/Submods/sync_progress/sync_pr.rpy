
init -990 python:
    store.mas_submod_utils.Submod(
        author="Amanda Watson",
        name="Синхронизация прогресса",
        description=(
            "Небольшая надстройка для синхронизации прогресса «не отходя от кассы»."
        ),
        version="1.0",
        settings_pane="sync_settings"
    )

screen sync_settings():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"
        textbutton _("Загрузить на сервер") action UploadSync()
        textbutton _("Скачать с сервера") action DownloadSync()

style sync_label_text is confirm_prompt_text
style sync_text is confirm_prompt_text
style sync_button is confirm_button
style sync_button_text is confirm_button_text
