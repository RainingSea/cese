from models import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in [user.username for user in self.users]:
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def load_users(self) -> list:
        users = []
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users