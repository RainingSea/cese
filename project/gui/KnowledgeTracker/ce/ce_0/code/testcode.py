import unittest
import tkinter as tk
from knowledge_manager import KnowledgeManager
from main import Main

class TestKnowledgeTracker(unittest.TestCase):

    def setUp(self):
        # Initialize the application
        self.app = Main()
        self.app.root.update()  # Update the GUI to reflect changes

    def tearDown(self):
        # Destroy the application after each test
        self.app.root.destroy()

    def test_input_and_categorize_scientific_knowledge(self):
        # Test adding a theory
        self.app.input_field.insert(0, "Theory of Relativity")
        self.app.category_var.set("Physics")
        self.app.add_knowledge()
        self.assertIn({'id': 1, 'content': 'Theory of Relativity', 'category': 'Physics'}, self.app.knowledge_manager.retrieve_knowledge())

        # Test adding a concept
        self.app.input_field.insert(0, "Quantum Mechanics")
        self.app.category_var.set("Physics")
        self.app.add_knowledge()
        self.assertIn({'id': 2, 'content': 'Quantum Mechanics', 'category': 'Physics'}, self.app.knowledge_manager.retrieve_knowledge())

        # Test adding an experiment
        self.app.input_field.insert(0, "Double-slit Experiment")
        self.app.category_var.set("Physics")
        self.app.add_knowledge()
        self.assertIn({'id': 3, 'content': 'Double-slit Experiment', 'category': 'Physics'}, self.app.knowledge_manager.retrieve_knowledge())

    def test_easy_access_and_retrieval_of_knowledge(self):
        # Add sample data
        self.app.knowledge_manager.add_knowledge({'id': 1, 'content': 'Theory of Relativity', 'category': 'Physics'})
        self.app.knowledge_manager.add_knowledge({'id': 2, 'content': 'Quantum Mechanics', 'category': 'Physics'})

        # Test retrieving knowledge
        self.app.retrieve_knowledge()
        displayed_text = self.app.text_area.get("1.0", tk.END)
        self.assertIn("Theory of Relativity", displayed_text)
        self.assertIn("Quantum Mechanics", displayed_text)

    def test_update_and_add_new_knowledge_over_time(self):
        # Add initial data
        self.app.knowledge_manager.add_knowledge({'id': 1, 'content': 'Theory of Relativity', 'category': 'Physics'})

        # Update the knowledge
        self.app.input_field.insert(0, "1 Updated Theory of Relativity")
        self.app.category_var.set("Physics")
        self.app.update_knowledge()
        updated_knowledge = self.app.knowledge_manager.retrieve_knowledge()
        self.assertIn({'id': 1, 'content': 'Updated Theory of Relativity', 'category': 'Physics'}, updated_knowledge)

        # Add new knowledge
        self.app.input_field.insert(0, "String Theory")
        self.app.category_var.set("Physics")
        self.app.add_knowledge()
        new_knowledge = self.app.knowledge_manager.retrieve_knowledge()
        self.assertIn({'id': 2, 'content': 'String Theory', 'category': 'Physics'}, new_knowledge)

if __name__ == '__main__':
    unittest.main()
