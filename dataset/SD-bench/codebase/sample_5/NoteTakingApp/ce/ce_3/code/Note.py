from FileManager import FileManager

class Note:
    def __init__(self, username: str):
        self.username = username
        self.file_manager = FileManager()

    def create_note(self, title: str, content: str) -> None:
        self.file_manager.save_note_data(self.username, title, content)

    def edit_note(self, old_title: str, new_title: str, new_content: str) -> None:
        notes = self.file_manager.load_note_data(self.username)
        updated_notes = []
        for note in notes:
            if note['title'] == old_title:
                updated_notes.append({'title': new_title, 'content': new_content})
            else:
                updated_notes.append(note)
        self._overwrite_notes(updated_notes)

    def delete_note(self, title: str) -> None:
        notes = self.file_manager.load_note_data(self.username)
        updated_notes = [note for note in notes if note['title'] != title]
        self._overwrite_notes(updated_notes)

    def _overwrite_notes(self, notes: list) -> None:
        with open(f'notes_{self.username}.txt', 'w') as f:
            for note in notes:
                f.write(f"{note['title']}|{note['content']}\n")