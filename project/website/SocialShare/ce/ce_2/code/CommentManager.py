import json

class Comment:
    def __init__(self, article_id: str, user: str, content: str):
        self.article_id = article_id
        self.user = user
        self.content = content

    def to_dict(self) -> dict:
        return {
            'article_id': self.article_id,
            'user': self.user,
            'content': self.content
        }

class CommentManager:
    def __init__(self):
        self.comments = []

    def load_comments(self) -> None:
        try:
            with open('comments.txt', 'r') as f:
                for line in f:
                    article_id, user, content = line.strip().split('|')
                    comment = Comment(article_id, user, content)
                    self.comments.append(comment)
        except FileNotFoundError:
            pass

    def save_comment(self, comment: Comment) -> None:
        self.comments.append(comment)
        with open('comments.txt', 'a') as f:
            f.write(f"{comment.article_id}|{comment.user}|{comment.content}\n")