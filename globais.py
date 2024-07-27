import os
import pygame
from pygame import *
import time
"""
instancia dos padrões pygame dos elementos da tela e audio
"""

pygame.init()

scr_size = (width, height) = (800,250) #tamanho da tela
FPS = 60
gravity = 0.6
quantDinos = 200
quantcromossomos = 70

black = (0,0,0)
white = (255,228,196) #255
background_col = (255,228,196) #235

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("CrisDino Game ")

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')

"""
funções para carregamento de imagens de sprite
"""

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    i = 1
    while(i == 1):
        try:
            image = pygame.image.load(fullname)
            image = image.convert()
            i = 0
        except:
            i = 1

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    i = 1
    while(i == 1):
        try:
            fullname = os.path.join('sprites',sheetname)
            sheet = pygame.image.load(fullname)
            i = 0
        except:
            time.sleep(0.2)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex, i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect
"""
função gameover
"""
def disp_gameOver_msg(retbutton_image, gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = int(width / 2)
    retbutton_rect.top = int(height*0.52)

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = int(width/2)
    gameover_rect.centery = int(height*0.35)

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

"""
Função dos números para futuro score
"""
def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

