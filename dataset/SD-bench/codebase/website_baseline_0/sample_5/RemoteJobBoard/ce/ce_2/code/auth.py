class Auth:
    def __init__(self):
        self.users_file = 'users.txt'
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                self.users[username] = {'password': password, 'email': email}

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user['password'] == password:
            return True
        return False

    def register(self, username: str, password: str, email: str) -> None:
        if username not in self.users:
            self.users[username] = {'password': password, 'email': email}
            with open(self.users_file, 'a') as file:
                file.write(f"{username}|{password}|{email}\n")

    def logout(self) -> None:
        pass  # Implement logout logic if necessary