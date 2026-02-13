import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *

vec = pg.math.Vector2

# I can push from vscode

# the game class that will be instantuated in order to run the game. . . 

class Game:
    def __init__(self):
        pg.init()
        # setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000) # amount of miliseconds till the countdown returns false
    
    # method is a function tied to Class

    def load_data(self):
        self.game_dir = path.dirname(__file__) # file accesses the file space that we are in aka the level1.txt file 
        self.map = Map(path.join(self.game_dir,'level1.txt'))
        print("data is loaded succesfully")

    def new(self):
        self.load_data()
        # gets all of these cool things from sprites
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 4, 4) 
        # self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        for row, tiles in enumerate(self.map.data): # builds the map from the level1.txt
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning variable...when
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self,col,row)
        self.run()

    def run(self):
        while self.running:
            # while the game is running it goes back to all of these and keeps them going
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        # things that you , the player does, 
        # stuff that happens with peripherals - keyboard, mouse, microhpone, camera, touchscreen 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            pass
            # if event.type == pg.MOUSEBUTTONUP:
            #     print(event.pos)
            # if event.type == pg.KEYDOWN:
            #     # determines when the key is pressed down.
            #     # W is the keypress to move forward
            #     if event.key == pg.K_w:
            #         pass
            #     # A is the key press to move to the right
            #     if event.key == pg.K_a:
            #         pass      
            #     if event.key == pg.K_s:
            #         pass              
            # if event.type == pg.KEYUP:
            #     # determines when the key is released up.
            #     if event.key == pg.K_w:
            #         pass
            #     if event.key == pg.K_a:
            #         pass
            #     if event.key == pg.K_s:
            #         pass
    def quit(self):
        pass

    def update(self):
        # updates all of the objects  
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()

pg.quit()
