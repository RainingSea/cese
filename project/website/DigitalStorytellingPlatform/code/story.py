class Story:
    """Represents a story created by a user."""
    
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def save(self):
        """Saves the story information to a file."""
        with open('stories.txt', 'a') as f:
            f.write(f"{self.username},{self.title},{self.content}\n")

    @staticmethod
    def load_stories():
        """Loads stories from a file."""
        stories = []
        try:
            with open('stories.txt', 'r') as f:
                for line in f:
                    username, title, content = line.strip().split(',')
                    stories.append(Story(username, title, content))
        except FileNotFoundError:
            pass
        return stories