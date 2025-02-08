import unittest
from knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):

    def setUp(self):
        self.knowledge_manager = KnowledgeManager()
        # Clear the files before each test
        for category in self.knowledge_manager.file_paths:
            with open(self.knowledge_manager.file_paths[category], 'w') as file:
                file.write('')

    def test_add_knowledge(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        self.knowledge_manager.add_knowledge('theories', 'Test Theory')
        self.knowledge_manager.add_knowledge('concepts', 'Test Concept')
        self.knowledge_manager.add_knowledge('experiments', 'Test Experiment')

        self.assertIn('Test Theory', self.knowledge_manager.view_knowledge('theories'))
        self.assertIn('Test Concept', self.knowledge_manager.view_knowledge('concepts'))
        self.assertIn('Test Experiment', self.knowledge_manager.view_knowledge('experiments'))

    def test_view_knowledge(self):
        # Functionality 2: Easy Access and Retrieval of Knowledge
        self.knowledge_manager.add_knowledge('theories', 'Test Theory')
        
        theories = self.knowledge_manager.view_knowledge('theories')
        self.assertIn('Test Theory', theories)

        # Simulate searching for a specific concept (not implemented in the codebase)
        self.fail("Search functionality not implemented")

    def test_update_knowledge(self):
        # Functionality 3: Update and Add New Knowledge Over Time
        self.knowledge_manager.add_knowledge('theories', 'Old Theory')
        self.knowledge_manager.update_knowledge('theories', 'Old Theory', 'Updated Theory')

        theories = self.knowledge_manager.view_knowledge('theories')
        self.assertNotIn('Old Theory', theories)
        self.assertIn('Updated Theory', theories)

        # Add a new theory and verify both are present
        self.knowledge_manager.add_knowledge('theories', 'New Theory')
        theories = self.knowledge_manager.view_knowledge('theories')
        self.assertIn('Updated Theory', theories)
        self.assertIn('New Theory', theories)

if __name__ == '__main__':
    unittest.main()
