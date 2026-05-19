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
PLAYER_SPEED = 125
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE, TILESIZE) # hitbox of player

# Projectiles / fishing 
PROJECTILE_SPEED = 200
PROJECTILE_LASTING_TIME = 2000  # how long it lasts before despawns
PROJECTILE_SIZE = 10
PROJECTILE_INACCURACY = 15 # it is put in degrees so i need to import math  to be able to do it

PROJECTILE_DRAG = 0.94    # how fast it slows down
# PROJECTILE_DRIFT = 30  # how much sideways curve  
PROJECTILE_DRIFT = 30  # how much sideways curve  

FISHING_WAIT_MIN = 2000  # minimum amount of miliseconds before a fish will bite
FISHING_WAIT_MAX = 6000  # max miliseconds before bite

HOOK_LEVELS = {
    1: {"texture": "hook1_img", "speed": 100,  "lasting_time": 4000, "loot_bonus": 0},
    2: {"texture": "hook2_img", "speed": 125,  "lasting_time": 3750, "loot_bonus": 5},
    3: {"texture": "hook3_img", "speed": 150,  "lasting_time": 3500, "loot_bonus": 10},
    4: {"texture": "hook4_img", "speed": 175,  "lasting_time": 3100, "loot_bonus": 10},
}
ROD_LEVELS = {
    1: {"texture_icon": "rod_img1", "texture": "rod_img12","speed": 100, "loot_bonus": 0, "accuracy": 0},
    2: {"texture_icon": "rod_img2", "texture": "rod_img22","speed": 150, "loot_bonus": 5, "accuracy": 3},
    3: {"texture_icon": "rod_img3", "texture": "rod_img32","speed": 300, "loot_bonus": 10, "accuracy": 5},
    4: {"texture_icon": "rod_img4", "texture": "rod_img42","speed": 400, "loot_bonus": 10, "accuracy": 8},
}





#storm caller, ghost fish, primordial ooze, amberjack, peacock bass,  bigeye tuna,    swordtail,  cutthroat trout, nassau grouper 25kg, steelhead, sawfish 200kg, 
#deepest, medium,           normal ,        shallow,   medium         ,  medium,       ocean,   shallow,       medium ,          , shallow,         medium, 

LOOT_TABLES = {
    'w': [  # shallow water
        {'name': 'guppy', 'weight': 10},
        {'name': 'diver lure', 'weight': 10},
        {'name': 'picasso triggerfish', 'weight': 10},

        {'name': 'largemouth bass', 'weight': 10},
        {'name': 'crawfish crank', 'weight': 10},

        {'name': 'guppy', 'weight': 10},
        {'name': 'guppy', 'weight': 10},
        {'name': 'guppy', 'weight': 10},




    ],
    'W': [  # water
        {'name': 'mjolnir', 'weight': 10},
        {'name': 'asian arowana', 'weight': 10},
        {'name': 'moby dick', 'weight': 50},
        {'name': 'world serpent', 'weight': 40},
        

        {'name': 'asian arowana', 'weight': 10},
    ],
    'm': [  # water
        {'name': 'dragons scale', 'weight': 10},

        {'name': 'mermaids tear', 'weight': 50},

        {'name': 'asian arowana', 'weight': 40},
        {'name': 'asian arowana', 'weight': 10},
    ],
    'D': [  # deep water 
        {'name': 'leviathan scale', 'weight': 10},
        {'name': 'betta', 'weight': 10},

    ],  
    'o': [  # deep ocean 
        {'name': 'stardust', 'weight': 2},
        {'name': 'squid skirt', 'weight': 18},

        # {'name': '3fish3', 'weight': 80},
    ]
}

DEFAULT_LOOT = [  #if not water
    {'name': 'Nothing', 'weight': 100},
]

FISH_DATA = {
    # shallow water
    "guppy":  {"image": "guppy.png", "cost": 1},
    "leviathan scale":  {"image": "leviathan scale.png", "cost": 5},
    "mjolnir":  {"image": "mjolnir.png", "cost": 5},
    "asian arowana":  {"image": "asian arowana.png", "cost": 7},
    "diver lure":  {"image": "asian arowana.png", "cost": 2},
    "dragons scale":  {"image": "dragons scale.png", "cost": 12},
    "picasso triggerfish":  {"image": "picasso triggerfish.png", "cost": 4},
    "world serpent":  {"image": "world serpent.png", "cost": 8},
    "betta":  {"image": "betta.png", "cost": 30},



    "largemouth bass":  {"image": "largemouth bass.png", "cost": 1},
    "crawfish crank":  {"image": "crawfish crank.png", "cost": 1},
    "moby dick":  {"image": "moby dick.png", "cost": 1},
    "mermaids tear":  {"image": "mermaids tear.png", "cost": 1},
    "stardust":  {"image": "stardust.png", "cost": 1},
    "squid skirt":  {"image": "squid skirt.png", "cost": 1},

    # "guppy":  {"image": "guppy.png", "cost": 1},
    # "guppy":  {"image": "guppy.png", "cost": 1},
    # "guppy":  {"image": "guppy.png", "cost": 1},
    # "guppy":  {"image": "guppy.png", "cost": 1},
    # "guppy":  {"image": "guppy.png", "cost": 1},
    # "guppy":  {"image": "guppy.png", "cost": 1},
    # # etc...
    "Nothing": {"image": None},  # no image for nothing
}

# Mob settings

# MOB_TYPES = [Kingcrab, Worm] # moved to main, because the classes/sprites arent defined in settings
MOB_COUNT = 1 # total amount of mobs

#COLOR VALUES 

# hotbar settings
SLOT_COUNT = 10
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

    4: [  # level 4
        ["top_rope1", "top_rope2", "top_rope3", "top_rope4", "top_rope5"],
        ["left_empty", "wood_plank20", "wood_plank21", "wood_plank22", "right_empty"],
        ["left_pole", "wood_plank00", "wood_plank01", "wood_plank02", "right_pole"],
        ["left_empty", "wood_plank10", "wood_plank11", "wood_plank12", "right_empty"],
        ["left_pole", "wood_plank20", "wood_plank21", "wood_plank22", "right_pole"],
        ["left_empty", "wood_plank00", "wood_plank01", "wood_plank02", "right_empty"],

        ["left_pole", "wood_plank10",  "wood_plank11", "wood_plank12",    "top_rope3",      "top_rope2",    "top_rope3",    "bottom_long_rope1", "bottom_long_rope2", "top_rope5"],
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