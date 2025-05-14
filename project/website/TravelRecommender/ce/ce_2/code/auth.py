from flask import session

class AuthManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        try:
            with open(self.users_file, 'a+') as f:
                f.seek(0)
                for line in f:
                    if line.split('|')[0] == username:
                        return False
                f.write(f"{username}|{password}\n")
                return True
        except IOError:
            return False

    def login(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username and parts[1] == password:
                        session['username'] = username
                        return True
            return False
        except IOError:
            return False

    def is_logged_in(self):
        return 'username' in session

    def logout(self):
        session.pop('username', None)