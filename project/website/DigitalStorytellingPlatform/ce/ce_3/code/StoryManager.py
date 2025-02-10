class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('stories.txt', 'a') as f:
            f.write(f"{self.username}|{self.title}|{self.content}\n")


class StoryManager:
    def create_story(self, username: str, title: str, content: str) -> None:
        story = Story(username, title, content)
        story.save()

    def load_stories(self) -> list:
        stories = []
        try:
            with open('stories.txt', 'r') as f:
                for line in f:
                    username, title, content = line.strip().split('|')
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            pass  # File does not exist yet
        return stories