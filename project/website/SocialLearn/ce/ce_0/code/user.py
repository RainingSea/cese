class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self):
        """Save the user to the users.txt file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")