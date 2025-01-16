import json
from typing import List

class User:
    def __init__(self, username: str, password: str, bio: str):
        self.username = username
        self.password = password
        self.bio = bio

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "bio": self.bio
        }

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users: List[User] = []
        self.load_users()

    def load_users(self) -> None:
        try:
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
                self.users = [User(**user) for user in users_data]
        except FileNotFoundError:
            self.users = []

    def save_users(self) -> None:
        with open(self.users_file, 'w') as f:
            json.dump([user.to_dict() for user in self.users], f)

    def register_user(self, username: str, password: str, bio: str) -> None:
        if any(user.username == username for user in self.users):
            raise ValueError("Username already exists.")
        new_user = User(username, password, bio)
        self.users.append(new_user)
        self.save_users()

    def login_user(self, username: str, password: str) -> User:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        raise ValueError("Invalid username or password.")

    def update_user_profile(self, username: str, new_password: str, new_bio: str) -> None:
        for user in self.users:
            if user.username == username:
                user.password = new_password
                user.bio = new_bio
                self.save_users()
                return
        raise ValueError("User not found.")

    def logout_user(self) -> None:
        # Placeholder for logout functionality
        pass