from user import User

class Auth:
    def register(self, username: str, password: str, email: str) -> bool:
        users = User.load_all()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def logout(self) -> None:
        pass  # Placeholder for logout functionality