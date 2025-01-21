class Bookmark:
    def __init__(self, username: str, culture_name: str = ''):
        self.username = username
        self.culture_name = culture_name

    def save(self):
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.username}|{self.culture_name}\n")

    @staticmethod
    def load_bookmarks(username: str):
        bookmarks = []
        try:
            with open('bookmarks.txt', 'r') as f:
                for line in f:
                    user, culture_name = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks