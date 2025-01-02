class Thread:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")