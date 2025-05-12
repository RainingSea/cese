class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user['username'] == username:
                user.update(new_info)
                self.save_users()
                return True
        return False

    def delete_account(self, username: str) -> bool:
        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                self.save_users()
                return True
        return False