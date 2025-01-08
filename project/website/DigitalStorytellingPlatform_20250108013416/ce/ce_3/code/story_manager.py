class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as file:
            file.write(f"{self.username}:{self.title}:{self.content}\n")

    def edit(self, title: str, content: str):
        self.title = title
        self.content = content

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def create_story(self, username: str, title: str, content: str):
        new_story = Story(username, title, content)
        new_story.save()
        self.stories.append(new_story)

    def load_stories(self, username: str = None) -> list:
        self.stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    user, title, content = line.strip().split(':')
                    if username is None or user == username:
                        self.stories.append(Story(user, title, content))
        except FileNotFoundError:
            pass
        return self.stories