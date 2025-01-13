class Story:
    def __init__(self, title: str, content: str, username: str):
        self.title = title
        self.content = content
        self.username = username

    def save(self) -> None:
        with open('stories.txt', 'a') as f:
            f.write(f"{self.username}|{self.title}|{self.content}\n")


class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def save_story(self, title: str, content: str, username: str) -> None:
        story = Story(title, content, username)
        story.save()

    def get_stories(self, username: str) -> list:
        stories = []
        with open(self.stories_file, 'r') as f:
            for line in f:
                user, title, content = line.strip().split('|')
                if user == username:
                    stories.append((title, content))
        return stories