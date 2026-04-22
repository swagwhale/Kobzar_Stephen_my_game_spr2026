import pygame as pg

WIDTH = 800
HEIGHT = 600

# GAME_WIDTH = 533.33333333333 
# GAME_HEIGHT = 400

GAME_WIDTH = 400
GAME_HEIGHT = 300

TITLE = "My cool game . . ."
FPS = 60
TILESIZE = 32

# player values settings
PLAYER_SPEED = 150
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE) # hitbox of player

# Projectiles / fishing 
PROJECTILE_SPEED = 200 
PROJECTILE_LASTING_TIME = 3000  # how long it lasts before despawns
PROJECTILE_SIZE = 10
PROJECTILE_INACCURACY = 15 # it is put in degrees so i need to import math  to be able to do it

PROJECTILE_DRAG = 0.95    # how fast it slows down
PROJECTILE_DRIFT = 30  # how much sideways curve
PROJECTILE_SPEED = 600   

FISHING_WAIT_MIN = 2000  # minimum amount of miliseconds before a fish will bite
FISHING_WAIT_MAX = 6000  # max miliseconds before bite

LOOT_TABLES = {
    'w': [  # shallow water
        {'name': 'fish1', 'weight': 5},
        {'name': 'fish2', 'weight': 60},
        {'name': 'fish3', 'weight': 35},
    ],
    'W': [  # water
        {'name': '1fish1', 'weight': 50},
        {'name': '1fish2', 'weight': 40},
        {'name': '1fish3', 'weight': 10},
    ],
    'D': [  # deep water 
        {'name': '2fish1', 'weight': 2},
        {'name': '2fish2', 'weight': 15},
        {'name': '2fish3', 'weight': 83},
    ],  
    'D': [  # deep ocean 
        {'name': '3fish1', 'weight': 2},
        {'name': '3fish2', 'weight': 18},
        {'name': '3fish3', 'weight': 80},
    ]
}

DEFAULT_LOOT = [  #if not water
    {'name': 'Nothing', 'weight': 100},
]



# Mob settings

# MOB_TYPES = [Kingcrab, Worm] # moved to main, because the classes/sprites arent defined in settings
MOB_COUNT = 1 # total amount of mobs

#COLOR VALUES 

# hotbar settings
SLOT_COUNT = 3
SLOT_SIZE = 32  # smaller to fit game resolution
SLOT_MARGIN = 3 # space between each slot
selected_slot = 0
inventory = [None] * SLOT_COUNT

# constant storing

BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0, 255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)