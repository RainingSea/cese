import unittest
from book_manager import BookManager
from note_manager import NoteManager
from models import Book, Note

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.note_manager = NoteManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        self.book_manager.add_book("New Book", "New Author", "New Genre", "2023")
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertEqual(self.book_manager.books[-1].title, "New Book")

    def test_create_notes_for_each_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note("The Great Gatsby", "Chapter 2", "This is a new note for Chapter 2.")
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertEqual(self.note_manager.notes[-1].chapter, "Chapter 2")

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note("1984", "Chapter 2", "This is a text note for Chapter 2.")
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertEqual(self.note_manager.notes[-1].text, "This is a text note for Chapter 2.")

    def test_organize_notes_for_easy_access(self):
        # Functionalities 4: Organize Notes for Easy Access
        notes = self.note_manager.search_notes("Chapter 1")
        self.assertTrue(all(note.chapter == "Chapter 1" for note in notes))

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        self.fail("not implemented")  # No implementation for categorizing notes in the codebase

    def test_search_for_specific_books(self):
        # Functionalities 6: Search for Specific Books
        found_books = [book for book in self.book_manager.books if "1984" in book.title]
        self.assertTrue(any(book.title == "1984" for book in found_books))

    def test_search_for_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        notes = self.note_manager.search_notes("oppressive")
        self.assertTrue(any("oppressive" in note.text for note in notes))

        self.fail("not implemented")  # No implementation for searching notes by category in the codebase

if __name__ == '__main__':
    unittest.main()
