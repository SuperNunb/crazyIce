import pygame as pg

TITLE = "Crazy Ice"
WIDTH = 1000
HEIGHT = 600
FPS = 30
screen = pg.display.set_mode((WIDTH, HEIGHT))
SPRITESHEET = "sprites.png"
FONT1 = 'trebuchetms'
FONT2 = 'arial'
FONT3 = 'comicsansms'
HS_FILE = 'highscore'

MUSIC3 = "harpsichord_chorale.ogg"
MUSIC1 = "tiptoe_celesta.ogg"
MUSIC2 = "sunset_chorale.ogg"
COIN_COLLECTION_SOUND = "coin.ogg"

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

AVATAR_GRAV = 0.6
AVATAR_MOVE_ACC = 0.15
AVATAR_JUMP = 12.5
LIVES = 3
POW_CHANCE = 100
VEL_LIMIT = 1
