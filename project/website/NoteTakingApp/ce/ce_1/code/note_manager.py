class NoteManager:
    def __init__(self, notes_file: str):
        self.notes_file = notes_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as file:
                for line in file:
                    title, content, username = line.strip().split('|')
                    if username not in self.notes:
                        self.notes[username] = []
                    self.notes[username].append({'title': title, 'content': content})

    def add_note(self, title: str, content: str, username: str) -> bool:
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'title': title, 'content': content})
        with open(self.notes_file, 'a') as file:
            file.write(f"{title}|{content}|{username}\n")
        return True

    def get_notes(self, username: str) -> list:
        return self.notes.get(username, [])

    def edit_note(self, title: str, new_content: str, username: str) -> bool:
        for note in self.notes.get(username, []):
            if note['title'] == title:
                note['content'] = new_content
                self.save_notes()
                return True
        return False

    def delete_note(self, title: str, username: str) -> bool:
        self.notes[username] = [note for note in self.notes.get(username, []) if note['title'] != title]
        self.save_notes()
        return True

    def search_notes(self, title: str, username: str) -> list:
        return [note for note in self.notes.get(username, []) if title in note['title']]

    def save_notes(self):
        with open(self.notes_file, 'w') as file:
            for username, notes in self.notes.items():
                for note in notes:
                    file.write(f"{note['title']}|{note['content']}|{username}\n")