class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")

    def validate_password(self, password: str) -> bool:
        return self.password == password


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        user = User(username, password, email)
        user.save()
        self.users.append(user)  # Update in-memory list
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.validate_password(password) for user in self.users)