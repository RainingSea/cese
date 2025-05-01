import unittest
from main import Main
from note_manager import NoteManager
from note import Note
import os

class TestNoteArchiver(unittest.TestCase):

    def setUp(self):
        self.note_manager = NoteManager()
        self.main_app = Main(tk.Tk())
        self.test_note_id = self.note_manager.notes[0].id if self.note_manager.notes else None

    def test_archive_note_success(self):
        # Functionality 1: Archive Entire Notebooks or Specific Notes
        if self.test_note_id:
            self.main_app.archive_note()
            self.assertNotIn(self.test_note_id, [note.id for note in self.note_manager.notes])
            self.assertTrue(os.path.exists('archived_notes.txt'))

    def test_restore_note_success(self):
        # Functionality 2: Securely Store Archived Notes and Allow Easy Access or Restoration
        if self.test_note_id:
            archived_note = self.note_manager.restore(self.test_note_id)
            self.assertIsNotNone(archived_note)
            self.assertIn(self.test_note_id, [note.id for note in self.note_manager.notes])

    def test_add_tag_success(self):
        # Functionality 3: Add Tags or Labels to Archived Notes
        if self.test_note_id:
            self.main_app.add_tag()
            note = self.note_manager.find_note_by_id(self.test_note_id)
            self.assertIn("example_tag", note.tags)

    def test_search_by_tag_success(self):
        # Functionality 3: Search for archived notes using the added tag
        if self.test_note_id:
            self.main_app.search_entry.insert(0, "example_tag")
            self.main_app.search_by_tag()
            notes = self.note_manager.search_by_tag("example_tag")
            self.assertGreater(len(notes), 0)

    def test_interface_display(self):
        # Functionality 4: Clean and Intuitive Interface for Managing Archived Notes
        self.assertIsNotNone(self.main_app.notes_display)

    def test_data_integrity_backup(self):
        # Functionality 5: Ensure Data Integrity with Automatic Backup Capabilities
        self.fail("Backup functionality not implemented")

if __name__ == '__main__':
    unittest.main()
