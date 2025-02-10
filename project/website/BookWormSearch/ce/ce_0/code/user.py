class User:
    def __init__(self):
        self.users_file = 'users.txt'
    
    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if username in users:
            return False
        users[username] = password
        self.save_users(users)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def save_users(self, users: dict):
        with open(self.users_file, 'w') as file:
            for username, password in users.items():
                file.write(f"{username}|{password}\n")