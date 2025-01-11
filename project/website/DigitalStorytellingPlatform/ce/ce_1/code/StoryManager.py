class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save_story(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.username},{self.title},{self.content}\n")

    def edit_story(self, title: str, content: str):
        self.title = title
        self.content = content
        self.save_story()


class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self):
        self.stories = {}
        with open(self.stories_file, 'r') as f:
            for line in f:
                username, title, content = line.strip().split(',')
                if username not in self.stories:
                    self.stories[username] = []
                self.stories[username].append(Story(username, title, content))

    def save_story(self, story: Story):
        story.save_story()
        if story.username not in self.stories:
            self.stories[story.username] = []
        self.stories[story.username].append(story)

    def get_stories(self, username: str) -> list:
        return self.stories.get(username, [])