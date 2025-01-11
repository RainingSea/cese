class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> bool:
        try:
            with open('users.txt', 'w') as file:
                for username, password in self.users.items():
                    file.write(f"{username}|{password}\n")
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False

    def add_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        return self.save_users()

    def validate_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password