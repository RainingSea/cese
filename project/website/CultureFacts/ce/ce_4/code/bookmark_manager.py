class BookmarkManager:
    def __init__(self, username: str):
        self.username = username
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self) -> list:
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    user, culture_name = line.strip().split('|')
                    if user == self.username:
                        bookmarks.append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks

    def add_bookmark(self, culture_name: str) -> bool:
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{self.username}|{culture_name}\n")
        return True

    def get_bookmarks(self) -> list:
        return self.bookmarks