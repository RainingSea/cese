class BookmarkManager:
    def __init__(self, bookmarks_file: str):
        self.bookmarks_file = bookmarks_file
        self.load_bookmarks()

    def load_bookmarks(self):
        self.bookmarks = []
        try:
            with open(self.bookmarks_file, 'r') as file:
                self.bookmarks = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def add_bookmark(self, culture_name: str) -> bool:
        if culture_name in self.bookmarks:
            return False
        self.bookmarks.append(culture_name)
        with open(self.bookmarks_file, 'a') as file:
            file.write(f"{culture_name}\n")
        return True

    def get_bookmarks(self) -> list:
        return self.bookmarks

    def remove_bookmark(self, culture_name: str) -> bool:
        if culture_name in self.bookmarks:
            self.bookmarks.remove(culture_name)
            with open(self.bookmarks_file, 'w') as file:
                for bookmark in self.bookmarks:
                    file.write(f"{bookmark}\n")
            return True
        return False