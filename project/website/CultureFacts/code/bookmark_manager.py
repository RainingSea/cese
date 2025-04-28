class BookmarkManager:
    def __init__(self):
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        bookmarks = {}
        try:
            with open('bookmarks.txt', 'r') as file:
                for line in file:
                    username, culture_name = line.strip().split('|')
                    if username not in bookmarks:
                        bookmarks[username] = []
                    bookmarks[username].append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks

    def add_bookmark(self, username: str, culture_name: str) -> bool:
        if username not in self.bookmarks:
            self.bookmarks[username] = []
        if culture_name not in self.bookmarks[username]:
            self.bookmarks[username].append(culture_name)
            with open('bookmarks.txt', 'a') as file:
                file.write(f"{username}|{culture_name}\n")
            return True
        return False

    def remove_bookmark(self, username: str, culture_name: str) -> bool:
        if username in self.bookmarks and culture_name in self.bookmarks[username]:
            self.bookmarks[username].remove(culture_name)
            self.save_bookmarks()
            return True
        return False

    def get_bookmarks(self, username: str):
        return self.bookmarks.get(username, [])

    def save_bookmarks(self):
        with open('bookmarks.txt', 'w') as file:
            for username, cultures in self.bookmarks.items():
                for culture in cultures:
                    file.write(f"{username}|{culture}\n")