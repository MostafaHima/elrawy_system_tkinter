
from db.database import database_instance
class ReminderDB:
    def __init__(self, tree):
        self.tree = tree
        self.db = database_instance
        self.ides = []
        self.data = []


    def get_products_count(self):

        with self.db.app.app_context():
            products = self.db.Inventroy.query.all()
            for product in products:
                product_quantity = product.total_quantity
                if product_quantity <= 5:
                    self.ides.append(product.id)

    def get_data_from_db(self):
        self.ides.clear()
        self.data.clear()
        self.get_products_count()
        if self.ides:
            for item in self.tree.get_children():
                self.tree.delete(item)

            with self.db.app.app_context():

                for _id in self.ides:
                    product = self.db.Inventroy.query.filter_by(id=_id).first()
                    self.data.append({
                        "id": product.id,
                        "product_name": product.product_name,
                        "total_quantity": product.total_quantity,
                        "category": product.category,
                        "time": product.time,
                        "date": product.date
                    })





    def load_reminder_data(self):
        self.get_data_from_db()
        for item in self.data:
            self.tree.insert("", "end", values=(item.get("id"),
                                                item.get("product_name"),
                                                item.get("total_quantity"),
                                                item.get("category"),
                                                item.get("time"),
                                                item.get("date")),
                             tags=("written",))


