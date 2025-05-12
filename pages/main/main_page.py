from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import Style

from pages.main.sales_page import SalesTable
from pages.main.inventroy_page import InventoryTable
from pages.main.reminder_page import ReminderTable





class DashBoardPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username



        self.sales_ui = SalesTable(self.root, self.back_dashboard, username=self.username)
        self.sales_ui.place_frame(1, 1)

        self.inventrory_page = InventoryTable(self.root, self.back_dashboard, username=self.username)
        self.inventrory_page.place_frame(1, 1)



        self.reminder_page = ReminderTable(self.root, self.back_dashboard)
        self.reminder_page.place_frame(1, 1)


        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=1, relheight=1)
        self.set_style()
        self.create_widgets()
        self.root.unbind("<Return>")


    def create_widgets(self):

        self.frame.grid_columnconfigure(index=(0,1,2), weight=1, uniform="a")
        self.frame.grid_rowconfigure(index=0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(index=1, weight=2, uniform="a")

        self.welcome = ttk.Label(self.frame, text="", font="calibri 24 bold", style="warning")
        self.welcome.grid(row=0, column=1,)

        reminder_btn = ttk.Button(self.frame, text="Open Reminder", style="warning-Outline", cursor="hand2", command=self.open_reminder)
        sales_btn = ttk.Button(self.frame, text="Open Sales", cursor="hand2", style="warning-Outline", command=self.open_sales)
        inventory_btn  = ttk.Button(self.frame, text="Open Inventory", cursor="hand2", style="warning-Outline", command=self.open_inventory)

        reminder_btn.grid(row=1, column=0, sticky="nswe", padx=50, pady=100)
        inventory_btn.grid(row=1, column=1, sticky="nswe", padx=50, pady=100)
        sales_btn.grid(row=1, column=2, sticky="nswe", padx=50, pady=100)

        logout_btn = ttk.Button(self.frame, text="Logout", cursor="hand2", style="warning-Outline", width=15, padding=15, command=self.logout)
        logout_btn.grid(row=0, column=2, sticky="ne", padx=20, pady=20)

    def open_sales(self):
        self.sales_ui.frame.tkraise()

    def back_dashboard(self):
        self.frame.tkraise()

    def open_inventory(self):
        self.inventrory_page.frame.tkraise()
        self.inventrory_page.inventory_logic.inv_db.get_quantity_count()
        self.inventrory_page.inventory_logic.inv_db.load_data()


    def open_reminder(self):
        self.reminder_page.frame.tkraise()
        self.reminder_page.reminder_logic.load_reminder_data()


    def logout(self):
        import logic.core.app
        logic.core.app.App(self.root).show_login()


    def set_username(self, username):
        username = username
        self.welcome["text"] = f"Welcome Back {username}"



    def set_style(self):
        style = Style()
        style.configure("success.Outline.TButton", font="calibri 15 bold")
        style.configure("danger.Outline.TButton", font="calibri 15 bold")
        style.configure("info.Outline.TButton", font="calibri 15 bold")
        style.configure("warning.Outline.TButton", font="calibri 15 bold")
