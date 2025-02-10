class BookmarkManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.bookmarks = self.load_bookmarks()

    def add_bookmark(self, username: str, story_id: int) -> bool:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if story_id not in self.bookmarks[username]:
            self.bookmarks[username].append(story_id)
            self.save_bookmarks()
            return True
        return False

    def get_bookmarks(self, username: str) -> list:
        return self.bookmarks.get(username, [])

    def remove_bookmark(self, username: str, story_id: int) -> bool:
        if username in self.bookmarks and story_id in self.bookmarks[username]:
            self.bookmarks[username].remove(story_id)
            self.save_bookmarks()
            return True
        return False

    def load_bookmarks(self) -> dict:
        bookmarks = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, story_id = line.strip().split('|')
                    if username not in bookmarks:
                        bookmarks[username] = []
                    bookmarks[username].append(int(story_id))
        except FileNotFoundError:
            pass
        return bookmarks

    def save_bookmarks(self):
        with open(self.filename, 'w') as file:
            for username, story_ids in self.bookmarks.items():
                for story_id in story_ids:
                    file.write(f"{username}|{story_id}\n")