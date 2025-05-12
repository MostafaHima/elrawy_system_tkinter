from pages.auth.login_page import LoginPage
from pages.auth.register_page import RegisterPage
from db.db_auth.auth_db import AuthDB

class App:
    def __init__(self, root):
        self.root = root
        self.user_count = AuthDB().get_total_users()

        if self.user_count == 0:
            self.show_register()
            return
        self.show_login()

    def show_login(self):
        self.clear()
        if self.user_count >= 2:
            LoginPage(self.root, self.show_register, switch_state="disable")
            return
        LoginPage(self.root, self.show_register)

    def show_register(self):
        self.clear()
        RegisterPage(self.root, self.show_login)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


