class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save_story(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")

class StoryManager:
    def create_story(self, username: str, title: str, content: str):
        story = Story(username, title, content)
        story.save_story()

    def load_stories(self) -> list:
        stories = []
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',')
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            pass
        return stories