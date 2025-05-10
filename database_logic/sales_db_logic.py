
import database_logic.database
from datetime import datetime as dt
import database_logic.inventroy_db_logic
class SalesDBLogic:
    def __init__(self):
        self.db = database_logic.database.database_instance

    def search(self, search_value):
        with self.db.app.app_context():
            result = self.db.db.session.query(self.db.Inventroy).filter(self.db.Inventroy.product_name.ilike(f"%{search_value}%")).all()
            return result

    def add_data_to_db(self,inv_prod_id,  tree, **kwargs):
        with self.db.app.app_context():
            product = self.db.Sales(**kwargs, time= dt.now().time().strftime("%I:%M: %p"),
                date = dt.now().date().strftime("%Y-%m-%d"))
            self.db.db.session.add(product)
            self.db.db.session.commit()

        self.load_sales_data(tree)
        self.update_data(inv_prod_id, kwargs.get("quantity"))

    def update_data(self, _id, new_value):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(id=_id).first()
            item.total_quantity = item.total_quantity - new_value
            self.db.db.session.commit()


    def check_id_exists(self, _id):
        with self.db.app.app_context():
            product_id = self.db.Sales.query.filter_by(id=_id).first()
            return product_id

    def check_product_name_existing(self, value):
        with self.db.app.app_context():
            exists = self.db.Inventroy.query.filter_by(product_name = value).first()
            return exists


    def get_old_quantity(self, _id):
        with self.db.app.app_context():
            row = self.db.Sales.query.filter_by(id=_id).first()
            return row.quantity, row.product_name


    def edit_data(self, _id, new_quantity, tree):
        new_quantity = int(new_quantity)
        with self.db.app.app_context():
            item = self.db.Sales.query.filter_by(id=_id).first()
            item.quantity = new_quantity
            item.total_price = new_quantity * item.unit_price
            self.db.db.session.commit()
            self.load_sales_data(tree)

    def update_inv_quantity(self, product_name, old_quantity, new_quantity):
        new_quantity = int(new_quantity)
        old_quantity = int(old_quantity)

        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(product_name=product_name).first()
            difference = abs(new_quantity - old_quantity)

            if new_quantity > old_quantity:
                # خَصم من المخزون
                item.total_quantity -= difference
            elif new_quantity < old_quantity:
                # أضف للمخزون
                item.total_quantity += difference
            # لو متساويين، ما تعملش حاجة

            self.db.db.session.commit()


    def delete_data(self, _id, tree):
        with self.db.app.app_context():
            item = self.db.Sales.query.filter_by(id=_id).first()
            item_quantity = item.quantity
            item_name = item.product_name
            self.update_inv_after_delete(item_name, item_quantity)
            self.db.db.session.delete(item)
            self.db.db.session.commit()
            self.load_sales_data(tree)

    def update_inv_after_delete(self, item_name, item_quantity):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(product_name=item_name).first()
            item.total_quantity += item_quantity
            self.db.db.session.commit()

    def check_product_quantity(self, product_name):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(product_name=product_name).first()
            return item

    def load_sales_data(self, tree):

        for item in tree.get_children():
            tree.delete(item)

        with self.db.app.app_context():
            count = self.db.Sales.query.count()
            if count is not None and count >=1:
                data = self.db.Sales.query.all()


                quantity = 0
                unit_price = 0
                total_price = 0

                for product in data:

                    if product.quantity == int(product.quantity):
                        quantity = int(product.quantity)
                    else:
                        quantity = product.quantity

                    if product.unit_price == int(product.unit_price):
                        unit_price = int(product.unit_price)
                    else:
                        unit_price = product.unit_price


                    if product.total_price == int(product.total_price):
                        total_price = int(product.total_price)
                    else:
                        total_price = product.total_price

                    tree.insert("", "end", values=(
                        product.id, product.user, product.product_name, quantity, product.category,
                        unit_price, total_price, product.time, product.date),
                                tags=("written",))




