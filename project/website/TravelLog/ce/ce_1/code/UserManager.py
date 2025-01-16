class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in [user.split(',')[0] for user in self.users]:
            return False
        with open(self.filename, 'a') as f:
            f.write(f"{username},{password}\n")
        self.users.append(f"{username},{password}")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user == f"{username},{password}" for user in self.users)

    def load_users(self) -> list:
        try:
            with open(self.filename, 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []