import time

from pages.base_buttons import BaseButtons
from ui.message import MessagePopup
import ttkbootstrap as ttk
import database_logic.inventroy_db_logic

class InvetroyLogic:
    def __init__(self, root, tree, user):

        self.inv_db = database_logic.inventroy_db_logic.InventroyDBLogic(tree)
        self.root = root
        self.tree = tree
        self.user = user
        self.edit_id = None

        self.inv_db.load_data()

        self.inv_labels =["Product Name", "Package Number", "Quantity", "Unit Price", "Profit", "Category"]

        self.add = BaseButtons("Add Data", "Add to Your Inventroy", self.inv_labels)
        self.edit = BaseButtons("Edit Data", "Edit any Product you want", ["ID"])
        self.delete = BaseButtons("Delete Data", "Delete a with an ID", ["ID"])
        self.item = BaseButtons("Edit item", "", self.inv_labels)


    def add_data(self):

        self.organize_inputs(self.add)
        self.add.run()
        self.add.submit_button(cmd=lambda :self.add_action)
        self.add.center_window()
        self.add.window.bind("<Return>", lambda event: self.add_action())
    def add_action(self):
        self.validate_add_inputs()
    def validate_add_inputs(self):
        valid = True
        outputs = self.add.get_data()
        for (key, var), label in zip(outputs.items(), self.inv_labels):

            if key == label:
                if key == "Package Number" and var == "0" or key == "Category" and not var:
                    continue

                if key == "Quantity" or key == "Package Number" or key == "Unit Price" or key == "Profit":
                    if float(var):
                        continue
                    if not var.isdigit():
                        MessagePopup(self.root, "Wrong", f"{key} is not number",f"The {key} has to be numbers not string\nPlease try again with numbers", 'danger' )
                        valid = False
                        break

                if not var or var == "0":
                    MessagePopup(self.root, "Wrong", f"{key} is required", f"Please don't skip {key}\nYou have to fiil it out", "danger")
                    valid = False
                    break

                if key == "Quantity" or key == "Package Number" or key == "Unit Price" or key == "Profit":
                    if float(var) <=0:
                        MessagePopup(self.root, "Wrong", f"{key} has small number", "You must type number over 1\nYou might typed 0, 00 or 000 an so on", "danger")
                        valid = False
                        break
        if valid:
            self.add.window.destroy()
            self.add_to_db()
            MessagePopup(self.root, "success", "Added done successfuly!", f"your product added successfuly!", "success")
    def add_to_db(self):
        data = self.add.get_data()
        user = self.user
        product_name = data["Product Name"]

        package_number = float(data["Package Number"])
        quantity = float(data["Quantity"])
        total_quantity = quantity * package_number if package_number > 0 else quantity

        unit_price = float(data["Unit Price"])
        profit = float(data["Profit"])
        total_price = unit_price + profit

        category = data["Category"] if data["Category"] else "--"
        self.inv_db.add_data(self.tree, user, product_name, package_number, quantity, total_quantity, unit_price, profit, total_price, category)



    def edit_data(self):
        self.edit.vars["ID"].set("0")
        self.edit.run()
        self.edit.submit_button(cmd=self.edit_action)
        self.edit.center_window()
        self.edit.window.bind("<Return>", lambda event: self.edit_action())

    def edit_action(self):
        self.vaildate_edit_id()


    def vaildate_edit_id(self):
        _id = self.edit.get_data()["ID"]
        self.edit_id = _id
        valid = self.inv_db.check_id_exists(_id)
        if valid is not None:
            self.edit.window.destroy()
            self.edit_item()

        else:
            MessagePopup(self.root, "Error", "ID does not exist",
                         f"Please check your input\n your data does not have any row with {_id} number",
                         "danger")


    def edit_item(self, ):
        self.organize_inputs(self.item)
        self.item.subtitle = f"Edit item {self.edit_id} Information"

        self.item.run()
        self.item.submit_button(cmd=self.edit_item_action)
        self.item.center_window()
        self.item.window.bind("<Return>", lambda event: self.edit_item_action())



    def edit_item_action(self):
        self.validate_edit()
        self.item.window.destroy()


    def validate_edit(self):
        db_data = self.inv_db.get_data_with_id(self.edit_id)
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



        self.inv_db.edit_data(self.edit_id, product_name, package_number, quantity, unit_price, profit, category)
        self.inv_db.load_data()


    def handle_edit_exception(self, key, var, db):
        try:
            value = float(var)
            if value > 0:
                return value
        except ValueError:
            pass
        return getattr(db, key)

    def delete_data(self):
        self.delete.vars["ID"].set("0")
        self.delete.run()
        self.delete.submit_button(cmd=self.delete_action)
        self.delete.center_window()
        self.delete.window.bind("<Return>", lambda event: self.delete_action())

    def delete_action(self):

        _id = self.delete.get_data()["ID"]
        vaild = self.inv_db.check_id_exists(_id)
        if vaild is not None:
            self.inv_db.delete_data(_id)
            self.inv_db.load_data()
            self.delete.window.destroy()
        else:
            MessagePopup(self.root, "Error", "ID does not exist",
                         f"Please check your input\n your data does not have any row with {_id} number",
                         "danger")

    def organize_inputs(self, obj):
        for key, var in obj.vars.items():
            if key == "Package Number" or key == "Quantity" or key == "Unit Price" or key == "Profit":
                var.set("0")
            else:
                var.set("")


