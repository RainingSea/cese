class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")