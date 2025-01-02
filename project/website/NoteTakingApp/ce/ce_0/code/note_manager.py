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