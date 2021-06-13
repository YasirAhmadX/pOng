from tkinter import *
from random import randint
from tkinter import messagebox as msg
import os
import pygame
import csv
import sys
#import numpy as np
sys.stdout = open("exec_log\\stdout.txt",'w')
sys.stderr = open("exec_log\\stderr.txt","w")

def Game(mode):
    print('Its Game mode <',mode,'>')

    if mode == 1:
        collect_data('O')
    elif mode == 3:
        predict_KNN('O')
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
        SCORE = 0

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
        def move_bot(self,position:int):
            """
            Move pad to given position
            """
            self.draw(bg_color)
            self.position = (self.position[0],position)
            self.draw(self.default_color)
                
    class Ball:
        '''
        ball object : prequisite pygame
        '''
        RADIUS = 10
        g_over = False
        
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

        def update(self,pads:list):
            '''
            Update ball position.
                This method paints old ball with bg_color and then draws new ball in new position.
            '''

            self.manage_collisions(pads) #manage collisions and change velociies
            
            self.draw(bg_color)
            self.position = [i+j for i,j in zip(self.position,self.velocity)]
            self.draw(self.color)
        
        def manage_collisions(self,pads:list):
            '''
            this function manages collisions:
            '''
            newcords = [i+j for i,j in zip(self.position,self.velocity)]

            if newcords[1] < self.playground['ymin'] + self.RADIUS or newcords[1] > self.playground['ymax'] - self.RADIUS:
                self.velocity[1] *= -1
                pygame.mixer.Sound.play(plob_sound)

            pad = pads[0]

            if newcords[0] > self.playground['xmax'] - pad.WIDTH - self.RADIUS:
                if newcords[0] > self.playground['xmax'] + self.RADIUS:
                    self.g_over = True
                    pass
                elif abs(newcords[1] - pad.position[1] - self.RADIUS) < pad.HEIGHT//2:
                    self.velocity[0] *= -1
                    self.velocity[0] -= 1 #increase xvelocity
                    pad.SCORE += 100 + abs(newcords[1] - pad.position[1] - self.RADIUS)
                    pygame.mixer.Sound.play(score_sound)
            if mode == 1:
                if newcords[0] < self.playground['xmin'] + self.RADIUS :
                    self.velocity[0] *= -1
                    pygame.mixer.Sound.play(plob_sound)
            else:
                pad = pads[1]
                if newcords[0] < self.playground['xmin'] + pad.WIDTH + self.RADIUS:
                    if newcords[0] < self.playground['xmin'] + self.RADIUS:
                        self.g_over = True
                        pass
                    elif abs(newcords[1] - pad.position[1] - self.RADIUS) < pad.HEIGHT//2:
                        self.velocity[0] *= -1
                        pad.SCORE += 100 + abs(newcords[1] - pad.position[1] - self.RADIUS)
                        pygame.mixer.Sound.play(score_sound)

    pygame.init()

    screen_width,screen_height = pygame.display.get_desktop_sizes()[0]

    border_width = 15
    border_color = pygame.Color('blue')

    bg_color = pygame.Color('black')

    playground = {
        'xmin' : border_width if mode == 1 else 0 , #1border @ left for squash version
        'xmax' : screen_width , #no border on right
        'ymin' : border_width , #1 border on top
        'ymax' : screen_height - border_width #1 border at bottom
    }

    pygame.mixer.init()
    plob_sound = pygame.mixer.Sound("assets\\pong.ogg")
    score_sound = pygame.mixer.Sound("assets\\score.ogg")

    clock = pygame.time.Clock()


    # initializing_objects---
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)

    ball = Ball(screen,playground,(screen_width//2,screen_height//2 - randint(100,300)),(-4,2),"yellow")
    ballpads = [Paddle(screen,playground,(screen_width-7,screen_height//2),"red")]

    if mode == 1:
        ballpads.append(None)
        pass
    else : #elif mode == "vs bot":
        ballpads.append(Paddle(screen,playground,(7,screen_height//2),"red"))
        pass

    borders = ()
    borders += (Border(screen,(0,0),(screen_width,border_width),border_color),)
    if mode == 1:
        borders += (Border(screen,(0,0),(border_width,screen_height),border_color),)
    borders += (Border(screen,(0,screen_height - border_width),(screen_width,border_width),border_color),)

    # draw_playground_area&bjects---

    ball.draw(ball.color)

    for ballpad in ballpads:
        if ballpad:
            ballpad.draw(ballpad.default_color)

    for i in borders:
        i.draw()

    pygame.display.flip()

    # game_loop---

    while True:
        ballpads[0].update_player()
        if ballpads[1]:
            if mode == 2:
                ballpads[1].update_SuperBot(ball)
            elif mode == 3:
                ballpads[1].move_bot(predict_KNN('P',screen_width - ball.position[0],ball.position[1]))
        ball.update(pads=ballpads)
        pygame.display.flip()

        if mode == 1:
            collect_data('D',[ball.position[0],ball.position[1],ball.velocity[0],ball.velocity[1],ballpads[0].position[1]])

        clock.tick(60)

        #gameover handelers
        if  ball.g_over:
            print(f"Score = {ballpads[0].SCORE}")
            font = pygame.font.SysFont("verdana", 72)
            if ball.position[0] < screen_width:
                msg = "Congratulations you won!"
                
            else:
                if mode == 3:
                    msg = "Your bot defeted you :)"
                msg = "Game Over !!!"
            print(msg)
            text = font.render(msg, True, (255, 0, 0))
            font2 = pygame.font.SysFont("verdana", 20)
            text2 = font2.render("SCORE = "+str(ballpads[0].SCORE), True, (255, 255, 255))
            screen.blit(text,((screen_width - text.get_width())//2, (screen_height - text.get_height())//2))
            screen.blit(text2,((screen_width - text2.get_width())//2, (screen_height + 2*text.get_height() - text2.get_height())//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            if mode == 1:
                collect_data('C')
            return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    print(f"<Button Pressed>  K_ESCAPE")
                    pygame.quit()
                    if mode == 1:
                        collect_data('C')

                    return

def MainFrame():
    global window
    global c
    window  =  Tk()
    window.title('pOng')
    window.attributes("-fullscreen",True)
    p = PhotoImage(file = "assets\\logo.png")
    window.iconphoto(False, p)
    window.configure(bg = '#04002e')
    L0 = Label(window,text = 'pOng ',font = ('Times New Roman',100,'bold'),bg = '#04002e',fg = '#ff0000')
    L0.pack(side = TOP,fill = 'x')
    L0.bind('<Enter>',lambda x : L0.configure(fg = '#ffff00'))
    L0.bind('<Leave>',lambda x : L0.configure(fg = '#ff0000'))
    nf = Frame(window,bg = '#04002e')
    nf.pack(side = BOTTOM,fill = 'x')
    L1 = Label(nf,text = 'By Yasir Ahmad\n[ EccentricX ]',font = ('Courier',8,'normal'),bg = '#04002e',fg = '#ffffff')
    L1.pack(side = RIGHT)
    L1.bind('<Enter>',lambda x : L1.configure(fg = '#ff0000'))
    L1.bind('<Leave>',lambda x : L1.configure(fg = '#ffffff'))
    Menu()

def ButtonGraphics(B,details):
    print(details)
    f = B['font'].split(' ')
    r = B['relief']
    if r == 'flat':
        r = RAISED
        f[2] = 'bold'
        B['fg'] = "#ffff00"
    elif r == 'raised':
        r = FLAT
        f[2] = 'normal'
        B['fg'] = "#ff0000"
    f = ' '.join(f)
    B.configure(font = f,relief = r)

def Menu():

    def PlayBot():
        print('<Button Pressed> ',B0['text'])
        Game(3)
        pass
    def PlaySuperBot():
        print('<Button Pressed> ',B1['text'])
        Game(2)
        pass
    def PlaySquash():
        print('<Button Pressed>',B2['text'])
        Game(1)
        pass
    def Help():
        print('<Button Pressed>',B3['text'])
        os.system("assets\\help.txt")
        pass
    def exit():
        print('<Button Pressed>',B4['text'])
        try:
            pygame.quit()
            sys.stdout.close()
            sys.stderr.close()
            
        except:
            pass
        finally:
            window.destroy()


    menuframe = Frame(window,bg = '#04002e')
    menuframe.pack(fill  =  'x')

    L0 = Label(menuframe,text = 'MENU',font = ('Verdana',40),bg = '#04002e',fg = "#ffff00")

    B0 = Button(menuframe,text = 'Play against Yourself',command = PlayBot,width = 30,font = ('Verdana',12,'normal'),activebackground = '#04002e',activeforeground = '#696969',bg = '#000020',fg = '#ff0000',relief = FLAT)
    B1 = Button(menuframe,text = 'Play against SuperBot',command = PlaySuperBot,width = 30,font = ('Verdana',12,'normal'),bg = '#000020',activebackground = '#04002e',activeforeground = '#696969',fg = '#ff0000',relief = FLAT)
    B2 = Button(menuframe,text = 'Play sQuash pOng',command = PlaySquash,width = 30,font = ('Verdana',12,'normal'),bg = '#000020',activebackground = '#04002e',activeforeground = '#696969',fg = '#ff0000',relief = FLAT)
    B3 = Button(menuframe,text = 'Help',command = Help,width = 30,font = ('Verdana',12,'normal'),bg = '#000020',activebackground = '#04002e',activeforeground = '#696969',fg = '#ff0000',relief = FLAT)
    B4 = Button(menuframe,text = 'Exit',command = exit,width = 30,font = ('Verdana',12,'normal'),bg = '#000020',activebackground = '#04002e',activeforeground = '#696969',fg = '#ff0000',relief = FLAT)

    L0.pack(pady = 10)
    B0.pack(pady = 2,ipady = 7)
    B1.pack(pady = 2,ipady = 7)
    B2.pack(pady = 2,ipady = 7)
    B3.pack(pady = 2,ipady = 7)
    B4.pack(pady = 2,ipady = 7)


    B0.bind('<Enter>',lambda x: ButtonGraphics(B0,x))
    B1.bind('<Enter>',lambda x: ButtonGraphics(B1,x))
    B2.bind('<Enter>',lambda x: ButtonGraphics(B2,x))
    B3.bind('<Enter>',lambda x: ButtonGraphics(B3,x))
    B4.bind('<Enter>',lambda x: ButtonGraphics(B4,x))


    B0.bind('<Leave>',lambda x: ButtonGraphics(B0,x))
    B1.bind('<Leave>',lambda x: ButtonGraphics(B1,x))
    B2.bind('<Leave>',lambda x: ButtonGraphics(B2,x))
    B3.bind('<Leave>',lambda x: ButtonGraphics(B3,x))
    B4.bind('<Leave>',lambda x: ButtonGraphics(B4,x))

    window.mainloop()

data = None

def predict_KNN(cmd,x=None,y=None):
    def euclideanDistance(a,b,c,d):
        return ((a-c)**2 + (b-d)**2)**0.5
    global data
    print("<predict_KNN called> ",cmd)
    if cmd == 'O':
        if os.path.exists("data\\gameData.csv"):
            f = open("data\\gameData.csv","r")
            data = csv.reader(f)
            data = [i for i in data]
            f.close()
        else:
            msg.showerror("pOng","No data available to train the bot, play Squash Pong to train the bot.")
            f.close() #to cause an exception
    elif cmd == 'P':
        l = []
        for points in data:
            if points[1].isdigit():
                l.append(euclideanDistance(int(points[0]),int(points[1]),x,y))
        return int(data[l.index(min(l))+1][4])

def collect_data(cmd,inpt=None):
    global data
    print("<collect_data called> ",cmd)
    if cmd == 'O':
        if os.path.exists("data\\gameData.csv"):
            data = open("data\\gameData.csv","a")
        else:
            data = open("data\\gameData.csv","w")
            print("x,y,vx,vy,paddle.y",file = data)
    elif cmd == 'D':
        print(*inpt,sep=',',file = data)
    else:
        data.close()

MainFrame()