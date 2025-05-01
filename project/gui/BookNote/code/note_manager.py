class Note:
    def __init__(self, chapter: str, content: str, category: str):
        self.chapter = chapter
        self.content = content
        self.category = category

class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def add_note(self, book_title: str, chapter: str, content: str, category: str):
        new_note = Note(chapter, content, category)
        self.notes.append((book_title, new_note))
        self.save_notes()

    def load_notes(self) -> None:
        try:
            with open("notes.txt", "r") as file:
                for line in file:
                    book_title, chapter, content, category = line.strip().split("|")
                    self.notes.append((book_title, Note(chapter, content, category)))
        except FileNotFoundError:
            pass

    def save_notes(self) -> None:
        with open("notes.txt", "w") as file:
            for book_title, note in self.notes:
                file.write(f"{book_title}|{note.chapter}|{note.content}|{note.category}\n")