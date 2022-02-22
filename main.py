import pygame as pg
from variables import *
from sprites import *
import sys
#allows us to find where the imported files are located
from os import path
from tilemap import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        #initialises pg
        pg.init()
        #allows you to include sound
        pg.mixer.init()
        #create the window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    
        #clock
        self.clock = pg.time.Clock()
        #makes it so if you hold down a key for 500 milliseconds you dont
        #have to keep pressing that key over and over for that movement to
        # repeat
        pg.key.set_repeat(500,100)
        self.load_data()

    def load_data(self):
        #game_folder is where the map.txt file is
        game_folder = path.dirname(__file__)
        #folder where all the images for the game are stored
        img_folder = path.join(game_folder, "Img")
        #folder where all the sounds are stored
        snd_folder = path.join(game_folder, "Sounds")
        #now uses the TiledMap class instead of the Map one.
        self.map = TiledMap(path.join("map.tmx"))
        #runs the code which does the rendering 
        self.map_img = self.map.make_map()
        #so that the map can be located on the screen so the code knows where to draw it
        self.map_rect = self.map_img.get_rect()
        #player images
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMAGE)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.font = path.join(game_folder, "font.ttf")
        #animal images:
        #penguin
        self.penguin_image = pg.image.load(path.join(img_folder, PENGUIN_IMAGE)).convert_alpha()
        self.penguin_image = pg.transform.scale(self.penguin_image, (TILESIZE, TILESIZE))
        #kangaroo
        self.kangaroo_image = pg.image.load(path.join(img_folder, KANGAROO_IMAGE)).convert_alpha()
        self.kangaroo_image = pg.transform.scale(self.kangaroo_image, (TILESIZE, TILESIZE))
        #giraffe
        self.giraffe_image = pg.image.load(path.join(img_folder, GIRAFFE_IMAGE)).convert_alpha()
        self.giraffe_image = pg.transform.scale(self.giraffe_image, (TILESIZE, TILESIZE))
        #zebra
        self.zebra_image = pg.image.load(path.join(img_folder, ZEBRA_IMAGE)).convert_alpha()
        self.zebra_image = pg.transform.scale(self.zebra_image, (TILESIZE, TILESIZE))
        #elephant
        self.elephant_image = pg.image.load(path.join(img_folder, ELEPHANT_IMAGE)).convert_alpha()
        self.elephant_image = pg.transform.scale(self.elephant_image, (TILESIZE, TILESIZE))
        #bear
        self.bear_image = pg.image.load(path.join(img_folder, BEAR_IMAGE)).convert_alpha()
        self.bear_image = pg.transform.scale(self.bear_image, (TILESIZE, TILESIZE))
        #monkey
        self.monkey_image = pg.image.load(path.join(img_folder, MONKEY_IMAGE)).convert_alpha()
        self.monkey_image = pg.transform.scale(self.monkey_image, (TILESIZE, TILESIZE))
        #elk
        self.elk_image = pg.image.load(path.join(img_folder, ELK_IMAGE)).convert_alpha()
        self.elk_image = pg.transform.scale(self.elk_image, (TILESIZE, TILESIZE))
        #hippo
        self.hippo_image = pg.image.load(path.join(img_folder, HIPPO_IMAGE)).convert_alpha()
        self.hippo_image = pg.transform.scale(self.hippo_image, (TILESIZE, TILESIZE))
        
            
        #sound loading
        pg.mixer.music.load(path.join(snd_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        
        
        
                

#GROUPS
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        #spawns the walls
        #enumerate gives the index and the data stored at that index.
        #this section gives the value as tile, the column as an index and the row as an index
        #for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #        #basically if there is a 1 on the map text file then a wall is spawned
        #        if tile == "1":
        #            Wall(self, col, row)
        #        if tile == "M":
        #            Mob(self, col, row)
        #        if tile == "P":
        #            self.player = Player(self, col, row)
        #for the objects in teh object layer of the tiled map
        self.counter = 0
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height/2)
            #if an object is called "Player"
            if tile_object.name == "Player":
                #create an instance of the player class
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "Wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "Mob":
                #create an instance of the mob class
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == "Penguin":
                Penguin(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Kangaroo":
                Kangaroo(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Giraffe":
                Giraffe(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Zebra":
                Zebra(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Elephant":
                Elephant(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Bear":
                Bear(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Monkey":
                Monkey(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Elk":
                Elk(self, obj_center, tile_object.name)
                self.counter += 1
            if tile_object.name == "Hippo":
                Hippo(self, obj_center, tile_object.name)
                self.counter += 1
                
        #tells the camera how big the total player area is
        self.camera= Camera(self.map.width, self.map.height)
        self.paused = False


#GAME LOOP
    def run(self):
        self.running = True
        pg.mixer.music.play(loops=-1)
        while self.running:
            #keeps the loop running at the right speed
            self.dt = self.clock.tick(FPS)/1000
            #runs the events, update and draw functions
            self.events()
            #only updates if paused == False
            if not self.paused:
                self.update()
  
            self.draw()
            
                
    def quit(self):
        #pygame is quit and the window is closed
        pg.quit()
        sys.exit()
    
    #EVENTS
    def events(self):
        events = pg.event.get()
        for event in events:
            #check if the window should be closed
            #if the x button is pressed the quit function is activated
            if event.type == pg.QUIT:
                self.quit()
         


    #START SCREEN
    def start_screen(self):
        self.screen.fill(GREEN)
        self.draw_text("Zoo Game", self.font, 100, BLACK, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Press Spacebar to begin game", self.font, 75, WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        self.draw_text("Press T to see how to play the game", self.font, 50, WHITE, WIDTH/2, HEIGHT*7/8, align="center")
        pg.display.flip()
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    waiting = False
                if event.type == pg.KEYDOWN and event.key == pg.K_t:
                    g.tutorial_screen()
            

    
        
        

    #END SCREEN
    def game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.font, 100, RED, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Press a key to start", self.font, 75, WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        #makes it so any events which were started before the game ends are cleared out of the system
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    #SETTINGS SCREEN
    def settings_screen(self):
        pass

    #TUTORIAL SCREEN
    def tutorial_screen(self):
        self.screen.fill(CYAN)
        self.draw_text("Tutorial", self.font, 100, BLACK, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Collect all the animals to save them, from being poached.", self.font, 25, WHITE, WIDTH/2, HEIGHT*5/8, align="center")
        self.draw_text("Use WASD or the arrow keys to move.", self.font, 25, WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        self.draw_text("Avoid the hunters.", self.font, 25, WHITE, WIDTH/2, HEIGHT*7/8, align="center")
        self.draw_text("Press space to start the game.", self.font, 25, WHITE, WIDTH/2, HEIGHT*1/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def complete_screen(self):
        self.screen.fill(MAGENTA)
        self.draw_text("YOU WIN!", self.font, 100, BLACK, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Congratulations, you saved all the animals from being poached.", self.font, 25, WHITE, WIDTH/2, HEIGHT*5/8, align="center")
        self.draw_text("What a legend", self.font, 25, WHITE, WIDTH/2, HEIGHT*3/4, align="center")
        self.draw_text("Press any key to play again", self.font, 25, WHITE, WIDTH/2, HEIGHT*7/8, align="center")
        pg.display.flip()
        self.wait_for_key()
        g.new()
        

    

    #UPDATE
    def update(self):
        self.all_sprites.update()
        #tells the camera update function that the entity it is following is the player
        self.camera.update(self.player)

        #when there are no more animals left self.playing = False
        if len(self.items) == 0:
            g.complete_screen()

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "Penguin":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Kangaroo":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Giraffe":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Zebra":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Elephant":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Bear":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Monkey":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Elk":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1
        for hit in hits:
            if hit.type == "Hippo":
                hit.kill()
                self.effects_sounds["collect_item"].play()
                self.counter -=1

        pg.display.set_caption(TITLE)
                
                
                
        #mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <=0:
                self.running = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
                
                
        
    
    
    #DRAW
    #draws a grid on the screen
    def draw_grid(self):
        #draws the vertical llines of a grid
        for x in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x,0), (x,HEIGHT))
        #draws the vertical lines of a grid
        for y in range(0,HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLUE, (0,y), (WIDTH, y))
    def draw(self):
        #self.screen.fill(BG_COLOUR)
        #calls draw grip method
        #self.draw_grid()
        #draws the map on the screen and applys the camera to the map_rect
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #draws all the sprites on the screen which are in the all_sprites group
        
        for sprite in self.all_sprites:
            #takes the camera and applys it to all the sprites
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #flips the screen to show what youve drawn on the screen
        #always goes last in the draw section
        draw_player_health(self.screen, 10, 10, self.player.health/ PLAYER_HEALTH)
        self.draw_text('Animals left to save: {}'.format(self.counter), self.font, 30, YELLOW,WIDTH - 10, 10, align="ne")

        
        pg.display.flip()
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

#create the game object which allows the code to actually be run
g = Game()
g.start_screen()
while True:
    g.new()
    g.run()
    g.game_over_screen()


