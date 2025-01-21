class NoteManager:
    def __init__(self, notes_file: str):
        self.notes_file = notes_file
        self.load_notes()

    def load_notes(self):
        self.notes = []
        try:
            with open(self.notes_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split('|')
                    self.notes.append({'username': username, 'title': title, 'content': content})
        except FileNotFoundError:
            pass

    def add_note(self, username: str, title: str, content: str) -> None:
        self.notes.append({'username': username, 'title': title, 'content': content})
        with open(self.notes_file, 'a') as file:
            file.write(f"{username}|{title}|{content}\n")

    def edit_note(self, note_id: int, title: str, content: str) -> None:
        if 0 <= note_id < len(self.notes):
            self.notes[note_id]['title'] = title
            self.notes[note_id]['content'] = content
            self.save_notes()

    def delete_note(self, note_id: int) -> None:
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self.save_notes()

    def get_notes(self, username: str) -> list:
        return [note for note in self.notes if note['username'] == username]

    def search_notes(self, username: str, title: str) -> list:
        return [note for note in self.notes if note['username'] == username and title in note['title']]

    def save_notes(self):
        with open(self.notes_file, 'w') as file:
            for note in self.notes:
                file.write(f"{note['username']}|{note['title']}|{note['content']}\n")