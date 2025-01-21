class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def add_comment(self, comment: str):
        self.comments.append(Comment(comment))


class Comment:
    def __init__(self, content: str):
        self.content = content


class Advice:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class ContactInquiry:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message