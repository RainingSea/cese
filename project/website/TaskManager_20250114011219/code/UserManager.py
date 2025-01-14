class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username},{self.password},{self.email}\n")

class UserManager:
    def register(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user.username == username and user.password == password for user in users)

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users