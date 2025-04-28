class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in [user.split('|')[0] for user in self.users]:
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append(f"{username}|{password}")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user == f"{username}|{password}" for user in self.users)

    def load_users(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            logging.error(f"File '{self.filename}' not found. Returning empty user list.")
            return []
        except Exception as e:
            logging.error(f"Error loading users from '{self.filename}': {e}")
            return []