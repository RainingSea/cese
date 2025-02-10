from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        users = User().load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        users = User().load_users()
        for user in users:
            if user.username == username:
                return False
        new_user = User(username, password, email)
        new_user.save_user()
        return True