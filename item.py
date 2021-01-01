import pygame
from pygame.locals import *
import os
import random

WIDTH = 792
HEIGHT = 432

class Energy_Drink(pygame.sprite.Sprite):

    def __init__(self, scene, player, cpu_player):
        pygame.sprite.Sprite.__init__(self)
        width = 16
        height = 16
        self.scene = scene
        self.player = player
        self.cpu_player = cpu_player
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(32, WIDTH - 32)
        self.rect.bottom = 32
        self.speedx = 0
        self.speedy = 0
        self.inair = True
        self.i_frames = 0 # idle frames

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        if self.i_frames > 36000:
            self.kill()
            return
        
        if self.inair and self.speedy < 5:
            self.speedy += 1

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.i_frames += 60
        
        try:
            # Set the floor for the current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [1, 2, 3, 4, 5, 6, 7, 8] or self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                self.speedy = 0
                self.isinair = False
            else:
                self.isinair = True

            # set the walls for rhe current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18] or self.scene.grid[self.rect.top // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18]:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28] or self.scene.grid[self.rect.top // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28]:
                self.rect.left = ((self.rect.left // 24))*24 + 24
                
        except IndexError:
            # if you fall off the map you die
            self.kill()
            return

        #Set Walls for Width and Height
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def check_player_collision(self, player):
        if pygame.sprite.collide_rect(self, player):
            return True
        else:
            return False
        

class Blue_Energy(Energy_Drink):

    def __init__(self, scene, player, cpu_player):
        super().__init__(scene, player, cpu_player)
        self.image = pygame.transform.scale(pygame.image.load('assets/items/blue_energy.png').convert_alpha(), (16, 16))

    def update(self):
        super().update()
        self.handle_collision(self.player)
        self.handle_collision(self.cpu_player)

    def handle_collision(self, player):
        if super().check_player_collision(player):
            player.blue_empowered = True
            player.e_frames = 0
            self.kill()

class Red_Energy(Energy_Drink):

    def __init__(self, scene, player, cpu_player):
        super().__init__(scene, player, cpu_player)
        self.image = pygame.transform.scale(pygame.image.load('assets/items/red_energy.png').convert_alpha(), (16, 16))

    def update(self):
        super().update()
        self.handle_collision(self.player)
        self.handle_collision(self.cpu_player)

    def handle_collision(self, player):
        if super().check_player_collision(player):
            player.damage = 0
            self.kill()

class Yellow_Energy(Energy_Drink):

    def __init__(self, scene, player, cpu_player):
        super().__init__(scene, player, cpu_player)
        self.image = pygame.transform.scale(pygame.image.load('assets/items/yellow_energy.png').convert_alpha(), (16, 16))

    def update(self):
        super().update()
        self.handle_collision(self.player)
        self.handle_collision(self.cpu_player)

    def handle_collision(self, player):
        if super().check_player_collision(player):
            player.yellow_empowered = True
            player.e_frames = 0
            self.kill()
