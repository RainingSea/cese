class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

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

    def login(self) -> bool:
        for user in User.load_users():
            if user.username == self.username and user.password == self.password:
                return True
        return False