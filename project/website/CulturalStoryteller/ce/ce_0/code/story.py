class Story:
    def __init__(self, title: str, content: str, cultural_origin: str):
        self.title = title
        self.content = content
        self.cultural_origin = cultural_origin

    def save(self):
        pass  # Not needed as we handle saving in main.py

    def load_all(self):
        pass  # Not needed as we handle loading in main.py