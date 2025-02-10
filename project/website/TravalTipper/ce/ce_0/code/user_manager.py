from models import User
import bcrypt

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users.append(User(username, password))

    def register_user(self, username: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username, hashed_password)
        self.users.append(new_user)
        self.save_users('users.txt')

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return True
        return False

    def save_users(self, file_path: str):
        with open(file_path, 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")