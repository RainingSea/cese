import unittest
import os
from knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):

    def setUp(self):
        self.km = KnowledgeManager()
        self.test_data = {
            'theories': 'Test Theory',
            'concepts': 'Test Concept',
            'experiments': 'Test Experiment'
        }
        # Clear existing data files for testing
        for file_name in self.km.data_storage.file_map.values():
            open(file_name, 'w').close()

    def test_add_and_retrieve_knowledge(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        # Add a theory
        self.km.add_knowledge('theories', self.test_data['theories'])
        self.assertIn(self.test_data['theories'], self.km.retrieve_knowledge('theories'))

        # Add a concept
        self.km.add_knowledge('concepts', self.test_data['concepts'])
        self.assertIn(self.test_data['concepts'], self.km.retrieve_knowledge('concepts'))

        # Add an experiment
        self.km.add_knowledge('experiments', self.test_data['experiments'])
        self.assertIn(self.test_data['experiments'], self.km.retrieve_knowledge('experiments'))

    def test_update_knowledge(self):
        # Functionality 3: Update and Add New Knowledge Over Time
        # Add a theory to update
        self.km.add_knowledge('theories', self.test_data['theories'])
        updated_theory = 'Updated Test Theory'
        
        # Update the theory
        self.km.update_knowledge('theories', self.test_data['theories'], updated_theory)
        self.assertIn(updated_theory, self.km.retrieve_knowledge('theories'))
        self.assertNotIn(self.test_data['theories'], self.km.retrieve_knowledge('theories'))

        # Add a new theory
        new_theory = 'New Test Theory'
        self.km.add_knowledge('theories', new_theory)
        self.assertIn(new_theory, self.km.retrieve_knowledge('theories'))

    def test_invalid_type_handling(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        with self.assertRaises(ValueError):
            self.km.add_knowledge('invalid_type', 'Some Knowledge')

        with self.assertRaises(ValueError):
            self.km.retrieve_knowledge('invalid_type')

        with self.assertRaises(ValueError):
            self.km.update_knowledge('invalid_type', 'Old Knowledge', 'New Knowledge')

if __name__ == '__main__':
    unittest.main()
