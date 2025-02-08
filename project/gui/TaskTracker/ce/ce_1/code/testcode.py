import unittest
from task_manager import TaskManager
from task import Task

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_create_organize_manage_tasks(self):
        # Test adding a task
        initial_task_count = len(self.task_manager.tasks)
        self.task_manager.add_task("New Task", "New Description", "2023-12-01", "Low")
        self.assertEqual(len(self.task_manager.tasks), initial_task_count + 1)
        self.assertEqual(self.task_manager.tasks[-1].title, "New Task")

        # Test updating a task
        task_id = self.task_manager.tasks[-1].id
        self.task_manager.update_task(task_id, "Updated Task", "Updated Description", "2023-12-02", "High")
        updated_task = self.task_manager.tasks[-1]
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated Description")

    def test_set_deadlines_and_assign_priority_levels(self):
        # Test adding a task with deadline and priority
        self.task_manager.add_task("Deadline Task", "Description", "2023-12-10", "Medium")
        task = self.task_manager.tasks[-1]
        self.assertEqual(task.due_date, "2023-12-10")
        self.assertEqual(task.priority, "Medium")

        # Test setting a past deadline (not implemented in codebase)
        # Assuming the application should prevent this, but since it's not implemented,
        # we will just note this as a failure point.
        self.fail("Setting past deadlines not implemented")

    def test_track_progress_of_tasks(self):
        # Test marking a task as complete
        self.task_manager.add_task("Progress Task", "Description", "2023-12-15", "Low")
        task_id = self.task_manager.tasks[-1].id
        self.task_manager.complete_task(task_id)
        self.assertTrue(self.task_manager.tasks[-1].completed)

    def test_task_categorization(self):
        # Test assigning a category (not implemented in codebase)
        self.fail("Task categorization not implemented")

    def test_search_for_specific_tasks(self):
        # Test searching for a task
        self.task_manager.add_task("Searchable Task", "Description", "2023-12-20", "High")
        results = self.task_manager.search_tasks("Searchable")
        self.assertGreater(len(results), 0)
        self.assertIn("Searchable Task", [task.title for task in results])

        # Test searching for a non-existent task
        results = self.task_manager.search_tasks("NonExistent")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
