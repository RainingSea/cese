class User:
    def __init__(self):
        self.username = ''
        self.password = ''

    @staticmethod
    def load_users():
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                user = User()
                user.username = username
                user.password = password
                users.append(user)
        return users

    def register(self, username: str, password: str) -> bool:
        self.username = username
        self.password = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in User.load_users():
            if user.username == username and user.password == password:
                return True
        return False