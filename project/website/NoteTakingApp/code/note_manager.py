import os
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.notes = {}

    def load_notes(self):
        # Load notes for each user
        for user in os.listdir('.'):
            if user.endswith('_notes.txt'):
                with open(user, 'r') as file:
                    self.notes[user[:-10]] = [line.strip() for line in file]

    def add_note(self, title: str, content: str, username: str) -> bool:
        notes_file = f"{username}_notes.txt"
        created_at = datetime.now().isoformat()
        modified_at = created_at
        note_entry = f"{title}|{content}|{username}|{created_at}|{modified_at}\n"
        with open(notes_file, 'a') as file:
            file.write(note_entry)
        return True

    def edit_note(self, title: str, content: str, username: str) -> bool:
        notes_file = f"{username}_notes.txt"
        notes = self.get_user_notes(username)
        updated_notes = []
        note_found = False
        for note in notes:
            note_title, note_content, note_username, created_at, modified_at = note.split('|')
            if note_title == title:
                modified_at = datetime.now().isoformat()
                updated_notes.append(f"{title}|{content}|{username}|{created_at}|{modified_at}")
                note_found = True
            else:
                updated_notes.append(note)
        if note_found:
            with open(notes_file, 'w') as file:
                file.writelines('\n'.join(updated_notes) + '\n')
        return note_found

    def delete_note(self, title: str, username: str) -> bool:
        notes_file = f"{username}_notes.txt"
        notes = self.get_user_notes(username)
        updated_notes = [note for note in notes if not note.startswith(title + '|')]
        if len(updated_notes) < len(notes):  # Check if a note was deleted
            with open(notes_file, 'w') as file:
                file.writelines('\n'.join(updated_notes) + '\n')
            return True
        return False

    def search_notes(self, query: str, username: str) -> list:
        notes = self.get_user_notes(username)
        return [note for note in notes if query.lower() in note.split('|')[0].lower()]

    def get_user_notes(self, username: str) -> list:
        notes_file = f"{username}_notes.txt"
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as file:
                return [line.strip() for line in file]
        return []