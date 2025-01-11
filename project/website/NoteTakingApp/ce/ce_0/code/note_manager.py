import os
from datetime import datetime

class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class NoteManager:
    def __init__(self):
        self.notes_directory = 'notes_'

    def load_notes(self, username: str) -> list:
        notes_file = f"{self.notes_directory}{username}.txt"
        if not os.path.exists(notes_file):
            return []
        with open(notes_file, 'r') as f:
            notes = []
            for line in f:
                title, content, timestamp = line.strip().split('|')
                notes.append(Note(title, content))
            return notes

    def save_notes(self, username: str, title: str, content: str) -> None:
        notes_file = f"{self.notes_directory}{username}.txt"
        with open(notes_file, 'a') as f:
            f.write(f"{title}|{content}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def search_notes(self, username: str, query: str) -> list:
        notes = self.load_notes(username)
        return [note for note in notes if query.lower() in note.title.lower()]

    def get_note_by_id(self, username: str, note_id: int):
        notes = self.load_notes(username)
        if 0 <= note_id < len(notes):
            return notes[note_id]
        return None