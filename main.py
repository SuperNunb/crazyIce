#!/usr/local/bin/python
import pygame as pg
import random
import time
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = screen
        self.all_sprites = pg.sprite.Group()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.lives = LIVES
        self.font1 = pg.font.match_font(FONT1)
        self.font2 = pg.font.match_font(FONT2)
        self.font3 = pg.font.match_font(FONT3)
        self.level = 1
        self.baddie_vel = WIDTH / 500
        pg.mouse.set_visible(False)
        self.paused = False
        self.playing = False
        self.options = False
        self.currentAvat = self.avat1
        self.currentAvatFlip = self.avat1Flip
        self.currentPlat = self.platform
        self.currentRink = self.rink
        self.score = 1000
        self.evilie = False
        self.idlable = True
        self.eviloAmount = -0.5
        self.stopwatchTimer = 0.00
        
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        sound_dir = path.join(self.dir, 'sound')
        hs_dir = path.join(self.dir, HS_FILE)
        with open(hs_dir, 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.spritesheet = Spritesheet(SPRITESHEET)
        pg.mixer.music.load(MUSIC1)
        pg.mixer.music.set_volume(0.175)
        self.coin_sound = pg.mixer.Sound(COIN_SOUND)
        self.jump_sound = pg.mixer.Sound(JUMP_SOUND)

        self.avat1 = self.spritesheet.getImage(709, 202, 29, 50, 34.48, 12.00)
        self.avat1Flip = self.spritesheet.getImage(678, 202, 29, 50, 34.48, 12.00)
        self.avat2 = self.spritesheet.getImage(647, 202, 29, 50, 34.48, 12.00)
        self.avat2Flip = self.spritesheet.getImage(616, 202, 29, 50, 34.48, 12.00)
        self.avat3 = self.spritesheet.getImage(585, 202, 29, 50, 34.48, 12.00)
        self.avat3Flip = self.spritesheet.getImage(554, 202, 29, 50, 34.48, 12.00)
        self.avat4 = self.spritesheet.getImage(802, 202, 29, 50, 34.48, 12.00)
        self.avat4Flip = self.spritesheet.getImage(771, 202, 29, 50, 34.48, 12.00)
        self.avat5 = self.spritesheet.getImage(740, 202, 29, 50, 34.48, 12.00)
        self.avat5Flip = self.spritesheet.getImage(523, 202, 29, 50, 34.48, 12.00)
        self.badd = self.spritesheet.getImage(355, 202, 40, 40, 25.00, 15.00)
        self.baddFlip = self.spritesheet.getImage(439,202, 40, 40, 25.00, 15.00)
        self.evil = self.spritesheet.getImage(311, 223, 42, 19, 23.81, 31.58)
        self.evilFlip = self.spritesheet.getImage(311,202, 42, 19, 23.81, 31.58)
        self.platform = self.spritesheet.getImage(0,202,125,50, 8.00, 12.00)
        self.rink = self.spritesheet.getImage(0,0,1000,200, 1.00, 3.00)
        self.coin = self.spritesheet.getImage(833,224,20,20, 50.00, 30.00)
        self.glowCoin = self.spritesheet.getImage(833,202,20,20, 50.00, 30.00)
        self.esc = self.spritesheet.getImage(219, 202, 90, 50, 11.11, 12.00)
        self.pse = self.spritesheet.getImage(127, 202, 90, 50, 11.11, 12.00)
        self.leftArrow =  self.spritesheet.getImage(397, 202, 40, 40, 25.00, 15.00)
        self.rightArrow =  self.spritesheet.getImage(481, 202, 40, 40, 25.00, 15.00)

    def new(self):
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.evilos = pg.sprite.Group()
        self.rink = Platform(self, WIDTH / 2, HEIGHT / 3 * 2, WIDTH, HEIGHT / 3, self.currentRink)
        self.plat1 = Platform(self, random.randrange(int(WIDTH / 8.00), int(WIDTH / 4.00)), random.randrange(int(HEIGHT / 4.80), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.plat2 = Platform(self, random.randrange(int(WIDTH / 2.35), int(WIDTH / 1.82)), random.randrange(int(HEIGHT / 6.00), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.plat3 = Platform(self, random.randrange(int(WIDTH / 1.33), int(WIDTH / 1.14)), random.randrange(int(HEIGHT / 2.40), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.avatar = Avatar(self, self.currentAvat)
        self.baddie = Baddie(self)
        self.platforms.add(self.rink, self.plat1, self.plat2, self.plat3)
        if self.evilie:
            eviloIndex = 0
            while eviloIndex < self.eviloAmount:
                self.baddie_vel += (WIDTH / 2000)
                Evilo(self)
                eviloIndex += 1

    def run(self):
        if self.running == False:
            return
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.avatar.rect.y += 1
        platformHits = pg.sprite.spritecollide(self.avatar, self.platforms, False)
        self.avatar.rect.y -= 1
        if platformHits:
            lowest = platformHits[0]
            for hit in platformHits:
                if hit.rect.bottom > lowest.rect.top:
                    lowest = hit
            if self.avatar.pos.y < lowest.rect.centery:
                self.avatar.pos.y = lowest.rect.top
                self.avatar.vel.y = 0
                self.avatar.acc.y = 0
                self.avatar.jumping = False

        baddieHits = pg.sprite.collide_rect(self.avatar, self.baddie)
        if baddieHits:
            time.sleep(0.35)
            self.death()
        try:
            eviloHits = pg.sprite.spritecollide(self.avatar, self.evilos, False)
            if eviloHits:
                time.sleep(0.35)
                self.death()
        except:
            pass
        
        if self.avatar.rect.top >= HEIGHT:
            self.death()

        coinHits = pg.sprite.spritecollide(self.avatar, self.coins, True)
        if coinHits:
            self.coin_sound.play()
            self.score += coinHits[0].coinValue
        if not self.coins:
            self.levelUp()

        if self.level >= 2:
            self.evilie = True

        self.stopwatchTimer += (1/90)
        self.score -= round(self.stopwatchTimer)
        if self.score < 0: self.score = 0 

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_SPACE:
                    self.avatar.jump()
                if event.key == pg.K_ESCAPE:
                    self.pause()
                if event.key == pg.K_p:
                    self.pause()
                if event.key == pg.K_b:
                    self.beatTheGame()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_SPACE:
                    self.avatar.jumpCut()

    def draw(self):
        self.screen.fill(OFF_WHITE)
        self.all_sprites.draw(self.screen)
        self.hud()
        pg.display.flip()

    def drawText(self, msg, size, color, x, y, foonti):
        font = pg.font.Font(foonti, size)
        text_surface = font.render(msg, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
        return text_surface

    def restart(self):
        self.all_sprites.empty()
        self.new()
        self.run()
        
    def restart_soft(self):
        self.avatar.kill()
        self.baddie.kill()
        self.avatar = Avatar(self, self.currentAvat)
        self.baddie = Baddie(self)

    def death(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
        else: self.restart_soft()

    def start_screen(self):
        self.screen.fill(OFF_WHITE)
        self.intro = True
        self.evilie = False
        def idle(seconds):
            if self.idlable:
                pg.display.flip()
                time.sleep(seconds)
            
        while self.intro:
            self.drawText("CRAZY ICE", int(HEIGHT / 9.375), BLUE, WIDTH / 2, HEIGHT / 5, self.font1)
            idle(1.5)
            self.drawText("COLLECT ALL OF THE COINS TO LEVEL UP", int(HEIGHT / 33.333), BLACK, WIDTH / 2, HEIGHT / 11 * 10, self.font2)
            idle(1.5)
            self.drawText("USE THE LEFT, RIGHT, AND UP ARROW KEYS TO MOVE", int(HEIGHT / 33.333), BLACK, WIDTH / 2, HEIGHT / 11, self.font2)
            idle(1.5)
            self.drawText("HIGH SCORE: " + str(self.highscore), int(HEIGHT / 16.667), BLUE, WIDTH / 2, HEIGHT / 5 * 4, self.font1)
            idle(1.5)
            avatar = self.currentAvatFlip
            avatar.set_colorkey(YELLOW)
            avatar = pg.transform.scale(avatar, (int(WIDTH / 17.24), int(HEIGHT / 6.00)))
            self.screen.blit(avatar, (WIDTH / 2 - (WIDTH / 34.48), HEIGHT / 2 - (HEIGHT / 12.00)))
            idle(3)
            self.esc.set_colorkey(YELLOW)
            self.pse.set_colorkey(YELLOW)
            self.screen.blit(self.esc, (WIDTH / 24, HEIGHT / 24))
            self.screen.blit(self.pse, (WIDTH / 24, HEIGHT / 24 + (HEIGHT / 8)))
            self.drawText("PRESS ANY KEY TO BEGIN", int(HEIGHT / 16.667), NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 3 * 2, self.font2)
            
            self.idlable = False
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.intro = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        self.intro = False
                        
                    else:
                        time.sleep(0.35)
                        if not self.paused and not self.playing:
                            self.intro = False
            pg.display.flip()

    def pause(self):
        self.paused = True
        spots = ["RESUME","OPTIONS","MAIN MENU"]
        spot = spots[0]
        i = 0
        while self.paused:
            pg.draw.rect(screen, NAVY_BLUE_GREY, (WIDTH / 48 * 15, HEIGHT / 64 * 6, WIDTH / 48 * 18, HEIGHT / 64 * 52))
            pg.draw.rect(screen, GREY, (WIDTH / 48 * 16, HEIGHT / 64 * 8, WIDTH / 48 * 16, HEIGHT / 64 * 48))
            self.drawText("RESUME", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 4, self.font2)
            self.drawText("OPTIONS", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            self.drawText("MAIN MENU", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)

            if spot == "RESUME":
                self.drawText("RESUME", int(HEIGHT / 12.5), SKY_BLUE, WIDTH / 2, HEIGHT / 4, self.font2)
            if spot == "OPTIONS":
                self.drawText("OPTIONS", int(HEIGHT / 12.5), SKY_BLUE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            if spot == "MAIN MENU":
                self.drawText("MAIN MENU", int(HEIGHT / 12.5), SKY_BLUE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.paused = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = False
                    if event.key == pg.K_p:
                        self.paused = False
                    if event.key == pg.K_DOWN:
                        i += 1
                        if i >= 3:
                            i = 0
                        spot = spots[i]
                    if event.key == pg.K_UP:
                        i -= 1
                        if i <= -1:
                            i = 2
                        spot = spots[i]
                    if event.key == pg.K_RETURN:
                        if spot == "RESUME":
                            self.paused = False
                        if spot == "OPTIONS":
                            self.optionsMenu()
                        if spot == "MAIN MENU":
                            self.paused = False
                            self.reset()

    def game_over(self):
        moribund = True
        while moribund:
            pg.mixer.music.fadeout(1000)
            self.drawText("GAME OVER", int(HEIGHT / 12.5), BLACK, WIDTH / 2, HEIGHT / 3, self.font1)
            self.drawText("PRESS ANY KEY TO CONTINUE", int(HEIGHT / 21.429), NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 7 * 4, self.font1)
            self.saveHighScore((WIDTH / 2, HEIGHT / 5 * 4), WHITE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    moribund = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    self.playing = False
                    moribund = False
                    self.all_sprites.empty()
            pg.display.flip()
        self.reset()

    def saveHighScore(self, pos, color):
        if self.score > self.highscore:
            self.highscore = self.score
            self.drawText("NEW HIGH SCORE!", int(HEIGHT / 16.667), color, pos[0], pos[1], self.font1)
            hs_dir = path.join(self.dir, HS_FILE)
            with open(hs_dir, 'w') as f:
                f.write(str(self.score))
                self.score = 0

    def reset(self):
        self.score = 1000
        self.lives = 3
        self.level = 1
        self.baddie_vel = WIDTH / 500
        self.eviloAmount = 0
        self.all_sprites.empty()
        time.sleep(0.35)
        self.playing = False
        pg.mixer.music.play(loops = -1)
        self.start_screen()
        self.restart()

    def levelUp(self):
        global time
        self.level += 1
        if self.level == 11:
            self.beatTheGame()
        self.drawText("LEVEL UP!", int(HEIGHT / 12.5), BLACK, WIDTH / 2, HEIGHT / 5 * 4, self.font2)
        pg.display.flip()
        self.baddie_vel += (WIDTH / 2000)
        self.eviloAmount += 0.5
        if self.baddie_vel > (WIDTH / 83.333): self.baddie_vel = (WIDTH / 83.333)
        time.sleep(1)
        self.restart()

    def hud(self):
        lifeLabel = str("LIVES: " + str(self.lives))
        levelLabel = str("LEVEL: " + str(self.level))
        scoreLabel = str("SCORE: " + str(self.score))
        self.drawText(levelLabel, int(HEIGHT / 20), NAVY_BLUE_GREY, int(WIDTH / 12), int(HEIGHT / 12), self.font1)
        self.drawText(lifeLabel, int(HEIGHT / 20), NAVY_BLUE_GREY, int(WIDTH / 12 * 11), int(HEIGHT / 12), self.font1)
        self.drawText(scoreLabel, int(HEIGHT / 20), NAVY_BLUE_GREY, int(WIDTH / 2), int(HEIGHT / 12), self.font1)
        pg.display.flip()

    def optionsMenu(self):
        self.options = True
        spots = ["MUSIC","AVATAR","GO BACK"]
        self.museSpots = [MUSIC1, MUSIC2, MUSIC3]
        self.avatSpots = [self.avat1, self.avat2, self.avat3, self.avat4, self.avat5]
        self.avatFlipSpots = [self.avat1Flip, self.avat2Flip, self.avat3Flip, self.avat4Flip, self.avat5Flip]
        spot = spots[0]
        self.museSpot = self.museSpots[0]
        self.avatSpot = self.avatSpots[0]
        self.avatFlipSpot = self.avatFlipSpots[0]
        i = 0
        self.j = 0
        self.l = 0
        arrowY = HEIGHT / 4

        def changeMusic(direction): 
            self.j += direction
            if self.j > 2:
                self.j = 0
            if self.j < 0:
                self.j = 2
            self.museSpot = self.museSpots[self.j]
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.load(self.museSpot)
            pg.mixer.music.play(loops = -1)
            
        def changeAvatar(direction):
            self.l += direction
            if self.l > 4:
                self.l = 0
            if self.l < 0:
                self.l = 4
            self.avatSpot = self.avatSpots[self.l]
            self.avatFlipSpot = self.avatFlipSpots[self.l]
            self.currentAvat = self.avatSpot
            self.currentAvatFlip = self.avatFlipSpot
            
        while self.options:
            self.screen.fill(BLUE)
            self.drawText("MUSIC", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 4, self.font2)
            self.drawText("AVATAR", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            self.drawText("GO BACK", int(HEIGHT / 12.5), WHITE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            avatar = self.currentAvat
            avatarFlip = self.currentAvatFlip
            avatar.set_colorkey(YELLOW)
            avatarFlip.set_colorkey(YELLOW)
            self.leftArrow.set_colorkey(YELLOW)
            self.rightArrow.set_colorkey(YELLOW)
            avatar = pg.transform.scale(avatar, (int(WIDTH / 17.24), int(HEIGHT / 6.00)))
            avatarFlip = pg.transform.scale(avatarFlip, (int(WIDTH / 17.24), int(HEIGHT / 6.00)))
            self.screen.blit(avatar, (WIDTH / 5 * 4 - (WIDTH / 34.48), HEIGHT / 2 - (HEIGHT / 12.00)))
            self.screen.blit(avatarFlip, (WIDTH / 5 + (WIDTH / 34.48), HEIGHT / 2 - (HEIGHT / 12.00)))
            self.screen.blit(self.leftArrow, (WIDTH / 3 - (WIDTH / 50), arrowY))
            self.screen.blit(self.rightArrow, (WIDTH / 3 * 2 - (WIDTH / 50), arrowY))

            if spot == "MUSIC":
                self.drawText("MUSIC", int(HEIGHT / 12.5), MINT, WIDTH / 2, HEIGHT / 4, self.font2)
                arrowY = HEIGHT / 4
            if spot == "AVATAR":
                self.drawText("AVATAR", int(HEIGHT / 12.5), MINT, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
                arrowY = HEIGHT / 7 * 3
            if spot == "GO BACK":
                self.drawText("GO BACK", int(HEIGHT / 12.5), MINT, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
                arrowY = HEIGHT
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.options = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.options = False
                    if event.key == pg.K_p:
                        self.options = False
                        self.paused = False
                    if event.key == pg.K_DOWN:
                        i += 1
                        if i >= 3:
                            i = 0
                        spot = spots[i]
                    if event.key == pg.K_UP:
                        i -= 1
                        if i <= -1:
                            i = 2
                        spot = spots[i]
                    if event.key == pg.K_LEFT:
                        if spot == "MUSIC":
                            changeMusic(-1)
                        if spot == "AVATAR":
                            changeAvatar(-1)
                        if spot == "GO BACK":
                            self.options = False
                    if event.key == pg.K_RETURN or event.key == pg.K_RIGHT:
                        if spot == "MUSIC":
                            changeMusic(1)
                        if spot == "AVATAR":
                            changeAvatar(1)
                        if spot == "GO BACK":
                            self.options = False

    def beatTheGame(self):
        gameBeat = True
        self.screen.fill(OFF_WHITE)
        while gameBeat:            
            self.drawText("YOU BEAT THE GAME!", int(HEIGHT / 12.5), BLUE, WIDTH / 2, HEIGHT / 5 * 2, self.font1)
            self.drawText("PRESS 'R' TO CONTINUE IN RISKY MODE? GAME MAY BECOME UNPLAYABLE", int(HEIGHT / 25), NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            self.drawText("OR YOU CAN RETURN TO THE MAIN MENU BY PRESSING 'M'", int(HEIGHT / 25), NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 5 * 4, self.font2)
            baddPic = self.baddFlip
            baddPic.set_colorkey(YELLOW)
            baddPic = pg.transform.scale(baddPic, (int(WIDTH / 12.5),int(HEIGHT / 7.5)))
            self.screen.blit(baddPic, (WIDTH / 2 - (WIDTH / 30), HEIGHT / 6 + (HEIGHT / 50)))
            self.saveHighScore((WIDTH / 2, HEIGHT / 5 * 3.5), BLUE)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        gameBeat = False
                    if event.key == pg.K_m or event.key == pg.K_ESCAPE:
                        gameBeat = False
                        self.reset()

g = Game()
while g.running:
    pg.mixer.music.play(loops = -1)
    g.start_screen()
    g.new()
    g.run()
pg.quit()
