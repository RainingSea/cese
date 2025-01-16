from user import User

class Auth:
    @staticmethod
    def login(username, password):
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    @staticmethod
    def register(username, password, email):
        new_user = User(username, password, email)
        new_user.save()
        return True

    @staticmethod
    def logout():
        pass  # Logout functionality is handled in main.py