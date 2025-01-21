class BookmarkManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def add_bookmark(self, article_id: str) -> None:
        self.bookmarks.append(article_id)
        self._save_bookmarks()

    def get_bookmarks(self) -> list:
        return self.bookmarks

    def _save_bookmarks(self) -> None:
        with open(self.file_path, 'w') as file:
            for bookmark in self.bookmarks:
                file.write(bookmark + '\n')