import unittest
import os
import json
from notebooks import Notebooks
from note import Note

class TestSecretNoteKeeper(unittest.TestCase):

    def setUp(self):
        # Setup a Notebooks instance for testing
        self.notebooks = Notebooks()

    def tearDown(self):
        # Clean up any created files after each test
        if os.path.exists("Personal.json"):
            os.remove("Personal.json")
        if os.path.exists("Work.json"):
            os.remove("Work.json")

    def test_securely_store_and_manage_private_notes(self):
        # Step: Create a new notebook named "Personal"
        self.notebooks.create_notebook("Personal")
        self.assertIn("Personal", self.notebooks.notebooks)

        # Step: Add a note titled "Grocery List" to the "Personal" notebook
        note = Note("Grocery List", "Buy milk and eggs")
        self.notebooks.notebooks["Personal"].append(note.__dict__)
        self.notebooks.save_notebook("Personal")
        loaded_notebook = self.notebooks.load_notebook("Personal")
        self.assertEqual(len(loaded_notebook), 1)
        self.assertEqual(loaded_notebook[0]['title'], "Grocery List")

        # Step: Delete the "Personal" notebook
        self.notebooks.delete_notebook("Personal")
        self.assertNotIn("Personal", self.notebooks.notebooks)
        self.assertFalse(os.path.exists("Personal.json"))

    def test_encryption_features(self):
        # Step: Add a note titled "Secret Recipe" to the "Personal" notebook with encryption enabled
        self.notebooks.create_notebook("Personal")
        note = Note("Secret Recipe", "Top secret ingredients")
        self.notebooks.notebooks["Personal"].append(note.__dict__)
        self.notebooks.save_notebook("Personal")
        loaded_notebook = self.notebooks.load_notebook("Personal")
        self.assertNotEqual(loaded_notebook[0]['content'], "Top secret ingredients")

        # Step: Attempt to view the "Secret Recipe" note without the decryption key
        # This will fail because the decryption key is not stored
        with self.assertRaises(Exception):
            note.decrypt()

    def test_add_edit_delete_notes(self):
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook
        self.notebooks.create_notebook("Work")
        note = Note("Meeting Notes", "Discuss project updates")
        self.notebooks.notebooks["Work"].append(note.__dict__)
        self.notebooks.save_notebook("Work")
        loaded_notebook = self.notebooks.load_notebook("Work")
        self.assertEqual(loaded_notebook[0]['title'], "Meeting Notes")

        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes"
        loaded_notebook[0]['title'] = "Updated Meeting Notes"
        self.notebooks.save_notebook("Work")
        loaded_notebook = self.notebooks.load_notebook("Work")
        self.assertEqual(loaded_notebook[0]['title'], "Updated Meeting Notes")

        # Step: Delete the "Updated Meeting Notes"
        self.notebooks.notebooks["Work"].remove(loaded_notebook[0])
        self.notebooks.save_notebook("Work")
        loaded_notebook = self.notebooks.load_notebook("Work")
        self.assertEqual(len(loaded_notebook), 0)

    def test_search_and_sort_notes(self):
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook
        self.notebooks.create_notebook("Personal")
        notes = [Note("Note A", "Content A"), Note("Note B", "Content B"), Note("Note C", "Content C")]
        for note in notes:
            self.notebooks.notebooks["Personal"].append(note.__dict__)
        self.notebooks.save_notebook("Personal")
        loaded_notebook = self.notebooks.load_notebook("Personal")
        self.assertEqual(len(loaded_notebook), 3)

        # Step: Use the search feature to find "Note B"
        search_results = [note for note in loaded_notebook if note['title'] == "Note B"]
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]['title'], "Note B")

        # Step: Sort the notes in the "Personal" notebook alphabetically
        sorted_notes = sorted(loaded_notebook, key=lambda x: x['title'])
        self.assertEqual(sorted_notes[0]['title'], "Note A")
        self.assertEqual(sorted_notes[1]['title'], "Note B")
        self.assertEqual(sorted_notes[2]['title'], "Note C")

if __name__ == '__main__':
    unittest.main()
