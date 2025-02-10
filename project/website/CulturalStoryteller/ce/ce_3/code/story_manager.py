class StoryManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.stories = self.load_stories()

    def load_stories(self) -> list:
        stories = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    story_id, title, content, cultural_background = line.strip().split('|')
                    stories.append({
                        'id': int(story_id),
                        'title': title,
                        'content': content,
                        'cultural_background': cultural_background
                    })
        except FileNotFoundError:
            pass
        return stories

    def get_story_details(self, story_id: int) -> dict:
        for story in self.stories:
            if story['id'] == story_id:
                return story
        return {}