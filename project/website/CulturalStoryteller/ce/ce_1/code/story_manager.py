from models import Story

class StoryManager:
    def load_stories(self) -> list:
        stories = []
        try:
            with open('stories.txt', 'r') as f:
                for line in f:
                    title, content, cultural_origin = line.strip().split('|')
                    stories.append(Story(title, content, cultural_origin))
        except FileNotFoundError:
            pass
        return stories

    def search_stories(self, query: str) -> list:
        stories = self.load_stories()
        return [story for story in stories if query.lower() in story.title.lower() or query.lower() in story.content.lower()]