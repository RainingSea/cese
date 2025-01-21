class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def to_string(self) -> str:
        return f"{self.username}|{self.content}"