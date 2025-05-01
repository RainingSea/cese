from book_manager import BookManager
from note_manager import NoteManager

class SearchEngine:
    def search_books(self, query: str, book_manager: BookManager) -> list:
        return [book for book in book_manager.books if query.lower() in book.title.lower()]
    
    def search_notes_by_category(self, category: str, note_manager: NoteManager) -> list:
        return [(book_title, note) for book_title, note in note_manager.notes if note.category.lower() == category.lower()]