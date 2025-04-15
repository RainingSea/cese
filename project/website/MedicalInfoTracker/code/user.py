class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def login(username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def save(self) -> bool:
        users = User.load_users()
        if self.username not in [user.username for user in users]:
            with open('users.txt', 'a') as file:
                file.write(f"{self.username}|{self.password}\n")
            return True
        return False