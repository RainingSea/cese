import os

class User:
    def __init__(self, username: str = '', password: str = '', email: str = ''):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    def load_users(self) -> list:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    users.append(line.strip().split('|'))
        return users