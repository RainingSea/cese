import time

class NoteManager:
    def __init__(self, note_file):
        self.note_file = note_file
        self.load_notes()

    def load_notes(self):
        self.notes = {}
        try:
            with open(self.note_file, 'r') as file:
                for line in file:
                    username, title, content, timestamp = line.strip().split('|')
                    if username not in self.notes:
                        self.notes[username] = []
                    self.notes[username].append({
                        'title': title,
                        'content': content,
                        'timestamp': timestamp
                    })
        except FileNotFoundError:
            open(self.note_file, 'w').close()  # Create the file if it doesn't exist

    def add_note(self, username: str, title: str, content: str) -> bool:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.note_file, 'a') as file:
            file.write(f"{username}|{title}|{content}|{timestamp}\n")
        if username not in self.notes:
            self.notes[username] = []
        self.notes[username].append({'title': title, 'content': content, 'timestamp': timestamp})
        return True

    def get_notes(self, username: str) -> list:
        return self.notes.get(username, [])

    def get_note_details(self, username: str, title: str) -> dict:
        for note in self.notes.get(username, []):
            if note['title'] == title:
                return note
        return {}

    def edit_note(self, username: str, title: str, new_content: str) -> bool:
        for note in self.notes.get(username, []):
            if note['title'] == title:
                note['content'] = new_content
                self.save_notes()
                return True
        return False

    def delete_note(self, username: str, title: str) -> bool:
        if username in self.notes:
            self.notes[username] = [note for note in self.notes[username] if note['title'] != title]
            self.save_notes()
            return True
        return False

    def search_notes(self, username: str, title: str) -> list:
        return [note for note in self.notes.get(username, []) if title.lower() in note['title'].lower()]

    def save_notes(self):
        with open(self.note_file, 'w') as file:
            for username, notes in self.notes.items():
                for note in notes:
                    file.write(f"{username}|{note['title']}|{note['content']}|{note['timestamp']}\n")