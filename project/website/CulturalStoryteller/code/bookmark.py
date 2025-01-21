class Bookmark:
    def __init__(self, user: str, story: str):
        self.user = user
        self.story = story

    def to_dict(self) -> dict:
        return {
            'user': self.user,
            'story': self.story
        }