class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as f:
            f.write(f'{username}|{password}\n')
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_users(self) -> list:
        return list(self.users.keys())