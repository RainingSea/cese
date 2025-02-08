import unittest
import os
from main import Book, Note, BookManager, NoteManager

class TestBookNoteApplication(unittest.TestCase):

    def setUp(self):
        # Ensure the test environment is clean
        if os.path.exists('books.txt'):
            os.remove('books.txt')
        if os.path.exists('notes.txt'):
            os.remove('notes.txt')

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        book = Book("Test Title", "Test Author", "Test Genre", "2023")
        book.save()
        
        book_manager = BookManager()
        books = book_manager.load_books()
        
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Title")
        self.assertEqual(books[0].author, "Test Author")
        self.assertEqual(books[0].genre, "Test Genre")
        self.assertEqual(books[0].publication_date, "2023")

    def test_create_notes_for_each_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        note = Note("Test Title", "Chapter 1", "This is a test note.")
        note.save()
        
        note_manager = NoteManager()
        notes = note_manager.load_notes()
        
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].book_title, "Test Title")
        self.assertEqual(notes[0].chapter, "Chapter 1")
        self.assertEqual(notes[0].content, "This is a test note.")

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        note = Note("Test Title", "Chapter 1", "This is another test note.")
        note.save()
        
        note_manager = NoteManager()
        notes = note_manager.load_notes()
        
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].content, "This is another test note.")

    def test_organize_notes_for_easy_access(self):
        # Functionalities 4: Organize Notes for Easy Access
        note = Note("Test Title", "Chapter 1", "Organized note content.")
        note.save()
        
        note_manager = NoteManager()
        notes = note_manager.load_notes()
        
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].chapter, "Chapter 1")

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        self.fail("not implemented")

    def test_search_for_specific_books(self):
        # Functionalities 6: Search for Specific Books
        book = Book("Searchable Title", "Author", "Genre", "2023")
        book.save()
        
        book_manager = BookManager()
        results = book_manager.search_books("Searchable")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Searchable Title")

    def test_search_for_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        note = Note("Test Title", "Chapter 1", "Keyword note content.")
        note.save()
        
        note_manager = NoteManager()
        results = note_manager.search_notes("Keyword")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].content, "Keyword note content.")

if __name__ == '__main__':
    unittest.main()
