class NoteManager:
    def __init__(self, username: str):
        self.filename = f'notes_{username}.txt'
        self.load_notes()

    def load_notes(self):
        self.notes = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    self.notes.append(line.strip())
        except FileNotFoundError:
            pass

    def add_note(self, title: str, content: str) -> None:
        timestamp = '2023-10-01'  # Placeholder for timestamp
        note = f"{title}|{content}|{timestamp}"
        self.notes.append(note)
        with open(self.filename, 'a') as file:
            file.write(f"{note}\n")

    def edit_note(self, old_title: str, new_title: str, new_content: str) -> None:
        for i, note in enumerate(self.notes):
            if note.split('|')[0] == old_title:
                self.notes[i] = f"{new_title}|{new_content}|{note.split('|')[2]}"
                self.save_notes()
                break

    def delete_note(self, title: str) -> None:
        self.notes = [note for note in self.notes if note.split('|')[0] != title]
        self.save_notes()

    def search_notes(self, query: str) -> list:
        return [note for note in self.notes if query.lower() in note.split('|')[0].lower()]

    def get_all_notes(self) -> list:
        return self.notes

    def save_notes(self):
        with open(self.filename, 'w') as file:
            for note in self.notes:
                file.write(f"{note}\n")