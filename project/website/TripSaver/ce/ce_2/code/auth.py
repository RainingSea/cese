from flask import redirect, url_for, request, flash

class AuthManager:
    def __init__(self, users_file):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                existing_user, _ = line.strip().split('|')
                if existing_user == username:
                    return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False