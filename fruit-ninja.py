import pygame
import string
from pygame.locals import *
import random
import time

pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 846, 476
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
display = pygame.display.set_mode((846, 476))
half_boom1 = pygame.image.load("fruit/explosion.png")
fond = pygame.image.load("dojo.jpg").convert()
fond_freeze = pygame.image.load("fruit/dojo_ice.jpg").convert()
letter = string.ascii_lowercase
fruit= ['abricot', 'banane', 'orange', 'pasteque', 'poire', 'bombe', 'glacon']
clock = pygame.time.Clock() 
point = 0
multiplicateur = 1
life = 3
glacon_time = 0
freeze = False
data = {} #création bibliotheque
display.blit(fond, (0, 0))#Fond de la fenetre
eliminated_fruits = []

WHITE = (255,255,255)
BLACK = (0, 0, 0)
COLORS = [(180, 100, 255), (255, 0, 0), (255, 255, 0), (255, 165, 0), (0, 128, 0), 
          (0, 128, 0), (255, 165, 0), (255, 255, 0), (255, 0, 0), (180, 100, 255)]

font = pygame.font.SysFont("arialblack", 32) #Police et taille
score_text = font.render('Score : ' + str(point), True, (255, 255, 255))

def draw_button(display, text, x, y, w, h, color, text_color):
    pygame.draw.rect(display, color, (x, y, w, h))
    font = pygame.font.SysFont("arialblack", 32)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    display.blit(text_surface, text_rect)
    return pygame.Rect(x, y, w, h)

def draw_colored_text(display, text, size, x, y, colors):
    font = pygame.font.SysFont("arialblack", size)
    letters = [letter for letter in text if letter != " "]  # Ignorer les espaces
    total_width = sum(font.render(letter, True, colors[i]).get_width() for i, letter in enumerate(letters))
    offset_x = x - total_width // 2
    color_index = 0
    for letter in text:
        if letter == " ":
            offset_x += font.render(" ", True, WHITE).get_width()
            continue
        text_surface = font.render(letter, True, colors[color_index])
        text_rect = text_surface.get_rect()
        text_rect.topleft = (offset_x, y)
        display.blit(text_surface, text_rect)
        offset_x += text_surface.get_width()
        color_index += 1

def generate_random_fruit(fruit):
    fruit_patch = "fruit/" + fruit + ".png" #tout les fruits mis dans une variable
    letter = string.ascii_lowercase
    data[fruit] = { #Donné des fruits (trajectoire, image...)
        'img': pygame.image.load(fruit_patch),
        'letter' : random.choice(letter),
        'x' : random.randint(100, 500),
        'y' : 500,
        'speed_x' : random.randint(-10, 10),
        'speed_y' : random.randint(-60, -40),
        'throw' : False,
        't' : 0,
        'hit' : False,
    }

    if random.random() >= 0.979:
        data[fruit]['throw'] = True
    else :
        data[fruit]['throw'] = False

for fruits in fruit: #genere un fruit random
    generate_random_fruit(fruits)

font_name = pygame.font.match_font('arialblack.ttf')

def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)

def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 100 * i)
        img_rect.y = y
        display.blit(img, img_rect)

def hide_cross_lives(display, x, y):
    display.blit(pygame.image.load('fruit/vie.png'), (x, y))


    
def calculate_combo_bonus(combo_length):
    
    if combo_length >= 3:
        return combo_length + (combo_length - 1)  
    return combo_length 



def show_gameover_screen():
    display.blit(fond, (0, 0))
    draw_text(display, "Score : " + str(point), 40, 423, 100)
    pygame.mixer.music.load('./audio/endgame.mp3')
    pygame.mixer.music.play(-1)
    replay_button = draw_button(display, "Rejouer", DISPLAY_WIDTH / 2 - 100, 200, 200, 50, WHITE, BLACK)
    return_button = draw_button(display, "Retour", DISPLAY_WIDTH / 2 - 100, 300, 200, 50, WHITE, BLACK)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    waiting = False
                    return 2
                if return_button.collidepoint(event.pos):
                    waiting = False
                    return 0
    pygame.mixer.music.stop()

def main_menu():
    display.blit(fond, (0, 0))
    draw_colored_text(display, "FRUIT NINJA", 64, DISPLAY_WIDTH / 2, 10, COLORS)
    pygame.mixer.music.load('./audio/menu.mp3')
    pygame.mixer.music.play(-1)
    play_button = draw_button(display, "Jouer", DISPLAY_WIDTH / 2 - 100, 150, 200, 50, WHITE, BLACK)
    quit_button = draw_button(display, "Quitter", DISPLAY_WIDTH / 2 - 100, 250, 200, 50, WHITE, BLACK)
    pygame.display.flip()
    

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    return False
    pygame.mixer.music.stop()

game_over = False
running = True
menu = True

# Boucle principal 


while running:
    if menu:
        if not main_menu():
            running = False
            break
        menu = False
        game_over = False
        life = 3
        point = 0
        data.clear()
        pygame.mixer.music.load('./audio/ost.mp3')
        pygame.mixer.music.play(-1)
        for fruits in fruit:
            generate_random_fruit(fruits)

    elif game_over:
        action = show_gameover_screen()
        if action == 1:
            running = False
        elif action == 2:
            game_over = False
            life = 3
            point = 0
            data.clear()
            pygame.mixer.music.load('./audio/ost.mp3')
            pygame.mixer.music.play(-1)
            life = 3
            glacon_time = 0
            freeze = False
            new_data = {}
            for fruits in fruit:  
                generate_random_fruit(fruits)
                new_data[fruits] = data[fruits]
            data.clear()
            data.update(new_data)
            for fruits in fruit:
                generate_random_fruit(fruits)
        elif action == 0:
            menu = True
            game_over = False

    else:
        if not freeze:
            display.blit(fond, (0, 0))
        else :
            display.blit(fond_freeze, (0, 0))
        display.blit(score_text, (0, 0))
        draw_lives(display, 520, 5, life, 'fruit/vie.png')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    
        for key, value in data.items():
            if value['throw']:
                letter = value['letter']

                if not freeze:
                    value['x'] += value['speed_x']
                    value['y'] += value['speed_y']
                    value['speed_y'] += (1 * value['t'])
                    value['t'] += 1

                if value['y'] <= 476:
                    display.blit(value['img'], (value['x'], value['y']))
                    draw_text(display, letter, 30, value['x'], value['y'])
                else :
                    if value['y'] >= 476 and not value['hit'] and key != 'bombe' and key != 'glacon':
                        life -= 1
                        if life <= 0:
                            game_over = True
                            if exit == 1:
                                pygame.quit()
                            score_text = font.render('Score : ' + str(point), True, (255, 255, 255))
                    if not freeze:
                        generate_random_fruit(key)

                if freeze == True:
                    now_time = pygame.time.get_ticks()
                    timer = now_time - glacon_time
                    if timer >= 3000:
                        freeze = False
                        value['speed_y'] = prep_valueY
                        value['speed_x'] = prep_valueX
                        if value['y'] <= 476:
                            display.blit(value['img'], (value['x'], value['y']))
                            draw_text(display, letter, 30, value['x'], value['y'])
                        
                            pygame.display.flip()

                if event.type == KEYUP:
                    tap_letter = event.unicode.lower()
                    if not value['hit'] and tap_letter == value['letter']:
                        if key == 'bombe':
                            life -= 3
                            display.blit(fond, (0, 0))
                            display.blit(half_boom1, (value['x'], value['y']))
                            pygame.display.update()
                            time.sleep(1)
                            if life <= 0:
                                game_over = True
                                if exit == 1:
                                    pygame.quit()
                                score_text = font.render('Score : ' + str(point), True, (255, 255, 255))
                        elif key == 'glacon':
                            freeze = True
                            glacon_time = pygame.time.get_ticks()
                            prep_valueY = value['speed_y']
                            prep_valueX = value['speed_x']
                            value['speed_y'] = 0
                            value['speed_x'] = 0
                        else:
                            half_fruit_path = "fruit/" + key + "_sliced.png"
                    
                            value['img'] = pygame.image.load(half_fruit_path)
                        value['speed_x'] += 15

                        if key != 'bombe' and key != 'glacon':
                            point += 1
                        score_text = font.render('Score : ' + str(point), True, (255, 255, 255))
                        
                        value['hit'] = True
                        display.blit(value['img'], (value['x'], value['y']))
                        pygame.display.update()

            else :
                if not freeze: 
                    generate_random_fruit(key)

    pygame.display.flip()#mise a jour de l'image a chaque fin de boucle
    clock.tick(11)
pygame.quit()