class NoteManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_notes()

    def load_notes(self):
        self.notes = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    title, content = line.strip().split('|', 1)
                    self.notes.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass

    def add_note(self, title: str, content: str) -> None:
        self.notes.append({'title': title, 'content': content})
        with open(self.filename, 'a') as f:
            f.write(f'{title}|{content}\n')

    def edit_note(self, title: str, new_content: str) -> None:
        for note in self.notes:
            if note['title'] == title:
                note['content'] = new_content
                self.save_notes()
                break

    def delete_note(self, title: str) -> None:
        self.notes = [note for note in self.notes if note['title'] != title]
        self.save_notes()

    def save_notes(self) -> None:
        with open(self.filename, 'w') as f:
            for note in self.notes:
                f.write(f"{note['title']}|{note['content']}\n")

    def get_notes(self) -> list:
        return self.notes

    def search_notes(self, query: str) -> list:
        return [note for note in self.notes if query.lower() in note['title'].lower()]