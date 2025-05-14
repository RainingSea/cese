import os

class AuthManager:
    def __init__(self):
        self.users_file = 'users.txt'
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def register(self, username, password, email=''):
        if not username or not password:
            return False
        
        if self._user_exists(username):
            return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def _user_exists(self, username):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username = line.strip().split('|')[0]
                if stored_username == username:
                    return True
        return False