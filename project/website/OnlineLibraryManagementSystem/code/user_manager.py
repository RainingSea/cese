class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, *entries = line.strip().split('|')
                    self.users[username] = (password, entries)
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create the file if it doesn't exist

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = (password, [])
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

    def list_users(self) -> list:
        return list(self.users.keys())