import unittest
import os
from text_editor import TextEditor

class TestTextEditor(unittest.TestCase):

    def setUp(self):
        self.editor = TextEditor()

    def test_enable_text_file_creation_and_editing(self):
        # Step: Open Notepad Plus application
        # Expectation: The application launches successfully, displaying a blank text area for editing
        self.assertEqual(self.editor.text_area.get(1.0, 'end-1c'), "")

        # Step: Type "Hello, World!" in the text area
        # Expectation: The text "Hello, World!" appears in the text area
        self.editor.text_area.insert('1.0', "Hello, World!")
        self.assertEqual(self.editor.text_area.get(1.0, 'end-1c'), "Hello, World!")

        # Step: Save the file with the name "test.txt"
        # Expectation: The file is saved successfully in the local storage
        test_filename = "test.txt"
        self.editor.save_file(test_filename)
        self.assertTrue(os.path.exists(test_filename))

        # Step: Open "test.txt" in Notepad Plus
        # Expectation: The text "Hello, World!" is displayed in the text area
        self.editor.open_file(test_filename)
        self.assertEqual(self.editor.text_area.get(1.0, 'end-1c'), "Hello, World!")

        # Clean up
        os.remove(test_filename)

    def test_provide_syntax_highlighting(self):
        # This functionality is not implemented in the codebase
        self.fail("Syntax highlighting functionality is not implemented")

    def test_offer_code_indentation_features(self):
        # This functionality is not implemented in the codebase
        self.fail("Code indentation functionality is not implemented")

    def test_provide_search_functionality(self):
        # Step: Open a text file containing the text "Hello, World!"
        self.editor.text_area.insert('1.0', "Hello, World!")

        # Step: Use the search feature to find "World"
        # Expectation: The search highlights the word "World" in the text area
        matches = self.editor.search("World")
        self.assertTrue(matches)

        # Step: Click "Next" to find the next occurrence
        # Expectation: If there are no more occurrences, a message indicates that the search has reached the end of the document
        self.assertEqual(len(matches), 1)

    def test_provide_replace_functionality(self):
        # Step: Open a text file containing the text "Hello, World!"
        self.editor.text_area.insert('1.0', "Hello, World!")

        # Step: Use the replace feature to replace "World" with "Universe"
        # Expectation: The text changes to "Hello, Universe!" in the text area
        self.editor.replace("World", "Universe")
        self.assertEqual(self.editor.text_area.get(1.0, 'end-1c'), "Hello, Universe!")

        # Step: Use the replace feature to replace "Hello" with "Greetings"
        # Expectation: The text changes to "Greetings, Universe!" in the text area
        self.editor.replace("Hello", "Greetings")
        self.assertEqual(self.editor.text_area.get(1.0, 'end-1c'), "Greetings, Universe!")

    def test_offer_customizable_themes(self):
        # This functionality is not implemented in the codebase
        self.fail("Customizable themes functionality is not implemented")

if __name__ == '__main__':
    unittest.main()
