class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self):
        self.stories = {}
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split('|')
                    if username not in self.stories:
                        self.stories[username] = []
                    self.stories[username].append((title, content))
        except FileNotFoundError:
            pass

    def save_story(self, username: str, title: str, content: str) -> None:
        with open(self.stories_file, 'a') as file:
            file.write(f"{username}|{title}|{content}\n")
        if username not in self.stories:
            self.stories[username] = []
        self.stories[username].append((title, content))

    def edit_story(self, username: str, title: str, new_content: str) -> None:
        # This method can be implemented if needed
        pass

    def load_stories(self, username: str) -> list:
        return self.stories.get(username, [])