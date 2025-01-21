class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            open(self.user_file, 'w').close()  # Create the file if it doesn't exist

    def register(self, username: str, password: str) -> bool:
        if self.is_username_taken(username):
            return False
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def is_username_taken(self, username: str) -> bool:
        return username in self.users