

from db.database import database_instance
from datetime import datetime as dt, timedelta

class weeklyLogic:
    def __init__(self, weekly_vars):
        self.db = database_instance
        self.today = self.date = dt.now().date().strftime("%Y-%m-%d")
        self.raw_date = dt.now().date() - timedelta(days=7)
        self.seven_days_ago = self.raw_date.strftime("%Y-%m-%d")

        self.weekly_vars = weekly_vars
        self.products = {}

        self._from_date()
        self._total_weekly_sales()
        self._total_weekly_profit()
        self._best_selling_product_and_total_item_sold()

    def _from_date(self):
        self.weekly_vars["from_date"].set(self.seven_days_ago)


    def _total_weekly_sales(self):
        total_sales = 0
        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(self.db.Sales.date >= self.seven_days_ago,
                                             self.db.Sales.date <= self.today).all()

            for row in rows:
                if row is not None:
                    total_sales += row.total_price
                    product_name = row.product_name
                    product_quantity = row.quantity

                    if product_name in self.products:
                        self.products[product_name]["quantity"] += product_quantity
                        continue

                    self.products[product_name] = {"quantity": product_quantity}

        self.weekly_vars["total_weekly_sales"].set(f"£ {total_sales}" )



    def _total_weekly_profit(self):
        total_profit = 0
        with self.db.app.app_context():
            if self.products:
                for product_name in self.products:
                    row = self.db.Inventroy.query.filter_by(product_name = product_name).first()
                    if row is not None:
                        profit = row.profit
                        quantity = self.products[product_name]["quantity"]
                        total_profit += profit * quantity

        self.weekly_vars["total_weekly_profit"].set(f"£ {total_profit}")




    def _best_selling_product_and_total_item_sold(self):
        best_selling_name = ""
        best_selling_quantity = 0

        for product in self.products:
            product_name = product
            product_quantity = self.products[product_name]["quantity"]

            if product_quantity > best_selling_quantity:
                best_selling_quantity = product_quantity
                best_selling_name = product_name

        self.weekly_vars["best_selling_product"].set(best_selling_name)
        self.weekly_vars["total_items_sold"].set(best_selling_quantity)




