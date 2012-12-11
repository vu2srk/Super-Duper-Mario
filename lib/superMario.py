import sys, os
import random

import pygame
from pygame.locals import *
from helpers import *
from components import *
from world import *

WIDTH = 640
HEIGHT = 480
LOOK_AHEAD = 64
VITALS_COLOR = (255, 255, 255)
MARGIN = 20

def RelRect(actor, camera):
    return Rect(actor.rect.x-camera.rect.x, actor.rect.y-camera.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = Rect(0, 0, width, HEIGHT)

    def update(self):

        #advance the camera to show more of the world
            
        player_x, player_y = self.player.rect.center
        world_x, world_y = self.rect.center

        add_world = 0

        if player_x > world_x + LOOK_AHEAD:
            add_world = LOOK_AHEAD
        if player_x < world_x - LOOK_AHEAD:
            add_world = -LOOK_AHEAD
        self.rect.centerx = player_x + LOOK_AHEAD

        add_world = 0

        if player_y > world_y + LOOK_AHEAD:
            add_world = LOOK_AHEAD
        if player_y < world_y - LOOK_AHEAD:
            add_world = -LOOK_AHEAD
        self.rect.centery = player_y + LOOK_AHEAD

        self.rect.clamp_ip(self.world)

    def draw_sprites(self, screen, sprites):
        for sprite in sprites:
            #check if the sprite falls within the world
            if sprite.rect.colliderect(self.rect):
                screen.blit(sprite.image, RelRect(sprite, self))

class SuperMario:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.quit = 0

        self.initGroups()

        Mario.groups = self.sprites, self.player_group
        Ground.groups = self.sprites, self.ground_group
        Bush.groups = self.sprites
        Cloud.groups = self.sprites, self.cloud_group
        Pipe.groups = self.sprites, self.ground_group
        QuestionMark.groups = self.sprites, self.ground_group
        Coin.groups = self.sprites, self.coin_group
        VenusFlytrap.groups = self.sprites, self.flytrap_group
        GrassHill.groups = self.sprites
        LifeMushroom.groups = self.sprites, self.mushroom_group
        Castle.groups = self.sprites
        Flagpole.groups = self.sprites, self.flag_group

        self.world = World()
        self.player = Mario((0,0))
        self.camera = Camera(self.player, self.world.get_size()[0])
        self.font = pygame.font.Font(filepath("fonts/font.ttf"), 16)
        self.music = "maintheme.ogg"

        self.scene_bg = load_image("background.png")
        self.lives_images = [load_image("mario1.png"), load_image("last-life.png")]

        play_music(self.music)
        self.start()

    def initGroups(self):
        #initialize all groups to OrderedUpdates -- to ensure sprites get loaded in the order of adding
        self.sprites = pygame.sprite.OrderedUpdates()
        self.player_group = pygame.sprite.OrderedUpdates()
        self.ground_group = pygame.sprite.OrderedUpdates()
        self.cloud_group = pygame.sprite.OrderedUpdates()
        self.coin_group = pygame.sprite.OrderedUpdates()
        self.flytrap_group = pygame.sprite.OrderedUpdates()
        self.mushroom_group = pygame.sprite.OrderedUpdates()
        self.flag_group = pygame.sprite.OrderedUpdates()
    
    def start(self):
        while not self.quit:
            
            self.camera.update()
            
            for sprite in self.sprites:
                sprite.update()
            
            #tell the component that it collides with everything in ground_group
            self.player.collidesWith(self.ground_group)
            self.player.collidesWith(self.coin_group)
            self.player.collidesWith(self.flytrap_group)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.quit = 1

            camera_x = self.camera.rect.x

            #draw background for each frame       
    
            self.screen.blit(self.scene_bg, (self.modWidth(camera_x), 0))
            self.screen.blit(self.scene_bg, (self.modWidth(camera_x) + WIDTH, 0))
            self.screen.blit(self.scene_bg, (self.modWidth(camera_x) - WIDTH, 0))
            self.camera.draw_sprites(self.screen, self.sprites)
            self.draw_vitals()

            pygame.display.flip()
            self.clock.tick(60)

    def modWidth(self, camera_x):
        return -camera_x % WIDTH

    def draw_vitals(self):
        if self.player.lives == 0:
            lives_image = self.lives_images[1]
        else:
            lives_image = self.lives_images[0]
        self.screen.blit(lives_image, (5, 10))
        ren = self.font.render("x%d" % self.player.lives, 1, VITALS_COLOR)
        self.screen.blit(ren, (lives_image.get_width() + MARGIN, MARGIN))

        ren = self.font.render("Coins: %03d" % self.player.coins, 1, VITALS_COLOR)
        self.screen.blit(ren, (WIDTH - (ren.get_width() + MARGIN), MARGIN))
