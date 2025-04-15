import bcrypt

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, hashed_password = line.strip().split('|')
                    self.users[username] = hashed_password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if self.user_exists(username):
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{hashed_password}\n")
        self.users[username] = hashed_password
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users:
            return bcrypt.checkpw(password.encode('utf-8'), self.users[username].encode('utf-8'))
        return False

    def user_exists(self, username: str) -> bool:
        return username in self.users