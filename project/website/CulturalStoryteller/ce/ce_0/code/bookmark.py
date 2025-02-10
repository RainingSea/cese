class Bookmark:
    def __init__(self, user, story):
        self.user = user
        self.story = story

    def add_to_bookmarks(self):
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.user.username}|{self.story.title}\n")

    def load_bookmarks(self, user):
        bookmarks = []
        if os.path.exists('bookmarks.txt'):
            with open('bookmarks.txt', 'r') as f:
                for line in f:
                    username, story_title = line.strip().split('|')
                    if username == user.username:
                        bookmarks.append(story_title)
        return bookmarks