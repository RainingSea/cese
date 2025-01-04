class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.submitted_recipes = []

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = User(username, password)
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        new_user = User(username, password)
        new_user.save()
        self.users[username] = new_user
        return True

    def login(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username].password == password

    def delete_account(self, username: str):
        if username in self.users:
            del self.users[username]
            self.save_users()

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users.values():
                f.write(f"{user.username}|{user.password}\n")