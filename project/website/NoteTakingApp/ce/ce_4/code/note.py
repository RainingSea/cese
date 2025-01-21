class Note:
    def __init__(self, username: str):
        self.username = username
        self.notes_file = f'notes_{username}.txt'

    def create_note(self, title: str, content: str) -> bool:
        with open(self.notes_file, 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def get_notes(self) -> list:
        notes = []
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as file:
                for line in file:
                    title, _ = line.strip().split('|')
                    notes.append(title)
        return notes

    def get_note_content(self, title: str) -> str:
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as file:
                for line in file:
                    note_title, content = line.strip().split('|')
                    if note_title == title:
                        return content
        return ""

    def search_notes(self, query: str) -> list:
        results = []
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    if query.lower() in title.lower():
                        results.append((title, content))
        return results