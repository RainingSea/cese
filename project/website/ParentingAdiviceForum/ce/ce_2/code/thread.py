class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def save(self):
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{'|'.join(self.comments)}\n")

    @staticmethod
    def load(thread_id: int):
        with open('threads.txt', 'r') as file:
            lines = file.readlines()
            if thread_id < len(lines):
                title, content, *comments = lines[thread_id].strip().split('|')
                thread = Thread(title, content)
                thread.comments = comments
                return thread
        return None