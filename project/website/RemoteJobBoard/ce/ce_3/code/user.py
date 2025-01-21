class User:
    def __init__(self, username: str = '', password: str = '', email: str = ''):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def save(self) -> None:
        pass

    def load(self, username: str) -> 'User':
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None