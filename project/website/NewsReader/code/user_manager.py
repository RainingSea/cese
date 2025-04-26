import os
from typing import List, Tuple

class UserManager:
    def __init__(self):
        self.users: List[Tuple[str, str]] = []
        self.load_users()

    def add_user(self, username: str, password: str) -> Tuple[bool, str]:
        if any(user[0] == username for user in self.users):
            return False, "Username already exists."
        self.users.append((username, password))
        self.save_users()
        return True, "User registered successfully."

    def validate_user(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')