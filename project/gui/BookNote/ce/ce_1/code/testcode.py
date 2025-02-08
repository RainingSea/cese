import unittest
from main import BookManager, NoteManager, Book, Note

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        # Setup for BookManager and NoteManager
        self.book_manager = BookManager()
        self.note_manager = NoteManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        new_book = Book("New Book", "New Author", "New Genre", "2023")
        self.book_manager.add_book(new_book)
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertIn(new_book, self.book_manager.books)

    def test_create_notes_for_each_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        new_note = Note("The Great Gatsby", "Chapter 4", "This is a new note for Chapter 4.")
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note(new_note)
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertIn(new_note, self.note_manager.notes)

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        new_note = Note("1984", "Chapter 5", "This is a text note for Chapter 5.")
        self.note_manager.add_note(new_note)
        self.assertIn(new_note, self.note_manager.notes)

    def test_organize_notes_for_easy_access(self):
        # Functionalities 4: Organize Notes for Easy Access
        notes_for_gatsby = [note for note in self.note_manager.notes if note.book_title == "The Great Gatsby"]
        self.assertTrue(all(note.book_title == "The Great Gatsby" for note in notes_for_gatsby))

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        # This functionality is not implemented in the codebase
        self.fail("Categorize Notes functionality not implemented")

    def test_search_for_specific_books(self):
        # Functionalities 6: Search for Specific Books
        search_results = self.book_manager.search_books("1984")
        self.assertTrue(any(book.title == "1984" for book in search_results))

    def test_search_for_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        search_results = self.note_manager.search_notes("first day of school")
        self.assertTrue(any("first day of school" in note.note_text for note in search_results))

        # Search for a note in a specific category is not implemented
        self.fail("Search for a note in a specific category functionality not implemented")

if __name__ == '__main__':
    unittest.main()
