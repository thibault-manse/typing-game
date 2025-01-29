import pygame
import string
from pygame.locals import *
import random
#import time

pygame.init()

fenetre = pygame.display.set_mode((846, 476))
fond = pygame.image.load("dojo.jpg").convert()#846x476 px
#letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letter = string.ascii_lowercase
fruit= ['abricot', 'banane', 'orange', 'pasteque', 'poire', 'bombe', 'glacon']
clock = pygame.time.Clock() #préréglage FPS
#bombe = pygame.image.load("bombe.png").convert_alpha() #626x626 px
#glace = pygame.image.load("glacon.png").convert_alpha() #281x281 px
point = 0
multiplicateur = 1
vie = 3
data = {} #création bibliotheque
#persoRect = perso.get_rect() #crée un rectangle autour d'une image
#persoRect.topleft = (270,380)#dimension du rectangle
fenetre.blit(fond, (0, 0))#Fond de la fenetre

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
font = pygame.font.SysFont("arialblack", 32) #Police et taille
score_text = font.render('Score : ' + str(point), True, (255, 255, 255))#Affichage des points

def generate_random_fruit(fruit):
    fruit_patch = "fruit/" + fruit + ".png" #tout les fruits mis dans une variable
    letter = string.ascii_lowercase
    data[fruit] = { #Donné des fruits (trajectoire, image...)
        'img': pygame.image.load(fruit_patch),
        'letter' : random.choice(letter),
        'x' : random.randint(100, 500),
        'y' : 500,
        'speed_x' : random.randint(-10, 10),
        'speed_y' : random.randint(-50, -40),
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

def draw_text(fenetre, text, size, x, y): #Fonction d'écriture de texte
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    fenetre.blit(text_surface, text_rect)

def draw_lives(fenetre, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        fenetre.blit(img, img_rect)

def hide_cross_lives(fenetre, x, y):
    fenetre.blit(pygame.image.load('fruit/vie.png'), (x, y))

def show_gameover_screen():
    fenetre.blit(fond, (0, 0))
    draw_text(fenetre, "FRUIT NINJA", 64, 800 / 2, 500 / 4)
    if not game_over:
        draw_text(fenetre, "Score : " + str(point), 40, 800 / 2, 250)

        draw_text(fenetre, "Press a key to begin", 24, 800 / 2, 500 * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

first_round = True
game_over = True
continuer = True

while continuer :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        vie = 3
        draw_lives(fenetre, 690, 5, vie, 'fruit/vie.png')
        point = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
    
    fenetre.blit(fond, (0, 0))
    fenetre.blit(score_text, (0, 0))
    draw_lives(fenetre, 690, 5, vie, 'fruit/vie.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1
            letter = value['letter']

            if value['y'] <= 600:
                fenetre.blit(value['img'], (value['x'], value['y']))
                draw_text(fenetre, letter, 30, value['x'], value['y'])
            else :
                generate_random_fruit(key)

            if event.type == KEYUP:
                tap_letter = event.unicode.lower()
                if not value['hit'] and tap_letter == value['letter']:
                    if key == 'bombe':
                        vie -= 3
                        if vie <= 0:
                            hide_cross_lives(fenetre, 690, 15)
                        elif vie == 1:
                            hide_cross_lives(fenetre, 725, 15)
                        elif vie == 2:
                            hide_cross_lives(fenetre, 760, 15)

                        if vie <= 0:
                            show_gameover_screen()
                            game_over = True
                    
                        #inclure explosion fruit/bombe/glace ici
                        half_fruit_path = "fruit/explosion.png"
                    else:
                        half_fruit_path = "fruit/explosion.png"
                
                    value['img'] = pygame.image.load(half_fruit_path)
                    value['speed_x'] += 10

                    if key != 'bombe' :
                        point += 1
                    score_text = font.render('Score : ' + str(point), True, (255, 255, 255))
                    value['hit'] = True

        else : 
            generate_random_fruit(key)

    pygame.display.update()#mise a jour de l'image a chaque fin de boucle
    clock.tick(13)
pygame.quit()