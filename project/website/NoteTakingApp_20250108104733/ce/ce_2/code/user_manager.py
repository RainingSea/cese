class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.user_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def logout(self):
        pass  # Session management handled in main.py