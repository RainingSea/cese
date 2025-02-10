class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }


class Tip:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content
        }


class Resource:
    def __init__(self, title: str, link: str) -> None:
        self.title = title
        self.link = link

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link
        }


class ForumPost:
    def __init__(self, username: str, content: str) -> None:
        self.username = username
        self.content = content

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "content": self.content
        }