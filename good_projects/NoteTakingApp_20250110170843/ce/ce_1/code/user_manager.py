import bcrypt

class UserManager:
    def __init__(self, user_file):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        with open(self.user_file, 'r') as file:
            for line in file:
                username, hashed_password = line.strip().split(':')
                self.users[username] = hashed_password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(self.user_file, 'a') as file:
            file.write(f'{username}:{hashed_password.decode("utf-8")}\n')
        self.users[username] = hashed_password.decode('utf-8')
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.users[username].encode('utf-8'))

    def get_user_notes(self, username: str) -> list:
        notes_file = f'{username}_notes.txt'
        try:
            with open(notes_file, 'r') as file:
                return [line.strip().split('|') for line in file]
        except FileNotFoundError:
            return []