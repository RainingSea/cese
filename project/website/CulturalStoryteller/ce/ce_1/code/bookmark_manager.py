from models import Bookmark

class BookmarkManager:
    def add_bookmark(self, username: str, story_title: str) -> None:
        new_bookmark = Bookmark(username, story_title)
        new_bookmark.save()

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as f:
                for line in f:
                    user, story_title = line.strip().split('|')
                    if user == username:
                        bookmarks.append(story_title)
        except FileNotFoundError:
            pass
        return bookmarks