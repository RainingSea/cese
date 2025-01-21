class User:
    """User class to represent a user in the system."""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self):
        """Save user information to the users.txt file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_from_file():
        """Load users from the users.txt file."""
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users