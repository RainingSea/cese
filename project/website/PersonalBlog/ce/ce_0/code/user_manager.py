class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.filename, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username][0] == password