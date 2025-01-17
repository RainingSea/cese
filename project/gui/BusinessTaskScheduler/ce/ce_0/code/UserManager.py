import json

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                users_data = json.load(file)
                self.users = [User(**user) for user in users_data]
        except FileNotFoundError:
            self.users = []

    def save_users(self, file_path: str):
        with open(file_path, 'w') as file:
            json.dump([{"name": user.name, "email": user.email} for user in self.users], file)

    def add_user(self, name: str, email: str):
        new_user = User(name, email)
        self.users.append(new_user)
        self.save_users('users.txt')

    def get_all_users(self) -> list:
        return [{"name": user.name, "email": user.email} for user in self.users]