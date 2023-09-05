#NOTE importing modules
import pygame as pg
import sys,time,random
from player import Player
from enemy import Enemy

#NOTE initializing pygame 
pg.init()
 
#NOTE Main Game Class
class Game:
    def __init__(self):

        #define game properties
        self.screenWidth=400
        self.screenHeight=800
        self.win=pg.display.set_mode((self.screenWidth,self.screenHeight))
        self.clock=pg.time.Clock()
        self.targetFps=60
        self.isGameOver=False
        self.score=0

        #Creating road
        self.road1=pg.image.load("assets/ROAD2.jpg").convert_alpha()
        self.road1Rect=self.road1.get_rect()
        self.road2=pg.image.load("assets/ROAD2.jpg").convert_alpha()
        self.road2Rect=self.road2.get_rect()
        self.road1Rect.x=0
        self.road1Rect.y=0
        self.road2Rect.bottom=0
        self.road2Rect.x=0
        self.roadSpeed=10

        #creating Player
        self.player=Player()

        #Loading and creating list of enemies
        self.enemyImages=[]
        for i in range(1,5):
            img=pg.image.load(f"assets/car_{i}.png").convert_alpha()
            img=pg.transform.rotate(img,180)
            img=pg.transform.scale(img,(50,100))
            self.enemyImages.append(img)
        
        #creating enemy group
        self.enemyGroup=pg.sprite.Group()
        
        #generating starting enemies
        self.generateEnemies(4,0)
        
        #Loading and creating fonts/texts
        self.font = pg.font.Font('ARIAL.TTF', 30)
        self.scoreText = self.font.render('Score:0', True, (0,0,0), (255,255,53))
        self.scoreTextRect = self.scoreText.get_rect()
        self.scoreTextRect.x=10
        self.scoreTextRect.y=10

        self.font2 = pg.font.Font('ARIAL.TTF', 48)
        self.gameOverText = self.font2.render('Game Over', True, (255,0,0), (255,255,255))
        self.gameOverTextRect = self.gameOverText.get_rect()
        self.gameOverTextRect.center=(self.screenWidth//2,self.screenHeight//2)

        #starting the game loop
        self.gameLoop()

    #NOTE updates the score and score text
    def updateScore(self):
        self.score+=1
        self.scoreText = self.font.render(f'Score: {self.score}', True, (0,0,0), (255,255,53))

    #NOTE changes the game state
    def gameOver(self):
        self.isGameOver=True

    #NOTE main game loop
    def gameLoop(self):
        old_time=time.time()
        count=0
        while True:
            #calculating delta time
            new_time=time.time()
            dt=new_time-old_time
            old_time=new_time

            #Event Loop
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            #Processing everything if the game is not over
            if self.isGameOver==False:
                #moving roads
                self.road1Rect.y+=int(self.roadSpeed*dt*self.targetFps)
                self.road2Rect.y+=int(self.roadSpeed*dt*self.targetFps)

                #moving players and enemies
                self.player.update(dt)
                self.enemyGroup.update(dt)

                #generating new enemies after the count of 50
                if count==50:
                    lastXPos=random.randint(0,270)
                    self.generateEnemies(1,lastXPos)
                    count=0
                else:
                    count+=1

                #checking the collisions
                self.checkCollisions()

                #resetting the road image position
                if self.road1Rect.y>=800:
                    self.road1Rect.bottom=0
                if self.road2Rect.y>=800:
                    self.road2Rect.bottom=0

            #displaying everything on the screen
            self.win.blit(self.road1,self.road1Rect)
            self.win.blit(self.road2,self.road2Rect)
            self.win.blit(self.player.image,self.player.rect)
            self.enemyGroup.draw(self.win)
            self.win.blit(self.scoreText,self.scoreTextRect)
        
            if self.isGameOver==True:
                self.win.blit(self.gameOverText,self.gameOverTextRect)
            
            #updating the screen
            pg.display.update()
            
            #limiting the FPS
            self.clock.tick(60)

    #NOTE checks collision of enemies and player
    def checkCollisions(self):

        #check to bound the player inside the screen
        if self.player.rect.x<=0:
            self.player.rect.x=0
        if self.player.rect.right>=self.screenWidth:
            self.player.rect.right=self.screenWidth
        if self.player.rect.y<=0:
            self.player.rect.y=0
        if self.player.rect.bottom>=self.screenHeight:
            self.player.rect.bottom=self.screenHeight

        #checking for game over and update score
        for enemy in self.enemyGroup:  
            if enemy.rect.colliderect(self.player.rect):
                self.gameOver() 
                break
            if enemy.rect.y>=self.screenHeight:
                enemy.kill()
                del enemy
                self.updateScore()
            
    #NOTE generates enemies according to the count and last x position
    def generateEnemies(self,count,lastXPos):
        for i in range(0,count):
            xpos=random.randint(lastXPos+30,lastXPos+90)
            ypos=-random.randint(80,200)
            enemy=Enemy(self.enemyImages,xpos,ypos)
            self.enemyGroup.add(enemy)
            lastXPos=xpos+40

            
#NOTE Creating game object
gameObj=Game()
