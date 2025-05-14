class AuthManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password, confirm_password):
        if password != confirm_password:
            return False
            
        users = self._load_users()
        if username in users:
            return False
            
        users[username] = password
        self._save_users(users)
        return True

    def login(self, username, password):
        users = self._load_users()
        return username in users and users[username] == password

    def _load_users(self):
        users = {}
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def _save_users(self, users):
        with open(self.users_file, 'w') as f:
            for username, password in users.items():
                f.write(f"{username}|{password}\n")