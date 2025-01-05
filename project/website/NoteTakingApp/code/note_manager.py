class NoteManager:
    def __init__(self, username: str):
        self.filename = f'notes_{username}.txt'
        self.username = username
        self.load_notes()

    def load_notes(self):
        self.notes = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    self.notes.append(line.strip())
        except FileNotFoundError:
            pass

    def add_note(self, title: str, content: str):
        timestamp = '2023-10-01 12:00:00'  # Placeholder for actual timestamp
        note_entry = f"{title}|{content}|{timestamp}"
        self.notes.append(note_entry)
        with open(self.filename, 'a') as file:
            file.write(note_entry + '\n')

    def edit_note(self, old_title: str, new_title: str, new_content: str):
        for i, note in enumerate(self.notes):
            if note.startswith(old_title):
                self.notes[i] = f"{new_title}|{new_content}|{note.split('|')[2]}"
                self.save_notes()
                return

    def delete_note(self, title: str):
        self.notes = [note for note in self.notes if not note.startswith(title)]
        self.save_notes()

    def search_notes(self, query: str):
        return [note for note in self.notes if query.lower() in note.lower()]

    def get_all_notes(self):
        return self.notes

    def save_notes(self):
        with open(self.filename, 'w') as file:
            for note in self.notes:
                file.write(note + '\n')