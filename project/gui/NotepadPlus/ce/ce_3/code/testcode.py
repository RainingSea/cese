import unittest
import tkinter as tk
from main import NotepadPlus

class TestNotepadPlus(unittest.TestCase):

    def setUp(self):
        # Initialize the NotepadPlus application
        self.app = NotepadPlus()
        self.app.root.update()  # Ensure the UI is updated

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.app.root.destroy()

    def test_enable_text_file_creation_and_editing(self):
        # Step 1: Check if the application launches successfully
        self.assertIsInstance(self.app.text_area, tk.Text)

        # Step 2: Type "Hello, World!" in the text area
        self.app.text_area.insert(tk.END, "Hello, World!")
        self.assertEqual(self.app.text_area.get(1.0, tk.END).strip(), "Hello, World!")

        # Step 3: Save the file with the name "test.txt"
        # Simulate file save (mocking file dialog is required for full test)
        self.app.save_file("test.txt")
        with open("test.txt", "r") as file:
            content = file.read()
        self.assertEqual(content.strip(), "Hello, World!")

        # Step 4: Open "test.txt" in Notepad Plus
        self.app.open_file("test.txt")
        self.assertEqual(self.app.text_area.get(1.0, tk.END).strip(), "Hello, World!")

    def test_provide_syntax_highlighting(self):
        # This functionality is not directly testable without additional implementation
        self.fail("Syntax highlighting test not implemented")

    def test_offer_code_indentation_features(self):
        # This functionality is not directly testable without additional implementation
        self.fail("Code indentation test not implemented")

    def test_provide_search_functionality(self):
        # Step 1: Open a text file containing the text "Hello, World!"
        self.app.text_area.insert(tk.END, "Hello, World!")

        # Step 2: Use the search feature to find "World"
        search_results = self.app.search_text("World")
        self.assertIn("Hello, World!", search_results)

    def test_provide_replace_functionality(self):
        # Step 1: Open a text file containing the text "Hello, World!"
        self.app.text_area.insert(tk.END, "Hello, World!")

        # Step 2: Use the replace feature to replace "World" with "Universe"
        self.app.replace_text("World", "Universe")
        self.assertEqual(self.app.text_area.get(1.0, tk.END).strip(), "Hello, Universe!")

        # Step 3: Use the replace feature to replace "Hello" with "Greetings"
        self.app.replace_text("Hello", "Greetings")
        self.assertEqual(self.app.text_area.get(1.0, tk.END).strip(), "Greetings, Universe!")

    def test_offer_customizable_themes(self):
        # Step 1: Change to dark theme
        self.app.apply_theme("dark")
        self.assertEqual(self.app.text_area.cget("bg"), "#000000")
        self.assertEqual(self.app.text_area.cget("fg"), "#ffffff")

        # Step 2: Change back to light theme
        self.app.apply_theme("light")
        self.assertEqual(self.app.text_area.cget("bg"), "#ffffff")
        self.assertEqual(self.app.text_area.cget("fg"), "#000000")

if __name__ == '__main__':
    unittest.main()
