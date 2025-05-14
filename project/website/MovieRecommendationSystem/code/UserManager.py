class UserManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.users_file = 'users.txt'

    def login(self, username, password):
        users = self.file_handler.read_file(self.users_file)
        for user in users:
            parts = user.split('|')
            if len(parts) == 2:
                stored_username, stored_password = parts
                if stored_username == username and stored_password == password:
                    return True
        return False

    def register(self, username, password):
        if not username or not password:
            return False
            
        users = self.file_handler.read_file(self.users_file)
        for user in users:
            parts = user.split('|')
            if len(parts) == 2:
                stored_username, _ = parts
                if stored_username == username:
                    return False
        
        users.append(f"{username}|{password}")
        self.file_handler.write_file(self.users_file, users)
        return True