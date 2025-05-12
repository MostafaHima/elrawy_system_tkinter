import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from themes.app_theme import AppTheme


class AuthFormBase:
    """
    A base class for authentication forms (login/register) using Tkinter and ttkbootstrap.
    Provides reusable UI components like entries, labels, buttons, and layout setup.
    """

    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.initial_focus_entry = None

        self.frame = ttk.Frame(self.parent)
        self.child_frame = tk.Frame(
            self.frame,
            highlightcolor="orange",
            highlightbackground='gray',
            highlightthickness=1,
            relief="solid"
        )
        self.child_frame.grid(row=2, column=0, padx=200, sticky="nswe", columnspan=2, pady=50, ipady=100)

        self.input_vars = self.init_form_variables()
        AppTheme()  # Apply the app theme

    def init_form_variables(self):
        """Initialize and return the form input variables."""
        return {
            "username": tk.StringVar(),
            "email": tk.StringVar(),
            "password": tk.StringVar()
        }

    def create_input_entries(self):
        """Create entry fields for each form input."""
        for row_index, (label, var) in enumerate(self.input_vars.items(), start=1):
            entry_options = {"textvariable": var}
            if label == "password":
                entry_options["show"] = "*"

            entry = ttk.Entry(
                self.child_frame,
                **entry_options,
                width=50,
                font=("calibri", 12, "bold"),
                style="success"
            )
            entry.grid(row=row_index, column=2, sticky="wns", columnspan=2, pady=10)

            if row_index == 1:
                self.initial_focus_entry = entry.focus_set()

    def create_input_labels(self):
        """Create labels for each input field."""
        for row_index, label_text in enumerate(self.input_vars.keys(), start=1):
            label = ttk.Label(
                self.child_frame,
                text=label_text.capitalize(),
                style="light",
                font="calibri 13 bold"
            )
            label.grid(row=row_index, column=1)

    def create_main_button(self, text, cmd=None):
        """Create the main submit button."""
        button = ttk.Button(
            self.child_frame,
            text=text,
            cursor="hand2",
            command=cmd,
            width=40,
            style="warning-Outline",
            padding=10
        )
        button.grid(row=4, column=0, columnspan=3, sticky="s")

    def create_forget_password_button(self, cmd=None):
        """Create 'Forget your password?' link-style button."""
        button = ttk.Button(
            self.child_frame,
            text="Forget your password?",
            cursor="hand2",
            command=cmd,
            style="warning-link"
        )
        button.grid(row=5, column=0, columnspan=3, sticky="n", pady=5)

    def set_title_label(self):
        """Set the title label above the form."""
        label = ttk.Label(
            self.child_frame,
            text=self.title,
            font="Calibri 22 bold",
            style="info"
        )
        label.grid(row=0, column=0, columnspan=3)

    def place_logo(self):
        """Load and place the logo at the top of the window."""
        screen_width, screen_height = self.get_window_size()
        img_width = int(screen_width * 0.25)
        img_height = int(screen_height * 0.25)

        logo_path = os.path.join("assets", "el_raway_logo2.png")
        img = Image.open(logo_path)
        img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)

        canvas = tk.Canvas(self.frame, width=img_width, height=img_height, highlightthickness=0)
        canvas.create_image(img_width // 2, img_height // 2, image=logo_img)
        canvas.image = logo_img  # Prevent garbage collection
        canvas.grid(row=0, column=0, rowspan=2, columnspan=3)

    def create_navigation_button(self, text, cmd=None, state="enable"):
        """Create a button to switch between login/register forms."""
        button = ttk.Button(
            self.frame,
            text=text,
            cursor="hand2",
            command=cmd,
            style="warning-Outline",
            padding=10,
            width=15,
            state=state
        )
        button.grid(row=0, column=1, sticky="e", padx=20)

    def configure_main_grid(self):
        """Configure grid weights for the main frame."""
        self.frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(1, weight=1, uniform="a")
        self.frame.grid_rowconfigure(2, weight=6, uniform="a")
        self.frame.grid_columnconfigure(0, weight=2, uniform="a")
        self.frame.grid_columnconfigure(1, weight=1, uniform="a")

    def configure_child_grid(self):
        """Configure grid weights for the inner child frame."""
        self.child_frame.grid_rowconfigure(0, weight=2, uniform="a")
        self.child_frame.grid_rowconfigure((1, 2, 3), pad=10, uniform="a")
        self.child_frame.grid_rowconfigure((4, 5), weight=1, uniform="a")
        self.child_frame.grid_columnconfigure(0, weight=1, uniform="a")
        self.child_frame.grid_columnconfigure(1, weight=1, uniform="a")
        self.child_frame.grid_columnconfigure(2, weight=2, uniform="a")

    def place_main_frame(self):
        """Place the main frame inside the parent."""
        self.frame.place(relwidth=1, relheight=1)

    def get_input_values(self):
        """Return a dictionary of all input field values."""
        return {key: var.get() for key, var in self.input_vars.items()}

    def get_window_size(self):
        """Return the screen size of the parent window."""
        return self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()

    def clear_input_fields(self):
        """Clear all input field values."""
        for var in self.input_vars.values():
            var.set("")
