class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}:{self.password}:{self.email}\n")

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users[username] = new_user
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password

    def load_users(self) -> list:
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(':')
                    self.users[username] = User(username, password, email)
        except FileNotFoundError:
            pass