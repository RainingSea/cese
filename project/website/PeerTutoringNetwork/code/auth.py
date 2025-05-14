from flask import flash
import os

class AuthHandler:
    def __init__(self, users_file):
        self.users_file = users_file
        self._ensure_file_exists()
    
    def register(self, username, password, email):
        if not self._validate_user_data(username, password, email):
            return False
        
        users = self._read_users_file()
        if any(user.split('|')[0] == username for user in users):
            flash('Username already exists')
            return False
        
        users.append(f"{username}|{password}|{email}")
        self._write_users_file(users)
        return True
    
    def login(self, username, password):
        users = self._read_users_file()
        for user in users:
            parts = user.split('|')
            if parts[0] == username and parts[1] == password:
                return True
        return False
    
    def get_user(self, username):
        users = self._read_users_file()
        for user in users:
            parts = user.split('|')
            if parts[0] == username:
                return {
                    'username': parts[0],
                    'email': parts[2] if len(parts) > 2 else ''
                }
        return None
    
    def _validate_user_data(self, username, password, email):
        if not username or not password or not email:
            flash('All fields are required')
            return False
        if '|' in username or '|' in password or '|' in email:
            flash('Invalid character in input')
            return False
        return True
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.users_file):
            open(self.users_file, 'a').close()
    
    def _read_users_file(self):
        try:
            with open(self.users_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
    
    def _write_users_file(self, users):
        try:
            with open(self.users_file, 'w') as f:
                f.write('\n'.join(users))
            return True
        except Exception as e:
            flash('Error saving user data')
            return False