init -2 python:
    os_blk = False
    import platform, subprocess
    macos_build = str(platform.mac_ver()[0])
    ten_platforms = ["10240", "14393", "17763", "19042", "19043", "19044", "19045"]
    user_dir = os.environ["ANDROID_PUBLIC"] if renpy.android else config.basedir
    if renpy.windows:
        try:
            svc_st = subprocess.check_output("sc query Winmgmt", universal_newlines=True, shell=True).strip().split("\n")[2]
            if not "running" in svc_st.lower():
                subprocess.check_output("sc start Winmgmt", shell=True)
        except:
            open(config.basedir+"/test_err.txt", "w").write("""Не удалось запустить службу "Инструментарий управления Windows".

Попробуйте запустить "DDLC.exe"/"DDLC-32.exe" от имени администратора. Если эта ошибка появится вновь, попробуйте запустить указанную службу вручную: https://ru.stackoverflow.com/a/770247
""")
            os.startfile(config.basedir+"/test_err.txt")
            subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
        if "\\u" in os.environ["USERNAME"].encode("unicode-escape") or "\\u" in config.basedir.encode("unicode-escape"):
            open(config.basedir+"/username_err.txt", "w").write("""В имени пользователя или директории игры обнаружена кириллица.

Ren'Py на данный момент времени испытывает проблемы с ANSI-кодировкой, используемой ОС Windows для обработки кириллических знаков, из-за чего возникают проблемы с использованием механизма сохранений, в связи с чем запуск игры был прекращён.
Пожалуйста, создайте вторую учётную запись с именем *на латинице, без специальных символов*, желательно без знаков препинания; и обязательно задайте пароль, сойдёт даже банальщина а-ля 0000; в Контрольных вопросах можно написать всякую несуразицу.
После этого зажмите клавишу Shift, нажмите Правой кнопкой мыши по исполняемому файлу и выберите Запуск от имени другого пользователя.

Во втором же случае, пожалуйста, переместите папку игры в другую папку, имя которой *состоит только из латиницы*.
""")
            os.startfile(config.basedir+"/username_err.txt")
            subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
        try:
            import codecs
            pc_model, pc_manufacturer = [
                line.strip()
                for line in subprocess.check_output(
                    " && ".join((
                        "wmic computersystem get model",
                        "wmic computersystem get manufacturer"
                    )),
                    shell=True
                ).decode("utf16").strip().split("\n")
                if line
            ][1::2]
            for i in pc_model, pc_manufacturer:
                i = codecs.decode(i, "utf8")
            if "wine" in (pc_model.lower(), pc_manufacturer.lower()): subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
        except ValueError:
            ten_version, pc_model, pc_manufacturer = [
                line.strip()
                for line in subprocess.check_output(
                    " && ".join((
                        "wmic os get buildnumber",
                        "wmic computersystem get model",
                        "wmic computersystem get manufacturer"
                    )),
                    universal_newlines=True,
                    shell=True
                ).split("\n")
                if line
            ][1::2]
            if "virtual" in pc_model.lower() or any(i in pc_manufacturer.lower() for i in ("qemu", "innotek", "oracle", "vmware")): subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
            import codecs
            activation_status = subprocess.check_output(
                "cscript /nologo \"C:\Windows\System32\slmgr.vbs\" /dli",
                shell=True
            ).decode("cp866").strip().replace("\r","").split("\n")[3]
            activation_status_ru = codecs.decode(activation_status, "utf8")
            activation_status_en = subprocess.check_output(
                "cscript /nologo \"C:\Windows\System32\slmgr.vbs\" /dli",
                shell=True
            ).decode("utf8").strip().replace("\r","").split("\n")[3]
    elif renpy.linux:
        pc_manufacturer = subprocess.check_output("cat /sys/devices/virtual/dmi/id/sys_vendor", universal_newlines=True, shell=True).strip()
        if any(i in pc_manufacturer.lower() for i in ("qemu", "innotek", "oracle", "vmware")):
            aa = subprocess.check_output("pidof DDLC", universal_newlines=True, shell=True).strip()
            subprocess.check_output("kill -9 "+aa, shell=True)
    elif renpy.macintosh:
        mac_fw_ver = subprocess.check_output("system_profiler SPHardwareDataType | awk '/System/ {print $4}'", universal_newlines=True, shell=True).strip()
        mac_sn_ver = subprocess.check_output("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'", universal_newlines=True, shell=True).strip()
        mac_rom_ver = subprocess.check_output("system_profiler SPHardwareDataType | awk '/Apple/ {print $4}'", universal_newlines=True, shell=True).strip()
        if mac_rom_ver and any(i in mac_rom_ver.lower() for i in ("vm", "welcome")): renpy.quit()
        if "vm" in [mac_fw_ver.lower(), mac_sn_ver.lower()]: renpy.quit()
    elif renpy.android:
        cpu = subprocess.check_output((
            "getprop", "ro.product.cpu.abilist"
        )).strip().decode("utf8")
        model = subprocess.check_output((
            "getprop", "ro.product.model"
        )).strip().decode("utf8")
        manufacturer = subprocess.check_output((
            "getprop", "ro.product.manufacturer"
        )).strip().decode("utf8")
        name = subprocess.check_output((
            "getprop", "ro.board.platform"
        )).strip().decode("utf8")
        version = subprocess.check_output((
            "getprop", "ro.build.version.sdk"
        )).strip().decode("utf8")
        if name in ["android-x86", "rpi"] and "virtual" in model or any(
            i in manufacturer for i in ("qemu", "innotek", "oracle", "vmware")
        ) or ("x86" in cpu and name not in ["android-x86", "rpi"]):
            renpy.quit()
        if version < "28": os_blk = True
    if renpy.windows and (platform.release() in ["Vista", "8"] or platform.release() == "7" and ten_version != "7601") or renpy.macintosh and int(macos_build[3:5]) < 15 and int(macos_build[:2]) <= 10: subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
    if renpy.windows and platform.release() == "10" and ten_version.startswith("2") and ten_version < "22000": subprocess.check_output("taskkill /fi \"WINDOWTITLE eq Моника: Эпилог\" /f", shell=True)
    if renpy.windows:
        if platform.release() == "10":
            os_blk = False if ten_version >= "22000" or ten_version in ten_platforms else True
        if not os_blk:
            os_blk = False if "имеет лицензию" in activation_status_ru or "Licensed" in activation_status_en else True
    if os_blk:
        config.keymap["skip"] = []
        config.keymap["toggle_skip"] = []
        config.keymap["fast_skip"] = []
    if renpy.android and "game" in os.listdir(user_dir):
        import shutil
        shutil.rmtree(user_dir+"/game")
        open(user_dir+"/Прочитай.txt", "w").write("Чел, прекрати страдать хуйнёй и поставь нативный порт.")
        renpy.quit()
    if os.path.isfile(config.basedir+"/test_err.txt"): os.remove(config.basedir+"/test_err.txt")
    if os.path.isfile(config.basedir+"/username_err.txt"): os.remove(config.basedir+"/username_err.txt")

init python:
    yaru = {"default" : [("gui/mouse/yaru/yaru_arrow.png", 7, 7)], "hand" : [("gui/mouse/yaru/yaru_hand.png", 12, 6)], "drag" : [("gui/mouse/yaru/yaru_drag.png", 17, 16)]}
    config.mouse = yaru if not renpy.android else None

define config.atl_start_on_show = False
define config.gl2 = True

# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
