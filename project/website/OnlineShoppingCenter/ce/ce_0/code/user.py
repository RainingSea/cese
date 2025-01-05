class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users():
        users = []
        with open('users.txt', 'r') as file:
            for line in file.read().strip().split('\n'):
                username, password, email = line.split('|')
                users.append(User(username, password, email))
        return users