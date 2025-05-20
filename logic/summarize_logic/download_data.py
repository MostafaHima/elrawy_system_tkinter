
from db.database import database_instance
from tkinter import filedialog
from datetime import datetime as dt
from openpyxl import Workbook
import calendar
from display_messages.message_popup import MessagePopup
class DownLoadData:
    def __init__(self, month_var, root):
        self.db = database_instance
        self.month_var = month_var
        self.root = root
        self.this_year = dt.now().year


    def check_data_exists(self):
        found = False

        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(
                self.db.Sales.date.like(f"{self.this_year}-{self.month_var.get()}-%")
            )
            for row in rows:
                if row:
                    found = True
                    break


        return found

    def run_to_save(self):
        exists = self.check_data_exists()
        if exists:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                    filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                                                    title="Save Excel file")
            if not file_path:
                return
            else:
                self.save_to_excel(file_path)
                MessagePopup(self.root, "Success", "Success", f"Excel File has saved at:\n{file_path}", "success")

    def save_to_excel(self, file_path):
        title = f"Data- {self.this_year}-{calendar.month_name[int(self.month_var.get())]}"
        wb = Workbook()
        ws = wb.active
        ws.title = title

        headings = ["Product ID",
            "User",
            "Product Name",
            "Quantity",
            "Category",
            "Unit Price",
            "Total Price",
            "Time",
            "Date"]

        ws.append(headings)
        with self.db.app.app_context():
            rows = self.db.Sales.query.filter(
                self.db.Sales.date.like(f"{self.this_year}-{self.month_var.get()}-%")
            )
            for row in rows:
                _id = row.id,
                user = row.user
                product_name = row.product_name
                quantity = row.quantity
                category = row.category
                unit_price = row.unit_price
                total_price = row.total_price
                time = row.time
                date = row.date
                if category == "--":
                    category = "Nan"
                ws.append(
                    [_id[0], user,
                    product_name, quantity,
                    category, unit_price,
                    total_price, time,date]
                )

        wb.save(file_path)





