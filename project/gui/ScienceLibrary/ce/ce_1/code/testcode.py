import unittest
import json
from main import Article, SearchEngine, Favorites, Annotations

class TestArticleManager(unittest.TestCase):

    def setUp(self):
        # Load articles from the JSON file for testing
        with open('articles.json', 'r') as file:
            articles_data = json.load(file)
            self.articles = [Article(**data) for data in articles_data]
        self.search_engine = SearchEngine(self.articles)
        self.favorites = Favorites()
        self.annotations = Annotations()

    def test_search_articles(self):
        # Functionalities 1: Search for Scientific Articles and Journals
        results = self.search_engine.search("Python")
        self.assertGreater(len(results), 0, "Expected to find articles related to 'Python'")
        
        results = self.search_engine.search("quantum physics")
        self.assertEqual(results, [], "Expected no articles related to 'quantum physics'")

    def test_access_article(self):
        # Functionalities 2: Access Scientific Articles and Journals
        # Since the actual viewing of articles is not implemented, we will simulate this
        article = self.articles[0]  # Access the first article
        self.assertIsNotNone(article, "Expected to access an article without errors")

    def test_favorites(self):
        # Functionalities 5: Save Favorite Articles
        article = self.articles[0]
        self.favorites.add_favorite(article)
        self.assertIn(article, self.favorites.favorite_articles, "Expected article to be in favorites")

        # View the Favorites list
        self.assertEqual(len(self.favorites.favorite_articles), 1, "Expected one favorite article")

        # Remove the favorite
        self.favorites.remove_favorite(article)
        self.assertNotIn(article, self.favorites.favorite_articles, "Expected article to be removed from favorites")

    def test_annotations(self):
        # Functionalities 7: Create Annotations on Articles
        article = self.articles[0]
        self.annotations.add_annotation(article, "Important note")
        self.assertIn("Important note", self.annotations.get_annotations(article), "Expected annotation to be saved")

        # Edit existing annotation
        self.annotations.add_annotation(article, "Updated note")
        self.assertIn("Updated note", self.annotations.get_annotations(article), "Expected updated annotation to be saved")

        # Delete an annotation
        self.annotations.article_annotations[article].remove("Important note")
        self.assertNotIn("Important note", self.annotations.get_annotations(article), "Expected annotation to be removed")

    def test_categorization(self):
        # Functionalities 3: Categorize Research Papers by Fields of Study
        self.fail("not implemented")  # This functionality is not implemented in the codebase

    def test_sorting(self):
        # Functionalities 4: Sort Research Papers Using Various Criteria
        self.fail("not implemented")  # This functionality is not implemented in the codebase

    def test_organize_saved_articles(self):
        # Functionalities 6: Organize Saved Articles
        self.fail("not implemented")  # This functionality is not implemented in the codebase

if __name__ == '__main__':
    unittest.main()
