class StoryManager:
    def __init__(self, stories_file: str, bookmarks_file: str):
        self.stories_file = stories_file
        self.bookmarks_file = bookmarks_file
        self.stories = self.load_stories()

    def load_stories(self) -> list:
        stories = []
        try:
            with open(self.stories_file, 'r') as file:
                for line in file:
                    story_id, title, content, cultural_background = line.strip().split('|')
                    stories.append({
                        'id': int(story_id),
                        'title': title,
                        'content': content,
                        'cultural_background': cultural_background
                    })
        except FileNotFoundError:
            pass
        return stories

    def get_story_details(self, story_id: int) -> dict:
        for story in self.stories:
            if story['id'] == story_id:
                return story
        return {}

    def bookmark_story(self, username: str, story_id: int) -> bool:
        with open(self.bookmarks_file, 'a') as file:
            file.write(f"{username}|{story_id}\n")
        return True

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open(self.bookmarks_file, 'r') as file:
                for line in file:
                    user, story_id = line.strip().split('|')
                    if user == username:
                        bookmarks.append(int(story_id))
        except FileNotFoundError:
            pass
        return bookmarks