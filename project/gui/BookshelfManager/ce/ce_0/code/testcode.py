import unittest
from book_manager import BookManager
from book import Book

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertEqual(self.book_manager.books[-1].title, "Dune")

    def test_categorize_books_into_custom_defined_shelves(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        shelves = self.book_manager.get_shelves()
        self.assertIn("Science Fiction", shelves)
        filtered_books = self.book_manager.filter_books({"shelf": "Science Fiction"})
        self.assertTrue(any(book.title == "Dune" for book in filtered_books))

    def test_add_personal_notes_to_books(self):
        # Functionalities 3: Add Personal Notes to Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        book = self.book_manager.books[-1]
        self.assertEqual(book.notes, "Epic novel")
        book.notes = "Favorite chapter is 3"
        self.assertEqual(book.notes, "Favorite chapter is 3")
        book.notes = ""
        self.assertEqual(book.notes, "")

    def test_add_ratings_to_books(self):
        # Functionalities 4: Add Ratings to Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        book = self.book_manager.books[-1]
        self.assertEqual(book.rating, 4.7)

    def test_generate_reports_on_the_book_collection(self):
        # Functionalities 5: Generate Reports on the Book Collection
        report = self.book_manager.generate_report()
        self.assertIn("total_books", report)
        self.assertIn("average_rating", report)
        self.assertIn("shelves", report)

    def test_search_for_books(self):
        # Functionalities 6: Search for Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        search_results = self.book_manager.search_books("Dune")
        self.assertTrue(any(book.title == "Dune" for book in search_results))

    def test_filter_books_based_on_criteria(self):
        # Functionalities 7: Filter Books Based on Criteria
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Science Fiction", "Epic novel", 4.7)
        filtered_books = self.book_manager.filter_books({"genre": "Science Fiction"})
        self.assertTrue(any(book.title == "Dune" for book in filtered_books))
        filtered_books = [book for book in self.book_manager.books if book.rating >= 4.0]
        self.assertTrue(all(book.rating >= 4.0 for book in filtered_books))

if __name__ == '__main__':
    unittest.main()
