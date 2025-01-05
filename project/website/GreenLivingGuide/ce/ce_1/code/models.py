class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        pass  # Saving logic will be handled in DataManager

class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        pass  # Saving logic will be handled in DataManager

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        pass  # Saving logic will be handled in DataManager

class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        pass  # Saving logic will be handled in DataManager