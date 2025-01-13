class Post:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('posts.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.content}\n")