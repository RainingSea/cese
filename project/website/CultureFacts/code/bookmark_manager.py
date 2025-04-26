class BookmarkManager:
    def __init__(self):
        self.bookmarks = []

    def add_bookmark(self, culture_name: str) -> None:
        if culture_name not in self.bookmarks:
            self.bookmarks.append(culture_name)
            self.save_bookmarks()

    def remove_bookmark(self, culture_name: str) -> None:
        if culture_name in self.bookmarks:
            self.bookmarks.remove(culture_name)
            self.save_bookmarks()

    def load_bookmarks(self) -> None:
        try:
            with open('bookmarks.txt', 'r') as file:
                self.bookmarks = file.read().strip().splitlines()
        except FileNotFoundError:
            self.bookmarks = []

    def save_bookmarks(self) -> None:
        with open('bookmarks.txt', 'w') as file:
            file.write('\n'.join(self.bookmarks))