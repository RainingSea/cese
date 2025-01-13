from user import User

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.add_user(username, password)

    def add_user(self, username: str, password: str):
        user = User(username, password)
        self.users.append(user)

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None