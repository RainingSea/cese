class User:
    """User class to handle user-related operations."""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self) -> None:
        """Save user information to the users.txt file."""
        try:
            with open('users.txt', 'a') as file:
                file.write(f"{self.username}|{self.password}\n")
        except Exception as e:
            print(f"Error saving user: {e}")