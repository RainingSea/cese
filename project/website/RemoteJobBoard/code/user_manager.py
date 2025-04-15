class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_user_profile(self, username: str) -> dict:
        return {'username': username}

    def edit_profile(self, username: str, new_data: dict) -> None:
        if username in self.users:
            self.users[username] = new_data.get('username', self.users[username])
            self.save_users()

    def save_users(self):
        with open(self.users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")