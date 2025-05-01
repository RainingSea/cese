import unittest
import os
import json
from main import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []  # Clear existing tasks for testing

    def test_add_task(self):
        # Functionality 1: Create, Organize, and Manage Tasks
        self.task_manager.add_task("Test Task", "This is a test task", "2023-10-30", "High", "Work")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, "Test Task")

        # Edit Task
        self.task_manager.edit_task(1, "Updated Task", "Updated description", "2023-10-31", "Medium", "Personal")
        self.assertEqual(self.task_manager.tasks[0].title, "Updated Task")

    def test_set_deadline_and_priority(self):
        # Functionality 2: Set Deadlines and Assign Priority Levels
        self.task_manager.add_task("Deadline Task", "Task with deadline", "2023-10-30", "High", "Work")
        self.assertEqual(self.task_manager.tasks[0].deadline, "2023-10-30")
        self.assertEqual(self.task_manager.tasks[0].priority, "High")

        # Attempt to set a past deadline (not implemented in the codebase)
        self.fail("Deadline cannot be set to a past date - functionality not implemented")

    def test_track_progress_of_tasks(self):
        # Functionality 3: Track Progress of Tasks
        self.fail("Task progress tracking not implemented in the codebase")

    def test_task_categorization(self):
        # Functionality 4: Task Categorization
        self.task_manager.add_task("Categorized Task", "Task with category", "2023-10-30", "High", "Urgent")
        self.assertEqual(self.task_manager.tasks[0].category, "Urgent")

        # Filter tasks by category (not implemented in the codebase)
        self.fail("Task filtering by category not implemented in the codebase")

    def test_search_for_specific_tasks(self):
        # Functionality 5: Search for Specific Tasks
        self.task_manager.add_task("Searchable Task", "This task can be searched", "2023-10-30", "High", "Work")
        results = self.task_manager.search_tasks("Searchable")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Searchable Task")

        # Search for a non-existing task
        results = self.task_manager.search_tasks("Non-existing Task")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
