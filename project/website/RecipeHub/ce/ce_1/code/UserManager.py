class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self, users_file: str = 'users.txt'):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        user = User(username, password)
        user.save_to_file()
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            self.save_all_users()
            return True
        return False

    def save_all_users(self):
        with open(self.users_file, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")