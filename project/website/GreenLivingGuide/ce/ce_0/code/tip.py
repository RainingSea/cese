class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}|{self.author}\n")