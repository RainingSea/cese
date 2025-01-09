class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self) -> list:
        users = []
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def get_users(self) -> list:
        return self.users