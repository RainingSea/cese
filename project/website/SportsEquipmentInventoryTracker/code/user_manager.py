from tools import load_users, save_users

class UserManager:
    def __init__(self):
        self.users = load_users()

    def register(self, username: str, password: str) -> dict:
        if any(user[0] == username for user in self.users):
            return {'success': False, 'message': 'Username already exists.'}
        self.users.append((username, password))
        save_users(self.users)
        return {'success': True, 'message': 'Registration successful, please log in.'}

    def login(self, username: str, password: str) -> dict:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return {'success': True, 'message': 'Login successful.'}
        return {'success': False, 'message': 'Invalid username or password.'}

    def load_users(self):
        self.users = load_users()

    def save_users(self):
        save_users(self.users)