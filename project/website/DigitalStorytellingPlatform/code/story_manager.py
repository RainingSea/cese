class Story:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file

    def create_story(self, title: str, content: str) -> None:
        story = Story(title, content)
        story.save()

    def edit_story(self, title: str, content: str) -> None:
        # This function can be implemented later if editing functionality is needed.
        pass