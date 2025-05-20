
import calendar
from db.database import database_instance
from datetime import datetime as dt

class MonthlyReportLogic:
    def __init__(self, report_vars, month_var):
        self.report_vars = report_vars
        self.month_var = month_var
        self.db = database_instance
        self.this_year = dt.now().year

        self.products = {}


        self._display_month()
        self._total_sales()
        self._total_profit()
        self._best_selling_product_and_total_items_sold()

    def _display_month(self):
        month = calendar.month_name[int(self.month_var.get())]
        self.report_vars["month"].set(f"{month} - {self.this_year}")

    def _total_sales(self):
        total_sales = 0
        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(self.db.Sales.date.like(f"{self.this_year}-{self.month_var.get()}-%"))

            for row in rows:
                if row is not None:
                    product_name = row.product_name
                    product_qantity = row.quantity
                    total_sales += row.total_price

                    if product_name in self.products:
                        self.products[product_name]["quantity"] += product_qantity
                        continue

                    self.products[product_name] = {"quantity": product_qantity}

        self.report_vars["total_sales"].set(f"£ {total_sales}")

    def _total_profit(self):
        total_profit = 0

        with self.db.app.app_context():
            for product_name in self.products:
                product = self.db.Inventroy.query.filter_by(product_name = product_name).first()
                if product is not None:

                    quantity = self.products[product_name]["quantity"]
                    profit = product.profit
                    total_profit += quantity * profit

        self.report_vars["total_profit"].set(f"£ {total_profit}")


    def _best_selling_product_and_total_items_sold(self):
        best_product_name = ""
        best_product_quantity = 0

        for product_name in self.products:

            quantity = self.products[product_name]["quantity"]
            if quantity > best_product_quantity:
                best_product_quantity = quantity
                best_product_name = product_name


        self.report_vars["total_items_sold"].set(f"{best_product_quantity} items")
        self.report_vars["best_selling_product"].set(best_product_name)





