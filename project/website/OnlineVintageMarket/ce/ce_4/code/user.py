class User:
    def __init__(self, username: str = '', password: str = '') -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def load_users(self) -> list:
        users_list = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users_list.append(User(username, password))
        except FileNotFoundError:
            pass
        return users_list