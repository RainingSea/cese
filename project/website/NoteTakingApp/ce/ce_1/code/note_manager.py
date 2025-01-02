class NoteManager:
    def __init__(self):
        self.username = None

    def add_note(self, title: str, content: str) -> None:
        if self.username is None:
            raise ValueError("Username must be set before adding notes.")
        
        note_id = self._get_next_note_id()
        note_entry = f"{note_id}:{title}:{content}\n"
        with open(f"notes_{self.username}.txt", "a") as file:
            file.write(note_entry)

    def _get_next_note_id(self) -> int:
        try:
            with open(f"notes_{self.username}.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    last_id = int(last_line.split(':')[0])
                    return last_id + 1
                return 1
        except FileNotFoundError:
            return 1

    def get_notes(self) -> list:
        notes = []
        try:
            with open(f"notes_{self.username}.txt", "r") as file:
                for line in file:
                    note_id, title, content = line.strip().split(':')
                    notes.append({'id': int(note_id), 'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return notes

    def get_note_by_id(self, note_id: int) -> dict:
        try:
            with open(f"notes_{self.username}.txt", "r") as file:
                for line in file:
                    current_id, title, content = line.strip().split(':')
                    if int(current_id) == note_id:
                        return {'id': int(current_id), 'title': title, 'content': content}
        except FileNotFoundError:
            pass
        return None

    def edit_note(self, note_id: int, title: str, content: str) -> None:
        notes = self.get_notes()
        with open(f"notes_{self.username}.txt", "w") as file:
            for note in notes:
                if note['id'] == note_id:
                    file.write(f"{note_id}:{title}:{content}\n")
                else:
                    file.write(f"{note['id']}:{note['title']}:{note['content']}\n")

    def delete_note(self, note_id: int) -> None:
        notes = self.get_notes()
        with open(f"notes_{self.username}.txt", "w") as file:
            for note in notes:
                if note['id'] != note_id:
                    file.write(f"{note['id']}:{note['title']}:{note['content']}\n")

    def search_notes(self, query: str) -> list:
        results = []
        try:
            with open(f"notes_{self.username}.txt", "r") as file:
                for line in file:
                    note_id, title, content = line.strip().split(':')
                    if query.lower() in title.lower():
                        results.append({'id': int(note_id), 'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return results