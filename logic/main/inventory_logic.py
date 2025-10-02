from pages.main.popup_data_entry import PopupDataEntry
from display_messages.message_popup import MessagePopup
from db.db_main.inventory import InventoryDB

class InventoryLogic:
    def __init__(self, root, tree, user):
        self.root = root
        self.tree = tree
        self.user = user
        self.product_name = None
        self.inv_db = InventoryDB(tree)


        self.inv_labels = ["Product Name", "Package Number", "Quantity", "Unit Price", "Profit", "Category"]

        self.add = PopupDataEntry("Add Data", "Add to Your Inventory", self.inv_labels)
        self.edit = PopupDataEntry("Edit Data", "Edit any Product you want", ["Product Name"])
        self.delete = PopupDataEntry("Delete Data", "Delete with an ID", ["ID"])
        self.item = PopupDataEntry("Edit item", "", self.inv_labels)

    def add_data(self):
        """Open the Add Product popup."""
        self.organize_inputs(self.add)
        self.add.run()
        self.add.submit_button(cmd=lambda: self.add_action())
        self.add.center_window()
        self.add.window.bind("<Return>", lambda event: self.add_action())

    def add_action(self):
        """Validate and process adding a new item."""
        if self.validate_add_inputs():
            self.add.window.destroy()
            self.add_to_db()
            MessagePopup(self.root, "Success", "Product Added", "Your product was added successfully.", "success")

    def validate_add_inputs(self):
        """Check if all add inputs are valid."""
        valid = True
        outputs = self.add.get_data()

        for (key, var), label in zip(outputs.items(), self.inv_labels):
            if key != label:
                continue

            if key in {"Package Number", "Category"} and not var:
                continue

            if key in {"Quantity", "Package Number", "Unit Price", "Profit"}:
                try:
                    value = float(var)
                    if value <= 0:
                        raise ValueError
                except ValueError:
                    MessagePopup(self.root, "Wrong", f"{key} is invalid",
                                 f"{key} must be a number greater than 0.", "danger")
                    valid = False
                    break

            if not var or var == "0":
                MessagePopup(self.root, "Missing", f"{key} is required",
                             f"Please fill in the {key}.", "danger")
                valid = False
                break

        return valid

    def add_to_db(self):
        """Push the validated add data to the database."""
        data = self.add.get_data()

        product_name = data["Product Name"]
        package_number = float(data["Package Number"])
        quantity = float(data["Quantity"])
        unit_price = float(data["Unit Price"])
        profit = float(data["Profit"])
        category = data["Category"] if data["Category"] else "Nan"

        total_quantity = quantity * package_number if package_number > 0 else quantity
        total_price = unit_price + profit

        self.inv_db.add_data(
            self.tree, self.user, product_name, package_number,
            quantity, total_quantity, unit_price, profit, total_price, category
        )

    def edit_data(self):
        """Open the popup to input an ID for editing."""

        try:
            old_entry_var = self.edit.vars.get("Product Name")
            if old_entry_var:
                old_entry_var.trace_remove("write", self.edit.trace_id)
        except:
            pass

        self.edit.vars["Product Name"].set("")
        self.edit.run()
        self.edit.submit_button(cmd=self.edit_action)
        self.edit.center_window()
        self.edit.list_box("Product Name")
        self.edit.window.bind("<Return>", lambda event: self.edit_action())

    def edit_action(self):
        """Validate and continue to edit specific product."""
        product_name = self.edit.get_data()["Product Name"]
        self.product_name = product_name
        if self.inv_db.check_product_name_existing(product_name):
            self.edit.window.destroy()
            self.edit_item()
        else:
            MessagePopup(self.root, "Error", "Invalid product Name",
                         f"No data found for product {product_name}.", "danger")

    def edit_item(self):
        """Open edit form for a specific item."""
        self.organize_inputs(self.item)
        self.item.subtitle = f"Edit item {self.product_name} Information"
        self.item.run()
        self.item.submit_button(cmd=self.edit_item_action)
        self.item.center_window()
        self.item.window.bind("<Return>", lambda event: self.edit_item_action())

    def edit_item_action(self):
        """Save the edited item."""
        self.validate_edit()
        self.item.window.destroy()
        MessagePopup(self.root, "success", "Editing went well",
                         f"{self.product_name} has been edited successfuly.", "success")


    def validate_edit(self):
        """Update the item with new values if valid."""
        db_data = self.inv_db.get_data_with_product_name(self.product_name)
        product_name = ""
        package_number = 0
        quantity = 0
        unit_price = 0
        profit = 0
        category = ""

        for (key, var) in self.item.get_data().items():
            value = self.handle_edit_exception(key.replace(" ", "_").lower(), var, db_data)
            if key == "Product Name":
                product_name = var if var else db_data.product_name

            if key == "Package Number":
                package_number = value

            if key == "Quantity":
                quantity = value

            if key == "Unit Price":
                unit_price = value

            if key == "Profit":
                profit = value

            if key == "Category":
                category = var if var else db_data.category
        self.inv_db.edit_data(self.product_name, product_name, package_number, quantity, unit_price, profit, category)
        
        
        self.inv_db.load_data()
        

    def handle_edit_exception(self, key, var, db):
        """Handle potential conversion errors during editing."""
        try:
            value = float(var)
            return value if value > 0 else getattr(db, key)
        except ValueError:
            return getattr(db, key)

    def delete_data(self):
        """Open delete popup."""
        self.delete.vars["ID"].set("0")
        self.delete.run()
        self.delete.submit_button(cmd=self.delete_action)
        self.delete.center_window()
        self.delete.window.bind("<Return>", lambda event: self.delete_action())

    def delete_action(self):
        """Perform deletion if ID is valid."""
        _id = self.delete.get_data()["ID"]
        if self.inv_db.check_id_exists(_id):
            self.inv_db.delete_data(_id)
            self.inv_db.load_data()
            self.delete.window.destroy()
        else:
            MessagePopup(self.root, "Error", "Invalid ID",
                         f"No data found for ID {_id}.", "danger")

    def organize_inputs(self, popup_obj):
        """Set default values for popup inputs."""
        for key, var in popup_obj.vars.items():
            var.set("0" if key in {"Package Number", "Quantity", "Unit Price", "Profit"} else "")
