from pages.main.base_table import BaseTable
from db.db_main.reminder_db import ReminderDB

class ReminderTable(BaseTable):
    def __init__(self, root, on_back):
        """
        Initializes the ReminderTable page with its layout and data logic.

        :param root: The parent window or frame.
        :param on_back: The callback function when the back button is pressed.
        """
        self.root = root
        self.on_back = on_back

        # Set table title
        super().__init__(self.root, "Reminder Page")

        # Define the column names for the Treeview
        self.columns = (
            "Product ID",
            "Product Name",
            "Total Quantity",
            "Category",
            "Time",
            "Date"
        )

        # Initialize and run the table layout and logic
        self._setup_reminder_page()

    def _setup_reminder_page(self):
        """
        Builds and places all components of the Reminder Table.
        """
        self.back_button(command=self.on_back)
        self.configure_grid()
        self.set_title(font="calibri 24 bold", style="danger")

        # Create and set up the Treeview
        tree = self.create_tree_view(column_names=self.columns)
        self.set_headings(tree, self.columns)
        self.set_columns(tree, columns=self.columns)

        # Connect the tree to the reminder database logic
        self.reminder_logic = ReminderDB(tree=tree)
