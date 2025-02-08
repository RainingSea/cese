import unittest
import tkinter as tk
from main import BookNoteApp, Book, Note

class TestBookNoteApp(unittest.TestCase):

    def setUp(self):
        # Set up the application for testing
        self.root = tk.Tk()
        self.app = BookNoteApp(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_input_book_details(self):
        # Functionalities 1: Input Book Details
        self.app.title_entry.insert(0, "New Book")
        self.app.author_entry.insert(0, "New Author")
        self.app.genre_entry.insert(0, "New Genre")
        self.app.pub_date_entry.insert(0, "2023")

        self.app.add_book()

        self.assertIn("New Book", [book.title for book in self.app.books])

    def test_create_notes_for_each_chapter(self):
        # Functionalities 2: Create Notes for Each Chapter or Section
        self.app.note_title_entry.insert(0, "The Great Gatsby")
        self.app.chapter_entry.insert(0, "Chapter 1")
        self.app.note_content_entry.insert(0, "New Note Content")

        self.app.add_note()

        self.assertIn("New Note Content", [note.content for note in self.app.notes])

    def test_add_text_notes(self):
        # Functionalities 3: Add Text Notes
        self.app.note_title_entry.insert(0, "1984")
        self.app.chapter_entry.insert(0, "Chapter 4")
        self.app.note_content_entry.insert(0, "Additional Note Content")

        self.app.add_note()

        self.assertIn("Additional Note Content", [note.content for note in self.app.notes])

    def test_organize_notes_for_easy_access(self):
        # Functionalities 4: Organize Notes for Easy Access
        # This functionality is not explicitly implemented in the codebase
        self.fail("Organize Notes for Easy Access not implemented")

    def test_categorize_notes(self):
        # Functionalities 5: Categorize Notes
        # This functionality is not explicitly implemented in the codebase
        self.fail("Categorize Notes not implemented")

    def test_search_for_specific_books(self):
        # Functionalities 6: Search for Specific Books
        self.app.search_entry.insert(0, "1984")
        self.app.search()

        search_results = self.app.display_area.get(1.0, tk.END).strip()
        self.assertIn("1984|George Orwell|Dystopian|1949", search_results)

    def test_search_for_specific_notes(self):
        # Functionalities 7: Search for Specific Notes
        self.app.search_entry.insert(0, "Jay Gatsby")
        self.app.search()

        search_results = self.app.display_area.get(1.0, tk.END).strip()
        self.assertIn("Introduction to the main character, Jay Gatsby.", search_results)

        # Search for a note in a specific category is not implemented
        self.fail("Search for a note in a specific category not implemented")

if __name__ == '__main__':
    unittest.main()
