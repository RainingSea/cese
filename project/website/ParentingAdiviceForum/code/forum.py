class Comment:
    def __init__(self, content: str):
        self.content = content

    def to_string(self) -> str:
        return self.content

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def to_string(self) -> str:
        return f"{self.title}|{self.content}"

class Forum:
    def __init__(self):
        self.threads = []

    def add_thread(self, thread: Thread):
        self.threads.append(thread)

    def get_thread(self, title: str) -> Thread:
        for thread in self.threads:
            if thread.title == title:
                return thread
        return None

    def list_threads(self) -> list:
        return self.threads