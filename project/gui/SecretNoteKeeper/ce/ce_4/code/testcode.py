import unittest
from encryption import EncryptionManager
from notebook import Notebook
from note import Note
import os

class TestNoteKeeperApp(unittest.TestCase):

    def setUp(self):
        # Setup for encryption
        self.encryption_manager = EncryptionManager(b'YOUR_KEY_HERE')
        
        # Setup for notebooks
        self.personal_notebook = Notebook("Personal")
        self.work_notebook = Notebook("Work")

    def test_securely_store_and_manage_private_notes(self):
        # Step: Create a new notebook named "Personal"
        self.personal_notebook = Notebook("Personal")
        self.assertEqual(self.personal_notebook.name, "Personal")
        
        # Step: Add a note titled "Grocery List" to the "Personal" notebook
        grocery_note = Note("Grocery List", "Buy milk and eggs")
        self.personal_notebook.add_note(grocery_note)
        self.assertIn(grocery_note, self.personal_notebook.notes)
        
        # Step: Delete the "Personal" notebook
        del self.personal_notebook
        self.assertFalse(os.path.exists("Personal.json"))

    def test_provide_encryption_features(self):
        # Step: Add a note titled "Secret Recipe" to the "Personal" notebook with encryption enabled
        secret_note = Note("Secret Recipe", "Top secret ingredients")
        encrypted_content = self.encryption_manager.encrypt_data(secret_note.content)
        secret_note.content = encrypted_content
        self.personal_notebook.add_note(secret_note)
        
        # Verify encryption
        self.assertNotEqual(secret_note.content, "Top secret ingredients")
        
        # Step: Attempt to view the "Secret Recipe" note without the decryption key
        with self.assertRaises(Exception):
            decrypted_content = self.encryption_manager.decrypt_data(secret_note.content)

    def test_add_edit_delete_notes(self):
        # Step: Add a note titled "Meeting Notes" to the "Work" notebook
        meeting_note = Note("Meeting Notes", "Discuss project timeline")
        self.work_notebook.add_note(meeting_note)
        self.assertIn(meeting_note, self.work_notebook.notes)
        
        # Step: Edit the "Meeting Notes" to change the title to "Updated Meeting Notes"
        self.work_notebook.edit_note("Meeting Notes", "Updated project timeline")
        self.assertEqual(self.work_notebook.notes[0].content, "Updated project timeline")
        
        # Step: Delete the "Updated Meeting Notes"
        self.work_notebook.delete_note("Meeting Notes")
        self.assertNotIn(meeting_note, self.work_notebook.notes)

    def test_support_search_and_sorting(self):
        # Step: Add multiple notes with titles "Note A", "Note B", and "Note C" to the "Personal" notebook
        note_a = Note("Note A", "Content A")
        note_b = Note("Note B", "Content B")
        note_c = Note("Note C", "Content C")
        self.personal_notebook.add_note(note_a)
        self.personal_notebook.add_note(note_b)
        self.personal_notebook.add_note(note_c)
        
        # Verify all notes are added
        self.assertIn(note_a, self.personal_notebook.notes)
        self.assertIn(note_b, self.personal_notebook.notes)
        self.assertIn(note_c, self.personal_notebook.notes)
        
        # Step: Use the search feature to find "Note B"
        search_results = self.personal_notebook.search_notes("Note B")
        self.assertIn(note_b, search_results)
        self.assertNotIn(note_a, search_results)
        self.assertNotIn(note_c, search_results)
        
        # Step: Sort the notes in the "Personal" notebook alphabetically
        sorted_notes = self.personal_notebook.sort_notes(by='title')
        self.assertEqual(sorted_notes, [note_a, note_b, note_c])

if __name__ == '__main__':
    unittest.main()
