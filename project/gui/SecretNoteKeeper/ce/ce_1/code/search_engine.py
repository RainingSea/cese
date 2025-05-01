class SearchEngine:
    def search(self, query: str, notes: list) -> list:
        return [note for note in notes if query.lower() in note.title.lower() or query.lower() in note.decrypt_content().lower()]