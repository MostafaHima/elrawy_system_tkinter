
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from widgets.action_buttons import ActionButtons

class BasePage:
    def __init__(self, root, title):
        self.root = root
        self.title = title
        self.frame = ttk.Frame(self.root)
        self.action_buttons = ActionButtons(self.root, self.frame)


    def create_tree_view(self, columns_name):
        tree = ttk.Treeview(self.frame, columns=columns_name, show="headings", style="info.Treeview",)
        self.style_treeview(tree)
        tree.grid(row=1, column=0, sticky="nswe", columnspan=3)
        return tree

    def set_headings(self, tree, columns_name):
        for column in columns_name:
            tree.heading(column, text=column)

    def set_columns(self, tree, columns):
        width = (self.root.winfo_screenwidth() // len(columns)) -30
        auto_resize_column = self.expand_columns(tree, width)

        for  column in columns:
            tree.column(column, width=width, anchor="center", stretch=True)
        tree.bind("<Double-Button-1>", auto_resize_column)


    def set_title(self, font:str, style:str):
        title = ttk.Label(self.frame, text=self.title, font=font,style=style)
        title.grid(row=0, column=1, sticky="ns")

    def back_btn(self, command):
        icon = Image.open(r"E:\Tkinter Projects\Elrawy_bookstore\assets\back_icon.png")
        resized = icon.resize((50, 50), Image.Resampling.LANCZOS)
        back_icon = ImageTk.PhotoImage(resized)
        btn = ttk.Button(self.frame, image=back_icon, cursor="hand2", style="darkly-Outline", command=command)
        btn.image = back_icon
        btn.grid(row=0, column=0, sticky="w", padx=15)

    def create_grid(self,):
        self.frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(1, weight=5, uniform="a")
        self.frame.grid_rowconfigure(2, weight=2, uniform='a')

    def place_frame(self, relwidth, relheight):
        self.frame.place(relwidth=relwidth, relheight=relheight)

    def style_treeview(self, tree):

        style = ttk.Style()
        background = style.lookup("Treeview", "selectbackground")

        style.configure("info.Treeview",
                        foreground="white",
                        rowheight=40,)

        style.configure("writtenRow.Treeview", background="#555555", foreground="black")
        tree.tag_configure("written", background=background, font=("Tahoma", 10, "bold"))

        style.configure("info.Treeview.Heading", font=("calibri", 12, "bold"))
        style.map("Treeview", background=[('selected', 'lightblue')])



    def expand_columns(self, tree, width):
        reminder_column = ""
        def auto_resize_column(event):
            nonlocal reminder_column
            col = tree.identify_column(event.x)
            if col and col != "#0":

                if reminder_column == col:
                    new_width = width
                    reminder_column = ""
                else:
                    reminder_column = col
                    new_width = int(width * 2)
                tree.column(col, width=new_width)
        return auto_resize_column
