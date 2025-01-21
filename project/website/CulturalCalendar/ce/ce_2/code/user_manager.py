class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def save_users(self):
        with open(self.filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")