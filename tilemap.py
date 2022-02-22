import pygame as pg
from variables import *
import pytmx

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        #opens whatever file has the name passed into the function and calls it f
        with open(filename, "rt") as f:
            #loops through each line in the file and adds it to the data list
            for line in f:
                self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        #loads file into pygame because pytmx can be used not in pygame so you need to specify
        #pixelalpha makes it so the tiles are the right transaperncy
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        #how many tiles across the map is * the width of each tile = the size of the total map
        self.width = tm.width * tm.tilewidth
        #same thing but with the height of the map
        self.height = tm.height * tm.tileheight
        #a variable which will hold all the data in this function so that it can be refered to easily
        self.tmxdata = tm

    def render(self, surface):
        #gets the image which corresponds with the tile
        #ti is used because the comand is quite long
        ti = self.tmxdata.get_tile_image_by_gid
        #olny the visible layers will be rendered
        for layer in self.tmxdata.visible_layers:
            #TiledTileLayer because there a multiple types of layers in Tiled
            #and the tile layer is the only one we want to currently render
            if isinstance(layer, pytmx.TiledTileLayer):
                #the x,y and gid for each tile in the layer
                for x, y, gid, in layer:
                    #the tile is equal to the image which corresponds to that tile
                    tile = ti(gid)
                    if tile:
                        #blits the tile at whatever location its supposed to be at
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
                    
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
        
        
        

class Camera:
    def __init__(self, width, height):
        #th epurpose of the camrea is to keep track of which section of the
        #map should be drawn on the screen
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        #the move command moves the rect by the cmaera coords
        return entity.rect.move(self.camera.topleft)
    #works the same as the other one but it can be applied to a rect
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        #adds half the screensize so the the player remians central
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)
        #limits the scrolling to the size of the map
        #make sure x is never bigeer than 0.
        x = min(0,x) #left side
        y = min(0,y) #top side
        x = max(-(self.width - WIDTH),x)#right
        y = max(-(self.height - HEIGHT),y)#bottom
        
        #updates the camera
        self.camera = pg.Rect(x,y, self.width, self.height)
    
 
