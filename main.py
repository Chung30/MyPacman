from tkinter import *
from PIL import Image, ImageTk
from View.selectmode import SelectMode  # Assuming you have this module
import pygame

class PacmanGame:
    def __init__(self):
        self.root = Tk()
        self.window_width = 600
        self.window_height = 500
        self.image_path = "asset/background.png"  # Replace with your image path
        self.label_image_path = "asset/logo1.png"
        self.button_image_path = "asset/button.png"
        self.menu = ["START", "SCORE", "SETTING", "HELP", "QUIT"]
        self.center_window()

        self.background_label = Label(self.root)
        self.label = Label(self.root)

        self.init_ui()
        self.root.mainloop()

    def center_window(self):
        sc_width = self.root.winfo_screenwidth()
        sc_height = self.root.winfo_screenheight()
        center_x = int(sc_width / 2 - self.window_width / 2)
        center_y = int(sc_height / 2 - self.window_height / 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.root.resizable(0, 0)

    def init_ui(self):
        self.load_images()
        self.show_background()
        self.show_label()
        self.show_buttons()

    def load_images(self):
        self.background_image = ImageTk.PhotoImage(Image.open(self.image_path))
        self.label_image = ImageTk.PhotoImage(Image.open(self.label_image_path))
        self.button_image = ImageTk.PhotoImage(Image.open(self.button_image_path).resize((185, 54)))

    def show_background(self):
        self.background_label.configure(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_label(self):
        self.label.configure(image=self.label_image)
        self.label.place(x=205, y=48)

    def show_buttons(self):
        x, y = 205, 160
        self.labels = []
        for i, item in enumerate(self.menu):
            if i == 0:
                button = Button(self.root, text=item, font=("Times New Roman", 12, "bold"),
                                command=self.hide, image=self.button_image, compound=CENTER)
            else:
                button = Button(self.root, text=item, font=("Times New Roman", 12, "bold"),
                                image=self.button_image, compound=CENTER)
            button.place(x=x, y=y)
            self.labels.append(button)
            y += 65
        self.labels[3].config(command=self.root.destroy)

    def hide(self):
        SelectMode(self.root)
        self.root.withdraw()

if __name__ == "__main__":
    game = PacmanGame()

