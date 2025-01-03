class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password, *entries = line.strip().split('|')
                self.users[username] = {'password': password, 'entries': entries}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'entries': []}
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username]['password'] == password

    def delete_account(self, username: str) -> bool:
        if username not in self.users:
            return False
        del self.users[username]
        self.save_users()
        return True

    def save_users(self):
        with open(self.users_file, 'w') as file:
            for username, data in self.users.items():
                file.write(f"{username}|{data['password']}|{','.join(data['entries'])}\n")