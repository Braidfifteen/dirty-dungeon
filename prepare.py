import os
import pygame as pg


# Useful constants.
CAPTION = "Dungeon"
SCREEN_SIZE = (1280, 704)
BACKGROUND_COLOR = pg.Color("gray5")
DIRECT_DICT = {"UP": ( 0,-1),
               "RIGHT" : ( 1, 0),
               "DOWN"  : ( 0, 1),
               "LEFT"  : (-1, 0)}
DIRECTIONS = ("UP", "RIGHT", "DOWN", "LEFT")
CONTROLS = {pg.K_w    : "UP",
            pg.K_d : "RIGHT",
            pg.K_s  : "DOWN",
            pg.K_a  : "LEFT"}
TILE_SIZE = (64, 64)

# Set up environment.
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

