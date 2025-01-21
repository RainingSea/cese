class User:
    """Represents a user in the system."""
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        """Saves the user to a file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str):
        """Loads a user by username."""
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

    @staticmethod
    def load_all():
        """Loads all users from the file."""
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users