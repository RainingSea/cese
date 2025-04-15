from flask import session
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password  # Store plain password for login

class UserManager:
    def __init__(self):
        self.users: List[User] = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username is not already taken."""
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, generate_password_hash(password)))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        """Log in a user by verifying username and password."""
        for user in self.users:
            if user.username == username and check_password_hash(user.password, password):
                session['username'] = username
                return True
        return False

    def load_users(self) -> None:
        """Load users from a file."""
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        """Save users to a file."""
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")