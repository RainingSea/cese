import unittest
from snippet_manager import SnippetManager
from snippet import Snippet
import os

class TestSnippetManager(unittest.TestCase):

    def setUp(self):
        # Setup a SnippetManager instance and a test file
        self.manager = SnippetManager()
        self.test_file = 'test_snippets.txt'
        self.manager.snippets = []  # Clear any existing snippets

    def tearDown(self):
        # Clean up the test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_store_text_snippets(self):
        # Test saving a valid snippet
        snippet = Snippet("print('Hello, World!')", ["python"], "A simple hello world snippet")
        self.manager.save_snippet(snippet)
        self.assertIn(snippet, self.manager.load_snippets())

        # Test saving an empty snippet
        with self.assertRaises(ValueError):
            self.manager.save_snippet(Snippet("", [], ""))

    def test_categorize_snippets_based_on_tags(self):
        # Test adding tags to a snippet
        snippet = Snippet("print('Hello, World!')", ["python"], "A simple hello world snippet")
        self.manager.save_snippet(snippet)
        snippet.tags.append("example")
        self.manager.save_snippet(snippet)
        self.assertIn("example", snippet.tags)

        # Test adding a tag that exceeds the character limit
        with self.assertRaises(ValueError):
            snippet.tags.append("a" * 256)  # Assuming 255 is the limit

    def test_add_descriptions_to_improve_searchability(self):
        # Test adding a description to a snippet
        snippet = Snippet("print('Hello, World!')", ["python"], "A simple hello world snippet")
        self.manager.save_snippet(snippet)
        snippet.description = "Updated description"
        self.manager.save_snippet(snippet)
        self.assertEqual(snippet.description, "Updated description")

        # Test saving a description that is too long
        with self.assertRaises(ValueError):
            snippet.description = "a" * 1024  # Assuming 1023 is the limit

    def test_support_text_formatting_for_readability(self):
        # Test applying bold formatting
        snippet = Snippet("print('Hello, World!')", ["python"], "A simple hello world snippet")
        formatted_snippet = self.manager.format_snippet("**bold**")
        self.assertEqual(formatted_snippet, "<b>bold</b>")

        # Test unsupported formatting
        with self.assertRaises(ValueError):
            self.manager.format_snippet("__underline__")

    def test_support_syntax_highlighting(self):
        # Test saving a code snippet with syntax highlighting
        snippet = Snippet("def add(a, b): return a + b", ["python"], "Function to add two numbers")
        self.manager.save_snippet(snippet)
        self.assertIn(snippet, self.manager.load_snippets())

        # Test changing the programming language
        snippet.tags = ["javascript"]
        self.manager.save_snippet(snippet)
        self.assertIn("javascript", snippet.tags)

if __name__ == '__main__':
    unittest.main()
