import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from models.deck import Deck
from utils.resource_path import resource_path

class DeckView:
    def __init__(self, root):
        self.root = root
        self.deck = Deck
        self.background_label = None
        self.setup_ui()

        self.root.bind('<Escape>', lambda e: self.go_back())

    def setup_ui(self):
        self.setup_background()
        self.deck_list()

    def setup_background(self):
        """Configura o background apenas uma vez"""
        if not self.background_label:
            bg_image_path = resource_path("images/background.jpg")
            self.bg_image = Image.open(bg_image_path)
            self.bg_image = self.bg_image.resize((1320, 700), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.bg_image)

            self.background_label = tk.Label(self.root, image=self.bg_image)
            self.background_label.place(relwidth=1, relheight=1)

    def deck_list(self):
        """Exibe todas as cartas do deck em uma grade rolável"""
        deck = self.deck.get_deck()
        colunas = 9
        linhas = (len(deck) // colunas) + (1 if len(deck) % colunas != 0 else 0)

        canvas = tk.Canvas(self.root, bg="#2C2C2C")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2C2C2C", height=700, width=1320)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._add_mouse_scroll(canvas)

        for index, carta in enumerate(deck):
            row, column = divmod(index, colunas)
            self._create_card_cell(scrollable_frame, carta, row, column)

    def _create_card_cell(self, parent, carta, row, column):
        """Cria uma célula clicável para cada carta"""
        cell = tk.Frame(parent, bg='black', highlightbackground="black",
                        highlightcolor="black", highlightthickness=1)
        cell.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Armazena a carta no frame para acesso posterior
        cell.carta_data = carta

        # Nome da carta
        tk.Label(
            cell,
            text=f"{carta['name']} - {carta['sequence']}",
            font=('Calibri 10'),
            bg='white',
            wraplength=180
        ).pack(side="top", pady=5)

        # Imagem da carta
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((75, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(cell, image=photo, bg='black')
            img_label.image = photo
            img_label.pack(side="bottom", pady=5)
        except FileNotFoundError:
            error_label = tk.Label(cell, text="Imagem não encontrada", bg='white')
            error_label.pack(side="bottom", pady=5)
            img_label = None

        # Torna toda a célula clicável
        cell.bind("<Button-1>", lambda e, c=carta: self.show_card_details(c))
        if img_label:
            img_label.bind("<Button-1>", lambda e, c=carta: self.show_card_details(c))

        # Efeito hover
        cell.bind("<Enter>", lambda e, c=cell: c.config(highlightbackground="white"))
        cell.bind("<Leave>", lambda e, c=cell: c.config(highlightbackground="black"))

    def show_card_details(self, carta):
        """Exibe os detalhes da carta em uma janela popup"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detalhes da Carta: {carta['name']}")
        detail_window.geometry("600x900")
        detail_window.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(detail_window, bg="#708090")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nome da carta
        tk.Label(
            main_frame,
            text=f"{carta['name']} - {carta['sequence']}",
            font=('Arial 20 bold'),
            bg="#708090",
            fg="white",
            pady=10
        ).pack()

        # Imagem da carta (maior)
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((250, 450), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(main_frame, image=photo, bg="#000000")
            img_label.image = photo
            img_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(main_frame, text="Imagem não disponível",
                     bg="#708090", fg="white").pack()

        # Descrição da carta
        desc_frame = tk.Frame(main_frame, bg="#708090")
        desc_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            desc_frame,
            text="Significado:",
            font=('Arial 12 bold'),
            bg="#708090",
            fg="white",
            anchor="w"
        ).pack(fill="x")

        message_text = carta.get("message", str(carta['desc']).replace(".", ".\n"))
        tk.Label(
            desc_frame,
            text=message_text,
            font=("Arial 12"),
            bg="#708090",
            fg="white",
            wraplength=550,
            justify="left"
        ).pack(fill="x", pady=(0, 10))

        # Se tiver significado invertido
        if "rdesc" in carta:
            tk.Label(
                desc_frame,
                text="Significado Invertido:",
                font=('Arial 12 bold'),
                bg="#708090",
                fg="white",
                anchor="w"
            ).pack(fill="x")

            tk.Label(
                desc_frame,
                text=carta["rdesc"],
                font=("Arial 12"),
                bg="#708090",
                fg="white",
                wraplength=550,
                justify="left"
            ).pack(fill="x")

        # Botão de fechar
        tk.Button(
            detail_window,
            text="Fechar",
            command=detail_window.destroy,
            bg="#B0C4DE",
            fg="black",
            font=("Arial", 12),
            width=15
        ).pack(pady=10)

    def _add_mouse_scroll(self, canvas):
        """Adiciona suporte à rolagem com mouse"""

        def _on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            else:
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        canvas.bind_all("<Button-4>", _on_mouse_wheel)
        canvas.bind_all("<Button-5>", _on_mouse_wheel)

    def _remove_all_binds(self):
        """Remove todos os binds de teclado e mouse"""
        # Remove bind do ESC
        self.root.unbind('<Escape>')

        # Remove binds do mouse wheel
        if hasattr(self, 'mouse_binds'):
            for bind in self.mouse_binds:
                self.root.unbind_all(bind[0])

    def go_back(self):
        """Volta para a tela principal"""
        from views.main_view import Application
        self.clear_frame()
        # Remove o binding do ESC para evitar múltiplas chamadas
        self._remove_all_binds()
        Application(self.root)

    def clear_frame(self):
        """Limpa todos os widgets exceto o background"""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()