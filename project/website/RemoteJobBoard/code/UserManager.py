class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password, *entries = line.strip().split('|')
                    self.users[username] = {'password': password, 'entries': entries}
        except FileNotFoundError:
            open(self.user_file, 'w').close()  # Create file if it doesn't exist

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'entries': []}
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username]['password'] == password

    def get_user_profile(self, username: str) -> dict:
        return self.users.get(username, {})

    def update_user_profile(self, username: str, new_password: str) -> bool:
        if username in self.users:
            self.users[username]['password'] = new_password
            self.save_users()
            return True
        return False

    def save_users(self):
        with open(self.user_file, 'w') as file:
            for username, data in self.users.items():
                entries = ','.join(data['entries'])
                file.write(f"{username}|{data['password']}|{entries}\n")