class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, _ = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as f:
            for username, password in self.users.items():
                f.write(f"{username}|{password}|\n")