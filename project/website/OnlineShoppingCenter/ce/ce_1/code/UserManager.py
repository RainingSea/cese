class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.users = {}

    def load_users(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str, email: str) -> bool:
        if username not in self.users:
            self.users[username] = {'password': password, 'email': email}
            with open(self.filename, 'a') as file:
                file.write(f"{username}|{password}|{email}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username]['password'] == password