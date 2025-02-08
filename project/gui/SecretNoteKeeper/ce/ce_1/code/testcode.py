import unittest
import os
import json
from notebooks.note_keeper import NoteKeeper
from notebooks.notebook import Notebook

class TestNoteKeeper(unittest.TestCase):

    def setUp(self):
        # Set up a fresh NoteKeeper instance for each test
        self.note_keeper = NoteKeeper()

    def tearDown(self):
        # Clean up any created files
        if os.path.exists('notebooks/Personal.json'):
            os.remove('notebooks/Personal.json')
        if os.path.exists('notebooks/Work.json'):
            os.remove('notebooks/Work.json')
        if os.path.exists('notebooks/notebooks_list.json'):
            os.remove('notebooks/notebooks_list.json')

    def test_securely_store_and_manage_private_notes(self):
        # Step: Create a new notebook named "Personal"
        self.note_keeper.create_notebook("Personal")
        self.assertIn("Personal", self.note_keeper.notebooks)

        # Step: Add a note titled "Grocery List" to the "Personal" notebook
        personal_notebook = self.note_keeper.get_notebook("Personal")
        personal_notebook.add_note("Grocery List", "Buy milk and eggs")
        self.assertEqual(len(personal_notebook.notes), 1)
        self.assertEqual(personal_notebook.notes[0].title, "Grocery List")

        # Step: Delete the "Personal" notebook
        self.note_keeper.delete_notebook("Personal")
        self.assertNotIn("Personal", self.note_keeper.notebooks)

    def test_encryption_features(self):
        # Encryption features are not implemented in the codebase
        self.fail("Encryption features are not implemented")

    def test_add_edit_delete_notes(self):
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook
        self.note_keeper.create_notebook("Work")
        work_notebook = self.note_keeper.get_notebook("Work")
        work_notebook.add_note("Meeting Notes", "Discuss project timeline")
        self.assertEqual(len(work_notebook.notes), 1)
        self.assertEqual(work_notebook.notes[0].title, "Meeting Notes")

        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes"
        work_notebook.edit_note(work_notebook.notes[0], "Updated Meeting Notes", "Discuss project timeline")
        self.assertEqual(work_notebook.notes[0].title, "Updated Meeting Notes")

        # Step: Delete the "Updated Meeting Notes"
        work_notebook.delete_note(work_notebook.notes[0])
        self.assertEqual(len(work_notebook.notes), 0)

    def test_search_and_sort_notes(self):
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook
        self.note_keeper.create_notebook("Personal")
        personal_notebook = self.note_keeper.get_notebook("Personal")
        personal_notebook.add_note("Note A", "Content A")
        personal_notebook.add_note("Note B", "Content B")
        personal_notebook.add_note("Note C", "Content C")
        self.assertEqual(len(personal_notebook.notes), 3)

        # Step: Use the search feature to find "Note B"
        search_results = personal_notebook.search_notes("Note B")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "Note B")

        # Step: Sort the notes in the "Personal" notebook alphabetically
        sorted_notes = personal_notebook.sort_notes("title")
        self.assertEqual([note.title for note in sorted_notes], ["Note A", "Note B", "Note C"])

if __name__ == '__main__':
    unittest.main()
