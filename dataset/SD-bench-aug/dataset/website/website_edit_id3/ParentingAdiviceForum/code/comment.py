class Comment:
    def __init__(self, thread_id: int, content: str):
        self.thread_id = thread_id
        self.content = content

    def save(self):
        with open('comments.txt', 'a') as file:
            file.write(f"{self.thread_id}|{self.content}\n")

    @staticmethod
    def load_all(thread_id: int):
        comments = []
        with open('comments.txt', 'r') as file:
            for line in file:
                tid, content = line.strip().split('|')
                if int(tid) == thread_id:
                    comments.append(Comment(int(tid), content))
        return comments