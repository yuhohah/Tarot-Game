from mimetypes import init
import random
import tkinter as tk
from PIL import ImageTk, Image
import Deck
import string

window = tk.Tk()
window.title('Tarot')
window.geometry("700x700")
window.resizable(True, True)

deck = Deck.get_deck()
Deck.deck_suffle(deck)


label = tk.Label(window, text="Puxe uma Sorte!", font=('Calibri 15 bold'))
label.pack(pady=20)

rodape = tk.Label(window, text="Feito por Luan", font=("Calibri 12 bold"))
rodape.pack(pady=20, side=tk.BOTTOM)

descricao = tk.Label(window, text="", font=("Calibri 12"), wraplength= 300)
descricao.pack(pady=20, side=tk.BOTTOM)


print(set(descricao.configure().keys()) - set(descricao.configure().keys()))


def on_click_btn2():
    carta = Deck.get_card(deck)
def on_click_btn1():
    carta = Deck.get_card(deck)

    print(carta)

    # carta['name']
    # carta['image']
    # carta['desc']
    # carta['rdesc']
    # carta['sequence']
    # carta['cardtype']
    # carta['message']

    label["text"] = (carta['name'] )
                     # + " - " + str(carta['sequence']))
    image = Image.open(carta['image'])
    image = image.resize((175, 340), Image.LANCZOS)

    image = ImageTk.PhotoImage(image)
    label1 = tk.Label(image=image)
    label1.image = image
    #label1.pack(side="top")
    #label1.pack(side="bottom", fill="both")
    label1.place(x=260, y=80)

    descricao["text"] = carta["desc"]


btn1 = tk.Button(window, text="1X Sorte", command=on_click_btn1, width=15, padx=30)
btn1.pack(pady=25)
btn1.pack(side=tk.BOTTOM)
btn1.place(x=140, y=550)

btn2 = tk.Button(window, text="3X Sorte", command=on_click_btn2, width=15, padx=30)
btn2.pack(pady=25)
btn2.pack(side=tk.BOTTOM)
btn2.place(x=340, y=550)

window.mainloop()