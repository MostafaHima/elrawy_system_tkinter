import tkinter as tk
from tkinter import ttk

def create_treeview(root):
    # إنشاء الـ Treeview
    tree = ttk.Treeview(root, columns=("ID", "Product Name", "Description", "Stock Quantity", "Unit Price", "Category"), show="headings")

    # تحديد الأعمدة
    tree.heading("ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Description", text="Description")
    tree.heading("Stock Quantity", text="Stock Quantity")
    tree.heading("Unit Price", text="Unit Price")
    tree.heading("Category", text="Category")

    # ضبط الأعمدة لتكون مناسبة للعرض
    tree.column("ID", width=100, anchor="center", stretch=False)
    tree.column("Product Name", width=150, anchor="center", stretch=False)
    tree.column("Description", width=200, anchor="center", stretch=False)
    tree.column("Stock Quantity", width=120, anchor="center", stretch=False)
    tree.column("Unit Price", width=100, anchor="center", stretch=False)
    tree.column("Category", width=100, anchor="center", stretch=False)



    # إضافة Scrollbar
    scrollbar = tk.Scrollbar(root, orient="vertical", command=tree.yview())
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    tree.grid(row=0, column=0, padx=10, pady=10)

    return tree

def add_product(tree, id_entry, name_entry, desc_entry, qty_entry, price_entry, cat_entry):
    # الحصول على القيم من المدخلات
    product_id = id_entry.get()
    product_name = name_entry.get()
    description = desc_entry.get()
    qty = qty_entry.get()
    price = price_entry.get()
    category = cat_entry.get()

    # إضافة البيانات الجديدة إلى الـ Treeview
    tree.insert("", "end", values=(product_id, product_name, description, qty, price, category))

    # مسح الحقول بعد إضافة المنتج
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    cat_entry.delete(0, tk.END)

def style_treeview(root, tree):
    style = ttk.Style(root)
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=40,

                    fieldbackground="lightgray")
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="lightblue")
    style.map("Treeview", background=[('selected', 'lightblue')])

    # تخصيص الخطوط بين الأعمدة والصفوف
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # تخصيص مساحة شجرة العرض
    style.configure("Treeview", highlightthickness=10, bd=50, relief="solid")  # تخصيص سمك الخطوط

def main():
    root = tk.Tk()
    root.title("Library Management System")

    # إنشاء الـ Treeview مع Scrollbar
    tree = create_treeview(root)

    # تخصيص الـ Treeview
    style_treeview(root, tree)

    # إضافة مربعات نصية لإدخال البيانات
    id_label = tk.Label(root, text="Product ID:")
    id_label.grid(row=1, column=0, padx=10, pady=5)
    id_entry = tk.Entry(root)
    id_entry.grid(row=1, column=1, padx=10, pady=5)

    name_label = tk.Label(root, text="Product Name:")
    name_label.grid(row=2, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.grid(row=2, column=1, padx=10, pady=5)

    desc_label = tk.Label(root, text="Description:")
    desc_label.grid(row=3, column=0, padx=10, pady=5)
    desc_entry = tk.Entry(root)
    desc_entry.grid(row=3, column=1, padx=10, pady=5)

    qty_label = tk.Label(root, text="Stock Quantity:")
    qty_label.grid(row=4, column=0, padx=10, pady=5)
    qty_entry = tk.Entry(root)
    qty_entry.grid(row=4, column=1, padx=10, pady=5)

    price_label = tk.Label(root, text="Unit Price:")
    price_label.grid(row=5, column=0, padx=10, pady=5)
    price_entry = tk.Entry(root)
    price_entry.grid(row=5, column=1, padx=10, pady=5)

    cat_label = tk.Label(root, text="Category:")
    cat_label.grid(row=6, column=0, padx=10, pady=5)
    cat_entry = tk.Entry(root)
    cat_entry.grid(row=6, column=1, padx=10, pady=5)

    # زر لإضافة المنتج
    add_button = tk.Button(root, text="Add Product", command=lambda: add_product(tree, id_entry, name_entry, desc_entry, qty_entry, price_entry, cat_entry))
    add_button.grid(row=7, column=0, columnspan=2, pady=10)

    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    main()
