class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username},{self.title},{self.content}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def create_story(self, username: str, title: str, content: str) -> None:
        story = Story(username, title, content)
        story.save()

    def edit_story(self, username: str, title: str, content: str) -> None:
        # This method can be implemented if required in the future
        pass