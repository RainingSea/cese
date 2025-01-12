from User import User

class UserManager:
    def __init__(self, users_file: str = 'users.txt'):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        if not any(existing_user.username == username for existing_user in User.load_users()):
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = User(username, password)
        return user.validate()

    def load_users(self) -> list:
        return User.load_users()