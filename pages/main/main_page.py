from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import Style

from pages.main.sales_page import SalesTable
from pages.main.inventroy_page import InventoryTable
from pages.main.reminder_page import ReminderTable
from pages.summarize_page.summarize_page import SummarizePage

from logic.summarize_logic.daily_summarize_logic import DailyLogic


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

        self.summarize_page = SummarizePage(self.root, self.back_dashboard)
        self.summarize_page.pack(expand=True, fill="both")

        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=1, relheight=1)
        self.set_style()
        self.create_widgets()
        self.root.unbind("<Return>")


    def create_widgets(self):

        self.frame.grid_columnconfigure(index=(0,1,2,3), weight=1, uniform="a")
        self.frame.grid_rowconfigure(index=0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(index=1, weight=2, uniform="a")

        self.welcome = ttk.Label(self.frame, text="", font="calibri 24 bold", style="warning")
        self.welcome.grid(row=0, column=1, columnspan=2)

        reminder_button = ttk.Button(self.frame, text="Open Reminder", style="warning-Outline", cursor="hand2", command=self.open_reminder, takefocus=False)
        sales_button = ttk.Button(self.frame, text="Open Sales", cursor="hand2", style="warning-Outline", command=self.open_sales, takefocus=False)
        inventory_button  = ttk.Button(self.frame, text="Open Inventory", cursor="hand2", style="warning-Outline", command=self.open_inventory, takefocus=False)
        summarize_button  = ttk.Button(self.frame, text="Open Summarize", cursor="hand2", style="warning-Outline", command=self.open_summarize, takefocus=False)

        reminder_button.grid(row=1, column=0, sticky="nswe", padx=50, pady=150)
        inventory_button.grid(row=1, column=1, sticky="nswe", padx=50, pady=150)
        summarize_button.grid(row=1, column=2, sticky="nswe", padx=50, pady=150)
        sales_button.grid(row=1, column=3, sticky="nswe", padx=50, pady=150)


        logout_button = ttk.Button(self.frame, text="Logout", cursor="hand2", style="info-Outline", width=20, padding=15, command=self.logout)
        logout_button.grid(row=0, column=3, sticky="ne", padx=20, pady=20)

    def open_sales(self):
        self.sales_ui.frame.tkraise()

    def open_summarize(self):
        self.summarize_page.tkraise()
        self.summarize_page.load_summarizes_data()


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

    def back_dashboard(self):
        self.frame.tkraise()



    def set_style(self):
        style = Style()
        style.configure("success.Outline.TButton", font="calibri 15 bold")
        style.configure("danger.Outline.TButton", font="calibri 15 bold")
        style.configure("info.Outline.TButton", font="calibri 12 bold")
        style.configure("warning.Outline.TButton", font="calibri 15 bold")
