class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.user_file, 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username, password):
        if username in self.users:
            return False
        with open(self.user_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username, password):
        return self.users.get(username) == password

    def logout(self):
        pass  # Session management handled in main.py