import pygame
from pygame.locals import *
import os
import random
from scene import *
from player import *
from GUI import *
from item import *
import sys

# CONSTANTS
WIDTH = 792
HEIGHT = 432
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT = (196, 196, 196)
DARK = (80, 80, 80)

# init pygame
clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((BLACK))

background = pygame.image.load(os.path.join('', 'assets/background/background.jpg')).convert()

font_name = pygame.font.match_font('arial')
font = pygame.font.Font("assets/fonts/ka1.ttf", 20)
font_big = pygame.font.Font("assets/fonts/ka1.ttf", 40)
font_small = pygame.font.Font("assets/fonts/VCR.ttf", 14)
                
def checkCollision(sprite1, sprite2):
    return pygame.sprite.collide_rect(sprite1, sprite2)

def handle_collision(player1, player2):
    if player1.rect.x < player2.rect.x and player1.direction == 'R' and player2.state not in ['H', 'KO']:
        if player1.state in ['P', 'K']:
            if player1.blue_empowered:
                player2.damage += 0.20
            player2.state = 'H'
            player2.direction = 'L'
            player2.damage += 0.05
        elif player1.state in ['CP', 'JK']:
            if player1.blue_empowered:
                player2.damage += 0.20
            player2.state = 'KO'
            player2.direction = 'L'
            player2.damage += 0.20
    elif player1.rect.x > player2.rect.x and player1.direction == 'L' and player2.state not in ['H', 'KO']:
        if player1.state in ['P', 'K']:
            if player1.blue_empowered:
                player2.damage += 0.20
            player2.state = 'H'
            player2.direction = 'R'
            player2.damage += 0.05
        elif player1.state in ['CP', 'JK']:
            if player1.blue_empowered:
                player2.damage += 0.20
            player2.state = 'KO'
            player2.direction = 'R'
            player2.damage += 0.20
    if player2.rect.x < player1.rect.x and player2.direction == 'R' and player1.state not in ['H', 'KO']:
        if player2.state in ['P', 'K']:
            if player2.blue_empowered:
                player1.damage += 0.20
            player1.state = 'H'
            player1.direction = 'L'
            player1.damage += 0.05
        elif player2.state in ['CP', 'JK']:
            if player2.blue_empowered:
                player1.damage += 0.20
            player1.state = 'KO'
            player1.direction = 'L'
            player1.damage += 0.20
    elif player2.rect.x > player1.rect.x and player2.direction == 'L' and player1.state not in ['H', 'KO']:
        if player2.state in ['P', 'K']:
            if player2.blue_empowered:
                player1.damage += 0.20
            player1.state = 'H'
            player1.direction = 'R'
            player1.damage += 0.05
        elif player2.state in ['CP', 'JK']:
            if player2.blue_empowered:
                player1.damage += 0.20
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
        drawText('COVID 19 VIGILANTE 2020', font_big, screen, WIDTH // 2, HEIGHT // 2 - 40, WHITE)
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
        screen.blit(background, (0,0))
        drawText('COVID 19 VIGILANTE', font_big, screen, WIDTH // 2, 40, WHITE)

        mx, my = pygame.mouse.get_pos()

        campaign_button = Button(WIDTH // 2 - 125, HEIGHT // 2 - 90,250,50,BLACK,LIGHT,'Campaign')
        freeplay_button = Button(WIDTH // 2 - 125, HEIGHT // 2 - 30,250,50,BLACK,LIGHT,'Free Play')
        sandbox_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 30,250,50,BLACK,LIGHT,'Sandbox')
        tutorial_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 90,250,50,BLACK,LIGHT,'Tutorial')

        campaign_button.draw(screen, font)
        freeplay_button.draw(screen, font)
        sandbox_button.draw(screen, font)
        tutorial_button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    quit_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if campaign_button.check():
                        campaign()
                    elif freeplay_button.check():
                        character_selection_menu('freeplay')
                    elif sandbox_button.check():
                        character_selection_menu('sandbox')
                    elif tutorial_button.check():
                        tutorial()

        pygame.display.update()
        clock.tick(FPS)

def quit_menu():
    running = True
    while running:
        screen.blit(background, (0,0))
                
        mx, my = pygame.mouse.get_pos()

        continue_button = Button(WIDTH // 2 - 125, HEIGHT // 2 - 60,250,50,BLACK,LIGHT,'Continue')
        main_menu_button = Button(WIDTH // 2 - 125, HEIGHT // 2 ,250,50,BLACK,LIGHT,'Main Menu')
        quit_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 60,250,50,BLACK,LIGHT,'Quit Game')
        
        continue_button.draw(screen, font)
        main_menu_button.draw(screen,font)
        quit_button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if continue_button.check():
                        return True
                    elif main_menu_button.check():
                        return False
                    elif quit_button.check():
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
        clock.tick(FPS)
        
def character_selection_menu(game_type):
    running = True
    
    vigilante_image = pygame.image.load(os.path.join('', 'assets/vigilante/Vigilante_TitleScreen.png')).convert()
    renegade_image = pygame.image.load(os.path.join('', 'assets/renegade/Renegade_TitleScreen.png')).convert()
    ranger_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/ranger/NES_Ranger_TitleScreen.png')).convert(), (88, 136))
    agent_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/agent/SMS_Agent_TitleScreen.png')).convert(), (88, 136))
    soldier_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/soldier/SMS_TitleScreen.png')).convert(), (88, 136))
    
    while running:
        screen.blit(background, (0,0))
        drawText('Character Selection', font_big, screen, WIDTH // 2, 40, WHITE)

        mx, my = pygame.mouse.get_pos()

        vigilante_button = Button(WIDTH // 2 - 170, HEIGHT // 2 ,100,30,BLACK,LIGHT,'Vigilante')
        renegade_button = Button(WIDTH // 2 - 50, HEIGHT // 2 ,100,30,BLACK,LIGHT,'Renegade')
        ranger_button = Button(WIDTH // 2 + 70, HEIGHT // 2 ,100,30,BLACK,LIGHT,'Ranger')
        agent_button = Button(WIDTH // 2 - 110, HEIGHT // 2 + 180,100,30,BLACK,LIGHT,'Agent')
        soldier_button = Button(WIDTH // 2 + 10, HEIGHT // 2 + 180,100,30,BLACK,LIGHT,'Soldier')

        vigilante_button.draw(screen, font_small)
        renegade_button.draw(screen, font_small)
        ranger_button.draw(screen, font_small)
        agent_button.draw(screen, font_small)
        soldier_button.draw(screen, font_small)

        screen.blit(vigilante_image, (WIDTH // 2 - 164, HEIGHT // 2 - 137))
        screen.blit(renegade_image, (WIDTH // 2 - 44, HEIGHT // 2 - 137))
        screen.blit(ranger_image, (WIDTH // 2 + 76, HEIGHT // 2 - 137))
        screen.blit(agent_image, (WIDTH // 2 - 104, HEIGHT // 2 + 43))
        screen.blit(soldier_image, (WIDTH // 2 + 16, HEIGHT // 2 + 43))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if not quit_menu():
                        return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if vigilante_button.check():
                        map_selection_menu(game_type, 'Vigilante')
                        return
                    elif renegade_button.check():
                        map_selection_menu(game_type, 'Renegade')
                        return
                    elif ranger_button.check():
                        map_selection_menu(game_type, 'Ranger')
                        return
                    elif agent_button.check():
                        map_selection_menu(game_type, 'Agent')
                        return
                    elif soldier_button.check():
                        map_selection_menu(game_type, 'Soldier')
                        return
                
        pygame.display.update()
        clock.tick(FPS)
        
def map_selection_menu(game_type, character_selection):
    running = True
    durham_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/background/durham.jpg')).convert(), (200, 112))
    london_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/background/london.jpg')).convert(), (200, 112))
    downing_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/background/10_downing.jpg')).convert(), (200, 112))
    army_image = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/background/army_base.jpg')).convert(), (200, 112))
    
    while running:
        screen.blit(background, (0,0))
        drawText('Map Selection', font_big, screen, WIDTH // 2, 40, WHITE)

        mx, my = pygame.mouse.get_pos()

        durham_button = Button(WIDTH // 2 - 220, HEIGHT // 2 ,200,30,BLACK,LIGHT,'Durham')
        london_button = Button(WIDTH // 2 + 20, HEIGHT // 2 ,200,30,BLACK,LIGHT,'London')
        downing_button = Button(WIDTH // 2 - 220, HEIGHT // 2 + 175,200,30,BLACK,LIGHT,'10 Downing Street')
        army_button = Button(WIDTH // 2 + 20, HEIGHT // 2 + 175,200,30,BLACK,LIGHT,'Scottish Army Base')
        
        durham_button.draw(screen, font_small)
        london_button.draw(screen, font_small)
        downing_button.draw(screen, font_small)
        army_button.draw(screen, font_small)

        screen.blit(durham_image, (WIDTH // 2 - 220, HEIGHT // 2 - 113))
        screen.blit(london_image, (WIDTH // 2 + 20, HEIGHT // 2 - 113))
        screen.blit(downing_image, (WIDTH // 2 - 220, HEIGHT // 2 + 62))
        screen.blit(army_image, (WIDTH // 2 + 20, HEIGHT // 2 + 62))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if not quit_menu():
                        return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if durham_button.check():
                        game(game_type, character_selection, 'Durham')
                        return
                    elif london_button.check():
                        game(game_type, character_selection, 'London')
                        return
                    elif downing_button.check():
                        game(game_type, character_selection, '10 Downing')
                        return
                    elif army_button.check():
                        game(game_type, character_selection, 'Army Base')
                        return
                        
        pygame.display.update()
        clock.tick(FPS)

def pause_menu():
    running = True
    while running:

        mx, my = pygame.mouse.get_pos()

        resume_button = Button(WIDTH // 2 - 125, HEIGHT // 2 - 30,250,50,BLACK,LIGHT,'Resume Game')
        quit_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 30,250,50,BLACK,LIGHT,'Main Menu')
        
        resume_button.draw(screen, font)
        quit_button.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if resume_button.check():
                        return True
                    if quit_button.check():
                        return False
        pygame.display.update()
        clock.tick(FPS)

def victory_screen(player):
    running = True
    a_frames = 0.0
    while running:
        a_frames += 1.0
        
        if a_frames < 255:
            r_col = int(227 * (a_frames / 255))
            g_col = int(216 * (a_frames / 255))
            b_col = 0
            
        screen.fill((0,0,0))
        drawText('VICTORY', font_big, screen, WIDTH // 2, HEIGHT // 2, (r_col, g_col, b_col))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                if event.key==pygame.K_RETURN:
                    return

        if a_frames > 500:
            return

        pygame.display.update()
        clock.tick(FPS)

def defeat_screen(player):
    running = True
    a_frames = 0.0
    while running:
        a_frames += 1.0
        
        if a_frames < 255:
            r_col = int(227 * (a_frames / 255))
            g_col = int(23 * (a_frames / 255))
            b_col = 0
            
        screen.fill((0,0,0))
        drawText('DEFEAT', font_big, screen, WIDTH // 2, HEIGHT // 2, (r_col, g_col, b_col))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    return
                if event.key==pygame.K_RETURN:
                    return

        if a_frames > 500:
            return

        pygame.display.update()
        clock.tick(FPS)

def story_screen(text, seconds):
    running = True
    a_frames = 0
    while running:
        a_frames += 1
        
        if a_frames < 255:
            col = (a_frames, a_frames, a_frames)
            
        screen.fill((0,0,0))
        drawText(text, font_small, screen, WIDTH // 2, HEIGHT // 2, col)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    return True
                if event.key==pygame.K_ESCAPE:
                    if not quit_menu():
                        return False
                
        if a_frames > (seconds * FPS):
            return True

        pygame.display.update()
        clock.tick(FPS)

def campaign():
    s = story_screen('COVID 19 VIGILANTE 2020 campaign', 6.0)
    if not s:
        return

    s = story_screen('Before the covid19 pandemic Kieran Smith was just an ordindary local lad', 8.0)
    if not s:
        return

    s = story_screen("Kieran's gran was one of the first people in the UK to fall sick", 8.0)
    if not s:
        return

    s = story_screen("While Kieran's gran spent her nights in the hospital", 6.0)
    if not s:
        return

    s = story_screen("Kieran spent his nights on the street making sure everyone was obeying government regulations", 8.0)
    if not s:
        return

    s = story_screen("Kieran fought for his gran and the most vulnerble in our society", 8.0)
    if not s:
        return

    s = story_screen("He became known as the COVID 19 VIGILANTE ...", 6.0)
    if not s:
        return

    winner = False
    while winner == False:
        winner = game('campaign', 'Vigilante', 'Durham')
        if winner == None:
            return
        
    s = story_screen('After fighting countless anti-maskers on the streets of Durham a rumour surfaced', 8.0)
    if not s:
        return

    s = story_screen('Kieran had cought wind of a rumour that a cure for covid19 had been found', 8.0)
    if not s:
        return

    s = story_screen('Supposedly the cure was being kept secret by the government, but why?', 8.0)
    if not s:
        return

    s = story_screen('Kieran decided to head to london for answers but was soon caught in the middle of something', 8.0)
    if not s:
        return

    s = story_screen('An extinction rebellion march? No one was obeying social distancing rules', 8.0)
    if not s:
        return

    s = story_screen('The vigilante decided to take the law into his hands once again ...', 6.0)
    if not s:
        return
    
    winner = False
    while winner == False:
        winner = game('campaign', 'Vigilante', 'London')
        if winner == None:
            return
        
    s = story_screen('After making quick work of the extinction rebellion march Kieran was on the run', 8.0)
    if not s:
        return

    s = story_screen('Kieran made his way to 10 downing street to get his answers', 8.0)
    if not s:
        return

    s = story_screen('Before reaching the Prime Minister Kieran was intercepted by a government agent', 8.0)
    if not s:
        return

    s = story_screen('The agent was onto him and Kieran had to act swiftly ...', 6.0)
    if not s:
        return
    
    winner = False
    while winner == False:
        winner = game('campaign', 'Vigilante', '10 Downing')
        if winner == None:
            return
        
    s = story_screen('The dazed government agent surrendered himself to Kieran and said', 8.0)
    if not s:
        return

    s = story_screen('"Do what I could not and make the world a better place...', 6.0)
    if not s:
        return

    s = story_screen('"go to these coordinates and you will find what you are looking for"', 6.0)
    if not s:
        return

    s = story_screen('Without hesitation Kieran got on the first LNER train', 6.0)
    if not s:
        return

    s = story_screen('He was bound for the a secret army camp hidden in the scottish highlands', 8.0)
    if not s:
        return

    s = story_screen('What he would find he did not know ...', 6.0)
    if not s:
        return
    
    winner = False
    while winner == False:
        winner = game('campaign', 'Vigilante', 'Army Base')
        if winner == None:
            return
        
    s = story_screen("Kieran took the unconcious Soldier's keycard and downloaded all the government's secrets ", 8.0)
    if not s:
        return

    s = story_screen("The government had found a cure to covid19 but had been keeping it secret", 8.0)
    if not s:
        return

    s = story_screen("The vigilante acted switfly exposing the government and they had no choice but to resign", 8.0)
    if not s:
        return

    s = story_screen("The new administration distributed the cure around the UK, saving Kieran's gran's life in the process", 8.0)
    if not s:
        return

    s = story_screen("The covid19 pandemic was finished", 4.0)
    if not s:
        return

    s = story_screen("The End", 8.0)
    if not s:
        return

def tutorial():
    running = True
    scene = Scene('Durham')
    bg = pygame.image.load(os.path.join('', scene.bg_path)).convert()
    all_sprites = pygame.sprite.Group()
    player = Vigilante_Player(scene)
    all_sprites.add(player)
    player.lives = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    player.reset()
                if event.key==pygame.K_ESCAPE:
                    if not pause_menu():
                        return
        
        all_sprites.update()
        screen.blit(bg, (0,0))
        
        
        all_sprites.draw(screen)
        scene.draw(screen)
        

        if player.state == "D":
            drawText('Press ENTER to respawn', font_big, screen, WIDTH // 2, 50, DARK)
        else:
            drawText('To Move:', font, screen, 90, 25, DARK)
            drawText('W', font_big, screen, 90, 70, DARK)
            drawText('A S D', font_big, screen, 90, 115, DARK)
            drawText('LSHIFT', font, screen, 90, 160, DARK)

            drawText('To Attack:', font, screen, 250, 25, DARK)
            drawText('LMB', font_big, screen, 250, 70, DARK)
            drawText('RMB', font_big, screen, 250, 115, DARK)

            drawText('Combos:', font, screen, 420, 25, DARK)
            drawText('S LMB', font_big, screen, 420, 70, DARK)
            drawText('S RMB', font_big, screen, 420, 115, DARK)

            drawText('Advanced:', font, screen, 630, 25, DARK)
            drawText('W S RMB', font_big, screen, 630, 70, DARK)
                
            
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)  
     
        
# game loop
def game(game_type, character_selection, map_selection):
    running = True
    scene = Scene(map_selection)
    bg = pygame.image.load(os.path.join('', scene.bg_path)).convert()
    i_bar = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/GUI/bar.png')).convert_alpha(), (156, 40))
    i_life = pygame.transform.scale(pygame.image.load(os.path.join('', 'assets/GUI/life.png')).convert_alpha(), (20, 20))

    pygame.time.set_timer(USEREVENT+1, 15000)
    
    all_sprites = pygame.sprite.Group()
    player = None
    cpu_player =  None

    if character_selection == 'Vigilante':
        player = Vigilante_Player(scene)
    elif character_selection == 'Renegade':
        player = Renegade_Player(scene)        
    elif character_selection == 'Ranger':
        player = Ranger_Player(scene)              
    elif character_selection == 'Agent':
        player = Agent_Player(scene)      
    elif character_selection == 'Soldier':
        player = Soldier_Player(scene)
    else:
        return

    all_sprites.add(player)
                
    if game_type in ['freeplay', 'campaign']:    
        if map_selection == 'Durham':
            cpu_player = Renegade_CPU(scene)
        elif map_selection == 'London':
            cpu_player = Ranger_CPU(scene)        
        elif map_selection == '10 Downing':
            cpu_player = Agent_CPU(scene)
        elif map_selection == 'Army Base':
            cpu_player = Soldier_CPU(scene)
        else:
            return
             
        all_sprites.add(cpu_player)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    if game_type in ['sandbox', 'tutorial']:
                        player.lives = 3
                        player.reset()
                if event.key==pygame.K_ESCAPE:
                    if not pause_menu():
                        return None
            if event.type == USEREVENT+1:
                random_drink = random.randint(1, 3)
                if random_drink == 1:     
                   item = Blue_Energy(scene, player, cpu_player)
                   all_sprites.add(item)
                elif random_drink == 2:
                   item = Red_Energy(scene, player, cpu_player)
                   all_sprites.add(item)
                else:
                   item = Yellow_Energy(scene, player, cpu_player)
                   all_sprites.add(item)
                   
        if game_type in ['freeplay', 'campaign']:
            cpu_player.make_action(player)
            if checkCollision(player, cpu_player):
                handle_collision(player, cpu_player)

        all_sprites.update()
        screen.blit(bg, (0,0))
        
        all_sprites.draw(screen)
        scene.draw(screen)

        if game_type in ['freeplay', 'campaign']:
            drawText(player.name, font, screen, 90, 25, BLACK)
            for x in range(player.lives):
                screen.blit(i_life, (20 + x*20, 85))
            screen.blit(i_bar, (90 - 78, 61 - 20))
            
            drawText('DMG : '+ str(int(player.damage*100)), font, screen, 90, 61, DARK)
            
            drawText('CPU', font, screen, 702, 25, BLACK)
            for x in range(cpu_player.lives):
                screen.blit(i_life, (632 + x*20, 85))
            screen.blit(i_bar, (702 - 78, 61 - 20))
            drawText('DMG : '+ str(int(cpu_player.damage*100)), font, screen, 702, 61, DARK)
        else:
            if player.state == "D" and player.lives < 1:
                drawText('Press ENTER to respawn', font_big, screen, WIDTH // 2, 50, BLACK)
            else:
                drawText(player.name, font, screen, 90, 25, BLACK)
                for x in range(player.lives):
                    screen.blit(i_life, (20 + x*20, 85))
                screen.blit(i_bar, (90 - 78, 61 - 20))
            
                drawText('DMG : '+ str(int(player.damage*100)), font, screen, 90, 61, DARK)
                
        pygame.display.flip()
        pygame.display.update()
        clock.tick(FPS)
        
        if game_type in ['freeplay', 'campaign']:
            if player.lives == 0:
                defeat_screen(cpu_player)
                return False
            elif cpu_player.lives == 0:
                victory_screen(player)
                return True
                
start_screen()
start_menu()

pygame.quit()
sys.exit()



