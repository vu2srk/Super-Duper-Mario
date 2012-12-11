import pygame
from random import randint
from pygame.locals import *

from helpers import *

FORWARD = 1
BACKWARD = -1

FLYTRAP_TOP = 310
FLYTRAP_BOTTOM = 370

TOP    = 0
RIGHT  = 1
BOTTOM = 2
LEFT = 3

def which_side(dx,dy):
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    if dy < 0:
        return TOP
    elif dx > 0:
        return RIGHT
    elif dy > 0:
        return BOTTOM
    elif dx < 0:
        return LEFT
    else:
        return 0, 0

class Components(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.collision_groups = []

    def collidesWith(self, group):
        if group not in self.collision_groups:
            self.collision_groups.append(group)

    def move(self, dx, dy):
        if dx!=0:
            self.__move(dx,0)
        if dy!=0:
            self.__move(0,dy)

    def __move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
        for sprite_group in self.collision_groups:
            for sprite in sprite_group:
                if sprite.rect.colliderect(self.rect):
                    collided_side = which_side(dx, dy)
                    self.on_collision(collided_side, sprite)

    def dealWithCollision(self, sprite, side):
        if side == TOP:
            self.rect.top = sprite.rect.bottom
        if side == RIGHT:
            self.rect.right = sprite.rect.left
        if side == BOTTOM:
            self.rect.bottom = sprite.rect.top
        if side == LEFT:
            self.rect.left = sprite.rect.right

class Mario(Components):
    
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.forward_images = [load_image("mario1.png"), load_image("mario2.png"), load_image("mario3.png"), load_image("mario4.png"), load_image("mario1.png"), load_image("mario5.png")]
        self.backward_images = [pygame.transform.flip(image, 1, 0) for image in self.forward_images]
        self.jumping_images = [self.forward_images[5], self.backward_images[5]]
        self.image = self.forward_images[0]
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = FORWARD
        self.is_jumping = False
        self.jump_speed = 0
        self.accel = 0.3
        self.frame = 0

        self.jump_sound = load_sound("jump.ogg")

    def on_collision(self, side, sprite):
        self.dealWithCollision(sprite, side)
        if side == TOP:
            self.jump_speed = 0
        if side == BOTTOM:
            self.jump_speed = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.jump_speed = -9.4
            self.is_jumping = True
            self.jump_sound.play() 

    def update(self):
        dy = 0
        dx = 0

        if self.is_jumping == False:
            if self.direction == FORWARD:
                self.image = self.forward_images[0]
            else:
                self.image = self.backward_images[0]
    
        self.frame += 1
        key = pygame.key.get_pressed()

        if key[K_LEFT]:
            self.direction = BACKWARD
            self.image = self.backward_images[self.frame/6 % 5]
            dx = self.direction
        if key[K_RIGHT]:
            self.direction = FORWARD
            self.image = self.forward_images[self.frame/6 % 5]
            dx = self.direction

        jump = key[K_UP]

        if jump:
            self.accel = 0.3
            if self.direction == FORWARD:
                self.image = self.jumping_images[0]
            else:
                self.image = self.jumping_images[1]
            self.jump()

        if self.jump_speed < 8:
            self.jump_speed += self.accel
        if self.jump_speed > 3:
            self.is_jumping = True

        if self.rect.left < 0:
            self.rect.left = 0

        self.move(3*dx, self.jump_speed)

class Ground(Components):
    
    def __init__(self, pos, p_type="ground"):
        Components.__init__(self, self.groups)
        if p_type == "air":
            self.image = load_image("platform-air.png")
        elif p_type == "brick":
            self.image = load_image("platform-brick.png")
        else:
            self.image = load_image("platform.png")
        self.rect = self.image.get_rect(topleft = pos)

class QuestionMark(Components):
    def __init__(self, pos, p_type="ground"):
        Components.__init__(self, self.groups)
        self.images = [load_image("platform-q%d.png" % i) for i in range(0, 3)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 8 == 0:
            self.image = self.images[self.frame/4 % 3]

class Coin(Components):
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.images = [load_image("coin%d.png" % i) for i in range(1, 4)]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame  = 0

    def update(self):
        self.frame += 1
        if self.frame % 8 == 0:
            self.image = self.images[self.frame/4 % 3]

class Bush(Components):

    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.image = load_image("bush.png")
        self.rect = self.image.get_rect(topleft = pos)
        
class Cloud(Components):
     def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.image = load_image("cloud.png")
        self.rect = self.image.get_rect(topleft = pos)

     def update(self):
        self.move(-1, 0)

class Pipe(Components):
    def __init__(self, pos, big = False):
        Components.__init__(self, self.groups)
        if big:
            self.image = load_image("pipe-big.png")
        else:
            self.image = load_image("pipe.png")
        self.rect = self.image.get_rect(topleft = pos)

class VenusFlytrap(Components):
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.images = [load_image("flytrap.png"), load_image("flytrap_open.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.is_open = False
        self.speed = -1
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 15 == 0:
            if self.is_open:
                self.image = self.images[0]
                self.is_open = False
            else:
                self.image = self.images[1]
                self.is_open = True

        if self.rect.centery <= FLYTRAP_TOP:
            self.speed = 1

        if self.rect.centery >= FLYTRAP_BOTTOM:
            self.speed = 0

        flytrap_pop_random = randint(50, 100)

        if self.speed == 0 and self.frame % flytrap_pop_random == 0:
            self.speed = -1
        
        self.move(0, self.speed)
