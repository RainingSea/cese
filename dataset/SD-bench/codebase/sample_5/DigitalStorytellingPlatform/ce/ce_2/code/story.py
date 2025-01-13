class Story:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.author}\n")

    @staticmethod
    def load_all() -> list:
        stories = []
        with open('stories.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                stories.append(Story(title, content, author))
        return stories