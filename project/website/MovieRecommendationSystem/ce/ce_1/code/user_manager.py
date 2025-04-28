class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")