import unittest
from task import Task
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()
        self.task_manager.load_tasks('tasks.txt')

    def test_create_organize_manage_tasks(self):
        # Test adding a new task
        new_task = Task("New Task", "New Description", "2023-11-01", "High")
        self.task_manager.add_task(new_task)
        self.assertIn(new_task, self.task_manager.tasks)

        # Test updating an existing task
        updated_task = Task("Updated Task", "Updated Description", "2023-11-02", "Medium")
        self.task_manager.update_task(0, updated_task)
        self.assertEqual(self.task_manager.tasks[0].title, "Updated Task")

    def test_set_deadlines_and_assign_priority_levels(self):
        # Test adding a task with deadline and priority
        task_with_deadline = Task("Deadline Task", "Description", "2023-11-03", "Low")
        self.task_manager.add_task(task_with_deadline)
        self.assertIn(task_with_deadline, self.task_manager.tasks)

        # Test changing deadline to a past date (not implemented in codebase)
        self.fail("Changing deadline to a past date is not implemented")

    def test_track_progress_of_tasks(self):
        # Test marking a task as complete
        self.task_manager.mark_task_complete(0)
        self.assertEqual(self.task_manager.tasks[0].status, "Complete")

        # Test marking a task as in progress (not implemented in codebase)
        self.fail("Marking task as 'In Progress' is not implemented")

    def test_task_categorization(self):
        # Test assigning a category to a task (not implemented in codebase)
        self.fail("Task categorization is not implemented")

        # Test filtering tasks by category (not implemented in codebase)
        self.fail("Filtering tasks by category is not implemented")

    def test_search_for_specific_tasks(self):
        # Test searching for a task by keyword
        results = self.task_manager.search_tasks("Task 1")
        self.assertTrue(any("Task 1" in task.title for task in results))

        # Test searching for a non-existent task
        results = self.task_manager.search_tasks("Non-existent Task")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
