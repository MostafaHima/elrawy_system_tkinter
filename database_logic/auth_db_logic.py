
import database_logic.database
class AuthDBLogic:
    def __init__(self):
            self.db = database_logic.database.database_instance

    def add_user(self, username, email, password):
        with self.db.app.app_context():
            new = self.db.Users(username=username, email=email, password=password)
            self.db.db.session.add(new)
            self.db.db.session.commit()



    def check_exists_username(self, username):
        with self.db.app.app_context():
            user = self.db.Users.query.filter_by(username=username).first()
            return user


    def check_email_exists(self, email):
        with self.db.app.app_context():
            user = self.db.Users.query.filter_by(email=email).first()
            return user

    def get_users_count(self):
        with self.db.app.app_context():
            count = self.db.Users.query.count()
            return count
