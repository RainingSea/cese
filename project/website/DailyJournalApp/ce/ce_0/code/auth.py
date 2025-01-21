from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        users = User().load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        users = User()
        existing_users = users.load_users()
        for user in existing_users:
            if user['username'] == username:
                return False  # User already exists
        new_user = User(username, password)
        new_user.save()
        return True

    def logout(self) -> None:
        pass  # Logout logic handled in main.py