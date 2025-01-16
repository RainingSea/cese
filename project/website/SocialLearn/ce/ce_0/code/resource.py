class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def save(self):
        pass  # Saving handled in main.py