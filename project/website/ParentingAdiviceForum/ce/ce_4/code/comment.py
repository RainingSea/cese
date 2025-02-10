class Comment:
    def __init__(self, thread_id: int, content: str):
        self.thread_id = thread_id
        self.content = content

    def save(self) -> None:
        with open('comments.txt', 'a') as f:
            f.write(f"{self.thread_id}|{self.content}\n")

    @staticmethod
    def load_all(thread_id: int) -> list:
        comments = []
        try:
            with open('comments.txt', 'r') as f:
                for line in f:
                    tid, content = line.strip().split('|')
                    if int(tid) == thread_id:
                        comments.append(Comment(thread_id, content))
        except FileNotFoundError:
            pass
        return comments