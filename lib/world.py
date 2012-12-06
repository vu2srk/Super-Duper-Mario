import pygame
from pygame.locals import *

from helpers import *
from components import *

class World:

    def __init__(self, level = 1):
        #converts the image to a different pixel format -- returns pygame.Surface
        self.world = pygame.image.load(filepath("lvl.png")).convert()
        
        self.x = 0
        self.y = 0
        
        for y in range(self.world.get_height()):
            self.y = y
            
            for x in range(self.world.get_width()):
                self.x = x
                
                color = self.world.get_at((self.x, self.y))
                
                if color == (0, 0, 0, 255):
                    Ground((self.x*32, self.y*32))
    
    def color_at(self, dx, dy):
        try:
            return self.world.get_at((self.x+dx, self.y+dy))
        except:
            pass

    def get_size(self):
        return [self.world.get_size()[0]*32, self.world.get_size()[1]*32]
        
