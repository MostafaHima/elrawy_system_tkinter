

import db.database
from datetime import datetime as dt

class InventoryDB:
    def __init__(self, tree):
        self.db = db.database.database_instance
        self.tree = tree


    def load_data(self):


        for item in self.tree.get_children():
            self.tree.delete(item)

        with self.db.app.app_context():
            count = self.db.Inventroy.query.count()
            if count is not None and count >=1:
                data = self.db.Inventroy.query.all()

                package_number = 0
                quantity = 0
                total_quantity = 0
                unit_price = 0
                profit = 0
                total_price = 0

                for row in data:
                    if row.package_number == int(row.package_number):
                        package_number = int(row.package_number)
                    else:
                        package_number = row.package_number

                    if row.quantity == int(row.quantity):
                        quantity = int(row.quantity)
                    else:
                        quantity = row.quantity

                    if row.total_quantity == int(row.total_quantity):
                        total_quantity = int(row.total_quantity)
                    else:
                        total_quantity = row.total_quantity

                    if row.unit_price == int(row.unit_price):
                        unit_price = int(row.unit_price)
                    else:
                        unit_price = row.unit_price

                    if row.profit == int(row.profit):
                        profit = int(row.profit)
                    else:
                        profit = row.profit

                    if row.total_price == int(row.total_price):
                        total_price = int(row.total_price)
                    else:
                        total_price = row.total_price


                    self.tree.insert("", "end", values=(
                        row.id, row.user, row.product_name, package_number, quantity, total_quantity, unit_price, profit,
                        total_price,row.category, row.time, row.date),
                                tags=("written",))


    def add_data(self,tree, user, product_name, package_number, quantity, total_quantity, unit_price, profit, total_price, category):
        with self.db.app.app_context():
            new_prduct = self.db.Inventroy(
                user=user,
                product_name=product_name,
                package_number=package_number,
                quantity=quantity,
                total_quantity=total_quantity,
                unit_price=unit_price,
                profit=profit,
                total_price=total_price,
                category=category,
                time=dt.now().time().strftime("%I:%M: %p"),
                date = dt.now().date().strftime("%Y-%m-%d")
                                           )

            self.db.db.session.add(new_prduct)
            self.db.db.session.commit()

            self.load_data()

    def check_id_exists(self, _id):
        with self.db.app.app_context():
            row = self.db.Inventroy.query.filter_by(id=_id).first()
            return row

    def get_data_with_id(self, _id):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(id=_id).first()
            return item


    def edit_data(self, _product_name, product_name, package_number, qunatity, unit_price, profit, category):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(product_name=_product_name).first()
            if qunatity > 0 and package_number == 0:
                package_number = 1

            item.product_name = product_name
            item.package_number = package_number
            item.quantity = qunatity
            item.unit_price = unit_price
            item.profit = profit
            item.category = category



            item.total_quantity = qunatity * package_number
            item.total_price = unit_price + profit
            item.time =  dt.now().time().strftime("%I:%M: %p")
            item.date = dt.now().date().strftime("%Y-%m-%d")
            self.db.db.session.commit()



    def delete_data(self, _id):
        with self.db.app.app_context():
            row = self.db.Inventroy.query.filter_by(id=_id).first()
            self.db.db.session.delete(row)
            self.db.db.session.commit()

    def get_quantity_count(self):
        with self.db.app.app_context():
            rows = self.db.Inventroy.query.all()
            for row in rows:
                if row.total_quantity == 0:
                    row.quantity = 0
                    row.package_number = 0
            self.db.db.session.commit()

    def check_product_name_existing(self, value):
        with self.db.app.app_context():
            exists = self.db.Inventroy.query.filter_by(product_name = value).first()
            return exists
        
    def get_data_with_product_name(self, prod_name):
        with self.db.app.app_context():
            item = self.db.Inventroy.query.filter_by(product_name=prod_name).first()
            return item








