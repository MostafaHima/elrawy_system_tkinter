


from pages.auth_base import AuthBase
from logic.auth import AuthManager


class RegisterPage(AuthBase):
    def __init__(self, root, switch_to_login):

        super().__init__(root, "Create a New Account")
        self.switch_to_login = switch_to_login
        self.auth = AuthManager(root)
        self.run()


    def run(self):
        self.set_logo()
        self.switch_frames_button(text="Login", cmd=self.switch_to_login)
        self.set_title()
        self.create_entries()
        self.create_labels()
        self.create_main_button(text="Register", cmd=self.send_info) # cmd command
        self.set_main_grid()
        self.set_child_grid()
        self.place_main_frame()
        self.parent.bind("<Return>", lambda event:self.send_info())


    def send_info(self):
        user_inputs = self.get_inputs()

        username = user_inputs["Username"]
        email = user_inputs["Email"]
        password = user_inputs["Password"]
        self.auth.register(username, email, password, self.clear_entries)





