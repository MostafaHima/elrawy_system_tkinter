import ttkbootstrap as ttk
import tkinter as tk
import os

class Window(ttk.Window):
    def __init__(self):
        super().__init__(themename="solar")
        self.center_window()
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.title("El-Rawy Bookstore")
        self.iconbitmap(False, os.path.join("assets", "logo.ico"))



    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = screen_width - 100
        height = screen_height - 150

        x_pos = (screen_width // 2) - (width // 2)
        y_pos = ((screen_height - 70) // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")