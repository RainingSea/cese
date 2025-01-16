class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create file if it doesn't exist
        return users

    def register(self, username: str, password: str) -> bool:
        if not self.user_exists(username):
            self.users[username] = password
            with open(self.filename, 'a') as file:
                file.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        if self.user_exists(username):
            return self.users[username] == password
        return False

    def user_exists(self, username: str) -> bool:
        return username in self.users