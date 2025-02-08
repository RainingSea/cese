import unittest
from article_manager import ArticleManager
from search_engine import SearchEngine
import json
import os

class TestScienceLibrary(unittest.TestCase):

    def setUp(self):
        # Setup for ArticleManager
        self.article_manager = ArticleManager()
        self.article_manager.load_articles()

        # Setup for SearchEngine
        self.search_engine = SearchEngine()

        # Ensure favorites.json is reset
        with open('favorites.json', 'w') as file:
            json.dump([], file)

    def test_search_for_articles(self):
        # Functionalities 1: Search for Scientific Articles and Journals
        results = self.search_engine.search("quantum physics")
        self.assertTrue(any("Quantum Mechanics" in article['title'] for article in results))

    def test_access_scientific_articles(self):
        # Functionalities 2: Access Scientific Articles and Journals
        results = self.search_engine.search("quantum physics")
        if results:
            article = results[0]
            self.assertIn("Quantum mechanics is a fundamental theory in physics.", article['content'])
        else:
            self.fail("No articles found for valid search query.")

    def test_categorize_research_papers(self):
        # Functionalities 3: Categorize Research Papers by Fields of Study
        results = self.search_engine.search("Biology")
        self.assertTrue(all("Biology" in article['title'] or "Biology" in article['content'] for article in results))

    def test_save_favorite_articles(self):
        # Functionalities 5: Save Favorite Articles
        self.article_manager.save_favorites("1")
        with open('favorites.json', 'r') as file:
            favorites = json.load(file)
        self.assertIn("1", favorites)

    def test_view_favorites_list(self):
        # Functionalities 5: View the Favorites list
        self.article_manager.save_favorites("1")
        with open('favorites.json', 'r') as file:
            favorites = json.load(file)
        self.assertEqual(favorites, ["1"])

    def test_create_annotations(self):
        # Functionalities 7: Create Annotations on Articles
        self.article_manager.create_annotation("1", "Important note on quantum mechanics.")
        with open('annotations.json', 'r') as file:
            annotations = json.load(file)
        self.assertIn("Important note on quantum mechanics.", annotations.get("1", []))

    def test_edit_annotations(self):
        # Functionalities 7: Edit an existing annotation
        self.article_manager.create_annotation("1", "Initial note.")
        self.article_manager.create_annotation("1", "Updated note.")
        with open('annotations.json', 'r') as file:
            annotations = json.load(file)
        self.assertIn("Updated note.", annotations.get("1", []))

    def test_delete_annotations(self):
        # Functionalities 7: Delete an annotation
        self.article_manager.create_annotation("1", "Temporary note.")
        self.article_manager.annotations["1"].remove("Temporary note.")
        with open('annotations.json', 'w') as file:
            json.dump(self.article_manager.annotations, file)
        with open('annotations.json', 'r') as file:
            annotations = json.load(file)
        self.assertNotIn("Temporary note.", annotations.get("1", []))

if __name__ == '__main__':
    unittest.main()
