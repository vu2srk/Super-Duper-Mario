import pygame, random, math
from pygame.locals import *

from helpers import *

class Components(pygame.sprite.Sprite):
    
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, groups)

class Mario(Components):
    
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.images_forward = [load_image("mario%d.png" % i) for i in range(1, 5)]
        self.images_backward = [pygame.transform.flip(image, 1, 0) for image in self.images_forward]
        self.image = self.images_forward[0]
        self.rect = self.image.get_rect(topleft = pos)

class Ground(Components):
    
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.image = load_image("platform.png")
        self.rect = self.image.get_rect(topleft = pos)

class Bush(Components):

    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.image = load_image("bush.png")
        self.rect = self.image.get_rect(topleft = pos)

