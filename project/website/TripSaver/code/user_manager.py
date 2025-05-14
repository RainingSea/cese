class UserManager:
    def __init__(self, file_path='users.txt'):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        try:
            with open(self.file_path, 'r'):
                pass
        except FileNotFoundError:
            with open(self.file_path, 'w'):
                pass

    def register(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
            
        with open(self.file_path, 'r') as file:
            for line in file:
                existing_username, _ = line.strip().split('|')
                if existing_username == username:
                    return False, "Username already exists"

        with open(self.file_path, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True, "Registration successful"

    def login(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
            
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    existing_username, existing_password = line.strip().split('|')
                    if existing_username == username and existing_password == password:
                        return True, "Login successful"
        except FileNotFoundError:
            return False, "User database not found"
        return False, "Invalid credentials"