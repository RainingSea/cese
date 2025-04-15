class NoteManager:
    def __init__(self):
        pass

    def add_note(self, username: str, title: str, content: str) -> bool:
        """Add a new note for the specified user."""
        note_file = f"notes_{username}.txt"
        with open(note_file, 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def get_notes(self, username: str) -> list:
        """Retrieve all notes for the specified user."""
        note_file = f"notes_{username}.txt"
        try:
            with open(note_file, 'r') as file:
                return [line.strip().split('|') for line in file]
        except FileNotFoundError:
            return []

    def edit_note(self, username: str, title: str, new_content: str) -> bool:
        """Edit an existing note for the specified user."""
        notes = self.get_notes(username)
        note_file = f"notes_{username}.txt"
        with open(note_file, 'w') as file:
            for note_title, content in notes:
                if note_title == title:
                    file.write(f"{note_title}|{new_content}\n")
                else:
                    file.write(f"{note_title}|{content}\n")
        return True

    def delete_note(self, username: str, title: str) -> bool:
        """Delete a note for the specified user."""
        notes = self.get_notes(username)
        note_file = f"notes_{username}.txt"
        with open(note_file, 'w') as file:
            for note_title, content in notes:
                if note_title != title:
                    file.write(f"{note_title}|{content}\n")
        return True

    def search_notes(self, username: str, query: str) -> list:
        """Search for notes containing the query string."""
        notes = self.get_notes(username)
        return [note for note in notes if query.lower() in note[0].lower() or query.lower() in note[1].lower()]