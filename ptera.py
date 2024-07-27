import pygame
import random
import globais as gl

"""
pterodactilo
"""
class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1, primeiroPtera = 0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = gl.load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [gl.height*0.90,gl.height*0.75,gl.height*0.60]
        if(primeiroPtera == 0):
            self.rect.centery = self.ptera_height[2]
        elif(primeiroPtera == 1):
            self.rect.centery = self.ptera_height[1]
        else:
            self.rect.centery = self.ptera_height[random.randrange(0,3)]

        self.rect.left = gl.width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        gl.screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter +1)
        if self.rect.right < 0:
            self.kill()
