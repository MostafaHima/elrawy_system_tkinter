# creat_db.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Date, Time
import os
import shutil
import sys


class Base(DeclarativeBase):
    pass

class DataBase:
    def __init__(self):


        app_folder = os.path.join(os.path.expanduser("~"), "MyProgramData", "elrawy_app")
        instance_folder = os.path.join(app_folder, "instance")
        assets_folder = os.path.join(app_folder, "assets")

        os.makedirs(instance_folder, exist_ok=True)
        os.makedirs(assets_folder, exist_ok=True)

        db_path = os.path.join(instance_folder, "elrawy_bookstore_mangment.db")
        if not os.path.exists(db_path):
            original_db = os.path.join("instance", "elrawy_bookstore_mangment.db")
            if os.path.exists(original_db):
                shutil.copy(original_db, db_path)

        # 📦 تحديد مجلد الصور حسب نوع التشغيل
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        else:
            base_path = os.path.abspath(".")

        project_assets = os.path.join(base_path, "assets")

        # 🔁 نسخ الصور
        if os.path.exists(project_assets):
            for filename in os.listdir(project_assets):
                src = os.path.join(project_assets, filename)
                dst = os.path.join(assets_folder, filename)
                if not os.path.exists(dst):
                    shutil.copy(src, dst)

        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        self.db = SQLAlchemy(model_class=Base)
        self.db.init_app(self.app)

        self.define_models()
        self.create_tables()

    def define_models(self):
        db = self.db

        class Users(db.Model):
            __tablename__ = "users"

            id: Mapped[int] = mapped_column(primary_key=True)
            username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
            email: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
            password: Mapped[str] = mapped_column(String(50), nullable=False)

        self.Users = Users

        class Sales(db.Model):
            __tablename__ = "sales"
            id: Mapped[int] = mapped_column(primary_key=True)
            user: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
            product_name: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
            quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
            category: Mapped[str] = mapped_column(String(500), unique=False, nullable=True)
            unit_price: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
            total_price: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
            time: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
            date: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)

        self.Sales = Sales

        class Inventroy(db.Model):
            __tablename__ = "inventroy"
            id: Mapped[int] = mapped_column(primary_key=True)
            user: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
            product_name: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
            package_number: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
            quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
            total_quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
            unit_price: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
            profit: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
            total_price: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
            category: Mapped[str] = mapped_column(String(500), unique=False, nullable=True)
            time: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
            date: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)

        self.Inventroy = Inventroy

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()



database_instance = DataBase()