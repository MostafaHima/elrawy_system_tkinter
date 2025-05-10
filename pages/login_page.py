
from pages.auth_base import AuthBase
from logic.auth import AuthManager
import ttkbootstrap as ttk
import tkinter as tk
from utils.forget_password_proccess import foreget_password


class LoginPage(AuthBase):
    def __init__(self, root, switch_to_register, switch_state='enable'):

        super().__init__(root, "Login To Your Account")
        self.switch_to_register = switch_to_register
        self.auth = AuthManager(root)
        self.email_var = tk.StringVar()
        self.switch_state = switch_state

        self.run()



    def run(self):
        self.set_logo()
        self.switch_frames_button(text="Register", cmd=self.switch_to_register, state=self.switch_state) # cmd command
        self.set_title()
        self.create_entries()
        self.create_labels()
        self.create_main_button(text="Login", cmd=self.send_info) # cmd command
        self.create_forget_button(cmd=lambda :foreget_password(self.parent, self.get_window_size, self.email_var)) # cmd command
        self.set_main_grid()
        self.set_child_grid()
        self.place_main_frame()
        self.parent.bind("<Return>", lambda event:self.send_info())


    def send_info(self):
        user_input = self.get_inputs()

        username = user_input["Username"]
        email = user_input["Email"]
        password = user_input["Password"]

        self.auth.login( username=username, email=email, password=password)










