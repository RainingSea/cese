import unittest
from snippets.snippet_manager import SnippetManager
from snippets.snippet import Snippet
import os
import json

class TestSnippetManager(unittest.TestCase):

    def setUp(self):
        self.snippet_manager = SnippetManager()
        # Ensure the snippets directory exists
        os.makedirs('snippets', exist_ok=True)

    def tearDown(self):
        # Clean up any created snippet files
        for filename in os.listdir('snippets'):
            if filename.endswith('.json'):
                os.remove(os.path.join('snippets', filename))

    def test_store_text_snippets(self):
        # Test adding a valid snippet
        self.snippet_manager.add_snippet("print('Hello World')", ["python", "hello"], "A simple hello world snippet in Python.")
        self.assertIn("python", self.snippet_manager.snippets)
        
        # Test saving an empty snippet
        with self.assertRaises(ValueError):
            self.snippet_manager.add_snippet("", [], "")

    def test_categorize_snippets_based_on_tags(self):
        # Test adding tags to a snippet
        self.snippet_manager.add_snippet("print('Hello World')", ["python"], "A simple hello world snippet in Python.")
        self.snippet_manager.edit_snippet("python", "print('Hello World')", ["python", "example"], "A simple hello world snippet in Python.")
        self.assertIn("example", self.snippet_manager.snippets["python"].tags)
        
        # Test adding a tag that exceeds the character limit
        long_tag = "a" * 256
        with self.assertRaises(ValueError):
            self.snippet_manager.edit_snippet("python", "print('Hello World')", [long_tag], "A simple hello world snippet in Python.")

    def test_add_descriptions_to_improve_searchability(self):
        # Test adding a description to a snippet
        self.snippet_manager.add_snippet("print('Hello World')", ["python"], "A simple hello world snippet in Python.")
        self.snippet_manager.edit_snippet("python", "print('Hello World')", ["python"], "Updated description")
        self.assertEqual(self.snippet_manager.snippets["python"].description, "Updated description")
        
        # Test saving a description that is too long
        long_description = "a" * 1024
        with self.assertRaises(ValueError):
            self.snippet_manager.edit_snippet("python", "print('Hello World')", ["python"], long_description)

    def test_support_text_formatting_for_readability(self):
        # This functionality is not implemented in the codebase
        self.fail("Support for text formatting is not implemented")

    def test_support_syntax_highlighting(self):
        # This functionality is not implemented in the codebase
        self.fail("Support for syntax highlighting is not implemented")

if __name__ == '__main__':
    unittest.main()
