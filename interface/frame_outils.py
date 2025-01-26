from tkinter import *
from PIL import Image,ImageTk

class FrameOutils(Frame):
    def __init__(self,boss):
        self.boss=boss
        Frame.__init__(self,master=boss,bg='grey30')
        self.img_can=None
        self.boutton_plus_un=Button(self,text="Avance une frame",command=self.avance_une_frame)
        self.boutton_plus_un.grid(row=0,column=0)
        self.boutton_play=Button(self, text="Play", command=self.play)
        self.boutton_play.grid(row=1, column=0,pady=20)
        self.boutton_stop=Button(self, text="Stop", command=self.stop)
        self.boutton_stop.grid(row=2, column=0)
        self.boutton_clean = Button(self, text="Clean", command=self.boss.clean)
        self.boutton_clean.grid(row=3, column=0,pady=20)

        self.frame_model=Frame(self,bg='grey30')
        self.listbox=Listbox(self.frame_model,width=20,height=10)
        self.listbox.grid(row=0,column=0,rowspan=3)
        self.listbox.bind("<ButtonRelease-1>",self.sortie_listbox)
        self.boutton_rotation_right=Button(self.frame_model,text='⟳',command=self.boss.rotation_right)
        self.boutton_rotation_right.grid(row=0,column=1)
        self.boutton_rotation_left=Button(self.frame_model,text='↻',command=self.boss.rotation_left)
        self.boutton_rotation_left.grid(row=2,column=1)
        self.can=Canvas(self.frame_model,width=50,height=50,bg='white')
        self.can.grid(row=1,column=1,pady=20,padx=20)
        self.frame_model.grid(row=4,column=0)



    def remplis_listbox(self,liste):
        self.listbox.delete('end',0)
        for e in liste:
            self.listbox.insert('end',e)

    def sortie_listbox(self,event):
        index=self.listbox.curselection()
        self.boss.sortie_listbox(index[0])

    def mise_a_jour_model(self,name):
        self.can.delete(ALL)
        if name!="aucun":
            self.img_can=ImageTk.PhotoImage(name)
            self.can.create_image(1,1,anchor='nw',image=self.img_can)

    def avance_une_frame(self):
        self.boss.call_affiche_une_frame()

    def play(self):
        self.boutton_play['state']='disabled'
        self.boutton_plus_un['state']='disabled'
        self.boss.play()

    def stop(self):
        self.boutton_play['state'] = 'normal'
        self.boutton_plus_un['state'] = 'normal'
        self.boss.stop()