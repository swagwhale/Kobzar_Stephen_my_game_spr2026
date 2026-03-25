import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path

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
            print("collided with a wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width /2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir =='y': 
 
        hits = pg.sprite.spritecollide(sprite ,group, False, collide_hit_rect)
        if hits: 
            print("collided with a wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height /2
            if hits[0].rect.centery < sprite.hit_rect.centery:
               sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height /2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# def ground_under(self, object):
#     rect = object.rect.copy() 
#     rect.height = 5  
#     rect.y = object.rect.bottom  
#     ground_found = None

#     largest_overlap = 0 

#     for ground in self.all_grounds: 
#         if rect.colliderect(ground.rect): 
#             overlap_rect = rect.clip(ground.rect) 
#             overlap_area = overlap_rect.width * overlap_rect.height 

#             if overlap_area > largest_overlap: 
#                 largest_overlap = overlap_area 
#                 ground_found = ground 
#     return ground_found


class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        # use game object and it acces anything in the game, so can do collisions. 
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
        # test for now
        if keys[pg.K_k]:

            ground = self.game.ground_under(self)
            if ground:
                print(ground.tile_type , ground.pos)
            else:
                print("no ground under" )
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

                # if self.direction == "up":
                #     self.image = self.moving_up_frames[0]
                # elif self.direction == "down":
                #     self.image = self.moving_down_frames[0]
                # elif self.direction == "left":
                #     self.image = self.moving_left_frames[0]
                # elif self.direction == "right":
                #     self.image = self.moving_right_frames[0]

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


class Mob(Sprite): 
    # movable object
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = 10

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            print("collided")
            self.speed -=1
            self.new_rect = pg.Rect(self.pos.x, self.pos.y, 100, 100) 
            self.rect = self.new_rect
            self.image.fill(RED)
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
        self.pos += self.speed * self.vel
        self.rect.center = self.pos

class ground(Sprite):
    def __init__(self, game, x ,y, tile ):
        self.groups = game.all_grounds
        Sprite.__init__(self, self.groups) 
        self.game = game

        texture = 'S' # default texture if nothing in parenthesis
        if '(' in tile and ')' in tile: # checks if tile has parentheses
            texture = tile[tile.find('(')+1:tile.find(')')] # checks what is inside the parenthesis
    
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
        elif texture == "w":
            self.image = game.shallow_water_img
        else:
            self.image = game.sand_img



        self.tile_type = texture  # store the tile type so you know what it is

        def __repr__(self):
            return f"<Ground {self.tile_type} at ({self.pos.x},{self.pos.y})>"
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

class NPC(Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def update(self):
        pass