class Comment:
    def __init__(self, thread_id: int, content: str) -> None:
        self.thread_id = thread_id
        self.content = content

    def save(self) -> None:
        with open('comments.txt', 'a') as file:
            file.write(f"{self.thread_id}|{self.content}\n")