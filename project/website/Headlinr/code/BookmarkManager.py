import os

class BookmarkManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_bookmarks(self) -> None:
        with open(self.file_path, 'w') as file:
            for bookmark in self.bookmarks:
                file.write(f"{bookmark}\n")

    def add_bookmark(self, article_id: str) -> None:
        if article_id not in self.bookmarks:
            self.bookmarks.append(article_id)
            self.save_bookmarks()

    def remove_bookmark(self, article_id: str) -> None:
        if article_id in self.bookmarks:
            self.bookmarks.remove(article_id)
            self.save_bookmarks()