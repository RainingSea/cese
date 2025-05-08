class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def load_reading_list(self, username: str):
        reading_list_file = f"{username}_reading_list.txt"
        try:
            with open(reading_list_file, 'r') as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            return []