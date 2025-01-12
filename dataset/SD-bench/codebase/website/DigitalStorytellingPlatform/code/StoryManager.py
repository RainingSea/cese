import os

class Story:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")

    def edit(self, title: str, content: str):
        self.title = title
        self.content = content


class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def save_story(self, story: Story):
        story.save()

    def load_stories(self, author: str) -> list:
        stories = []
        if os.path.exists(self.stories_file):
            with open(self.stories_file, 'r') as f:
                for line in f:
                    title, content, story_author = line.strip().split('|')
                    if story_author == author:
                        stories.append(Story(title, content, story_author))
        return stories