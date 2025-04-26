class StoryManager:
    def __init__(self):
        self.stories = self.load_stories()
        self.bookmarks = self.load_bookmarks()

    def load_stories(self) -> list:
        stories = []
        with open('stories.txt', 'r') as file:
            for line in file:
                stories.append(line.strip())
        return stories

    def load_bookmarks(self) -> dict:
        bookmarks = {}
        with open('bookmarks.txt', 'r') as file:
            for line in file:
                username, story_id = line.strip().split('|')
                if username not in bookmarks:
                    bookmarks[username] = []
                bookmarks[username].append(int(story_id))
        return bookmarks

    def get_story_details(self, story_id: int) -> str:
        return self.stories[story_id]

    def bookmark_story(self, username: str, story_id: int) -> bool:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if story_id in self.bookmarks[username]:
            return False
        self.bookmarks[username].append(story_id)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{username}|{story_id}\n")
        return True

    def get_bookmarks(self, username: str) -> list:
        return self.bookmarks.get(username, [])