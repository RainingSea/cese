import unittest
import os
from book_manager import BookManager

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.manager = BookManager()
        # Clear books.txt and shelves.txt for testing
        open('books.txt', 'w').close()
        open('shelves.txt', 'w').close()

    def test_add_book(self):
        # Functionalities 1: Input Book Details
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.assertEqual(len(self.manager.books), 1)
        self.assertEqual(self.manager.books[0].title, "Dune")
        self.assertEqual(self.manager.books[0].author, "Frank Herbert")

    def test_create_shelf(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.manager.add_shelf("Science Fiction")
        self.assertEqual(len(self.manager.shelves), 1)
        self.assertEqual(self.manager.shelves[0].name, "Science Fiction")

    def test_add_note_to_book(self):
        # Functionalities 3: Add Personal Notes to Books
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_note_to_book(0, "Favorite chapter is 3")
        self.assertEqual(self.manager.books[0].notes[0], "Favorite chapter is 3")

    def test_rate_book(self):
        # Functionalities 4: Add Ratings to Books
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.rate_book(0, 4)
        self.assertEqual(self.manager.books[0].rating, 4)

    def test_generate_report(self):
        # Functionalities 5: Generate Reports on the Book Collection
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        report = self.manager.generate_report()
        self.assertIn("Dune by Frank Herbert", report)

    def test_search_books(self):
        # Functionalities 6: Search for Books
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        results = self.manager.search_books("Dune")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Dune")

    def test_filter_books(self):
        # Functionalities 7: Filter Books Based on Criteria
        self.manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_book("Foundation", "Isaac Asimov", "Science Fiction", 1951)
        filtered_books = self.manager.filter_books("Science Fiction")
        self.assertEqual(len(filtered_books), 2)

    def test_failures(self):
        # Testing unimplemented functionalities
        self.fail("Edit an existing note functionality not implemented")
        self.fail("Delete a note functionality not implemented")
        self.fail("Generate report for a specific category functionality not implemented")
        self.fail("Filter books by rating functionality not implemented")

if __name__ == '__main__':
    unittest.main()
