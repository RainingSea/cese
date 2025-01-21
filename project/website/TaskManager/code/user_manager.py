class UserManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.users = self.load_users()

    def load_users(self) -> dict:
        """Load users from the users.txt file."""
        users_data = self.file_handler.read_file('users.txt')
        users = {}
        for line in users_data:
            username, password, email = line.strip().split('|')
            users[username] = {'password': password, 'email': email}
        return users

    def register_user(self, username: str, password: str, email: str) -> bool:
        """Register a new user if the username does not already exist."""
        if username not in self.users:
            self.users[username] = {'password': password, 'email': email}
            self.file_handler.append_to_file('users.txt', f"{username}|{password}|{email}")
            return True
        return False

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user based on username and password."""
        return username in self.users and self.users[username]['password'] == password