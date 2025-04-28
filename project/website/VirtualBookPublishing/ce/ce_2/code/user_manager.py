class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                self.users[username] = password

    def register(self, username: str, password: str) -> None:
        with open(self.users_file, 'a') as file:
            file.write(f"{username}:{password}\n")
        self.users[username] = password

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password