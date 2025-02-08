import unittest
from task_manager import TaskManager
from tasks import Task

class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_create_organize_manage_tasks(self):
        # Test adding a new task
        new_task = Task("New Task", "Description", "2023-12-31", "High")
        self.task_manager.add_task(new_task)
        self.assertIn(new_task, self.task_manager.tasks)

        # Test updating an existing task
        updated_task = Task("New Task", "Updated Description", "2023-12-31", "Medium")
        self.task_manager.update_task(updated_task)
        self.assertEqual(self.task_manager.tasks[0].description, "Updated Description")
        self.assertEqual(self.task_manager.tasks[0].priority, "Medium")

    def test_set_deadlines_and_assign_priority_levels(self):
        # Test adding a task with deadline and priority
        task_with_deadline = Task("Deadline Task", "Description", "2023-12-31", "Low")
        self.task_manager.add_task(task_with_deadline)
        self.assertEqual(self.task_manager.tasks[-1].due_date, "2023-12-31")
        self.assertEqual(self.task_manager.tasks[-1].priority, "Low")

        # Test changing deadline to a past date (not implemented in codebase)
        self.fail("Changing deadline to a past date is not implemented")

    def test_track_progress_of_tasks(self):
        # Test marking a task as in progress
        task_in_progress = Task("Progress Task", "Description", "2023-12-31", "High")
        self.task_manager.add_task(task_in_progress)
        task_in_progress.mark_complete()
        self.assertEqual(task_in_progress.status, "complete")

    def test_task_categorization(self):
        # Test assigning a category to a task (not implemented in codebase)
        self.fail("Task categorization is not implemented")

    def test_search_for_specific_tasks(self):
        # Test searching for a task
        search_result = self.task_manager.search_tasks("Task 1")
        self.assertTrue(any(task.title == "Task 1" for task in search_result))

        # Test searching for a non-existent task
        search_result = self.task_manager.search_tasks("Non-existent Task")
        self.assertEqual(len(search_result), 0)

if __name__ == '__main__':
    unittest.main()
