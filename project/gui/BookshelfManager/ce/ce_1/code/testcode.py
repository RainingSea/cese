import unittest
from BookManager import BookManager
from Book import Book

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965, "Epic novel", 4.9)
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertEqual(self.book_manager.books[-1].title, "Dune")

    def test_categorize_books_into_custom_defined_shelves(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.fail("not implemented")

    def test_add_personal_notes_to_books(self):
        # Functionalities 3: Add Personal Notes to Books
        self.fail("not implemented")

    def test_add_ratings_to_books(self):
        # Functionalities 4: Add Ratings to Books
        book = self.book_manager.books[0]
        original_rating = book.rating
        self.book_manager.add_book("New Book", "New Author", "New Genre", 2023, "New Notes", 4.5)
        self.assertEqual(self.book_manager.books[-1].rating, 4.5)

    def test_generate_reports_on_the_book_collection(self):
        # Functionalities 5: Generate Reports on the Book Collection
        report = self.book_manager.generate_report()
        self.assertIn("The Great Gatsby by F. Scott Fitzgerald", report)
        self.fail("not implemented for specific category")

    def test_search_for_books(self):
        # Functionalities 6: Search for Books
        results = self.book_manager.search_books("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_filter_books_based_on_criteria(self):
        # Functionalities 7: Filter Books Based on Criteria
        filtered_books = self.book_manager.filter_books({'genre': 'Fiction'})
        self.assertTrue(all(book.genre == 'Fiction' for book in filtered_books))
        self.fail("not implemented for rating filter")

if __name__ == '__main__':
    unittest.main()
