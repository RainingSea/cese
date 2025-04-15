import os

class User:
    users_file = 'users.txt'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def load_users(cls):
        users = {}
        if os.path.exists(cls.users_file):
            with open(cls.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self):
        if self.username not in User.load_users():
            with open(User.users_file, 'a') as file:
                file.write(f"{self.username}|{self.password}\n")
            return True
        return False