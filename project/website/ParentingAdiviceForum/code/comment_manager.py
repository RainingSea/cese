class CommentManager:
    def __init__(self):
        self.comments = self.load_comments()

    def load_comments(self):
        comments = []
        try:
            with open('comments.txt', 'r') as file:
                for line in file:
                    thread_id, content, username = line.strip().split('|')
                    comments.append({'thread_id': int(thread_id), 'content': content, 'username': username})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return comments

    def add_comment(self, thread_id: int, content: str, username: str) -> bool:
        self.comments.append({'thread_id': thread_id, 'content': content, 'username': username})
        self.save_comments()
        return True

    def save_comments(self):
        with open('comments.txt', 'w') as file:
            for comment in self.comments:
                file.write(f"{comment['thread_id']}|{comment['content']}|{comment['username']}\n")

    def get_comments(self, thread_id: int) -> list:
        return [comment for comment in self.comments if comment['thread_id'] == thread_id]