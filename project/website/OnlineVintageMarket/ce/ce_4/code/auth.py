from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        users = User().load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str) -> None:
        new_user = User(username, password)
        new_user.save()