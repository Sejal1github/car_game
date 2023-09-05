import pygame as pg

#NOTE Player Class
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Defining the properties
        self.image=pg.image.load("assets/player.png").convert_alpha()
        self.image=pg.transform.scale(self.image,(40,80))
        self.rect=self.image.get_rect()
        self.rect.y=700
        self.speed=3
        
    #NOTE moving player when key presses
    def update(self,dt):
        key=pg.key.get_pressed()

        if key[pg.K_UP]:
            self.rect.y-=self.speed*dt*60
        elif key[pg.K_DOWN]:
            self.rect.y+=self.speed*dt*60
        elif key[pg.K_RIGHT]:
            self.rect.x+=self.speed*dt*60
        elif key[pg.K_LEFT]:
            self.rect.x-=self.speed*dt*60