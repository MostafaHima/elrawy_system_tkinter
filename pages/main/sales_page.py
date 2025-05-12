from pages.main.base_table import BaseTable
from logic.main.sales_logic import SalesLogic

class SalesTable(BaseTable):
    def __init__(self, root, on_back, username):
        """
        Initializes the Sales Table view.

        :param root: The parent Tkinter root or frame.
        :param on_back: Function to call when the back button is pressed.
        :param username: The current user performing sales.
        """
        self.root = root
        self.on_back = on_back
        self.username = username

        # Define the table's columns
        self.columns = (
            "Product ID",
            "User",
            "Product Name",
            "Quantity",
            "Category",
            "Unit Price",
            "Total Price",
            "Time",
            "Date"
        )

        # Set up the title and parent structure
        super().__init__(self.root, "Sales Page")

        # Run the full UI setup
        self._setup_sales_page()

    def _setup_sales_page(self):
        """
        Builds the sales table UI and links it to business logic.
        """
        self.configure_grid()
        self.set_title(font="Calibri 24 bold", style="success")
        self.back_button(command=self.on_back)

        # Create the tree view and populate its structure
        tree = self.create_tree_view(column_names=self.columns)
        self.set_headings(tree, self.columns)
        self.set_columns(tree, columns=self.columns)

        # Connect sales logic to the UI
        self.sales_logic = SalesLogic(self.root, tree, self.username)

        # Create action buttons for add/edit/delete
        self.action_buttons.create_act_buttons(
            add_cmd=self.sales_logic.add_data,
            edit_cmd=self.sales_logic.edit_data,
            delete_cmd=self.sales_logic.delete_data
        )
