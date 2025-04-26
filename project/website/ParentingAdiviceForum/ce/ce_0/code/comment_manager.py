class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        comments = {}
        with open('comments.txt', 'r') as file:
            for line in file:
                thread_id, comment = line.strip().split('|')
                if thread_id not in comments:
                    comments[thread_id] = []
                comments[thread_id].append(comment)
        return comments

    def add_comment(self, thread_id: int, comment: str) -> bool:
        if str(thread_id) not in self.comments:
            self.comments[str(thread_id)] = []
        self.comments[str(thread_id)].append(comment)
        with open('comments.txt', 'a') as file:
            file.write(f"{thread_id}|{comment}\n")
        return True