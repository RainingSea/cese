class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password