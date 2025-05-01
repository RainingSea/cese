import unittest
import os
from main import BookManager, NoteManager

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.note_manager = NoteManager()
        # Clear the books.txt and notes.txt before each test
        open("books.txt", "w").close()
        open("notes.txt", "w").close()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        self.book_manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "1925")
        books = self.book_manager.load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0], ("The Great Gatsby", "F. Scott Fitzgerald", "1925"))

    def test_create_notes_for_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        self.book_manager.add_book("1984", "George Orwell", "1949")
        self.note_manager.add_note("1984", "Chapter 1", "Introduction to the dystopian world.")
        notes = self.note_manager.load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], ("1984", "Chapter 1", "Introduction to the dystopian world."))

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        self.note_manager.add_note("The Great Gatsby", "Chapter 1", "Nick meets Gatsby.")
        notes = self.note_manager.load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], ("The Great Gatsby", "Chapter 1", "Nick meets Gatsby."))

    def test_organize_notes(self):
        # Functionalities 4: Organize Notes for Easy Access
        self.note_manager.add_note("To Kill a Mockingbird", "Chapter 1", "Scout's perspective on Boo Radley.")
        notes = self.note_manager.load_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], ("To Kill a Mockingbird", "Chapter 1", "Scout's perspective on Boo Radley."))

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        self.fail("Categorization of notes is not implemented.")

    def test_search_specific_books(self):
        # Functionalities 6: Search for Specific Books
        self.book_manager.add_book("1984", "George Orwell", "1949")
        books = self.book_manager.load_books()
        search_result = [book for book in books if "1984" in book[0]]
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], ("1984", "George Orwell", "1949"))

    def test_search_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        self.note_manager.add_note("1984", "Chapter 1", "Introduction to the dystopian world.")
        search_results = self.note_manager.search_notes("dystopian")
        self.assertEqual(len(search_results), 1)
        self.assertIn("1984 - Chapter 1: Introduction to the dystopian world.", search_results)

        # Search in a specific category (not implemented)
        self.fail("Searching notes by category is not implemented.")

if __name__ == '__main__':
    unittest.main()
