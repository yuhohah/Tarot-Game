import tkinter as tk
from PIL import ImageTk, Image
import Deck
import os
import sys


def resource_path(relative_path):
    """Obter o caminho absoluto para recursos, considerando o PyInstaller."""
    try:
        # Quando executado como um executável
        base_path = sys._MEIPASS
    except AttributeError:
        # Quando executado como um script Python
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Tarot')
        self.root.geometry("1320x700")
        self.root.resizable(True, True)
        #self.root.wm_attributes("-transparentcolor", '#708090')
        #self.root.wm_attributes("-transparentcolor", 'black')
        #self.root.wm_attributes("-transparentcolor", 'white')

        self.setup_background()

        self.setup_grid()
        self.create_initial_buttons()


    def setup_background(self):
        # Load the background image
        bg_image_path = resource_path( "images/background.jpg" )
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((1320, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

    def setup_grid(self):
        # Adiciona pesos iguais para colunas e linhas
        total_columns = 5
        total_rows = 4
        for i in range(total_columns):
            self.root.columnconfigure(i, weight=1)
        for i in range(total_rows):
            self.root.rowconfigure(i, weight=1)

    def clear_frame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def setup(self):
        self.clear_frame()
        self.setup_background()
        self.setup_grid()

    def start_game(self):
        self.deck = Deck.get_deck()
        Deck.deck_suffle(self.deck)

        self.create_buttons_game()

    def create_buttons_game(self):

        style = {
            "width": 20,
            "height": 2,
            "bg": "#B0C4DE",  # Dourado
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "relief": "raised",
            "bd": 5,
            "highlightthickness": 2,
            "highlightbackground": "black",
        }

        # Botão 1X Sorte
        btn1 = tk.Button(
            self.root,
            text="1X Sorte",
            command=self.on_click_btn1,
            **style
        )
        btn1.grid(row=3, column=2, pady=20, padx=10, sticky="nsew")
        self.apply_hover_effect(btn1, "#696969", "#B0C4DE")

        # Botão 3X Sorte
        btn2 = tk.Button(
            self.root,
            text="3X Sorte",
            command=self.on_click_btn3,
            **style
        )
        btn2.grid(row=4, column=2, pady=20, padx=10, sticky="nsew")
        self.apply_hover_effect(btn2, "#696969", "#B0C4DE")

    def apply_hover_effect(self, button, hover_color, original_color):
        def on_enter(event):
            button['bg'] = hover_color

        def on_leave(event):
            button['bg'] = original_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def display_card(self, carta, column, reversed=False):
        """
        Exibe uma carta na interface.
        :param carta: Dicionário contendo os dados da carta.
        :param column: Coluna onde a carta será exibida.
        :param reversed: Indica se a carta está invertida.
        """
        # Título da carta
        nomedacarta = tk.Label(
            self.root,
            text=f"{carta['name']} - {carta['sequence']}" + (" (Reversed)" if reversed else ""),
            font=('Arial 20 bold'),
            bg="#708090",  # Fundo cinza escuro
            fg="white",  # Texto branco
            padx=10, pady=5
        )
        nomedacarta.grid(row=0, column=column, pady=20, sticky="n")

        # Imagem da carta
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((175, 340), Image.LANCZOS)
            if reversed:  # Rotaciona a imagem se a carta estiver invertida
                image = image.rotate(180)
            image = ImageTk.PhotoImage(image)
            label = tk.Label(self.root, image=image, bg="#000000")  # Fundo preto
            label.image = image
            label.grid(row=1, column=column, pady=20, sticky="n")
        except FileNotFoundError:
            print(f"Erro: Imagem da carta {carta['image']} não encontrada.")

        # Mensagem da carta
        message_text = carta.get("rdesc" if reversed else "message", str(carta['desc']).replace(".", ".\n"))
        message = tk.Label(
            self.root,
            text=message_text,
            font=("Arial 14"),
            bg="#708090",  # Fundo cinza escuro
            fg="white",  # Texto branco
            padx=10, pady=5,
            wraplength=400 if column == 2 else 300  # Ajusta a largura do texto
        )
        message.grid(row=2, column=column, pady=20, sticky="n")

    def on_click_btn1(self):
        """
        Exibe uma única carta sorteada.
        """
        cart = Deck.get_card(self.deck)
        carta = cart[0]
        reversed = cart[1] == 1  # Verifica se a carta está invertida

        self.setup()  # Configura a interface

        # Exibe a carta na coluna central
        self.display_card(carta, column=2, reversed=reversed)

    def on_click_btn3(self):
        """
        Exibe três cartas sorteadas.
        """
        self.setup()  # Configura a interface

        # Puxa três cartas
        cartas = [Deck.get_card(self.deck) for _ in range(3)]

        # Exibe cada carta em uma coluna
        for i, (carta, reversed) in enumerate(cartas):
            self.display_card(carta, column=i + 1, reversed=(reversed == 1))

    def setup(self):
        """
        Configura a interface para exibição de cartas.
        """
        self.clear_frame()
        self.setup_background()
        self.setup_grid()

    def deck_list(self):
        """
        Exibe todas as cartas do deck em um layout de grade com rolagem do mouse.
        """
        deck = Deck.get_deck()
        colunas = 9  # Número de colunas
        linhas = (len(deck) // colunas) + (1 if len(deck) % colunas != 0 else 0)

        self.setup()

        # Criação do Canvas e Scrollbar
        canvas, scrollable_frame = self._create_scrollable_area()

        # Adicionar suporte à rolagem com o mouse
        self._add_mouse_scroll(canvas)

        # Adicionar cartas na grade
        for index, carta in enumerate(deck):
            row, column = divmod(index, colunas)
            self._create_card_cell(scrollable_frame, carta, row, column)

    def _create_scrollable_area(self):
        """
        Cria uma área rolável com um Canvas e um Frame interno.
        :return: canvas, scrollable_frame
        """
        canvas = tk.Canvas(self.root, bg="#2C2C2C")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2C2C2C", height=700, width=1320)

        # Configurar o canvas para rolar o frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Disposição do Canvas e da Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return canvas, scrollable_frame

    def _add_mouse_scroll(self, canvas):
        """
        Adiciona suporte à rolagem com o mouse no Canvas.
        :param canvas: Canvas onde a rolagem será aplicada.
        """

        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int((event.delta / 120)), "units")  # Windows/Linux
            if event.num == 4:  # Scroll para cima (macOS)
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Scroll para baixo (macOS)
                canvas.yview_scroll(1, "units")

        # Vincular eventos de rolagem do mouse
        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # Windows/Linux
        canvas.bind_all("<Button-4>", _on_mouse_wheel)  # macOS (scroll para cima)
        canvas.bind_all("<Button-5>", _on_mouse_wheel)  # macOS (scroll para baixo)

    def _create_card_cell(self, parent, carta, row, column):
        """
        Cria uma célula para exibir uma carta na grade.
        :param parent: Frame pai onde a célula será adicionada.
        :param carta: Dicionário contendo os dados da carta.
        :param row: Linha da grade.
        :param column: Coluna da grade.
        """
        # Criar célula para a carta
        cell = tk.Frame(parent, bg='black', highlightbackground="black",
                        highlightcolor="black", highlightthickness=1)
        cell.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Nome da carta
        nomedacarta = tk.Label(
            cell,
            text=f"{carta['name']} - {carta['sequence']}",
            font=('Calibri 10'),
            bg='white',
            wraplength=180
        )
        nomedacarta.pack(side="top", pady=5)

        # Imagem da carta
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((75, 150), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            label1 = tk.Label(cell, image=image)
            label1.image = image
            label1.pack(side="bottom", pady=5)
        except FileNotFoundError:
            print(f"Erro: Imagem da carta {carta['image']} não encontrada.")

    def on_click_btnstart(self):
        self.setup()
        self.start_game()

    def on_click_btncards(self):
        self.clear_frame()
        self.setup_background()

        self.deck_list()

    def create_initial_buttons(self):
        self.setup_background()
        self.setup_grid()

        # Estilo dos botões
        style = {
            "width": 20,
            "height": 2,
            "bg": "#B0C4DE",  # Dourado
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "relief": "raised",
            "bd": 5,
            "highlightthickness": 2,
            "highlightbackground": "black",
        }

        hover_style = {"bg": "#696969", "cursor": "hand2"}  # Amarelo mais claro

        # Botão "Start"
        btnstart = tk.Button(
            self.root,
            text="Start",
            command=self.on_click_btnstart,
            **style,
        )
        btnstart.grid(row=2, column=2, pady=10)

        # Botão "Cards"
        btncards = tk.Button(
            self.root,
            text="Cards",
            command=self.on_click_btncards,
            **style,
        )
        btncards.grid(row=3, column=2, pady=10)

        # Adicionar hover effects para os botões
        def on_enter(e, btn):
            btn.configure(**hover_style)

        def on_leave(e, btn):
            btn.configure(bg=style["bg"])

        btnstart.bind("<Enter>", lambda e, b=btnstart: on_enter(e, b))
        btnstart.bind("<Leave>", lambda e, b=btnstart: on_leave(e, b))

        btncards.bind("<Enter>", lambda e, b=btncards: on_enter(e, b))
        btncards.bind("<Leave>", lambda e, b=btncards: on_leave(e, b))

    def destroy_grid(self):
        """
        Remove todos os widgets da janela principal, mantendo elementos fixos, se necessário.
        """
        for widget in self.root.grid_slaves():  # Itera sobre os widgets no grid
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
