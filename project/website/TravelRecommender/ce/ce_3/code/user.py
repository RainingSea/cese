class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_user(self):
        pass  # User management is handled in main.py

    def load_user(self):
        return {'username': self.username, 'password': self.password}