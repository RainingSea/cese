class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = (password, email)
        self.save()
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

    def save(self):
        with open(self.filename, 'w') as file:
            for username, (password, email) in self.users.items():
                file.write(f"{username}|{password}|{email}\n")