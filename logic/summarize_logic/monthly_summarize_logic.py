

from datetime import datetime as dt, timedelta
from db.database import database_instance
class MonthlyLogic:
    def __init__(self, monthly_vars):
        self.monthly_vars = monthly_vars
        self.db = database_instance
        self.total_month_sales = 0

        self.today =  dt.now().date().strftime("%Y-%m-%d")
        self.raw_date = dt.now().date() - timedelta(days=30)
        self.month_ago = self.raw_date.strftime("%Y-%m-%d")



        self.products = {}

        self._month_date()
        self._total_monthly_sales()
        self._total_montly_profit()
        self._best_selling_product()
        self._month_over_month_change()


    def _month_date(self):
        self.monthly_vars["month_date"].set(self.month_ago)

    def _total_monthly_sales(self):

        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(
            self.db.Sales.date >= self.month_ago,
            self.db.Sales.date <= self.today ).all()

        for row in rows:
            if row is not None:
                product_name = row.product_name
                total_price = row.total_price
                product_quantity = row.quantity

                self.total_month_sales += total_price

                if product_name in self.products:
                    self.products[product_name]["quantity"] += product_quantity
                    continue
                self.products[product_name] = {'quantity': product_quantity}

        self.monthly_vars["total_monthly_sales"].set(f"£ {self.total_month_sales}")





    def _total_montly_profit(self):
        total_profit = 0
        with self.db.app.app_context():
            for product_name in self.products:
                row = self.db.Inventroy.query.filter_by(product_name=product_name).first()
                if row is not None:
                    profit = row.profit
                    quantity = self.products[product_name]["quantity"]

                    total_profit += profit * quantity

        self.monthly_vars["total_monthly_profit"].set(f"£ {total_profit}")



    def _best_selling_product(self):
        best_selling_name = ""
        best_selling_quantity = 0

        for product_name in self.products:
            quantity = self.products[product_name]["quantity"]
            if quantity > best_selling_quantity:
                best_selling_quantity = quantity
                best_selling_name = product_name

        self.monthly_vars["best_selling_product"].set(best_selling_name)


    def _month_over_month_change(self):
        two_months_ago_sales = 0
        raw_date = dt.now().date() - timedelta(days=60)
        two_months_ago = raw_date.strftime("%Y-%m-%d")

        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(
                self.db.Sales.date >= two_months_ago,
                self.db.Sales.date <= self.month_ago
            ).all()

            for row in rows:
                if row is not None:
                    total_price = row.total_price
                    two_months_ago_sales += total_price

            if two_months_ago_sales > 0:
                equation = ((self.total_month_sales - two_months_ago_sales) / two_months_ago) * 100
                self.monthly_vars["month_over_month_change"].set(f"{equation:.2f}%")
            else:
                self.monthly_vars["month_over_month_change"].set("Not data so far")



