
from pages.base_page import BasePage
import database_logic.reminder_db_logic

class ReminderPage(BasePage):
    def __init__(self, root, call_back):
        self.root = root
        self.call_back = call_back
        super().__init__(self.root, "Reminger Page")

        self.columns = ("Product ID", "Product Name", "Total Quantity", "Category", "Time", "Date")

        self.run_reminder()

    def run_reminder(self):
        self.back_btn(command=self.call_back)
        self.create_grid()
        self.set_title("calibri 24 bold", "danger")
        tree = self.create_tree_view(columns_name=self.columns)
        self.set_headings(tree, self.columns)
        self.reminder_db = database_logic.reminder_db_logic.RemingerDBLogic(tree=tree)
        self.set_columns(tree, columns=self.columns)


    def add_product(self, tree):
        tree.insert("", "end", values=("1", "كراسات عربي", "3", "كراسات", '5', "15", "20-10-2025"),tags=("written",))


