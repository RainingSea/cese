import os
import json
from cryptography.fernet import Fernet

class NotebookManager:
    def __init__(self):
        self.notebooks = {}
        self.load_notebooks()
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def create_notebook(self, name: str) -> None:
        if name not in self.notebooks:
            self.notebooks[name] = []
            self.save_notebooks()

    def add_note(self, notebook_name: str, note: str) -> None:
        if notebook_name in self.notebooks:
            encrypted_note = self.cipher.encrypt(note.encode()).decode()
            self.notebooks[notebook_name].append(encrypted_note)
            self.save_notebooks()

    def edit_note(self, notebook_name: str, note_index: int, new_note: str) -> None:
        if notebook_name in self.notebooks and 0 <= note_index < len(self.notebooks[notebook_name]):
            encrypted_note = self.cipher.encrypt(new_note.encode()).decode()
            self.notebooks[notebook_name][note_index] = encrypted_note
            self.save_notebooks()

    def delete_note(self, notebook_name: str, note_index: int) -> None:
        if notebook_name in self.notebooks and 0 <= note_index < len(self.notebooks[notebook_name]):
            del self.notebooks[notebook_name][note_index]
            self.save_notebooks()

    def search_notes(self, notebook_name: str, query: str) -> list:
        if notebook_name in self.notebooks:
            return [note for note in self.notebooks[notebook_name] if query in self.cipher.decrypt(note.encode()).decode()]
        return []

    def load_notebooks(self) -> None:
        for filename in os.listdir('.'):
            if filename.endswith('.json'):
                with open(filename, 'r') as file:
                    self.notebooks[filename[:-5]] = json.load(file)

    def save_notebooks(self) -> None:
        for notebook_name, notes in self.notebooks.items():
            with open(f'{notebook_name}.json', 'w') as file:
                json.dump(notes, file)