import unittest
import os
from data_manager import DataManager

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()
        # Clear the files before each test
        open(self.data_manager.books_file, 'w').close()
        open(self.data_manager.notes_file, 'w').close()
        open(self.data_manager.categories_file, 'w').close()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        self.data_manager.save_book("The Great Gatsby", "F. Scott Fitzgerald", "1925")
        books = self.data_manager.load_books()
        self.assertIn("The Great Gatsby|F. Scott Fitzgerald|1925", books)

    def test_create_notes_for_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        self.data_manager.save_book("The Great Gatsby", "F. Scott Fitzgerald", "1925")
        self.data_manager.save_note(1, "Chapter 1", "This is a note for chapter 1.")
        notes = self.data_manager.load_notes()
        self.assertIn("1|Chapter 1|This is a note for chapter 1.", notes)

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        self.data_manager.save_book("1984", "George Orwell", "1949")
        self.data_manager.save_note(1, "Chapter 1", "Important themes in 1984.")
        notes = self.data_manager.load_notes()
        self.assertIn("1|Chapter 1|Important themes in 1984.", notes)

    def test_organize_notes(self):
        # Functionalities 4: Organize Notes for Easy Access
        self.data_manager.save_book("To Kill a Mockingbird", "Harper Lee", "1960")
        self.data_manager.save_note(1, "Chapter 1", "Note for chapter 1.")
        notes = self.data_manager.load_notes()
        self.assertIn("1|Chapter 1|Note for chapter 1.", notes)

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        self.data_manager.save_category("Quotes")
        self.data_manager.save_note(1, "Chapter 1", "A famous quote.")
        categories = self.data_manager.load_categories()
        self.assertIn("Quotes", categories)

    def test_search_specific_books(self):
        # Functionalities 6: Search for Specific Books
        self.data_manager.save_book("The Great Gatsby", "F. Scott Fitzgerald", "1925")
        results = self.data_manager.load_books()
        matching_books = [book for book in results if "The Great Gatsby" in book]
        self.assertIn("The Great Gatsby|F. Scott Fitzgerald|1925", matching_books)

    def test_search_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        self.data_manager.save_book("1984", "George Orwell", "1949")
        self.data_manager.save_note(1, "Chapter 1", "Dystopian themes.")
        results = self.data_manager.load_notes()
        matching_notes = [note for note in results if "Dystopian" in note]
        self.assertIn("1|Chapter 1|Dystopian themes.", matching_notes)

    def test_search_notes_in_category(self):
        # Functionalities 8: Search Notes in a Specific Category
        self.fail("not implemented")  # This functionality is not implemented in the codebase

if __name__ == '__main__':
    unittest.main()
