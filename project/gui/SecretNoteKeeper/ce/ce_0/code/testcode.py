import unittest
import json
import os
from main import Main

class TestSecretNoteKeeper(unittest.TestCase):

    def setUp(self):
        # Initialize the Main application
        self.app = Main()
        self.notebooks_file = 'notebooks.json'
        self.personal_notes_file = 'personal_notes.json'
        self.work_notes_file = 'work_notes.json'

    def test_create_delete_notebook(self):
        # Functionality 1: Securely Store and Manage Private Notes within Categorized Notebooks
        # Step: Create a new notebook named "Personal".
        self.app.create_notebook("Personal")
        with open(self.notebooks_file, 'r') as f:
            notebooks = json.load(f)
        self.assertIn("Personal", notebooks['notebooks'])

        # Step: Delete the "Personal" notebook.
        self.app.delete_notebook("Personal")
        with open(self.notebooks_file, 'r') as f:
            notebooks = json.load(f)
        self.assertNotIn("Personal", notebooks['notebooks'])

    def test_encryption_features(self):
        # Functionality 2: Provide Encryption Features to Protect the Notes
        # Step: Add a note titled "Secret Recipe" to the "Personal" notebook with encryption enabled.
        # This functionality is not implemented in the codebase.
        self.fail("Encryption feature for notes not implemented.")

        # Step: Attempt to view the "Secret Recipe" note without the decryption key.
        # This functionality is not implemented in the codebase.
        self.fail("Access control for encrypted notes not implemented.")

    def test_add_edit_delete_notes(self):
        # Functionality 3: Add, Edit, and Delete Notes within Each Notebook
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook.
        self.app.create_notebook("Work")
        self.app.add_note_to_work("Meeting Notes")  # Assuming this method exists
        self.assertIn("Meeting Notes", self.load_notes(self.work_notes_file))

        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes".
        self.app.edit_note_in_work("Meeting Notes", "Updated Meeting Notes")  # Assuming this method exists
        self.assertIn("Updated Meeting Notes", self.load_notes(self.work_notes_file))

        # Step: Delete the "Updated Meeting Notes".
        self.app.delete_note_in_work("Updated Meeting Notes")  # Assuming this method exists
        self.assertNotIn("Updated Meeting Notes", self.load_notes(self.work_notes_file))

    def test_search_sort_notes(self):
        # Functionality 4: Support Search and Sorting for Easy Retrieval of Specific Notes
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook.
        self.app.create_notebook("Personal")
        self.app.add_note_to_personal("Note A")  # Assuming this method exists
        self.app.add_note_to_personal("Note B")  # Assuming this method exists
        self.app.add_note_to_personal("Note C")  # Assuming this method exists
        notes = self.load_notes(self.personal_notes_file)
        self.assertIn("Note A", notes)
        self.assertIn("Note B", notes)
        self.assertIn("Note C", notes)

        # Step: Use the search feature to find "Note B".
        search_results = self.app.search_notes("Note B")  # Assuming this method exists
        self.assertIn("Note B", search_results)
        self.assertNotIn("Note A", search_results)
        self.assertNotIn("Note C", search_results)

        # Step: Sort the notes in the "Personal" notebook alphabetically.
        sorted_notes = self.app.sort_notes()  # Assuming this method exists
        self.assertEqual(sorted_notes, ["Note A", "Note B", "Note C"])

    def load_notes(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

if __name__ == '__main__':
    unittest.main()
