class Thread:
    def __init__(self, title: str, content: str, comments: list = None):
        self.title = title
        self.content = content
        self.comments = comments if comments is not None else []

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def save(self):
        comments_str = ';'.join(self.comments)
        with open('threads.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{comments_str}\n")