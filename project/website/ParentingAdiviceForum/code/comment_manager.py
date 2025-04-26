class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        comments = []
        try:
            with open('comments.txt', 'r') as file:
                for line in file:
                    thread_id, comment = line.strip().split('|')
                    comments.append({'thread_id': int(thread_id), 'comment': comment})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return comments

    def add_comment(self, thread_id: int, comment: str) -> bool:
        self.comments.append({'thread_id': thread_id, 'comment': comment})
        self.save_comments()
        return True

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if comment['thread_id'] == thread_id]

    def save_comments(self):
        with open('comments.txt', 'w') as file:
            for comment in self.comments:
                file.write(f"{comment['thread_id']}|{comment['comment']}\n")