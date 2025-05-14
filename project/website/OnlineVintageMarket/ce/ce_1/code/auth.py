from flask import redirect, url_for, session
import os

class AuthManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self.sessions_file = 'sessions.txt'
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()
        if not os.path.exists(self.sessions_file):
            open(self.sessions_file, 'w').close()

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    with open(self.sessions_file, 'a') as sf:
                        sf.write(f"{username}\n")
                    return True
        return False

    def register(self, username, password, email):
        if not username or not password or not email:
            return False
            
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if parts[0] == username:
                    return False

        with open(self.users_file, 'a') as f:
            f.write(f"{username}:{password}:{email}\n")
        return True

    def is_logged_in(self, username):
        with open(self.sessions_file, 'r') as f:
            for line in f:
                if line.strip() == username:
                    return True
        return False