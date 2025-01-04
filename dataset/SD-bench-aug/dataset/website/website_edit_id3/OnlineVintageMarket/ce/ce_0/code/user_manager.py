class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def add_user(self, username: str, password: str) -> None:
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def authenticate(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False