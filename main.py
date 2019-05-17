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
        self.baddie_vel = 2
        pg.mouse.set_visible(False)
        self.paused = False
        self.playing = False
        self.options = False
        self.plat_dist = 40
        self.currentAvat = self.avat1
        self.currentAvatFlip = self.avat1Flip
        self.currentPlat = self.platform
        self.currentRink = self.rink
        self.score = 0
        self.evilie = False
        self.idlable = True
        
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
        self.coin_collection_sound = pg.mixer.Sound(COIN_COLLECTION_SOUND)

        self.avat1 = self.spritesheet.getImage(286, 202, 29, 50)
        self.avat1Flip = self.spritesheet.getImage(255, 202, 29, 50)
        self.avat2 = self.spritesheet.getImage(379, 202, 29, 50)
        self.avat2Flip = self.spritesheet.getImage(534, 202, 29, 50)
        self.avat3 = self.spritesheet.getImage(317, 202, 29, 50)
        self.avat3Flip = self.spritesheet.getImage(410, 202, 29, 50)
        self.avat4 = self.spritesheet.getImage(441, 202, 29, 50)
        self.avat4Flip = self.spritesheet.getImage(348, 202, 29, 50)
        self.avat5 = self.spritesheet.getImage(503, 202, 29, 50)
        self.avat5Flip = self.spritesheet.getImage(472, 202, 29, 50)
        self.badd = self.spritesheet.getImage(213, 202, 40, 40)
        self.baddFlip = self.spritesheet.getImage(171,202, 40, 40)
        self.evil = self.spritesheet.getImage(127, 223, 42, 19)
        self.evilFlip = self.spritesheet.getImage(127,202, 42, 19)
        self.platform = self.spritesheet.getImage(0,202,125,50)
        self.rink = self.spritesheet.getImage(0,0,1000,200)
        self.coin = self.spritesheet.getImage(565,202,20,20)

    def new(self):
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.rink = Platform(self, WIDTH / 2, HEIGHT / 3 * 2, WIDTH, HEIGHT / 3, self.currentRink)
        self.plat1 = Platform(self, random.randrange(int(WIDTH / 8), int(WIDTH / 3)), random.randrange(int(HEIGHT / 5), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.plat2 = Platform(self, random.randrange(int(WIDTH / 3), int(WIDTH / 3 * 2)), random.randrange(int(HEIGHT / 6), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.plat3 = Platform(self, random.randrange(int(WIDTH / 3 * 2), int(WIDTH / 8 * 7)), random.randrange(int(HEIGHT / 5 * 2), int(HEIGHT / 2)), int(WIDTH / 8), HEIGHT / 10, self.currentPlat)
        self.avatar = Avatar(self, self.currentAvat)
        self.baddie = Baddie(self)
        self.platforms.add(self.rink, self.plat1, self.plat2, self.plat3)
        self.check_nearby(self.plat1, self.plat2, self.plat_dist)
        self.check_nearby(self.plat1, self.plat3, self.plat_dist)
        self.check_nearby(self.plat2, self.plat3, self.plat_dist)
        if self.evilie:
            self.evilo = Evilo(self)
        
    def check_nearby(self, spriti, sprito, distance):
        spriti.rect.x -= distance
        hits = pg.sprite.collide_rect(spriti, sprito)
        spriti.rect.x += distance
        if hits: self.restart() 
        spriti.rect.x += distance
        hits = pg.sprite.collide_rect(spriti, sprito)
        spriti.rect.x -= distance
        if hits: self.restart() 
        sprito.rect.x -= distance
        hits = pg.sprite.collide_rect(sprito, spriti)
        sprito.rect.x += distance
        if hits: self.restart() 
        sprito.rect.x += distance
        hits = pg.sprite.collide_rect(sprito, spriti)
        sprito.rect.x -= distance
        if hits: self.restart() 
        spriti.rect.y -= distance
        hits = pg.sprite.collide_rect(spriti, sprito)
        spriti.rect.y += distance
        if hits: self.restart() 
        spriti.rect.y += distance
        hits = pg.sprite.collide_rect(spriti, sprito)
        spriti.rect.y -= distance
        if hits: self.restart()
        sprito.rect.y -= distance
        hits = pg.sprite.collide_rect(sprito, spriti)
        sprito.rect.y += distance
        if hits: self.restart() 
        sprito.rect.y += distance
        hits = pg.sprite.collide_rect(sprito, spriti)
        sprito.rect.y -= distance
        if hits: self.restart() 

    def run(self):
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
            if self.avatar.rect.bottom < lowest.rect.bottom:
                self.avatar.pos.y = lowest.rect.top
                self.avatar.vel.y = 0
                self.avatar.acc.y = 0
                self.avatar.jumping = False

        baddieHits = pg.sprite.collide_rect(self.avatar, self.baddie)
        if baddieHits:
            time.sleep(0.35)
            self.death()
        try:
            eviloHits = pg.sprite.collide_rect(self.avatar, self.evilo)
            if eviloHits:
                time.sleep(0.35)
                self.death()
        except:
            pass
        
        if self.avatar.rect.top >= HEIGHT:
            self.death()
        
        coinHits = pg.sprite.spritecollide(self.avatar, self.coins, True)
        if coinHits:
            self.coin_collection_sound.play()
            self.score += 1
        if not self.coins:
            self.levelUp()

        if self.level >= 2:
            self.evilie = True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.avatar.jump()
                if event.key == pg.K_ESCAPE:
                    self.pause()
                if event.key == pg.K_p:
                    self.pause()
                #if event.key == pg.K_r:
                 #   self.restart()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
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
            self.drawText("CRAZY ICE", 64, BLUE, WIDTH / 2, HEIGHT / 5, self.font1)
            idle(1.5)
            self.drawText("COLLECT ALL OF THE COINS TO LEVEL UP", 18, BLACK, WIDTH / 2, HEIGHT / 11 * 10, self.font2)
            idle(1.5)
            self.drawText("USE THE LEFT, RIGHT, AND UP ARROW KEYS TO MOVE", 18, BLACK, WIDTH / 2, HEIGHT / 11, self.font2)
            idle(1.5)
            self.drawText("HIGH SCORE: " + str(self.highscore), 36, BLUE, WIDTH / 2, HEIGHT / 5 * 4, self.font1)
            idle(1.5)
            avatar = self.currentAvatFlip
            avatar.set_colorkey(YELLOW)
            avatar = pg.transform.scale(avatar, (58,100))
            self.screen.blit(avatar, (WIDTH / 2 - 37, HEIGHT / 2 - 50))
            idle(3)
            self.drawText("PRESS ANY KEY TO BEGIN", 36, NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 3 * 2, self.font2)
            
            self.idlable = False
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()
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
            self.drawText("RESUME", 48, WHITE, WIDTH / 2, HEIGHT / 4, self.font2)
            self.drawText("OPTIONS", 48, WHITE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            self.drawText("MAIN MENU", 48, WHITE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)

            if spot == "RESUME":
                self.drawText("RESUME", 48, SKY_BLUE, WIDTH / 2, HEIGHT / 4, self.font2)
            if spot == "OPTIONS":
                self.drawText("OPTIONS", 48, SKY_BLUE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            if spot == "MAIN MENU":
                self.drawText("MAIN MENU", 48, SKY_BLUE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
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
                            self.playing = False
                            self.paused = False
                            self.score = 0
                            self.level = 1
                            self.start_screen()
                            self.restart()

    def game_over(self):
        moribund = True
        while moribund:
            pg.mixer.music.fadeout(1000)
            self.drawText("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 3, self.font1)
            self.drawText("PRESS ANY KEY TO CONTINUE", 28, NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 7 * 4, self.font2)
            if self.score > self.highscore:
                self.highscore = self.score
                self.drawText("NEW HIGH SCORE!", 36, WHITE, WIDTH / 2, HEIGHT / 5 * 4, self.font2)
                hs_dir = path.join(self.dir, HS_FILE)
                with open(hs_dir, 'w') as f:
                    f.write(str(self.score))
                    self.score = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    moribund = False
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()
                    else:
                        moribund = False
            pg.display.flip()
        self.score = 0
        self.lives = 3
        self.level = 1
        self.baddie_vel = 2
        self.all_sprites.empty()
        time.sleep(0.35)
        self.playing = False
        pg.mixer.music.play(loops = -1)
        self.start_screen()
        self.restart()

    def levelUp(self):
        global time
        self.level += 1
        self.drawText("LEVEL UP!", 48, WHITE, WIDTH / 2, HEIGHT / 5 * 4, self.font2)
        pg.display.flip()
        self.baddie_vel += 0.5
        if self.baddie_vel > 12.0: self.baddie_vel = 12.0
        self.plat_dist += 20
        time.sleep(1)
        self.restart()

    def hud(self):
        lifeLabel = str("LIVES: " + str(self.lives))
        levelLabel = str("LEVEL: " + str(self.level))
        scoreLabel = str("SCORE: " + str(self.score))
        self.drawText(levelLabel, 30, NAVY_BLUE_GREY, WIDTH / 12, HEIGHT / 12, self.font1)
        self.drawText(lifeLabel, 30, NAVY_BLUE_GREY, WIDTH / 12 * 11, HEIGHT / 12, self.font1)
        self.drawText(scoreLabel, 30, NAVY_BLUE_GREY, WIDTH / 2, HEIGHT / 12, self.font1)
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

        def changeMusic(direction): 
            self.j += direction
            if self.j >= 3:
                self.j = 0
            self.museSpot = self.museSpots[self.j]
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.load(self.museSpot)
            pg.mixer.music.play(loops = -1)
            
        def changeAvatar(direction):
            self.l += direction
            if self.l >= 5:
                self.l = 0
            self.avatSpot = self.avatSpots[self.l]
            self.avatFlipSpot = self.avatFlipSpots[self.l]
            self.currentAvat = self.avatSpot
            self.currentAvatFlip = self.avatFlipSpot
            
        while self.options:
            self.screen.fill(BLUE)
            self.drawText("MUSIC", 48, WHITE, WIDTH / 2, HEIGHT / 4, self.font2)
            self.drawText("AVATAR", 48, WHITE, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            self.drawText("GO BACK", 48, WHITE, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            avatar = self.currentAvat
            avatarFlip = self.currentAvatFlip
            avatar.set_colorkey(YELLOW)
            avatarFlip.set_colorkey(YELLOW)
            avatar = pg.transform.scale(avatar, (74,100))
            avatarFlip = pg.transform.scale(avatarFlip, (74,100))
            self.screen.blit(avatar, (WIDTH / 5 * 4 - 74, HEIGHT / 2 - 75))
            self.screen.blit(avatarFlip, (WIDTH / 5, HEIGHT / 2 - 75))

            if spot == "MUSIC":
                self.drawText("MUSIC", 48, MINT, WIDTH / 2, HEIGHT / 4, self.font2)
            if spot == "AVATAR":
                self.drawText("AVATAR", 48, MINT, WIDTH / 2, HEIGHT / 7 * 3, self.font2)
            if spot == "GO BACK":
                self.drawText("GO BACK", 48, MINT, WIDTH / 2, HEIGHT / 5 * 3, self.font2)
            pg.display.flip()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
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
                        changeMusic(-1)
                    if event.key == pg.K_RIGHT:
                        changeMusic(1)
                    if event.key == pg.K_RETURN:
                        if spot == "MUSIC":
                            changeMusic(1)
                        if spot == "AVATAR":
                            changeAvatar(1)
                        if spot == "GO BACK":
                            self.options = False
        
g = Game()
while g.running:
    pg.mixer.music.play(loops = -1)
    g.start_screen()
    g.new()
    g.run()
pg.quit()
