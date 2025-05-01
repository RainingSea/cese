class AuthManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        self._ensure_users_exist()

    def _ensure_users_exist(self):
        try:
            with open(self.users_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.users_file, 'w') as f:
                f.write("admin|admin123\n")

    def _load_users(self):
        with open(self.users_file, 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def _save_users(self, users):
        with open(self.users_file, 'w') as f:
            for user in users:
                f.write(f"{user[0]}|{user[1]}\n")

    def authenticate(self, username, password):
        users = self._load_users()
        return any(user[0] == username and user[1] == password for user in users)

    def register_user(self, username, password):
        if not username or not password:
            return False
        if self._user_exists(username):
            return False
        
        users = self._load_users()
        users.append((username, password))
        self._save_users(users)
        return True

    def _user_exists(self, username):
        users = self._load_users()
        return any(user[0] == username for user in users)