import pygame as pg

WIDTH = 800
HEIGHT = 600

GAME_WIDTH = 533.33333333333 
GAME_HEIGHT = 400

TITLE = "My cool game . . ."
FPS = 60
TILESIZE = 32

# player values settings
PLAYER_SPEED = 150
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE) # hitbox of player

# Projectiles / fishing 
PROJECTILE_SPEED = 400      
PROJECTILE_LASTING_TIME = 1200  # how long it lasts before despawns
PROJECTILE_SIZE = 10
PROJECTILE_INACCURACY = 15 # it is put in degrees so i need to import math  to be able to do it

PROJECTILE_DRAG = 0.95    # how fast it slows down
PROJECTILE_DRIFT = 15  # how much sideways curve
PROJECTILE_SPEED = 600   

#COLOR VALUES 

# constant storing

BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0, 255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)