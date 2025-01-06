class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def exists(username: str) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                if user.split('|')[0] == username:
                    return True
        return False

class UserManager:
    def register(self, username: str, password: str) -> bool:
        if not User.exists(username):
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                if user.strip() == f"{username}|{password}":
                    return True
        return False

    def load_users(self) -> list:
        users = []
        with open('users.txt', 'r') as f:
            users = [line.strip() for line in f.readlines()]
        return users