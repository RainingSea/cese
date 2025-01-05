class BlogPost:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def create_post(self, title: str, content: str, author: str) -> bool:
        # Creation logic already handled in main.py
        return True

    def edit_post(self, content: str) -> bool:
        self.content = content
        return True

    def delete_post(self, title: str) -> bool:
        # Deletion logic handled in main.py
        return True

    def view_post(self) -> str:
        return f"{self.title}: {self.content} by {self.author}"