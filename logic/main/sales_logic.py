from pages.main.popup_data_entry import PopupDataEntry
import db.db_main.sales_db
from display_messages.message_popup import MessagePopup

class SalesLogic:
    def __init__(self, root, tree, username):
        self.root = root
        self.tree = tree
        self.username = username
        self.edit_id = None

        self.labels = ["Product Name", "Quantity"]

        # نوافذ الإدخال المختلفة
        self.add = PopupDataEntry("Add Data", "Add a New Sale", self.labels)
        self.edit = PopupDataEntry("Edit Data", "Edit any Product you want", ["ID"])
        self.delete = PopupDataEntry("Delete Data", "Delete with an ID", ["ID"])
        self.edit_item = PopupDataEntry("Edit item", "", ["Quantity"])

        self.db = db.db_main.sales_db.SalesDBLogic()
        self.db.load_sales_data(self.tree)

    def add_data(self):
        # إزالة التتبع القديم إن وُجد
        try:
            old_entry_var = self.add.vars.get("Product Name")
            if old_entry_var:
                old_entry_var.trace_remove("write", self.add.trace_id)
        except:
            pass

        # إعادة تعيين القيم
        self.add.vars["Product Name"].set("")
        self.add.vars["Quantity"].set("0")

        # تشغيل النافذة
        self.add.run()
        self.add.submit_button(self.add_action)
        self.add.center_window()
        self.add.list_box(self.add.labels[0])
        self.add.window.bind("<Return>", lambda event: self.add_action())

    def add_action(self):
        self.validate_add_inputs()

    def validate_add_inputs(self):
        product_name = self.add.get_data().get("Product Name")
        quantity = self.add.get_data().get("Quantity")
        inventroy_product = self.db.check_product_name_existing(product_name)

        if product_name:
            if inventroy_product is not None:
                if quantity:
                    if quantity.isdigit():
                        if float(quantity) > 0:
                            if self.db.check_product_quantity(product_name).total_quantity > 0:
                                # إضافة بيانات البيع
                                self.db.add_data_to_db(
                                    inv_prod_id=inventroy_product.id,
                                    tree=self.tree,
                                    user=self.username,
                                    product_name=product_name,
                                    quantity=int(quantity),
                                    category=inventroy_product.category,
                                    unit_price=inventroy_product.total_price,
                                    total_price=float(quantity) * inventroy_product.total_price
                                )
                                self.add.window.destroy()
                                self.display_count_message(product_name)
                            else:
                                MessagePopup(
                                    self.root,
                                    "Error",
                                    "Not Enough Stock",
                                    "This product has zero quantity.\nPlease check the inventory page.",
                                    "danger"
                                )
                        else:
                            MessagePopup(
                                self.root,
                                "Error",
                                "Quantity Error",
                                "Quantity must be greater than 0.",
                                "danger"
                            )
                    else:
                        MessagePopup(
                            self.root,
                            "Error",
                            "Invalid Quantity",
                            "Please enter a numeric value for quantity.",
                            "danger"
                        )
                else:
                    MessagePopup(
                        self.root,
                        "Error",
                        "Missing Quantity",
                        "Please enter a quantity value.",
                        "danger"
                    )
            else:
                MessagePopup(
                    self.root,
                    "Error",
                    "Invalid Product Name",
                    "This product does not exist.\nPlease select from the list box.",
                    "danger"
                )
        else:
            MessagePopup(
                self.root,
                "Error",
                "Missing Product Name",
                "Please enter a product name.",
                "danger"
            )

    def edit_data(self):
        self.edit.vars["ID"].set("0")
        self.edit.run()
        self.edit.submit_button(cmd=self.edit_actions)
        self.edit.window.bind("<Return>", lambda event: self.edit_actions())
        self.edit.center_window()

    def edit_actions(self):
        self.vaildate_edit_inputs()

    def vaildate_edit_inputs(self):
        _id = self.edit.get_data()["ID"]
        self.edit_id = _id
        if _id:
            if _id.isdigit():
                if int(_id) > 0:
                    if self.db.check_id_exists(_id) is not None:
                        self.edit.window.destroy()
                        self.edit_item_func(_id)
                    else:
                        MessagePopup(
                            self.root,
                            "Error",
                            "Invalid ID",
                            "This ID does not exist.\nPlease enter a valid ID.",
                            "danger"
                        )
                else:
                    MessagePopup(
                        self.root,
                        "Error",
                        "ID Value Error",
                        "ID must be a number greater than 0.",
                        "danger"
                    )
            else:
                MessagePopup(
                    self.root,
                    "Error",
                    "Invalid ID Type",
                    "ID must be a numeric value.",
                    "danger"
                )
        else:
            MessagePopup(
                self.root,
                "Error",
                "Missing ID",
                "Please enter the ID.",
                "danger"
            )

    def edit_item_func(self, _id):
        self.edit_item.subtitle = f"Edit Quantity of item {_id}"
        self.edit_item.vars["Quantity"].set("0")
        self.edit_item.run()
        self.edit_item.submit_button(cmd=self.edit_item_fun_act)
        self.edit_item.window.bind("<Return>", lambda event: self.edit_item_fun_act())
        self.edit_item.center_window()

    def edit_item_fun_act(self):
        self.validate_edit_item_inputs()

    def validate_edit_item_inputs(self):
        old_quantity, product_name = self.db.get_old_quantity(self.edit_id)
        new_quantity = self.edit_item.get_data()["Quantity"]

        if new_quantity:
            if new_quantity.isdigit():
                if float(new_quantity) > 0:
                    if self.db.check_product_quantity(product_name).total_quantity > 0:
                        self.db.edit_data(self.edit_id, new_quantity, self.tree)
                        self.db.update_inv_quantity(product_name, old_quantity, new_quantity)
                        self.edit_item.window.destroy()
                        self.display_count_message(product_name)
                    else:
                        MessagePopup(
                            self.root,
                            "Error",
                            "Not Enough Stock",
                            "This product has zero quantity.\nPlease check the inventory page.",
                            "danger"
                        )
                else:
                    MessagePopup(
                        self.root,
                        "Error",
                        "Invalid Quantity",
                        "Quantity must be greater than 0.",
                        "danger"
                    )
            else:
                MessagePopup(
                    self.root,
                    "Error",
                    "Invalid Quantity Type",
                    "Quantity must be a numeric value.",
                    "danger"
                )
        else:
            MessagePopup(
                self.root,
                "Error",
                "Missing Quantity",
                "Please enter a quantity value.",
                "danger"
            )

    def delete_data(self):
        self.delete.vars["ID"].set("0")
        self.delete.run()
        self.delete.submit_button(cmd=self.delete_actions)
        self.delete.window.bind("<Return>", lambda event: self.delete_actions())
        self.delete.center_window()

    def delete_actions(self):
        self.vaildate_delete_inputs()

    def vaildate_delete_inputs(self):
        del_id = self.delete.get_data()["ID"]
        if del_id:
            if del_id.isdigit():
                if int(del_id) > 0:
                    if self.db.check_id_exists(del_id) is not None:
                        self.db.delete_data(del_id, self.tree)
                        self.delete.window.destroy()
                    else:
                        MessagePopup(
                            self.root,
                            "Error",
                            "Invalid ID",
                            "This ID does not exist.\nPlease enter a valid ID.",
                            "danger"
                        )
                else:
                    MessagePopup(
                        self.root,
                        "Error",
                        "ID Value Error",
                        "ID must be greater than 0.",
                        "danger"
                    )
            else:
                MessagePopup(
                    self.root,
                    "Error",
                    "Invalid ID Type",
                    "ID must be a numeric value.",
                    "danger"
                )
        else:
            MessagePopup(
                self.root,
                "Error",
                "Missing ID",
                "Please enter the ID.",
                "danger"
            )

    def display_count_message(self, product_name):
        product_count = self.db.check_product_quantity(product_name)
        if product_count.total_quantity <= 5:
            MessagePopup(
                self.root,
                "Warning",
                f"{product_name} is running low",
                f"Only {product_count.total_quantity} items left in stock.",
                "info"
            )
