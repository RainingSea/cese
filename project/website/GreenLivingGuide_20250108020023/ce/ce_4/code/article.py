class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        pass  # Not used, as we are directly writing to the file