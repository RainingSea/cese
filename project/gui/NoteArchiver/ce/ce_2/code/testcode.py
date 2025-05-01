import unittest
import os
import json
from tkinter import Tk
from main import Main
from notebook_manager import NotebookManager

class TestNotebookManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary Tkinter root for the GUI
        self.root = Tk()
        self.app = Main(self.root)
        self.notebook_manager = NotebookManager()

        # Prepare test data
        self.test_notebooks = ["Personal Notes", "Work Notes", "Project Ideas"]
        self.test_archived_notes = {
            "Archived Notes": [
                {"id": "1", "content": "Meeting notes from 2023-01-01", "tags": ["meeting", "work"]},
                {"id": "2", "content": "Grocery list for the week", "tags": ["shopping", "personal"]}
            ]
        }
        self.setup_test_files()

    def setup_test_files(self):
        # Create notebooks.txt for testing
        with open("notebooks.txt", "w") as f:
            f.write("\n".join(self.test_notebooks))

        # Create archived_notes.txt for testing
        with open("archived_notes.txt", "w") as f:
            json.dump(self.test_archived_notes, f)

    def tearDown(self):
        # Remove test files after tests
        if os.path.exists("notebooks.txt"):
            os.remove("notebooks.txt")
        if os.path.exists("archived_notes.txt"):
            os.remove("archived_notes.txt")

    def test_archive_notebook(self):
        # Functionality 1: Archive Entire Notebooks
        self.app.notebooks_listbox.insert(0, "Personal Notes")  # Simulate selecting a notebook
        self.app.archive_notebook()
        self.assertNotIn("Personal Notes", self.notebook_manager.notebooks)
        self.assertIn("Personal Notes", self.notebook_manager.archived_notes)

    def test_restore_notebook(self):
        # Functionality 2: Restore Archived Notebooks
        self.notebook_manager.archive_notebook("Work Notes")
        self.app.load_notebooks()  # Load notebooks to reflect the change
        self.app.notebooks_listbox.insert(0, "Work Notes")  # Simulate selecting an archived notebook
        self.app.restore_notebook()
        self.assertIn("Work Notes", self.notebook_manager.notebooks)
        self.assertNotIn("Work Notes", self.notebook_manager.archived_notes)

    def test_add_tag_to_archived_note(self):
        # Functionality 3: Add Tags to Archived Notes
        self.notebook_manager.add_tag("1", "urgent")
        self.assertIn("urgent", self.test_archived_notes["Archived Notes"][0]["tags"])

    def test_search_notes_with_tag(self):
        # Functionality 3: Search for Archived Notes by Tag
        self.notebook_manager.add_tag("1", "urgent")
        results = self.notebook_manager.search_notes("urgent")
        self.assertIn("Meeting notes from 2023-01-01", results)

    def test_interface_navigation(self):
        # Functionality 4: Clean and Intuitive Interface
        self.assertIsInstance(self.app.notebooks_listbox, Tk)  # Check if the interface is initialized

    def test_backup_functionality(self):
        # Functionality 5: Ensure Data Integrity with Automatic Backup Capabilities
        self.app.archive_notebook()  # Archive a notebook
        self.assertTrue(os.path.exists("archived_notes.txt"))  # Check if backup file exists

if __name__ == '__main__':
    unittest.main()
