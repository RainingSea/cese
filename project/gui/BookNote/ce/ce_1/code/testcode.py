import unittest
import os
from main import BookManager, NoteManager, SearchEngine

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.note_manager = NoteManager()
        self.search_engine = SearchEngine()

    def test_add_book(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        self.book_manager.add_book("New Book", "New Author", "2023")
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertEqual(self.book_manager.books[-1].title, "New Book")
        self.assertEqual(self.book_manager.books[-1].author, "New Author")
        self.assertEqual(self.book_manager.books[-1].publication_date, "2023")

    def test_create_note_for_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note("Chapter 3", "This is a note for Chapter 3.")
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertEqual(self.note_manager.notes[-1].chapter, "Chapter 3")
        self.assertEqual(self.note_manager.notes[-1].content, "This is a note for Chapter 3.")

    def test_add_text_note(self):
        # Functionalities 3: Add Text Notes
        initial_count = len(self.note_manager.notes)
        self.note_manager.add_note("Chapter 4", "This is a note for Chapter 4.")
        self.assertEqual(len(self.note_manager.notes), initial_count + 1)
        self.assertEqual(self.note_manager.notes[-1].chapter, "Chapter 4")
        self.assertEqual(self.note_manager.notes[-1].content, "This is a note for Chapter 4.")

    def test_organize_notes(self):
        # Functionalities 4: Organize Notes for Easy Access
        self.note_manager.add_note("Chapter 5", "This is a note for Chapter 5.")
        self.assertEqual(len(self.note_manager.notes), 3)  # Assuming 2 notes were added previously
        self.assertIn("Chapter 5", [note.chapter for note in self.note_manager.notes])

    def test_search_books(self):
        # Functionalities 6: Search for Specific Books
        self.book_manager.add_book("Another Book", "Another Author", "2022")
        results = self.search_engine.search_books("Another", self.book_manager)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Another Book")

    def test_search_notes(self):
        # Functionalities 7: Search for Specific Notes
        self.note_manager.add_note("Chapter 6", "This is a note for Chapter 6.")
        results = self.search_engine.search_notes("Chapter 6", self.note_manager)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].content, "This is a note for Chapter 6.")

    def tearDown(self):
        # Clean up the files created during tests
        if os.path.exists('books.txt'):
            os.remove('books.txt')
        if os.path.exists('notes.txt'):
            os.remove('notes.txt')

if __name__ == '__main__':
    unittest.main()
