import unittest
import os
from knowledge_tracker import KnowledgeTracker

class TestKnowledgeTracker(unittest.TestCase):

    def setUp(self):
        self.knowledge_tracker = KnowledgeTracker()
        # Clear the files before each test
        self._clear_files()

    def _clear_files(self):
        for filename in ['theories.txt', 'concepts.txt', 'experiments.txt']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_input_and_categorize_scientific_knowledge(self):
        # Functionality 1: Input and Categorize Scientific Knowledge
        self.knowledge_tracker.add_theory("Theory of Relativity")
        self.assertIn("Theory of Relativity", self.knowledge_tracker.retrieve_theories())

        self.knowledge_tracker.add_concept("Gravity")
        self.assertIn("Gravity", self.knowledge_tracker.retrieve_concepts())

        self.knowledge_tracker.add_experiment("Double-Slit Experiment")
        self.assertIn("Double-Slit Experiment", self.knowledge_tracker.retrieve_experiments())

    def test_easy_access_and_retrieval_of_knowledge(self):
        # Functionality 2: Easy Access and Retrieval of Knowledge
        self.knowledge_tracker.add_theory("Theory of Relativity")
        self.knowledge_tracker.add_concept("Gravity")
        self.knowledge_tracker.add_experiment("Double-Slit Experiment")

        theories = self.knowledge_tracker.retrieve_theories()
        self.assertEqual(theories, ["Theory of Relativity"])

        concepts = self.knowledge_tracker.retrieve_concepts()
        self.assertEqual(concepts, ["Gravity"])

        experiments = self.knowledge_tracker.retrieve_experiments()
        self.assertEqual(experiments, ["Double-Slit Experiment"])

    def test_update_and_add_new_knowledge_over_time(self):
        # Functionality 3: Update and Add New Knowledge Over Time
        self.knowledge_tracker.add_theory("Theory of Relativity")
        self.knowledge_tracker.update_theory(0, "Updated Theory of Relativity")
        self.assertIn("Updated Theory of Relativity", self.knowledge_tracker.retrieve_theories())

        self.knowledge_tracker.add_theory("Quantum Mechanics")
        self.assertIn("Quantum Mechanics", self.knowledge_tracker.retrieve_theories())

        theories = self.knowledge_tracker.retrieve_theories()
        self.assertEqual(theories, ["Updated Theory of Relativity", "Quantum Mechanics"])

if __name__ == '__main__':
    unittest.main()
