import tkinter as tk
from PIL import ImageTk, Image
from utils.resource_path import resource_path

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('Tarot')
        self.root.geometry("1320x700")
        self.root.resizable(True, True)
        self.show_cards_immediately = True 

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        self.setup_background()
        self.setup_grid()
        self.create_initial_buttons()
        self.update_config_button_style()

    def setup_background(self):
        bg_image_path = resource_path("images/background.jpg")
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((1320, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

    def setup_grid(self):
        total_columns = 5
        total_rows = 4
        for i in range(total_columns):
            self.root.columnconfigure(i, weight=1)
        for i in range(total_rows):
            self.root.rowconfigure(i, weight=1)

    def clear_frame(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()

    def create_initial_buttons(self):
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

        config_style = {
            "width": 3,        
            "height": 2,          
            "bg": "#1a1a2e",      
            "fg": "#d4af37",        
            "font": ("Georgia", 16, "bold"),  
            "relief": "flat",
            "bd": 0,
            "activebackground": "#2a2a4e",
            "activeforeground": "#f1e5ac",
            "cursor": "hand2",
            "text": "⚙️",         
        }

        self.btnconfig = tk.Button(
            self.root,
            command=self.on_click_btnconfig,
            **config_style,
        )
        self.btnconfig.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        title_label = tk.Label(
            self.root,
            text="T A R O T",
            font=("Georgia", 48, "bold"),
            bg="#0b0b14", # Very dark color to blend with typical night sky background
            fg="#d4af37",
            padx=20, pady=10
        )
        title_label.grid(row=1, column=2, pady=30)

        btnstart = tk.Button(
            self.root,
            text="Start",
            command=self.on_click_btnstart,
            **style,
        )
        btnstart.grid(row=2, column=2, pady=10)

        btncards = tk.Button(
            self.root,
            text="Cards",
            command=self.on_click_btncards,
            **style,
        )
        btncards.grid(row=3, column=2, pady=10)

        self.apply_hover_effect(btnstart, "#2a2a4e", "#1a1a2e")
        self.apply_hover_effect(btncards, "#2a2a4e", "#1a1a2e")
        self.apply_hover_effect(self.btnconfig, "#2a2a4e", "#1a1a2e")

    def apply_hover_effect(self, button, hover_color, original_color):
        def on_enter(event):
            button['bg'] = hover_color

        def on_leave(event):
            button['bg'] = original_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def update_config_button_style(self):
        if hasattr(self, 'btnconfig'):
            if self.show_cards_immediately:
                self.btnconfig.config(text="⚙️", bg="#1a1a2e")  # Normal gear
            else:
                self.btnconfig.config(text="🎭", bg="#d4af37", fg="#1a1a2e")  # Gold background for active state

    def on_click_btnconfig(self):
        """Toggle between reveal modes"""
        self.show_cards_immediately = not self.show_cards_immediately
        self.update_config_button_style()
        print(self.show_cards_immediately)

    def on_click_btnstart(self):
        from views.game_view import GameView
        self.clear_frame()
        GameView(self.root, self)

    def on_click_btncards(self):
        from views.deck_view import DeckView
        self.clear_frame()
        DeckView(self.root, self)