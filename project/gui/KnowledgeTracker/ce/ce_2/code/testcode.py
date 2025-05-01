import unittest
import os
from main import Main

class TestKnowledgeTracker(unittest.TestCase):

    def setUp(self):
        self.app = Main()
        self.app.knowledge_manager = self.app.knowledge_manager  # Access the knowledge manager directly for testing

    def test_add_knowledge(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        # Test adding a theory
        self.app.type_var.set("theory")
        self.app.content_var.set("Test Theory")
        self.app.add_knowledge()
        self.assertTrue(self._check_file_contains("theories.txt", "Test Theory"))

        # Test adding a concept
        self.app.type_var.set("concept")
        self.app.content_var.set("Test Concept")
        self.app.add_knowledge()
        self.assertTrue(self._check_file_contains("concepts.txt", "Test Concept"))

        # Test adding an experiment
        self.app.type_var.set("experiment")
        self.app.content_var.set("Test Experiment")
        self.app.add_knowledge()
        self.assertTrue(self._check_file_contains("experiments.txt", "Test Experiment"))

    def test_retrieve_knowledge(self):
        # Functionality 2: Easy Access and Retrieval of Knowledge
        # Test retrieving theories
        self.app.type_var.set("theory")
        theories = self.app.knowledge_manager.retrieve_knowledge("theory")
        self.assertIn("Test Theory", theories)

        # Test retrieving concepts
        self.app.type_var.set("concept")
        concepts = self.app.knowledge_manager.retrieve_knowledge("concept")
        self.assertIn("Test Concept", concepts)

        # Test retrieving experiments
        self.app.type_var.set("experiment")
        experiments = self.app.knowledge_manager.retrieve_knowledge("experiment")
        self.assertIn("Test Experiment", experiments)

    def test_update_knowledge(self):
        # Functionality 3: Update and Add New Knowledge Over Time
        # Test updating a theory
        self.app.type_var.set("theory")
        self.app.content_var.set("Updated Test Theory")
        self.app.knowledge_manager.update_knowledge("theory", "Test Theory", "Updated Test Theory")
        theories = self.app.knowledge_manager.retrieve_knowledge("theory")
        self.assertIn("Updated Test Theory", theories)
        self.assertNotIn("Test Theory", theories)

        # Test adding a new theory
        self.app.content_var.set("New Test Theory")
        self.app.add_knowledge()
        theories = self.app.knowledge_manager.retrieve_knowledge("theory")
        self.assertIn("New Test Theory", theories)

    def _check_file_contains(self, file_path, content):
        """Helper method to check if a file contains specific content."""
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as file:
            return content in file.read()

if __name__ == '__main__':
    unittest.main()
