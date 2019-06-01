import pygame as pg

TITLE = "Crazy Ice"
WIDTH = 1000
HEIGHT = 600
FPS = 30
screen = pg.display.set_mode((WIDTH, HEIGHT))#, pg.FULLSCREEN)
SPRITESHEET = "sprites.png"
FONT1 = 'trebuchetms'
FONT2 = 'arial'
FONT3 = 'comicsansms'
HS_FILE = 'highscore'

MUSIC3 = "harpsichord_chorale.ogg"
MUSIC1 = "tiptoe_celesta.ogg"
MUSIC2 = "sunset_chorale.ogg"
COIN_SOUND = "coin.ogg"
JUMP_SOUND = "jump.ogg"

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (122,122,122)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,122,0)
PINK = (255,0,255)
VIOLET = (122,0,255)
OFF_WHITE = (200,200,255)
NAVY_BLUE_GREY = (88,88,122)
SKY_BLUE = (122,122,255)
MINT = (0,199,199)

AVATAR_GRAV = HEIGHT / 1000
AVATAR_MOVE_ACC = WIDTH / 6666.67
AVATAR_JUMP = HEIGHT / 40
LIVES = 3
VEL_LIMIT = WIDTH / 1000
