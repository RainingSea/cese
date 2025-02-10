from user import User

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                self.add_user(User(username, password, email))

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")

    def add_user(self, user: User):
        self.users.append(user)
        self.save_users()

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None