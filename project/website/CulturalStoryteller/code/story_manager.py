import json
from story import Story

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def load_stories(self) -> list[Story]:
        try:
            with open(self.stories_file, 'r') as f:
                stories_data = json.load(f)
                return [Story(**story) for story in stories_data]
        except FileNotFoundError:
            return []

    def search_stories(self, keyword: str) -> list[Story]:
        stories = self.load_stories()
        return [story for story in stories if keyword.lower() in story.title.lower()]