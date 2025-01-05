class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def register(self, username: str, password: str) -> bool:
        users_data = self._read_users()
        if username in [user.split('|')[0] for user in users_data]:
            return False 
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        users_data = self._read_users()
        for user in users_data:
            if user.split('|')[0] == username and user.split('|')[1] == password:
                return True
        return False
    
    def _read_users(self) -> list:
        with open('users.txt', 'r') as f:
            return f.read().strip().split('\n')