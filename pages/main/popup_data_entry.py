
import ttkbootstrap as ttk
import tkinter as tk
import db.db_main.sales_db
from utils.assets_paths import asset_path
class PopupDataEntry:
    def __init__(self,title, subtitle, labels:list):
        self.labels = labels
        self.title = title
        self.subtitle = subtitle
        self.count_label = len(self.labels)
        self.vars = {}
        self.create_data_dict()


    def run(self):
        self.popup_window()
        self.create_grid()
        self.create_enteries()
        self.create_labels()
        self.create_subtitle(row=0, column=0, columnspan=4)


    def create_enteries(self):
        for index, var in enumerate(self.vars.values(), start=1):
            entry = ttk.Entry(self.window, textvariable=var, style="success", font="calibri 12 bold", width=40)
            entry.grid(row=index, column=2, columnspan=2, padx=20)
            if index == 1:
                entry.focus_set()


    def create_labels(self):
        for index, key in enumerate(self.vars.keys(), start=1):
            label = ttk.Label(self.window, text=key, style="light", font="calibri 13 bold")
            label.grid(row=index, column=1, sticky="e")

    def create_grid(self):
        self.window.grid_columnconfigure((0,1,2,3), weight=1, uniform="a")

        # grid for title
        self.window.grid_rowconfigure(0, weight=2, uniform="a")

        # grid for submit button
        self.window.grid_rowconfigure(self.count_label +1, weight=2, uniform="a")

        for row in range(1, self.count_label +1):
            self.window.grid_rowconfigure(row, pad=25, uniform="a")


    def submit_button(self, cmd=None):
        button = ttk.Button(self.window, text="Submit", width=25, cursor="hand2", command=cmd, style="warning-Outline")
        button.grid(row=self.count_label+1, column=0, columnspan=4)

    def center_window(self):
        self.window.update_idletasks()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        x_pos = (screen_width // 2 ) - (width // 2)
        y_pos = ((screen_height -70) // 2 ) - (height // 2)
        self.window.geometry(f"+{x_pos}+{y_pos}")

    def popup_window(self):
        self.window = ttk.Toplevel(title=self.title)
        self.window.focus_set()
        self.window.resizable(False, False)
        self.window.iconbitmap(False, asset_path("logo.ico"))

        self.create_subtitle(row=0, column=0, columnspan=4)
        self.window.grab_set()

    def create_subtitle(self, **options):
        subtitle = ttk.Label(self.window, text=self.subtitle, font="calibri 24 bold", style="danger")
        subtitle.grid(**options)

    def create_data_dict(self):
        for label in self.labels:
            self.vars[label] = tk.StringVar()


    def get_data(self):
        return {key: var.get() for key, var in self.vars.items()}

    def list_box(self, entry_var_name: str):

        self.entry_var_name = entry_var_name

        # إنشاء ليست بوكس
        self.listbox = tk.Listbox(self.window, height=5, cursor="hand2")
        self.listbox.grid(row=0, column=2, columnspan=2, padx=30, sticky="we")
        self.listbox.bind("<<ListboxSelect>>", self.fill_entry_from_listbox)

        # ربط الـ Entry بالكتابة
        entry_var = self.vars[self.entry_var_name]
        self.trace_id = entry_var.trace_add("write", self.update_listbox)

        # مبدئياً نخفي الليست بوكس
        self.listbox.grid_remove()

    def update_listbox(self, *args):

        typed = self.vars[self.entry_var_name].get().lower()

        if typed == "":
            self.listbox.grid_remove()
        else:
            suggestions = db.db_main.sales_db.SalesDBLogic().search(typed)
            filtered = [item.product_name for item in suggestions if typed in item.product_name.lower()]
            self.listbox.delete(0, tk.END)

            for item in filtered:
                self.listbox.insert(tk.END, item)

            if filtered:
                self.listbox.grid()
            else:
                self.listbox.grid_remove()

    def fill_entry_from_listbox(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected_text = self.listbox.get(selection[0])
            self.vars[self.entry_var_name].set(selected_text)
            self.listbox.grid_remove()








