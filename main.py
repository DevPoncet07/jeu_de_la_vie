import os
from tkinter import Tk
import numpy as np
from PIL import Image

from interface.framepygame import FramePygame
from interface.frame_outils import FrameOutils


class Root(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Game of life")
        self.name = None
        self.img_model_pixel = None
        self.rotation=0
        self.configure(bg='grey30')
        self.size_map = [70, 70]
        self.geometry(str(1+self.size_map[0]*7+250)+"x"+str(1+self.size_map[1]*7+50)+"+0+0")
        self.can=FramePygame(self,self.size_map)
        self.can.grid(row=0,column=0,padx=10,pady=10)

        self.frame_outils=FrameOutils(self)
        self.frame_outils.grid(row=0,column=1,padx=10,pady=10)

        self.all_map=self.cree_array_map(self.size_map)
        self.names_models=self.import_name_models()
        self.frame_outils.remplis_listbox(self.names_models)


    def call_affiche_une_frame(self):
        self.all_map=self.avance_une_frame(self.all_map)
        self.affiche_une_frame()

    def affiche_une_frame(self):
        liste_image = []
        for y in range(self.size_map[1]):
            for x in range(self.size_map[0]):
                if self.all_map[y][x] == 1:
                    liste_image.append([x, y])
        self.can.liste_image = liste_image

    def import_name_models(self):
        list_path=os.listdir("models/")
        names=["aucun"]
        for name in list_path:
            names.append(name[:-4])
        return names

    def sortie_listbox(self,index):
        self.name=self.names_models[index]
        if self.name!="aucun":
            self.img_model_pixel = Image.open("./models/" + str(self.name)+".png")
            self.can.mise_a_jour_model(self.img_model_pixel)
            img_model = self.img_model_pixel.resize((50, 50), resample=0)
            self.frame_outils.mise_a_jour_model(img_model)
        else:
            self.can.mise_a_jour_model(self.name)
            self.frame_outils.mise_a_jour_model(self.name)

    def rotation_right(self):
        self.rotation+=90
        self.img_model_pixel = Image.open("./models/" + str(self.name) + ".png")
        self.img_model_pixel=self.img_model_pixel.rotate(self.rotation,fillcolor=(255,255,255),expand=True)
        self.can.mise_a_jour_model(self.img_model_pixel)
        img_model = self.img_model_pixel.resize((50, 50), resample=0)
        self.frame_outils.mise_a_jour_model(img_model)

    def rotation_left(self):
        self.rotation-=90
        self.img_model_pixel = Image.open("./models/" + str(self.name) + ".png")
        self.img_model_pixel=self.img_model_pixel.rotate(self.rotation,fillcolor=(255,255,255),expand=True)
        self.can.mise_a_jour_model(self.img_model_pixel)
        img_model = self.img_model_pixel.resize((50, 50), resample=0)
        self.frame_outils.mise_a_jour_model(img_model)

    def cree_array_map(self,size):
        return [[0 for _ in range(size[0])] for _ in range(size[1])]

    def click(self,x,y):
        if self.all_map[y][x]==0:
            self.all_map[y][x]=1
            self.can.liste_image.append([x,y])
        else:
            self.all_map[y][x]=0
            del self.can.liste_image[self.can.liste_image.index([x,y])]

    def click_model(self,x,y):
        for ligne in range(self.img_model_pixel.size[1]):
            for colone in range(self.img_model_pixel.size[0]):
                new_x=x+colone
                new_y=y+ligne
                if new_x>=self.size_map[0]:
                    new_x=new_x-self.size_map[0]
                if new_y>=self.size_map[1]:
                    new_y=new_y-self.size_map[1]
                if self.img_model_pixel.getpixel([colone,ligne])==(0,0,0):

                    self.all_map[new_y][new_x]=1
        self.affiche_une_frame()

    def play(self):
        self.call_affiche_une_frame()
        self.can.run=True

    def stop(self):
        self.can.run=False

    def clean(self):
        self.all_map=self.cree_array_map((100,100))
        self.call_affiche_une_frame()


    def avance_une_frame(self,all_map):
        new_map=np.array(all_map)
        x_max=self.size_map[0]-1
        y_max=self.size_map[1]-1
        for y in range(y_max+1):
            for x in range(x_max+1):
                model=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
                index=0
                for e in model:
                    new_x=x+e[0]
                    new_y=y+e[1]
                    if new_x<0:
                        new_x=x_max
                    elif new_x>x_max:
                        new_x=0
                    if new_y<0:
                        new_y=y_max
                    elif new_y>y_max:
                        new_y=0
                    if all_map[new_y][new_x]==1:
                        index+=1
                if all_map[y][x] == 0 and index == 3:
                    new_map[y][x] = 1
                elif all_map[y][x]==1 and (index==2 or index==3):
                    pass
                else:
                    new_map[y][x]=0
        return new_map

if __name__=='__main__':
    root=Root()
    root.can.pygame_loop()
    root.mainloop()