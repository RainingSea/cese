from file_manager import FileManager

class Note:
    def __init__(self, username: str, title: str, content: str):
        self.username = username
        self.title = title
        self.content = content

    def create_note(self, username: str, title: str, content: str) -> bool:
        """Creates a new note for the user."""
        new_note = Note(username, title, content)
        file_manager = FileManager()
        file_manager.save_note_data(new_note)
        return True

    def edit_note(self, title: str, content: str) -> bool:
        """Edits an existing note."""
        notes = self.get_notes(self.username)
        for note in notes:
            if note.title == title:
                note.content = content
                self.save_all_notes(notes)
                return True
        return False

    def delete_note(self, title: str) -> bool:
        """Deletes a note by title."""
        notes = self.get_notes(self.username)
        notes = [note for note in notes if note.title != title]
        self.save_all_notes(notes)
        return True

    def get_notes(self, username: str) -> list:
        """Retrieves all notes for a user."""
        file_manager = FileManager()
        return file_manager.load_note_data(username)

    def save_all_notes(self, notes: list) -> None:
        """Saves all notes back to the file."""
        with open('notes.txt', 'w') as f:
            for note in notes:
                f.write(f"{note.username}:{note.title}:{note.content}\n")