from User import User

class UserManager:
    def add_user(self, username: str, password: str) -> None:
        user = User(username, password)
        user.save()

    def get_users(self) -> list:
        return User.load_users()