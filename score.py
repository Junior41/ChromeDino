import globais as gl
import pygame
"""
score
"""
class ScoreBoard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.tempimages,self.temprect = gl.load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = gl.width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = gl.height*0.1
        else:
            self.rect.top = y

    def draw(self):
        gl.screen.blit(self.image,self.rect)

    def update(self,score):
        score_digits = gl.extractDigits(score)
        self.image.fill(gl.background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0