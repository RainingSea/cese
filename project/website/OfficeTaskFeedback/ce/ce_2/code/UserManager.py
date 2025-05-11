class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if username not in self.users:
            self.users[username] = password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def is_manager(self, username: str) -> bool:
        return username == 'admin'  # Example logic for manager check

    def logout(self) -> None:
        pass  # Session management handled in main.py