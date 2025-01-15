class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'cover_image': self.cover_image
        }