class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        users = User.load_all()
        with open('users.txt', 'w') as file:
            for user in users:
                if user.username != self.username:
                    file.write(f"{user.username}|{user.password}\n")
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user = line.strip().split('|')
                if user[0] == username:
                    return User(user[0], user[1])
        return None

    @staticmethod
    def load_all():
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users