class Book:
    def __init__(self, title: str, author: str, genre: str, pub_date: str) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.pub_date = pub_date
        self.notes = {}

    def add_chapter_note(self, chapter: int, note: str) -> None:
        if chapter not in self.notes:
            self.notes[chapter] = []
        self.notes[chapter].append(note)

    def get_notes(self) -> dict:
        return self.notes