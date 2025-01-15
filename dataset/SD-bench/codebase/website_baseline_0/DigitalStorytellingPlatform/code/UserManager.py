class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")


class UserManager:
    def __init__(self, users_file: str = 'users.txt'):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in [user.username for user in self.users]:
            return False  # User already exists
        user = User(username, password, email)
        user.save()
        self.users.append(user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def load_users(self) -> list:
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass  # No users file found
        return users