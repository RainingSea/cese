class UserManager:
    def __init__(self):
        self.users = {}

    def load_users(self):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password