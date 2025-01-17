import unittest
import os
from knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):

    def setUp(self):
        # Initialize the KnowledgeManager and ensure files are clean before each test
        self.manager = KnowledgeManager()
        for file in self.manager.knowledge_files.values():
            with open(file, 'w') as f:
                f.truncate(0)  # Clear the file contents

    def test_input_and_categorize_scientific_knowledge(self):
        # Functionalities 1: Input and Categorize Scientific Knowledge

        # Add a theory
        self.manager.add_knowledge("Theories", "String Theory: A theoretical framework in which the point-like particles of particle physics are replaced by one-dimensional objects called strings.")
        theories = self.manager.view_knowledge("Theories")
        self.assertIn("String Theory: A theoretical framework in which the point-like particles of particle physics are replaced by one-dimensional objects called strings.\n", theories)

        # Add a concept
        self.manager.add_knowledge("Concepts", "Evolution: The process by which different kinds of living organisms are thought to have developed and diversified from earlier forms during the history of the earth.")
        concepts = self.manager.view_knowledge("Concepts")
        self.assertIn("Evolution: The process by which different kinds of living organisms are thought to have developed and diversified from earlier forms during the history of the earth.\n", concepts)

        # Add an experiment
        self.manager.add_knowledge("Experiments", "Cavendish Experiment: An experiment to measure the force of gravitational attraction between masses.")
        experiments = self.manager.view_knowledge("Experiments")
        self.assertIn("Cavendish Experiment: An experiment to measure the force of gravitational attraction between masses.\n", experiments)

    def test_easy_access_and_retrieval_of_knowledge(self):
        # Functionalities 2: Easy Access and Retrieval of Knowledge

        # Prepopulate some data
        self.manager.add_knowledge("Theories", "Theory of Everything: A hypothetical single, all-encompassing, coherent theoretical framework of physics.")
        
        # View theories
        theories = self.manager.view_knowledge("Theories")
        self.assertIn("Theory of Everything: A hypothetical single, all-encompassing, coherent theoretical framework of physics.\n", theories)

        # Test retrieval of a specific theory
        # Note: The GUI part of clicking and searching is not covered in this test as it requires integration testing with a GUI testing tool.

    def test_update_and_add_new_knowledge_over_time(self):
        # Functionalities 3: Update and Add New Knowledge Over Time

        # Add and update a theory
        self.manager.add_knowledge("Theories", "Old Theory: An outdated theory.")
        self.manager.update_knowledge("Theories", "Old Theory: An outdated theory.", "Updated Theory: A revised version of the theory.")
        theories = self.manager.view_knowledge("Theories")
        self.assertIn("Updated Theory: A revised version of the theory.\n", theories)
        self.assertNotIn("Old Theory: An outdated theory.\n", theories)

        # Add a new theory
        self.manager.add_knowledge("Theories", "New Theory: A newly proposed theory.")
        theories = self.manager.view_knowledge("Theories")
        self.assertIn("New Theory: A newly proposed theory.\n", theories)

if __name__ == '__main__':
    unittest.main()
