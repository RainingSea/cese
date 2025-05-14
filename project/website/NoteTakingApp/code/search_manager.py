class SearchManager:
    def __init__(self, note_manager):
        self.note_manager = note_manager

    def search_by_title(self, username, query):
        if not query:
            return []
            
        all_notes = self.note_manager.get_notes(username)
        results = []
        
        for note_id, note in all_notes.items():
            if query.lower() in note['title'].lower():
                results.append({
                    'id': note_id,
                    'title': note['title'],
                    'content': note['content'][:50] + '...' if len(note['content']) > 50 else note['content'],
                    'created_at': note['created_at']
                })
        
        return results