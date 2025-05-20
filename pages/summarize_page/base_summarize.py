
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from typing import List

class BaseSummarizePage:
    def __init__(self, parent):
        self.parent = parent
        self.vars = {}

        self.frame = tk.Frame(self.parent, highlightcolor="orange", highlightbackground='orange', highlightthickness=1, relief="solid")
        self.label_count = 0

    def create_labels_and_values(self, labels: List[str]):

        for i, label_text in enumerate(labels, start=1):
            key = label_text.lower().replace(" ", "_").replace("-", "_")
            if label_text == "":
                continue
            self.vars[key] = tk.StringVar(value="0")

            ttk.Label(self.frame, text=label_text, style="light", font=("calibri", 10, "bold")).grid(row=i, column=0)

            values = tk.Label(self.frame, textvariable=self.vars[key], font=("calibri", 12, "bold"), )
            values.grid(row=i, column=1)

            ttk.Separator(self.frame, orient="horizontal", style="danger").grid(row=i, column=0, columnspan=2,
                                                                               sticky="sew", padx=20)
        self.label_count = len(labels)
    def create_button(self,text, cmd=None, state=None):
        button = ttk.Button(self.frame, text=text, padding=10, style="info-Outline", command=cmd, cursor="hand2", takefocus=False, state=state)
        button.grid(row=self.label_count +1, column=0, columnspan=2, pady=10)


    def set_frame_title(self, title):
        frame_title = ttk.Label(self.frame, text=title, style="info", font="calibri 13 bold")
        frame_title.grid(row=0, column=0, columnspan=2,)


    def configure_child_grid(self, button=False, menu=False):
        start = 1
        end = self.label_count +1

        self.frame.grid_columnconfigure(index=(0, 1), weight=1, uniform="a")
        self.frame.grid_rowconfigure(index=0, weight=1, uniform="a")

        for i in range(start, end):

            self.frame.grid_rowconfigure(index=i, weight=1, uniform="a")

        if button:
            self.frame.grid_rowconfigure(index=self.label_count + 1, weight=2, uniform="a")
        else:
            self.frame.grid_rowconfigure(index=self.label_count + 1, weight=1, uniform="a")


    def get_values(self):
        return {key: value.get() for key, value in self.vars.items()}













