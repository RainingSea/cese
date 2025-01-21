class Story:
    def __init__(self, title: str, content: str, cultural_background: str):
        self.title = title
        self.content = content
        self.cultural_background = cultural_background

    def get_story_details(self) -> dict:
        return {
            'title': self.title,
            'content': self.content,
            'cultural_background': self.cultural_background
        }