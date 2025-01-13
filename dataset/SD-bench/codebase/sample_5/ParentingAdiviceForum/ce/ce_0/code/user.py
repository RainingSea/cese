class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def delete(self) -> None:
        pass  # Deletion logic can be implemented later