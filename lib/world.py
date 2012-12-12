import pygame
from pygame.locals import *

from helpers import *
from components import *

SCALE = 32
DISPLACE = 8

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
                    Ground((self.x * SCALE, self.y * SCALE))
            
                if color == (127, 0, 55, 255):
                    Bush((self.x * SCALE, self.y * SCALE))

                if color == (87, 0, 127, 255):
                   Cloud((self.x * SCALE, self.y * SCALE))

                if color == (91, 127, 0, 255):
                    VenusFlytrap((self.x * SCALE + (DISPLACE * 2), self.y * 28))
                    Pipe((self.x * SCALE, self.y * 28))

                if color == (178, 0, 255, 255):
                    big = True
                    Pipe((self.x * SCALE, self.y * 25), big)
                
                if color == (255, 200, 0, 255):
                    p_type = "air"
                    Ground((self.x * SCALE, self.y * SCALE), p_type)

                if color == (0, 74, 127, 255):
                    p_type = "brick"
                    Ground((self.x * SCALE, self.y * SCALE), p_type)

                if color == (127, 51, 0, 255):
                    QuestionMark((self.x * SCALE, self.y * SCALE))

                if color == (255, 255, 0, 255):
                    Coin((self.x * SCALE + DISPLACE, self.y * SCALE))

                if color == (109, 127, 63, 255):
                    Ground((self.x * SCALE, self.y * SCALE), "brick")

                if color == (255, 233, 127, 255):
                    GrassHill((self.x * SCALE, self.y * 29))

                if color == (0, 127, 70, 255):
                    LifeMushroom((self.x * SCALE, self.y * SCALE))
                
                if color == (80, 63, 127, 255):
                    Castle((self.x * SCALE, self.y * 22))

                if color == (0, 255, 0, 255):
                    Flagpole((self.x * SCALE , self.y * 10))

                if color == (0, 255, 255, 255):
                    BadMushroom((self.x * SCALE, self.y * SCALE))
 
    def color_at(self, dx, dy):
        try:
            return self.world.get_at((self.x+dx, self.y+dy))
        except:
            pass

    def get_size(self):
        return [self.world.get_size()[0] * SCALE, self.world.get_size()[1] * SCALE]
        
