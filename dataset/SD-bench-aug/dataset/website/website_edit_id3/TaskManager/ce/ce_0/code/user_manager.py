class UserManager:
    def __init__(self, filename='users.txt'):
        self.filename = filename

    def register(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        if username in [user[0] for user in users]:
            return False  # User already exists
        with open(self.filename, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user[0] == username and user[1] == password for user in users)

    def load_users(self) -> list:
        users = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    users.append(line.strip().split('|'))
        except FileNotFoundError:
            pass  # File doesn't exist yet
        return users