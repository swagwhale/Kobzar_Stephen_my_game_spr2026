import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *

vec = pg.math.Vector2

MOB_TYPES = [Kingcrab, ]  # all of the mob types.

# I can push from vscode 2

# the game class that will be instantuated in order to run the game. . .  
 
# Design Goals: 
# make a relaxing Make a relaxing fishing game 
# Try to get rich by fishing 
# Expand dock to reach deeper water 
# Deeper waters would have better fish from a loot pool 
# Items and bait can be collection on the map and used to upgrade tools 
# At the end of the game there will be a boss fight  
# NPCs that have quests with rewards 
# Sharks can spawn in waters and you would have to defeat them  
 
class Game:
    def __init__(self): 
        pg.init()
        pg.mixer.init()
        # setting up pygame screen using tuple value for width height
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        ##########################
        #self.window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE) # resizable so you can fullscreen and change size of window
        ##########################
        self.window = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pg.RESIZABLE | pg.SCALED)

        self.screen = self.window  # the resolution inside the window can be changed. 
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.camera = vec(0, 0) # camera offset so that the world moves, 
        self.deadzone_radius = TILESIZE *1.5 # zone where the player can move but camera doesn't 
        self.game_cooldown = Cooldown(5000) # amount of miliseconds till the countdown returns false
        self.fullscreen = False

        # hotbar
        self.selected_slot = 0
        self.hotbar_slots = [None] * SLOT_COUNT
        self.hotbar_slots[0] = "rod"  # put rod in first slot

    def load_data(self):
        self.game_dir = path.dirname(__file__) # file accesses the file space that we are in ex: the level1.txt file or all of the pngs
        # looks inside of images and sounds folders
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'sounds')
        # textures:


        # water levels
        self.shallow_water_img = pg.image.load(path.join(self.img_dir, 'shallow_water_art.png')).convert_alpha()
        self.water_img = pg.image.load(path.join(self.img_dir, 'water_art.png')).convert_alpha()
        self.medium_water_img = pg.image.load(path.join(self.img_dir, 'medium_water_art.png')).convert_alpha()
        self.deep_water_img = pg.image.load(path.join(self.img_dir, 'deep_water_art.png')).convert_alpha()
        self.deep_ocean_img = pg.image.load(path.join(self.img_dir, 'deep_ocean_art.png')).convert_alpha()

        self.wavy_sand_img = pg.image.load(path.join(self.img_dir, 'wavy_sand_art.png')).convert_alpha()
        self.sand_img = pg.image.load(path.join(self.img_dir, 'sand_art.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(self.img_dir, 'stone_wall_art.png')).convert_alpha()
        self.grass_img = pg.image.load(path.join(self.img_dir, 'grass_art.png')).convert_alpha()
        self.sandy_grass_img = pg.image.load(path.join(self.img_dir, 'sandy_grass_art.png')).convert_alpha()
        self.grassy_sand_img = pg.image.load(path.join(self.img_dir, 'grassy_sand_art.png')).convert_alpha()
        self.dirt_img = pg.image.load(path.join(self.img_dir, 'dirt_art.png')).convert_alpha()
        self.wet_sand_img = pg.image.load(path.join(self.img_dir, 'wet_sand_art.png')).convert_alpha()

        # hooks
        self.hook1_img = pg.image.load(path.join(self.img_dir, 'hook_art1.png')).convert_alpha()
        self.hook2_img = pg.image.load(path.join(self.img_dir, 'hook_art2.png')).convert_alpha()
        self.hook3_img = pg.image.load(path.join(self.img_dir, 'hook_art3.png')).convert_alpha()
        self.hook4_img = pg.image.load(path.join(self.img_dir, 'hook_art4.png')).convert_alpha()
        #rod
        self.rod_img1 = pg.image.load(path.join(self.img_dir, "starter_fishing_rod_art.png")).convert_alpha()
        self.rod_img2 = pg.image.load(path.join(self.img_dir, "fishing_rod_art2.png")).convert_alpha()

        # swing rod
        self.rod_img12 = pg.image.load(path.join(self.img_dir, "starter_fishing_rod2.png")).convert_alpha()
        self.rod_img22 = pg.image.load(path.join(self.img_dir, "fishing_rod2.png")).convert_alpha()

        # spools


        
        # sounds
        # self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "pickup.wav"))

        # self.soundtrack_guitar_snd = pg.mixer.Sound(path.join(self.snd_dir, "soundtrack_guitar.mp3"))

        # self.snd_dir = path.join(self.game_dir, 'sounds')
        # self.pickup_snd = pg.mixer.Sound(path.join())

        # check cozart for audio sound help 

        self.gold_icon = pg.image.load(path.join(self.img_dir, 'gold_art.png')).convert_alpha()
        self.gold_icon = pg.transform.smoothscale(self.gold_icon, (32, 32))


        self.map = Map(path.join(self.game_dir, 'map.txt'))
        print('data is loaded')

    def new(self):
        self.load_data()
        # gets all of these cool things from sprites 
        self.all_grounds = pg.sprite.Group()
        self.all_dock_tiles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()

        self.notifications = NotificationManager(self)

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
                # if tile.startswith('P'):
                #     ground(self, col, row, tile)
                #     self.player = Player(self, col, row)
                # if tile.startswith('M'):
                #     ground(self, col, row, tile)
                #     Mob(self,col,row)

        self.player = Player(self, 49 , 42)
        self.camera = vec(GAME_WIDTH/2, GAME_HEIGHT/2) - self.player.pos  # brings camera to player immediatly

        self.rod_level =1
        self.hotbar = Hotbar(self)
        self.npc = NPC(self, 51, 39)
        
        self.gold = 9999999999999999999999999  # starting gold
        self.shop = Shop(self)

        self.hook_level = 1

        # gives player fishing rod on slot 0 or 1

        # self.mob = Kingcrab(self, 16 , 16 )

        # for i in range(MOB_COUNT):
        #     while True: # spawns a crab on a random block of grass (TEST)

        #         x = random.randint(0, self.map.tilewidth - 1)
        #         y = random.randint(0, self.map.tileheight - 1)
        #         tile = self.map.data[y][x]
        #         if tile.startswith('G') and '(G)' in tile:
        #             mob_type = random.choice(MOB_TYPES)
        #             mob_type(self, x, y)
        #             break

            
        # pg.mixer.music.load(path.join(self.snd_dir, "soundtrack_guitar.mp3"))
        # pg.mixer.music.play(loops=-1)

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

            # if event.type == pg.WINDOWMAXIMIZED:
            #     self.fullscreen = not self.fullscreen
            #     if self.fullscreen:
            #         self.window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            #     else:
            #         self.window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)


            if event.type == pg.MOUSEBUTTONUP:
                print("i can get mouse input")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:  # F toggles fullscreen
                    self.fullscreen = not self.fullscreen
                    pg.display.toggle_fullscreen()
                if event.key == pg.K_p:  # TEST, press P to print coords (delete in final)
                    tile_x = int(self.player.pos.x // TILESIZE)
                    tile_y = int(self.player.pos.y // TILESIZE)
                    print(f"tile: {tile_x}, {tile_y}")

                    # if self.fullscreen:
                    #     self.window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN | pg.SCALED)

                    # else:
                    #     self.window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.SCALED)

                if event.key == pg.K_e:
                    if self.npc.is_player_close():
                        self.npc.shop_open = not self.npc.shop_open
                        if self.npc.shop_open:
                            print("Shop opened!")
                        else: 
                            print("Shop closed!")


                self.hotbar.handle_key(event.key) # for the hotbar keys 
                if event.key == pg.K_k:
                    print("i can determine when keys are pressed")
            if self.npc.shop_open:
                self.shop.handle_event(event)
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
    
    def add_to_hotbar(self, item):
        for i in range(len(self.hotbar_slots)):
            if self.hotbar_slots[i] is None:
                self.hotbar_slots[i] = item
                return True
        return False  # hotbar full
    
    def get_selected_item(self): # gives selected item based on key presses
        if 0 <= self.selected_slot < len(self.hotbar_slots):
            return self.hotbar_slots[self.selected_slot]
        return None
    
    def has_fishing_rod_selected(self): # TEST to see if just works for fishing rod
        return self.get_selected_item() == "rod"

    def quit(self):
        pass

    def update(self):
        # updates all of the objects
        self.all_sprites.update()
        self.notifications.update()

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
        self.screen.fill(BLACK)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        
        for sprite in self.all_grounds:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.camera)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.camera)
            
        for projectile in self.all_projectiles: # draws a line from the top of the fishing rod to the projectile
            pg.draw.line(self.screen, BLACK, #
                self.player.rod_tip,
                projectile.pos + self.camera, 2) # 2 pixels wide
        self.player.draw_rod(self.screen, self.camera)  # draws fishing rod after line
        self.hotbar.draw(self.screen) # draws hotbar
        if self.npc.is_player_close():
            self.draw_text("Press E to open shop", 12, WHITE, GAME_WIDTH/2, GAME_HEIGHT - 53)


        # displays amount of gold in corner
        gold_text = self.draw_text_surface(str(self.gold) + "g", 20, (255, 220, 60)) # turns amount of gold into text 
        text_x = GAME_WIDTH - gold_text.get_width() - self.gold_icon.get_width() - 8 # calculates the x at which it should spawn
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]: # creates a black border around the text
            black = self.draw_text_surface(str(self.gold) + "g", 20, BLACK) #creates black text slightly bigger but offseting so black text would go past gold
            self.screen.blit(black, (text_x + dx, 4 + dy))
        self.screen.blit(gold_text, (text_x, 4)) # draws gold text after black text to create border around gold text
        self.screen.blit(self.gold_icon, (text_x + gold_text.get_width() + 2, 4))

        if self.npc.shop_open:
            self.shop.draw(self.screen)
        self.notifications.draw(self.screen)
        #scaled = pg.transform.scale(self.screen, self.window.get_size())
        # self.window.blit(scaled, (0, 0))
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        #draws text, used for npcs later...
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_text_surface(self, text, size, color):
        font = pg.font.Font(path.join(self.game_dir, 'Baloo2-VariableFont_wght.ttf'), size)
        return font.render(text, True, color)


if __name__ == "__main__": # instantiate game
    g = Game()

while g.running:
    g.new()

pg.quit()