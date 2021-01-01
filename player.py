import pygame
from pygame.locals import *
import os
import random

WIDTH = 792
HEIGHT = 432

class CPU_Player(pygame.sprite.Sprite):

    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene 
        width = 16
        height = 32
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = scene.CPU_respawn_point[0]   #center of rectangle
        self.rect.bottom = scene.CPU_respawn_point[1]   #pixels up from the bottom
        self.speedx = 0
        self.speedy = 8
        self.damage = 0.0
        self.lives = 3
        self.isjump = True
        self.isdoublejump = True
        self.direction = 'L'
        self.state = 'I'
        self.i_frames = 0 # idle frames
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames
        self.e_frames = 0 # empowered frames
        self.blue_empowered = False
        self.yellow_empowered = False

    def reset(self):
        self.rect.centerx = self.scene.CPU_respawn_point[0]
        self.rect.bottom = self.scene.CPU_respawn_point[1]
        self.speedx = 0
        self.speedy = 8
        self.damage = 0.0
        self.isjump = True
        self.isdoublejump = True
        self.direction = 'L'
        self.state = 'I'
        self.i_frames = 0 # idle frames
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames
        self.e_frames = 0 # empowered frames
        self.blue_empowered = False
        self.yellow_empowered = False

    def update_state(self, new):
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']:
            self.state = new
            self.a_frames = 0

    def make_jump(self):
        self.isjump = True
        self.j_frames = 0
        
    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

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

        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
            
        if self.state == "I":
            frame = (self.i_frames // 360) % len(self.s_idle)
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
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        self.handle_scene()

    def handle_scene(self):
        try:
            # Set the floor for the current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [1, 2, 3, 4, 5, 6, 7, 8] or self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                self.isjump = False
                self.isdoublejump = False
                self.speedy = 0
            else:
                self.isjump = True

            # set the walls for rhe current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18] or self.scene.grid[self.rect.top // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18]:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28] or self.scene.grid[self.rect.top // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28]:
                self.rect.left = ((self.rect.left // 24))*24 + 24
        except IndexError:
            # if you fall off the map you die
            if self.state != 'D':
                self.state = 'D'
                self.lives = self.lives - 1
                self.a_frames = 0

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

class Ranger_CPU(CPU_Player):
    
    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 60
        self.name = "Ranger"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/ranger/NES_Ranger_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/ranger/NES_Ranger_Idle_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/ranger/NES_Ranger_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/ranger/NES_Ranger_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/ranger/NES_Ranger_JumpKick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/ranger/NES_Ranger_HeadButt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/ranger/NES_Ranger_Get_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/ranger/NES_Ranger_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/ranger/NES_Ranger_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/ranger/NES_Ranger_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/ranger/NES_Ranger_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/ranger/NES_Ranger_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/ranger/NES_Ranger_Knockdown.png').convert_alpha()
        self.i_death = pygame.image.load('assets/ranger/NES_Ranger_Own_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def make_action(self, player):
        action_space = ['K', 'CP', 'P', 'JK']
        direction_space = ['L', 'R']

        if player.state != "D":
            if player.rect.x < self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'L'
            elif player.rect.x > self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'R'
                
            if abs(player.rect.y - self.rect.y) < 24:   
                if abs(player.rect.x - self.rect.x) < 10:
                    self.update_state(random.choice(action_space))
                elif player.rect.x < 600 and player.rect.x > 168:
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
            elif player.rect.x < 600 and player.rect.x > 168 and abs(player.rect.x - self.rect.x) > 10:
                self.update_state('W')
            else:
                self.update_state('I')
            
        if (abs(self.rect.x - 432) < 10 and self.direction == 'L') or (abs(self.rect.x - 360) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
            self.update_state('R')
            self.make_jump()

        if self.state == "R":
            self.speedx = 4
        if self.state == "W":
            self.speedx = 2
        if self.isjump == True:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360:
                self.speedy = (-600 // self.mass)
                if self.yellow_empowered:
                    self.speedy = int(self.speedy * 1.5)
            else:
                self.speedy += 1

    def make_jump(self):
        super().make_jump()

    def update(self):
        super().update()

class Soldier_CPU(CPU_Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 75
        self.name = "Soldier"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/soldier/SMS_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/soldier/SMS_Soldier_Idle_2_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/soldier/SMS_Soldier_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/soldier/SMS_Soldier_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/soldier/SMS_Soldier_Jump_Kick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/soldier/SMS_Soldier_Combo_strip6.png').get_strip(24, 32, 144, 32)
        self.i_crouch = pygame.image.load('assets/soldier/SMS_Soldier_Pick_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/soldier/SMS_Soldier_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/soldier/SMS_Soldier_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/soldier/SMS_Soldier_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/soldier/SMS_Soldier_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/soldier/SMS_Soldier_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/soldier/SMS_Soldier_Knock_Down.png').convert_alpha()
        self.i_death = pygame.image.load('assets/soldier/SMS_Soldier_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def make_action(self, player):
        action_space = ['K', 'P', 'CP']
        direction_space = ['L', 'R']

        if player.state != "D":
            if player.rect.x < self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'L'
            elif player.rect.x > self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'R'
               
            if abs(player.rect.y - self.rect.y) < 24:   
                if abs(player.rect.x - self.rect.x) < 10:
                    self.update_state(random.choice(action_space))
                elif player.rect.x < 696 and player.rect.x > 96:
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
            elif player.rect.x < 696 and player.rect.x > 96 and abs(player.rect.x - self.rect.x) > 10:
                self.update_state('W')
            else:
                self.update_state('I')
                    
            if (abs(self.rect.x - 240) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
                self.update_state('R')
                self.make_jump()
            elif (abs(self.rect.x - 624) < 10 and self.direction == 'R') or (abs(self.rect.x - 504) < 10 and self.direction == 'L') and (self.rect.y) > 288 and self.state in ['W', 'R']:
                self.update_state('R')
                self.make_jump()

        if self.state == "R":
            self.speedx = 4
        if self.state == "W":
            self.speedx = 2
        if self.isjump == True:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360:
                self.speedy = (-600 // self.mass)
                if self.yellow_empowered:
                    self.speedy = int(self.speedy * 1.5)
            else:
                self.speedy += 1
                if self.speedy == 0:
                    self.update_state('JK')

    def make_jump(self):
        super().make_jump()

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

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
            if self.a_frames in [540, 1080, 1620, 2160, 2700, 3240]:
                self.speedx = 3
            if self.a_frames < 540:
                frame = self.s_headbutt[0]
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.s_headbutt[1]
                self.image = frame
            elif self.a_frames < 1620:
                frame = self.s_headbutt[2]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_headbutt[3]
                self.image = frame
            elif self.a_frames < 2700:
                frame = self.s_headbutt[4]
                self.image = frame
            elif self.a_frames < 3240:
                frame = self.s_headbutt[5]
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

        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
            
        if self.state == "I":
            frame = (self.i_frames // 360) % len(self.s_idle)
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
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        super().handle_scene()
    

class Renegade_CPU(CPU_Player):
    
    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 90
        self.name = "Renegade"
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/renegade/Renegade_TitleScreen.png')).convert()

        self.s_idle = SpriteStrip('assets/renegade/Renegade_Idle_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/renegade/Renegade_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/renegade/Renegade_Run_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = None
        self.s_headbutt = SpriteStrip('assets/renegade/Renegade_Head_Butt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/renegade/Renegade_Get_up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/renegade/Renegade_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/renegade/Renegade_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/renegade/Renegade_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/renegade/Renegade_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/renegade/Renegade_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/renegade/Renegade_Knock_Out.png').convert_alpha()
        self.i_death = pygame.image.load('assets/renegade/Renegade_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def make_action(self, player):
        action_space = ['K', 'CP', 'P']
        direction_space = ['L', 'R']

        if player.state != "D":
            if player.rect.x < self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'L'
            elif player.rect.x > self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'R'
                    
            if abs(player.rect.y - self.rect.y) < 24:
                
                if abs(player.rect.x - self.rect.x) < 10:
                    self.update_state(random.choice(action_space))
                elif player.rect.x < 576 and player.rect.x > 240:
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
                        
            elif player.rect.x < 576 and player.rect.x > 240 and abs(player.rect.x - self.rect.x) > 10:
                self.update_state('W')
            else:
                self.update_state('I')
        
        if self.state == "R":
            self.speedx = 4
        if self.state == "W":
            self.speedx = 2
        if self.isjump == True:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360:
                self.speedy = (-600 // self.mass)
                if self.yellow_empowered:
                    self.speedy = int(self.speedy * 1.5)
            else:
                self.speedy += 1

    def make_jump(self):
        super().make_jump()

    def update(self):
        super().update()

class Agent_CPU(CPU_Player):
    
    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 55
        self.name = "Agent"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/agent/SMS_Agent_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/agent/SMS_Adv_Idle_Gun_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/agent/SMS_Adv_Idle_strip4.png').get_strip(24, 32, 96, 32)
        self.s_running = SpriteStrip('assets/agent/SMS_Adv_Idle_strip4.png').get_strip(24, 32, 96, 32)
        self.s_aerial = SpriteStrip('assets/agent/SMS_Adv_Jump_1_strip6.png').get_strip(32, 32, 192, 32)
        self.s_headbutt = None
        self.i_crouch = None
        self.i_punch_1 = pygame.image.load('assets/agent/SMS_Adv_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/agent/SMS_Adv_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/agent/SMS_Adv_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/agent/SMS_Adv_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/agent/SMS_Adv_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/agent/SMS_Adv_Knockback.png').convert_alpha()
        self.i_death = pygame.image.load('assets/agent/SMS_Adv_Down.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def make_action(self, player):
        action_space = ['K', 'P', 'JK']
        direction_space = ['L', 'R']

        if player.state != "D":
            if player.rect.x < self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'L'
            elif player.rect.x > self.rect.x:
                if self.state not in ['D', 'H', 'KO']:
                    self.direction = 'R'
                
            if abs(player.rect.y - self.rect.y) < 24:   
                if abs(player.rect.x - self.rect.x) < 10:
                    self.update_state(random.choice(action_space))
                elif player.rect.x < 720 and player.rect.x > 72:
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
            elif player.rect.x < 720 and player.rect.x > 72 and abs(player.rect.x - self.rect.x) > 10:
                self.update_state('W')
            else:
                self.update_state('I')
            
        if (abs(self.rect.x - 264) < 10 and self.direction == 'L') or (abs(self.rect.x - 168) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
            self.update_state('R')
            self.make_jump()
        elif (abs(self.rect.x - 576) < 10 and self.direction == 'L') or (abs(self.rect.x - 504) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
            self.update_state('R')
            self.make_jump()

        if self.state == "R":
            self.speedx = 4
        if self.state == "W":
            self.speedx = 2
        if self.isjump == True:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360:
                self.speedy = (-600 // self.mass)
                if self.yellow_empowered:
                    self.speedy = int(self.speedy * 1.5)
            else:
                self.speedy += 1
                if self.speedy == 0:
                    self.update_state('JK')

    def make_jump(self):
        super().make_jump()

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

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
                
        if self.state == "JK":
            self.speedx = 0
            self.speedy = 0
            if self.a_frames in [360, 720]:
                self.speedx = 15
                self.speedy = -8
            elif self.a_frames == 1440:
                self.speedx = 15
            if self.a_frames < 360:
                frame = self.s_aerial[0]
                self.image = frame
            elif self.a_frames < 720:
                frame = self.s_aerial[1]
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.s_aerial[2]
                self.image = frame
            elif self.a_frames < 1440:
                frame = self.s_aerial[3]
                self.image = frame
            elif self.a_frames < 1800:
                frame = self.s_aerial[4]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_aerial[5]
                self.image = frame
            else:
                self.state = "C"

        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
            
        if self.state == "I" or self.state == "C":
            frame = (self.i_frames // 360) % len(self.s_idle)
            self.image = self.s_idle[frame]
            self.speedx = 0
        if self.state == "W":
            frame = (pos_x // 10) % len(self.s_walking)
            self.image = self.s_walking[frame]
        if self.state == "R":
            frame = (pos_x // 20) % len(self.s_running)
            self.image = self.s_running[frame]
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        super().handle_scene()
    
class Player(pygame.sprite.Sprite):

    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene 
        width = 16
        height = 32
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = scene.player_respawn_point[0]   #center of rectangle
        self.rect.bottom = scene.player_respawn_point[1]  #pixels up from the bottom
        self.speedx = 0
        self.speedy = 8
        self.damage = 0.0
        self.lives = 3
        self.isjump = True
        self.isdoublejump = True
        self.direction = 'R'
        self.state = 'I'
        self.i_frames = 0 # idle frames
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames
        self.e_frames = 0 # empowered frames
        self.blue_empowered = False
        self.yellow_empowered = False


    def reset(self):
        self.rect.centerx = self.scene.player_respawn_point[0]   #center of rectangle
        self.rect.bottom = self.scene.player_respawn_point[1]  #pixels up from the bottom
        self.speedx = 0
        self.speedy = 8
        self.damage = 0.0
        self.isjump = True
        self.isdoublejump = True
        self.direction = 'R'
        self.state = 'I'
        self.a_frames = 0 # animation frames
        self.j_frames = 0 # jumping frames
        self.i_frames = 0 # idle frames
        self.e_frames = 0 # eempowered frames
        self.blue_empowered = False
        self.yellow_empowered = False

    def update_state(self, new):
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']:
            self.state = new
            self.a_frames = 0
            
    def handle_controls(self):
        keystate = pygame.key.get_pressed()
        # manage player direction
        if self.state not in ['D', 'H', 'KO']:
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
                self.speedy = (-600 // self.mass)
                if self.yellow_empowered:
                    self.speedy = int(self.speedy * 1.5)
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
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']:
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
            elif self.a_frames < 1620:
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
            elif self.a_frames < 1440:
                frame = self.s_aerial[2]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_aerial[3]
                self.image = frame
            else:
                self.state = "C"
                
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
        
        if self.state == "I":
            frame = (self.i_frames // 360) % len(self.s_idle)
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
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60
        
        self.handle_scene()


    def handle_scene(self):
        try:
            # Set the floor for the current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [1, 2, 3, 4, 5, 6, 7, 8] or self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                self.isjump = False
                self.isdoublejump = False
                self.speedy = 0
            else:
                self.isjump = True

            # set the walls for rhe current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18] or self.scene.grid[self.rect.top // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18]:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28] or self.scene.grid[self.rect.top // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28]:
                self.rect.left = ((self.rect.left // 24))*24 + 24
        except IndexError:
            # if you fall off the map you die
            if self.state != 'D':
                self.state = 'D'
                self.lives = self.lives - 1
                self.a_frames = 0

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

class Ranger_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 60
        self.name = "Ranger"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/ranger/NES_Ranger_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/ranger/NES_Ranger_Idle_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/ranger/NES_Ranger_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/ranger/NES_Ranger_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/ranger/NES_Ranger_JumpKick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/ranger/NES_Ranger_HeadButt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/ranger/NES_Ranger_Get_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/ranger/NES_Ranger_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/ranger/NES_Ranger_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/ranger/NES_Ranger_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/ranger/NES_Ranger_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/ranger/NES_Ranger_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/ranger/NES_Ranger_Knockdown.png').convert_alpha()
        self.i_death = pygame.image.load('assets/ranger/NES_Ranger_Own_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def handle_controls(self):
        super().handle_controls()

    def update(self):
        super().update()

    
class Vigilante_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 60
        self.name = "Vigilante"
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/vigilante/Vigilante_TitleScreen.png')).convert()

        self.s_idle = SpriteStrip('assets/vigilante/Vigilante_Idle_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/vigilante/Vigilante_Walk_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/vigilante/Vigilante_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/vigilante/Vigilante_Jump_Kick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/vigilante/Vigilante_Head_Butt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/vigilante/Vigilante_Get_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/vigilante/Vigilante_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/vigilante/Vigilante_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/vigilante/Vigilante_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/vigilante/Vigilante_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/vigilante/Vigilante_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/vigilante/Vigilante_Knock_out.png').convert_alpha()
        self.i_death = pygame.image.load('assets/vigilante/Vigilante_Down_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def handle_controls(self):
        super().handle_controls()

    def update(self):
        super().update()


class Soldier_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 75
        self.name = "Soldier"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/soldier/SMS_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/soldier/SMS_Soldier_Idle_2_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/soldier/SMS_Soldier_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/soldier/SMS_Soldier_Run_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = SpriteStrip('assets/soldier/SMS_Soldier_Jump_Kick_strip4.png').get_strip(24, 32, 96, 32)
        self.s_headbutt = SpriteStrip('assets/soldier/SMS_Soldier_Combo_strip6.png').get_strip(24, 32, 144, 32)
        self.i_crouch = pygame.image.load('assets/soldier/SMS_Soldier_Pick_Up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/soldier/SMS_Soldier_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/soldier/SMS_Soldier_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/soldier/SMS_Soldier_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/soldier/SMS_Soldier_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/soldier/SMS_Soldier_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/soldier/SMS_Soldier_Knock_Down.png').convert_alpha()
        self.i_death = pygame.image.load('assets/soldier/SMS_Soldier_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def handle_controls(self):
        super().handle_controls()

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
            if self.a_frames in [540, 1080, 1620, 2160, 2700, 3240]:
                self.speedx = 3
            if self.a_frames < 540:
                frame = self.s_headbutt[0]
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.s_headbutt[1]
                self.image = frame
            elif self.a_frames < 1620:
                frame = self.s_headbutt[2]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_headbutt[3]
                self.image = frame
            elif self.a_frames < 2700:
                frame = self.s_headbutt[4]
                self.image = frame
            elif self.a_frames < 3240:
                frame = self.s_headbutt[5]
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
            elif self.a_frames < 1440:
                frame = self.s_aerial[2]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_aerial[3]
                self.image = frame
            else:
                self.state = "C"
                
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
        
        if self.state == "I":
            frame = (self.i_frames // 360) % len(self.s_idle)
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
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
             
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        super().handle_scene()

class Renegade_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 90
        self.name = "Renegade"
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/renegade/Renegade_TitleScreen.png')).convert()

        self.s_idle = SpriteStrip('assets/renegade/Renegade_Idle_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/renegade/Renegade_Walk_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_running = SpriteStrip('assets/renegade/Renegade_Run_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_aerial = None
        self.s_headbutt = SpriteStrip('assets/renegade/Renegade_Head_Butt_strip2.png').get_strip(24, 32, 48, 32)
        self.i_crouch = pygame.image.load('assets/renegade/Renegade_Get_up.png').convert_alpha()
        self.i_punch_1 = pygame.image.load('assets/renegade/Renegade_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/renegade/Renegade_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/renegade/Renegade_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/renegade/Renegade_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/renegade/Renegade_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/renegade/Renegade_Knock_Out.png').convert_alpha()
        self.i_death = pygame.image.load('assets/renegade/Renegade_Death.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def handle_controls(self):
        super().handle_controls()
        if self.state == 'JK':
            self.state = 'K'
            self.a_frames = 0
            self.isdoublejump = False

    def update(self):
        super().update()

class Agent_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 55
        self.name = "Agent"
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/agent/SMS_Agent_TitleScreen.png')).convert(), (88, 136))

        self.s_idle = SpriteStrip('assets/agent/SMS_Adv_Idle_Gun_1_strip4.png').get_strip(16, 32, 64, 32)
        self.s_walking = SpriteStrip('assets/agent/SMS_Adv_Idle_strip4.png').get_strip(24, 32, 96, 32)
        self.s_running = SpriteStrip('assets/agent/SMS_Adv_Idle_strip4.png').get_strip(24, 32, 96, 32)
        self.s_aerial = SpriteStrip('assets/agent/SMS_Adv_Jump_1_strip6.png').get_strip(32, 32, 192, 32)
        self.s_headbutt = None
        self.i_crouch = None
        self.i_punch_1 = pygame.image.load('assets/agent/SMS_Adv_Punch_1.png').convert_alpha()
        self.i_punch_2 = pygame.image.load('assets/agent/SMS_Adv_Punch_2.png').convert_alpha()
        self.i_kick_1 = pygame.image.load('assets/agent/SMS_Adv_Kick_1.png').convert_alpha()
        self.i_kick_2 = pygame.image.load('assets/agent/SMS_Adv_Kick_2.png').convert_alpha()
        self.i_hurt = pygame.image.load('assets/agent/SMS_Adv_Hurt.png').convert_alpha()
        self.i_knockout = pygame.image.load('assets/agent/SMS_Adv_Knockback.png').convert_alpha()
        self.i_death = pygame.image.load('assets/agent/SMS_Adv_Down.png').convert_alpha()

    def reset(self):
        super().reset()

    def update_state(self, new):
        super().update_state(new)

    def handle_controls(self):
        super().handle_controls()
        if self.state == 'CP':
            self.state = 'P'
            self.a_frames = 0
            self.isdoublejump = False

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
                
        if self.state == "JK":
            self.speedx = 0
            self.speedy = 0
            if self.a_frames in [360, 720]:
                self.speedx = 15
                self.speedy = -8
            elif self.a_frames == 1440:
                self.speedx = 15
            if self.a_frames < 360:
                frame = self.s_aerial[0]
                self.image = frame
            elif self.a_frames < 720:
                frame = self.s_aerial[1]
                self.image = frame
            elif self.a_frames < 1080:
                frame = self.s_aerial[2]
                self.image = frame
            elif self.a_frames < 1440:
                frame = self.s_aerial[3]
                self.image = frame
            elif self.a_frames < 1800:
                frame = self.s_aerial[4]
                self.image = frame
            elif self.a_frames < 2160:
                frame = self.s_aerial[5]
                self.image = frame
            else:
                self.state = "C"
                
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
        
        if self.state == "I" or self.state == "C":
            frame = (self.i_frames // 360) % len(self.s_idle)
            self.image = self.s_idle[frame]
            self.speedx = 0
        if self.state == "W":
            frame = (pos_x // 10) % len(self.s_walking)
            self.image = self.s_walking[frame]
        if self.state == "R":
            frame = (pos_x // 20) % len(self.s_running)
            self.image = self.s_running[frame]
        if self.state == "H":
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000:
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            self.yellow_empowered = False

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        super().handle_scene()
    

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
