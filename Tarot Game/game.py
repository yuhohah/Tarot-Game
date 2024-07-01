import tkinter as tk
from PIL import ImageTk, Image
import Deck

window = tk.Tk()
window.title('Tarot')
window.geometry("700x600")
window.resizable(False, False)
window.configure(background='#008080')

deck = Deck.get_deck()
Deck.deck_suffle(deck)

label = tk.Label(window, text="Escolha a quantidade de Cartas!", font=('Calibri 15 bold'))
label.pack(pady=20)
label.configure(background='#008080')

# rodape = tk.Label(window, text="Feito por Luan", font=("Calibri 12 bold"))
# rodape.pack(pady=20, side=tk.BOTTOM)

def on_click_btn2():

    label.destroy()

    window.geometry('1124x650')

    carta_component()

    carta_component()

    carta_component()

    btn1.destroy()
    btn2.destroy()

def on_click_btn1():
    label.destroy()
    carta_component()

    btn2.destroy()
    btn1.destroy()

def carta_component():
    carta = Deck.get_card(deck)
    informacao = carta[0]
    reverso = carta[1]
    print(reverso)

    titulo = tk.Label(window, font=('Calibri 15 bold'))
    titulo.pack(pady=20)
    titulo.configure(background='#008080')

    titulo["text"] = (informacao['name'] + " - " + str(informacao['sequence']))
    image = Image.open(informacao['image'])
    image = image.resize((175, 340), Image.LANCZOS)

    if (reverso == -1):
        image.rotate(180)

    image = ImageTk.PhotoImage(image)
    imagem = tk.Label(image=image)
    imagem.image = image
    imagem.place(x=260, y=80)

    descricao = tk.Label(window, text="", font=("Calibri 12"), wraplength=450)
    descricao.pack(pady=75, side=tk.BOTTOM)
    descricao.configure(background='#008080')

    if (reverso == -1):
        descricao["text"] = informacao["rdesc"]
    else:
        descricao["text"] = informacao["desc"]



btn1 = tk.Button(window, text="1-Carta", command=on_click_btn1, width=15, padx=30)
btn1.pack(pady=25)
btn1.pack(side=tk.BOTTOM)
btn1.place(x=140, y=500)
btn1.configure(background='grey')

btn2 = tk.Button(window, text="3-Carta", command=on_click_btn2, width=15, padx=30)
btn2.pack(pady=25)
btn2.pack(side=tk.BOTTOM)
btn2.place(x=340, y=500)
btn2.configure(background='grey')

window.mainloop()