import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class Rule(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title('Rule')
        self.iconbitmap("asset/game.ico")
        self['bg'] = 'lightgray'
        self.attributes('-topmost', True)
        self.setBackground()
        self.center_screen()
        photo = tk.PhotoImage(file="asset/back-arrow.png")
        self.photoimage = photo.subsample(16, 16)
        label = tk.Label(self, text='Rule', font=('cambria', 16), width=25)
        label.place(x=150, y=40)

        textbox = tk.Text(self, wrap=tk.WORD, width=50, height=20, font=('Comic Sans MS', 10), bg="#006666",
                          fg="#FFFFFF")
        data = " "
        with open('asset/Rule.txt', encoding='utf-8') as file:
            for line in file:
                data += line
        textbox.insert(tk.END, data)
        textbox.place(x=100, y=80)
        textbox.config(state=tk.DISABLED)

        back_button = tk.Button(self, text="Back", image=self.photoimage, compound=tk.LEFT, command=self.back)
        back_button.place(x=480, y=450)

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