class NoteManager:
    def __init__(self):
        pass

    def add_note(self, username: str, title: str, content: str) -> None:
        with open(f'notes_{username}.txt', 'a') as file:
            file.write(f"{title}|{content}\n")

    def edit_note(self, username: str, title: str, new_content: str) -> None:
        notes = self.get_all_notes(username)
        with open(f'notes_{username}.txt', 'w') as file:
            for note in notes:
                if note['title'] == title:
                    file.write(f"{title}|{new_content}\n")
                else:
                    file.write(f"{note['title']}|{note['content']}\n")

    def delete_note(self, username: str, title: str) -> None:
        notes = self.get_all_notes(username)
        with open(f'notes_{username}.txt', 'w') as file:
            for note in notes:
                if note['title'] != title:
                    file.write(f"{note['title']}|{note['content']}\n")

    def search_notes(self, username: str, query: str) -> list:
        notes = self.get_all_notes(username)
        return [note for note in notes if query.lower() in note['title'].lower()]

    def get_all_notes(self, username: str) -> list:
        notes = []
        try:
            with open(f'notes_{username}.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    notes.append({'title': title, 'content': content})
        except FileNotFoundError:
            pass
        return notes

    def get_note(self, username: str, title: str) -> dict:
        notes = self.get_all_notes(username)
        for note in notes:
            if note['title'] == title:
                return note
        return None