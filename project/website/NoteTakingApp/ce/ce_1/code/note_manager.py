import os
import json
from datetime import datetime

class NoteManager:
    def __init__(self, username: str):
        self.filename = f'notes_{username}.txt'
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    note_id, title, content, timestamp = line.strip().split('|')
                    self.notes[int(note_id)] = {
                        'title': title,
                        'content': content,
                        'timestamp': timestamp
                    }

    def add_note(self, title: str, content: str) -> bool:
        note_id = len(self.notes) + 1
        timestamp = datetime.now().isoformat()
        self.notes[note_id] = {
            'title': title,
            'content': content,
            'timestamp': timestamp
        }
        with open(self.filename, 'a') as file:
            file.write(f"{note_id}|{title}|{content}|{timestamp}\n")
        return True

    def get_notes(self) -> list:
        return self.notes.values()

    def delete_note(self, note_id: int) -> bool:
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
            return True
        return False

    def save_notes(self):
        with open(self.filename, 'w') as file:
            for note_id, note in self.notes.items():
                file.write(f"{note_id}|{note['title']}|{note['content']}|{note['timestamp']}\n")