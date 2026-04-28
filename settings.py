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
PLAYER_SPEED = 300 # 125
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE) # hitbox of player

# Projectiles / fishing 
PROJECTILE_SPEED = 200
PROJECTILE_LASTING_TIME = 3000  # how long it lasts before despawns
PROJECTILE_SIZE = 10
PROJECTILE_INACCURACY = 15 # it is put in degrees so i need to import math  to be able to do it

PROJECTILE_DRAG = 0.94    # how fast it slows down
PROJECTILE_DRIFT = 30  # how much sideways curve  

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

# dock settings

DOCK_LAYOUTS = {
    # 1: [  # level 1 dock, small
    #     ["wood_plank20", "wood_plank21", "wood_plank22"],
    #     ["end_bottom1",  "end_bottom2", "end_bottom3"],
    # ],
    1: [  # level 1 dock, small
        ["top_rope1", "top_rope2", "top_rope3", "top_rope4", "top_rope5"],
        ["left_empty", "wood_plank20", "wood_plank21", "wood_plank22", "right_empty"],
        ["left_pole", "wood_plank00", "wood_plank01", "wood_plank02", "right_pole"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "right_empty"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "right_pole"],
        [None, "end_bottom1",  "end_bottom2", "end_bottom3", None],
    ], 
    2: [  # level 2 
        ["top_rope1", "top_rope2", "top_rope3", "top_rope4", "top_rope5"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "right_empty"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "right_pole"],
        ["left_empty", "wood_plank00", "wood_plank01", "wood_plank02", "right_empty"],
        ["left_pole", "wood_plank10", "wood_plank11", "wood_plank12", "right_pole"],
        ["left_empty", "wood_plank20", "wood_plank21", "wood_plank22", "right_empty"],
        ["left_pole", "wood_plank00", "wood_plank01", "wood_plank02", "right_pole"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "right_empty"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "right_pole"],
        [None, "end_bottom1",  "end_bottom2", "end_bottom3", None],
    ],

    3: [  # level 3
        ["top_rope1", "top_rope2",     "top_rope3",    "top_rope4",    "top_rope3",      "top_rope2",    "top_rope3",    "bottom_long_rope1", "bottom_long_rope2", "top_rope5"],
        ["left_empty", "wood_plank20", "wood_plank21", "wood_plank22", "wood_plank10",    "wood_plank20",  "wood_plank21", "wood_plank22" , "wood_plank11" , "right_empty"],
        ["left_pole", "wood_plank00", "wood_plank01", "wood_plank02", "wood_plank20",   "wood_plank00",  "wood_plank01", "wood_plank02","wood_plank21" , "right_pole"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "wood_plank10",     "wood_plank11", "wood_plank12", "wood_plank00", "wood_plank01", "right_pole_con"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "connect_up_down","bottom_rope3",  "bottom_rope4", "bottom_rope3", "bottom_rope4", "bottom_rope5"],
        ["left_empty", "wood_plank00", "wood_plank01", "wood_plank02", "right_empty",    "bottom_poles2",  None, "bottom_poles2", None, "bottom_poles3"],
        ["left_pole", "wood_plank10", "wood_plank11", "wood_plank12", "right_pole"],
        ["left_empty", "wood_plank20", "wood_plank21", "wood_plank22", "right_empty"],
        ["left_pole", "wood_plank00", "wood_plank01", "wood_plank02", "right_pole"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "right_empty"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "right_pole"],
        [None, "end_bottom1",  "end_bottom2", "end_bottom3", None],
    ],
    # add more levels later like 6 or 7
} 

# maps piece names to where they are on the spritesheet (row, col)
DOCK_PIECE_MAP = {
    # rope that goes at end of dock.
    "top_rope1":  (0, 0),
    "top_rope2":   (1, 0),
    "top_rope3":   (2, 0),
    "top_rope4":   (3, 0),
    "top_rope5":   (4, 0),

    "left_pole_con": (0,3),
    "right_pole_con": (4,3),
    # rope on bottom part (with poles. )
    "bottom_rope1":  (0, 4),
    "bottom_rope2":  (1, 4),
    "bottom_rope3":  (2, 4),
    "bottom_rope4":  (3, 4),
    "bottom_rope5":  (4, 4),

    "bottom_long_rope1": (6,1),
    "bottom_long_rope2": (7,1),

    "bottom_poles1": (0,5),
    "bottom_poles2": (2,5),
    "bottom_poles3": (4,5),


    "tops":  (5, 4),
    # left and right ropes go on left and right side of dock patern 
    "left_pole":  (0, 2),
    "right_pole":  (4, 2),

    # without poles. 
    "left_empty":  (8, 3),
    "right_empty":  (8, 2),
    #
    "connect_up_down": (5,0),

    # walkway on the dock, different varietys, 
    # put it together like:
    # 00 01 02
    # 10 11 12
    # 20 21 22

    "wood_plank00":(9, 0),
    "wood_plank01":(10, 0),
    "wood_plank02":(11, 0),
    "wood_plank10":(9, 1),
    "wood_plank11":(10, 1),
    "wood_plank12":(11, 1),
    "wood_plank20":(9, 2),
    "wood_plank21":(10, 2),
    "wood_plank22":(11, 2),
    # end / begining of dock  ( 1 , 2 , 3)
    "end_bottom1":(5, 3),
    "end_bottom2":(6, 3),
    "end_bottom3":(7, 3),

    # add more as you build out the spritesheet
}

# constant storing

BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0, 255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)