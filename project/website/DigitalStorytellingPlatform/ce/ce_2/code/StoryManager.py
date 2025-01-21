from models import Story

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.stories = self.load_stories()

    def create_story(self, title: str, content: str, author: str) -> None:
        new_story = Story(title, content, author)
        new_story.save()
        self.stories.append(new_story)

    def load_stories(self) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    stories.append(Story(title, content, author))
        except FileNotFoundError:
            pass
        return stories