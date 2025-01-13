from comment import Comment

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def save(self) -> None:
        """Save the thread to the threads.txt file."""
        with open('threads.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    def add_comment(self, comment_content: str) -> None:
        """Add a comment to the thread."""
        self.comments.append(Comment(comment_content))

    def get_comments(self) -> list:
        """Get all comments for the thread."""
        return self.comments