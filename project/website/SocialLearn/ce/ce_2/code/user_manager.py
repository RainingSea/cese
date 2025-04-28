class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user['username']}|{user['password']}\n")