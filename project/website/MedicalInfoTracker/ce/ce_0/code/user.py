class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        users = self.load_users()
        if self.username not in [user.username for user in users]:
            with open('users.txt', 'a') as f:
                f.write(f"{self.username}|{self.password}\n")
            return True
        return False

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users