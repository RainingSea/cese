import unittest
from book import Book
from bookshelf_manager import BookshelfManager

class TestBookshelfManager(unittest.TestCase):

    def setUp(self):
        self.manager = BookshelfManager()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        book = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_book(book)
        self.assertIn(book, self.manager.books)

    def test_categorize_books_into_custom_defined_shelves(self):
        # Functionalities 2: Categorize Books into Custom-Defined Shelves
        self.fail("not implemented")  # No implementation for custom shelves in the codebase

    def test_add_personal_notes_to_books(self):
        # Functionalities 3: Add Personal Notes to Books
        book = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_book(book)
        
        # Add a note
        book.add_notes("Favorite chapter is 3")
        self.assertEqual(book.notes, "Favorite chapter is 3")
        
        # Edit the note
        book.add_notes("Favorite chapter is 4")
        self.assertEqual(book.notes, "Favorite chapter is 4")
        
        # Delete the note
        book.add_notes("")
        self.assertEqual(book.notes, "")

    def test_add_ratings_to_books(self):
        # Functionalities 4: Add Ratings to Books
        book = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_book(book)
        
        # Add a valid rating
        book.add_rating(4.0)
        self.assertEqual(book.rating, 4.0)

    def test_generate_reports_on_the_book_collection(self):
        # Functionalities 5: Generate Reports on the Book Collection
        book1 = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        book2 = Book("1984", "George Orwell", "Dystopian", 1949)
        self.manager.add_book(book1)
        self.manager.add_book(book2)
        
        report = self.manager.generate_report()
        self.assertEqual(report['total_books'], 2)
        self.assertAlmostEqual(report['average_rating'], 0.0)  # No ratings added yet

        self.fail("not implemented")  # No implementation for category-specific reports in the codebase

    def test_search_for_books(self):
        # Functionalities 6: Search for Books
        book = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.manager.add_book(book)
        
        results = self.manager.search_books("Dune")
        self.assertIn(book, results)

    def test_filter_books_based_on_criteria(self):
        # Functionalities 7: Filter Books Based on Criteria
        book1 = Book("Dune", "Frank Herbert", "Science Fiction", 1965)
        book2 = Book("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937)
        self.manager.add_book(book1)
        self.manager.add_book(book2)
        
        # Filter by genre
        filtered_books = self.manager.filter_books({'genre': 'Fantasy'})
        self.assertIn(book2, filtered_books)
        self.assertNotIn(book1, filtered_books)

        # Filter by rating
        book1.add_rating(4.5)
        book2.add_rating(3.0)
        filtered_books = self.manager.filter_books({'rating': 4})
        self.fail("not implemented")  # No implementation for rating-based filtering in the codebase

if __name__ == '__main__':
    unittest.main()
