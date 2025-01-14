import logging
from story import Story

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.stories = self.load_stories()

    def save_story(self, story: Story) -> None:
        try:
            story.save()
            self.stories.append(story)
        except Exception as e:
            logging.error("Failed to save story: %s", e)
            raise

    def load_stories(self) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            logging.error("Stories file not found.")
            raise
        return stories