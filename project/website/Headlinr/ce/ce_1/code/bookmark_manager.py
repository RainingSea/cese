class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def add_bookmark(self, article_id: str) -> None:
        self.bookmarks.append(article_id)
        self.save_bookmarks()

    def remove_bookmark(self, article_id: str) -> None:
        self.bookmarks.remove(article_id)
        self.save_bookmarks()

    def load_bookmarks(self) -> list:
        try:
            with open('bookmarks.txt', 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def save_bookmarks(self) -> None:
        with open('bookmarks.txt', 'w') as file:
            for bookmark in self.bookmarks:
                file.write(f'{bookmark}\n')