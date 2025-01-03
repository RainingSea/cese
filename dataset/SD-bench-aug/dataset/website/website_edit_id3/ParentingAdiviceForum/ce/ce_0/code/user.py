class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @classmethod
    def load_all(cls):
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(cls(username, password))
        except FileNotFoundError:
            pass
        return users

    def login(self):
        users = self.load_all()
        for user in users:
            if user.username == self.username and user.password == self.password:
                return True
        return False