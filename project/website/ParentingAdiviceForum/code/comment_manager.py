import os

class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        if not os.path.exists('comments.txt'):
            return []
        with open('comments.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_comment(self, thread_id: int, comment: str) -> bool:
        self.comments.append([str(thread_id), comment])
        self.save_comments()
        return True

    def save_comments(self):
        with open('comments.txt', 'w') as file:
            for comment in self.comments:
                file.write('|'.join(comment) + '\n')

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if int(comment[0]) == thread_id]