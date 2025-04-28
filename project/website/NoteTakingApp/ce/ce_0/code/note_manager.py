import os

class NoteManager:
    def __init__(self):
        self.notes = {}

    def add_note(self, username: str, title: str, content: str) -> None:
        note_id = len(self.load_notes(username))
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'id': note_id, 'title': title, 'content': content})
        self.save_notes(username)

    def edit_note(self, username: str, note_id: str, new_title: str, new_content: str) -> None:
        if username in self.notes:
            for note in self.notes[username]:
                if note['id'] == int(note_id):
                    note['title'] = new_title
                    note['content'] = new_content
                    self.save_notes(username)
                    break

    def delete_note(self, username: str, note_id: str) -> None:
        if username in self.notes:
            self.notes[username] = [note for note in self.notes[username] if note['id'] != int(note_id)]
            self.save_notes(username)

    def load_notes(self, username: str) -> list:
        if username not in self.notes:
            notes_file = f"{username}_notes.txt"
            if os.path.exists(notes_file):
                with open(notes_file, 'r') as file:
                    self.notes[username] = []
                    for line in file:
                        title, content = line.strip().split('|')
                        self.notes[username].append({'id': len(self.notes[username]), 'title': title, 'content': content})
            else:
                self.notes[username] = []
        return self.notes[username]

    def search_notes(self, username: str, title: str) -> list:
        if username in self.notes:
            return [note for note in self.notes[username] if title.lower() in note['title'].lower()]
        return []

    def save_notes(self, username: str) -> None:
        notes_file = f"{username}_notes.txt"
        with open(notes_file, 'w') as file:
            for note in self.notes[username]:
                file.write(f"{note['title']}|{note['content']}\n")