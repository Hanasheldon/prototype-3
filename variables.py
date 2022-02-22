import pygame as pg
#COLOURS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0,)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)

#SETTINGS
WIDTH = 1024
HEIGHT = 768
FPS = 30
TITLE = "Zoo Game"
BG_COLOUR = BLACK

TILESIZE = 64
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

#PLAYER SETTINGS
PLAYER_HEALTH = 100
PLAYER_SPEED = 200
PLAYER_IMG = "mainCharacter.png"
PLAYER_ROT_SPEED= 250 #degrees per second
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)

#MOB SETTINGS
MOB_IMAGE = "hunter.png"
MOB_SPEEDS = [130, 150, 140, 120]
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 500


#MAP SETTINGS
WALL_IMG = "tile_01.png"

#Item_images:
PENGUIN_IMAGE = "penguin.png"
KANGAROO_IMAGE = "kangaroo.png"
GIRAFFE_IMAGE = "giraffe.png"
ZEBRA_IMAGE = "zebra.png"
ELEPHANT_IMAGE = "elephant.png"
BEAR_IMAGE = "bear.png"
MONKEY_IMAGE = "monkey.png"
ELK_IMAGE = "elk.png"
HIPPO_IMAGE = "hippo.png"

#Sounds
BG_MUSIC = "background.mp3"
EFFECTS_SOUNDS = {"collect_item":"collect_item.mp3", "hunter": "hunter.mp3"}




