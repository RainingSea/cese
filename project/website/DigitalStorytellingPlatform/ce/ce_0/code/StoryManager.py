class Story:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def load_stories(self):
        stories = []
        with open(self.stories_file, 'r') as f:
            for line in f:
                title, content = line.strip().split('|')
                stories.append(Story(title, content))
        return stories

    def save_story(self, title: str, content: str):
        new_story = Story(title, content)
        new_story.save()