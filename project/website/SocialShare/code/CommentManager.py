import json
from typing import List

class Comment:
    def __init__(self, article_id: str, author: str, content: str):
        self.article_id = article_id
        self.author = author
        self.content = content

    def to_dict(self) -> dict:
        return {
            "article_id": self.article_id,
            "author": self.author,
            "content": self.content
        }

class CommentManager:
    def __init__(self, comments_file: str):
        self.comments_file = comments_file
        self.comments: List[Comment] = []
        self.load_comments()

    def load_comments(self) -> None:
        try:
            with open(self.comments_file, 'r') as f:
                comments_data = json.load(f)
                self.comments = [Comment(**comment) for comment in comments_data]
        except FileNotFoundError:
            self.comments = []

    def save_comments(self) -> None:
        with open(self.comments_file, 'w') as f:
            json.dump([comment.to_dict() for comment in self.comments], f)

    def add_comment(self, article_id: str, author: str, content: str) -> None:
        new_comment = Comment(article_id, author, content)
        self.comments.append(new_comment)
        self.save_comments()

    def get_comments(self, article_id: str) -> List[Comment]:
        return [comment for comment in self.comments if comment.article_id == article_id]