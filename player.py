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
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']: # can't change state during an animation
            self.state = new
            self.a_frames = 0 # reset animation frames

    def make_jump(self):
        pygame.mixer.Sound("./assets/sounds/jump.wav").play() # play jump sound
        self.isjump = True # set isjump to True
        self.j_frames = 0 # reset jumping frames
        
    def update(self): # on all_sprites.update
        # get sprite x y position
        pos_x = self.rect.x
        pos_y = self.rect.y

        # if punching follow the punching animation
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

        # if kicking follow the kicking animation
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

        # combo punch animation
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

        # jump kick animation
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

        # hurt animation
        if self.state == "H":
            if self.a_frames < 2160:
                # knockback speed is proportional to damage taken
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True # can't jump out of it
            else:
                self.state = "I"

        # knock out animation
        if self.state == "KO":
            if self.a_frames < 2160:
                # knockback speed is proportional to damage taken and doubled
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True # can't jump out of it
            else:
                self.state = "I"

        # handle other player states
        if self.state == "I":
            # follow idle animation
            frame = (self.i_frames // 360) % len(self.s_idle) 
            self.image = self.s_idle[frame]
            self.speedx = 0
        if self.state == "W":
            # follow walking animation
            frame = (pos_x // 10) % len(self.s_walking)
            self.image = self.s_walking[frame]
        if self.state == "R":
            # follow running animation
            frame = (pos_x // 20) % len(self.s_running)
            self.image = self.s_running[frame]
        if self.state == "C":
            # use crouch frame
            frame = self.i_crouch
            self.image = frame
            self.speedx = 0
        if self.state == "H":
            # use hurt frame
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            # use knockout frame
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            # use death frame
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000:
                self.reset()
            
        if self.direction == "L": # if facing left then flip thee image
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1) # reverse speedx

        if self.blue_empowered and self.e_frames < 18000: # if blue empowered tint the image blue
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            # afetr 5 seconds remove power
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000: # if yellow empowered tinit yellow
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else:
            # after 5 seconds remove power
            self.yellow_empowered = False

        # update position according to speedx and speedy
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # increment the animation frames, jumping frames, idle frames and empowered frames
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        # handle scene walls and floor
        self.handle_scene()

    def handle_scene(self):
        try:
            # Set the floor for the current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [1, 2, 3, 4, 5, 6, 7, 8] or self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [1, 2, 3, 4, 5, 6, 7, 8]:
                # if touching the floor
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                # can jump and double jump
                self.isjump = False
                self.isdoublejump = False
                self.speedy = 0 # set speed to 0
            else:
                # in the air so can't jump
                self.isjump = True

            # set the walls for rhe current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18] or self.scene.grid[self.rect.top // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18]:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28] or self.scene.grid[self.rect.top // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28]:
                self.rect.left = ((self.rect.left // 24))*24 + 24
                
        except IndexError:
            # if you fall off the map you die
            if self.state != 'D':
                pygame.mixer.Sound("./assets/sounds/death.wav").play()
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

        self.mass = 60 # set mass of the character
        self.name = "Ranger" # set name of the character
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/ranger/NES_Ranger_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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
        action_space = ['K', 'CP', 'P', 'JK'] # actions the CPU can take
        direction_space = ['L', 'R'] # directions

        if player.state != "D": # can't do anything if dead
            # face towards the opponent player
            if player.rect.x < self.rect.x:
                if self.state not in ['D', 'H', 'KO']: # if not dead, hurt or knocked out
                    self.direction = 'L'
            elif player.rect.x > self.rect.x:
                if self.state not in ['D', 'H', 'KO']: # if not dead, hurt or knocked out
                    self.direction = 'R'

            # if similar y value
            if abs(player.rect.y - self.rect.y) < 24:   
                if abs(player.rect.x - self.rect.x) < 10: # if very close to the opposing player value make an attack
                    self.update_state(random.choice(action_space)) # randomly pick an attack
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play() # play punch sound
                elif player.rect.x < 600 and player.rect.x > 168: # don't walk off the map
                    if abs(player.rect.x - self.rect.x) < 50: # if close  to the opposing player sprint before attacking
                        self.update_state('R')
                    else:
                        self.update_state('W') # else walk
            elif player.rect.x < 600 and player.rect.x > 168 and abs(player.rect.x - self.rect.x) > 10: # don't walk off the map
                self.update_state('W') # walk in the direction of the opposing player
            else:
                self.update_state('I')

        # make jump at this part of the map 
        if (abs(self.rect.x - 432) < 10 and self.direction == 'L') or (abs(self.rect.x - 360) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
            self.update_state('R') 
            self.make_jump()

        if self.state == "R":
            self.speedx = 4 # set speedx during running
        if self.state == "W":
            self.speedx = 2 # set speedx during walking
        if self.isjump == True: # if jumping
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360: # when jumping farmes get to 360 begin jump
                self.speedy = (-600 // self.mass) # gain speedy proportional to mass 
                if self.yellow_empowered: # if yellow empowered increase jumping speed by 50%
                    self.speedy = int(self.speedy * 1.5) 
            else:
                self.speedy += 1 # handle gravity and decrement speedy

    def make_jump(self):
        super().make_jump()

    def update(self):
        super().update()

class Soldier_CPU(CPU_Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 75 # set mass of character
        self.name = "Soldier" # set name of character
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/soldier/SMS_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
                elif player.rect.x < 696 and player.rect.x > 96: # don't walk off the map
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
                        
            elif player.rect.x < 696 and player.rect.x > 96 and abs(player.rect.x - self.rect.x) > 10: # don't walk off the map
                self.update_state('W')
            else:
                self.update_state('I')

            # make jump at this part of the map 
            if (abs(self.rect.x - 240) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
                self.update_state('R')
                self.make_jump()
                
            # make jump at this part of the map 
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
                if self.speedy == 0: # at the top of the jump make a double jump
                    self.update_state('JK') # make jump kick
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play() # play punch sound

    def make_jump(self):
        super().make_jump()

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        # punching animation
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

        # kicking animation
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

        # override combo punch animation
        # unique soldier combo punch animation
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

        # jump kick animation
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

        # hurt
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # knockout
        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # handle other states
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

        self.mass = 90 # set mass of character
        self.name = "Renegade" # set name of character
        # get character portrait
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/renegade/Renegade_TitleScreen.png')).convert()

        # load in frames and animation strips
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
                    
            if abs(player.rect.y - self.rect.y) < 24: # similar y value
                if abs(player.rect.x - self.rect.x) < 10:
                    self.update_state(random.choice(action_space)) # close x values make attack
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
                elif player.rect.x < 576 and player.rect.x > 240: # don't walk off the map
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
                        
            elif player.rect.x < 576 and player.rect.x > 240 and abs(player.rect.x - self.rect.x) > 10:  # don't walk off the map
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

        self.mass = 55 # set character mass
        self.name = "Agent" # set character name
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/agent/SMS_Agent_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
                elif player.rect.x < 720 and player.rect.x > 72: # don't walk off the map
                    if abs(player.rect.x - self.rect.x) < 50:
                        self.update_state('R')
                    else:
                        self.update_state('W')
            elif player.rect.x < 720 and player.rect.x > 72 and abs(player.rect.x - self.rect.x) > 10: # don't walk off the map
                self.update_state('W')
            else:
                self.update_state('I')
                
        # make jump at this part of the map 
        if (abs(self.rect.x - 264) < 10 and self.direction == 'L') or (abs(self.rect.x - 168) < 10 and self.direction == 'R') and self.state in ['W', 'R']:
            self.update_state('R')
            self.make_jump()

        # make jump at this part of the map 
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
                if self.speedy == 0: # at the top of the jump make a double jump
                    self.update_state('JK') # make a jump kick
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play() # play punch sound

    def make_jump(self):
        super().make_jump()

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        # punch animation
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

        # kick animation
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

        # override jump kick animation
        # unique agent jump kick flip animation 
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

        # hurt
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # knockout
        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # handle other states
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
        self.e_frames = 0 # empowered frames
        self.blue_empowered = False
        self.yellow_empowered = False

    def update_state(self, new):
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']: # can't make actions during animations
            self.state = new
            self.a_frames = 0 # reset animation frames
            
    def handle_controls(self):
        keystate = pygame.key.get_pressed()
        # handle player direction
        if self.state not in ['D', 'H', 'KO']: # can't change direction when dead, hurt or knockedout
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
                pygame.mixer.Sound("./assets/sounds/jump.wav").play() # play jumping sound
                self.j_frames = 0
                self.isjump = True
        else:
            if self.j_frames < 360:
                self.speedy = 0
            elif self.j_frames == 360: # starting jump when jumping frames equals 360
                self.speedy = (-600 // self.mass) # gain speedy proportional to character mass
                if self.yellow_empowered: # if yellow empowered increase speedy by 50%
                    self.speedy = int(self.speedy * 1.5)
            else:
                self.speedy += 1 # handle gravity and decrement speedy
                
        # handle additional key presses
        if keystate[pygame.K_s]:
            self.update_state('C') # crouch on [S] key pressed
        elif keystate[pygame.K_LSHIFT]: # sprint on [LSHIFT] key pressed
            self.update_state('R')
            self.speedx = self.speedx*2 # multiply speed by 2

        # handle mouse clicks / player attacks
        mousestate = pygame.mouse.get_pressed()
        if self.state not in ['P', 'K', 'JK', 'CP', 'D', 'H', 'KO']: # can't make an action during an animation
            if self.state == "C":
                if mousestate == (0,0,1) and self.isdoublejump == False: # if crouching and right click then jump kick
                    self.update_state('JK')
                    self.a_frames = 0
                    self.isdoublejump = True
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play() # play punching sound
                elif mousestate == (1,0,0): # if crouching and left click then combo punch
                    self.update_state('CP')
                    self.a_frames = 0
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
            else:   
                if mousestate == (0,0,1): # if right click then kick
                    self.update_state('K')
                    self.a_frames = 0
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
                elif mousestate == (1,0,0): # if left click then punch
                    self.update_state('P')
                    self.a_frames = 0
                    pygame.mixer.Sound("./assets/sounds/punch.wav").play()
            
                    
    def update(self):
        # get character positional informtaion
        pos_x = self.rect.x
        pos_y = self.rect.y

        self.speedx = 0 # reset speedx to 0 before handling controls
        self.update_state('I')

        self.handle_controls() # update state based on user input

        # if punching follow punching animation
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

        # if kicking follow kicking animation
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

        # combo punch animation
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

        # jump kick animation
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

        # hurt
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass # knock back proportional to character mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # knockout
        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass # knock back proportional to character mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # handl other player states
        if self.state == "I":
            # follow idle animation using idle frames
            frame = (self.i_frames // 360) % len(self.s_idle)
            self.image = self.s_idle[frame]
            self.speedx = 0
        if self.state == "W":
            # follow walking animation
            frame = (pos_x // 10) % len(self.s_walking)
            self.image = self.s_walking[frame]
        if self.state == "R":
            # follow running animation
            frame = (pos_x // 20) % len(self.s_running)
            self.image = self.s_running[frame]
        if self.state == "C":
            # use crouch frame
            frame = self.i_crouch
            self.image = frame
            self.speedx = 0
        if self.state == "H":
            # use hurt frame
            frame = self.i_hurt
            self.image = frame
        if self.state == "KO":
            # use knockout frame
            frame = self.i_knockout
            self.image = frame
        if self.state == "D":
            # use death frame
            frame = self.i_death
            self.image = frame
            self.speedx = 0
            self.speedy = 0
            if self.lives > 0 and self.a_frames > 3000: # respawn shortly after character death
                self.reset()
            
        if self.direction == "L": # if facing left flip the character frame
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = self.speedx * (-1)

        if self.blue_empowered and self.e_frames < 18000: # if blue empowered tint the image blue
            tint_image = self.image.copy()
            tint_image.fill((0,0,190, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else: # after 5 seconds remove power
            self.blue_empowered = False

        if self.yellow_empowered and self.e_frames < 18000: # if yellow empowered tint the image yellow
            tint_image = self.image.copy()
            tint_image.fill((190,190,0, 100), special_flags=pygame.BLEND_ADD)
            self.image = tint_image
        else: # after 5 seconds remove power
            self.yellow_empowered = False

        # update character position based on speedx and speedy
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # increment animation frames, jumping frames, idle frames, and empowered frames
        self.a_frames += 60
        self.j_frames += 60
        self.i_frames += 60
        self.e_frames += 60

        # handle wall and floors of the game scene
        self.handle_scene()


    def handle_scene(self):
        try:
            # Set the floor for the current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [1, 2, 3, 4, 5, 6, 7, 8] or self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.rect.bottom = ((self.rect.bottom // 24))*24 - 1
                # if touching floor
                # can jump and double jump
                self.isjump = False
                self.isdoublejump = False
                self.speedy = 0 # set speedy to 0
            else:
                # if not touching the floor can't jump
                self.isjump = True

            # set the walls for rhe current game scene
            if self.scene.grid[self.rect.bottom // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18] or self.scene.grid[self.rect.top // 24][self.rect.right // 24] in [11, 12, 13, 14, 15, 16, 17, 18]:
                self.rect.right = ((self.rect.right // 24))*24 - 1

            if self.scene.grid[self.rect.bottom // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28] or self.scene.grid[self.rect.top // 24][self.rect.left // 24] in [21, 22, 23, 24, 25, 26, 27, 28]:
                self.rect.left = ((self.rect.left // 24))*24 + 24
        except IndexError:
            # if you fall off the map you die
            if self.state != 'D':
                pygame.mixer.Sound("./assets/sounds/death.wav").play()
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

        self.mass = 60 # set character mass
        self.name = "Ranger" # set character name
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/ranger/NES_Ranger_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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

        self.mass = 60 # set character mass
        self.name = "Vigilante" # set character name
        # get character portrait
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/vigilante/Vigilante_TitleScreen.png')).convert()

        # load in frames and animation strip
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

        self.mass = 75 # set character mass
        self.name = "Soldier" # set character name
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/soldier/SMS_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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

        self.speedx = 0
        self.update_state('I')

        self.handle_controls()

        # punching animation
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

        # kicking animation
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

        # override combo punch animation
        # unique soldier combo punch animation
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

        # jump kick animation
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

        # hurt
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # knockout
        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # handle other player states
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

        self.mass = 90 # set character mass
        self.name = "Renegade" # set character name
        # get character portrait
        self.i_title_screen = pygame.image.load(os.path.join('', 'assets/renegade/Renegade_TitleScreen.png')).convert()

        # load in frames and animation strips
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
        # override jump kick state
        if self.state == 'JK':
            # don't have a jump kick animation strip so use kick animation strip
            self.state = 'K'
            self.a_frames = 0
            self.isdoublejump = False

    def update(self):
        super().update()

class Agent_Player(Player):

    def __init__(self, scene):
        super().__init__(scene)

        self.mass = 55 # set character mass
        self.name = "Agent" # set character name
        # get character portrait
        self.i_title_screen = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/agent/SMS_Agent_TitleScreen.png')).convert(), (88, 136))

        # load in frames and animation strips
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
        # override combo punch state
        if self.state == 'CP':
            # don't have a combo punch animation strip so use punch animation
            self.state = 'P'
            self.a_frames = 0
            self.isdoublejump = False

    def update(self):
        pos_x = self.rect.x
        pos_y = self.rect.y

        self.speedx = 0
        self.update_state('I')

        self.handle_controls()

        # punching animation
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

        # kicking animation
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

        # override jump kick animation
        # unique agent jump kick flip animation 
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

        # hurt
        if self.state == "H":
            if self.a_frames < 2160:
                self.speedx = int(-100*self.damage) // self.mass
                self.speedy = int(-1*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"

        # knockout
        if self.state == "KO":
            if self.a_frames < 2160:
                self.speedx = int(-200*self.damage) // self.mass
                self.speedy = int(-2*self.damage) // self.mass
                self.isjump = True
            else:
                self.state = "I"
        # handle other player states
        if self.state == "I" or self.state == "C":
            # don't have a crouching frame
            # use idle frames for crouching
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
    

# SpriteStrip class handles the conversion of animation strips to python lists of frames
class SpriteStrip(object):
    def __init__(self, file_name):
        # load in animation strip from filename
        self.sprite_strip = pygame.image.load(file_name).convert_alpha()

    def get_strip(self, width, height, t_width, t_height):
        # convert the sprite strip to pyhton list
        strip = []
        n = t_width // width
        # cut the stripe strip up into n pieces defined by width, height, total width, and total height
        for i in range(0,n):
            image = pygame.Surface([width, height], pygame.SRCALPHA)
            image.blit(self.sprite_strip, (0,0), (i*width, 0, width, height))
            strip.append(image)
        return strip
