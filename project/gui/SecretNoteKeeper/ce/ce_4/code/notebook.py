import json
from typing import List
from note import Note

class Notebook:
    def __init__(self, name: str):
        self.name = name
        self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note)

    def edit_note(self, title: str, new_content: str):
        for note in self.notes:
            if note.title == title:
                note.content = new_content
                break

    def delete_note(self, title: str):
        self.notes = [note for note in self.notes if note.title != title]

    def search_notes(self, query: str) -> List[Note]:
        return [note for note in self.notes if query in note.title or query in note.content]

    def sort_notes(self, by: str) -> List[Note]:
        if by == 'date':
            return sorted(self.notes, key=lambda note: note.created_at)
        elif by == 'title':
            return sorted(self.notes, key=lambda note: note.title)
        return self.notes

    def save_to_file(self):
        with open(f"{self.name}.json", "w") as file:
            json.dump([note.__dict__ for note in self.notes], file)

    def load_from_file(self):
        try:
            with open(f"{self.name}.json", "r") as file:
                notes_data = json.load(file)
                self.notes = [Note(note['title'], note['content']) for note in notes_data]
        except FileNotFoundError:
            self.notes = []