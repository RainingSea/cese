class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        # Check if the username already exists
        for user in self.read_users():
            if user.split('|')[0] == username:
                return False
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.read_users():
            if user.split('|')[0] == username and user.split('|')[1] == password:
                return True
        return False

    def delete_account(self, username: str) -> bool:
        users = self.read_users()
        new_users = [user for user in users if user.split('|')[0] != username]
        if len(new_users) < len(users):
            with open('users.txt', 'w') as f:
                f.write('\n'.join(new_users))
            return True
        return False

    def read_users(self):
        with open('users.txt', 'r') as f:
            return f.read().strip().split('\n')