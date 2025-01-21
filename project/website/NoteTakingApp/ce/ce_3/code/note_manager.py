from note import Note

class NoteManager:
    def load_notes(self):
        notes = []
        with open('notes.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                notes.append(Note(title, content))
        return notes

    def add_note(self, note: Note):
        note.save()

    def edit_note(self, title: str, new_content: str):
        notes = self.load_notes()
        for note in notes:
            if note.title == title:
                note.content = new_content
                self.save_all(notes)
                break

    def delete_note(self, title: str):
        notes = self.load_notes()
        notes = [note for note in notes if note.title != title]
        self.save_all(notes)

    def search_notes(self, query: str):
        notes = self.load_notes()
        return [note for note in notes if query.lower() in note.title.lower()]

    def save_all(self, notes):
        with open('notes.txt', 'w') as file:
            for note in notes:
                file.write(f"{note.title}|{note.content}\n")