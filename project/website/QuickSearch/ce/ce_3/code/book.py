class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self._title = title
        self._author = author
        self._summary = summary
        self._cover_image = cover_image

    def get_details(self) -> dict:
        return {
            'title': self._title,
            'author': self._author,
            'summary': self._summary,
            'cover_image': self._cover_image
        }