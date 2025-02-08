import unittest
from snippet_manager import SnippetManager
from snippet import Snippet

class TestSnippetManager(unittest.TestCase):

    def setUp(self):
        self.snippet_manager = SnippetManager()

    def test_store_text_snippets(self):
        # Test saving a valid snippet
        self.snippet_manager.add_snippet("Sample snippet", ["tag1"], "Sample description")
        self.assertEqual(len(self.snippet_manager.snippets), 1)
        self.assertEqual(self.snippet_manager.snippets[0].text, "Sample snippet")

        # Test saving an empty snippet
        with self.assertRaises(ValueError):
            self.snippet_manager.add_snippet("", [], "")

    def test_categorize_snippets_based_on_tags(self):
        # Test adding tags to a snippet
        self.snippet_manager.add_snippet("Sample snippet", ["tag1"], "Sample description")
        snippet = self.snippet_manager.snippets[0]
        snippet.tags.append("new_tag")
        self.assertIn("new_tag", snippet.tags)

        # Test adding a tag that exceeds the character limit
        with self.assertRaises(ValueError):
            snippet.tags.append("a" * 101)  # Assuming 100 is the character limit

    def test_add_descriptions_to_improve_searchability(self):
        # Test adding a description to a snippet
        self.snippet_manager.add_snippet("Sample snippet", ["tag1"], "Sample description")
        snippet = self.snippet_manager.snippets[0]
        snippet.description = "New description"
        self.assertEqual(snippet.description, "New description")

        # Test saving a description that is too long
        with self.assertRaises(ValueError):
            snippet.description = "a" * 501  # Assuming 500 is the character limit

    def test_support_text_formatting_for_readability(self):
        # This functionality is not implemented in the codebase
        self.fail("Text formatting functionality not implemented")

    def test_support_syntax_highlighting(self):
        # This functionality is not implemented in the codebase
        self.fail("Syntax highlighting functionality not implemented")

if __name__ == '__main__':
    unittest.main()
