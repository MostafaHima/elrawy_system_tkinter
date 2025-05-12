from pages.main.base_table import BaseTable
from logic.main.inventory_logic import InventoryLogic

class InventoryTable(BaseTable):
    def __init__(self, root, on_back, username):
        """
        Initializes the Inventory Table view.

        :param root: The main Tkinter root or parent widget.
        :param on_back: Function to call when the back button is clicked.
        :param username: The user currently using the inventory interface.
        """
        self.root = root
        self.on_back = on_back
        self.username = username

        # Define the inventory table columns
        self.columns = (
            "Product ID",
            "User",
            "Product Name",
            "Package Number",
            "Quantity",
            "Total Quantity",
            "Unit Price",
            "Profit",
            "Total Price",
            "Category",
            "Time",
            "Date"
        )

        # Initialize the base layout
        super().__init__(root, "Inventory Page")

        # Build the UI
        self._setup_inventory_page()

    def _setup_inventory_page(self):
        """
        Builds and configures the inventory table UI and links it to the logic.
        """
        self.configure_grid()
        self.set_title(font="Calibri 24 bold", style="danger")
        self.back_button(command=self.on_back)

        # Create and configure the treeview table
        self.tree = self.create_tree_view(column_names=self.columns)
        self.set_headings(self.tree, self.columns)
        self.set_columns(self.tree, columns=self.columns)

        # Link the logic for inventory actions
        self.inventory_logic = InventoryLogic(self.root, self.tree, user=self.username)

        # Create Add/Edit/Delete action buttons
        self.action_buttons.create_act_buttons(
            add_cmd=self.inventory_logic.add_data,
            edit_cmd=self.inventory_logic.edit_data,
            delete_cmd=self.inventory_logic.delete_data
        )
