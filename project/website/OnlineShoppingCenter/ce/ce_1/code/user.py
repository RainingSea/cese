class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def load_users(cls) -> list:
        users_list = []
        with open('users.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')
                if len(data) == 3:
                    user = cls(data[0], data[1], data[2])
                    users_list.append(user)
        return users_list

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")