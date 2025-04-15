import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password}\n")

    def validate_password(self, password: str) -> bool:
        return self.password == password


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate_password(password):
                return True
        return False

    def load_users(self) -> list:
        users = []
        if not os.path.exists(self.users_file):
            return users
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append(User(username, password))
        return users