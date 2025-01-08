class NoteManager:
    def __init__(self):
        self.notes = {}

    def add_note(self, username, title, content):
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'title': title, 'content': content})
        self.save_notes(username)

    def edit_note(self, username, title, new_content):
        for note in self.notes.get(username, []):
            if note['title'] == title:
                note['content'] = new_content
        self.save_notes(username)

    def delete_note(self, username, title):
        self.notes[username] = [note for note in self.notes.get(username, []) if note['title'] != title]
        self.save_notes(username)

    def search_notes(self, username, query):
        return [note for note in self.notes.get(username, []) if query.lower() in note['title'].lower()]

    def get_all_notes(self, username):
        return self.notes.get(username, [])

    def get_note(self, username, title):
        for note in self.notes.get(username, []):
            if note['title'] == title:
                return note
        return None

    def save_notes(self, username):
        with open(f'notes_{username}.txt', 'w') as f:
            for note in self.notes.get(username, []):
                f.write(f"{note['title']}|{note['content']}\n")

    def load_notes(self, username):
        try:
            with open(f'notes_{username}.txt', 'r') as f:
                self.notes[username] = []
                for line in f:
                    title, content = line.strip().split('|')
                    self.notes[username].append({'title': title, 'content': content})
        except FileNotFoundError:
            self.notes[username] = []