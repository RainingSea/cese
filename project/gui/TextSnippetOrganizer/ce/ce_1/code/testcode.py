import unittest
import os
from main import SnippetManager

class TestSnippetManager(unittest.TestCase):

    def setUp(self):
        self.snippet_manager = SnippetManager()
        # Clear existing snippets for testing
        self.snippet_manager.snippets = []
        self.snippet_manager.tags = []
        self.snippet_manager.descriptions = []
        self.snippet_manager.save_snippets()

    def test_store_text_snippets(self):
        # Functionality 1: Store Text Snippets
        self.snippet_manager.add_snippet("First snippet example.", ["example"], "This is the first snippet.")
        self.assertIn("First snippet example.", self.snippet_manager.snippets)
        
        # Attempt to save an empty snippet
        with self.assertRaises(ValueError):
            self.snippet_manager.add_snippet("", ["tag"], "Description")  # This should raise an error

    def test_categorize_snippets_based_on_tags(self):
        # Functionality 2: Categorize Snippets Based on Tags
        self.snippet_manager.add_snippet("Second snippet example.", ["example"], "This is the second snippet.")
        self.snippet_manager.tags.append("example")
        self.snippet_manager.save_snippets()
        
        self.assertIn("example", self.snippet_manager.tags)

        # Attempt to add a tag that exceeds the character limit
        long_tag = "a" * 256  # Assuming 255 is the limit
        with self.assertRaises(ValueError):
            self.snippet_manager.add_snippet("Snippet", [long_tag], "Description")  # This should raise an error

    def test_add_descriptions(self):
        # Functionality 3: Add Descriptions to Improve Searchability
        self.snippet_manager.add_snippet("Snippet with description.", ["tag"], "This is a valid description.")
        self.assertIn("This is a valid description.", self.snippet_manager.descriptions)

        # Attempt to save a description that is too long
        long_description = "a" * 256  # Assuming 255 is the limit
        with self.assertRaises(ValueError):
            self.snippet_manager.add_snippet("Snippet", ["tag"], long_description)  # This should raise an error

    def test_support_text_formatting(self):
        # Functionality 4: Support Text Formatting for Readability
        # This functionality is not implemented in the codebase
        self.fail("Text formatting functionality not implemented.")

    def test_support_syntax_highlighting(self):
        # Functionality 5: Support Syntax Highlighting
        # This functionality is not implemented in the codebase
        self.fail("Syntax highlighting functionality not implemented.")

if __name__ == '__main__':
    unittest.main()
