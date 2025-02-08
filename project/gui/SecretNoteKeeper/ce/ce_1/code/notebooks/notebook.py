import json
from typing import List
from .note import Note

class Notebook:
    def __init__(self, name: str):
        self.name = name
        self.notes = []

    def add_note(self, title: str, content: str):
        new_note = Note(title, content)
        self.notes.append(new_note)
        self.save_notes()

    def edit_note(self, note: Note, new_title: str, new_content: str):
        note.title = new_title
        note.content = new_content
        self.save_notes()

    def delete_note(self, note: Note):
        self.notes.remove(note)
        self.save_notes()

    def search_notes(self, query: str) -> List[Note]:
        return [note for note in self.notes if query.lower() in note.title.lower()]

    def sort_notes(self, criteria: str) -> List[Note]:
        if criteria == 'date':
            return sorted(self.notes, key=lambda note: note.timestamp)
        elif criteria == 'title':
            return sorted(self.notes, key=lambda note: note.title)
        return self.notes

    def save_notes(self):
        with open(f'notebooks/{self.name}.json', 'w') as f:
            json.dump([note.__dict__ for note in self.notes], f)

    def load_notes(self):
        try:
            with open(f'notebooks/{self.name}.json', 'r') as f:
                notes_data = json.load(f)
                self.notes = [Note(note['title'], note['content']) for note in notes_data]
        except FileNotFoundError:
            self.notes = []