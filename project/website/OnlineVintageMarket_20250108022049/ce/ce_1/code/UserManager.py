import json

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as file:
                return [User(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def add_user(self, username: str, password: str) -> None:
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None