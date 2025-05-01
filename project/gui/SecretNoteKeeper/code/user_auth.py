import os

class UserAuth:
    def __init__(self):
        self.user_data_file = 'users.txt'
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register_user(self, username: str, password: str) -> None:
        if username not in self.users:
            self.users[username] = password
            with open(self.user_data_file, 'a') as f:
                f.write(f"{username}|{password}\n")
        else:
            raise ValueError("User already exists.")

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password