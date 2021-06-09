'''
MY Implementation of classic game 'PONG' using python/pygame and OOP paradigm !
'''
#Squash Version.

# libraries---
import pygame

# variables---
screen_width = 1200
screen_height = 600

border_width = 15
border_color = pygame.Color('blue')

playground = {
    'xmin' : border_width , #1border @ left
    'xmax' : screen_width , #no border on right
    'ymin' : border_width , #1 border on top
    'ymax' : screen_height - border_width #1 border at bottom
}

bg_color = pygame.Color('black')

pygame.mixer.init()
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# objects---
class Border:
    """
    border object : prequisite pygame
    """

    def __init__(self,surface:pygame.Surface,position:tuple,dimensions:tuple,color:str):
        self.position = position
        self.dimensions = dimensions
        self.color = color
        self.screen = surface
  
    def draw(self):
        pygame.draw.rect(self.screen,self.color,pygame.Rect(self.position,self.dimensions))

class Paddle:
    '''
    Paddle object : prequisite pygame
    '''
    WIDTH = 15
    HEIGHT  = 100

    def __init__(self,surface:pygame.Surface,playground_coordinates:dict,position:tuple,color:str):
        self.position = position
        self.default_color = pygame.Color(color)
        self.screen = surface
        self.playground = playground_coordinates
        
    def draw(self,color:str):
        '''
        Draw the paddle.
        '''
        pygame.draw.rect(self.screen,color,pygame.Rect((self.position[0] - self.WIDTH//2,self.position[1] - self.HEIGHT//2),(self.WIDTH,self.HEIGHT)))

    def update_player(self):
        '''
        Update paddle position based on y-coordinate of the mouse.
            This method paints old paddle with bg_color and then draws new paddle based on y-coordinate of mouse.
        '''
        mouse_position = pygame.mouse.get_pos()[1]

        if self.playground['ymin'] + self.HEIGHT//2 < mouse_position < self.playground['ymax'] - self.HEIGHT//2:
            self.draw(bg_color)
            self.position = (self.position[0],mouse_position)
            self.draw(self.default_color)
    def update_SuperBot(self,ball):
        '''
        Update paddle position based on y-coordinate of the ball
        '''
        if self.playground['ymin'] + self.HEIGHT//2 < ball.position[1] < self.playground['ymax'] - self.HEIGHT//2:
            self.draw(bg_color)
            self.position = (self.position[0],ball.position[1])
            self.draw(self.default_color)
            

class Ball:
    '''
    ball object : prequisite pygame
    '''
    RADIUS = 10
    def __init__(self,surface:pygame.Surface,plaground:dict,pos:tuple,velocity:tuple,color:str):
        self.screen = surface
        self.playground = playground
        self.position = list(pos)
        self.velocity = list(velocity)
        self.color = pygame.Color(color)
        
    def draw(self,color:str):
        '''
        Draw the ball.
        '''
        pygame.draw.circle(self.screen,color,self.position,self.RADIUS)

    def update(self,pad:Paddle):
        '''
        Update ball position.
            This method paints old ball with bg_color and then draws new ball in new position.
        '''

        self.manage_collisions(pad) #manage collisions and change velociies
        
        self.draw(bg_color)
        self.position = [i+j for i,j in zip(self.position,self.velocity)]
        self.draw(self.color)
    
    def manage_collisions(self,pad:Paddle):
        newcords = [i+j for i,j in zip(self.position,self.velocity)]

        if newcords[1] < self.playground['ymin'] + self.RADIUS or newcords[1] > self.playground['ymax'] - self.RADIUS:
            self.velocity[1] *= -1
            pygame.mixer.Sound.play(plob_sound)
        if newcords[0] < self.playground['xmin'] + self.RADIUS :
            self.velocity[0] *= -1
            pygame.mixer.Sound.play(plob_sound)
        if newcords[0] > self.playground['xmax'] - pad.WIDTH - self.RADIUS:
            if newcords[0] > self.playground['xmax'] + self.RADIUS:
                pygame.quit()
                print('Game Over')
            elif abs(newcords[1] - pad.position[1] - self.RADIUS) < pad.HEIGHT//2:
                self.velocity[0] *= -1
                pygame.mixer.Sound.play(score_sound)


# initializing_objects---
screen = pygame.display.set_mode((screen_width, screen_height))

ball = Ball(screen,playground,(screen_width-100,screen_height//2),(-1,1),'yellow')
ballpad = Paddle(screen,playground,(screen_width-7,screen_height//2),"red")

borders = ()
borders += (Border(screen,(0,0),(screen_width,border_width),border_color),)
borders += (Border(screen,(0,0),(border_width,screen_height),border_color),)
borders += (Border(screen,(0,screen_height - border_width),(screen_width,border_width),border_color),)

# draw_playground_area&bjects---

ball.draw(ball.color)
ballpad.draw(ballpad.default_color)

for i in borders:
    i.draw()


pygame.display.flip()

# game_loop---
while True:
    ballpad.update_player()
    ball.update(pad=ballpad)
    pygame.display.flip()

    e = pygame.event.poll()
    if e.type == pygame.QUIT :
        break

    #print(pygame.event.get())

pygame.quit()
