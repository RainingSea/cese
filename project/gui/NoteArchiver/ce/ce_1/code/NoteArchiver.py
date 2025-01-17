import json
from typing import List
from Note import Note

class NoteArchiver:
    def __init__(self):
        self.notes = []
        self.archived_notes = []
        self.load_notes()

    def archive_note(self, note: Note):
        self.archived_notes.append(note)
        self.notes.remove(note)
        self.save_archived_notes()

    def restore_note(self, note_id: str):
        for note in self.archived_notes:
            if note.id == note_id:
                self.notes.append(note)
                self.archived_notes.remove(note)
                self.save_archived_notes()
                break

    def add_tag(self, note_id: str, tag: str):
        for note in self.notes:
            if note.id == note_id:
                note.add_tag(tag)
                break

    def load_notes(self) -> List[Note]:
        try:
            with open('archived_notes.json', 'r') as file:
                data = json.load(file)
                for note_data in data:
                    note = Note(note_data['id'], note_data['content'])
                    note.tags = note_data['tags']
                    self.archived_notes.append(note)
        except FileNotFoundError:
            self.archived_notes = []

    def save_archived_notes(self):
        with open('archived_notes.json', 'w') as file:
            json_data = [{'id': note.id, 'content': note.content, 'tags': note.tags} for note in self.archived_notes]
            json.dump(json_data, file)