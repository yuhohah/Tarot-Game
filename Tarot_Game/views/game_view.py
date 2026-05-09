import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from models.deck_manager import DeckManager
from utils.resource_path import resource_path

class GameView:
    def __init__(self, root, app_instance):
        self.root = root
        self.app_instance = app_instance
        self.deck_manager = DeckManager()
        self.btn1 = None
        self.btn2 = None
        self.btn_shuffle = None
        self.background_label = None  # Referência ao background
        self.root.bind('<Escape>', lambda e: self.go_back())
        self.show_cards_immediately = app_instance.show_cards_immediately
        self.setup_ui()

    def setup_ui(self):
        self.setup_background()
        self.setup_grid()
        self.create_menu_button()
        self.create_buttons_game()

    def create_menu_button(self):
        """Botão fixo de Menu no canto superior direito"""
        self.btn_voltar_menu = tk.Button(
            self.root, text="Menu", command=self.go_back,
            bg="#1a1a2e", fg="#d4af37", font=("Georgia", 12, "bold"), relief="flat", cursor="hand2",
            padx=15, pady=5
        )
        self.btn_voltar_menu.grid(row=0, column=4, sticky="ne", padx=10, pady=5)
        self.apply_hover_effect(self.btn_voltar_menu, "#2a2a4e", "#1a1a2e")

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
        # 5 columns: col 0 (empty), col 1,2,3 (cards), col 4 (menu btn)
        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        # Rows: 0 = menu btn, 1 = card titles, 2 = card images, 3 = action btns, 4 = limpar, 5 = embaralhar
        self.root.rowconfigure(0, weight=0)  # compact menu row
        for i in range(1, 6):
            self.root.rowconfigure(i, weight=1)

    def create_restart_button(self):
        """Cria o botão de Novo Jogo"""
        style = {
            "width": 20,
            "height": 2,
            "bg": "#1a1a2e",
            "fg": "#d4af37",
            "font": ("Georgia", 14, "bold"),
            "relief": "flat",
            "bd": 0,
            "activebackground": "#2a2a4e",
            "activeforeground": "#f1e5ac",
            "cursor": "hand2",
        }

        self.restart_btn = tk.Button(
            self.root,
            text="Limpar Mesa",
            command=self.restart_game,
            **style
        )
        self.restart_btn.grid(row=5, column=2, pady=10, padx=10, sticky="nsew")
        self.apply_hover_effect(self.restart_btn, "#2a2a4e", "#1a1a2e")

    def restart_game(self):
        """Limpa as cartas da mesa sem sair do jogo"""
        self.clear_frame()
        # Reset row/column configs before re-setup
        for i in range(5):
            self.root.columnconfigure(i, weight=0)
        for i in range(6):
            self.root.rowconfigure(i, weight=0)
        self.setup_ui()

    def create_buttons_game(self):
        style = {
            "width": 14,
            "height": 1,
            "bg": "#1a1a2e",
            "fg": "#d4af37",
            "font": ("Georgia", 12, "bold"),
            "relief": "flat",
            "bd": 0,
            "activebackground": "#2a2a4e",
            "activeforeground": "#f1e5ac",
            "cursor": "hand2",
        }

        self.btn1 = tk.Button(
            self.root,
            text="Uma Carta",
            command=self.on_click_btn1,
            **style
        )
        self.btn1.grid(row=3, column=2, pady=10, padx=10, sticky="nsew")
        self.apply_hover_effect(self.btn1, "#2a2a4e", "#1a1a2e")

        self.btn2 = tk.Button(
            self.root,
            text="Três Cartas",
            command=self.on_click_btn3,
            **style
        )
        self.btn2.grid(row=4, column=2, pady=10, padx=10, sticky="nsew")
        self.apply_hover_effect(self.btn2, "#2a2a4e", "#1a1a2e")

        self.btn_shuffle = tk.Button(
            self.root,
            text="Embaralhar",
            command=self.shuffle_deck_action,
            **style
        )
        self.btn_shuffle.grid(row=5, column=2, pady=10, padx=10, sticky="nsew")
        self.apply_hover_effect(self.btn_shuffle, "#2a2a4e", "#1a1a2e")

    def shuffle_deck_action(self):
        """Embaralha o deck com animação"""
        import threading
        import time

        # Disable button to prevent double-click
        self.btn_shuffle.config(state="disabled", text="Embaralhando...")

        # --- Full-screen overlay ---
        overlay = tk.Frame(self.root, bg="#0b0b14")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lift()

        SYMBOLS = ["\U0001f0c0", "\U0001f0cf", "\U0001f0a1", "\U0001f0b1", "\U0001f0c1",
                   "\U0001f0a2", "\U0001f0b2", "\U0001f0c2"]

        symbol_label = tk.Label(
            overlay, text="\U0001f0cf",
            font=("Georgia", 96), bg="#0b0b14", fg="#d4af37"
        )
        symbol_label.pack(expand=True, pady=(80, 0))

        status_label = tk.Label(
            overlay,
            text="Embaralhando o baralho com\nentropia qu\u00e2ntica...",
            font=("Georgia", 18, "italic"),
            bg="#0b0b14", fg="#e6e6fa"
        )
        status_label.pack(pady=10)

        dots_label = tk.Label(
            overlay, text="", font=("Georgia", 24), bg="#0b0b14", fg="#d4af37"
        )
        dots_label.pack(pady=5)

        self._shuffle_done = False
        self._shuffle_started_at = time.time()
        self._anim_idx = [0]
        self._dot_idx = [0]

        def animate():
            if not overlay.winfo_exists():
                return
            self._anim_idx[0] = (self._anim_idx[0] + 1) % len(SYMBOLS)
            symbol_label.config(text=SYMBOLS[self._anim_idx[0]])

            self._dot_idx[0] = (self._dot_idx[0] + 1) % 4
            dots_label.config(text="\u2022" * self._dot_idx[0] + "\u25e6" * (3 - self._dot_idx[0]))

            elapsed = time.time() - self._shuffle_started_at
            if self._shuffle_done and elapsed >= 3.0:
                overlay.destroy()
                if self.btn_shuffle.winfo_exists():
                    self.btn_shuffle.config(state="normal", text="Embaralhar")
            else:
                self.root.after(250, animate)

        def do_shuffle():
            self.deck_manager.shuffle_deck()
            self._shuffle_done = True

        threading.Thread(target=do_shuffle, daemon=True).start()
        animate()

    def apply_hover_effect(self, button, hover_color, original_color):
        def on_enter(event):
            button['bg'] = hover_color

        def on_leave(event):
            button['bg'] = original_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def animate_card_draw(self, carta, column, reversed, callback):
        """
        Card-flip animation: squeezes a card-back to nothing,
        then expands the real card front from the center outward.
        """
        TARGET_W, TARGET_H = 175, 340
        STEPS = 8
        DELAY = 35  # ms per frame

        # Show face-down placeholder
        placeholder = tk.Label(
            self.root, text="\U0001f0cf",
            font=("Georgia", 64), bg="#1a1a2e", fg="#d4af37",
            width=8, height=8, relief="flat"
        )
        placeholder.grid(row=2, column=column, pady=10, sticky="n")

        # Pre-load the real card image
        try:
            image_path = resource_path(carta['image'])
            base_image = Image.open(image_path).resize((TARGET_W, TARGET_H), Image.LANCZOS)
            if reversed:
                base_image = base_image.rotate(180)
        except FileNotFoundError:
            placeholder.destroy()
            callback()
            return

        back_color = Image.new("RGB", (TARGET_W, TARGET_H), "#1a1a2e")
        shrink_steps = [max(1, int(TARGET_W * (1 - i / STEPS))) for i in range(STEPS + 1)]
        grow_steps   = [max(1, int(TARGET_W * i / STEPS)) for i in range(1, STEPS + 1)]
        reveal_label = tk.Label(self.root, bg="#000000")

        def phase1(idx=0):
            if not placeholder.winfo_exists():
                return
            w = shrink_steps[idx]
            img = ImageTk.PhotoImage(back_color.resize((w, TARGET_H), Image.LANCZOS))
            placeholder.config(image=img, text="", width=w, height=TARGET_H)
            placeholder.image = img
            if idx < len(shrink_steps) - 1:
                self.root.after(DELAY, lambda: phase1(idx + 1))
            else:
                placeholder.destroy()
                reveal_label.grid(row=2, column=column, pady=10, sticky="n")
                self.root.after(DELAY, lambda: phase2(0))

        def phase2(idx=0):
            if not reveal_label.winfo_exists():
                return
            w = grow_steps[idx]
            photo = ImageTk.PhotoImage(base_image.resize((w, TARGET_H), Image.LANCZOS))
            reveal_label.config(image=photo)
            reveal_label.image = photo
            if idx < len(grow_steps) - 1:
                self.root.after(DELAY, lambda: phase2(idx + 1))
            else:
                reveal_label.destroy()
                callback()

        phase1()

    def display_card_title(self, carta, column, reversed=False):
        """Shows just the card title above the animation area."""
        nomedacarta = tk.Label(
            self.root,
            text=f"{carta['name']} - {carta['sequence']}" + (" (Revertida)" if reversed else ""),
            font=('Georgia', 18, 'bold'),
            bg="#0b0b14", fg="#d4af37",
            padx=10, pady=5, cursor="hand2",
            wraplength=220, height=2
        )
        nomedacarta.grid(row=1, column=column, pady=10, sticky="n")
        nomedacarta.bind("<Button-1>", lambda e, c=carta, r=reversed: self.show_card_details(c, r))

    def display_card(self, carta, column, reversed=False):
        nomedacarta = tk.Label(
            self.root,
            text=f"{carta['name']} - {carta['sequence']}" + (" (Revertida)" if reversed else ""),
            font=('Georgia', 18, 'bold'),
            bg="#0b0b14",
            fg="#d4af37",
            padx=10, pady=5,
            cursor="hand2",
            wraplength=220,
            height=2
        )
        nomedacarta.grid(row=1, column=column, pady=10, sticky="n")

        label = None
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((175, 340), Image.LANCZOS)
            if reversed:
                image = image.rotate(180)
            image = ImageTk.PhotoImage(image)
            label = tk.Label(self.root, image=image, bg="#000000", cursor="hand2")
            label.image = image
            label.grid(row=2, column=column, pady=10, sticky="n")
        except FileNotFoundError:
            print(f"Erro: Imagem da carta {carta['image']} não encontrada.")

        # Bind click events
        nomedacarta.bind("<Button-1>", lambda e, c=carta, r=reversed: self.show_card_details(c, r))
        if label:
            label.bind("<Button-1>", lambda e, c=carta, r=reversed: self.show_card_details(c, r))

    def display_card_hidden(self, carta, column, reversed=False):
        btn_reveal = tk.Button(
            self.root,
            text="Revelar\nCarta",
            command=lambda: self.reveal_card(carta, column, reversed, btn_reveal),
            bg="#1a1a2e", fg="#d4af37", font=("Georgia", 14, "bold"),
            width=12, height=15, relief="flat", cursor="hand2",
            activebackground="#2a2a4e", activeforeground="#f1e5ac"
        )
        btn_reveal.grid(row=2, column=column, pady=10, sticky="n")
        self.apply_hover_effect(btn_reveal, "#2a2a4e", "#1a1a2e")

    def reveal_card(self, carta, column, reversed, btn_reveal):
        btn_reveal.destroy()
        self.display_card(carta, column, reversed)

    def show_card_details(self, carta, reversed=False):
        """Exibe os detalhes da carta em uma janela popup"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detalhes da Carta: {carta['name']}")
        detail_window.geometry("600x900")
        detail_window.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(detail_window, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nome da carta
        tk.Label(
            main_frame,
            text=f"{carta['name']} - {carta['sequence']}",
            font=('Georgia', 24, 'bold'),
            bg="#121212",
            fg="#d4af37",
            pady=10
        ).pack()

        # Imagem da carta (maior)
        try:
            image_path = resource_path(carta['image'])
            image = Image.open(image_path)
            image = image.resize((250, 450), Image.LANCZOS)
            if reversed:
                image = image.rotate(180)
            photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(main_frame, image=photo, bg="#000000")
            img_label.image = photo
            img_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(main_frame, text="Imagem não disponível",
                     bg="#121212", fg="#e6e6fa").pack()

        # Descrição da carta
        if not reversed:
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

    def remove_buttons(self):
        """Remove os botões da tela"""
        if self.btn1:
            self.btn1.destroy()
        if self.btn2:
            self.btn2.destroy()
        if self.btn_shuffle:
            self.btn_shuffle.destroy()

    def on_click_btn1(self):
        cart = self.deck_manager.get_card()
        if not cart:
            messagebox.showinfo("Fim do Baralho", "Não há mais cartas no baralho! Por favor, clique em 'Embaralhar'.")
            return
            
        carta = cart[0]
        rev = cart[1] == 1

        self.remove_buttons()
        self.display_card_title(carta, column=2, reversed=rev)

        def show():
            if self.show_cards_immediately:
                self.display_card(carta, column=2, reversed=rev)
            else:
                self.display_card_hidden(carta, column=2, reversed=rev)
            self.create_restart_button()

        self.animate_card_draw(carta, column=2, reversed=rev, callback=show)

    def on_click_btn3(self):
        cartas = []
        for _ in range(3):
            card = self.deck_manager.get_card()
            if card:
                cartas.append(card)
                
        if not cartas:
            messagebox.showinfo("Fim do Baralho", "Não há mais cartas no baralho! Por favor, clique em 'Embaralhar'.")
            return

        self.remove_buttons()

        # Show all titles first
        for i, cart in enumerate(cartas):
            self.display_card_title(cart[0], column=i + 1, reversed=(cart[1] == 1))

        # Chain animations in sequence
        def draw_sequence(idx=0):
            if idx >= len(cartas):
                self.create_restart_button()
                if len(cartas) < 3:
                    messagebox.showinfo("Fim do Baralho", "O baralho acabou antes de tirar todas as cartas! Por favor, clique em 'Limpar Mesa' e depois em 'Embaralhar'.")
                return
            cart = cartas[idx]
            carta = cart[0]
            rev = cart[1] == 1
            col = idx + 1

            def after_anim():
                if self.show_cards_immediately:
                    self.display_card(carta, column=col, reversed=rev)
                else:
                    self.display_card_hidden(carta, column=col, reversed=rev)
                self.root.after(150, lambda: draw_sequence(idx + 1))

            self.animate_card_draw(carta, column=col, reversed=rev, callback=after_anim)

        draw_sequence()

    def go_back(self):
        """Volta para a tela principal"""
        self.clear_frame()
        self.root.unbind('<Escape>')
        self.app_instance.show_main_menu()

    def clear_frame(self):
        """Limpa todos os widgets exceto o background"""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()