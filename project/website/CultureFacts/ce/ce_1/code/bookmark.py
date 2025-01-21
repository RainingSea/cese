class Bookmark:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        bookmarks = {}
        with open('bookmarks.txt', 'r') as file:
            for line in file:
                user, culture_name = line.strip().split('|')
                if user not in bookmarks:
                    bookmarks[user] = []
                bookmarks[user].append(culture_name)
        return bookmarks

    def add_bookmark(self, user: str, culture_name: str) -> None:
        if user not in self.bookmarks:
            self.bookmarks[user] = []
        self.bookmarks[user].append(culture_name)
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{user}|{culture_name}\n")

    def get_bookmarks(self, user: str) -> list:
        return self.bookmarks.get(user, [])