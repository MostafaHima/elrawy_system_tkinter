from pages.auth.auth_base import AuthFormBase
from logic.auth.auth_logic import AuthManager


class RegisterPage(AuthFormBase):
    def __init__(self, root, switch_to_login):
        """
        Initialize the registration page with title and logic handlers.
        """
        super().__init__(root, "Create a New Account")
        self.switch_to_login = switch_to_login
        self.auth = AuthManager(root)
        self.run()

    def run(self):
        """
        Builds and places all the UI components for the registration form.
        """
        self.place_logo()
        self.create_navigation_button(
            text="Login",
            cmd=self.switch_to_login
        )
        self.set_title_label()
        self.create_input_entries()
        self.create_input_labels()
        self.create_main_button(
            text="Create Account",
            cmd=self.send_info
        )
        self.configure_main_grid()
        self.configure_child_grid()
        self.place_main_frame()
        self.parent.bind("<Return>", lambda event: self.send_info())

    def send_info(self):
        """
        Gathers user input and calls the registration logic.
        """
        user_inputs = self.get_input_values()

        username = user_inputs["username"]
        email = user_inputs["email"]
        password = user_inputs["password"]
        self.auth.register(username, email, password, self.clear_input_fields)
