import unittest
import json
import os
from main import Task, TaskManager, UI

class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        # Clear the tasks.json file before each test
        self.tasks_file = 'tasks.json'
        if os.path.exists(self.tasks_file):
            os.remove(self.tasks_file)
        self.task_manager = TaskManager()

    def test_create_and_manage_tasks(self):
        # Functionality 1: Create, Organize, and Manage Tasks
        task = Task("Test Task", "This is a test task", "2023-12-31", "High")
        self.task_manager.add_task(task)
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, "Test Task")

        # Edit Task
        task.edit_task(title="Updated Task", description="Updated description")
        self.assertEqual(self.task_manager.tasks[0].title, "Updated Task")
        self.assertEqual(self.task_manager.tasks[0].description, "Updated description")

    def test_set_deadlines_and_priority_levels(self):
        # Functionality 2: Set Deadlines and Assign Priority Levels
        task = Task("Deadline Task", "Task with deadline", "2023-12-31", "High")
        self.task_manager.add_task(task)
        self.assertEqual(self.task_manager.tasks[0].deadline, "2023-12-31")
        self.assertEqual(self.task_manager.tasks[0].priority, "High")

        # Attempt to set a past deadline (not implemented in the codebase)
        self.fail("Setting a past deadline should raise an error (not implemented)")

    def test_track_progress_of_tasks(self):
        # Functionality 3: Track Progress of Tasks
        task = Task("Progress Task", "Task to track progress", "2023-12-31", "Medium")
        self.task_manager.add_task(task)
        task.update_status("In Progress")
        self.assertEqual(self.task_manager.tasks[0].status, "In Progress")

        task.update_status("Complete")
        self.assertEqual(self.task_manager.tasks[0].status, "Complete")

    def test_task_categorization(self):
        # Functionality 4: Task Categorization
        task = Task("Categorized Task", "Task with category", "2023-12-31", "Low", category="Work")
        self.task_manager.add_task(task)
        self.assertEqual(self.task_manager.tasks[0].category, "Work")

        # Filter tasks by category (not implemented in the codebase)
        self.fail("Filtering tasks by category should be implemented (not implemented)")

    def test_search_for_specific_tasks(self):
        # Functionality 5: Search for Specific Tasks
        task1 = Task("Search Task 1", "First task", "2023-12-31", "High")
        task2 = Task("Search Task 2", "Second task", "2023-12-31", "Medium")
        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)

        # Search for a task that exists
        search_results = self.task_manager.search_tasks("Search Task 1")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].title, "Search Task 1")

        # Search for a task that does not exist
        search_results = self.task_manager.search_tasks("Nonexistent Task")
        self.assertEqual(len(search_results), 0)

if __name__ == '__main__':
    unittest.main()
