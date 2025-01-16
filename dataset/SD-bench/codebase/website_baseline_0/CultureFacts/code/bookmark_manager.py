class BookmarkManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.bookmarks = self.load_bookmarks()

    def add_bookmark(self, username: str, culture_name: str) -> bool:
        """Adds a bookmark for a user."""
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if culture_name in self.bookmarks[username]:
            return False
        self.bookmarks[username].append(culture_name)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{culture_name}\n")
        return True

    def get_bookmarks(self, username: str) -> list:
        """Retrieves bookmarks for a specific user."""
        return self.bookmarks.get(username, [])

    def load_bookmarks(self) -> dict:
        """Loads bookmarks from the specified file."""
        bookmarks = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, culture_name = line.strip().split('|')
                    if username not in bookmarks:
                        bookmarks[username] = []
                    bookmarks[username].append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks