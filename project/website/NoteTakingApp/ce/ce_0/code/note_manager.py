import os

class NoteManager:
    """Manages notes for users."""
    
    def __init__(self, filename: str):
        """Initializes NoteManager with a given filename."""
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self) -> list:
        """Loads notes from a file into a list."""
        notes = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    note_id, title, content, username = line.strip().split('|')
                    notes.append({
                        'id': int(note_id),
                        'title': title,
                        'content': content,
                        'username': username
                    })
        return notes

    def add_note(self, title: str, content: str, username: str) -> bool:
        """Adds a new note for the specified user."""
        note_id = len(self.notes) + 1
        self.notes.append({'id': note_id, 'title': title, 'content': content, 'username': username})
        with open(self.filename, 'a') as file:
            file.write(f"{note_id}|{title}|{content}|{username}\n")
        return True

    def get_notes(self, username: str) -> list:
        """Retrieves notes for a specific user."""
        return [note for note in self.notes if note['username'] == username]

    def get_note_details(self, note_id: int) -> dict:
        """Retrieves details of a specific note."""
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return {}

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
        """Deletes a specific note."""
        self.notes = [note for note in self.notes if note['id'] != note_id]
        self.save_notes()
        return True

    def search_notes(self, title: str, username: str) -> list:
        """Searches for notes by title for a specific user."""
        return [note for note in self.notes if title.lower() in note['title'].lower() and note['username'] == username]

    def save_notes(self):
        """Saves all notes back to the file."""
        with open(self.filename, 'w') as file:
            for note in self.notes:
                file.write(f"{note['id']}|{note['title']}|{note['content']}|{note['username']}\n")