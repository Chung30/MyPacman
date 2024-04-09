from tkinter import *
from PIL import ImageTk, Image
from Control.run import GameController
from Model.constants import STATE1


class SelectMode(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pac man")
        self.resizable(0, 0)
        self.width = 600
        self.height = 500
        sc_width = self.winfo_screenwidth()
        sc_height = self.winfo_screenheight()
        center_x = int(sc_width / 2 - self.width / 2)
        center_y = int(sc_height / 2 - self.height / 2)
        self.geometry(f'{600}x{500}+{center_x}+{center_y}')
        self.setBackgroud()
        self.logo = ImageTk.PhotoImage(Image.open("asset/logo1.png"))
        self.labelLogo = Label(self, image=self.logo).place(x=205, y=40)
        self.back = Button(self, text="back", command=self.backbtn).grid(column=0, row=0)
        self.image = ImageTk.PhotoImage(Image.open("asset/user.png").resize((60, 40)))

        self.single_player = Button(self, image=self.image, width=150, height=160, compound=TOP,command=self.single_player).place(x=50, y=140)
        self.muilti_player = Button(self, image=self.image, width=150, height=160, compound=TOP).place(x=400, y=140)
        self.input_name = Entry(self, width=30).place(x=205, y=400)

    # hidden Present and show menu frame
    def backbtn(self):
        self.master.deiconify()
        self.withdraw()

        # Add code to start single player mode here

    def start_multiplayer(self):
        print("Starting multiplayer mode...")
        # Add code to start multiplayer mode here
    def single_player(self):
        self.withdraw()
        game = GameController(STATE1)
        game.startGame()
        while True:
            game.update()

    def setBackgroud(self):
        self.image_path = "asset/background.png"  # Replace with your image path
        self.image = Image.open(self.image_path)
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)



