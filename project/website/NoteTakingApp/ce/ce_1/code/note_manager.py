import os

class NoteManager:
    def __init__(self):
        self.notes = self.load_notes()

    def load_notes(self):
        notes = {}
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as file:
                for line in file:
                    note_id, title, content, username = line.strip().split('|')
                    notes[int(note_id)] = {'title': title, 'content': content, 'username': username}
        return notes

    def add_note(self, title: str, content: str, username: str) -> bool:
        note_id = len(self.notes) + 1
        self.notes[note_id] = {'title': title, 'content': content, 'username': username}
        with open('notes.txt', 'a') as file:
            file.write(f"{note_id}|{title}|{content}|{username}\n")
        return True

    def edit_note(self, note_id: int, title: str, content: str) -> bool:
        if note_id in self.notes:
            self.notes[note_id]['title'] = title
            self.notes[note_id]['content'] = content
            self.save_notes()
            return True
        return False

    def delete_note(self, note_id: int) -> bool:
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_notes()
            return True
        return False

    def get_notes(self, username: str) -> list:
        return [note for note in self.notes.values() if note['username'] == username]

    def search_notes(self, query: str, username: str) -> list:
        return [note for note in self.notes.values() if query.lower() in note['title'].lower() and note['username'] == username]

    def save_notes(self):
        with open('notes.txt', 'w') as file:
            for note_id, note in self.notes.items():
                file.write(f"{note_id}|{note['title']}|{note['content']}|{note['username']}\n")