import tkinter as tk
from PIL import ImageTk, Image
from models.deck_manager import DeckManager
from utils.resource_path import resource_path


class GameView:
    def __init__(self, root):
        self.root = root
        self.deck_manager = DeckManager()
        self.btn1 = None
        self.btn2 = None
        self.background_label = None  # Referência ao background
        self.setup_ui()

    def setup_ui(self):
        self.setup_background()
        self.setup_grid()
        self.create_buttons_game()

    def setup_background(self):
        bg_image_path = resource_path("images/background.jpg")
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((1320, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Cria o label de background se não existir
        if not self.background_label:
            self.background_label = tk.Label(self.root, image=self.bg_image)
            self.background_label.place(relwidth=1, relheight=1)
        else:
            # Atualiza a imagem se já existir
            self.background_label.config(image=self.bg_image)
            self.background_label.image = self.bg_image

    def setup_grid(self):
        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        for i in range(4):
            self.root.rowconfigure(i, weight=1)

    def create_restart_button(self):
        """Cria o botão de Novo Jogo"""
        style = {
            "width": 20,
            "height": 2,
            "bg": "#FFA500",  # Laranja para destacar
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "relief": "raised",
            "bd": 5,
            "highlightthickness": 2,
            "highlightbackground": "black",
        }

        self.restart_btn = tk.Button(
            self.root,
            text="Novo Jogo",
            command=self.restart_game,
            **style
        )
        self.restart_btn.grid(row=4, column=2, pady=20, padx=10, sticky="nsew")
        self.apply_hover_effect(self.restart_btn, "#FF8C00", "#FFA500")

    def restart_game(self):
        """Reinicia o jogo completamente"""
        self.clear_frame()
        self.deck_manager = DeckManager()  # Recria o baralho
        self.setup_ui()  # Recria a interface inicial

    def create_buttons_game(self):
        style = {
            "width": 20,
            "height": 2,
            "bg": "#B0C4DE",
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "relief": "raised",
            "bd": 5,
            "highlightthickness": 2,
            "highlightbackground": "black",
        }

        self.btn1 = tk.Button(
            self.root,
            text="1X Sorte",
            command=self.on_click_btn1,
            **style
        )
        self.btn1.grid(row=3, column=2, pady=20, padx=10, sticky="nsew")
        self.apply_hover_effect(self.btn1, "#696969", "#B0C4DE")

        self.btn2 = tk.Button(
            self.root,
            text="3X Sorte",
            command=self.on_click_btn3,
            **style
        )
        self.btn2.grid(row=4, column=2, pady=20, padx=10, sticky="nsew")
        self.apply_hover_effect(self.btn2, "#696969", "#B0C4DE")

    def apply_hover_effect(self, button, hover_color, original_color):
        def on_enter(event):
            button['bg'] = hover_color

        def on_leave(event):
            button['bg'] = original_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def display_card(self, carta, column, reversed=False):
        nomedacarta = tk.Label(
            self.root,
            text=f"{carta['name']} - {carta['sequence']}" + (" (Reversed)" if reversed else ""),
            font=('Arial 20 bold'),
            bg="#708090",
            fg="white",
            padx=10, pady=5
        )
        nomedacarta.grid(row=0, column=column, pady=20, sticky="n")

        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((175, 340), Image.LANCZOS)
            if reversed:
                image = image.rotate(180)
            image = ImageTk.PhotoImage(image)
            label = tk.Label(self.root, image=image, bg="#000000")
            label.image = image
            label.grid(row=1, column=column, pady=20, sticky="n")
        except FileNotFoundError:
            print(f"Erro: Imagem da carta {carta['image']} não encontrada.")

        message_text = carta.get("rdesc" if reversed else "message", str(carta['desc']).replace(".", ".\n"))
        message = tk.Label(
            self.root,
            text=message_text,
            font=("Arial 14"),
            bg="#708090",
            fg="white",
            padx=10, pady=5,
            wraplength=400 if column == 2 else 300
        )
        message.grid(row=2, column=column, pady=20, sticky="n")

    def remove_buttons(self):
        """Remove os botões da tela"""
        if self.btn1:
            self.btn1.destroy()
        if self.btn2:
            self.btn2.destroy()

    def on_click_btn1(self):
        cart = self.deck_manager.get_card()
        carta = cart[0]
        reversed = cart[1] == 1

        self.remove_buttons()  # Remove os botões
        self.display_card(carta, column=2, reversed=reversed)
        self.create_restart_button()

    def on_click_btn3(self):
        cartas = [self.deck_manager.get_card() for _ in range(3)]
        self.remove_buttons()  # Remove os botões

        for i, (carta, reversed) in enumerate(cartas):
            self.display_card(carta, column=i + 1, reversed=(reversed == 1))
            self.create_restart_button()

    def clear_frame(self):
        """Limpa todos os widgets exceto o background"""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()