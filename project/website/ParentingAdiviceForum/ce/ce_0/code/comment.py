class Comment:
    def __init__(self, thread_id: int, content: str, author: str):
        self.thread_id = thread_id
        self.content = content
        self.author = author

    def save(self):
        with open('comments.txt', 'a') as file:
            file.write(f"{self.thread_id}|{self.content}|{self.author}\n")