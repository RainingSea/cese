class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, interests = line.strip().split('|')
                    users[username] = {'password': password, 'interests': interests}
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'interests': ''}
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username]['password'] == password

    def update_profile(self, username: str, interests: str) -> bool:
        if username in self.users:
            self.users[username]['interests'] = interests
            self.save_users()
            return True
        return False

    def save_users(self):
        with open(self.filename, 'w') as file:
            for username, data in self.users.items():
                file.write(f"{username}|{data['password']}|{data['interests']}\n")