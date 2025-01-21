class NoteManager:
    def __init__(self, note_file: str):
        self.note_file = note_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        try:
            with open(self.note_file, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|', 1)
                    self.notes[title] = content
        except FileNotFoundError:
            pass

    def add_note(self, username: str, title: str, content: str) -> None:
        self.notes[title] = content
        with open(f'notes_{username}.txt', 'a') as file:
            file.write(f"{title}|{content}\n")

    def get_notes(self, username: str) -> list:
        self.load_notes()
        return list(self.notes.items())

    def edit_note(self, username: str, title: str, new_content: str) -> None:
        if title in self.notes:
            self.notes[title] = new_content
            self.save_notes(username)

    def delete_note(self, username: str, title: str) -> None:
        if title in self.notes:
            del self.notes[title]
            self.save_notes(username)

    def search_notes(self, username: str, title: str) -> list:
        self.load_notes()
        return [note for note in self.notes.items() if title.lower() in note[0].lower()]

    def save_notes(self, username: str) -> None:
        with open(f'notes_{username}.txt', 'w') as file:
            for title, content in self.notes.items():
                file.write(f"{title}|{content}\n")