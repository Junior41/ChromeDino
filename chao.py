import globais as gl

"""
chão
"""
class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = gl.load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = gl.load_image('ground.png',-1,-1,-1)
        self.rect.bottom = gl.height
        self.rect1.bottom = gl.height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        gl.screen.blit(self.image,self.rect)
        gl.screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
