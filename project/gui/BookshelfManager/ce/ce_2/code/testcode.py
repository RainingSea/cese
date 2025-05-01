import unittest
from book_manager import BookManager

class TestBookManager(unittest.TestCase):

    def setUp(self):
        self.book_manager = BookManager()
        self.book_manager.books = []  # Reset books for testing
        self.book_manager.notes = {}
        self.book_manager.ratings = {}
        self.book_manager.next_id = 1  # Start IDs from 1 for testing

    def test_add_book(self):
        # Functionalities 1: Input Book Details
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.assertEqual(len(self.book_manager.books), 1)
        self.assertEqual(self.book_manager.books[0].title, "Dune")
        self.assertEqual(self.book_manager.books[0].author, "Frank Herbert")
        self.assertEqual(self.book_manager.books[0].genre, "Science Fiction")
        self.assertEqual(self.book_manager.books[0].year, 1965)

    def test_add_note(self):
        # Functionalities 3: Add Personal Notes to Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.book_manager.add_note(1, "Favorite chapter is 3")
        self.assertEqual(self.book_manager.notes[1], "Favorite chapter is 3")

        # Edit an existing note
        self.book_manager.add_note(1, "Updated note")
        self.assertEqual(self.book_manager.notes[1], "Updated note")

        # Delete a note
        del self.book_manager.notes[1]
        self.assertNotIn(1, self.book_manager.notes)

    def test_add_rating(self):
        # Functionalities 4: Add Ratings to Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.book_manager.add_rating(1, 4.5)
        self.assertEqual(self.book_manager.ratings[1], 4.5)

    def test_generate_report(self):
        # Functionalities 5: Generate Reports on the Book Collection
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.book_manager.add_note(1, "Favorite chapter is 3")
        self.book_manager.add_rating(1, 4.5)
        report = self.book_manager.generate_report()
        self.assertIn("Dune by Frank Herbert - Science Fiction (1965)", report)
        self.assertIn("Note: Favorite chapter is 3", report)
        self.assertIn("Rating: 4.5", report)

    def test_search_books(self):
        # Functionalities 6: Search for Books
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        results = self.book_manager.search_books("Dune")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Dune")

    def test_filter_books(self):
        # Functionalities 7: Filter Books Based on Criteria
        self.book_manager.add_book("Dune", "Frank Herbert", "Science Fiction", 1965)
        self.book_manager.add_book("Foundation", "Isaac Asimov", "Science Fiction", 1951)
        filtered = self.book_manager.filter_books("Science Fiction")
        self.assertEqual(len(filtered), 2)

        # Test filtering by rating
        self.book_manager.add_rating(1, 4.5)
        self.book_manager.add_rating(2, 3.5)
        high_rated = [book for book in self.book_manager.books if self.book_manager.ratings.get(book.id, 0) >= 4.0]
        self.assertEqual(len(high_rated), 1)
        self.assertEqual(high_rated[0].title, "Dune")

if __name__ == '__main__':
    unittest.main()
