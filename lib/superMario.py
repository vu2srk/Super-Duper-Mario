import sys, os
import random

import pygame
from pygame.locals import *
from helpers import *
from components import *
from world import *

def RelRect(actor, camera):
    return Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, 480)
        self.rect.center = self.player.rect.center

    def update(self):
        if self.player.rect.centerx > self.rect.centerx+64:
            self.rect.centerx = self.player.rect.centerx-64
        if self.player.rect.centerx < self.rect.centerx-64:
            self.rect.centerx = self.player.rect.centerx+64
        if self.player.rect.centery > self.rect.centery+64:
            self.rect.centery = self.player.rect.centery-64
        if self.player.rect.centery < self.rect.centery-64:
            self.rect.centery = self.player.rect.centery+64
        self.rect.clamp_ip(self.world)
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))


class SuperMario:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.quit = 0

        self.initGroups()

        Mario.groups = self.sprites, self.player_group
        Ground.groups = self.sprites, self.ground_group

        self.player = Mario((0,0))
        self.world = World()
        self.camera = Camera(self.player, self.world.get_size()[0])
        self.scene_bg = load_image("background.png")
        self.start()

    def initGroups(self):
        self.sprites = pygame.sprite.OrderedUpdates()
        self.player_group = pygame.sprite.OrderedUpdates()
        self.ground_group = pygame.sprite.OrderedUpdates()
    
    def start(self):
        while not self.quit:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.quit = 1

            self.screen.blit(self.scene_bg, ((-self.camera.rect.x/1)%640, 0))
            self.screen.blit(self.scene_bg, ((-self.camera.rect.x/1)%640 + 640, 0))
            self.screen.blit(self.scene_bg, ((-self.camera.rect.x/1)%640 - 640, 0))
            self.camera.draw_sprites(self.screen, self.sprites)

            pygame.display.flip()
            self.clock.tick(20)


