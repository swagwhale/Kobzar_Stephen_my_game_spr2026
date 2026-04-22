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

        self.casting = False
        self.cast_timer = 0
        self.cast_duration = 150
        self.mouse_dir = vec(1, 0) # default direction 
        self.rod_img = pg.image.load(path.join(self.game.img_dir, "starter_fishing_rod2.png")).convert_alpha()
        self.rod_img = pg.transform.scale(self.rod_img, (self.rod_img.get_width() * 1.67, self.rod_img.get_height() * 1.67)) # scales rod with use of transform -> scale
        self.rod_tip = vec(0, 0) # also default . 

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

        if not keys[pg.K_SPACE]:
            self.space_held = False
        if keys[pg.K_SPACE]: 
            if self.game.has_fishing_rod_selected(): # must have rod in my hotbar selected
                if not self.space_held and self.shoot_cooldown.ready(): # if the space isnt held since last frame and cooldown is ready
                    self.shoot_cooldown.start()
                    self.space_held = True
                    mouse_screen = vec(pg.mouse.get_pos()) # position of mouse (but in the entire screeen, not the game) 
                    # now have to turn these positions, in relation to the game:
                    # scale_x = GAME_WIDTH / self.game.window.get_width()
                    # scale_y = GAME_HEIGHT / self.game.window.get_height()

                    win_w, win_h = self.game.window.get_size()
                    scale = min(win_w / GAME_WIDTH, win_h / GAME_HEIGHT)
                    scaled_w = int(GAME_WIDTH * scale)
                    scaled_h = int(GAME_HEIGHT * scale)
                    x_offset = (win_w - scaled_w) // 2
                    y_offset = (win_h - scaled_h) // 2

                    scale_x = GAME_WIDTH / scaled_w
                    scale_y = GAME_HEIGHT / scaled_h
                    mouse_game = vec((mouse_screen.x - x_offset) * scale_x, (mouse_screen.y - y_offset) * scale_y)
                    mouse_game = vec(mouse_screen.x * scale_x, mouse_screen.y * scale_y)




                    player_screen = self.pos + self.game.camera # world position plus the offset to figure out where player is actually on screen
                    direction = mouse_game - player_screen # gives a vector from the player to the mouce
                    if direction.length() > 0:
                        direction = direction.normalize()
                        ###################################################################################
                        self.casting = True
                        self.cast_timer = pg.time.get_ticks()
                        self.mouse_dir = direction  # direction is already calculated there
                        ###################################################################################
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

    def draw_rod(self, screen, camera): 
        if not self.game.has_fishing_rod_selected(): # if the rod isn't selected in the hotbar, then kills all projectiles and cancels casting
            self.casting = False
            for p in list(self.game.all_projectiles):  
                p.kill()
            return

        player_screen = self.pos + camera
        w, h = self.rod_img.get_size()
        angle = 0 


        # swing animation for the rod: 
        if self.casting: # counts time to see how long cast
            elapsed = pg.time.get_ticks() - self.cast_timer
            if elapsed > self.cast_duration:
                self.casting = False
            
            # this is the swing animation for the rod cast, by swinging at where mouse is pointed
            progress = elapsed / self.cast_duration # by changing cast duration, you can change speed of swing
            base_angle = -math.degrees(math.atan2(self.mouse_dir.y, self.mouse_dir.x))
            # adjusted angles to look most realistic: 
            start_angle = base_angle - 170 
            end_angle = base_angle - 20
            angle = start_angle + (end_angle - start_angle) * progress

            tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle))) #this block of code is reused for making the line follow rod, and rod rotate about player
            self.rod_tip = player_screen + tip_dir * h - vec(-tip_dir.y, tip_dir.x) * w


            rotated = pg.transform.rotate(self.rod_img, angle)
            angle_rad = math.radians(angle)
            bl_offset = vec(-w / 2, h / 2)
            rotated_bl = vec(
                bl_offset.x * math.cos(-angle_rad) - bl_offset.y * math.sin(-angle_rad),
                bl_offset.x * math.sin(-angle_rad) + bl_offset.y * math.cos(-angle_rad))
            rotated_rect = rotated.get_rect()
            rotated_rect.center = player_screen - rotated_bl
            screen.blit(rotated, rotated_rect)







        # rod follows the projectile and rotates
        else:
            # checks if there is a projectile to track
            projectiles = list(self.game.all_projectiles) # gets all projectiles in game
            if projectiles:
                to_projectile = projectiles[-1].pos - self.pos # [-1] means it looks at the last projectile thrown
                if to_projectile.length() > 0: # just makes sure the length isnt 0, so arent any dumb errors
                    angle = -math.degrees(math.atan2(to_projectile.y, to_projectile.x))  -10  # converts vector to angle using tan inverse (kind of)
       # flip rod when projectile is to the left
                    if to_projectile.x < 0:
                        angle_rad = math.radians(angle)
                        # tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))
                        # self.rod_tip = player_screen + tip_dir * h + vec(-tip_dir.y, tip_dir.x) * w - tip_dir * 20

                        # tip_dir = vec(math.cos(math.radians(-angle )), math.sin(math.radians(-angle)))
                        # self.rod_tip = player_screen + tip_dir * h

                        # rotated = pg.transform.flip(pg.transform.rotate(self.rod_img, -angle), True , False)

                        tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))
                        rotated = pg.transform.flip(pg.transform.rotate(self.rod_img, -angle +180 ), True , False)
                        # self.rod_tip = player_screen + tip_dir * h + vec(-tip_dir.y, tip_dir.x) * w


                        bl_offset = vec(w / 2, h / 2) # center of image to bottom left 
                        rotated_bl = vec(
                            bl_offset.x * math.cos(-angle_rad ) - bl_offset.y * math.sin(-angle_rad), # used this before when determining rotation of projectiles
                            bl_offset.x * math.sin(-angle_rad) + bl_offset.y * math.cos(-angle_rad))
                        
                        rotated_rect = rotated.get_rect()
                        rotated_rect.center = player_screen + rotated_bl
                        self.rod_tip = player_screen + tip_dir * h + vec(-tip_dir.y, tip_dir.x) * w
                        screen.blit(rotated, rotated_rect)


                    else:
                # if to_projectile.x > 0
                        tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))
                        rotated = pg.transform.rotate(self.rod_img, angle)
                        self.rod_tip = player_screen + tip_dir * h  - vec(-tip_dir.y, tip_dir.x) * w

                        angle_rad = math.radians(angle)
                        # bottom left of rod stays attached to player
                        bl_offset = vec(-w / 2, h / 2) # center of image to bottom left 
                        rotated_bl = vec(
                            bl_offset.x * math.cos(-angle_rad) - bl_offset.y * math.sin(-angle_rad), # used this before when determining rotation of projectiles
                            bl_offset.x * math.sin(-angle_rad) + bl_offset.y * math.cos(-angle_rad))
                        
                        rotated_rect = rotated.get_rect()
                        rotated_rect.center = player_screen - rotated_bl
                        screen.blit(rotated, rotated_rect)
            else: 
                return























        # rotates fishing rod while still keeping it to the player
        # rotated = pg.transform.rotate(self.rod_img, angle)
        # angle_rad = math.radians(angle)
        # original size of fishing rod (because we scale it) 
        # player_screen = self.pos + camera
        # w, h = self.rod_img.get_size()


        # rotated_rect = rotated.get_rect()
        # rotated_rect.center = player_screen - rotated_bl
        # screen.blit(rotated, rotated_rect)

        # player_screen = self.pos + camera #worrld position turned into screen position 
        # rotated_rect = rotated.get_rect()
        # rotated_rect.center = player_screen - rotated_bl

        # tip_dir = vec(math.cos(math.radians(-angle + 90)), math.sin(math.radians(-angle - 90)))
        # self.rod_tip = player_screen + tip_dir * h

        # self.rod_tip = player_screen + tip_dir * h  - vec(-tip_dir.y, tip_dir.x) * w




        # tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))
        # perp = vec(-tip_dir.y, tip_dir.x)  # perpendicular to tip direction
        # self.rod_tip = player_screen + tip_dir * h - perp * w
        # tip_dir = vec(math.cos(math.radians(-angle)), math.sin(math.radians(-angle)))
        # self.rod_tip = vec(rotated_rect.center) + tip_dir * (h * 0.6)
        # self.rod_tip = vec(rotated_rect.topright)

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
        elif texture == 'm':
            self.image = game.medium_water_img
        elif texture == 'D':
            self.image = game.deep_water_img
        elif texture == 'o':
            self.image = game.deep_ocean_img
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


class NPC(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)  # placeholder, swap with spritesheet later typertyuiol, 
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.interaction_range = TILESIZE * 2  # how close player needs to be to interact
        self.shop_open = False

    def is_player_close(self):
        return (self.game.player.pos - self.pos).length() < self.interaction_range

    def update(self):
        if self.is_player_close():
            # show E prompt — for now just prints, swap with UI later
            pass
        else:
            self.shop_open = False  # close shop if player walks away






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

        self.image =  pg.transform.scale(game.hook3_img, (game.hook3_img.get_width() * 0.5, game.hook3_img.get_height() * 0.5)) # add so it checks what level the hook is and changes texture of it
        self.rect = self.image.get_rect()

        # makes projectile spawn in a different place basically so the projectile doesnt spawn on top of player, slightly infront
        spawn_offset = direction_vec * (TILESIZE * 0.6) #0.7)
        self.pos = vec(x, y) + spawn_offset
        self.rect.center = self.pos

        self.vel = direction_vec * (PROJECTILE_SPEED + self.game.player.vel.length())

        # small random sideways drift for the curve effect
        perpendicular = vec(-direction_vec.y, direction_vec.x)  # perpendicular to the cast direction
        projectile_drift = random.uniform(-PROJECTILE_DRIFT, PROJECTILE_DRIFT) # slight drift 
        self.drift_vec = perpendicular * projectile_drift

        self.spawn_time = pg.time.get_ticks()

        self.frozen = False 
        self.fishing_cooldown = None

    def roll_loot(self, loot_table):
        total = sum(item['weight'] for item in loot_table)
        roll = random.uniform(0, total)
        cumulative = 0
        for item in loot_table:
            cumulative += item['weight']
            if roll <= cumulative:
                return item['name']
        return loot_table[-1]['name']
    
    def update(self):
        if self.frozen: #when the projectile has setttles after a slight drift and the timer has ended, the fishing would begin
            if self.fishing_cooldown and self.fishing_cooldown.ready():
                ground = self.game.ground_under(self)
                tile_type = ground.tile_type if ground else None
                loot_table = LOOT_TABLES.get(tile_type, DEFAULT_LOOT)
                result = self.roll_loot(loot_table)
                print(f"You caught: {result}  (tile: {tile_type})")
                self.kill()
            return

        self.vel *= PROJECTILE_DRAG # slows down the particle's speed with drag

        self.vel += self.drift_vec * self.game.dt # adds a slight sideways curve

        self.pos += self.vel * self.game.dt # determining the position based on velocity  and time
        self.rect.center = self.pos # moves projectile to that new position

        if pg.time.get_ticks() - self.spawn_time > PROJECTILE_LASTING_TIME: # if projectile exceeds the lasting time, it becomes frozen
            self.frozen = True
            wait = random.randint(FISHING_WAIT_MIN, FISHING_WAIT_MAX)
            self.fishing_cooldown = Cooldown(wait)
            self.fishing_cooldown.start()
            print(f"Hook settled, waiting {wait}ms for a bite...")
            return

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)  # if it hits a wall it kills the projectile
        if hits:
            self.kill()
        # if it hits a mob. damages it, add later...
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)  # if it hits a wall it kills the projectile
        if hits:
            self.kill()

class Hotbar: # gotten from online source and iterated slightly
    # searched up "how to make simple hotbar with numbers in pygame" and copilot search gave a simple hotbar class

    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont(None, 12) # size, default font

        rod_scale = 1.28  # change this to make it bigger/smaller (multiplying by 1.28 because sprite is 25 pixels, and to scale to show full icon must make 32, so 32/25 = 1.28)
        rod_img = pg.image.load(path.join(self.game.img_dir, "starter_fishing_rod_art.png")).convert_alpha()
        self.item_images = {
            "rod": pg.transform.scale(rod_img, (25 * rod_scale, 25 * rod_scale))
        }

    def draw(self, screen):
        total_hotbar_width = SLOT_COUNT * (SLOT_SIZE + SLOT_MARGIN) + SLOT_MARGIN
        start_hotbar_x = (GAME_WIDTH - total_hotbar_width) // 2 # to know where to start drawing the hot bar, so it it centered
        y = GAME_HEIGHT - SLOT_SIZE - 6  # 6 pixels from the botttom of screen 

        for i in range(SLOT_COUNT):
            x = start_hotbar_x + SLOT_MARGIN + i * (SLOT_SIZE + SLOT_MARGIN)
            color = YELLOW if i == self.game.selected_slot else (180, 180, 180) # selected hotbar makes it coloured yellow
            pg.draw.rect(screen, color, (x, y, SLOT_SIZE, SLOT_SIZE), border_radius=2)
            pg.draw.rect(screen, BLACK, (x, y, SLOT_SIZE, SLOT_SIZE), 1, border_radius=2)

            # draws item inside if slot has something
            if self.game.hotbar_slots[i] is not None:

                item = self.game.hotbar_slots[i]
                if item in self.item_images:
                    screen.blit(self.item_images[item], (x, y))
                else:
                    pg.draw.rect(screen, (200, 200, 200), (x, y, SLOT_SIZE, SLOT_SIZE))  # grey fallback

                #pg.draw.rect(screen, self.game.hotbar_slots[i], (x + 3, y + 3, SLOT_SIZE - 6, SLOT_SIZE - 6))

            # slot number
            num = self.font.render(str(i + 1), True, BLACK)
            screen.blit(num, (x + 2, y + SLOT_SIZE - 10))


    def add_item(self, item_id, count=1):
        for i in range(len(self.hotbar)):
            slot = self.hotbar[i]
            if slot and slot[0] == item_id:
                self.hotbar[i] = (item_id, slot[1] + count)
                return True

        # Second: find lowest empty slot
        for i in range(len(self.hotbar)):
            if self.hotbar[i] is None:
                self.hotbar[i] = (item_id, count)
                return True
        return False  # when hotbar is full
    
    def use_selected(self):
        slot = self.hotbar[self.selected_slot]
        if not slot:
            return

        item_id, count = slot

        if count <= 1:
            self.hotbar[self.selected_slot] = None
        else:
            self.hotbar[self.selected_slot] = (item_id, count - 1)


    def handle_key(self, key):
        if pg.K_1 <= key <= pg.K_9:
            slot = key - pg.K_1
            if slot < SLOT_COUNT:  # only switches if slot actually exists
                self.game.selected_slot = slot