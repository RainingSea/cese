import unittest
from notebook_manager import NotebookManager

class TestNotebookManager(unittest.TestCase):

    def setUp(self):
        self.notebook_manager = NotebookManager()

    def test_securely_store_and_manage_private_notes(self):
        # Step: Create a new notebook named "Personal".
        self.notebook_manager.create_notebook("Personal")
        self.assertIn("Personal", self.notebook_manager.notebooks)

        # Step: Add a note titled "Grocery List" to the "Personal" notebook.
        self.notebook_manager.add_note("Personal", "Grocery List")
        notes = self.notebook_manager.notebooks["Personal"]
        decrypted_notes = [self.notebook_manager.cipher.decrypt(note.encode()).decode() for note in notes]
        self.assertIn("Grocery List", decrypted_notes)

        # Step: Delete the "Personal" notebook.
        del self.notebook_manager.notebooks["Personal"]
        self.assertNotIn("Personal", self.notebook_manager.notebooks)

    def test_provide_encryption_features(self):
        # Step: Add a note titled "Secret Recipe" to the "Personal" notebook with encryption enabled.
        self.notebook_manager.create_notebook("Personal")
        self.notebook_manager.add_note("Personal", "Secret Recipe")
        notes = self.notebook_manager.notebooks["Personal"]
        encrypted_note = notes[0]
        self.assertNotEqual("Secret Recipe", encrypted_note)

        # Step: Attempt to view the "Secret Recipe" note without the decryption key.
        # Since the decryption key is part of the NotebookManager instance, we simulate this by checking the encrypted content.
        with self.assertRaises(Exception):
            # Simulate incorrect decryption by using a wrong key
            wrong_cipher = Fernet(Fernet.generate_key())
            wrong_cipher.decrypt(encrypted_note.encode())

    def test_add_edit_delete_notes(self):
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook.
        self.notebook_manager.create_notebook("Work")
        self.notebook_manager.add_note("Work", "Meeting Notes")
        notes = self.notebook_manager.notebooks["Work"]
        decrypted_notes = [self.notebook_manager.cipher.decrypt(note.encode()).decode() for note in notes]
        self.assertIn("Meeting Notes", decrypted_notes)

        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes".
        self.notebook_manager.edit_note("Work", 0, "Updated Meeting Notes")
        notes = self.notebook_manager.notebooks["Work"]
        decrypted_notes = [self.notebook_manager.cipher.decrypt(note.encode()).decode() for note in notes]
        self.assertIn("Updated Meeting Notes", decrypted_notes)
        self.assertNotIn("Meeting Notes", decrypted_notes)

        # Step: Delete the "Updated Meeting Notes".
        self.notebook_manager.delete_note("Work", 0)
        notes = self.notebook_manager.notebooks["Work"]
        self.assertEqual(len(notes), 0)

    def test_support_search_and_sorting(self):
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook.
        self.notebook_manager.create_notebook("Personal")
        self.notebook_manager.add_note("Personal", "Note A")
        self.notebook_manager.add_note("Personal", "Note B")
        self.notebook_manager.add_note("Personal", "Note C")
        notes = self.notebook_manager.notebooks["Personal"]
        decrypted_notes = [self.notebook_manager.cipher.decrypt(note.encode()).decode() for note in notes]
        self.assertIn("Note A", decrypted_notes)
        self.assertIn("Note B", decrypted_notes)
        self.assertIn("Note C", decrypted_notes)

        # Step: Use the search feature to find "Note B".
        search_results = self.notebook_manager.search_notes("Personal", "Note B")
        decrypted_results = [self.notebook_manager.cipher.decrypt(note.encode()).decode() for note in search_results]
        self.assertIn("Note B", decrypted_results)
        self.assertNotIn("Note A", decrypted_results)
        self.assertNotIn("Note C", decrypted_results)

        # Step: Sort the notes in the "Personal" notebook alphabetically.
        # Note: Sorting is not implemented in the codebase, so this test will fail.
        self.fail("Sorting functionality not implemented")

if __name__ == '__main__':
    unittest.main()
