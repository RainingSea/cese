import unittest
import os
from main import NotepadPlus

class TestNotepadPlus(unittest.TestCase):

    def setUp(self):
        # Initialize the NotepadPlus application
        self.notepad = NotepadPlus()

    def test_text_file_creation_and_editing(self):
        # Functionalities 1: Enable Text File Creation and Editing
        self.notepad.create_new_file()
        self.notepad.text_area.set_content("Hello, World!")
        self.assertEqual(self.notepad.text_area.get_content().strip(), "Hello, World!")

        # Save the file
        test_file_path = "test.txt"
        self.notepad.save_file(test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

        # Open the file
        self.notepad.open_file(test_file_path)
        self.assertEqual(self.notepad.text_area.get_content().strip(), "Hello, World!")

        # Clean up
        os.remove(test_file_path)

    def test_syntax_highlighting(self):
        # Functionalities 2: Provide Syntax Highlighting for Various Programming Languages
        # This functionality requires GUI interaction and is not directly testable with unittest.
        self.fail("Syntax highlighting test not implemented due to GUI limitations.")

    def test_code_indentation(self):
        # Functionalities 3: Offer Code Indentation Features
        # This functionality requires GUI interaction and is not directly testable with unittest.
        self.fail("Code indentation test not implemented due to GUI limitations.")

    def test_search_functionality(self):
        # Functionalities 4: Provide Search Functionality
        self.notepad.text_area.set_content("Hello, World!")
        self.notepad.search_text("World")
        # Since search result is shown via messagebox, we cannot capture it directly in unittest.
        self.fail("Search functionality test not implemented due to GUI limitations.")

    def test_replace_functionality(self):
        # Functionalities 5: Provide Replace Functionality
        self.notepad.text_area.set_content("Hello, World!")
        self.notepad.replace_text("World", "Universe")
        self.assertEqual(self.notepad.text_area.get_content().strip(), "Hello, Universe!")

        self.notepad.replace_text("Hello", "Greetings")
        self.assertEqual(self.notepad.text_area.get_content().strip(), "Greetings, Universe!")

    def test_customizable_themes(self):
        # Functionalities 6: Offer Customizable Themes
        # This functionality requires GUI interaction and is not directly testable with unittest.
        self.fail("Customizable themes test not implemented due to GUI limitations.")

if __name__ == '__main__':
    unittest.main()
