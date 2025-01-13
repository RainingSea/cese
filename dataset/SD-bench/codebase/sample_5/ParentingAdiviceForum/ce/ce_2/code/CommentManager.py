import json
import os

class CommentManager:
    def __init__(self, data_file='comments.txt'):
        self.data_file = data_file
        self.load_comments()

    def load_comments(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.comments = [json.loads(line.strip()) for line in file.readlines()]
        else:
            self.comments = []

    def add_comment(self, thread_id: int, comment: str) -> bool:
        comment_data = {'thread_id': thread_id, 'comment': comment}
        self.comments.append(comment_data)
        self.save_comments()
        return True

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if comment['thread_id'] == thread_id]

    def save_comments(self):
        with open(self.data_file, 'w') as file:
            for comment in self.comments:
                file.write(json.dumps(comment) + '\n')