class User:
    def __init__(self, username: str, password: str):
        """Initialize a User with username and password."""
        self.username = username
        self.password = password

    def save(self) -> None:
        """Save the user to the users.txt file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str) -> 'User':
        """Load a user by username from the users.txt file."""
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None