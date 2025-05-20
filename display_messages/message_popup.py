from tkinter import ttk
from ttkbootstrap import Toplevel
import ttkbootstrap as ttk
import tkinter as tk
import os

class MessagePopup(Toplevel):
    def __init__(self,root, subtitle, title, message, style):
        super().__init__()
        self.cmd = self.destroy

        self.root = root
        self.message = message
        self.text_title = title
        self.text_style = style
        self.iconbitmap(False, os.path.join("assets", "logo.ico"))


        self.title(subtitle)
        self.resizable(False, False)


        title = ttk.Label(self, text= self.text_title, font="calibri 18 bold", style=self.text_style)
        title.pack(padx=50, pady=20)

        message = ttk.Label(self, text=self.message, font="calibri 12 bold", style="light")
        message.pack(padx=50, )

        button = ttk.Button(self, text="OK", style="warning-Outline", width=20,  padding=10, cursor="hand2", command=self.cmd)
        button.pack(padx=50, pady=35)
        self.bind("<Return>", lambda evnet :self.cmd())
        self.grab_set()
        self.focus_set()

        self.center_window()


    def center_window(self):
        self.update_idletasks()

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2 ) - (window_width // 2)
        y = ((screen_height -70) // 2) - (window_height // 2)

        self.geometry(f"+{x}+{y}")


