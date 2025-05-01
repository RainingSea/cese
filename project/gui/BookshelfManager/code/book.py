class Book:
    def __init__(self, title: str, author: str, genre: str, year: int, notes: list = None, rating: float = None, shelf: str = None) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = year
        self.notes = notes if notes is not None else []
        self.rating = rating
        self.shelf = shelf

    def add_note(self, note: str) -> None:
        """Adds a note to the book's notes."""
        self.notes.append(note)

    def edit_note(self, note_index: int, new_note: str) -> None:
        """Edits a note at a specific index."""
        if 0 <= note_index < len(self.notes):
            self.notes[note_index] = new_note

    def delete_note(self, note_index: int) -> None:
        """Deletes a note at a specific index."""
        if 0 <= note_index < len(self.notes):
            del self.notes[note_index]