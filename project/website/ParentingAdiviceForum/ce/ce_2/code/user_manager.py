import json

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}
        except FileNotFoundError:
            return {}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_user(self, username: str) -> dict:
        return {'username': username, 'password': self.users.get(username)}

    def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")