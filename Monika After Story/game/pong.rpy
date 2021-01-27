
default persistent._mas_pong_difficulty = 10

default persistent._mas_pong_difficulty_change_next_game = 0

default persistent._mas_pm_ever_let_monika_win_on_purpose = False

default persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()

define PONG_DIFFICULTY_CHANGE_ON_WIN = +1
define PONG_DIFFICULTY_CHANGE_ON_LOSS = -1
define PONG_DIFFICULTY_POWERUP = +5
define PONG_DIFFICULTY_POWERDOWN = -5
define PONG_PONG_DIFFICULTY_POWERDOWNBIG = -10


define PONG_MONIKA_RESPONSE_NONE = 0
define PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 1
define PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES = 2
define PONG_MONIKA_RESPONSE_WIN_LONG_GAME = 3
define PONG_MONIKA_RESPONSE_WIN_SHORT_GAME = 4
define PONG_MONIKA_RESPONSE_WIN_TRICKSHOT = 5
define PONG_MONIKA_RESPONSE_WIN_EASY_GAME = 6
define PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME = 7
define PONG_MONIKA_RESPONSE_WIN_HARD_GAME = 8
define PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME = 9
define PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME = 10
define PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL = 11
define PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT = 12
define PONG_MONIKA_RESPONSE_LOSE_LONG_GAME = 13
define PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME = 14
define PONG_MONIKA_RESPONSE_LOSE_EASY_GAME = 15
define PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME = 16
define PONG_MONIKA_RESPONSE_LOSE_HARD_GAME = 17
define PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME = 18
define PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME = 19

define pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

define played_pong_this_session = False
define mas_pong_taking_break = False
define player_lets_monika_win_on_purpose = False
define instant_loss_streak_counter = 0
define loss_streak_counter = 0
define win_streak_counter = 0
define lose_on_purpose = False
define monika_asks_to_go_easy = False


define ball_paddle_bounces = 0
define powerup_value_this_game = 0
define instant_loss_streak_counter_before = 0
define loss_streak_counter_before = 0
define win_streak_counter_before = 0
define pong_difficulty_before = 0
define pong_angle_last_shot = 0.0

init:

    image bg pong field = "mod_assets/games/pong/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):
            
            def __init__(self):
                
                renpy.Displayable.__init__(self)
                
                
                self.paddle = Image("mod_assets/games/pong/pong.png")
                self.ball = Image("mod_assets/games/pong/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("[monika_name]"), size=36)
                self.ctb = Text(_("Нажми, чтобы начать"), size=36)
                
                
                self.playsounds = True
                self.soundboop = "mod_assets/sounds/pong_sounds/pong_boop.wav"
                self.soundbeep = "mod_assets/sounds/pong_sounds/pong_beep.wav"
                
                
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654
                
                
                self.CURRENT_DIFFICULTY = max(persistent._mas_pong_difficulty + persistent._mas_pong_difficulty_change_next_game, 0)
                
                self.COURT_WIDTH = 1280
                self.COURT_HEIGHT = 720
                
                self.BALL_LEFT = 80 - self.BALL_WIDTH / 2
                self.BALL_RIGHT = 1199 + self.BALL_WIDTH / 2
                self.BALL_TOP = self.COURT_TOP + self.BALL_HEIGHT / 2
                self.BALL_BOTTOM = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                
                self.PADDLE_X_PLAYER = 128                                      
                self.PADDLE_X_MONIKA = 1152 - self.PADDLE_WIDTH                 
                
                self.BALL_MAX_SPEED = 2000.0 + self.CURRENT_DIFFICULTY * 100.0
                
                
                
                self.MAX_REFLECT_ANGLE = math.pi / 3
                
                self.MAX_ANGLE = 0.9
                
                
                self.stuck = True
                
                
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                
                
                
                
                self.ctargetoffset = self.get_random_offset()
                
                
                self.computerspeed = 150.0 + self.CURRENT_DIFFICULTY * 30.0
                
                
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)
                
                
                self.bx = self.PADDLE_X_PLAYER + self.PADDLE_WIDTH + 0.1
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0 + self.CURRENT_DIFFICULTY * 25
                
                
                self.ctargety = self.by + self.ctargetoffset
                
                
                self.oldst = None
                
                
                self.winner = None
            
            def get_random_offset(self):
                return random.uniform(-self.PADDLE_RADIUS, self.PADDLE_RADIUS)
            
            def visit(self):
                return [ self.paddle, self.ball, self.player, self.monika, self.ctb ]
            
            def check_bounce_off_top(self):
                
                if self.by < self.BALL_TOP and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_TOP) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_TOP
                    
                    
                    self.by = -self.by + 2 * self.BALL_TOP
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by > self.BALL_BOTTOM:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_BOTTOM) / (self.bounceby - self.by))
                        self.by = self.BALL_BOTTOM
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def check_bounce_off_bottom(self):
                
                if self.by > self.BALL_BOTTOM and self.oldby - self.by != 0:
                    
                    
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_BOTTOM) / (self.oldby - self.by))
                    
                    
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return
                    
                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_BOTTOM
                    
                    
                    self.by = -self.by + 2 * self.BALL_BOTTOM
                    
                    if not self.stuck:
                        self.bdy = -self.bdy
                    
                    
                    
                    if self.by < self.BALL_TOP:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_TOP) / (self.bounceby - self.by))
                        self.by = self.BALL_TOP
                        self.bdy = -self.bdy
                    
                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)
                    
                    return True
                return False
            
            def getCollisionY(self, hotside, is_computer):
                
                
                
                self.collidedonx = is_computer and self.oldbx <= hotside <= self.bx or not is_computer and self.oldbx >= hotside >= self.bx;
                
                if self.collidedonx:
                    
                    
                    if self.oldbx <= self.bouncebx <= hotside <= self.bx or self.oldbx >= self.bouncebx >= hotside >= self.bx:
                        startbx = self.bouncebx
                        startby = self.bounceby
                    else:
                        startbx = self.oldbx
                        startby = self.oldby
                    
                    
                    if startbx - self.bx != 0:
                        return startby + (self.by - startby) * ((startbx - hotside) / (startbx - self.bx))
                    else:
                        return startby
                
                
                else:
                    return self.oldby
            
            
            
            def render(self, width, height, st, at):
                
                
                r = renpy.Render(width, height)
                
                
                if self.oldst is None:
                    self.oldst = st
                
                dtime = st - self.oldst
                self.oldst = st
                
                
                speed = dtime * self.bspeed
                
                
                self.oldbx = self.bx
                self.oldby = self.by
                self.bouncebx = self.bx
                self.bounceby = self.by
                
                
                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed
                
                
                if not self.check_bounce_off_top():
                    self.check_bounce_off_bottom()
                
                
                
                
                
                collisionby = self.getCollisionY(self.PADDLE_X_MONIKA, True)
                if self.collidedonx:
                    self.ctargety = collisionby + self.ctargetoffset
                else:
                    self.ctargety = self.by + self.ctargetoffset
                
                cspeed = self.computerspeed * dtime
                
                
                
                global lose_on_purpose
                if lose_on_purpose and self.bx >= self.COURT_WIDTH * 0.75:
                    if self.bx <= self.PADDLE_X_MONIKA:
                        if self.ctargety > self.computery:
                            self.computery -= cspeed
                        else:
                            self.computery += cspeed
                
                else:
                    cspeed = self.computerspeed * dtime
                    
                    if abs(self.ctargety - self.computery) <= cspeed:
                        self.computery = self.ctargety
                    elif self.ctargety >= self.computery:
                        self.computery += cspeed
                    else:
                        self.computery -= cspeed
                
                
                if self.computery > self.COURT_BOTTOM:
                    self.computery = self.COURT_BOTTOM
                elif self.computery < self.COURT_TOP:
                    self.computery = self.COURT_TOP;
                
                
                def paddle(px, py, hotside, is_computer):
                    
                    
                    
                    
                    
                    
                    pi = renpy.render(self.paddle, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    
                    
                    
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))
                    
                    
                    collisionby = self.getCollisionY(hotside, is_computer)
                    
                    
                    collidedony = py - self.PADDLE_RADIUS - self.BALL_HEIGHT / 2 <= collisionby <= py + self.PADDLE_RADIUS + self.BALL_HEIGHT / 2
                    
                    
                    if not self.stuck and self.collidedonx and collidedony:
                        hit = True
                        if self.oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif self.oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False
                        
                        if hit:
                            
                            
                            angle = (self.by - py) / (self.PADDLE_RADIUS + self.BALL_HEIGHT / 2) * self.MAX_REFLECT_ANGLE
                            
                            if angle >    self.MAX_ANGLE:
                                angle =   self.MAX_ANGLE
                            elif angle < -self.MAX_ANGLE:
                                angle =  -self.MAX_ANGLE;
                            
                            global pong_angle_last_shot
                            pong_angle_last_shot = angle;
                            
                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)
                            
                            global ball_paddle_bounces
                            ball_paddle_bounces += 1
                            
                            
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()
                            
                            if self.playsounds:
                                renpy.sound.play(self.soundboop, channel=1)
                            
                            self.bspeed += 125.0 + self.CURRENT_DIFFICULTY * 12.5
                            if self.bspeed > self.BALL_MAX_SPEED:
                                self.bspeed = self.BALL_MAX_SPEED
                
                
                paddle(self.PADDLE_X_PLAYER, self.playery, self.PADDLE_X_PLAYER + self.PADDLE_WIDTH, False)
                paddle(self.PADDLE_X_MONIKA, self.computery, self.PADDLE_X_MONIKA, True)
                
                
                ball = renpy.render(self.ball, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))
                
                
                player = renpy.render(self.player, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(player, (self.PADDLE_X_PLAYER, 25))
                
                
                monika = renpy.render(self.monika, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (self.PADDLE_X_MONIKA - ew, 25))
                
                
                if self.stuck:
                    ctb = renpy.render(self.ctb, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, ((self.COURT_WIDTH - cw) / 2, 30))
                
                
                
                if self.bx < -200:
                    
                    if self.winner == None:
                        global loss_streak_counter
                        loss_streak_counter += 1
                        
                        if ball_paddle_bounces <= 1:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter += 1
                        else:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter = 0
                    
                    global win_streak_counter
                    win_streak_counter = 0;
                    
                    self.winner = "monika"
                    
                    
                    
                    renpy.timeout(0)
                
                elif self.bx > self.COURT_WIDTH + 200:
                    
                    if self.winner == None:
                        global win_streak_counter
                        win_streak_counter += 1;
                    
                    global loss_streak_counter
                    loss_streak_counter = 0
                    
                    
                    if ball_paddle_bounces > 1:
                        global instant_loss_streak_counter
                        instant_loss_streak_counter = 0
                    
                    self.winner = "player"
                    
                    renpy.timeout(0)
                
                
                
                renpy.redraw(self, 0.0)
                
                
                return r
            
            
            def event(self, ev, x, y, st):
                
                import pygame
                
                
                
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False
                
                
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y
                
                
                
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()

label game_pong:
    hide screen keylistener

    if played_pong_this_session:
        if mas_pong_taking_break:
            $ MAS.MonikaElastic()
            m 1eua "Готов[mas_gender_none] к очередной попытке?"
            $ MAS.MonikaElastic()
            m 2tfb "Покажи мне, на что ты способ[mas_gender_en], [player]!"


            $ mas_pong_taking_break = False
        else:
            $ MAS.MonikaElastic()
            m 1hua "Хочешь сыграть в пинг-понг ещё раз?"
            $ MAS.MonikaElastic()
            m 3eub "Я буду готова тогда же, когда и ты~"
    else:
        $ MAS.MonikaElastic()
        m 1eua "Ты хочешь поиграть в пинг-понг? Хорошо!"
        $ played_pong_this_session = True

    $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

    $ MSR.HideAffIndicator()
    call demo_minigame_pong from _call_demo_minigame_pong
    $ MSR.ShowAffIndicator()
    return

label demo_minigame_pong:

    window hide None


    scene bg pong field


    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        $ playing_okayev = store.songs.getPlayingMusicName() == "Okay, Everyone! (Monika)"


        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    $ ball_paddle_bounces = 0
    $ pong_difficulty_before = persistent._mas_pong_difficulty
    $ powerup_value_this_game = persistent._mas_pong_difficulty_change_next_game
    $ loss_streak_counter_before = loss_streak_counter
    $ win_streak_counter_before = win_streak_counter
    $ instant_loss_streak_counter_before = instant_loss_streak_counter


    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)


    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        call natsuki_name_scare (playing_okayev=playing_okayev) from _call_natsuki_name_scare


    call spaceroom (scene_change=True, force_exp='monika 3eua')


    $ persistent._mas_pong_difficulty_change_next_game = 0;

    if winner == "monika":
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_LOSS

        $ inst_dialogue = store.mas_pong.DLG_WINNER
    else:

        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_WIN

        $ inst_dialogue = store.mas_pong.DLG_LOSER


        if not persistent.ever_won['pong']:
            $persistent.ever_won['pong'] = True

    if new_difficulty < 0:
        $ persistent._mas_pong_difficulty = 0
    else:
        $ persistent._mas_pong_difficulty = new_difficulty;

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    $ MAS.MonikaElastic()
    m 3eua "Ты хочешь сыграть снова?{nw}"
    $ _history_list.pop()
    menu:
        m "Ты хочешь сыграть снова?{fast}"
        "Да.":
            $ MSR.HideAffIndicator()
            $ pong_ev = mas_getEV("mas_pong")
            if pong_ev:

                $ pong_ev.shown_count += 1

            jump demo_minigame_pong
        "Нет.":

            if winner == "monika":
                if renpy.seen_label(store.mas_pong.DLG_WINNER_END):
                    $ end_dialogue = store.mas_pong.DLG_WINNER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_WINNER_END
            else:

                if renpy.seen_label(store.mas_pong.DLG_LOSER_END):
                    $ end_dialogue = store.mas_pong.DLG_LOSER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_LOSER_END

            call expression end_dialogue from _mas_pong_end_dialogue
    return


init -1 python in mas_pong:

    DLG_WINNER = "mas_pong_dlg_winner"
    DLG_WINNER_FAST = "mas_pong_dlg_winner_fast"
    DLG_LOSER = "mas_pong_dlg_loser"
    DLG_LOSER_FAST = "mas_pong_dlg_loser_fast"

    DLG_WINNER_END = "mas_pong_dlg_winner_end"
    DLG_LOSER_END = "mas_pong_dlg_loser_end"


    DLG_BLOCKS = (
        DLG_WINNER,
        DLG_WINNER_FAST,
        DLG_WINNER_END,
        DLG_LOSER,
        DLG_LOSER_FAST,
        DLG_LOSER_END
    )


label mas_pong_dlg_winner:






    if monika_asks_to_go_easy and ball_paddle_bounces == 1:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1rksdla "А-ха-ха..."
        $ MAS.MonikaElastic()
        m 1hksdla "Я знаю, что просила быть полегче со мной... но я не это имела в виду, [player]."
        $ MAS.MonikaElastic()
        m 3eka "Но я ценю такой поступок~"
        $ monika_asks_to_go_easy = False


    elif monika_asks_to_go_easy and ball_paddle_bounces <= 9:
        m 1hub "Ура, я выиграла!"
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Спасибо, [player]!"
        $ MAS.MonikaElastic()
        m 5hubfb "Ты так[mas_gender_oi] мил[mas_gender_iii]...{w=0.5} что позволяешь мне победить~"
        $ monika_asks_to_go_easy = False



    elif ball_paddle_bounces == 1:


        if instant_loss_streak_counter == 1:
            if persistent.msr_voice:
                $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m 2rksdlb "А-ха-ха, как ты мог[mas_gender_g] пропустить подачу?"


        elif instant_loss_streak_counter == 2:
            m 2rksdlc "[player],{w=1} ты опять пропустил[mas_gender_none]..."


        elif instant_loss_streak_counter == 3:
            m 2tfd "[player]!"

            if persistent._mas_pm_ever_let_monika_win_on_purpose:
                $ menu_response = _("Ты опять намеренно поддаёшься мне?")
            else:
                $ menu_response = _("Ты намеренно поддаёшься мне?")

            m 2rkc "[menu_response]"
            $ _history_list.pop()
            menu:
                m "[menu_response]{fast}"
                "Да...":

                    $ MAS.MonikaElastic(voice="monika_giggle")
                    m 1hua "Э-хе-хе!"
                    $ MAS.MonikaElastic()
                    m 1eka "Спасибо, что дал[mas_gender_none] мне выиграть, [player]~"
                    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eka "Но, знаешь, я буду только рада проигрывать тебе иногда."

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        $ MAS.MonikaElastic()
                        m 5eua "Мне нравится видеть, как ты побеждаешь, в той же мере, что и при ином исходе~"

                    $ player_lets_monika_win_on_purpose = True
                    $ persistent._mas_pm_ever_let_monika_win_on_purpose = True
                "Нет.":

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        show monika 1ttu
                        $ MAS.MonikaElastic()
                        m "Ты уверен[mas_gender_none]?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Ты уверен[mas_gender_none]?{fast}"
                            "Да.":

                                call mas_pong_dlg_sorry_assuming
                            "Нет.":

                                $ MAS.MonikaElastic()
                                m 1rfu "[player]!"
                                $ MAS.MonikaElastic()
                                m 2hksdlb "Перестань дразнить меня!"
                                $ player_lets_monika_win_on_purpose = True
                                $ lose_on_purpose = True
                    else:

                        call mas_pong_dlg_sorry_assuming from _call_mas_pong_dlg_sorry_assuming_1
        else:


            if player_lets_monika_win_on_purpose:
                m 2tku "Тебе ещё не надоело поддаваться мне, [player]?"
            else:
                m 1rsc "..."


                if random.randint(1,3) == 1:
                    $ MAS.MonikaElastic()
                    m 1eka "Ну же, [player]!"
                    $ MAS.MonikaElastic()
                    m 1hub "Ты сможешь, я верю в тебя!"


    elif instant_loss_streak_counter_before >= 3 and player_lets_monika_win_on_purpose:
        m 3hub "Хорошая попытка, [player]!"
        $ MAS.MonikaElastic()
        m 3tsu "Но, как видишь, я могу выиграть в одиночку!"
        $ MAS.MonikaElastic(voice="monika_giggle")
        m 3hub "А-ха-ха!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hua "Э-хе-хе~"

        if persistent._mas_pong_difficulty_change_next_game_date == datetime.date.today():
            $ MAS.MonikaElastic()
            m 2tsb "Разве я тебе не говорила, что я на этот раз выиграю?"
        else:
            $ MAS.MonikaElastic()
            m 2ttu "Ты помнишь, [player]?"
            $ MAS.MonikaElastic()
            m 2tfb "Я говорила тебе, что выиграю в следующей игре."


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1rksdla "Оу."
        $ MAS.MonikaElastic()
        m 3hksdlb "Попробуй ещё раз, [player]!"

        $ persistent._mas_pong_difficulty_change_next_game = PONG_PONG_DIFFICULTY_POWERDOWNBIG


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 2rksdlb "А-ха-ха..."
        $ MAS.MonikaElastic()
        m 2eksdla "Я правда надеялась, что ты выиграешь в этой игре."
        $ MAS.MonikaElastic()
        m 2hksdlb "Прости за это, [player]!"


    elif loss_streak_counter >= 3 and loss_streak_counter % 5 == 3:
        m 2eka "Ну же, [player], я знаю, что ты сможешь победить меня..."
        $ MAS.MonikaElastic()
        m 3hub "Продолжай стараться!"


    elif loss_streak_counter >= 5 and loss_streak_counter % 5 == 0:
        m 1eua "Надеюсь, тебе весело, [player]."
        $ MAS.MonikaElastic()
        m 1eka "И потом, я не хочу, чтобы ты расстраивал[mas_gender_sya] из-за игры."
        $ MAS.MonikaElastic()
        m 1hua "Мы всегда можем взять перерыв и сыграть позже, если хочешь."


    elif win_streak_counter_before >= 3:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hub "А-ха-ха!"
        $ MAS.MonikaElastic()
        m 2tfu "Прости, [player]."
        $ MAS.MonikaElastic()
        m 2tub "Похоже, твоя удача закончилась."
        $ MAS.MonikaElastic()
        m 2hub "Настал мой час славы~"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hua "Э-хе-хе!"
        $ MAS.MonikaElastic()
        m 1tub "Не отставай, [player]!"
        $ MAS.MonikaElastic()
        m 2tfu "Похоже, твоя серия побед закончилась!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES


    elif ball_paddle_bounces > 9 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_LONG_GAME:
            m 3eub "Играть против тебя и вправду тяжело, [player]."
            $ MAS.MonikaElastic()
            m 1hub "Продолжай в том же духе, и ты сможешь меня победить, я уверена в этом!"
        else:
            m 3hub "Хорошо сыграно, [player], ты молодец!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1tfu "Но и я не лыком шита,{w=0.1} {nw}"
            extend 1hub "а-ха-ха!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_LONG_GAME


    elif ball_paddle_bounces <= 3:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_SHORT_GAME:
            m 3hub "Очередная быстрая победа на моём счету~"
        else:
            if persistent.msr_voice:
                $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m 4huu "Э-хе-хе,{w=0.1} {nw}"
            extend 4hub "я тебя всё-таки одолела!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_SHORT_GAME


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_TRICKSHOT:
            m 2eksdld "Оу..."
            $ MAS.MonikaElastic()
            m 2rksdlc "Это снова произошло."
            $ MAS.MonikaElastic()
            m 1hksdlb "Прости за это, [player]!"
        else:
            if persistent.msr_voice:
                $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m 2rksdlb "А-ха-ха, прости, [player]!"
            $ MAS.MonikaElastic()
            m 3hksdlb "Я не хотела, чтобы он так сильно отскочил..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_TRICKSHOT
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EASY_GAME:
                m 1eub "Ты сможешь, [player]!"
                $ MAS.MonikaElastic()
                m 3hub "Я верю в тебя~"
            else:
                m 2duu "Сосредоточься, [player]."
                $ MAS.MonikaElastic()
                m 3hub "Продолжай стараться, я знаю, что ты скоро победишь меня!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME:
                m 1hub "Очередной раунд за мной~"
            else:
                if loss_streak_counter > 1:
                    m 3hub "Похоже, я снова победила~"
                else:
                    m 3hua "Похоже, я победила~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_HARD_GAME:
                if persistent.msr_voice:
                    $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
                m 1hub "А-ха-ха!"
                $ MAS.MonikaElastic()
                m 2tsb "Я слишком хорошо для тебя играю?"
                $ MAS.MonikaElastic()
                m 1tsu "Я просто шучу, [player]."
                $ MAS.MonikaElastic()
                m 3hub "Ты и так прекрасно справляешься!"
            else:
                if loss_streak_counter > 1:
                    m 1hub "Я снова победила~"
                else:
                    m 1huu "Я победила~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME:
                m 2tub "Как же приятно побеждать!"
                $ MAS.MonikaElastic()
                m 2hub "Не волнуйся, я уверена, что ты вскоре победишь~"
            else:
                if loss_streak_counter > 1:
                    m 2eub "Очередной раунд за мной!"
                else:
                    m 2eub "Этот раунд за мной!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME:
                m 2duu "Неплохо, [player]."
                $ MAS.MonikaElastic()
                m 4eua "Я старалась изо всех сил, так что не расстраивайся из-за того, что периодически проигрываешь."
                $ MAS.MonikaElastic()
                m 4eub "Продолжай стараться, и тогда ты победишь меня!"
            else:
                m 2hub "На этот раз, победа за мной!"
                $ MAS.MonikaElastic()
                m 2efu "Продолжай стараться, [player]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME

    return



label mas_pong_dlg_sorry_assuming:
    m 3eka "Ладно."
    $ MAS.MonikaElastic()
    m 2ekc "Прости за предположения..."



    $ player_lets_monika_win_on_purpose = False

    m 3eka "Would you like to take a break, [player]?{nw}"
    $ MAS.MonikaElastic()
    m 3eka "Хочешь взять перерыв, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Хочешь взять перерыв, [player]?{fast}"
        "Конечно.":

            $ MAS.MonikaElastic()
            m 1eka "Хорошо, [player]."
            $ MAS.MonikaElastic()
            m 1hua "Мне было весело, спасибо за то, что сыграл[mas_gender_none] со мной в Пинг-понг!"
            $ MAS.MonikaElastic()
            m 1eua "Дай знать, когда будешь готов[mas_gender_none] сыграть ещё раз."


            $ mas_pong_taking_break = True


            show monika idle with dissolve_monika
            jump ch30_loop
        "Нет.":

            $ MAS.MonikaElastic()
            m 1eka "Ладно, [player]. Если ты так уверен[mas_gender_none] в этом."
            $ MAS.MonikaElastic()
            m 1hub "Продолжай стараться, ты скоро победишь меня!"
    return


label mas_pong_dlg_loser:





    $ monika_asks_to_go_easy = False


    if lose_on_purpose:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hub "А-ха-ха!"
        $ MAS.MonikaElastic()
        m 1kua "Теперь мы квиты, [player]!"
        $ lose_on_purpose = False


    elif ball_paddle_bounces == 0:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1rksdlb "А-ха-ха..."

        $ MAS.MonikaElastic()
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL:
            m "Наверное, я должна стараться сильнее..."
        else:
            m "Наверное, я была слишком медленной..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL


    elif instant_loss_streak_counter_before >= 3 and persistent._mas_pm_ever_let_monika_win_on_purpose:
        m 2tsu "Значит, ты сейчас играешь на полном серьёзе?"
        $ MAS.MonikaElastic()
        m 2tfu "Давай посмотрим, насколько ты хорош[mas_gender_none], [player]!"



    elif loss_streak_counter_before >= 3:
        m 4eub "Поздравляю, [player]!"
        $ MAS.MonikaElastic()
        m 2hub "Я знала, что ты победишь в игре после приобретения большого опыта!"
        $ MAS.MonikaElastic()
        m 4eua "Помни, что навыки зачастую приобретаются путём повторных тренировок."
        $ MAS.MonikaElastic()
        m 4hub "Если ты будешь достаточно долго тренироваться, я уверена, ты сможешь достичь всего, к чему стремишься!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 2wuo "Ого..."
        $ MAS.MonikaElastic()
        m 3wuo "На этот раз я правда старалась!"
        $ MAS.MonikaElastic()
        m 1hub "Так держать, [player]!"


    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        if persistent.msr_voice:
            $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
        m 1hua "Э-хе-хе!"
        $ MAS.MonikaElastic()
        m 2hub "Отличная работа, [player]!"


    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 1hua "Я рада, что ты победил[mas_gender_none] на этот раз, [player]."


    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT:
            m 2wuo "[player]!"
            $ MAS.MonikaElastic()
            m 2hksdlb "Я никак не смогла бы так ударить!"
        else:
            m 2wuo "Ого, я никак не смогла бы так ударить!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT


    elif win_streak_counter == 3:
        m 2wuo "Ого, [player]..."
        $ MAS.MonikaElastic()
        m 2wud "Ты выиграл уже три раза подряд..."



        if pong_difficulty_before <= 5:
            $ MAS.MonikaElastic()
            m 2tsu "Наверное, я должна быть с тобой полегче~"


        elif pong_difficulty_before <= 10:
            $ MAS.MonikaElastic()
            m 4hua "У тебя неплохо получается!"


        elif pong_difficulty_before <= 15:
            $ MAS.MonikaElastic()
            m 3hub "Отлично сыграли!"


        elif pong_difficulty_before <= 20:
            $ MAS.MonikaElastic()
            m 4wuo "Это было потрясающе!"
        else:


            $ MAS.MonikaElastic()
            m 2wuo "Ого!"
            $ MAS.MonikaElastic()
            m 2wuw "Ты выиграл меня три раза подряд, а я старалась изо всех сил!"
            $ MAS.MonikaElastic()
            m 2hub "Отличная работа, [player]!"
            $ MAS.MonikaElastic(voice="monika_giggle")
            m 1kua "Э-хе-хе!"


    elif win_streak_counter == 5:
        m 2wud "[player]..."
        $ MAS.MonikaElastic()
        m 2tsu "Сколько времени ты уже тренируешься?"
        $ MAS.MonikaElastic()
        m 3hksdlb "Я не знаю, что произошло, но у меня против тебя не было ни единого шанса!"
        $ MAS.MonikaElastic()
        m 1eka "Не мог[mas_gender_g] бы ты быть со мной полегче, пожалуйста?"
        $ MAS.MonikaElastic()
        m 3hub "Я была бы очень признательна~"
        $ monika_asks_to_go_easy = True


    elif ball_paddle_bounces > 10 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_LONG_GAME:
            m 2wuo "Невероятно, [player]!"
            $ MAS.MonikaElastic()
            m 4hksdlb "Я за тобой не поспеваю!"
        else:
            m 2hub "Потрясающе, [player]!"
            $ MAS.MonikaElastic()
            m 4eub "У тебя неплохо получается!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_LONG_GAME


    elif ball_paddle_bounces <= 2:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME:
            if persistent.msr_voice:
                $ renpy.music.play("sfx/monika_giggle.ogg", channel="sound")
            m 2hksdlb "А-ха-ха..."
            $ MAS.MonikaElastic()
            m 3eksdla "Наверное, я должна стараться сильнее..."
        else:
            m 1rusdlb "Я не ожидала того, что проиграю так быстро."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME
    else:



        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EASY_GAME:
                m 4eub "Да, этот раунд за тобой."
            else:
                if win_streak_counter > 1:
                    m 1hub "Ты снова победил[mas_gender_none]!"
                else:
                    m 1hua "Ты победил[mas_gender_none]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EASY_GAME


        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME:
                m 1eua "Приятно видеть, как ты побеждаешь, [player]."
                $ MAS.MonikaElastic()
                m 1hub "Продолжай в том же духе~"
            else:
                if win_streak_counter > 1:
                    m 1hub "Ты снова победил[mas_gender_none]! Молодец~"
                else:
                    m 1eua "Ты победил[mas_gender_none]! Неплохо."

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME


        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_HARD_GAME:
                m 4hub "Очередная победа за тобой!"
                $ MAS.MonikaElastic()
                m 4eua "Ты молодец, [player]."
            else:
                if win_streak_counter > 1:
                    m 2hub "Ты снова победил[mas_gender_none]! Поздравляю!"
                else:
                    m 2hua "Ты победил[mas_gender_none]! Поздравляю!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_HARD_GAME


        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME:
                m 2wuo "Ого,{w=1} я правда пыталась...{w=1} тебя не остановить!"
                $ MAS.MonikaElastic()
                m 2tfu "Но я уверена, что одолею тебя рано или поздно, [player]."
                $ MAS.MonikaElastic(voice="monika_giggle")
                m 3hub "А-ха-ха!"
            else:
                if win_streak_counter > 1:
                    m 4hub "Ты снова победил[mas_gender_none]! Поразительно!"
                else:
                    m 4hub "Ты победил[mas_gender_none]! Поразительно!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME
        else:


            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME:
                m 3eua "Ты молодец, [player]."
                $ MAS.MonikaElastic()
                m 1hub "Мне нравится играть в Пинг-понг с тобой!"
            else:
                m 1tsu "Это просто нечто!"
                $ MAS.MonikaElastic()
                m 1hub "Ты молодец, [player]!"


            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME
    return



label mas_pong_dlg_loser_fast:
    m 1eka "Ладно, [player]."
    $ MAS.MonikaElastic()
    m 3tfu "Но я одолею тебя в следующий раз."

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERUP;
    $ persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()
    return


label mas_pong_dlg_winner_fast:
    m 1eka "Ладно, [player]."
    $ MAS.MonikaElastic()
    m 1eka "Спасибо, что сыграл со мной в Пинг-понг и поддался мне."
    $ MAS.MonikaElastic()
    m 1hua "Мне было очень весело! Давай как-нибудь ещё сыграем, ладно?"

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERDOWN;
    return


label mas_pong_dlg_loser_end:
    m 1wuo "Ого, на этот раз я старалась изо всех сил."
    $ MAS.MonikaElastic()
    m 1eua "Ты, наверное, упорно тренировал[mas_gender_sya], чтобы добиться таких результатов."
    $ MAS.MonikaElastic()
    m 2tuu "Полагаю, ты хотел[mas_gender_none] впечатлить меня, [player]."
    $ MAS.MonikaElastic()
    m 1hua "Ты так[mas_gender_oi] мил[mas_gender_iii]~"
    return


label mas_pong_dlg_winner_end:
    m 4tku "Я правда не испытываю восторг от того, что эта игра оказалась настолько простой..."
    $ MAS.MonikaElastic()
    m 1eua "Но, по крайней мере, в неё всё равно весело играть."
    $ MAS.MonikaElastic()
    m 1ekbsa "Особенно с тобой, [player]."
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hubfb "А-ха-ха!"
    $ MAS.MonikaElastic()
    m 1ekbfa "Но спасибо, что поддался мне."
    $ MAS.MonikaElastic()
    m 1tku "Только ученики начальных классов всерьёз проигрывают в Пинг-понге, верно?"
    $ MAS.MonikaElastic(voice="monika_giggle")
    m 1hua "Э-хе-хе~"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
