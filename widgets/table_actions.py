import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class ActionButtons:
    def __init__(self, root,  parent):
        self.parent = parent
        self.root = root

    def create_act_buttons(self, add_cmd=None, edit_cmd=None, delete_cmd=None):
        add_data = ttk.Button(self.parent, cursor="hand2", text="Add data", style="Success-Outline", command=add_cmd, takefocus=False)
        edit_data = ttk.Button(self.parent, cursor="hand2", text="Edit data", style="warning-Outline", command=edit_cmd, takefocus=False)
        delete_data = ttk.Button(self.parent, cursor="hand2", text="Delete data", style="danger-Outline", command=delete_cmd, takefocus=False)


        add_data.grid(row=2, column=2, sticky="nswe", padx=30, pady=30)
        edit_data.grid(row=2, column=1, sticky="nswe", padx=30, pady=30)
        delete_data.grid(row=2, column=0, sticky="nswe", padx=30, pady=30)




