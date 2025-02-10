import os

class NoteManager:
    def __init__(self):
        self.note_files = {}

    def get_note_file(self, username: str):
        if username not in self.note_files:
            self.note_files[username] = f'notes_{username}.txt'
            if not os.path.exists(self.note_files[username]):
                with open(self.note_files[username], 'w') as file:
                    pass
        return self.note_files[username]

    def add_note(self, username: str, title: str, content: str):
        note_file = self.get_note_file(username)
        with open(note_file, 'a') as file:
            file.write(f"{title}|{content}\n")

    def edit_note(self, username: str, note_id: int, title: str, content: str):
        note_file = self.get_note_file(username)
        notes = self.get_notes(username)
        notes[note_id] = {'title': title, 'content': content}
        self.save_notes(username, notes)

    def delete_note(self, username: str, note_id: int):
        note_file = self.get_note_file(username)
        notes = self.get_notes(username)
        notes.pop(note_id)
        self.save_notes(username, notes)

    def get_notes(self, username: str):
        note_file = self.get_note_file(username)
        notes = []
        with open(note_file, 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                notes.append({'title': title, 'content': content})
        return notes

    def search_notes(self, username: str, title: str):
        notes = self.get_notes(username)
        return [note for note in notes if title.lower() in note['title'].lower()]

    def save_notes(self, username: str, notes):
        note_file = self.get_note_file(username)
        with open(note_file, 'w') as file:
            for note in notes:
                file.write(f"{note['title']}|{note['content']}\n")