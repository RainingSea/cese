import os

class NoteManager:
    def __init__(self):
        pass

    def get_notes(self, username: str) -> list:
        notes_file = f"{username}_notes.txt"
        if not os.path.exists(notes_file):
            return []
        with open(notes_file, 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_note(self, username: str, title: str, content: str) -> None:
        notes_file = f"{username}_notes.txt"
        with open(notes_file, 'a') as file:
            file.write(f"{title}|{content}\n")

    def get_note(self, username: str, title: str) -> dict:
        notes = self.get_notes(username)
        for note in notes:
            if note[0] == title:
                return {'title': note[0], 'content': note[1]}
        return None

    def search_notes(self, username: str, query: str) -> list:
        notes = self.get_notes(username)
        return [note for note in notes if query.lower() in note[0].lower() or query.lower() in note[1].lower()]