class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append({'username': username, 'password': password, 'email': email})
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{email}\n")
        self.users.append({'username': username, 'password': password, 'email': email})

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False