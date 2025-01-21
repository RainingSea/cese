import json
from bookmark import Bookmark

class BookmarkManager:
    def __init__(self, bookmarks_file: str):
        self.bookmarks_file = bookmarks_file

    def add_bookmark(self, user: str, story: str) -> None:
        bookmarks = self.load_bookmarks(user)
        if not any(b['story'] == story for b in bookmarks):
            bookmarks.append(Bookmark(user, story).to_dict())
            self.save_bookmarks(user, bookmarks)

    def remove_bookmark(self, user: str, story: str) -> None:
        bookmarks = self.load_bookmarks(user)
        bookmarks = [b for b in bookmarks if b['story'] != story]
        self.save_bookmarks(user, bookmarks)

    def load_bookmarks(self, user: str) -> list[dict]:
        try:
            with open(self.bookmarks_file, 'r') as f:
                bookmarks_data = json.load(f)
                return [b for b in bookmarks_data if b['user'] == user]
        except FileNotFoundError:
            return []

    def save_bookmarks(self, user: str, bookmarks: list[dict]) -> None:
        try:
            with open(self.bookmarks_file, 'r') as f:
                all_bookmarks = json.load(f)
        except FileNotFoundError:
            all_bookmarks = []

        all_bookmarks = [b for b in all_bookmarks if b['user'] != user]
        all_bookmarks.extend(bookmarks)

        with open(self.bookmarks_file, 'w') as f:
            json.dump(all_bookmarks, f)