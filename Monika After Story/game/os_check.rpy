image birdy = "/images/epicfail/birdy.png"
image birdy_dancing = Movie(play="/images/epicfail/birdy_dancing.ogv")
image bg Android_5 = "/images/os/Android5.png"
image bg Android_6 = "/images/os/Android6.png"
image bg Android_7 = "/images/os/Android7.png"
image bg Android_8 = "/images/os/Android8.png"
image bg Android_9 = "/images/os/Android9.png"
image bg Android_10 = "/images/os/Android10.png"
image bg Windows_7 = "/images/os/Windows7.png"
image bg Windows_ES7 = "/images/os/WindowsES7.png"
image bg Windows_81 = "/images/os/Windows81.png"
image bg Windows_10 = "/images/os/Windows10.png"
image bg Windows_10_1903 = "/images/os/Windows10-1903.png"
image bg Snow_Leopard = "/images/os/MacSnowLeopard.png"
image bg Lion = "/images/os/MacLion.png"
image bg Mountain_Lion = "/images/os/MacMountainLion.png"
image bg Mavericks = "/images/os/MacMavericks.png"
image bg Yosemite = "/images/os/MacYosemite.png"
image bg El_Capitan = "/images/os/MacElCapitan.png"
image bg Sierra = "/images/os/MacSierra.png"
image bg High_Sierra = "/images/os/MacHighSierra.png"
image bg Mojave = "/images/os/MacMojave.png"
image bg Mojave_Night = "/images/os/MacMojaveNight.png"
image bg Catalina = "/images/os/MacCatalina.png"
image bg Catalina_Night = "/images/os/MacCatalinaNight.png"
image bg Fedora = "/images/os/Fedora.png"
image bg Ubuntu = "/images/os/Ubuntu.png"
image bg Debian = "/images/os/Debian.png"

define bi = Character('Птичка', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

default persistent.check_os = False
default question = 0
default ask_1 = False
default ask_2 = False
default ask_3 = False
default ask_4 = False

init -100 python:
    import platform

    if platform.release() in ["XP", "Vista", "7", "8"]:
        config.name = "Bird After Story"


label os_check_failure:
    $ quick_menu = False
    python:
        if platform.release() == "XP":
            fail_os = "Windows XP"
        elif platform.release() == "Vista":
            fail_os = "Windows Vista"
        elif platform.release() == "7":
            fail_os = "Windows 7"
        elif platform.release() == "8":
            fail_os = "Windows 8"
    if persistent.splash_now:
        scene white
    else:
        scene black
    pause 0.5
    scene birdy
    with Dissolve(1.0)
    pause 1.0
    bi "Ну, привет, что ли. :Д"
    bi "Не ожидал увидеть меня здесь?"
    bi "Думаю, ты оказался здесь лишь потому, что ты всё ещё сидишь на [fail_os]."
    label os_check_failure2:
        if question == 0:
            $ bi_speak = "Если у тебя есть какие-то вопросы, можешь позадавать их мне..."
        else:
            $ bi_speak = "Ещё что-нибудь тебя интересует? :3"
        menu:
            bi "[bi_speak]"
            "Почему вы ограничиваете поддержку систем?" if not ask_1:
                $ ask_1 = True
                bi "Дело в том, что у каждой версии операционной системы (здесь я не ограничиваюсь только Windows) есть ограниченный срок поддержки..."
                bi "И пока конец этой самой поддержки ещё не настал, разработчики этих систем выпускают для них так называемые «заплатки»."
                bi "Разработчики программного обеспечения ориентируются на то, какую систему ещё поддерживают в актуальном состоянии, и ставят соответствующий уровень совместимости."
                bi "К примеру, новые версии известного браузера Mozilla Firefox поддерживают только Windows 8.1 и выше."
                bi "Следовательно, из этого всего можно сделать вывод, что никому из разработчиков прикладного ПО не выгодно поддерживать «дырявые» системы..."
                bi "А разработчикам ОС – держать отдельно сервер для обновлений морально устаревшей системы, поскольку существует не менее перспективный и современный аналог оной."
                bi "И, в общем, выходов остаётся всего два..."
                bi "Либо обновлять систему, либо уходить на её актуальный аналог."
                bi "К примеру, поддержка Windows 7 уже закончилась (14 января 2020 года), но её аналог – Windows Embedded Standard 7 – будут поддерживать до 13 октября 2020 года."
                bi "А ещё эта версия «семёрки» намного производительнее её оригинальной версии. Чем не повод перейти на неё? ;)"
                bi "Ладно, по этому вопросу я тебе уже всё рассказал..."
                $ question += 1
                jump os_check_failure2
            "Что плохого в использовании морально устаревшей системы?" if not ask_2:
                $ ask_2 = True
                bi "Во-первых, старые ОС не могут использовать новые инструкции, которые требуют большинство прикладного ПО."
                bi "В результате, это самое прикладное ПО может либо работать некорректно, либо не запуститься вовсе."
                bi "А про ПайТома я вообще молчу. ¯\_(ツ)_/¯"
                bi "Мне кажется, он будет в своём уютном Ренпае поддерживать устаревшие системы, пока не состарится. :Д"
                bi "А толку от полурабочей ОС нет абсолютно никакого, согласись?"
                bi "Ну да ладно, если разработчик Ренпая всё-таки одумается и переосмыслит код движка, то ты меня будешь видеть гораздо реже. :Д"
                bi "Ладно, по этому вопросу я тебе уже всё рассказал..."
                $ question += 1
                jump os_check_failure2
            "Ты кто, блин? :)" if not ask_3:
                $ ask_3 = True
                bi "Меня все называют «Птичка», а ты кто? ;P"
                bi "Я являюсь помощником RG Smoking Room в вопросах фрагментации операционных систем."
                bi "Как бы тебя там ни звали, мне очень приятно познакомиться с тобой. :3"
                $ question += 1
                jump os_check_failure2
            "А ты хорошо умеешь танцевать?" if not ask_4:
                $ ask_4 = True
                bi "А как же? :Д"
                bi "Могу даже показать, мне не слабо. ;P"
                bi "Давай, поднимай свою попу и танцуй вместе со мной! ХД"
                $ question += 1
                jump os_check_failure3
    label os_check_failure3:
        $ persistent.autoload = "os_check_failure3"
        $ renpy.save_persistent()
        hide birdy
        show birdy_dancing zorder 100
        $ renpy.pause(hard=True)

define windows10_platforms = ["10.0.10240", "10.0.14393", "10.0.16299", "10.0.17134", "10.0.17763", "10.0.18362"]
default persistent.saveblock = False

init python:
    import platform
    import store
    if renpy.windows:
        if platform.release() == "7":
            if not os.path.isfile(os.environ["WINDIR"] + "\servicing\slc.dll") and not os.path.isfile(os.environ["WINDIR"] + "\Embedded.xml"):
                persistent.saveblock = True
        elif platform.release() == "10":
            if platform.version() >= "10.0.19041" or platform.version() in windows10_platforms:
                persistent.saveblock = False
            else:
                persistent.saveblock = True
    elif renpy.macintosh:
        macos_major = str(platform.mac_ver()[0])[:2]
        macos_minor = str(platform.mac_ver()[0])[3:5]
        if int(macos_major) < 11 and int(macos_minor) < 13: # 11.0 - Big Sur; 10.13 - High Sierra
            persistent.saveblock = True
        else:
            persistent.saveblock = False
    elif renpy.android:
        import subprocess
        droid_sdk = str(subprocess.check_output(["getprop", "ro.build.version.sdk"]))[:2]
        if droid_sdk < "21":
            persistent.saveblock = True
        else:
            persistent.saveblock = False
    else:
        persistent.saveblock = False
    

label os_check:

    python:
        from time import localtime, strftime
        t = strftime("%H:%M:%S", localtime())
        hour, min, sec = t.split(":")
        hour = int(hour)
        import os
        import platform
        if renpy.windows:
            import _winreg
        if renpy.linux:
            import distro
        import re
        import subprocess
        ren_os = None
        win10_build = None
        droid_ver = None
        output = None
        droid_codename = None
        droid_sdk = None
        macos_codename = None
        macos_build = None
        macos_name = None
        macos_latest = None
        macos_beta = None
        ltsc_build = False
        ltsb_build = False
        insider_build = False
        compatible_os = False
        linux_distrib = None
        fedora_beta = False
        mydick = None
        eol_date = None
        if renpy.android:
            dl_dir = os.path.join(os.path.join(os.environ["ANDROID_STORAGE"]), "emulated", "0", "Download")
        # импорты и дефолты для работы; так называемая "стартовая точка"
        # if platform.release() == "XP":
        #     compatible_os = False
        #     try:
        #         winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\WPA\\PosReady')
        #         ren_os = "Windows Embedded POSReady 2009"
        #     except:
        #         ren_os = "Windows XP"
        # внимание: поддержка Windows XP прекращена 8 апреля 2014 года; поддержка Windows Embedded POSReady 2009 прекращена 9 апреля 2019 года
        # if platform.release() == "Vista":
        #     compatible_os = False
        #     ren_os = "Windows Vista"
        # внимание: поддержка Windows Vista прекращена 11 апреля 2017 года
        if platform.release() == "2000":
            renpy.error("Молодец, молодой энтузиаст, только вот зачем всё это нужно было? Ты хвастаешься точно так же, как и любители «конструкторов» для Apple Mac II?")
        # внимание: это своеобразная "пасхалка" для тех, кто смог завести Ren'Py на Windows 2000
        if platform.release() == "7":
            compatible_os = True
            if os.path.isfile(os.environ["WINDIR"] + "\servicing\slc.dll"):
                ren_os = "Windows 7 (ESU)"
            elif os.path.isfile(os.environ["WINDIR"] + "\Embedded.xml"):
                ren_os = "Windows Embedded Standard 7"
            else:
                ren_os = "Windows 7"
        # внимание: поддержка Windows 7 SP1 будет убрана 14 января 2020 года; поддержка Windows Embedded Standard 7 будет убрана 13 октября 2020 года
        # if platform.release() == "8":
        #     compatible_os = False
        #     ren_os = "Windows 8"
        if platform.release() == "8.1":
            compatible_os = True
            ren_os = "Windows 8.1"
        # внимание: поддержка Windows 8.1 будет убрана 10 января 2023 года
        # примечание: после обновления файла "platform.pyo", движок Ren'Py корректно определяет версию ОС
        # if platform.release() == "2008ServerR2":
        #     compatible_os = False
        #     ren_os = "Windows Server 2008 R2"
        # внимание: поддержка Windows Server 2008 R2 будет убрана 14 января 2020 года
        if renpy.linux:
            if distro.id() == "fedora" and distro.version() == "31":
                compatible_os = True
                fedora_beta = True
                ren_os = "Fedora"
            if distro.id() == "fedora" and distro.version() == "30":
                compatible_os = True
                fedora_latest = True
                ren_os = "Fedora"
            if distro.id() == "ubuntu" and distro.version() == "19.04":
                compatible_os = True
                ubuntu_latest = True
                ren_os = "Ubuntu"
            if distro.id() == "ubuntu" and distro.version() == "18.04.3":
                #compatible_os = True
                ubuntu_lts = True
                ren_os = "Ubuntu"
            if distro.id() == "debian":
                ren_os = "Debian"
            if distro.id() == "rhel":
                ren_os = "RedHat Enterprise Linux"
            if distro.id() == "centos":
                ren_os = "CentOS"
            if distro.id() == "opensuse":
                ren_os = "openSUSE"
            if distro.id() == "amazon":
                ren_os = "Amazon Linux"
            if distro.id() == "arch":
                ren_os = "Arch Linux"
            if distro.id() == "cloudlinux":
                ren_os = "CloudLinux OS"
            if distro.id() == "gentoo":
                ren_os = "GenToo Linux"
            if distro.id() == "linuxmint":
                ren_os = "Linux Mint"
            if distro.id() == "mageia":
                ren_os = "Mageia"
            if distro.id() == "mandriva":
                ren_os = "Mandriva Linux"
            if distro.id() == "slackware":
                ren_os = "Slackware"
            if distro.id() == "sles":
                ren_os = "SUSE Linux Enterprise Server"
            if distro.id() == "exherbo":
                ren_os = "Exherbo Linux"
            if distro.id() == "parallels":
                ren_os = "Parallels"
            if distro.id() == "pidora":
                ren_os = "Pidora"
            if distro.id() == "raspbian":
                ren_os = "Raspbian"
            if distro.id() == "scientific":
                ren_os = "Scientific Linux"
            if distro.id() == "oracle":
                ren_os = "Oracle Linux"
            if distro.id() == "xenserver":
                ren_os = "XenServer"
            if distro.id() == "openbsd":
                ren_os = "OpenBSD"
            if distro.id() == "netbsd":
                ren_os = "NetBSD"
            if distro.id() == "freebsd":
                ren_os = "FreeBSD"
            linux_distrib = "{0} {1}".format(ren_os, distro.version())
        if platform.system() == "Darwin":
            macos_build = str(platform.mac_ver()[0])
            if int(macos_build[3:5]) <= 8:
                macos_name = "Mac OS X"
            elif int(macos_build[3:5]) <= 12:
                macos_name = "OS X"
            else:
                macos_name = "macOS"
            if int(macos_build[3:5]) == 6:
                compatible_os = False
                macos_codename = "Snow Leopard"
            if int(macos_build[3:5]) == 7:
                compatible_os = False
                macos_codename = "Lion"
            if int(macos_build[3:5]) == 8:
                compatible_os = False
                macos_codename = "Mountain Lion"
            if int(macos_build[3:5]) == 9:
                compatible_os = False
                macos_codename = "Mavericks"
            if int(macos_build[3:5]) == 10:
                compatible_os = True
                macos_codename = "Yosemite"
            if int(macos_build[3:5]) == 11:
                compatible_os = True
                macos_codename = "El Capitan"
            if int(macos_build[3:5]) == 12:
                compatible_os = True
                macos_codename = "Sierra"
            if int(macos_build[3:5]) == 13:
                compatible_os = True
                macos_codename = "High Sierra"
            if int(macos_build[3:5]) == 14:
                compatible_os = True
                macos_codename = "Mojave"
            if int(macos_build[3:5]) == 15:
                compatible_os = True
                macos_latest = True
                macos_codename = "Catalina"
        if platform.release() == "10":
            if platform.version() in ["10.0.18362", "10.0.19041"]:
                compatible_os = True
                win10_build = str(platform.version())[5:10]
                ren_os = "Windows 10, сборка {0}".format(win10_build)
            elif platform.version() == "10.0.17763" or platform.version() == "10.0.14393":
                compatible_os = True
                ltsc_build = True
                win10_build = str(platform.version())[5:10]
                ren_os = "Windows 10, сборка {0} (LTSC-сборка с продлённым сроком поддержки)".format(win10_build)
            elif platform.version() == "10.0.10240":
                compatible_os = True
                ltsb_build = True
                win10_build = str(platform.version())[5:10]
                ren_os = "Windows 10, сборка {0} (LTSB-сборка с продлённым сроком поддержки)".format(win10_build)
            elif platform.version() == "10.0.19536" or platform.version() > "10.0.19041" or platform.version() == "10.0.18363":
                compatible_os = True
                insider_build = True
                win10_build = str(platform.version())[5:10]
                ren_os = "Windows 10, сборка {0} (инсайдерская сборка)".format(win10_build)
            else:
                compatible_os = False
                win10_build = str(platform.version())[5:10]
                ren_os = "Windows 10, сборка {0} (явно устаревшая)".format(win10_build)
        # примечание: версия будет повышаться по мере выхода новых версий ОС Windows 10
        if renpy.android:
            try:
            # код для Non-Treble-прошивок
                for line1 in open('/system/build.prop'):
                    mth = re.search("ro.build.version.release=(.*)", line1)
                    if mth:
                        droid_ver = mth.group(1)
                for line2 in open('/system/build.prop'):
                    mtg = re.search("ro.build.version.sdk=(.*)", line2)
                    if mtg:
                        droid_sdk = mtg.group(1)
            except:
            # код для Treble-прошивок
                try:
                    f = open(dl_dir + "/getprop_ver.txt", "w+")
                    output1 = subprocess.check_output(["getprop", "ro.build.version.release"])
                    f.write(output1)
                    f.close()
                    f = open(dl_dir+ "/getprop_ver.txt", "r")
                    contents1 = f.read()
                    one = re.search(r"(.*)", contents1)
                    if one:
                        droid_ver = one.group(1)
                    gpr = open(dl_dir + "/getprop_sdk.txt", "w+")
                    output2 = subprocess.check_output(["getprop", "ro.build.version.sdk"])
                    gpr.write(output2)
                    gpr.close()
                    gpr = open(dl_dir + "/getprop_sdk.txt", "r")
                    contents2 = gpr.read()
                    two = re.search(r"(.*)", contents2)
                    if two:
                        droid_sdk = two.group(1)
                except:
                    f = open(user_dir + "/getprop_ver.txt", "w+")
                    output1 = subprocess.check_output(["getprop", "ro.build.version.release"])
                    f.write(output1)
                    f.close()
                    f = open(user_dir + "/getprop_ver.txt", "r")
                    contents1 = f.read()
                    one = re.search(r"(.*)", contents1)
                    if one:
                        droid_ver = one.group(1)
                    gpr = open(user_dir + "/getprop_sdk.txt", "w+")
                    output2 = subprocess.check_output(["getprop", "ro.build.version.sdk"])
                    gpr.write(output2)
                    gpr.close()
                    gpr = open(user_dir + "/getprop_sdk.txt", "r")
                    contents2 = gpr.read()
                    two = re.search(r"(.*)", contents2)
                    if two:
                        droid_sdk = two.group(1)

            if droid_sdk == '21' or droid_sdk == '22':
                droid_codename = 'Lollipop'
            if droid_sdk == '23':
                droid_codename = 'Marshmallow'
            if droid_sdk == '24' or droid_sdk == '25':
                droid_codename = 'Nougat'
            if droid_sdk == '26' or droid_sdk == '27':
                droid_codename = 'Oreo'
            if droid_sdk == '28':
                droid_codename = 'Pie'
            if droid_sdk == '29':
                droid_codename = 'Q'
            # поддержка версий Android ниже 5.0 была отозвана самим разработчиком движка

    if droid_sdk == '21' or droid_sdk == '22':
        show bg Android_5 with dissolve
    if droid_sdk == '23':
        show bg Android_6 with dissolve
    if droid_sdk == '24' or droid_sdk == '25':
        show bg Android_7 with dissolve
    if droid_sdk == '26' or droid_sdk == '27':
        show bg Android_8 with dissolve
    if droid_sdk == '28':
        show bg Android_9 with dissolve
    if droid_sdk == '29':
        show bg Android_10 with dissolve
    # if platform.release() == "XP":
    #     show bg Windows_XP with dissolve
    # if platform.release() == "Vista":
    #     show bg Windows_Vista with dissolve
    # if ren_os == "Windows 7":
    #     show bg Windows_7 with dissolve
    if ren_os == "Windows Embedded Standard 7":
        show bg Windows_ES7 with dissolve
    # if platform.release() == "2008ServerR2":
    #     show bg Server2008R2 with dissolve
    # if platform.release() == "8":
    #     show bg Windows_8 with dissolve
    if platform.release() == "8.1":
        show bg Windows_81 with dissolve
    if platform.release() == "10" and platform.version() == "10.0.18362":
        show bg Windows_10_1903 with dissolve
    if platform.release() == "10" and platform.version() != "10.0.18362":
        show bg Windows_10 with dissolve
    if macos_build == "10.6":
        show bg Snow_Leopard with dissolve
    if macos_build == "10.7":
        show bg Lion with dissolve
    if macos_build == "10.8":
        show bg Mountain_Lion with dissolve
    if macos_build == "10.9":
        show bg Mavericks with dissolve
    if macos_build == "10.10":
        show bg Yosemite with dissolve
    if macos_build == '10.11':
        show bg El_Captain with dissolve
    if macos_build == '10.12':
        show bg Sierra with dissolve
    if macos_build == '10.13':
        show bg High_Sierra with dissolve
    if macos_build == '10.14' and hour in [20,21,22,23,24,0,1,2,3,4,5,6]:
        show bg Mojave_Night with dissolve
    if macos_build == '10.14' and not hour in [20,21,22,23,24,0,1,2,3,4,5,6]:
        show bg Mojave with dissolve
    if macos_build == '10.15' and hour in [20,21,22,23,24,0,1,2,3,4,5,6]:
        show bg Catalina_Night with dissolve
    if macos_build == '10.15' and not hour in [20,21,22,23,24,0,1,2,3,4,5,6]:
        show bg Catalina with dissolve
    if ren_os == "Fedora":
        show bg Fedora with dissolve
    if ren_os == "Ubuntu":
        show bg Ubuntu with dissolve
    if ren_os == "Debian":
        show bg Debian with dissolve
    if ren_os == "RedHat Enterprise Linux":
        show bg RedHat with dissolve
    if ren_os == "CentOS":
        show bg CentOS with dissolve
    if ren_os == "openSUSE":
        show bg openSUSE with dissolve
    if ren_os == "Amazon Linux":
        show bg Amazon with dissolve
    if ren_os == "Arch Linux":
        show bg Arch with dissolve
    if ren_os == "CloudLinux OS":
        show bg CloudLinux with dissolve
    if ren_os == "GenToo Linux":
        show bg GenToo with dissolve
    if ren_os == "Linux Mint":
        show bg Mint with dissolve
    if ren_os == "Mageia":
        show bg Mageia with dissolve
    if ren_os == "Mandriva Linux":
        show bg Mandriva with dissolve
    if ren_os == "Slackware":
        show bg Slackware with dissolve
    if ren_os == "SUSE Linux Enterprise Server":
        show bg SUSE_Server with dissolve
    if ren_os == "Exherbo Linux":
        show bg Exherbo with dissolve
    if ren_os == "Parallels":
        show bg Parallels with dissolve
    if ren_os == "Pidora":
        show bg Pidora with dissolve
    if ren_os == "Raspbian":
        show bg Raspbian with dissolve
    if ren_os == "Scientific Linux":
        show bg Scientific with dissolve
    if ren_os == "Oracle Linux":
        show bg Oracle with dissolve
    if ren_os == "XenServer":
        show bg XenServer with dissolve
    if ren_os == "OpenBSD":
        show bg OpenBSD with dissolve
    if ren_os == "NetBSD":
        show bg NetBSD with dissolve
    if ren_os == "FreeBSD":
        show bg FreeBSD with dissolve
    # возможно, здесь будет прописана (а в отдельной папке - сложена) куча картинок, но это уже совсем другая история :Д

    if renpy.android:
        "Обнаружена операционная система: Android [droid_ver] ([droid_codename])."
        if droid_sdk == '21' or droid_sdk == '22' or droid_sdk == '23':
            "Внимание: используется морально устаревшая версия системы Android."
            "Настоятельно рекомендуем обновить стоковую прошивку (OTA-обновление или через компьютер), перепрошить устройство на кастомную прошивку, основанную на более новой версии, или купить новое устройство."
            if droid_sdk == '21' or droid_sdk == '22' or droid_sdk == '23':
                "Кстати, ты уже играл в игру «Flappy Android»? ;3"
        if droid_sdk == '24' or droid_sdk == '25' or droid_sdk == '26' or droid_sdk == '27' or droid_sdk == '28':
            "Поздравляем, у вас более-менее свежая версия прошивки! ^.^"
            "Следите за обновлениями от производителя вашего устройства. :3"
            if droid_sdk == '24' or droid_sdk == '25':
                "Кстати, сколько котов ты уже успел наловить? ;3"
            if droid_sdk == '26' or droid_sdk == '27':
                "Кстати, ты уже играл с осьминогом, прячущимся за печенькой Орео? ;3"
            if droid_sdk == '28':
                "Кстати, ты уже пробовал представить себя художником? ;3"
                "И, согласись, Google в последнее время делает Android схожим с iOS..."
                "Почувствуй себя обладателем нового iPhone из линейки X! :Д"
        if droid_sdk == '29':
            "Поздравляем, у вас установлена самая последняя (на момент последней правки модуля) версия прошивки!"
            "Следите за обновлениями от производителя вашего устройства. :3"

    elif renpy.windows:
        "Обнаружена операционная система: [ren_os]."
        # if platform.release() == "XP" and ren_os == "Windows Embedded POSReady 2009":
        #     "Внимание: поддержка данной операционной системы была прекращена 9 апреля 2019 года."
        #     "Настоятельно рекомендуем установить более новую версию Windows."
        #     nm "Да, старик, твоё время для ностальгии уже давным-давно закончилось. :Д"
        #     nm "Но раз ты такой же «особо одарённый», как и некоторые личности (да, Чмыряра и FUF'sobbing?), то можешь продолжать игру."
        # if platform.release() == "XP" and ren_os != "Windows Embedded POSReady 2009":
        #     "Внимание: поддержка данной операционной системы была прекращена 8 апреля 2014 года."
        #     "Настоятельно рекомендуем установить более новую версию Windows."
        # if platform.release() == "Vista":
        #     "Внимание: поддержка данной операционной системы была прекращена 11 апреля 2017 года."
        #     "Настоятельно рекомендуем установить более новую версию Windows (блин, чувак, ну серьёзно)."
        # if ren_os == "Windows 7":
        #     "Внимание: поддержка данной операционной системы будет прекращена 14 января 2020 года."
        #     "Можете пока продолжать пользоваться этой ОС. Ну, или можете обновиться до Windows 10."
        #     "В принципе, вы можете так же установить Windows Embedded Standard 7, благо она будет жить «дольше» оригинальной семёрки. :Д"
        if ren_os == "Windows Embedded Standard 7":
            "Внимание: поддержка данной операционной системы будет прекращена 13 октября 2020 года."
            "Если вы мигрировали на данную сборку с оригинальной Windows 7, то можете погладить себя по головке, вы это заслужили. :3"
            "Можете пока пользоваться этой системой, если у вас совсем нет никакого желания обновляться до Windows 10."
        # if platform.release() == "2008ServerR2":
        #     "Внимание: поддержка данной операционной системы будет прекращена 14 января 2020 года."
        #     "Также имейте в виду, что эта операционная система, в отличие от Windows 7, является серверной."
        #     "Можете пока продолжать использовать её, или же обновить её до более новой версии, к примеру, до Windows Server 2012."
        # if platform.release() == "8":
        #     "Внимание: поддержка данной операционной системы была прекращена 12 января 2016 года."
        #     "Настоятельно рекомендуем установить более новую версию Windows."
        #     "Ну там... Windows 8.1 или даже Windows 10..."
        #     "Короче, сами подумайте."
        if platform.release() == "8.1":
            "Внимание: поддержка данной операционной системы будет прекращена 10 января 2023 года."
            "Можете пока продолжать пользоваться этой ОС, если она вам действительно нравится..."
            "А если вы обновились до этой версии с Windows 8 легальным методом (через Магазин), то вы – молодец!"
            "Ну, или можете установить Windows 10... в общем, подумайте над этим."
        if platform.release() == "10":
            if platform.version() == "10.0.18362":
                "Мои поздравления, для вашей системы, на данный момент, нет новых крупных обновлений."
                "Но они определённо будут в скором времени, так что просто ждите. :3"
            elif ltsc_build or ltsb_build:
                if platform.version() == "10.0.17763":
                    $ eol_date = "9 января 2029 года"
                elif platform.version() == "10.0.14393":
                    $ eol_date = "13 октября 2026 года"
                elif platform.version() == "10.0.10240":
                    $ eol_date = "14 октября 2025 года"
                "Внимание: поддержка этой сборки Windows 10 будет прекращена [eol_date]."
                "Пока эта дата ещё не наступила, вы можете устанавливать накопительные обновления... хотя мы настоятельно рекомендуем установить Ноябрьское обновление."
                "Впрочем, если учесть, что у вас «сборка-продлёнка», то пока можете ни о чём не беспокоиться. :3"
            elif insider_build:
                "Внимание: инсайдерские сборки Windows 10 могут нести в себе множество багов, и не факт, что все они окажутся «безобидными»."
                "Если вы являетесь энтузиастом, датамайнером, или даже тестером, которым такие ситуации не кажутся безвыходными, можете смело продолжать работу."
                "Мы искренне благодарны вам за оперативную доставку новостей касательно ожидаемых новых функций в Windows 10. :3"
            else:
                "Это хорошо, что у вас установлена Windows 10, но почему вы не ставите последние обновления?"
                "Вас они не устраивают, или Центр обновлений Windows их просто не видит?"
                "Или у вас слетела активация? :Д"
                "Если последнее – про вас, то... как вариант, могу посоветовать воспользоваться активаторами, типа Re-Loader, AAct или какой-нибудь ревизией KMSAuto."
                "Или можете вообще лицензию купить. :Д"
                "Не отставайте от прогресса, иначе это может выйти для вас боком!"
                "Лечите свою операционную систему от жадности, и чем скорее вы это сделаете – тем лучше!"
                "Не болейте! :Д"
        # if not compatible_os:
        #     "Обращаю ваше внимание на то, что поддержка устаревших систем, в число которых также входят Windows XP, Windows Vista и Windows 7, будет безвозвратно отозвана 14 января 2020 года."
        #     "Если вам реально всё равно, то я могу вам только посочувствовать..."
        #     "Но если у вас, к примеру, трудное материальное положение или система сама по себе противится установке обновлений, перепишите следующий код на листок бумаги, в Блокнот или ещё куда-нибудь..."
        #     python:
        #         persistent.my_uuid = str(uuid.uuid4())
        #         persistent.uuid_generated = True
        #         renpy.save_persistent()
        #     "Откройте Блокнот или любой другой текстовый редактор и перепишите следующий код: [persistent.my_uuid]."
        #     "После этого, сохраните файл в корневой папке игры и назовите его «my_uuid» (без кавычек). Убедитесь, что указан тип «Текстовый документ»."
        #     "Удачи. :3"
        #     $ renpy.quit()

    elif renpy.macintosh:
        "Обнаружена операционная система: [macos_name] [macos_build] ([macos_codename])."
        if not compatible_os and macos_beta is None and macos_latest is None:
            "Настоятельно рекомендуем обновить системное программное обеспечение вашего Mac до последней версии."
        if compatible_os and macos_beta is None and macos_latest is None:
            "Мои поздравления, у вас более-менее актуальная версия системного программного обеспечения Mac."
            "Но мы настоятельно рекомендуем обновить его до последней версии."
        if compatible_os and macos_latest:
            "Поздравляем, у вас самая актуальная (на момент создания модуля) версия системного программного обеспечения Mac."
            "В ближайшее время корпорация Apple выпустит новую версию macOS, которая несёт в себе кучу фишек для владельцев оригинальных компьютеров (и кучу проблем для хакинтошников :Д)."
            "Следите за новостями! :3"
        if compatible_os and macos_beta:
            "О, вы решили попробовать что-то новенькое? :3"
            "Учтите, что некоторые функции бета-версии могут работать неправильно, или не работать вообще. :Д"
            "Приятного тестирования. ^.^"

    elif renpy.linux:
        "Обнаружена операционная система: [linux_distrib]."
        if distro.id() == "fedora" and fedora_beta:
            "О, вы решили попробовать тестовую версию Fedora? :3"
            "Что ж, удачи в ваших начинаниях! Надеюсь, у вас она работает более-менее стабильно. ^.^"
        if distro.id() == "fedora" and fedora_latest:
            "Мои поздравления, для вашего дистрибутива пока нет новых версий. По крайней мере, стабильных. :3"
            "Но они определённо будут в скором времени, так что просто ждите. ^.^"
        if distro.id() == "fedora" and not fedora_latest:
            "Настоятельно рекомендуем обновить версию вашего дистрибутива до самой актуальной."
        if distro.id() == "ubuntu" and ubuntu_latest:
            "Мои поздравления, для вашего дистрибутива пока нет новых версий. По крайней мере, стабильных. :3"
            "Но они определённо будут в скором времени, так что просто ждите. ^.^"
        if compatible_os is None:
            "Код для данного дистрибутива пока ещё не написан, но сам модуль будет дописан в скором времени."
            "Следите за обновлениями. :3"
        # TODO: дописать для других дистрибутивов
    else:
        "О, привет. :Р"
        "Ты как здесь оказался? :3"
        "Твоя операционная система, внезапно, оказалась неизвестной природе? ^.^"
        "Или код для неё пока ещё не записан в модуле? :Д"
        "В любом случае, удачи тебе в твоих начинаниях. :3"

    if persistent.splash_now:
        scene white with Dissolve(2)
    else:
        scene black with Dissolve(2)
    return
