class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.user_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.user_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users