import json

class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        try:
            with open('comments.txt', 'r') as file:
                return [json.loads(line) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def add_comment(self, thread_id: int, comment: str) -> bool:
        comment_data = {'thread_id': thread_id, 'comment': comment}
        self.comments.append(comment_data)
        self.save_comments()
        return True

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if comment['thread_id'] == thread_id]

    def save_comments(self):
        with open('comments.txt', 'w') as file:
            for comment in self.comments:
                file.write(json.dumps(comment) + '\n')