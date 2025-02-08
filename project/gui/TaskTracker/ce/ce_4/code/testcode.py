import unittest
from Task import Task
from TaskManager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_create_and_manage_tasks(self):
        # Functionalities 1: Create, Organize, and Manage Tasks
        task = Task("Test Task", "Test Description", "2023-12-31", "Medium")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.tasks)

        # Update task
        updated_task = Task("Updated Task", "Updated Description", "2023-12-31", "High")
        self.task_manager.update_task(0, updated_task)
        self.assertEqual(self.task_manager.tasks[0].title, "Updated Task")
        self.assertEqual(self.task_manager.tasks[0].description, "Updated Description")

    def test_set_deadlines_and_priority(self):
        # Functionalities 2: Set Deadlines and Assign Priority Levels
        task = Task("Deadline Task", "Description", "2023-12-31", "High")
        self.task_manager.add_task(task)
        self.assertEqual(self.task_manager.tasks[0].due_date, "2023-12-31")
        self.assertEqual(self.task_manager.tasks[0].priority, "High")

        # Test for past deadline (not implemented in codebase)
        self.fail("Test for past deadline not implemented in codebase")

    def test_track_progress_of_tasks(self):
        # Functionalities 3: Track Progress of Tasks
        task = Task("Progress Task", "Description", "2023-12-31", "Medium")
        self.task_manager.add_task(task)

        # Mark task as complete
        self.task_manager.mark_task_complete(0)
        self.assertEqual(self.task_manager.tasks[0].status, "Complete")

        # Test for "In Progress" status (not implemented in codebase)
        self.fail("Test for 'In Progress' status not implemented in codebase")

    def test_task_categorization(self):
        # Functionalities 4: Task Categorization
        self.fail("Task categorization not implemented in codebase")

    def test_search_for_specific_tasks(self):
        # Functionalities 5: Search for Specific Tasks
        task1 = Task("Search Task 1", "Description", "2023-12-31", "Medium")
        task2 = Task("Another Task", "Description", "2023-12-31", "Low")
        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)

        results = self.task_manager.search_tasks("Search")
        self.assertIn(task1, results)
        self.assertNotIn(task2, results)

        results = self.task_manager.search_tasks("Nonexistent")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
