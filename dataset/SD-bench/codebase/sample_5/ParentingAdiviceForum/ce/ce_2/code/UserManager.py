import json
import os

class UserManager:
    def __init__(self, data_file='users.txt'):
        self.data_file = data_file
        self.load_users()

    def load_users(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]
        else:
            self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user[0] == username:
                user[1] = new_info.get('password', user[1])
                self.save_users()
                return True
        return False

    def delete_account(self, username: str) -> bool:
        for user in self.users:
            if user[0] == username:
                self.users.remove(user)
                self.save_users()
                return True
        return False

    def save_users(self):
        with open(self.data_file, 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')