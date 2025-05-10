
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from themes.app_theme import AppTheme


class AuthBase:
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title

        self.frame = ttk.Frame(self.parent)
        self.child_frame = tk.Frame(self.frame, highlightcolor="orange",highlightbackground='gray', highlightthickness=1, relief="solid")
        self.child_frame.grid(row=2, column=0, padx=200,sticky="nswe", columnspan=2, pady=50, ipady=100)
        self.take_facous = None


        self.vars = {
            "Username": tk.StringVar(),
            "Email": tk.StringVar(),
            "Password": tk.StringVar()
        }
        AppTheme()

    def create_entries(self):
        for row_index, (label ,var) in enumerate(self.vars.items(), start=1):
            entry_opts = {"textvariable": var}
            if label.lower() == "password":
                entry_opts["show"] = "*"

            entry = ttk.Entry(self.child_frame, **entry_opts, width=50, font=("calibri", 12, "bold"), style="success")
            entry.grid(row=row_index, column=2, sticky="wns", columnspan=2, pady=10)
            if row_index == 1:
                self.take_facous = entry.focus_set()


    def create_labels(self):
        for row_index, text in enumerate(self.vars.keys(), start=1):
            lables = ttk.Label(self.child_frame, text=text, style="light", font="calibri 13 bold")
            lables.grid(row=row_index, column=1,)


    def create_main_button(self, text, cmd=None):
        main_button = ttk.Button(self.child_frame, text=text, cursor="hand2", command=cmd, width=40, style="warning-Outline", padding=10)
        main_button.grid(row=4, column=0, columnspan=3, sticky="s",)

    def create_forget_button(self, cmd=None):
        forget_button = ttk.Button(self.child_frame, text="Forget your password ?", cursor="hand2", command=cmd, style="warning-link")
        forget_button.grid(row=5, column=0, columnspan=3, sticky="n", pady=5)

    def set_title(self):
        title = ttk.Label(self.child_frame, text=self.title, font="Calibri 22 bold", style="info")
        title.grid(row=0, column=0, columnspan=3)

    def set_logo(self):
        screen_w, screen_h = self.get_window_size()
        img_width = int(screen_w * 0.25)
        img_height = int(screen_h * 0.25)

        img = Image.open(r"E:\Tkinter Projects\Elrawy_bookstore\assets\el_raway_logo2.png")
        img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)  # جودة عالية

        logo_img = ImageTk.PhotoImage(img)  # احفظ الصورة عشان ماتمسحش من الذاكرة

        canvas = tk.Canvas(self.frame, width=img_width, height=img_height, highlightthickness=0)

        canvas.create_image(img_width // 2, img_height // 2, image=logo_img)
        canvas.image = logo_img
        canvas.grid(row=0, column=0, rowspan=2, columnspan=3)

    def switch_frames_button(self, text, cmd=None, state="enable"):
        button = ttk.Button(self.frame, text=text, cursor="hand2", command=cmd, style="warning-Outline", padding=10, width=15, state=state)
        button.grid(row=0, column=1, sticky="e", padx=20,)



    def set_main_grid(self):
        self.frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(1, weight=1, uniform="a")
        self.frame.grid_rowconfigure(2, weight=6, uniform="a")

        self.frame.grid_columnconfigure(0, weight=2, uniform="a")
        self.frame.grid_columnconfigure(1, weight=1, uniform="a")



    def set_child_grid(self):
        self.child_frame.grid_rowconfigure(0, weight=2, uniform="a")
        self.child_frame.grid_rowconfigure((1, 2, 3), pad=10, uniform="a")
        self.child_frame.grid_rowconfigure((4, 5), weight=1, uniform="a")


        self.child_frame.grid_columnconfigure(0, weight=1, uniform="a")
        self.child_frame.grid_columnconfigure(1, weight=1, uniform="a")
        self.child_frame.grid_columnconfigure(2, weight=2, uniform="a")


    def place_main_frame(self):
        self.frame.place(relwidth=1, relheight=1)

    def get_inputs(self):
        return {key: var.get() for key, var in self.vars.items()}

    def get_window_size(self):
        width = self.parent.winfo_screenwidth()
        height = self.parent.winfo_screenheight()
        return width, height

    def clear_entries(self):
        for var in self.vars.values():
            var.set("")




