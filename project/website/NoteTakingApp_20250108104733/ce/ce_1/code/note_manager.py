class NoteManager:
    def __init__(self):
        pass

    def add_note(self, username: str, title: str, content: str) -> None:
        with open(f'notes_{username}.txt', 'a') as f:
            f.write(f"{title}|{content}\n")

    def edit_note(self, username: str, title: str, new_content: str) -> None:
        notes = self.get_all_notes(username)
        with open(f'notes_{username}.txt', 'w') as f:
            for note in notes:
                if note[0] == title:
                    f.write(f"{title}|{new_content}\n")
                else:
                    f.write(f"{note[0]}|{note[1]}\n")

    def delete_note(self, username: str, title: str) -> None:
        notes = self.get_all_notes(username)
        with open(f'notes_{username}.txt', 'w') as f:
            for note in notes:
                if note[0] != title:
                    f.write(f"{note[0]}|{note[1]}\n")

    def search_notes(self, username: str, query: str) -> list:
        notes = self.get_all_notes(username)
        return [note for note in notes if query.lower() in note[0].lower()]

    def get_all_notes(self, username: str) -> list:
        try:
            with open(f'notes_{username}.txt', 'r') as f:
                return [line.strip().split('|') for line in f]
        except FileNotFoundError:
            return []

    def get_note(self, username: str, title: str):
        notes = self.get_all_notes(username)
        for note in notes:
            if note[0] == title:
                return note
        return None