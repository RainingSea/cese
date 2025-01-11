class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save_user(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username},{self.password},{self.email}\n")


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as f:
            for line in f:
                username, password, email = line.strip().split(',')
                self.users[username] = User(username, password, email)

    def register_user(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        new_user = User(username, password, email)
        new_user.save_user()
        self.users[username] = new_user
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.password == password:
            return True
        return False