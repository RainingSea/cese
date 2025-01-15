import bcrypt

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        if self.load_users():
            for user in self.load_users():
                if user.username == username:
                    return False  # User already exists
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
        return False

    def load_users(self) -> list:
        users = []
        with open(self.users_file, 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                users.append(User(user_data[0], user_data[1]))
        return users