class Auth:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def register(self, username, password):
        for user in self.user_manager.users:
            if user[0] == username:
                return False  # Username already exists
        self.user_manager.save(username, password)
        return True

    def login(self, username, password):
        for user in self.user_manager.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def logout(self):
        pass  # Logout logic handled in main.py