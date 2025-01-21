class User:
    """Represents a user in the system."""
    
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        """Saves the user information to a file."""
        with open('users.txt', 'a') as f:
            f.write(f"{self.username},{self.password},{self.email}\n")

    @staticmethod
    def load_users():
        """Loads users from a file."""
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users