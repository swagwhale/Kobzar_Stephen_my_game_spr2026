import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
import math
import random

vec = pg.math.Vector2

# creating function, so it is usable for the classes
def collide_hit_rect(one,two): # allows for collision between all objects
    return one.hit_rect.colliderect(two.rect)

# checks if the players x collides with the wall, or the y collides with a wall
# then after checking the direction, it sees if they have the same x coordinate or y coordinate
# then it sets the velocity on that direction to 0

def collide_with_walls(sprite, group, dir):
    # dir is direction
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite ,group, False, collide_hit_rect)
        # sprite collide tells if one collided with two
        # it uses the hit_rect, but we are going to reset its position so it doesnt pass through
        if hits:
            # print("collided with a wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width /2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir =='y': 
        hits = pg.sprite.spritecollide(sprite ,group, False, collide_hit_rect)
        if hits: 
            # print("collided with a wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height /2
            if hits[0].rect.centery < sprite.hit_rect.centery:
               sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height /2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        # use game object and it access anything in the game, so can do collisions. 
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image = self.spritesheet.get_image((0,0,TILESIZE, TILESIZE))
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.jumping = False
        self.walking = False
        self.last_update = 0
        self.current_frame = 0

        self.shoot_cooldown = Cooldown(300) #cooldown for shots of projectiles
        self.shoot_cooldown.start() # then allows for shot again
        self.direction = "down"
        self.space_held = False # holding space wont spam cast, but have to make it initially false so you can cast first try
        # self.direction = "down" # initialy facing down

    def get_keys(self):
        self.vel = vec(0,0)
        #so it doesnt constanty move the charecter around
        keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]:
        #     PLAYER_SPEED *= 2
        if keys[pg.K_a]:
            self.vel.x= - PLAYER_SPEED
            self.walking = True
        if keys[pg.K_d]:
            self.vel.x=   PLAYER_SPEED
            self.walking = True
        if keys[pg.K_w]:
            self.vel.y= - PLAYER_SPEED
            self.walking = True
        if keys[pg.K_s]:
            self.vel.y=   PLAYER_SPEED
            self.walking = True
        if keys[pg.K_m]: # just a test delete later
            if True: # not self.space_held and self.shoot_cooldown.ready(): # if the space isnt held since last frame and cooldown is ready
                self.shoot_cooldown.start()
                self.space_held = True 

                mouse_screen = vec(pg.mouse.get_pos()) # position of mouse (but in the entire screeen, not the game) 
                # now have to turn these positions, in relation to the game:
                scale_x = GAME_WIDTH / self.game.window.get_width()
                scale_y = GAME_HEIGHT / self.game.window.get_height()
                mouse_game = vec(mouse_screen.x * scale_x, mouse_screen.y * scale_y)
                player_screen = self.pos + self.game.camera # world position plus the offset to figure out where player is actually on screen
                direction = mouse_game - player_screen # gives a vector from the player to the mouce
                if direction.length() > 0:
                    direction = direction.normalize()

                    # apply random deviation in degrees
                    angle_offset = random.uniform(-PROJECTILE_INACCURACY, PROJECTILE_INACCURACY) # the random angles are limited by the projectile inaccuracy, (uniform includes decimals)
                    angle_rad = math.radians(angle_offset) # converts angles to radians
                    cos_a = math.cos(angle_rad)
                    sin_a = math.sin(angle_rad)
                    # uses cos and sin for vector
                    deviation = vec(
                        # vector x = direction of x muliplied byt (cos(angle),)
                        direction.x * cos_a - direction.y * sin_a, # sin_a is how much y shifts in the x (minus added so it goes in the right direction)
                        direction.x * sin_a + direction.y * cos_a  # cos a is how much x moves in the y
                    )
                    Projectile(self.game, self.pos.x, self.pos.y, deviation)
                    print('projectile fired')
            else:
                self.space_held = False  # reset when space is released

        if keys[pg.K_SPACE]: 
            if not self.space_held and self.shoot_cooldown.ready(): # if the space isnt held since last frame and cooldown is ready
                self.shoot_cooldown.start()
                self.space_held = True 

                mouse_screen = vec(pg.mouse.get_pos()) # position of mouse (but in the entire screeen, not the game) 
                # now have to turn these positions, in relation to the game:
                scale_x = GAME_WIDTH / self.game.window.get_width()
                scale_y = GAME_HEIGHT / self.game.window.get_height()
                mouse_game = vec(mouse_screen.x * scale_x, mouse_screen.y * scale_y)
                player_screen = self.pos + self.game.camera # world position plus the offset to figure out where player is actually on screen
                direction = mouse_game - player_screen # gives a vector from the player to the mouce
                if direction.length() > 0:
                    direction = direction.normalize()

                    # apply random deviation in degrees
                    angle_offset = random.uniform(-PROJECTILE_INACCURACY, PROJECTILE_INACCURACY) # the random angles are limited by the projectile inaccuracy, (uniform includes decimals)
                    angle_rad = math.radians(angle_offset) # converts angles to radians
                    cos = math.cos(angle_rad)
                    sin = math.sin(angle_rad)
                    deviation_vec = vec(
                        # vector x = direction of x muliplied by (cos(angle),sin(angle)) 
                        direction.x * cos - direction.y * sin, # sin_a is how much y shifts in the x (minus added so it goes in the right direction)
                        direction.x * sin + direction.y * cos  # cos a is how much x moves in the y
                    )
                    Projectile(self.game, self.pos.x, self.pos.y, deviation_vec)
                    print('projectile fired')
        else:
            self.space_held = False  # reset when space is released
            
            # if self.shoot_cooldown.ready():
            #     self.shoot_cooldown.start()
            #     Projectile(self.game, self.pos.x, self.pos.y, self.direction)
            #     print('fired a projectile')

        # test for now
        if keys[pg.K_k]:
            ground = self.game.ground_under(self) # calls ground under from game class
            if ground: # if ground exists
                print(ground.tile_type , ground.pos)
            else:
                print("no ground under (aka void)" )
        # if keys(pg.K_SPACE):
        #     self.dash = True 

        if self.vel.x != 0 and self .vel.y != 0:
            self.vel *= 0.7071

        
    def load_images(self):
        # player animations when walking in different directions
        self.moving_up_frames = self.spritesheet.get_row(0, TILESIZE, 4) 
        self.moving_down_frames = self.spritesheet.get_row(1, TILESIZE, 4)
        self.moving_right_frames = self.spritesheet.get_row(2, TILESIZE, 4)
        self.moving_left_frames = self.spritesheet.get_row(3, TILESIZE, 4)
        
        self.standing_up_frame = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)] # when the player is standing still but facing up.
        
        # for frame in self.standing_up_frame:
        #     frame.set_colorkey(BLACK)  # puts black in the places wehre the player is transparent 
        # for frame in self.moving_up_frames:
        #     frame.set_colorkey(BLACK) 
            
    def animate(self):
        now = pg.time.get_ticks() # now is the tick number that it is at 

        if not self.jumping and not self.walking:  # when isnt walking or jumping it will be in its idle animation
            if now - self.last_update > 350: # waits 350 milliseconds till next frame 
                self.last_update = now
                self.current_frame = (self.current_frame +1) % len(self.standing_up_frame)
                bottom = self.rect.bottom
                self.image = self.standing_up_frame[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif self.moving: # when player is moving, similar to walking because player could be running 
            if now - self.last_update > 150 :# waits 150 milliseconds till next frame
                # if player is walking / running in a certain direction when walking the time between frames slower*
                self.last_update = now
                self.current_frame = (self.current_frame + 1) #% len(self.moving_up_frames)

                if self.direction == "up":
                    frames = self.moving_up_frames
                elif self.direction == "down":
                    frames = self.moving_down_frames
                elif self.direction == "left":
                    frames = self.moving_left_frames
                elif self.direction == "right":
                    frames = self.moving_right_frames

                self.current_frame %= len(frames)
                bottom = self.rect.bottom
                self.image = frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def state_check(self): # just checks if the players velocity is not 0, then it is moving. 
        if self.vel != vec(0,0):
            self.moving = True
        else: 
            self.moving = False

        # determines direction the player is going by looking at velocity. wasd
        if self.vel.x > 0:
            self.direction = "right"
        elif self.vel.x < 0:
            self.direction = "left"
        elif self.vel.y > 0:
            self.direction = "down"
        elif self.vel.y < 0:
            self.direction = "up"

    def update(self):
        # updates the player
        self.get_keys()
        self.state_check()
        self.animate()
        self.rect.center = self.pos  
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        # calls in the collide with wall def, and checks when collodes with wall
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        self.rect.center = self.hit_rect.center

    def swing(self):
        pass


# class Mob(Sprite): 
#     # movable object
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         # self.spritesheet = Spritesheet(path.join(self.game.img_dir, "king_crab_spritesheet_art.png"))

#         self.load_images()

#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.vel = vec(1,0)
#         self.pos = vec(x,y) * TILESIZE
#         self.speed = 10

#     def update(self):
#         hits = pg.sprite.spritecollide(self, self.game.all_players, True)
#         if hits:
#             print("collided with player")
#             self.speed -=1
#             self.new_rect = pg.Rect(self.pos.x, self.pos.y, 100, 100) 
#             self.rect = self.new_rect
#             self.image.fill(RED)
#         if self.rect.x > WIDTH or self.rect.x < 0:
#             self.speed *= -1
#             self.pos.y += TILESIZE
#         self.pos += int(self.speed) * int(self.vel)
#         self.rect.center = self.pos


class Mob(Sprite):
    def __init__(self, game, x, y):
        # most of code in here was taken from the player class
        # this class is used for all mobs
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.game = game
        self.vel = vec(0.0,0.0)
        self.pos = vec(x,y) * TILESIZE

        self.speed = 10
        self.last_update =0
        self.current_frame = 0 
        self.moving = False
        self.direction = "right"

    def update(self):
        self.state_check()
        self.animate()

        # hits = pg.sprite.spritecollide(self, self.game.all_walls, True) # if the mob collides with wall it stops.
        # if hits:
        #     self.speed -=1
        #     self.new_rect = pg.Rect(self.pos.x, self.pos.y, 100, 100) 
        #     self.rect = self.new_rect
        # if self.rect.x > WIDTH or self.rect.x < 0:
        #     self.speed *= -1
        #     self.pos.y += TILESIZE
        
        self.pos += self.vel #self.speed * self.vel
        self.rect.center = self.pos

    # def load_images(self):
    #     # player animations when walking in different directions
    #     SPRITE_SIZE = 64
    #     size = (TILESIZE*2, TILESIZE*2)
        
    #     self.idle_frames    = self.spritesheet.get_row(0, SPRITE_SIZE, 6, size)
    #     # moving up should be reverse of moving down
    #     self.moving_down_frames  = self.spritesheet.get_row(1, SPRITE_SIZE, 8, size)
    #     self.moving_right_frames = self.spritesheet.get_row(3, SPRITE_SIZE, 8, size)
    #     self.moving_left_frames  = self.spritesheet.get_row(3, SPRITE_SIZE, 4, size)

    #     # self.idle_frames   = [self.spritesheet.get_image(0, 0, SPRITE_SIZE, SPRITE_SIZE, size)]
            
    def animate(self):
        now = pg.time.get_ticks() # now is the tick number that it is at 

        if not self.moving:  # when isnt walking or jumping it will be in its idle animation
            if now - self.last_update > 150: # waits 350 milliseconds till next frame 
                self.last_update = now
                self.current_frame = (self.current_frame +1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif self.moving: # when player is moving, similar to walking because player could be running 
            if now - self.last_update > 200 : # waits 150 milliseconds till next frame
                # if player is walking / running in a certain direction when walking the time between frames slower*
                self.last_update = now
                self.current_frame = (self.current_frame + 1)

                if self.direction == "up":
                    frames = self.moving_up_frames
                elif self.direction == "down":
                    frames = self.moving_down_frames
                elif self.direction == "left":
                    frames = self.moving_left_frames
                elif self.direction == "right":
                    frames = self.moving_right_frames

                self.current_frame %= len(frames)
                bottom = self.rect.bottom
                self.image = frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def state_check(self): # just checks if the players velocity is not 0, then it is moving. 
        if self.vel != vec(0,0):
            self.moving = True
        else: 
            self.moving = False

        # determines direction the mob is going by looking at velocity. 
        if abs(self.vel.x) > abs(self.vel.y): # checks if the x is moving more than y, so that mob animation wont always be moving in one direction
            if self.vel.x > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            if self.vel.y > 0:
                self.direction = "down"
            else:
                self.direction = "up"
        # if self.vel.x > 0:
        #     self.direction = "right"
        # elif self.vel.x < 0:
        #     self.direction = "left"
        # elif self.vel.y > 0:
        #     self.direction = "down"
        # elif self.vel.y < 0:
        #     self.direction = "up"

class Kingcrab(Mob): # looks at the mob 
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "king_crab_spritesheet_art.png"))
        self.speed = 60
        self.load_images()
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def load_images(self):
        SPRITE_SIZE = 64
        size = (TILESIZE * 2, TILESIZE * 2)

        self.idle_frames    = self.spritesheet.get_row(0, SPRITE_SIZE, 6, size)
        self.moving_down_frames  = self.spritesheet.get_row(1, SPRITE_SIZE, 8, size)
        # self.moving_up_frames  = self.spritesheet.get_row(1, SPRITE_SIZE, 8, size)
        self.moving_up_frames = list(reversed(self.spritesheet.get_row(1, SPRITE_SIZE, 8, size))) # reverses the animation of moving down
        self.moving_right_frames = self.spritesheet.get_row(3, SPRITE_SIZE, 8, size)
        self.moving_left_frames = [pg.transform.flip(frame, True, False) for frame in self.moving_right_frames]

    def update(self): 
            # move toward player
            to_player = self.game.player.pos - self.pos
            if to_player.length() > 5:
                self.vel = to_player.normalize() * self.speed * self.game.dt
            else:
                self.vel = vec(0, 0)  # fixes bug where even if crab want moving, it would still do moving animations
            self.state_check()
            self.animate()
            self.pos += self.vel
            self.rect.center = self.pos


class ground(Sprite):
    def __init__(self, game, x ,y, tile ):
        self.groups = game.all_grounds
        Sprite.__init__(self, self.groups) 
        self.game = game

        texture = 'S' # default texture if nothing in parenthesis
        if '(' in tile and ')' in tile: # checks if tile has parentheses
            texture = tile[tile.find('(')+1 :tile.find(')')] # checks what is inside the parenthesis
    
        if texture == 'S':
            self.image = game.wavy_sand_img
        elif texture == 's':
            self.image = game.sand_img
        elif texture == 'G':
            self.image = game.grass_img
        elif texture == 'g':
            self.image = game.sandy_grass_img
        elif texture == 'R':
            self.image = game.grassy_sand_img
        elif texture == 'W':
            self.image = game.water_img
        elif texture == 'D':
            self.image = game.deep_water_img
        elif texture == 'd':
            self.image = game.dirt_img
        elif texture == 'b':
            self.image = game.wet_sand_img
        elif texture == "w":
            self.image = game.shallow_water_img
        else:
            self.image = game.sand_img

        self.tile_type = texture  # store the tile type so you know what it is
        # self.image = game.ground_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos

    def update(self):
        pass

# class NPC(Sprite):
#     def __init__(self, game, x,y):
#         self.groups = game.all_sprites
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = game.wall_img
#         self.rect = self.image.get_rect()
#         self.vel = vec(0,0) 
#         self.pos = vec(x,y) * TILESIZE
#         self.rect.center = self.pos

# class Coin(Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites
#         Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.vel = vec(0,0)
#         self.pos = vec(x,y) * TILESIZE
#     def update(self):
#         pass

class Projectile(Sprite):
    def __init__(self, game, x, y, direction_vec):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.image.fill(YELLOW) # change projectile design later . . .

        self.rect = self.image.get_rect()

        # makes projectile spawn in a different place
        spawn_offset = direction_vec * (TILESIZE * 0.6) #0.7)
        self.pos = vec(x, y) + spawn_offset
        self.rect.center = self.pos

        self.vel = direction_vec * (PROJECTILE_SPEED + self.game.player.vel.length())

        # small random sideways drift for the curve effect
        perp = vec(-direction_vec.y, direction_vec.x)  # perpendicular to the cast direction
        drift = random.uniform(-PROJECTILE_DRIFT, PROJECTILE_DRIFT)
        self.drift_vec = perp * drift

        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.vel *= PROJECTILE_DRAG # slows down the particle's speed with drag

        self.vel += self.drift_vec * self.game.dt # adds a slight sideways curve

        self.pos += self.vel * self.game.dt # determining the position based on velocity  and time
        self.rect.center = self.pos # moves projectile to that new position

        if pg.time.get_ticks() - self.spawn_time > PROJECTILE_LASTING_TIME: # if projectile exceeds the lasting time, it kills projectile
            self.kill()

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)  # if it hits a wall it kills the projectile
        if hits:
            self.kill()
        # if it hits a mob. damages it, add later...
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)  # if it hits a wall it kills the projectile
        if hits:
            self.kill()