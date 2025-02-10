class Note:
    def __init__(self, note_file='notes.txt'):
        self.note_file = note_file

    def create_note(self, username: str, title: str, content: str) -> bool:
        with open(self.note_file, 'a') as f:
            f.write(f"{username},{title},{content}\n")
        return True

    def edit_note(self, title: str, content: str) -> bool:
        notes = self.load_notes()
        with open(self.note_file, 'w') as f:
            for note in notes:
                if note['title'] == title:
                    note['content'] = content
                f.write(f"{note['username']},{note['title']},{note['content']}\n")
        return True

    def delete_note(self, title: str) -> bool:
        notes = self.load_notes()
        with open(self.note_file, 'w') as f:
            for note in notes:
                if note['title'] != title:
                    f.write(f"{note['username']},{note['title']},{note['content']}\n")
        return True

    def search_notes(self, username: str, title: str) -> list:
        notes = self.load_notes()
        return [note for note in notes if note['username'] == username and title in note['title']]

    def load_notes(self):
        notes = []
        with open(self.note_file, 'r') as f:
            for line in f:
                username, title, content = line.strip().split(',')
                notes.append({'username': username, 'title': title, 'content': content})
        return notes