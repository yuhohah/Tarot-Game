from mimetypes import init
import random
import tkinter as tk
from PIL import ImageTk, Image
import Deck
import string
from tkinter import ttk
import time

index = [1, 2, 3, 4, 5]
window = tk.Tk()
window.title('Tarot')
window.geometry("980x600")
window.resizable(True, True)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)
window.columnconfigure(3, weight=2)
window.columnconfigure(4, weight=1)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=2)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
#window.rowconfigure(4, weight=1)

def clear_frame():
    for widgets in window.winfo_children():
        widgets.destroy()

def game():
    deck = Deck.get_deck()
    Deck.deck_suffle(deck)
    #rodape = tk.Label(window, text="Feito por ", font=("Calibri 12 bold"))
    #rodape.grid(row=5,column=2)

    def on_click_btn2():
        start_time = time.time()
        clear_frame()

        carta1 = Deck.get_card(deck)
        #rev_carta1 = carta1["rev"]
        #carta1 = carta1["card"]

        carta = Deck.get_card(deck)
        #rev_carta = int(carta["rev"])
        #carta = carta["card"]

        carta2 = Deck.get_card(deck)
        #rev_carta2 = carta2["rev"]
        #carta2 = carta2["card"]

        #print( rev_carta, rev_carta1, rev_carta2)

        nomedacarta = tk.Label(window, text="",font=('Calibri 15 bold'))
        nomedacarta.grid(row=0, column=2)
        nomedacarta1 = tk.Label(window, text="",font=('Calibri 15 bold'))
        nomedacarta1.grid(row=0, column=1)
        nomedacarta2 = tk.Label(window, text="",font=('Calibri 15 bold'))
        nomedacarta2.grid(row=0, column=3)

        nomedacarta1["text"] = carta1['name'] + " - " + str(carta1['sequence'])
        nomedacarta["text"] = carta['name'] + " - " + str(carta['sequence'])
        nomedacarta2["text"] = carta2['name'] + " - " + str(carta2['sequence'])

        image = Image.open(carta['image'])
        image = image.resize((175,340), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        widgetimage = tk.Label(image=image)
        widgetimage.image = image
        widgetimage.grid( row=1, column=2)

        image = Image.open(carta1['image'])
        image = image.resize((175,340), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        widgetimage1 = tk.Label(image=image)
        widgetimage1.image = image
        widgetimage1.grid( row=1, column=1)

        image = Image.open(carta2['image'])
        image = image.resize((175,340), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        widgetimage2 = tk.Label(image=image)
        widgetimage2.image = image
        widgetimage2.grid( row=1, column=3)

        message = tk.Label(window, text="", font=("Calibri 12"))
        message.grid(row=2, column=2)
        message1 = tk.Label(window, text="", font=("Calibri 12"))
        message1.grid(row=2, column=1)
        message2 = tk.Label(window, text="", font=("Calibri 12"))
        message2.grid(row=2, column=3)

        if carta.get("message") != None:
            message["text"] = carta["message"]
        else:
            message["text"] = str(carta['desc']).replace(".", ".\n")
        if carta1.get("message") != None:
            message1["text"] = carta1["message"]
        else:
            message1["text"] = str(carta1['desc']).replace(".", ".\n")
        if carta2.get("message") != None:
            message2["text"] = carta2["message"]
        else:
            message2["text"] = str(carta2['desc']).replace(".", ".\n")


    def on_click_btn1():
        carta = Deck.get_card(deck)

        nomedacarta = tk.Label(window, text="Puxe uma Sorte!",font=('Calibri 15 bold'))
        nomedacarta.grid(row=0, column=2)

        nomedacarta["text"] = carta['name'] + " - " + str(carta['sequence'])
        image = Image.open(carta['image'])
        image = image.resize((175,340), Image.LANCZOS)

        image = ImageTk.PhotoImage(image)
        label1 = tk.Label(image=image)
        label1.image = image
        label1.grid( row=1, column=2)

        message = tk.Label(window, text="", font=("Calibri 12"))
        message.grid(row=2, column=2)

        if carta.get("message") != None:
            message["text"] = carta["message"]
        else:
            message["text"] = str(carta['desc']).replace(".", ".\n")

    btn1 = tk.Button(window, text="1X Sorte", command=on_click_btn1, width=20, padx=30, bg='gold', font='sans')
    btn1.grid(row=3, column=2)

    btn2 = tk.Button(window, text="3X Sorte", command=on_click_btn2, width=60, padx=10)
    btn2.grid(row=4, column=2)

def deck_list():
    deck = Deck.get_deck()
    #center = tk.Frame(window, )
    cells = {}
    for row in range(4):
        for column in range(4):
            cell = tk.Frame(window, bg='black', highlightbackground="black",
                        highlightcolor="black", highlightthickness=1,
                        width=100, height=100,  padx=3,  pady=3)
            cell.rowconfigure(row=0, weight=1)
            carta = Deck.get_card(deck)

            nomedacarta = tk.Label(cell, text="",font=('Calibri 10'))
            nomedacarta.grid(row=0, column=column, sticky="n")
            nomedacarta["text"] = carta['name'] + " - " + str(carta['sequence'])
            image = Image.open(carta['image'])
            image = image.resize((100,200), Image.LANCZOS)

            image = ImageTk.PhotoImage(image)
            label1 = tk.Label(image=image)
            label1.image = image
            label1.grid(row=1, column=column, sticky="s")

            cell.grid(row=row, column=column)

            cells[(row, column)] = cell




def on_click_btnstart():
    clear_frame()
    game()

btnstart = tk.Button(window, text="Start", command=on_click_btnstart, width=60, padx=10)
btnstart.grid(row=2, column=2)

def on_click_btncards():
    clear_frame()
    deck_list()

btncards = tk.Button(window, text="Cards", command=on_click_btncards, width=60, padx=10)
btncards.grid(row=3, column=2)

window.mainloop()