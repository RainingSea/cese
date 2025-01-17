import unittest
from article_manager import ArticleManager
from search_engine import SearchEngine
import os

class TestScienceLibrary(unittest.TestCase):

    def setUp(self):
        # Ensure the environment is clean before each test
        self.article_manager = ArticleManager()
        self.search_engine = SearchEngine()
        # Clear favorites and annotations for a clean state
        open('favorites.txt', 'w').close()
        open('annotations.txt', 'w').close()

    def test_search_for_scientific_articles(self):
        # Functionalities 1: Search for Scientific Articles and Journals
        results = self.search_engine.search("quantum physics")
        self.assertIn("Understanding Quantum Physics", results)

    def test_access_scientific_articles(self):
        # Functionalities 2: Access Scientific Articles and Journals
        # This functionality requires GUI interaction, which is not directly testable here.
        self.fail("GUI interaction test not implemented")

    def test_categorize_research_papers(self):
        # Functionalities 3: Categorize Research Papers by Fields of Study
        # This functionality is not implemented in the codebase.
        self.fail("Categorize research papers functionality not implemented")

    def test_sort_research_papers(self):
        # Functionalities 4: Sort Research Papers Using Various Criteria
        # This functionality is not implemented in the codebase.
        self.fail("Sort research papers functionality not implemented")

    def test_save_favorite_articles(self):
        # Functionalities 5: Save Favorite Articles
        self.article_manager.save_favorite("Understanding Quantum Physics")
        favorites = self.article_manager.get_favorites()
        self.assertIn("Understanding Quantum Physics", favorites)

    def test_view_favorites_list(self):
        # Functionalities 5: View the Favorites list
        self.article_manager.save_favorite("The Basics of Machine Learning")
        favorites = self.article_manager.get_favorites()
        self.assertIn("The Basics of Machine Learning", favorites)

    def test_organize_saved_articles(self):
        # Functionalities 6: Organize Saved Articles
        # This functionality is not implemented in the codebase.
        self.fail("Organize saved articles functionality not implemented")

    def test_create_annotations_on_articles(self):
        # Functionalities 7: Create Annotations on Articles
        self.article_manager.add_annotation("Understanding Quantum Physics", "Important concept")
        annotations = self.article_manager.load_annotations()
        self.assertEqual(annotations.get("Understanding Quantum Physics"), "Important concept")

    def test_edit_annotations_on_articles(self):
        # Functionalities 7: Edit an existing annotation
        self.article_manager.add_annotation("Understanding Quantum Physics", "Initial note")
        self.article_manager.add_annotation("Understanding Quantum Physics", "Updated note")
        annotations = self.article_manager.load_annotations()
        self.assertEqual(annotations.get("Understanding Quantum Physics"), "Updated note")

    def test_delete_annotations_on_articles(self):
        # Functionalities 7: Delete an annotation
        self.article_manager.add_annotation("Understanding Quantum Physics", "To be deleted")
        self.article_manager.annotations.pop("Understanding Quantum Physics", None)
        self.article_manager.save_annotations()
        annotations = self.article_manager.load_annotations()
        self.assertNotIn("Understanding Quantum Physics", annotations)

if __name__ == '__main__':
    unittest.main()
