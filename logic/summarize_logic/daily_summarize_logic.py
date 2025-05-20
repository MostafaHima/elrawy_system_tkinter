
from db.database import database_instance
from datetime import datetime as dt
class DailyLogic:
    def __init__(self, daily_data):
        self.db = database_instance
        self.daily_data = daily_data
        self.date = dt.now().date().strftime("%Y-%m-%d")

        self.products = {}

        self._total_daily_sales()
        self._total_daily_profit()
        self._best_selling_product_and_total_item_sold()

    def _total_daily_sales(self):
        total_sales = 0
        with self.db.app.app_context():
            products = self.db.Sales.query.filter_by(date=self.date).all()

            if products is not None:
                for product in products:
                    product_name = product.product_name
                    quantity = product.quantity
                    total_sales += product.total_price

                    if product_name in self.products:
                        self.products[product_name]["quantity"] += quantity
                        continue

                    self.products[product_name] = {"quantity": product.quantity}



        self.daily_data["total_daily_sales"].set(f"£ {total_sales}")

    def _total_daily_profit(self):
        total_profit = 0
        with self.db.app.app_context():
            for product_name in self.products:

                item = self.db.Inventroy.query.filter_by(product_name=product_name).first()
                if item is not None:
                    product_quantity = self.products[product_name]["quantity"]

                    product_profit = item.profit
                    total_profit += product_quantity * product_profit

            self.daily_data["total_daily_profit"].set(f"£ {total_profit}")

    def _best_selling_product_and_total_item_sold(self):
        best_product_quantity = 0
        best_product_name = ""
        for product in self.products:

            quantity = self.products[product]["quantity"]
            if quantity > best_product_quantity:
                best_product_quantity = quantity
                best_product_name = product

        if best_product_name:
            self.daily_data["best_selling_product"].set(best_product_name)
        else:
            self.daily_data["best_selling_product"].set("Nan")

        self.daily_data["total_items_sold"].set(best_product_quantity)












