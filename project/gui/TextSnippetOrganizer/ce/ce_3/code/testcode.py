import unittest
from snippets.snippet_manager import SnippetManager
import os

class TestSnippetManager(unittest.TestCase):

    def setUp(self):
        # Setup a temporary directory for testing
        self.test_dir = 'test_snippets'
        os.makedirs(self.test_dir, exist_ok=True)
        self.snippet_manager = SnippetManager(snippet_directory=self.test_dir)

    def tearDown(self):
        # Clean up the test directory after each test
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.test_dir)

    def test_store_text_snippets(self):
        # Test saving a valid snippet
        self.snippet_manager.save_snippet('test_tag', 'print("Hello, World!")', 'A simple print statement')
        snippets = self.snippet_manager.list_snippets()
        self.assertIn('test_tag', snippets)

        # Test saving an empty snippet
        with self.assertRaises(ValueError):
            self.snippet_manager.save_snippet('empty_tag', '', '')

    def test_categorize_snippets_based_on_tags(self):
        # This functionality is not directly supported by the current codebase
        self.fail("Categorize snippets based on tags functionality not implemented")

    def test_add_descriptions_to_improve_searchability(self):
        # Test adding a description to a snippet
        self.snippet_manager.save_snippet('desc_tag', 'print("Hello, World!")', 'A simple print statement')
        snippet_data = self.snippet_manager.retrieve_snippet('desc_tag')
        self.assertEqual(snippet_data['description'], 'A simple print statement')

        # Test saving a description that is too long
        long_description = 'x' * 1001  # Assuming 1000 is the limit
        with self.assertRaises(ValueError):
            self.snippet_manager.save_snippet('long_desc_tag', 'print("Hello, World!")', long_description)

    def test_support_text_formatting_for_readability(self):
        # This functionality is not directly supported by the current codebase
        self.fail("Support text formatting for readability functionality not implemented")

    def test_support_syntax_highlighting(self):
        # This functionality is not directly supported by the current codebase
        self.fail("Support syntax highlighting functionality not implemented")

if __name__ == '__main__':
    unittest.main()
