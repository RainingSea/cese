class User:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    users.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return users