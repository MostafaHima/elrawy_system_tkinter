from db.database import database_instance
from datetime import datetime as dt

class YearlyLogic:
    def __init__(self, yearly_vars):
        self.db = database_instance
        self.yearly_vars = yearly_vars
        self.this_year = dt.now().year
        self.today = dt.now().date().strftime("%Y-%m-%d")
        self.products = {}
        self.total_sales = 0

        self._current_year()
        self._total_yearly_sales()
        self._total_yearly_profit()
        self._average_monthly_sales()

    def _current_year(self):
        self.yearly_vars["current_year"].set(self.this_year)

    def _total_yearly_sales(self):

        with self.db.app.app_context():
            products = self.db.Sales.query.filter(
                self.db.Sales.date.like(f"{self.this_year}-%")
            ).all()

            for product in products:
                if product is not None:
                    product_name = product.product_name
                    product_quantity = product.quantity
                    self.total_sales += product.total_price

                    if product_name in self.products:
                        self.products[product_name]["quantity"] += product_quantity
                        continue

                    self.products[product_name] = {"quantity": product_quantity}

        self.yearly_vars["total_sales"].set(f"£ {self.total_sales}")


    def _total_yearly_profit(self):
        total_profit = 0

        with self.db.app.app_context():

            if self.products:
                for product_name in self.products:
                    products = self.db.Inventroy.query.filter_by(product_name=product_name)
                    for product in products:
                        if product is not None:
                            profit = product.profit
                            quantity = self.products[product_name]["quantity"]

                            total_profit += profit * quantity

            self.yearly_vars["total_profit"].set(f"£ {total_profit}")



    def _average_monthly_sales(self):
        months = 0
        with self.db.app.app_context():
            products = self.db.Sales.query.all()
            for product in products:
                if product is not None:
                    day = product.date.split("-")[-1]
                    if day == "1":
                        months +=1

        if months == 0:
            months = 1

        mean = self.total_sales / months
        self.yearly_vars["average_monthly_sales"].set(f"£ {int(mean)}")
