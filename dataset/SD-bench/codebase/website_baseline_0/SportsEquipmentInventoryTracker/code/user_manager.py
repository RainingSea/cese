import json
from models import User

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if self.load(username) is None:
            new_user = User(username, password)
            new_user.save()
            self.users.append(new_user)
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = self.load(username)
        if user and user.password == password:
            return True
        return False

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    user_data = json.loads(line.strip())
                    self.users.append(User(user_data['username'], user_data['password']))
        except FileNotFoundError:
            pass  # If the file does not exist, we simply ignore it

    def load(self, username: str) -> User:
        return User.load(username)