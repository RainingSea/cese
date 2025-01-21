class Bookmark:
    def __init__(self):
        self.username = ""
        self.story_title = ""

    def add_bookmark(self, username: str, story_title: str) -> bool:
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{username}|{story_title}\n")
        return True

    def get_bookmarks(self, username: str) -> list:
        bookmarks = []
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                stored_username, stored_story_title = line.strip().split('|')
                if stored_username == username:
                    bookmarks.append(stored_story_title)
        return bookmarks