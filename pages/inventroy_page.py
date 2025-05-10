from pages.base_page import BasePage
import logic.inventory_logic

class InventoryPage(BasePage):
    def __init__(self, root, back_command, username):
        self.back_command = back_command
        self.username = username

        super().__init__(root, "Inventroy Page", )
        self.root = root

        self.columns = ("Product ID", "User", "Product Name", "Package Number", "Quantity", "Total Quantity" ,
                        "Unit Price", "Profit", "Total Price", "Category", "Time", "Date")


        self.run_inventroy()

    def run_inventroy(self):

        self.create_grid()

        self.set_title("Calibri 24 bold", style="danger")
        self.back_btn(self.back_command)

        self.tree = self.create_tree_view(columns_name = self.columns)
        self.set_headings(self.tree, self.columns)
        self.set_columns(self.tree, columns=self.columns)

        self.inventroy_lgoic = logic.inventory_logic.InvetroyLogic(self.root, self.tree, user=self.username)
        self.action_buttons.create_act_buttons(add_cmd=self.inventroy_lgoic.add_data, edit_cmd=self.inventroy_lgoic.edit_data, delete_cmd=self.inventroy_lgoic.delete_data)



