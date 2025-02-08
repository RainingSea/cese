import unittest
from ArticleManager import ArticleManager
from SearchEngine import SearchEngine
import os
import json

class TestScienceLibrary(unittest.TestCase):

    def setUp(self):
        # Setup for ArticleManager and SearchEngine
        self.article_manager = ArticleManager()
        self.article_manager.load_articles('articles.json')
        self.search_engine = SearchEngine()

    def test_search_for_scientific_articles(self):
        # Functionalities 1: Search for Scientific Articles and Journals
        results = self.search_engine.search("quantum physics")
        self.assertTrue(any("Quantum Physics" in article['title'] for article in results))

    def test_access_scientific_articles(self):
        # Functionalities 2: Access Scientific Articles and Journals
        results = self.search_engine.search("quantum physics")
        if results:
            article = results[0]
            self.assertIn("Quantum physics is a fundamental theory", article['content'])
        else:
            self.fail("No articles found for the search term.")

    def test_categorize_research_papers(self):
        # Functionalities 3: Categorize Research Papers by Fields of Study
        biology_articles = [article for article in self.article_manager.articles if article.category == "Biology"]
        self.assertTrue(all(article.category == "Biology" for article in biology_articles))

    def test_save_favorite_articles(self):
        # Functionalities 5: Save Favorite Articles
        self.article_manager.save_favorite("1")
        favorites = self.article_manager.get_favorites()
        self.assertIn("1", favorites)

    def test_view_favorites_list(self):
        # Functionalities 5: View the Favorites list
        self.article_manager.save_favorite("1")
        favorites = self.article_manager.get_favorites()
        self.assertIn("1", favorites)

    def test_create_annotations_on_articles(self):
        # Functionalities 7: Create Annotations on Articles
        self.article_manager.add_annotation("1", "Important section")
        annotations = self.article_manager.get_annotations()
        self.assertIn("Important section", annotations.get("1", []))

    def test_edit_annotation(self):
        # Functionalities 7: Edit an existing annotation
        self.article_manager.add_annotation("1", "Important section")
        self.article_manager.add_annotation("1", "Updated section")
        annotations = self.article_manager.get_annotations()
        self.assertIn("Updated section", annotations.get("1", []))

    def test_delete_annotation(self):
        # Functionalities 7: Delete an annotation
        self.article_manager.add_annotation("1", "Important section")
        annotations = self.article_manager.get_annotations()
        annotations["1"].remove("Important section")
        with open('annotations.json', 'w') as file:
            json.dump(annotations, file)
        annotations = self.article_manager.get_annotations()
        self.assertNotIn("Important section", annotations.get("1", []))

    def tearDown(self):
        # Clean up any changes made during tests
        if os.path.exists('favorites.json'):
            os.remove('favorites.json')
        if os.path.exists('annotations.json'):
            os.remove('annotations.json')

if __name__ == '__main__':
    unittest.main()
