import pygame as pg
from variables import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
from random import choice, random
def collide_with_walls(sprite,group, dir):
    #if the direction of the player is along the x axis 
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        #then the code checks if the player sprite is hitting any wall sprites
        if hits:
            #if the player is on teh right side of the wall
            if hits[0].rect.centerx  > sprite.hit_rect.centerx:
                #if it is then the x becomes the coordinate of the thing its hitting minus the width of the player
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2 #/2 so that we are using the center
            #if the player is on the left side of the wall
            if hits[0].rect.centerx  < sprite.hit_rect.centerx:
                #if its not then the x becomes the coordinates of the right corner
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
            #x displacememnt becomes 0
            sprite.vel.x = 0
            #the rect x coordinate becomes sprite.x
            sprite.hit_rect.centerx= sprite.pos.x
    #if the direction of the player is along the y axis
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        #then the code checks if the player sprite is hitting any wall sprites
        if hits:
            #if the player is underneath the wall
            if hits[0].rect.centery  > sprite.hit_rect.centery:
                #if it is then the y becomes the coordinate of the thing its hitting minus the height of the player
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            #if the player is above a wall
            if hits[0].rect.centery  < sprite.hit_rect.centery:
                #if its not then the y becomes the coordinates of the bottom
                sprite.pos.y = hits[0].rect.bottom +sprite.hit_rect.height/2
            sprite.vel.y = 0
            #y displacememnt becomes 0
            sprite.hit_rect.centery= sprite.pos.y
            #the rect y coordinate becomes self.y


class Player(pg.sprite.Sprite):
    #player sprite
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img       
        #the rectangle that encloses the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        #vectors
        self.vel = vec(0,0)
        self.pos = vec(x,y)
        #0 degrees means the player will be pointing directly to the right
        self.rot = 0
        self.health = PLAYER_HEALTH
        self.paused = False


    def get_keys(self):
        self.rot_speed = 0
        #the velocity of the sprite is the vector (0,0)
        self.vel = vec(0,0)
        keys =pg.key.get_pressed()
        #when the left arrow or the A key is pressed the player rotates to the left
        if keys[pg.K_LEFT] or keys [pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        #when the right arrow key or D is pressed the player rotates to the right
        if keys[pg.K_RIGHT] or keys [pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        #moves the player forwards
        if keys[pg.K_UP] or keys [pg.K_w]:
            #the vec prodecure does trigonometry so that the code is simpler for us
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        #moves the player backwards at half speed.
        if keys[pg.K_DOWN] or keys [pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)
        if keys[pg.K_p]:
            self.paused = not self.paused



    def update(self):
        self.get_keys()
        #the rotation is the rotation plus (the speed multiplied by the
        #game time step). this value is then divided by 360 and the remainder is obtained.
        self.rot = (self.rot +self.rot_speed * self.game.dt)%360
        #position attribute becomes position + the velocity multiplied
        #by the gmae time step
        #rotates the player sprite
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        #update the player rect
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        
        
        #sets the centre of the rectangle to the position of the player sprite
        self.rect.center = self.pos
        #sets the rect to the x and y coordinates
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls,"x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls,"y")
        self.rect.center = self.hit_rect.center
        if self.health <=0:
            self.kill()
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #make it a member of the sprites group and the mobs group
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.rot =0
        self.vel= vec(0,0)
        self.acc = vec(0,0)
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        
    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                #works out position vector between the mob and the player
                dist = self.pos- mob.pos
                #if that position vector is withing the range that the avoid radius applies to 
                if 0< dist.length() < AVOID_RADIUS:
                    #the acceleration = the acceleration + the position vector we just worked out
                    self.acc += dist.normalize()
        
    def update(self):
        #distance worked out using vectors
        target_dist = self.target.pos - self.pos
        #uses squared because its faster for the computer to work out than square root
        if target_dist.length_squared() < DETECT_RADIUS**2:
            #hunter sounds
            #random number is less than 0.002
            if random() < 0.002:
                #play the hunter sound effect
                self.game.effects_sounds["hunter"].play()
            #the rotation is worked out using the distance we found
            self.rot = target_dist.angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            #acceleration to be the vector of the mob speed but rotated
            #in the negative direction of the rot value 
            self.acc = vec(1,0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            #then add vel multiplied by -1 so that there is a max speed
            self.acc += self.vel*-1
            #vel = vel+ (acc * game time step)
            self.vel += self.acc * self.game.dt
            #uses s=ut + 1/2at^2
            self.pos += self.vel* self.game.dt + 0.5* self.acc * self.game.dt **2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, "x")
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, "y")
            self.rect.center = self.hit_rect.center
        
    
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #make it a member of the sprites group and the walls group
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #makes the actual walls
        self.image = game.wall_img

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    #the x,y and width and height parameters are all passed into the function
    def __init__(self, game, x, y, w, h):
        #make it a member of the walls group
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #creates a rect of the object using the x,y
        #coords and the width and height of the object
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
#penguin
class Penguin(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.penguin_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Kangaroo(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.kangaroo_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Giraffe(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.giraffe_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Zebra(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zebra_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Elephant(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.elephant_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Bear(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bear_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Monkey(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.monkey_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Elk(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.elk_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos

class Hippo(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        #adds it to the all_sprites group and the animals group
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.hippo_image
        self.rect = self.image.get_rect()
        self.type = type
        #the rect is at the position the item is at in the tiled map
        self.rect.center = pos



        












        



        
