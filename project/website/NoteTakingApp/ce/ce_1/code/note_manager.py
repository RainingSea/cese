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
        timestamp = '2023-10-01 12:00'  # Placeholder for actual timestamp
        self.notes.append(f"{title}|{content}|{timestamp}")
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{content}|{timestamp}\n")

    def edit_note(self, old_title: str, new_title: str, new_content: str) -> None:
        for index, note in enumerate(self.notes):
            if note.split('|')[0] == old_title:
                self.notes[index] = f"{new_title}|{new_content}|timestamp"
                self.save_notes()
                break

    def delete_note(self, title: str) -> None:
        self.notes = [note for note in self.notes if note.split('|')[0] != title]
        self.save_notes()

    def search_notes(self, query: str) -> list:
        return [note for note in self.notes if query in note.split('|')[0]]

    def get_all_notes(self) -> list:
        return self.notes

    def save_notes(self) -> None:
        with open(self.filename, 'w') as file:
            for note in self.notes:
                file.write(f"{note}\n")