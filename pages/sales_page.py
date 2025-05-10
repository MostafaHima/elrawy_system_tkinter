from pages.base_page import BasePage
from logic.sales_logic import SalesLogic

class SalesPage(BasePage):
    def __init__(self, root, back_command, username):
        self.root = root
        super().__init__(self.root, "Sales Page", )
        self.username = username
        self.columns = ("Product ID", "User", "Product Name", "Quantity", "Category", "Unit Price", "Total Price", "Time", "Date")
        self.back_command = back_command


        self.run_sales()

    def run_sales(self):
        self.create_grid()
        self.set_title("Calibri 24 bold", style="success")
        self.back_btn(self.back_command)


        tree = self.create_tree_view(columns_name = self.columns)
        self.set_headings(tree, self.columns)

        self.set_columns(tree, columns=self.columns)

        self.sale_logic = SalesLogic(self.root, tree, self.username, )
        self.action_buttons.create_act_buttons(add_cmd=self.sale_logic.add_data, edit_cmd=self.sale_logic.edit_data, delete_cmd=self.sale_logic.delete_data)



    def add_product(self, tree):
        tree.insert("", "end", values=("1", "كراسات عربي", "3", "كراسات", '5', "15", "20-10-2025"), tags=("written",))
