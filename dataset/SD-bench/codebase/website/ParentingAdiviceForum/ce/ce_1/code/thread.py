class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    def add_comment(self, comment: str):
        self.comments.append(Comment(comment))
        with open('comments.txt', 'a') as file:
            file.write(f"{comment}\n")