import pygame
from pygame.locals import *
import os
import random

pygame.init()

WIDTH = 792
HEIGHT = 432
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(os.path.join('', 'assets/background/bg.jpg')).convert()

bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class Scene():

    def __init__(self):
        self.grid = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        self.i_grass = pygame.image.load('assets/terrain/Grass_Tile.png')
        self.WIDTH = 24
        self.HEIGHT = 24
        self.MARGIN = 0
        
    def draw(self):
        for row in range(0, len(self.grid)):
            for column in range(0, len(self.grid[row])):
                if self.grid[row][column] != 0:
                    color = GREEN
                    screen.blit(self.i_grass,
                             [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                              (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                              self.WIDTH,
                              self.HEIGHT])
                
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 16
        height = 32
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2 - 5   #center of rectangle
        self.rect.bottom = HEIGHT // 2 - 5  #pixels up from the bottom
        self.speedx = 0
        self.speedy = 8
        self.isjump = False
        self.isdoublejump = False
        self.direction = 'R'
        self.state = 'I'
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames

        self.s_idle = SpriteStrip('assets/player/Vigilante_Idle_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/player/Vigilante_Walk_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/player/Vigilante_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/player/Vigilante_Jump_Kick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/player/Vigilante_Head_Butt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/player/Vigilante_Get_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/player/Vigilante_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/player/Vigilante_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/player/Vigilante_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/player/Vigilante_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/player/Vigilante_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/player/Vigilante_Knock_out.png').convert_alpha()
        self.i_death = pygame.image.load('assets/player/Vigilante_Down_Death.png').convert_alpha()

    def reset(self):
        self.rect.centerx = WIDTH // 2 - 5   #center of rectangle
        self.rect.bottom = HEIGHT // 2 - 5  #pixels up from the bottom
        self.speedx = 0
        self.speedy = 8
        self.isjump = False
        self.isdoublejump = False
        self.direction = 'R'
        self.state = 'I'
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames

        
    def update_state(self, new):
        if self.state not in ['P', 'K', 'JK', 'CP', 'D']:
            self.state = new

    def handle_controls(self):
        keystate = pygame.key.get_pressed()
        # manage player direction
        if self.state != 'D':
            if keystate[pygame.K_a]:
                self.direction = 'L'
                self.update_state('W')
                self.speedx = 2
            elif keystate[pygame.K_d]:
                self.direction = 'R'
                self.update_state('W')
                self.speedx = 2

        # handle player jumping            
        if self.isjump == False:
            if keystate[pygame.K_w]:
                self.j_frames = 0
                self.isjump = True
        else:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360:
                self.speedy = -8
            else:
                self.speedy += 1
                
        # handle additional key presses
        if keystate[pygame.K_s]:
            self.update_state('C')
        elif keystate[pygame.K_LSHIFT]:
            self.update_state('R')
            self.speedx = self.speedx*2

        # handle mouse clicks / player attacks
        mousestate = pygame.mouse.get_pressed()
        if self.state not in ['P', 'K', 'JK', 'CP', 'D']:
            if self.state == "C":
                if mousestate == (0,0,1) and self.isdoublejump == False:
                    self.update_state('JK')
                    self.a_frames = 0
                    self.isdoublejump = True
                elif mousestate == (1,0,0):
                    self.update_state('CP')
                    self.a_frames = 0
            else:   
                if mousestate == (0,0,1):
                    self.update_state('K')
                    self.a_frames = 0
                elif mousestate == (1,0,0):
                    self.update_state('P')
                    self.a_frames = 0

        
    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        self.speedx = 0 #Need these to make sure
        self.update_state('I')

        self.handle_controls()
                
        if self.state == "P":
            self.speedx = 0
            if self.a_frames == 540:
                self.speedx = 10
            if self.a_frames < 540:
                frame = self.i_punch_1
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.i_punch_2
                self.image = frame
            else:
                self.state = "I"
                
        if self.state == "K":
            self.speedx = 0
            if self.a_frames == 1080:
                self.speedx = 10
            if self.a_frames < 540:
                frame = self.s_idle[0]
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.i_kick_1
                self.image = frame
            elif self.a_frames < 1620:
                frame = self.i_kick_2
                self.image = frame
            else:
                self.state = "I"
                
        if self.state == "CP":
            self.speedx = 0
            if self.a_frames == 1080:
                self.speedx = 5
            if self.a_frames < 540:
                frame = self.i_punch_1
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.i_punch_2
                self.image = frame
            if self.a_frames < 1620:
                frame = self.s_headbutt[0]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_headbutt[1]
                self.image = frame
            else:
                self.state = "C"
                
        if self.state == "JK":
            self.speedx = 0
            self.speedy = 0
            if self.a_frames in [360, 720]:
                self.speedx = 15
                self.speedy = -8
            elif self.a_frames == 1440:
                self.speedx = 15
                self.speedy = 16
            if self.a_frames < 360:
                frame = self.s_aerial[0]
                self.image = frame
            elif self.a_frames < 720:
                frame = self.s_aerial[1]
                self.image = frame
            if self.a_frames < 1440:
                frame = self.s_aerial[2]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_aerial[3]
                self.image = frame
            else:
                self.state = "C"
        
        if self.state == "I":
            frame = (self.a_frames // 360) % len(self.s_idle)
            self.image = self.s_idle[frame]
            self.speedx = 0
        if self.state == "W":
            frame = (pos_x // 10) % len(self.s_walking)
            self.image = self.s_walking[frame]
        if self.state == "R":
            frame = (pos_x // 20) % len(self.s_running)
            self.image = self.s_running[frame]
        if self.state == "C":
            frame = self.i_crouch
            self.image = frame
            self.speedx = 0
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.a_frames += 60
        self.j_frames += 60

        
        try:
            # Set the floor for the current game scene
            if scene.grid[self.rect.bottom // 24][self.rect.right // 24] == 1 or scene.grid[self.rect.bottom // 24][self.rect.left // 24] == 1:
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                self.isjump = False
                self.isdoublejump = False
                self.speedy = 0
            else:
                self.isjump = True

            # set the walls for rhe current game scene
            if scene.grid[self.rect.bottom // 24][self.rect.right // 24] == 2 or scene.grid[self.rect.top // 24][self.rect.right // 24] == 2:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if scene.grid[self.rect.bottom // 24][self.rect.left // 24] == 3 or scene.grid[self.rect.top // 24][self.rect.left // 24] == 3:
                self.rect.left = ((self.rect.left // 24))*24 + 24
        except IndexError:
            # if you fall off the map you die
            self.state = 'D'

        #Set Walls for Width and Height
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.isjump = False
            self.speedy = 0

        
class SpriteStrip(object):
    def __init__(self, file_name):
        # You have to call `convert_alpha`, so that the background of
        # the surface is transparent.
        self.sprite_strip = pygame.image.load(file_name).convert_alpha()

    def get_strip(self, width, height, t_width, t_height):
        strip = []
        n = t_width // width
        for i in range(0,n):
            image = pygame.Surface([width, height], pygame.SRCALPHA)
            image.blit(self.sprite_strip, (0,0), (i*width, 0, width, height))
            strip.append(image)
        return strip
            
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

scene = Scene()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                player.reset()
            #some codes
        
    all_sprites.update()
    screen.blit(bg, (bgX,0))
    all_sprites.draw(screen)
    scene.draw()
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
