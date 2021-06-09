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
VELOCITY = 1

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
        else:
            self.show(bgColor) #hide old ball in bgcolor
            self.x += self.vx
            self.y += self.vy
            self.show(fgColor) #draw new ball in new position


#initialize_objects------
ballplay = Ball(WIDTH-Ball.RADIUS,HEIGHT//2,-VELOCITY,VELOCITY)
#content-------

#drawing screen
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(WIDTH,BORDER)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(BORDER,HEIGHT)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,HEIGHT-BORDER),(WIDTH,BORDER)))
ballplay.show(fgColor)
#pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect((WIDTH-BORDER,0),(WIDTH,HEIGHT)))

pygame.display.flip()

while True: #game_loop
    
    ballplay.update()
    pygame.display.flip()

    e = pygame.event.poll()
    if e.type==pygame.QUIT: #quit if user clikcs 'X'
        break

pygame.quit()
