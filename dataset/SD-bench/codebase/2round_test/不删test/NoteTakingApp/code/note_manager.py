import os

class NoteManager:
    def __init__(self, notes_file):
        self.notes_file = notes_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        if not os.path.exists(self.notes_file):
            open(self.notes_file, 'w').close()  # Create file if it doesn't exist
        with open(self.notes_file, 'r') as file:
            for line in file:
                username, title, content = line.strip().split('|')
                if username not in self.notes:
                    self.notes[username] = []
                self.notes[username].append((title, content))

    def add_note(self, username: str, title: str, content: str) -> None:
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append((title, content))
        with open(self.notes_file, 'a') as file:
            file.write(f"{username}|{title}|{content}\n")

    def get_notes(self, username: str) -> list:
        return self.notes.get(username, [])

    def get_note_by_title(self, username: str, title: str) -> tuple:
        for note_title, content in self.notes.get(username, []):
            if note_title == title:
                return (note_title, content)
        return None

    def edit_note(self, username: str, title: str, new_content: str) -> None:
        for index, (note_title, _) in enumerate(self.notes.get(username, [])):
            if note_title == title:
                self.notes[username][index] = (title, new_content)
                self.save_notes()
                break

    def delete_note(self, username: str, title: str) -> None:
        self.notes[username] = [note for note in self.notes.get(username, []) if note[0] != title]
        self.save_notes()

    def search_notes(self, username: str, title: str) -> list:
        return [note for note in self.notes.get(username, []) if title in note[0]]

    def save_notes(self) -> None:
        with open(self.notes_file, 'w') as file:
            for username, notes in self.notes.items():
                for title, content in notes:
                    file.write(f"{username}|{title}|{content}\n")