class BookmarkManager:
    def __init__(self, bookmarks_file: str):
        self.bookmarks_file = bookmarks_file

    def add_bookmark(self, username: str, culture_name: str) -> bool:
        with open(self.bookmarks_file, 'a') as f:
            f.write(f"{username}|{culture_name}\n")
        return True

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open(self.bookmarks_file, 'r') as f:
                for line in f:
                    user, culture_name = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks