from story import Story

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def load_stories(self):
        stories = []
        with open(self.stories_file, 'r') as f:
            for line in f:
                username, title, content = line.strip().split('|')
                stories.append(Story(username, title, content))
        return stories

    def save_story(self, story: Story):
        story.save()