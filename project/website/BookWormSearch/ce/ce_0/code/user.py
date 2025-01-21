class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def load_users(file_path: str) -> dict:
        users = {}
        with open(file_path, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, users: dict) -> bool:
        if self.username in users:
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

    def login(self, users: dict) -> bool:
        return users.get(self.username) == self.password