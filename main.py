import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *

vec = pg.math.Vector2

# I can push from vscode 2

# the game class that will be instantuated in order to run the game. . . 

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # setting up pygame screen using tuple value for width height
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE) # resizable so you can fullscreen and change size of window
        self.screen = pg.Surface((GAME_WIDTH, GAME_HEIGHT))  # the resolution inside the window can be changed. 
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.camera = vec(0, 0) # camera offset so that the world moves, 
        self.deadzone_radius = TILESIZE *1.5 # zone where the player can move but camera doesn't 
        self.game_cooldown = Cooldown(5000) # amount of miliseconds till the countdown returns false
    
    # method is a function tied to Class

    def load_data(self):
        self.game_dir = path.dirname(__file__) # file accesses the file space that we are in ex: the level1.txt file or all of the pngs
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'sounds')
        self.wavy_sand_img = pg.image.load(path.join(self.img_dir, 'wavy_sand_art.png')).convert_alpha()
        self.sand_img = pg.image.load(path.join(self.img_dir, 'sand_art.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(self.img_dir, 'stone_wall_art.png')).convert_alpha()
        self.water_img = pg.image.load(path.join(self.img_dir, 'water_art.png')).convert_alpha()
        self.deep_water_img = pg.image.load(path.join(self.img_dir, 'deep_water_art.png')).convert_alpha()
        self.shallow_water_img = pg.image.load(path.join(self.img_dir, 'shallow_water_art.png')).convert_alpha()
        self.grass_img = pg.image.load(path.join(self.img_dir, 'grass_art.png')).convert_alpha()
        self.sandy_grass_img = pg.image.load(path.join(self.img_dir, 'sandy_grass_art.png')).convert_alpha()
        self.grassy_sand_img = pg.image.load(path.join(self.img_dir, 'grassy_sand_art.png')).convert_alpha()

        # sounds
        # self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "pickup.wav"))
        self.soundtrack_guitar_snd = pg.mixer.Sound(path.join(self.snd_dir, "soundtrack_guitar.mp3"))
        # self.snd_dir = path.join(self.game_dir, 'sounds')
        # self.pickup_snd = pg.mixer.Sound(path.join())

        # check cozart 

        self.map = Map(path.join(self.game_dir, 'map.txt'))
        print('data is loaded')

    def new(self):
        self.load_data()
        # gets all of these cool things from sprites 
        self.all_grounds = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 4, 4) 
        # self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        for row, tiles in enumerate(self.map.data): # builds the map from the level1.txt
            for col, tile, in enumerate(tiles):
                # if tile == ['P', 'M', '']
                if tile.startswith('G'):
                    ground(self, col, row, tile)
                if tile.startswith('W'):
                    # call class constructor without assigning variable..
                    Wall(self, col, row)
                if tile.startswith('P'):
                    ground(self, col, row, tile)
                    self.player = Player(self, col, row)
                if tile.startswith('M'):
                    ground(self, col, row, tile)
                    Mob(self,col,row)

        pg.mixer.music.load(path.join(self.snd_dir, "soundtrack_guitar.mp3"))
        pg.mixer.music.play(loops=-1)

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
            if event.type == pg.MOUSEBUTTONUP:
                print("i can get mouse input")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    print("i can determine when keys are pressed")


            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    print("i can determine when keys are released")

    def ground_under(self, object): # this function just checks what ground is under the object. 
        rect = object.rect.copy() # creates a rectangle copy of the object

        largest_overlap = 0 
        ground_found = None # if no ground under, reterns None

        for ground in self.all_grounds: # checks for all grounds
            if rect.colliderect(ground.rect): 
                overlap_rect = rect.clip(ground.rect) 
                overlap_area = overlap_rect.width * overlap_rect.height # calculates the area of the 
                if overlap_area > largest_overlap: # picks the ground we are on the most, not which we touch first
                    largest_overlap = overlap_area 
                    ground_found = ground 
        return ground_found

    def quit(self):
        pass

    def update(self):
        # updates all of the objects
        self.all_sprites.update()

        # used ai to figure out how to move map, so I commented explaining how it works. 
        player_screen_pos = self.player.pos + self.camera # you need to determine where the player is on the screen, not in the world

        center = vec(GAME_WIDTH/2, GAME_HEIGHT/2) # where the center of the screen is 
        offset = player_screen_pos - center # offset is the direction + distance from center
        distance = offset.length()

        if distance > self.deadzone_radius: # if the distance traveled by player surpases the circle then...
            move_back = offset.normalize() * (distance - self.deadzone_radius) # pushes the player back to the edge of the deadzone radius

            if move_back.length() > 0.5:  
                self.camera -= move_back * 0.1  # self.camera is how much the world has moved, and the 0.1 can change the speed that the camera moves. 

    def draw(self):
        self.screen.fill(BLUE)

        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        for sprite in self.all_grounds:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.camera)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.camera)
        scaled = pg.transform.scale(self.screen, self.window.get_size()) # stretches the resolution screen to the window
        self.window.blit(scaled, (0,0)) # draws scaled version at (0,0)

        pg.display.flip()


    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__": # instantiate game
    g = Game()

while g.running:
    g.new()

pg.quit()