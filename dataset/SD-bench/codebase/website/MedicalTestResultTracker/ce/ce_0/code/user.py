class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_to_file(self, filename: str):
        with open(filename, 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_from_file(filename: str) -> list:
        users = []
        with open(filename, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users