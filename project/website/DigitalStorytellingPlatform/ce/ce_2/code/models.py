class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")


class Story:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self) -> None:
        with open('stories.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")