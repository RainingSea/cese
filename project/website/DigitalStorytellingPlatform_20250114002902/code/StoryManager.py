class Story:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.username},{self.title},{self.content}\n")

class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self):
        self.stories = {}
        with open(self.stories_file, 'r') as f:
            for line in f:
                username, title, content = line.strip().split(',')
                self.stories[(username, title)] = Story(username, title, content)

    def create_story(self, username: str, title: str, content: str):
        story = Story(username, title, content)
        story.save()
        self.stories[(username, title)] = story

    def edit_story(self, username: str, title: str, new_content: str):
        if (username, title) in self.stories:
            self.stories[(username, title)].content = new_content
            self.save_all_stories()

    def save_all_stories(self):
        with open(self.stories_file, 'w') as f:
            for story in self.stories.values():
                f.write(f"{story.username},{story.title},{story.content}\n")

    def get_story(self, username: str, title: str):
        return self.stories.get((username, title))