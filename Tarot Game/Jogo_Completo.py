import random
import tkinter as tk
from PIL import ImageTk, Image
import Deck
import string
from tkinter import ttk
import time

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Tarot')
        self.root.geometry("1320x700")
        self.root.resizable(True, True)

        self.setup_background()

        self.setup_grid()
        self.create_initial_buttons()

    def setup_background(self):
        # Load the background image
        self.bg_image = Image.open("images/background.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

    def setup_grid(self):
        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        for i in range(4):
            self.root.rowconfigure(i, weight=1)

    def clear_frame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def game(self):
        self.deck = Deck.get_deck()
        Deck.deck_suffle(self.deck)

        self.create_buttons()

    def create_buttons(self):
        btn1 = tk.Button(self.root, text="1X Sorte", command=self.on_click_btn1, width=20, padx=30, bg='gold', font='sans')
        btn1.grid(row=3, column=2)

        btn2 = tk.Button(self.root, text="3X Sorte", command=self.on_click_btn2, width=60, padx=10)
        btn2.grid(row=4, column=2)

    def on_click_btn1(self):
        cart = Deck.get_card(self.deck)
        carta = cart[0]
        rev = cart[1]

        self.clear_frame()
        self.setup_background()
        self.setup_grid()

        nomedacarta = tk.Label(self.root, text="Puxe uma Sorte!", font=('Calibri 15 bold'))
        nomedacarta.grid(row=0, column=2)

        nomedacarta["text"] = carta['name'] + " - " + str(carta['sequence'])
        image = Image.open(carta['image'])
        image = image.resize((175, 340), Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        label1 = tk.Label(image=image)
        label1.image = image
        label1.grid(row=1, column=2)

        message = tk.Label(self.root, text="", font=("Calibri 12"))
        message.grid(row=2, column=2)

        if carta.get("message") is not None:
            message["text"] = carta["message"]
        else:
            message["text"] = str(carta['desc']).replace(".", ".\n")

    def on_click_btn2(self):
        start_time = time.time()
        self.clear_frame()
        self.setup_grid()

        carta1 = Deck.get_card(self.deck)
        rev_carta1 = carta1[1]
        carta1 = carta1[0]

        carta = Deck.get_card(self.deck)
        rev_carta = carta[1]
        carta = carta[0]

        carta2 = Deck.get_card(self.deck)
        rev_carta2 = carta2[1]
        carta2 = carta2[0]

        nomedacarta1 = tk.Label(self.root, text=carta1['name'] + " - " + str(carta1['sequence']), font=('Calibri 15 bold'))
        nomedacarta1.grid(row=0, column=1)

        nomedacarta = tk.Label(self.root, text=carta['name'] + " - " + str(carta['sequence']), font=('Calibri 15 bold'))
        nomedacarta.grid(row=0, column=2)

        nomedacarta2 = tk.Label(self.root, text=carta2['name'] + " - " + str(carta2['sequence']), font=('Calibri 15 bold'))
        nomedacarta2.grid(row=0, column=3)

        self.display_card_image(carta, 1, 2)
        self.display_card_image(carta1, 1, 1)
        self.display_card_image(carta2, 1, 3)

        self.display_message(carta, 2, 2)
        self.display_message(carta1, 2, 1)
        self.display_message(carta2, 2, 3)

    def display_card_image(self, carta, row, column):
        image = Image.open(carta['image'])
        image = image.resize((175, 340), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        widgetimage = tk.Label(image=image)
        widgetimage.image = image
        widgetimage.grid(row=row, column=column)

    def display_message(self, carta, row, column):
        message = tk.Label(self.root, text="", font=("Calibri 12"))
        message.grid(row=row, column=column)
        if carta.get("message") is not None:
            message["text"] = carta["message"]
        else:
            message["text"] = str(carta['desc']).replace(".", ".\n")

    def deck_list(self):
        deck = Deck.get_deck()
        cells = {}
        for row in range(4):
            for column in range(4):
                cell = tk.Frame(self.root, bg='black', highlightbackground="black",
                                highlightcolor="black", highlightthickness=1,
                                width=100, height=100, padx=3, pady=3)
                cell.rowconfigure(row=0, weight=1)
                carta = Deck.get_card(deck)

                nomedacarta = tk.Label(cell, text=carta['name'] + " - " + str(carta['sequence']), font=('Calibri 10'))
                nomedacarta.grid(row=0, column=column, sticky="n")

                image = Image.open(carta['image'])
                image = image.resize((100, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
                label1 = tk.Label(image=image)
                label1.image = image
                label1.grid(row=1, column=column, sticky="s")

                cell.grid(row=row, column=column)

                cells[(row, column)] = cell

    def on_click_btnstart(self):
        self.clear_frame()
        self.game()

    def on_click_btncards(self):
        self.clear_frame()
        self.deck_list()

    def create_initial_buttons(self):
        btnstart = tk.Button(self.root, text="Start", command=self.on_click_btnstart, width=40, height=7, padx=10)
        btnstart.grid(row=2, column=2)
        btnstart.configure(background='gold')

        btncards = tk.Button(self.root, text="Cards", command=self.on_click_btncards, width=40, height=5, padx=10)
        btncards.grid(row=3, column=2)
        btncards.configure(background='grey')

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
