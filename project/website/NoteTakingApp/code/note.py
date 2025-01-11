class Note:
    """Represents a note."""
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def edit(self, new_title: str, new_content: str) -> None:
        """Edits the note's title and content."""
        self.title = new_title
        self.content = new_content

    def delete(self) -> None:
        """Deletes the note (handled in NoteManager)."""
        pass


class NoteManager:
    """Manages notes for a specific user."""
    def __init__(self, username: str):
        self.username = username
        self.notes = []

    def load_notes(self) -> None:
        """Loads notes from a file."""
        try:
            with open(f'notes_{self.username}.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.notes.append(Note(title, content))
        except FileNotFoundError:
            pass

    def save_notes(self) -> None:
        """Saves notes to a file."""
        with open(f'notes_{self.username}.txt', 'w') as file:
            for note in self.notes:
                file.write(f"{note.title}|{note.content}\n")

    def add_note(self, title: str, content: str) -> None:
        """Adds a new note."""
        new_note = Note(title, content)
        self.notes.append(new_note)
        self.save_notes()

    def get_notes(self) -> list[Note]:
        """Returns the list of notes."""
        return self.notes

    def find_note_by_title(self, title: str) -> Note:
        """Finds a note by its title."""
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def delete_note(self, note: Note) -> None:
        """Deletes a note."""
        self.notes.remove(note)
        self.save_notes()