import pygame
import random
from pygame import *
from aprendizado import aprendizado
from ptera import Ptera
from dino import Dino
from cactus import Cactus
from chao import Ground
from nuvens import Cloud
from score import ScoreBoard
import globais as gl
import matplotlib.pyplot as plt

"""
primeira tela
"""
def screen():
    temps_dino = []
    i = 0
    while(i < gl.quantDinos):
        temps_dino.append(Dino(44,47))
        temps_dino[i].isBlinking = True
        i+=1
    gameStart = False

    temp_ground,temp_ground_rect = gl.load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect_left = gl.width/20
    temp_ground_rect.bottom = gl.height

    for temp_dino in temps_dino:
        temp_dino.isJumping = True
        temp_dino.isBlinking = False
        temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

    if pygame.display.get_surface() != None:
        gl.screen.fill(gl.background_col)
        gl.screen.blit(temp_ground[0],temp_ground_rect)
        for temp_dino in temps_dino:
            temp_dino.draw()

        pygame.display.update()

    gl.clock.tick(gl.FPS)
    gameStart = True



def plotaGrafico():
    arquivo = open("resultados.txt", "r")
    x = []
    y = []
    for linhas in arquivo:
        if(linhas != '\n'):
            lista = list(map(int, linhas.split(" - ")))
            plt.plot(lista[0], lista[1], "o", color = 'r')
            x.append(lista[0])
            y.append(lista[1])
    plt.title("Score de cada geração")
    plt.xlabel("Geração")
    plt.ylabel("Score")
    plt.plot(x, y, color = 'b')
    plt.xlim(max(x), min(x))
    plt.show()
    arquivo.close()

"""
regras do jogo
"""
def gameplay(mortos = [], old_ground = 0, temp_imagesOld = 0, temp_rectOld = 0, controle = 0):
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    i = 0
    primeiroPtera = 0

    playersDino = []

    if mortos == []:
        controle = aprendizado()
        print("Tamanho da população:", gl.quantDinos)
        while(i < gl.quantDinos):
            playersDino.append(Dino(44,47))
            i+=1
    else:
        filho, aleatoriedade = controle.crossover(mortos)

        print("Tamanho da população: ", len(mortos))
        print("Aleatoriedade: ", aleatoriedade)
        print("Vitorias:", controle.vitorias)


        while(i < len(mortos) - 3):
            playersDino.append(mortos[i])
            playersDino[i].ressucitar()

            playersDino[i] = controle.mutacao(playersDino[i], filho)
            i+=1

        mortos[len(mortos) - 1].ressucitar()
        mortos[len(mortos) - 2].ressucitar()
        playersDino.append(mortos[len(mortos) - 1])
        playersDino.append(mortos[len(mortos) - 2])

    mortos = []
    if(old_ground != 0):
        new_ground = old_ground
        new_ground.speed = -4
    else:
        new_ground = Ground(-1*gamespeed)

    scb = ScoreBoard()
    highsc = ScoreBoard(gl.width*0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbuttom_image,retbuttom_rect = gl.load_image('replay_button.png',35,31,-1)
    gameover_image,gameover_rect = gl.load_image('game_over.png',190,11,-1)

    if(temp_imagesOld == 0):
        temp_images,temp_rect = gl.load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    else:
        temp_images,temp_rect = temp_imagesOld,temp_rectOld
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(gl.background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = gl.height*0.1
    HI_rect.left = gl.width*0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                haObstaculo = 1

                if(len(cacti.sprites()) != 0 and len(pteras) != 0):
                    if (cacti.sprites()[0].rect[0] < pteras.sprites()[0].rect[0]) and cacti.sprites()[0].rect[0]  > 10:
                        distancia = cacti.sprites()[0].rect[0]
                        altura = cacti.sprites()[0].rect[1]
                        larguraObj = 40
                    elif(pteras.sprites()[0].rect[0]  > 10):
                        distancia = pteras.sprites()[0].rect[0]
                        altura = pteras.sprites()[0].rect.centery
                        larguraObj = 46
                    else:
                        haObstaculo = 0
                elif(len(cacti.sprites()) != 0 and cacti.sprites()[0].rect[0] > 10):
                    distancia = cacti.sprites()[0].rect[0]
                    altura = cacti.sprites()[0].rect[1]
                    larguraObj = 40
                elif(len(pteras) != 0 and pteras.sprites()[0].rect[0] > 10):
                    distancia = pteras.sprites()[0].rect[0]
                    altura = pteras.sprites()[0].rect.centery
                    larguraObj = 46
                else:
                    haObstaculo = 0

                if(haObstaculo == 1):
                    for playerDino in playersDino:

                        if controle.controlaDino(playerDino, distancia, altura, gamespeed, playerDino.movement[1], larguraObj) == 1:

                            if playerDino.rect.bottom == int(0.98*gl.height):
                                playerDino.isJumping = True

                                if pygame.mixer.get_init() != None:
                                    gl.jump_sound.play()
                                playerDino.movement[1] = -1*playerDino.jumpSpeed

                        if controle.controlaDino(playerDino, distancia, altura, gamespeed, playerDino.movement[1], larguraObj) == 0:
                            playerDino.isJuping = False
                            playerDino.movement[1] = 0.8*playerDino.jumpSpeed
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True


                        if controle.controlaDino(playerDino, distancia, altura, gamespeed, playerDino.movement[1], larguraObj) != 0:
                            playerDino.isDucking = False
            for c in cacti:
                c.movement[0] = -1*gamespeed
                for playerDino in playersDino:
                    if pygame.sprite.collide_mask(playerDino,c):
                        playerDino.isDead = True
                        if pygame.mixer.get_init() != None:
                            gl.die_sound.play()

            for p in pteras:
                p.movement[0] = -1*gamespeed
                for playerDino in playersDino:
                    if pygame.sprite.collide_mask(playerDino,p):
                        playerDino.isDead = True
                        if pygame.mixer.get_init() != None:
                            gl.die_sound.play()

            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < gl.width*0.7 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            elif len(pteras) == 0 and random.randrange(0,60) == 10:
                for l in last_obstacle:
                    if l.rect.right < gl.width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40, primeiroPtera))
                        primeiroPtera += 1

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(gl.width,random.randrange(gl.height/5,gl.height/2))

            for playerDino in playersDino:
                playerDino.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            for playerDino in playersDino:
                scb.update(playerDino.score)
            highsc.update(gl.high_score)

            if pygame.display.get_surface() != None:
                gl.screen.fill(gl.background_col)
                new_ground.draw()
                clouds.draw(gl.screen)
                scb.draw()
                if gl.high_score != 0:
                    highsc.draw()
                    gl.screen.blit(HI_image,HI_rect)
                cacti.draw(gl.screen)
                pteras.draw(gl.screen)
                for playerDino in playersDino:
                    playerDino.draw()

                pygame.display.update()
            gl.clock.tick(gl.FPS)

            l = 0
            while l < len(playersDino):
                if playersDino[l].isDead:
                    mortos.append(playersDino[l])
                    if playersDino[l].score > gl.high_score:
                        gl.high_score = playersDino[l].score
                    playersDino.remove(playersDino[l])

                else:
                    l+=1

            if(playersDino == []):
                gameOver = True
            if counter%700 == 699 and counter < 7000:
                new_ground.speed -=1
                gamespeed += 1

            flag = 0
            for playerDino in playersDino:
                if(playerDino.score > 2000):
                    playerDino.isDead = True
                    gameOver = True
                    mortos.append(playerDino)
                    playersDino.remove(playerDino)

                    if(controle.vitorias < 5):
                        if(flag == 0):
                            controle.vitorias += 1
                            flag = 1

                        if playerDino.score > gl.high_score:
                            gl.high_score = playerDino.score
                    else:
                        arquivo = open("melhorDino.txt", "w")
                        arquivo.write(str(playerDino.cromossomos))
                        arquivo.close()
                        print("Fim do jogo.")
                        plotaGrafico()
                        exit(1)

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            gameQuit = False
            gameplay(mortos = mortos, old_ground = new_ground, temp_imagesOld = temp_images, temp_rectOld = temp_rect, controle = controle)

    pygame.quit()
    quit()


def main():
    arquivo = open('resultados.txt', "w")
    arquivo.close()


    isGameQuit = screen()
    if not isGameQuit:
        gameplay()

main()
