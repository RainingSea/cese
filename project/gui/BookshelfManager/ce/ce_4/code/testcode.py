import unittest
from books import BookManager, Book

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.book_manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "Classic American novel", 4.5)

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        initial_count = len(self.book_manager.books)
        self.book_manager.add_book("1984", "George Orwell", "Dystopian", 1949, "A novel about totalitarianism", 4.7)
        self.assertEqual(len(self.book_manager.books), initial_count + 1)
        self.assertEqual(self.book_manager.books[-1].title, "1984")

    def test_categorize_books_into_custom_defined_shelves(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.fail("not implemented")

    def test_add_personal_notes_to_books(self):
        # Functionalities 3: Add Personal Notes to Books
        book = self.book_manager.books[0]
        original_notes = book.notes
        book.notes = "Favorite chapter is 3"
        self.assertEqual(book.notes, "Favorite chapter is 3")
        
        # Edit an existing note
        book.notes = "Updated note"
        self.assertEqual(book.notes, "Updated note")
        
        # Delete a note from a book
        book.notes = ""
        self.assertEqual(book.notes, "")

    def test_add_ratings_to_books(self):
        # Functionalities 4: Add Ratings to Books
        book = self.book_manager.books[0]
        book.rating = 4.0
        self.assertEqual(book.rating, 4.0)

    def test_generate_reports_on_the_book_collection(self):
        # Functionalities 5: Generate Reports on the Book Collection
        report = self.book_manager.generate_report()
        self.assertIn("The Great Gatsby by F. Scott Fitzgerald", report)
        self.fail("Generate a report for a specific category not implemented")

    def test_search_for_books(self):
        # Functionalities 6: Search for Books
        results = self.book_manager.search_books("Gatsby")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Great Gatsby")

    def test_filter_books_based_on_criteria(self):
        # Functionalities 7: Filter Books Based on Criteria
        results = self.book_manager.filter_books({'genre': 'Fiction'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Great Gatsby")
        
        # Filter by rating
        results = self.book_manager.filter_books({'year': 1925})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Great Gatsby")

if __name__ == '__main__':
    unittest.main()
