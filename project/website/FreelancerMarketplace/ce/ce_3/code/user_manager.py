class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f'{self.username}|{self.password}\n')


class UserManager:
    def create_user(self, username: str, password: str) -> User:
        user = User(username, password)
        user.save()
        return user

    def authenticate(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users