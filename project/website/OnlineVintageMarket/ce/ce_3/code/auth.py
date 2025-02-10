from user import User

class Auth:
    def __init__(self):
        self.users = self.load_users()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username:
                return False  # User already exists
        new_user = User(username, password)
        new_user.save()
        return True

    def load_users(self) -> list:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users