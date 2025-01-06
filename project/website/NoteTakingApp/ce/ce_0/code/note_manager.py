class NoteManager:
    def __init__(self, notes_file: str):
        self.notes_file = notes_file
        self.notes = self.load_notes()

    def add_note(self, title: str, content: str) -> None:
        self.notes[title] = content
        with open(self.notes_file, 'a') as f:
            f.write(f"{title}|{content}\n")

    def edit_note(self, title: str, new_content: str) -> None:
        if title in self.notes:
            self.notes[title] = new_content
            self.save_notes()

    def delete_note(self, title: str) -> None:
        if title in self.notes:
            del self.notes[title]
            self.save_notes()

    def search_notes(self, query: str) -> list:
        return [title for title in self.notes if query.lower() in title.lower()]

    def load_notes(self) -> dict:
        notes = {}
        try:
            with open(self.notes_file, 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    notes[title] = content
        except FileNotFoundError:
            pass
        return notes

    def save_notes(self) -> None:
        with open(self.notes_file, 'w') as f:
            for title, content in self.notes.items():
                f.write(f"{title}|{content}\n")