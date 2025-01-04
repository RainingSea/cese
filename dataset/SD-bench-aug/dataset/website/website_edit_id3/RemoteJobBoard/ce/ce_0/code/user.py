class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        users = User.load_users()
        with open('users.txt', 'w') as file:
            for user in users:
                if user.username == self.username:
                    file.write(f"{self.username}|{self.password}|{self.email}\n")
                else:
                    file.write(f"{user.username}|{user.password}|{user.email}\n")

    @staticmethod
    def load_users():
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users