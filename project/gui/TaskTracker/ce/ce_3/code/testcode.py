import unittest
from TaskManager import TaskManager
from Task import Task

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_create_organize_manage_tasks(self):
        # Functionalities 1: Create, Organize, and Manage Tasks
        task = Task("Test Task", "Test Description", "2023-12-01", "High", "Incomplete")
        self.task_manager.add_task(task)
        self.assertIn(task, self.task_manager.get_tasks(), "Task should be added to the task list.")

        # Update task
        updated_task = Task("Updated Task", "Updated Description", "2023-12-02", "Medium", "Incomplete")
        self.task_manager.update_task(0, updated_task)
        self.assertEqual(self.task_manager.get_tasks()[0].title, "Updated Task", "Task title should be updated.")

    def test_set_deadlines_and_assign_priority(self):
        # Functionalities 2: Set Deadlines and Assign Priority Levels
        task = Task("Deadline Task", "Description", "2023-12-01", "High", "Incomplete")
        self.task_manager.add_task(task)
        self.assertEqual(self.task_manager.get_tasks()[0].due_date, "2023-12-01", "Task deadline should be set correctly.")
        self.assertEqual(self.task_manager.get_tasks()[0].priority, "High", "Task priority should be set correctly.")

        # Test for past date (not implemented in the codebase, so we simulate a failure)
        self.fail("Past date validation not implemented")

    def test_track_progress_of_tasks(self):
        # Functionalities 3: Track Progress of Tasks
        task = Task("Progress Task", "Description", "2023-12-01", "High", "Incomplete")
        self.task_manager.add_task(task)
        task.status = "In Progress"
        self.assertEqual(self.task_manager.get_tasks()[0].status, "In Progress", "Task status should be updated to In Progress.")

        task.status = "Complete"
        self.assertEqual(self.task_manager.get_tasks()[0].status, "Complete", "Task status should be updated to Complete.")

    def test_task_categorization(self):
        # Functionalities 4: Task Categorization
        self.fail("Task categorization not implemented")

    def test_search_for_specific_tasks(self):
        # Functionalities 5: Search for Specific Tasks
        task1 = Task("Searchable Task", "Description", "2023-12-01", "High", "Incomplete")
        task2 = Task("Another Task", "Description", "2023-12-02", "Medium", "Incomplete")
        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)

        results = self.task_manager.search_tasks("Searchable")
        self.assertIn(task1, results, "Task with matching keyword should be found.")

        results = self.task_manager.search_tasks("Nonexistent")
        self.assertEqual(len(results), 0, "No tasks should be found with a non-matching keyword.")

if __name__ == '__main__':
    unittest.main()
