class Story:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self) -> None:
        with open(f'stories/{self.author}_{self.title}.txt', 'w') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")