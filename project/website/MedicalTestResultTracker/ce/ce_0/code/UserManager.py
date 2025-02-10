import bcrypt

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if username in [user.split('|')[0] for user in users]:
            return False
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            stored_username, stored_password = user.split('|')
            if stored_username == username and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True
        return False

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []