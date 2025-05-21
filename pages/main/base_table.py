import os.path
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from widgets.table_actions import ActionButtons
from utils.assets_paths import asset_path

class BaseTable:
    def __init__(self, root, title):
        """
        Initializes the base table frame with a title and action buttons.
        """
        self.root = root
        self.title = title
        self.frame = ttk.Frame(self.root)
        self.action_buttons = ActionButtons(self.root, self.frame)

    def create_tree_view(self, column_names):
        """
        Creates a styled Treeview with the specified column names.
        """
        tree = ttk.Treeview(
            self.frame,
            columns=column_names,
            show="headings",
            style="info.Treeview"
        )
        self._style_treeview(tree)
        tree.grid(row=1, column=0, columnspan=3, sticky="nswe")
        return tree

    def set_headings(self, tree, column_names):
        """
        Sets the heading names for the Treeview columns.
        """
        for column in column_names:
            tree.heading(column, text=column)

    def set_columns(self, tree, columns):
        """
        Sets the column widths and binds double-click to auto-resize.
        """
        default_width = (self.root.winfo_screenwidth() // len(columns)) - 30
        resize_event = self._get_resize_callback(tree, default_width)

        for column in columns:
            tree.column(column, width=default_width, anchor="center", stretch=True)

        tree.bind("<Double-Button-1>", resize_event)

    def set_title(self, font: str, style: str):
        """
        Places a label as the title of the table.
        """
        title_label = ttk.Label(self.frame, text=self.title, font=font, style=style)
        title_label.grid(row=0, column=1, sticky="ns")

    def back_button(self, command):
        """
        Places a back button with an icon to navigate back.
        """
        icon_path = asset_path("back_icon.png")
        icon = Image.open(icon_path)
        resized_icon = icon.resize((50, 50), Image.Resampling.LANCZOS)
        back_image = ImageTk.PhotoImage(resized_icon)

        back_btn = ttk.Button(
            self.frame,
            image=back_image,
            command=command,
            style="darkly.Outline",
            cursor="hand2"
        )
        back_btn.image = back_image  # prevent garbage collection
        back_btn.grid(row=0, column=0, padx=15, sticky="w")

    def configure_grid(self):
        """
        Configures the grid layout of the frame.
        """
        self.frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(1, weight=5, uniform="a")
        self.frame.grid_rowconfigure(2, weight=2, uniform="a")

    def place_frame(self, relwidth, relheight):
        """
        Places the frame inside the parent using relative dimensions.
        """
        self.frame.place(relwidth=relwidth, relheight=relheight)

    def _style_treeview(self, tree):
        """
        Applies custom styles to the Treeview widget.
        """
        style = ttk.Style()
        selected_bg = style.lookup("Treeview", "selectbackground")

        style.configure("info.Treeview", foreground="white", rowheight=40)
        style.configure("writtenRow.Treeview", background="#555555", foreground="black")
        tree.tag_configure("written", background=selected_bg, font=("Tahoma", 10, "bold"))

        style.configure("info.Treeview.Heading", font=("calibri", 12, "bold"))
        style.map("Treeview", background=[('selected', 'lightblue')])

    def _get_resize_callback(self, tree, base_width):
        """
        Returns a callback function to resize the clicked column.
        """
        last_resized_col = {"col": ""}

        def resize(event):
            col = tree.identify_column(event.x)
            if col and col != "#0":
                if last_resized_col["col"] == col:
                    new_width = base_width
                    last_resized_col["col"] = ""
                else:
                    new_width = int(base_width * 2)
                    last_resized_col["col"] = col
                tree.column(col, width=new_width)
        return resize
