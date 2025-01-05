class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.content}\n")


class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def load_stories(self) -> list:
        stories = []
        with open(self.stories_file, 'r') as file:
            for line in file:
                username, title, content = line.strip().split('|')
                stories.append(Story(username, title, content))
        return stories

    def save_story(self, story: Story) -> None:
        story.save()