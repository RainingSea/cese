import os

class NoteManager:
    def __init__(self):
        pass

    def get_notes(self, username: str) -> list:
        notes_file = f'notes_{username}.txt'
        if not os.path.exists(notes_file):
            return []
        with open(notes_file, 'r') as file:
            return [line.strip().split('|') for line in file]

    def add_note(self, username: str, title: str, content: str) -> None:
        notes_file = f'notes_{username}.txt'
        with open(notes_file, 'a') as file:
            file.write(f"{title}|{content}\n")

    def edit_note(self, username: str, old_title: str, new_title: str, new_content: str) -> None:
        notes_file = f'notes_{username}.txt'
        notes = self.get_notes(username)
        with open(notes_file, 'w') as file:
            for title, content in notes:
                if title == old_title:
                    file.write(f"{new_title}|{new_content}\n")
                else:
                    file.write(f"{title}|{content}\n")

    def delete_note(self, username: str, title: str) -> None:
        notes_file = f'notes_{username}.txt'
        notes = self.get_notes(username)
        with open(notes_file, 'w') as file:
            for note_title, content in notes:
                if note_title != title:
                    file.write(f"{note_title}|{content}\n")

    def search_notes(self, username: str, title: str) -> list:
        notes = self.get_notes(username)
        return [note for note in notes if title.lower() in note[0].lower()]

    def get_note(self, username: str, title: str):
        notes = self.get_notes(username)
        for note_title, content in notes:
            if note_title == title:
                return (note_title, content)
        return None