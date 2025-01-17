import unittest
import os
from main import Note, NoteArchiver

class TestNoteArchiver(unittest.TestCase):

    def setUp(self):
        # Setup a temporary directory for testing
        self.test_dir = "test_archived_notes"
        os.makedirs(self.test_dir, exist_ok=True)
        self.archiver = NoteArchiver(self.test_dir)

    def tearDown(self):
        # Clean up the test directory after tests
        for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.test_dir)

    def test_archive_notebook(self):
        # Functionality 1: Archive Entire Notebooks
        note1 = Note("Meeting notes", ["work", "2023", "important"])
        note2 = Note("Grocery list", ["personal", "shopping"])
        self.archiver.archived_notes.extend([note1, note2])
        
        result = self.archiver.archive_notebook("test_notebook")
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test_notebook.txt")))

    def test_archive_specific_note(self):
        # Functionality 1: Archive Specific Notes
        note1 = Note("Meeting notes", ["work", "2023", "important"])
        self.archiver.archived_notes.append(note1)
        
        result = self.archiver.archive_note("test_notebook", "Meeting notes")
        self.assertTrue(result)
        with open(os.path.join(self.test_dir, "test_notebook.txt"), 'r') as file:
            content = file.read()
            self.assertIn("Meeting notes|work|2023|important", content)

    def test_restore_note(self):
        # Functionality 2: Restore Notes
        note1 = Note("Meeting notes", ["work", "2023", "important"])
        self.archiver.archived_notes.append(note1)
        
        result = self.archiver.restore_note("Meeting notes")
        self.assertTrue(result)
        self.assertNotIn(note1, self.archiver.archived_notes)

    def test_search_notes(self):
        # Functionality 3: Search Notes by Tag
        note1 = Note("Meeting notes", ["work", "2023", "important"])
        note2 = Note("Grocery list", ["personal", "shopping"])
        self.archiver.archived_notes.extend([note1, note2])
        
        results = self.archiver.search_notes("work")
        self.assertIn(note1, results)
        self.assertNotIn(note2, results)

    def test_add_tag_to_note_failure(self):
        # Functionality 3: Add Tags to Archived Notes
        # This functionality is not implemented in the codebase
        self.fail("Add tag functionality not implemented")

    def test_interface_cleanliness(self):
        # Functionality 4: Clean and Intuitive Interface
        # This functionality is related to GUI and cannot be tested with unittest
        self.fail("GUI interface testing not implemented")

    def test_backup_capabilities(self):
        # Functionality 5: Ensure Data Integrity with Automatic Backup
        # This functionality is not implemented in the codebase
        self.fail("Backup functionality not implemented")

if __name__ == '__main__':
    unittest.main()
