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

    def load_stories(self, username: str = None):
        self.stories = {}
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    user, title, content = line.strip().split(':')
                    if username is None or user == username:
                        if user not in self.stories:
                            self.stories[user] = []
                        self.stories[user].append(Story(user, title, content))
        except FileNotFoundError:
            open(self.stories_file, 'w').close()

    def create_story(self, username: str, title: str, content: str):
        new_story = Story(username, title, content)
        new_story.save()
        if username not in self.stories:
            self.stories[username] = []
        self.stories[username].append(new_story)