class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append({'username': username, 'password': password, 'email': email})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return users

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password, 'email': email})
        self.save_users()
        return True

    def update_profile(self, username: str, new_info: dict) -> bool:
        for user in self.users:
            if user['username'] == username:
                user.update(new_info)
                self.save_users()
                return True
        return False

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}|{user['email']}\n")