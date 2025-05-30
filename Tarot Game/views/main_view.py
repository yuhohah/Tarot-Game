import tkinter as tk

from PIL import ImageTk, Image
from utils.resource_path import resource_path


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
            "bg": "#B0C4DE",
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "relief": "raised",
            "bd": 5,
            "highlightthickness": 2,
            "highlightbackground": "black",
        }

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

        self.apply_hover_effect(btnstart, "#696969", "#B0C4DE")
        self.apply_hover_effect(btncards, "#696969", "#B0C4DE")

    def apply_hover_effect(self, button, hover_color, original_color):
        def on_enter(event):
            button['bg'] = hover_color

        def on_leave(event):
            button['bg'] = original_color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def on_click_btnstart(self):
        from views.game_view import GameView
        self.clear_frame()
        GameView(self.root)

    def on_click_btncards(self):
        from views.deck_view import DeckView
        self.clear_frame()
        DeckView(self.root)