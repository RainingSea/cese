class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary
        }