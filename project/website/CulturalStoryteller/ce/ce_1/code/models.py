class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")


class Story:
    def __init__(self, title: str, content: str, cultural_origin: str):
        self.title = title
        self.content = content
        self.cultural_origin = cultural_origin

    def save(self):
        with open('stories.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.cultural_origin}\n")


class Bookmark:
    def __init__(self, username: str, story_title: str):
        self.username = username
        self.story_title = story_title

    def save(self):
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.username}|{self.story_title}\n")