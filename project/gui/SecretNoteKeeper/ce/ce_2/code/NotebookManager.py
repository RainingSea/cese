import os
import json
from Note import Note
from cryptography.fernet import Fernet

class NotebookManager:
    def __init__(self):
        self.notebooks = []

    def create_notebook(self, name: str) -> None:
        self.notebooks.append(name)
        with open(f'notebooks/{name}.txt', 'w') as f:
            f.write('')

    def open_notebook(self, name: str) -> dict:
        with open(f'notebooks/{name}.txt', 'r') as f:
            notes_data = f.readlines()
        notes = {}
        for line in notes_data:
            title, content = line.strip().split('|')
            notes[title] = content
        return notes

    def save_notebook(self, name: str) -> None:
        with open(f'notebooks/{name}.txt', 'w') as f:
            for note in self.notebooks:
                f.write(f"{note.title}|{note.encrypt_content()}\n")

    def add_note(self, title: str, content: str) -> None:
        note = Note(title, content)
        self.notebooks.append(note)

    def edit_note(self, title: str, new_content: str) -> None:
        for note in self.notebooks:
            if note.title == title:
                note.content = new_content
                break

    def delete_note(self, title: str) -> None:
        self.notebooks = [note for note in self.notebooks if note.title != title]

    def search_notes(self, query: str) -> list:
        return [note for note in self.notebooks if query in note.title]

    def sort_notes(self) -> list:
        return sorted(self.notebooks, key=lambda x: x.title)