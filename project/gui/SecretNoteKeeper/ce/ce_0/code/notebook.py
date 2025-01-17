class Notebook:
    def __init__(self, notes=None):
        self.notes = notes if notes is not None else []

    def add(self, note: str) -> None:
        """Add a note to the notebook."""
        self.notes.append(note)

    def edit(self, note_id: int, new_note: str) -> None:
        """Edit a note in the notebook."""
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = new_note
        else:
            print("Note ID is out of range.")

    def delete(self, note_id: int) -> None:
        """Delete a note from the notebook."""
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
        else:
            print("Note ID is out of range.")

    def search(self, query: str) -> list:
        """Search for notes containing the query."""
        return [note for note in self.notes if query in note]

    def sort(self, key: str) -> list:
        """Sort notes based on the given key."""
        if key == "alphabetical":
            return sorted(self.notes)
        return self.notes