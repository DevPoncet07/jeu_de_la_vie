from tkinter import *
from PIL import Image ,ImageTk
import numpy as np

class CanvasPrincipale(Canvas):
    def __init__(self,boss):
        self.boss=boss
        Canvas.__init__(self,master=boss,width=701,height=701,bg='white',borderwidth=0,highlightthickness=0)
        self.bind("<Button-1>",self.click)
        self.img_final=None

    def click(self,event):
        x=event.x//7
        y=event.y//7
        self.boss.click(x,y)

    def affiche_une_frame(self,frame):
        self.delete(ALL)
        img=Image.fromarray(np.uint8(frame)).convert('RGB')
        self.img_final=ImageTk.PhotoImage(img)
        self.create_image(0,0,anchor="nw",image=self.img_final)
