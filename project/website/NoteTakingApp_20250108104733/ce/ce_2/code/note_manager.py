import os

class NoteManager:
    def __init__(self):
        pass

    def _get_note_file(self, username: str) -> str:
        return f'notes_{username}.txt'

    def add_note(self, username: str, title: str, content: str) -> None:
        note_file = self._get_note_file(username)
        with open(note_file, 'a') as file:
            file.write(f"{title}|{content}\n")

    def edit_note(self, username: str, title: str, new_content: str) -> None:
        note_file = self._get_note_file(username)
        notes = self.get_all_notes(username)
        with open(note_file, 'w') as file:
            for note_title, note_content in notes:
                if note_title == title:
                    file.write(f"{note_title}|{new_content}\n")
                else:
                    file.write(f"{note_title}|{note_content}\n")

    def delete_note(self, username: str, title: str) -> None:
        note_file = self._get_note_file(username)
        notes = self.get_all_notes(username)
        with open(note_file, 'w') as file:
            for note_title, note_content in notes:
                if note_title != title:
                    file.write(f"{note_title}|{note_content}\n")

    def search_notes(self, username: str, query: str) -> list:
        notes = self.get_all_notes(username)
        return [note for note in notes if query.lower() in note[0].lower()]

    def get_all_notes(self, username: str) -> list:
        note_file = self._get_note_file(username)
        if not os.path.exists(note_file):
            return []
        with open(note_file, 'r') as file:
            return [line.strip().split('|') for line in file]

    def get_note(self, username: str, title: str):
        notes = self.get_all_notes(username)
        for note_title, note_content in notes:
            if note_title == title:
                return (note_title, note_content)
        return None