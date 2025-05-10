from pages.login_page import LoginPage
from pages.register_page import RegisterPage
import database_logic.auth_db_logic

class App:
    def __init__(self, root):
        self.root = root
        self.user_count = database_logic.auth_db_logic.AuthDBLogic().get_users_count()

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


