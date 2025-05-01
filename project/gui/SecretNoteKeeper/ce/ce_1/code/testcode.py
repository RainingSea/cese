import unittest
import os
from notebook_manager import NotebookManager
from note import Note
from search_engine import SearchEngine

class TestSecretNoteKeeper(unittest.TestCase):

    def setUp(self):
        self.notebook_manager = NotebookManager()
        self.search_engine = SearchEngine()
        self.test_notebook_name = "Personal"
        self.test_note_title = "Grocery List"
        self.test_note_content = "Buy milk and eggs."

    def test_create_and_delete_notebook(self):
        # Functionality 1: Securely Store and Manage Private Notes within Categorized Notebooks
        self.notebook_manager.create_notebook(self.test_notebook_name)
        self.assertIn(self.test_notebook_name, self.notebook_manager.load_notebooks())

        # Add a note to the notebook
        self.notebook_manager.load_notebook(self.test_notebook_name).append(Note(self.test_note_title, self.test_note_content))

        # Verify the note is added
        notes = self.notebook_manager.load_notebook(self.test_notebook_name)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, self.test_note_title)

        # Delete the notebook
        self.notebook_manager.delete_notebook(self.test_notebook_name)
        self.assertNotIn(self.test_notebook_name, self.notebook_manager.load_notebooks())

    def test_encryption_feature(self):
        # Functionality 2: Provide Encryption Features to Protect the Notes
        self.notebook_manager.create_notebook(self.test_notebook_name)
        secret_note = Note("Secret Recipe", "This is a secret recipe.")
        encrypted_content = secret_note.encrypt_content()

        # Simulate storing the encrypted note
        self.notebook_manager.load_notebook(self.test_notebook_name).append(secret_note)

        # Attempt to view the note without decryption
        with self.assertRaises(Exception):
            secret_note.decrypt_content()  # This should raise an error because we are not using the correct key

    def test_add_edit_delete_notes(self):
        # Functionality 3: Add, Edit, and Delete Notes within Each Notebook
        self.notebook_manager.create_notebook("Work")
        work_note = Note("Meeting Notes", "Discuss project updates.")
        self.notebook_manager.load_notebook("Work").append(work_note)

        # Verify the note is added
        notes = self.notebook_manager.load_notebook("Work")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, "Meeting Notes")

        # Edit the note
        notes[0].title = "Updated Meeting Notes"

        # Verify the note title is updated
        self.assertEqual(notes[0].title, "Updated Meeting Notes")

        # Delete the note
        self.notebook_manager.load_notebook("Work").remove(notes[0])
        self.assertEqual(len(self.notebook_manager.load_notebook("Work")), 0)

    def test_search_and_sort_notes(self):
        # Functionality 4: Support Search and Sorting for Easy Retrieval of Specific Notes
        self.notebook_manager.create_notebook("Personal")
        self.notebook_manager.load_notebook("Personal").append(Note("Note A", "Content A"))
        self.notebook_manager.load_notebook("Personal").append(Note("Note B", "Content B"))
        self.notebook_manager.load_notebook("Personal").append(Note("Note C", "Content C"))

        # Search for "Note B"
        results = self.search_engine.search("Note B", self.notebook_manager.load_notebook("Personal"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Note B")

        # Check that other notes are not in the results
        self.assertNotIn("Note A", [note.title for note in results])
        self.assertNotIn("Note C", [note.title for note in results])

        # Sort notes (this part is not implemented in the original code, so we will fail this test)
        self.fail("Sorting functionality not implemented.")

if __name__ == '__main__':
    unittest.main()
