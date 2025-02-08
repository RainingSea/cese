import unittest
import os
from knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):

    def setUp(self):
        # Create a KnowledgeManager instance
        self.manager = KnowledgeManager()
        # Ensure test files are clean before each test
        for category in self.manager.file_paths.values():
            with open(category, 'w') as file:
                file.truncate(0)

    def test_add_knowledge(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        self.manager.add_knowledge("theories", "Test Theory", "This is a test theory.")
        self.manager.add_knowledge("concepts", "Test Concept", "This is a test concept.")
        self.manager.add_knowledge("experiments", "Test Experiment", "This is a test experiment.")

        # Verify the entries were added
        theories = self.manager.retrieve_knowledge("theories")
        concepts = self.manager.retrieve_knowledge("concepts")
        experiments = self.manager.retrieve_knowledge("experiments")

        self.assertIn("Test Theory|This is a test theory.", theories)
        self.assertIn("Test Concept|This is a test concept.", concepts)
        self.assertIn("Test Experiment|This is a test experiment.", experiments)

    def test_retrieve_knowledge(self):
        # Functionality 2: Easy Access and Retrieval of Knowledge
        self.manager.add_knowledge("theories", "Test Theory", "This is a test theory.")
        self.manager.add_knowledge("concepts", "Test Concept", "This is a test concept.")

        # Retrieve and verify
        theories = self.manager.retrieve_knowledge("theories")
        concepts = self.manager.retrieve_knowledge("concepts")

        self.assertEqual(theories, ["Test Theory|This is a test theory."])
        self.assertEqual(concepts, ["Test Concept|This is a test concept."])

    def test_update_knowledge(self):
        # Functionality 3: Update and Add New Knowledge Over Time
        self.manager.add_knowledge("theories", "Test Theory", "This is a test theory.")
        self.manager.update_knowledge("theories", "Test Theory", "This is an updated test theory.")

        # Verify the update
        theories = self.manager.retrieve_knowledge("theories")
        self.assertEqual(theories, ["Test Theory|This is an updated test theory."])

        # Add new knowledge and verify
        self.manager.add_knowledge("theories", "New Theory", "This is a new theory.")
        theories = self.manager.retrieve_knowledge("theories")
        self.assertIn("New Theory|This is a new theory.", theories)

    def tearDown(self):
        # Clean up test files after each test
        for category in self.manager.file_paths.values():
            if os.path.exists(category):
                os.remove(category)

if __name__ == '__main__':
    unittest.main()
