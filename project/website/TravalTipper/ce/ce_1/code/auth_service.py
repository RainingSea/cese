from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a+') as file:
            file.seek(0)
            for line in file:
                existing_username, _ = line.strip().split('|')
                if existing_username == username:
                    return False
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False