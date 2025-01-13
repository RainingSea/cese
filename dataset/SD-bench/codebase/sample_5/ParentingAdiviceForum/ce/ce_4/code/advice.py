class Advice:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('advice.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")