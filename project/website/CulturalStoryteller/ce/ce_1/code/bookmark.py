class Bookmark:
    def __init__(self, username: str, story_title: str):
        self.username = username
        self.story_title = story_title

    def save(self):
        pass  # Not needed for this implementation

    def load(self):
        return {"username": self.username, "story_title": self.story_title}