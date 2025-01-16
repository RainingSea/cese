class User:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username, password):
        if any(user.username == username for user in self.load_users()):
            return False
        self.username = username
        self.password = password
        self.save()
        return True