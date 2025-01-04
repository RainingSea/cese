class User:
    def __init__(self):
        self.file_manager = FileManager()

    def register(self, username: str, password: str) -> bool:
        users = self.file_manager.read_users()
        if username not in [user.split('|')[0] for user in users]:
            self.file_manager.write_user(username, password)
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        users = self.file_manager.read_users()
        return any(user.split('|')[0] == username and user.split('|')[1] == password for user in users)

    def delete_account(self, username: str) -> bool:
        users = self.file_manager.read_users()
        if username in [user.split('|')[0] for user in users]:
            users = [user for user in users if user.split('|')[0] != username]
            with open('users.txt', 'w') as f:
                f.write('\n'.join(users))
            return True
        return False