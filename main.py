import pygame
from pygame.locals import *
import os
import random
from scene import *
from player import *
from GUI import *

# CONSTANTS
WIDTH = 792
HEIGHT = 432
FPS = 60

YELLOW = (252, 244, 3)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# init pygame
clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((BLACK))
bg = pygame.image.load(os.path.join('', 'assets/background/durham.jpg')).convert()

bgX = 0
bgX2 = bg.get_width()

font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 20)
font_big = pygame.font.Font(font_name, 50)

# player handling functions
def CPU_action(player, cpu_player):
        action_space = ['K']
        direction_space = ['L', 'R']

        if player.state != "D":
            if player.rect.x < cpu_player.rect.x:
                if cpu_player.state not in ['D', 'H', 'KO']:
                    cpu_player.direction = 'L'
            elif player.rect.x > cpu_player.rect.x:
                if cpu_player.state not in ['D', 'H', 'KO']:
                    cpu_player.direction = 'R'

            if abs(player.rect.x - cpu_player.rect.x) < 10:
                cpu_player.update_state(random.choice(action_space))
            elif abs(player.rect.x - cpu_player.rect.x) < 150:
                cpu_player.update_state('W')
            else:
                cpu_player.update_state('I')
        else:
            cpu_player.update_state('I')
        
        if cpu_player.state == "R":
            cpu_player.speedx = 4
        if cpu_player.state == "W":
            cpu_player.speedx = 2
        if cpu_player.isjump == True:
            if cpu_player.j_frames < 360:
                cpu_player.speedy = 0
            elif cpu_player.j_frames == 360:
                cpu_player.speedy = (-600 // cpu_player.mass)
            else:
                cpu_player.speedy += 1
                
def checkCollision(sprite1, sprite2):
    return pygame.sprite.collide_rect(sprite1, sprite2)

def handle_collision(player1, player2):
    if player1.rect.x < player2.rect.x and player1.direction == 'R' and player2.state not in ['H', 'KO']:
        if player1.state in ['P', 'K']:
            player2.state = 'H'
            player2.direction = 'L'
            player2.damage += 0.05
            player2.forcex = -20
        elif player1.state in ['CP', 'JK']:
            player2.state = 'KO'
            player2.direction = 'L'
            player2.damage += 0.20
    elif player1.rect.x > player2.rect.x and player1.direction == 'L' and player2.state not in ['H', 'KO']:
        if player1.state in ['P', 'K']:
            player2.state = 'H'
            player2.direction = 'R'
            player2.damage += 0.05
        elif player1.state in ['CP', 'JK']:
            player2.state = 'KO'
            player2.direction = 'R'
            player2.damage += 0.20
    if player2.rect.x < player1.rect.x and player2.direction == 'R' and player1.state not in ['H', 'KO']:
        if player2.state in ['P', 'K']:
            player1.state = 'H'
            player1.direction = 'L'
            player1.damage += 0.05
        elif player2.state in ['CP', 'JK']:
            player1.state = 'KO'
            player1.direction = 'L'
            player1.damage += 0.20
    elif player2.rect.x > player1.rect.x and player2.direction == 'L' and player1.state not in ['H', 'KO']:
        if player2.state in ['P', 'K']:
            player1.state = 'H'
            player1.direction = 'R'
            player1.damage += 0.05
        elif player2.state in ['CP', 'JK']:
            player1.state = 'KO'
            player1.direction = 'R'
            player1.damage += 0.20

# start screen loop
def start_screen():
    running = True
    a_frames = 0
    while running:
        if a_frames < 255:
            a_frames += 1
        screen.fill((0,0,0))
        drawText('COVID 19 \n VIGILANTE 2020', font_big, screen, WIDTH // 2, HEIGHT // 2 - 40, WHITE)
        drawText('Press [ENTER] to Continue', font, screen, WIDTH // 2, HEIGHT // 2 + 20, (a_frames, a_frames, a_frames))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    running = False

        pygame.display.update()
        clock.tick(FPS)

# start menu loop
def start_menu():
    while True:
        screen.blit(bg, (bgX,0))
        drawText('COVID 19 VIGILANTE', font_big, screen, WIDTH // 2, 40, BLACK)

        mx, my = pygame.mouse.get_pos()

        campaign_button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 90,100,50,BLACK,BLUE,'Campaign')
        freeplay_button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 30,100,50,BLACK,BLUE,'Free Play')
        sandbox_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 30,100,50,BLACK,BLUE,'Sandbox')
        tutorial_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 90,100,50,BLACK,BLUE,'Tutorial')

        campaign_button.draw(screen, font)
        freeplay_button.draw(screen, font)
        sandbox_button.draw(screen, font)
        tutorial_button.draw(screen, font)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if campaign_button.check():
                        pass
                    if freeplay_button.check():
                        game()
                    if sandbox_button.check():
                        pass
                    if tutorial_button.check():
                        pass

        pygame.display.update()
        clock.tick(FPS)

# game loop
def game():
    running = True
    scene = Scene()

    all_sprites = pygame.sprite.Group()
    player = Agent_Player(scene)
    all_sprites.add(player)
    cpu_player = Renegade_CPU(scene)
    all_sprites.add(cpu_player)
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    player.reset()
                    cpu_player.reset()
                if event.key==pygame.K_ESCAPE:
                    running = False

        CPU_action(player, cpu_player)
        
        if checkCollision(player, cpu_player):
            handle_collision(player, cpu_player)

        all_sprites.update()
        screen.blit(bg, (bgX,0))
        # draw scores
        drawText(player.name +' : '+ str(int(player.damage*100)) + '%', font, screen, 90, 400, WHITE)
        drawText('CPU : '+ str(int(cpu_player.damage*100)) + '%', font, screen, 702, 400, WHITE)
        all_sprites.draw(screen)
        scene.draw(screen)
            
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)

start_screen()
start_menu()

pygame.quit()




