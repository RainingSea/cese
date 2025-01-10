import json
import os

class NoteManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_notes()

    def load_notes(self):
        """Loads notes from the JSON file."""
        self.notes = []
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r') as file:
            self.notes = json.load(file)

    def add_note(self, title: str, content: str, username: str) -> bool:
        """Adds a new note for the specified user."""
        note_id = len(self.notes)
        note = {"id": note_id, "title": title, "content": content, "username": username}
        self.notes.append(note)
        self.save_notes()
        return True

    def get_notes(self, username: str) -> list:
        """Retrieves notes for the specified user."""
        return [note for note in self.notes if note['username'] == username]

    def edit_note(self, note_id: int, title: str, content: str) -> bool:
        """Edits an existing note."""
        for note in self.notes:
            if note['id'] == note_id:
                note['title'] = title
                note['content'] = content
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id: int) -> bool:
        """Deletes a note by its ID."""
        self.notes = [note for note in self.notes if note['id'] != note_id]
        self.save_notes()
        return True

    def search_notes(self, title: str, username: str) -> list:
        """Searches for notes by title for the specified user."""
        return [note for note in self.notes if title.lower() in note['title'].lower() and note['username'] == username]

    def save_notes(self):
        """Saves notes to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.notes, file)