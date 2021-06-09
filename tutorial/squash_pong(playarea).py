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
fgColor = pygame.Color("blue")

#content-------

#drawing screen
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(WIDTH,BORDER)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,0),(BORDER,HEIGHT)))
pygame.draw.rect(screen,fgColor,pygame.Rect((0,HEIGHT-BORDER),(WIDTH,BORDER)))

#pygame.draw.rect(screen,pygame.Color('red'),pygame.Rect((WIDTH-BORDER,0),(WIDTH,HEIGHT)))

pygame.display.flip()

while True: #game_loop
    e = pygame.event.poll()
    if e.type==pygame.QUIT: #quit if user clikcs 'X'
        break

pygame.quit()
