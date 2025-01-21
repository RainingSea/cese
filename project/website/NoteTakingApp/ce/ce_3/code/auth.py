from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        users = User().load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        users = User().load_users()
        if any(user['username'] == username for user in users):
            return False
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.save()
        return True