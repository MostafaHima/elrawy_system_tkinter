from db.db_auth.auth_db import AuthDB
from display_messages.message_popup import MessagePopup
from pages.main.main_page import DashBoardPage


class AuthManager:
    def __init__(self, root):
        """
        Initialize the AuthManager with root window and database logic.
        """
        self.root = root
        self.db = AuthDB()

    def show_popup(self, subtitle, title, message, style):
        """
        Helper function to show a message popup with consistent parameters.
        """
        MessagePopup(self.root, subtitle=subtitle, title=title, message=message, style=style)

    def login(self, username, email, password):
        """
        Handles login logic: validates inputs, checks database, and shows messages accordingly.
        """
        show_message = self.validate_inputs(username, email, password)
        if show_message:
            self.show_popup(*show_message)
        else:
            user_info = self.db.is_username_taken(username)

            if user_info is not None:

                if user_info.email == email and user_info.password == password and user_info.email == email:
                    self.open_dashboard(username)
                else:
                    self.show_popup("Error", "Incorrect Credentials",
                                    "The email or password you entered is incorrect.\nPlease try again.", "danger")
            else:
                self.show_popup("Error", "Account Not Found",
                                "No account found with that username.\nPlease check your information or register a new account.", "danger")

    def register(self, username, email, password, clear_entries):
        """
        Handles registration logic: validates inputs, checks for duplicates, and adds user to database.
        """
        show_message = self.validate_inputs(username, email, password)
        if show_message:
            self.show_popup(*show_message)
        else:
            check_username = self.db.is_username_taken(username)
            check_email = self.db.is_email_taken(email)

            if check_username is None:
                if check_email is None:
                    if len(password) >= 8:
                        self.db.add_user(username=username, email=email, password=password)
                        self.show_popup("Success", "Account Created",
                                        f"Your account has been successfully created.\nWelcome, {username}!", "success")
                        clear_entries()
                    else:
                        self.show_popup("Info", "This password is short", "Please type a password long\n it must be over 8 chars", "info")
                else:
                    self.show_popup("Error", "Email Already Exists",
                                    "The email you entered is already associated with another account.\nPlease use a different one.", "danger")
            else:
                self.show_popup("Error", "Username Already Exists",
                                "This username is already taken.\nPlease choose a different one.", "danger")

    def open_dashboard(self, username):
        """
        Destroys login widgets and opens the dashboard page.
        """
        for child in self.root.winfo_children():
            child.destroy()

        dashboard = DashBoardPage(self.root, username)
        dashboard.set_username(username)
        dashboard.frame.tkraise()

    def validate_inputs(self, username, email, password):
        """
        Validates that the username, email, and password are properly filled and formatted.
        Returns a tuple (subtitle, title, message, style) if there's an issue; otherwise returns None.
        """
        if not username:
            return "Info", "Missing Username", "Please enter your username to proceed.", "info"

        elif not email:
            return "Info", "Missing Email", "Please enter your email address to continue.", "info"

        elif "@" not in email:
            return "Error", "Invalid Email", "Email address must include an '@' symbol.", "danger"

        elif "gmail.com" not in email:
            return "Error", "Invalid Email Domain", "Email must include a valid domain like 'gmail.com'.", "danger"

        elif not password:
            return "Info", "Missing Password", "Please enter your password.", "info"


