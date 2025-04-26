class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> list:
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            open(self.users_file, 'w').close()  # Create file if it doesn't exist
        return users

    def login(self, username: str, password: str) -> bool:
        return (username, password) in self.users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))
        return True

    def get_users(self) -> list:
        return self.users