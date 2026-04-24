import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        # creating data for building map using list.
        self.data = []
        # open file and close it using "with" 
        with open(filename, 'rt') as f: 
            for line in f:
                self.data.append(line.strip().split()) # changed this line so the parenthesis in the map wont cound for spaces. 
                    # but make sure to put a space between each tile or else wont work
                
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

# this class gets images / frames, from the sprite sheet
class Spritesheet:
    def __init__(self, filename): # loads the image 
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height, scale=None): # this extracts a specific piece of the large sheet (with all the textures)
        image = pg.Surface((width, height), pg.SRCALPHA ) # this SRCALPHA allows for the transparent parts of the sprite to be transparent, not black
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        if scale: # to scale images not 32 x 32
            image = pg.transform.scale(image, scale)
        return image
    
    # def load_animation_row(self, row): # defenition so it does'nt make animations in code look messy

    #     frames = []
    #     sheet_width = self.spritesheet.sheet.get_width()

    #     for x in range(0, sheet_width, TILESIZE):
    #         image = self.spritesheet.get_image(x, row * TILESIZE, TILESIZE, TILESIZE)
    #         frames.append(image)

    #     return frames
    def get_row(self, row, tile_size, frames, scale=None):
        return [self.get_image(i * tile_size, row * tile_size, tile_size, tile_size, scale)
                for i in range(frames)]



#class that creates a countdown timer for cooldown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        # allows us to set property for time until cooldown
        self.time = time
        # self.current_time = self.time
    def start(self):
        self.start_time = pg.time.get_ticks()

    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False

# # derived from paarths code
# def draw_corner_brackets(screen, rect, color, corner_len=10, thickness=2, inset=2):
#     """Small L-shaped corners around a screen rect (status FX frame)."""
#     x, y, w, h = rect.x, rect.y, rect.width, rect.height
#     x0, y0 = x + inset, y + inset
#     x1, y1 = x + w - inset, y + h - inset
#     L = max(4, min(corner_len, w // 2 - 2, h // 2 - 2))
#     pg.draw.line(screen, color, (x0, y0), (x0 + L, y0), thickness)
#     pg.draw.line(screen, color, (x0, y0), (x0, y0 + L), thickness)
#     pg.draw.line(screen, color, (x1, y0), (x1 - L, y0), thickness)
#     pg.draw.line(screen, color, (x1, y0), (x1, y0 + L), thickness)
#     pg.draw.line(screen, color, (x0, y1), (x0 + L, y1), thickness)
#     pg.draw.line(screen, color, (x0, y1), (x0, y1 - L), thickness)
#     pg.draw.line(screen, color, (x1, y1), (x1 - L, y1), thickness)
#     pg.draw.line(screen, color, (x1, y1), (x1, y1 - L), thickness)
