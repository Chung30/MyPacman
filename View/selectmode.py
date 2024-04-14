from tkinter import *
from PIL import ImageTk, Image
from Control.run import GameController
from Model.constants import STATE1, STATE2


class SelectMode(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pac - man")
        self.resizable(0, 0)
        self.center_screen()
        self.setBackgroud()
        self.logo = ImageTk.PhotoImage(Image.open("asset/logo1.png"))
        self.labelLogo = Label(self, image=self.logo).place(x=205, y=40)
        self.photo = PhotoImage(file="asset/back-arrow.png")
        self.photoimage = self.photo.subsample(16, 16)
        self.back_button = Button(self, text="Back", image=self.photoimage, compound=LEFT,
                                     command=self.backbtn).place(x=480, y=450)

        self.image1 = ImageTk.PhotoImage(Image.open("asset/2player.png"))
        self.image2 = ImageTk.PhotoImage(Image.open("asset/1player.png"))


        self.single_player = Button(self, image=self.image1, width=150, height=160, compound=TOP,command=self.single_player).place(x=50, y=140)
        self.muilti_player = Button(self, image=self.image2, width=150, height=160, compound=TOP,command=self.start_multiplayer).place(x=400, y=140)
        self.input_name = Entry(self, width=30)
        self.input_name.place(x=205, y=400)

    # hidden Present and show menu frame
    def backbtn(self):
        self.master.deiconify()
        self.withdraw()

        # Add code to start single player mode here

    def start_multiplayer(self):
        self.withdraw()
        game = GameController(STATE2,"")
        game.startGame()
        while True:
            game.update()
    def single_player(self):

        self.withdraw()
        game = GameController(STATE1,self.writePlayerName())
        game.startGame()
        while True:
            game.update()

    def setBackgroud(self):
        self.image_path = "asset/background.png"  # Replace with your image path
        self.image = Image.open(self.image_path)
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def writePlayerName(self):
        player_name = self.input_name.get()
        return player_name
    def center_screen(self):
        self.width = 600
        self.height = 500
        sc_width = self.winfo_screenwidth()
        sc_height = self.winfo_screenheight()
        center_x = int(sc_width / 2 - self.width / 2)
        center_y = int(sc_height / 2 - self.height / 2)
        self.geometry(f'{600}x{500}+{center_x}+{center_y}')



