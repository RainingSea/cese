class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username][0] == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        except FileNotFoundError:
            pass
        return users