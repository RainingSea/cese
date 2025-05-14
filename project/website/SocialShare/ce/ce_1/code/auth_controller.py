import os

class AuthController:
    def __init__(self):
        self.users_file = "users.txt"
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                existing_username, _ = line.strip().split('|')
                if existing_username == username:
                    return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                existing_username, existing_password = line.strip().split('|')
                if existing_username == username and existing_password == password:
                    return True
        return False

    def logout(self):
        return True