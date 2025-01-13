class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def add_user(self, username: str, password: str):
        user = User(username, password)
        self.users.append(user)
        user.save()

    def find_user(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None