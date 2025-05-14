from flask import redirect, url_for, session

class AuthManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        try:
            with open(self.users_file, 'a+') as f:
                f.seek(0)
                for line in f:
                    if line.startswith(username + ':'):
                        return False
                f.write(f"{username}:{password}\n")
                return True
        except IOError:
            return False

    def login(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split(':')
                    if stored_username == username and stored_password == password:
                        return True
            return False
        except IOError:
            return False