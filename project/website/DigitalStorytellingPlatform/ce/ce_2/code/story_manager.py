class StoryManager:
    def __init__(self, stories_file: str):
        self.stories_file = stories_file
        self.load_stories()

    def load_stories(self):
        """Load stories from the stories file into memory."""
        self.stories = []
        if os.path.exists(self.stories_file):
            with open(self.stories_file, 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    self.stories.append({'title': title, 'content': content, 'username': username})

    def create_story(self, title: str, content: str, username: str) -> bool:
        """Create a new story."""
        with open(self.stories_file, 'a') as file:
            file.write(f"{title}|{content}|{username}\n")
        self.stories.append({'title': title, 'content': content, 'username': username})
        return True

    def edit_story(self, title: str, content: str, username: str) -> bool:
        """Edit an existing story."""
        for story in self.stories:
            if story['title'] == title and story['username'] == username:
                story['content'] = content
                self.save_stories()
                return True
        return False

    def save_stories(self) -> bool:
        """Save all stories back to the stories file."""
        with open(self.stories_file, 'w') as file:
            for story in self.stories:
                file.write(f"{story['title']}|{story['content']}|{story['username']}\n")
        return True