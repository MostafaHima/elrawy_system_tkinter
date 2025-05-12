from pages.auth.auth_base import AuthFormBase
from logic.auth.auth_logic import AuthManager
import tkinter as tk
from utils.password_reset import forget_password


class LoginPage(AuthFormBase):
    def __init__(self, root, switch_to_register, switch_state='enable'):
        """
        Initialize the login page with title and necessary logic handlers.
        """
        super().__init__(root, "Login to Your Account")
        self.switch_to_register = switch_to_register
        self.auth = AuthManager(root)
        self.email_var = tk.StringVar()
        self.switch_state = switch_state
        self.run()

    def run(self):
        """
        Builds and places all the UI components for the login form.
        """
        self.place_logo()
        self.create_navigation_button(
            text="Register",
            cmd=self.switch_to_register,
            state=self.switch_state
        )
        self.set_title_label()
        self.create_input_entries()
        self.create_input_labels()
        self.create_main_button(
            text="Login Now",
            cmd=self.send_info
        )
        self.create_forget_password_button(
            cmd=lambda: forget_password(self.parent, self.get_window_size, self.email_var)
        )
        self.configure_main_grid()
        self.configure_child_grid()
        self.place_main_frame()
        self.parent.bind("<Return>", lambda event: self.send_info())

    def send_info(self):
        """
        Gathers user inputs and passes them to the authentication logic.
        """
        user_input = self.get_input_values()

        username = user_input["username"]
        email = user_input["email"]
        password = user_input["password"]

        self.auth.login(username=username, email=email, password=password)
