class StoryManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.stories = self.load_stories()

    def save_story(self, username: str, title: str, content: str) -> None:
        """Saves a new story for the given user."""
        self.stories.append((username, title, content))
        self.save_stories()

    def load_stories(self) -> list:
        """Loads stories from the specified file."""
        stories = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split('|')
                    stories.append((username, title, content))
        except FileNotFoundError:
            pass
        return stories

    def edit_story(self, username: str, title: str, new_content: str) -> bool:
        """Edits an existing story for the given user."""
        for i, (user, story_title, _) in enumerate(self.stories):
            if user == username and story_title == title:
                self.stories[i] = (user, story_title, new_content)
                self.save_stories()
                return True
        return False

    def save_stories(self) -> None:
        """Saves the current stories to the specified file."""
        with open(self.filename, 'w') as file:
            for username, title, content in self.stories:
                file.write(f"{username}|{title}|{content}\n")