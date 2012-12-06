import os, pygame
from pygame.locals import *

helpers_path = os.path.abspath(os.path.dirname(__file__))
dir_path = os.path.normpath(os.path.join(helpers_path, '..', 'public'))

def filepath(filename):
    return os.path.join(dir_path, filename)

def load(filename, mode='rb'):

    return open(os.path.join(dir_path, filename), mode)

def load_image(filename):
    filename = filepath(filename)
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    except pygame.error:
        raise SystemExit, "Unable to load: " + filename
    return image.convert_alpha()

