class UserManager:
    def __init__(self, user_file: str) -> None:
        self.user_file = user_file
        self.users = {}
        self.load_users()

    def load_users(self) -> None:
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_users(self) -> list:
        return list(self.users.keys())