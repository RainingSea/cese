class User:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user[0] == username and user[1] == password:
                return True
        return False

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    users.append(line.strip().split('|'))
        except FileNotFoundError:
            return users
        return users