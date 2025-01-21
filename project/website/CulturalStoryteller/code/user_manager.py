import json
from user import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password)
        users.append(new_user)
        self.save_users(users)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user.username == username and user.password == password for user in users)

    def load_users(self) -> list[User]:
        try:
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
                return [User(**user) for user in users_data]
        except FileNotFoundError:
            return []

    def save_users(self, users: list[User]) -> None:
        with open(self.users_file, 'w') as f:
            json.dump([user.to_dict() for user in users], f)