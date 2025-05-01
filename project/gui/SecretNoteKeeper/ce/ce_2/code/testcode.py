import unittest
from NotebookManager import NotebookManager
from Note import Note

class TestNotebookManager(unittest.TestCase):

    def setUp(self):
        self.manager = NotebookManager()

    def test_create_and_delete_notebook(self):
        # Functionality 1: Securely Store and Manage Private Notes within Categorized Notebooks
        self.manager.create_notebook("Personal")
        self.assertIn("Personal", self.manager.notebooks)

        self.manager.delete_note("Personal")
        self.assertNotIn("Personal", self.manager.notebooks)

    def test_add_and_delete_note(self):
        # Functionality 3: Add, Edit, and Delete Notes within Each Notebook
        self.manager.create_notebook("Work")
        self.manager.add_note("Meeting Notes", "Discuss project updates")
        self.assertEqual(len(self.manager.notebooks), 1)  # One note added

        self.manager.edit_note("Meeting Notes", "Updated Meeting Notes")
        self.assertEqual(self.manager.notebooks[0].title, "Updated Meeting Notes")

        self.manager.delete_note("Updated Meeting Notes")
        self.assertEqual(len(self.manager.notebooks), 0)  # Note deleted

    def test_encryption_feature(self):
        # Functionality 2: Provide Encryption Features to Protect the Notes
        self.manager.create_notebook("Personal")
        self.manager.add_note("Secret Recipe", "Chocolate Cake Recipe")
        note = self.manager.notebooks[0]

        encrypted_content = note.encrypt_content()
        self.assertNotEqual(note.content, encrypted_content)  # Ensure content is encrypted

        with self.assertRaises(Exception):
            note.decrypt_content("wrong_encrypted_content")  # Attempt to decrypt with wrong key

    def test_search_and_sort_notes(self):
        # Functionality 4: Support Search and Sorting for Easy Retrieval of Specific Notes
        self.manager.create_notebook("Personal")
        self.manager.add_note("Note A", "Content A")
        self.manager.add_note("Note B", "Content B")
        self.manager.add_note("Note C", "Content C")

        search_results = self.manager.search_notes("Note B")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "Note B")

        sorted_notes = self.manager.sort_notes()
        self.assertEqual([note.title for note in sorted_notes], ["Note A", "Note B", "Note C"])

if __name__ == '__main__':
    unittest.main()
