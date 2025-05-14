import os
import tempfile

class UserManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

    def add_user(self, username, password):
        users = self.list_users()
        if any(user[0] == username for user in users):
            raise ValueError("Username already exists")
        
        with open(self.file_path, 'a') as f:
            f.write(f"{username}|{password}\n")

    def validate_user(self, username, password):
        users = self.list_users()
        return any(user[0] == username and user[1] == password for user in users)

    def list_users(self):
        users = []
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    username, password = line.split('|')
                    users.append((username, password))
        return users