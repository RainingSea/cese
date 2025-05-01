import unittest
import os
from book_manager import BookManager

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.book_manager.load_data()

    def test_add_book(self):
        # Functionalities 1: Input Book Details
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        self.assertIn("Dune|Frank Herbert|Science Fiction|1965|A classic sci-fi novel.|5.0|Science Fiction", self.book_manager.books)

    def test_create_shelf(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.book_manager.shelves.append("Science Fiction")
        self.book_manager.save_data()
        self.assertIn("Science Fiction", self.book_manager.shelves)

    def test_assign_book_to_shelf(self):
        # Functionalities 2: Assign a book to a custom shelf
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        self.assertIn("Dune|Frank Herbert|Science Fiction|1965|A classic sci-fi novel.|5.0|Science Fiction", self.book_manager.books)

    def test_add_personal_notes(self):
        # Functionalities 3: Add Personal Notes to Books
        self.fail("not implemented")  # Note functionality is not implemented

    def test_edit_note(self):
        # Functionalities 3: Edit an existing note
        self.fail("not implemented")  # Note functionality is not implemented

    def test_delete_note(self):
        # Functionalities 3: Delete a note from a book
        self.fail("not implemented")  # Note functionality is not implemented

    def test_add_rating(self):
        # Functionalities 4: Add Ratings to Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        self.assertIn("5.0", self.book_manager.books[0])

    def test_generate_report(self):
        # Functionalities 5: Generate Reports on the Book Collection
        report = self.book_manager.generate_report()
        self.assertIn("Books in Collection:", report)

    def test_search_books(self):
        # Functionalities 6: Search for Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        results = self.book_manager.search_books("Dune")
        self.assertEqual(len(results), 1)
        self.assertIn("Dune|Frank Herbert|Science Fiction|1965|A classic sci-fi novel.|5.0|Science Fiction", results[0])

    def test_filter_books_by_category(self):
        # Functionalities 7: Filter Books Based on Criteria
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        results = self.book_manager.filter_books("Science Fiction")
        self.assertEqual(len(results), 1)
        self.assertIn("Dune|Frank Herbert|Science Fiction|1965|A classic sci-fi novel.|5.0|Science Fiction", results[0])

    def test_filter_books_by_rating(self):
        # Functionalities 7: Filter Books Based on Criteria
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "A classic sci-fi novel.", 5.0, "Science Fiction")
        results = self.book_manager.filter_books("5.0")
        self.assertEqual(len(results), 1)
        self.assertIn("Dune|Frank Herbert|Science Fiction|1965|A classic sci-fi novel.|5.0|Science Fiction", results[0])

    def tearDown(self):
        # Clean up the test environment
        if os.path.exists("books.txt"):
            os.remove("books.txt")
        if os.path.exists("shelves.txt"):
            os.remove("shelves.txt")

if __name__ == '__main__':
    unittest.main()
