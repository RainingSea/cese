import json
import os
from note import Note

class ArchiveManager:
    def __init__(self):
        self.notes = self.load_archived_notes()

    def archive_note(self, note: Note):
        self.notes.append(note)
        self.save_archived_notes()

    def restore_note(self, note_id: int) -> Note:
        for note in self.notes:
            if note.id == note_id:
                self.notes.remove(note)
                self.save_archived_notes()
                return note
        return None

    def search_notes(self, tag: str) -> list:
        return [note for note in self.notes if tag in note.tags]

    def load_archived_notes(self) -> list:
        if not os.path.exists('archived_notes.txt'):
            return []
        with open('archived_notes.txt', 'r') as file:
            data = file.readlines()
        notes = []
        for line in data:
            id, content, tags = line.strip().split('|')
            notes.append(Note(int(id), content, tags.split(',')))
        return notes

    def save_archived_notes(self):
        with open('archived_notes.txt', 'w') as file:
            for note in self.notes:
                file.write(f"{note.id}|{note.content}|{','.join(note.tags)}\n")