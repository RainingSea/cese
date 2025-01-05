from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        if User.load(username) is None:
            new_user = User(username, password, email)
            new_user.save()
            return True
        return False