class CultureManager:
    def __init__(self, cultures_file: str, bookmarks_file: str):
        self.cultures_file = cultures_file
        self.bookmarks_file = bookmarks_file
        self.cultures = self.load_cultures()

    def load_cultures(self) -> list:
        cultures = []
        try:
            with open(self.cultures_file, 'r') as f:
                for line in f:
                    cultures.append(line.strip())
        except FileNotFoundError:
            pass
        return cultures

    def get_culture_details(self, culture_name: str) -> dict:
        # For simplicity, returning a static detail for each culture
        return {"name": culture_name, "details": f"Details about {culture_name}"}

    def bookmark_culture(self, username: str, culture_name: str) -> bool:
        with open(self.bookmarks_file, 'a') as f:
            f.write(f"{username}|{culture_name}\n")
        return True

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open(self.bookmarks_file, 'r') as f:
                for line in f:
                    user, culture = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture)
        except FileNotFoundError:
            pass
        return bookmarks