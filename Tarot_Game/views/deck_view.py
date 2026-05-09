import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from models.deck import Deck
from utils.resource_path import resource_path

class DeckView:
    def __init__(self, root, app_instance):
        self.root = root
        self.app_instance = app_instance
        from models.deck_manager import DeckManager
        self.deck_manager = DeckManager()
        self.background_label = None
        self.setup_ui()

        self.root.bind('<Escape>', lambda e: self.go_back())

    def setup_ui(self):
        self.setup_background()
        self.view_mode = "estado_atual"
        self.setup_topbar()
        self.content_frame = tk.Frame(self.root, bg="#121212")
        self.content_frame.pack(side="top", fill="both", expand=True)
        self.deck_list()

    def setup_topbar(self):
        topbar = tk.Frame(self.root, bg="#0b0b14", pady=10)
        topbar.pack(side="top", fill="x")
        
        btn_atual = tk.Button(
            topbar, text="Estado Atual", command=lambda: self.change_mode("estado_atual"),
            bg="#1a1a2e", fg="#d4af37", font=("Georgia", 12, "bold"), relief="flat", cursor="hand2"
        )
        btn_atual.pack(side="left", padx=20)
        
        btn_original = tk.Button(
            topbar, text="Ordem Original", command=lambda: self.change_mode("ordem_original"),
            bg="#1a1a2e", fg="#d4af37", font=("Georgia", 12, "bold"), relief="flat", cursor="hand2"
        )
        btn_original.pack(side="left", padx=20)
        
        btn_voltar = tk.Button(
            topbar, text="Menu", command=self.go_back,
            bg="#1a1a2e", fg="#d4af37", font=("Georgia", 12, "bold"), relief="flat", cursor="hand2"
        )
        btn_voltar.pack(side="right", padx=20)
        
        self._add_hover(btn_atual)
        self._add_hover(btn_original)
        self._add_hover(btn_voltar)

    def _add_hover(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg="#2a2a4e", fg="#f1e5ac"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#1a1a2e", fg="#d4af37"))

    def change_mode(self, mode):
        self.view_mode = mode
        for widget in self.content_frame.winfo_children():
            widget.destroy()
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
        
        all_cards = []
        if self.view_mode == "estado_atual":
            for drawn in self.deck_manager.drawn_cards:
                c = drawn[0].copy()
                c['is_drawn'] = True
                c['is_reversed'] = (drawn[1] == 1)
                all_cards.append(c)
                
            for card in self.deck_manager.deck:
                c = card.copy()
                c['is_drawn'] = False
                c['is_reversed'] = card.get('is_reversed', 0) == 1
                all_cards.append(c)
        else:
            from models.deck import Deck
            deck_orig = Deck.get_deck()
            for card in deck_orig:
                c = card.copy()
                c['is_drawn'] = False
                c['is_reversed'] = False
                all_cards.append(c)

        colunas = 9
        linhas = (len(all_cards) // colunas) + (1 if len(all_cards) % colunas != 0 else 0)

        canvas = tk.Canvas(self.content_frame, bg="#121212")
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#121212", height=700, width=1320)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._add_mouse_scroll(canvas)

        for index, carta in enumerate(all_cards):
            row, column = divmod(index, colunas)
            self._create_card_cell(scrollable_frame, carta, row, column)

    def _create_card_cell(self, parent, carta, row, column):
        """Cria uma célula clicável para cada carta"""
        cell = tk.Frame(parent, bg='#0b0b14', highlightbackground="#1a1a2e",
                        highlightcolor="#d4af37", highlightthickness=2, cursor="hand2")
        cell.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Armazena a carta no frame para acesso posterior
        cell.carta_data = carta

        # Nome da carta
        drawn_text = " (Drawn)" if carta.get('is_drawn') else ""
        reversed_text = " (Rev)" if carta.get('is_reversed') else ""
        
        tk.Label(
            cell,
            text=f"{carta['name']} - {carta['sequence']}{drawn_text}{reversed_text}",
            font=('Georgia', 10, 'bold'),
            bg='#0b0b14',
            fg="#ff6b35" if carta.get('is_drawn') else "#d4af37",
            wraplength=180,
            cursor="hand2"
        ).pack(side="top", pady=5)

        # Imagem da carta
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((75, 150), Image.LANCZOS)
            if carta.get('is_reversed'):
                image = image.rotate(180)
            photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(cell, image=photo, bg='#0b0b14', cursor="hand2")
            img_label.image = photo
            img_label.pack(side="bottom", pady=5)
        except FileNotFoundError:
            error_label = tk.Label(cell, text="Imagem não encontrada", bg='#0b0b14', fg="#e6e6fa")
            error_label.pack(side="bottom", pady=5)
            img_label = None

        # Torna toda a célula clicável
        cell.bind("<Button-1>", lambda e, c=carta: self.show_card_details(c))
        if img_label:
            img_label.bind("<Button-1>", lambda e, c=carta: self.show_card_details(c))

        # Efeito hover
        cell.bind("<Enter>", lambda e, c=cell: c.config(highlightbackground="#d4af37"))
        cell.bind("<Leave>", lambda e, c=cell: c.config(highlightbackground="#1a1a2e"))

    def show_card_details(self, carta):
        """Exibe os detalhes da carta em uma janela popup"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detalhes da Carta: {carta['name']}")
        detail_window.geometry("600x900")
        detail_window.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(detail_window, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nome da carta
        drawn_text = " (Comprada)" if carta.get('is_drawn') else ""
        reversed_text = " (Revertida)" if carta.get('is_reversed') else ""
        tk.Label(
            main_frame,
            text=f"{carta['name']} - {carta['sequence']}{drawn_text}{reversed_text}",
            font=('Georgia', 24, 'bold'),
            bg="#121212",
            fg="#ff6b35" if carta.get('is_drawn') else "#d4af37",
            pady=10
        ).pack()

        # Imagem da carta (maior)
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((250, 450), Image.LANCZOS)
            if carta.get('is_reversed'):
                image = image.rotate(180)
            photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(main_frame, image=photo, bg="#000000")
            img_label.image = photo
            img_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(main_frame, text="Imagem não disponível",
                     bg="#121212", fg="#e6e6fa").pack()

        # Descrição da carta
        if not carta.get('is_reversed'):
            desc_frame = tk.Frame(main_frame, bg="#121212")
            desc_frame.pack(fill="x", padx=20, pady=10)
    
            tk.Label(
                desc_frame,
                text="Significado:",
                font=('Georgia', 16, 'bold'),
                bg="#121212",
                fg="#d4af37",
                anchor="w"
            ).pack(fill="x")
    
            message_text = carta.get("message", str(carta['desc']).replace(".", ".\n"))
            tk.Label(
                desc_frame,
                text=message_text,
                font=("Georgia", 14),
                bg="#121212",
                fg="#e6e6fa",
                wraplength=550,
                justify="left"
            ).pack(fill="x", pady=(0, 10))
        else:

        # Se tiver significado invertido
            desc_frame = tk.Frame(main_frame, bg="#121212")
            desc_frame.pack(fill="x", padx=20, pady=10)
            
            if "rdesc" in carta:
                tk.Label(
                desc_frame,
                text="Significado Invertido:",
                font=('Georgia', 16, 'bold'),
                bg="#121212",
                fg="#d4af37",
                anchor="w"
            ).pack(fill="x")

            tk.Label(
                desc_frame,
                text=carta["rdesc"],
                font=("Georgia", 14),
                bg="#121212",
                fg="#e6e6fa",
                wraplength=550,
                justify="left"
            ).pack(fill="x")

        # Botão de fechar
        tk.Button(
            detail_window,
            text="Fechar",
            command=detail_window.destroy,
            bg="#1a1a2e",
            fg="#d4af37",
            font=("Georgia", 14, "bold"),
            relief="flat",
            activebackground="#2a2a4e",
            activeforeground="#f1e5ac",
            cursor="hand2",
            width=15
        ).pack(pady=20)

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
        self.clear_frame()
        # Remove o binding do ESC para evitar múltiplas chamadas
        self._remove_all_binds()
        self.app_instance.show_main_menu()

    def clear_frame(self):
        """Limpa todos os widgets exceto o background"""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()