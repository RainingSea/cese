class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}:{self.title}:{self.content}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self, username: str) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    user, title, content = line.strip().split(':')
                    if user == username:
                        stories.append(Story(user, title, content))
        except FileNotFoundError:
            pass
        return stories

    def create_story(self, username: str, title: str, content: str) -> None:
        story = Story(username, title, content)
        story.save()

    def edit_story(self, username: str, title: str, content: str) -> None:
        # This function is not implemented as per the current design
        pass