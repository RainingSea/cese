from note import Note
from file_manager import FileManager

class NoteManager:
    def __init__(self):
        self.notes = []
        self.file_manager = FileManager()

    def load_notes(self, user: str) -> list[Note]:
        """Load notes for a specific user."""
        self.notes = []
        notes_data = self.file_manager.read_file('notes.txt')
        for line in notes_data:
            title, content, note_user = line.strip().split('|')
            if note_user == user:
                self.notes.append(Note(title, content, note_user))
        return self.notes

    def add_note(self, note: Note):
        """Add a new note."""
        note.save()

    def delete_note(self, title: str):
        """Delete a note by title."""
        self.notes = [note for note in self.notes if note.title != title]
        self.file_manager.write_file('notes.txt', [note.to_string() for note in self.notes])

    def edit_note(self, title: str, new_content: str):
        """Edit a note's content."""
        for note in self.notes:
            if note.title == title:
                note.content = new_content
                self.file_manager.write_file('notes.txt', [note.to_string() for note in self.notes])
                break

    def search_notes(self, title: str) -> list[Note]:
        """Search for notes by title."""
        return [note for note in self.notes if title.lower() in note.title.lower()]