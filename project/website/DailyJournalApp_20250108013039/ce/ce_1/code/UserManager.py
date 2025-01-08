from User import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self) -> None:
        self.users = {}
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users[username] = User(username, password)
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        user = User(username, password)
        user.save()
        self.users[username] = user
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.validate_password(password):
            return True
        return False

    def get_all_users(self) -> list:
        return list(self.users.keys())