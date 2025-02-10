import json

class User:
    def __init__(self, username: str, password: str, bio: str):
        self.username = username
        self.password = password
        self.bio = bio

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
            'bio': self.bio
        }

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, bio = line.strip().split('|')
                    user = User(username, password, bio)
                    self.users.append(user)
        except FileNotFoundError:
            pass

    def save_user(self, user: User) -> None:
        self.users.append(user)
        with open('users.txt', 'a') as f:
            f.write(f"{user.username}|{user.password}|{user.bio}\n")

    def authenticate(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def update_user_bio(self, username: str, bio: str) -> None:
        for user in self.users:
            if user.username == username:
                user.bio = bio
                self.save_all_users()
                break

    def save_all_users(self) -> None:
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user.username}|{user.password}|{user.bio}\n")