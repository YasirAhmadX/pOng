'''
Implementation of classic game 'PONG' using python/pygame and OOP paradigm ! 
@author: Isaac Triguero and Thorsten Altenkirch
<Computerphile/>
'''
import pygame

#variables-------
WIDTH = 1200 #width of window
HEIGHT = 600 #height of window
BORDER = 20 #thickness of the border of walls
bgColor = pygame.Color("black")
fgColor = pygame.Color("white")
VELOCITY = 3
FRAMERATE = 100

#define_objects-------
class Ball:

    RADIUS = 10 #radius of every ball object

    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self,color):
        global screen
        pygame.draw.circle(screen,color,(self.x,self.y),self.RADIUS)
    
    def update(self):
        global bgColor, fgColor
        newx = self.x + self.vx
        newy = self.y + self.vy

        if newx< BORDER + self.RADIUS:
            self.vx = -self.vx
        elif newy< BORDER + self.RADIUS or newy> HEIGHT - BORDER - self.RADIUS:
            self.vy = -self.vy
        elif newx + Ball.RADIUS > WIDTH - Paddle.WIDTH and abs(newy - paddleplay.y) < Paddle.HEIGHT//2:
            self.vx = -self.vx
        else:
            self.show(bgColor) #hide old ball in bgcolor
            self.x += self.vx
            self.y += self.vy
            self.show(fgColor) #draw new ball in new position

class Paddle:
    WIDTH = 20
    HEIGHT = 100

    def __init__(self,y):
        self.y = y

    def show(self,color):
        global screen
        pygame.draw.rect(screen,color,pygame.Rect((WIDTH - self.WIDTH, self.y - self.HEIGHT//2),(self.WIDTH,self.HEIGHT)))
    
    def update(self):
        self.show(bgColor)
        self.y = pygame.mouse.get_pos()[1]
        if self.y < BORDER + self.HEIGHT//2 :
            self.y = BORDER + self.HEIGHT//2
        elif self.y > HEIGHT - self.HEIGHT//2 - BORDER:
            self.y = HEIGHT - self.HEIGHT//2 - BORDER
        self.show(fgColor)

#initialize_objects------
ballplay = Ball(WIDTH-Ball.RADIUS-100,HEIGHT//2,-VELOCITY,VELOCITY)
paddleplay = Paddle(HEIGHT//2)
#content-------

#drawing screen
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(WIDTH,BORDER)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(BORDER,HEIGHT)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,HEIGHT-BORDER),(WIDTH,BORDER)))
ballplay.show(fgColor)
paddleplay.show(fgColor)
#pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect((WIDTH-BORDER,0),(BORDER,HEIGHT)))

pygame.display.flip()

clock = pygame.time.Clock()

while True: #game_loop
    clock.tick(FRAMERATE) #to control the framerate of the game
    
    ballplay.update()
    paddleplay.update()
    pygame.display.flip()

    e = pygame.event.poll()
    if e.type==pygame.QUIT: #quit if user clikcs 'X'
        break

pygame.quit()
