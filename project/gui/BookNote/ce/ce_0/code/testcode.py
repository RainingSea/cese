import unittest
from books.BookManager import BookManager

class TestBookNoteApp(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        self.assertIn("Test Book", self.book_manager.books)
        book = self.book_manager.books["Test Book"]
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Author Name")
        self.assertEqual(book.genre, "Fiction")
        self.assertEqual(book.pub_date, "2023-01-01")

    def test_create_notes_for_each_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        self.book_manager.add_note_to_chapter("Test Book", 1, "This is a note for chapter 1.")
        book = self.book_manager.books["Test Book"]
        self.assertIn(1, book.get_notes())
        self.assertIn("This is a note for chapter 1.", book.get_notes()[1])

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        self.book_manager.add_note_to_chapter("Test Book", 1, "This is a text note.")
        book = self.book_manager.books["Test Book"]
        self.assertIn("This is a text note.", book.get_notes()[1])

    def test_organize_notes_for_easy_access(self):
        # Functionalities 4: Organize Notes for Easy Access
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        self.book_manager.add_note_to_chapter("Test Book", 1, "Note 1")
        self.book_manager.add_note_to_chapter("Test Book", 2, "Note 2")
        book = self.book_manager.books["Test Book"]
        notes = book.get_notes()
        self.assertIn(1, notes)
        self.assertIn(2, notes)
        self.assertIn("Note 1", notes[1])
        self.assertIn("Note 2", notes[2])

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        self.fail("not implemented")

    def test_search_for_specific_books(self):
        # Functionalities 6: Search for Specific Books
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        results = self.book_manager.search_books("Test Book")
        self.assertIn("Test Book", results)

    def test_search_for_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        self.book_manager.add_book("Test Book", "Author Name", "Fiction", "2023-01-01")
        self.book_manager.add_note_to_chapter("Test Book", 1, "Important note")
        results = self.book_manager.search_notes("Important")
        self.assertTrue(any("Important note" in note for _, _, note in results))

if __name__ == '__main__':
    unittest.main()
