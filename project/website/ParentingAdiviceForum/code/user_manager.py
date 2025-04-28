import os

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # Username already exists
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user[0] == username:
                user[1] = new_info.get('password', user[1])
                self.save_users()
                return True
        return False

    def delete_account(self, username: str) -> bool:
        self.users = [user for user in self.users if user[0] != username]
        self.save_users()
        return True