import os

class NoteManager:
    def __init__(self):
        self.notes = {}
        self.load_notes()

    def add_note(self, title: str, content: str, username: str) -> None:
        note_id = str(len(self.notes) + 1)
        self.notes[note_id] = {'title': title, 'content': content, 'username': username}
        self.save_notes()

    def edit_note(self, note_id: str, title: str, content: str) -> None:
        if note_id in self.notes:
            self.notes[note_id]['title'] = title
            self.notes[note_id]['content'] = content
            self.save_notes()

    def delete_note(self, note_id: str) -> None:
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()

    def get_notes(self, username: str) -> list:
        return [note for note in self.notes.values() if note['username'] == username]

    def search_notes(self, title: str, username: str) -> list:
        return [note for note in self.notes.values() if note['username'] == username and title.lower() in note['title'].lower()]

    def load_notes(self) -> None:
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as file:
                for line in file:
                    note_id, title, content, username = line.strip().split('|')
                    self.notes[note_id] = {'title': title, 'content': content, 'username': username}

    def save_notes(self) -> None:
        with open('notes.txt', 'w') as file:
            for note_id, note in self.notes.items():
                file.write(f"{note_id}|{note['title']}|{note['content']}|{note['username']}\n")