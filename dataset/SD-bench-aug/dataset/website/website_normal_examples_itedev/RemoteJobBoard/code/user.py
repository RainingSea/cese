class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except Exception as e:
            print(f"Error loading users: {e}")
        return users