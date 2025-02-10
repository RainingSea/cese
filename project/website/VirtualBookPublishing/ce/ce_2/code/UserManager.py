class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.file_path, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_all_users(self) -> list:
        return list(self.users.keys())