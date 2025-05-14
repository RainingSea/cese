class AuthHandler:
    def __init__(self, users_file):
        self.users_file = users_file

    def validate_login(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                        return True
        except FileNotFoundError:
            return False
        return False

    def create_user(self, username, password, email):
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username}|{password}|{email}\n")
            return True
        except:
            return False

    def get_user_info(self, username):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username:
                        return {
                            'username': parts[0],
                            'email': parts[2] if len(parts) > 2 else ''
                        }
        except FileNotFoundError:
            return None
        return None