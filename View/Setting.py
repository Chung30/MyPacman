import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Setting(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Setting')
        self.iconbitmap("asset/game.ico")
        self.attributes('-topmost', True)
        self.center_screen()
        self.setBackground()
        self.photo = tk.PhotoImage(file="asset/back-arrow.png")
        self.photoimage = self.photo.subsample(16, 16)
        self.label = tk.Label(self, text='Setting', font=('cambria', 16), width=25)
        self.label.place(x=150, y=40)

        self.frame = tk.Frame(self, width=600, height=500)
        self.frame.place(x=180, y=100)

        self.label1 = tk.Label(self.frame, text='Sound:', font=('cambria', 12), width=25)
        self.label1.pack(side=LEFT)

        self.var1 = tk.IntVar()
        self.chb = tk.Checkbutton(self.frame, variable=self.var1, onvalue=1, offvalue=0)
        self.chb.pack(side=LEFT)

        self.init_checkbox()
        self.back_button = tk.Button(self, text="Back", image=self.photoimage, compound=tk.LEFT, command=self.back).place(x=480, y=450)
        self.save_button = tk.Button(self,text="Save",compound=CENTER,command=self.save,width=10,height=2).place(x=50,y=450)

    def setBackground(self):
        self.image_path = "asset/background.png"  # Replace with your image path
        self.image = Image.open(self.image_path)
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def back(self):
        self.master.deiconify()
        self.withdraw()

    def center_screen(self):
        self.width = 600
        self.height = 500
        sc_width = self.winfo_screenwidth()
        sc_height = self.winfo_screenheight()
        center_x = int(sc_width / 2 - self.width / 2)
        center_y = int(sc_height / 2 - self.height / 2)
        self.geometry(f'{600}x{500}+{center_x}+{center_y}')
    def save(self):
        try:
            with open("asset/setting.txt", "w") as file:
                if self.var1.get() == 1:
                    file.write(str(1))
                else:
                    file.write(str(0))
        except Exception as e:
            print(e)
        self.back()
    def init_checkbox(self):
        with open("asset/setting.txt","r") as file:
            check = file.read().strip()
            if int(check) == 1:
                self.var1.set(1)
            else:
                self.var1.set(0)
