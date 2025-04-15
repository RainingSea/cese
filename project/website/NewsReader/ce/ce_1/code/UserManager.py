class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self) -> None:
        """Load users from the users.txt file."""
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        """Save users to the users.txt file."""
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user if the username is not taken."""
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password))
        self.save_users()
        return True

    def login_user(self, username: str, password: str) -> bool:
        """Log in a user by checking username and password."""
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False