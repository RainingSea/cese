import json
from notebook import Notebook
from cryptography.fernet import Fernet

class SecretNoteKeeper:
    def __init__(self):
        self.notebooks = {}

    def load_notebooks(self) -> None:
        """Load notebooks from local text files."""
        try:
            with open('notebooks/notebook1.txt', 'r') as file:
                data = json.load(file)
                self.notebooks['notebook1'] = Notebook(data['notes'])
            with open('notebooks/notebook2.txt', 'r') as file:
                data = json.load(file)
                self.notebooks['notebook2'] = Notebook(data['notes'])
        except FileNotFoundError:
            print("No notebooks found. Starting fresh.")

    def save_notebooks(self) -> None:
        """Save notebooks to local text files."""
        for name, notebook in self.notebooks.items():
            with open(f'notebooks/{name}.txt', 'w') as file:
                json.dump({'notes': notebook.notes}, file)

    def add_note(self, notebook_name: str, note: str) -> None:
        """Add a note to a specified notebook."""
        if notebook_name in self.notebooks:
            self.notebooks[notebook_name].add(note)
        else:
            print(f"Notebook '{notebook_name}' does not exist.")

    def edit_note(self, notebook_name: str, note_id: int, new_note: str) -> None:
        """Edit a note in a specified notebook."""
        if notebook_name in self.notebooks:
            self.notebooks[notebook_name].edit(note_id, new_note)
        else:
            print(f"Notebook '{notebook_name}' does not exist.")

    def delete_note(self, notebook_name: str, note_id: int) -> None:
        """Delete a note from a specified notebook."""
        if notebook_name in self.notebooks:
            self.notebooks[notebook_name].delete(note_id)
        else:
            print(f"Notebook '{notebook_name}' does not exist.")

    def search_notes(self, notebook_name: str, query: str) -> list:
        """Search for notes in a specified notebook."""
        if notebook_name in self.notebooks:
            return self.notebooks[notebook_name].search(query)
        else:
            print(f"Notebook '{notebook_name}' does not exist.")
            return []

    def sort_notes(self, notebook_name: str, key: str) -> list:
        """Sort notes in a specified notebook."""
        if notebook_name in self.notebooks:
            return self.notebooks[notebook_name].sort(key)
        else:
            print(f"Notebook '{notebook_name}' does not exist.")
            return []