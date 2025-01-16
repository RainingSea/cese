import json

class User:
    def __init__(self, username: str, password: str, active: bool = True):
        self.username = username
        self.password = password
        self.active = active

    def to_dict(self) -> dict:
        return {"username": self.username, "password": self.password, "active": self.active}

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, active = line.strip().split('|')
                    self.add_user(User(username, password, active == 'True'))
        except FileNotFoundError:
            print("Warning: users.txt not found. Starting with an empty user list.")

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.active}\n")

    def add_user(self, username: str, password: str) -> bool:
        if self.find_user(username) is not None:
            return False
        user = User(username, password)
        self.users.append(user)
        self.save_users()
        return True

    def deactivate_user(self, username: str) -> bool:
        user = self.find_user(username)
        if user:
            user.active = False
            self.save_users()
            return True
        return False

    def change_password(self, username: str, new_password: str) -> bool:
        user = self.find_user(username)
        if user:
            user.password = new_password
            self.save_users()
            return True
        return False

    def get_users(self) -> list:
        return [user for user in self.users if user.active]

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None