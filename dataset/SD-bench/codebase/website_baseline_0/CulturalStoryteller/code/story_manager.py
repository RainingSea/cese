class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()

    def load_stories(self) -> list:
        """Load stories from a file into a list."""
        stories = []
        try:
            with open('stories.txt', 'r') as file:
                for line in file:
                    story_id, title, content, cultural_info = line.strip().split('|')
                    stories.append({
                        'id': int(story_id),
                        'title': title,
                        'content': content,
                        'cultural_info': cultural_info
                    })
        except FileNotFoundError:
            pass
        return stories

    def get_story_details(self, story_id: int) -> dict:
        """Get the details of a specific story by its ID."""
        for story in self.stories:
            if story['id'] == story_id:
                return story
        return {}

    def search_stories(self, query: str) -> list:
        """Search for stories that contain the query in their title."""
        return [story for story in self.stories if query.lower() in story['title'].lower()]

    def load_bookmarks(self, username: str) -> list:
        """Load bookmarks for a specific user from a file."""
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    user, story_id = line.strip().split('|')
                    if user == username:
                        bookmarks.append(int(story_id))
        except FileNotFoundError:
            pass
        return bookmarks

    def save_bookmarks(self, username: str, bookmarks: list) -> None:
        """Save bookmarks for a specific user to a file."""
        with open('bookmarks.txt', 'w') as file:
            for story_id in bookmarks:
                file.write(f"{username}|{story_id}\n")

    def manage_bookmarks(self, username: str) -> list:
        """Manage bookmarks for a specific user."""
        return self.load_bookmarks(username)