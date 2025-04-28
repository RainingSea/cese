class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass  # If the file does not exist, return an empty dictionary
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users or not username or not password:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def logout(self) -> None:
        pass  # No action needed for logout