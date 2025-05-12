class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.filename, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = password

    def register(self, username, password):
        if username not in self.users:
            self.users[username] = password
            with open(self.filename, 'a') as file:
                file.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username, password):
        return self.users.get(username) == password

    def get_user(self, username):
        return self.users.get(username)

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False

    def save_users(self):
        with open(self.filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")