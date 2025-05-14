import json
import time
import os

class NoteManager:
    def __init__(self):
        if not os.path.exists('user_notes'):
            os.makedirs('user_notes')

    def _get_notes_file(self, username):
        return f"user_notes/notes_{username}.json"

    def add_note(self, username, title, content):
        if not title or not content:
            return False
            
        notes = self._load_notes(username)
        note_id = str(int(time.time()))
        notes[note_id] = {
            'title': title,
            'content': content,
            'created_at': int(time.time())
        }
        self._save_notes(username, notes)
        return True

    def get_notes(self, username):
        return self._load_notes(username)

    def get_note(self, username, note_id):
        notes = self._load_notes(username)
        return notes.get(note_id)

    def update_note(self, username, note_id, new_title, content):
        notes = self._load_notes(username)
        if note_id not in notes:
            return False
            
        notes[note_id] = {
            'title': new_title,
            'content': content,
            'created_at': notes[note_id]['created_at']
        }
        self._save_notes(username, notes)
        return True

    def delete_note(self, username, note_id):
        notes = self._load_notes(username)
        if note_id not in notes:
            return False
            
        del notes[note_id]
        self._save_notes(username, notes)
        return True

    def _load_notes(self, username):
        notes_file = self._get_notes_file(username)
        try:
            with open(notes_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_notes(self, username, notes):
        notes_file = self._get_notes_file(username)
        with open(notes_file, 'w') as f:
            json.dump(notes, f, indent=4)