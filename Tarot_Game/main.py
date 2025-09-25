import tkinter as tk
#Ola
from views.main_view import Application

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()