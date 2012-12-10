import pygame, random, math
from pygame.locals import *

from helpers import *

TOP_SIDE    = 0
BOTTOM_SIDE = 2
LEFT_SIDE   = 3
RIGHT_SIDE  = 1

def speed_to_side(dx,dy):
    if abs(dx) > abs(dy):
        dy = 0
    else:
        dx = 0
    if dy < 0:
        return TOP_SIDE
    elif dx > 0:
        return RIGHT_SIDE
    elif dy > 0:
        return BOTTOM_SIDE
    elif dx < 0:
        return LEFT_SIDE
    else:
        return 0, 0

class Components(pygame.sprite.Sprite):

    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.collision_groups = []
        self.xoffset = 0
        self.yoffset = 0

    def collidesWith(self, group):
        if group not in self.collision_groups:
            self.collision_groups.append(group)

    def move(self, dx, dy, collide=True):
        if collide:
            if dx!=0:
                dx, dummy = self.__move(dx,0)
            if dy!=0:
                dummy, dy = self.__move(0,dy)
        else:
            self.rect.move_ip(dx, dy)
        return dx, dy

    def clamp_off(self, sprite, side):
        if side == TOP_SIDE:
            self.rect.top = sprite.rect.bottom
        if side == RIGHT_SIDE:
            self.rect.right = sprite.rect.left
        if side == BOTTOM_SIDE:
            self.rect.bottom = sprite.rect.top
        if side == LEFT_SIDE:
            self.rect.left = sprite.rect.right

    def __move(self,dx,dy):
        oldr = self.rect
        self.rect.move_ip(dx, dy)        

        side = speed_to_side(dx, dy)
        
        for group in self.collision_groups:
            for sprite in group:
                if sprite.rect.colliderect(self.rect):
                    self.on_collision(side, sprite, group)

        return self.rect.left-oldr.left,self.rect.top-oldr.top

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)

    def draw(self, surf):
        surf.blit(self.image, (self.rect[0]+self.xoffset, self.rect[1]+self.yoffset))

class Mario(Components):
    
    def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.forward_images = [load_image("mario1.png"), load_image("mario2.png"), load_image("mario3.png"), load_image("mario4.png"), load_image("mario1.png"), load_image("mario5.png")]
        self.backward_images = [pygame.transform.flip(image, 1, 0) for image in self.forward_images]
        self.image = self.forward_images[0]
        self.rect = self.image.get_rect(topleft = pos)

        self.jump_speed = 0
        self.jump_accel = 0.3
        self.jumping = False
        self.frame = 0
        self.facing = 1
        self.angle = 0
        self.dying = False
        self.shooting = False
        self.shoot_timer = 0
        self.still_timer = 0
        self.hp = 1
        self.hit_timer = 0
        self.springing = False

        self.jump_sound = load_sound("jump.ogg")

    def on_collision(self, side, sprite, group):
        self.clamp_off(sprite, side)
        if side == TOP_SIDE:
            self.jump_speed = 0
        if side == BOTTOM_SIDE:
            self.jump_speed = 0
            self.jumping = False
            self.springing = False

    def jump(self):
        if not self.jumping and not self.shooting and self.still_timer <= 0:
            self.jump_speed = -9.4
            self.jumping = True
            self.move(0, -4)
            self.jump_sound.play() 

    def update(self):
        self.frame += 1 
        self.still_timer -= 1
        self.hit_timer -= 1
        dx = 0
        key = pygame.key.get_pressed()

        if key[K_z]:
            if not self.springing:
                self.jump_accel = 0.3
            else:
                self.jump_accel = 0.6
            self.jump()

        if self.jump_speed < 8:
            self.jump_speed += self.jump_accel
        if self.jump_speed > 3:
            self.jumping = True

        if self.shooting:
            self.shoot_timer -= 1
            id = self.shoot_timer/5
            if self.shoot_timer % 5 == 0 and id != 0:
                self.string = Stringer(self.rect.center, self.facing, id, self)
            if self.shoot_timer <= 0:
                self.shooting = False
        else:
            if self.still_timer <= 0:
                if key[K_LEFT]:
                    dx = -1
                    self.facing = dx
                if key[K_RIGHT]:
                    dx = 1
                    self.facing = dx

        if self.facing > 0:
            self.image = self.forward_images[0]
        if self.facing < 0:
            self.image = self.backward_images[0]
        if dx > 0:
            self.image = self.forward_images[self.frame/6%5]
        if dx < 0:
            self.image = self.backward_images[self.frame/6%5]
        if self.facing > 0 and self.jumping:
            self.image = self.forward_images[5]
        if self.facing < 0 and self.jumping:
            self.image = self.backward_images[5]
        if self.hit_timer > 0:
            if not self.frame % 2:
                if self.facing > 0:
                    self.image = self.forward_images[2]
                if self.facing < 0:
                    self.image = self.backward_images[2]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top >= 475:
            pygame.sprite.Sprite.kill(self)

        self.move(3*dx, self.jump_speed)

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
        
class Cloud(Components):
     def __init__(self, pos):
        Components.__init__(self, self.groups)
        self.image = load_image("cloud.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.oldy = self.rect.centerx
        self.speed = -00.1
     def on_collision(self, side, sprite, group):
         if side == TOP_SIDE:
             sprite.rect.right = self.rect.left
             sprite.jump_speed = 1
         if side == BOTTOM_SIDE:
             sprite.rect.right = self.rect.left
     def update(self):
        if self.rect.centerx & self.oldy+64:
            self.speed = -self.speed
        if self.rect.centerx & self.oldy-64:
            self.speed = -self.speed
        self.move(-1, self.speed)

