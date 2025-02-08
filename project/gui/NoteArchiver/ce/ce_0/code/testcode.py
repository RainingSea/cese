import unittest
import os
from ArchiveManager import ArchiveManager

class TestArchiveManager(unittest.TestCase):

    def setUp(self):
        # Setup a test instance of ArchiveManager with a test file
        self.test_notes_file = 'test_archived_notes.txt'
        self.test_tags_file = 'test_tags.txt'
        self.archive_manager = ArchiveManager(notes_file=self.test_notes_file, tags_file=self.test_tags_file)
        # Create test files
        with open(self.test_notes_file, 'w') as nf:
            nf.write("Test Note|This is a test note|test\n")
        with open(self.test_tags_file, 'w') as tf:
            tf.write("test\n")

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_notes_file):
            os.remove(self.test_notes_file)
        if os.path.exists(self.test_tags_file):
            os.remove(self.test_tags_file)
        if os.path.exists(self.test_notes_file + '.bak'):
            os.remove(self.test_notes_file + '.bak')
        if os.path.exists(self.test_tags_file + '.bak'):
            os.remove(self.test_tags_file + '.bak')

    def test_archive_note(self):
        # Functionality 1: Archive Entire Notebooks or Specific Notes
        self.archive_manager.archive_note("New Note", "Content of new note", ["new", "note"])
        with open(self.test_notes_file, 'r') as nf:
            notes = nf.readlines()
        self.assertIn("New Note|Content of new note|new,note\n", notes)

    def test_restore_note(self):
        # Functionality 2: Securely Store Archived Notes and Allow Easy Access or Restoration
        restored_note = self.archive_manager.restore_note("Test Note")
        self.assertEqual(restored_note, "Test Note|This is a test note|test")

    def test_add_tag(self):
        # Functionality 3: Add Tags or Labels to Archived Notes
        self.archive_manager.add_tag("Test Note", "newtag")
        with open(self.test_notes_file, 'r') as nf:
            notes = nf.readlines()
        self.assertIn("Test Note|This is a test note|test,newtag\n", notes)

    def test_search_notes(self):
        # Functionality 3: Search for archived notes using the added tag
        self.archive_manager.add_tag("Test Note", "searchtag")
        found_notes = self.archive_manager.search_notes("searchtag")
        self.assertIn("Test Note|This is a test note|test,searchtag", found_notes)

    def test_backup_data(self):
        # Functionality 5: Ensure Data Integrity with Automatic Backup Capabilities
        self.archive_manager.backup_data()
        self.assertTrue(os.path.exists(self.test_notes_file + '.bak'))
        self.assertTrue(os.path.exists(self.test_tags_file + '.bak'))

if __name__ == '__main__':
    unittest.main()
