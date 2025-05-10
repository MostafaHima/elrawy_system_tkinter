
# from database_logic.database import database_instance
from database_logic.auth_db_logic import AuthDBLogic
from ui.message import MessagePopup
from pages.dashboard_page import DashBoardPage


class AuthManager:
    def __init__(self, root):
        self.root = root
        self.db_auth = AuthDBLogic()


    def login(self, username, email, password):
        show_message = self.validate_inputs(username, email, password)
        if show_message:
            MessagePopup(self.root, subtitle=show_message[0], title=show_message[1], message=show_message[2], style=show_message[3])
        else:
            db_info = self.db_auth.check_exists_username(username)
            if db_info is not None:
                if db_info.email == email and db_info.password == password:
                    self.open_dashboard(username)
                else:
                    MessagePopup(self.root, subtitle="Error", title="The information is wrong", message="Please check your inputs and try again", style="danger")
            else:
                MessagePopup(self.root, subtitle='Error', title="This account is not existing", message="That username is not existing in the system", style="danger")



    def register(self, username, email, password, clear_entries):
        show_message = self.validate_inputs(username, email, password)
        if show_message:
            MessagePopup(self.root, subtitle=show_message[0], title=show_message[1], message=show_message[2],style=show_message[3])
        else:
            check_username = self.db_auth.check_exists_username(username)
            check_email = self.db_auth.check_email_exists(email)

            if check_username is None:
                if check_email is None:

                    self.db_auth.add_user(username=username, email=email, password=password)
                    MessagePopup(self.root, subtitle="Success", title="Creating a new account", message=f"Your account is ready to use {username}",
                                 style="success")
                    clear_entries()
                else:
                    MessagePopup(self.root, "Wrong", "Email is existing", "This Email is already existing\nin the system try to use another one", "danger")
            else:
                MessagePopup(self.root, "Wrong", "Username is existing", "This username is already existing\nin the system try to use another one", "danger")

    def open_dashboard(self, username):
        for child in self.root.winfo_children():
            child.destroy()

        dashboard = DashBoardPage(self.root, username)
        dashboard.set_username(username)

        dashboard.frame.tkraise()


    def validate_inputs(self, username, email, password):
        if not username:
            return "Info", "Username Filed is Missing", "Please don't skip Username filed", "info"

        elif not email:
            return "Info", "Email Filed is Missing", "Please don't skip Email filed", "info"

        elif "@" not in email:
            return "Worng", "Email does not have @", "Please write @ sign in your email", "danger"

        elif "gmail.com" not in email:
            return "Wrong", "Email does not have the host", "Please write gmail.com in your email", "danger"

        elif not password:
            return "Info", "Password Filed is Missing", "Please don't skip Password filed", "info"













