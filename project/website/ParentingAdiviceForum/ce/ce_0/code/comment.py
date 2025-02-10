class Comment:
    def __init__(self, thread_id: str, content: str):
        self.thread_id = thread_id
        self.content = content

    def save(self):
        with open('comments.txt', 'a') as file:
            file.write(f"{self.thread_id}|{self.content}\n")