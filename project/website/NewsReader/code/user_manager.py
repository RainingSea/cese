class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> dict:
        if username in self.users:
            return {'success': False, 'message': 'Username already taken.'}
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return {'success': True, 'message': 'Registration successful.'}

    def login(self, username: str, password: str) -> dict:
        if username not in self.users:
            return {'success': False, 'message': 'Invalid credentials.'}
        if self.users[username] == password:
            return {'success': True, 'message': 'Login successful.'}
        return {'success': False, 'message': 'Invalid credentials.'}

    def logout(self) -> None:
        pass  # Session management is handled in main.py