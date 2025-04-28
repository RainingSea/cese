class UserManager:
    def __init__(self, filename):
        self.users = self.load_users(filename)

    def load_users(self, filename):
        users = {}
        with open(filename, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def login(self, username, password):
        return self.users.get(username) == password

    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True