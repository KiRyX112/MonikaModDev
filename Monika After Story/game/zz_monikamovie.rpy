


label ch30_monikamovie:
    init python:


        MOVIE_X = 680
        MOVIE_Y = 40
        MOVIE_W = 450
        MOVIE_H = 640
        MOVIE_XALIGN = -0.05
        MOVIE_AREA = (MOVIE_X, MOVIE_Y, MOVIE_W, MOVIE_H)
        MOVIE_RETURN = "I changed my mind"


        gamedir = os.path.normpath(config.gamedir)




        class AvaiableMovies:
            def __init__(self):
                self.listOfMovies = []
                self.checkMovies()
            
            def checkMovies(self):
                with open(os.path.join(gamedir, "movies-info.mms"),"r") as f: 
                    lines = f.readlines()
                listOfStrings = [x.strip() for x in lines]
                
                
                for line in listOfStrings:
                    if "#" in line:
                        continue
                    partialSplittedSentence = line.split(" ", 1)
                    firstWord = ""
                    if len(partialSplittedSentence) >= 2:
                        firstWord = partialSplittedSentence[0]
                        data = partialSplittedSentence[1]
                    if "movie" in firstWord:
                        self.listOfMovies.append((data, data, False, False))
            
            def searchMovies(self, movieName):
                foundMovies = []
                for xName in self.listOfMovies:
                    if movieName.lower() in xName.lower():
                        foundMovies.append(xName)
                return foundMovies

        class ParsedMovie:
            def __init__(self, movieName):
                self.descriptionList = []
                self.reactionList = []
                self.closure = None
                self.currentReactionIndex = 0 
                self.retrieveMovie(movieName)
            
            def reactionsAreFinished(self):
                return self.currentReactionIndex >= len(self.reactionList)
            
            def stringReactionToTuple(self, string):
                emotion = None
                when = ""
                what = ""
                listOfInfo = []
                if not string[0] == "[": 
                    listOfInfo = string.split(" ", 2)
                    emotion = listOfInfo [0]
                    when = listOfInfo [1]
                    what = listOfInfo [2]
                else:
                    listOfInfo = string.split(" ", 1)
                    when = listOfInfo [0]
                    what = listOfInfo [1]
                return emotion,when,what
            
            def formattedTimeToSeconds(self, string):
                string = string.replace('[','')
                string = string.replace(']','')
                infoList = string.split(":")
                hours = int(infoList[0])
                minutes = int(infoList[1])
                seconds = int(infoList[2])
                return 3600*hours + 60*minutes + seconds
            
            def obtainCurrentReactionTuple(self):
                string = self.reactionList[self.currentReactionIndex]
                emotion, when, what = self.stringReactionToTuple(string)
                return emotion,when,what
            
            def popReaction(self):
                emotion, when, what = self.obtainCurrentReactionTuple()
                self.currentReactionIndex += 1
                return emotion,when,what
            
            
            def canReact(self, time):
                if(self.reactionsAreFinished()):
                    return False
                emotion, when, what = self.obtainCurrentReactionTuple()
                
                expectedToReact = self.formattedTimeToSeconds(when)
                return time > expectedToReact
            
            
            def popDescription(self):
                string = self.descriptionList.pop(0)
                stringArray = string.split(" ", 1)
                emotion = stringArray[0]
                line = stringArray[1]
                
                return emotion, line
            
            def hasDescription(self):
                return len(self.descriptionList) > 0
            
            def formatData(self, data):
                return data.replace('"','')
            
            def retrieveMovie(self, movieName):
                with open(os.path.join(gamedir, "movies-info.mms"),"r") as f:
                    lines = f.readlines()
                listOfStrings = [x.strip() for x in lines]
                
                
                filmFound = False
                for line in listOfStrings:
                    if "#" in line:
                        continue
                    partialSplittedSentence = line.split(" ", 1)
                    firstWord = ""
                    if len(partialSplittedSentence) >= 2:
                        firstWord = partialSplittedSentence[0]
                        data = partialSplittedSentence[1]
                        data = self.formatData(data)
                    if "movie" in firstWord:
                        filmFound = movieName == partialSplittedSentence[1]
                    if filmFound:
                        if "description" == firstWord:
                            self.descriptionList.append(data)
                        if "m" == firstWord:
                            self.reactionList.append(data)
                        if "closure" == firstWord:
                            self.closure = data
            
            def resynchronizeIndex(self, timer):
                self.currentReactionIndex = 0
                while((not (self.reactionsAreFinished())) and self.canReact(timer.seconds)):
                    self.currentReactionIndex += 1


        class MovieTimer:
            def __init__(self):
                self.seconds = 0
            def seconds(self):
                return self.seconds
            def addSeconds(self, secondsAdded):
                self.seconds += secondsAdded
            def formattedTime(self):
                secondsPool = self.seconds
                hours = int(secondsPool / 3600)
                secondsPool -= hours * 3600
                minutes = int(secondsPool / 60)
                secondsPool -= minutes * 60
                secs = secondsPool
                return hours, minutes, secs
            def setFormattedTime(self,hours,minutes,seconds):
                self.seconds = int(hours)*3600 + int(minutes)*60 + int(seconds)



        def iterate_timer(st, at, timer):
            
            deltaTime = st - globals()['lastCountdownTime']
            globals()['lastCountdownTime'] = st
            if watchingMovie:
                timer.addSeconds(deltaTime)
            
            
            hours, minutes, secs = timer.formattedTime()
            d = Text("%02d:%02d:%02d" % (hours, minutes, secs))
            return d, 0.1
        def fastforward(timer,secondsAdded):
            timer.addSeconds(secondsAdded)

        def updateEmotionMonika(emotion):
            if emotion is not None:
                monika_reaction = "monika %s" % (emotion)
                renpy.show(monika_reaction)



        watchingMovie = False
        lastCountdownTime = 0 
        firstComment = False
        timer = MovieTimer()

    $ final_item = (MOVIE_RETURN, False, False, False, 20)

    $ listMovies = AvaiableMovies()

    m 1eub "Ты хочешь посмотреть фильм?"

    label mm_choose_movie:

        m "Какой бы ты хотел[mas_gender_none] посмотреть?"


        show monika at t21


        call screen mas_gen_scrollable_menu(listMovies.listOfMovies, MOVIE_AREA, MOVIE_XALIGN, final_item=final_item)


        show monika at t11


        if _return:
            $ movieInformation = ParsedMovie(_return)
            jump mm_found_movie
        else:
            jump mm_movie_loop_end

    label mm_found_movie:
        $ MovieOverlayShowButtons()
        stop music fadeout 2.0
        image countdown = DynamicDisplayable(iterate_timer, timer)
        show countdown at topleft

        python:
            while(movieInformation.hasDescription()):
                emotion, what =  movieInformation.popDescription()
                updateEmotionMonika(emotion)
                renpy.say(eval("m"), what)
        m 3eub "Давай синхронизируем начало фильма."
        m 1hub "Приготовься начать просмотр, я начинаю обратный отчёт!"

        menu:
            "Готов[mas_gender_none]?"
            "Да.":
                label mm_movie_resume:
                    $ mas_RaiseShield_dlg()
                    m 1eua "Три...{w=1}{nw}"
                    m "Два...{w=1}{nw}"
                    m "Один...{w=1}{nw}"

                    $ watchingMovie = True
                    label movie_loop:
                        pause 1.0
                        python:
                            if movieInformation.canReact(timer.seconds):
                                emotion, when, what = movieInformation.popReaction()
                                updateEmotionMonika(emotion)
                                
                                if not (what == "" or what is None):
                                    what += "{w=10}{nw}"
                                    renpy.say(eval("m"), what)

                        if movieInformation.reactionsAreFinished():
                            hide countdown
                            $ MovieOverlayHideButtons()
                            m 1eua "У меня только что закончилось! А тебе понравилось?"
                            jump mm_movie_closure

                        jump movie_loop
            "Нет.":

                hide countdown
                $ MovieOverlayHideButtons()
                m 1eua "Ох, ладно! Тогда просто подожду тебя~"
                jump mm_movie_loop_end

        label mm_movie_closure:

            python:
                if movieInformation.closure:
                    pushEvent(movieInformation.closure)



    label mm_movie_loop_end:
        hide countdown
        $ mas_DropShield_dlg()
        $ watchingMovie = False
        $ timer.seconds = 0
        $ MovieOverlayHideButtons()
        $ play_song(store.songs.selected_track)
        show monika 1esa
        jump ch30_loop

    label mm_movie_pausefilm:
        $ watchingMovie = False
        m 1eub "Ох, ты поставил[mas_gender_none] фильм на паузу, [player]."
        menu:
            "Хочешь продолжить?"
            "Да.":
                m 1hua "Отлично, [player_abb]."
                jump mm_movie_resume
            "Нет.":
                m 1eua "Ох, тогда всё нормально, [player_abb]."
                jump mm_movie_loop_end

    label mm_movie_settime:
        $ watchingMovie = False
        m 1eub "Ты хочешь синхронизировать время?"
        label mm_movie_repeattime:
            m 1eub "Скажи мне его в формате HH:MM:SS, [player]."
            python:
                player_dialogue = renpy.input('Какое время я должна установить? ',default='',pixel_width=720,length=50)
                splittedTime = player_dialogue.split(":",2)
                bad_format = len(splittedTime) != 3
                if not bad_format:
                    hours = splittedTime[0]
                    minutes = splittedTime[1]
                    seconds = splittedTime[2]
                    bad_format = not (hours.isdigit() and minutes.isdigit() and seconds.isdigit())
                    if not bad_format:
                        bad_format = int(minutes) >= 60 or int(seconds) >= 60
            if bad_format:
                m 1lksdlc "Эмм..."
                m 1lksdlb "Прости, но я не совсем поняла то, что ты вв[mas_gender_iol], [player]."
                m 1eka "Запомни, время должно быть в формате HH:MM:SS."
                m 3eua "Это «Часы:Минуты:Секунды»."
                m "Вот пример, [player]."
                m "01:05:32"
                m 1eub "Это 1 час, 5 минут и 32 секунды."
                m 3hua "Поэтому попробуй ещё раз!"
                jump mm_movie_repeattime
            else:
                $ timer.setFormattedTime(splittedTime[0],splittedTime[1],splittedTime[2])
                $ movieInformation.resynchronizeIndex(timer)
        m 1eua "Всё готово! Давай смотреть!"
        jump mm_movie_resume
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
