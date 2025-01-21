class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self) -> list:
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    bookmarks.append(line.strip())
        except FileNotFoundError:
            pass
        return bookmarks

    def add_bookmark(self, article_id: str):
        self.bookmarks.append(article_id)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{article_id}\n")

    def remove_bookmark(self, article_id: str):
        self.bookmarks.remove(article_id)
        with open('bookmarks.txt', 'w') as file:
            for bookmark in self.bookmarks:
                file.write(f"{bookmark}\n")