class Comment:
    def __init__(self, thread_id: int, content: str):
        self.thread_id = thread_id
        self.content = content

    def save(self):
        with open('comments.txt', 'a') as f:
            f.write(f"{self.thread_id}|{self.content}\n")

    @classmethod
    def load_all(cls, thread_id: int):
        comments = []
        try:
            with open('comments.txt', 'r') as f:
                for line in f:
                    tid, content = line.strip().split('|')
                    if int(tid) == thread_id:
                        comments.append(cls(thread_id, content))
        except FileNotFoundError:
            pass
        return comments