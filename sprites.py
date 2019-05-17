import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def getImage(self, x, y, w, h):
        image = pg.Surface((w,h))
        image.blit(self.spritesheet, (0,0), (x,y,w,h))
        return image

class Avatar(pg.sprite.Sprite):
    def __init__(self, game, avatImg):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = avatImg
        self.image.set_colorkey(YELLOW)
        self.acc = vec(0,AVATAR_GRAV)
        self.vel = vec(0,0)
        self.pos = vec(WIDTH / 2, HEIGHT / 3 * 2)
        self.rect = self.image.get_rect()
        self.jumping = False

    def update(self):
        self.vel.x = 0
        self.acc.y = AVATAR_GRAV
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:             #KEY INPUTS
            self.acc.x -= AVATAR_MOVE_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x += AVATAR_MOVE_ACC

        self.vel += self.acc
        self.pos += self.vel
            
        if self.pos.x >= WIDTH:         #LEFT AND RIGHT EDGES OF SCREEN
            self.acc.x = -self.acc.x / 4
            self.vel.x = 0
            self.pos.x = WIDTH
        if self.pos.x <= 0:
            self.acc.x = -self.acc.x / 4
            self.vel.x = 0
            self.pos.x = 0

        if self.vel.x >= VEL_LIMIT:
            self.vel.x = VEL_LIMIT
        if self.vel.x <= -VEL_LIMIT:
            self.vel.x = -VEL_LIMIT

        if self.vel.x > 0:
            self.image = self.game.currentAvatFlip #self.game.avat1Flip
            self.image.set_colorkey(YELLOW)
        if self.vel.x < 0:
            self.image = self.game.currentAvat #self.game.avat1
            self.image.set_colorkey(YELLOW)
        
        self.rect.midbottom = self.pos

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -AVATAR_JUMP

    def jumpCut(self):
        if self.jumping:
            if self.vel.y < -4:
                self.vel.y = -4

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, sheetPreset):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = sheetPreset
        self.image.set_colorkey(YELLOW)
        self.pos = vec(x,y)
        self.rect = self.image.get_rect()
        self.rect.midtop = self.pos
        if random.randrange(100) < POW_CHANCE and w < WIDTH:
            Coin(self.game, self)

class Baddie(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        self.width = 34
        self.height = 37
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.badd
        self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        
        self.pos = vec(random.choice([0,WIDTH]), HEIGHT / 3 * 2)
        self.vel = vec(self.game.baddie_vel,0)

        if self.pos.x >= WIDTH:
            self.vel.x *= -1

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if self.pos.x > WIDTH or self.pos.x < 0:
            self.vel *= -1

        if self.vel.x > 0:
            self.image = self.game.baddFlip
            self.image.set_colorkey(YELLOW)
        if self.vel.x < 0:
            self.image = self.game.badd
            self.image.set_colorkey(YELLOW)

class Coin(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.image = self.game.coin
        self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 12

    def update(self):
        pass

class Evilo(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.evil
        self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(0, random.randrange(int(WIDTH / 12), int(WIDTH / 5)))
        self.vel = vec(self.game.baddie_vel / 3 * 2, 0)

    def update(self):
        self.rect.center = self.pos
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos = vec(0, random.randrange(int(WIDTH / 12), int(WIDTH / 5)))
        if self.pos.x < 0:
            self.pos = vec(WIDTH, random.randrange(int(WIDTH / 12), int(WIDTH / 5)))

        if self.vel.x > 0:
            self.image = self.game.evilFlip
            self.image.set_colorkey(YELLOW)
        if self.vel.x < 0:
            self.image = self.game.evil
            self.image.set_colorkey(YELLOW)
