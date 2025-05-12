from db.database import database_instance


class AuthDB:
    def __init__(self):
        # Reference to the shared database instance
        self.db_instance = database_instance

    def add_user(self, username, email, password):
        """
        Adds a new user to the database.
        """
        with self.db_instance.app.app_context():
            new_user = self.db_instance.Users(
                username=username,
                email=email,
                password=password
            )
            self.db_instance.db.session.add(new_user)
            self.db_instance.db.session.commit()

    def is_username_taken(self, username):
        """
        Checks if a username already exists in the database.
        Returns the user object if found, otherwise None.
        """
        with self.db_instance.app.app_context():
            return self.db_instance.Users.query.filter_by(username=username).first()

    def is_email_taken(self, email):
        """
        Checks if an email is already registered in the database.
        Returns the user object if found, otherwise None.
        """
        with self.db_instance.app.app_context():
            return self.db_instance.Users.query.filter_by(email=email).first()

    def get_total_users(self):
        """
        Returns the total number of users in the database.
        """
        with self.db_instance.app.app_context():
            return self.db_instance.Users.query.count()
