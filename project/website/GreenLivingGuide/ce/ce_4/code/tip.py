class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}\n")