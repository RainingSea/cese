class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def get_user_profile(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def save_users(self):
        with open(self.filename, 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")