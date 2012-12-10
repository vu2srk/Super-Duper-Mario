import pygame, os
from superMario import *

#include only the pygame constants
from pygame.locals import *

def main():
    #centre the window
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    #initialize all the modules used. No exception will be thrown. (success, faliure) will be returned as a tuple
    pygame.init()
    
    pygame.mouse.set_visible(0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Duper Mario")
    
    SuperMario(screen).start()
