class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username not in self.users:
            self.users[username] = password
            self.save_users()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")