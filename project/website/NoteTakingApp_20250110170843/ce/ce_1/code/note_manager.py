class NoteManager:
    def __init__(self):
        pass

    def add_note(self, username: str, title: str, content: str) -> bool:
        notes_file = f'{username}_notes.txt'
        note_id = self.get_next_note_id(notes_file)
        with open(notes_file, 'a') as file:
            file.write(f'{note_id}|{title}|{content}\n')
        return True

    def get_next_note_id(self, notes_file: str) -> int:
        try:
            with open(notes_file, 'r') as file:
                return sum(1 for _ in file)
        except FileNotFoundError:
            return 0

    def get_note_by_id(self, username: str, note_id: int):
        notes_file = f'{username}_notes.txt'
        try:
            with open(notes_file, 'r') as file:
                for line in file:
                    note = line.strip().split('|')
                    if int(note[0]) == note_id:
                        return note
        except FileNotFoundError:
            return None

    def search_notes(self, username: str, query: str) -> list:
        notes_file = f'{username}_notes.txt'
        results = []
        try:
            with open(notes_file, 'r') as file:
                for line in file:
                    note = line.strip().split('|')
                    if query.lower() in note[1].lower() or query.lower() in note[2].lower():
                        results.append(note)
        except FileNotFoundError:
            pass
        return results