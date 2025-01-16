from user import User

class Auth:
    def register(self, username: str, password: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password)
        new_user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = User.load_users()
        return any(user.username == username and user.password == password for user in users)

    def logout(self):
        pass  # Logout logic is handled in main.py