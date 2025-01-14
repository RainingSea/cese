from user import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(':')
                    self.users[username] = User(username, password)
        except FileNotFoundError:
            open(self.users_file, 'w').close()  # Create file if it doesn't exist

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