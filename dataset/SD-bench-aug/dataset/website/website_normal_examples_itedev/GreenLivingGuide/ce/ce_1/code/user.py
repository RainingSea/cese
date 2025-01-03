class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            pass
        return users

    def authenticate(self) -> bool:
        users = User.load_users()
        for user in users:
            if user[0] == self.username and user[1] == self.password:
                return True
        return False