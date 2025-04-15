class NoteManager:
    def __init__(self, note_file: str, metadata_file: str):
        self.note_file = note_file
        self.metadata_file = metadata_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        try:
            with open(self.note_file, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.notes[title] = content
        except FileNotFoundError:
            pass

    def add_note(self, title: str, content: str) -> None:
        with open(self.note_file, 'a') as file:
            file.write(f"{title}|{content}\n")
        self.notes[title] = content

    def get_notes(self) -> list:
        return list(self.notes.keys())

    def get_note(self, title: str) -> str:
        return self.notes.get(title, '')

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

    def save_notes(self) -> None:
        with open(self.note_file, 'w') as file:
            for title, content in self.notes.items():
                file.write(f"{title}|{content}\n")