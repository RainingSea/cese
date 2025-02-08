import unittest
from secret_note_keeper import SecretNoteKeeper
from notebook import Notebook

class TestSecretNoteKeeper(unittest.TestCase):

    def setUp(self):
        self.note_keeper = SecretNoteKeeper()
        self.note_keeper.notebooks['Personal'] = Notebook()
        self.note_keeper.notebooks['Work'] = Notebook()

    def test_securely_store_and_manage_private_notes(self):
        # Step: Create a new notebook named "Personal".
        # Expectation: The notebook "Personal" is created successfully and appears in the list of notebooks.
        self.note_keeper.notebooks['Personal'] = Notebook()
        self.assertIn('Personal', self.note_keeper.notebooks)

        # Step: Add a note titled "Grocery List" to the "Personal" notebook.
        # Expectation: The note "Grocery List" is added successfully and is visible within the "Personal" notebook.
        self.note_keeper.add_note('Personal', 'Grocery List')
        self.assertIn('Grocery List', self.note_keeper.notebooks['Personal'].notes)

        # Step: Delete the "Personal" notebook.
        # Expectation: The notebook "Personal" is deleted successfully and no longer appears in the list of notebooks.
        del self.note_keeper.notebooks['Personal']
        self.assertNotIn('Personal', self.note_keeper.notebooks)

    def test_provide_encryption_features(self):
        # Step: Add a note titled "Secret Recipe" to the "Personal" notebook with encryption enabled.
        # Expectation: The note "Secret Recipe" is stored securely and cannot be accessed without the correct decryption key.
        self.fail("Encryption feature not implemented")

        # Step: Attempt to view the "Secret Recipe" note without the decryption key.
        # Expectation: Access is denied, and an error message is displayed indicating that the note is encrypted.
        self.fail("Encryption feature not implemented")

    def test_add_edit_delete_notes(self):
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook.
        # Expectation: The note "Meeting Notes" is added successfully and is visible within the "Work" notebook.
        self.note_keeper.add_note('Work', 'Meeting Notes')
        self.assertIn('Meeting Notes', self.note_keeper.notebooks['Work'].notes)

        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes".
        # Expectation: The note title is updated successfully, and "Updated Meeting Notes" is visible in the "Work" notebook.
        self.note_keeper.edit_note('Work', 0, 'Updated Meeting Notes')
        self.assertIn('Updated Meeting Notes', self.note_keeper.notebooks['Work'].notes)

        # Step: Delete the "Updated Meeting Notes".
        # Expectation: The note "Updated Meeting Notes" is deleted successfully and no longer appears in the "Work" notebook.
        self.note_keeper.delete_note('Work', 0)
        self.assertNotIn('Updated Meeting Notes', self.note_keeper.notebooks['Work'].notes)

    def test_search_and_sort_notes(self):
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook.
        # Expectation: All notes are added successfully and are visible in the "Personal" notebook.
        self.note_keeper.add_note('Personal', 'Note A')
        self.note_keeper.add_note('Personal', 'Note B')
        self.note_keeper.add_note('Personal', 'Note C')
        self.assertIn('Note A', self.note_keeper.notebooks['Personal'].notes)
        self.assertIn('Note B', self.note_keeper.notebooks['Personal'].notes)
        self.assertIn('Note C', self.note_keeper.notebooks['Personal'].notes)

        # Step: Use the search feature to find "Note B".
        # Expectation: The search results display "Note B" correctly, while "Note A" and "Note C" are not shown.
        search_results = self.note_keeper.search_notes('Personal', 'Note B')
        self.assertEqual(search_results, ['Note B'])

        # Step: Sort the notes in the "Personal" notebook alphabetically.
        # Expectation: The notes are displayed in alphabetical order, with "Note A", "Note B", and "Note C" arranged accordingly.
        sorted_notes = self.note_keeper.sort_notes('Personal', 'alphabetical')
        self.assertEqual(sorted_notes, ['Note A', 'Note B', 'Note C'])

if __name__ == '__main__':
    unittest.main()
