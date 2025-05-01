import unittest
from tkinter import Tk
from main import Main
from task_manager import TaskManager

class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = Main(self.root)

    def test_create_and_manage_tasks(self):
        # Functionality 1: Create, Organize, and Manage Tasks
        self.app.add_task()  # Simulate adding a task
        self.app.task_manager.add_task("Test Task", "Description", "2023-10-10", "High", "Incomplete", "Work")
        self.assertEqual(len(self.app.task_manager.get_tasks()), 1)

        # Edit the task
        self.app.task_manager.edit_task(0, "Updated Task", "Updated Description", "2023-10-11", "Medium", "Incomplete", "Personal")
        updated_task = self.app.task_manager.get_tasks()[0]
        self.assertEqual(updated_task['title'], "Updated Task")
        self.assertEqual(updated_task['description'], "Updated Description")

    def test_set_deadlines_and_priority_levels(self):
        # Functionality 2: Set Deadlines and Assign Priority Levels
        self.app.task_manager.add_task("Deadline Task", "Description", "2023-10-10", "High", "Incomplete", "Work")
        task = self.app.task_manager.get_tasks()[0]
        self.assertEqual(task['deadline'], "2023-10-10")
        self.assertEqual(task['priority'], "High")

        # Attempt to set a past deadline (not implemented in the codebase)
        self.fail("Deadline cannot be in the past - functionality not implemented")

    def test_track_progress_of_tasks(self):
        # Functionality 3: Track Progress of Tasks
        self.app.task_manager.add_task("Progress Task", "Description", "2023-10-10", "High", "Incomplete", "Work")
        self.app.task_manager.edit_task(0, "Progress Task", "Description", "2023-10-10", "High", "In Progress", "Work")
        task = self.app.task_manager.get_tasks()[0]
        self.assertEqual(task['status'], "In Progress")

        # Mark as complete
        self.app.task_manager.edit_task(0, "Progress Task", "Description", "2023-10-10", "High", "Complete", "Work")
        task = self.app.task_manager.get_tasks()[0]
        self.assertEqual(task['status'], "Complete")

    def test_task_categorization(self):
        # Functionality 4: Task Categorization
        self.app.task_manager.add_task("Categorized Task", "Description", "2023-10-10", "High", "Incomplete", "Work")
        task = self.app.task_manager.get_tasks()[0]
        self.assertEqual(task['category'], "Work")

        # Filter tasks by category (not implemented in the codebase)
        self.fail("Filtering tasks by category - functionality not implemented")

    def test_search_for_specific_tasks(self):
        # Functionality 5: Search for Specific Tasks
        self.app.task_manager.add_task("Search Task", "Description", "2023-10-10", "High", "Incomplete", "Work")
        search_results = self.app.task_manager.search_tasks("Search")
        self.assertEqual(len(search_results), 1)

        # Search for a non-existing task
        search_results = self.app.task_manager.search_tasks("Non-existing Task")
        self.assertEqual(len(search_results), 0)

if __name__ == '__main__':
    unittest.main()
