class User:
    def __init__(self):
        self.users_file = 'users.txt'
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False

    def save_users(self):
        with open(self.users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")