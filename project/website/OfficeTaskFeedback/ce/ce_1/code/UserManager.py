class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username:
                return False  # User already exists
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False