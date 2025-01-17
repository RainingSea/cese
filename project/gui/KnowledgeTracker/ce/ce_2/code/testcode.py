import unittest
import os
import json
from knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):

    def setUp(self):
        # Setup a temporary file for testing
        self.test_file = 'test_knowledge.json'
        with open(self.test_file, 'w') as f:
            json.dump([], f)
        self.manager = KnowledgeManager(self.test_file)

    def tearDown(self):
        # Clean up the temporary file after tests
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_input_and_categorize_scientific_knowledge(self):
        # Test adding a theory
        theory = {
            "title": "Theory of Relativity",
            "category": "Theory",
            "content": "A theory developed by Albert Einstein."
        }
        self.manager.save_knowledge(theory)
        self.assertEqual(len(self.manager.knowledge_list), 1)
        self.assertEqual(self.manager.knowledge_list[0].to_dict(), theory)

        # Test adding a concept
        concept = {
            "title": "Quantum Mechanics",
            "category": "Concept",
            "content": "A fundamental theory in physics."
        }
        self.manager.save_knowledge(concept)
        self.assertEqual(len(self.manager.knowledge_list), 2)
        self.assertEqual(self.manager.knowledge_list[1].to_dict(), concept)

        # Test adding an experiment
        experiment = {
            "title": "Double-slit Experiment",
            "category": "Experiment",
            "content": "A demonstration that light and matter can display characteristics of both waves and particles."
        }
        self.manager.save_knowledge(experiment)
        self.assertEqual(len(self.manager.knowledge_list), 3)
        self.assertEqual(self.manager.knowledge_list[2].to_dict(), experiment)

    def test_easy_access_and_retrieval_of_knowledge(self):
        # Prepopulate with some knowledge
        self.manager.save_knowledge({
            "title": "Theory of Relativity",
            "category": "Theory",
            "content": "A theory developed by Albert Einstein."
        })
        self.manager.save_knowledge({
            "title": "Quantum Mechanics",
            "category": "Concept",
            "content": "A fundamental theory in physics."
        })

        # Test retrieval by category
        theories = [k.to_dict() for k in self.manager.knowledge_list if k.category == "Theory"]
        self.assertEqual(len(theories), 1)
        self.assertEqual(theories[0]['title'], "Theory of Relativity")

        # Test retrieval by title
        concepts = [k.to_dict() for k in self.manager.knowledge_list if k.title == "Quantum Mechanics"]
        self.assertEqual(len(concepts), 1)
        self.assertEqual(concepts[0]['content'], "A fundamental theory in physics.")

    def test_update_and_add_new_knowledge_over_time(self):
        # Add initial knowledge
        self.manager.save_knowledge({
            "title": "Theory of Relativity",
            "category": "Theory",
            "content": "A theory developed by Albert Einstein."
        })

        # Update existing knowledge
        updated_theory = {
            "title": "Theory of Relativity",
            "category": "Theory",
            "content": "Updated content about relativity."
        }
        self.manager.update_knowledge(0, updated_theory)
        self.assertEqual(self.manager.knowledge_list[0].to_dict(), updated_theory)

        # Add new knowledge
        new_theory = {
            "title": "String Theory",
            "category": "Theory",
            "content": "A theoretical framework in which the point-like particles are replaced by one-dimensional objects called strings."
        }
        self.manager.save_knowledge(new_theory)
        self.assertEqual(len(self.manager.knowledge_list), 2)
        self.assertEqual(self.manager.knowledge_list[1].to_dict(), new_theory)

        # Verify both updated and new knowledge
        self.assertEqual(self.manager.knowledge_list[0].content, "Updated content about relativity.")
        self.assertEqual(self.manager.knowledge_list[1].title, "String Theory")

if __name__ == '__main__':
    unittest.main()
