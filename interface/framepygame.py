import os
from tkinter import Frame
import pygame
import time


class FramePygame(Frame):
    def __init__(self,boss,size_map):
        self.boss=boss
        self.size_map=size_map
        Frame.__init__(self,master=boss,width=1+7*size_map[0],height=1+7*size_map[1])
        self.bind('<Button-1>',self.click)
        self.bind('<ButtonRelease-1>',self.unclick)
        self.bind('<Motion>',self.motion)
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.liste_image=[]
        self.onclick=False
        self.last_case=[-1,-1]
        self.motion_coord=[size_map[0]*7+10,size_map[1]*7+10]
        self.run=False
        self.model_focus=None

    def click(self,event):
        self.onclick = True
        x =( event.x-1) // 7
        y = (event.y-1) // 7
        self.last_case = [x, y]
        if not self.model_focus:
            self.boss.click(x,y)
        else:
            self.boss.click_model(x,y)

    def unclick(self,event):
        self.onclick=False

    def motion(self,event):
        if not self.model_focus:
            if self.onclick:
                x=(event.x-1)//7
                y=(event.y-1)//7
                if 0<=x<=self.size_map[0]-1 and 0<=y<=self.size_map[1]-1:
                    if [x,y]==self.last_case:
                        pass
                    else:
                        self.boss.click(x,y)
                        self.last_case=[x,y]
        else:
            x = event.x-1
            y = event.y-1
            self.motion_coord=[x,y]

    def pygame_loop(self):
        if self.run:
            self.boss.call_affiche_une_frame()
        chrono1=time.time()
        self.screen.fill((255, 255, 255))
        for e in self.liste_image:
            pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(1+e[0]*7,1+e[1]*7,6,6))
        if self.model_focus:
            self.affiche_model()
        pygame.display.flip()
        chrono2=time.time()
        self.boss.after(10, self.pygame_loop)

    def affiche_model(self):
        x,y=self.motion_coord[0]//7,self.motion_coord[1]//7
        for ligne in range(self.model_focus.size[1]):
            for colone in range(self.model_focus.size[0]):
                if self.model_focus.getpixel([colone,ligne]) ==(0,0,0):
                    new_x=x+colone
                    new_y=y+ligne
                    if new_x>=self.size_map[0]:
                        new_x=new_x-self.size_map[0]
                    if new_y>=self.size_map[1]:
                        new_y=new_y-self.size_map[1]

                    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(1 + new_x* 7, 1 + new_y * 7, 6, 6))

    def mise_a_jour_model(self, img_model):
        if img_model!='aucun':
            self.model_focus=img_model
        else:
            self.model_focus=None