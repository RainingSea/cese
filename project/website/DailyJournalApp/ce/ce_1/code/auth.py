import json
from user import User

class Auth:
    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        if user.save():
            return True
        return False

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as file:
                return [json.loads(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def logout(self) -> None:
        pass