from user import User

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        user = User(username, password, email)
        user.save()
        self.users[username] = user
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.password == password:
            return True
        return False

    def load_users(self) -> dict:
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users[username] = User(username, password, email)
        except FileNotFoundError:
            pass
        return users