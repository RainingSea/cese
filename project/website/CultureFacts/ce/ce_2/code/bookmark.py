class Bookmark:
    def __init__(self, username: str, culture_name: str):
        self.username = username
        self.culture_name = culture_name

    def save(self):
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{self.username}|{self.culture_name}\n")

    @staticmethod
    def load_all(username: str) -> list:
        bookmarks = []
        with open('bookmarks.txt', 'r') as file:
            for line in file:
                user, culture_name = line.strip().split('|')
                if user == username:
                    bookmarks.append(Bookmark(user, culture_name))
        return bookmarks