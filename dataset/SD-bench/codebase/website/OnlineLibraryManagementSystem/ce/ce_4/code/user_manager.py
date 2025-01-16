class UserManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.filepath, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filepath, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def list_users(self) -> list:
        return list(self.users.keys())